"""
Admin tasks:
  python -m server.cli set-admin-password        # prompts, prints the line to put in .env
  python -m server.cli seed-demo                 # inserts clearly-labelled demo rows
  python -m server.cli purge-demo                # removes them
  python -m server.cli stats
"""
from __future__ import annotations
import getpass, sys, time
from . import db, security


def set_admin_password(argv):
    pw = argv[0] if argv else getpass.getpass("New admin password: ")
    if len(pw) < 10:
        print("Use at least 10 characters."); sys.exit(1)
    print("\nAdd this line to .env (and restart the server):\n")
    print("ETC_ADMIN_PASSWORD_HASH=" + security.hash_password(pw))
    print("\nOptionally set ETC_ADMIN_USER=<name> (default: admin).")


DEMO_APPS = [
    ("Demo", "Applicant", "demo.applicant@example.com", "demo_user", "web-dev", "https://example.com", "DEMO DATA — This row was created by `seed-demo` to show the dashboard. It is not a real application.", "new"),
    ("Demo", "Editor", "demo.editor@example.com", "demo_editor", "video-editor", "", "DEMO DATA — sample cover letter for a video editor application.", "reviewing"),
    ("Demo", "Moderator", "demo.mod@example.com", "demo_mod", "community-mod", "", "DEMO DATA — sample application.", "shortlisted"),
]
DEMO_REQS = [
    ("Demo Client", "demo.client@example.com", "", "A booking site for a small studio", "software", "medium", "1-3 months", "DEMO DATA — sample project request created by `seed-demo`. Not a real client.", "new"),
    ("Demo Founder", "demo.founder@example.com", "demo_founder", "An AI assistant for support tickets", "ai", "large", "flexible", "DEMO DATA — sample project request.", "reviewing"),
]


def seed_demo(argv):
    db.init()
    n = 0
    for i, (f, l, e, d, pos, url, cover, status) in enumerate(DEMO_APPS):
        db.insert("application", {"first_name": f, "last_name": l, "email": e, "discord": d, "position": pos, "portfolio": url, "cover_letter": cover, "status": status, "is_demo": 1, "created_at": time.time() - i * 86400 * 1.5}); n += 1
    for i, (name, e, d, b, need, scale, tl, msg, status) in enumerate(DEMO_REQS):
        db.insert("request", {"name": name, "email": e, "discord": d, "building": b, "need": need, "scale": scale, "timeline": tl, "message": msg, "status": status, "is_demo": 1, "created_at": time.time() - i * 86400 * 2}); n += 1
    db.audit("cli", "seed-demo", str(n))
    print(f"Inserted {n} demo rows (flagged is_demo=1, labelled DEMO in the dashboard). Remove with: python -m server.cli purge-demo")


def purge_demo(argv):
    db.init()
    print(f"Removed {db.purge_demo()} demo rows.")


def stats(argv):
    db.init()
    s = db.summary()
    print(f"Applications: {s['applications_total']} ({s['applications_week']} this week) {s['applications']}")
    print(f"Project requests: {s['requests_total']} ({s['requests_week']} this week) {s['requests']}")
    print(f"Demo rows: {s['demo_rows']}")


COMMANDS = {"set-admin-password": set_admin_password, "seed-demo": seed_demo, "purge-demo": purge_demo, "stats": stats}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd not in COMMANDS:
        print(__doc__); sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
