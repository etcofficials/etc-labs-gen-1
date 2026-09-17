"""Generates the seven content pages (plus the /admin/ redirect page) from one shared shell.
Run: python build_pages.py   ·   index.html is hand-written and not touched."""
import pathlib
ROOT = pathlib.Path(__file__).parent
SITE = "https://etcofficials.github.io/etc-labs-gen-1/"
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#07070b">
  <link rel="canonical" href="{site}{page}.html">
  <meta property="og:site_name" content="ETC Labs — Gen 1">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site}{page}.html">
  <meta property="og:image" content="{site}assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/tokens.css">
  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/world.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="stylesheet" href="assets/css/mobile.css">
</head>
<body data-page="{page}" class="is-entering">
  <a class="skip-link" href="#main">Skip to content</a>
  <etc-nav></etc-nav>
  <main id="main">
'''
FOOT = '''  </main>
  <etc-footer></etc-footer>
  <script src="assets/js/config.js"></script>
  <script src="assets/js/data.js"></script>
  <script src="assets/js/world.js"></script>
  <script src="assets/js/ui.js"></script>
  <script src="assets/js/pages.js"></script>
  <script src="assets/js/touch.js"></script>
{extra}</body>
</html>
'''
UP = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M9 7h8v8"/></svg>'
RT = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
HP = '<input type="hidden" name="started_at" value=""><label class="hp" aria-hidden="true">Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label>'
TICK = '<div class="tick"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 7"/></svg></div>'
MAIL_ICO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
IG_ICO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
EMAIL = "etcofficials28@gmail.com"
IG_URL = "https://www.instagram.com/etcofficials/"

def cta(h2, lead, a, ah, b, bh, tone="violet"):
    return f'    <section class="section" data-tone="{tone}" aria-labelledby="cta-title"><div class="container"><div class="cta-band" data-reveal="scale"><div><h2 id="cta-title">{h2}</h2><p class="lead">{lead}</p></div><div class="actions"><a class="btn btn-primary solid lg" href="{ah}">{a} {UP}</a><a class="btn btn-secondary lg" href="{bh}">{b}</a></div></div></div></section>\n'

def head(kicker, h2, lead, hid):
    return f'<div class="head split-head"><div><span class="kicker" data-reveal>{kicker}</span><h2 id="{hid}" data-reveal style="--i:1">{h2}</h2></div><p class="lead" data-reveal style="--i:2">{lead}</p></div>'

pages = {}

pages["what-we-do"] = dict(title="What We Build — ETC Labs — Gen 1", desc="What ETC Labs builds: software engineering, AI & automation, product & UI design, infrastructure & deployment, security & reliability — in plain language, with what the result looks like.", body=f'''
    <section class="hero" data-tone="cyan" aria-labelledby="hero-title"><div class="container">
      <span class="kicker" data-reveal>What we build</span>
      <h1 id="hero-title" data-lines>What does ETC Labs<br>actually build?</h1>
      <p class="lead mt-3" data-reveal style="--i:2">Five areas. Pick one and we&rsquo;ll tell you what it is, what we build, who it helps and what the result looks like. No jargon &mdash; and the first worked example of every area is this site itself.</p>
      <div class="hero-actions" data-reveal style="--i:3"><a class="btn btn-primary" href="contact.html">Discuss a build {UP}</a><a class="link-arrow" href="#how-we-work">How a build runs {RT}</a></div>
    </div></section>
    <section class="section flush" data-tone="cyan" aria-label="Areas"><div class="container"><div class="ld"><div class="ld-list" id="svc-list" role="tablist" aria-label="Areas"></div><div class="ld-detail" id="svc-detail" aria-live="polite"></div></div></div></section>
    <section class="section" id="how-we-work" data-tone="blue" aria-labelledby="process-title"><div class="container">
      {head("How a build runs", "One builder. Direct communication. No hand-off maze.", "You talk to the person building the thing. Design, engineering and infrastructure sit together, which means fewer hand-offs and faster decisions.", "process-title")}
      <div class="how"><div data-reveal style="--i:0"><span class="n">01</span><h3>Talk</h3><p>You send a request. You get questions back and an honest take on fit, scope and rough scale.</p></div><div data-reveal style="--i:1"><span class="n">02</span><h3>Scope</h3><p>We agree what version one needs to do &mdash; and what it does not. Written down, so nobody is surprised later.</p></div><div data-reveal style="--i:2"><span class="n">03</span><h3>Build</h3><p>Design and engineering run together. You see working progress, not slide decks.</p></div><div data-reveal style="--i:3"><span class="n">04</span><h3>Ship &amp; document</h3><p>It gets deployed, documented and handed over cleanly &mdash; the way this site was.</p></div></div>
    </div></section>
{cta("Not sure which one you need?", "That is normal. Describe the problem, not the solution — you will get a straight answer on what it would take.", "Send a request", "contact.html", "See what has been built", "projects.html")}''')

pages["products"] = dict(title="Products — ETC Labs — Gen 1", desc="ETC Labs products you can use now: Transfer, Voice Rooms, AI Utilities, the Creator Toolkit, the Creator Directory and the Gen 1 platform — every one of them live.", body=f'''
    <section class="hero" data-tone="blue" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div><span class="kicker" data-reveal>Products</span><h1 id="hero-title" data-lines>Things we build<br>for people to use.</h1><p class="lead mt-3" data-reveal style="--i:2">Every product on this page is live: open it and use it. No waitlists, no concepts dressed up as products, and no invented usage numbers.</p><div class="cluster mt-4" data-reveal style="--i:3"><a class="btn btn-primary" href="tools.html">Open the tools {UP}</a><a class="link-arrow" href="#roadmap">What shipped {RT}</a></div></div>
      <div class="distinction" data-reveal="right" style="--i:2"><div><h3><span class="k"></span>Products</h3><p>Things ETC Labs builds for people to use &mdash; this page.</p></div><div><h3><span class="k alt"></span>Projects</h3><p>Builds, experiments and showcase pieces &mdash; the work itself. <a class="link" href="projects.html">See projects</a></p></div></div>
    </div></div></section>
    <section class="section flush" data-tone="blue" aria-label="Product list"><div class="container" id="products"></div></section>
    <section class="section" id="roadmap" data-tone="violet" aria-labelledby="roadmap-title"><div class="container">{head("What shipped", "Everything on the list is done — plus the limits we document instead of hiding.", "Gen 1 set out to prove the whole stack. Each line below is a completed build you can open; the last one lists the configurations a deployment can still be missing.", "roadmap-title")}<div style="max-width:820px" id="roadmap-list"></div></div></section>
{cta("Want to help build the next one?", "The tools are open to everyone; the roles are open too.", "See open roles", "careers.html", "Contact ETC Labs", "contact.html", "magenta")}''')

pages["projects"] = dict(title="Projects — ETC Labs — Gen 1", desc="ETC Labs projects — nine live builds across software, design, infrastructure, AI and creative work: the problem, what was built, how it works, the technology and where to open it.", body=f'''
    <section class="hero" data-tone="green" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div><span class="kicker" data-reveal>Projects</span><h1 id="hero-title" data-lines>Proof that<br>we build.</h1><p class="lead mt-3" data-reveal style="--i:2">Builds, experiments and showcase pieces. Each one says what the problem was, what was built, how, and with which technology &mdash; and every one of them is live. Several you are using right now; the rest open with one tap.</p></div>
      <div class="distinction" data-reveal="right" style="--i:2"><div><h3><span class="k"></span>Projects</h3><p>The work &mdash; builds, experiments and showcase pieces. This page.</p></div><div><h3><span class="k alt"></span>Products</h3><p>Finished or in-progress tools for people to use. <a class="link" href="products.html">See products</a></p></div></div>
    </div></div></section>
    <section class="section flush" data-tone="green" aria-label="Project list"><div class="container"><div class="filters" id="filters" role="group" aria-label="Filter projects by category" data-reveal></div><div class="grid project-grid filter-grid" id="projects" aria-live="polite"></div><div class="empty" id="projects-empty" hidden>No projects match this category yet.</div></div></section>
{cta("Want something like this built?", "Tell us what you are building. If it fits, we build it together.", "Contact ETC Labs", "contact.html", "What we build", "what-we-do.html", "cyan")}''')

pages["community"] = dict(title="Community — ETC Labs — Gen 1", desc="The ETC Labs community: a verified creator directory with admin-verified contributions, drop-in voice rooms, file transfer and open lab tools. Why it exists and how to get listed.", body=f'''
    <section class="hero league-hero" data-tone="magenta" aria-labelledby="hero-title"><div class="container"><div class="split">
      <div><span class="kicker" data-reveal>Community &middot; Creator directory live</span><h1 id="hero-title" class="display" data-lines>Build with<br>people who<br><span class="grad-magenta">build.</span></h1><p class="lead mt-3" data-reveal style="--i:3">The ETC Labs community is for creators, developers, designers, editors, artists, writers and builders. A verified creator directory with real contribution points, drop-in voice rooms and shared tools &mdash; built to find collaborators and build together, not to grow an audience alone.</p>
        <ul class="benefits" data-reveal style="--i:4"><li>Collaborate on real projects with people who have the skills you don&rsquo;t</li><li>Find creators through a directory that is actually verified</li><li>Share progress and finished work, get honest feedback</li><li>Learn from members who teach what they know</li><li>Drop into a voice room or send a file to a collaborator in one tap</li></ul>
        <div class="hero-actions" data-reveal style="--i:5"><a class="btn btn-primary solid lg" href="#creators">See the creators {UP}</a><a class="btn btn-secondary lg" href="#how">What you get</a></div>
        <div class="hero-meta" data-reveal style="--i:6"><span>Free to join</span><span>Creators verified by hand</span><span>Built by ETC Labs</span></div></div>
      <div data-reveal="scale" style="--i:2" id="graph"></div>
    </div></div></section>
    <section class="section flush" data-tone="magenta" aria-labelledby="why-title"><div class="container">{head("Why it exists", "More than an audience.", "The community is designed around collaboration instead of follower counts: a useful network, stronger opportunities and a place to build alongside people with different skills.", "why-title")}<div class="why-grid" id="why"></div></div></section>
    <section class="section" id="creators" data-tone="violet" aria-labelledby="board-title"><div class="container"><div class="head split-head"><div><span class="kicker" data-reveal>Creator directory</span><h2 id="board-title" data-reveal style="--i:1">Creators building alongside ETC Labs.</h2></div><div data-reveal style="--i:2"><p class="lead">Every row below was checked against the exact YouTube channel it links to &mdash; name, handle, profile image and the public subscriber count YouTube shows.</p><p class="small muted mt-2">Ordered by joined date, not by audience size. Counts are static snapshots with a verification date, not live numbers. Contribution points are recorded by ETC Labs for verified work and cannot be edited by creators &mdash; switch the ranking below to see them.</p></div></div><div id="board"></div></div></section>
    <section class="section" id="how" data-tone="violet" aria-labelledby="how-title"><div class="container">{head("What you get", "Six things the community is built around.", "All six are live. Tap any of them to open it.", "how-title")}<div id="features"></div></div></section>
    <section class="section" data-tone="magenta" aria-labelledby="community-title"><div class="container"><div class="head split-head"><div><span class="kicker" data-reveal>How it works</span><h2 id="community-title" data-reveal style="--i:1">People &rarr; skills &rarr; projects.</h2></div><div data-reveal style="--i:2"><p class="lead">A developer needs an editor for a launch video. An artist needs a writer. A builder needs everyone. The community exists so those people can find each other.</p><p class="small muted mt-2"><strong>Illustration:</strong> the roles below show how different skills connect on a project &mdash; they are not people, members or statistics. Real creators are in the directory above.</p></div></div><div id="members"></div><h3 class="mt-5" data-reveal>Who it is for</h3><p class="muted" data-reveal>Anyone who cares about making things &mdash; whether the output is a video, design, game, product, song, story, stream or tool.</p><div class="cluster mt-2" id="who" data-reveal></div></div></section>
    <section class="section flush" id="roadmap" data-tone="violet" aria-labelledby="roadmap-title"><div class="container">{head("What shipped", "Directory, contributions, rooms, transfer, tools.", "The community layer of Gen 1 is complete. The last line lists what a deployment can still be missing, documented instead of hidden.", "roadmap-title")}<div style="max-width:820px" id="roadmap-list"></div></div></section>
    <section class="section flush" id="join" data-tone="magenta" aria-labelledby="join-title"><div class="container"><div class="join-band" data-reveal="scale"><div><span class="kicker">Join</span><h2 id="join-title">Want to be listed, or build with us?</h2><p class="lead">There is no automated sign-up yet. Send a message with what you make and a link to your work &mdash; a person reads it.</p><div class="cluster mt-3"><a class="btn btn-primary solid lg" href="contact.html?need=creative">Get in touch {UP}</a><a class="link-arrow" href="https://www.instagram.com/etcofficials/" target="_blank" rel="noopener noreferrer">Follow @etcofficials {UP}</a></div></div><div class="steps"><div class="step"><div><h4>Say what you make</h4><p>Your discipline and a link to your channel, portfolio or repo.</p></div></div><div class="step"><div><h4>We verify it</h4><p>Directory rows are checked by hand against the real channel.</p></div></div><div class="step"><div><h4>Get listed, start collaborating</h4><p>Open a voice room, send files, earn verified contribution points.</p></div></div></div></div></div></section>
