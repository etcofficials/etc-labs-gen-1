/* ==========================================================================
   ETC Labs — Gen 1 · Touch-first behaviours shared by every page (cheap, observer-driven).
   - sections get .in-view for the animated divider (phones)
   - hero accent line
   - expandable cards are wired wherever they appear
   ========================================================================== */
(function () {
  "use strict";
  const M = window.ETC;
  document.addEventListener("DOMContentLoaded", () => {
    const k = document.querySelector(".hero .kicker"); if (k && !document.querySelector(".hero-line")) { const l = document.createElement("div"); l.className = "hero-line"; l.setAttribute("aria-hidden", "true"); k.insertAdjacentElement("afterend", l); }
    const sections = Array.from(document.querySelectorAll("main .section"));
    if (M.env.reduce || !("IntersectionObserver" in window)) { sections.forEach((s) => s.classList.add("in-view")); return; }
    const io = new IntersectionObserver((entries) => entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in-view"); io.unobserve(en.target); } }), { rootMargin: "0px 0px -10% 0px", threshold: 0.05 });
    sections.forEach((s) => io.observe(s));
  });
})();
