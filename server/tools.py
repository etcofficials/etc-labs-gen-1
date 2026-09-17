"""
ETC Labs — Gen 1 · Tools API: Transfer (temporary file sharing), Voice Rooms (WebRTC signalling),
AI Utilities (server-side model calls), community contributions and the admin system panel.

Mounted from app.py. Everything user-facing is rate-limited per client; nothing here exposes secrets.
"""
from __future__ import annotations
import asyncio, json, logging, os, re, secrets, shutil, sys, time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse

from . import config, db, security

log = logging.getLogger("etc")
router = APIRouter()


def ok(data=None, status: int = 200) -> JSONResponse:
    return JSONResponse({"ok": True, **(data or {})}, status_code=status)


def fail(message: str, status: int = 400, **extra) -> JSONResponse:
    return JSONResponse({"ok": False, "error": message, **extra}, status_code=status)


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "0.0.0.0")


# ================================================================ TRANSFER
_SAFE_NAME = re.compile(r"[^A-Za-z0-9._ ()\-\[\]]+")


def _safe_filename(name: str) -> str:
    base = os.path.basename((name or "").replace("\\", "/")).strip()
    base = _SAFE_NAME.sub("_", base)[:120].strip(". ") or "file"
    return base


def purge_expired_transfers() -> int:
    """Delete files whose time or download allowance is used up. Cheap; called opportunistically."""
    n = 0
    for t in db.transfers_expired(time.time()):
        try:
            (config.TRANSFER_DIR / t["stored_name"]).unlink(missing_ok=True)
        except OSError as e:
            log.warning("transfer purge failed for %s: %s", t["id"], e)
        db.transfer_mark_deleted(t["id"])
        n += 1
    return n


@router.get("/api/transfers/config")
def transfer_config():
    return ok({"max_mb": config.TRANSFER_MAX_MB, "ttls": list(config.TRANSFER_TTL_HOURS.keys()), "max_downloads": config.TRANSFER_MAX_DOWNLOADS})


@router.post("/api/transfers")
async def transfer_create(request: Request, file: UploadFile = File(...), ttl: str = Form("24h")):
    key = security.client_key(client_ip(request))
    if not security.limiter.check("transfer", key, *config.RATE_TRANSFER):
        return fail("Too many uploads from this connection. Please try again in an hour.", 429)
    if ttl not in config.TRANSFER_TTL_HOURS:
        return fail("Choose a valid expiry.", 422)
    purge_expired_transfers()
    stored = secrets.token_hex(16) + ".bin"
    dest = config.TRANSFER_DIR / stored
    size = 0
    try:
        with open(dest, "wb") as out:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > config.TRANSFER_MAX_BYTES:
                    raise ValueError(f"Files must be under {config.TRANSFER_MAX_MB} MB.")
                out.write(chunk)
        if size == 0:
            raise ValueError("That file is empty.")
    except ValueError as e:
        dest.unlink(missing_ok=True)
        return fail(str(e), 422)
    except Exception:
        dest.unlink(missing_ok=True)
        log.exception("transfer write failed")
        return fail("The upload could not be stored. Please try again.", 500)
    owner_token = secrets.token_urlsafe(18)
    expires_at = time.time() + config.TRANSFER_TTL_HOURS[ttl] * 3600
    tid = db.transfer_create({"expires_at": expires_at, "original_name": _safe_filename(file.filename or ""), "stored_name": stored, "size": size,
                              "max_downloads": config.TRANSFER_MAX_DOWNLOADS, "owner_token": owner_token, "client_key": key})
    db.audit("public", "transfer.created", tid)
    log.info("transfer %s created (%d bytes, %s)", tid, size, ttl)
    return ok({"id": tid, "expires_at": expires_at, "size": size, "name": _safe_filename(file.filename or ""), "owner_token": owner_token,
               "link": f"{config.SITE_URL}/transfer.html?t={tid}", "download": f"/api/transfers/{tid}/download"}, 201)


