'use strict';

/* ===== SMOOTH SCROLL ===== */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const id = this.getAttribute('href');
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const headerH = document.getElementById('site-header').offsetHeight;
    const top = target.getBoundingClientRect().top + window.scrollY - headerH - 8;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

/* ===== HEADER SCROLL STATE ===== */
const header = document.getElementById('site-header');
function updateHeader() {
  header.classList.toggle('scrolled', window.scrollY > 40);
}
window.addEventListener('scroll', updateHeader, { passive: true });
updateHeader();

/* ===== MOBILE NAV TOGGLE ===== */
const navToggle = document.getElementById('nav-toggle');
const mainNav   = document.getElementById('main-nav');

navToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

mainNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  });
});

/* ===== INTERSECTION OBSERVER – SCROLL ANIMATIONS ===== */
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReduced) {
  document.querySelectorAll('.animate-on-scroll').forEach(el => el.classList.add('visible'));
} else {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
}

/* ===== CALCULATOR ===== */
const calcBtn       = document.getElementById('calc-btn');
const calcDataInput = document.getElementById('calc-data');
const calcSexo      = document.getElementById('calc-sexo');
const calcResultado = document.getElementById('calc-resultado');
const calcErro      = document.getElementById('calc-erro');

function showCalcError(msg) {
  calcErro.textContent = msg;
  calcErro.hidden = false;
  calcResultado.hidden = true;
}

function showCalcResult(html) {
  calcResultado.innerHTML = html;
  calcResultado.hidden = false;
  calcErro.hidden = true;
}

calcBtn.addEventListener('click', () => {
  calcResultado.hidden = true;
  calcErro.hidden = true;

  const rawDate = calcDataInput.value;
  if (!rawDate) {
    showCalcError('Por favor, informe a data da última doação.');
    return;
  }

  const data = new Date(rawDate + 'T00:00:00');
  if (isNaN(data.getTime())) {
    showCalcError('Data inválida. Verifique o valor informado.');
    return;
  }

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  if (data > hoje) {
    showCalcError('A data da última doação não pode ser no futuro.');
    return;
  }

  const dias = calcSexo.value === 'M' ? 60 : 90;
  const proxima = new Date(data);
  proxima.setDate(proxima.getDate() + dias);

  const fmt = d => d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  const diff = Math.ceil((proxima - hoje) / 86400000);

  let msg;
  if (diff > 0) {
    const plural = diff === 1 ? 'dia' : 'dias';
    msg = `Sua próxima doação pode ser a partir de <strong>${fmt(proxima)}</strong> (em ${diff} ${plural}).`;
  } else {
    msg = `Você já está apto(a) para doar! Sua data foi <strong>${fmt(proxima)}</strong>. `
        + `Que tal <a href="https://agenda.df.gov.br" target="_blank" rel="noopener noreferrer">agendar agora</a>?`;
  }

  showCalcResult(msg);
  calcResultado.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

/* Allow pressing Enter in date input */
calcDataInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') calcBtn.click();
});

/* ===== HIDE MOBILE CTA NEAR FOOTER ===== */
const mobileCta = document.querySelector('.mobile-cta-fixed');
if (mobileCta) {
  const footer = document.querySelector('.site-footer');
  const ctaObserver = new IntersectionObserver(entries => {
    mobileCta.style.opacity = entries[0].isIntersecting ? '0' : '1';
    mobileCta.style.pointerEvents = entries[0].isIntersecting ? 'none' : '';
  }, { threshold: 0.1 });
  ctaObserver.observe(footer);
}
