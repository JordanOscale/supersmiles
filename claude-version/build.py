#!/usr/bin/env python3
"""Static builder for the Super Smiles site (claude-version).
Assembles shared chrome (head, SVG sprite, nav, footer, sticky CTA, scripts)
with per-page body content so every page stays consistent. No emoji — all
iconography is inline SVG line icons."""

import os

OUT = os.path.dirname(os.path.abspath(__file__))
BOOK = "https://book.supersmiles.au/widget/booking/IcBxYi1F0l8vxlMzEX2c"
LOGO = "https://assets.cdn.filesafe.space/p2dIZOM82vMDqT0ka5Tj/media/688c1a341fcebd6e78757872.png"

# ----------------------------------------------------------------------------
# SVG sprite — one hidden <svg> with all symbols. Inlined per page so it works
# over file:// (external <use> refs are blocked by browsers on file://).
# ----------------------------------------------------------------------------
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></symbol>
<symbol id="i-arrow-left" viewBox="0 0 24 24"><path d="M19 12H5"/><path d="m11 18-6-6 6-6"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
<symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></symbol>
<symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/></symbol>
<symbol id="i-tooth" viewBox="0 0 24 24"><path d="M12 5.5c-1.5-1-3-1.5-4.5-1C5 5.6 3 7.5 3 11c0 3.4 1 5 1.5 8 .3 1.7.7 3 2 3 1.4 0 1.3-3 2.5-3s1.1 3 2.5 3c1.3 0 1.7-1.3 2-3 .5-3 1.5-4.6 1.5-8 0-3.5-2-5.4-4.5-6.5-1.5-.5-3 0-4.5 1z"/></symbol>
<symbol id="i-clipboard" viewBox="0 0 24 24"><rect x="8" y="3" width="8" height="4" rx="1.2"/><path d="M16 5h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2"/><path d="M9 12h6M9 16h4"/></symbol>
<symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5l3.2 2"/></symbol>
<symbol id="i-lock" viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="11" rx="2.4"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></symbol>
<symbol id="i-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.4"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.2 5.2l2.1 2.1M16.7 16.7l2.1 2.1M18.8 5.2l-2.1 2.1M7.3 16.7l-2.1 2.1"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></symbol>
<symbol id="i-file" viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M9 13h6M9 17h4"/></symbol>
<symbol id="i-doc-check" viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="m9 15 2 2 4-4"/></symbol>
<symbol id="i-coin" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v10M14.6 9.3c0-1-1.2-1.8-2.6-1.8S9.4 8.3 9.4 9.3 10.6 11 12 11s2.6.8 2.6 1.8-1.2 1.8-2.6 1.8-2.6-.8-2.6-1.8"/></symbol>
<symbol id="i-chart" viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M8 17v-5M13 17V8M18 17v-8"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.6h.01"/></symbol>
<symbol id="i-warning" viewBox="0 0 24 24"><path d="M12 3 2.5 20.5h19L12 3z"/><path d="M12 10v4M12 17.5h.01"/></symbol>
<symbol id="i-stethoscope" viewBox="0 0 24 24"><path d="M5 3v6a5 5 0 0 0 10 0V3"/><path d="M5 3H3.5M15 3h1.5M10 14v1.5a5 5 0 0 0 10 0v-1"/><circle cx="20" cy="12.5" r="2"/></symbol>
<symbol id="i-sparkle" viewBox="0 0 24 24"><path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M6 3h3l2 5-2.4 1.6a11 11 0 0 0 5 5L17 13l5 2v3.5a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3z"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2.4"/><path d="m3.5 7 8.5 6 8.5-6"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 18.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9L12 2.5z"/></symbol>
<symbol id="i-users" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></symbol>
<symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 21s-7-4.4-9.4-8.6C1 9.5 2.6 5.5 6.2 5.5c2 0 3.3 1.2 4.1 2.4l1.7 2 1.7-2c.8-1.2 2.1-2.4 4.1-2.4 3.6 0 5.2 4 3.6 6.9C19 16.6 12 21 12 21z"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-bank" viewBox="0 0 24 24"><path d="M3 21h18M5 21V10M9.5 21V10M14.5 21V10M19 21V10M3.5 10 12 3.5 20.5 10z"/></symbol>
<symbol id="i-percent" viewBox="0 0 24 24"><path d="M19 5 5 19"/><circle cx="7.2" cy="7.2" r="2.2"/><circle cx="16.8" cy="16.8" r="2.2"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.7 3.8 9S14.5 18.5 12 21C9.5 18.5 8.2 15.3 8.2 12S9.5 5.5 12 3z"/></symbol>
<symbol id="i-printer" viewBox="0 0 24 24"><path d="M7 8V3h10v5"/><path d="M5 8h14a2 2 0 0 1 2 2v6h-4M5 16H3v-6a2 2 0 0 1 2-2"/><rect x="7" y="14" width="10" height="7" rx="1.2"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></symbol>
<symbol id="i-monitor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="12" rx="2.4"/><path d="M8 20h8M12 16v4"/></symbol>
<symbol id="i-award" viewBox="0 0 24 24"><circle cx="12" cy="9" r="6"/><path d="M9 14.3 7.5 22 12 19.2 16.5 22 15 14.3"/></symbol>
<symbol id="i-route" viewBox="0 0 24 24"><circle cx="6" cy="19" r="2.4"/><circle cx="18" cy="5" r="2.4"/><path d="M8.4 19H14a3.5 3.5 0 0 0 0-7h-4a3.5 3.5 0 0 1 0-7h5.6"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-scissors" viewBox="0 0 24 24"><circle cx="6" cy="6" r="2.4"/><circle cx="6" cy="18" r="2.4"/><path d="M8 7.5 20 16M8 16.5 20 8"/></symbol>
</defs>
</svg>"""

NAV_ITEMS = [
    ("about-us.html", "About", "about"),
    ("how-it-works.html", "How It Works", "how"),
    ("eligibility.html", "Eligibility", "elig"),
    ("find-a-dentist.html", "Find a Dentist", "dentist"),
    ("faq.html", "FAQ", "faq"),
    ("contact-us.html", "Contact", "contact"),
]


def nav(active):
    links = "".join(
        '<a href="%s" class="nav-link%s">%s</a>' % (href, " active" if key == active else "", label)
        for href, label, key in NAV_ITEMS
    )
    mlinks = "".join(
        '<a href="%s" class="m-link%s">%s</a>' % (href, " active" if key == active else "", label)
        for href, label, key in NAV_ITEMS
    )
    return """<header class="nav">
  <div class="wrap nav-inner">
    <a href="index.html" class="nav-logo" aria-label="Super Smiles home"><img src="%(logo)s" alt="Super Smiles"></a>
    <nav class="nav-links">%(links)s</nav>
    <div class="nav-cta">
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-sm btn-desktop">Book free consult<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      <button id="burger" class="nav-burger" aria-label="Menu" aria-expanded="false">
        <svg class="icon i-menu"><use href="#i-menu"/></svg>
        <svg class="icon i-close hidden"><use href="#i-close"/></svg>
      </button>
    </div>
  </div>
  <div id="mobileMenu" class="mobile-menu">%(mlinks)s
    <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-block" style="margin-top:10px;">Book free consult</a>
  </div>
</header>""" % {"logo": LOGO, "links": links, "mlinks": mlinks, "book": BOOK}


def footer():
    return """<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-logo"><img src="%(logo)s" alt="Super Smiles" style="filter:brightness(0) invert(1);opacity:.95;"></div>
        <p class="footer-desc">We help everyday Australians legally access their super early — through the ATO's Compassionate Release of Super program — to pay for urgent dental treatment. Done for you, end to end.</p>
      </div>
      <div>
        <h4>Service</h4>
        <a href="how-it-works.html" class="f-link">How it works</a>
        <a href="eligibility.html" class="f-link">Check eligibility</a>
        <a href="find-a-dentist.html" class="f-link">Find a dentist</a>
        <a href="how-it-works.html#pricing" class="f-link">Pricing</a>
      </div>
      <div>
        <h4>Company</h4>
        <a href="about-us.html" class="f-link">About us</a>
        <a href="faq.html" class="f-link">FAQ</a>
        <a href="contact-us.html" class="f-link">Contact</a>
      </div>
      <div>
        <h4>Get started</h4>
        <p class="footer-desc" style="margin-bottom:16px;">A free, no-obligation eligibility check takes about 60 seconds.</p>
        <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad">Book free consult<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="year">2026</span> Super Smiles · supersmiles.au · All rights reserved.</p>
      <p>Super Smiles is a Compassionate Release of Super facilitation service, not a financial adviser, tax agent or lawyer. Information here is general only. Australia only.</p>
    </div>
  </div>
