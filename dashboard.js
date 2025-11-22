// dashboard.js — Чистый, современный, без багов (2025 edition)

const results = document.getElementById('results');
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menuToggle');
const toTopBtn = document.getElementById('toTop');

// Поиск: оба поля
const searchInputDesktop = document.getElementById('searchInput');
const searchInputMobile = document.getElementById('searchInputMobile');
const searchInputs = [searchInputDesktop, searchInputMobile].filter(Boolean);

let currentFilter = 'all';        // 'all' | 'acc' | 'no'
let currentSearchTerm = '';

// === СИНХРОНИЗАЦИЯ ПОИСКА ===
function handleSearch(e) {
  currentSearchTerm = e.target.value.trim().toLowerCase();
  // Синхронизируем оба поля
  searchInputs.forEach(i => i.value = e.target.value);
  applyFilterAndSearch();
}

searchInputs.forEach(input => {
  input.addEventListener('input', handleSearch);
});

function render(list) {
  if (!list || list.length === 0) {
    results.innerHTML = '<p style="text-align:center;color:#aaa;padding:120px 20px;font-size:20px;">Ничего не найдено</p>';
    return;
  }

  results.innerHTML = list.map(c => `
    <div class="card">
      <h3>${c.name}</h3>
      
      <p style="font-size: 1.48rem; margin: 14px 0 8px;"><strong>ИНН:</strong> ${c.inn}</p>
      <p style="font-size: 1.48rem; margin: 8px 0;"><strong>Город:</strong> ${c.city}</p>
      <p style="font-size: 1.48rem; margin: 12px 0 20px;">
        <strong>${c.phone || '+7 (___) ___-__-__'}</strong>
      </p>
      
      <span class="tag ${c.accredited ? 'acc' : 'no'}">
        ${c.accredited ? 'Аккредитована' : 'Не аккредитована'}
      </span>
    </div>
  `).join('');
}
// === ОБНОВЛЕНИЕ СЧЁТЧИКОВ В КНОПКАХ ===
function updateCounters() {
  const total = companies.length;
  const accredited = companies.filter(c => c.accredited).length;
  const notAccredited = total - accredited;

  document.getElementById('countAll').textContent = total;
  document.getElementById('countAcc').textContent = accredited;
  document.getElementById('countNo').textContent = notAccredited;
}

// === ФИЛЬТР + ПОИСК ===
function applyFilterAndSearch() {
  let filtered = [...companies];

  // Фильтр по аккредитации
  if (currentFilter === 'acc') {
    filtered = filtered.filter(c => c.accredited);
  } else if (currentFilter === 'no') {
    filtered = filtered.filter(c => !c.accredited);
  }

  // Поиск
  if (currentSearchTerm) {
    filtered = filtered.filter(c =>
      c.name.toLowerCase().includes(currentSearchTerm) ||
      c.inn.includes(currentSearchTerm) ||
      c.city.toLowerCase().includes(currentSearchTerm)
    );
  }

  render(filtered);
  updateCounters(); // Обновляем цифры в кнопках
}

// === ЗАПУСК ===
document.addEventListener('DOMContentLoaded', () => {
  // Первичная загрузка
  updateCounters();
  render(companies);

  // === ГЛАВНЫЕ КНОПКИ ФИЛЬТРОВ (сверху) ===
  document.querySelectorAll('.main-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      // Снимаем активность со всех
      document.querySelectorAll('.main-filter-btn').forEach(b => b.classList.remove('active'));
      // Активируем текущую
      btn.classList.add('active');
      // Применяем фильтр
      currentFilter = btn.dataset.filter;
      applyFilterAndSearch();
    });
  });

  // === БУРГЕР-МЕНЮ ===
  menuToggle?.addEventListener('click', e => {
    e.stopPropagation();
    sidebar.classList.toggle('open');
    menuToggle.classList.toggle('active');
  });

  document.querySelector('.close-sidebar')?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    menuToggle.classList.remove('active');
  });

  document.addEventListener('click', e => {
    if (sidebar.classList.contains('open') && 
        !sidebar.contains(e.target) && 
        e.target !== menuToggle && 
        !e.target.closest('.menu-toggle')) {
      sidebar.classList.remove('open');
      menuToggle.classList.remove('active');
    }
  });

  // === НАВБАР + КНОПКА НАВЕРХ ===
  window.addEventListener('scroll', () => {
    document.querySelector('nav').classList.toggle('scrolled', window.scrollY > 50);
    toTopBtn.style.opacity = window.scrollY > 600 ? '1' : '0';
    toTopBtn.style.transform = window.scrollY > 600 ? 'scale(1)' : 'scale(0.8)';
  });

  toTopBtn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // === АНИМАЦИЯ КАРТОЧЕК ===
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  const observeCards = () => {
    document.querySelectorAll('#results .card').forEach(card => {
      card.classList.remove('visible');
      observer.observe(card);
    });
  };

  // Перезапускаем анимацию после каждого рендера
  const originalRender = render;
  render = function(list) {
    originalRender(list);
    setTimeout(observeCards, 100);
  };

  // Первичная анимация
  observeCards();
});