def _transfer_or_error(tid: str):
    if not re.fullmatch(r"tr_[0-9a-f]{16}", tid or ""):
        return None, fail("That transfer link is not valid.", 404)
    t = db.transfer_get(tid)
    if not t or t["deleted"]:
        return None, fail("This transfer does not exist or has been removed.", 404)
    if t["expires_at"] < time.time() or t["downloads"] >= t["max_downloads"]:
        purge_expired_transfers()
        return None, fail("This transfer has expired.", 410, expired=True)
    return t, None


@router.get("/api/transfers/{tid}")
def transfer_info(tid: str):
    t, err = _transfer_or_error(tid)
    if err:
        return err
    return ok({"id": t["id"], "name": t["original_name"], "size": t["size"], "expires_at": t["expires_at"], "downloads": t["downloads"],
               "downloads_left": t["max_downloads"] - t["downloads"], "download": f"/api/transfers/{tid}/download"})


@router.get("/api/transfers/{tid}/download")
def transfer_download(tid: str):
    t, err = _transfer_or_error(tid)
    if err:
        return err
    path = (config.TRANSFER_DIR / Path(t["stored_name"]).name).resolve()
    if config.TRANSFER_DIR.resolve() not in path.parents or not path.exists():
        return fail("The file is no longer available.", 410, expired=True)
    db.transfer_count_download(tid)
    # Always served as an opaque attachment: never rendered inline, so an uploaded HTML/SVG can't run on this origin.
    return FileResponse(path, media_type="application/octet-stream", filename=t["original_name"],
                        headers={"X-Content-Type-Options": "nosniff", "Cache-Control": "no-store"})


@router.delete("/api/transfers/{tid}")
def transfer_delete(tid: str, token: str = ""):
    t = db.transfer_get(tid) if re.fullmatch(r"tr_[0-9a-f]{16}", tid or "") else None
    if not t or t["deleted"]:
        return fail("This transfer does not exist or has been removed.", 404)
    if not token or not secrets.compare_digest(token, t["owner_token"]):
        return fail("Only the person who uploaded this file can delete it.", 403)
    (config.TRANSFER_DIR / Path(t["stored_name"]).name).unlink(missing_ok=True)
    db.transfer_mark_deleted(tid)
    db.audit("public", "transfer.deleted", tid)
    return ok()


# ================================================================ VOICE ROOMS (WebRTC signalling)
ROOM_RE = re.compile(r"^[a-z0-9]{4,12}$")


class Room:
    def __init__(self, code: str):
        self.code = code
        self.peers: dict[str, dict[str, Any]] = {}   # id -> {"ws": WebSocket, "name": str, "muted": bool}

    async def broadcast(self, message: dict, exclude: str | None = None):
        dead = []
        for pid, p in list(self.peers.items()):
            if pid == exclude:
                continue
            try:
                await p["ws"].send_json(message)
            except Exception:
                dead.append(pid)
        for pid in dead:
            self.peers.pop(pid, None)


ROOMS: dict[str, Room] = {}


def _origin_allowed(ws: WebSocket) -> bool:
    origin = ws.headers.get("origin", "")
    if not origin:
        return True  # non-browser clients (tests); browsers always send Origin
    host = ws.headers.get("host", "")
    if origin.split("://", 1)[-1] == host:
        return True
    return origin.rstrip("/") in config.ALLOWED_ORIGINS


@router.get("/api/voice/config")
def voice_config():
    return ok({"ice_servers": config.ICE_SERVERS, "max_peers": config.VOICE_ROOM_MAX, "turn": any("turn:" in u for s in config.ICE_SERVERS for u in s["urls"])})


@router.post("/api/voice/rooms")
def voice_room_create(request: Request):
    key = security.client_key(client_ip(request))
    if not security.limiter.check("voice", key, 30, 3600):
        return fail("Too many rooms created from this connection.", 429)
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    code = "".join(secrets.choice(alphabet) for _ in range(6))
    return ok({"room": code, "link": f"{config.SITE_URL}/voice.html?room={code}"}, 201)