</footer>"""  % {"logo": LOGO, "book": BOOK}


def sticky():
    return """<div class="sticky-cta">
  <a href="eligibility.html" class="btn btn-soft">60-sec check</a>
  <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad">Book free call</a>
</div>""" % {"book": BOOK}


def page(title, desc, active, body):
    return """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Outfit:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
%(sprite)s
%(nav)s
%(body)s
%(footer)s
%(sticky)s
<script src="assets/app.js"></script>
</body>
</html>""" % {
        "title": title, "desc": desc, "sprite": SPRITE,
        "nav": nav(active), "body": body, "footer": footer(), "sticky": sticky(),
    }


# ----------------------------------------------------------------------------
# Reusable body components
# ----------------------------------------------------------------------------

def cta_dark(eyebrow, heading, sub, primary_label="Book my free consult"):
    return """<section class="section hero bg-night">
  <div class="glow-blob" style="width:520px;height:520px;background:rgba(140,82,255,.28);top:50%%;left:50%%;transform:translate(-50%%,-50%%);"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">%(eyebrow)s</span>
    <h2 class="reveal" data-d="1" style="font-size:clamp(2rem,4.4vw,3.2rem);margin:18px 0 18px;">%(heading)s</h2>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:600px;margin:0 auto 34px;line-height:1.7;">%(sub)s</p>
    <div class="hero-cta-row reveal" data-d="3" style="justify-content:center;">
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-lg">%(primary)s<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      <a href="eligibility.html" class="btn btn-ghost-light btn-lg">Try the 60-sec check</a>
    </div>
    <p class="reveal" data-d="3" style="margin-top:22px;color:rgba(255,255,255,.4);font-size:.86rem;">Free check &middot; No obligation &middot; No approval, no fee</p>
  </div>
</section>""" % {"eyebrow": eyebrow, "heading": heading, "sub": sub, "primary": primary_label, "book": BOOK}


CHECKER_HTML = """<div class="checker" id="checker">
  <div class="checker-head">
    <span class="chip chip-grad"><svg class="icon"><use href="#i-sparkle"/></svg></span>
    <div>
      <div class="checker-kicker">60-second eligibility check</div>
      <h3>Could you qualify?</h3>
    </div>
  </div>
  <div class="checker-progress"><div class="checker-bar" id="checkerBar"></div></div>
  <div id="checkerStage"></div>
  <div class="checker-foot" id="checkerFoot">
    <button type="button" id="checkerBack" class="checker-back"><svg class="icon icon-sm"><use href="#i-arrow-left"/></svg>Back</button>
    <span class="checker-step" id="checkerStep">Question 1 of 4</span>
  </div>
</div>"""


SLIDER_HTML = """<div class="slider-card">
  <div class="slider-head">
    <div>
      <div class="slider-kicker">Super to release</div>
      <div class="slider-amount mono-num" id="sliderAmount">$30,000</div>
    </div>
    <span class="chip chip-grad"><svg class="icon"><use href="#i-coin"/></svg></span>
  </div>
  <input type="range" id="sliderRange" class="slider-range" min="10000" max="60000" step="1000" value="30000" aria-label="Amount of super to release">
  <div class="slider-scale"><span>$10k</span><span>$60k</span></div>
  <div class="slider-rows">
    <div class="slider-row"><span>Estimated tax withheld (~22%)</span><strong id="sliderTax">$6,600</strong></div>
    <div class="slider-row"><span>Our fee &mdash; $600 per $10k released</span><strong id="sliderFee">$1,800</strong></div>
    <div class="slider-row total"><span>Approx. left for your treatment</span><strong id="sliderNet">$21,600</strong></div>
  </div>
  <p class="slider-note">Estimates only. Actual tax depends on your age and the components of your super. This is not tax advice.</p>
</div>"""


# ----------------------------------------------------------------------------
# PAGE: index
# ----------------------------------------------------------------------------
def body_index():
    return """
<section class="section hero hero-dark">
  <div class="glow-blob" style="width:560px;height:560px;background:rgba(140,82,255,.30);top:-160px;left:-120px;"></div>
  <div class="glow-blob" style="width:430px;height:430px;background:rgba(107,63,212,.30);bottom:-150px;right:-90px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="pill pill-dark reveal" style="margin-bottom:22px;"><svg class="icon"><use href="#i-shield"/></svg>ATO Compassionate Release of Super</span>
    <h1 class="reveal" data-d="1">Use your super for the dental care you <span class="gradient-text">can't keep putting off.</span></h1>
    <p class="hero-sub reveal" data-d="2" style="margin:22px auto 0;">In pain, and the quote feels impossible? You may be able to legally access your superannuation early to pay for urgent dental treatment. We do the entire process for you — for free until it's approved.</p>
    <div class="hero-cta-row reveal" data-d="3" style="margin-top:32px;justify-content:center;">
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-lg">Book a free call<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      <a href="#check" class="btn btn-ghost-light btn-lg">Check if you qualify</a>
    </div>
    <div class="hero-trust reveal" data-d="4" style="margin-top:34px;justify-content:center;">
      <span><svg class="icon"><use href="#i-check"/></svg>No approval, no fee</span>
      <span><svg class="icon"><use href="#i-check"/></svg>No upfront treatment cost</span>
      <span><svg class="icon"><use href="#i-check"/></svg>Australia-wide</span>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">A real, legal program</span>
      <h2 style="font-size:clamp(1.8rem,3.6vw,2.7rem);margin:16px 0 20px;">A legitimate ATO program — not a loophole.</h2>
      <p class="lead" style="margin-bottom:18px;">You're right to be cautious about anything that touches your retirement savings, and the regulator has warned about dodgy operators. So here's exactly how Super Smiles keeps everything above board.</p>
      <a href="faq.html" class="btn btn-soft">Read the full safety FAQ<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
    </div>
    <div class="grid reveal" data-d="1" style="gap:16px;">
      <div class="card card-hover" style="padding:22px 24px;"><div class="flex" style="align-items:flex-start;gap:14px;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#i-bank"/></svg></span><div><h4 style="font-size:1rem;margin-bottom:4px;">Administered by the ATO</h4><p style="color:var(--fg-muted);font-size:.93rem;">Compassionate Release of Super is a genuine government program. We work strictly within its rules — nothing off-book.</p></div></div></div>
      <div class="card card-hover" style="padding:22px 24px;"><div class="flex" style="align-items:flex-start;gap:14px;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#i-lock"/></svg></span><div><h4 style="font-size:1rem;margin-bottom:4px;">We never touch your treatment money</h4><p style="color:var(--fg-muted);font-size:.93rem;">Funds are released to you, then you pay your dentist. We never ask you to pay for treatment upfront.</p></div></div></div>
      <div class="card card-hover" style="padding:22px 24px;"><div class="flex" style="align-items:flex-start;gap:14px;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#i-shield"/></svg></span><div><h4 style="font-size:1rem;margin-bottom:4px;">No approval, no fee</h4><p style="color:var(--fg-muted);font-size:.93rem;">If your application isn't approved, you don't pay our service fee. Our incentives are aligned with yours.</p></div></div></div>
    </div>
  </div>
</section>

<section class="section bg-cream" id="check">
  <div class="wrap wrap-md center">
    <span class="eyebrow center reveal">Free eligibility check</span>
    <h2 class="reveal" data-d="1">See if you're likely eligible — in 60 seconds</h2>
    <p class="reveal" data-d="2">Four plain-English questions. No obligation, no judgment — just an honest, instant read on whether the program could work for you.</p>
  </div>
  <div class="wrap wrap-sm reveal" data-d="2" style="margin-top:38px;">
    %(checker)s
  </div>