''')

pages["about"] = dict(title="About — ETC Labs — Gen 1", desc="What ETC Labs — Gen 1 is, why it exists, what it is experimenting with, how things are built, the design and technology philosophy, and where it is going. An independent showcase, not affiliated with MXT.", body=f'''
    <section class="hero" data-tone="violet" aria-labelledby="hero-title"><div class="container"><div class="split">
      <div><span class="kicker" data-reveal>About ETC Labs</span><h1 id="hero-title" class="display" data-lines>Make advanced<br>technology feel<br><span class="grad">effortless.</span></h1><p class="lead mt-3" data-reveal style="--i:3">ETC Labs &mdash; Gen 1 is an independent personal technology showcase. One builder, one lab: design, engineering, infrastructure and a creator community, built end to end and shown honestly.</p></div>
      <div class="abstract" data-reveal="scale" style="--i:2" role="img" aria-label="Abstract composition"><i class="a3"></i><i class="a2"></i><i class="a1"></i><i class="a4"></i><span class="cap">design &times; engineering &times; infrastructure</span></div>
    </div></div></section>
    <section class="section flush" data-tone="violet" aria-label="The ETC Labs story"><div class="container">
      <div class="stage-note" data-reveal style="max-width:820px;margin-bottom:clamp(40px,6vw,72px)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg><div><strong>Early stage, on purpose.</strong> ETC Labs is not a company with employees, customers or revenue. It is a lab: the work on this site is the claim, and we&rsquo;d rather grow into bigger claims than start with them. It is an independent project and is not affiliated with MXT.</div></div>
      <div class="story" data-reveal><div class="side"><span class="kicker">01</span><h2>What it is</h2></div><div class="body"><p>ETC Labs &mdash; Gen 1 is a technology showcase built by one person to demonstrate the whole stack: frontend development, UI/UX and product design, animation and interaction, responsive engineering, a real backend with a database, authentication and an admin system, and a clean Git-based deployment.</p><p>&ldquo;Gen 1&rdquo; is literal: this is the first generation. Everything here works today; the few things a deployment can still be missing are documented as configuration, not hidden behind a &ldquo;coming soon&rdquo;.</p></div></div>
      <div class="story" data-reveal><div class="side"><span class="kicker">02</span><h2>Why it exists</h2></div><div class="body"><p>Most portfolios show screenshots. This one runs. The forms store real submissions, the admin dashboard really authenticates and really reads the database, the creator directory was really verified, and the deployment is really split between a static host and a private backend. The point is to show serious engineering underneath a visual experience &mdash; and to be honest about what is and isn&rsquo;t built yet.</p></div></div>
      <div class="story" data-reveal><div class="side"><span class="kicker">03</span><h2>What it is experimenting with</h2></div><div class="body"><p>A single coherent animated &ldquo;world&rdquo; that stays at 60 fps on throttled CPUs; small tools that are genuinely usable &mdash; file transfer, peer-to-peer voice rooms, AI utilities, a local-first creator toolkit; and a community that starts from verified people and verified contributions rather than vanity metrics.</p></div></div>
      <div class="story" data-reveal><div class="side"><span class="kicker">04</span><h2>How things are built</h2></div><div class="body"><p><strong>Design philosophy:</strong> futuristic, not cluttered. Neon is an accent, not a background. Motion is connected to state and interaction, never decoration for its own sake, and it steps back on phones and under reduced-motion.</p><p><strong>Technology philosophy:</strong> the simplest thing that is genuinely robust. Vanilla HTML, CSS and JavaScript on the front; Python, FastAPI and SQLite on the back; secrets in environment variables; validation on the server; least privilege everywhere.</p><div class="principles" id="principles"></div></div></div>
      <div class="story" data-reveal><div class="side"><span class="kicker">05</span><h2>Where it&rsquo;s going</h2></div><div class="body"><div class="timeline"><div class="tl-item" data-status="done"><div class="panel" style="padding:16px 18px"><div class="tl-meta"><h3 style="font-size:1rem;margin:0">Gen 1 &mdash; website, backend, admin, deployment</h3><span class="badge badge-done">Completed</span></div><p class="small muted">The full stack, built and documented.</p></div></div><div class="tl-item" data-status="done"><div class="panel" style="padding:16px 18px"><div class="tl-meta"><h3 style="font-size:1rem;margin:0">Creator directory, contributions, voice rooms</h3><span class="badge badge-done">Completed</span></div><p class="small muted">Ten verified creators, admin-verified contribution points, peer-to-peer voice rooms.</p></div></div><div class="tl-item" data-status="done"><div class="panel" style="padding:16px 18px"><div class="tl-meta"><h3 style="font-size:1rem;margin:0">Transfer &middot; AI Utilities &middot; Creator Toolkit</h3><span class="badge badge-done">Completed</span></div><p class="small muted">All four tools are live on the <a class="link" href="tools.html">Tools</a> page.</p></div></div><div class="tl-item" data-status="limit"><div class="panel" style="padding:16px 18px"><div class="tl-meta"><h3 style="font-size:1rem;margin:0">Documented limitations</h3><span class="badge badge-limit">Configuration</span></div><p class="small muted">AI Utilities need a model key on the server; Voice Rooms need a TURN relay on the strictest networks; Render needs an attached disk for persistence. Each is a setting, not missing code &mdash; details in the README.</p></div></div></div></div></div>
    </div></section>
    <section class="section" id="who" data-tone="cyan" aria-labelledby="team-title"><div class="container">{head("Who is behind it", "Founded by ETC. One builder, for now.", "No invented team and no fictional names: ETC is the founder and builder behind the lab, and the ETC mark is its identity. Demo members shown on the Community page are labelled as demo data.", "team-title")}<div id="founder"></div></div></section>
{cta("Want to build with the lab — or have it build for you?", "Projects, collaborations and applications all start with one message.", "Contact ETC Labs", "contact.html", "Open roles", "careers.html")}''')

pages["careers"] = dict(title="Careers — ETC Labs — Gen 1", desc="Collaborate with ETC Labs. Open remote collaboration roles across media, community, engineering, AI and research — with one short application and a clear process.", extra='  <script src="assets/js/forms.js"></script>\n', body=f'''
    <section class="hero" data-tone="green" aria-labelledby="hero-title"><div class="container">
      <span class="kicker" data-reveal>Careers &middot; Applications open</span>
      <h1 id="hero-title" data-lines>Build with us.</h1>
      <p class="lead mt-3" data-reveal style="--i:2">ETC Labs is an early-stage, one-person lab looking for collaborators &mdash; not a company advertising salaried jobs. If you want to build real things in the open and see them ship, this is for you.</p>
      <div class="hero-actions" data-reveal style="--i:3"><a class="btn btn-primary" href="#roles">See open roles {RT}</a><a class="btn btn-secondary" href="#apply">Apply now</a></div>
      <div class="trio mt-5" data-reveal style="--i:4"><div><h3>Why join</h3><p>Real ownership of a product or the community, no layers, and work that goes live under your name.</p></div><div><h3>Who we&rsquo;re looking for</h3><p>People who finish things and can show it &mdash; a portfolio, a repo, a channel, a community you ran.</p></div><div><h3>Early stage, honestly</h3><p>Roles are remote collaborations. There is no payroll yet; compensation, if any, is agreed per project. That is the trade-off and the upside.</p></div></div>
    </div></section>
    <section class="section" id="roles" data-tone="green" aria-labelledby="roles-title"><div class="container">{head("Open roles", "Five collaboration roles are open.", "Pick a role to see what you would do, what we look for and what is nice to have — then apply from the same place.", "roles-title")}<div class="ld"><div class="ld-list" id="role-list" role="tablist" aria-label="Open roles"></div><div class="ld-detail" id="role-detail" aria-live="polite"></div></div></div></section>
    <section class="section flush" data-tone="cyan" aria-labelledby="after-title"><div class="container"><h2 id="after-title" class="sr-only">What happens after you apply</h2><div class="after"><div data-reveal style="--i:0"><span class="n">01</span><h3>You apply</h3><p>One form, about three minutes. Resume optional.</p></div><div data-reveal style="--i:1"><span class="n">02</span><h3>It gets read</h3><p>A person reads every application in the admin dashboard &mdash; the same one shown on this site.</p></div><div data-reveal style="--i:2"><span class="n">03</span><h3>You hear back if it fits</h3><p>On Discord or by email, with next steps &mdash; usually a short conversation first.</p></div></div></div></section>
    <section class="section" id="apply" data-tone="green" aria-labelledby="apply-title"><div class="container"><div class="panel apply-panel" data-reveal="scale">
      <div class="apply-head"><div><span class="kicker">Application</span><h2 id="apply-title">Send your application.</h2><p class="muted">Tell us who you are, what you want to work on, and where we can see your work.</p></div><span class="badge badge-live">Applications open</span></div>
      <form class="form" id="careers-form" novalidate enctype="multipart/form-data">
        {HP}
        <div class="form-row"><div class="field"><label for="firstName">First name <span class="req" aria-hidden="true">*</span></label><input class="input" id="firstName" name="firstName" autocomplete="given-name" required data-validate="required"><span class="field-error" role="alert"></span></div><div class="field"><label for="lastName">Last name <span class="req" aria-hidden="true">*</span></label><input class="input" id="lastName" name="lastName" autocomplete="family-name" required data-validate="required"><span class="field-error" role="alert"></span></div></div>
        <div class="form-row"><div class="field"><label for="email">Email <span class="req" aria-hidden="true">*</span></label><input class="input" id="email" name="email" type="email" autocomplete="email" required data-validate="required email"><span class="field-error" role="alert"></span></div><div class="field"><label for="discord">Discord username <span class="req" aria-hidden="true">*</span></label><input class="input" id="discord" name="discord" required data-validate="required"><span class="field-hint">We will reach you here first.</span><span class="field-error" role="alert"></span></div></div>
        <div class="form-row"><div class="field"><label for="position">Position <span class="req" aria-hidden="true">*</span></label><select class="select" id="position" name="position" required data-validate="required"></select><span class="field-error" role="alert"></span></div><div class="field"><label for="portfolio">Portfolio / LinkedIn <span class="opt">Optional</span></label><input class="input" id="portfolio" name="portfolio" type="url" inputmode="url" placeholder="https://" data-validate="url"><span class="field-error" role="alert"></span></div></div>
        <div class="field"><label for="cover">Cover letter <span class="opt">Optional</span> <span class="opt" style="margin-left:auto" data-count>0 / 1000</span></label><textarea class="textarea" id="cover" name="cover" maxlength="1000" placeholder="What you want to build, what you are great at, and why ETC Labs."></textarea></div>
        <div class="field"><label for="resume">Resume <span class="opt">Optional &middot; PDF, DOC or DOCX &middot; up to 5 MB</span></label><div class="file-drop"><input id="resume" name="resume" type="file" accept=".pdf,.doc,.docx"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M6 10l6-6 6 6M4 20h16"/></svg></span><div><b data-file-name>Choose your resume</b><span>Click to browse, or drop a file here</span></div><span class="btn btn-secondary sm" aria-hidden="true">Browse</span></div><div class="upload-bar" aria-hidden="true"><i></i></div></div>
        <div class="form-status" role="status" aria-live="polite"></div>
        <div class="form-foot"><p class="form-note">Your details are stored privately on the ETC Labs backend and used only for this application. Resumes are never public.</p><button class="btn btn-primary lg" type="submit">Submit application {UP}</button></div>
      </form>
      <div class="form-success" id="careers-success" aria-live="polite">{TICK}<h3>Application received.</h3><p class="muted">Thanks for applying. Every application is read, and you will hear back on Discord or by email if there is a fit.</p><p class="ref"></p><a class="btn btn-secondary mt-3" href="community.html">Meanwhile, explore the community</a></div>
    </div></div></section>
