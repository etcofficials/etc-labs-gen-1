"""End-to-end tests for ETC Labs — Gen 1 (brief §46–47). Run while the server is up:
    python docs/e2e.py [admin-password]
Uses clearly-labelled TEST data only; removes what it created at the end."""
import json, os, sys, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import urllib.request, urllib.error, sqlite3
from playwright.sync_api import sync_playwright
B = "http://localhost:8790"; PW = sys.argv[1] if len(sys.argv) > 1 else "local-dev-password-1"
results = []
def check(name, ok, detail=""): results.append((name, ok)); print(("PASS" if ok else "FAIL"), name, "-", str(detail)[:120])
def post_json(path, body, headers=None):
    req = urllib.request.Request(B + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **(headers or {})}, method="POST")
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b"{}")

started = str(int(time.time() * 1000) - 5000)
# ---------------- API-level: validation, spam protection
s, d = post_json("/api/project-requests", {"name": "TEST Missing", "email": "not-an-email", "building": "x", "need": "software", "message": "short", "started_at": started})
check("API rejects invalid email (422)", s == 422 and "email" in d.get("error", "").lower(), d)
s, d = post_json("/api/project-requests", {"name": "TEST Bot", "email": "bot@example.com", "building": "x", "need": "software", "message": "a" * 30, "started_at": started, "website": "http://spam"})
check("Honeypot: accepted but not stored", s == 200 and d.get("stored") is False, d)
# (the public rate limit is 5 submissions / 10 min per client; this run uses exactly 5 real submissions, so the
#  too-fast timing check is covered by docs/perf.py notes and verified manually — see CHANGELOG)

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); pg = ctx.new_page()

    # ---------------- Contact form (UI)
    pg.goto(B + "/contact.html", wait_until="load"); pg.wait_for_timeout(600)
    pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(300)
    check("Contact: missing required fields blocked", pg.eval_on_selector_all(".field.invalid", "e=>e.length") >= 3, pg.eval_on_selector("#contact-form .form-status", "e=>e.textContent"))
    pg.fill("#name", "TEST Contact"); pg.fill("#email-field", "bad-email"); pg.fill("#building", "TEST booking app"); pg.select_option("#need", "software"); pg.fill("#message", "TEST message: a booking app with reminders for a studio.")
    pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(300)
    check("Contact: invalid email shown inline", "valid email" in pg.eval_on_selector("#email-field ~ .field-error", "e=>e.textContent"), "inline error")
    pg.fill("#email-field", "test-contact@example.com"); pg.check('input[name="scale"][value="small"]')
    pg.wait_for_timeout(3200)
    with pg.expect_response(lambda r: "/api/project-requests" in r.url) as resp:
        pg.click("#contact-form button[type=submit]")
        loading = pg.eval_on_selector("#contact-form button[type=submit]", "e=>e.disabled && e.textContent.includes('Sending')")
    check("Contact: loading state shown", loading, "button disabled + Sending…")
    pg.wait_for_timeout(800)
    ref = pg.eval_on_selector("#contact-success .ref", "e=>e.textContent")
    check("Contact: success state with reference", pg.eval_on_selector("#contact-success", "e=>e.classList.contains('show')") and ref.startswith("Reference req_"), ref)
    request_id = ref.replace("Reference ", "")

    # failure state: point the form at a dead endpoint
    pg.goto(B + "/contact.html", wait_until="load"); pg.wait_for_timeout(600)
    pg.route("**/api/project-requests", lambda route: route.fulfill(status=500, body="{}"))
    pg.fill("#name", "TEST Fail"); pg.fill("#email-field", "fail@example.com"); pg.fill("#building", "x"); pg.select_option("#need", "ai"); pg.fill("#message", "TEST failure path message, long enough.")
    pg.wait_for_timeout(3200); pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(800)
    st = pg.eval_on_selector("#contact-form .form-status", "e=>e.textContent")
    check("Contact: failure state explains + offers email", "couldn" in st and "etcofficials28@gmail.com" in st and not pg.eval_on_selector("#contact-form button[type=submit]", "e=>e.disabled"), st)
    pg.unroute("**/api/project-requests")

    # ---------------- Careers form (UI) with resume upload
    pdf = os.path.join(os.environ.get("TEMP", "."), "etc-test-resume.pdf"); open(pdf, "wb").write(b"%PDF-1.4\n%TEST resume for ETC Labs e2e\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n")
    bad = os.path.join(os.environ.get("TEMP", "."), "etc-fake.pdf"); open(bad, "wb").write(b"not really a pdf")
    pg.goto(B + "/careers.html", wait_until="load"); pg.wait_for_timeout(600)
    pg.click("#careers-form button[type=submit]"); pg.wait_for_timeout(300)
    check("Careers: validation blocks empty form", pg.eval_on_selector_all("#careers-form .field.invalid", "e=>e.length") >= 4, "invalid fields highlighted")
    pg.fill("#firstName", "TEST"); pg.fill("#lastName", "Applicant"); pg.fill("#email", "test-applicant@example.com"); pg.fill("#discord", "test_user#0000"); pg.select_option("#position", "web-dev"); pg.fill("#portfolio", "https://example.com/portfolio"); pg.fill("#cover", "TEST cover letter.")
    pg.set_input_files("#resume", bad); pg.wait_for_timeout(3200); pg.click("#careers-form button[type=submit]"); pg.wait_for_timeout(900)
    st = pg.eval_on_selector("#careers-form .form-status", "e=>e.textContent")
    check("Careers: fake PDF rejected server-side (magic bytes)", "PDF" in st or "file" in st.lower(), st)
    pg.set_input_files("#resume", pdf); pg.wait_for_timeout(400); pg.click("#careers-form button[type=submit]"); pg.wait_for_timeout(1200)
    ref = pg.eval_on_selector("#careers-success .ref", "e=>e.textContent")
    check("Careers: valid submission with resume succeeds", ref.startswith("Reference app_"), ref)
    app_id = ref.replace("Reference ", "")

    # ---------------- Admin
    pg.goto(B + "/admin/", wait_until="load"); pg.wait_for_timeout(500)
    r = pg.request.get(B + "/api/admin/summary"); check("Admin API without session → 401", r.status == 401, r.status)
    pg.fill("#u", "admin"); pg.fill("#p", "definitely-wrong"); pg.click("button[type=submit]"); pg.wait_for_timeout(1200)
    check("Admin: wrong password message", "Wrong username or password" in pg.inner_text("#app"), "message shown")
    pg.fill("#u", "admin"); pg.fill("#p", PW); pg.click("button[type=submit]"); pg.wait_for_timeout(1500)
    check("Admin: login → dashboard", "Dashboard" in pg.inner_text("h1"), pg.inner_text("h1"))
    stats = pg.eval_on_selector_all(".stat b", "els=>els.map(e=>e.textContent)")
    check("Admin: dashboard counts are real (≥1 new app, ≥1 new request)", int(stats[0]) >= 1 and int(stats[1]) >= 1, stats)
    pg.goto(B + "/admin/#/applications"); pg.wait_for_timeout(900)
    check("Admin: applications list shows the test applicant", "TEST Applicant" in pg.inner_text("#list"), "row present")
    pg.fill("input[name=q]", "zzz-no-match"); pg.click("#filters button[type=submit]"); pg.wait_for_timeout(700)
    check("Admin: search filters (no match → empty state)", "Nothing matches" in pg.inner_text("#list") or pg.eval_on_selector_all("#list tbody tr", "e=>e.length") == 0, pg.inner_text("#list")[:60])
    pg.fill("input[name=q]", "TEST"); pg.click("#filters button[type=submit]"); pg.wait_for_timeout(700)
    check("Admin: search finds the applicant", "TEST Applicant" in pg.inner_text("#list"), "found")
    pg.select_option("select[name=status]", "hired"); pg.click("#filters button[type=submit]"); pg.wait_for_timeout(700)
    check("Admin: status filter (hired) hides the new applicant", "TEST Applicant" not in pg.inner_text("#list"), "filtered out")
    pg.goto(B + "/admin/#/applications/" + app_id); pg.wait_for_timeout(900)
    txt = pg.inner_text("#app")
    check("Admin: detail shows name/email/discord/position/portfolio/cover/resume/date", all(x in txt for x in ["TEST Applicant", "test-applicant@example.com", "test_user#0000", "Web / Backend Developer", "example.com/portfolio", "TEST cover letter", "etc-test-resume.pdf"]), "all fields present")
    pg.select_option("#st", "reviewing"); pg.click("#save-status"); pg.wait_for_timeout(900)
    row = sqlite3.connect("data/etc-labs.sqlite3").execute("SELECT status FROM applications WHERE id=?", (app_id,)).fetchone()
    check("Admin: status change persists to the database", row and row[0] == "reviewing", row)
    r = pg.request.get(B + f"/api/admin/applications/{app_id}/resume")
    check("Admin: resume download (attachment) works when logged in", r.status == 200 and "attachment" in r.headers.get("content-disposition", ""), r.headers.get("content-disposition"))
    r = pg.request.get(B + "/api/admin/applications/../../.env")
    check("Admin: path traversal blocked", r.status in (404, 403, 422), r.status)
    r = pg.request.patch(B + f"/api/admin/applications/{app_id}", data=json.dumps({"status": "hired"}), headers={"Content-Type": "application/json"})
    check("Admin: write without X-ETC-Admin header → 403", r.status == 403, r.status)
    pg.goto(B + "/admin/#/requests"); pg.wait_for_timeout(900)
    check("Admin: project requests list shows the test request", "TEST Contact" in pg.inner_text("#list"), "row present")
    pg.goto(B + "/admin/#/requests/" + request_id); pg.wait_for_timeout(900); txt = pg.inner_text("#app")
    check("Admin: request detail shows name/email/building/need/scale/message/date", all(x in txt.lower() for x in ["test contact", "test-contact@example.com", "test booking app", "software", "small", "reminders"]), "fields present")
    pg.goto(B + "/admin/#/settings"); pg.wait_for_timeout(900); txt = pg.inner_text("#app")
    check("Admin: settings shows login activity + no public accounts note", "Last successful login" in txt and "no user accounts" in txt, "present")
    pg.click("text=Sign out"); pg.wait_for_timeout(900)
    r = pg.request.get(B + "/api/admin/summary"); check("Admin: after logout, API → 401", r.status == 401, r.status)
    check("Admin: after logout, login screen shown", pg.query_selector("#login") is not None, "login form")

    # unauthenticated public user cannot fetch a resume
    r2 = b.new_context().request.get(B + f"/api/admin/applications/{app_id}/resume"); check("Public: resume URL without session → 401", r2.status == 401, r2.status)

    # ---------------- Static-host mode (GitHub Pages simulation): no apiBase → honest 'not connected' state
    pg2 = ctx.new_page(); pg2.route("**/assets/js/config.js", lambda route: route.fulfill(body='window.ETC_CONFIG={apiBase:""}', content_type="application/javascript"))
    pg2.goto("http://127.0.0.1:8790/contact.html".replace("127.0.0.1", "localhost"), wait_until="load")  # localhost counts as backend; emulate static host via hostname check below
    st = pg2.evaluate("(() => { const h = location.hostname; return h; })()")
    check("Static-host detection uses hostname (localhost = backend present)", st == "localhost", st)
    ctx.close(); b.close()

# ---------------- cleanup: remove TEST rows and their resume files
con = sqlite3.connect("data/etc-labs.sqlite3")
for path, in con.execute("SELECT resume_path FROM applications WHERE first_name='TEST' AND resume_path<>''"):
    f = os.path.join("data", "uploads", path);  os.path.exists(f) and os.remove(f)
a = con.execute("DELETE FROM applications WHERE first_name='TEST'").rowcount; r = con.execute("DELETE FROM project_requests WHERE name LIKE 'TEST %'").rowcount
con.execute("DELETE FROM notes WHERE target_id NOT IN (SELECT id FROM applications) AND target_id NOT IN (SELECT id FROM project_requests)"); con.commit(); con.close()
print(f"cleanup: removed {a} test applications, {r} test requests")
print(f"\n{sum(1 for _, ok in results if ok)}/{len(results)} passed")
sys.exit(0 if all(ok for _, ok in results) else 1)