</section>

<section class="section bg-white" id="estimate">
  <div class="wrap wrap-md center">
    <span class="eyebrow center reveal">Cost estimator</span>
    <h2 class="reveal" data-d="1">See the tax and the fee before you commit</h2>
    <p class="reveal" data-d="2">Drag the slider to the amount of super you'd release. We'll show the estimated tax withheld and our fee — $600 per $10,000 — so there are no surprises.</p>
  </div>
  <div class="wrap wrap-sm reveal" data-d="2" style="margin-top:38px;">
    %(slider)s
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">What we do</span>
      <h2 style="font-size:clamp(1.8rem,3.6vw,2.7rem);margin:16px 0 20px;">Urgent dental work is expensive. Your savings are sitting in super.</h2>
      <p class="lead" style="margin-bottom:18px;">For thousands of Australians, the money to fix a painful, urgent dental problem is locked away in superannuation — out of reach exactly when it's needed most.</p>
      <p class="lead">The Compassionate Release of Super program exists for precisely this. The catch is the paperwork: a GP letter, an itemised dental quote, and an ATO application that has to be exactly right. That's the part we take off your hands.</p>
    </div>
    <div class="grid g-2 reveal" data-d="1" style="gap:18px;">
      <div class="card card-hover"><span class="chip chip-coral"><svg class="icon"><use href="#i-heart"/></svg></span><h3 style="font-size:1.05rem;margin:16px 0 7px;">You're in pain</h3><p style="color:var(--fg-muted);font-size:.92rem;">Toothache and infection don't wait for payday.</p></div>
      <div class="card card-hover" style="margin-top:24px;"><span class="chip chip-violet"><svg class="icon"><use href="#i-coin"/></svg></span><h3 style="font-size:1.05rem;margin:16px 0 7px;">The quote is huge</h3><p style="color:var(--fg-muted);font-size:.92rem;">Implants and major work run into the thousands.</p></div>
      <div class="card card-hover"><span class="chip chip-amber"><svg class="icon"><use href="#i-lock"/></svg></span><h3 style="font-size:1.05rem;margin:16px 0 7px;">Super feels locked</h3><p style="color:var(--fg-muted);font-size:.92rem;">Most people don't know early access is even possible.</p></div>
      <div class="card card-hover" style="margin-top:24px;"><span class="chip chip-violet"><svg class="icon"><use href="#i-route"/></svg></span><h3 style="font-size:1.05rem;margin:16px 0 7px;">The process is daunting</h3><p style="color:var(--fg-muted);font-size:.92rem;">GP letters, ATO forms, quotes — we do all of it.</p></div>
    </div>
  </div>
</section>

<section class="section bg-white" id="how">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">How it works</span>
      <h2 class="reveal" data-d="1">Four steps. We do the hard parts.</h2>
      <p class="reveal" data-d="2">From first call to funds released, here's the whole journey — and exactly where we take over.</p>
    </div>
    <div class="grid g-4">
      <div class="card card-hover reveal"><span class="step-num">1</span><h3 style="font-size:1.12rem;margin:18px 0 9px;">Free eligibility check</h3><p style="color:var(--fg-muted);font-size:.94rem;">A quick, judgment-free conversation to confirm the program fits your situation. Costs nothing.</p></div>
      <div class="card card-hover reveal" data-d="1"><span class="step-num">2</span><h3 style="font-size:1.12rem;margin:18px 0 9px;">GP letter, sorted</h3><p style="color:var(--fg-muted);font-size:.94rem;">We remove the biggest bottleneck — arranging the supporting medical letter the ATO requires.</p></div>
      <div class="card card-hover reveal" data-d="2"><span class="step-num">3</span><h3 style="font-size:1.12rem;margin:18px 0 9px;">Itemised dental quote</h3><p style="color:var(--fg-muted);font-size:.94rem;">We brief your dentist on exactly what the ATO needs and gather the quote on your behalf.</p></div>
      <div class="card card-glow card-hover reveal" data-d="3"><span class="step-num">4</span><h3 style="font-size:1.12rem;margin:18px 0 9px;">We lodge it for you</h3><p style="color:var(--fg-muted);font-size:.94rem;">We prepare and submit the full ATO application and stay with you until your super is released.</p></div>
    </div>
    <div class="center reveal" style="margin-top:40px;">
      <a href="how-it-works.html" class="btn btn-outline btn-lg">See the full process<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
    </div>
  </div>
</section>

<section class="section bg-night hero">
  <div class="glow-blob" style="width:480px;height:480px;background:rgba(140,82,255,.22);top:-120px;right:-80px;"></div>
  <div class="wrap" style="position:relative;z-index:2;">
    <div class="grid g-4" style="text-align:center;gap:30px;">
      <div class="stat reveal"><div class="stat-n gradient-text" data-count="14" data-suffix=" days">14 days</div><div class="stat-l">Typical ATO processing time</div></div>
      <div class="stat reveal" data-d="1"><div class="stat-n gradient-text" data-count="0" data-prefix="$">$0</div><div class="stat-l">Upfront — free until approval</div></div>
      <div class="stat reveal" data-d="2"><div class="stat-n gradient-text" data-count="3">3</div><div class="stat-l">Documents handled for you</div></div>
      <div class="stat reveal" data-d="3"><div class="stat-n gradient-text" data-count="1">1</div><div class="stat-l">Dedicated case manager</div></div>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Who it's for</span>
      <h2 class="reveal" data-d="1">Built for people who need their smile fixed now</h2>
      <p class="reveal" data-d="2">If urgent dental treatment is out of reach financially, this program may have been designed with you in mind.</p>
    </div>
    <div class="grid g-3">
      %(personas)s
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Why use us</span>
      <h2 class="reveal" data-d="1">Why not just do it yourself?</h2>
      <p class="reveal" data-d="2">You can — the program is open to everyone. But the paperwork is exactly where most people stall. Here's the honest difference.</p>
    </div>
    <div class="wrap-md grid g-2" style="margin:0 auto;">
      <div class="card card-hover reveal">
        <span class="pill" style="margin-bottom:18px;"><svg class="icon" style="color:var(--fg-subtle);"><use href="#i-user"/></svg>Going it alone</span>
        <ul class="checklist">
          <li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>Decode the ATO's rules and forms yourself</span></li>
          <li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>Chase a GP for a letter with the right wording</span></li>
          <li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>Hope your dentist's quote meets ATO standards</span></li>
          <li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>Risk rejection over one small paperwork error</span></li>
          <li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>Handle the ATO portal and follow-ups alone</span></li>
        </ul>
      </div>
      <div class="card card-glow card-hover reveal" data-d="1">
        <span class="pill pill-green" style="margin-bottom:18px;"><svg class="icon"><use href="#i-shield"/></svg>With Super Smiles</span>
        <ul class="checklist">
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>We confirm your eligibility in plain English, free</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>We arrange the GP letter with the correct wording</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>We brief your dentist for an ATO-ready quote</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>We quality-check everything before lodging</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>We lodge and manage ATO follow-ups for you</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Common questions</span>
      <h2 class="reveal" data-d="1">The things people ask first</h2>
    </div>
    <div class="wrap-md" style="margin:0 auto;">
      <div class="faq">
        %(faqs)s
      </div>
      <div class="center reveal" style="margin-top:32px;">
        <a href="faq.html" class="btn btn-outline">See all FAQs<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      </div>
    </div>
  </div>
</section>

