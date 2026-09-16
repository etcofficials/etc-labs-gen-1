/* ==========================================================================
   ETC Labs — Gen 1 · Deployment configuration (safe to commit: no secrets)

   apiBase: where the backend (FastAPI) is running. The forms POST to
   `${apiBase}/api/...` and the /admin/ page redirects to `${apiBase}/admin/`.

   - Leave "" when the frontend is served BY the backend (local dev: python -m uvicorn …).
   - Set the public backend URL (no trailing slash) when the frontend is on GitHub Pages,
     e.g. "https://etc-labs-gen-1.onrender.com".
   ========================================================================== */
window.ETC_CONFIG = {
  apiBase: ""
};
