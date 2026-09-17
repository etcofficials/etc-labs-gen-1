# ETC Labs — Gen 1

An independent personal technology showcase: a futuristic, touch-first responsive website, four **working
tools** (Transfer, Voice Rooms, AI Utilities, Creator Toolkit), a **real backend** (applications, project requests,
transfers, contributions; resumes stored privately), a **protected admin dashboard**, and a split deployment
(static frontend on GitHub Pages, backend as a container on Render). Nothing on the site is a placeholder: every
product is live, and the few things a deployment can still be missing are documented as configuration.

> **Important:** ETC Labs — Gen 1 is an independent showcase / learning project. It is **not** the official MXT
> website and is **not affiliated with MXT**. The site structure was originally inspired by a recreation exercise
> of a public website; all content, branding, code, data and infrastructure here are ETC Labs' own.

- Live website: **https://etcofficials.github.io/etc-labs-gen-1/**
- Repository: **https://github.com/etcofficials/etc-labs-gen-1**
- Contact: **etcofficials28@gmail.com** · Instagram **[@etcofficials](https://www.instagram.com/etcofficials/)**

## Features

| Area | What is there |
| --- | --- |
| Frontend | 13 pages (Home, What We Build, Products, Projects, Tools, Transfer, Voice Rooms, AI Utilities, Creator Toolkit, Community, About, Careers, Contact), one coherent animated "world" background (canvas flow lines on desktop, CSS aurora on phones), short opening sequence, cursor tracker, page transitions, tap-to-select orbit visualization with a detail panel, expandable cards, reduced-motion support, tested from 320 px to 1440 px |
| Transfer | Send a file with a link: drag & drop up to 25 MB, upload progress, expiry (24 h / 3 d / 7 d or 100 downloads), owner-only deletion, attachment-only downloads (`transfer.html`) |
| Voice Rooms | Peer-to-peer WebRTC audio for up to six people, signalled over a WebSocket on the backend; mute, participant list, connection state, leave (`voice.html`) |
| AI Utilities | Summarize / rewrite / content ideas / titles through the backend (`POST /api/ai/{tool}`), rate-limited, key only on the server; honest "not enabled" state without a key (`ai.html`) |
| Creator Toolkit | Local-first ideas board, publishing checklist and project tracking with JSON export/import — stored in the browser, no account (`toolkit.html`) |
| About | Founder card using the official ETC mark (`etc-founder.jpg/.webp`), no invented team |
| Community | Verified creator directory (10 creators, each checked against the exact YouTube channel on 2026-09-17) with admin-verified **contribution points** served by the backend and a joined-date / contributions ranking toggle |
| Contact | Email (`mailto:`), copy-to-clipboard, Instagram (new tab, `noopener noreferrer`), and a project-request form with validation / loading / success / failure states |
| Careers | 5 collaboration roles with details, application form with optional resume upload (PDF/DOC/DOCX ≤ 5 MB) |
| Backend | FastAPI + SQLite: submissions, transfers, voice signalling, AI proxy, contributions; server-side validation, magic-byte file checks, honeypot + minimum-time spam protection, duplicate protection, per-client rate limiting, audit log, optional Discord/email notifications |
| Admin | `/admin/` on the backend: dashboard, applications & requests (search / filters / detail / status flow / notes / archive / private resume download / CSV export), contributions (record verified creator work), system panel (health, storage, feature configuration, limits — never secret values), settings with login activity |
| Authentication | scrypt password hash (from env), HMAC-signed HttpOnly `SameSite=Strict` cookie, custom header on every state-changing request, login rate limit |
| Deployment | GitHub Pages (frontend) + Docker image (backend) with `render.yaml` / `fly.toml`; CORS restricted to the frontend origin; `.env.example`; no secrets in the repo |

## Architecture

```
Browser ──▶ GitHub Pages  (public/  — static HTML/CSS/JS)
   │             assets/js/config.js → apiBase = backend URL
   │
   ├──▶ WebRTC (peer ↔ peer)   voice audio never touches the server; STUN built in, TURN optional
   │
   └──▶ Backend host (Render, Docker: FastAPI + uvicorn)  https://etc-labs-gen-1.onrender.com
             ├── /api/project-requests, /api/applications   ← public, CORS-limited to the Pages origin
             ├── /api/transfers/*                            ← upload / info / download / owner delete
             ├── /ws/voice/{room}, /api/voice/*              ← signalling (origin-checked WebSocket), room codes, ICE config
             ├── /api/ai/{tool}                              ← model calls with the key from the environment
             ├── /api/community/contributions                ← public aggregate of admin-verified points
             ├── /api/admin/*                                ← cookie session + X-ETC-Admin header
             ├── /admin/                                     ← admin dashboard (served by the backend)
             └── $ETC_DATA_DIR/  (persistent disk)
                    ├── etc-labs.sqlite3   applications, project_requests, notes, audit_log, transfers, contributions
                    ├── uploads/           resumes, random file names, admin-only download
                    ├── transfers/         transfer files, random names, deleted on expiry
                    └── logs/server.log
```

The backend can also serve the whole site by itself (it mounts `public/` at `/`), which is how local
development works.

## Project structure

```text
etc-labs-gen-1/
│
├── public/                      public website (deployed to GitHub Pages)
│   ├── index.html               home (hand-written)
│   ├── what-we-do.html · products.html · projects.html · community.html
│   ├── tools.html · transfer.html · voice.html · ai.html · toolkit.html
│   ├── about.html · careers.html · contact.html      (all generated by build_pages.py)
│   ├── admin/index.html         redirects to <backend>/admin/ (or explains it is not configured)
│   └── assets/
│       ├── css/                 tokens · base · world · components · pages · mobile
│       ├── js/                  config (backend URL) · data (all content) · world · ui · pages · touch · forms · tools
│       └── img/                 etc-logo.svg · etc-logo-mask.svg · favicon.svg · og.png · creators/*.jpg
│
├── admin/                       admin dashboard SPA (index.html, admin.js, admin.css, logo.svg) — served by the backend
├── server/                      FastAPI backend: app.py · tools.py · notify.py · config.py · db.py · security.py · cli.py
├── docs/                        screenshots/, CHANGELOG.md, test scripts (audit, perf, e2e, static_sim, persona, mobile, live)
│
├── build_pages.py               regenerates the seven content pages from one shell
├── Dockerfile · .dockerignore   backend container
├── render.yaml · fly.toml       backend hosting configs (Render / Fly.io)
├── README.md
├── .gitignore                   ignores .env, data/, caches
└── .env.example                 variable names only — copy to .env and fill in
```

## Local development

Requirements: Python 3.11+.

```bash
pip install -r server/requirements.txt
cp .env.example .env
python -m server.cli set-admin-password       # prompts; prints ETC_ADMIN_PASSWORD_HASH=... → paste into .env
python -m uvicorn server.app:app --port 8790  # http://localhost:8790  (site)  ·  http://localhost:8790/admin/  (admin)
```

Optional: `python -m server.cli seed-demo` inserts five rows labelled **DEMO** so the dashboard is not empty;
`python -m server.cli purge-demo` removes them. `python -m server.cli stats` prints counts.

After editing `build_pages.py`, run `python build_pages.py` to regenerate the content pages. All repeated
content (services, products, projects, creators, roadmap, roles, nav, contact details) lives in
`public/assets/js/data.js`.

## Environment variables (backend)

Copy `.env.example` to `.env`. Never commit `.env`.

| Variable | Required | Meaning |
| --- | --- | --- |
| `ETC_ADMIN_USER` | yes | Admin username (default `admin`) |
| `ETC_ADMIN_PASSWORD_HASH` | yes | scrypt hash printed by `python -m server.cli set-admin-password` — never the password itself |
| `ETC_SECRET_KEY` | production | 32+ random characters used to sign session cookies (locally a key is generated into `data/.secret_key`) |
| `ETC_ALLOWED_ORIGINS` | when frontend is on Pages | Comma-separated origins allowed to call the public submission API, e.g. `https://etcofficials.github.io` |
| `ETC_SECURE_COOKIES` | production | `1` when the backend is served over HTTPS |
| `ETC_DATA_DIR` | production | Directory for the database, uploads and logs — point it at a persistent disk |
| `ETC_SITE_URL` | production | Public site URL used in generated links (transfer links, room links) |
| `ETC_ANTHROPIC_API_KEY`, `ETC_AI_MODEL` | optional | Enables AI Utilities (default model `claude-opus-5`). Without the key the tool shows an honest "not enabled" state |
| `ETC_TURN_URL`, `ETC_TURN_USER`, `ETC_TURN_PASS` | optional | TURN relay for Voice Rooms on strict NATs; STUN is built in |
| `ETC_DISCORD_WEBHOOK_URL` | optional | Server-side chat notification on new submissions |
| `ETC_SMTP_HOST/PORT/USER/PASS/TLS`, `ETC_NOTIFY_FROM`, `ETC_NOTIFY_TO` | optional | Server-side email notification on new submissions |
| `ETC_MAX_UPLOAD_MB`, `ETC_TRANSFER_MAX_MB`, `ETC_SESSION_HOURS` | optional | Resume limit (5), transfer limit (25), session length (12 h) |

The frontend has exactly one deployment setting, and it is not a secret: `public/assets/js/config.js →
apiBase` (the backend URL).

## Backend setup and deployment

The backend is a single Docker image (`Dockerfile`). It needs a host that can run a container **and keep a
persistent disk** for `$ETC_DATA_DIR` (SQLite + resumes). Two ready-made configs are included:

**Render (recommended, simplest):**
1. Push this repo to GitHub (done) and sign in at https://dashboard.render.com with GitHub.
2. *New → Blueprint* → select `etcofficials/etc-labs-gen-1`. Render reads `render.yaml`: a Docker web service
   with a 1 GB disk mounted at `/var/data`, `ETC_SECRET_KEY` auto-generated, `ETC_SECURE_COOKIES=1`,
   `ETC_ALLOWED_ORIGINS=https://etcofficials.github.io`.
3. When asked for `ETC_ADMIN_PASSWORD_HASH`, paste the value printed locally by
   `python -m server.cli set-admin-password` (the hash, not the password).
4. Deploy. Your backend URL will look like `https://etc-labs-gen-1-api.onrender.com`. Check
   `https://<backend>/api/health` → `{"ok": true, "admin_configured": true}`.
   *Note:* a persistent disk needs a paid instance type on Render; on the free tier the disk line in `render.yaml`
   must be removed and **data is lost on every deploy** — fine for a demo, not for real submissions.

**Fly.io (alternative, has a free allowance with volumes):** `fly launch --copy-config --yes`, then
`fly volumes create etc_data --size 1`, `fly secrets set ETC_ADMIN_PASSWORD_HASH='…' ETC_SECRET_KEY='…'`,
`fly deploy`.

**Any Docker host / VPS:** `docker build -t etc-labs . && docker run -p 8000:8000 -v etc_data:/var/data
--env-file .env etc-labs`, behind a TLS-terminating proxy (Caddy/nginx) with `ETC_SECURE_COOKIES=1`.

**Connect the frontend:** put the backend URL into `public/assets/js/config.js` (`apiBase:
"https://<backend>"`), commit and push — GitHub Pages redeploys automatically. Until this is done the forms
show an honest "backend isn't connected on this deployment yet — email us" state (they never fake success).

## Frontend deployment (GitHub Pages)

The workflow `.github/workflows/pages.yml` uploads the `public/` folder as the Pages artifact on every push
to `main` and deploys it (GitHub's "deploy from a branch" mode only offers `/` or `/docs`, so Actions is used).
Repository *Settings → Pages → Source* must be **GitHub Actions** — the workflow enables this automatically on
its first run. All links and asset paths are relative, so the site works under the `/etc-labs-gen-1/` sub-path.

## Admin

- **ADMIN URL:** `https://<backend-url>/admin/` (for local development: http://localhost:8790/admin/)
- **LOGIN URL:** the same page — it shows the login form when you are signed out.
- The public site's `/admin/` path (`https://etcofficials.github.io/etc-labs-gen-1/admin/`) redirects to the
  backend admin once `apiBase` is configured.
- Account: one admin account, username from `ETC_ADMIN_USER`, password set by you via
  `python -m server.cli set-admin-password` (stored only as a scrypt hash in the backend's environment).
- Sessions last 12 hours; *Sign out* is in the sidebar. **Settings** shows last successful login, last failed
  attempt, failed attempts in 24 h, total logins and the recent login/logout events. The public website has no
  user accounts, so there are no public-user login records — and nothing is tracked about visitors.

## API

Public (submissions rate-limited 8 / 10 min per client; CORS limited to `ETC_ALLOWED_ORIGINS`):
- `POST /api/project-requests` — JSON `{name, email, discord?, building, need, scale?, timeline?, message, website (honeypot), started_at}` · 409 if the same email sent the same request within an hour
- `POST /api/applications` — multipart `{firstName, lastName, email, discord, position, portfolio?, cover?, resume? (pdf/doc/docx ≤ 5 MB), website, started_at}` · 409 if the same email applied for the same role within 24 h
- `GET /api/health` — includes which optional features are configured
- Transfer: `GET /api/transfers/config` · `POST /api/transfers` (multipart `file`, `ttl` = 24h|3d|7d; 10 / hour) · `GET /api/transfers/{id}` · `GET /api/transfers/{id}/download` (attachment, nosniff) · `DELETE /api/transfers/{id}?token=` (owner token)
- Voice: `GET /api/voice/config` (ICE servers) · `POST /api/voice/rooms` (new code) · `GET /api/voice/rooms/{code}` · `WS /ws/voice/{code}` (join → welcome/peers; signal relay; mute; leave)
- AI: `GET /api/ai/status` · `POST /api/ai/{summarize|rewrite|ideas|titles}` `{text ≤ 6000 chars, option?}` (20 / hour; 503 `configured:false` without a key)
- Community: `GET /api/community/contributions` — points per creator handle (no notes, no verifier)

Admin (cookie session + `X-ETC-Admin: 1` header on non-GET; never exposed via CORS):
- `POST /api/admin/login` · `POST /api/admin/logout` · `GET /api/admin/me` · `GET /api/admin/summary` · `GET /api/admin/account`
- `GET /api/admin/{applications|requests}?status=&q=&position=&need=&archived=&date_from=&date_to=`
- `GET|PATCH /api/admin/{kind}/{id}` (`{status, archived}`) · `POST /api/admin/{kind}/{id}/notes` · `DELETE /api/admin/notes/{id}`
- `GET /api/admin/applications/{id}/resume` — attachment download, audited
- `GET|POST /api/admin/contributions` · `DELETE /api/admin/contributions/{id}` — verified creator contributions (handle, kind, 1–100 points, note)
- `GET /api/admin/system` — uptime, data dir + persistence warning, disk/db/upload/transfer sizes, open rooms, configured features (booleans only), limits
- `GET /api/admin/export/{applications|requests}.csv` — CSV export (internal columns omitted, formula-safe)

Status flows — applications: `new → reviewing → shortlisted → interview → rejected | hired`;
project requests: `new → reviewing → replied → scoping → won | closed`.

## Database

SQLite (`$ETC_DATA_DIR/etc-labs.sqlite3`, WAL mode), created automatically:

| Table | Important fields |
| --- | --- |
| `applications` | id, created_at, updated_at, first_name, last_name, email, discord, position, portfolio, cover_letter, resume_path (random stored name), resume_name, resume_size, status, archived, is_demo |
| `project_requests` | id, created_at, updated_at, name, email, discord, building, need, scale, timeline, message, status, archived, is_demo |
| `notes` | id, kind, target_id, created_at, author, body |
| `transfers` | id, created_at, expires_at, original_name, stored_name (random), size, downloads, max_downloads, owner_token, deleted |
| `contributions` | id, created_at, creator_handle, kind (project/collaboration/event/content/other), points, note, verified_by |
| `audit_log` | id, created_at, actor, action, target (submissions, logins, status changes, downloads, transfers, contributions) |

No passwords are stored in any table. Client IPs are not stored — only a keyed hash used for rate limiting.

## Security notes

- Secrets only in environment variables; `.env` is git-ignored; `.env.example` has names only.
- All input validated server-side (lengths, email, URL, enum statuses); resumes checked by extension, size
  **and** magic bytes, stored under random names outside the web root, served only through the admin API.
- Admin: scrypt hashes, HMAC-signed expiring cookie (HttpOnly, SameSite=Strict, Secure in production),
  custom header required on writes (CSRF defence in depth), 6 login attempts / 15 min, 0.4 s delay on failure.
- Security headers on every response; CSP on the backend-served pages and admin (no inline scripts).
- CORS only for the two public submission endpoints and only for the configured frontend origin.
- Rate limiting per client: 8 submissions / 10 min, 10 transfers / hour, 20 AI calls / hour, 30 rooms / hour, 240 admin calls / min.
- Transfers: random opaque IDs, files stored under random names, always served as `application/octet-stream` attachments with `nosniff` (an uploaded HTML/SVG can never execute on the origin), deleted on expiry or after 100 downloads, owner-token deletion.
- Voice: the WebSocket checks the `Origin` header against the allowed origins; audio is peer-to-peer and never relayed or stored; rooms are capped at six and vanish when empty.
- AI: text limited to 6,000 characters, nothing is stored, the provider key only exists in the server environment.

## Testing

Run while the server is up (needs `playwright` + Edge/Chromium):

| Script | What it checks |
| --- | --- |
| `docs/audit.py` | every page × desktop/mobile: JS errors, horizontal overflow, tiny text, small touch targets; writes screenshots |
| `docs/perf.py` | fps idle + scrolling at 1× and 4× CPU throttling (desktop and mobile), keyboard navigation, reduced motion |
| `docs/e2e.py` | forms (missing fields, invalid email, loading, success, failure, fake-PDF rejection, real resume upload) and admin (401, wrong password, login, counts, search, filters, detail, status persistence, resume download, traversal, header check, logout) — 30 checks |
| `docs/static_sim.py` | the GitHub Pages deployment simulated in-browser: relative paths, no 404s, honest "not connected" state, admin redirect, real cross-origin submission through CORS |
| `docs/persona_test.py` | five visitor personas (first-timer, client, creator, applicant, admin) |
| `docs/mobile_test.py` | touch-first checks at 390 px (orbit tap-select, build rows, filters, expandable products, creator cards, nav stagger, careers) + no-overflow sweep at 320/360/390/412/430/480/768/1024/1440 px |
| `docs/live_check.py` | the deployed GitHub Pages site in a real browser |
| `docs/cleanup_tests.py` | removes any rows the test scripts left behind |

## Documented limitations (configuration, not missing code)

| Item | What is needed | Until then |
| --- | --- | --- |
| AI Utilities on the live backend | `ETC_ANTHROPIC_API_KEY` on Render | the page shows "Not enabled on this deployment yet"; the API answers 503 `configured:false` |
| Voice Rooms on strict corporate NATs | a TURN relay via `ETC_TURN_URL/USER/PASS` | rooms work on normal home/mobile networks with the built-in STUN; the room shows "no route" for a peer it cannot reach |
| Data persistence on Render | a disk mounted at `/var/data` + `ETC_DATA_DIR=/var/data` (see `render.yaml`) | the admin System page shows a persistence warning; SQLite, resumes and transfers reset on each deploy |
| Email notifications | `ETC_SMTP_*`, `ETC_NOTIFY_FROM`, `ETC_NOTIFY_TO` | nothing is sent; submissions are still stored and visible in the admin |

## Creator directory data

Stored in `public/assets/js/data.js → ETC.creators.rows`. Each row: `name`, `handle`, `subscribers`,
`channelUrl`, `channelId`, `avatarUrl` (local file in `public/assets/img/creators/`), `avatarSource`,
`verifiedAt`. Counts are **static** snapshots verified by hand against each channel page (no API, nothing is
fetched live). To update a creator: open `channelUrl`, re-check, edit the row, bump `verifiedAt`. To add one:
append a row with the next `rank` (ranking is by joined date, not audience) and drop the avatar into
`public/assets/img/creators/`. Rows without a count show "—".

## Changelog

See [docs/CHANGELOG.md](docs/CHANGELOG.md).
