// [PENDING] Contact email: choose between sarahsaafwan@gmail.com and
// sarahsafwan.creates@gmail.com. Changing this one line updates every page.
const EMAIL = 'sarahsaafwan@gmail.com';

const root = document.documentElement;
root.classList.add('js');

// Draft view: add ?draft to any URL to see content still awaiting a decision.
if (new URLSearchParams(location.search).has('draft')) {
  root.classList.add('draft');
  document.querySelectorAll('a[href$=".html"], a[href*=".html#"]').forEach((a) => {
    const url = new URL(a.href, location.href);
    if (url.origin === location.origin) {
      url.searchParams.set('draft', '');
      a.href = url.href;
    }
  });
}

document.querySelectorAll('[data-email]').forEach((el) => {
  if (el.tagName === 'A') el.href = 'mailto:' + EMAIL;
  if (!el.textContent.trim()) el.textContent = EMAIL;
});

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Mobile navigation
const toggle = document.querySelector('.nav-toggle');
const navList = document.getElementById('nav-list');
if (toggle && navList) {
  toggle.addEventListener('click', () => {
    const open = navList.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  });
}

// Subtle fade-in on scroll
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('in'));
}

// CV: "Download PDF" opens the print dialog, where the visitor saves as PDF.
const printBtn = document.getElementById('print-cv');
if (printBtn) printBtn.addEventListener('click', () => window.print());

// Contact form: opens the visitor's email app with the message filled in.
const form = document.getElementById('contact-form');
if (form) {
  const service = new URLSearchParams(location.search).get('service');
  if (service && form.topic) {
    const match = [...form.topic.options].find((o) => o.value === service);
    if (match) form.topic.value = service;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const subject = `${data.get('topic')}: ${data.get('name')}`;
    const body = [
      data.get('message'),
      '',
      `${data.get('name')}`,
      data.get('company') ? `${data.get('company')}` : '',
      `${data.get('email')}`,
    ].filter((line, i) => i < 2 || line).join('\n');
    location.href = `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
}
