(function () {
  'use strict';

  /* ---- Thème jour/nuit (clair par défaut) ---- */
  var root = document.documentElement;
  if (localStorage.getItem('sylvia-theme') === 'dark') {
    root.setAttribute('data-theme', 'dark');
  }
  window.toggleTheme = function () {
    var isDark = root.getAttribute('data-theme') === 'dark';
    if (isDark) {
      root.removeAttribute('data-theme');
      localStorage.setItem('sylvia-theme', 'light');
    } else {
      root.setAttribute('data-theme', 'dark');
      localStorage.setItem('sylvia-theme', 'dark');
    }
    syncThemeButton();
  };
  function syncThemeButton() {
    var btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
  }

  document.addEventListener('DOMContentLoaded', function () {
    syncThemeButton();

    /* ---- Menu hamburger ---- */
    var nav = document.querySelector('.nav');
    var navToggle = document.querySelector('.nav__toggle');
    var navLinks = document.querySelectorAll('.nav__link');

    if (navToggle && nav) {
      navToggle.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('nav--open');
        navToggle.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav && nav.classList.contains('nav--open')) {
        nav.classList.remove('nav--open');
        if (navToggle) { navToggle.setAttribute('aria-expanded', 'false'); navToggle.focus(); }
        document.body.style.overflow = '';
      }
    });

    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.forEach(function (link) {
      if (link.getAttribute('href') === currentPage) {
        link.classList.add('nav__link--active');
      }
      link.addEventListener('click', function () {
        if (nav) {
          nav.classList.remove('nav--open');
          if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        }
      });
    });
  });

  /* ---- Recherche globale ---- */
  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('searchInput');
    var out = document.getElementById('searchResults');
    if (!input || !out) return;
    var data = [];
    function norm(t) { return t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
    function esc(t) { return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function render() {
      var q = norm(input.value.trim());
      if (!q) { out.innerHTML = ''; return; }
      var html = '';
      data.forEach(function (page) {
        var hits = page.extraits.filter(function (e) { return norm(e).indexOf(q) !== -1; });
        if (norm(page.titre).indexOf(q) === -1 && !hits.length) return;
        html += '<div class="search__item"><a href="' + esc(page.url) + '">' + esc(page.titre) + '</a>';
        (hits.length ? hits : page.extraits.slice(0, 1)).slice(0, 3).forEach(function (e) {
          html += '<p>' + esc(e) + '</p>';
        });
        html += '</div>';
      });
      out.innerHTML = html || '<p>Aucun résultat.</p>';
    }
    fetch('data/search.json').then(function (r) { return r.json(); }).then(function (d) {
      data = d; render();
    }).catch(function () { out.innerHTML = '<p>Index de recherche indisponible.</p>'; });
    input.addEventListener('input', render);
  });
})();
