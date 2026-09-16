/* ==========================================================================
   ETC Labs — Gen 1 · Page initialisers (dispatched by <body data-page>)
   ========================================================================== */
(function () {
  "use strict";
  const M = window.ETC, R = M.render, esc = M.esc, icon = M.icon;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const arrow = M.icons.arrowRight, arrowUp = M.icons.arrow;

  /* ---------- Ecosystem visual (home hero) ---------- */
  function ecosystem(el) {
    const W = 560, H = 560, cx = W / 2, cy = H / 2, R1 = 205;
    const icons = { software: '<path d="m-5-4-4 4 4 4M5-4l4 4-4 4"/>', ai: '<circle r="4"/><path d="M0-9v3M0 6v3M-9 0h3M6 0h3"/>', products: '<path d="M-7-6h14v12H-7z"/><path d="M-3-2h6M-3 2h4"/>', infra: '<rect x="-8" y="-7" width="16" height="5" rx="1.5"/><rect x="-8" y="2" width="16" height="5" rx="1.5"/>', community: '<circle cx="-5" cy="2" r="2.5"/><circle cx="5" cy="-4" r="2.5"/><circle cx="5" cy="6" r="2.5"/><path d="M-2.8 1 2.6-3M-2.8 3l5.4 2.4"/>' };
    const nodes = M.build.map((b, i) => { const a = -Math.PI / 2 + (i / M.build.length) * Math.PI * 2; return { ...b, x: cx + Math.cos(a) * R1, y: cy + Math.sin(a) * R1 }; });
    const paths = nodes.map((n, i) => { const mx = (cx + n.x) / 2 + (n.y - cy) * 0.18, my = (cy + n.y) / 2 - (n.x - cx) * 0.18; return `<path class="link" d="M${cx} ${cy} Q${mx} ${my} ${n.x} ${n.y}"/><path class="pulse" d="M${cx} ${cy} Q${mx} ${my} ${n.x} ${n.y}" style="--d:${(i * 0.8).toFixed(1)}s"/>`; }).join("");
    const g = nodes.map((n, i) => `<a class="node" href="${n.href}" data-i="${i}" style="--c:${n.color}" data-cursor="Explore" aria-label="${esc(n.title)}"><g transform="translate(${n.x} ${n.y})"><circle class="halo" r="46"/><circle class="bg" r="40"/><g class="ico" transform="translate(0 -10)">${icons[n.key]}</g><text y="14">${esc(n.title === "Creator & community systems" ? "Community" : n.title)}</text><text y="27" class="sub">${esc(n.key === "community" ? "creator systems" : n.key === "products" ? "our own tools" : n.key === "infra" ? "deploy · scale" : n.key === "ai" ? "agents · automation" : "apps · tools")}</text></g></a>`).join("");
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="ETC Labs ecosystem: a core connected to Software, AI systems, Digital products, Infrastructure and Community">
      <defs><linearGradient id="eco-g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="0.6" stop-color="#8b5cf6"/><stop offset="1" stop-color="#e879f9"/></linearGradient><radialGradient id="eco-core" cx="0.35" cy="0.3"><stop offset="0" stop-color="#c4b5fd"/><stop offset="0.55" stop-color="#7c3aed"/><stop offset="1" stop-color="#2e1065"/></radialGradient><radialGradient id="eco-halo"><stop offset="0" stop-color="#8b5cf6" stop-opacity="0.5"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient></defs>
      <circle class="ring" cx="${cx}" cy="${cy}" r="${R1}"/><circle class="ring hi" cx="${cx}" cy="${cy}" r="${R1 - 60}"/><circle class="ring" cx="${cx}" cy="${cy}" r="${R1 + 48}"/>
      ${paths}
      <circle class="core-glow" cx="${cx}" cy="${cy}" r="110" fill="url(#eco-halo)"/>
      <g class="core"><circle cx="${cx}" cy="${cy}" r="58" fill="url(#eco-core)"/><circle cx="${cx}" cy="${cy}" r="58" fill="none" stroke="rgba(255,255,255,.25)"/><text class="core-text" x="${cx}" y="${cy + 6}">ETC</text></g>
      ${g}</svg><div class="eco-caption">${M.env.finePointer ? "hover a system · click to explore" : "tap a system to explore"}</div>`;
    // pointer parallax: nodes drift toward the cursor (transform only, rAF-throttled)
    if (M.env.finePointer && !M.env.reduce) {
      const els = $$(".node", el); let raf = null, px = 0, py = 0;
      el.addEventListener("pointermove", (e) => { const r = el.getBoundingClientRect(); px = (e.clientX - r.left) / r.width - 0.5; py = (e.clientY - r.top) / r.height - 0.5; if (!raf) raf = requestAnimationFrame(() => { els.forEach((n, i) => { const k = 6 + (i % 3) * 3; n.style.setProperty("--px", (px * k).toFixed(1) + "px"); n.style.setProperty("--py", (py * k).toFixed(1) + "px"); }); raf = null; }); }, { passive: true });
      el.addEventListener("pointerleave", () => els.forEach((n) => { n.style.setProperty("--px", "0px"); n.style.setProperty("--py", "0px"); }));
    }
  }

  /* ---------- Interactive "what we build" ---------- */
  function buildRows(list, visual) {
    list.innerHTML = `<div class="rows">${M.build.map((b, i) => `<a class="row" href="${b.href}" data-i="${i}" aria-selected="${i === 0}" data-reveal style="--i:${i}"><span class="num">0${i + 1}</span><div><h3>${esc(b.title)}</h3><p>${esc(b.text)}</p></div><span class="end link-arrow">${arrow}</span></a>`).join("")}</div>`;
    const show = (i) => { const b = M.build[i]; visual.innerHTML = `<div class="mock-wrap" style="--tone-rgb:${hexRgb(b.color)}">${M.mock(b.mock, accentName(b.color), true)}</div>`; $$(".row", list).forEach((r) => r.setAttribute("aria-selected", String(+r.dataset.i === i))); };
    list.addEventListener("pointerover", (e) => { const r = e.target.closest(".row"); if (r) show(+r.dataset.i); });
    list.addEventListener("focusin", (e) => { const r = e.target.closest(".row"); if (r) show(+r.dataset.i); });
    show(0);
  }
  const hexRgb = (h) => { const n = parseInt(h.slice(1), 16); return `${n >> 16}, ${(n >> 8) & 255}, ${n & 255}`; };
  const accentName = (h) => ({ "#22d3ee": "cyan", "#8b5cf6": "violet", "#e879f9": "magenta", "#60a5fa": "blue", "#34d399": "green" }[h] || "cyan");

  const pages = {
    home() {
      ecosystem($("#eco"));
      buildRows($("#build-rows"), $("#build-visual"));
      R.showcase($("#showcase"));
      R.projects($("#projects-strip"), M.projects.slice(0, 3), { featured: false });
      R.communityGraph($("#home-graph"));
    },
    "what-we-do"() {
      R.listDetail({ list: $("#svc-list"), detail: $("#svc-detail"), items: M.services.map((s) => ({ ...s, small: s.short })), key: "key", cursorLabel: "Select",
        render: (s) => `<div class="svc-detail"><div class="svc-visual mock-wrap">${M.mock(s.mock, s.accent, true)}</div><span class="kicker">${s.num} · ${esc(s.title)}</span><h2>${esc(s.title)}</h2><p class="lead">${esc(s.short)}</p>
          <div class="svc-grid"><div><h4>What we do</h4><p>${esc(s.what)}</p><h4 class="mt-3">Who it's for</h4><p>${esc(s.who)}</p></div><div class="svc-deliver"><h4>What you get</h4><ul class="list-check stack">${s.get.map((d) => `<li>${esc(d)}</li>`).join("")}</ul></div></div>
          <div class="cluster mt-4"><a class="btn btn-primary" href="contact.html?need=${encodeURIComponent(s.key)}">Discuss ${esc(s.title.toLowerCase())} ${arrowUp}</a><a class="link-arrow" href="projects.html">See related work ${arrow}</a></div></div>` });
    },
    products() { R.products($("#products")); R.roadmap($("#roadmap-list")); },
    projects() { const grid = $("#projects"); R.projects(grid); R.projectFilters($("#filters"), grid, $("#projects-empty")); },
    community() {
      R.communityGraph($("#graph")); R.communityWhy($("#why")); R.communityFeatures($("#features")); R.communityCards($("#members")); R.chips($("#who"), M.communityWho); R.creators($("#board"));
      R.roadmap($("#roadmap-list"), (r) => r.major || r.title.indexOf("Community") > -1);
    },
    about() { R.principles($("#principles")); R.team($("#team")); },
    careers() {
      const select = R.listDetail({ list: $("#role-list"), detail: $("#role-detail"), items: M.roles.map((r) => ({ ...r, small: `${r.team} · ${r.type}${r.remote ? " · Remote" : ""}` })), key: "key", cursorLabel: "View role",
        render: (r) => `<div class="role-detail"><span class="kicker">${esc(r.team)}</span><h2>${esc(r.title)}</h2><div class="role-meta"><span class="chip sm">${esc(r.type)}</span>${r.remote ? '<span class="chip sm">Remote</span>' : ""}<span class="chip sm">Applications open</span></div><p class="lead">${esc(r.summary)}</p>
          <div class="role-cols"><div><h4>What you'll do</h4><ul class="list-check stack">${r.doing.map((d) => `<li>${esc(d)}</li>`).join("")}</ul></div><div><h4>What we're looking for</h4><ul class="list-check stack">${r.looking.map((d) => `<li>${esc(d)}</li>`).join("")}</ul></div><div><h4>Nice to have</h4><ul class="list-check stack">${(r.nice || []).map((d) => `<li>${esc(d)}</li>`).join("")}</ul></div></div>
          <div class="cluster mt-4"><a class="btn btn-primary" href="#apply" data-apply="${r.key}">Apply for ${esc(r.title)} ${arrowUp}</a><span class="small muted">Pre-fills the form below.</span></div></div>` });
      M.selectRole = select;
    },
    contact() {
      const c = M.config;
      $$("[data-email]").forEach((a) => { a.textContent = c.email; a.href = "mailto:" + c.email; });
      $$("[data-email-btn]").forEach((a) => { a.href = "mailto:" + c.email; });
      $$("[data-copy-email]").forEach((b) => { b.dataset.copy = c.email; });
      $$("[data-instagram]").forEach((a) => { a.href = c.instagram.url; a.textContent = c.instagram.handle; });
    }
  };

  /* ---------- Shared behaviours ---------- */
  document.addEventListener("click", async (e) => {
    const b = e.target.closest("[data-copy]"); if (!b) return;
    try { await navigator.clipboard.writeText(b.dataset.copy); M.toast("Copied " + b.dataset.copy); } catch { M.toast(b.dataset.copy); }
  });

  document.addEventListener("DOMContentLoaded", () => {
    $$("h1[data-lines]").forEach(M.splitLines);
    const page = document.body.dataset.page;
    if (pages[page]) pages[page]();
    const go = () => { M.reveal(); if (location.hash && !document.getElementById(location.hash.slice(1))) return; if (location.hash) { const t = document.getElementById(location.hash.slice(1)); t && setTimeout(() => t.scrollIntoView({ behavior: M.env.reduce ? "auto" : "smooth", block: "start" }), 120); } };
    if (M.introPending) M.onIntroDone = go; else go();
    document.body.classList.remove("is-entering");
  });
})();
