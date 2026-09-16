"""
SQLite storage for applications, project requests, notes and an audit log.
Single-file database in data/, WAL mode, created on first run.
"""
from __future__ import annotations
import sqlite3, secrets, time
from contextlib import contextmanager
from typing import Any, Iterable, Optional
from . import config

APPLICATION_STATUSES = ["new", "reviewing", "shortlisted", "interview", "rejected", "hired"]
REQUEST_STATUSES = ["new", "reviewing", "replied", "scoping", "won", "closed"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
  id TEXT PRIMARY KEY,
  created_at REAL NOT NULL,
  updated_at REAL NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  discord TEXT NOT NULL,
  position TEXT NOT NULL,
  portfolio TEXT DEFAULT '',
  cover_letter TEXT DEFAULT '',
  resume_path TEXT DEFAULT '',
  resume_name TEXT DEFAULT '',
  resume_size INTEGER DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'new',
  archived INTEGER NOT NULL DEFAULT 0,
  is_demo INTEGER NOT NULL DEFAULT 0,
  client_key TEXT DEFAULT '',
  user_agent TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS project_requests (
  id TEXT PRIMARY KEY,
  created_at REAL NOT NULL,
  updated_at REAL NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  discord TEXT DEFAULT '',
  building TEXT NOT NULL,
  need TEXT NOT NULL,
  scale TEXT DEFAULT '',
  timeline TEXT DEFAULT '',
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',
  archived INTEGER NOT NULL DEFAULT 0,
  is_demo INTEGER NOT NULL DEFAULT 0,
  client_key TEXT DEFAULT '',
  user_agent TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS notes (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,            -- 'application' | 'request'
  target_id TEXT NOT NULL,
  created_at REAL NOT NULL,
  author TEXT NOT NULL,
  body TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS notes_target ON notes(kind, target_id);
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at REAL NOT NULL,
  actor TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT DEFAULT ''
);
"""


def new_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(6)}"


@contextmanager
def connect():
    con = sqlite3.connect(config.DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init() -> None:
    with connect() as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.executescript(SCHEMA)


def row_to_dict(row: sqlite3.Row | None) -> Optional[dict[str, Any]]:
    return dict(row) if row is not None else None


# ---------------------------------------------------------------- generic helpers
TABLES = {"application": "applications", "request": "project_requests"}
STATUSES = {"application": APPLICATION_STATUSES, "request": REQUEST_STATUSES}


def insert(kind: str, data: dict[str, Any]) -> str:
    table = TABLES[kind]
    data = dict(data)
    data.setdefault("id", new_id("app" if kind == "application" else "req"))
    now = time.time()
    data.setdefault("created_at", now)
    data["updated_at"] = now
    cols = ", ".join(data.keys())
    marks = ", ".join("?" for _ in data)
    with connect() as con:
        con.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", list(data.values()))
    return data["id"]


def get(kind: str, item_id: str) -> Optional[dict[str, Any]]:
    with connect() as con:
        row = con.execute(f"SELECT * FROM {TABLES[kind]} WHERE id = ?", (item_id,)).fetchone()
        item = row_to_dict(row)
        if item:
            item["notes"] = [dict(n) for n in con.execute(
                "SELECT id, created_at, author, body FROM notes WHERE kind = ? AND target_id = ? ORDER BY created_at DESC",
                (kind, item_id)).fetchall()]
        return item


def list_items(kind: str, *, status: str = "", q: str = "", position: str = "", need: str = "",
               archived: bool = False, date_from: float | None = None, date_to: float | None = None,
               limit: int = 200) -> list[dict[str, Any]]:
    table = TABLES[kind]
    where, params = ["archived = ?"], [1 if archived else 0]
    if status:
        where.append("status = ?"); params.append(status)
    if kind == "application" and position:
        where.append("position = ?"); params.append(position)
    if kind == "request" and need:
        where.append("need = ?"); params.append(need)
    if date_from is not None:
        where.append("created_at >= ?"); params.append(date_from)
    if date_to is not None:
        where.append("created_at <= ?"); params.append(date_to)
    if q:
        like = f"%{q.lower()}%"
        if kind == "application":
            where.append("(lower(first_name || ' ' || last_name) LIKE ? OR lower(email) LIKE ? OR lower(discord) LIKE ?)")
        else:
            where.append("(lower(name) LIKE ? OR lower(email) LIKE ? OR lower(discord) LIKE ?)")
        params += [like, like, like]
    sql = f"SELECT * FROM {table} WHERE {' AND '.join(where)} ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with connect() as con:
        rows = con.execute(sql, params).fetchall()
        items = [dict(r) for r in rows]
        if items:
            ids = [i["id"] for i in items]
            counts = con.execute(
                f"SELECT target_id, COUNT(*) c FROM notes WHERE kind = ? AND target_id IN ({','.join('?' * len(ids))}) GROUP BY target_id",
                [kind, *ids]).fetchall()
            cmap = {r["target_id"]: r["c"] for r in counts}
            for i in items:
                i["note_count"] = cmap.get(i["id"], 0)
                i.pop("cover_letter", None); i.pop("message", None)
        return items


def update(kind: str, item_id: str, fields: dict[str, Any]) -> bool:
    allowed = {"status", "archived"}
    fields = {k: v for k, v in fields.items() if k in allowed}
    if not fields:
        return False
    if "status" in fields and fields["status"] not in STATUSES[kind]:
        raise ValueError("Unknown status.")
    fields["updated_at"] = time.time()
    sets = ", ".join(f"{k} = ?" for k in fields)
    with connect() as con:
        cur = con.execute(f"UPDATE {TABLES[kind]} SET {sets} WHERE id = ?", [*fields.values(), item_id])
        return cur.rowcount > 0


def add_note(kind: str, item_id: str, author: str, body: str) -> dict[str, Any]:
    note = {"id": new_id("note"), "kind": kind, "target_id": item_id, "created_at": time.time(), "author": author, "body": body}
    with connect() as con:
        con.execute("INSERT INTO notes (id, kind, target_id, created_at, author, body) VALUES (?, ?, ?, ?, ?, ?)", list(note.values()))
        con.execute(f"UPDATE {TABLES[kind]} SET updated_at = ? WHERE id = ?", (time.time(), item_id))
    return note


def delete_note(note_id: str) -> bool:
    with connect() as con:
        return con.execute("DELETE FROM notes WHERE id = ?", (note_id,)).rowcount > 0


def summary() -> dict[str, Any]:
    with connect() as con:
        def count(table: str, where: str = "1=1", params: Iterable[Any] = ()) -> int:
            return con.execute(f"SELECT COUNT(*) FROM {table} WHERE archived = 0 AND {where}", tuple(params)).fetchone()[0]
        week_ago = time.time() - 7 * 86400
        return {
            "applications": {s: count("applications", "status = ?", (s,)) for s in APPLICATION_STATUSES},
            "requests": {s: count("project_requests", "status = ?", (s,)) for s in REQUEST_STATUSES},
            "applications_total": count("applications"),
            "requests_total": count("project_requests"),
            "applications_week": count("applications", "created_at >= ?", (week_ago,)),
            "requests_week": count("project_requests", "created_at >= ?", (week_ago,)),
            "demo_rows": con.execute("SELECT (SELECT COUNT(*) FROM applications WHERE is_demo = 1) + (SELECT COUNT(*) FROM project_requests WHERE is_demo = 1)").fetchone()[0],
        }


def audit(actor: str, action: str, target: str = "") -> None:
    with connect() as con:
        con.execute("INSERT INTO audit_log (created_at, actor, action, target) VALUES (?, ?, ?, ?)", (time.time(), actor, action, target))


def recent_activity(limit: int = 20) -> list[dict[str, Any]]:
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT created_at, actor, action, target FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def login_info() -> dict[str, Any]:
    """Admin-account activity from the audit log (no secrets, no tokens). Public users have no accounts."""
    with connect() as con:
        last_ok = con.execute("SELECT created_at, actor FROM audit_log WHERE action = 'login.ok' ORDER BY id DESC LIMIT 1").fetchone()
        last_fail = con.execute("SELECT created_at FROM audit_log WHERE action = 'login.failed' ORDER BY id DESC LIMIT 1").fetchone()
        day_ago = time.time() - 86400
        failed_24h = con.execute("SELECT COUNT(*) FROM audit_log WHERE action = 'login.failed' AND created_at >= ?", (day_ago,)).fetchone()[0]
        logins_total = con.execute("SELECT COUNT(*) FROM audit_log WHERE action = 'login.ok'").fetchone()[0]
        recent = [dict(r) for r in con.execute("SELECT created_at, actor, action FROM audit_log WHERE action IN ('login.ok','login.failed','logout') ORDER BY id DESC LIMIT 15").fetchall()]
        return {"last_login": last_ok["created_at"] if last_ok else None, "last_login_user": last_ok["actor"] if last_ok else None,
                "last_failed": last_fail["created_at"] if last_fail else None, "failed_24h": failed_24h, "logins_total": logins_total, "recent": recent}


def purge_demo() -> int:
    with connect() as con:
        a = con.execute("DELETE FROM applications WHERE is_demo = 1").rowcount
        b = con.execute("DELETE FROM project_requests WHERE is_demo = 1").rowcount
        con.execute("DELETE FROM notes WHERE target_id NOT IN (SELECT id FROM applications) AND target_id NOT IN (SELECT id FROM project_requests)")
        return a + b
