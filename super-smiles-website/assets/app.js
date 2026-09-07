/* Super Smiles — Framer version · shared interactions */
(function () {
  "use strict";

  /* ---- mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("open");
        toggle.classList.remove("open");
      });
    });
  }

  /* ---- FAQ accordion ---- */
  document.querySelectorAll(".faq-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var item = q.closest(".faq-item");
      var ans = item.querySelector(".faq-a");
      var isOpen = item.classList.toggle("open");
      q.setAttribute("aria-expanded", isOpen ? "true" : "false");
      ans.style.maxHeight = isOpen ? ans.scrollHeight + "px" : 0;
    });
  });

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- announcement ticker ----
     Builds the scrolling track from the one message already in the HTML,
     so the markup stays a single source of truth and the no-JS / reduced-
     motion rendering is just that static message, centred.

     The track is aria-hidden and duplicated; the accessible copy is the
     .sr-only paragraph, announced once instead of on every repeat. */
  var announce = document.querySelector(".announce");
  if (announce) {
    /* Each state has its own track; only the active one is displayed, so
       measure that one — a display:none track measures 0 wide. */
    var state = document.documentElement.getAttribute("data-bookings") || "closed";
    var track = announce.querySelector('.announce__track[data-when="' + state + '"]');
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (track && track.children.length && !reduced) {
      /* One "phrase cycle" is every phrase in the track, in order. Repeat
         whole cycles until they outrun the widest plausible viewport, then
         double the lot so translateX(-50%) lands exactly one group along —
         a seamless loop with no empty gap and no phrase cut mid-cycle.
         Screen width, not innerWidth, so resizing can't reveal the end. */
      var cycle = [].slice.call(track.children);
      var cycleWidth = cycle.reduce(function (w, el) {
        return w + el.getBoundingClientRect().width;
      }, 0);
      var target = Math.max(window.innerWidth, window.screen ? window.screen.width : 0) + cycleWidth;
      var reps = cycleWidth > 0 ? Math.max(2, Math.ceil(target / cycleWidth)) : 4;

      var group = document.createDocumentFragment();
      for (var i = 0; i < reps; i++) {
        for (var j = 0; j < cycle.length; j++) group.appendChild(cycle[j].cloneNode(true));
      }
      track.innerHTML = "";
      track.appendChild(group.cloneNode(true));
      track.appendChild(group);
      track.classList.add("is-marquee");
    }

    /* Session-only dismiss. gate-config.js re-reads this on the next page
       load; it is intentionally NOT persisted beyond the session. */
    var dismiss = announce.querySelector(".announce__dismiss");
    if (dismiss) {
      dismiss.addEventListener("click", function () {
        document.documentElement.setAttribute("data-announce", "dismissed");
        try { sessionStorage.setItem("ss-announce-dismissed", "1"); } catch (e) {}
      });
    }
  }

  /* ---- footer year ---- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- smooth page transitions: fade out before navigating to an internal page ---- */
  if (!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches)) {
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      if (a.target === "_blank" || a.hasAttribute("download")) return;
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#") return;            // same-page anchor
      if (/^(https?:|mailto:|tel:)/i.test(href)) return;       // external / non-page link
      e.preventDefault();
      document.body.classList.add("is-leaving");
      setTimeout(function () { window.location.href = href; }, 130);
    });
    // reset when returning via the browser's back/forward cache
    window.addEventListener("pageshow", function (e) {
      if (e.persisted) document.body.classList.remove("is-leaving");
    });
  }

  /* ============================================================
     Eligibility self-check — the category's biggest unmet need.
     Plain-English, judgment-free, "you may be eligible" framing.
     Never guarantees approval (compliance: supersmiles.md §13).
     ============================================================ */
  var checker = document.getElementById("checker");
  if (!checker) return;

  var steps = Array.prototype.slice.call(checker.querySelectorAll(".q-step"));
  var bar = checker.querySelector(".checker-progress > span");
  var counter = checker.querySelector("[data-q-counter]");
  var result = checker.querySelector(".checker-result");
  var yesCount = 0;
  var idx = 0;
  var total = steps.length;

  function render() {
    steps.forEach(function (s, i) { s.classList.toggle("active", i === idx); s.classList.remove("leaving"); });
    if (bar) bar.style.width = ((idx) / total) * 100 + "%";
    if (counter) counter.textContent = "Question " + (idx + 1) + " of " + total;
  }

  var locked = false;
  checker.querySelectorAll(".opt").forEach(function (opt) {
    opt.addEventListener("click", function () {
      if (locked) return;
      locked = true;
      opt.classList.add("selected");          // gradient fill sweeps in
      if (opt.dataset.val === "yes") yesCount++;
      var step = opt.closest(".q-step");
      setTimeout(function () {                 // start fading the current question out
        if (step) step.classList.add("leaving");
      }, 340);
      setTimeout(function () {                 // swap to the next question (it fades in)
        idx++;
        if (idx >= total) { showResult(); } else { render(); }
        locked = false;
      }, 560);
    });
  });

  function showResult() {
    if (bar) bar.style.width = "100%";
    steps.forEach(function (s) { s.classList.remove("active"); });
    if (counter) counter.textContent = "Your result";
    // 3+ "yes" answers => likely eligible. Soft, non-binding language.
    var likely = yesCount >= 3;
    var head = result.querySelector("[data-result-head]");
    var body = result.querySelector("[data-result-body]");
    if (likely) {
      head.textContent = "It could be worth a free check.";
      body.textContent = "People in situations like yours sometimes qualify — but only the ATO can decide. The free check is a no-obligation way to find out where you stand, and we handle the paperwork either way.";
    } else {
      head.textContent = "It's worth checking properly.";
      body.textContent = "Eligibility depends on a few details the ATO looks at, and a quick conversation often surfaces a path you didn't know you had. The check is free, with no obligation and no judgment.";
    }
    result.classList.add("show");
  }

  var restart = checker.querySelector("[data-restart]");
  if (restart) {
    restart.addEventListener("click", function () {
      idx = 0; yesCount = 0; locked = false;
      checker.querySelectorAll(".opt").forEach(function (o) { o.classList.remove("selected"); });
      result.classList.remove("show");
      render();
    });
  }

  render();
})();

/* before/after comparison slider (homepage) — drag anywhere on the bar (mouse + touch) */
(function () {
  var ba = document.getElementById("baSlider");
  if (!ba) return;
  var r = ba.querySelector(".ba-range");
  var set = function (v) {
    v = Math.max(0, Math.min(100, v));
    ba.style.setProperty("--pos", v + "%");
    if (r) r.value = v;
  };
  var posFrom = function (e) {
    var rect = ba.getBoundingClientRect();
    var cx = (e.clientX != null) ? e.clientX
           : (e.touches && e.touches[0]) ? e.touches[0].clientX : rect.left;
    return (cx - rect.left) / rect.width * 100;
  };
  var dragging = false;
  ba.addEventListener("pointerdown", function (e) {
    dragging = true;
    try { ba.setPointerCapture(e.pointerId); } catch (x) {}
    set(posFrom(e));
    e.preventDefault();
  });
  ba.addEventListener("pointermove", function (e) { if (dragging) set(posFrom(e)); });
  var stop = function () { dragging = false; };
  ba.addEventListener("pointerup", stop);
  ba.addEventListener("pointercancel", stop);
  ba.addEventListener("lostpointercapture", stop);
  if (r) r.addEventListener("input", function () { set(r.value); });
  set(r ? r.value : 50);
})();