%(cta)s
""" % {
        "book": BOOK,
        "checker": CHECKER_HTML,
        "slider": SLIDER_HTML,
        "personas": personas_grid(),
        "faqs": faq_block(HOME_FAQS),
        "cta": cta_dark("Your super, your smile",
                        "Find out where you stand — for free.",
                        "It takes about a minute to see if you're likely eligible, and a short call to get the whole thing moving. No pressure, no upfront cost, and a straight answer either way."),
    }


def personas_grid():
    data = [
        ("i-tooth", "Urgent & in pain", "Toothache, infection, an abscess or a broken tooth that simply can't wait."),
        ("i-doc-check", "Facing a big quote", "Implants, crowns, bridges, root canals or full-mouth rehabilitation."),
        ("i-coin", "Short on cash now", "The treatment is necessary, but paying for it out of pocket isn't realistic."),
        ("i-users", "Putting family first", "Looking to fund necessary dental care for yourself, a partner or a child."),
        ("i-clock", "Tired of waiting lists", "Public dental waitlists stretch for months while the problem gets worse."),
        ("i-shield", "Want it done right", "You'd rather have experts handle the ATO paperwork than risk getting it wrong."),
    ]
    out = []
    for i, (ic, t, d) in enumerate(data):
        out.append('<div class="card card-hover reveal" data-d="%d"><span class="chip chip-violet"><svg class="icon"><use href="#%s"/></svg></span><h3 style="font-size:1.1rem;margin:18px 0 8px;">%s</h3><p style="color:var(--fg-muted);font-size:.94rem;">%s</p></div>' % (i % 4, ic, t, d))
    return "\n      ".join(out)


def faq_block(items):
    out = []
    for q, a in items:
        out.append("""<div class="faq-item">
          <button class="faq-q">%s<span class="faq-ico"><svg class="icon"><use href="#i-plus"/></svg></span></button>
          <div class="faq-a"><div class="faq-a-inner">%s</div></div>
        </div>""" % (q, a))
    return "\n        ".join(out)


HOME_FAQS = [
    ("Is accessing my super for dental actually legal?",
     "Yes. The Compassionate Release of Super (CRS) program is administered by the ATO and specifically allows early access to super for necessary medical and dental treatment when you can't cover the cost another way. We only ever work within those rules."),
    ("What does it cost to use Super Smiles?",
     "The eligibility check is free. Our service fee is $600 for every $10,000 of super successfully released, and it's only charged after your funds come through. If your application isn't approved, you don't pay our fee."),
    ("How long does it take?",
     "It varies by case, but the ATO aims to process most complete applications within around 14 business days. Gathering your documents — the GP letter and dental quote — is usually the longest part, and that's exactly what we speed up for you."),
    ("Will this affect my retirement or my tax?",
     "Money you release now is money that won't be in your super at retirement, and compassionate release is taxed — the rate depends on your age and super components. We're upfront about this and recommend speaking with a tax adviser. We are not financial advisers."),
]


# ----------------------------------------------------------------------------
# PAGE: how-it-works
# ----------------------------------------------------------------------------
def body_how():
    steps = [
        ("01", "i-sparkle", "Free eligibility check",
         "We start with a free, no-obligation conversation. We listen to your situation, explain the program in plain English, and give you an honest read on whether you're likely to qualify — before you invest any time or money.",
         ["Takes about 15 minutes", "Plain-English, judgment-free", "Costs you nothing"]),
        ("02", "i-stethoscope", "We arrange your GP letter",
         "The ATO requires a supporting letter from a registered medical practitioner. This is where most people get stuck — so we remove the friction entirely, coordinating the right letter with the correct wording.",
         ["We brief the GP on ATO requirements", "Correct clinical wording", "No chasing paperwork yourself"]),
        ("03", "i-tooth", "We gather your dental quote",
         "Your treatment needs an itemised quote on the practice's letterhead, with the right item numbers. We brief your dentist — your own, or one near you — so the quote meets the ATO's standard first time.",
         ["Use your own dentist", "We send them a clear guide", "Itemised, ATO-ready quote"]),
        ("04", "i-doc-check", "We prepare & lodge the application",
         "We assemble everything, quality-check it, and lodge the full application with the ATO on your behalf. Then we track it and stay with you right through until your super fund releases the money.",
         ["Full application prepared for you", "Internal quality check", "We track it to release"]),
    ]
    step_html = []
    for i, (n, ic, t, d, points) in enumerate(steps):
        pts = "".join('<li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>%s</span></li>' % p for p in points)
        media = """<div class="card card-glow reveal step-media" data-d="1" style="display:flex;align-items:center;justify-content:center;min-height:230px;background:%s;">
          <span class="chip chip-grad" style="width:96px;height:96px;border-radius:28px;"><svg class="icon" style="width:46px;height:46px;"><use href="#%s"/></svg></span>
        </div>""" % ("var(--violet-mist)" if i % 2 == 0 else "var(--cream)", ic)
        text = """<div class="reveal">
          <span class="eyebrow">Step %s</span>
          <h2 style="font-size:clamp(1.6rem,3.2vw,2.3rem);margin:14px 0 16px;">%s</h2>
          <p class="lead" style="margin-bottom:22px;">%s</p>
          <ul class="checklist">%s</ul>
        </div>""" % (n, t, d, pts)
        cols = (text, media) if i % 2 == 0 else (media, text)
        step_html.append("""<div class="wrap split" style="margin-bottom:%spx;">%s%s</div>"""
                         % (0 if i == len(steps) - 1 else 72, cols[0], cols[1]))

    included = [
        ("i-chat", "Dedicated case manager", "One person owns your case end to end — no being passed around a call centre."),
        ("i-stethoscope", "GP letter coordination", "We arrange the supporting medical letter with the correct ATO wording."),
        ("i-tooth", "Dentist liaison", "We brief your dentist and collect a compliant, itemised quote."),
        ("i-doc-check", "Application preparation", "Every form completed correctly and quality-checked before lodging."),
        ("i-monitor", "Lodged on your behalf", "We submit directly to the ATO so you never wrestle with the portal."),
        ("i-coin", "Release support", "We stay with you after approval until funds land in your account."),
    ]
    inc_html = "".join(
        '<div class="card card-hover reveal" data-d="%d"><span class="chip chip-violet"><svg class="icon"><use href="#%s"/></svg></span><h3 style="font-size:1.08rem;margin:16px 0 8px;">%s</h3><p style="color:var(--fg-muted);font-size:.93rem;">%s</p></div>' % (i % 3, ic, t, d)
        for i, (ic, t, d) in enumerate(included)
    )

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(56px,8vw,90px);">
  <div class="glow-blob" style="width:500px;height:500px;background:rgba(140,82,255,.28);top:-140px;right:-80px;"></div>
  <div class="glow-blob" style="width:360px;height:360px;background:rgba(107,63,212,.26);bottom:-120px;left:-80px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">How it works</span>
    <h1 class="reveal" data-d="1" style="margin:18px 0 18px;">A done-for-you process, <span class="gradient-text">start to finish.</span></h1>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:620px;margin:0 auto 32px;line-height:1.7;">You focus on getting better. We handle the GP letter, the dental quote, and the entire ATO application — and we don't charge our fee unless it's approved.</p>
    <div class="hero-cta-row reveal" data-d="3" style="justify-content:center;">
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-lg">Book a free call<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      <a href="eligibility.html" class="btn btn-ghost-light btn-lg">Check eligibility</a>
    </div>
  </div>
</section>

<section class="section bg-white">
  %(steps)s
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">What's included</span>
      <h2 class="reveal" data-d="1">Everything's handled — for one simple fee</h2>
      <p class="reveal" data-d="2">No hidden extras. When you work with us, all of this is part of the service.</p>
    </div>
    <div class="grid g-3">%(included)s</div>
  </div>
</section>

<section class="section bg-white" id="pricing">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Pricing</span>
      <h2 class="reveal" data-d="1">Honest, success-based pricing</h2>
      <p class="reveal" data-d="2">You only pay our fee once your super is actually released. Nothing upfront.</p>
    </div>
    <div class="wrap-md grid g-2" style="margin:0 auto;">
      <div class="card card-hover reveal">
        <span class="eyebrow">Step one</span>
        <div class="mono-num gradient-text" style="font-size:3.4rem;margin:14px 0 6px;">Free</div>
        <p style="color:var(--fg-muted);margin-bottom:20px;">The eligibility check costs you nothing — no obligation to continue.</p>
        <ul class="checklist">
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Honest assessment of your situation</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Plain-English explanation of the program</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Zero pressure to proceed</span></li>
        </ul>
      </div>
      <div class="card card-glow card-hover reveal" data-d="1" style="background:var(--g-violet);color:#fff;">
        <span class="eyebrow" style="color:rgba(255,255,255,.9);">Service fee</span>
        <div class="mono-num" style="font-size:3.4rem;margin:14px 0 6px;color:#fff;">$600<span style="font-size:1.1rem;font-family:'Outfit';font-weight:500;color:rgba(255,255,255,.72);"> / $10k released</span></div>
        <p style="color:rgba(255,255,255,.78);margin-bottom:20px;">Charged only after your super is successfully released — not before.</p>
        <ul class="checklist">
          <li><span class="check-dot" style="background:#fff;"><svg class="icon" style="color:var(--violet);"><use href="#i-check"/></svg></span><span style="color:rgba(255,255,255,.92);">No approval, no fee</span></li>
          <li><span class="check-dot" style="background:#fff;"><svg class="icon" style="color:var(--violet);"><use href="#i-check"/></svg></span><span style="color:rgba(255,255,255,.92);">Fee scales proportionally to the amount released</span></li>
          <li><span class="check-dot" style="background:#fff;"><svg class="icon" style="color:var(--violet);"><use href="#i-check"/></svg></span><span style="color:rgba(255,255,255,.92);">Deducted from released funds — nothing out of pocket</span></li>
        </ul>
        <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-light btn-block" style="margin-top:24px;">Get started free<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      </div>
    </div>
    <div class="wrap-sm reveal" style="margin:36px auto 0;">
      %(slider)s
    </div>
    <div class="wrap-md" style="margin:24px auto 0;">
      <div class="note note-amber reveal"><svg class="icon"><use href="#i-warning"/></svg><div><h4>A word on tax</h4><p>Compassionate release is taxed — typically around 22%%, withheld by your fund before the money reaches you, with the exact rate depending on your age and the components of your super. We always explain this clearly upfront so there are no surprises. We're not tax advisers, and we'll suggest you confirm your position with one.</p></div></div>
    </div>
  </div>
</section>

%(cta)s
""" % {
        "book": BOOK,
        "steps": "\n  ".join(step_html),
        "included": inc_html,
        "slider": SLIDER_HTML,
        "cta": cta_dark("Ready when you are", "Let's get your application moving.",
                        "Book a free call and we'll start the done-for-you process — GP letter, dental quote, and ATO lodgement, all handled."),
    }


