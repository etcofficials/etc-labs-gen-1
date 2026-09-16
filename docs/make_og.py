"""Renders assets/img/og.png (1200x630 social preview) from a small HTML template. Run while the server is up."""
from playwright.sync_api import sync_playwright
HTML = """<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet"><style>
body{margin:0;width:1200px;height:630px;background:radial-gradient(900px 500px at 15% 20%,rgba(139,92,246,.35),transparent 60%),radial-gradient(700px 500px at 85% 90%,rgba(34,211,238,.28),transparent 60%),#07070b;font-family:'Space Grotesk',sans-serif;color:#f4f4fb;position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:60px 60px;mask-image:radial-gradient(closest-side at 50% 50%,#000,transparent)}
.logo{position:absolute;left:80px;top:80px;width:360px}.h{position:absolute;left:80px;top:220px;font-size:96px;line-height:1;font-weight:700;letter-spacing:-.03em}
.g{background:linear-gradient(90deg,#22d3ee,#8b5cf6,#e879f9);-webkit-background-clip:text;color:transparent}
.s{position:absolute;left:84px;top:520px;font-family:'JetBrains Mono',monospace;font-size:22px;letter-spacing:.12em;text-transform:uppercase;color:#a9a6c4}
</style></head><body><div class="grid"></div><img class="logo" src="http://localhost:8790/assets/img/etc-logo.svg"><div class="h">We build<br>what comes <span class="g">next.</span></div><div class="s">Gen 1 · independent technology showcase</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(HTML); pg.wait_for_timeout(1200); pg.screenshot(path="public/assets/img/og.png"); b.close(); print("og.png written")
