# ETC Labs — Gen 1 · Changelog

## Gen 1 completion (2026-09-17) — every product live, touch-first mobile

### Products and projects — no more planned / exploring / in-development
| Feature | Previous status | Now | How it is real |
| --- | --- | --- | --- |
| Transfer | Planned (concept card) | **Live** — `transfer.html` | `POST /api/transfers` streams the file into private storage (25 MB cap, real progress bar), opaque `tr_` ids, expiry 24 h / 3 d / 7 d or 100 downloads, owner-token deletion, attachment-only downloads, opportunistic purge |
| Voice Rooms | Exploring | **Live** — `voice.html` | Full-mesh WebRTC audio (≤ 6 people) signalled over `WS /ws/voice/{code}`; create/join by code, mic permission, mute, participant list with connection state, leave; tested 3-way in real browser tabs |
| AI Utilities | Exploring | **Live** — `ai.html` | `POST /api/ai/{summarize,rewrite,ideas,titles}` calls the Claude API from the backend (key in env only), 6,000-char limit, 20/hour per visitor, typed error handling; without a key the page shows an honest "not enabled" state and the API returns 503 `configured:false` |
| Creator Toolkit | Exploring | **Live** — `toolkit.html` | Local-first ideas board (states, tags, filters), publishing checklist with progress, projects with due dates, JSON export/import with validation; persists across reloads, honest warning if storage is blocked |
| Creator Directory | In development | **Live** | + admin-verified contribution points served by `GET /api/community/contributions`, ranking toggle (joined date / contributions); creators cannot edit points |
| Submissions Admin | In development | **Live** | + Contributions page, System panel, CSV export, duplicate protection |
| Community features (rooms, circles, challenges, skill exchange, lab tools) | Planned / Exploring | **Replaced by real features** | Voice Rooms, Transfer, Lab Tools (open to all — no member gate), Contributions, Get listed; the fictional "demo members" diagram is now labelled an illustration |
| Roadmap sections | Planned / Exploring items | **"What shipped"** + one "Documented limitation" line | About timeline, products page and community page updated |

### Backend
- New `server/tools.py` (transfers, voice signalling, AI, contributions, admin system/export) and `server/notify.py` (Discord + SMTP email, background thread, never blocks a submission).
- New tables `transfers`, `contributions` (+ indexes on created_at). `GET /api/health` now reports configured features.
- Duplicate protection: same email + role within 24 h → 409 with the existing reference; same email + building within 1 h → 409.
- Submissions limit raised from 5 to 8 per 10 min per client (room for a corrected resend). CORS extended to the tool endpoints only; admin routes stay same-origin. `Permissions-Policy` now allows the microphone on same-origin pages (it was blocking Voice Rooms when the backend serves the site).
- Admin extras are registered before the generic `/api/admin/{kind}` routes.

### Mobile experience (touch-first, desktop untouched)
- `assets/css/mobile.css` + `assets/js/touch.js`: tap feedback on every control, CSS aurora background layer on phones (canvas stays desktop-only), animated section dividers and kicker accents as sections enter, hero accent line, intentional mobile typography and full-width CTAs.
- Orbit visualization: tap a system → it lights up with its link, one dynamic detail panel appears below with a description and Explore; tap again to open. Keyboard focus still selects; desktop hover still works. Touch targets ≥ 54 px.
- Routing cards become bordered cards with an animated accent bar; "What we build" rows tap to expand and swap the visual; product cards collapse details behind a "Details" toggle; project filters scroll horizontally; creator rows render as cards with staggered entrance; careers/what-we-build list+detail act as an accordion; inputs are 16 px / 48 px; the mobile menu staggers its groups and shows an active-page indicator; the Tools group lists all four tools.
- Bug fixed on the way: the page-transition handler ignored `preventDefault`, and `focusin` pre-selected orbit nodes on tap.

### Tests (all passing on a fresh local server)
audit.py 26 renders (13 pages × desktop/mobile) 0 errors / 0 overflow · e2e.py **48/48** (forms, duplicates, admin, contributions, system, CSV export, transfer API, AI 503) · static_sim.py 20/20 · persona_test.py 13/13 · mobile_test.py **28/28** · perf.py 58–60 fps at 4× CPU throttle (JS 85 KB, CSS 107 KB) · tools walkthrough in a real browser: upload → link → download (bytes identical) → owner delete → expired/invalid states; toolkit persistence, export; AI disabled state; voice 3-way WebRTC with mute and leave.

