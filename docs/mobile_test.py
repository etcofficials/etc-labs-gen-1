"""Touch-first mobile checks + breakpoint sweep. Run while the server is up:  python docs/mobile_test.py"""
import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
B = "http://localhost:8790"; results = []
def check(name, ok, detail=""): results.append(ok); print(("PASS" if ok else "FAIL"), name, "-", str(detail)[:110])
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')")
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(B + "/", wait_until="load"); pg.wait_for_timeout(900)
    check("Home: aurora layer present and hero accent line rendered", pg.evaluate("!!document.querySelector('.world-aurora') && getComputedStyle(document.querySelector('.hero-line')).display !== 'none'"))
    check("Home: hero headline + five build chips visible in first viewport", pg.evaluate("[...document.querySelectorAll('.home-hero .build-list li')].every(e=>e.getBoundingClientRect().top < 844)"))
    # orbit: tap a node → panel; second tap navigates
    pg.evaluate("document.querySelector('#eco').scrollIntoView({block:'center'})"); pg.wait_for_timeout(400)
    pg.tap('.eco .node[data-i="1"]'); pg.wait_for_timeout(400)
    check("Orbit: first tap selects node and shows detail panel (no navigation)", pg.url.endswith("/") and pg.evaluate("document.querySelector('.eco-panel').classList.contains('show') && document.querySelector('.eco .node[data-i=\"1\"]').classList.contains('on')"), pg.eval_on_selector(".eco-panel h3", "e=>e.textContent"))
    pg.tap('.eco .node[data-i="3"]'); pg.wait_for_timeout(300)
    check("Orbit: tapping another node switches the same panel", pg.eval_on_selector(".eco-panel h3", "e=>e.textContent") == "Infrastructure", pg.eval_on_selector(".eco-panel h3", "e=>e.textContent"))
    box = pg.eval_on_selector('.eco .node[data-i="3"] circle.bg', "e=>{const r=e.getBoundingClientRect();return [r.width,r.height]}")
    check("Orbit: node touch target ≥ 44px", box[0] >= 44 and box[1] >= 44, box)
    pg.tap('.eco .node[data-i="3"]'); pg.wait_for_timeout(700)
    check("Orbit: second tap on the selected node navigates", "what-we-do.html" in pg.url, pg.url)
    # what we build rows: first tap selects, second navigates
    pg.goto(B + "/", wait_until="load"); pg.wait_for_timeout(700); pg.evaluate("document.querySelector('#build-rows').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.tap('#build-rows .row[data-i="2"]'); pg.wait_for_timeout(400)
    check("Build rows: tap selects + expands description + swaps visual", pg.url.endswith("/") and pg.evaluate("document.querySelector('#build-rows .row[data-i=\"2\"]').getAttribute('aria-selected')==='true' && getComputedStyle(document.querySelector('#build-rows .row[data-i=\"2\"] p')).opacity==='1' && !!document.querySelector('#build-visual .mock')"))
    # sections divider animates in
    check("Sections: in-view class applied on scroll (animated divider)", pg.evaluate("[...document.querySelectorAll('main .section')].filter(s=>s.classList.contains('in-view')).length >= 2"))
    # nav menu stagger + active indicator
    pg.tap(".nav-toggle"); pg.wait_for_timeout(500)
    check("Nav: menu open, groups animated in, Tools group lists four tools", pg.evaluate("document.querySelector('.nav-mobile').classList.contains('open') && getComputedStyle(document.querySelector('.nav-mobile .nav-group')).opacity==='1' && [...document.querySelectorAll('.nav-mobile a')].filter(a=>/Transfer|Voice Rooms|AI Utilities|Creator Toolkit/.test(a.textContent)).length===4"))
    check("Nav: every menu link ≥ 44px tall", pg.evaluate("[...document.querySelectorAll('.nav-mobile a')].every(a=>a.getBoundingClientRect().height>=44)"))
    pg.tap(".nav-toggle"); pg.wait_for_timeout(400)
    # projects filters scroll horizontally, no overflow
    pg.goto(B + "/projects.html", wait_until="load"); pg.wait_for_timeout(700)
    check("Projects: filter chips scroll horizontally, page does not overflow", pg.evaluate("getComputedStyle(document.querySelector('#filters')).overflowX==='auto' && document.documentElement.scrollWidth<=innerWidth"))
    pg.tap('.filter-btn[data-filter="ai"]'); pg.wait_for_timeout(500)
    check("Projects: tapping a filter works", pg.evaluate("[...document.querySelectorAll('.project')].filter(c=>!c.classList.contains('is-hidden')).length") == 1)
    # products: expandable details
    pg.goto(B + "/products.html", wait_until="load"); pg.wait_for_timeout(700); pg.evaluate("document.querySelector('.product-item').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
    before = pg.evaluate("document.querySelector('.product-item .expandable').getBoundingClientRect().height"); pg.tap(".product-item .expand-toggle"); pg.wait_for_timeout(600); after = pg.evaluate("document.querySelector('.product-item .expandable').getBoundingClientRect().height")
    check("Products: Details toggle expands the card", before == 0 and after > 60, f"{before}→{after}")
    check("Products: every card has a working Open button", pg.evaluate("[...document.querySelectorAll('.product-item .foot a')].every(a=>/\\.html/.test(a.getAttribute('href')))"))
    # community creators as cards
    pg.goto(B + "/community.html", wait_until="load"); pg.wait_for_timeout(700); pg.evaluate("document.querySelector('#board').scrollIntoView()"); pg.wait_for_timeout(900)
    check("Community: creator rows render as cards with avatar, handle, count, points, channel", pg.evaluate("[...document.querySelectorAll('.board-row:not(.head)')].slice(0,10).every(r=>r.querySelector('.avatar img') && r.querySelector('.handle') && r.querySelector('.stat') && r.querySelector('.pts') && r.querySelector('.action a').getBoundingClientRect().height>=40)"))
    check("Community: contribution toggle enabled (backend reachable)", pg.evaluate("!document.querySelector('[data-sort=\"points\"]').disabled"))
    # careers list-detail behaves like an accordion
    pg.goto(B + "/careers.html", wait_until="load"); pg.wait_for_timeout(700); pg.evaluate("document.querySelector('#role-list').scrollIntoView()"); pg.wait_for_timeout(200)
    pg.tap('.ld-item[data-key="web-dev"]'); pg.wait_for_timeout(500)
    check("Careers: tapping a role updates the detail and marks it selected", pg.evaluate("document.querySelector('.ld-item[data-key=\"web-dev\"]').getAttribute('aria-selected')==='true' && document.querySelector('#role-detail h2').textContent.includes('Developer')"))
    check("Careers: inputs use 16px+ font (no iOS zoom) and are ≥ 48px", pg.evaluate("[...document.querySelectorAll('#careers-form .input, #careers-form .select')].every(i=>parseFloat(getComputedStyle(i).fontSize)>=16 && i.getBoundingClientRect().height>=48)"))
    check("No console/page errors during the mobile walkthrough", not errs, errs[:2])
    pg.close()
    # breakpoint sweep
    for w in (320, 360, 390, 412, 430, 480, 768, 1024, 1440):
        c2 = b.new_context(viewport={"width": w, "height": 900}, is_mobile=w < 700, has_touch=w < 700); c2.add_init_script("sessionStorage.setItem('etc-intro','1')"); q = c2.new_page(); bad = []
        for name in ["index", "products", "projects", "community", "careers", "contact", "transfer", "voice", "toolkit"]:
            q.goto(f"{B}/{name}.html", wait_until="load"); q.wait_for_timeout(250)
            if q.evaluate("document.documentElement.scrollWidth > innerWidth + 1"): bad.append(name)
        check(f"{w}px: no horizontal overflow on 9 pages", not bad, bad); c2.close()
    b.close()
print(f"\n{sum(results)}/{len(results)} passed"); sys.exit(0 if all(results) else 1)