# ----------------------------------------------------------------------------
# PAGE: eligibility
# ----------------------------------------------------------------------------
def body_elig():
    req = [
        ("i-stethoscope", "It's medically necessary", "A registered practitioner supports that the treatment is needed to relieve pain, treat infection or prevent your health deteriorating."),
        ("i-coin", "You can't readily pay", "The scheme is specifically for people who can't reasonably cover the cost of the treatment another way."),
        ("i-bank", "You have super to release", "You hold an active Australian super balance large enough to cover the treatment and your fund's release minimum."),
    ]
    req_html = "".join(
        '<div class="card %s card-hover reveal" data-d="%d"><span class="chip chip-violet"><svg class="icon"><use href="#%s"/></svg></span><h3 style="font-size:1.1rem;margin:16px 0 8px;">%s</h3><p style="color:var(--fg-muted);font-size:.94rem;">%s</p></div>'
        % ("card-glow" if i == 1 else "", i, ic, t, d)
        for i, (ic, t, d) in enumerate(req)
    )

    qualify = [
        "Dental implants to replace missing teeth",
        "Root canal treatment for infection or pain",
        "Crowns, bridges and major restorations",
        "Treatment for moderate to severe gum disease",
        "Complex extractions and oral surgery",
        "Full-mouth rehabilitation where clinically needed",
    ]
    notq = [
        "Teeth whitening and bleaching",
        "Veneers for purely aesthetic reasons",
        "Cosmetic contouring or reshaping",
        "Elective work with no health basis",
    ]
    q_html = "".join('<li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>%s</span></li>' % q for q in qualify)
    n_html = "".join('<li><span class="cross-dot"><svg class="icon"><use href="#i-x"/></svg></span><span>%s</span></li>' % q for q in notq)

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(48px,6vw,70px);">
  <div class="glow-blob" style="width:480px;height:480px;background:rgba(140,82,255,.28);top:-130px;left:-70px;"></div>
  <div class="glow-blob" style="width:360px;height:360px;background:rgba(107,63,212,.26);bottom:-110px;right:-70px;"></div>
  <div class="wrap hero-grid" style="align-items:center;">
    <div>
      <span class="pill pill-dark reveal" style="margin-bottom:20px;"><svg class="icon"><use href="#i-sparkle"/></svg>60-second self-check</span>
      <h1 class="reveal" data-d="1">See if you're likely <span class="gradient-text">eligible — in under a minute.</span></h1>
      <p class="hero-sub reveal" data-d="2" style="margin-top:20px;">No forms, no judgment, no obligation. Answer four plain-English questions and get an honest, instant read on whether the program could work for you.</p>
      <div class="hero-trust reveal" data-d="3" style="margin-top:28px;">
        <span><svg class="icon"><use href="#i-check"/></svg>Anonymous</span>
        <span><svg class="icon"><use href="#i-check"/></svg>Takes ~60 seconds</span>
        <span><svg class="icon"><use href="#i-check"/></svg>No obligation</span>
      </div>
    </div>
    <div class="reveal" data-d="2">%(checker)s</div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">What the ATO looks for</span>
      <h2 class="reveal" data-d="1">Three things generally need to be true</h2>
      <p class="reveal" data-d="2">Every application is assessed individually, but eligibility usually comes down to these three pillars.</p>
    </div>
    <div class="grid g-3">%(req)s</div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Treatment</span>
      <h2 class="reveal" data-d="1">What kind of dental work qualifies?</h2>
      <p class="reveal" data-d="2">The deciding factor is health necessity. If treatment relieves pain or protects your health, it's far more likely to qualify than purely cosmetic work.</p>
    </div>
    <div class="wrap-md grid g-2" style="margin:0 auto;">
      <div class="card reveal">
        <span class="pill pill-green" style="margin-bottom:18px;"><svg class="icon"><use href="#i-check"/></svg>Typically qualifies</span>
        <ul class="checklist">%(qualify)s</ul>
      </div>
      <div class="card reveal" data-d="1">
        <span class="pill" style="margin-bottom:18px;color:var(--fg-subtle);"><svg class="icon" style="color:var(--fg-subtle);"><use href="#i-x"/></svg>Usually won't qualify</span>
        <ul class="checklist">%(notq)s</ul>
      </div>
    </div>
    <div class="wrap-md" style="margin:26px auto 0;display:flex;flex-direction:column;gap:16px;">
      <div class="note note-violet reveal"><svg class="icon"><use href="#i-info"/></svg><div><h4>"Means test" — reframed</h4><p>Being asked whether you can afford the treatment isn't a judgment. This program was created specifically for people who can't readily cover necessary care — that's the whole point of it.</p></div></div>
      <div class="note note-amber reveal"><svg class="icon"><use href="#i-warning"/></svg><div><h4>Remember the tax</h4><p>Released super is taxed — typically around 22%%, withheld before funds reach you, depending on your age and super components. Factor this in when estimating how much to release. We'll walk you through it.</p></div></div>
    </div>
  </div>
</section>

