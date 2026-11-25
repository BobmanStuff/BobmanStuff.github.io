"""Erzeugt die statische Website „Bibelstudium-Ecke“ aus website/build/bibel.json.

Ablauf:
    python -I website/tools/build_data.py      # RTF -> build/bibel.json (nur nötig, wenn sich RTFs ändern)
    python -I website/tools/check_headings.py  # eigene Überschriften prüfen
    python -I website/tools/build_site.py      # HTML-Seiten erzeugen

Alle Seiten sind reine HTML-Dateien mit relativen Links (funktionieren per Doppelklick, ohne Server).
"""
import html
import json
import pathlib
import re
import shutil

WEB = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((WEB / 'build' / 'bibel.json').read_text(encoding='utf-8'))
BOOKS = DATA['books']
SITE_NAME = 'Bibelstudium-Ecke'
STAND = '25.11.2026'

# Hinweis: Es werden ausschließlich Überschriften aus der Vorlage (Buchübersicht der
# Neue-Welt-Übersetzung) angezeigt – auf Wunsch des Nutzers keine selbst verfassten Überschriften.

esc = lambda s: html.escape(str(s), quote=True)
unstress = lambda s: re.sub('[̣́]', '', __import__('unicodedata').normalize('NFD', s))


def nfc(s):
    import unicodedata
    return unicodedata.normalize('NFC', s)


def slug(bk):
    s = bk['name'].lower().replace('. ', '-').replace(' ', '-')
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        s = s.replace(a, b)
    return f"{bk['n']:02d}-{s}"


for bk in BOOKS:
    bk['slug'] = slug(bk)

GROUPS = [
    ('Gesetz', 1, 5, 'gesetz'), ('Geschichte', 6, 17, 'geschichte'), ('Poesie und Weisheit', 18, 22, 'poesie'),
    ('Große Propheten', 23, 27, 'propheten'), ('Kleine Propheten', 28, 39, 'kleine'), ('Evangelien', 40, 43, 'evangelien'),
    ('Apostelgeschichte', 44, 44, 'apg'), ('Briefe des Paulus', 45, 58, 'paulus'), ('Weitere Briefe', 59, 65, 'briefe'),
    ('Prophezeiung', 66, 66, 'offenbarung'),
]
group_of = lambda n: next(g for g in GROUPS if g[1] <= n <= g[2])
chap_word = lambda n: 'Psalm' if n == 19 else 'Kapitel'

# ---------------------------------------------------------------- Icons (eigene, flache Linien-Icons)
EMBLEM = {
    'gesetz': '<path d="M14 54V20a9 9 0 0 1 18 0v34zM32 54V20a9 9 0 0 1 18 0v34z"/><path d="M19 26h8M19 32h8M19 38h8M19 44h8M37 26h8M37 32h8M37 38h8M37 44h8"/>',
    'geschichte': '<path d="M8 54V26h8v6h6v-6h8v6h4v-6h8v6h6v-6h8v28z"/><path d="M28 54V42a4 4 0 0 1 8 0v12M14 40h6M44 40h6"/><path d="M32 26V10l10 4-10 4"/>',
    'poesie': '<path d="M18 52c-6-10-6-30 4-40M46 52c6-10 6-30-4-40"/><path d="M14 52h36M22 12h20"/><path d="M26 14v36M32 13v37M38 14v36"/>',
    'propheten': '<path d="M14 18h30a6 6 0 0 1 0 12H20M14 18a6 6 0 0 0 0 12h4v18a6 6 0 0 0 6 6h26a6 6 0 0 0 0-12H24"/><path d="M26 36h18M26 41h12"/>',
    'kleine': '<path d="M10 42c6 6 30 6 40 0 4-3 6-8 6-12H6c0 4 1 9 4 12z"/><path d="M50 32c4-4 8-4 8 0M30 30c0-6 6-8 4-16 6 4 6 10 2 16"/><path d="M24 50h18"/>',
    'evangelien': '<path d="M8 40h48l-6 10H14z"/><path d="M30 40V8l18 26H30M30 12L16 34h14"/><path d="M4 56c6-4 10 4 16 0s10 4 16 0 10 4 16 0 8 4 10 2"/>',
    'apg': '<path d="M10 42h44l-8 10H18z"/><path d="M24 42V12l14 24H24M38 42V18l12 20H38"/><path d="M4 56c6-4 10 4 16 0s10 4 16 0 10 4 16 0"/><circle cx="52" cy="12" r="4"/>',
    'paulus': '<path d="M12 14h32v38H12z"/><path d="M18 22h20M18 28h20M18 34h14M18 40h18"/><path d="M56 6C46 12 40 24 38 38l4-2c4-10 10-20 14-30z"/><path d="M38 38l-2 6"/>',
    'briefe': '<path d="M10 16h44v32H10z"/><path d="M10 16l22 18 22-18"/><circle cx="32" cy="40" r="6"/>',
    'offenbarung': '<circle cx="32" cy="40" r="14"/><path d="M18 40h28M32 26c-6 6-6 22 0 28M32 26c6 6 6 22 0 28"/><path d="M16 22l6-12 10 8 10-8 6 12z"/>',
    # Themen
    'name': '<path d="M12 50V14h40v36z"/><path d="M20 26h24M20 34h24M20 42h14"/><circle cx="46" cy="44" r="6"/>',
    'reich': '<path d="M14 40l-4-22 12 10 10-16 10 16 12-10-4 22z"/><path d="M14 46h36"/>',
    'paradies': '<path d="M6 50c10-8 20-8 26 0 6-8 16-8 26 0"/><circle cx="44" cy="18" r="7"/><path d="M20 44V28M20 28c-8 0-10-8-10-12 8 0 10 6 10 12zM20 32c6 0 10-6 10-12-6 0-10 6-10 12z"/>',
    'tod': '<path d="M14 50c0-12 8-20 18-20s18 8 18 20"/><path d="M32 30V12M26 18l6-6 6 6"/><path d="M8 54h48"/>',
    'loesegeld': '<path d="M10 30h44M14 30l18-16 18 16"/><path d="M18 30v20M46 30v20M10 52h44"/><path d="M32 36v10"/>',
    'jesus': '<path d="M8 44h48l-6 8H14z"/><path d="M14 44c4-14 32-14 36 0"/><path d="M32 30V14"/><circle cx="32" cy="12" r="3"/>',
    'gebet': '<path d="M24 54V32l8-18 8 18v22"/><path d="M24 40h16"/><path d="M14 12l4 4M50 12l-4 4M32 4v6"/>',
    'familie': '<path d="M8 30l24-18 24 18"/><path d="M14 26v26h36V26"/><path d="M28 52V40h8v12"/>',
}


