#!/usr/bin/env python3
"""
Build a GoHighLevel-importable export of the Super Smiles site.

GHL has no "import an .html file" feature. Each page is pasted into a
Custom Code / HTML element on a blank GHL page, so every exported page is
BODY MARKUP ONLY — no <!DOCTYPE>, <html>, <head> or <body> wrapper.

Two sets are produced from the same source:

  ghl-export/pages/            lean body markup; CSS + JS live once in the
                               site-wide setup files (recommended)
  ghl-export/pages-standalone/ same markup with styles.css + app.js +
                               gate-config inlined per page (fallback if
                               site-wide tracking code isn't available)

/book ships as TWO pages, because in GHL they're two separate blank pages.
GHL won't let two pages share a path, so they live at different slugs and
are swapped when the gate flips (see ghl-export/README.md):
  07  closed gate  -> waitlist state  (/book while closed)
  08  open  gate   -> booking widget  (/book-open, unpublished, until opened)

CTA labels are NOT rewritten per page: every /book button carries both
labels as data-when spans, and BOOKINGS_OPEN in the head code picks one.

Run:  python3 tools/build-ghl-export.py
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "super-smiles-website"
OUT = ROOT / "ghl-export"

# Where the images/fonts are served from. The pages reference assets
# relatively ("assets/hero.jpg"), which breaks the moment the markup lives
# on a GHL page, so every asset URL is rewritten to this absolute base.
# Swap this one string if the assets ever move into GHL's media library.
ASSET_BASE = "https://supersmiles-jordan-os-projects.vercel.app"

# (order, source file, GHL page name, GHL slug)
PAGES = [
    ("01", "index.html",                "Home",                          "/"),
    ("02", "about.html",                "About",                         "/about"),
    ("03", "how-it-works.html",         "How It Works",                  "/how-it-works"),
    ("04", "eligibility.html",          "Eligibility",                   "/eligibility"),
    ("05", "faq.html",                  "FAQ",                           "/faq"),
    ("06", "contact.html",              "Contact",                       "/contact"),
    ("07", "book.html",                 "Book — CLOSED gate (waitlist)", "/book"),
    ("08", "book.html",                 "Book — OPEN gate (booking)",    "/book-open"),
    ("09", "terms-and-conditions.html", "Terms & Conditions",            "/terms-and-conditions"),
    ("10", "privacy-policy.html",       "Privacy Policy",                "/privacy-policy"),
    ("11", "cookie-policy.html",        "Cookie Policy",                 "/cookie-policy"),
    ("12", "disclaimer.html",           "Disclaimer",                    "/disclaimer"),
]

SLUGS = {
    "01": "home", "02": "about", "03": "how-it-works", "04": "eligibility",
    "05": "faq", "06": "contact", "07": "book-closed-gate-waitlist",
    "08": "book-open-gate-booking", "09": "terms-and-conditions",
    "10": "privacy-policy", "11": "cookie-policy", "12": "disclaimer",
}

# ---------------------------------------------------------------- helpers


def read(p):
    return (SRC / p).read_text(encoding="utf-8")


def meta(doc, *, name=None, prop=None):
    """Pull one <meta> content value out of the source <head>."""
    attr, val = ("name", name) if name else ("property", prop)
    m = re.search(
        r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']\s*/?>' % (attr, re.escape(val)),
        doc, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def title_of(doc):
    m = re.search(r"<title>(.*?)</title>", doc, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def body_of(doc):
    m = re.search(r"<body[^>]*>(.*)</body>", doc, re.I | re.S)
    if not m:
        raise SystemExit("no <body> found")
    return m.group(1)


def absolutise(s):
    """Point every relative asset reference at ASSET_BASE."""
    s = re.sub(r'(src|href)="/?assets/', r'\1="%s/assets/' % ASSET_BASE, s)
    s = s.replace('href="/favicon.ico"', 'href="%s/favicon.ico"' % ASSET_BASE)
    # OG/Twitter images point at www.supersmiles.au, which currently serves a
    # different site — repoint so previews resolve today.
    s = s.replace("https://www.supersmiles.au/assets/", "%s/assets/" % ASSET_BASE)
    return s


def strip_shared_scripts(body):
    """Remove the <script src> tags that the setup files now provide.

    Must run BEFORE absolutise(), or the "assets/..." paths it matches are
    already rewritten and app.js ends up loaded twice — once from Vercel and
    once from the footer setup file, doubling every event listener.
    """
    body = re.sub(r'\s*<script src="assets/app\.js"></script>', "", body)
    body = re.sub(r'\s*<script src="assets/gate-config\.js"></script>', "", body)
    body = re.sub(r'\s*<script src="https://link\.msgsndr\.com/js/form_embed\.js"'
                  r'[^>]*></script>', "", body)
    return body


# The source comments point at file paths that don't exist in GHL.
COMMENT_FIXES = [
    ("State + dismiss come from assets/gate-config.js (loaded in <head>).\n"
     "     Flip BOOKINGS_OPEN in that one file to switch every page.",
     "State + dismiss come from the gate script in GHL's HEAD tracking code\n"
     "     (SETUP-1-head-code.html). Flip BOOKINGS_OPEN there to switch every page."),
]


def fix_comments(body):
    for old, new in COMMENT_FIXES:
        body = body.replace(old, new)
    return body


# ------------------------------------------------------- /book gate splitting

TEMPLATE_RE = re.compile(
    r'<template id="booking-flow">(.*?)</template>', re.S)
GATE_SWAP_RE = re.compile(
    r"<script>\s*/\* Swap in the real booking flow.*?</script>", re.S)
WAITLIST_RE = re.compile(
    r'<section class="section" id="waitlist-state".*?</section>\s*(?=<script>)', re.S)
GATE_COMMENT_RE = re.compile(
    r"<!-- =+\s*\n\s*BOOKING GATE.*?=+ -->", re.S)
WAITLIST_COMMENT_RE = re.compile(
    r"<!-- WAITLIST STATE \(rendered while the gate is closed\) -->\s*")

def stamp(state):
    """Force this page's own ticker to match the gate state it renders."""
    return (
        '<!-- This page IS the gate, so it stamps its own state before any\n'
        '     markup paints: the ticker and every CTA label read it. The other\n'
        '     pages read the site-wide switch in the head tracking code —\n'
        '     flip that to "%s" too. -->\n'
        '<script>document.documentElement.setAttribute("data-bookings","%s");</script>\n'
        % (state, state))