%(cta)s
""" % {
        "checker": CHECKER_HTML,
        "req": req_html,
        "qualify": q_html,
        "notq": n_html,
        "cta": cta_dark("Likely eligible?", "Let's turn a maybe into a yes.",
                        "Book a free call and we'll confirm your eligibility properly, then handle the entire application for you."),
    }


# ----------------------------------------------------------------------------
# PAGE: find-a-dentist
# ----------------------------------------------------------------------------
def body_dentist():
    needs = [
        ("01", "i-clipboard", "An itemised quote", "Each procedure listed with its dental item number and cost, on the practice's official letterhead.", "Required"),
        ("02", "i-file", "A necessity statement", "A short letter confirming the treatment is clinically necessary and shouldn't be delayed.", "Most important"),
        ("03", "i-award", "Practice details", "The dentist's registration number and practice ABN — usually already on the letterhead.", "Usually automatic"),
    ]
    need_html = "".join(
        '<div class="card %s card-hover reveal" data-d="%d"><span class="step-num">%s</span><h3 style="font-size:1.1rem;margin:18px 0 9px;">%s</h3><p style="color:var(--fg-muted);font-size:.94rem;margin-bottom:14px;">%s</p><span class="pill" style="color:var(--violet);"><svg class="icon"><use href="#i-check"/></svg>%s</span></div>'
        % ("card-glow" if i == 1 else "", i, n, t, d, tag)
        for i, (n, ic, t, d, tag) in enumerate(needs)
    )

    treatments = [
        ("i-tooth", "Implants & missing teeth", "Implants, bridges and dentures that restore function and prevent bone loss."),
        ("i-stethoscope", "Root canal treatment", "Endodontic work to relieve pain and save an infected tooth."),
        ("i-heart", "Gum disease treatment", "Periodontal care for gum disease affecting oral and general health."),
        ("i-gear", "Crowns & restorations", "Crowns, inlays and major repairs for compromised teeth."),
        ("i-scissors", "Extractions & surgery", "Complex extractions, impacted wisdom teeth and oral surgery."),
        ("i-sparkle", "Some orthodontics", "Braces or aligners where there's a documented functional or health need."),
    ]
    treat_html = "".join(
        '<div class="card card-line card-hover reveal" data-d="%d" style="display:flex;gap:16px;align-items:flex-start;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#%s"/></svg></span><div><h4 style="font-size:.98rem;margin-bottom:5px;">%s</h4><p style="color:var(--fg-muted);font-size:.88rem;">%s</p></div></div>'
        % (i % 3, ic, t, d) for i, (ic, t, d) in enumerate(treatments)
    )

    tips = [
        ("i-chat", '"I need an itemised quote for an ATO super release"', "This exact phrase tells your dentist precisely what kind of document to prepare."),
        ("i-clipboard", "Ask for dental item numbers", "The ATO needs procedure codes — a plain description on its own isn't enough."),
        ("i-file", "Request a one-paragraph necessity note", "Have them confirm the treatment is clinically necessary. This matters most."),
        ("i-printer", "Everything on letterhead", "Practice name, ABN and the dentist's signature — the ATO rejects documents without them."),
    ]
    tip_html = "".join(
        '<div class="flex gap-sm reveal" style="gap:14px;align-items:flex-start;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#%s"/></svg></span><div><h4 style="font-size:.96rem;margin-bottom:4px;">%s</h4><p style="color:var(--fg-muted);font-size:.9rem;">%s</p></div></div>'
        % (ic, t, d) for ic, t, d in tips
    )

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(56px,8vw,90px);">
  <div class="glow-blob" style="width:500px;height:500px;background:rgba(140,82,255,.26);top:-130px;left:-90px;"></div>
  <div class="glow-blob" style="width:360px;height:360px;background:rgba(107,63,212,.26);bottom:-110px;right:-70px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">Find a dentist</span>
    <h1 class="reveal" data-d="1" style="margin:18px 0 18px;">Use your own dentist. <span class="gradient-text">Or we'll help you find one.</span></h1>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:620px;margin:0 auto 32px;line-height:1.7;">The ATO doesn't require a special dentist — any registered Australian practice can provide what you need. We brief them on the rest.</p>
    <div class="hero-cta-row reveal" data-d="3" style="justify-content:center;">
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-lg">Book a free call<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      <a href="eligibility.html" class="btn btn-ghost-light btn-lg">Check eligibility first</a>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap wrap-md" style="margin:0 auto;">
    <div class="card card-glow reveal center" style="padding:44px;">
      <span class="chip chip-grad" style="width:64px;height:64px;border-radius:20px;margin:0 auto 18px;"><svg class="icon" style="width:30px;height:30px;"><use href="#i-tooth"/></svg></span>
      <h2 style="font-size:clamp(1.5rem,3vw,2.1rem);margin-bottom:14px;">Your existing dentist is probably perfect</h2>
      <p class="lead" style="max-width:560px;margin:0 auto;">There's no closed network here. Use the dentist you already trust, or a new one near you. All the ATO needs is an itemised quote on their letterhead — and we handle everything around it.</p>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">For your dentist</span>
      <h2 class="reveal" data-d="1">What the ATO needs from them</h2>
      <p class="reveal" data-d="2">Three straightforward documents — most practices can prepare them in a single appointment.</p>
    </div>
    <div class="grid g-3">%(needs)s</div>
    <p class="center reveal" style="margin-top:26px;color:var(--fg-subtle);font-size:.92rem;">We send your dentist a clear one-page guide spelling out exactly what to include.</p>
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center reveal">Eligible treatment</span>
      <h2 class="reveal" data-d="1">What dental work tends to qualify</h2>
      <p class="reveal" data-d="2">Necessary, health-driven treatment qualifies far more readily than purely cosmetic work.</p>
    </div>
    <div class="grid g-3">%(treat)s</div>
    <div class="wrap-md" style="margin:28px auto 0;">
      <div class="note note-amber reveal"><svg class="icon"><use href="#i-warning"/></svg><div><h4>Purely cosmetic work won't qualify</h4><p>Whitening, aesthetic-only veneers and cosmetic contouring aren't approved by the ATO — treatment has to address a genuine health need. Not sure which side yours falls on? Book a free call and we'll tell you honestly.</p></div></div>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div>
      <span class="eyebrow reveal">At the appointment</span>
      <h2 class="reveal" data-d="1" style="font-size:clamp(1.7rem,3.4vw,2.4rem);margin:14px 0 28px;">What to say to your dentist</h2>
      <div class="flex" style="flex-direction:column;gap:22px;">%(tips)s</div>
    </div>
    <div class="card card-glow reveal" data-d="1">
      <span class="eyebrow">We make it easy</span>
      <h3 style="font-size:1.3rem;margin:12px 0 16px;">We brief your dentist for you</h3>
      <p style="color:var(--fg-muted);margin-bottom:22px;">Once you're underway, we send your practice a one-page briefing covering exactly what the ATO requires — so they don't have to guess.</p>
      <ul class="checklist">
        <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Required item-number format</span></li>
        <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Necessity-letter wording guide</span></li>
        <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Letterhead checklist</span></li>
        <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>A direct line if they have questions</span></li>
      </ul>
      <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-block" style="margin-top:24px;">Book your free consult<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
    </div>
  </div>
</section>

%(cta)s
""" % {
        "book": BOOK,
        "needs": need_html,
        "treat": treat_html,
        "tips": tip_html,
        "cta": cta_dark("Your super, your smile", "Ready to get your dental work funded?",
                        "Book a free call. We'll confirm eligibility, brief your dentist, and prepare your whole ATO application."),
    }