## Gen 1 refinement (2026-09-17) — MXT delta audit, 10-creator directory, founder mark

Read-only audit of the current public MXT site compared with ETC Labs. Only the genuinely useful differences were
translated into ETC's own design; nothing was copied.

### Delta audit summary
- MXT now: single-page site (Home · About · Creation League · Careers as in-page sections), a 10-creator
  leaderboard "Ranked by Joined Date" with hot-linked YouTube avatars and "--" for three creators without a count,
  a founder spotlight section (quote + focus tags + Discord-hosted avatar), the same five tools (all "In
  Development"/"Exploring"), three projects, five openings, one application form that now also asks for a phone
  number and posts from the browser straight to a chat webhook, no contact email or social links, no footer links.
- Useful for ETC and adopted: the expanded creator list (verified independently, not copied), real avatars
  (self-hosted, not hot-linked), an explicit "--" rule for unavailable counts, a founder spotlight (implemented as
  the ETC founder card with the real ETC mark, focus areas and quote).
- Deliberately not copied: single-page navigation (worse for deep links/SEO), the phone field (unnecessary
  personal data), browser-side webhook submission (exposes the webhook; ETC keeps its server-side API), hot-linked
  avatars, removal of contact channels, MXT product/community names.

### Creator directory (verified 2026-09-17 against each channel page; counts static)
| # | Creator | Handle | Channel id | Subscribers | Avatar |
| --- | --- | --- | --- | --- | --- |
| 1 | Kajuto | @Kajutoo | UCF5ksRyJ9DjjMScxLqPIcFw | 993K | real |
| 2 | UMESH X | @UMESHX_GAMER | UCB_eN9_IzSfJcvoi1sUT74Q | 54.1K | real |
| 3 | AayushLit | @AayushLit | UCnP9sxLR3mSmOx3z4_qCu5A | 38.2K | real |
| 4 | Zaptroo Plays | @ZaptrooPlays | UCrRDtqbqbC0n1uHel6-JUew | 35K | real |
| 5 | VexXD | @VexFr_1 (the supplied @Vexx1_1 does not exist) | UClvphUxileIksrXhN7pWxbA | 7.74K | real |
| 6 | Mystic Priya | @mysticpriya | UCBaBy8eHr8EPfp74jX2mINQ | 4.65K | real |
| 7 | SIRJOHNPVP | @sirjohn.exe20 (the supplied @sirjohn.exe2 does not exist) | UCGBPTlAV54cHLlaX7H7ajVA | 1.67K | real |
| 8 | Rouckz | @RealRouckz | UCLr67LxrHYCjwZPB3IsZLSQ | 343 | real |
| 9 | Hamerplayz | @HamerplayzMc | UCNloqfaBpwsPGBO0ZrNoa0A | 48 | real |
| 10 | BROLYHUOFFICIAL | @BROLYHUOFFICIAL | UCz83lpkB302KvGI6NcX0U1g | 2 | real |

Ranking is by joined date (labelled); subscriber counts are informational metadata. Avatars are the creators'
public YouTube profile images (176 px, 7–22 KB) in `public/assets/img/creators/<handle>.jpg`, with an
initial-letter fallback if an image fails.

### Founder mark (About)
The "one builder" card now uses the official ETC mark (`assets/img/etc-founder.jpg` 512 px + `.webp`, square
crop of the supplied artwork, no redesign) in a circular frame at 200 px (148 px on phones), with "Founded by ETC",
role, description, quote, focus chips and links; subtle border/scale hover, reduced-motion safe, alt text, and a
text fallback if the image fails. No human name invented.

### Fixes
- Creator board: a 52 px gap under the column header (generic `.head` margin leaking onto `.board-row.head`).

### Tests (this update)
audit.py 16/16 renders clean · e2e.py 30/30 · static_sim.py 15/15 · persona_test.py 13/13 (now checks 10 rows) ·
perf.py 60 fps at 4× throttle · broken-image fallbacks for avatars and founder mark verified · live check after deploy.
No backend changes.

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
