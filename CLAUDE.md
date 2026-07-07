# Super Smiles — project context (read first)

This file is the source of truth for working on the Super Smiles website. If you're picking this up fresh: read this top-to-bottom before editing.

## What this is
Super Smiles is an Australian **done-for-you service** that helps everyday Australians **prepare and organise** an application for early release of super on **compassionate grounds (the ATO's CRS program)** for **urgent dental treatment**. Domain: **supersmiles.au**. Tagline: *"Your super. Your smile. Our support."*
Audience: Australians ~35–55, often financially stressed, in dental pain, wary of scams. Voice: warm, plain-English, short sentences, no hype, no shame, no jargon.

## The ONE live site: `framer-version/`
- **`framer-version/` is the canonical, live build. Only edit this** unless explicitly told otherwise.
- The other folders — `claude-version/`, `eloquent-version/`, `vercel-version/` — are **old drafts, NOT deployed**, and still contain outdated / non-compliant copy (old fees, tax %, "super-approved", etc.). Don't edit or copy from them unless asked; they're reference only.
- `bestprinciples.md` (competitive research) and `supersmiles.md` (business + colours brief) are the source docs.

Pages (all in `framer-version/`): `index.html` (Home), `about-us.html`, `how-it-works.html`, `eligibility.html`, `find-a-dentist.html`, `faq.html`, `contact-us.html`.
**Legal pages** (white bg, black text, built from the Termly templates): `terms-and-conditions.html`, `privacy-policy.html`, `cookie-policy.html`, `disclaimer.html` — linked from a `.footer-legal` row below the footer line on every page. They're AI-drafted from Termly form-structures and tailored to Super Smiles; **must be lawyer-reviewed** and have their `[placeholders]` (entity, ABN, contact, effective date, state) filled before publishing.
Shared assets: `assets/styles.css` (all styling + design tokens), `assets/app.js` (all interactivity), `assets/sierra.png` (chatbot avatar). Nav + footer are duplicated in each HTML file (no shared include) — edit all pages when changing them (use a scripted find/replace).

## Hosting + deploy pipeline (auto-publish)
- **GitHub:** `JordanOscale/supersmiles` (private), branch `main`. Repo root = this folder.
- **Vercel:** project `jordan-os-projects/supersmiles`, **Root Directory = `framer-version`**, connected to the GitHub repo → **every push to `main` auto-builds & publishes**.
- **Live URL (our build — always review here):** https://supersmiles-jordan-os-projects.vercel.app  (also https://supersmiles.vercel.app; deployment protection OFF = public).
- **⚠️ `supersmiles.au` is NOT our build (as of 7 Jul 2026).** The public domain `supersmiles.au` serves a SEPARATE, older site (behind Cloudflare with a Google origin, page title "SuperSmile") — it does **not** point to this Vercel project, so our changes never appear there. Repointing (add the domain in Vercel + change Cloudflare DNS) is deferred pending the founder's go-ahead. **If the user ever says "the changes aren't showing," check which URL they're viewing first** — they're likely on `supersmiles.au` instead of the Vercel URL.
- **Standing preference: after ANY site change, automatically `git add` + `commit` + `push origin main`** — do not wait for the user to say "publish". Pushing = publishing (Vercel auto-deploys in ~30s). See memory `[[supersmiles-autodeploy]]`.
- Tooling already set up: `gh` CLI at `~/.local/bin/gh` (git creds via `gh auth setup-git`); Vercel CLI authed as `jordan-6644`. `.vercel/` is gitignored via `framer-version/.gitignore`.

## Design system (in `assets/styles.css` `:root`)
- **Fonts:** Plus Jakarta Sans = display/headings (`--font-display`); Outfit = body (`--font-body`); Space Mono = eyebrows/labels/nav badge (`--font-mono`); Barlow Condensed = big stat numbers (`--font-condensed`). Matches the DS at https://super-smile-ds.vercel.app.
- **Colours:** violet `#8C52FF` (`--violet`, primary), coral `#FB7777` (`--coral`, used only inside the brand gradient), cream `#FFF5E3` (`--cream`, page bg), white, near-black text `#161514`. **Brand gradient** `--gradient-brand` = `linear-gradient(135deg,#8C52FF,#FB7777)` — used on bottom CTAs, nav "Book" button, and as gradient text on the hero highlight word (`.grad-text`).
- **Dark sections:** background `--ink-section #121110` (true near-black, not chocolate); charcoal cards `--card-dark #1F1D1B`; footer uses `--ink-section`.
- Cards are black/white/violet (+ the apricot `--cream-deep` only on small "creamish" cards). Rounded **pill** buttons; **monoline SVG icons** (no emoji); `.reveal` = slide-up-on-scroll (heroes animate on load too); page-to-page transition fades **content only** (nav stays put).
- See memory `[[supersmiles-design-rules]]` for the cross-site design checklist (light→dark flow, no red on dark, number-or-icon-not-both, true-black, hover, etc.).

## Key interactive pieces
- **Eligibility self-check** (Home + Eligibility): logic in `app.js`. Options fill a small purple circle (radio-style, fades in), progress bar = brand gradient, then a soft result ("could be worth a free check — only the ATO decides"). Result "Book" button = gradient.
- **Before/after smile slider** (Home, section `#transform`): drag-to-compare; **replaced the old cost/tax estimator** (which was removed for compliance). Images are placeholders — swap for real client before/after photos.
- **Sierra live chat** (top of FAQ, section `#sierra`): a **self-contained front-end chat** (type/Send/Enter/quick-replies, typing dots, canned answers that route to eligibility/how-it-works/booking). The LeadConnector corner widget was **removed entirely** (their widget only renders as a corner bubble and can't be embedded inline). Avatar = `assets/sierra.png`. If the client wants the real LC bot inside the box, they must supply a GHL **inline embed** URL.
- **Nav "Chat" badge:** the FAQ nav link (desktop + mobile, every page) has a pulsing violet "Chat" badge signalling the chatbot.
- Booking CTA everywhere → `https://book.supersmiles.au/widget/booking/IcBxYi1F0l8vxlMzEX2c`.

## ⚠️ COMPLIANCE RULES — do not regress (from the 25 Jun 2026 handover)
- **NO fees/prices anywhere.** No "$600", "$500", "per $10,000", "our fee", "success-based", "no approval no fee". Route cost questions to: *"free eligibility check & consultation; we'll explain any costs in writing before you commit."* Never imply the whole service is free (the *check/consult* being free is fine to say).
- **NO tax numbers and NO tax advice.** No "22% / marginal rate / withheld". Keep only the statement that **we're not tax/financial advisers** and to see a **registered professional**.
- **Evidence = two medical reports** (a GP report **and** a dentist report) + an itemised quote + a complete application. Never say just "GP letter".
- **No "super-approved"/"accredited" dentists** — say "a dentist experienced with this process" (there's no ATO/fund accreditation).
- **No "compliant quote"/"worded to meet ATO"/"medical wording the ATO looks for".** Say "fully itemised" and always add **"we never change what your dentist recommends."**
- **Soften eligibility claims:** "you *may be able to* help / *may be* eligible", "only the ATO can decide". No "you may well be eligible", no "fast/easy/guaranteed approval".
- **myGov safeguard** ("we never ask for your login; you lodge from your own myGov") present on Home, How It Works, FAQ.
- **Cosmetic** work generally doesn't qualify and doesn't become eligible just because it's bundled with necessary treatment.
- **Footer disclaimer** (all pages): trading name + ABN, "not the ATO / not advisers / can't guarantee outcome / last resort".

## Outstanding — founder must supply (visible `[placeholders]` left in the code; DO NOT invent)
- `[Legal entity name]`, `[ABN]`, `[Business address]`, `[Phone]`, `[Email]` (footer + Contact), and a **Privacy Policy** page/link.
- **Affiliation with "Super Smiles Dental":** currently a neutral, always-true disclosure ("never required to use a dentist we suggest; we'll disclose any connection"). Swap to the exact wording once the relationship is confirmed.
- Non-copy actions still open (founder): fee-charging legality / tax-agent status, conflict-of-interest structure, whether any clinic requires upfront payment, internal "Our Services" SOP wording, confirming the myGov process never uses client credentials.
- **Sierra avatar** (`assets/sierra.png`) is a low-res Memoji screenshot — swap for a higher-res square PNG for crispness.

## Do-not-invent (leave labelled placeholders, flag them)
Phone, email, physical address, real testimonials/reviews, named dentists, ABN/legal registration, founder/team names.