# ----------------------------------------------------------------------------
# PAGE: faq
# ----------------------------------------------------------------------------
FAQ_GROUPS = [
    ("i-shield", "Is this safe & legitimate?", [
        ("Is this actually legal?", "Yes. Compassionate Release of Super is a legitimate program administered by the ATO that permits early access to super for necessary medical and dental treatment. We operate strictly within its published rules."),
        ("How do I know you're not a scam?", "Fair question — the regulator has warned about dodgy operators, so scepticism is healthy. The honest signals to look for: we never ask you to pay for your treatment upfront, funds are released to you (not us), and we charge no service fee unless your application is approved."),
        ("Do you ever take my treatment money?", "No. Your released super is paid to you, and you pay your dentist directly. We're never in the middle of your treatment funds."),
        ("What if my application isn't approved?", "Then you don't pay our service fee. We'll also review the ATO's reasons and advise whether it's worth reapplying with additional documentation."),
    ]),
    ("i-user", "Eligibility", [
        ("Am I eligible?", "Generally you need an active Australian super fund, dental treatment that's medically necessary (not cosmetic), an inability to readily pay for it another way, and enough super to cover the cost. The ATO assesses each case individually — our free check gives you a reliable early read."),
        ("Does my employment status matter?", "No. Compassionate release isn't tied to whether you're employed, self-employed or not working. What matters is the medical necessity of the treatment and that it can't reasonably wait."),
        ("Can I access super for my family's dental work?", "The program allows release to cover necessary treatment for you, your spouse or your children. Each person's claim must independently meet the criteria with its own documentation."),
        ("Does cosmetic work qualify?", "No. Purely cosmetic treatment — whitening, aesthetic veneers, contouring — doesn't meet the criteria. Treatment must relieve pain or protect your health."),
    ]),
    ("i-route", "The process", [
        ("What does Super Smiles actually do?", "We run the whole thing: confirm eligibility, coordinate your GP letter, brief your dentist and gather the itemised quote, prepare and lodge the ATO application, and support you until your fund releases the money. You don't deal with the ATO directly."),
        ("How long does it take?", "It varies, but the ATO aims to process most complete applications within around 14 business days, after which your fund processes payment. Assembling documents is usually the longest part — and the part we accelerate."),
        ("Can I use my own dentist?", "Absolutely. Any registered Australian dentist works — we brief them on exactly what the ATO needs so the quote is right first time."),
        ("Do I have to deal with the ATO myself?", "No. With your authority we prepare and lodge everything on your behalf and manage any follow-up requests."),
    ]),
    ("i-percent", "Costs, super & tax", [
        ("How much do you charge?", "The eligibility check is free. Our service fee is $600 for every $10,000 successfully released, charged only after the funds come through. No approval, no fee."),
        ("Are there hidden costs?", "No hidden charges from us. You may pay your dentist and GP their normal consultation fees, and once super is released your treatment is paid from those funds."),
        ("Is released super taxed?", "Yes. Compassionate release is taxable and your fund withholds tax before paying you — typically around 22%, with the exact rate depending on your age and the components of your super. We're not tax advisers and recommend confirming your position with one."),
        ("Will this affect my retirement or Centrelink?", "Money released now won't be in your super at retirement, and a payment could affect Centrelink depending on your circumstances. These are important trade-offs — we're upfront about them and suggest speaking with a financial adviser."),
    ]),
]


def body_faq():
    groups = []
    for ic, title, items in FAQ_GROUPS:
        groups.append("""<div class="reveal" style="margin-bottom:44px;">
      <div class="flex gap-sm items-center" style="gap:14px;margin-bottom:20px;">
        <span class="chip chip-violet chip-sm"><svg class="icon"><use href="#%s"/></svg></span>
        <h2 style="font-size:1.35rem;">%s</h2>
      </div>
      <div class="faq">%s</div>
    </div>""" % (ic, title, faq_block(items)))

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(48px,6vw,72px);">
  <div class="glow-blob" style="width:480px;height:480px;background:rgba(140,82,255,.26);top:-120px;right:-80px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">FAQ</span>
    <h1 class="reveal" data-d="1" style="margin:18px 0 18px;">Honest answers to <span class="gradient-text">every question.</span></h1>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:560px;margin:0 auto;line-height:1.7;">Including the ones you're right to ask before trusting anyone with your retirement savings.</p>
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap wrap-md" style="margin:0 auto;">
    %(groups)s
    <div class="note note-violet reveal"><svg class="icon"><use href="#i-info"/></svg><div><h4>General information only</h4><p>Super Smiles facilitates Compassionate Release of Super applications. We're not financial advisers, tax agents or lawyers, and the answers here are general. For advice on your personal tax, retirement or Centrelink position, please speak with a qualified professional.</p></div></div>
  </div>
</section>

%(cta)s
""" % {
        "groups": "\n    ".join(groups),
        "cta": cta_dark("Still wondering?", "Ask us anything on a free call.",
                        "No question is too small. We'll give you a straight answer about your specific situation — with no pressure to proceed."),
    }


# ----------------------------------------------------------------------------
# PAGE: about-us
# ----------------------------------------------------------------------------
def body_about():
    values = [
        ("i-shield", "Compliance first", "We align with the ATO and AHPRA, never cut corners, and would rather lose a client than risk theirs."),
        ("i-eye", "Radical honesty", "We explain the tax, the trade-offs and the catches plainly — even when it's easier not to."),
        ("i-heart", "Genuinely done-for-you", "We take on the paperwork that stops people, so getting out of pain isn't a second job."),
        ("i-target", "Aligned incentives", "No approval, no fee. We only succeed when you do — and that keeps us honest."),
        ("i-lock", "Your money stays yours", "Released super goes to you, and you pay your dentist. We're never in the middle of it."),
        ("i-users", "Treated like a person", "One dedicated case manager, no call-centre runaround, no judgment about your situation."),
    ]
    val_html = "".join(
        '<div class="card-dark card-hover reveal" data-d="%d"><span class="chip chip-glass"><svg class="icon"><use href="#%s"/></svg></span><h3>%s</h3><p>%s</p></div>'
        % (i % 3, ic, t, d) for i, (ic, t, d) in enumerate(values)
    )

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(56px,8vw,90px);">
  <div class="glow-blob" style="width:500px;height:500px;background:rgba(140,82,255,.26);top:-130px;left:-80px;"></div>
  <div class="glow-blob" style="width:360px;height:360px;background:rgba(107,63,212,.26);bottom:-110px;right:-70px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">About us</span>
    <h1 class="reveal" data-d="1" style="margin:18px 0 18px;">We exist to get Australians <span class="gradient-text">out of pain.</span></h1>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:620px;margin:0 auto;line-height:1.7;">Too many people live with dental pain because the money to fix it is locked in their super and the paperwork to access it feels impossible. We make that pathway simple, honest and done-for-you.</p>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our mission</span>
      <h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem);margin:16px 0 20px;">A clear path through a confusing system</h2>
      <p class="lead" style="margin-bottom:18px;">The Compassionate Release of Super program is genuinely good policy — but it's buried in requirements that stop people right when they're least able to deal with them.</p>
      <p class="lead">We built Super Smiles to be the opposite of that: plain English, a single dedicated contact, and a service that does the hard parts for you. We only charge when it works, so we're motivated to get it right.</p>
    </div>
    <div class="grid g-2 reveal" data-d="1" style="gap:18px;">
      <div class="card card-line"><div class="mono-num gradient-text" style="font-size:2.6rem;">Free</div><p style="color:var(--fg-muted);font-size:.9rem;margin-top:6px;">Eligibility check</p></div>
      <div class="card card-line" style="margin-top:22px;"><div class="mono-num gradient-text" style="font-size:2.6rem;">$0</div><p style="color:var(--fg-muted);font-size:.9rem;margin-top:6px;">Upfront — pay on success</p></div>
      <div class="card card-line"><div class="mono-num gradient-text" style="font-size:2.6rem;">3</div><p style="color:var(--fg-muted);font-size:.9rem;margin-top:6px;">Documents handled for you</p></div>
      <div class="card card-line" style="margin-top:22px;"><div class="mono-num gradient-text" style="font-size:2.6rem;">AU</div><p style="color:var(--fg-muted);font-size:.9rem;margin-top:6px;">Australia-wide service</p></div>
    </div>
  </div>
</section>

<section class="section bg-night">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow center on-dark reveal">What we stand for</span>
      <h2 class="reveal" data-d="1">Principles we won't bend on</h2>
      <p class="reveal" data-d="2">In a market under scrutiny, how you operate matters as much as what you deliver.</p>
    </div>
    <div class="grid g-3">%(values)s</div>
  </div>
</section>

%(cta)s
""" % {
        "values": val_html,
        "cta": cta_dark("Let's begin", "See if we can help you, for free.",
                        "Book a no-obligation call and we'll give you an honest read on your situation — and take it from there only if it's right for you."),
    }


