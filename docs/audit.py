"""Audit + screenshots for ETC Labs — Gen 1 public pages. Run while the server is up:  python docs/audit.py"""
from playwright.sync_api import sync_playwright
import os, json, time
B = "http://localhost:8790"
PAGES = ["index", "what-we-do", "products", "projects", "community", "about", "careers", "contact"]
os.makedirs("docs/screenshots", exist_ok=True)
FORCE = """() => { document.querySelectorAll('[data-reveal], .lines').forEach(e => e.classList.add('in')); document.querySelectorAll('.progress > i[data-w]').forEach(b => b.style.width = b.dataset.w); document.querySelectorAll('.world').forEach(w => { w.style.position = 'absolute'; w.style.height = document.documentElement.scrollHeight + 'px'; }); window.scrollTo(0,0); }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w, h, label in ((1440, 900, "desktop"), (390, 844, "mobile")):
        for name in PAGES:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=w < 500, has_touch=w < 500)
            ctx.add_init_script("sessionStorage.setItem('etc-intro','1')")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            t0 = time.time(); pg.goto(f"{B}/{name}.html", wait_until="load"); load = round((time.time() - t0) * 1000)
            pg.wait_for_timeout(600)
            sw = pg.evaluate("document.documentElement.scrollWidth"); iw = pg.evaluate("innerWidth")
            small = pg.evaluate("[...document.querySelectorAll('main p, main li, main a, main span, main b')].filter(e=>{const s=getComputedStyle(e);return parseFloat(s.fontSize)<11.5 && e.textContent.trim().length>2 && e.offsetParent && !e.closest('.mock') && !e.closest('svg')}).length")
            tiny_targets = pg.evaluate("[...document.querySelectorAll('main a, main button')].filter(e=>{const r=e.getBoundingClientRect();return e.offsetParent && r.width>0 && (r.height<32 || r.width<32) && !e.closest('svg')}).length") if w < 500 else 0
            pg.screenshot(path=f"docs/screenshots/{name}-{label}-hero.png")
            pg.evaluate(FORCE); pg.wait_for_timeout(500)
            pg.screenshot(path=f"docs/screenshots/{name}-{label}-full.png", full_page=True, animations="disabled")
            print(f"{label:7} {name:16} load={load:4}ms errors={len(errs)} overflow={'YES' if sw > iw else 'no '} tiny-text={small} small-targets={tiny_targets} {errs[:1]}")
            ctx.close()
    # opening: capture the intro frame on a fresh session
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page(); pg.goto(B + "/", wait_until="load"); pg.wait_for_timeout(500); pg.screenshot(path="docs/screenshots/opening-intro.png"); ctx.close()
    b.close()
