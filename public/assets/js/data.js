/* ==========================================================================
   ETC Labs — Gen 1 · Site content. Edit this file to change what the site says.
   No secrets live here; forms talk to the backend at `${ETC_CONFIG.apiBase}/api/*`.

   ETC Labs — Gen 1 is an independent personal technology showcase.
   It is not affiliated with MXT or any other organization.
   ========================================================================== */
window.ETC = window.ETC || {};

ETC.config = {
  brand: "ETC Labs",
  gen: "Gen 1",
  email: "etcofficials28@gmail.com",
  instagram: { handle: "@etcofficials", url: "https://www.instagram.com/etcofficials/" },
  github: "https://github.com/etcofficials/etc-labs-gen-1",
  apiBase: (window.ETC_CONFIG && window.ETC_CONFIG.apiBase || "").replace(/\/+$/, "")
};

ETC.nav = [
  { key: "what-we-do", label: "What We Build", href: "what-we-do.html", group: "Explore" },
  { key: "products", label: "Products", href: "products.html", group: "Explore" },
  { key: "projects", label: "Projects", href: "projects.html", group: "Explore" },
  { key: "community", label: "Community", href: "community.html", group: "Community" },
  { key: "about", label: "About", href: "about.html", group: "Lab" },
  { key: "careers", label: "Careers", href: "careers.html", group: "Lab" }
];
ETC.cta = { label: "Contact", href: "contact.html" };

