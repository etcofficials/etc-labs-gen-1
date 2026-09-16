"""Performance + keyboard checks. Run while the server is up: python docs/perf.py"""
from playwright.sync_api import sync_playwright
B = "http://localhost:8790"
FPS = """async () => { let frames = 0, long = 0, last = performance.now(); const t0 = last; await new Promise(res => { function f(t) { frames++; if (t - last > 50) long++; last = t; if (t - t0 < 3000) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); }); return { fps: Math.round(frames / 3), longFrames: long }; }"""
SCROLL_FPS = """async () => { let frames = 0, long = 0, last = performance.now(); const t0 = last; let y = 0; await new Promise(res => { function f(t) { frames++; if (t - last > 50) long++; last = t; y += 24; window.scrollTo(0, y); if (t - t0 < 3000) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); }); return { fps: Math.round(frames / 3), longFrames: long }; }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for label, vp, cpu in (("desktop 1x", (1440, 900), 1), ("desktop 4x slow CPU", (1440, 900), 4), ("mobile 4x slow CPU", (390, 844), 4)):
        ctx = b.new_context(viewport={"width": vp[0], "height": vp[1]}, is_mobile=vp[0] < 500); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')")
        pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); cdp.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
        pg.goto(B + "/", wait_until="load"); pg.wait_for_timeout(800)
        idle = pg.evaluate(FPS); scroll = pg.evaluate(SCROLL_FPS)
        js = pg.evaluate("performance.getEntriesByType('resource').filter(r=>r.name.endsWith('.js')).reduce((a,r)=>a+(r.transferSize||r.encodedBodySize||0),0)")
        css = pg.evaluate("performance.getEntriesByType('resource').filter(r=>r.name.endsWith('.css')).reduce((a,r)=>a+(r.transferSize||r.encodedBodySize||0),0)")
        dom = pg.evaluate("document.querySelectorAll('*').length")
        print(f"{label:20} idle {idle['fps']} fps ({idle['longFrames']} long) · scroll {scroll['fps']} fps ({scroll['longFrames']} long) · JS {js//1024} KB · CSS {css//1024} KB · DOM {dom} nodes")
        ctx.close()
    # keyboard: tab through the nav and open the mobile menu with keyboard
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); pg = ctx.new_page(); pg.goto(B + "/", wait_until="load")
    seq = []
    for _ in range(9): pg.keyboard.press("Tab"); seq.append(pg.evaluate("(document.activeElement.textContent||document.activeElement.getAttribute('aria-label')||'').trim().slice(0,24)"))
    print("tab order:", seq)
    pg.keyboard.press("Enter"); pg.wait_for_timeout(700); print("enter on focused link navigated to:", pg.url)
    ctx.close()
    ctx = b.new_context(viewport={"width": 390, "height": 844}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); pg = ctx.new_page(); pg.goto(B + "/", wait_until="load")
    pg.focus(".nav-toggle"); pg.keyboard.press("Enter"); pg.wait_for_timeout(500); print("mobile menu open via keyboard:", pg.eval_on_selector(".nav-mobile", "e=>e.classList.contains('open')"), "| focus:", pg.evaluate("document.activeElement.textContent.trim().slice(0,12)"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400); print("closed via Esc:", not pg.eval_on_selector(".nav-mobile", "e=>e.classList.contains('open')"))
    # reduced motion
    ctx2 = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg2 = ctx2.new_page(); pg2.goto(B + "/", wait_until="load"); pg2.wait_for_timeout(300)
    print("reduced-motion: intro shown?", pg2.evaluate("!!document.querySelector('.intro')"), "| flow canvas running?", pg2.evaluate("getComputedStyle(document.querySelector('.world-flow')).display !== 'none'"), "| hero visible immediately?", pg2.eval_on_selector("#hero-title", "e=>getComputedStyle(e).opacity") == "1")
    b.close()
