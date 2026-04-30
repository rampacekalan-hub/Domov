// Year
document.getElementById('year').textContent = new Date().getFullYear();

// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');
toggle?.addEventListener('click', () => nav.classList.toggle('open'));
nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

// Active nav highlight on scroll
const sections = ['domov','o-nas','sluzby','kontakt'].map(id => document.getElementById(id)).filter(Boolean);
const links = document.querySelectorAll('.main-nav a');
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach(s => obs.observe(s));

// Reveal-on-scroll fade-in
const reveals = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
      revealObs.unobserve(e.target);
    }
  });
}, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
reveals.forEach(el => revealObs.observe(el));

// Animated counters for case studies
const counters = document.querySelectorAll('.case-num');
const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const target = parseFloat(el.dataset.target);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const decimals = (el.dataset.target.includes('.')) ? 1 : 0;
    const duration = 1400;
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const val = (target * eased).toFixed(decimals);
      el.textContent = prefix + val + suffix;
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    counterObs.unobserve(el);
  });
}, { threshold: 0.5 });
counters.forEach(c => counterObs.observe(c));

// Cookie banner
const banner = document.getElementById('cookie-banner');
const COOKIE_KEY = 'nk_cookie_consent';
function loadAnalytics() {
  // Tu sa môžu spustiť GA / Pixel po súhlase
  if (window.gtag) gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'granted' });
}
if (banner) {
  const stored = localStorage.getItem(COOKIE_KEY);
  if (!stored) banner.hidden = false;
  else if (stored === 'accept') loadAnalytics();
  banner.querySelectorAll('[data-cookie]').forEach(btn => {
    btn.addEventListener('click', () => {
      localStorage.setItem(COOKIE_KEY, btn.dataset.cookie);
      banner.hidden = true;
      if (btn.dataset.cookie === 'accept') loadAnalytics();
    });
  });
}

// Form submit handler with Formspree-friendly UX
const form = document.querySelector('.contact-form');
form?.addEventListener('submit', async (ev) => {
  if (!form.action || form.action.includes('YOUR_FORM_ID')) {
    ev.preventDefault();
    alert('Formulár ešte nie je napojený. Doplň Formspree endpoint v index.html (action="...").');
    return;
  }
  ev.preventDefault();
  const data = new FormData(form);
  try {
    const res = await fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json' }
    });
    if (res.ok) {
      form.reset();
      alert('Ďakujeme! Ozveme sa vám čoskoro.');
      if (window.gtag) gtag('event', 'lead_submit');
      if (window.fbq) fbq('track', 'Lead');
    } else {
      alert('Niečo sa pokazilo. Skúste to prosím znova alebo nám napíšte na e-mail.');
    }
  } catch {
    alert('Nepodarilo sa odoslať. Skontrolujte internet a skúste znova.');
  }
});
