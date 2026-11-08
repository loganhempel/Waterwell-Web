/* Waterwell concept, Spec style: shared behaviour for every /concept-spec page.
   Loaded AFTER the inline analytics block on pages with a form (GA4_ID /
   AW_ID / AW_LEAD + gtag loader, identical to v4). The enquiry handler at the
   bottom is copied unchanged from /assets/v4/site.js. */

// The ONLY place the quiz URL lives: every a[data-quiz] gets it from here.
const QUIZ_URL = 'https://kohei-63rjqpz4.scoreapp.com';

(function(){
  var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  var yr=$('#yr'); if(yr) yr.textContent=new Date().getFullYear();

  // Browser time zone rides along in a hidden field (as v4).
  try {
    var zone=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
    var local=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
    $$('input[name="timezone"]').forEach(function(el){ el.value=zone?zone+' (their local time '+local+')':''; });
  } catch(e){}

  // Quiz links
  $$('a[data-quiz]').forEach(function(a){
    a.href=QUIZ_URL;
    a.addEventListener('click',function(){ if(typeof gtag==='function') gtag('event','quiz_click',{location:a.dataset.quiz||''}); });
  });

  // Nav state + sticky mobile CTA (steps aside while a [data-mcta-hide] band is on screen)
  var nav=$('#nav'), mcta=$('#mcta'), hiders=$$('[data-mcta-hide]');
  function onScroll(){
    var y=scrollY;
    if(nav) nav.classList.toggle('solid', y>24);
    if(mcta){
      var hide=hiders.some(function(el){ var r=el.getBoundingClientRect(); return r.top<innerHeight*.85 && r.bottom>0; });
      mcta.classList.toggle('show', y>innerHeight*.8 && !hide);
    }
  }
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  // Mobile sheet
  var mb=$('#menuBtn'), sh=$('#sheet');
  if(mb&&sh){
    var setSheet=function(open){ mb.setAttribute('aria-expanded',open?'true':'false'); mb.setAttribute('aria-label',open?'Close menu':'Open menu'); sh.hidden=!open; };
    mb.addEventListener('click',function(){ setSheet(sh.hidden); });
    $$('a',sh).forEach(function(a){ a.addEventListener('click',function(){ setSheet(false); }); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!sh.hidden){ setSheet(false); mb.focus(); } });
  }

  // /conditions/* 301s land on /#tsw, /#acne ...: open the matching panel.
  function openFromHash(){
    var id=decodeURIComponent(location.hash.slice(1)), el=id&&document.getElementById(id);
    if(el&&el.tagName==='DETAILS'){ el.open=true; el.scrollIntoView({block:'start'}); }
  }
  openFromHash(); addEventListener('hashchange',openFromHash);

  // Hero quiz card: ticks land once, in order
  var rows=$$('#quizCard .g-row');
  if(reduce){ rows.forEach(function(r){ r.classList.add('on'); }); }
  else rows.forEach(function(r,i){ setTimeout(function(){ r.classList.add('on'); var t=$('.tick',r); t.classList.add('ping'); setTimeout(function(){ t.classList.remove('ping'); },380); }, 900+i*650); });

  // Scroll-linked lists (clear path + journey)
  function track(list,rowSel){
    if(!list) return;
    var items=$$(rowSel,list);
    if(reduce||!('IntersectionObserver' in window)){ items.forEach(function(r){ r.classList.add('in'); }); list.style.setProperty('--prog','100%'); return; }
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); },{rootMargin:'0px 0px -35% 0px'});
    items.forEach(function(r){ io.observe(r); });
    var tick=false;
    function prog(){ tick=false; var r=list.getBoundingClientRect(), p=(innerHeight*.65-r.top)/r.height; p=Math.max(0,Math.min(1,p)); list.style.setProperty('--prog',(p*100).toFixed(1)+'%'); }
    addEventListener('scroll',function(){ if(!tick){ tick=true; requestAnimationFrame(prog); } },{passive:true}); prog();
  }
  track($('#bwList'),'.bw-row');
  track($('#jList'),'.j-step');

  // Ripple rings: run only while visible, with a pause control
  var rings=$('#rings'), pp=$('#ringsPP');
  if(rings&&pp){
    var on=!reduce, vis=false;
    if(reduce){ pp.hidden=true; }
    else {
      var apply=function(){ rings.classList.toggle('go',vis); rings.classList.toggle('paused',!on||document.hidden); };
      new IntersectionObserver(function(es){ vis=es[0].isIntersecting; apply(); },{threshold:.1}).observe(rings.parentNode);
      document.addEventListener('visibilitychange',apply);
      pp.addEventListener('click',function(){ on=!on; pp.setAttribute('aria-pressed',on?'false':'true'); pp.classList.toggle('paused',!on); $('.pp-t',pp).textContent=on?'Pause':'Play'; apply(); });
    }
  }
})();