def book_closed(body):
    body = TEMPLATE_RE.sub("", body)
    body = GATE_SWAP_RE.sub("", body)
    body = GATE_COMMENT_RE.sub("", body)
    return stamp("closed") + body


def book_open(body):
    m = TEMPLATE_RE.search(body)
    if not m:
        raise SystemExit("booking-flow template not found in book.html")
    flow = m.group(1).strip()
    body = TEMPLATE_RE.sub("", body)
    body = WAITLIST_RE.sub(flow + "\n\n", body)
    body = GATE_SWAP_RE.sub("", body)
    body = GATE_COMMENT_RE.sub("", body)
    # the waitlist is gone from this page — its heading comment must go too
    body = WAITLIST_COMMENT_RE.sub("", body)
    return stamp("open") + body


# ------------------------------------------------------------------- output

GHL_COMPAT = """
/* ============================================================
   GHL COMPATIBILITY
   Our markup now sits inside GHL's own row/column wrappers, which
   add padding and a max-width. These sections are full-bleed by
   design (ticker, dark bands, footer), so the wrapper has to get
   out of the way. Set the GHL section to full-width with zero
   padding in the builder as well — this is the belt to that braces.
   ============================================================ */
.c-section > .inner, .c-row, .c-column, .c-wrapper,
[class*="hl_page-preview"] .c-column{
  max-width:none !important;
}
.ss-root .c-column, .ss-root .c-row{padding:0 !important;}
/* sticky nav needs no clipping ancestor */
.c-section, .c-row, .c-column, .c-wrapper{overflow:visible !important;}
"""


