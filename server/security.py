"""
Security helpers: password hashing (scrypt), signed session tokens (HMAC),
in-memory rate limiting, anti-spam checks, upload validation, input cleaning.
"""
from __future__ import annotations
import base64, hashlib, hmac, json, os, re, secrets, time
from collections import defaultdict, deque
from typing import Optional
from . import config

# ---------------------------------------------------------------- passwords
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return "scrypt$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, salt_b64, digest_b64 = stored.split("$")
        if algo != "scrypt":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


# ---------------------------------------------------------------- sessions
def _sign(payload: bytes) -> str:
    return hmac.new(config.SECRET_KEY.encode(), payload, hashlib.sha256).hexdigest()


def make_session(user: str) -> str:
    body = json.dumps({"u": user, "exp": int(time.time()) + config.SESSION_HOURS * 3600, "n": secrets.token_hex(8)}).encode()
    b = base64.urlsafe_b64encode(body).decode().rstrip("=")
    return f"{b}.{_sign(body)}"


def read_session(token: Optional[str]) -> Optional[str]:
    if not token or "." not in token:
        return None
    b, sig = token.rsplit(".", 1)
    try:
        body = base64.urlsafe_b64decode(b + "=" * (-len(b) % 4))
    except Exception:
        return None
    if not hmac.compare_digest(_sign(body), sig):
        return None
    try:
        data = json.loads(body)
    except Exception:
        return None
    if data.get("exp", 0) < time.time():
        return None
    return data.get("u")


# ---------------------------------------------------------------- rate limiting
class RateLimiter:
    """Sliding-window limiter keyed by (bucket, client). In-memory: fine for a single process."""
    def __init__(self):
        self._hits: dict[tuple[str, str], deque] = defaultdict(deque)

    def check(self, bucket: str, client: str, limit: int, window: int) -> bool:
        now = time.time()
        q = self._hits[(bucket, client)]
        while q and q[0] < now - window:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True


limiter = RateLimiter()


def client_key(ip: str) -> str:
    """We never store raw IPs; a keyed hash is enough for rate limiting and abuse review."""
    return hashlib.sha256((config.SECRET_KEY + "|" + ip).encode()).hexdigest()[:24]


# ---------------------------------------------------------------- anti-spam
def spam_check(honeypot: str, started_at: str) -> Optional[str]:
    """Returns a reason string if the submission looks automated, else None."""
    if honeypot.strip():
        return "honeypot"
    try:
        t = int(started_at)
    except (TypeError, ValueError):
        return "no-timer"
    elapsed = time.time() * 1000 - t
    if elapsed < config.MIN_FORM_SECONDS * 1000:
        return "too-fast"
    if elapsed > 6 * 3600 * 1000:
        return "stale"
    return None


# ---------------------------------------------------------------- input cleaning
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
URL_RE = re.compile(r"^(https?://)?[\w.-]+\.[a-z]{2,}([/?#].*)?$", re.I)


def clean(value: Optional[str], max_len: int, required: bool = False, field: str = "") -> str:
    v = _CTRL.sub("", (value or "")).strip()
    if required and not v:
        raise ValueError(f"{field or 'This field'} is required.")
    if len(v) > max_len:
        raise ValueError(f"{field or 'This field'} is too long (max {max_len} characters).")
    return v


def clean_email(value: Optional[str]) -> str:
    v = clean(value, 254, True, "Email").lower()
    if not EMAIL_RE.match(v):
        raise ValueError("Enter a valid email address.")
    return v


def clean_url(value: Optional[str]) -> str:
    v = clean(value, 500)
    if v and not URL_RE.match(v):
        raise ValueError("Enter a valid link (e.g. https://yourwork.com).")
    if v and not v.lower().startswith(("http://", "https://")):
        v = "https://" + v
    return v


# ---------------------------------------------------------------- uploads
_MAGIC = {
    ".pdf": [b"%PDF"],
    ".doc": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"],
    ".docx": [b"PK\x03\x04"],
}


def validate_resume(filename: str, data: bytes) -> str:
    """Validate extension, size and magic bytes. Returns the normalised extension."""
    name = (filename or "").strip()
    ext = os.path.splitext(name)[1].lower()
    if ext not in config.ALLOWED_RESUME_EXT:
        raise ValueError("Resume must be a PDF, DOC or DOCX file.")
    if len(data) == 0:
        raise ValueError("The resume file is empty.")
    if len(data) > config.MAX_UPLOAD_BYTES:
        raise ValueError(f"Resume must be under {config.MAX_UPLOAD_MB} MB.")
    if not any(data.startswith(m) for m in _MAGIC[ext]):
        raise ValueError("That file does not look like a valid " + ext[1:].upper() + " document.")
    return ext


def safe_download_name(first: str, last: str, ext: str) -> str:
    base = re.sub(r"[^A-Za-z0-9_-]+", "-", f"{first}-{last}").strip("-") or "resume"
    return f"{base}{ext}"
