// utils.js - helper functions for Django Bus Booking App
// (localStorage replaced with Django session/API calls)

function showToast(msg, type = 'success') {
  const old = document.querySelector('.toast');
  if (old) old.remove();

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = msg;
  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

function formatDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  return d.toLocaleDateString('en-IN', options);
}

function formatCurrency(amount) {
  return '₹' + Number(amount).toLocaleString('en-IN');
}

// CSRF token helper for Django POST requests
function getCsrfToken() {
  const el = document.querySelector('[name=csrfmiddlewaretoken]');
  if (el) return el.value;
  // Try cookie
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

async function apiPost(url, data) {
  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify(data),
  });
  return resp.json();
}

async function apiGet(url) {
  const resp = await fetch(url);
  return resp.json();
}

// generate a simple QR code SVG (same as original)
function generateQRCode(text) {
  const size = 120;
  const cells = 10;
  const cellSize = size / cells;
  let rects = '';

  let seed = 0;
  for (let i = 0; i < text.length; i++) seed += text.charCodeAt(i);

  function seededRandom(s) {
    const x = Math.sin(s) * 10000;
    return x - Math.floor(x);
  }

  for (let r = 0; r < cells; r++) {
    for (let c = 0; c < cells; c++) {
      const isCorner = (r < 3 && c < 3) || (r < 3 && c >= cells - 3) || (r >= cells - 3 && c < 3);
      const shouldFill = isCorner ? true : seededRandom(seed + r * cells + c) > 0.5;
      if (shouldFill) {
        rects += `<rect x="${c * cellSize}" y="${r * cellSize}" width="${cellSize}" height="${cellSize}" fill="black"/>`;
      }
    }
  }

  return `<svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg" style="border:4px solid white;background:white">
    ${rects}
  </svg>`;
}

const CITIES = [
  'Bhubaneswar', 'Kolkata', 'Puri', 'Cuttack', 'Visakhapatnam',
  'Hyderabad', 'Chennai', 'Mumbai', 'Delhi', 'Bangalore',
  'Patna', 'Ranchi', 'Rourkela', 'Sambalpur', 'Berhampur'
];

function setupAutocomplete(inputId, listId) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);
  if (!input || !list) return;

  input.addEventListener('input', function () {
    const val = this.value.toLowerCase();
    list.innerHTML = '';
    if (!val) { list.style.display = 'none'; return; }

    const matches = CITIES.filter(c => c.toLowerCase().startsWith(val));
    if (matches.length === 0) { list.style.display = 'none'; return; }

    matches.forEach(city => {
      const li = document.createElement('li');
      li.textContent = city;
      li.onclick = () => {
        input.value = city;
        list.style.display = 'none';
      };
      list.appendChild(li);
    });
    list.style.display = 'block';
  });

  document.addEventListener('click', e => {
    if (!input.contains(e.target)) list.style.display = 'none';
  });
}

// Hamburger + scroll-to-top (same as original)
document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('nav');
  if (nav && !nav.querySelector('.hamburger')) {
    const hb = document.createElement('button');
    hb.className = 'hamburger';
    hb.setAttribute('aria-label', 'Toggle menu');
    hb.innerHTML = '<span></span><span></span><span></span>';
    hb.addEventListener('click', () => {
      hb.classList.toggle('open');
      const nr = document.getElementById('nav-right');
      if (nr) nr.classList.toggle('open');
    });
    const nr = document.getElementById('nav-right');
    if (nr) nav.insertBefore(hb, nr);
  }

  if (!document.getElementById('scroll-top')) {
    const btn = document.createElement('button');
    btn.id = 'scroll-top';
    btn.title = 'Back to top';
    btn.textContent = '↑';
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 300);
    });
  }
});