@router.get("/api/voice/rooms/{code}")
def voice_room_info(code: str):
    if not ROOM_RE.match(code):
        return fail("Room codes are 4–12 letters or digits.", 422)
    room = ROOMS.get(code)
    return ok({"room": code, "peers": len(room.peers) if room else 0, "max_peers": config.VOICE_ROOM_MAX})


@router.websocket("/ws/voice/{code}")
async def voice_ws(ws: WebSocket, code: str):
    if not ROOM_RE.match(code) or not _origin_allowed(ws):
        await ws.close(code=4403)
        return
    await ws.accept()
    room = ROOMS.setdefault(code, Room(code))
    if len(room.peers) >= config.VOICE_ROOM_MAX:
        await ws.send_json({"type": "error", "code": "full", "message": f"This room is full ({config.VOICE_ROOM_MAX} people)."})
        await ws.close(code=4409)
        return
    pid = secrets.token_hex(4)
    try:
        first = await asyncio.wait_for(ws.receive_json(), timeout=10)
    except Exception:
        await ws.close(code=4400)
        return
    name = security.clean(str(first.get("name", "")), 24) or "Guest"
    room.peers[pid] = {"ws": ws, "name": name, "muted": False}
    await ws.send_json({"type": "welcome", "id": pid, "room": code, "ice_servers": config.ICE_SERVERS,
                        "peers": [{"id": i, "name": p["name"], "muted": p["muted"]} for i, p in room.peers.items() if i != pid]})
    await room.broadcast({"type": "peer-joined", "id": pid, "name": name}, exclude=pid)
    try:
        while True:
            msg = await ws.receive_json()
            t = msg.get("type")
            if t == "signal" and isinstance(msg.get("to"), str) and msg["to"] in room.peers and isinstance(msg.get("data"), dict):
                try:
                    await room.peers[msg["to"]]["ws"].send_json({"type": "signal", "from": pid, "data": msg["data"]})
                except Exception:
                    pass
            elif t == "mute":
                room.peers[pid]["muted"] = bool(msg.get("muted"))
                await room.broadcast({"type": "peer-mute", "id": pid, "muted": room.peers[pid]["muted"]}, exclude=pid)
            elif t == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        log.info("voice ws closed: %s", e.__class__.__name__)
    finally:
        room.peers.pop(pid, None)
        await room.broadcast({"type": "peer-left", "id": pid})
        if not room.peers:
            ROOMS.pop(code, None)


# ================================================================ AI UTILITIES
AI_TOOLS = {
    "summarize": {"label": "Summarize", "system": "You summarize text for busy creators and small teams. Return a tight summary: 2–4 sentences, then up to 5 bullet points of the most important facts. Plain language, no preamble."},
    "rewrite": {"label": "Rewrite", "system": "You rewrite text while keeping its meaning. Match the requested tone exactly ({option}). Keep names, numbers and links unchanged. Return only the rewritten text, no commentary."},
    "ideas": {"label": "Content ideas", "system": "You generate content ideas for a creator or a small team. Given a topic or channel description, return 8 specific, non-generic ideas as a numbered list; each idea is one line: a working title, then a dash and a one-sentence angle. No preamble."},
    "titles": {"label": "Titles & tags", "system": "You write titles and tags for a video, post or article. Return: 6 title options as a numbered list (each under 70 characters), then a line 'Tags:' followed by 10 comma-separated lowercase tags. No preamble."},
}
AI_TONES = ["clear", "friendly", "professional", "shorter", "more energetic"]


def _ai_configured() -> bool:
    return bool(config.ANTHROPIC_API_KEY) or os.environ.get("ETC_AI_PROVIDER") == "test"


@router.get("/api/ai/status")
def ai_status():
    return ok({"configured": _ai_configured(), "model": config.AI_MODEL if config.ANTHROPIC_API_KEY else ("test-provider" if _ai_configured() else None),
               "tools": {k: v["label"] for k, v in AI_TOOLS.items()}, "tones": AI_TONES, "max_chars": config.AI_MAX_INPUT_CHARS})


