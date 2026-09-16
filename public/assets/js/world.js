/* ==========================================================================
   ETC Labs — Gen 1 · World & motion engine
   background world · tone · flow canvas (desktop) · cursor light · cursor
   tracker · scroll progress · intro · magnetic buttons · page transitions
   Everything here animates transform/opacity only and stops when unseen.
   ========================================================================== */
(function () {
  "use strict";
  const M = (window.ETC = window.ETC || {});
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(pointer: fine)").matches;
  const small = matchMedia("(max-width: 767px)").matches;
  const saveData = navigator.connection && navigator.connection.saveData;
  const lowPower = small || saveData || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4 && !finePointer);
  M.env = { reduce, finePointer, small, lowPower };

  /* ---------- World markup ---------- */
  const world = document.createElement("div");
  world.className = "world"; world.setAttribute("aria-hidden", "true");
  world.innerHTML = '<div class="world-base"></div><div class="light a"></div><div class="light b"></div><div class="light c"></div><div class="world-grid"></div><canvas class="world-flow"></canvas><div class="world-cursor"></div><div class="world-noise"></div><div class="world-vignette"></div>';
  document.body.prepend(world);
  const progress = document.createElement("div"); progress.className = "progress-bar"; progress.setAttribute("aria-hidden", "true"); document.body.prepend(progress);

  /* ---------- Tone: the world follows the section in view ---------- */
  const toneSections = document.querySelectorAll("[data-tone]");
  if (toneSections.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) document.body.dataset.tone = en.target.dataset.tone; });
    }, { rootMargin: "-40% 0px -40% 0px" });
    toneSections.forEach((s) => io.observe(s));
  }

  /* ---------- Scroll progress + nav state (one rAF-throttled handler) ---------- */
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.setProperty("--p", max > 0 ? (scrollY / max).toFixed(4) : 0);
      const nav = document.querySelector(".nav"); if (nav) nav.classList.toggle("scrolled", scrollY > 12);
      ticking = false;
    });
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Cursor light + tracker (fine pointers only) ---------- */
  if (finePointer && !small && !reduce) {
    const light = world.querySelector(".world-cursor");
    const cursor = document.createElement("div"); cursor.className = "cursor"; cursor.setAttribute("aria-hidden", "true"); document.body.appendChild(cursor);
    let tx = innerWidth / 2, ty = innerHeight / 2, lx = tx, ly = ty, cx = tx, cy = ty, raf = null, active = false;
    const loop = () => {
      lx += (tx - lx) * 0.06; ly += (ty - ly) * 0.06;        // slow light
      cx += (tx - cx) * 0.35; cy += (ty - cy) * 0.35;        // quick ring
      light.style.transform = `translate3d(${lx.toFixed(1)}px, ${ly.toFixed(1)}px, 0)`;
      cursor.style.transform = `translate3d(${cx.toFixed(1)}px, ${cy.toFixed(1)}px, 0)`;
      if (Math.abs(tx - lx) > 0.5 || Math.abs(ty - ly) > 0.5 || Math.abs(tx - cx) > 0.2) raf = requestAnimationFrame(loop); else raf = null;
    };
    const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
    addEventListener("pointermove", (e) => { tx = e.clientX; ty = e.clientY; if (!active) { active = true; world.classList.add("has-pointer"); cursor.classList.add("on"); } kick(); }, { passive: true });
    document.addEventListener("pointerleave", () => { cursor.classList.remove("on"); });
    document.addEventListener("pointerenter", () => { if (active) cursor.classList.add("on"); });
    addEventListener("pointerdown", () => cursor.classList.add("press"));
    addEventListener("pointerup", () => cursor.classList.remove("press"));
    // Contextual state: hover on interactive things, label from data-cursor
    document.addEventListener("pointerover", (e) => {
      const labelled = e.target.closest("[data-cursor]");
      const inter = e.target.closest("a, button, [role=button], input, select, textarea, label, summary");
      cursor.classList.toggle("label", !!labelled);
      cursor.classList.toggle("hover", !!inter && !labelled);
      cursor.textContent = labelled ? labelled.dataset.cursor : "";
    });
    document.addEventListener("pointerout", (e) => { if (!e.relatedTarget) { cursor.classList.remove("label", "hover"); cursor.textContent = ""; } });
  }

  /* ---------- Flow canvas: a few drifting lines (desktop only) ---------- */
  const canvas = world.querySelector(".world-flow");
  if (canvas && !lowPower && !reduce && finePointer) {
    const ctx = canvas.getContext("2d", { alpha: true });
    let w = 0, h = 0, lines = [], raf = null, last = 0, running = false;
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    const resize = () => {
      w = innerWidth; h = innerHeight; canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.width = w + "px"; canvas.style.height = h + "px"; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      lines = Array.from({ length: w > 1400 ? 9 : 7 }, (_, i) => ({ y: (i + 0.5) * (h / 9), amp: 40 + Math.random() * 90, len: 0.6 + Math.random() * 0.8, speed: 0.00012 + Math.random() * 0.00018, phase: Math.random() * 100, hue: i % 3 }));
    };
    const draw = (t) => {
      ctx.clearRect(0, 0, w, h);
      const cols = ["34,211,238", "139,92,246", "232,121,249"];
      for (const L of lines) {
        const grad = ctx.createLinearGradient(0, 0, w, 0);
        grad.addColorStop(0, `rgba(${cols[L.hue]},0)`); grad.addColorStop(0.5, `rgba(${cols[L.hue]},0.16)`); grad.addColorStop(1, `rgba(${cols[L.hue]},0)`);
        ctx.strokeStyle = grad; ctx.lineWidth = 1; ctx.beginPath();
        for (let x = 0; x <= w; x += 24) {
          const y = L.y + Math.sin(x * 0.0022 * L.len + t * L.speed + L.phase) * L.amp + Math.sin(x * 0.0007 + t * L.speed * 0.6) * L.amp * 0.4;
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    };
    const step = (t) => { if (t - last > 33) { draw(t); last = t; } raf = requestAnimationFrame(step); }; // ~30fps is plenty for a background
    const start = () => { if (!running) { running = true; raf = requestAnimationFrame(step); } };
    const stop = () => { running = false; if (raf) cancelAnimationFrame(raf); raf = null; };
    resize(); start();
    addEventListener("resize", () => { resize(); }, { passive: true });
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
  }

  /* ---------- Buttons: cursor-following light + gentle magnetism ---------- */
  document.addEventListener("pointermove", (e) => {
    const b = e.target.closest(".btn-primary, .cta-band, .mock-wrap, .mock");
    if (!b) return;
    const r = b.getBoundingClientRect();
    b.style.setProperty("--x", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
    b.style.setProperty("--y", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
    if (b.classList.contains("mock") || b.classList.contains("mock-wrap")) { const m = b.classList.contains("mock") ? b : b.querySelector(".mock"); if (m) { m.style.setProperty("--mx", b.style.getPropertyValue("--x")); m.style.setProperty("--my", b.style.getPropertyValue("--y")); } }
  }, { passive: true });
  if (finePointer && !reduce) {
    document.addEventListener("pointermove", (e) => {
      const b = e.target.closest(".btn-primary, .btn-secondary");
      if (!b) return;
      const r = b.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
      b.style.transform = `translate3d(${(dx * 0.12).toFixed(1)}px, ${(dy * 0.18).toFixed(1)}px, 0)`;
    }, { passive: true });
    document.addEventListener("pointerout", (e) => { const b = e.target.closest(".btn-primary, .btn-secondary"); if (b && !b.contains(e.relatedTarget)) b.style.transform = ""; });
  }

  /* ---------- Page transitions (internal links) ---------- */
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]"); if (!a || reduce) return;
    const href = a.getAttribute("href");
    if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:") || a.target === "_blank" || /^https?:/i.test(href) || a.hasAttribute("download")) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); document.body.classList.add("is-leaving");
    setTimeout(() => { location.href = href; }, 220);
  });
  addEventListener("pageshow", (e) => { document.body.classList.remove("is-leaving"); if (e.persisted) document.body.classList.remove("is-entering"); });

  /* ---------- Intro: ≤1.2s, once per session, click to skip, never blocks ---------- */
  const wantsIntro = document.body.dataset.intro === "1" && !reduce && !sessionStorage.getItem("etc-intro");
  if (wantsIntro) {
    document.body.classList.add("intro-active");
    const intro = document.createElement("div"); intro.className = "intro"; intro.setAttribute("aria-hidden", "true");
    intro.innerHTML = '<div><div class="intro-mark"><img src="assets/img/etc-logo.svg" alt="" width="252" height="52"></div><div class="intro-line"><i></i></div><div class="intro-tag">Gen 1</div></div><div class="intro-skip">click to skip</div>';
    document.body.appendChild(intro);
    const end = () => { if (intro.classList.contains("done")) return; intro.classList.add("done"); document.body.classList.remove("intro-active"); sessionStorage.setItem("etc-intro", "1"); setTimeout(() => intro.remove(), 600); M.onIntroDone && M.onIntroDone(); };
    intro.addEventListener("click", end); setTimeout(end, 1250);
    M.introPending = true; M.endIntro = end;
  }
})();
