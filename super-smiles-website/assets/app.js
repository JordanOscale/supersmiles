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
