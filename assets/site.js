/* Bibelstudium-Ecke – kleine Helfer für die statische Website (Themes, Suche, Bibelstellen). */
(function () {
  'use strict';
  var root = document.documentElement.dataset.root || '';
  var KEY = 'bse.einstellungen';
  var S = {};
  try { S = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { S = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { } }
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  /* ---------- Darstellung ---------- */
  var panel = $('#settings');
  var FONTS = { serif: '"Noto Serif",Georgia,serif', sans: '"Noto Sans",Arial,sans-serif', atkinson: '"Atkinson Hyperlegible",Verdana,sans-serif', garamond: '"EB Garamond","Noto Serif",Georgia,serif' };
  var TOGGLES = ['hideOff', 'noNum', 'versweise', 'zweispaltig', 'weit', 'lesezeile', 'fokus'];
  var darkMQ = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
  // „auto“ und „jahreszeit“ werden zur Laufzeit in ein echtes Theme übersetzt
  function resolveTheme(t) {
    t = t || 'standard';
    if (t === 'auto') return darkMQ && darkMQ.matches ? 'nacht' : 'standard';
    if (t === 'jahreszeit') { var m = new Date().getMonth(); return (m === 11 || m < 2) ? 'winter' : m < 5 ? 'fruehling' : m < 8 ? 'sommer' : 'herbst'; }
    return t;
  }
  function setVar(name, val) { var h = document.documentElement; if (val == null || val === '') h.style.removeProperty(name); else h.style.setProperty(name, val); }
  function apply() {
    var h = document.documentElement;
    h.dataset.theme = resolveTheme(S.theme);
    setVar('--fs', S.fs ? S.fs + 'px' : null);
    setVar('--lh', S.lh || null);
    setVar('--measure', S.measure ? S.measure + 'ch' : null);
    setVar('--font-read-user', FONTS[S.fontRead] || null);
    TOGGLES.forEach(function (k) { h.classList.toggle(k, !!S[k]); });
    $$('[data-theme-set]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeSet === (S.theme || 'standard'))); });
    $$('[data-num]').forEach(function (r) { r.value = S[r.dataset.num] || r.dataset.def; r.nextElementSibling.textContent = r.dataset.num === 'fs' ? r.value + ' px' : r.dataset.num === 'measure' ? r.value + ' Z.' : r.value; });
    $$('[data-toggle]').forEach(function (c) { c.checked = !!S[c.dataset.toggle]; });
    var fsel = $('[data-font]'); if (fsel) fsel.value = S.fontRead || '';
    updateRuler();
  }
  if (darkMQ && darkMQ.addEventListener) darkMQ.addEventListener('change', function () { if (S.theme === 'auto') apply(); });
  // zusätzlich beim Zurückkehren ins Fenster prüfen (Windows-Wechsel hell/dunkel, neuer Monat bei „Jahreszeit“)
  function recheck() { if (S.theme === 'auto' || S.theme === 'jahreszeit') apply(); }
  window.addEventListener('focus', recheck);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) recheck(); });
  $$('[data-open-settings]').forEach(function (b) { b.addEventListener('click', function () {
    var cur = S.theme || 'standard';   // Gruppe mit dem aktiven Theme aufklappen
    $$('.tgroup').forEach(function (d) { if ((' ' + d.dataset.keys + ' ').indexOf(' ' + cur + ' ') !== -1) d.open = true; });
    panel.hidden = false; $('[data-close-settings]').focus(); }); });
  $$('[data-close-settings]').forEach(function (b) { b.addEventListener('click', function () { panel.hidden = true; }); });
  panel.addEventListener('click', function (e) { if (e.target === panel) panel.hidden = true; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { panel.hidden = true; if (S.fokus) { S.fokus = false; save(); apply(); } } });
  $$('[data-theme-set]').forEach(function (b) { b.addEventListener('click', function () { S.theme = b.dataset.themeSet; save(); apply(); }); });
  $$('[data-num]').forEach(function (r) { r.addEventListener('input', function () { S[r.dataset.num] = +r.value; save(); apply(); }); });
  $$('[data-toggle]').forEach(function (c) { c.addEventListener('change', function () { S[c.dataset.toggle] = c.checked; save(); apply(); }); });
  var fontSel = $('[data-font]'); if (fontSel) fontSel.addEventListener('change', function () { S.fontRead = fontSel.value; save(); apply(); });
  $$('[data-reset]').forEach(function (b) { b.addEventListener('click', function () { S = {}; save(); apply(); }); });
  $$('[data-fokus-exit]').forEach(function (b) { b.addEventListener('click', function () { S.fokus = false; save(); apply(); }); });

  /* ---------- Lesezeile: folgt Maus/Finger, sonst Bildschirmmitte ---------- */
  var rulerY = null;
  function updateRuler() {
    var h = document.documentElement;
    if (!h.classList.contains('lesezeile')) return;
    var fsPx = parseFloat(getComputedStyle(h).getPropertyValue('--fs')) || 19;
    var lh = parseFloat(getComputedStyle(h).getPropertyValue('--lh')) || 1.8;
    h.style.setProperty('--band', Math.round(fsPx * lh * 1.25) + 'px');
    h.style.setProperty('--ry', (rulerY == null ? innerHeight * 0.45 : rulerY) + 'px');
  }
  document.addEventListener('mousemove', function (e) { rulerY = e.clientY; updateRuler(); }, { passive: true });
  document.addEventListener('touchmove', function (e) { rulerY = e.touches[0].clientY; updateRuler(); }, { passive: true });
  apply();

  /* ---------- Bibelstellen erkennen ---------- */
  var B = window.BUECHER || [];  // [n, name, abbr, spoken, slug, kapitel]
  var alias = {};
  function add(a, n) { alias[a.toLowerCase().replace(/[.\s]/g, '')] = n; }
  B.forEach(function (b) { add(b[1], b[0]); add(b[2], b[0]); add(b[3], b[0]); });
  ('gen:1 ex:2 lev:3 num:4 dtn:5 rut:8 1sam:9 2sam:10 1kön:11 2kön:12 1chr:13 2chr:14 neh:16 ijob:18 psalm:19 pred:21 hld:22 klgl:25 ez:26 dan:27 obd:31 zef:36 ' +
    'mt:40 mk:41 lk:42 röm:45 1kor:46 2kor:47 phil:50 1thess:52 2thess:53 1tim:54 2tim:55 phlm:57 hebr:58 1petr:60 2petr:61 1joh:62 2joh:63 3joh:64 offb:66')
    .split(' ').forEach(function (p) { var x = p.split(':'); add(x[0], +x[1]); });
  function findBook(s) {
    var k = s.toLowerCase().replace(/[.\s]/g, '');
    if (alias[k]) return alias[k];
    k = k.replace(/^(erster|erste)/, '1').replace(/^(zweiter|zweite)/, '2').replace(/^(dritter|dritte)/, '3').replace(/^(vierter|vierte)/, '4').replace(/^(fünfter|fünfte)/, '5');
    if (alias[k]) return alias[k];
    if (k.length >= 3) { for (var a in alias) if (a.indexOf(k) === 0) return alias[a]; }
    return null;
  }
  function parseRef(q) {
    var m = q.trim().replace(/\s+/g, ' ').match(/^((?:[1-5]\.?\s?|erster |zweiter |dritter |vierter |fünfter )?[a-zäöüß]+(?: lied)?)\.?\s*(\d+)(?:\s*(?:[:,.]|\s+vers\s+|\s)\s*(\d+))?/i);
    if (!m || m[0].length < q.trim().replace(/\s+/g, ' ').replace(/\s*[-–]\s*\d+$/, '').length) return null;
    var n = findBook(m[1]); if (!n) return null;
    var b = B[n - 1], c = +m[2], v = m[3] ? +m[3] : null;
    if (b[5] === 1 && !v && c > 1) { v = c; c = 1; }
    if (c < 1 || c > b[5]) return null;
    return { b: b, c: c, v: v };
  }
  function refUrl(r) { return root + 'bibel/' + r.b[4] + '/' + r.c + '.html' + (r.v ? '#v' + r.v : ''); }
  $$('form[data-quick]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      var q = f.q.value.trim(); if (!q) { e.preventDefault(); return; }
      var r = parseRef(q); if (r) { e.preventDefault(); location.href = refUrl(r); }
    });
  });

  /* ---------- Bibelvers für heute ---------- */
  var tpl = $$('template[data-votd]');
  if (tpl.length) {
    var now = new Date(), day = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 864e5);
    $('[data-votd-out]').innerHTML = tpl[day % tpl.length].innerHTML;
  }

  /* ---------- Filter (Lexikon, Konkordanz) ---------- */
  $$('[data-filter]').forEach(function (inp) {
    var items = $$(inp.dataset.filter);
    inp.addEventListener('input', function () {
      var q = inp.value.trim().toLowerCase();
      items.forEach(function (el) { el.hidden = q && el.querySelector('dt').textContent.toLowerCase().indexOf(q) === -1; });
      $$('.letter').forEach(function (h) { var dl = h.nextElementSibling; h.hidden = dl && !$$('.entry', dl).some(function (x) { return !x.hidden; }); });
    });
  });

  /* ---------- Suche ---------- */
  var form = $('form[data-search]'), out = $('#ergebnisse');
  if (form && out && window.SUCHINDEX) {
    var IDX = window.SUCHINDEX.map(function (r) { return { b: r[0], c: r[1], v: r[2], t: r[3], n: r[3].toLowerCase() }; });
    var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var reEsc = function (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); };
    var params = new URLSearchParams(location.search);
    form.q.value = params.get('q') || '';
    var shown = 50;
    function run() {
      var q = form.q.value.trim();
      var teil = ($('[name=teil]:checked') || {}).value, ganz = $('[name=ganz]').checked;
      if (!q) { out.innerHTML = ''; return; }
      var html = '';
      var r = parseRef(q);
      if (r) html += '<a class="res" href="' + refUrl(r) + '"><b>Bibelstelle öffnen</b><span>' + esc(r.b[1] + ' ' + r.c + (r.v ? ':' + r.v : '')) + '</span></a>';
      var terms = [], neg = [], m, re = /(-?)"([^"]+)"|(-?)(\S+)/g, qq = q.replace(/[„“”]/g, '"');
      while ((m = re.exec(qq))) { var t = (m[2] || m[4]).toLowerCase(); if (t === '-') continue; ((m[1] || m[3]) ? neg : terms).push(t); }
      var mk = function (t) { return ganz ? new RegExp('(?<![\\p{L}\\p{N}])' + reEsc(t) + '(?![\\p{L}\\p{N}])', 'u') : null; };
      var rx = terms.map(mk), nx = neg.map(mk);
      var hits = IDX.filter(function (o) {
        if (teil === 'hs' && o.b >= 40) return false;
        if (teil === 'cgs' && o.b < 40) return false;
        for (var i = 0; i < terms.length; i++) if (rx[i] ? !rx[i].test(o.n) : o.n.indexOf(terms[i]) === -1) return false;
        for (var j = 0; j < neg.length; j++) if (nx[j] ? nx[j].test(o.n) : o.n.indexOf(neg[j]) !== -1) return false;
        return true;
      });
      var hl = terms.length ? new RegExp((ganz ? '(?<![\\p{L}\\p{N}])(' : '(') + terms.map(reEsc).sort(function (a, b) { return b.length - a.length; }).join('|') + (ganz ? ')(?![\\p{L}\\p{N}])' : ')'), 'giu') : null;
      html += '<p class="res-stats">' + hits.length.toLocaleString('de-DE') + ' Verse gefunden</p>';
      hits.slice(0, shown).forEach(function (o) {
        var b = B[o.b - 1];
        html += '<a class="res" href="' + root + 'bibel/' + b[4] + '/' + o.c + '.html#v' + o.v + '"><b>' + esc(b[1] + ' ' + o.c + ':' + o.v) + '</b><span>' + (hl ? esc(o.t).replace(hl, '<mark>$1</mark>') : esc(o.t)) + '</span></a>';
      });
      if (hits.length > shown) html += '<p><button class="btn ghost" id="mehr">Weitere anzeigen</button></p>';
      out.innerHTML = html;
      var more = $('#mehr'); if (more) more.addEventListener('click', function () { shown += 50; run(); });
    }
    var t;
    form.addEventListener('submit', function (e) { e.preventDefault(); var r = parseRef(form.q.value); if (r && form.q.value.trim().split(/\s+/).length <= 4) { location.href = refUrl(r); return; } shown = 50; history.replaceState(null, '', '?q=' + encodeURIComponent(form.q.value)); run(); });
    form.q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { shown = 50; run(); }, 200); });
    $$('.search-opts input').forEach(function (i) { i.addEventListener('change', function () { shown = 50; run(); }); });
    run();
  }
})();