def icon(key, cls='ico'):
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{EMBLEM[key]}</g></svg>'


LOGO = ('<svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="6" fill="var(--brand)"/>'
        '<path d="M20 13c-4-3-8-3.5-12-3v17c4-.5 8 0 12 3 4-3 8-3.5 12-3V10c-4-.5-8 0-12 3z" fill="#fff"/>'
        '<path d="M20 13v17" stroke="var(--brand)" stroke-width="1.6"/></svg>')

# ---------------------------------------------------------------- Darstellung (Themes und Lese-Optionen)
# Schlüssel, Name, Hintergrund der Vorschau, Farbbalken, optionaler Stil für "Aa"
THEME_GROUPS = [
    ('Automatisch', [
        ('auto', 'Hell/Dunkel wie Windows', 'linear-gradient(135deg,#fff 50%,#17151c 50%)', '#5b3c88', ''),
        ('jahreszeit', 'Jahreszeit (nach Datum)', 'linear-gradient(90deg,#8cc157 25%,#f6a623 25% 50%,#b3541e 50% 75%,#a8d8ff 75%)', '#1b2633', ''),
    ]),
    ('Klassisch', [
        ('standard', 'Standard', '#fff', '#5b3c88', ''), ('nacht', 'Nacht', '#17151c', '#a98ad6', ''),
        ('sepia', 'Sepia', '#f6efe2', '#7a4f2a', ''), ('druckbibel', 'Druckbibel', '#fbf8f1', '#6b1f1f', "font:600 13px 'EB Garamond';color:#1f1a14"),
        ('schreibmaschine', 'Schreibmaschine', '#efeadf', 'repeating-linear-gradient(90deg,#1e1c1a 0 6px,transparent 6px 9px)', "font:400 12px 'Special Elite';color:#1e1c1a"),
    ]),
    ('Im Stil von', [
        ('jworg', 'JW.ORG', '#f1f1f1', '#4a6da7', "font:700 11px 'Noto Sans';color:#4a6da7"),
        ('jwlibrary', 'JW Library', '#2f2f2f', '#c2d4f1', "font:700 11px 'Noto Sans';color:#f2f2f2"),
        ('wachtturm', 'Wachtturm', '#fff', '#1f5aa6', "font:600 13px 'Noto Serif';color:#1f5aa6"),
        ('ikea', 'IKEA', '#fff', '#ffdb00', "font:800 13px 'Noto Sans';color:#0058a3"),
        ('google', 'Google', '#fff', 'linear-gradient(90deg,#4285f4 25%,#ea4335 25% 50%,#fbbc04 50% 75%,#34a853 75%)', 'font:500 13px Roboto;color:#1a73e8'),
        ('apple', 'Apple', '#f5f5f7', '#0071e3', 'font:600 13px system-ui;color:#1d1d1f'),
        ('lego', 'LEGO', '#ffcf00', 'repeating-linear-gradient(90deg,#d01012 0 8px,#006cb7 8px 16px,#00852b 16px 24px)', 'font:800 13px Outfit;color:#d01012'),
        ('blaugelb', 'Blau &amp; Gelb', '#0058a3', '#ffdb00', ''),
    ]),
    ('Natur', [
        ('wald', 'Wald', '#f3f6f0', '#2f6b3a', ''), ('meer', 'Meer', '#f2f8fb', '#0f6d8f', ''),
        ('wueste', 'Wüste', '#faf3e6', '#b5652b', ''), ('paradies', 'Paradies', 'linear-gradient(#2a8ec4,#f4fbf4)', '#2e8b57', ''),
    ]),
    ('Jahreszeiten', [
        ('fruehling', 'Frühling', '#fdfbf6', 'linear-gradient(90deg,#8cc157,#f2a7c3)', ''), ('sommer', 'Sommer', '#fffdf5', 'linear-gradient(90deg,#f6a623,#00a6c8)', ''),
        ('herbst', 'Herbst', '#faf5ef', 'linear-gradient(90deg,#8c3f14,#d9a13b)', ''), ('winter', 'Winter', '#f6f9fc', 'linear-gradient(90deg,#2c5584,#a8d8ff)', ''),
    ]),
    ('Für die Augen', [
        ('kontrast', 'Hoher Kontrast', '#000', '#ffe14d', ''), ('gelbschwarz', 'Gelb auf Schwarz', '#000', '#ffe600', 'font:800 13px sans-serif;color:#ffe600'),
        ('weissblau', 'Weiß auf Dunkelblau', '#0b1f4d', '#fff', 'font:800 13px sans-serif;color:#fff'), ('blendarm', 'Blendarm', '#e6e3dc', '#4a5f7a', ''),
    ]),
]
# Zusätzliche Themes aus themes_extra.py einsortieren (eigene CSS-Datei assets/themes-extra.css)
import sys as _sys  # noqa: E402
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import themes_extra  # noqa: E402
_groups = dict(THEME_GROUPS)
for _g, _items in themes_extra.buttons_by_group().items():
    _groups.setdefault(_g, []).extend(_items)
THEME_GROUPS = [(g, _groups[g]) for g in themes_extra.GROUP_ORDER if g in _groups]
THEME_KEYS = [k for _, items in THEME_GROUPS for k, *_ in items]
assert len(THEME_KEYS) == len(set(THEME_KEYS)), 'Theme-Schlüssel doppelt'


