# ETC Labs — Gen 1 · Changelog

## Gen 1 final build (2026-09-16) — branding, contact, backend deployment, creator audit

This pass took the approved design and made it ETC Labs' own. The visual system (world background, opening,
buttons, cursor tracker, typography, layouts) was **preserved**; everything below is branding, content honesty,
functionality, deployment and testing.

### Branding
- Public name everywhere: **ETC Labs — Gen 1**. New vector logo (`etc-logo.svg`, mask variant for the opening
  sweep), favicon, Open Graph image (`og.png`), page titles, meta descriptions, canonical URLs, OG/Twitter tags.
- JavaScript namespace `ETC`, custom elements `<etc-nav>` / `<etc-footer>`, session key `etc-intro`.
- Backend: env vars `ETC_*`, cookie `etc_admin`, header `X-ETC-Admin`, database `etc-labs.sqlite3`, logger `etc`.
- Repository, README, Dockerfile, hosting configs, test scripts, demo data — all re-authored. A footer line and
  the About page state plainly that this is an independent showcase not affiliated with MXT.

### Content re-authored (no invented claims)
- Products: **Live** = Gen 1 Platform (this site + backend + admin — genuinely running); **In development** =
  Creator Directory, Submissions Admin; **Planned/Exploring** = Transfer, Voice Rooms, AI Utilities, Creator Toolkit.
- Projects: five live pieces you are using (Gen 1 Website, Submissions Backend & Admin, Creator Directory,
  Deployment Pipeline, The World Background) with Problem → What was built → How → Technology → Status → Link;
  four concepts marked Planned/Exploring with "nothing public yet".
- Community: "Creation League" reworked into the **ETC Labs Community** — creator directory live, rooms/circles/
  challenges planned; demo members explicitly labelled demo; join flow via contact (no fake sign-up).
- About: what it is, why it exists, what it experiments with, design + technology philosophy, where it is going.
  Team section replaced by an honest "one builder, for now" — no invented team members.
- Careers: five *collaboration* roles, early-stage disclosure ("no payroll yet"), same application flow.
- Navigation: Home · What We Build · Products · Projects · Community · About · Careers · Contact.

### Contact (new, required)
- Hero: "Have something you want to build, ask, or discuss? Get in touch with ETC Labs." with what to contact
  for, **etcofficials28@gmail.com** as a `mailto:` link, an **Email us ↗** button, copy-address button, and
  **Instagram @etcofficials** (`https://www.instagram.com/etcofficials/`, `target="_blank"`,
  `rel="noopener noreferrer"`). Subtle neon border on hover, monitored-inbox indicator, entrance animation.
- Old placeholder addresses (`hello@`, `work@`, `league@themxt.online`) removed everywhere; email and Instagram
  also in the footer. No other social accounts invented.

### Backend & deployment
- Frontend is deployable as static files: every path made relative (works under `/etc-labs-gen-1/`),
  `assets/js/config.js` holds the backend URL, `public/admin/` redirects to the backend admin.
- CORS (only `/api/project-requests`, `/api/applications`, `/api/health`; only `ETC_ALLOWED_ORIGINS`).
- Forms: when served from a static host without a configured backend they show an honest "not connected —
  email us" state with the submit button disabled; failure messages include the email fallback.
- `Dockerfile`, `.dockerignore`, `render.yaml` (Docker + persistent disk), `fly.toml`, GitHub Actions
  workflow deploying `public/` to GitHub Pages, `.env.example` (names only), stricter `.gitignore`.
- Admin: `GET /api/admin/account` + Settings panel with last login, last failed attempt, failed attempts (24 h),
  total logins, recent login/logout events, and the explicit note that public users have no accounts.
  Logout is now audited. Role labels updated.

### Creator data audit (brief §61)
Every row checked against the exact channel URL on 2026-09-16 (channel name, canonical handle, channel id,
public subscriber count, profile image). Avatars are the creators' public YouTube profile images stored in
`public/assets/img/creators/` with an initial-letter fallback if an image fails.

| Creator (was) | Verified channel | Name shown | Subscribers (was → now) | Avatar | Link |
| --- | --- | --- | --- | --- | --- |
| ZaptrooOP | @ZaptrooPlays · UCrRDtqbqbC0n1uHel6-JUew | Zaptroo Plays | 35K → 35K | real | Working |
| Kajuto | @Kajutoo · UCF5ksRyJ9DjjMScxLqPIcFw | Kajuto | 990K → 992K | real | Working |
| Rouckz | @RealRouckz · UCLr67LxrHYCjwZPB3IsZLSQ | Rouckz | — → 343 | real | Working (trailing `/featured` removed) |
| Umesh | @UMESHX_GAMER · UCB_eN9_IzSfJcvoi1sUT74Q | UMESH X | 54.3K → 54.1K | real | Working (trailing `/shorts` removed) |
| Mystic Priya | @mysticpriya · UCBaBy8eHr8EPfp74jX2mINQ | Mystic Priya | 4.54K → 4.65K | real | Working (trailing `/featured` removed) |

Ranking stays "by joined date" (unchanged and labelled). Counts are static with a visible verification date.

### Testing (all run against the live local server)
- `docs/audit.py`: 16 renders (8 pages × desktop/mobile) — 0 JS errors, 0 horizontal overflow.
- `docs/perf.py`: 58–60 fps idle, 60 fps scrolling at 1× and 4× CPU throttle (desktop and mobile profiles);
  keyboard order, Enter/Esc on the mobile menu, reduced-motion honoured. JS 74 KB, CSS 82 KB, 674 DOM nodes.
- `docs/e2e.py`: 30/30 — contact form (missing fields, invalid email, loading, success with reference,
  failure with email fallback), careers form (validation, fake-PDF rejection by magic bytes, real resume
  upload), admin (401 without session, wrong password, login, real counts, search, status filter, detail
  fields, status change persisted in SQLite, resume download, path traversal → 404, missing header → 403,
  request detail, settings/login activity, logout → 401, public resume URL → 401).
- `docs/static_sim.py`: 15/15 — GitHub Pages origin simulated in-browser: all 8 pages render with relative
  paths and no 404s, forms show the honest not-connected state when `apiBase` is empty, `/admin/` explains or
  redirects, a real cross-origin submission succeeds through CORS, admin routes are not CORS-exposed.
- `docs/persona_test.py`: 13/13.
- `docs/live_check.py` (after deployment): all 8 pages on https://etcofficials.github.io/etc-labs-gen-1/ at desktop
  and mobile — 0 errors, 0 failed requests, 0 overflow, fonts/CSS/JS loaded, mobile menu works, creator avatars
  and channel links correct, contact links correct, forms in the honest not-connected state, `/admin/` explains
  that the backend is not configured yet.
- Test rows removed after each run; the local database is empty (`python -m server.cli stats`).

### Secrets check before pushing
Repository scanned for keys, tokens, hashes, webhooks and credentials; `.env` (which holds the local admin
hash) is git-ignored and was never staged; `.env.example` contains names only; `data/` is ignored.

## Earlier history
The design and interaction system (world background, opening, motion, list+detail components, product-mock
kit, forms, backend and admin) was built in earlier iterations as a recreation/learning exercise; that history
lives outside this repository. Gen 1 is the first ETC Labs release.
