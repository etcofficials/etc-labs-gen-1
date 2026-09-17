"""Five-persona walkthrough. Asserts each question is answerable from the live site. Run while the server is up."""
from playwright.sync_api import sync_playwright
import time, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
B = "http://localhost:8790"; PW = "local-dev-password-1"
results = []
def check(name, ok, detail=""): results.append((name, ok, detail)); print(("PASS" if ok else "FAIL"), name, "-", detail)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); pg = ctx.new_page()

    # USER 1 — first-time visitor: "What is ETC Labs?" from the first viewport, no scrolling
    pg.goto(B + "/", wait_until="load"); pg.wait_for_timeout(700)
    above = pg.evaluate("[...document.querySelectorAll('main h1, main .lead, main .build-list li')].filter(e=>e.getBoundingClientRect().bottom<900).map(e=>e.textContent.trim()).join(' | ')")
    check("U1 what is ETC Labs above the fold", "independent technology lab" in above and "Software" in above and "Creator" in above, above[:140])

    # USER 2 — potential client: find the relevant service and the contact flow
    pg.click("text=What We Build"); pg.wait_for_timeout(900)
    pg.click('.ld-item[data-key="ai"]'); pg.wait_for_timeout(500)
    check("U2 service detail explains what/who/get", pg.evaluate("['What we do','Who it','What you get'].every(t=>document.querySelector('#svc-detail').textContent.includes(t))"), pg.eval_on_selector("#svc-detail h2", "e=>e.textContent"))
    pg.click('#svc-detail a.btn-primary'); pg.wait_for_timeout(900)
    check("U2 CTA lands on contact with need pre-filled", "contact.html" in pg.url and pg.eval_on_selector("#need", "e=>e.value") == "ai", pg.url)
    t0 = time.time(); pg.fill("#name", "Persona Client"); pg.fill("#email-field", "persona@example.com"); pg.fill("#building", "A booking app"); pg.fill("#message", "Persona test: a booking app with reminders for a small studio.")
    pg.wait_for_timeout(max(0, 3300 - int((time.time() - t0) * 1000))); pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(1500)
    check("U2 request submitted with a reference", pg.eval_on_selector("#contact-success", "e=>e.classList.contains('show')"), pg.eval_on_selector("#contact-success .ref", "e=>e.textContent"))

    # USER 3 — creator: understand the community without an essay
    pg.goto(B + "/community.html", wait_until="load"); pg.wait_for_timeout(700)
    hero = pg.evaluate("[...document.querySelectorAll('.league-hero h1, .league-hero .lead, .league-hero .benefits li')].map(e=>e.textContent.trim())")
    join_label = pg.eval_on_selector(".league-hero .btn-primary", "e=>e.textContent.trim()")
    check("U3 what/why/how above the fold", len(hero) >= 6 and any("community" in h for h in hero) and any("Collaborate" in h for h in hero), f"{len(hero)} statements, join button: {join_label}")
    check("U3 how to participate is explicit", pg.evaluate("document.querySelector('#join').textContent.includes('Say what you make')"), "join steps present")
    rows = pg.evaluate("[...document.querySelectorAll('.board-row:not(.head) .creator .name')].map(e=>e.textContent)")
    check("U3 creator directory shows verified rows with avatars", len(rows) == 10 and pg.evaluate("[...document.querySelectorAll('.avatar.img img')].every(i=>i.getAttribute('src').includes('creators/'))"), rows)

    # USER 4 — applicant: roles, requirements, apply
    pg.goto(B + "/careers.html", wait_until="load"); pg.wait_for_timeout(700)
    check("U4 roles visible without accordion", pg.eval_on_selector_all(".ld-item", "els=>els.length") == 5, "5 roles in the list")
    pg.click('.ld-item[data-key="community-mod"]'); pg.wait_for_timeout(400)
    check("U4 requirements on the role", pg.evaluate("document.querySelector('#role-detail').textContent.includes(\"What we're looking for\")"), pg.eval_on_selector("#role-detail h2", "e=>e.textContent"))
    pg.click('[data-apply="community-mod"]'); pg.wait_for_timeout(600)
    check("U4 apply pre-fills the form", pg.eval_on_selector("#position", "e=>e.value") == "community-mod", "position=community-mod, form in view")
    check("U4 knows what happens after", pg.evaluate("document.querySelector('.after').textContent.includes('hear back if it fits')"), "after-apply steps present")

    # USER 5 — ETC Labs (admin): where are applications and requests?
    pg.goto(B + "/admin/", wait_until="load"); pg.fill("#u", "admin"); pg.fill("#p", PW); pg.click("button[type=submit]"); pg.wait_for_timeout(1500)
    stats = pg.eval_on_selector_all(".stat b", "els=>els.map(e=>e.textContent)")
    check("U5 dashboard shows new counts immediately", len(stats) >= 2, f"new apps={stats[0]}, new requests={stats[1]}")
    pg.goto(B + "/admin/#/requests"); pg.wait_for_timeout(1000)
    check("U5 persona request is in the list", pg.evaluate("document.body.textContent.includes('Persona Client')"), "found in project requests")
    ctx.close(); b.close()
print(f"\n{sum(1 for r in results if r[1])}/{len(results)} passed")
