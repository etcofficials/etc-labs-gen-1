/* ==========================================================================
   ETC Labs — Gen 1 · Deployment configuration (safe to commit: no secrets)

   apiBase: where the backend (FastAPI) is running. The forms POST to
   `${apiBase}/api/...` and the /admin/ page redirects to `${apiBase}/admin/`.

   - Production (GitHub Pages): the Render backend URL, no trailing slash.
   - Local development (python -m uvicorn … on localhost): "" = same origin, so the
     forms talk to your local server, not to production.
   ========================================================================== */
window.ETC_CONFIG = {
  apiBase: /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)
    ? ""
    : "https://etc-labs-gen-1.onrender.com"
};
