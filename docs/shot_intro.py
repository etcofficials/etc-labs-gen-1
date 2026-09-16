from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://localhost:8790/", wait_until="load"); pg.wait_for_timeout(650); pg.screenshot(path="docs/screenshots/opening-intro.png")
    pg.wait_for_timeout(900)
    print("intro released:", pg.evaluate("!document.querySelector('.intro') || document.querySelector('.intro').classList.contains('done')"), "| hero visible:", pg.eval_on_selector("#hero-title", "e=>getComputedStyle(e).opacity"))
    b.close()
