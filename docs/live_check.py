"""Checks the deployed GitHub Pages site in a real browser. Run: python docs/live_check.py"""
import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
B = "https://etcofficials.github.io/etc-labs-gen-1/"
PAGES = ["", "what-we-do.html", "products.html", "projects.html", "community.html", "about.html", "careers.html", "contact.html"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w, h, label in ((1440, 900, "desktop"), (390, 844, "mobile")):
        for name in PAGES:
            ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=w < 500, has_touch=w < 500); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); pg = ctx.new_page(); errs = []; bad = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("response", lambda r: bad.append(r.url) if r.status >= 400 else None)
            pg.goto(B + name, wait_until="load"); pg.wait_for_timeout(1200)
            sw = pg.evaluate("document.documentElement.scrollWidth"); iw = pg.evaluate("innerWidth"); css = pg.evaluate("getComputedStyle(document.body).fontFamily")
            print(f"{label:7} /{name or 'index':16} errors={len(errs)} bad-responses={len(bad)} overflow={'YES' if sw > iw else 'no'} nav-links={pg.eval_on_selector_all('etc-nav a', 'a=>a.length')} css-ok={'Inter' in css}", errs[:1], bad[:1])
            if name == "contact.html" and label == "desktop":
                print("  contact status:", pg.eval_on_selector("#contact-form .form-status", "e=>e.textContent.trim().slice(0,70)"), "| submit disabled:", pg.eval_on_selector("#contact-form button[type=submit]", "e=>e.disabled"))
                print("  links:", pg.evaluate("[...document.querySelectorAll('a[href^=mailto], a[href*=instagram]')].map(a=>a.getAttribute('href')+' '+a.target+' '+a.rel).slice(0,3)"))
            if name == "community.html" and label == "desktop":
                pg.evaluate("document.querySelector('#board').scrollIntoView()"); pg.wait_for_timeout(1200)
                print("  avatars loaded:", pg.evaluate("[...document.querySelectorAll('.avatar.img img')].map(i=>i.naturalWidth)"), "channels:", pg.evaluate("[...document.querySelectorAll('.board-row a')].map(a=>a.href.split('.com/')[1]+' '+a.target+' '+a.rel)"))
            if name == "" and label == "mobile":
                pg.click(".nav-toggle"); pg.wait_for_timeout(500); print("  mobile menu open:", pg.eval_on_selector(".nav-mobile", "e=>e.classList.contains('open')"), pg.eval_on_selector_all(".nav-mobile a", "a=>a.map(x=>x.textContent.trim()).slice(0,8)"))
                pg.click(".nav-toggle"); pg.wait_for_timeout(400); pg.screenshot(path="docs/screenshots/live-home-mobile.png")
            if name == "" and label == "desktop":
                pg.screenshot(path="docs/screenshots/live-home-desktop.png")
            ctx.close()
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page(); pg.goto(B + "admin/", wait_until="load"); pg.wait_for_timeout(1500); print("live /admin/ →", pg.url if not pg.url.startswith(B) else pg.inner_text("#msg")[:110]); ctx.close(); b.close()
