/* ═══════════════════════════════════════════
   GLOBUSNET — globusnet.org — Layout Injector
   ═══════════════════════════════════════════ */

const NAV_HTML = `
<nav id="main-nav">
  <a href="index.html" class="nav-logo">Globus<span>Net</span></a>
  <ul class="nav-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="pages/report-a-scam.html">Report a Scam</a></li>
    <li><a href="pages/crypto-scams.html">Crypto Forensics</a></li>
    <li><a href="pages/coinbase-support.html">Coinbase Support</a></li>
    <li><a href="reviews/index.html">Broker Reviews</a></li>
    <li><a href="pages/timeshare-exit.html">Timeshare Exit</a></li>
    <li><a href="de/index.html">🇩🇪 Deutsch</a></li>
    <li><a href="pages/contact.html" class="nav-cta">Get Help</a></li>
  </ul>
  <div class="nav-hamburger" id="hamburger">
    <span></span><span></span><span></span>
  </div>
</nav>
<div class="mobile-overlay" id="mobile-overlay">
  <button class="mobile-close" id="mobile-close">✕</button>
  <nav class="mobile-nav">
    <a href="index.html">Home</a>
    <a href="pages/report-a-scam.html">Report a Scam</a>
    <a href="pages/how-to-report-a-scam.html">How to Report</a>
    <a href="pages/crypto-scams.html">Crypto On-Chain Forensics</a>
    <a href="pages/coinbase-support.html">Coinbase Support Guide</a>
    <a href="pages/private-investigator.html">Private Investigators</a>
    <a href="reviews/index.html">Broker Reviews</a>
    <a href="pages/timeshare-exit.html">Timeshare Exit</a>
    <a href="de/index.html">🇩🇪 Betrug melden</a>
    <a href="pages/contact.html" class="mobile-cta">Get Help</a>
  </nav>
</div>`;

const FOOTER_HTML = `
<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="index.html" class="nav-logo">Globus<span>Net</span></a>
      <p>Report fraud. Report a scam. On-chain crypto forensics and licensed investigators worldwide. Free consultation. Action Fraud, FTC, BaFin and 50+ reporting authorities covered.</p>
      <div class="footer-badge">Free Consultation · On-Chain Forensics · 50+ Countries</div>
    </div>
    <div class="footer-col">
      <h4>Report</h4>
      <ul>
        <li><a href="pages/report-a-scam.html">Report a Scam</a></li>
        <li><a href="pages/how-to-report-a-scam.html">How to Report a Scam</a></li>
        <li><a href="pages/report-scam-website.html">Report a Scam Website</a></li>
        <li><a href="pages/action-fraud.html">Action Fraud (UK)</a></li>
        <li><a href="pages/federal-trade-commission.html">FTC Report Fraud (US)</a></li>
        <li><a href="pages/fraud-authorities.html">All Global Authorities</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      <ul>
        <li><a href="pages/crypto-scams.html">Crypto On-Chain Forensics</a>
    <a href="pages/coinbase-support.html">Coinbase Support Guide</a></li>
        <li><a href="pages/private-investigator.html">Private Investigators</a></li>
        <li><a href="pages/timeshare-exit.html">Timeshare Exit</a></li>
        <li><a href="pages/investment-fraud.html">Investment Fraud</a></li>
        <li><a href="pages/pig-butchering-scam.html">Pig Butchering Scam</a></li>
        <li><a href="reviews/index.html">Broker Reviews</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Deutsch</h4>
      <ul>
        <li><a href="de/index.html">Startseite (DE)</a></li>
        <li><a href="de/betrug-melden.html">Betrug melden</a></li>
        <li><a href="de/krypto-betrug.html">Krypto-Betrug</a></li>
        <li><a href="pages/faq.html">FAQ</a></li>
        <li><a href="pages/about.html">About</a></li>
        <li><a href="pages/contact.html">Get Help Now</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 GlobusNet. All rights reserved. Not legal or financial advice.</p>
    <p>Consultation is free. Not legal or financial advice.</p>
  </div>
</footer>`;

/* ─── PATH RESOLVER (works from any subfolder depth) ─── */
function resolvePath(href) {
  const depth = (window.location.pathname.match(/\//g) || []).length - 1;
  if (depth <= 0) return href;
  return '../'.repeat(depth) + href;
}

function resolveNav(html) {
  return html.replace(/href="([^"#]+)"/g, (match, p1) => {
    if (p1.startsWith('http') || p1.startsWith('#')) return match;
    return `href="${resolvePath(p1)}"`;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  /* ─── INJECT NAV + FOOTER ─── */
  const navEl = document.getElementById('nav-placeholder');
  const footerEl = document.getElementById('footer-placeholder');
  if (navEl) navEl.outerHTML = resolveNav(NAV_HTML);
  if (footerEl) footerEl.outerHTML = resolveNav(FOOTER_HTML);

  /* ─── NAV SCROLL EFFECT ─── */
  const nav = document.getElementById('main-nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 50);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ─── MOBILE MENU ─── */
  const hamburger = document.getElementById('hamburger');
  const overlay = document.getElementById('mobile-overlay');
  const closeBtn = document.getElementById('mobile-close');
  if (hamburger && overlay) {
    hamburger.addEventListener('click', () => overlay.classList.add('open'));
    closeBtn?.addEventListener('click', () => overlay.classList.remove('open'));
    overlay.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => overlay.classList.remove('open'))
    );
  }

  /* ─── SCROLL REVEAL ─── */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    reveals.forEach(el => io.observe(el));
  }

  /* ─── FAQ ACCORDION ─── */
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ─── FORM SUBMIT ─── */
  document.querySelectorAll('form[data-fraudshield]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('[type=submit]');
      const orig = btn.textContent;
      btn.textContent = 'Received — we\'ll contact you within 24h';
      btn.disabled = true;
      btn.style.opacity = '0.7';
    });
  });

  /* ─── CARD HOVER MAGNETIC GLOW ─── */
  document.querySelectorAll('.service-card, .glass-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width * 100).toFixed(1);
      const y = ((e.clientY - r.top) / r.height * 100).toFixed(1);
      card.style.setProperty('--mx', x + '%');
      card.style.setProperty('--my', y + '%');
    });
  });
});
