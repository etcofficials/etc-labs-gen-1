"""Simulates the GitHub Pages deployment (https://etcofficials.github.io/etc-labs-gen-1/) by serving public/ from
that origin inside Playwright, with the real backend on localhost:8790. Checks: relative paths resolve, no 404s,
no console errors, honest 'backend not connected' state when apiBase is empty, admin redirect page, and a real
cross-origin submission (CORS) when apiBase is set.   Run while the server is up:  python docs/static_sim.py"""
import io, sys, mimetypes, pathlib, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
ORIGIN = "https://etcofficials.github.io"; BASE = ORIGIN + "/etc-labs-gen-1/"; PUB = pathlib.Path("public"); API = "http://localhost:8790"
PAGES = ["index", "what-we-do", "products", "projects", "community", "about", "careers", "contact"]
results = []
def check(name, ok, detail=""): results.append(ok); print(("PASS" if ok else "FAIL"), name, "-", str(detail)[:110])

def serve(api_base):
    def handler(route):
        url = route.request.url
        if not url.startswith(BASE): return route.continue_()
        rel = url[len(BASE):].split("#")[0].split("?")[0] or "index.html"
        if rel.endswith("/"): rel += "index.html"
        f = PUB / rel
        if rel == "assets/js/config.js": return route.fulfill(body=f'window.ETC_CONFIG={{apiBase:"{api_base}"}};', content_type="application/javascript")
        if f.is_file(): return route.fulfill(body=f.read_bytes(), content_type=mimetypes.guess_type(str(f))[0] or "application/octet-stream")
        route.fulfill(status=404, body="not found")
    return handler

with sync_playwright() as p:
    # The simulation talks from a public origin to localhost, which Chromium's Local/Private Network Access blocks
    # (a real deployment talks public → public and is unaffected). Disable that check for the test only.
    b = p.chromium.launch(channel="msedge", headless=True, args=["--disable-features=LocalNetworkAccessChecks,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests,PrivateNetworkAccessSendPreflights"])
    # ---- 1. apiBase empty: every page must still render; forms show the honest not-connected state
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); ctx.route("**/*", serve(""))
    for name in PAGES:
        pg = ctx.new_page(); errs, missing = [], []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("response", lambda r: missing.append(r.url) if r.status == 404 and r.url.startswith(ORIGIN) else None)
        pg.goto(BASE + name + ".html", wait_until="load"); pg.wait_for_timeout(700)
        nav_ok = pg.evaluate("[...document.querySelectorAll('etc-nav a[href], etc-footer a[href]')].every(a => !a.getAttribute('href').startsWith('/'))")
        check(f"Pages sim: {name}.html renders (0 errors, 0 missing assets, no root-absolute links)", not errs and not missing and nav_ok, (errs + missing)[:2])
        pg.close()
    pg = ctx.new_page(); pg.goto(BASE + "contact.html", wait_until="load"); pg.wait_for_timeout(700)
    st = pg.inner_text("#contact-form .form-status"); dis = pg.eval_on_selector("#contact-form button[type=submit]", "e=>e.disabled")
    check("Pages sim: contact form says backend not connected + email fallback, submit disabled", "isn’t connected" in st and "etcofficials28@gmail.com" in st and dis, st)
    pg.goto(BASE + "careers.html", wait_until="load"); pg.wait_for_timeout(700)
    check("Pages sim: careers form shows the same honest state", pg.eval_on_selector("#careers-form button[type=submit]", "e=>e.disabled"), "disabled")
    pg.goto(BASE + "admin/", wait_until="load"); pg.wait_for_timeout(300)
    check("Pages sim: /admin/ explains that the backend is not configured", "not on this static host" in pg.inner_text("#msg"), pg.inner_text("#msg")[:80])
    ctx.close()

    # ---- 2. apiBase set: cross-origin submission must work (CORS) and /admin/ must redirect to the backend
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); ctx.route("**/*", serve(API))
    pg = ctx.new_page(); pg.goto(BASE + "contact.html", wait_until="load"); pg.wait_for_timeout(700)
    check("Pages sim (apiBase set): form enabled", not pg.eval_on_selector("#contact-form button[type=submit]", "e=>e.disabled"), "enabled")
    pg.fill("#name", "TEST Static"); pg.fill("#email-field", "static@example.com"); pg.fill("#building", "TEST cross-origin"); pg.select_option("#need", "software"); pg.fill("#message", "TEST message sent from the GitHub Pages simulation.")
    pg.wait_for_timeout(3200); pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(1500)
    ref = pg.eval_on_selector("#contact-success .ref", "e=>e.textContent")
    check("Pages sim (apiBase set): cross-origin submission stored via CORS", ref.startswith("Reference req_"), ref or pg.inner_text("#contact-form .form-status"))
    r = pg.request.fetch(API + "/api/admin/summary", method="OPTIONS", headers={"Origin": ORIGIN, "Access-Control-Request-Method": "GET"})
    check("CORS is NOT opened for admin routes", "access-control-allow-origin" not in {k.lower() for k in r.headers}, r.status)
    pg.goto(BASE + "admin/", wait_until="load"); pg.wait_for_timeout(1200)
    check("Pages sim (apiBase set): /admin/ redirects to backend admin", pg.url.startswith(API + "/admin"), pg.url)
    ctx.close(); b.close()
import sqlite3, os
con = sqlite3.connect("data/etc-labs.sqlite3"); n = con.execute("DELETE FROM project_requests WHERE name='TEST Static'").rowcount; con.commit(); con.close(); print("cleanup:", n)
print(f"\n{sum(results)}/{len(results)} passed"); sys.exit(0 if all(results) else 1)
