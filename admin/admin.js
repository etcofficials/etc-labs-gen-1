/* ETC Labs admin — vanilla SPA over /api/admin. Hash routes: #/dashboard, #/applications, #/applications/:id, #/requests, #/requests/:id */
(function () {
  "use strict";
  const app = document.getElementById("app");
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (t) => t ? new Date(t * 1000).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) : "—";
  const ago = (t) => { const d = (Date.now() / 1000 - t); if (d < 3600) return Math.max(1, Math.round(d / 60)) + "m ago"; if (d < 86400) return Math.round(d / 3600) + "h ago"; return Math.round(d / 86400) + "d ago"; };
  const POS = { "video-editor": "Video Editor", "community-mod": "Community Moderator", "web-dev": "Web / Backend Developer", "ai-engineer": "AI / Automation Engineer", "creator-research": "Creator Research", "other": "Other / general" };
  const NEED = { software: "Software", ai: "AI & automation", design: "Product & UI design", infrastructure: "Infrastructure", security: "Security", creative: "Creative", unsure: "Not sure" };
  const STATUS = { application: ["new", "reviewing", "shortlisted", "interview", "rejected", "hired"], request: ["new", "reviewing", "replied", "scoping", "won", "closed"] };
  let me = null, summary = null;

  const api = async (path, opts = {}) => {
    const res = await fetch("/api/admin" + path, { credentials: "same-origin", ...opts, headers: { "X-ETC-Admin": "1", ...(opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : {}), ...(opts.headers || {}) } });
    if (res.status === 401 && path !== "/login") { const wasIn = me !== null; me = null; if (wasIn) renderLogin("Your session expired. Please sign in again."); throw new Error("Not signed in"); }
    let data = null; try { data = await res.json(); } catch {}
    if (!res.ok) throw new Error((data && (data.error || data.detail)) || `Request failed (${res.status})`);
    return data;
  };
  let toastEl; const toast = (m) => { if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; document.body.appendChild(toastEl); } toastEl.textContent = m; toastEl.classList.add("show"); clearTimeout(toastEl._t); toastEl._t = setTimeout(() => toastEl.classList.remove("show"), 2600); };

  /* ---------- Login ---------- */
  const renderLogin = (msg = "") => {
    app.innerHTML = `<div class="login"><form id="login"><h1><img src="/admin/logo.svg" alt="ETC Labs">Admin</h1>${msg ? `<div class="error">${esc(msg)}</div>` : ""}<div><label for="u">Username</label><input class="input" id="u" name="username" autocomplete="username" required></div><div><label for="p">Password</label><input class="input" id="p" name="password" type="password" autocomplete="current-password" required></div><button class="btn primary" type="submit">Sign in</button><p class="hint">Internal ETC Labs dashboard. Sessions expire after 12 hours.</p></form></div>`;
    const f = document.getElementById("login");
    f.addEventListener("submit", async (e) => {
      e.preventDefault(); const b = f.querySelector("button"); b.disabled = true; b.textContent = "Signing in…";
      try { const r = await api("/login", { method: "POST", body: JSON.stringify({ username: f.username.value, password: f.password.value }) }); me = r.user; location.hash = location.hash || "#/dashboard"; render(); }
      catch (err) { renderLogin(err.message); }
    });
    setTimeout(() => document.getElementById("u")?.focus(), 50);
  };

  /* ---------- Shell ---------- */
  const shell = (title, sub, body, active) => {
    const s = summary || {};
    const nav = (href, label, count, key) => `<a href="${href}" class="${active === key ? "on" : ""}">${label}${count != null ? `<span class="count">${count}</span>` : ""}</a>`;
    app.innerHTML = `<div class="shell"><aside class="side"><div class="brand"><img src="/admin/logo.svg" alt="ETC Labs"> <span>ADMIN</span></div>
      ${nav("#/dashboard", "Dashboard", null, "dashboard")}${nav("#/applications", "Applications", s.applications_total, "applications")}${nav("#/requests", "Project requests", s.requests_total, "requests")}${nav("#/settings", "Settings", null, "settings")}
      <div class="foot"><span>Signed in as <b>${esc(me)}</b></span><button id="logout" type="button">Sign out</button><a href="/" target="_blank" rel="noopener">View site ↗</a></div></aside>
      <main class="main"><div class="topbar"><div><h1>${title}</h1><div class="sub">${sub}</div></div><div id="topbar-actions"></div></div><div id="view">${body}</div></main></div>`;
    document.getElementById("logout").addEventListener("click", async () => { await api("/logout", { method: "POST" }); me = null; render(); });
  };
  const loadSummary = async () => { const r = await api("/summary"); summary = r.summary; summary._activity = r.activity; };

  /* ---------- Dashboard ---------- */
  const renderDashboard = async () => {
    await loadSummary(); const s = summary;
    const stat = (n, l, hot) => `<div class="stat ${hot ? "hot" : ""}"><b>${n}</b><span>${l}</span></div>`;
    shell("Dashboard", "What needs attention", `
      <div class="stats">${stat(s.applications.new, "New applications", s.applications.new > 0)}${stat(s.requests.new, "New project requests", s.requests.new > 0)}${stat(s.applications.reviewing + s.requests.reviewing, "Reviewing")}${stat(s.applications.shortlisted, "Shortlisted")}${stat(s.applications.interview, "Interview")}${stat(s.applications_week + " / " + s.requests_week, "This week (apps / requests)")}</div>
      ${s.demo_rows ? `<div class="ok">${s.demo_rows} demo rows are in the database (labelled DEMO). Remove with <code>python -m server.cli purge-demo</code>.</div>` : ""}
      <div class="two"><div class="panel"><div class="hd">Latest applications <a class="btn sm" href="#/applications">All</a></div><div class="bd" id="dash-apps"><div class="loading">Loading…</div></div></div><div class="panel"><div class="hd">Latest project requests <a class="btn sm" href="#/requests">All</a></div><div class="bd" id="dash-reqs"><div class="loading">Loading…</div></div></div></div>
      <div class="panel" style="margin-top:14px"><div class="hd">Recent activity</div><div class="bd activity">${(s._activity || []).map((a) => `<div><time>${esc(fmt(a.created_at))}</time><span>${esc(a.actor)} · ${esc(a.action)} ${a.target ? `<a href="#/${a.action.startsWith("application") ? "applications" : "requests"}/${esc(a.target)}">${esc(a.target)}</a>` : ""}</span></div>`).join("") || '<div class="empty">No activity yet.</div>'}</div></div>`, "dashboard");
    const [a, r] = await Promise.all([api("/applications"), api("/requests")]);
    document.getElementById("dash-apps").innerHTML = a.items.length ? a.items.slice(0, 6).map((i) => `<div style="display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)"><a href="#/applications/${i.id}">${esc(i.first_name)} ${esc(i.last_name)}${i.is_demo ? '<span class="demo">DEMO</span>' : ""}<span class="sub">${esc(POS[i.position] || i.position)} · ${ago(i.created_at)}</span></a><span class="status ${i.status}">${i.status}</span></div>`).join("") : '<div class="empty">No applications yet.</div>';
    document.getElementById("dash-reqs").innerHTML = r.items.length ? r.items.slice(0, 6).map((i) => `<div style="display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)"><a href="#/requests/${i.id}">${esc(i.name)}${i.is_demo ? '<span class="demo">DEMO</span>' : ""}<span class="sub">${esc(i.building)} · ${ago(i.created_at)}</span></a><span class="status ${i.status}">${i.status}</span></div>`).join("") : '<div class="empty">No project requests yet.</div>';
  };

  /* ---------- Lists ---------- */
  const listState = { applications: { q: "", status: "", position: "", archived: 0 }, requests: { q: "", status: "", need: "", archived: 0 } };
  const renderList = async (kind) => {
    const isApp = kind === "applications", st = listState[kind];
    if (!summary) await loadSummary();
    const opts = (o, cur) => Object.entries(o).map(([k, v]) => `<option value="${k}" ${k === cur ? "selected" : ""}>${esc(v)}</option>`).join("");
    shell(isApp ? "Applications" : "Project requests", isApp ? "Everyone who applied through the site" : "Everyone who asked ETC Labs to build something", `
      <form class="filters" id="filters"><div><label>Search</label><input class="input" name="q" value="${esc(st.q)}" placeholder="${isApp ? "Name, email or Discord" : "Name, email or Discord"}"></div>
        <div><label>Status</label><select class="select" name="status"><option value="">All</option>${opts(Object.fromEntries(STATUS[isApp ? "application" : "request"].map((s) => [s, s])), st.status)}</select></div>
        <div><label>${isApp ? "Position" : "Need"}</label><select class="select" name="${isApp ? "position" : "need"}"><option value="">All</option>${opts(isApp ? POS : NEED, isApp ? st.position : st.need)}</select></div>
        <div><label>Show</label><select class="select" name="archived"><option value="0" ${!st.archived ? "selected" : ""}>Active</option><option value="1" ${st.archived ? "selected" : ""}>Archived</option></select></div>
        <button class="btn" type="submit">Apply</button></form>
      <div id="list"><div class="loading">Loading…</div></div>`, kind);
    document.getElementById("filters").addEventListener("submit", (e) => { e.preventDefault(); const f = new FormData(e.target); st.q = f.get("q"); st.status = f.get("status"); if (isApp) st.position = f.get("position"); else st.need = f.get("need"); st.archived = +f.get("archived"); load(); });
    const load = async () => {
      const q = new URLSearchParams({ q: st.q, status: st.status, archived: st.archived, ...(isApp ? { position: st.position } : { need: st.need }) });
      try {
        const r = await api(`/${kind}?${q}`);
        document.getElementById("list").innerHTML = r.items.length ? `<div class="table-wrap"><table><thead><tr>${isApp ? "<th>Name</th><th>Position</th><th>Contact</th><th>Resume</th>" : "<th>Name</th><th>Building</th><th>Need</th><th>Scale</th>"}<th>Submitted</th><th>Status</th><th>Notes</th></tr></thead><tbody>${r.items.map((i) => isApp
          ? `<tr data-href="#/applications/${i.id}"><td><b>${esc(i.first_name)} ${esc(i.last_name)}</b>${i.is_demo ? '<span class="demo">DEMO</span>' : ""}</td><td>${esc(POS[i.position] || i.position)}</td><td>${esc(i.email)}<span class="sub">${esc(i.discord)}</span></td><td>${i.resume_path ? "yes" : "—"}</td><td>${esc(fmt(i.created_at))}<span class="sub">${ago(i.created_at)}</span></td><td><span class="status ${i.status}">${i.status}</span></td><td>${i.note_count || ""}</td></tr>`
          : `<tr data-href="#/requests/${i.id}"><td><b>${esc(i.name)}</b>${i.is_demo ? '<span class="demo">DEMO</span>' : ""}<span class="sub">${esc(i.email)}</span></td><td>${esc(i.building)}</td><td>${esc(NEED[i.need] || i.need)}</td><td>${esc(i.scale || "—")}</td><td>${esc(fmt(i.created_at))}<span class="sub">${ago(i.created_at)}</span></td><td><span class="status ${i.status}">${i.status}</span></td><td>${i.note_count || ""}</td></tr>`).join("")}</tbody></table></div>`
          : `<div class="panel"><div class="empty">${st.q || st.status ? "Nothing matches these filters." : st.archived ? "Nothing archived." : (isApp ? "No applications yet. They will appear here the moment someone applies on the site." : "No project requests yet.")}</div></div>`;
        document.querySelectorAll("tr[data-href]").forEach((tr) => tr.addEventListener("click", () => (location.hash = tr.dataset.href)));
      } catch (err) { document.getElementById("list").innerHTML = `<div class="error">${esc(err.message)}</div>`; }
    };
    load();
  };

  /* ---------- Detail ---------- */
  const renderDetail = async (kind, id) => {
    const isApp = kind === "applications"; if (!summary) await loadSummary();
    shell(isApp ? "Application" : "Project request", "", '<div class="loading">Loading…</div>', kind);
    let item;
    try { item = (await api(`/${kind}/${id}`)).item; } catch (err) { document.getElementById("view").innerHTML = `<div class="error">${esc(err.message)}</div>`; return; }
    const k = isApp ? "application" : "request";
    const draw = () => {
      const title = isApp ? `${item.first_name} ${item.last_name}` : item.name;
      document.querySelector(".topbar h1").textContent = title; document.querySelector(".topbar .sub").textContent = `${isApp ? POS[item.position] || item.position : item.building} · submitted ${fmt(item.created_at)}`;
      const kv = isApp ? [["Email", `<a href="mailto:${esc(item.email)}">${esc(item.email)}</a>`], ["Discord", esc(item.discord)], ["Position", esc(POS[item.position] || item.position)], ["Portfolio", item.portfolio ? `<a href="${esc(item.portfolio)}" target="_blank" rel="noopener">${esc(item.portfolio)}</a>` : "—"], ["Resume", item.resume_path ? `<a class="btn sm" href="/api/admin/applications/${item.id}/resume">Download ${esc(item.resume_name)} (${Math.round(item.resume_size / 1024)} KB)</a>` : "Not provided"], ["Submitted", fmt(item.created_at)], ["Updated", fmt(item.updated_at)], ["Browser", `<span class="sub">${esc(item.user_agent || "—")}</span>`]]
        : [["Email", `<a href="mailto:${esc(item.email)}">${esc(item.email)}</a>`], ["Discord", esc(item.discord || "—")], ["Building", esc(item.building)], ["Need", esc(NEED[item.need] || item.need)], ["Scale", esc(item.scale || "—")], ["Timeline", esc(item.timeline || "—")], ["Submitted", fmt(item.created_at)], ["Updated", fmt(item.updated_at)]];
      document.getElementById("view").innerHTML = `<div class="crumb"><a href="#/${kind}">← ${isApp ? "Applications" : "Project requests"}</a>${item.is_demo ? ' <span class="demo">DEMO DATA</span>' : ""}${item.archived ? ' <span class="status">archived</span>' : ""}</div>
        <div class="detail"><div>
          <div class="panel"><div class="hd">Details</div><div class="bd"><dl class="kv">${kv.map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join("")}</dl></div></div>
          <div class="panel" style="margin-top:14px"><div class="hd">${isApp ? "Cover letter" : "Message"}</div><div class="bd"><div class="pre">${esc(isApp ? item.cover_letter || "(none)" : item.message)}</div></div></div>
          <div class="panel" style="margin-top:14px"><div class="hd">Internal notes <span class="sub" style="font-weight:400;color:var(--muted)">only visible here</span></div><div class="bd"><form id="note-form" style="display:grid;gap:8px;margin-bottom:12px"><textarea class="textarea" name="body" placeholder="Add a note for the team…" required></textarea><div><button class="btn" type="submit">Add note</button></div></form><div class="notes" id="notes">${item.notes.length ? item.notes.map((n) => `<div class="note"><div class="meta"><span>${esc(n.author)} · ${esc(fmt(n.created_at))}</span><button type="button" data-del="${n.id}">delete</button></div>${esc(n.body)}</div>`).join("") : '<div class="empty" style="padding:10px">No notes yet.</div>'}</div></div></div>
        </div><div class="actions">
          <div class="panel"><div class="hd">Status</div><div class="bd"><span class="status ${item.status}" style="margin-bottom:10px">${item.status}</span><label for="st">Change status</label><select class="select" id="st">${STATUS[k].map((s) => `<option value="${s}" ${s === item.status ? "selected" : ""}>${s}</option>`).join("")}</select><div class="row" style="margin-top:8px"><button class="btn primary" id="save-status" type="button">Save</button></div></div></div>
          <div class="panel"><div class="hd">Contact</div><div class="bd row"><a class="btn" href="mailto:${esc(item.email)}?subject=${encodeURIComponent(isApp ? "Your ETC Labs application" : "Your ETC Labs project request")}">Email</a>${item.discord ? `<button class="btn" type="button" data-copy="${esc(item.discord)}">Copy Discord</button>` : ""}</div></div>
          <div class="panel"><div class="hd">Archive</div><div class="bd"><button class="btn ${item.archived ? "" : "danger"}" id="archive" type="button">${item.archived ? "Restore" : "Archive"}</button><p class="sub" style="margin:8px 0 0;color:var(--muted)">Archived items leave the main lists but are never deleted.</p></div></div>
        </div></div>`;
      document.getElementById("save-status").addEventListener("click", async () => { try { item = (await api(`/${kind}/${id}`, { method: "PATCH", body: JSON.stringify({ status: document.getElementById("st").value }) })).item; toast("Status updated"); loadSummary().then(draw); } catch (e) { toast(e.message); } });
      document.getElementById("archive").addEventListener("click", async () => { try { item = (await api(`/${kind}/${id}`, { method: "PATCH", body: JSON.stringify({ archived: item.archived ? 0 : 1 }) })).item; toast(item.archived ? "Archived" : "Restored"); loadSummary().then(draw); } catch (e) { toast(e.message); } });
      document.getElementById("note-form").addEventListener("submit", async (e) => { e.preventDefault(); const body = e.target.body.value.trim(); if (!body) return; try { await api(`/${kind}/${id}/notes`, { method: "POST", body: JSON.stringify({ body }) }); item = (await api(`/${kind}/${id}`)).item; toast("Note added"); draw(); } catch (err) { toast(err.message); } });
      document.getElementById("notes").addEventListener("click", async (e) => { const b = e.target.closest("[data-del]"); if (!b || !confirm("Delete this note?")) return; try { await api(`/notes/${b.dataset.del}`, { method: "DELETE" }); item = (await api(`/${kind}/${id}`)).item; draw(); } catch (err) { toast(err.message); } });
      document.querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", async () => { try { await navigator.clipboard.writeText(b.dataset.copy); toast("Copied"); } catch { toast(b.dataset.copy); } }));
    };
    draw();
  };

  const renderSettings = async () => {
    if (!summary) await loadSummary();
    let health = {}; try { health = await (await fetch("/api/health")).json(); } catch {}
    let acct = null; try { acct = (await api("/account")).login; } catch {}
    const acctInfo = acct ? `<div class="panel" style="margin-top:14px"><div class="hd">Admin account &amp; login activity</div><div class="bd"><dl class="kv"><dt>Account</dt><dd><code>${esc(me)}</code> · status: active · single admin account</dd><dt>Last successful login</dt><dd>${fmt(acct.last_login)}${acct.last_login_user ? ` (${esc(acct.last_login_user)})` : ""}</dd><dt>Last failed attempt</dt><dd>${fmt(acct.last_failed)}</dd><dt>Failed attempts (24h)</dt><dd>${acct.failed_24h}</dd><dt>Successful logins (all time)</dt><dd>${acct.logins_total}</dd><dt>Public user accounts</dt><dd>None — the public website has no user accounts, so there are no public-user login records.</dd></dl>
      <div class="table-wrap" style="margin-top:10px"><table><thead><tr><th>When</th><th>Account</th><th>Event</th></tr></thead><tbody>${acct.recent.length ? acct.recent.map((r) => `<tr><td>${fmt(r.created_at)}</td><td>${esc(r.actor)}</td><td>${esc(r.action)}</td></tr>`).join("") : `<tr><td colspan="3" class="muted">No login events yet.</td></tr>`}</tbody></table></div></div></div>` : "";
    shell("Settings", "Server configuration is read from .env — nothing here is editable from the browser by design.", `<div class="panel"><div class="hd">Status</div><div class="bd"><dl class="kv"><dt>Admin configured</dt><dd>${health.admin_configured ? "yes" : "no — run python -m server.cli set-admin-password"}</dd><dt>Applications stored</dt><dd>${summary.applications_total}</dd><dt>Project requests stored</dt><dd>${summary.requests_total}</dd><dt>Demo rows</dt><dd>${summary.demo_rows}</dd></dl></div></div>
      <div class="panel" style="margin-top:14px"><div class="hd">Where things live</div><div class="bd"><dl class="kv"><dt>Database</dt><dd><code>data/etc-labs.sqlite3</code> (SQLite, on the backend host — set <code>ETC_DATA_DIR</code> to a persistent disk)</dd><dt>Resumes</dt><dd><code>data/uploads/</code> (random file names, served only through this dashboard)</dd><dt>Logs</dt><dd><code>data/logs/server.log</code></dd><dt>Discord notifications</dt><dd>Optional, server-side, via <code>ETC_DISCORD_WEBHOOK_URL</code> in .env</dd></dl></div></div>${acctInfo}`, "settings");
  };

  /* ---------- Router ---------- */
  const render = async () => {
    if (me === null) { try { me = (await api("/me")).user; } catch { renderLogin(); return; } }
    const [, kind, id] = (location.hash || "#/dashboard").slice(2).split("/").length === 1 ? ["", (location.hash || "#/dashboard").slice(2), ""] : ["", ...(location.hash.slice(2).split("/"))];
    try {
      if (kind === "applications" || kind === "requests") { id ? await renderDetail(kind, id) : await renderList(kind); }
      else if (kind === "settings") await renderSettings();
      else await renderDashboard();
    } catch (err) { if (err.message !== "Not signed in") { const v = document.getElementById("view"); if (v) v.innerHTML = `<div class="error">${esc(err.message)}</div>`; } }
  };
  addEventListener("hashchange", render);
  render();
})();