def head_block(order, name, slug, doc):
    """The per-page values that go in GHL's page settings, not the markup."""
    return f"""<!--
================================================================
  {order} · {name}
  GHL slug: {slug}
----------------------------------------------------------------
  Paste everything BELOW this comment into a single full-width
  Custom Code / HTML element on the blank "{name}" page.

  These go in GHL's page Settings, not in the markup:

  SEO title       {title_of(doc)}
  Meta description {meta(doc, name='description')}
  OG image        {absolutise(meta(doc, prop='og:image'))}
  Canonical       {"/book" if slug.startswith("/book") else slug}
================================================================
-->
"""


def build():
    # wipe generated output only — README.md is hand-written and stays
    for d in ("pages", "pages-standalone"):
        if (OUT / d).exists():
            shutil.rmtree(OUT / d)
        (OUT / d).mkdir(parents=True)

    css = read("assets/styles.css")
    js = read("assets/app.js")
    gate = read("assets/gate-config.js")
    fonts = ("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600"
             "&family=Outfit:wght@300;400;500;600;700"
             "&family=Plus+Jakarta+Sans:wght@400;500;600;700;800"
             "&family=Space+Mono:wght@400;700&display=swap")

    # ---- one-time setup files -------------------------------------------
    (OUT / "SETUP-1-head-code.html").write_text(
        "<!-- Site Settings > Tracking Code > HEAD. Paste once; every page reads it. -->\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="{fonts}" rel="stylesheet">\n\n'
        "<!-- THE ONE SWITCH: edit BOOKINGS_OPEN below to flip the ticker\n"
        "     sitewide, then publish the matching /book page (07 or 08). -->\n"
        f"<script>\n{gate}\n</script>\n", encoding="utf-8")

    (OUT / "SETUP-2-custom-css.css").write_text(
        "/* Site Settings > Custom CSS (or wrap in <style> in the head code).\n"
        "   Paste once; every page reads it. Source: assets/styles.css */\n\n"
        + absolutise(css) + GHL_COMPAT, encoding="utf-8")

    (OUT / "SETUP-3-footer-code.html").write_text(
        "<!-- Site Settings > Tracking Code > BODY / FOOTER. Paste once. -->\n"
        '<script src="https://link.msgsndr.com/js/form_embed.js"></script>\n'
        f"<script>\n{js}\n</script>\n", encoding="utf-8")

    # ---- pages -----------------------------------------------------------
    for order, srcfile, name, slug in PAGES:
        doc = read(srcfile)
        body = body_of(doc)

        if order == "07":
            body = book_closed(body)
        elif order == "08":
            body = book_open(body)

        # strip first (matches relative paths), fix comments, then absolutise
        body = absolutise(fix_comments(strip_shared_scripts(body)))
        body = re.sub(r"\n{3,}", "\n\n", body).strip()

        head = head_block(order, name, slug, doc)
        fname = f"{order}-{SLUGS[order]}.html"
        markup = '\n<div class="ss-root">\n' + body + "\n</div>\n"

        # lean: CSS + JS come from the three SETUP files
        (OUT / "pages" / fname).write_text(head + markup, encoding="utf-8")

        # standalone: everything this page needs, in this page
        (OUT / "pages-standalone" / fname).write_text(
            head
            + '\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            + f'<link href="{fonts}" rel="stylesheet">\n'
            + f"<script>\n{gate}\n</script>\n"
            + f"<style>\n{absolutise(css)}{GHL_COMPAT}</style>\n"
            + markup
            + '\n<script src="https://link.msgsndr.com/js/form_embed.js"></script>\n'
            + f"<script>\n{js}\n</script>\n", encoding="utf-8")

        print(f"{order}  {name:32s} {slug:24s} -> {fname}")

    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    build()