def theme_button(k, label, bg, bar, aa):
    inner = f'Aa<b style="background:{bar}"></b>' if aa else f'<b style="background:{bar}"></b>'
    return f'<button data-theme-set="{k}"><i class="{"ab" if aa else ""}" style="background:{bg};{aa}">{inner}</i>{label}</button>'


SETTINGS_HTML = '''<div class="settings" id="settings" role="dialog" aria-label="Darstellung" hidden>
  <div class="settings-card">
    <div class="settings-head"><h2>Darstellung</h2><button data-close-settings aria-label="Schließen">✕</button></div>
    <h3>Theme</h3>''' + ''.join(
    f'<details class="tgroup" data-keys="{" ".join(t[0] for t in items)}"><summary>{g} <span>{len(items)}</span></summary><div class="themes">'
    + ''.join(theme_button(*t) for t in items) + '</div></details>' for g, items in THEME_GROUPS) + '''
    <p class="hint">„Im Stil von“ heißt: Farben, Schrift und Formen angelehnt – ohne Logos oder Inhalte der Vorbilder. Bei „Für die Augen“ ist individuell verschieden, was am angenehmsten ist.</p>
    <h3>Lesen</h3>
    <label class="range-row" for="opt-font">Schrift<select id="opt-font" data-font style="grid-column:2/4">
      <option value="">Wie im Theme</option><option value="serif">Mit Serifen (Noto Serif)</option><option value="sans">Ohne Serifen (Noto Sans)</option>
      <option value="atkinson">Besonders gut lesbar (Atkinson Hyperlegible)</option><option value="garamond">Klassisch (EB Garamond)</option></select></label>
    <label class="range-row">Schriftgröße<input type="range" min="15" max="40" step="1" data-num="fs" data-def="19"><output></output></label>
    <label class="range-row">Zeilenabstand<input type="range" min="1.4" max="2.6" step="0.05" data-num="lh" data-def="1.8"><output></output></label>
    <label class="range-row">Lesebreite<input type="range" min="40" max="110" step="2" data-num="measure" data-def="72"><output></output></label>
    <label class="sw"><input type="checkbox" data-toggle="versweise"> Vers für Vers (jeder Vers in eigener Zeile)</label>
    <label class="sw"><input type="checkbox" data-toggle="zweispaltig"> Zweispaltig (auf breiten Bildschirmen)</label>
    <label class="sw"><input type="checkbox" data-toggle="weit"> Weite Buchstaben- und Wortabstände</label>
    <label class="sw"><input type="checkbox" data-toggle="lesezeile"> Lesezeile (Rest abdunkeln)</label>
    <label class="sw"><input type="checkbox" data-toggle="fokus"> Fokus-Modus (nur Bibeltext)</label>
    <h3>Anzeige</h3>
    <label class="sw"><input type="checkbox" data-toggle="hideOff"> Überschriften ausblenden</label>
    <label class="sw"><input type="checkbox" data-toggle="noNum"> Versnummern ausblenden</label>
    <button class="btn ghost reset" data-reset>Alles zurücksetzen</button>
  </div>
</div>
<button class="btn primary fokus-exit" data-fokus-exit>Fokus beenden</button>
<div class="ruler top" aria-hidden="true"></div><div class="ruler bot" aria-hidden="true"></div>'''

# Läuft im <head>, bevor die Seite gezeichnet wird (kein Aufflackern beim Seitenwechsel)
HEAD_JS = ("try{var s=JSON.parse(localStorage.getItem('bse.einstellungen')||'{}'),h=document.documentElement,t=s.theme||'standard';"
           "if(t==='auto')t=matchMedia('(prefers-color-scheme: dark)').matches?'nacht':'standard';"
           "if(t==='jahreszeit'){var m=new Date().getMonth();t=(m===11||m<2)?'winter':m<5?'fruehling':m<8?'sommer':'herbst'}"
           "h.dataset.theme=t;var F={serif:'\"Noto Serif\",Georgia,serif',sans:'\"Noto Sans\",Arial,sans-serif',"
           "atkinson:'\"Atkinson Hyperlegible\",Verdana,sans-serif',garamond:'\"EB Garamond\",\"Noto Serif\",Georgia,serif'};"
           "if(s.fs)h.style.setProperty('--fs',s.fs+'px');if(s.lh)h.style.setProperty('--lh',s.lh);"
           "if(s.measure)h.style.setProperty('--measure',s.measure+'ch');if(F[s.fontRead])h.style.setProperty('--font-read-user',F[s.fontRead]);"
           "['hideOff','noNum','versweise','zweispaltig','weit','lesezeile','fokus'].forEach(function(k){if(s[k])h.classList.add(k)})}catch(e){}")

# ---------------------------------------------------------------- Bibelstellen in Texten verlinken
SPOKEN = sorted({b['spoken'] for b in BOOKS} | {'Da'}, key=len, reverse=True)
SPOKEN_RE = [re.sub(r'^(erster|zweiter|dritter|vierter|fünfter) ', lambda m: '[' + m.group(1)[0] + m.group(1)[0].upper() + ']' + m.group(1)[1:] + ' ', re.escape(s).replace('\\ ', ' ')) for s in SPOKEN]
TAIL = r'(?:(?:, | bis )\d+(?! Vers))*'
REF_IN_TEXT = re.compile('(' + '|'.join(SPOKEN_RE) + r') (\d+)(?: Vers (\d+))?(' + TAIL + r')((?:(?:; | bis )\d+ Vers \d+' + TAIL + r')*)')
CHAIN = re.compile(r'(; | bis )(\d+) Vers (\d+)(' + TAIL + ')')
BY_SPOKEN = {b['spoken'].lower(): b for b in BOOKS}
BY_SPOKEN['da'] = BOOKS[26]


def chap_href(bk, c, v=None, root=''):
    return f"{root}bibel/{bk['slug']}/{c}.html" + (f'#v{v}' if v else '')


