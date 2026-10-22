/* Furry Pooch — interactions: paw cursor, click magic, scroll reveals, marquee, tilt, boop dog, booking form */
(() => {
  'use strict';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const rand = (a, b) => a + Math.random() * (b - a);
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const html = document.documentElement, body = document.body;
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const PHONE = '919940727027';
  const EMAIL = 'furrypooch2@gmail.com';
  const COLORS = ['#605ED0', '#4A2410', '#FF9ECB', '#F6C25B', '#FFF6DF', '#FFDE59'];
  const WORDS = ['woof!', 'boop!', 'arf arf!', 'bork!', 'zoomies!', 'good boy!', 'pawsome!', 'wag wag', 'treat?', 'sniff sniff', 'walkies?!', 'bestie!'];
  const sprite = id => `<svg viewBox="0 0 100 100" aria-hidden="true"><use href="#${id}"/></svg>`;

  html.classList.remove('no-js');
  body.classList.add('is-loading');

  /* ---------------- tiny fx factory ---------------- */
  function fx(cls, inner, x, y) {
    const e = document.createElement('div');
    e.className = 'fx ' + cls;
    e.innerHTML = inner;
    e.style.transform = `translate3d(${x}px,${y}px,0)`;
    document.body.appendChild(e);
    return e;
  }
  function play(el, frames, opts) {
    const a = el.animate(frames, Object.assign({ fill: 'forwards' }, opts));
    a.onfinish = () => el.remove();
    return a;
  }

  /* ---------------- preloader ---------------- */
  function ready() {
    if (body.classList.contains('is-ready')) return;
    $('#preloader').classList.add('done');
    body.classList.remove('is-loading');
    body.classList.add('is-ready');
    setTimeout(() => $('#preloader') && ($('#preloader').style.display = 'none'), 1400);
    initReveal();
  }
  const minWait = new Promise(r => setTimeout(r, reduce ? 200 : 1300));
  const loaded = new Promise(r => (document.readyState === 'complete' ? r() : addEventListener('load', r)));
  const safety = new Promise(r => setTimeout(r, 4500));
  Promise.race([Promise.all([minWait, loaded]), safety]).then(ready);

  /* ---------------- hero headline word stagger ---------------- */
  $$('.split').forEach((s, i) => s.style.setProperty('--i', i));

  /* ---------------- reveal on scroll ---------------- */
  const revealIO = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); revealIO.unobserve(e.target); }
  }), { threshold: 0.1, rootMargin: '0px 0px -5% 0px' }) : null;
  function observeReveal(items) { items.forEach(i => (revealIO ? revealIO.observe(i) : i.classList.add('in'))); }
  function initReveal() { observeReveal($$('.reveal:not(.in), .steps-trail:not(.in)')); }

  /* ---------------- pointer state ---------------- */
  let mx = innerWidth / 2, my = innerHeight / 2;
  let cx = mx, cy = my, lx = mx, ly = my;
  let moved = false, trailDist = 0, trailSide = 1, clicks = 0;
  let rot = -18, nx = 0, ny = 0, px = 0, py = 0;

  /* ---------------- paw cursor ---------------- */
  let cursor, label;
  if (fine) {
    html.classList.add('has-paw');
    cursor = document.createElement('div');
    cursor.className = 'paw-cursor';
    cursor.innerHTML = '<div class="paw-in"><svg viewBox="0 0 100 100"><use href="#paw"/></svg></div>';
    label = document.createElement('div');
    label.className = 'cursor-label';
    document.body.append(cursor, label);

    document.addEventListener('mouseover', e => {
      const t = e.target.closest('a,button,select,input,textarea,label,[data-tilt],[data-cursor],.nose,.pcard,.col-row');
      cursor.classList.toggle('hover', !!t);
      const c = e.target.closest('[data-cursor]');
      if (c) { label.textContent = c.dataset.cursor; label.classList.add('show'); }
      else label.classList.remove('show');
    });
    document.addEventListener('mouseleave', () => { cursor.classList.remove('on'); label.classList.remove('show'); });
    document.addEventListener('mouseenter', () => cursor.classList.add('on'));
    addEventListener('pointerdown', () => cursor.classList.add('down'));
    addEventListener('pointerup', () => cursor.classList.remove('down'));
  }

  addEventListener('pointermove', e => {
    mx = e.clientX; my = e.clientY;
    nx = mx / innerWidth - 0.5; ny = my / innerHeight - 0.5;
    if (!moved) { moved = true; cx = mx; cy = my; lx = mx; ly = my; }
    if (cursor) cursor.classList.add('on');
    if (fine && !reduce && body.classList.contains('is-ready')) {
      const dx = mx - lx, dy = my - ly, d = Math.hypot(dx, dy);
      trailDist += d; lx = mx; ly = my;
      if (trailDist > 70) {
        trailDist = 0;
        const a = Math.atan2(dy, dx);
        const ox = Math.cos(a + Math.PI / 2) * 11 * trailSide, oy = Math.sin(a + Math.PI / 2) * 11 * trailSide;
        trailSide *= -1;
        const deg = a * 180 / Math.PI + 90;
        const el = fx('trail', sprite('paw'), mx + ox, my + oy);
        el.firstChild.style.rotate = deg + 'deg';
        el.firstChild.style.fill = pick(['#605ED0', '#605ED0', '#4A2410']);
        play(el, [{ opacity: 0, scale: 0.4 }, { opacity: 0.55, scale: 1, offset: 0.12 }, { opacity: 0, scale: 0.85 }], { duration: 1300, easing: 'ease-out' });
      }
    }
  }, { passive: true });

  /* ---------------- CLICK MAGIC ---------------- */
  function burst(x, y, strong, kinds) {
    const types = kinds || ['paw', 'heart', 'bone', 'sparkle', 'paw'];
    // big paw stamp where you clicked
    const r = rand(-35, 35);
    const st = fx('stamp', sprite('paw'), x, y);
    st.firstChild.style.fill = pick(['#605ED0', '#4A2410', '#605ED0']);
    st.firstChild.style.filter = 'drop-shadow(2px 2px 0 rgba(255,246,223,.9))';
    play(st, [
      { opacity: 0, scale: 2.2, rotate: r + 'deg' },
      { opacity: 0.95, scale: 1, rotate: r + 'deg', offset: 0.16, easing: 'cubic-bezier(.34,1.56,.64,1)' },
      { opacity: 0.85, scale: 1, rotate: r + 'deg', offset: 0.6 },
      { opacity: 0, scale: 0.96, rotate: r + 'deg' }
    ], { duration: 1800 });
    if (reduce) return;

    // flying bits
    const n = strong ? 14 : 9;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + rand(-0.3, 0.3);
      const d = rand(60, strong ? 190 : 130);
      const dx = Math.cos(a) * d, dy = Math.sin(a) * d;
      const el = fx('bit', sprite(pick(types)), x, y);
      const s = el.firstChild;
      s.style.fill = pick(COLORS);
      s.style.filter = 'drop-shadow(1.5px 1.5px 0 #4A2410)';
      const sc = rand(0.8, strong ? 1.8 : 1.4), rr = rand(-200, 200);
      play(el, [
        { opacity: 0, translate: '0 0', scale: 0.1, rotate: '0deg' },
        { opacity: 1, translate: `${dx}px ${dy - 18}px`, scale: sc, rotate: rr + 'deg', offset: 0.55, easing: 'cubic-bezier(.15,.8,.3,1)' },
        { opacity: 0, translate: `${dx * 1.1}px ${dy + 46}px`, scale: sc * 0.5, rotate: rr * 1.4 + 'deg' }
      ], { duration: rand(800, 1200), easing: 'ease-out' });
    }

    // word pop
    const w = fx('word', pick(WORDS), clamp(x, 80, innerWidth - 80), clamp(y - 30, 40, innerHeight));
    const wr = rand(-10, 10);
    w.style.marginLeft = '-1.8em';
    play(w, [
      { opacity: 0, translate: '0 10px', scale: 0.3, rotate: wr + 'deg' },
      { opacity: 1, translate: '0 -26px', scale: 1.15, rotate: wr + 'deg', offset: 0.25, easing: 'cubic-bezier(.34,1.56,.64,1)' },
      { opacity: 1, translate: '0 -56px', scale: 1, rotate: wr + 'deg', offset: 0.7 },
      { opacity: 0, translate: '0 -90px', scale: 0.9, rotate: wr + 'deg' }
    ], { duration: 1300 });
  }

  function toast(text) {
    const t = document.createElement('div');
    t.className = 'toast'; t.textContent = text;
    document.body.appendChild(t);
    play(t, [
      { opacity: 0, scale: 0.2, rotate: '-14deg' },
      { opacity: 1, scale: 1.1, rotate: '-6deg', offset: 0.25, easing: 'cubic-bezier(.34,1.56,.64,1)' },
      { opacity: 1, scale: 1, rotate: '-6deg', offset: 0.75 },
      { opacity: 0, scale: 1.4, rotate: '-6deg' }
    ], { duration: 1500 });
  }

  function pawRain() {
    if (reduce) return;
    toast('ZOOMIES!');
    for (let i = 0; i < 34; i++) {
      const el = fx('rain', sprite(pick(['paw', 'paw', 'bone', 'heart'])), rand(0, innerWidth), -60);
      const s = el.firstChild;
      s.style.fill = pick(COLORS); s.style.filter = 'drop-shadow(2px 2px 0 #4A2410)';
      const sway = rand(-80, 80), rr = rand(-360, 360);
      play(el, [
        { translate: '0 0', rotate: '0deg', opacity: 1 },
        { translate: `${sway}px ${innerHeight + 140}px`, rotate: rr + 'deg', opacity: 1 }
      ], { duration: rand(1400, 2600), delay: rand(0, 900), easing: 'cubic-bezier(.4,0,.8,.6)' });
    }
  }

  addEventListener('pointerdown', e => {
    if (e.button !== 0 && e.pointerType === 'mouse') return;
    clicks++;
    const strong = !!e.target.closest('.btn,button,a,.nose');
    burst(e.clientX, e.clientY, strong);
    if (clicks % 10 === 0) pawRain();
  });

  /* ---------------- main RAF loop (cursor, parallax, marquee) ---------------- */
  const parallax = $$('[data-depth]');
  const marquees = $$('.marquee').map(m => ({ m, t: $('.m-track', m), speed: +m.dataset.speed, dir: +m.dataset.dir, p: 0, w: 0 }));
  function setupMarquee(o) {
    $$('.clone', o.t).forEach(c => c.remove());
    const kids = [...o.t.children];
    if (!kids.length) return;
    let w = 0;
    const first = kids[0];
    let sets = 0;
    do {
      kids.forEach(k => { const c = k.cloneNode(true); c.classList.add('clone'); o.t.appendChild(c); });
      sets++;
      const firstClone = $('.clone', o.t);
      w = firstClone.offsetLeft - first.offsetLeft;
    } while (o.t.scrollWidth < o.m.offsetWidth + w * 2 && sets < 6);
    o.w = w;
  }
  const setupAll = () => marquees.forEach(setupMarquee);
  setupAll();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(setupAll);
  let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(setupAll, 200); });

  let lastScroll = scrollY, vel = 0;
  const bar = $('#progressBar'), pawP = $('#progressPaw'), nav = $('#nav');
  const eyes = $$('.eye');
  const dogEl = $('#dog');

  function loop() {
    // cursor
    if (cursor) {
      cx += (mx - cx) * 0.28; cy += (my - cy) * 0.28;
      const vx = mx - cx;
      rot += ((-18 + clamp(vx * 1.1, -40, 40)) - rot) * 0.2;
      cursor.style.transform = `translate3d(${cx}px,${cy}px,0)`;
      cursor.style.setProperty('--rot', rot + 'deg');
      label.style.transform = `translate3d(${cx + 28}px,${cy + 22}px,0)`;
    }
    // parallax
    if (fine && !reduce) {
      px += (nx - px) * 0.08; py += (ny - py) * 0.08;
      for (const el of parallax) {
        const d = parseFloat(el.dataset.depth);
        el.style.transform = `translate3d(${px * d * -700}px,${py * d * -700}px,0)`;
      }
    }
    // scroll velocity + marquee
    const sy = scrollY; vel += ((sy - lastScroll) - vel) * 0.1; lastScroll = sy;
    if (!reduce) for (const o of marquees) {
      if (!o.w) continue;
      o.p += o.speed * (1.4 + Math.abs(vel) * 0.35);
      const mod = o.p % o.w;
      const x = o.dir < 0 ? -mod : -(o.w - mod);
      o.t.style.transform = `translate3d(${x}px,0,0)`;
    }
    // eyes follow
    if (dogEl && eyes.length) {
      const r = dogEl.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) {
        const k = 400 / r.width;
        for (const eye of eyes) {
          const c = eye.firstElementChild.getBoundingClientRect();
          const ex = c.left + c.width / 2, ey = c.top + c.height / 2;
          const dx = mx - ex, dy = my - ey, dist = Math.hypot(dx, dy) || 1;
          const m = Math.min(11, dist * k * 0.12);
          $('.pupil', eye).style.transform = `translate(${dx / dist * m}px,${dy / dist * m}px)`;
        }
      }
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  /* ---------------- scroll: progress bar + nav hide ---------------- */
  let lastY = 0;
  function onScroll() {
    const h = document.documentElement.scrollHeight - innerHeight;
    const p = h > 0 ? scrollY / h : 0;
    bar.style.width = (p * 100) + '%';
    pawP.style.left = (p * 100) + '%';
    const menuOpen = $('#menu').classList.contains('open');
    nav.classList.toggle('hide', scrollY > lastY && scrollY > 260 && !menuOpen);
    lastY = scrollY;
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------------- mobile menu ---------------- */
  const burger = $('#burger'), menu = $('#menu');
  let menuWasOpen = false;
  function setMenu(open) {
    menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    menu.setAttribute('aria-hidden', !open);
    if (open !== menuWasOpen) { menuWasOpen = open; lock(open); }
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  burger.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  $$('a', menu).forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  addEventListener('resize', () => { if (innerWidth > 1000) setMenu(false); });

  /* ---------------- magnetic buttons ---------------- */
  if (fine && !reduce) {
    $$('[data-magnet]').forEach(el => {
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        el.style.translate = `${(e.clientX - r.left - r.width / 2) * 0.22}px ${(e.clientY - r.top - r.height / 2) * 0.3}px`;
      });
      el.addEventListener('pointerleave', () => { el.style.translate = ''; });
    });

    /* ---------------- 3D tilt ---------------- */
    $$('[data-tilt]').forEach(el => {
      const max = +el.dataset.tiltMax || 8;
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = `perspective(900px) rotateX(${-y * max}deg) rotateY(${x * max}deg) translateZ(0)`;
        el.style.setProperty('--gx', (x + 0.5) * 100 + '%');
        el.style.setProperty('--gy', (y + 0.5) * 100 + '%');
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  /* ---------------- boop the dog ---------------- */
  const bubble = $('#bubble'), countEl = $('#boopCount');
  let boops = 0, bTimer, dTimer;
  if (dogEl) {
    dogEl.addEventListener('click', e => {
      const onNose = !!e.target.closest('#nose');
      dogEl.classList.remove('boop'); void dogEl.getBoundingClientRect(); dogEl.classList.add('boop');
      clearTimeout(dTimer); dTimer = setTimeout(() => dogEl.classList.remove('boop'), 1300);
      const msg = onNose ? pick(['boop!', 'woof!', 'eep!', 'hehe!', 'arf!']) : pick(['blep :P', 'huh?', 'hello!', 'wag wag']);
      bubble.textContent = msg; bubble.classList.add('show');
      clearTimeout(bTimer); bTimer = setTimeout(() => bubble.classList.remove('show'), 1200);
      if (onNose) {
        boops++; countEl.textContent = boops;
        burst(e.clientX, e.clientY, true, ['heart', 'heart', 'sparkle']);
        if (boops % 10 === 0) pawRain();
      }
    });
  }

  /* ============================================================
     SHOP: collections, filters, grid, quick view, My picks, lookbook, order helper
     ============================================================ */
  const P = window.FP_PRODUCTS || [], COLS = window.FP_COLLECTIONS || [], LB = window.FP_LOOKBOOK || [];
  const byCode = Object.fromEntries(P.map(p => [p.c, p]));
  const colName = Object.fromEntries(COLS.map(c => [c.key, c.name]));
  const photo = (c, alt) => `assets/products/${c}${alt ? '-b' : ''}.webp`;
  const esc = s => String(s).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  const tagOf = p => p.t || colName[p.k];
  const IG = 'https://ig.me/m/furry.pooch';

  /* ---- scroll lock shared by modal, drawer and menu ---- */
  let locks = 0;
  function lock(on) { locks = Math.max(0, locks + (on ? 1 : -1)); body.style.overflow = locks ? 'hidden' : ''; }

  /* ---- clipboard ---- */
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); return true; } catch (_) {}
    const t = document.createElement('textarea'); t.value = text; t.style.cssText = 'position:fixed;opacity:0;top:0';
    document.body.appendChild(t); t.select();
    let ok = false; try { ok = document.execCommand('copy'); } catch (_) {} t.remove(); return ok;
  }

  /* ---- My picks (kept in memory, remembered in this browser when allowed) ---- */
  let picks = [];
  try { picks = JSON.parse(localStorage.getItem('fp-picks') || '[]').filter(c => byCode[c]); } catch (_) {}
  const fab = $('#fab'), fabCount = $('#fabCount');
  const drawer = $('#drawer'), dList = $('#dList'), dEmpty = $('#dEmpty'), dCount = $('#dCount');
  const oCodes = $('#oCodes'), picksLine = $('#picksLine');
  let codesDirty = false;

  function savePicks() { try { localStorage.setItem('fp-picks', JSON.stringify(picks)); } catch (_) {} }
  function refreshPicks(bump) {
    savePicks();
    fabCount.textContent = picks.length; dCount.textContent = picks.length;
    fab.classList.toggle('has', picks.length > 0);
    if (bump) { fab.classList.remove('bump'); void fab.offsetWidth; fab.classList.add('bump'); }
    $$('.pick-btn').forEach(b => {
      const cs = b.dataset.pick.split(','), on = cs.every(c => picks.includes(c));
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
      b.setAttribute('aria-label', (on ? 'Remove ' : 'Add ') + cs.join(', ') + (on ? ' from' : ' to') + ' my picks');
    });
    dList.innerHTML = picks.map(c => { const p = byCode[c]; return `<li><img src="${photo(c)}" alt=""><div><b>${c}</b><span>${esc(p.n)}</span></div><button data-rm="${c}" aria-label="Remove ${c}" data-cursor="remove"><svg><use href="#close"/></svg></button></li>`; }).join('');
    dEmpty.hidden = picks.length > 0;
    $('#dGo').style.display = $('#dClear').style.display = picks.length ? '' : 'none';
    if (!codesDirty) oCodes.value = picks.join(', ');
    picksLine.textContent = picks.length ? 'Filled from My picks: ' + picks.map(c => byCode[c].n).join(', ') + '.' : '';
    syncOrder();
    if ($('#modal') && !$('#modal').hidden && modalCode) fillPickBtn();
  }
  function togglePick(codes, el) {
    const cs = String(codes).split(',');
    const adding = !cs.every(c => picks.includes(c));
    if (adding) {
      cs.forEach(c => { if (!picks.includes(c)) picks.push(c); });
      if (el) { const r = el.getBoundingClientRect(); burst(r.left + r.width / 2, r.top + r.height / 2, true, ['paw', 'heart', 'sparkle']); }
    } else picks = picks.filter(c => !cs.includes(c));
    refreshPicks(adding);
  }
  function openDrawer() { drawer.hidden = false; requestAnimationFrame(() => drawer.classList.add('open')); lock(true); $('.drawer-head button', drawer).focus(); }
  function closeDrawer() { drawer.classList.remove('open'); lock(false); setTimeout(() => { drawer.hidden = true; }, 350); fab.focus({ preventScroll: true }); }
  fab.addEventListener('click', openDrawer);
  drawer.addEventListener('click', e => {
    if (e.target.closest('[data-dclose]')) return closeDrawer();
    const rm = e.target.closest('[data-rm]'); if (rm) { picks = picks.filter(c => c !== rm.dataset.rm); refreshPicks(); }
  });
  $('#dClear').addEventListener('click', () => { picks = []; codesDirty = false; refreshPicks(); });
  $('#dGo').addEventListener('click', () => { closeDrawer(); });

  /* ---- collections index ---- */
  const colList = $('#colList');
  colList.innerHTML = COLS.map((c, i) => {
    const items = P.filter(p => p.k === c.key), n = items.length;
    const idx = n > 2 ? [0, Math.floor(n / 2), n - 1] : n === 2 ? [0, 1] : [0];
    const th = idx.map(k => `<img src="${photo(items[k].c)}" alt="" loading="lazy">`).join('');
    const range = c.from === c.to ? `FP${String(c.from).padStart(2, '0')}` : `FP${String(c.from).padStart(2, '0')}–FP${String(c.to).padStart(2, '0')}`;
    return `<li class="reveal" style="--d:${i * 0.05}s"><button class="col-row" data-col="${c.key}" data-cursor="browse"><span class="col-no">${String(i + 1).padStart(2, '0')}</span><span class="col-txt"><b>${esc(c.name)}</b><small>${esc(c.blurb)} · ${range}</small></span><span class="col-th">${th}</span><span class="col-pill">${n} ${n === 1 ? 'style' : 'styles'}</span></button></li>`;
  }).join('');
  colList.addEventListener('click', e => { const b = e.target.closest('[data-col]'); if (b) { setFilter(b.dataset.col); $('#shop').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); } });

  /* ---- filters + grid ---- */
  const fchips = $('#fchips'), grid = $('#grid'), qEl = $('#q'), shopCount = $('#shopCount'), emptyEl = $('#empty');
  let fcol = 'all', fq = '';
  fchips.innerHTML = [{ key: 'all', name: 'All', n: P.length }, ...COLS.map(c => ({ key: c.key, name: c.name, n: P.filter(p => p.k === c.key).length }))]
    .map(c => `<button class="fchip" data-f="${c.key}" aria-pressed="${c.key === 'all'}" data-cursor="filter">${esc(c.name)} <i>${c.n}</i></button>`).join('');
  fchips.addEventListener('click', e => { const b = e.target.closest('[data-f]'); if (b) setFilter(b.dataset.f); });
  qEl.addEventListener('input', () => { fq = qEl.value.trim().toLowerCase(); renderGrid(); });
  $('#clearF').addEventListener('click', () => { qEl.value = ''; fq = ''; setFilter('all'); });
  function setFilter(k) {
    fcol = k;
    $$('.fchip', fchips).forEach(b => b.setAttribute('aria-pressed', b.dataset.f === k));
    renderGrid();
  }
  function matches(p) {
    if (fcol !== 'all' && p.k !== fcol) return false;
    if (!fq) return true;
    let q = fq; const m = q.match(/^fp\s*-?\s*(\d{1,2})$/); if (m) q = 'fp' + m[1].padStart(2, '0');
    return (p.c + ' ' + p.n + ' ' + p.d + ' ' + tagOf(p) + ' ' + p.b.join(' ')).toLowerCase().includes(q);
  }
  let shown = P;
  function renderGrid() {
    shown = P.filter(matches);
    grid.innerHTML = shown.map((p, i) => `<li class="reveal" style="--d:${(i % 4) * 0.06}s">
      <article class="pcard">
        <button class="pimg" data-open="${p.c}" aria-label="View ${esc(p.n)}, ${p.c}" data-cursor="view">
          <img class="p-a" src="${photo(p.c)}" alt="${esc(p.n)}" loading="lazy" decoding="async" width="720" height="560">
          <img class="p-b" src="${photo(p.c, 1)}" alt="" loading="lazy" decoding="async" width="520" height="520">
          <span class="code">${p.c}</span>
        </button>
        <button class="pick-btn" data-pick="${p.c}" aria-pressed="false" data-cursor="add!"><svg><use href="#paw"/></svg></button>
        <div class="pbody"><span class="tag">${esc(tagOf(p))}</span><h3>${esc(p.n)}</h3><p>${esc(p.d)}</p></div>
      </article></li>`).join('');
    emptyEl.hidden = shown.length > 0;
    const label = fcol === 'all' ? 'all collections' : colName[fcol];
    shopCount.textContent = `Showing ${shown.length} ${shown.length === 1 ? 'style' : 'styles'} · ${label}` + (fq ? ` · “${qEl.value.trim()}”` : '');
    refreshPicks();
    observeReveal($$('.reveal:not(.in)', grid));
  }
  grid.addEventListener('click', e => {
    const o = e.target.closest('[data-open]'); if (o) return openModal(o.dataset.open, shown, o);
    const b = e.target.closest('[data-pick]'); if (b) togglePick(b.dataset.pick, b);
  });

  /* ---- quick view modal ---- */
  const modal = $('#modal'), mImg = $('#mImg'), mThumbs = $('#mThumbs');
  let modalCode = null, modalList = P, modalOpener = null, modalView = 0;
  function showView(v) {
    modalView = v;
    mImg.src = photo(modalCode, v === 1);
    $$('button', mThumbs).forEach((b, i) => b.setAttribute('aria-pressed', i === v));
  }
  function fillModal(code) {
    const p = byCode[code]; modalCode = code;
    $('#mCode').textContent = code; $('#mTag').textContent = tagOf(p); $('#mName').textContent = p.n; $('#mDesc').textContent = p.d;
    $('#mList').innerHTML = p.b.map(x => `<li><svg><use href="#paw"/></svg>${esc(x)}</li>`).join('');
    mImg.alt = p.n;
    mThumbs.innerHTML = [0, 1].map(i => `<button data-v="${i}" aria-label="${i ? 'Flat-lay or detail' : 'On a pet'}" aria-pressed="false"><img src="${photo(code, i === 1)}" alt=""></button>`).join('');
    showView(0); fillPickBtn();
    $('#mHint').textContent = 'We copy the message so you can paste it in the DM.';
  }
  function fillPickBtn() {
    const on = picks.includes(modalCode), b = $('#mPick');
    b.innerHTML = `<svg><use href="#paw"/></svg>${on ? 'In my picks · remove' : 'Add to my picks'}`;
    b.classList.toggle('is-on', on);
  }
  function openModal(code, list, opener) {
    modalList = list && list.length ? list : P; modalOpener = opener || null;
    fillModal(code); modal.hidden = false; requestAnimationFrame(() => modal.classList.add('open')); lock(true);
    $('.modal-x', modal).focus();
  }
  function closeModal() { modal.classList.remove('open'); lock(false); setTimeout(() => { modal.hidden = true; }, 300); if (modalOpener && modalOpener.focus) modalOpener.focus({ preventScroll: true }); }
  function stepModal(d) {
    let i = modalList.findIndex(p => p.c === modalCode);
    if (i < 0) i = 0;
    fillModal(modalList[(i + d + modalList.length) % modalList.length].c);
    const card = $('#modalCard'); card.classList.remove('swap'); void card.offsetWidth; card.classList.add('swap');
  }
  modal.addEventListener('click', e => {
    if (e.target.closest('[data-close]')) return closeModal();
    const v = e.target.closest('[data-v]'); if (v) showView(+v.dataset.v);
  });
  $('#mPrev').addEventListener('click', () => stepModal(-1));
  $('#mNext').addEventListener('click', () => stepModal(1));
  $('#mPick').addEventListener('click', e => togglePick(modalCode, e.currentTarget));
  $('#mIg').addEventListener('click', async () => {
    const p = byCode[modalCode];
    const ok = await copyText(`Hi Furry Pooch! 🐾 I'd like to order ${p.c} ${p.n}. My pet's size: `);
    $('#mHint').textContent = ok ? 'Copied! Paste it in the Instagram chat and add your pet\'s size.' : 'Message @furry.pooch with the code ' + p.c + '.';
  });
  addEventListener('keydown', e => {
    if (!modal.hidden) {
      if (e.key === 'Escape') closeModal();
      else if (e.key === 'ArrowRight') stepModal(1);
      else if (e.key === 'ArrowLeft') stepModal(-1);
      else if (e.key === 'Tab') {
        const f = $$('button:not([disabled]),a[href]', $('#modalCard')).filter(x => x.offsetParent !== null);
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    } else if (!drawer.hidden && e.key === 'Escape') closeDrawer();
  });

  /* ---- lookbook ---- */
  const lbTrack = $('#lbTrack');
  lbTrack.innerHTML = LB.map(l => {
    const p = byCode[l.c], all = [l.c, ...(l.also || [])];
    const badge = all.length > 1 ? `${all[0]}–${all[all.length - 1].slice(2)}` : l.c;
    const name = l.title || p.n;
    return `<figure class="lb-card"><button class="lb-img" data-open="${l.c}" aria-label="View ${esc(name)}, ${badge}" data-cursor="view"><img src="${l.img}" alt="Lookbook collage: ${esc(name)} on dogs and cats, with fabric and stitching close-ups" loading="lazy" width="${l.w}" height="${l.h}" style="aspect-ratio:${l.w}/${l.h}"></button>
      <figcaption><span class="code">${badge}</span><div><b>${esc(name)}</b><small>${esc(l.note)}</small></div><button class="pick-btn" data-pick="${all.join(',')}" aria-pressed="false" data-cursor="add!"><svg><use href="#paw"/></svg></button></figcaption></figure>`;
  }).join('');
  lbTrack.addEventListener('click', e => {
    const o = e.target.closest('[data-open]'); if (o) return openModal(o.dataset.open, LB.map(l => byCode[l.c]), o);
    const b = e.target.closest('[data-pick]'); if (b) togglePick(b.dataset.pick, b);
  });
  const lbStep = d => { const c = $('.lb-card', lbTrack); lbTrack.scrollBy({ left: d * (c ? c.offsetWidth + 24 : 400), behavior: reduce ? 'auto' : 'smooth' }); };
  $('#lbPrev').addEventListener('click', () => lbStep(-1));
  $('#lbNext').addEventListener('click', () => lbStep(1));
  lbTrack.addEventListener('keydown', e => { if (e.key === 'ArrowRight') lbStep(1); if (e.key === 'ArrowLeft') lbStep(-1); });
  // drag to scroll with a mouse
  (() => {
    let down = false, sx = 0, sl = 0, moved2 = 0;
    lbTrack.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = lbTrack.scrollLeft; moved2 = 0; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved2 = Math.max(moved2, Math.abs(dx)); lbTrack.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { down = false; });
    lbTrack.addEventListener('click', e => { if (moved2 > 6) { e.stopPropagation(); e.preventDefault(); } }, true);
  })();

  /* ---- order helper ---- */
  const form = $('#bookForm'), errEl = $('#formErr'), igBtn = $('#igBtn'), waBtn = $('#waBtn'), hint = $('#formHint');
  const oName = $('#oName'), oPet = $('#oPet'), oNote = $('#oNote');
  function parseCodes(v) {
    const found = [...v.matchAll(/fp\s*-?\s*(\d{1,2})/gi)].map(m => 'FP' + m[1].padStart(2, '0'));
    return [...new Set(found)];
  }
  function orderMessage() {
    const raw = oCodes.value.trim(), codes = parseCodes(raw);
    const items = codes.length ? codes.map(c => byCode[c] ? `${c} ${byCode[c].n}` : c) : (raw ? [raw] : []);
    const pet = oPet.value.trim(), note = oNote.value.trim(), name = oName.value.trim();
    return `Hi Furry Pooch! 🐾 I'd like to order: ${items.length ? items.join(', ') : '…'}.` + (pet ? ` For my pet: ${pet}.` : '') + (note ? ` Note: ${note}.` : '') + (name ? ` Thanks, ${name}` : '');
  }
  function syncOrder() { if (waBtn) waBtn.href = `https://wa.me/${PHONE}?text=${encodeURIComponent(orderMessage())}`; }
  function validOrder() {
    const okName = !!oName.value.trim(), okCodes = !!oCodes.value.trim();
    oName.classList.toggle('err', !okName); oCodes.classList.toggle('err', !okCodes);
    errEl.textContent = okName && okCodes ? '' : 'Please add your name and at least one product code, like FP07 🐾';
    return okName && okCodes;
  }
  oCodes.addEventListener('input', () => { codesDirty = oCodes.value.trim() !== ''; });
  form.addEventListener('input', e => { e.target.classList.remove('err'); syncOrder(); });
  form.addEventListener('submit', e => e.preventDefault());
  igBtn.addEventListener('click', async e => {
    if (!validOrder()) { e.preventDefault(); return; }
    const ok = await copyText(orderMessage());
    hint.textContent = ok ? 'Copied! Paste it into your chat with @furry.pooch.' : 'Message @furry.pooch with your codes and pet size.';
    if (ok) toast('COPIED!');
  });
  waBtn.addEventListener('click', e => { syncOrder(); if (!validOrder()) e.preventDefault(); else toast('WOOF!'); });
  $('#copyBtn').addEventListener('click', async () => {
    if (!validOrder()) return;
    const ok = await copyText(orderMessage());
    hint.innerHTML = ok ? 'Copied! Paste it in an Instagram DM to <b>@furry.pooch</b>, or text <b>+91 99407 27027</b>.' : 'Select and copy this: <b></b>';
    if (!ok) hint.querySelector('b').textContent = orderMessage(); else toast('COPIED!');
  });

  renderGrid();

  /* ---------------- in-page links (reliable inside a sandboxed frame) ---------------- */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const t = id ? document.getElementById(id) : null;
    if (id && !t) return;
    e.preventDefault();
    if (!t || id === 'top') scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    else t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  });

  /* ---------------- footer ---------------- */
  $('#year').textContent = new Date().getFullYear();
  $('#toTop').addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));
})();