# ----------------------------------------------------------------------------
# PAGE: contact-us
# ----------------------------------------------------------------------------
def body_contact():
    links = [
        ("eligibility.html", "i-sparkle", "Check my eligibility", "A 60-second, no-obligation self-check."),
        ("how-it-works.html", "i-route", "How the process works", "The full done-for-you journey, step by step."),
        ("find-a-dentist.html", "i-tooth", "Dentist information", "What your dentist needs to prepare."),
        ("faq.html", "i-chat", "Read the FAQ", "Eligibility, process, costs, tax — answered."),
    ]
    link_html = "".join(
        '<a href="%s" class="card card-line card-hover reveal" data-d="%d" style="display:flex;gap:16px;align-items:flex-start;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#%s"/></svg></span><div><h4 style="font-size:.98rem;margin-bottom:4px;">%s</h4><p style="color:var(--fg-muted);font-size:.88rem;">%s</p></div></a>'
        % (href, i % 4, ic, t, d) for i, (href, ic, t, d) in enumerate(links)
    )

    return """
<section class="section hero hero-dark" style="padding-bottom:clamp(48px,6vw,72px);">
  <div class="glow-blob" style="width:480px;height:480px;background:rgba(140,82,255,.26);top:-120px;left:-80px;"></div>
  <div class="glow-blob" style="width:360px;height:360px;background:rgba(107,63,212,.26);bottom:-110px;right:-70px;"></div>
  <div class="wrap wrap-md center" style="position:relative;z-index:2;">
    <span class="eyebrow center on-dark reveal">Contact</span>
    <h1 class="reveal" data-d="1" style="margin:18px 0 18px;">We're here to <span class="gradient-text">help you decide.</span></h1>
    <p class="reveal" data-d="2" style="color:rgba(255,255,255,.66);font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:560px;margin:0 auto;line-height:1.7;">Book a free call for the fastest answer, or send a message and we'll get back to you within one business day.</p>
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap split" style="align-items:start;gap:32px;">
    <div class="reveal">
      <span class="eyebrow">Fastest way to start</span>
      <div class="card card-glow" style="margin-top:18px;">
        <span class="chip chip-grad" style="width:56px;height:56px;border-radius:18px;"><svg class="icon" style="width:26px;height:26px;"><use href="#i-calendar"/></svg></span>
        <h2 style="font-size:1.4rem;margin:18px 0 10px;">Book a free 15-minute call</h2>
        <p style="color:var(--fg-muted);margin-bottom:22px;">Pick a time that suits you. We'll confirm your eligibility, explain the process, and answer anything — with no obligation.</p>
        <ul class="checklist" style="margin-bottom:24px;">
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Confirm whether you're likely eligible</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Understand exactly what's involved</span></li>
          <li><span class="check-dot"><svg class="icon"><use href="#i-check"/></svg></span><span>Ask anything — no question too small</span></li>
        </ul>
        <a href="%(book)s" target="_blank" rel="noopener" class="btn btn-grad btn-lg btn-block">Book my free call<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>
      </div>
      <div class="flex gap-sm" style="margin-top:18px;gap:16px;flex-wrap:wrap;">
        <div class="card card-line" style="flex:1;padding:20px;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#i-globe"/></svg></span><h4 style="font-size:.92rem;margin:12px 0 4px;">Australia-wide</h4><p style="color:var(--fg-muted);font-size:.84rem;">We work with residents and super funds across Australia.</p></div>
        <div class="card card-line" style="flex:1;padding:20px;"><span class="chip chip-violet chip-sm"><svg class="icon"><use href="#i-lock"/></svg></span><h4 style="font-size:.92rem;margin:12px 0 4px;">Confidential</h4><p style="color:var(--fg-muted);font-size:.84rem;">Your details stay private — never shared without consent.</p></div>
      </div>
    </div>

    <div class="reveal" data-d="1">
      <span class="eyebrow">Or send a message</span>
      <div class="card" style="margin-top:18px;">
        <form data-mock="1" data-success="formSuccess" style="display:flex;flex-direction:column;gap:18px;">
          <div class="grid g-2" style="gap:16px;">
            <div class="field"><label for="fn">First name</label><input id="fn" type="text" placeholder="Jordan" required></div>
            <div class="field"><label for="ln">Last name</label><input id="ln" type="text" placeholder="Smith" required></div>
          </div>
          <div class="field"><label for="em">Email</label><input id="em" type="email" placeholder="you@example.com" required></div>
          <div class="field"><label for="tp">What's your enquiry about?</label>
            <select id="tp" required>
              <option value="" disabled selected>Choose a topic…</option>
              <option>Checking my eligibility</option>
              <option>Understanding the process</option>
              <option>Finding or briefing a dentist</option>
              <option>Help with my application</option>
              <option>I'm an existing client</option>
              <option>Something else</option>
            </select>
          </div>
          <div class="field"><label for="ms">Your message</label><textarea id="ms" placeholder="Tell us a little about your situation…" required></textarea></div>
          <div class="note note-violet"><svg class="icon"><use href="#i-info"/></svg><div><p style="color:var(--fg-muted);">Prefer a faster answer? Booking a free call above usually gets you a response the same or next day.</p></div></div>
          <button type="submit" class="btn btn-grad btn-lg btn-block">Send message<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></button>
        </form>
        <div id="formSuccess" class="hidden center" style="padding:30px 10px;">
          <span class="chip chip-grad" style="width:64px;height:64px;border-radius:50%%;margin:0 auto 18px;"><svg class="icon" style="width:30px;height:30px;"><use href="#i-check"/></svg></span>
          <h3 style="font-size:1.3rem;margin-bottom:10px;">Message sent</h3>
          <p style="color:var(--fg-muted);">Thanks — we'll be in touch within one business day. For a faster answer, you're welcome to <a href="%(book)s" target="_blank" rel="noopener" style="color:var(--violet);font-weight:600;">book a free call</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight bg-white">
  <div class="wrap">
    <div class="section-head center" style="margin-bottom:36px;">
      <span class="eyebrow center reveal">Help yourself</span>
      <h2 class="reveal" data-d="1" style="font-size:clamp(1.5rem,3vw,2.1rem);">Find an answer right now</h2>
    </div>
    <div class="grid g-2">%(links)s</div>
  </div>
</section>

<section class="section-tight bg-paper">
  <div class="wrap wrap-md" style="margin:0 auto;">
    <div class="note note-violet reveal"><svg class="icon"><use href="#i-info"/></svg><div><h4>Not financial or legal advice</h4><p>Super Smiles facilitates Compassionate Release of Super applications. We're not financial advisers, tax agents or lawyers. For advice on how early access affects your retirement, tax or Centrelink position, please consult a qualified professional. Australia only.</p></div></div>
  </div>
</section>
""" % {"book": BOOK, "links": link_html}


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
PAGES = [
    ("index.html", "Super Smiles — Use Your Super for Urgent Dental Care", "Access your superannuation early through the ATO Compassionate Release of Super program to pay for urgent dental treatment. Free eligibility check, done-for-you, no approval no fee.", "home", body_index),
    ("how-it-works.html", "How It Works — Super Smiles", "A done-for-you process: free eligibility check, GP letter, itemised dental quote, and ATO lodgement. You only pay when your super is released.", "how", body_how),
    ("eligibility.html", "Check Your Eligibility — Super Smiles", "Find out in 60 seconds if you're likely eligible to access your super early for dental treatment through the ATO's Compassionate Release of Super.", "elig", body_elig),
    ("find-a-dentist.html", "Find a Dentist — Super Smiles", "Use your own dentist or find one nearby. See exactly what the ATO needs from your dental practice — we brief them for you.", "dentist", body_dentist),
    ("faq.html", "FAQ — Super Smiles", "Honest answers about safety, eligibility, the process, costs and tax for accessing super early for dental treatment via the ATO.", "faq", body_faq),
    ("about-us.html", "About Us — Super Smiles", "We help Australians get out of dental pain by making early super access simple, honest and done-for-you.", "about", body_about),
    ("contact-us.html", "Contact — Super Smiles", "Book a free call or send a message about using your super for urgent dental treatment. Australia-wide.", "contact", body_contact),
]

for fname, title, desc, active, fn in PAGES:
    html = page(title, desc, active, fn())
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)

print("done")