def linkify(escaped, root):
    def rep(m):
        name, a, v, rest, chain = m.groups()
        bk = BY_SPOKEN.get(name.lower())
        if not bk:
            return m.group(0)
        c, vv = int(a), int(v) if v else None
        if not v and len(bk['ch']) == 1:
            c, vv = 1, c
        if c > len(bk['ch']):
            return m.group(0)
        head = m.group(0)[:len(m.group(0)) - len(chain)]
        out = f'<a class="ref" href="{chap_href(bk, c, vv, root)}">{head}</a>'
        out += CHAIN.sub(lambda k: f'{k.group(1)}<a class="ref" href="{chap_href(bk, int(k.group(2)), int(k.group(3)), root)}">{k.group(2)} Vers {k.group(3)}{k.group(4)}</a>' if int(k.group(2)) <= len(bk['ch']) else k.group(0), chain)
        return out
    return REF_IN_TEXT.sub(rep, escaped)


# ---------------------------------------------------------------- Verse
def verses_of(bk, c):
    out, cur = {}, None
    for p in bk['ch'][c - 1]:
        if p[0] in 'hd':
            continue
        for x in p[1:]:
            if isinstance(x, int):
                cur = x
                out[cur] = []
            elif cur is not None:
                out[cur].append(x)
    return {v: re.sub(r'\s+', ' ', ' '.join(t)).strip() for v, t in out.items()}


def vtext(b, c, v):
    return verses_of(BOOKS[b - 1], c).get(v, '')


# ---------------------------------------------------------------- Seitenrahmen
NAV = [('index.html', 'Start'), ('bibel.html', 'Bibel'), ('themen.html', 'Themen'), ('suche.html', 'Suche'), ('lexikon.html', 'Lexikon'), ('hinweise.html', 'Hinweise')]


def page(path, title, body, active='', desc=''):
    depth = path.count('/')
    root = '../' * depth
    nav = ''.join(f'<a href="{root}{h}"{" aria-current=page" if active == h else ""}>{l}</a>' for h, l in NAV)
    doc = f'''<!doctype html>
<html lang="de" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} – {SITE_NAME}</title>
<meta name="description" content="{esc(desc or 'Private Studienseite mit der Neue-Welt-Übersetzung')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800&family=Noto+Serif:ital,wght@0,400;0,600;1,400&family=Roboto:wght@400;500;700&family=Outfit:wght@400;600;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Special+Elite&{FONTS_EXTRA}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="stylesheet" href="{root}assets/themes-extra.css">
<link rel="icon" href="{root}assets/logo.svg">
<script>{HEAD_JS}</script>
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="topline"></div>
<header class="site-head">
  <div class="wrap head-row">
    <a class="brand" href="{root}index.html">{LOGO}<span>{SITE_NAME}</span></a>
    <form class="qs" action="{root}suche.html" method="get" role="search" data-quick>
      <input name="q" type="search" placeholder="Suchen oder Bibelstelle (z. B. Joh 17:3)" aria-label="Suchen">
      <button aria-label="Suchen"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></button>
    </form>
    <button class="theme-btn" data-open-settings aria-haspopup="dialog"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg><span>Darstellung</span></button>
  </div>
  <nav class="wrap main-nav" aria-label="Hauptnavigation">{nav}</nav>
</header>
<main id="inhalt">
{body}
</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div><a class="brand" href="{root}index.html">{LOGO}<span>{SITE_NAME}</span></a>
      <p>Private Seite für das persönliche Bibelstudium. <strong>Keine offizielle Website von Jehovas Zeugen.</strong> Bibeltext: Neue-Welt-Übersetzung der Heiligen Schrift (lokale Kopie aus eigenen RTF-Dateien).</p></div>
    <div><h3>Bibel</h3><a href="{root}bibel.html">Alle Bücher</a><a href="{root}themen.html">Themen</a><a href="{root}suche.html">Suche</a></div>
    <div><h3>Hilfen</h3><a href="{root}lexikon.html">Worterklärungen</a><a href="{root}konkordanz.html">Konkordanz</a><a href="{root}anhang-a.html">Anhang A</a><a href="{root}vorwort.html">Vorwort</a></div>
    <div><h3>Über</h3><a href="{root}hinweise.html">Hinweise &amp; Kennzeichnung</a><span class="muted">Stand {STAND}</span></div>
  </div>
</footer>
{SETTINGS_HTML}
<script src="{root}assets/buecher.js"></script>
<script src="{root}assets/site.js"></script>
</body>
</html>
'''
    out = WEB / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding='utf-8')
    return root


