/* ==========================================================================
   ETC Labs — Gen 1 · UI: nav, footer, reveals, toast, render helpers, product mocks
   ========================================================================== */
(function () {
  "use strict";
  const M = window.ETC;
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const icon = (k) => M.icons[k] || "";
  const arrow = M.icons.arrowRight, arrowUp = M.icons.arrow;
  M.esc = esc; M.icon = icon;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* ---------- Nav ---------- */
  class EtcNav extends HTMLElement {
    connectedCallback() {
      const cur = document.body.dataset.page || "";
      const isCur = (n) => n.key === cur || (n.children || []).some((c) => c.key === cur);
      const link = (n, extra = "") => `<a class="nav-link" href="${n.href}" ${isCur(n) ? 'aria-current="page"' : ""}>${esc(n.label)}${extra}</a>`;
      const groups = [...new Set(M.nav.map((n) => n.group))];
      const desktop = groups.map((g) => M.nav.filter((n) => n.group === g).map((n) => link(n)).join("")).join('<span class="nav-sep" aria-hidden="true"></span>');
      const mobile = groups.map((g) => `<div class="nav-group"><h4>${esc(g)}</h4>${M.nav.filter((n) => n.group === g).flatMap((n) => n.children ? [link({ ...n, label: n.label + " · all" }, arrow), ...n.children.map((c) => link(c, arrow))] : [link(n, arrow)]).join("")}</div>`).join("");
      this.innerHTML = `
        <header class="nav" id="site-nav"><div class="nav-inner">
          <a class="brand" href="index.html" aria-label="ETC Labs — Gen 1 — home" ${cur === "home" ? 'aria-current="page"' : ""}><img src="assets/img/etc-logo.svg" alt="ETC Labs" width="126" height="26"><span class="brand-tag">Gen 1</span></a>
          <nav class="nav-links" aria-label="Primary">${desktop}</nav>
          <div class="nav-right"><a class="btn btn-primary sm" href="${M.cta.href}">${esc(M.cta.label)} ${arrowUp}</a><button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-mobile"><span></span></button></div>
        </div></header>
        <div class="nav-mobile" id="nav-mobile" aria-label="Mobile navigation" hidden>
          <div class="nav-group"><h4>Start</h4><a class="nav-link" href="index.html" ${cur === "home" ? 'aria-current="page"' : ""}>Home${arrow}</a></div>${mobile}
          <a class="btn btn-primary solid lg block nav-mobile-cta" href="${M.cta.href}">${esc(M.cta.label)} ${arrowUp}</a>
          <p class="nav-mobile-foot">ETC Labs — Gen 1 · an independent technology showcase</p>
        </div>`;
      const toggle = $(".nav-toggle", this), panel = $(".nav-mobile", this);
      const setOpen = (open) => {
        toggle.setAttribute("aria-expanded", String(open)); toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
        panel.hidden = false; requestAnimationFrame(() => panel.classList.toggle("open", open));
        document.body.style.overflow = open ? "hidden" : "";
        if (!open) setTimeout(() => { if (!panel.classList.contains("open")) panel.hidden = true; }, 300);
        if (open) setTimeout(() => panel.querySelector("a")?.focus(), 320);
      };
      toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
      panel.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
      document.addEventListener("keydown", (e) => { if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { setOpen(false); toggle.focus(); } });
      addEventListener("resize", () => { if (innerWidth >= 1100 && toggle.getAttribute("aria-expanded") === "true") setOpen(false); });
    }
  }
  customElements.define("etc-nav", EtcNav);

  /* ---------- Footer ---------- */
  class EtcFooter extends HTMLElement {
    connectedCallback() {
      const c = M.config, year = new Date().getFullYear();
      const group = (title, links) => `<div class="fgroup"><h4>${title}<button type="button" aria-label="Toggle ${title}" aria-expanded="false">+</button></h4><nav class="footer-links" aria-label="Footer ${title}">${links}</nav></div>`;
      this.innerHTML = `<footer class="footer"><div class="footer-inner"><div class="footer-grid">
          <div class="footer-brand"><a class="brand" href="index.html" aria-label="ETC Labs — Gen 1 — home"><img src="assets/img/etc-logo.svg" alt="ETC Labs" width="126" height="26"></a><p>ETC Labs — Gen 1 is an independent technology showcase: software, AI systems, digital products, infrastructure and a creator community — designed, built and deployed as one project.</p>
            <div class="social mt-2"><a href="${esc(c.instagram.url)}" target="_blank" rel="noopener noreferrer" aria-label="Instagram ${esc(c.instagram.handle)}" data-cursor="Open">${icon("instagram")}</a><a href="mailto:${esc(c.email)}" aria-label="Email ${esc(c.email)}" data-cursor="Email">${icon("mail")}</a></div></div>
          ${group("Explore", `<a href="index.html">Home</a><a href="what-we-do.html">What We Build</a><a href="products.html">Products</a><a href="projects.html">Projects</a>`)}
          ${group("Tools", `<a href="transfer.html">Transfer</a><a href="voice.html">Voice Rooms</a><a href="ai.html">AI Utilities</a><a href="toolkit.html">Creator Toolkit</a>`)}
          ${group("Lab", `<a href="community.html">Community</a><a href="about.html">About</a><a href="careers.html">Careers</a><a href="contact.html">Contact</a>`)}
          ${group("Contact", `<a href="mailto:${esc(c.email)}">${esc(c.email)}</a><a href="${esc(c.instagram.url)}" target="_blank" rel="noopener noreferrer">Instagram ${esc(c.instagram.handle)}</a><a href="${esc(c.github)}" target="_blank" rel="noopener noreferrer">Source on GitHub</a>`)}
        </div><div class="footer-bottom"><span>© ${year} ETC Labs — Gen 1 · Independent showcase, not affiliated with MXT</span><span class="status-dot"><i></i>ETC Labs is building</span></div></div></footer>`;
      $$(".fgroup h4", this).forEach((h) => h.addEventListener("click", () => { const g = h.parentElement, open = !g.classList.contains("open"); g.classList.toggle("open", open); h.querySelector("button").setAttribute("aria-expanded", String(open)); }));
    }
  }
  customElements.define("etc-footer", EtcFooter);

  /* ---------- Reveal ---------- */
  M.reveal = () => {
    const els = $$("[data-reveal]:not(.in), .lines:not(.in)");
    if (M.env.reduce || !("IntersectionObserver" in window)) { els.forEach((e) => e.classList.add("in")); return; }
    const io = new IntersectionObserver((entries) => { entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { rootMargin: "0px 0px -4% 0px", threshold: 0.04 });
    els.forEach((e) => { const r = e.getBoundingClientRect(); if (r.top < innerHeight * 0.92 && r.bottom > 0) e.classList.add("in"); else io.observe(e); });
  };
  /* Split a heading into animated lines: <h1 class="lines"><span><span>text</span></span>… */
  M.splitLines = (el) => { const parts = el.innerHTML.split("<br>"); el.innerHTML = parts.map((p, i) => `<span><span style="--n:${i}">${p.trim()}</span></span>`).join(""); el.classList.add("lines"); };

  /* ---------- Toast ---------- */
  let toastEl;
  M.toast = (msg) => { if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); } toastEl.textContent = msg; toastEl.classList.add("show"); clearTimeout(toastEl._t); toastEl._t = setTimeout(() => toastEl.classList.remove("show"), 3200); };

  /* ---------- Product UI mocks ---------- */
  const bar = (l) => `<div class="bar"><i></i><i></i><i></i><span>${l}</span></div>`;
  const wave = [35, 60, 80, 55, 90, 45, 70, 30, 65, 85, 50, 40, 75, 55, 30].map((h, k) => `<i style="--h:${h}%;--k:${k}"></i>`).join("");
  const mocks = {
    transfer: () => `${bar("Transfer")}<div class="box"><b>Drop a file</b>No account · link expires in 24h</div><div class="row2"><i></i><b>launch-cut_v3.mp4</b><span>1.2 GB</span></div><div class="prog"><i></i></div><div class="pill"><i></i>etc.link/k9f2 · copied</div>`,
    voice: () => `${bar("Voice Rooms")}<div class="avs"><i class="on"></i><i class="on"></i><i></i><i></i></div><div class="wave">${wave}</div><div class="pill"><i></i>4 in room · 38 ms</div><div class="btns"><i></i><i class="k"></i><i></i></div>`,
    ai: () => `${bar("AI Utilities")}<div class="prompt">Turn this recording into chapters + a summary</div><div class="out"><div class="line w80" style="--k:0"></div><div class="line w60" style="--k:1"></div><div class="line w40" style="--k:2"></div></div><div class="pill"><i></i>Done · 3 chapters</div>`,
    members: () => `${bar("Submissions Admin")}<div class="grid4"><i class="k"></i><i></i><i></i><i class="k"></i><i></i><i class="k"></i><i></i><i></i></div><div class="pill"><i></i>Admin only</div>`,
    community: () => `${bar("Creator Directory")}<div class="chan"><div class="side"><i class="on"></i><i></i><i></i><i></i><i></i></div><div class="msgs"><div class="msg"><i></i><div class="line w80"></div></div><div class="msg"><i></i><div class="line w60"></div></div><div class="msg"><i></i><div class="line w40"></div></div></div></div><div class="pill"><i></i>#creators · verified</div>`,
    toolkit: () => `${bar("Creator Toolkit")}<div class="check"><div><i class="k"></i>Plan this week</div><div><i class="k"></i>Publish schedule</div><div><i></i>Collab request</div><div><i></i>Asset library</div></div>`,
    infra: () => `${bar("Deployment")}<div class="log"><div><b>→</b> build  ok  12.4s</div><div><b>→</b> deploy pages  ok</div><div><b>→</b> health  200  38ms</div><div><b>→</b> rollback  ready</div></div><div class="pill"><i></i>3 services · healthy</div>`,
    world: () => `${bar("World background · 60 fps")}<div class="worldp"><i class="l1"></i><i class="l2"></i><i class="g"></i><span>tone: violet → cyan</span></div><div class="pill"><i></i>4× CPU throttle · 60 fps</div>`,
    tools: () => `${bar("Web tools")}<div class="row2"><i></i><b>Link shortener</b><span>ready</span></div><div class="row2"><i></i><b>Image resize</b><span>ready</span></div><div class="row2"><i></i><b>Quick share</b><span>soon</span></div>`,
    brand: () => `${bar("ETC Labs design system")}<div class="type">Aa</div><div class="swatches"><i style="background:#07070b;border:1px solid var(--line)"></i><i style="background:#22d3ee"></i><i style="background:#8b5cf6"></i><i style="background:#e879f9"></i></div><div class="line w60"></div><div class="line w40"></div>`
  };
  M.mock = (type, accent = "cyan", live = false) => `<div class="mock ${esc(accent)} ${live ? "live" : ""}" aria-hidden="true">${(mocks[type] || mocks.tools)()}</div>`;

  /* ---------- Render helpers ---------- */
  const R = (M.render = {});
  const productCta = (p) => p.cta ? `<a class="link-arrow" href="${p.cta.href}" data-cursor="Explore">${esc(p.cta.label)} ${arrow}</a>` : `<span class="tag">No public page yet</span>`;

  R.products = (el) => {
    el.innerHTML = M.productGroups.map((g) => {
      const head = `<div class="product-group-head" data-reveal><span class="badge ${g.badge}">${esc(g.label)}</span><h2 id="pg-${g.key}" class="sr-only">${esc(g.label)} products</h2><p>${esc(g.intro)}</p></div>`;
      const body = `<div class="product-grid">${g.items.map((p, i) => `<article class="product-item" data-reveal style="--i:${i}" data-expand>${M.mock(p.mock, p.accent, true)}<div class="body"><div class="head-row"><h3 style="margin:0">${esc(p.name)}</h3><span class="badge ${g.badge} live-pulse">${esc(p.status)}</span></div><p class="mt-1">${esc(p.tagline)}</p>
        <button class="expand-toggle" type="button" aria-expanded="false"><span>Details</span>${arrow}</button>
        <div class="expandable"><div class="problem"><span>Problem it solves</span><p>${esc(p.problem)}</p></div><ul class="keys">${p.keys.map((k) => `<li>${esc(k)}</li>`).join("")}</ul><div class="who-for">${p.who.map((w) => `<span class="chip sm">${esc(w)}</span>`).join("")}</div></div>
        <div class="foot"><a class="btn btn-primary sm" href="${p.cta.href}">${esc(p.cta.label)} ${arrowUp}</a></div></div></article>`).join("")}</div>`;
      return `<section class="product-group" id="${g.key}" aria-labelledby="pg-${g.key}">${head}${body}${M.productStatusNote ? `<p class="small muted mt-3" data-reveal>${esc(M.productStatusNote)}</p>` : ""}</section>`;
    }).join("");
    M.wireExpand(el);
  };

  /* Touch-first expand/collapse for cards: on phones details are collapsed behind a "Details" toggle; on wide screens everything is shown. */
  M.wireExpand = (root) => {
    $$("[data-expand] .expand-toggle", root).forEach((btn) => btn.addEventListener("click", () => {
      const card = btn.closest("[data-expand]"), open = !card.classList.contains("open");
      card.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open)); btn.querySelector("span").textContent = open ? "Less" : "Details";
    }));
  };

  R.showcase = (el) => {
    const picks = M.productGroups[0].items.slice(0, 3), badge = ["badge-live", "badge-live", "badge-live"];
    el.innerHTML = picks.map((p, i) => `<div class="showcase ${i % 2 ? "flip" : ""}" data-reveal><div class="mock-wrap">${M.mock(p.mock, p.accent, true)}</div><div><span class="badge ${badge[i]}">${esc(p.status)}</span><h3>${esc(p.name)}</h3><p>${esc(p.tagline)}</p><p class="small muted">${esc(p.problem)}</p><div class="mt-2">${productCta(p)}</div></div></div>`).join("");
  };

  R.projects = (el, list = M.projects, { featured = true } = {}) => {
    el.innerHTML = list.map((p, i) => {
      const links = (p.links && p.links.length ? p.links : [{ label: "Details", href: "products.html" }]).map((l) => `<a class="link-arrow" href="${esc(l.href)}" ${l.external ? 'target="_blank" rel="noopener noreferrer"' : ""}>${esc(l.label)} ${l.external ? arrowUp : arrow}</a>`).join("");
      const isF = featured && i === 0;
      return `<article class="project ${isF ? "featured" : ""}" id="${p.id}" data-cat="${p.category}" data-reveal style="--i:${i % 6}">
        <div class="visual" data-cursor="${isF ? "Featured" : "View"}">${M.mock(p.mock, p.accent, isF)}<div class="overlay"><div class="meta-list"><span class="chip sm">${esc(p.approach)}</span></div></div></div>
        <div><div class="meta"><span class="tag">${esc(p.catLabel)}</span><span class="badge ${p.badge}">${esc(p.status)}</span></div><h3>${esc(p.name)}</h3><p>${esc(p.desc)}</p>
        ${isF ? `<div class="q"><div><b>Problem</b><span>${esc(p.problem)}</span></div><div><b>What we built</b><span>${esc(p.built)}</span></div><div><b>Approach</b><span>${esc(p.approach)}</span></div></div>` : ""}
        <div class="foot"><span class="tech">${p.focus.map(esc).join(" · ")}</span><span class="links">${links}</span></div></div></article>`;
    }).join("");
  };

  R.projectFilters = (el, grid, emptyEl) => {
    const counts = M.projects.reduce((a, p) => ((a[p.category] = (a[p.category] || 0) + 1), a), { all: M.projects.length });
    el.innerHTML = M.projectCategories.map((c) => `<button class="filter-btn" type="button" data-filter="${c.key}" aria-pressed="${c.key === "all"}">${esc(c.label)}<span class="count">${counts[c.key] || 0}</span></button>`).join("");
    el.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn"); if (!btn) return;
      $$(".filter-btn", el).forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      const key = btn.dataset.filter; let shown = 0;
      Array.from(grid.children).forEach((card) => {
        const show = key === "all" || card.dataset.cat === key; if (show) shown++;
        if (show) { card.classList.remove("is-hidden"); requestAnimationFrame(() => card.classList.remove("is-hiding")); }
        else { card.classList.add("is-hiding"); setTimeout(() => { if (card.classList.contains("is-hiding")) card.classList.add("is-hidden"); }, 280); }
      });
      if (emptyEl) emptyEl.hidden = shown > 0;
    });
  };

  R.communityFeatures = (el) => { el.innerHTML = `<div class="feature-grid">${M.communityFeatures.map((f, i) => { const [cls, lbl] = M.communityStatus[f.status]; const tag = f.href ? "a" : "div"; return `<${tag} ${f.href ? `href="${esc(f.href)}" data-cursor="Open"` : ""} data-reveal style="--i:${i}"><span class="badge ${cls} status">${lbl}</span><span class="icon">${icon(f.icon)}</span><h3>${esc(f.title)}</h3><p>${esc(f.text)}</p><span class="tag">${esc(f.tag)}${f.href ? " " + arrow : ""}</span></${tag}>`; }).join("")}</div>`; };
  R.communityWhy = (el) => { el.innerHTML = M.communityWhy.map((w, i) => `<div class="why-item" data-reveal style="--i:${i}"><span class="n">0${i + 1}</span><h3>${esc(w.title)}</h3><p>${esc(w.text)}</p></div>`).join(""); };
  R.chips = (el, list) => { el.innerHTML = list.map((t) => `<span class="chip">${esc(t)}</span>`).join(""); };

  R.communityGraph = (el) => {
    const W = 640, H = 440, cx = W / 2, cy = H / 2, r = 160;
    const nodes = M.communityDemo.map((m, i) => { const a = -Math.PI / 2 + (i / M.communityDemo.length) * Math.PI * 2; return { ...m, i, x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r }; });
    const lines = nodes.map((n) => `<line x1="${n.x}" y1="${n.y}" x2="${cx}" y2="${cy}" class="cg-link" data-n="${n.i}"/>`).join("");
    const cross = nodes.map((n, i) => { const m = nodes[(i + 2) % nodes.length]; return `<line x1="${n.x}" y1="${n.y}" x2="${m.x}" y2="${m.y}" class="cg-link faint" data-n="${n.i}" data-m="${m.i}"/>`; }).join("");
    const dots = nodes.map((n, i) => `<g class="cg-node" data-n="${i}" tabindex="0" role="img" aria-label="${esc(n.role)} — ${esc(n.skill)} (demo)"><circle cx="${n.x}" cy="${n.y}" r="32" class="bg" stroke="${n.color}" stroke-width="1.5"/><circle cx="${n.x}" cy="${n.y}" r="32" fill="none" stroke="${n.color}" class="cg-ring" style="--d:${i * 0.7}s"/><text x="${n.x}" y="${n.y - 3}" text-anchor="middle" class="cg-role">${esc(n.role)}</text><text x="${n.x}" y="${n.y + 12}" text-anchor="middle" class="cg-skill">${esc(n.skill)}</text></g>`).join("");
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Diagram: six creator roles connected to a shared project" class="cg"><defs><linearGradient id="cg-core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#e879f9"/></linearGradient></defs><g>${cross}${lines}</g><g><circle cx="${cx}" cy="${cy}" r="54" fill="url(#cg-core)"/><text x="${cx}" y="${cy - 2}" text-anchor="middle" class="cg-core-t">PROJECT</text><text x="${cx}" y="${cy + 14}" text-anchor="middle" class="cg-core-s">built together</text></g>${dots}</svg>`;
    // hover a member → its connections light up
    el.addEventListener("pointerover", (e) => { const n = e.target.closest(".cg-node"); if (!n) return; $$(`.cg-link[data-n="${n.dataset.n}"], .cg-link[data-m="${n.dataset.n}"]`, el).forEach((l) => l.classList.add("hot")); });
    el.addEventListener("pointerout", (e) => { const n = e.target.closest(".cg-node"); if (!n) return; $$(".cg-link.hot", el).forEach((l) => l.classList.remove("hot")); });
  };
  R.communityCards = (el) => { el.innerHTML = `<div class="members">${M.communityDemo.map((m, i) => `<div class="member" data-reveal style="--i:${i}"><span class="avatar" style="background:linear-gradient(135deg,${m.color},#4c1d95)">${esc(m.role[0])}</span><div><b>${esc(m.role)}</b><span>${esc(m.skill)} · illustration</span></div></div>`).join("")}</div>`; };

  R.creators = (el) => {
    const L = M.creators; let sortBy = "joined", totals = null;
    const avatar = (r) => r.avatarUrl ? `<span class="avatar img"><img src="${esc(r.avatarUrl)}" alt="" width="44" height="44" loading="lazy" decoding="async"><b aria-hidden="true">${esc(r.name[0])}</b></span>` : `<span class="avatar">${esc(r.name[0])}</span>`;
    const pts = (r) => totals && totals[r.handle] ? totals[r.handle] : null;
    const draw = () => {
      const rows = [...L.rows]; if (sortBy === "points") rows.sort((a, b) => ((pts(b) && pts(b).points) || 0) - ((pts(a) && pts(a).points) || 0) || a.rank - b.rank);
      el.innerHTML = `<div class="board" data-reveal><div class="board-head"><span class="kicker" style="margin:0">Creators</span><div class="board-sort" role="group" aria-label="Ranking"><button class="filter-btn" type="button" data-sort="joined" aria-pressed="${sortBy === "joined"}">Joined date</button><button class="filter-btn" type="button" data-sort="points" aria-pressed="${sortBy === "points"}" ${totals ? "" : 'disabled title="Contribution points load from the backend"'}>Contributions</button></div><span class="small muted">verified ${esc(L.verifiedAt)}</span></div><div class="board-row head" aria-hidden="true"><span>Rank</span><span>Creator</span><span>Audience</span><span>Contribution</span><span>Channel</span></div>
        ${rows.map((r, i) => { const c = pts(r); return `<div class="board-row ${i === 0 ? "top" : ""}" data-reveal style="--i:${i}"><span class="rank">#${String(sortBy === "points" ? i + 1 : r.rank).padStart(2, "0")}</span><span class="creator">${avatar(r)}<span><span class="name">${esc(r.name)}</span><span class="handle">${esc(r.handle)}</span></span></span><span class="stat">${r.subscribers ? esc(r.subscribers) : "—"}<small>${r.subscribers ? esc(r.platform) + " subscribers" : "count unavailable"}</small></span><span class="stat pts">${c ? c.points : "—"}<small>${c ? c.count + " verified" : totals ? "none yet" : "points"}</small></span><span class="action"><a class="btn btn-secondary sm" href="${esc(r.channelUrl)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${esc(r.name)} on ${esc(r.platform)}" data-cursor="Open">Channel ${arrowUp}</a></span></div>`; }).join("")}
        <div class="board-row" style="grid-template-columns:1fr"><span class="small muted center">${esc(L.note)} Contribution points are recorded by ETC Labs for verified work (projects, collaborations, events, content) and cannot be edited by creators.</span></div></div>`;
      $$(".avatar.img img", el).forEach((img) => { img.addEventListener("error", () => img.parentElement.classList.add("broken")); if (img.complete && img.naturalWidth === 0) img.parentElement.classList.add("broken"); });
      $$("[data-sort]", el).forEach((b) => b.addEventListener("click", () => { sortBy = b.dataset.sort; draw(); }));
      M.reveal();
    };
    draw();
    // contribution points come from the backend; without one the column shows "—" and the toggle stays disabled
    const API = M.config.apiBase; const staticHost = !API && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
    if (!staticHost) fetch(API + "/api/community/contributions").then((r) => r.json()).then((d) => { if (d && d.ok) { totals = Object.fromEntries(d.totals.map((t) => [t.handle, t])); draw(); } }).catch(() => {});
  };

  R.roadmap = (el, filter) => {
    const items = filter ? M.roadmap.filter(filter) : M.roadmap;
    el.innerHTML = `<ol class="timeline">${items.map((r, i) => `<li class="tl-item ${r.major ? "major" : "minor"}" data-status="${r.status}" data-reveal style="--i:${i}"><div class="panel"><div class="tl-meta"><h3>${esc(r.title)}</h3><span class="badge ${M.roadmapBadge[r.status]}">${esc(r.label)}</span></div><p>${esc(r.what)}</p>${typeof r.progress === "number" ? `<div class="progress ${r.status === "done" ? "done" : ""} mt-2" role="progressbar" aria-valuenow="${r.progress}" aria-valuemin="0" aria-valuemax="100" aria-label="${esc(r.title)} progress"><i data-w="${r.progress}%"></i></div>` : ""}<div class="tl-why"><strong>Why it matters</strong>${esc(r.why)}</div></div></li>`).join("")}</ol>`;
    $$(".progress > i[data-w]", el).forEach((b) => { const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { b.style.width = b.dataset.w; io.disconnect(); } }); io.observe(b); });
  };

  R.founder = (el) => {
    const f = M.founder;
    el.innerHTML = `<article class="founder" data-reveal="scale" aria-labelledby="founder-name">
      <div class="founder-mark"><picture>${f.imageWebp ? `<source srcset="${esc(f.imageWebp)}" type="image/webp">` : ""}<img src="${esc(f.image)}" alt="${esc(f.imageAlt)}" width="512" height="512" decoding="async"></picture></div>
      <div class="founder-body"><span class="kicker">${esc(f.label)}</span><h3 id="founder-name">${esc(f.name)}</h3><span class="role">${esc(f.role)}</span><p>${esc(f.text)}</p>${f.quote ? `<p class="team-quote">“${esc(f.quote)}”</p>` : ""}
        ${f.focus ? `<div class="cluster mt-2" aria-label="Focus areas">${f.focus.map((x) => `<span class="chip sm">${esc(x)}</span>`).join("")}</div>` : ""}
        ${f.links ? `<div class="cluster mt-3">${f.links.map((l) => `<a class="link-arrow" href="${esc(l.href)}" ${l.external ? 'target="_blank" rel="noopener noreferrer"' : ""}>${esc(l.label)} ${arrowUp}</a>`).join("")}</div>` : ""}</div></article>`;
    const img = el.querySelector(".founder-mark img"); img && img.addEventListener("error", () => el.querySelector(".founder-mark").classList.add("broken"));
  };
  R.team = (el) => { el.innerHTML = M.team.map((t, i) => `<div class="team" data-reveal style="--i:${i}"><span class="avatar lg">${esc(t.name[0])}</span><h3>${esc(t.name)}</h3><span class="role">${esc(t.role)}</span><p>${esc(t.text)}</p>${t.quote ? `<p class="team-quote">“${esc(t.quote)}”</p>` : ""}${t.links ? `<div class="cluster mt-2">${t.links.map((l) => `<a class="link-arrow" href="${esc(l.href)}" ${l.external ? 'target="_blank" rel="noopener noreferrer"' : ""}>${esc(l.label)} ${arrowUp}</a>`).join("")}</div>` : ""}</div>`).join(""); };
  R.principles = (el) => { el.innerHTML = M.principles.map((p, i) => `<div class="principle" data-reveal style="--i:${i}"><span class="tag">${esc(p.tag)}</span><h3>${esc(p.title)}</h3><p>${esc(p.text)}</p></div>`).join(""); };

  /* Generic list + detail (services, roles): buttons on the left, content on the right, hash-addressable */
  R.listDetail = ({ list, detail, items, render, key, cursorLabel }) => {
    const byKey = Object.fromEntries(items.map((it) => [it[key], it]));
    list.innerHTML = items.map((it, i) => `<button class="ld-item" type="button" role="tab" data-key="${it[key]}" aria-selected="false" ${cursorLabel ? `data-cursor="${cursorLabel}"` : ""}><span class="num">${String(i + 1).padStart(2, "0")}</span><span><b>${esc(it.title)}</b><small>${esc(it.small || "")}</small></span>${arrow}</button>`).join("");
    const select = (k, push = true) => {
      const it = byKey[k] || items[0];
      $$(".ld-item", list).forEach((b) => b.setAttribute("aria-selected", String(b.dataset.key === it[key])));
      detail.innerHTML = render(it);
      if (push && history.replaceState) history.replaceState(null, "", "#" + it[key]);
      M.reveal();
    };
    list.addEventListener("click", (e) => { const b = e.target.closest(".ld-item"); if (b) { select(b.dataset.key); if (innerWidth < 900) detail.scrollIntoView({ behavior: M.env.reduce ? "auto" : "smooth", block: "start" }); } });
    const initial = location.hash.slice(1);
    select(byKey[initial] ? initial : items[0][key], false);
    addEventListener("hashchange", () => { const k = location.hash.slice(1); if (byKey[k]) select(k, false); });
    return select;
  };
})();