// ── Enquiry forms ───────────────────────────────────────────────────────
// One handler for every form[data-enquiry]: the homepage #visit form and the
// two booking landers. The plumbing is the v3 handler unchanged — Web3Forms
// primary post, optional clinic copy, fail-safe honeypot, browser time zone,
// mailto fallback, and the Google Ads conversion fired ONLY in the success
// branch. Per form, only the subject, the booking type and the GA `form`
// label differ (data-subject / data-booking / data-form).
(function(){
  // Do NOT add a `ccemail` field: Web3Forms free rejects it with HTTP 400 and
  // the submission dies invisibly. Test against production.
  const WEB3FORMS_KEY = 'afca65db-afc1-4398-8f94-7a142f2994bb';
  const KEY_SET = /^[0-9a-f-]{30,}$/i.test(WEB3FORMS_KEY);

  // Second recipient (the clinic's own inbox) — a second access key, never a
  // CC. Empty = the copy is skipped outright, so behaviour cannot regress.
  const CLINIC_KEY = '';
  const CLINIC_SET = /^[0-9a-f-]{30,}$/i.test(CLINIC_KEY);

  // Fire-and-forget. The visitor's success message depends ONLY on the
  // primary post.
  function copyToClinic(payload){
    if(!CLINIC_SET) return;
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: {'Content-Type':'application/json', 'Accept':'application/json'},
      body: JSON.stringify(Object.assign({}, payload, {access_key: CLINIC_KEY}))
    }).catch(function(){ /* the lead is already captured; nothing to surface */ });
  }

  function mailtoFallback(name, body, subject){
    window.location.href = 'mailto:info@waterwellclinic.com?subject='
      + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  document.querySelectorAll('form[data-enquiry]').forEach(f => {
    const formLabel = f.dataset.form || 'discovery_session';
    const subjectBase = f.dataset.subject || 'Website enquiry';
    const booking = f.dataset.booking || '';

    const status = document.createElement('p');
    status.className = 'bf-status';
    status.setAttribute('role','status');
    status.setAttribute('aria-live','polite');
    status.hidden = true;
    const _sub = f.querySelector('[type="submit"]');
    if (_sub) f.insertBefore(status, _sub); else f.appendChild(status);

    function say(msg, ok){
      status.textContent = msg;
      status.hidden = false;
      status.classList.toggle('ok', !!ok);
      status.classList.toggle('err', !ok);
    }

    f.addEventListener('submit', async e => {
      e.preventDefault();
      // Honeypot is fail-safe: a filled honeypot flags the subject for
      // triage, it never discards a lead (Chrome autofill fills these).
      const suspect = !!(f.bf_xq7 && f.bf_xq7.value.trim());
      const name = f.name.value.trim(), email = f.email.value.trim();
      if(!name){ f.name.focus(); say('Please add your name so I know who to reply to.', false); return; }
      if(!email){ f.email.focus(); say('Please add an email address for the reply.', false); return; }
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){ f.email.focus();
        say('That email address does not look right. Check it and try again.', false); return; }

      // The form is novalidate, so every required field needs its own check.
      // City is optional (audit 2): the browser time zone already rides along.
      const hasCity = !!f.city;
      const city = hasCity ? f.city.value.trim() : '';
      if(hasCity && f.city.required && !city){ f.city.focus(); say('Please add your city so I can offer a sensible time.', false); return; }

      const concern = booking || (f.concern ? f.concern.value : '');
      const tz = (f.timezone && f.timezone.value) || '';
      const msg = f.msg ? (f.msg.value || '') : '';
      const body = ('Name: ' + name + '\nEmail: ' + email
        + (city ? '\nCity: ' + city : '')
        + (tz ? '\nTime zone: ' + tz : '')
        + (booking ? '\nBooking: ' + booking : '\nEnquiry: ' + (concern || 'Not specified'))
        + '\n\n' + msg).trim();
      const subject = (suspect ? '[CHECK] ' : '') + subjectBase + ' — ' + name
        + (!booking && concern ? ' (' + concern + ')' : '');

      if(!KEY_SET){ mailtoFallback(name, body, subject); return; }

      const btn = f.querySelector('[type="submit"]');
      const label = btn ? btn.innerHTML : '';
      if(btn){ btn.disabled = true; btn.textContent = 'Sending…'; }
      say('Sending…', true);

      const payload = {
        access_key: WEB3FORMS_KEY,
        subject: subject,
        from_name: 'Waterwell website',
        name: name,
        email: email,
        city: city,
        timezone: tz,
        concern: concern,
        message: msg,
        page: location.pathname
      };
      if (booking) payload.booking_type = booking;
      copyToClinic(payload);

      try {
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: {'Content-Type':'application/json', 'Accept':'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await res.json().catch(() => ({}));
        if(res.ok && data.success){
          f.reset();
          say(f.dataset.thanks || 'Thanks, that’s come through. My team and I reply within one working day.', true);
          // Conversion signal — the success branch is the ONLY place the
          // Google Ads conversion fires (there is no thank-you page).
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({event:'generate_lead', form:formLabel, concern:concern});
          if(typeof gtag === 'function'){
            gtag('event','generate_lead',{form:formLabel, concern:concern});
            gtag('event','conversion',{send_to:AW_LEAD, value:1.0, currency:'AUD'});
          }
        } else {
          say('That didn’t send, so your email app will open instead.', false);
          mailtoFallback(name, body, subject);
        }
      } catch(err){
        say('That didn’t send, so your email app will open instead.', false);
        mailtoFallback(name, body, subject);
      } finally {
        if(btn){ btn.disabled = false; btn.innerHTML = label; }
      }
    });
  });
})();
