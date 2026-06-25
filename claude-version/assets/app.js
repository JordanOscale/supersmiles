/* ============================================================
   SUPER SMILES — interactions
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Mobile nav ---------- */
  function initNav() {
    var burger = document.getElementById('burger');
    var menu = document.getElementById('mobileMenu');
    if (!burger || !menu) return;
    var iconMenu = burger.querySelector('.i-menu');
    var iconClose = burger.querySelector('.i-close');
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (iconMenu && iconClose) {
        iconMenu.classList.toggle('hidden', open);
        iconClose.classList.toggle('hidden', !open);
      }
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.remove('open');
        if (iconMenu && iconClose) { iconMenu.classList.remove('hidden'); iconClose.classList.add('hidden'); }
      });
    });
  }

  /* ---------- FAQ accordion ---------- */
  function initFaq() {
    document.querySelectorAll('.faq-q').forEach(function (q) {
      q.addEventListener('click', function () {
        var item = q.closest('.faq-item');
        var ans = item.querySelector('.faq-a');
        var isOpen = item.classList.contains('open');
        // close siblings within same group
        var group = item.closest('.faq') || document;
        group.querySelectorAll('.faq-item.open').forEach(function (other) {
          if (other !== item) {
            other.classList.remove('open');
            other.querySelector('.faq-a').style.maxHeight = null;
          }
        });
        if (isOpen) {
          item.classList.remove('open');
          ans.style.maxHeight = null;
        } else {
          item.classList.add('open');
          ans.style.maxHeight = ans.scrollHeight + 'px';
        }
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || !els.length) {
      els.forEach(function (e) { e.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---------- Contact / notify forms ---------- */
  function initForms() {
    document.querySelectorAll('form[data-mock]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var success = document.getElementById(form.getAttribute('data-success'));
        if (success) { form.classList.add('hidden'); success.classList.remove('hidden'); }
      });
    });
  }

  /* ---------- Eligibility checker ---------- */
  var BOOKING = 'https://book.supersmiles.au/widget/booking/IcBxYi1F0l8vxlMzEX2c';

  var QUESTIONS = [
    {
      q: 'Do you have an active Australian super fund?',
      help: 'Industry, retail and self-managed funds all generally qualify.',
      opts: [
        { t: 'Yes, I have super', v: 'good' },
        { t: 'I’m not sure', v: 'maybe' },
        { t: 'No active super', v: 'bad' }
      ]
    },
    {
      q: 'What kind of dental treatment do you need?',
      help: 'The ATO covers treatment that is medically necessary — not purely cosmetic.',
      opts: [
        { t: 'Treatment for pain, infection or a health issue', v: 'good' },
        { t: 'A mix of necessary and cosmetic work', v: 'maybe' },
        { t: 'Purely cosmetic (whitening, aesthetic veneers)', v: 'bad' }
      ]
    },
    {
      q: 'Can you comfortably afford the treatment another way?',
      help: 'This scheme exists specifically for people who can’t readily cover the cost.',
      opts: [
        { t: 'No — I can’t cover it right now', v: 'good' },
        { t: 'It would be a real stretch', v: 'good' },
        { t: 'Yes, easily', v: 'maybe' }
      ]
    },
    {
      q: 'Have you had a dental assessment or quote?',
      help: 'You don’t need this yet — we help arrange it. We’re just getting a picture.',
      opts: [
        { t: 'Yes, I have a quote ready', v: 'good' },
        { t: 'I’ve seen a dentist but no quote yet', v: 'good' },
        { t: 'Not yet', v: 'maybe' }
      ]
    }
  ];

  function initChecker() {
    var root = document.getElementById('checker');
    if (!root) return;

    var bar = root.querySelector('#checkerBar');
    var stage = root.querySelector('#checkerStage');
    var foot = root.querySelector('#checkerFoot');
    var stepLbl = root.querySelector('#checkerStep');
    var backBtn = root.querySelector('#checkerBack');

    var idx = 0;
    var answers = [];

    function render() {
      var Q = QUESTIONS[idx];
      var pct = ((idx) / QUESTIONS.length) * 100;
      bar.style.width = Math.max(8, pct) + '%';
      stepLbl.textContent = 'Question ' + (idx + 1) + ' of ' + QUESTIONS.length;
      backBtn.style.visibility = idx === 0 ? 'hidden' : 'visible';

      var html = '<div class="q-text">' + Q.q + '</div>';
      html += '<div class="q-help">' + Q.help + '</div>';
      html += '<div class="opt-list">';
      Q.opts.forEach(function (o, i) {
        var sel = answers[idx] === i ? ' selected' : '';
        html += '<button type="button" class="opt' + sel + '" data-i="' + i + '" data-v="' + o.v + '">'
          + '<span class="opt-dot"></span><span>' + o.t + '</span></button>';
      });
      html += '</div>';
      stage.innerHTML = html;

      stage.querySelectorAll('.opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
          answers[idx] = parseInt(btn.getAttribute('data-i'), 10);
          stage.querySelectorAll('.opt').forEach(function (b) { b.classList.remove('selected'); });
          btn.classList.add('selected');
          setTimeout(next, 240);
        });
      });
    }

    function next() {
      if (idx < QUESTIONS.length - 1) { idx++; render(); }
      else { showResult(); }
    }

    function back() {
      if (idx > 0) { idx--; render(); }
    }
    backBtn.addEventListener('click', back);

    function showResult() {
      bar.style.width = '100%';
      foot.classList.add('hidden');

      var scores = answers.map(function (a, i) { return QUESTIONS[i].opts[a].v; });
      var bad = scores.filter(function (s) { return s === 'bad'; }).length;
      var maybe = scores.filter(function (s) { return s === 'maybe'; }).length;

      var verdict = 'good';
      if (bad >= 1) verdict = bad >= 2 ? 'bad' : 'maybe';
      else if (maybe >= 2) verdict = 'maybe';

      var html = '';
      if (verdict === 'good') {
        html = result('good', 'sparkle',
          'Great news — you’re likely eligible',
          'Your answers match the typical profile for the ATO Compassionate Release of Super for dental treatment. The next step is a free, no-obligation consult where we confirm the details and handle the paperwork for you.',
          'Book my free consult');
      } else if (verdict === 'maybe') {
        html = result('maybe', 'info',
          'You may well be eligible',
          'A couple of your answers need a closer look — which is completely normal. Eligibility is assessed case by case, and many people in your situation still qualify. Let’s check properly on a free call.',
          'Check with a free call');
      } else {
        html = result('maybe', 'info',
          'Let’s talk it through',
          'Based on your answers this scheme may not be the right fit right now — but the rules have nuances and a quick conversation costs nothing. We’ll give you an honest answer either way.',
          'Talk to us free');
      }
      stage.innerHTML = html;
      stepLbl.textContent = 'Complete';
    }

    function result(kind, icon, title, body, cta) {
      return '<div class="result reveal in">'
        + '<div class="result-badge ' + kind + '"><svg class="icon"><use href="#i-' + icon + '"/></svg></div>'
        + '<h3>' + title + '</h3>'
        + '<p>' + body + '</p>'
        + '<a href="' + BOOKING + '" target="_blank" rel="noopener" class="btn btn-grad btn-lg btn-block">'
        + cta + '<svg class="icon icon-arrow"><use href="#i-arrow-right"/></svg></a>'
        + '<button type="button" id="checkerRestart" class="checker-back" style="margin:18px auto 0;">'
        + '<svg class="icon icon-sm"><use href="#i-arrow-left"/></svg>Start over</button>'
        + '</div>';
    }

    stage.addEventListener('click', function (e) {
      var r = e.target.closest('#checkerRestart');
      if (r) { idx = 0; answers = []; foot.classList.remove('hidden'); render(); }
    });

    render();
  }

  /* ---------- Footer year ---------- */
  function initYear() {
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- Count-up stats ---------- */
  function initCounters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function fmt(el, v) {
      return (el.getAttribute('data-prefix') || '') + Math.round(v).toLocaleString() + (el.getAttribute('data-suffix') || '');
    }
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.textContent = fmt(el, parseFloat(el.getAttribute('data-count'))); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; io.unobserve(el);
        var target = parseFloat(el.getAttribute('data-count')), dur = 1200, start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(el, target * e);
          if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(el, target);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.45 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Cost slider (tax + fee) ---------- */
  function initSlider() {
    var r = document.getElementById('sliderRange');
    if (!r) return;
    var amt = document.getElementById('sliderAmount'),
        tax = document.getElementById('sliderTax'),
        fee = document.getElementById('sliderFee'),
        net = document.getElementById('sliderNet');
    function money(n) { return '$' + Math.round(n).toLocaleString(); }
    function update() {
      var v = parseInt(r.value, 10);
      var t = v * 0.22;            // estimated tax withheld (~22%)
      var f = (v / 10000) * 600;   // our fee: $600 per $10k
      var n = v - t - f;           // approx left for treatment
      if (amt) amt.textContent = money(v);
      if (tax) tax.textContent = money(t);
      if (fee) fee.textContent = money(f);
      if (net) net.textContent = money(n);
      var pct = (v - r.min) / (r.max - r.min) * 100;
      r.style.background = 'linear-gradient(90deg, var(--violet) ' + pct + '%, var(--violet-soft) ' + pct + '%)';
    }
    r.addEventListener('input', update);
    update();
  }

  /* ---------- Nav shadow on scroll ---------- */
  function initNavShadow() {
    var nav = document.querySelector('.nav');
    if (!nav) return;
    function onScroll() { nav.classList.toggle('scrolled', window.scrollY > 8); }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initNav();
    initFaq();
    initReveal();
    initForms();
    initChecker();
    initYear();
    initCounters();
    initSlider();
    initNavShadow();
  });
})();
