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
