/* ============================================================
   Super Smiles — shared script
   - injects an inline SVG icon sprite (no emoji anywhere)
   - mobile nav, eligibility checker, fee calculator, FAQ,
     live-chat stub, scroll reveal, footer year
   ============================================================ */

/* ---------- SVG icon sprite (stroke icons, Geist-friendly) ---------- */
var SPRITE = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
+ '<symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 4l1.7 4.6L18 10l-4.3 1.4L12 16l-1.7-4.6L6 10l4.3-1.4z"/><path d="M18.6 4.2l.5 1.4 1.4.5-1.4.5-.5 1.4-.5-1.4-1.4-.5 1.4-.5z"/></symbol>'
+ '<symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></symbol>'
+ '<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></symbol>'
+ '<symbol id="i-landmark" viewBox="0 0 24 24"><path d="M3 10l9-6 9 6"/><path d="M5 10v9M9 10v9M15 10v9M19 10v9"/><path d="M3 20h18"/></symbol>'
+ '<symbol id="i-card" viewBox="0 0 24 24"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19"/><path d="M6 15h4"/></symbol>'
+ '<symbol id="i-pin" viewBox="0 0 24 24"><path d="M20 10c0 6-8 11-8 11s-8-5-8-11a8 8 0 0116 0z"/><circle cx="12" cy="10" r="3"/></symbol>'
+ '<symbol id="i-file" viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/></symbol>'
+ '<symbol id="i-pulse" viewBox="0 0 24 24"><path d="M22 12h-4l-3 8L9 4l-3 8H2"/></symbol>'
+ '<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></symbol>'
+ '<symbol id="i-user" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></symbol>'
+ '<symbol id="i-users" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/><circle cx="9.5" cy="7" r="4"/><path d="M22 21v-2a4 4 0 00-3-3.9"/><path d="M16 3.1A4 4 0 0116 11"/></symbol>'
+ '<symbol id="i-lock" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/></symbol>'
+ '<symbol id="i-message" viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H8l-5 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></symbol>'
+ '<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></symbol>'
+ '<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>'
+ '<symbol id="i-heart" viewBox="0 0 24 24"><path d="M20.8 5.6a5.4 5.4 0 00-7.7 0L12 6.7l-1.1-1.1a5.4 5.4 0 10-7.7 7.7L12 22l8.8-8.7a5.4 5.4 0 000-7.7z"/></symbol>'
+ '<symbol id="i-tooth" viewBox="0 0 24 24"><path d="M12 5.6C10.6 4 8.7 3.5 7.1 4 5 4.7 3.8 7 4 10c.2 2.5 1 6 2.2 7.8.5.8 1.4.7 1.7-.2.4-1.2.7-3 1.2-4.4.2-.6.5-1 .9-1s.7.4.9 1c.5 1.4.8 3.2 1.2 4.4.3.9 1.2 1 1.7.2C19 16 19.8 12.5 20 10c.2-3-1-5.3-3.1-6-1.6-.5-3.5 0-4.9 1.6z"/></symbol>'
+ '<symbol id="i-smile" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01M15 9h.01"/></symbol>'
+ '<symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.9v2.5a2 2 0 01-2.2 2 19.6 19.6 0 01-8.5-3 19.3 19.3 0 01-6-6 19.6 19.6 0 01-3-8.6A2 2 0 014.3 2H7a2 2 0 012 1.7c.1.9.3 1.7.6 2.5a2 2 0 01-.5 2.1L8 9.4a16 16 0 006 6l1.1-1.1a2 2 0 012.1-.5c.8.3 1.6.5 2.5.6A2 2 0 0122 16.9z"/></symbol>'
+ '<symbol id="i-mail" viewBox="0 0 24 24"><rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M3 6.5l9 6 9-6"/></symbol>'
+ '<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></symbol>'
+ '<symbol id="i-route" viewBox="0 0 24 24"><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M9 19h6a3 3 0 003-3V8"/></symbol>'
+ '<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></symbol>'
+ '<symbol id="i-x" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></symbol>'
+ '</svg>';

(function injectSprite(){
  function go(){ var d=document.createElement('div'); d.innerHTML=SPRITE; document.body.insertBefore(d.firstChild, document.body.firstChild); }
  if(document.body){go();} else {document.addEventListener('DOMContentLoaded',go);}
})();

function ic(id, cls){ return '<svg class="svgi'+(cls?' '+cls:'')+'"><use href="#i-'+id+'"/></svg>'; }

