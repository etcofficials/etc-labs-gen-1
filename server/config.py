"""
ETC Labs — Gen 1 server configuration.

Values come from environment variables, optionally loaded from a `.env` file
in the project root (see `.env.example`). Nothing here is ever sent to the browser.
"""
from __future__ import annotations
import os, secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv(ROOT / ".env")

DATA_DIR = Path(os.environ.get("ETC_DATA_DIR", ROOT / "data")).resolve()
UPLOAD_DIR = DATA_DIR / "uploads"
LOG_DIR = DATA_DIR / "logs"
DB_PATH = DATA_DIR / "etc-labs.sqlite3"
for d in (DATA_DIR, UPLOAD_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)


def _secret_key() -> str:
    """Use ETC_SECRET_KEY if set; otherwise generate one once and keep it in data/ (dev convenience)."""
    env = os.environ.get("ETC_SECRET_KEY")
    if env and len(env) >= 32:
        return env
    f = DATA_DIR / ".secret_key"
    if f.exists():
        return f.read_text(encoding="utf-8").strip()
    key = secrets.token_urlsafe(48)
    f.write_text(key, encoding="utf-8")
    try:
        os.chmod(f, 0o600)
    except OSError:
        pass
    return key


SECRET_KEY = _secret_key()

# Admin credentials: set with `python -m server.cli set-admin-password`
ADMIN_USER = os.environ.get("ETC_ADMIN_USER", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ETC_ADMIN_PASSWORD_HASH", "")

# Optional server-side notifications (never exposed to the browser)
DISCORD_WEBHOOK_URL = os.environ.get("ETC_DISCORD_WEBHOOK_URL", "").strip()

# Frontend origins allowed to call the public submission API cross-origin (comma-separated).
# Defaults to the GitHub Pages origin of this project; override with ETC_ALLOWED_ORIGINS (set to "-" to disable).
ALLOWED_ORIGINS = [o.strip().rstrip("/") for o in os.environ.get("ETC_ALLOWED_ORIGINS", "https://etcofficials.github.io").split(",") if o.strip()]

# Cookies: mark Secure when served over HTTPS in production
SECURE_COOKIES = os.environ.get("ETC_SECURE_COOKIES", "0") == "1"
SESSION_HOURS = int(os.environ.get("ETC_SESSION_HOURS", "12"))

# Uploads
MAX_UPLOAD_MB = int(os.environ.get("ETC_MAX_UPLOAD_MB", "5"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
ALLOWED_RESUME_EXT = {".pdf", ".doc", ".docx"}

# Rate limits (requests per window per client)
RATE_SUBMIT = (8, 600)     # 8 submissions / 10 min (room for a corrected resend; still blocks floods)
RATE_LOGIN = (6, 900)      # 6 login attempts / 15 min
RATE_ADMIN = (240, 60)     # 240 admin API calls / min

# Minimum seconds between form render and submit (bots submit instantly)
MIN_FORM_SECONDS = 3

# ---------------------------------------------------------------- tools (Gen 1 completion)
SITE_URL = os.environ.get("ETC_SITE_URL", "https://etcofficials.github.io/etc-labs-gen-1").rstrip("/")

# Transfer: temporary file sharing. Files live under DATA_DIR/transfers and are deleted when they expire.
TRANSFER_DIR = DATA_DIR / "transfers"
TRANSFER_DIR.mkdir(parents=True, exist_ok=True)
TRANSFER_MAX_MB = int(os.environ.get("ETC_TRANSFER_MAX_MB", "25"))
TRANSFER_MAX_BYTES = TRANSFER_MAX_MB * 1024 * 1024
TRANSFER_TTL_HOURS = {"24h": 24, "3d": 72, "7d": 168}
TRANSFER_MAX_DOWNLOADS = 100
RATE_TRANSFER = (10, 3600)   # 10 uploads / hour per client

# Voice rooms: WebRTC peer-to-peer audio, signalled over a WebSocket on this server.
# STUN is enough on most networks; set a TURN server for strict NATs (TURN credentials are handed to clients by design - use short-lived ones).
ICE_SERVERS = [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]
if os.environ.get("ETC_TURN_URL"):
    ICE_SERVERS.append({"urls": [os.environ["ETC_TURN_URL"]], "username": os.environ.get("ETC_TURN_USER", ""), "credential": os.environ.get("ETC_TURN_PASS", "")})
VOICE_ROOM_MAX = 6

# AI utilities: server-side only; the key never reaches the browser.
ANTHROPIC_API_KEY = os.environ.get("ETC_ANTHROPIC_API_KEY", "").strip()
AI_MODEL = os.environ.get("ETC_AI_MODEL", "claude-opus-5")
AI_MAX_INPUT_CHARS = 6000
RATE_AI = (20, 3600)         # 20 AI requests / hour per client

# Email notifications (optional, server-side). Leave empty to disable.
SMTP_HOST = os.environ.get("ETC_SMTP_HOST", "").strip()
SMTP_PORT = int(os.environ.get("ETC_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("ETC_SMTP_USER", "")
SMTP_PASS = os.environ.get("ETC_SMTP_PASS", "")
SMTP_TLS = os.environ.get("ETC_SMTP_TLS", "1") == "1"
NOTIFY_FROM = os.environ.get("ETC_NOTIFY_FROM", SMTP_USER)
NOTIFY_TO = os.environ.get("ETC_NOTIFY_TO", "").strip()
EMAIL_ENABLED = bool(SMTP_HOST and NOTIFY_TO and NOTIFY_FROM)

# Data persistence hint: on Render the default ./data inside the container is wiped on every deploy.
DATA_DIR_EXPLICIT = bool(os.environ.get("ETC_DATA_DIR"))

PUBLIC_DIR = ROOT / "public"
ADMIN_DIR = ROOT / "admin"
