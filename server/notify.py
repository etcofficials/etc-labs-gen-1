"""
Server-side notifications for new submissions: optional Discord webhook and optional SMTP email.
Runs in a background thread so a slow provider can never fail or delay a submission.
Nothing here is ever exposed to the browser; misconfiguration only logs a warning.
"""
from __future__ import annotations
import json, logging, smtplib, threading, urllib.request
from email.message import EmailMessage
from . import config

log = logging.getLogger("etc")


def _discord(title: str, lines: list[str]) -> None:
    if not config.DISCORD_WEBHOOK_URL:
        return
    payload = json.dumps({"content": f"**{title}**\n" + "\n".join(lines)}).encode()
    req = urllib.request.Request(config.DISCORD_WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json", "User-Agent": "ETC-Labs-server"})
    urllib.request.urlopen(req, timeout=8).read()


def _email(title: str, lines: list[str]) -> None:
    if not config.EMAIL_ENABLED:
        return
    msg = EmailMessage()
    msg["Subject"] = f"[ETC Labs] {title}"
    msg["From"] = config.NOTIFY_FROM
    msg["To"] = config.NOTIFY_TO
    msg.set_content("\n".join(lines) + "\n\n— ETC Labs backend")
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=15) as smtp:
        if config.SMTP_TLS:
            smtp.starttls()
        if config.SMTP_USER:
            smtp.login(config.SMTP_USER, config.SMTP_PASS)
        smtp.send_message(msg)


def send(title: str, lines: list[str]) -> None:
    """Fire-and-forget. Never raises into the request handler."""
    def run():
        for name, fn in (("discord", _discord), ("email", _email)):
            try:
                fn(title, lines)
            except Exception as e:  # provider failure must never affect the submission
                log.warning("%s notification failed: %s", name, e.__class__.__name__)
    threading.Thread(target=run, daemon=True).start()


def status() -> dict[str, bool]:
    return {"discord": bool(config.DISCORD_WEBHOOK_URL), "email": config.EMAIL_ENABLED}
