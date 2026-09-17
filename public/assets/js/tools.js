/* ==========================================================================
   ETC Labs — Gen 1 · Tools: Transfer · Voice Rooms · AI Utilities · Creator Toolkit
   Real functionality only. Every tool has loading / success / error / empty / offline states.
   ========================================================================== */
(function () {
  "use strict";
  const M = window.ETC, esc = M.esc;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const API = M.config.apiBase;
  const isStaticHost = !API && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  const WS_BASE = (API || location.origin).replace(/^http/, "ws");
  const fmtBytes = (n) => n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(0) + " KB" : (n / 1048576).toFixed(1) + " MB";
  const fmtIn = (ts) => { const s = ts - Date.now() / 1000; if (s < 3600) return Math.max(1, Math.round(s / 60)) + " min"; if (s < 86400) return Math.round(s / 3600) + " h"; return Math.round(s / 86400) + " d"; };
  const showState = (app, name) => $$(".tool-state", app).forEach((el) => { el.classList.toggle("show", el.dataset.state === name); el.hidden = el.dataset.state !== name; });
  const status = (root, kind, html) => { const el = $(".form-status", root); if (!el) return; el.className = "form-status " + (kind ? "show " + kind : ""); el.innerHTML = kind === "loading" ? `<span class="spinner"></span><span>${html}</span>` : html; };
  const copy = async (text, btn) => { try { await navigator.clipboard.writeText(text); M.toast("Copied"); } catch { M.toast(text); } if (btn) { const t = btn.textContent; btn.textContent = "Copied"; setTimeout(() => (btn.textContent = t), 1400); } };
  const api = async (path, opts = {}) => {
    const res = await fetch(API + path, { ...opts, headers: { ...(opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : {}), ...(opts.headers || {}) } });
    let data = null; try { data = await res.json(); } catch {}
    return { status: res.status, data };
  };

  /* ================================================================ TRANSFER */
  function transfer() {
    const app = $("#transfer-app"); if (!app) return;
    const params = new URLSearchParams(location.search), tid = params.get("t"), owner = params.get("owner");
    if (isStaticHost) return showState(app, "offline");
    api("/api/transfers/config").then((r) => { if (r.data && r.data.max_mb) $$("[data-max-mb]").forEach((e) => (e.textContent = r.data.max_mb)); });

    if (tid) {
      showState(app, owner ? "owner" : "download");
      api("/api/transfers/" + encodeURIComponent(tid)).then((r) => {
        if (!r.data || !r.data.ok) { showState(app, "error"); $("#ename").textContent = r.status === 410 ? "This transfer has expired" : r.status === 404 ? "This link doesn’t work" : "Something went wrong"; $("#emsg").textContent = (r.data && r.data.error) || "We couldn’t reach the server. Please try again."; return; }
        const d = r.data, meta = `${fmtBytes(d.size)} · expires in ${fmtIn(d.expires_at)} · ${d.downloads_left} download${d.downloads_left === 1 ? "" : "s"} left`;
        if (owner) {
          $("#oname").textContent = d.name; $("#ometa").textContent = meta;
          $("#odelete").addEventListener("click", async () => {
            if (!confirm("Delete this transfer now? The link will stop working immediately.")) return;
            const del = await api(`/api/transfers/${encodeURIComponent(tid)}?token=${encodeURIComponent(owner)}`, { method: "DELETE" });
            if (del.data && del.data.ok) { status($('[data-state="owner"]', app), "success", "Deleted. The link no longer works."); $("#odelete").disabled = true; }
            else status($('[data-state="owner"]', app), "error", (del.data && del.data.error) || "Could not delete.");
          });
        } else { $("#dname").textContent = d.name; $("#dmeta").textContent = meta; $("#ddownload").href = API + d.download; }
      }).catch(() => { showState(app, "error"); $("#emsg").textContent = "We couldn’t reach the server. Please check your connection and try again."; });
      return;
    }

    showState(app, "upload");
    const input = $("#tfile"), drop = $("#drop"), name = $("[data-file-name]", app), send = $("#tsend"), bar = $(".upload-bar", app), state = $('[data-state="upload"]', app);
    let file = null, maxMb = 25;
    api("/api/transfers/config").then((r) => { if (r.data && r.data.max_mb) maxMb = r.data.max_mb; });
    const pick = (f) => {
      if (!f) return;
      if (f.size > maxMb * 1048576) { status(state, "error", `That file is ${fmtBytes(f.size)}. The limit is ${maxMb} MB.`); file = null; send.disabled = true; name.textContent = "Choose a file"; return; }
      if (f.size === 0) { status(state, "error", "That file is empty."); return; }
      file = f; name.textContent = `${f.name} · ${fmtBytes(f.size)}`; send.disabled = false; status(state, "", ""); drop.classList.add("has-file");
    };
    input.addEventListener("change", () => pick(input.files[0]));
    ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); }));
    ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("over"); if (ev === "drop" && e.dataTransfer.files[0]) pick(e.dataTransfer.files[0]); }));
    send.addEventListener("click", () => {
      if (!file) return;
      if (!navigator.onLine) return status(state, "error", "You look offline. Nothing was uploaded.");
      const fd = new FormData(); fd.append("file", file, file.name); fd.append("ttl", $('input[name="ttl"]:checked', app).value);
      send.disabled = true; send.innerHTML = '<span class="spinner"></span> Uploading…'; bar.classList.add("show"); status(state, "loading", "Uploading " + esc(file.name) + "…");
      const xhr = new XMLHttpRequest(); xhr.open("POST", API + "/api/transfers"); xhr.timeout = 120000;
      xhr.upload.onprogress = (e) => { if (e.lengthComputable) { const p = Math.round((e.loaded / e.total) * 100); bar.style.setProperty("--w", p + "%"); status(state, "loading", `Uploading… ${p}%`); } };
      const reset = () => { send.disabled = false; send.innerHTML = "Create link " + M.icons.arrow; bar.classList.remove("show"); bar.style.setProperty("--w", "0%"); };
      xhr.onload = () => {
        let d = null; try { d = JSON.parse(xhr.responseText); } catch {}
        if (xhr.status === 201 && d && d.ok) {
          showState(app, "done");
          $("#tsummary").textContent = `${d.name} · ${fmtBytes(d.size)} · expires in ${fmtIn(d.expires_at)}`;
          const link = location.origin + location.pathname + "?t=" + d.id; $("#tlink").value = link;
          $("#towner").href = link + "&owner=" + encodeURIComponent(d.owner_token);
          $("#tcopy").addEventListener("click", () => copy(link, $("#tcopy")));
          $("#tlink").addEventListener("focus", (e) => e.target.select());
        } else { status(state, "error", (d && d.error) || (xhr.status === 413 ? "That file is too large." : "The upload failed. Please try again.")); reset(); }
      };
      xhr.onerror = () => { status(state, "error", "We couldn’t reach the server. Please check your connection and try again."); reset(); };
      xhr.ontimeout = () => { status(state, "error", "The upload took too long. Try a smaller file or a better connection."); reset(); };
      xhr.send(fd);
    });
  }

  /* ================================================================ VOICE ROOMS (WebRTC full mesh) */
  function voice() {
    const app = $("#voice-app"); if (!app) return;
    if (isStaticHost) return showState(app, "offline");
    const lobby = $('[data-state="lobby"]', app), room = $('[data-state="room"]', app);
    const nameIn = $("#vname"), codeIn = $("#vcode");
    try { nameIn.value = localStorage.getItem("etc-voice-name") || ""; } catch {}
    const params = new URLSearchParams(location.search); if (params.get("room")) codeIn.value = params.get("room").toLowerCase();
    showState(app, "lobby");
    if (!("RTCPeerConnection" in window) || !navigator.mediaDevices) { status(lobby, "error", "This browser does not support WebRTC voice. Try Chrome, Edge, Safari or Firefox."); $("#vcreate").disabled = $("#vjoin").disabled = true; return; }

    let ws = null, myId = null, stream = null, muted = false; const peers = new Map(); let iceServers = [];
    const setConn = (state, label) => { const c = $("#rconn"); c.dataset.state = state; c.querySelector("span").textContent = label; };
    const renderPeers = () => {
      const list = [{ id: myId, name: (nameIn.value || "You") + " (you)", muted, state: "you" }, ...[...peers.values()].map((p) => ({ id: p.id, name: p.name, muted: p.muted, state: p.state }))];
      $("#rpeers").innerHTML = list.map((p) => `<li class="peer ${p.state}"><span class="avatar sm">${esc(p.name[0].toUpperCase())}</span><span class="pname">${esc(p.name)}</span><span class="pstate">${p.muted ? "muted" : p.state === "you" ? "" : p.state === "connected" ? "connected" : p.state === "failed" ? "no route" : "connecting"}</span><i class="level" aria-hidden="true"></i></li>`).join("") || "";
    };
    const cleanup = () => {
      peers.forEach((p) => { try { p.pc.close(); } catch {} }); peers.clear();
      if (stream) { stream.getTracks().forEach((t) => t.stop()); stream = null; }
      if (ws) { try { ws.close(); } catch {} ws = null; }
      $("#raudio").innerHTML = "";
    };
    const makePeer = (id, name, initiator) => {
      const pc = new RTCPeerConnection({ iceServers });
      const p = { id, name, pc, muted: false, state: "connecting" }; peers.set(id, p);
      stream.getTracks().forEach((t) => pc.addTrack(t, stream));
      pc.onicecandidate = (e) => { if (e.candidate && ws) ws.send(JSON.stringify({ type: "signal", to: id, data: { candidate: e.candidate } })); };
      pc.ontrack = (e) => { let a = $(`audio[data-peer="${id}"]`); if (!a) { a = document.createElement("audio"); a.dataset.peer = id; a.autoplay = true; a.playsInline = true; $("#raudio").appendChild(a); } a.srcObject = e.streams[0]; a.play().catch(() => {}); };
      pc.onconnectionstatechange = () => { p.state = pc.connectionState === "connected" ? "connected" : pc.connectionState === "failed" || pc.connectionState === "disconnected" ? "failed" : "connecting"; renderPeers(); const any = [...peers.values()].some((x) => x.state === "connected"); setConn(peers.size === 0 ? "alone" : any ? "ok" : "connecting", peers.size === 0 ? "waiting for others" : any ? "connected" : "connecting"); if (p.state === "failed") status(room, "error", `Could not connect to ${esc(name)} directly. On strict networks a TURN relay is required (not configured on this deployment).`); };
      if (initiator) pc.createOffer().then((o) => pc.setLocalDescription(o)).then(() => ws.send(JSON.stringify({ type: "signal", to: id, data: { sdp: pc.localDescription } })));
      return p;
    };
    const onSignal = async (from, data) => {
      let p = peers.get(from); if (!p) p = makePeer(from, "Guest", false);
      if (data.sdp) {
        await p.pc.setRemoteDescription(new RTCSessionDescription(data.sdp));
        if (data.sdp.type === "offer") { const ans = await p.pc.createAnswer(); await p.pc.setLocalDescription(ans); ws.send(JSON.stringify({ type: "signal", to: from, data: { sdp: p.pc.localDescription } })); }
      } else if (data.candidate) { try { await p.pc.addIceCandidate(new RTCIceCandidate(data.candidate)); } catch {} }
    };
    const enter = async (code) => {
      code = (code || "").trim().toLowerCase();
      if (!/^[a-z0-9]{4,12}$/.test(code)) return status(lobby, "error", "Room codes are 4–12 letters or digits.");
      const nm = (nameIn.value || "").trim().slice(0, 24) || "Guest"; try { localStorage.setItem("etc-voice-name", nm); } catch {}
      status(lobby, "loading", "Asking for microphone access…");
      try { stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true }, video: false }); }
      catch (e) { return status(lobby, "error", e.name === "NotAllowedError" ? "Microphone access was blocked. Allow the microphone for this site and try again." : "No microphone was found on this device."); }
      status(lobby, "loading", "Joining room…");
      const cfg = await api("/api/voice/config").catch(() => ({ data: null })); iceServers = (cfg.data && cfg.data.ice_servers) || [{ urls: ["stun:stun.l.google.com:19302"] }];
      ws = new WebSocket(`${WS_BASE}/ws/voice/${code}`);
      ws.onopen = () => ws.send(JSON.stringify({ type: "join", name: nm }));
      ws.onmessage = async (ev) => {
        const m = JSON.parse(ev.data);
        if (m.type === "welcome") {
          myId = m.id; if (m.ice_servers) iceServers = m.ice_servers;
          showState(app, "room"); status(lobby, "", ""); $("#rcode").textContent = code;
          const link = location.origin + location.pathname + "?room=" + code; $("#rlink").value = link; history.replaceState(null, "", "?room=" + code);
          m.peers.forEach((p) => { const peer = makePeer(p.id, p.name, true); peer.muted = p.muted; });
          setConn(m.peers.length ? "connecting" : "alone", m.peers.length ? "connecting" : "waiting for others — share the code"); renderPeers();
        } else if (m.type === "peer-joined") { makePeer(m.id, m.name, false); renderPeers(); M.toast(`${m.name} joined`); }
        else if (m.type === "signal") { await onSignal(m.from, m.data); }
        else if (m.type === "peer-mute") { const p = peers.get(m.id); if (p) { p.muted = m.muted; renderPeers(); } }
        else if (m.type === "peer-left") { const p = peers.get(m.id); if (p) { try { p.pc.close(); } catch {} peers.delete(m.id); const a = $(`audio[data-peer="${m.id}"]`); a && a.remove(); renderPeers(); if (!peers.size) setConn("alone", "waiting for others — share the code"); } }
        else if (m.type === "error") { status(lobby, "error", m.message || "Could not join."); cleanup(); showState(app, "lobby"); }
      };
      ws.onerror = () => { status(lobby, "error", "Could not reach the voice server. Please try again."); cleanup(); showState(app, "lobby"); };
      ws.onclose = (e) => { if (app.querySelector('[data-state="room"].show')) { setConn("failed", "disconnected"); status(room, "error", e.code === 4409 ? "This room is full." : "Connection to the room was lost. Leave and rejoin to reconnect."); } };
    };
    $("#vcreate").addEventListener("click", async () => {
      $("#vcreate").disabled = true;
      try { const r = await api("/api/voice/rooms", { method: "POST" }); if (r.data && r.data.room) await enter(r.data.room); else status(lobby, "error", (r.data && r.data.error) || "Could not create a room."); }
      catch { status(lobby, "error", "We couldn’t reach the server."); }
      $("#vcreate").disabled = false;
    });
    $("#vjoin").addEventListener("click", () => enter(codeIn.value));
    codeIn.addEventListener("keydown", (e) => { if (e.key === "Enter") enter(codeIn.value); });
    $("#rcopy").addEventListener("click", () => copy($("#rlink").value, $("#rcopy")));
    $("#rmute").addEventListener("click", () => { muted = !muted; stream && stream.getAudioTracks().forEach((t) => (t.enabled = !muted)); $("#rmute").textContent = muted ? "Unmute" : "Mute"; $("#rmute").setAttribute("aria-pressed", String(muted)); ws && ws.readyState === 1 && ws.send(JSON.stringify({ type: "mute", muted })); renderPeers(); });
    $("#rleave").addEventListener("click", () => { cleanup(); showState(app, "lobby"); status(lobby, "success", "You left the room."); history.replaceState(null, "", location.pathname); });
    addEventListener("pagehide", cleanup);
    if (params.get("room") && nameIn.value) status(lobby, "", "");
  }

  /* ================================================================ AI UTILITIES */
  function ai() {
    const app = $("#ai-app"); if (!app) return;
    if (isStaticHost) return showState(app, "offline");
    const ready = $('[data-state="ready"]', app), text = $("#ai-text"), run = $("#ai-run"), count = $("#ai-count"), out = $("#ai-output"), result = $("#ai-result");
    let tool = "summarize", tools = {}, tones = [], busy = false;
    const update = () => { count.textContent = `${text.value.length} / 6000`; run.disabled = busy || text.value.trim().length < 10; $("#ai-hint").textContent = text.value.trim().length < 10 ? "Pick a tool and paste some text (at least 10 characters)." : `Runs ${tools[tool] || tool} on ${text.value.trim().length} characters.`; };
    const renderTools = () => { $("#ai-tools").innerHTML = Object.entries(tools).map(([k, v]) => `<button class="filter-btn" type="button" data-tool="${k}" aria-pressed="${k === tool}">${esc(v)}</button>`).join(""); $("#ai-tone-field").hidden = tool !== "rewrite"; };
    api("/api/ai/status").then((r) => {
      if (!r.data || !r.data.ok) { status(ready, "error", "Could not reach the backend."); return; }
      if (!r.data.configured) { showState(app, "disabled"); $$("[data-ai-model]").forEach((e) => (e.textContent = "not configured")); return; }
      showState(app, "ready"); tools = r.data.tools; tones = r.data.tones; $$("[data-ai-model]").forEach((e) => (e.textContent = r.data.model));
      $("#ai-tone").innerHTML = tones.map((t) => `<option value="${esc(t)}">${esc(t)}</option>`).join(""); renderTools(); update();
    }).catch(() => status(ready, "error", "Could not reach the backend."));
    $("#ai-tools").addEventListener("click", (e) => { const b = e.target.closest("[data-tool]"); if (!b) return; tool = b.dataset.tool; renderTools(); update(); });
    text.addEventListener("input", update);
    const go = async () => {
      if (busy || text.value.trim().length < 10) return;
      busy = true; run.disabled = true; run.innerHTML = '<span class="spinner"></span> Working…'; status(ready, "loading", "Sending to the model…"); out.hidden = true;
      try {
        const r = await api("/api/ai/" + tool, { method: "POST", body: JSON.stringify({ text: text.value, option: $("#ai-tone").value }) });
        if (r.data && r.data.ok) { result.textContent = r.data.output; $("#ai-output-label").textContent = `${tools[tool]} · ${r.data.model}`; out.hidden = false; status(ready, "", ""); out.scrollIntoView({ behavior: M.env.reduce ? "auto" : "smooth", block: "nearest" }); }
        else if (r.status === 503 && r.data && r.data.configured === false) showState(app, "disabled");
        else status(ready, "error", (r.data && r.data.error) || "The request failed. Please try again.");
      } catch { status(ready, "error", "We couldn’t reach the server. Check your connection and try again."); }
      busy = false; run.innerHTML = "Run " + M.icons.arrow; update();
    };
    run.addEventListener("click", go); $("#ai-again").addEventListener("click", go);
    $("#ai-copy").addEventListener("click", () => copy(result.textContent, $("#ai-copy")));
    text.addEventListener("keydown", (e) => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") go(); });
  }

  /* ================================================================ CREATOR TOOLKIT (local-first) */
  function toolkit() {
    const app = $("#toolkit-app"); if (!app) return;
    const KEY = "etc-toolkit-v1", STEPS = ["Idea locked", "Script / outline", "Recorded / drafted", "Edited", "Thumbnail & title", "Published", "Shared"];
    const blank = () => ({ ideas: [], pieces: [], projects: [] });
    let data = blank(), storageOk = true;
    try { data = { ...blank(), ...(JSON.parse(localStorage.getItem(KEY) || "null") || {}) }; } catch { storageOk = false; }
    const save = () => { try { localStorage.setItem(KEY, JSON.stringify(data)); } catch { storageOk = false; status(app, "error", "This browser is blocking storage, so changes will be lost when you leave. Export a backup."); } stats(); };
    const uid = () => Math.random().toString(36).slice(2, 10);
    const stats = () => { $('[data-stat="ideas"]').textContent = data.ideas.length; $('[data-stat="checklist"]').textContent = data.pieces.filter((p) => p.done.length === STEPS.length).length; $('[data-stat="projects"]').textContent = data.projects.filter((p) => !p.done).length; };
    if (!storageOk) status(app, "error", "This browser is blocking local storage. The toolkit will work for this visit only.");
    // tabs
    $$(".tab", app).forEach((t) => t.addEventListener("click", () => { $$(".tab", app).forEach((x) => x.setAttribute("aria-selected", String(x === t))); $$(".tab-panel", app).forEach((p) => (p.hidden = p.dataset.panel !== t.dataset.tab)); try { localStorage.setItem(KEY + "-tab", t.dataset.tab); } catch {} }));
    try { const last = localStorage.getItem(KEY + "-tab"); if (last) $(`.tab[data-tab="${last}"]`, app)?.click(); } catch {}
    // ideas
    const IDEA_STATES = ["new", "developing", "ready", "done"]; let ideaFilter = "all";
    const renderIdeas = () => {
      const tags = [...new Set(data.ideas.flatMap((i) => i.tags))];
      $("#idea-filters").innerHTML = [["all", "All"], ...IDEA_STATES.map((s) => [s, s])].map(([k, l]) => `<button class="filter-btn" type="button" data-f="${k}" aria-pressed="${ideaFilter === k}">${esc(l)}<span class="count">${k === "all" ? data.ideas.length : data.ideas.filter((i) => i.state === k).length}</span></button>`).join("") + (tags.length ? `<span class="small muted" style="align-self:center;margin-left:6px">${tags.length} tag${tags.length > 1 ? "s" : ""}</span>` : "");
      const list = data.ideas.filter((i) => ideaFilter === "all" || i.state === ideaFilter);
      $("#idea-list").innerHTML = list.length ? list.map((i) => `<li class="tk-item" data-id="${i.id}"><div class="tk-main"><b>${esc(i.title)}</b><span class="tk-tags">${i.tags.map((t) => `<span class="chip sm">${esc(t)}</span>`).join("")}</span></div><select class="select sm" aria-label="Status for ${esc(i.title)}" data-act="state">${IDEA_STATES.map((s) => `<option value="${s}" ${s === i.state ? "selected" : ""}>${s}</option>`).join("")}</select><button class="icon-btn" type="button" data-act="del" aria-label="Delete ${esc(i.title)}">✕</button></li>`).join("")
        : `<li class="empty">${data.ideas.length ? "No ideas with this status." : "No ideas yet. Add the first one above — it stays in this browser."}</li>`;
    };
    $("#idea-form").addEventListener("submit", (e) => { e.preventDefault(); const f = e.target; const title = f.title.value.trim(); if (!title) return; data.ideas.unshift({ id: uid(), title, tags: f.tags.value.split(",").map((t) => t.trim().toLowerCase()).filter(Boolean).slice(0, 6), state: "new", at: Date.now() }); f.reset(); save(); renderIdeas(); M.toast("Idea added"); });
    $("#idea-filters").addEventListener("click", (e) => { const b = e.target.closest("[data-f]"); if (b) { ideaFilter = b.dataset.f; renderIdeas(); } });
    $("#idea-list").addEventListener("change", (e) => { const li = e.target.closest(".tk-item"); const i = data.ideas.find((x) => x.id === li.dataset.id); if (i && e.target.dataset.act === "state") { i.state = e.target.value; save(); renderIdeas(); } });
    $("#idea-list").addEventListener("click", (e) => { const b = e.target.closest('[data-act="del"]'); if (!b) return; const li = b.closest(".tk-item"); data.ideas = data.ideas.filter((x) => x.id !== li.dataset.id); save(); renderIdeas(); });
    // publishing checklist
    const renderPieces = () => {
      $("#piece-list").innerHTML = data.pieces.length ? data.pieces.map((p) => { const pct = Math.round((p.done.length / STEPS.length) * 100); return `<div class="tk-piece" data-id="${p.id}"><div class="tk-piece-head"><b>${esc(p.title)}</b><span class="small muted">${p.done.length}/${STEPS.length}</span><button class="icon-btn" type="button" data-act="del" aria-label="Delete ${esc(p.title)}">✕</button></div><div class="progress ${pct === 100 ? "done" : ""}" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100" aria-label="${esc(p.title)} progress"><i style="width:${pct}%"></i></div><ul class="tk-steps">${STEPS.map((s, k) => `<li><label class="check"><input type="checkbox" data-step="${k}" ${p.done.includes(k) ? "checked" : ""}><span>${esc(s)}</span></label></li>`).join("")}</ul></div>`; }).join("")
        : `<div class="empty">No pieces in progress. Start a checklist for your next video, post or episode.</div>`;
    };
    $("#piece-form").addEventListener("submit", (e) => { e.preventDefault(); const title = e.target.title.value.trim(); if (!title) return; data.pieces.unshift({ id: uid(), title, done: [], at: Date.now() }); e.target.reset(); save(); renderPieces(); });
    $("#piece-list").addEventListener("change", (e) => { const wrap = e.target.closest(".tk-piece"); const p = data.pieces.find((x) => x.id === wrap.dataset.id); if (!p || e.target.dataset.step === undefined) return; const k = +e.target.dataset.step; p.done = e.target.checked ? [...new Set([...p.done, k])] : p.done.filter((x) => x !== k); save(); renderPieces(); if (p.done.length === STEPS.length) M.toast("Published — nice work"); });
    $("#piece-list").addEventListener("click", (e) => { const b = e.target.closest('[data-act="del"]'); if (!b) return; data.pieces = data.pieces.filter((x) => x.id !== b.closest(".tk-piece").dataset.id); save(); renderPieces(); });
    // projects
    const renderProjects = () => {
      const list = [...data.projects].sort((a, b) => (a.done - b.done) || ((a.due || "9") > (b.due || "9") ? 1 : -1));
      $("#project-list").innerHTML = list.length ? list.map((p) => { const late = p.due && !p.done && p.due < new Date().toISOString().slice(0, 10); return `<li class="tk-item ${p.done ? "is-done" : ""}" data-id="${p.id}"><label class="check"><input type="checkbox" data-act="done" ${p.done ? "checked" : ""} aria-label="Mark ${esc(p.title)} done"><span></span></label><div class="tk-main"><b>${esc(p.title)}</b><span class="small ${late ? "late" : "muted"}">${p.due ? (late ? "overdue · " : "due ") + p.due : "no date"}</span></div><button class="icon-btn" type="button" data-act="del" aria-label="Delete ${esc(p.title)}">✕</button></li>`; }).join("")
        : `<li class="empty">No projects yet. Add one with an optional due date.</li>`;
    };
    $("#project-form").addEventListener("submit", (e) => { e.preventDefault(); const f = e.target; const title = f.title.value.trim(); if (!title) return; data.projects.unshift({ id: uid(), title, due: f.due.value || "", done: false, at: Date.now() }); f.reset(); save(); renderProjects(); });
    $("#project-list").addEventListener("change", (e) => { const li = e.target.closest(".tk-item"); const p = data.projects.find((x) => x.id === li.dataset.id); if (p && e.target.dataset.act === "done") { p.done = e.target.checked; save(); renderProjects(); } });
    $("#project-list").addEventListener("click", (e) => { const b = e.target.closest('[data-act="del"]'); if (!b) return; data.projects = data.projects.filter((x) => x.id !== b.closest(".tk-item").dataset.id); save(); renderProjects(); });
    // export / import
    $("#tk-export").addEventListener("click", () => { const blob = new Blob([JSON.stringify({ app: "etc-labs-creator-toolkit", version: 1, exported: new Date().toISOString(), data }, null, 2)], { type: "application/json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `etc-toolkit-${new Date().toISOString().slice(0, 10)}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); M.toast("Exported"); });
    $("#tk-import-file").addEventListener("change", async (e) => {
      const f = e.target.files[0]; if (!f) return;
      try { const j = JSON.parse(await f.text()); const d = j.data || j; if (!d || !Array.isArray(d.ideas) || !Array.isArray(d.pieces) || !Array.isArray(d.projects)) throw new Error("shape");
        if (data.ideas.length + data.pieces.length + data.projects.length && !confirm("Replace your current toolkit data with the imported file?")) return;
        data = { ideas: d.ideas.slice(0, 500).map((i) => ({ id: String(i.id || uid()), title: String(i.title || "").slice(0, 120), tags: (i.tags || []).map(String).slice(0, 6), state: IDEA_STATES.includes(i.state) ? i.state : "new", at: +i.at || Date.now() })),
                 pieces: d.pieces.slice(0, 500).map((p) => ({ id: String(p.id || uid()), title: String(p.title || "").slice(0, 120), done: (p.done || []).map(Number).filter((k) => k >= 0 && k < STEPS.length), at: +p.at || Date.now() })),
                 projects: d.projects.slice(0, 500).map((p) => ({ id: String(p.id || uid()), title: String(p.title || "").slice(0, 120), due: /^\d{4}-\d{2}-\d{2}$/.test(p.due || "") ? p.due : "", done: !!p.done, at: +p.at || Date.now() })) };
        save(); renderIdeas(); renderPieces(); renderProjects(); status(app, "success", "Imported " + (data.ideas.length + data.pieces.length + data.projects.length) + " items.");
      } catch { status(app, "error", "That file is not a Creator Toolkit export."); }
      e.target.value = "";
    });
    renderIdeas(); renderPieces(); renderProjects(); stats();
  }

  document.addEventListener("DOMContentLoaded", () => { transfer(); voice(); ai(); toolkit(); });
})();
