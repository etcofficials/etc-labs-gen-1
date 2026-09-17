/* ==========================================================================
   ETC Labs — Gen 1 · Forms: real submissions to `${apiBase}/api` with proper UI states
   loading · success · error · offline · validation · upload progress
   ========================================================================== */
(function () {
  "use strict";
  const M = window.ETC;
  const $ = (s, r = document) => r.querySelector(s);
  const API = M.config.apiBase;                       // "" = same origin (backend serves the site)
  const isStaticHost = !API && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  const mailto = `<a href="mailto:${M.esc(M.config.email)}">${M.esc(M.config.email)}</a>`;
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  const validators = {
    required: (v) => v.trim().length > 0 || "This field is required.",
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || "Enter a valid email address.",
    min: (n) => (v) => v.trim().length >= n || `Please add a little more detail (at least ${n} characters).`,
    url: (v) => !v.trim() || /^(https?:\/\/)?[\w.-]+\.[a-z]{2,}([\/?#].*)?$/i.test(v.trim()) || "Enter a valid link (e.g. https://yourwork.com)."
  };
  const validateField = (field) => {
    const input = field.querySelector("input, select, textarea"); if (!input || input.type === "file") return true;
    const rules = (input.dataset.validate || "").split(" ").filter(Boolean); let msg = true;
    for (const r of rules) { const fn = r.startsWith("min:") ? validators.min(+r.slice(4)) : validators[r]; if (!fn) continue; const res = fn(input.value); if (res !== true) { msg = res; break; } }
    setFieldError(field, msg === true ? "" : msg);
    return msg === true;
  };
  const setFieldError = (field, msg) => { const input = field.querySelector("input, select, textarea"); field.classList.toggle("invalid", !!msg); input && input.setAttribute("aria-invalid", String(!!msg)); const err = field.querySelector(".field-error"); if (err) err.textContent = msg; };

  const status = (form, kind, text) => { const el = $(".form-status", form.parentElement) || $(".form-status", form); if (!el) return; el.className = "form-status " + (kind ? "show " + kind : ""); el.innerHTML = kind === "loading" ? `<span class="spinner"></span><span>${text}</span>` : text; };

  /* Send with XHR so we can show upload progress for resumes */
  const send = (url, body, isMultipart, onProgress) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest(); xhr.open("POST", url); xhr.timeout = 30000; xhr.withCredentials = false;
    if (!isMultipart) xhr.setRequestHeader("Content-Type", "application/json");
    xhr.upload.onprogress = (e) => { if (e.lengthComputable && onProgress) onProgress(e.loaded / e.total); };
    xhr.onload = () => { let data = null; try { data = JSON.parse(xhr.responseText); } catch {} resolve({ status: xhr.status, data }); };
    xhr.onerror = () => reject(new Error("network")); xhr.ontimeout = () => reject(new Error("timeout"));
    xhr.send(body);
  });

  const wire = (form, { url, multipart, success, subjectLine }) => {
    const fields = $$(".field", form);
    const started = form.querySelector('[name="started_at"]'); if (started) started.value = String(Date.now());
    fields.forEach((f) => { const i = f.querySelector("input, select, textarea"); if (!i) return; i.addEventListener("blur", () => validateField(f)); i.addEventListener("input", () => { if (f.classList.contains("invalid")) validateField(f); }); });
    const btn = form.querySelector('[type="submit"]'), label = btn.innerHTML, bar = $(".upload-bar", form);
    if (isStaticHost) {
      // Honest state: this copy of the site is served from a static host and no backend URL is configured.
      status(form, "error", `The submission backend isn&rsquo;t connected on this deployment yet, so this form can&rsquo;t send. Email ${mailto} instead — it reaches the same person.`);
      btn.disabled = true; btn.setAttribute("aria-disabled", "true");
      return;
    }

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!fields.map(validateField).every(Boolean)) { const first = $(".field.invalid input, .field.invalid select, .field.invalid textarea", form); first && first.focus(); status(form, "error", "Please check the highlighted fields."); return; }
      if (!navigator.onLine) { status(form, "error", "You look offline. Check your connection and try again — nothing was sent."); return; }
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Sending…'; status(form, "loading", subjectLine || "Sending…");
      form.setAttribute("aria-busy", "true");
      try {
        let body;
        if (multipart) { body = new FormData(form); if (bar) bar.classList.add("show"); }
        else { const o = {}; new FormData(form).forEach((v, k) => { o[k] = v; }); body = JSON.stringify(o); }
        const res = await send(url, body, multipart, (p) => { if (bar) bar.style.setProperty("--w", Math.round(p * 100) + "%"); });
        if (res.status === 429) { status(form, "error", (res.data && res.data.error) || "Too many submissions right now. Please try again in a few minutes."); }
        else if (res.status === 409 && res.data) { status(form, "error", res.data.error); }
        else if (res.status === 422 && res.data) { status(form, "error", res.data.error); if (res.data.field) { const f = form.querySelector(`[name="${res.data.field}"]`)?.closest(".field"); f && setFieldError(f, res.data.error); } }
        else if (res.status >= 500 || !res.data) { status(form, "error", `We couldn&rsquo;t send that right now. Please try again in a moment — or email ${mailto} directly.`); }
        else if (res.data.ok) {
          form.classList.add("is-hidden"); status(form, "", "");
          const s = $(success); if (s) { s.classList.add("show"); const ref = $(".ref", s); if (ref) ref.textContent = res.data.stored ? "Reference " + res.data.id : ""; s.setAttribute("tabindex", "-1"); s.focus({ preventScroll: false }); }
          return;
        } else status(form, "error", res.data.error || "Something went wrong.");
      } catch (err) {
        status(form, "error", err.message === "timeout" ? "That took too long. Please try again." : `We couldn&rsquo;t reach the server. Please check your connection and try again — or email ${mailto}.`);
      }
      btn.disabled = false; btn.innerHTML = label; form.removeAttribute("aria-busy"); if (bar) { bar.classList.remove("show"); bar.style.setProperty("--w", "0%"); }
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    const contact = $("#contact-form");
    if (contact) {
      wire(contact, { url: API + "/api/project-requests", multipart: false, success: "#contact-success", subjectLine: "Sending your request…" });
      const need = new URLSearchParams(location.search).get("need");
      if (need) { const sel = $('[name="need"]', contact); if (sel && [...sel.options].some((o) => o.value === need)) sel.value = need; }
    }
    const careers = $("#careers-form");
    if (careers) {
      const select = $('[name="position"]', careers);
      select.innerHTML = `<option value="">Select a role</option>${M.roles.map((r) => `<option value="${r.key}">${M.esc(r.title)}</option>`).join("")}<option value="other">Other / general application</option>`;
      wire(careers, { url: API + "/api/applications", multipart: true, success: "#careers-success", subjectLine: "Sending your application…" });
      document.addEventListener("click", (e) => { const a = e.target.closest("[data-apply]"); if (!a) return; select.value = a.dataset.apply; setTimeout(() => $('[name="firstName"]', careers)?.focus({ preventScroll: true }), 500); });
      const file = $('input[type="file"]', careers), name = $("[data-file-name]", careers), drop = file && file.closest(".file-drop");
      const pick = () => { const f = file.files[0]; if (!f) { name.textContent = "Choose your resume"; return; } if (f.size > 5 * 1024 * 1024) { file.value = ""; name.textContent = "Choose your resume"; M.toast("Resume must be under 5 MB."); return; } if (!/\.(pdf|docx?)$/i.test(f.name)) { file.value = ""; name.textContent = "Choose your resume"; M.toast("PDF, DOC or DOCX only."); return; } name.textContent = `${f.name} · ${(f.size / 1024).toFixed(0)} KB`; };
      file && file.addEventListener("change", pick);
      if (drop) { ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); })); ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, () => drop.classList.remove("over"))); }
      const cover = $('[name="cover"]', careers), counter = $("[data-count]", careers);
      cover && counter && cover.addEventListener("input", () => (counter.textContent = `${cover.value.length} / 1000`));
    }
  });
})();