def _run_model(system: str, text: str) -> str:
    """Calls the configured provider. Runs in a worker thread (see ai_run)."""
    if os.environ.get("ETC_AI_PROVIDER") == "test" and not config.ANTHROPIC_API_KEY:
        # Deterministic stand-in for automated tests only — never enabled in production by default.
        return "[test provider] " + " ".join(text.split()[:40])
    import anthropic  # imported lazily so the server starts without the SDK installed in minimal setups
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY, max_retries=1, timeout=45.0)
    response = client.messages.create(
        model=config.AI_MODEL, max_tokens=1200, system=system,
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": text}],
    )
    if response.stop_reason == "refusal":
        raise ValueError("The model declined this request.")
    return "".join(b.text for b in response.content if b.type == "text").strip()


@router.post("/api/ai/{tool}")
async def ai_run(tool: str, request: Request):
    if tool not in AI_TOOLS:
        raise HTTPException(404, "Unknown tool.")
    key = security.client_key(client_ip(request))
    if not security.limiter.check("ai", key, *config.RATE_AI):
        return fail("You have used the AI utilities a lot in the last hour. Please try again later.", 429)
    if not _ai_configured():
        return fail("AI utilities are not enabled on this deployment yet (no model key configured on the server).", 503, configured=False)
    try:
        body = await request.json()
    except Exception:
        return fail("Invalid request body.")
    try:
        text = security.clean(str(body.get("text", "")), config.AI_MAX_INPUT_CHARS, True, "Text")
    except ValueError as e:
        return fail(str(e), 422)
    if len(text) < 10:
        return fail("Please paste a little more text (at least 10 characters).", 422)
    option = str(body.get("option", "clear"))
    if tool == "rewrite" and option not in AI_TONES:
        option = "clear"
    system = AI_TOOLS[tool]["system"].replace("{option}", option)
    try:
        output = await asyncio.to_thread(_run_model, system, text)
    except ValueError as e:
        return fail(str(e), 422)
    except Exception as e:
        name = e.__class__.__name__
        log.warning("ai call failed: %s", name)
        if "RateLimit" in name:
            return fail("The AI provider is busy right now. Please try again in a minute.", 503)
        if "Authentication" in name or "PermissionDenied" in name:
            return fail("The AI provider rejected the server's credentials. The administrator needs to check the configuration.", 503)
        return fail("The AI request could not be completed. Please try again.", 502)
    db.audit("public", f"ai.{tool}")
    return ok({"tool": tool, "output": output, "model": config.AI_MODEL if config.ANTHROPIC_API_KEY else "test-provider"})


# ================================================================ COMMUNITY CONTRIBUTIONS (public read)
@router.get("/api/community/contributions")
def community_contributions():
    return JSONResponse({"ok": True, "totals": db.contributions_totals(), "kinds": db.CONTRIBUTION_KINDS}, headers={"Cache-Control": "public, max-age=60"})