''')

pages["contact"] = dict(title="Contact — ETC Labs — Gen 1", desc="Contact ETC Labs: have something you want to build, ask, or discuss? Email etcofficials28@gmail.com, follow @etcofficials on Instagram, or send a project request.", extra='  <script src="assets/js/forms.js"></script>\n', body=f'''
    <section class="hero" data-tone="cyan" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div>
        <span class="kicker" data-reveal>Contact us</span>
        <h1 id="hero-title" class="display" data-lines>Have something<br>you want to build,<br><span class="grad-cyan">ask, or discuss?</span></h1>
        <p class="lead mt-3" data-reveal style="--i:3">Get in touch with ETC Labs. You don&rsquo;t need a spec, a budget or the right vocabulary &mdash; describe the thing and a person takes it from there.</p>
        <ul class="contact-for mt-3" data-reveal style="--i:4" aria-label="What to contact us about"><li>General questions</li><li>Project or build requests</li><li>Collaboration</li><li>Community and creator directory questions</li><li>Careers and application questions</li></ul>
      </div>
      <div class="channels" data-reveal="right" style="--i:2" aria-label="Contact channels">
        <div class="chan" id="email"><div class="top">{MAIL_ICO}<h3>Primary email</h3><span class="live" aria-label="Inbox is monitored"><i></i>monitored</span></div><a class="value" href="mailto:{EMAIL}" data-email>{EMAIL}</a><p>The fastest way to reach ETC Labs for anything on the list.</p><div class="row"><a class="btn btn-primary" href="mailto:{EMAIL}" data-email-btn data-cursor="Email">Email us {UP}</a><button class="btn btn-secondary sm copy" type="button" data-copy="{EMAIL}" data-copy-email>Copy address</button></div></div>
        <div class="chan ig" id="instagram"><div class="top">{IG_ICO}<h3>Instagram</h3></div><a class="value" href="{IG_URL}" target="_blank" rel="noopener noreferrer" data-instagram>@etcofficials</a><p>Follow the lab, or send a message there.</p><div class="row"><a class="btn btn-secondary sm" href="{IG_URL}" target="_blank" rel="noopener noreferrer" data-cursor="Open">Open Instagram {UP}</a></div></div>
      </div>
    </div></div></section>
    <section class="section flush" data-tone="violet" aria-labelledby="request-title"><div class="container">
      <div class="head split-head"><div><span class="kicker" data-reveal>Project request</span><h2 id="request-title" data-reveal style="--i:1">Or send the details as a request.</h2></div><div data-reveal style="--i:2"><p class="lead">The form stores your request on the ETC Labs backend, where it is read and tracked. About two minutes.</p><div class="steps mt-3" style="max-width:520px"><div class="step"><div><h4>You describe what you&rsquo;re building</h4><p>Problem first, solution optional.</p></div></div><div class="step"><div><h4>It gets reviewed</h4><p>A person reads it in the admin dashboard.</p></div></div><div class="step"><div><h4>You get next steps</h4><p>By email or Discord: questions, a rough scope, and an honest answer on fit.</p></div></div></div></div></div>
      <div class="contact-layout single">
      <div class="panel contact-panel" data-reveal>
        <form class="form" id="contact-form" novalidate>
          {HP}
          <div class="form-row"><div class="field"><label for="name">Name <span class="req" aria-hidden="true">*</span></label><input class="input" id="name" name="name" autocomplete="name" required data-validate="required"><span class="field-error" role="alert"></span></div><div class="field"><label for="email-field">Email <span class="req" aria-hidden="true">*</span></label><input class="input" id="email-field" name="email" type="email" autocomplete="email" required data-validate="required email"><span class="field-error" role="alert"></span></div></div>
          <div class="form-row"><div class="field"><label for="discord">Discord <span class="opt">Optional</span></label><input class="input" id="discord" name="discord"><span class="field-hint">If you prefer to talk there.</span></div><div class="field"><label for="building">What are you building? <span class="req" aria-hidden="true">*</span></label><input class="input" id="building" name="building" placeholder="e.g. a booking app for my studio" required data-validate="required"><span class="field-error" role="alert"></span></div></div>
          <div class="field"><label for="need">What do you need? <span class="req" aria-hidden="true">*</span></label><select class="select" id="need" name="need" required data-validate="required"><option value="">Choose the closest match</option><option value="software">Software &mdash; website, app, internal tool</option><option value="ai">AI &amp; automation &mdash; assistants, workflows, integrations</option><option value="design">Product &amp; UI design &mdash; interface, prototype, design system</option><option value="infrastructure">Infrastructure &amp; deployment &mdash; hosting, databases, integrations</option><option value="security">Security &amp; reliability &mdash; review, hardening, operations</option><option value="creative">Creative collaboration &mdash; media, content, community</option><option value="unsure">Not sure yet &mdash; help me figure it out</option></select><span class="field-error" role="alert"></span></div>
          <div class="form-row">
            <div class="field"><label id="scale-label">Budget / scale <span class="opt">Optional</span></label><div class="radio-group" role="radiogroup" aria-labelledby="scale-label"><label class="radio-chip"><input type="radio" name="scale" value="small"><span>Small</span></label><label class="radio-chip"><input type="radio" name="scale" value="medium"><span>Medium</span></label><label class="radio-chip"><input type="radio" name="scale" value="large"><span>Large</span></label><label class="radio-chip"><input type="radio" name="scale" value="unsure"><span>Not sure</span></label></div><span class="field-hint">Small: a prototype or focused fix &middot; Medium: a full product &middot; Large: a system with several parts</span></div>
            <div class="field"><label id="timeline-label">Timeline <span class="opt">Optional</span></label><div class="radio-group" role="radiogroup" aria-labelledby="timeline-label"><label class="radio-chip"><input type="radio" name="timeline" value="asap"><span>As soon as possible</span></label><label class="radio-chip"><input type="radio" name="timeline" value="1-3 months"><span>1&ndash;3 months</span></label><label class="radio-chip"><input type="radio" name="timeline" value="flexible"><span>Flexible</span></label></div></div>
          </div>
          <div class="field"><label for="message">Message <span class="req" aria-hidden="true">*</span></label><textarea class="textarea" id="message" name="message" placeholder="What does it need to do? Who is it for? Anything else we should know." required data-validate="required min:20"></textarea><span class="field-error" role="alert"></span></div>
          <div class="form-status" role="status" aria-live="polite"></div>
          <div class="form-foot"><p class="form-note">You get a reply by email, or Discord if you gave a username. No newsletter, no sales sequence.</p><button class="btn btn-primary lg" type="submit">Send project request {UP}</button></div>
        </form>
        <div class="form-success" id="contact-success" aria-live="polite">{TICK}<h3>Got it. Your request is in.</h3><p class="muted">It has been stored and will be read. You will get next steps by email or Discord.</p><p class="ref"></p><a class="btn btn-secondary mt-3" href="projects.html">See what has been built meanwhile</a></div>
      </div>
      </div>
    </div></section>