/* ---- Icons (one stroke style) ---- */
const I = (d) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
ETC.icons = {
  code: I('<path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>'),
  ai: I('<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="4"/>'),
  design: I('<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><path d="M17 13v8M13 17h8"/>'),
  infra: I('<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>'),
  shield: I('<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>'),
  rooms: I('<path d="M4 5h16v11H8l-4 4V5Z"/><path d="M8 9h8M8 12h5"/>'),
  circle: I('<circle cx="12" cy="7" r="3"/><circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="M12 10v2.5M9.6 9.5 6.5 14M14.4 9.5l3.1 4.5"/>'),
  trophy: I('<path d="M8 4h8v5a4 4 0 0 1-8 0V4Z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M9 21h6M10 17h4"/>'),
  showcase: I('<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M7 13l3-3 2 2 4-4 1 1"/>'),
  exchange: I('<path d="M4 8h13l-3-3M20 16H7l3 3"/>'),
  tools: I('<path d="m14.5 6.5 3 3L9 18H6v-3l8.5-8.5Z"/><path d="M13 8l3 3M4 20h16"/>'),
  upload: I('<path d="M12 16V4M6 10l6-6 6 6M4 20h16"/>'),
  info: I('<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>'),
  mail: I('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
  instagram: I('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>'),
  arrow: '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M9 7h8v8"/></svg>',
  arrowRight: '<svg class="arrow right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  check: '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 7"/></svg>'
};

/* ---- The five things ETC Labs builds (hero + ecosystem + "what we build") ---- */
ETC.build = [
  { key: "software", title: "Software", text: "Websites, web apps and internal tools — like this site, its backend and its admin dashboard.", color: "#22d3ee", mock: "tools", href: "what-we-do.html#software" },
  { key: "ai", title: "AI systems", text: "Assistants, automations and model integrations wired into real workflows.", color: "#8b5cf6", mock: "ai", href: "what-we-do.html#ai" },
  { key: "products", title: "Digital products", text: "Our own tools and experiments — from concept to something you can actually use.", color: "#e879f9", mock: "transfer", href: "products.html" },
  { key: "infra", title: "Infrastructure", text: "Deployment, databases, storage and the pipeline that keeps a product online.", color: "#60a5fa", mock: "infra", href: "what-we-do.html#infrastructure" },
  { key: "community", title: "Creator & community systems", text: "A creator directory and community tools — built for people who make things.", color: "#34d399", mock: "community", href: "community.html" }
];

/* ---- What we build (services / areas) ---- */
ETC.services = [
  { num: "01", icon: "code", key: "software", mock: "tools", accent: "cyan", title: "Software Engineering",
    short: "Websites, web apps, internal tools and custom software.",
    what: "We design and build web applications, internal tools and custom software. The site you are reading — its pages, backend API and admin dashboard — is the first worked example.",
    who: "Founders, small teams and creators who need something built properly, not from a template.",
    get: ["Web applications", "Internal tools & dashboards", "APIs & integrations", "Forms with real backends", "Custom platforms"] },
  { num: "02", icon: "ai", key: "ai", mock: "ai", accent: "violet", title: "AI & Automation",
    short: "AI assistants, automated workflows and model integrations.",
    what: "We connect AI models to real work: assistants, content pipelines, data processing and the automations that remove repetitive steps.",
    who: "Teams drowning in manual steps, and creators who want tooling around their process.",
    get: ["AI assistants & agents", "Workflow automation", "Model integrations", "Content & data pipelines", "Internal AI tools"] },
  { num: "03", icon: "design", key: "design", mock: "brand", accent: "magenta", title: "Product & UI Design",
    short: "Interfaces, prototypes, motion and design systems.",
    what: "We shape how a product looks and behaves — from the first wireframe to a design system and motion language the whole build can follow.",
    who: "Anyone launching a product, redesigning one, or tired of an interface people don't understand.",
    get: ["UI / UX design", "Interactive prototypes", "Design systems & tokens", "Animation & interaction design", "Landing pages & brand sites"] },
  { num: "04", icon: "infra", key: "infrastructure", mock: "infra", accent: "blue", title: "Infrastructure & Deployment",
    short: "Hosting, deployment, databases and the parts users never see.",
    what: "We set up what holds a product together: static hosting, API deployment, databases, file storage, environment configuration and Git-based workflows.",
    who: "Products that need to stay up, deploy cleanly and talk to other services.",
    get: ["Deployment & hosting setup", "Databases & storage", "CI / Git workflows", "Third-party integrations", "Monitoring & operations"] },
  { num: "05", icon: "shield", key: "security", mock: "members", accent: "green", title: "Security & Reliability",
    short: "Security-minded engineering and systems that don't fall over.",
    what: "We build with security as a default — authentication, access control, validated uploads, rate limiting and sane operations — so a product doesn't break the first time it matters.",
    who: "Teams handling user data, submissions, communities or anything that would hurt to lose.",
    get: ["Auth & session architecture", "Server-side validation", "Secure file handling", "Rate limiting & spam protection", "Operational guidance"] }
];

/* ---- Products: things ETC Labs is building for people to use ---- */
ETC.productGroups = [
  { key: "live", label: "Live", badge: "badge-live", intro: "Usable now. Only what is genuinely running qualifies — we'd rather list one real thing than pad the list.",
    items: [
      { name: "Gen 1 Platform", mock: "brand", accent: "cyan", status: "Live", tagline: "This website, its submissions backend and the admin dashboard — the first complete ETC Labs build.",
        problem: "A showcase should prove the whole stack works: design, motion, forms that store real data, a protected admin and a clean deployment — not just a pretty landing page.",
        who: ["Visitors", "Collaborators", "Anyone evaluating the work"],
        keys: ["Futuristic responsive frontend with purposeful motion", "Real applications & contact backend (FastAPI + SQLite)", "Protected admin dashboard with status tracking"],
        cta: { label: "See how it was built", href: "projects.html#gen1-platform" } }
    ] },
  { key: "dev", label: "In development", badge: "badge-dev", intro: "Being built right now. Not released, and details may change.",
    items: [
      { name: "Creator Directory", mock: "community", accent: "magenta", status: "In development", tagline: "A verified directory of creators around ETC Labs — real channels, real public counts, no fabricated stats.",
        problem: "Creator lists on the web are usually stale or wrong. This one is verified against each channel and says when it was last checked.", who: ["Creators", "Collaborators"],
        keys: ["Verified channel links and avatars", "Public subscriber counts with a verification date", "Ranked by joined date, not audience"], cta: { label: "Open the directory", href: "community.html#creators" } },
      { name: "Submissions Admin", mock: "members", accent: "violet", status: "In development · Internal", tagline: "The internal tool behind the careers and contact forms: search, filters, status flow, notes and secure resume access.",
        problem: "Submissions should land somewhere a person can actually manage them — with statuses that persist, not an inbox.", who: ["ETC Labs (internal)"],
        keys: ["Applications: NEW → REVIEWING → SHORTLISTED → INTERVIEW → REJECTED / HIRED", "Project requests with status and notes", "Private resume storage, admin-only download"], cta: { label: "View project", href: "projects.html#submissions-backend" } }
    ] },
  { key: "exploring", label: "Exploring", badge: "badge-exploring", intro: "Ideas we're researching or prototyping. No timeline, no promises — listed so you know where we're looking.",
    items: [
      { name: "Transfer", mock: "transfer", accent: "cyan", status: "Planned", tagline: "Fast, temporary file sharing with no account and privacy by default.", problem: "Sending a large file shouldn't need an account, an app install or a ten-step upload flow.", who: ["Creators", "Small teams"], keys: [], cta: null },
      { name: "Voice Rooms", mock: "voice", accent: "blue", status: "Exploring", tagline: "A focused realtime voice room for small teams and creator groups.", problem: "Most collaboration tools are noisy. We're exploring whether a smaller one can just work.", who: ["Creator groups", "Small teams"], keys: [], cta: null },
      { name: "AI Utilities", mock: "ai", accent: "violet", status: "Exploring", tagline: "Small AI tools for the repetitive parts of creator and team work.", problem: "Organizing, drafting and formatting eat the hours that should go into making things.", who: ["Creators", "Teams"], keys: [], cta: null },
      { name: "Creator Toolkit", mock: "toolkit", accent: "magenta", status: "Exploring", tagline: "Utilities to help creators organize, publish and collaborate.", problem: "Creator workflows are scattered across ten apps. We're finding out whether one focused toolkit would help.", who: ["Creators"], keys: [], cta: null }
    ] }
];

/* ---- Projects: builds, experiments and showcase pieces ---- */
ETC.projectCategories = [
  { key: "all", label: "All" }, { key: "software", label: "Software" }, { key: "design", label: "Design" }, { key: "infrastructure", label: "Infrastructure" }, { key: "ai", label: "AI" }, { key: "creative", label: "Creative" }
];
ETC.projects = [
  { id: "gen1-platform", name: "Gen 1 Website", category: "design", catLabel: "Frontend · Design system", status: "Live", badge: "badge-live", mock: "brand", accent: "cyan",
    problem: "A showcase site needs to feel futuristic and stay fast on mid-range phones at the same time.", built: "Eight static pages, one coherent animated background, a cursor tracker, page transitions and a product-mock kit — vanilla HTML, CSS and JS, no framework.", approach: "Design tokens, transform/opacity-only motion, IntersectionObserver reveals, reduced-motion support", desc: "The site you are on: a futuristic, responsive frontend built without a framework, tuned for 60 fps on throttled CPUs.",
    focus: ["HTML / CSS / JS", "Design tokens", "Motion design", "Accessibility"], links: [{ label: "You're looking at it", href: "index.html" }, { label: "Source on GitHub", href: "https://github.com/etcofficials/etc-labs-gen-1", external: true }] },
  { id: "submissions-backend", name: "Submissions Backend & Admin", category: "software", catLabel: "Backend · Internal tool", status: "Live", badge: "badge-live", mock: "members", accent: "violet",
    problem: "Careers and contact forms usually go nowhere — or to an inbox that nobody tracks.", built: "A FastAPI + SQLite backend that stores applications and project requests, validates resumes server-side and stores them privately, plus an admin dashboard with login, search, filters, a status flow and notes.", approach: "Server-side validation, scrypt password hashing, signed HttpOnly session cookies, rate limiting, honeypot + timing checks", desc: "The real backend behind the forms on this site, and the internal dashboard that manages what comes in.",
    focus: ["Python / FastAPI", "SQLite", "Authentication", "File uploads"], links: [{ label: "Try the contact form", href: "contact.html" }] },
  { id: "creator-directory", name: "Creator Directory", category: "creative", catLabel: "Community · Data", status: "Live", badge: "badge-live", mock: "community", accent: "magenta",
    problem: "Creator leaderboards go stale and quietly lie about numbers.", built: "A creator directory where every row was checked against the exact YouTube channel — name, handle, avatar, public subscriber count and link — with a visible verification date.", approach: "Manual verification against each channel page, stored avatars, static counts with a dated audit", desc: "Verified creators around ETC Labs, ranked by joined date, with public audience numbers that say when they were last checked.",
    focus: ["Data verification", "Responsive tables", "Image fallbacks"], links: [{ label: "Open the directory", href: "community.html#creators" }] },
  { id: "deployment", name: "Deployment Pipeline", category: "infrastructure", catLabel: "Infrastructure", status: "Live", badge: "badge-live", mock: "infra", accent: "blue",
    problem: "A static host can't run a private database, but the site still needs a real backend.", built: "Frontend on GitHub Pages, backend as a container on a separate host, environment-based configuration, a .env.example and a secrets scan before every push.", approach: "GitHub Pages + containerized API, CORS scoped to the frontend origin, no secrets in the repository", desc: "How the public site and the private backend are deployed separately and connected securely.",
    focus: ["GitHub Pages", "Docker", "Environment config", "CORS"], links: [{ label: "Deployment notes", href: "https://github.com/etcofficials/etc-labs-gen-1#deployment", external: true }] },
  { id: "world-background", name: "The World Background", category: "design", catLabel: "Interaction · Performance", status: "Live", badge: "badge-live", mock: "world", accent: "cyan",
    problem: "Animated backgrounds usually either look generic or destroy frame rate.", built: "A layered background — base gradient, tone-following lights, a faint grid, a lightweight flow-line canvas capped at 30 fps and desktop only, a pointer light and static noise — that shifts colour with the section in view.", approach: "Fixed layers, CSS transforms, capped canvas work, everything heavy disabled on touch devices and under reduced-motion", desc: "One coherent visual world across every page, measured at 60 fps while scrolling under 4× CPU throttling.",
    focus: ["Canvas", "CSS", "Performance budgets"], links: [{ label: "Scroll this page", href: "index.html" }] },
  { id: "transfer", name: "Transfer", category: "software", catLabel: "Digital utility", status: "Planned", badge: "badge-planned", mock: "transfer", accent: "cyan",
    problem: "Sharing a large file still needs an account or an app.", built: "Nothing public yet — the concept is a web app: drop a file, get a link that expires. No sign-up.", approach: "Web app, streaming uploads, privacy-first", desc: "A planned temporary file-sharing tool with no account, no clutter and privacy as the default.",
    focus: ["Concept", "File handling", "Privacy-first"], links: [] },
  { id: "voice-rooms", name: "Voice Rooms", category: "software", catLabel: "Realtime", status: "Exploring", badge: "badge-exploring", mock: "voice", accent: "blue",
    problem: "Collaboration calls are noisy and heavy.", built: "Nothing public yet — exploring a small, focused realtime voice environment for creator groups.", approach: "WebRTC research, small-group UX", desc: "An exploration into a lighter realtime voice room for small teams and creator groups.",
    focus: ["Research", "WebRTC", "Small-group UX"], links: [] },
  { id: "ai-utilities", name: "AI Utilities", category: "ai", catLabel: "AI experiments", status: "Exploring", badge: "badge-exploring", mock: "ai", accent: "violet",
    problem: "Repetitive digital work eats creative time.", built: "Prototyping small AI utilities for drafting, organising and automating — nothing released.", approach: "LLM integrations, workflow automation", desc: "Experiments with AI utilities for creators and teams — drafting, organizing and automating repetitive work.",
    focus: ["LLM integrations", "Automation", "Prototyping"], links: [] },
  { id: "creator-toolkit", name: "Creator Toolkit", category: "creative", catLabel: "Creator tools", status: "Exploring", badge: "badge-exploring", mock: "toolkit", accent: "magenta",
    problem: "Creator workflows are scattered across ten apps.", built: "Nothing yet — researching whether a focused toolkit would actually help.", approach: "Research, creator conversations", desc: "Utilities and workflows to help creators organize, publish and collaborate more efficiently.",
    focus: ["Research", "Creator workflows"], links: [] }
];

/* ---- Community ---- */
ETC.communityFeatures = [
  { icon: "showcase", title: "Creator Directory", text: "A verified list of creators around ETC Labs with real channel links and dated public counts.", tag: "Discover", status: "live" },
  { icon: "rooms", title: "Creator Rooms", text: "Spaces organized by discipline, interest and active project.", tag: "Connect", status: "planned" },
  { icon: "circle", title: "Build Circles", text: "Small groups working on ideas together, with accountability and feedback.", tag: "Collaborate", status: "planned" },
  { icon: "trophy", title: "Creation Challenges", text: "Creative and technical challenges that push toward finished work.", tag: "Create", status: "planned" },
  { icon: "exchange", title: "Skill Exchange", text: "Members teach and learn from each other through practical critique.", tag: "Learn", status: "exploring" },
  { icon: "tools", title: "Lab Tools", text: "Early access to ETC Labs utilities and experiments as they become usable.", tag: "Build", status: "exploring" }
];
ETC.communityStatus = { live: ["badge-live", "Live"], planned: ["badge-planned", "Planned"], exploring: ["badge-exploring", "Exploring"] };
ETC.communityWho = ["Video creators", "Editors", "Designers", "Developers", "Artists", "Streamers", "Writers", "Musicians", "Game creators", "Photographers", "Builders", "Creative teams"];
ETC.communityWhy = [
  { title: "Meet collaborators", text: "Editors, designers, developers, artists, streamers, writers — people with the skills you don't have." },
  { title: "Build together", text: "Form a project team, exchange skills and turn an idea into finished work." },
  { title: "Learn in public", text: "Share progress, get honest feedback, improve with the community's knowledge." },
  { title: "Get discovered", text: "Show meaningful work and open new paths to collaboration and opportunity." }
];
/* Demo members — fictional roles that illustrate how the community concept works. Clearly labelled as demo in the UI. */
ETC.communityDemo = [
  { role: "Developer", skill: "Web & bots", color: "#22d3ee" }, { role: "Designer", skill: "UI & brand", color: "#60a5fa" }, { role: "Video Editor", skill: "Edits & motion", color: "#e879f9" },
  { role: "Artist", skill: "Illustration", color: "#fbbf24" }, { role: "Writer", skill: "Scripts & copy", color: "#34d399" }, { role: "Builder", skill: "Projects & ops", color: "#8b5cf6" }
];

/* ---- Creator directory ----
   Every row was verified against the exact YouTube channel page on `verifiedAt`
   (channel name, handle, channel id, public subscriber count, avatar). Counts are STATIC —
   they are not fetched live. To update: open channelUrl, re-check, edit the row, bump verifiedAt.
   Avatars are the creators' public YouTube profile images, stored in assets/img/creators/.
   Ranking is by joined date (rank field), not by subscriber count. */
ETC.creators = {
  rankedBy: "joined date", verifiedAt: "2026-09-16", source: "YouTube channel pages (public subscriber count as displayed by YouTube)",
  note: "Audience numbers are the public counts YouTube displayed on the verification date; they are not live.",
  rows: [
    { rank: 1, name: "Zaptroo Plays", handle: "@ZaptrooPlays", subscribers: "35K", platform: "YouTube", channelUrl: "https://www.youtube.com/@ZaptrooPlays", channelId: "UCrRDtqbqbC0n1uHel6-JUew", avatarUrl: "assets/img/creators/ZaptrooPlays.jpg", avatarSource: "YouTube", verifiedAt: "2026-09-16" },
    { rank: 2, name: "Kajuto", handle: "@Kajutoo", subscribers: "992K", platform: "YouTube", channelUrl: "https://www.youtube.com/@Kajutoo", channelId: "UCF5ksRyJ9DjjMScxLqPIcFw", avatarUrl: "assets/img/creators/Kajutoo.jpg", avatarSource: "YouTube", verifiedAt: "2026-09-16" },
    { rank: 3, name: "Rouckz", handle: "@RealRouckz", subscribers: "343", platform: "YouTube", channelUrl: "https://www.youtube.com/@RealRouckz", channelId: "UCLr67LxrHYCjwZPB3IsZLSQ", avatarUrl: "assets/img/creators/RealRouckz.jpg", avatarSource: "YouTube", verifiedAt: "2026-09-16" },
    { rank: 4, name: "UMESH X", handle: "@UMESHX_GAMER", subscribers: "54.1K", platform: "YouTube", channelUrl: "https://www.youtube.com/@UMESHX_GAMER", channelId: "UCB_eN9_IzSfJcvoi1sUT74Q", avatarUrl: "assets/img/creators/UMESHX_GAMER.jpg", avatarSource: "YouTube", verifiedAt: "2026-09-16" },
    { rank: 5, name: "Mystic Priya", handle: "@mysticpriya", subscribers: "4.65K", platform: "YouTube", channelUrl: "https://www.youtube.com/@mysticpriya", channelId: "UCBaBy8eHr8EPfp74jX2mINQ", avatarUrl: "assets/img/creators/mysticpriya.jpg", avatarSource: "YouTube", verifiedAt: "2026-09-16" }
  ]
};

/* ---- Roadmap ---- */
ETC.roadmap = [
  { title: "Gen 1 — Website, backend & admin", status: "done", label: "Completed", major: true, progress: 100, what: "The public site, the submissions API, private resume storage and the admin dashboard — designed, built, tested and deployed.", why: "Gen 1 had to prove the whole stack end to end before anything else was worth building." },
  { title: "Creator Directory", status: "progress", label: "In progress", major: true, progress: 70, what: "Verified creator rows are live; adding creators, a contribution signal and a proper submission flow come next.", why: "The community starts with people who can be found and trusted." },
  { title: "Community spaces", status: "planned", label: "Planned", major: false, what: "Creator rooms, build circles and challenges — the collaboration layer around the directory.", why: "A directory is a list; a community is what people do with it." },
  { title: "Transfer", status: "planned", label: "Planned", major: false, what: "Temporary, private file sharing with no account.", why: "The first standalone ETC Labs product — small, useful, shippable." },
  { title: "Voice Rooms", status: "exploring", label: "Exploring", major: false, what: "A focused realtime voice room for small groups.", why: "Only worth building if it can be lighter than what exists." },
  { title: "AI Utilities & Creator Toolkit", status: "exploring", label: "Exploring", major: false, what: "Small tools for the repetitive parts of creator work.", why: "We're asking creators first instead of guessing." }
];
ETC.roadmapBadge = { done: "badge-done", progress: "badge-progress", planned: "badge-planned", exploring: "badge-exploring" };

/* ---- Who is behind it (no invented team) ---- */
ETC.team = [
  { name: "ETC", role: "Founder · Builder", text: "Designs, builds and ships everything in the lab — frontend, backend, admin, deployment. ETC Labs — Gen 1 is a one-person showcase for now.", quote: "Build it, test it, ship it, document it.", links: [{ label: "Instagram @etcofficials", href: "https://www.instagram.com/etcofficials/", external: true }, { label: "GitHub", href: "https://github.com/etcofficials", external: true }] }
];
ETC.principles = [
  { tag: "01 / Speed", title: "Move with intent", text: "Speed matters when it comes from clarity, not shortcuts." },
  { tag: "02 / Honesty", title: "Say what is real", text: "Live means live. Planned means planned. Demo data is labelled demo." },
  { tag: "03 / Quality", title: "Ship work that lasts", text: "Good foundations make every future change easier." }
];

/* ---- Careers: collaboration roles for an early-stage lab ---- */
ETC.roles = [
  { key: "video-editor", title: "Video Editor", team: "Media", type: "Collaboration", remote: true, summary: "Edit videos for ETC Labs and the creators around it — shorts, long-form and promo content.", doing: ["Edit short-form and long-form video for ETC Labs projects and creator collaborations", "Add motion, captions and pacing that keep people watching", "Work with creators and the lab on content direction"], looking: ["A portfolio of finished edits (any platform)", "Comfort with Premiere, DaVinci Resolve, CapCut or similar", "Reliable turnaround and clear communication"], nice: ["Motion graphics or thumbnail design", "Experience editing for creators or gaming channels"] },
  { key: "community-mod", title: "Community Moderator", team: "Community", type: "Collaboration", remote: true, summary: "Help shape and moderate the ETC Labs community as the creator directory grows into rooms and circles.", doing: ["Moderate community spaces with clear, fair guidelines", "Welcome new members and help them find their room or circle", "Run or support challenges, events and showcases"], looking: ["Experience moderating Discord or similar communities", "Calm judgement and consistency", "Genuine interest in creators and building things"], nice: ["Discord bot / automod configuration", "Experience running events or challenges"] },
  { key: "web-dev", title: "Web / Backend Developer", team: "Engineering", type: "Collaboration", remote: true, summary: "Build with us on the Gen 1 platform, the creator directory and the next tools.", doing: ["Ship features across the frontend and the FastAPI backend", "Improve deployments, integrations and the admin dashboard", "Turn ideas into working software and document them"], looking: ["Solid JavaScript and/or Python", "Comfort with databases, hosting and Git", "Links to things you've actually built"], nice: ["Discord bot development", "Experience with realtime (WebSocket / WebRTC) systems"] },
  { key: "ai-engineer", title: "AI / Automation Engineer", team: "AI", type: "Collaboration", remote: true, summary: "Design the logic behind the AI utilities and automations we are exploring.", doing: ["Prototype AI tools and automations", "Work with model integrations, data processing and evaluation", "Explain trade-offs clearly"], looking: ["Strong problem-solving background", "Experience with Python and LLM tooling", "Examples of algorithmic or research work"], nice: ["Open-source contributions", "Familiarity with evaluation and data pipelines"] },
  { key: "creator-research", title: "Creator Research", team: "Research", type: "Collaboration", remote: true, summary: "Find creators, trends and opportunities that fit the ETC Labs community.", doing: ["Research creators and communities that fit the directory", "Track trends and surface content ideas", "Help with outreach and first contact"], looking: ["Deep familiarity with YouTube, short-form and creator ecosystems", "Organized research habits", "Clear written communication"], nice: ["A network in creator communities", "Basic analytics or spreadsheet skills"] }
];
