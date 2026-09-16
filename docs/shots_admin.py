"""Admin screenshots on DEMO data. Run: python -m server.cli seed-demo && python docs/shots_admin.py"""
from playwright.sync_api import sync_playwright
import sys
B = "http://localhost:8790"; PW = sys.argv[1] if len(sys.argv) > 1 else "local-dev-password-1"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(B + "/admin/", wait_until="load"); pg.wait_for_timeout(400); pg.screenshot(path="docs/screenshots/admin-login.png")
    pg.fill("#u", "admin"); pg.fill("#p", PW); pg.click("button[type=submit]"); pg.wait_for_timeout(1500); pg.screenshot(path="docs/screenshots/admin-dashboard.png")
    pg.goto(B + "/admin/#/applications"); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-applications.png")
    first = pg.eval_on_selector("tbody tr", "e=>e.dataset.href"); pg.goto(B + "/admin/" + first); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-application-detail.png", full_page=True)
    pg.goto(B + "/admin/#/requests"); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-requests.png")
    pg.goto(B + "/admin/#/settings"); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-settings.png", full_page=True)
    pg.set_viewport_size({"width": 390, "height": 844}); pg.goto(B + "/admin/#/applications"); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-applications-mobile.png", full_page=True)
    pg.goto(B + "/admin/#/dashboard"); pg.wait_for_timeout(1200); pg.screenshot(path="docs/screenshots/admin-dashboard-mobile.png", full_page=True)
    b.close(); print("admin screenshots done")