def crumbs(root, *items):
    parts = [f'<a href="{root}index.html">Start</a>']
    for href, label in items:
        parts.append(f'<a href="{root}{href}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
    return '<nav class="crumbs wrap" aria-label="Brotkrumen">' + '<span class="sep">›</span>'.join(parts) + '</nav>'


# ---------------------------------------------------------------- Überschriften je Kapitel
def split_outline(t):
    return [(int(m.group(2)), m.group(1).strip()) for m in re.finditer(r'\s*,?\s*([^()]+?)\s*\((?:Vers |Psalm )?(\d+)[^)]*\)', t) if m.group(1).strip()]


def headings(bk, c):
    hs, subtitles = {}, []
    for oc, lvl, t in bk['outline']:
        if oc != c:
            continue
        parts = split_outline(t)
        if not parts:
            if lvl == 0:
                subtitles.append(t)
            continue
        for v, label in parts:
            if not any(h[1] == label for h in hs.get(v, [])):
                hs.setdefault(v, []).append(('off0' if lvl == 0 else 'off1', label))
    return hs, subtitles


def head_html(kind, text):
    if kind == 'off0':
        return f'<h2 class="h-off">{esc(text)}</h2>'
    return f'<h3 class="h-off sub">{esc(text)}</h3>'


# ---------------------------------------------------------------- Kapitelseite
def chapter_page(bk, c):
    n, nch = bk['n'], len(bk['ch'])
    path = f"bibel/{bk['slug']}/{c}.html"
    root = '../../'
    hs, subtitles = headings(bk, c)
    body, cur = '', None
    for p in bk['ch'][c - 1]:
        kind = p[0]
        if kind == 'h':
            body += f'<p class="superscription">{esc(p[1])}</p>'
            continue
        if kind == 'd':
            body += f'<p class="division">{esc(p[1])}</p>'
            continue
        inner, i = '', 1
        while i < len(p):
            x = p[i]
            if isinstance(x, int):
                cur = x
                if x in hs:
                    if inner:
                        body += f'<p class="{kind}">{inner}</p>'
                        inner = ''
                    body += ''.join(head_html(k, t) for k, t in hs[x])
                txt = p[i + 1] if i + 1 < len(p) and isinstance(p[i + 1], str) else ''
                if txt:
                    i += 1
                inner += f'<span class="v" id="v{x}"><a class="vn" href="#v{x}" aria-label="Vers {x}">{x}</a>{esc(txt)}</span> '
            elif cur is not None:
                inner += f'<span class="v" data-v="{cur}">{esc(x)}</span> '
            i += 1
        if inner:
            body += f'<p class="{kind}">{inner}</p>'
    # Übersicht der Überschriften
    toc = ''.join(
        f'<li class="t-{k}"><a href="#v{v}"><span class="tv">{v}</span><span>{esc(t)}</span></a></li>'
        for v in sorted(hs) for k, t in hs[v])
    prev = (bk, c - 1) if c > 1 else ((BOOKS[n - 2], len(BOOKS[n - 2]['ch'])) if n > 1 else None)
    nxt = (bk, c + 1) if c < nch else ((BOOKS[n], 1) if n < 66 else None)
    pager = '<nav class="pager" aria-label="Kapitel blättern">'
    pager += (f'<a class="btn ghost" rel="prev" href="{chap_href(prev[0], prev[1], root=root)}">← {esc(prev[0]["name"])} {prev[1]}</a>' if prev else '<span></span>')
    pager += f'<a class="btn ghost" href="index.html">Alle Kapitel</a>'
    pager += (f'<a class="btn primary" rel="next" href="{chap_href(nxt[0], nxt[1], root=root)}">{esc(nxt[0]["name"])} {nxt[1]} →</a>' if nxt else '<span></span>')
    pager += '</nav>'
    chips = ''.join(f'<a href="{i}.html"{" aria-current=page" if i == c else ""}>{i}</a>' for i in range(1, nch + 1))
    g = group_of(n)
    html_body = f'''{crumbs(root, ("bibel.html", "Bibel"), (f"bibel/{bk['slug']}/index.html", bk['name']), (None, f"{chap_word(n)} {c}"))}
<div class="wrap reader">
  <aside class="reader-side">
    <div class="side-card">
      <div class="side-title">{icon(g[3])}<div><div class="kicker">{esc(bk['name'])}</div><div class="bignum">{c}</div></div></div>
      {('<p class="subtitle">' + ' · '.join(esc(s) for s in subtitles) + '</p>') if subtitles else ''}
      <details class="chapters-pop"><summary>{chap_word(n)} wählen</summary><div class="chip-grid">{chips}</div></details>
      {f'<h2 class="side-h">Übersicht</h2><ol class="toc">{toc}</ol>' if toc else ''}
      <p class="legend">Überschriften: Buchübersicht der Neue-Welt-Übersetzung</p>
    </div>
  </aside>
  <article class="reader-main">
    <header class="chapter-head">
      <p class="kicker">{esc(bk['title'])}</p>
      <h1>{esc(bk['name'])} {c}</h1>
    </header>
    <div class="scripture">{body}</div>
    {pager}
  </article>
</div>'''
    page(path, f"{bk['name']} {c}", html_body, 'bibel.html', f"{bk['name']} {c} – Neue-Welt-Übersetzung")


# ---------------------------------------------------------------- Buchseite
def book_page(bk):
    n = bk['n']
    root = '../../'
    g = group_of(n)
    info = bk.get('info', {})
    meta = ''.join(f'<div><dt>{k}</dt><dd>{esc(info[k])}</dd></div>' for k in ('Schreiber', 'Wo geschrieben', 'Wann fertig', 'Zeitspanne') if info.get(k))
    grid = ''.join(f'<a class="num-tile" href="{i}.html">{i}</a>' for i in range(1, len(bk['ch']) + 1))
    by_ch = {}
    for c, lvl, t in bk['outline']:
        by_ch.setdefault(c, []).append((lvl, t))
    outline = ''
    for c in sorted(by_ch):
        items = ''.join(f'<li class="l{min(l, 2)}"><a href="{c}.html{("#v" + str(split_outline(t)[0][0])) if split_outline(t) else ""}">{esc(t)}</a></li>' for l, t in by_ch[c])
        outline += f'<details><summary>{chap_word(n)} {c}</summary><ul>{items}</ul></details>'
    body = f'''{crumbs(root, ("bibel.html", "Bibel"), (None, bk['name']))}
<section class="wrap book-hero">
  <div class="book-hero-ico">{icon(g[3])}</div>
  <div>
    <p class="kicker">{'Hebräische Schriften' if n < 40 else 'Christliche Griechische Schriften'} · {g[0]}</p>
    <h1>{esc(bk['name'])}</h1>
    <p class="lead">{esc(bk['title'])}</p>
    <dl class="meta">{meta}</dl>
    <p><a class="btn primary" href="1.html">Mit {chap_word(n)} 1 beginnen</a></p>
  </div>
</section>
<section class="wrap block">
  <h2 class="block-h">{'Psalmen' if n == 19 else 'Kapitel'}</h2>
  <div class="num-grid">{grid}</div>
</section>
<section class="wrap block">
  <h2 class="block-h">Übersicht des Buches</h2>
  <div class="outline">{outline or '<p class="muted">Keine Übersicht vorhanden.</p>'}</div>
</section>'''
    page(f"bibel/{bk['slug']}/index.html", bk['name'], body, 'bibel.html', f"{bk['name']} – Übersicht und Kapitel")


# ---------------------------------------------------------------- Bibel-Übersicht
def bible_index():
    root = ''
    sec = ''
    for title, a, z in (('Hebräische Schriften', 1, 39), ('Christliche Griechische Schriften', 40, 66)):
        sec += f'<section class="wrap block"><h2 class="block-h">{title}</h2>'
        for g in GROUPS:
            if g[1] < a or g[2] > z:
                continue
            tiles = ''.join(
                f'<a class="book-tile g-{g[3]}" href="bibel/{BOOKS[i - 1]["slug"]}/index.html">{icon(g[3])}<b>{esc(BOOKS[i - 1]["name"])}</b><span>{len(BOOKS[i - 1]["ch"])} {chap_word(i) if i != 19 else "Psalmen"}</span></a>'
                for i in range(g[1], g[2] + 1))
            sec += f'<h3 class="group-h">{g[0]}</h3><div class="book-grid">{tiles}</div>'
        sec += '</section>'
    body = f'''{crumbs(root, (None, "Bibel"))}
<section class="wrap page-head"><h1>Die Bibel</h1><p class="lead">66 Bücher · Neue-Welt-Übersetzung der Heiligen Schrift</p></section>
{sec}'''
    page('bibel.html', 'Bibel', body, 'bibel.html', 'Alle 66 Bücher der Bibel')


# ---------------------------------------------------------------- Startseite und Themen
VOTD = [(19, 83, 18), (43, 17, 3), (40, 6, 9), (40, 6, 10), (66, 21, 3), (66, 21, 4), (19, 37, 29), (19, 37, 11), (23, 65, 21), (23, 11, 6), (27, 2, 44),
        (40, 24, 14), (55, 3, 16), (20, 3, 5), (20, 3, 6), (59, 4, 8), (62, 5, 3), (44, 24, 15), (43, 5, 28), (21, 9, 5), (19, 146, 4), (40, 20, 28),
        (43, 3, 16), (62, 4, 8), (23, 41, 10), (19, 34, 18), (19, 55, 22), (40, 5, 3), (60, 5, 7), (50, 4, 6), (50, 4, 7), (23, 33, 24), (23, 35, 5),
        (61, 3, 13), (45, 8, 38), (19, 145, 18), (2, 3, 15), (23, 42, 8)]

# Themen: nur Bibelstellen, Überschriften im Sinne der Neue-Welt-Übersetzung
THEMEN = [
    ('name', 'Gottes Name', 'Gott hat einen persönlichen Namen: Jehova.', [(19, 83, 18), (2, 3, 15), (23, 42, 8), (40, 6, 9)]),
    ('reich', 'Gottes Königreich', 'Eine echte Regierung im Himmel, die die Erde regieren wird.', [(27, 2, 44), (40, 6, 10), (40, 24, 14), (66, 11, 15)]),
    ('paradies', 'Das Paradies auf der Erde', 'Gottes Vorsatz mit der Erde und den Menschen.', [(19, 37, 29), (19, 37, 11), (23, 65, 21), (23, 11, 6), (66, 21, 4)]),
    ('tod', 'Tod und Auferstehung', 'Was mit den Toten ist – und welche Hoffnung es gibt.', [(21, 9, 5), (19, 146, 4), (43, 5, 28), (43, 5, 29), (44, 24, 15)]),
    ('loesegeld', 'Das Lösegeld', 'Warum Jesus sein Leben gegeben hat.', [(40, 20, 28), (43, 3, 16), (45, 6, 23), (62, 2, 2)]),
    ('jesus', 'Jesus Christus', 'Gottes Sohn, König des Königreiches.', [(43, 17, 3), (43, 14, 28), (40, 3, 17), (50, 2, 9), (50, 2, 10)]),
    ('gebet', 'Beten', 'Wie wir Jehova näherkommen können.', [(59, 4, 8), (50, 4, 6), (50, 4, 7), (19, 145, 18), (62, 5, 14)]),
    ('familie', 'Ehe und Familie', 'Rat aus der Bibel für das Familienleben.', [(49, 5, 33), (51, 3, 13), (40, 19, 6), (5, 6, 7), (20, 22, 6)]),
]


def verse_card(b, c, v, root=''):
    bk = BOOKS[b - 1]
    if not vtext(b, c, v):
        raise SystemExit(f'Bibelstelle fehlt: {bk["name"]} {c}:{v}')
    return (f'<blockquote class="verse-card"><p>{esc(nfc(unstress(vtext(b, c, v))))}</p>'
            f'<a href="{chap_href(bk, c, v, root)}">{esc(bk["name"])} {c}:{v}</a></blockquote>')


def home():
    votd = ''.join(f'<template data-votd>{verse_card(*x)}</template>' for x in VOTD)
    themes = ''.join(f'<a class="topic-tile" href="themen.html#{k}">{icon(k)}<b>{esc(t)}</b><span>{esc(d)}</span></a>' for k, t, d, _ in THEMEN[:4])
    groups = ''.join(f'<a class="book-tile g-{g[3]}" href="bibel/{BOOKS[g[1] - 1]["slug"]}/index.html">{icon(g[3])}<b>{g[0]}</b><span>{BOOKS[g[1] - 1]["name"]}{" – " + BOOKS[g[2] - 1]["name"] if g[2] != g[1] else ""}</span></a>' for g in GROUPS)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker light">Persönliches Bibelstudium</p>
      <h1>Lies die Bibel. Lerne Jehova kennen.</h1>
      <p class="lead">Die ganze Neue-Welt-Übersetzung – übersichtlich, durchsuchbar und mit den Überschriften aus der Buchübersicht.</p>
      <p class="hero-actions"><a class="btn accent" href="bibel/01-1-mose/1.html">Mit 1. Mose beginnen</a><a class="btn light" href="bibel.html">Alle Bücher</a></p>
    </div>
    <div class="hero-art" aria-hidden="true">
      <svg viewBox="0 0 320 240"><rect x="0" y="150" width="320" height="90" rx="12" fill="rgba(255,255,255,.12)"/><circle cx="250" cy="60" r="34" fill="#ffdb00"/>
      <path d="M160 70c-30-20-70-24-110-18v130c40-6 80-2 110 18 30-20 70-24 110-18V52c-40-6-80-2-110 18z" fill="#fff"/>
      <path d="M160 70v130" stroke="var(--brand)" stroke-width="4"/>
      <g stroke="var(--brand-soft-strong)" stroke-width="6" stroke-linecap="round"><path d="M72 84h62M72 104h62M72 124h50M72 144h62M186 84h62M186 104h62M186 124h62M186 144h44"/></g>
      <path d="M150 196c-14 10-20 20-18 30M170 196c14 10 20 20 18 30" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
    </div>
  </div>
</section>
<section class="wrap block two">
  <div class="card votd"><h2 class="block-h small">Bibelvers für heute</h2><div data-votd-out>{verse_card(*VOTD[0])}</div>{votd}</div>
  <div class="card steps">
    <h2 class="block-h small">So studierst du</h2>
    <ol class="step-list">
      <li><b>Beten</b><span>Bitte Jehova um Hilfe und Verständnis.</span></li>
      <li><b>Lesen</b><span>Lies ein ganzes Kapitel – die Überschriften zeigen dir die Abschnitte.</span></li>
      <li><b>Nachdenken</b><span>Frag dich: Was lerne ich hier über Jehova und seinen Vorsatz?</span></li>
      <li><b>Anwenden</b><span>Überlege, wie du das Gelernte im Alltag umsetzt.</span></li>
    </ol>
  </div>
</section>
<section class="wrap block">
  <div class="block-row"><h2 class="block-h">Themen der Bibel</h2><a class="more" href="themen.html">Alle Themen →</a></div>
  <div class="topic-grid">{themes}</div>
</section>
<section class="wrap block">
  <div class="block-row"><h2 class="block-h">Bücher der Bibel</h2><a class="more" href="bibel.html">Alle 66 Bücher →</a></div>
  <div class="book-grid">{groups}</div>
</section>
<section class="wrap block">
  <div class="card notice"><h2 class="block-h small">Überschriften im Bibeltext</h2>
    <p>Die <span class="h-off-demo">Überschriften</span> im Bibeltext stammen aus der Buchübersicht der Neue-Welt-Übersetzung. Es wurden keine eigenen Überschriften hinzugefügt. Unter „Darstellung“ kannst du sie ausblenden. <a href="hinweise.html">Mehr dazu</a></p></div>
</section>'''
    page('index.html', 'Start', body, 'index.html', 'Persönliches Bibelstudium mit der Neue-Welt-Übersetzung')


def themen():
    secs = ''
    for k, t, d, refs in THEMEN:
        secs += f'<section class="wrap block topic" id="{k}"><div class="topic-head">{icon(k)}<div><h2 class="block-h">{esc(t)}</h2><p class="lead">{esc(d)}</p></div></div><div class="verse-grid">{"".join(verse_card(*r) for r in refs)}</div></section>'
    body = f'''{crumbs('', (None, "Themen"))}
<section class="wrap page-head"><h1>Themen der Bibel</h1><p class="lead">Was die Bibel selbst sagt – zusammengestellt aus Bibelstellen der Neue-Welt-Übersetzung.</p></section>
{secs}'''
    page('themen.html', 'Themen', body, 'themen.html', 'Themen der Bibel mit Bibelstellen')


# ---------------------------------------------------------------- Lexikon, Konkordanz, Extras
def first_letter(w):
    ch = nfc(unstress(w))[:1].upper()
    return {'Ä': 'A', 'Ö': 'O', 'Ü': 'U'}.get(ch, ch) if ch.isalpha() else '#'


def az(entries):
    letters = sorted({first_letter(e[0]) for e in entries}, key=lambda x: (x == '#', x))
    return letters, '<nav class="az" aria-label="Alphabet">' + ''.join(f'<a href="#buchstabe-{l}">{l}</a>' for l in letters) + '</nav>'


def lexikon():
    letters, nav = az(DATA['glossar'])
    secs = ''
    for l in letters:
        items = ''.join(f'<div class="entry" id="{esc(re.sub(r"[^a-z0-9]+", "-", w.lower()))}"><dt>{esc(w)}</dt><dd>{"".join("<p>" + linkify(esc(p), "") + "</p>" for p in txt.split(chr(10)))}</dd></div>'
                        for w, txt in DATA['glossar'] if first_letter(w) == l)
        secs += f'<h2 class="letter" id="buchstabe-{l}">{l}</h2><dl class="entries">{items}</dl>'
    body = f'''{crumbs('', (None, "Worterklärungen"))}
<section class="wrap page-head"><h1>Worterklärungen</h1><p class="lead">{len(DATA["glossar"])} Begriffe aus der Neue-Welt-Übersetzung – Bibelstellen sind verlinkt.</p>
<input class="filter" type="search" placeholder="Begriff filtern …" data-filter=".entry" aria-label="Begriffe filtern"></section>
<div class="wrap">{nav}{secs}</div>'''
    page('lexikon.html', 'Worterklärungen', body, 'lexikon.html')


def konkordanz():
    letters, nav = az(DATA['konkordanz'])
    secs = ''
    for l in letters:
        items = ''
        for w, refs in DATA['konkordanz']:
            if first_letter(w) != l:
                continue
            lis = ''.join((f'<li>{linkify(esc(r), "")} <span class="muted">– {esc(s)}</span></li>' if r else f'<li><em>{linkify(esc(s), "")}</em></li>') for r, s in refs)
            items += f'<div class="entry"><dt>{esc(w)}</dt><dd><ul>{lis}</ul></dd></div>'
        secs += f'<h2 class="letter" id="buchstabe-{l}">{l}</h2><dl class="entries">{items}</dl>'
    body = f'''{crumbs('', (None, "Konkordanz"))}
<section class="wrap page-head"><h1>Konkordanz</h1><p class="lead">{len(DATA["konkordanz"])} Stichwörter mit Fundstellen. Das Stichwort ist in den Auszügen mit seinem Anfangsbuchstaben abgekürzt.</p>
<input class="filter" type="search" placeholder="Stichwort filtern …" data-filter=".entry" aria-label="Stichwörter filtern"></section>
<div class="wrap">{nav}{secs}</div>'''
    page('konkordanz.html', 'Konkordanz', body, 'lexikon.html')


def extras():
    for ex, fname in zip(DATA['extras'], ('vorwort.html', 'anhang-a.html', 'anhang-b.html')):
        h = ''
        for k, t in ex['items']:
            h += f'<h2>{esc(t)}</h2>' if k == 't' else f'<h3>{esc(t)}</h3>' if k == 'h' else f'<p>{linkify(esc(t), "")}</p>'
        body = f'''{crumbs('', (None, ex['title']))}<article class="wrap prose">{h}</article>'''
        page(fname, ex['title'], body, '')


def suche():
    body = f'''{crumbs('', (None, "Suche"))}
<section class="wrap page-head"><h1>Suche</h1>
<form class="bigsearch" data-search><input name="q" type="search" placeholder="Wort, Satzteil in Anführungszeichen oder Bibelstelle" aria-label="Suchbegriff" autocomplete="off"><button class="btn primary">Suchen</button></form>
<div class="search-opts"><label><input type="radio" name="teil" value="" checked> Ganze Bibel</label><label><input type="radio" name="teil" value="hs"> Hebräische Schriften</label><label><input type="radio" name="teil" value="cgs"> Christliche Griechische Schriften</label><label><input type="checkbox" name="ganz"> Ganze Wörter</label></div>
<p class="muted small">Mehrere Wörter müssen alle vorkommen · <code>"Name Jehovas"</code> sucht genau diesen Satzteil · <code>-Wort</code> schließt aus · Bibelstellen wie <code>Ps 83:18</code> öffnen direkt.</p></section>
<section class="wrap"><div id="ergebnisse" aria-live="polite"></div></section>
<script src="assets/suchindex.js"></script>'''
    page('suche.html', 'Suche', body, 'suche.html')


def hinweise():
    body = f'''{crumbs('', (None, "Hinweise"))}
<article class="wrap prose">
<h1>Hinweise &amp; Kennzeichnung</h1>
<h2>Was ist diese Seite?</h2>
<p>Eine private, lokal gespeicherte Studienseite. Sie ist <strong>keine offizielle Website von Jehovas Zeugen</strong> und ersetzt nicht die offiziellen Ausgaben. Der Bibeltext stammt aus eigenen RTF-Dateien der Neue-Welt-Übersetzung und wurde unverändert übernommen; nur offensichtliche Exportfehler bei Versnummern wurden korrigiert.</p>
<h2>Überschriften</h2>
<div class="demo"><h2 class="h-off">Hauptüberschrift</h2><h3 class="h-off sub">Unterüberschrift</h3>
<p>Alle Überschriften im Bibeltext stammen aus der Buchübersicht der Neue-Welt-Übersetzung (Gliederung am Anfang jedes Buches). <strong>Es wurden keine eigenen Überschriften hinzugefügt.</strong> Wo die Vorlage mehrere Überschriften in einer Zeile zusammenfasst (z. B. „Wut (Vers 21 bis 26), Ehebruch (Vers 27 bis 30)“), werden sie einzeln am jeweiligen Vers angezeigt.</p></div>
<p>Die Überschriften lassen sich unter „Darstellung“ ausblenden.</p>
<h2>Themen</h2>
<p>Die Themenseite stellt nur Bibelstellen zusammen. Die kurzen Einleitungssätze fassen zusammen, was diese Verse sagen.</p>
<h2>Speicherung</h2>
<p>Die Seite speichert nur deine Darstellungs-Einstellungen (Theme, Schriftgröße, Anzeige) im Browser. Es werden keine Daten ins Internet übertragen; lediglich die Schriftarten werden von Google Fonts geladen (ohne Internet wird eine Systemschrift verwendet).</p>
</article>'''
    page('hinweise.html', 'Hinweise', body, 'hinweise.html')


# ---------------------------------------------------------------- Daten für JavaScript
FONTS_EXTRA = '&'.join('family=' + f for f in themes_extra.FONT_FAMILIES)


def js_data():
    (WEB / 'assets' / 'themes-extra.css').write_text(themes_extra.css(), encoding='utf-8')
    books = [[b['n'], b['name'], b['abbr'], b['spoken'], b['slug'], len(b['ch'])] for b in BOOKS]
    (WEB / 'assets').mkdir(exist_ok=True)
    (WEB / 'assets' / 'buecher.js').write_text('window.BUECHER=' + json.dumps(books, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    rows = []
    for bk in BOOKS:
        for c in range(1, len(bk['ch']) + 1):
            for v, t in verses_of(bk, c).items():
                rows.append([bk['n'], c, v, nfc(unstress(t))])
    (WEB / 'assets' / 'suchindex.js').write_text('window.SUCHINDEX=' + json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    (WEB / 'assets' / 'logo.svg').write_text(LOGO.replace('class="logo" ', 'xmlns="http://www.w3.org/2000/svg" ').replace('var(--brand)', '#5b3c88'), encoding='utf-8')
    return len(rows)


def main():
    # alte generierte Seiten entfernen (nur bibel/ – wird vollständig neu erzeugt)
    if (WEB / 'bibel').exists():
        shutil.rmtree(WEB / 'bibel')
    nverse = js_data()
    pages = 0
    for bk in BOOKS:
        book_page(bk)
        pages += 1
        for c in range(1, len(bk['ch']) + 1):
            chapter_page(bk, c)
            pages += 1
    for f in (home, bible_index, themen, lexikon, konkordanz, extras, suche, hinweise):
        f()
    pages += 10
    size = sum(p.stat().st_size for p in WEB.rglob('*.html'))
    print(f'{pages} Seiten erzeugt ({size / 1e6:.1f} MB HTML), Suchindex mit {nverse} Versen')


if __name__ == '__main__':
    main()