# ================================================================ ADMIN extras (auth dependency injected from app.py)
def admin_routes(current_admin):
    r = APIRouter()

    @r.get("/api/admin/contributions")
    def list_contributions(handle: str = "", user: str = Depends(current_admin)):
        return ok({"items": db.contributions_list(handle[:60]), "totals": db.contributions_totals(), "kinds": db.CONTRIBUTION_KINDS})

    @r.post("/api/admin/contributions")
    async def add_contribution(request: Request, user: str = Depends(current_admin)):
        body = await request.json()
        try:
            handle = security.clean(str(body.get("handle", "")), 60, True, "Creator handle")
            if not handle.startswith("@"):
                raise ValueError("Use the creator's handle, starting with @.")
            kind = str(body.get("kind", "other"))
            if kind not in db.CONTRIBUTION_KINDS:
                raise ValueError("Unknown contribution kind.")
            points = int(body.get("points", 0))
            if not 1 <= points <= 100:
                raise ValueError("Points must be between 1 and 100.")
            note = security.clean(str(body.get("note", "")), 300)
        except (ValueError, TypeError) as e:
            return fail(str(e) if str(e) else "Invalid contribution.", 422)
        row = db.contribution_add(handle, kind, points, note, user)
        db.audit(user, f"contribution.added:{kind}:{points}", handle)
        return ok({"item": row}, 201)

    @r.delete("/api/admin/contributions/{cid}")
    def delete_contribution(cid: str, user: str = Depends(current_admin)):
        if not db.contribution_delete(cid):
            raise HTTPException(404, "Not found.")
        db.audit(user, "contribution.deleted", cid)
        return ok()

    @r.get("/api/admin/system")
    def system_info(user: str = Depends(current_admin)):
        """Operational overview. Reports which optional features are configured — never their values."""
        from . import notify
        usage = shutil.disk_usage(config.DATA_DIR)
        db_size = config.DB_PATH.stat().st_size if config.DB_PATH.exists() else 0
        uploads = sum(f.stat().st_size for f in config.UPLOAD_DIR.glob("*") if f.is_file())
        transfers = sum(f.stat().st_size for f in config.TRANSFER_DIR.glob("*") if f.is_file())
        return ok({
            "service": "etc-labs-gen-1", "python": sys.version.split()[0], "started_at": STARTED_AT, "uptime_seconds": round(time.time() - STARTED_AT),
            "data_dir": str(config.DATA_DIR), "data_dir_explicit": config.DATA_DIR_EXPLICIT,
            "persistence_warning": None if config.DATA_DIR_EXPLICIT else "ETC_DATA_DIR is not set: on Render the default data directory is wiped on every deploy. Attach a disk and set ETC_DATA_DIR to its mount path.",
            "disk": {"total": usage.total, "used": usage.used, "free": usage.free}, "db_bytes": db_size, "uploads_bytes": uploads, "transfers_bytes": transfers,
            "transfers": db.transfers_stats(), "voice_rooms": len(ROOMS), "voice_peers": sum(len(r.peers) for r in ROOMS.values()),
            "features": {"ai": _ai_configured(), "ai_model": config.AI_MODEL if config.ANTHROPIC_API_KEY else None, "turn": any("turn:" in u for s in config.ICE_SERVERS for u in s["urls"]),
                         "notifications": notify.status(), "secure_cookies": config.SECURE_COOKIES, "allowed_origins": config.ALLOWED_ORIGINS, "secret_key_from_env": bool(os.environ.get("ETC_SECRET_KEY"))},
            "limits": {"resume_mb": config.MAX_UPLOAD_MB, "transfer_mb": config.TRANSFER_MAX_MB, "rate_submit": config.RATE_SUBMIT, "rate_login": config.RATE_LOGIN, "rate_ai": config.RATE_AI, "rate_transfer": config.RATE_TRANSFER},
        })

    @r.get("/api/admin/export/{kind}.csv")
    def export_csv(kind: str, user: str = Depends(current_admin)):
        import csv, io
        k = {"applications": "application", "requests": "request"}.get(kind)
        if not k:
            raise HTTPException(404, "Unknown collection.")
        items = db.list_items(k, limit=5000) + db.list_items(k, archived=True, limit=5000)
        drop = {"client_key", "user_agent", "resume_path", "note_count"}
        cols = [c for c in (items[0].keys() if items else []) if c not in drop]
        buf = io.StringIO(); w = csv.writer(buf); w.writerow(cols)
        for it in items:
            w.writerow([("'" + str(it[c])) if isinstance(it[c], str) and it[c][:1] in "=+-@" else it[c] for c in cols])  # neutralise spreadsheet formulas
        db.audit(user, f"{k}.exported")
        return PlainTextResponse(buf.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="etc-{kind}.csv"', "Cache-Control": "no-store"})

    return r


STARTED_AT = time.time()
