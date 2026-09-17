"""
ETC Labs — Gen 1 · application server.

  uvicorn server.app:app --reload          (development)
  uvicorn server.app:app --host 0.0.0.0    (production, behind a TLS proxy)

Serves the public site (/), the admin app (/admin/) and the JSON API (/api/...).
When the public site is hosted elsewhere (GitHub Pages), only /api/* and /admin/ are used
and ETC_ALLOWED_ORIGINS must include the frontend origin.
"""
from __future__ import annotations
import json, logging, secrets, time, urllib.request
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from . import config, db, notify, security, tools

# ---------------------------------------------------------------- logging
log = logging.getLogger("etc")
log.setLevel(logging.INFO)
_handler = RotatingFileHandler(config.LOG_DIR / "server.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(_handler)
log.addHandler(logging.StreamHandler())

app = FastAPI(title="ETC Labs — Gen 1", docs_url=None, redoc_url=None, openapi_url=None)
db.init()


# ---------------------------------------------------------------- security headers
class SecurityHeaders(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp: Response = await call_next(request)
        path = request.url.path
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(self), geolocation=()")
        if path.startswith("/admin") or path.startswith("/api"):
            resp.headers.setdefault("X-Frame-Options", "DENY")
            resp.headers.setdefault("Cache-Control", "no-store")
        if path.startswith("/admin"):
            resp.headers.setdefault("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        elif not path.startswith("/api"):
            resp.headers.setdefault("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; connect-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'")
        return resp


app.add_middleware(SecurityHeaders)

# CORS: only the public submission endpoints are called cross-origin (from the GitHub Pages frontend).
# Admin routes stay same-origin (cookie session + custom header), so they are not exposed via CORS.
if config.ALLOWED_ORIGINS:
    class PublicApiCORS(CORSMiddleware):
        async def __call__(self, scope, receive, send):
            if scope["type"] == "http" and (scope["path"] in ("/api/project-requests", "/api/applications", "/api/health", "/api/community/contributions")
                                             or scope["path"].startswith(("/api/transfers", "/api/voice", "/api/ai"))):
                return await super().__call__(scope, receive, send)
            return await self.app(scope, receive, send)
    app.add_middleware(PublicApiCORS, allow_origins=config.ALLOWED_ORIGINS, allow_methods=["POST", "GET", "DELETE", "OPTIONS"], allow_headers=["Content-Type"], allow_credentials=False, max_age=600)


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    return (fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "0.0.0.0"))


def ok(data=None, status: int = 200) -> JSONResponse:
    return JSONResponse({"ok": True, **(data or {})}, status_code=status)


def fail(message: str, status: int = 400, field: str | None = None) -> JSONResponse:
    body = {"ok": False, "error": message}
    if field:
        body["field"] = field
    return JSONResponse(body, status_code=status)


# ================================================================ PUBLIC API
@app.get("/api/health")
def health():
    return {"ok": True, "service": "etc-labs-gen-1", "admin_configured": bool(config.ADMIN_PASSWORD_HASH), "time": time.time(),
            "features": {"transfer": True, "voice": True, "ai": tools._ai_configured(), "notifications": notify.status()}}


@app.post("/api/project-requests")
async def create_project_request(request: Request):
    key = security.client_key(client_ip(request))
    if not security.limiter.check("submit", key, *config.RATE_SUBMIT):
        return fail("Too many submissions from this connection. Please try again in a few minutes.", 429)
    try:
        body = await request.json()
    except Exception:
        return fail("Invalid request body.")
    if not isinstance(body, dict):
        return fail("Invalid request body.")
    if reason := security.spam_check(str(body.get("website", "")), str(body.get("started_at", ""))):
        log.info("request rejected as spam (%s) from %s", reason, key)
        # Respond as if accepted so bots learn nothing; nothing is stored.
        return ok({"id": "req_" + secrets.token_hex(6), "stored": False})
    try:
        data = {
            "name": security.clean(body.get("name"), 120, True, "Name"),
            "email": security.clean_email(body.get("email")),
            "discord": security.clean(body.get("discord"), 80),
            "building": security.clean(body.get("building"), 200, True, "What you are building"),
            "need": security.clean(body.get("need"), 40, True, "What you need"),
            "scale": security.clean(body.get("scale"), 40),
            "timeline": security.clean(body.get("timeline"), 40),
            "message": security.clean(body.get("message"), 4000, True, "Message"),
        }
        if len(data["message"]) < 20:
            raise ValueError("Please add a little more detail to your message (at least 20 characters).")
    except ValueError as e:
        return fail(str(e), 422)
    if dup := db.recent_duplicate("request", data["email"], "building", data["building"], 3600):
        return fail(f"We already have this request from you (reference {dup}). If you want to add details, email us and quote the reference.", 409)
    data["client_key"] = key
    data["user_agent"] = security.clean(request.headers.get("user-agent"), 300)
    rid = db.insert("request", data)
    db.audit("public", "request.created", rid)
    log.info("project request %s created", rid)
    notify.send("New project request", [f"{data['name']} <{data['email']}>", f"Building: {data['building']}", f"Need: {data['need']} · Scale: {data['scale'] or '—'}", f"Open: /admin/#/requests/{rid}"])
    return ok({"id": rid, "stored": True}, 201)


@app.post("/api/applications")
async def create_application(
    request: Request,
    firstName: str = Form(""), lastName: str = Form(""), email: str = Form(""), discord: str = Form(""),
    position: str = Form(""), portfolio: str = Form(""), cover: str = Form(""),
    website: str = Form(""), started_at: str = Form(""),
    resume: Optional[UploadFile] = File(None),
):
    key = security.client_key(client_ip(request))
    if not security.limiter.check("submit", key, *config.RATE_SUBMIT):
        return fail("Too many submissions from this connection. Please try again in a few minutes.", 429)
    if reason := security.spam_check(website, started_at):
        log.info("application rejected as spam (%s) from %s", reason, key)
        return ok({"id": "app_" + secrets.token_hex(6), "stored": False})
    try:
        data = {
            "first_name": security.clean(firstName, 80, True, "First name"),
            "last_name": security.clean(lastName, 80, True, "Last name"),
            "email": security.clean_email(email),
            "discord": security.clean(discord, 80, True, "Discord username"),
            "position": security.clean(position, 40, True, "Position"),
            "portfolio": security.clean_url(portfolio),
            "cover_letter": security.clean(cover, 1000),
        }
    except ValueError as e:
        return fail(str(e), 422)
    if dup := db.recent_duplicate("application", data["email"], "position", data["position"], 24 * 3600):
        return fail(f"You already applied for this role in the last 24 hours (reference {dup}). We have it — no need to send it again.", 409)

    resume_path = resume_name = ""
    resume_size = 0
    if resume is not None and resume.filename:
        raw = await resume.read(config.MAX_UPLOAD_BYTES + 1)
        try:
            ext = security.validate_resume(resume.filename, raw)
        except ValueError as e:
            return fail(str(e), 422, "resume")
        stored = f"{secrets.token_hex(16)}{ext}"       # random name, never the user's filename
        (config.UPLOAD_DIR / stored).write_bytes(raw)
        resume_path, resume_name, resume_size = stored, security.clean(resume.filename, 200), len(raw)

    data.update({"resume_path": resume_path, "resume_name": resume_name, "resume_size": resume_size,
                 "client_key": key, "user_agent": security.clean(request.headers.get("user-agent"), 300)})
    aid = db.insert("application", data)
    db.audit("public", "application.created", aid)
    log.info("application %s created for %s", aid, data["position"])
    notify.send("New application", [f"{data['first_name']} {data['last_name']} · {data['position']}", f"{data['email']} · Discord: {data['discord']}", f"Resume: {'yes' if resume_path else 'no'}", f"Open: /admin/#/applications/{aid}"])
    return ok({"id": aid, "stored": True}, 201)


# ================================================================ ADMIN AUTH
COOKIE = "etc_admin"


def current_admin(request: Request) -> str:
    user = security.read_session(request.cookies.get(COOKIE))
    if not user:
        raise HTTPException(401, "Not signed in.")
    # Custom header requirement blocks cross-site form posts (defence in depth next to SameSite=Strict)
    if request.method not in ("GET", "HEAD") and request.headers.get("x-etc-admin") != "1":
        raise HTTPException(403, "Missing admin header.")
    key = security.client_key(client_ip(request))
    if not security.limiter.check("admin", key, *config.RATE_ADMIN):
        raise HTTPException(429, "Slow down.")
    return user


@app.post("/api/admin/login")
async def admin_login(request: Request, response: Response):
    key = security.client_key(client_ip(request))
    if not security.limiter.check("login", key, *config.RATE_LOGIN):
        return fail("Too many login attempts. Wait 15 minutes and try again.", 429)
    if not config.ADMIN_PASSWORD_HASH:
        return fail("Admin access is not configured yet. Run: python -m server.cli set-admin-password", 503)
    try:
        body = await request.json()
    except Exception:
        return fail("Invalid request.")
    user = str(body.get("username", "")).strip()
    password = str(body.get("password", ""))
    if user != config.ADMIN_USER or not security.verify_password(password, config.ADMIN_PASSWORD_HASH):
        time.sleep(0.4)  # slow brute force a little
        db.audit(user or "?", "login.failed")
        return fail("Wrong username or password.", 401)
    token = security.make_session(user)
    resp = ok({"user": user})
    resp.set_cookie(COOKIE, token, max_age=config.SESSION_HOURS * 3600, httponly=True, samesite="strict", secure=config.SECURE_COOKIES, path="/")
    db.audit(user, "login.ok")
    return resp


@app.post("/api/admin/logout")
def admin_logout(request: Request):
    user = security.read_session(request.cookies.get(COOKIE))
    if user:
        db.audit(user, "logout")
    resp = ok()
    resp.delete_cookie(COOKIE, path="/")
    return resp


@app.get("/api/admin/account")
def admin_account(user: str = Depends(current_admin)):
    """Who is logged in + login activity. Never returns hashes, secrets or session tokens."""
    return ok({"user": user, "account": config.ADMIN_USER, "configured": bool(config.ADMIN_PASSWORD_HASH), "session_hours": config.SESSION_HOURS,
               "public_accounts": False, "login": db.login_info()})


@app.get("/api/admin/me")
def admin_me(user: str = Depends(current_admin)):
    return ok({"user": user})


# ================================================================ TOOLS (transfer · voice · ai · community) + admin extras
# Registered before the generic /api/admin/{kind} routes so /api/admin/system, /contributions and /export/* resolve first.
app.include_router(tools.router)
app.include_router(tools.admin_routes(current_admin))


# ================================================================ ADMIN DATA
@app.get("/api/admin/summary")
def admin_summary(user: str = Depends(current_admin)):
    return ok({"summary": db.summary(), "activity": db.recent_activity(12), "statuses": {"application": db.APPLICATION_STATUSES, "request": db.REQUEST_STATUSES}})


def _kind(kind: str) -> str:
    k = {"applications": "application", "requests": "request"}.get(kind)
    if not k:
        raise HTTPException(404, "Unknown collection.")
    return k


@app.get("/api/admin/{kind}")
def admin_list(kind: str, status: str = "", q: str = "", position: str = "", need: str = "", archived: int = 0,
               date_from: float | None = None, date_to: float | None = None, user: str = Depends(current_admin)):
    k = _kind(kind)
    items = db.list_items(k, status=status, q=q[:80], position=position, need=need, archived=bool(archived), date_from=date_from, date_to=date_to)
    return ok({"items": items})


@app.get("/api/admin/{kind}/{item_id}")
def admin_get(kind: str, item_id: str, user: str = Depends(current_admin)):
    item = db.get(_kind(kind), item_id)
    if not item:
        raise HTTPException(404, "Not found.")
    item.pop("client_key", None)
    return ok({"item": item})


@app.patch("/api/admin/{kind}/{item_id}")
async def admin_update(kind: str, item_id: str, request: Request, user: str = Depends(current_admin)):
    k = _kind(kind)
    body = await request.json()
    try:
        changed = db.update(k, item_id, {key: body[key] for key in ("status", "archived") if key in body})
    except ValueError as e:
        return fail(str(e), 422)
    if not changed:
        raise HTTPException(404, "Nothing updated.")
    db.audit(user, f"{k}.updated:{','.join(f'{a}={body[a]}' for a in ('status','archived') if a in body)}", item_id)
    return ok({"item": db.get(k, item_id)})


@app.post("/api/admin/{kind}/{item_id}/notes")
async def admin_add_note(kind: str, item_id: str, request: Request, user: str = Depends(current_admin)):
    k = _kind(kind)
    if not db.get(k, item_id):
        raise HTTPException(404, "Not found.")
    body = await request.json()
    text = security.clean(body.get("body"), 2000)
    if not text:
        return fail("Note is empty.", 422)
    note = db.add_note(k, item_id, user, text)
    db.audit(user, f"{k}.note", item_id)
    return ok({"note": note}, 201)


@app.delete("/api/admin/notes/{note_id}")
def admin_delete_note(note_id: str, user: str = Depends(current_admin)):
    if not db.delete_note(note_id):
        raise HTTPException(404, "Not found.")
    return ok()


@app.get("/api/admin/applications/{item_id}/resume")
def admin_resume(item_id: str, user: str = Depends(current_admin)):
    item = db.get("application", item_id)
    if not item or not item.get("resume_path"):
        raise HTTPException(404, "No resume on this application.")
    path = (config.UPLOAD_DIR / Path(item["resume_path"]).name).resolve()
    if config.UPLOAD_DIR not in path.parents or not path.exists():
        raise HTTPException(404, "File missing.")
    db.audit(user, "application.resume_download", item_id)
    ext = path.suffix
    media = {".pdf": "application/pdf", ".doc": "application/msword", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}[ext]
    return FileResponse(path, media_type=media, filename=security.safe_download_name(item["first_name"], item["last_name"], ext), headers={"X-Content-Type-Options": "nosniff", "Content-Disposition-Type": "attachment"})


# ================================================================ STATIC
@app.get("/admin")
@app.get("/admin/")
def admin_index():
    return FileResponse(config.ADMIN_DIR / "index.html", headers={"Cache-Control": "no-store"})


app.mount("/admin", StaticFiles(directory=config.ADMIN_DIR), name="admin")
app.mount("/", StaticFiles(directory=config.PUBLIC_DIR, html=True), name="public")

