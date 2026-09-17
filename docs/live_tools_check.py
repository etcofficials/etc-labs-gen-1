"""Production check of the tools from the live GitHub Pages site against the Render backend. Run any time."""
import io, sys, os, json; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
B = "https://etcofficials.github.io/etc-labs-gen-1/"; API = "https://etc-labs-gen-1.onrender.com"
results = []
def check(name, ok, detail=""): results.append(ok); print(("PASS" if ok else "FAIL"), name, "-", str(detail)[:120])
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); ctx.add_init_script("sessionStorage.setItem('etc-intro','1')"); errs = []
    def page():
        pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); return pg
    # Transfer end to end
    f = os.path.join(os.environ.get("TEMP", "."), "etc-live-transfer.txt"); open(f, "wb").write(b"ETC Labs live transfer test " * 1500)
    pg = page(); pg.goto(B + "transfer.html", wait_until="load"); pg.wait_for_timeout(1500)
    check("Transfer page: upload state (backend connected)", pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state") == "upload", pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state"))
    pg.set_input_files("#tfile", f); pg.wait_for_timeout(300); pg.click("#tsend"); pg.wait_for_timeout(6000)
    st = pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state"); link = pg.eval_on_selector("#tlink", "e=>e.value") if st == "done" else ""
    check("Transfer: upload to Render succeeded with a Pages link", st == "done" and link.startswith(B + "transfer.html?t=tr_"), link or pg.eval_on_selector('[data-state="upload"] .form-status', "e=>e.textContent"))
    if link:
        pg.goto(link, wait_until="load"); pg.wait_for_timeout(3000)
        check("Transfer: download view resolves the link", pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state") == "download", pg.eval_on_selector("#dname", "e=>e.textContent"))
        with pg.expect_download(timeout=60000) as dl: pg.click("#ddownload")
        d = dl.value; check("Transfer: file downloads with identical size", os.path.getsize(d.path()) == os.path.getsize(f), d.suggested_filename)
        owner = pg.eval_on_selector("#towner", "e=>e.href") if False else None
    pg.close()
    # Voice: two tabs on the live site, signalling via Render WebSocket, real WebRTC
    a = page(); a.goto(B + "voice.html", wait_until="load"); a.wait_for_timeout(1200); a.fill("#vname", "LiveA"); a.click("#vcreate"); a.wait_for_timeout(5000)
    code = a.eval_on_selector("#rcode", "e=>e.textContent"); check("Voice: room created via Render (WebSocket welcome)", bool(code) and a.evaluate("document.querySelector('.tool-state.show')?.dataset.state") == "room", code or a.eval_on_selector('[data-state="lobby"] .form-status', "e=>e.textContent"))
    if code:
        c2 = page(); c2.goto(B + f"voice.html?room={code}", wait_until="load"); c2.wait_for_timeout(1000); c2.fill("#vname", "LiveB"); c2.click("#vjoin"); c2.wait_for_timeout(8000)
        check("Voice: second peer joins and connects (P2P through STUN)", a.eval_on_selector_all("#rpeers .peer", "els=>els.length") == 2 and "connected" in a.eval_on_selector("#rconn span", "e=>e.textContent"), a.eval_on_selector("#rconn span", "e=>e.textContent"))
        c2.click("#rleave"); c2.close()
    a.close()
    # AI + contributions + pages
    pg = page(); pg.goto(B + "ai.html", wait_until="load"); pg.wait_for_timeout(2500)
    check("AI page: honest 'not enabled' state on the live backend (no key set)", pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state") == "disabled", pg.evaluate("document.querySelector('.tool-state.show')?.dataset.state"))
    pg.goto(B + "community.html", wait_until="load"); pg.wait_for_timeout(3000)
    check("Community: contribution toggle enabled (public endpoint reachable through CORS)", pg.evaluate("!document.querySelector('[data-sort=\"points\"]').disabled"))
    pg.goto(B + "toolkit.html", wait_until="load"); pg.wait_for_timeout(800); pg.fill("#idea-form input[name=title]", "live test idea"); pg.click("#idea-form button"); pg.wait_for_timeout(300)
    check("Toolkit: works on the static host (local-first)", pg.evaluate("document.querySelectorAll('#idea-list .tk-item').length") == 1)
    for name in ["", "tools.html", "products.html", "projects.html", "about.html", "careers.html", "contact.html"]:
        pg.goto(B + name, wait_until="load"); pg.wait_for_timeout(700)
    check("All live pages: no console/page errors", not errs, errs[:2])
    b.close()
# clean the test transfer from the backend is not possible without the owner token in this script's flow; it expires in 24 h and is 42 KB.
print(f"\n{sum(results)}/{len(results)} passed"); sys.exit(0 if all(results) else 1)