/* ---------- footer year ---------- */
document.addEventListener('DOMContentLoaded',function(){
  var y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
  initReveal();
});

/* ---------- mobile nav ---------- */
function toggleNav(open){var m=document.getElementById('mnav');if(!m)return;m.classList.toggle('open',open);document.body.style.overflow=open?'hidden':'';}

/* ---------- eligibility checker ---------- */
var current=0, answers=[], TOTAL=4;
function showStep(i){
  document.querySelectorAll('#checker .step').forEach(function(s){s.classList.toggle('active',+s.dataset.step===i)});
  var bar=document.getElementById('bar'); if(bar) bar.style.width=(Math.min(i,TOTAL)/TOTAL*100)+'%';
  var b=document.getElementById('backBtn'); if(b) b.style.visibility=(i>0&&i<=TOTAL)?'visible':'hidden';
  current=i;
}
function answer(step,el){
  var opts=document.querySelector('#checker .step[data-step="'+step+'"]').querySelectorAll('.opt');
  answers[step]=Array.prototype.indexOf.call(opts, el);
  if(step<TOTAL-1){ showStep(step+1); }
  else { buildResult(); showStep(TOTAL); }
}
function back(){ if(current>0) showStep(current-1); }
function buildResult(){
  var title="You're likely a good fit for a free check.";
  var body="Based on your answers, it's worth having us confirm your eligibility properly — for free, with no obligation. Pop in a contact and a real person (not a bot) will walk you through the next step.";
  if(answers[2]===2){
    title="Let's find out together — it's still worth a quick chat.";
    body="Not sure if you have super? That's common, and a free check is the easiest way to find out. Leave a contact and we'll help you look into it — no pressure either way.";
  }
  var t=document.getElementById('resTitle'), bd=document.getElementById('resBody');
  if(t) t.textContent=title; if(bd) bd.textContent=body;
}
function submitCheck(){
  var name=(document.getElementById('resName')||{}).value, contact=(document.getElementById('resContact')||{}).value;
  name=(name||'').trim(); contact=(contact||'').trim();
  if(!contact){ alert("Just add an email or mobile so a real person can reach you — that's all we need."); return; }
  var b=document.getElementById('checkerBody');
  b.innerHTML='<div class="result" style="padding:18px 4px"><div class="tick">'+ic('check')+'</div>'+
    '<h3>Thanks'+(name?', '+escapeHtml(name):'')+' — you\'re in good hands.</h3>'+
    '<p>We\'ve got your details. A real person from Super Smiles will be in touch shortly to walk you through your free eligibility check. No judgment, no pressure.</p>'+
    '<div class="disclaim">Demo form — not yet connected to a backend. Wire this to your CRM / booking system before going live.</div></div>';
}
function escapeHtml(s){return s.replace(/[&<>"']/g,function(c){return({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])})}

/* ---------- fee calculator ($600 per $10,000) ---------- */
function calc(){
  var r=document.getElementById('rng'); if(!r) return;
  var v=+r.value;
  var fee=Math.round(v/10000*600);
  var tax=Math.round(v*0.20); // ~20% illustration
  set('rngAmt','$'+v.toLocaleString());
  set('fee','$'+fee.toLocaleString());
  set('tax','$'+tax.toLocaleString());
}
function set(id,val){var e=document.getElementById(id); if(e) e.textContent=val;}

/* ---------- FAQ ---------- */
function toggleFaq(btn){
  var item=btn.parentElement, a=item.querySelector('.faq-a');
  var open=item.classList.toggle('open');
  a.style.maxHeight=open?a.scrollHeight+'px':0;
}

/* ---------- live chat stub ---------- */
function liveChat(e){if(e)e.preventDefault();alert("Sierra — your 24/7 live chat — would open here. (Demo stub: connect your chat widget.)");}

/* ---------- contact form stub ---------- */
function submitContact(e){
  e.preventDefault();
  var f=e.target;
  f.innerHTML='<div class="result" style="padding:8px 4px"><div class="tick">'+ic('check')+'</div>'+
    '<h3>Thanks — message received.</h3>'+
    '<p>A real person from Super Smiles will get back to you shortly. No judgment, no pressure.</p>'+
    '<div class="disclaim">Demo form — connect to your CRM / inbox before going live.</div></div>';
  return false;
}

/* ---------- scroll reveal ---------- */
function initReveal(){
  var els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})
  },{threshold:0.12});
  els.forEach(function(el){io.observe(el)});
}