''')

UP_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M6 10l6-6 6 6M4 20h16"/></svg>'
ICONS = {'exchange': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13l-3-3M20 16H7l3 3"/></svg>', 'rooms': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H8l-4 4V5Z"/><path d="M8 9h8M8 12h5"/></svg>', 'ai': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="4"/></svg>', 'tools': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m14.5 6.5 3 3L9 18H6v-3l8.5-8.5Z"/><path d="M13 8l3 3M4 20h16"/></svg>'}
ETC_ICON = lambda k: ICONS[k]

TOOLS_JS = '  <script src="assets/js/tools.js"></script>\n'

pages["tools"] = dict(title="Tools — ETC Labs — Gen 1", desc="ETC Labs tools you can use right now: Transfer (send files with an expiring link), Voice Rooms (peer-to-peer voice for small groups), AI Utilities and the Creator Toolkit.", body=f"""
    <section class="hero" data-tone="magenta" aria-labelledby="hero-title"><div class="container">
      <span class="kicker" data-reveal>Tools · all live</span>
      <h1 id="hero-title" data-lines>Things you can<br>use right now.</h1>
      <p class="lead mt-3" data-reveal style="--i:2">Four small tools built on the Gen 1 backend. No accounts, no waitlists. Each one says exactly what it does and what it doesn&rsquo;t.</p>
    </div></section>
    <section class="section flush" data-tone="magenta" aria-label="Tool list"><div class="container"><div class="tool-grid">
      <a class="tool-card" href="transfer.html" data-reveal style="--i:0" data-cursor="Open"><span class="badge badge-live live-pulse">Live</span><span class="icon">{ETC_ICON("exchange")}</span><h2>Transfer</h2><p>Send a file with a link that expires. Up to 25 MB, no account.</p><span class="link-arrow">Open Transfer {RT}</span></a>
      <a class="tool-card" href="voice.html" data-reveal style="--i:1" data-cursor="Open"><span class="badge badge-live live-pulse">Live</span><span class="icon">{ETC_ICON("rooms")}</span><h2>Voice Rooms</h2><p>Peer-to-peer voice for up to six people. Share a room code and talk.</p><span class="link-arrow">Open Voice Rooms {RT}</span></a>
      <a class="tool-card" href="ai.html" data-reveal style="--i:2" data-cursor="Open"><span class="badge badge-live live-pulse">Live</span><span class="icon">{ETC_ICON("ai")}</span><h2>AI Utilities</h2><p>Summarize, rewrite, content ideas and titles &mdash; through the ETC Labs backend.</p><span class="link-arrow">Open AI Utilities {RT}</span></a>
      <a class="tool-card" href="toolkit.html" data-reveal style="--i:3" data-cursor="Open"><span class="badge badge-live live-pulse">Live</span><span class="icon">{ETC_ICON("tools")}</span><h2>Creator Toolkit</h2><p>Ideas board, publishing checklist and project tracking &mdash; private to your browser.</p><span class="link-arrow">Open Creator Toolkit {RT}</span></a>
    </div></div></section>
{cta("Want a tool that does not exist yet?", "Tell us what would save you time. If it fits the lab, it gets built and listed here — only once it works.", "Send a request", "contact.html?need=software", "See the products", "products.html", "violet")}""")

pages["transfer"] = dict(title="Transfer — ETC Labs — Gen 1", desc="ETC Labs Transfer: send a file with a link that expires. Drag and drop up to 25 MB, no account, delete it early with your owner link.", extra=TOOLS_JS, body=f"""
    <section class="hero" data-tone="cyan" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div><span class="kicker" data-reveal>Transfer · Live</span><h1 id="hero-title" data-lines>Send a file<br>with a link.</h1><p class="lead mt-3" data-reveal style="--i:2">Drop a file, get a link, share it. The link stops working after the time you choose or after 100 downloads &mdash; whichever comes first. No account, no app.</p>
        <ul class="contact-for mt-3" data-reveal style="--i:3" aria-label="How it works"><li>Files up to <b data-max-mb>25</b> MB</li><li>Expires after 24 hours, 3 days or 7 days</li><li>Downloads are served as attachments &mdash; never opened in the browser</li><li>You get a private owner link to delete it early</li></ul></div>
      <div class="panel tool-panel" data-reveal="right" style="--i:2" id="transfer-app" aria-live="polite">
        <div class="tool-state" data-state="upload">
          <label class="file-drop big" id="drop" for="tfile"><input id="tfile" name="file" type="file" aria-describedby="drop-hint"><span class="icon">{UP_ICON}</span><div><b data-file-name>Choose a file</b><span id="drop-hint">Tap to browse, or drop a file here</span></div></label>
          <div class="field mt-3"><label id="ttl-label">Link expires after</label><div class="radio-group" role="radiogroup" aria-labelledby="ttl-label"><label class="radio-chip"><input type="radio" name="ttl" value="24h" checked><span>24 hours</span></label><label class="radio-chip"><input type="radio" name="ttl" value="3d"><span>3 days</span></label><label class="radio-chip"><input type="radio" name="ttl" value="7d"><span>7 days</span></label></div></div>
          <div class="upload-bar mt-2" aria-hidden="true"><i></i></div>
          <div class="form-status" role="status" aria-live="polite"></div>
          <div class="form-foot"><p class="form-note">Stored privately on the ETC Labs backend until it expires, then deleted.</p><button class="btn btn-primary lg" type="button" id="tsend" disabled>Create link {UP}</button></div>
        </div>
        <div class="tool-state form-success" data-state="done">{TICK}<h3>Your link is ready.</h3><p class="muted" id="tsummary"></p>
          <div class="share-row"><input class="input mono" id="tlink" readonly aria-label="Share link"><button class="btn btn-primary" type="button" id="tcopy">Copy link</button></div>
          <p class="small muted mt-2">Owner link (keep this private &mdash; anyone with it can delete the file): <a class="link mono" id="towner" href="#">delete link</a></p>
          <div class="cluster mt-3"><a class="btn btn-secondary" href="transfer.html">Send another</a></div></div>
        <div class="tool-state" data-state="download"><span class="kicker">Someone sent you a file</span><h3 id="dname" class="mt-1"></h3><p class="muted" id="dmeta"></p><div class="cluster mt-3"><a class="btn btn-primary lg" id="ddownload" href="#" download>Download {UP}</a><a class="link-arrow" href="transfer.html">Send your own {RT}</a></div><p class="small muted mt-3">Downloads are served as attachments. Only open files from people you trust.</p></div>
        <div class="tool-state" data-state="owner"><span class="kicker">Owner controls</span><h3 class="mt-1" id="oname"></h3><p class="muted" id="ometa"></p><div class="form-status" role="status"></div><div class="cluster mt-3"><button class="btn btn-secondary danger" type="button" id="odelete">Delete this transfer</button><a class="link-arrow" href="transfer.html">Send another {RT}</a></div></div>
        <div class="tool-state" data-state="error"><span class="kicker">Transfer</span><h3 class="mt-1" id="ename">This link doesn&rsquo;t work</h3><p class="muted" id="emsg"></p><div class="cluster mt-3"><a class="btn btn-primary" href="transfer.html">Send a file {UP}</a></div></div>
        <div class="tool-state" data-state="offline"><span class="kicker">Transfer</span><h3 class="mt-1">Backend not connected</h3><p class="muted">This copy of the site has no backend configured, so files cannot be stored. Email <a class="link" href="mailto:{EMAIL}">{EMAIL}</a> instead.</p></div>
      </div>
    </div></div></section>
""")

pages["voice"] = dict(title="Voice Rooms — ETC Labs — Gen 1", desc="ETC Labs Voice Rooms: peer-to-peer voice for up to six people in the browser. Create a room, share the code, talk. Nothing is recorded or relayed.", extra=TOOLS_JS, body=f"""
    <section class="hero" data-tone="blue" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div><span class="kicker" data-reveal>Voice Rooms · Live</span><h1 id="hero-title" data-lines>A room code<br>and a microphone.</h1><p class="lead mt-3" data-reveal style="--i:2">Create a room, share the six-letter code, talk. Audio goes directly between browsers (WebRTC); the ETC Labs backend only introduces the peers. Up to six people per room, nothing recorded.</p>
        <ul class="contact-for mt-3" data-reveal style="--i:3" aria-label="How it works"><li>Works on desktop and phone browsers &mdash; Chrome, Edge, Safari, Firefox</li><li>Mute, participant list, live connection state</li><li>Rooms disappear when the last person leaves</li><li>Strict corporate networks may need a TURN relay &mdash; the room will tell you if it cannot connect</li></ul></div>
      <div class="panel tool-panel" data-reveal="right" style="--i:2" id="voice-app" aria-live="polite">
        <div class="tool-state" data-state="lobby">
          <div class="field"><label for="vname">Your name</label><input class="input" id="vname" maxlength="24" autocomplete="nickname" placeholder="How others will see you"></div>
          <div class="form-row mt-2"><div class="field"><label for="vcode">Room code</label><input class="input mono" id="vcode" maxlength="12" autocapitalize="none" autocorrect="off" spellcheck="false" inputmode="text" placeholder="e.g. k7m2xq"></div><div class="field" style="align-self:end"><button class="btn btn-secondary lg block" type="button" id="vjoin">Join room</button></div></div>
          <div class="or"><span>or</span></div>
          <div class="form-status" role="status" aria-live="polite"></div>
          <button class="btn btn-primary lg block" type="button" id="vcreate">Create a new room {UP}</button>
          <p class="form-note mt-2">Your browser will ask for microphone permission when you enter a room.</p>
        </div>
        <div class="tool-state" data-state="room">
          <div class="room-head"><div><span class="kicker">Room</span><h3 class="mono" id="rcode"></h3></div><span class="conn" id="rconn"><i></i><span>connecting</span></span></div>
          <div class="share-row mt-2"><input class="input mono" id="rlink" readonly aria-label="Room link"><button class="btn btn-secondary" type="button" id="rcopy">Copy link</button></div>
          <ul class="peers mt-3" id="rpeers" aria-label="People in this room"></ul>
          <div class="form-status" role="status" aria-live="polite"></div>
          <div class="room-controls mt-3"><button class="btn btn-primary" type="button" id="rmute" aria-pressed="false">Mute</button><button class="btn btn-secondary danger" type="button" id="rleave">Leave</button></div>
          <div id="raudio" hidden></div>
        </div>
        <div class="tool-state" data-state="offline"><span class="kicker">Voice Rooms</span><h3 class="mt-1">Backend not connected</h3><p class="muted">This copy of the site has no backend configured, so rooms cannot be created.</p></div>
      </div>
    </div></div></section>
""")

pages["ai"] = dict(title="AI Utilities — ETC Labs — Gen 1", desc="ETC Labs AI Utilities: summarize, rewrite, generate content ideas and titles. Runs through the ETC Labs backend — no keys in the browser, rate-limited per visitor.", extra=TOOLS_JS, body=f"""
    <section class="hero" data-tone="violet" aria-labelledby="hero-title"><div class="container"><div class="split top">
      <div><span class="kicker" data-reveal>AI Utilities · Live</span><h1 id="hero-title" data-lines>The repetitive<br>parts, handled.</h1><p class="lead mt-3" data-reveal style="--i:2">Four focused tools for creators and small teams. Paste text, pick a tool, get a clean result. Requests go through the ETC Labs backend; the model key never reaches your browser.</p>
        <ul class="contact-for mt-3" data-reveal style="--i:3" aria-label="Notes"><li>Up to 6,000 characters per request</li><li>Rate-limited per visitor to keep it free for everyone</li><li>Nothing you paste is stored &mdash; the text is sent to the model and forgotten</li><li id="ai-model-note">Model: <span data-ai-model>&hellip;</span></li></ul></div>
      <div class="panel tool-panel" data-reveal="right" style="--i:2" id="ai-app" aria-live="polite">
        <div class="tool-state" data-state="ready">
          <div class="filters" id="ai-tools" role="group" aria-label="Tool"></div>
          <div class="field mt-3" id="ai-tone-field" hidden><label for="ai-tone">Tone</label><select class="select" id="ai-tone"></select></div>
          <div class="field mt-3"><label for="ai-text">Your text <span class="opt" style="margin-left:auto" id="ai-count">0 / 6000</span></label><textarea class="textarea" id="ai-text" rows="7" maxlength="6000" placeholder="Paste a transcript, a draft, a topic, or a description of your channel&hellip;"></textarea></div>
          <div class="form-status" role="status" aria-live="polite"></div>
          <div class="form-foot"><p class="form-note" id="ai-hint">Pick a tool and paste some text.</p><button class="btn btn-primary lg" type="button" id="ai-run" disabled>Run {UP}</button></div>
          <div class="ai-output" id="ai-output" hidden><div class="ai-output-head"><span class="kicker" id="ai-output-label">Result</span><div class="cluster"><button class="btn btn-secondary sm" type="button" id="ai-copy">Copy</button><button class="btn btn-secondary sm" type="button" id="ai-again">Run again</button></div></div><pre id="ai-result"></pre></div>
        </div>
        <div class="tool-state" data-state="disabled"><span class="kicker">AI Utilities</span><h3 class="mt-1">Not enabled on this deployment yet</h3><p class="muted">The backend is running but has no model key configured, so the tools cannot answer. This is a server configuration (<code>ETC_ANTHROPIC_API_KEY</code>), not a missing feature &mdash; the code path is complete and tested.</p><div class="cluster mt-3"><a class="link-arrow" href="tools.html">Other tools {RT}</a></div></div>
        <div class="tool-state" data-state="offline"><span class="kicker">AI Utilities</span><h3 class="mt-1">Backend not connected</h3><p class="muted">This copy of the site has no backend configured.</p></div>
      </div>
    </div></div></section>
""")

pages["toolkit"] = dict(title="Creator Toolkit — ETC Labs — Gen 1", desc="ETC Labs Creator Toolkit: an ideas board, a publishing checklist and project tracking for creators — private, saved in your browser, export and import as JSON.", extra=TOOLS_JS, body=f"""
    <section class="hero" data-tone="magenta" aria-labelledby="hero-title"><div class="container">
      <div class="split top"><div><span class="kicker" data-reveal>Creator Toolkit · Live</span><h1 id="hero-title" data-lines>Your workspace,<br>your browser.</h1><p class="lead mt-3" data-reveal style="--i:2">Ideas, a publishing checklist and project tracking in one place. Everything is saved locally in this browser &mdash; nothing is uploaded, no account exists. Export a JSON backup any time.</p></div>
      <div class="toolkit-stats" data-reveal="right" style="--i:2"><div><b data-stat="ideas">0</b><span>ideas</span></div><div><b data-stat="checklist">0</b><span>checklist done</span></div><div><b data-stat="projects">0</b><span>projects</span></div></div></div>
    </div></section>
    <section class="section flush" data-tone="magenta" aria-label="Toolkit"><div class="container"><div class="panel tool-panel wide" id="toolkit-app">
      <div class="tabs" role="tablist" aria-label="Toolkit sections"><button class="tab" role="tab" aria-selected="true" data-tab="ideas" id="tab-ideas">Ideas</button><button class="tab" role="tab" aria-selected="false" data-tab="checklist" id="tab-checklist">Publishing checklist</button><button class="tab" role="tab" aria-selected="false" data-tab="projects" id="tab-projects">Projects</button><div class="tab-spacer"></div><button class="btn btn-secondary sm" type="button" id="tk-export">Export</button><label class="btn btn-secondary sm" for="tk-import-file">Import<input id="tk-import-file" type="file" accept="application/json" hidden></label></div>
      <div class="form-status" role="status" aria-live="polite" id="tk-status"></div>
      <section class="tab-panel" role="tabpanel" aria-labelledby="tab-ideas" data-panel="ideas">
        <form class="tk-add" id="idea-form"><input class="input" name="title" maxlength="120" placeholder="New idea &mdash; e.g. Behind the scenes of the studio move" required aria-label="Idea"><input class="input tags" name="tags" maxlength="60" placeholder="tags, comma separated" aria-label="Tags"><button class="btn btn-primary" type="submit">Add</button></form>
        <div class="filters mt-2" id="idea-filters" role="group" aria-label="Filter ideas"></div>
        <ul class="tk-list" id="idea-list" aria-live="polite"></ul>
      </section>
      <section class="tab-panel" role="tabpanel" aria-labelledby="tab-checklist" data-panel="checklist" hidden>
        <form class="tk-add" id="piece-form"><input class="input" name="title" maxlength="120" placeholder="Piece of content &mdash; e.g. Episode 12" required aria-label="Content piece"><button class="btn btn-primary" type="submit">Start checklist</button></form>
        <div id="piece-list" aria-live="polite"></div>
      </section>
      <section class="tab-panel" role="tabpanel" aria-labelledby="tab-projects" data-panel="projects" hidden>
        <form class="tk-add" id="project-form"><input class="input" name="title" maxlength="120" placeholder="Project &mdash; e.g. Channel rebrand" required aria-label="Project"><input class="input" name="due" type="date" aria-label="Due date"><button class="btn btn-primary" type="submit">Add</button></form>
        <ul class="tk-list" id="project-list" aria-live="polite"></ul>
      </section>
    </div></div></section>
""")

ADMIN_REDIRECT = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Admin — ETC Labs — Gen 1</title>
  <link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
  <style>
    body { margin: 0; min-height: 100vh; display: grid; place-items: center; background: #07070b; color: #e6e6f0; font: 15px/1.6 Inter, system-ui, sans-serif; padding: 24px; box-sizing: border-box; }
    .box { max-width: 520px; border: 1px solid rgba(255,255,255,.12); border-radius: 16px; padding: 28px; background: #101018; }
    h1 { font-size: 1.15rem; margin: 0 0 8px; } p { margin: 0 0 12px; color: #a9a6c4; } code { color: #22d3ee; } a { color: #22d3ee; }
  </style>
</head>
<body>
  <div class="box" id="box"><h1>ETC Labs admin</h1><p id="msg">Redirecting to the admin dashboard&hellip;</p></div>
  <script src="../assets/js/config.js"></script>
  <script>
    (function () {
      var base = (window.ETC_CONFIG && window.ETC_CONFIG.apiBase || "").replace(/\\/+$/, "");
      var local = /^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname);
      if (base) { location.replace(base + "/admin/"); return; }
      document.getElementById("msg").innerHTML = local
        ? "You are viewing the static copy of the site. Run the backend (<code>python -m uvicorn server.app:app --port 8790</code>) and open <a href=\\"http://localhost:8790/admin/\\">http://localhost:8790/admin/</a>."
        : "The admin dashboard runs on the backend, not on this static host. No backend URL is configured yet: deploy the backend, then set <code>apiBase</code> in <code>assets/js/config.js</code> and redeploy. The dashboard will then be at <code>&lt;backend-url&gt;/admin/</code>.";
    })();
  </script>
</body>
</html>
'''

for key, p in pages.items():
    html = HEAD.format(title=p["title"], desc=p["desc"], page=key, site=SITE) + p["body"] + FOOT.format(extra=p.get("extra", ""))
    (ROOT / "public" / f"{key}.html").write_text(html, encoding="utf-8")
    print(key, len(html))
(ROOT / "public" / "admin").mkdir(exist_ok=True)
(ROOT / "public" / "admin" / "index.html").write_text(ADMIN_REDIRECT, encoding="utf-8")
old = ROOT / "public" / "creation-league.html"
if old.exists():
    old.unlink(); print("removed creation-league.html")
