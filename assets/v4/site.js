/* Waterwell Clinic v4 — shared behaviour for every v4 page.
   Loaded AFTER the inline analytics block on each page, which declares
   GA4_ID / AW_ID / AW_LEAD and the gtag loader (kept inline on purpose:
   tools/build_conditions.py reads those constants out of index.html). */

// ── Lead-magnet quiz ────────────────────────────────────────────────────
// "What's Driving Your Eczema?" — free 3-minute, 10-question quiz on
// ScoreApp; results are emailed. NOT PUBLICLY PUBLISHED YET (7 Nov 2026).
// This is the ONLY place the URL lives: every link marked data-quiz gets
// it from here. Swap it once the quiz (or an on-site version) goes live.
const QUIZ_URL = 'https://kohei-63rjqpz4.scoreapp.com';

(function(){
  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Browser time zone rides along in a hidden field on every enquiry form,
  // so the client is never asked for it. Silent if unsupported.
  try {
    const zone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    const local = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    document.querySelectorAll('input[name="timezone"]').forEach(el => {
      el.value = zone ? `${zone} (their local time ${local})` : '';
    });
  } catch (e) {}

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Quiz links
  document.querySelectorAll('a[data-quiz]').forEach(a => {
    a.href = QUIZ_URL;
    a.addEventListener('click', () => {
      if (typeof gtag === 'function') gtag('event', 'quiz_click', {location: a.dataset.quiz || ''});
    });
  });

  // Nav state + sticky mobile CTA
  const nav = document.getElementById('nav'), mcta = document.getElementById('mcta');
  const visit = document.getElementById('visit');
  function onScroll(){
    const y = window.scrollY;
    if (nav) nav.classList.toggle('scrolled', y > 20);
    if (mcta){
      let hide = false;
      if (visit){ hide = visit.getBoundingClientRect().top < window.innerHeight * 0.85; }
      mcta.classList.toggle('show', y > window.innerHeight * 0.8 && !hide);
    }
  }
  addEventListener('scroll', onScroll, {passive:true}); onScroll();

  // Mobile drawer
  const burger = document.getElementById('burger'), drawer = document.getElementById('drawer');
  if (burger && drawer){
    const setDrawer = open => {
      drawer.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      drawer.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('drawer-open', open);
      if (open){ drawer.scrollTop = 0; const first = drawer.querySelector('a'); if (first) first.focus(); }
    };
    burger.addEventListener('click', () => setDrawer(!drawer.classList.contains('open')));
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setDrawer(false)));
    addEventListener('keydown', e => {
      if (e.key === 'Escape' && drawer.classList.contains('open')) { setDrawer(false); burger.focus(); }
    });
  }

  // Reveals (subtle: .45s, 14px, no blur — see the 10 Aug motion budget)
  const rev = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce){
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    }), {threshold:0.02, rootMargin:'0px 0px 10% 0px'});
    rev.forEach(el => io.observe(el));
  } else rev.forEach(el => el.classList.add('in'));

  // Credibility strip — WCAG 2.2.2: moving content needs a pause control.
  const cred = document.querySelector('.cred'), credBtn = document.querySelector('.cred-toggle');
  if (cred && credBtn){
    credBtn.addEventListener('click', () => {
      const p = cred.classList.toggle('paused');
      credBtn.setAttribute('aria-pressed', String(p));
      credBtn.setAttribute('aria-label', p ? 'Play the credentials ticker' : 'Pause the credentials ticker');
    });
  }

  // /conditions/* 301 to /#tsw, /#acne ... : open the matching panel.
  function openFromHash(){
    const id = decodeURIComponent(location.hash.slice(1));
    const el = id && document.getElementById(id);
    if (el && el.tagName === 'DETAILS'){ el.open = true;
      const top = el.getBoundingClientRect().top + scrollY - (nav ? nav.getBoundingClientRect().height + 16 : 0);
      scrollTo(0, Math.max(0, top)); }
  }
  openFromHash(); addEventListener('hashchange', openFromHash);

  // Fixed-duration anchor scrolling (carried over from v3).
  const DUR = 560;
  const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3)/2;
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const el = id && document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    const start = scrollY;
    const offset = nav ? nav.getBoundingClientRect().height : 0;
    const max = document.documentElement.scrollHeight - innerHeight;
    const dest = Math.max(0, Math.min(el.getBoundingClientRect().top + start - offset, max));
    const dist = dest - start;
    const done = () => {
      history.replaceState(null, '', '#' + id);
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
      el.focus({preventScroll:true});
    };
    if (reduce || Math.abs(dist) < 2){ scrollTo(0, dest); done(); return; }
    let t0 = null;
    requestAnimationFrame(function step(t){
      if (!t0) t0 = t;
      const p = Math.min(1, (t - t0)/DUR);
      scrollTo(0, start + dist*ease(p));
      p < 1 ? requestAnimationFrame(step) : done();
    });
  });
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
      if(!name){ f.name.focus(); say('Please add your name so Kohei knows who to reply to.', false); return; }
      if(!email){ f.email.focus(); say('Please add an email address for the reply.', false); return; }
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){ f.email.focus();
        say('That email address does not look right. Check it and try again.', false); return; }

      // The form is novalidate, so every required field needs its own check.
      const hasCity = !!f.city;
      const city = hasCity ? f.city.value.trim() : '';
      if(hasCity && !city){ f.city.focus(); say('Please add your city so Kohei can offer a sensible time.', false); return; }

      const concern = booking || (f.concern ? f.concern.value : '');
      const tz = (f.timezone && f.timezone.value) || '';
      const msg = f.msg ? (f.msg.value || '') : '';
      const body = ('Name: ' + name + '\nEmail: ' + email
        + (hasCity ? '\nCity: ' + city : '')
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
          say(f.dataset.thanks || 'Thanks, that’s come through. Kohei usually replies within one working day.', true);
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
