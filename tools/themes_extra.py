"""Zusätzliche Themes der Bibelstudium-Ecke (werden zu assets/themes-extra.css).

Jedes Theme: Schlüssel, Name, Gruppe, Vorschau (Hintergrund, Balken, Stil für „Aa“),
Farb-Token (Reihenfolge siehe P), optionale Schriften/Formen und zusätzliche Regeln.
In den Zusatzregeln steht „&“ für den Theme-Selektor [data-theme="…"].
„Im Stil von“ = angelehnt an Farben, Formen und (freie, ähnliche) Schriften – ohne Logos oder Inhalte.
"""

SANS = '"Noto Sans", Arial, sans-serif'
SERIF = '"Noto Serif", Georgia, serif'
MONO = '"Courier Prime", "Courier New", monospace'

# zusätzliche Google-Fonts-Familien für diese Themes
FONT_FAMILIES = [
    'UnifrakturMaguntia', 'IM+Fell+English:ital@0;1', 'Cinzel:wght@500;700', 'Caveat:wght@500;700',
    'Playfair+Display:wght@700;900', 'VT323', 'Press+Start+2P', 'Space+Grotesk:wght@400;700',
    'Titillium+Web:ital,wght@0,400;0,700;0,900;1,900', 'Montserrat:wght@400;600;800', 'Bebas+Neue', 'Lobster',
    'Inter:wght@400;600;700', 'Nunito:wght@400;700;900', 'Lora:wght@500;700',
]

TOKENS = ['bg', 'bg-alt', 'card', 'text', 'muted', 'line', 'brand', 'brand-dark', 'brand-soft', 'brand-soft-strong',
          'on-brand', 'accent', 'on-accent', 'link', 'hero', 'hero2', 'head', 'on-head', 'mark']


def P(*colors, **kw):
    assert len(colors) == len(TOKENS), colors
    d = dict(zip(TOKENS, colors))
    d.update({k.replace('_', '-'): v for k, v in kw.items()})
    return d


# Für Themes mit heller Startfläche: Text dort dunkel statt weiß
LIGHT_HERO = '''& .hero, & .hero h1 { color: var(--text); } & .hero .lead { color: var(--muted); } & .kicker.light { color: var(--brand); }
& .btn.light { color: var(--text); border-color: var(--text); } & .hero-art path[fill="#fff"] { stroke: var(--text); stroke-width: 2; }'''
NO_TOPLINE = '& .topline { display: none; }'
GRAY_ART = '& .ico, & .hero-art { filter: grayscale(1); }'

THEMES = [
    # ------------------------------------------------------------ Historisch & biblisch
    ('schriftrolle', 'Schriftrolle', 'Historisch & biblisch', '#e9dcc0', '#7a3b16', "font:400 13px 'IM Fell English';color:#3a2a18",
     P('#e9dcc0', '#e2d2b2', '#f2e7cf', '#3a2a18', '#6e5a40', '#c9b48c', '#7a3b16', '#5e2c10', '#ead9b8', '#d6bd8f', '#f7efdd', '#a0522d', '#fff', '#7a3b16', '#6b4a2a', '#8a6238', '#efe3c8', '#3a2a18', '#e8cf8f',
       font=SANS, font_read='"IM Fell English", ' + SERIF, font_head='"IM Fell English", ' + SERIF, r='2px', btn_r='2px', shadow='none'),
     '''& body { background-image: radial-gradient(1200px 500px at 50% 0, rgba(255,255,255,.35), transparent 70%), radial-gradient(800px 600px at 0 100%, rgba(120,80,30,.12), transparent 70%); }
& .topline { background: linear-gradient(90deg, #7a3b16, #c9b48c, #7a3b16); height: 10px; border-radius: 0 0 50% 50%; }
@media (min-width: 1100px) { & .scripture { column-width: 21em; column-gap: 2.4em; column-rule: 1px dotted #a88d60; max-width: none; } }
& .h-off { font-variant: small-caps; text-transform: none; letter-spacing: .06em; font-size: 1.05em; color: #7a3b16; border-bottom: 1px dotted #a88d60; font-family: var(--font-head); }
& .card, & .side-card { box-shadow: inset 0 0 40px rgba(120,80,30,.12); }'''),

    ('tontafel', 'Tontafel', 'Historisch & biblisch', '#b9a088', '#5a3a22', "font:700 12px Cinzel;color:#2b1d12",
     P('#b9a088', '#a98f76', '#c9b29a', '#2b1d12', '#4e3a2a', '#8d735b', '#5a3a22', '#3f2816', '#c4ab92', '#9c7f63', '#f3e6d6', '#7a4a2a', '#fff', '#3f2816', '#6e4c33', '#8a6446', '#c9b29a', '#2b1d12', '#d9c09b',
       font=SANS, font_read=SERIF, font_head='Cinzel, ' + SERIF, r='10px', btn_r='6px', shadow='none'),
     '''& .topline { background: #6e4c33; }
& h1, & h2, & h3, & .block-h, & .h-off { text-shadow: 1px 1px 0 rgba(255,255,255,.3), -1px -1px 0 rgba(0,0,0,.25); }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile { box-shadow: inset 3px 3px 6px rgba(0,0,0,.25), inset -3px -3px 6px rgba(255,255,255,.25); border-color: transparent; }
& .h-off { color: #2b1d12; border-bottom-color: #8d735b; font-family: var(--font-head); }'''),

    ('altdruck', 'Altes Druckbuch', 'Historisch & biblisch', '#f3ecdc', '#9b1b1b', "font:400 15px UnifrakturMaguntia;color:#201812",
     P('#f3ecdc', '#ebe2cc', '#f8f2e4', '#201812', '#5e5240', '#cdbf9f', '#9b1b1b', '#7a1414', '#f0dfd6', '#dcb9ae', '#fff', '#9b1b1b', '#fff', '#9b1b1b', '#2a1f17', '#3a2c20', '#f8f2e4', '#201812', '#ecd9a6',
       font=SANS, font_read='"IM Fell English", ' + SERIF, font_head='UnifrakturMaguntia, "IM Fell English", serif', r='0px', btn_r='0px', shadow='none', head_ls='0'),
     '''& .topline { background: #9b1b1b; height: 4px; }
& h1, & .block-h { font-weight: 400; } & h1::first-letter { color: #9b1b1b; font-size: 1.35em; }
& .h-off { font: 400 1.35em var(--font-head); text-transform: none; letter-spacing: 0; color: #9b1b1b; border-bottom: 0; text-align: center; }
& .h-off.sub { font: italic 1em var(--font-read); color: #201812; } & .h-off.sub::before { display: none; }
& .vn { color: #9b1b1b; } & .scripture { text-align: justify; hyphens: auto; }'''),

    ('stiftshuette', 'Stiftshütte', 'Historisch & biblisch', 'linear-gradient(90deg,#2c4a8c 25%,#5a2a6e 25% 50%,#8c1c2c 50% 75%,#c9a23a 75%)', '#f7f3ea', '',
     P('#f7f3ea', '#efe8d8', '#fffaf0', '#2a2233', '#5f5568', '#ddd2bd', '#2c4a8c', '#223a6e', '#e5ebf6', '#c6d2ea', '#fff', '#c9a23a', '#2a2233', '#2c4a8c', '#5a2a6e', '#8c1c2c', '#fffaf0', '#2a2233', '#f2e3a6'),
     '''& .topline { background: linear-gradient(90deg, #2c4a8c 0 25%, #5a2a6e 25% 50%, #8c1c2c 50% 75%, #c9a23a 75%); height: 8px; }
& .h-off { color: #8c1c2c; border-bottom: 2px solid #c9a23a; } & .vn { color: #5a2a6e; }
& .step-list li::before { background: #c9a23a; }'''),

    # ------------------------------------------------------------ Papier & Schreibgeräte
    ('notizbuch', 'Notizbuch', 'Papier & Schreibgeräte', 'repeating-linear-gradient(0deg,#fff 0 5px,#cfe0f7 5px 6px)', '#2a56c6', "font:700 15px Caveat;color:#2a56c6",
     P('#fdfdf8', '#f4f6fb', '#ffffff', '#23262d', '#5a606b', '#d7e1f2', '#2a56c6', '#1f45a3', '#e8eefb', '#c6d4f2', '#fff', '#fff176', '#23262d', '#2a56c6', '#2a56c6', '#3d6be0', '#fdfdf8', '#23262d', '#fff176',
       font=SANS, font_read=SANS, font_head='Caveat, cursive', r='6px', shadow='0 2px 6px rgba(0,0,0,.08)', head_ls='0'),
     '''& body { background-image: linear-gradient(rgba(120,150,210,.18) 1px, transparent 1px), linear-gradient(90deg, rgba(120,150,210,.18) 1px, transparent 1px); background-size: 22px 22px; }
& h1, & .block-h, & h2 { font-weight: 700; font-size: 1.5em; } & h1 { font-size: clamp(40px, 6vw, 60px); }
& .h-off { font: 700 1.6em var(--font-head); text-transform: none; letter-spacing: 0; color: #2a56c6; border-bottom: 0; }
& .h-off.sub { font-size: 1.3em; color: #c0392b; } & .h-off.sub::before { display: none; }
& .v:target, & mark { background: linear-gradient(104deg, transparent .5%, #fff176 2%, #fff59d 97%, transparent 99%); box-shadow: none; }
& .topline { background: #c0392b; height: 3px; }'''),

    ('karteikarte', 'Karteikarte', 'Papier & Schreibgeräte', '#fffdf6', '#c0392b', '',
     P('#e9e4d8', '#f1ede3', '#fffdf6', '#222222', '#5c5a55', '#d6d0c2', '#c0392b', '#9c2d22', '#f7e3e0', '#e9b9b3', '#fff', '#2e86de', '#fff', '#1f6fbf', '#c0392b', '#d35445', '#fffdf6', '#222222', '#fdf1a9',
       r='3px', btn_r='3px', shadow='0 2px 4px rgba(0,0,0,.12)'),
     '''& .card, & .side-card, & .entry, & .res { border-top: 4px solid #c0392b; background-image: repeating-linear-gradient(#fffdf6 0 27px, #cfe3f5 27px 28px); }
& .scripture p { background: #fffdf6 repeating-linear-gradient(transparent 0 calc(var(--fs) * var(--lh, 1.8) - 1px), #cfe3f5 0 calc(var(--fs) * var(--lh, 1.8))); border-top: 4px solid #c0392b; padding: 10px 16px; box-shadow: 0 2px 4px rgba(0,0,0,.12); }
& .scripture p.q { padding-left: 2em; }
& .entry { padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,.12); }'''),

    ('zeitung', 'Zeitung', 'Papier & Schreibgeräte', '#f4f1ea', '#111', "font:900 13px 'Playfair Display';color:#111",
     P('#f4f1ea', '#ebe7dc', '#f9f7f1', '#111111', '#4a4a4a', '#111111', '#111111', '#000000', '#e6e2d6', '#c9c4b6', '#f9f7f1', '#111111', '#f9f7f1', '#111111', '#f4f1ea', '#f4f1ea', '#f4f1ea', '#111111', '#e8e2c6',
       font=SANS, font_read=SERIF, font_head='"Playfair Display", ' + SERIF, r='0px', btn_r='0px', shadow='none', head_ls='-.01em'),
     LIGHT_HERO + '''
& .topline { height: 0; } & .site-head { border-bottom: 4px double #111; }
& .brand { font-family: var(--font-head); font-size: 24px; font-weight: 900; }
& h1 { font-weight: 900; font-size: clamp(36px, 6vw, 64px); } & .block-h { font-weight: 900; }
& .hero { border-bottom: 4px double #111; } & .card { border: 1px solid #111; }
& .h-off { font: 900 1.1em var(--font-head); text-transform: uppercase; letter-spacing: .04em; color: #111; border-top: 2px solid #111; border-bottom: 1px solid #111; padding: 4px 0; text-align: center; }
& .scripture { text-align: justify; hyphens: auto; }
@media (min-width: 900px) { & .scripture { column-count: 2; column-gap: 2em; column-rule: 1px solid #111; max-width: none; } }
@media (min-width: 1300px) { & .scripture { column-count: 3; } }'''),

    ('blaupause', 'Blaupause', 'Papier & Schreibgeräte', '#0d3b66', '#fff', "font:700 12px 'Space Grotesk';color:#fff",
     P('#0d3b66', '#114778', '#0f416f', '#eaf3ff', '#b9d3f0', '#8fb4dc', '#ffffff', '#dbe9ff', '#164f85', '#3d6fa3', '#0d3b66', '#ffffff', '#0d3b66', '#ffffff', '#0d3b66', '#0d3b66', '#0d3b66', '#eaf3ff', '#2b6299',
       font='"Space Grotesk", ' + SANS, font_read='"Space Grotesk", ' + SANS, font_head='"Space Grotesk", ' + SANS, r='0px', btn_r='0px', shadow='none', head_ls='.06em', logo_book='#0d3b66', logo_spine='#fff'),
     '''& { color-scheme: dark; }
& body { background-image: linear-gradient(rgba(255,255,255,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px), linear-gradient(rgba(255,255,255,.12) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.12) 1px, transparent 1px); background-size: 20px 20px, 20px 20px, 100px 100px, 100px 100px; }
& h1, & h2, & .block-h { text-transform: uppercase; font-weight: 700; }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .res { background: transparent; border: 1px dashed #b9d3f0; }
& .hero { border-bottom: 1px dashed #b9d3f0; } & .topline { background: #fff; height: 2px; }
& .h-off { color: #fff; border-bottom: 1px dashed #fff; } & .vn { color: #ffd66b; }'''),

    # ------------------------------------------------------------ Technik & Retro
    ('terminal', 'Terminal', 'Technik & Retro', '#000', '#33ff66', "font:400 18px VT323;color:#33ff66",
     P('#000000', '#050f07', '#020a04', '#33ff66', '#1fae46', '#1f7a3a', '#33ff66', '#7dff9e', '#062b12', '#0e5524', '#000000', '#33ff66', '#000000', '#7dff9e', '#000000', '#000000', '#000000', '#33ff66', '#0e5524',
       font='VT323, monospace', font_read='VT323, monospace', font_head='VT323, monospace', r='0px', btn_r='0px', shadow='none', head_ls='.02em', fs='24px', logo_book='#000', logo_spine='#33ff66'),
     '''& { color-scheme: dark; } & body { font-size: 20px; text-shadow: 0 0 4px rgba(51,255,102,.55); }
& body::after { content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 90; background: repeating-linear-gradient(0deg, rgba(0,0,0,.25) 0 1px, transparent 1px 3px); }
& h1::after { content: "█"; margin-left: .15em; animation: blink 1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .res, & .qs, & .theme-btn { border: 1px solid #33ff66; background: #000; }
& .h-off { color: #33ff66; border-bottom: 1px dashed #33ff66; } & .h-off::before { content: "> "; }
& .kicker::before { content: "$ "; } & .hero { border-bottom: 1px solid #33ff66; } & .topline { background: #33ff66; height: 2px; }'''),

    ('ereader', 'E-Reader', 'Technik & Retro', '#f2f2ef', '#1a1a1a', "font:400 13px 'Noto Serif';color:#1a1a1a",
     P('#f2f2ef', '#e9e9e5', '#f2f2ef', '#1a1a1a', '#555555', '#bdbdbd', '#1a1a1a', '#000000', '#e2e2de', '#c4c4bf', '#f2f2ef', '#1a1a1a', '#f2f2ef', '#1a1a1a', '#3a3a3a', '#3a3a3a', '#f2f2ef', '#1a1a1a', '#d6d6d1',
       font=SANS, font_read=SERIF, font_head=SERIF, r='2px', btn_r='2px', shadow='none'),
     NO_TOPLINE + '\n' + GRAY_ART + '''
& *, & *::before, & *::after { transition: none !important; animation: none !important; }
& .h-off { color: #1a1a1a; text-transform: none; letter-spacing: 0; border-bottom: 1px solid #bdbdbd; }'''),

    ('pixel', 'Pixel / 8-Bit', 'Technik & Retro', '#1d1d3b', '#ff4f9a', "font:400 9px 'Press Start 2P';color:#ffd23f",
     P('#1d1d3b', '#26264d', '#2a2a55', '#f8f8f8', '#b9b9e0', '#f8f8f8', '#ff4f9a', '#ff7ab5', '#3a2a5c', '#6a3a7a', '#1d1d3b', '#ffd23f', '#1d1d3b', '#7ee8fa', '#1d1d3b', '#2d1d5b', '#1d1d3b', '#f8f8f8', '#5a3a7a',
       font='VT323, monospace', font_read='VT323, monospace', font_head='"Press Start 2P", monospace', r='0px', btn_r='0px', shadow='4px 4px 0 #000', head_ls='0', fs='24px'),
     '''& { color-scheme: dark; } & body { font-size: 20px; }
& h1 { font-size: clamp(20px, 3vw, 30px); line-height: 1.5; } & h2, & .block-h { font-size: 16px; line-height: 1.6; } & .brand { font-family: var(--font-head); font-size: 11px; }
& .topline { background: repeating-linear-gradient(90deg, #ff4f9a 0 16px, #ffd23f 16px 32px, #7ee8fa 32px 48px, #7cff6b 48px 64px); height: 8px; }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .btn, & .res, & .qs { border: 4px solid #f8f8f8; box-shadow: 4px 4px 0 #000; }
& .h-off { font: 400 13px var(--font-head); color: #ffd23f; border-bottom: 4px solid #ff4f9a; line-height: 1.6; }
& .h-off.sub { font-size: 11px; color: #7ee8fa; } & .vn { color: #ffd23f; }'''),

    ('fernschreiber', 'Fernschreiber', 'Technik & Retro', 'repeating-linear-gradient(0deg,#f5f2e6 0 6px,#dfead9 6px 12px)', '#222', "font:700 12px 'Courier Prime';color:#222",
     P('#f5f2e6', '#ece8d8', '#f8f6ec', '#222222', '#555555', '#222222', '#222222', '#000000', '#e6e2d2', '#c8c3ae', '#f8f6ec', '#c0392b', '#fff', '#222222', '#f5f2e6', '#f5f2e6', '#f8f6ec', '#222222', '#dfead9',
       font=MONO, font_read=MONO, font_head=MONO, r='0px', btn_r='0px', shadow='none', head_ls='.08em'),
     LIGHT_HERO + '''
& body { text-transform: uppercase; letter-spacing: .03em; background-image: radial-gradient(circle at 14px 12px, #d9d4c0 5px, transparent 6px), radial-gradient(circle at calc(100% - 14px) 12px, #d9d4c0 5px, transparent 6px), repeating-linear-gradient(0deg, rgba(150,200,150,.18) 0 48px, transparent 48px 96px); background-size: 100% 24px, 100% 24px, auto; background-repeat: repeat-y, repeat-y, repeat; }
& .topline { height: 0; } & .site-head, & .hero, & .site-foot { border-color: #222; }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .res { border: 1px solid #222; background: transparent; }
& .h-off { color: #222; border-bottom: 1px dashed #222; } & .h-off::before { content: "+++ "; } & .h-off::after { content: " +++"; }
& .vn { color: #c0392b; }'''),

    # ------------------------------------------------------------ Stimmungen
    ('morgenandacht', 'Morgenandacht', 'Stimmungen', 'linear-gradient(#f6c9b0,#fff8f3)', '#d9826b', '',
     P('#fff8f3', '#fdeee4', '#ffffff', '#3a2f2f', '#7a6563', '#f1dcd2', '#c46f56', '#a85c46', '#fbe6dd', '#f2c6b5', '#fff', '#f3d27a', '#3a2f2f', '#b5604a', '#a9543a', '#c4704f', '#ffffff', '#3a2f2f', '#fbe2b8'),
     '& .topline { background: linear-gradient(90deg, #f6c9b0, #f3d27a, #c9dcf0); }'),

    ('abendlicht', 'Abendlicht', 'Stimmungen', '#22170f', '#f0a05a', '',
     P('#22170f', '#2d1f14', '#2b1e14', '#f3dcc0', '#c7a47e', '#4a3524', '#f0a05a', '#ffb86b', '#3d2a1a', '#6b4626', '#22170f', '#ffb86b', '#22170f', '#f6b77a', '#3a2414', '#5a3418', '#22170f', '#f3dcc0', '#5c3b1c'),
     '& { color-scheme: dark; } & .topline { background: linear-gradient(90deg, #8a3a14, #f0a05a, #ffd08a); }'),

    ('sternenhimmel', 'Sternenhimmel', 'Stimmungen', 'radial-gradient(circle at 30% 30%,#fff 1px,transparent 2px),radial-gradient(circle at 70% 60%,#fff 1px,transparent 2px),#0b1030', '#ffd86b', '',
     P('#0b1030', '#121a45', '#141a46', '#e8ecff', '#aab3e0', '#2b3466', '#ffd86b', '#ffe59a', '#1c2560', '#3a4590', '#0b1030', '#ffd86b', '#0b1030', '#ffe59a', '#0b1030', '#1c2560', '#0b1030', '#e8ecff', '#3a4590', logo_book='#0b1030'),
     '''& { color-scheme: dark; }
& body { background-image: radial-gradient(1.2px 1.2px at 20px 30px, #fff, transparent), radial-gradient(1px 1px at 120px 80px, #fff, transparent), radial-gradient(1.5px 1.5px at 200px 160px, #ffe59a, transparent), radial-gradient(1px 1px at 300px 40px, #cdd6ff, transparent), radial-gradient(1px 1px at 80px 220px, #fff, transparent), radial-gradient(1.3px 1.3px at 260px 250px, #fff, transparent); background-size: 340px 300px; background-attachment: fixed; }
& .card, & .side-card { background: rgba(20,26,70,.85); } & .topline { background: linear-gradient(90deg, #0b1030, #ffd86b, #0b1030); }'''),

    ('garten', 'Garten', 'Stimmungen', '#fbfdf7', 'linear-gradient(90deg,#5b8c3a,#f4a6b8)', '',
     P('#fbfdf7', '#eef6e6', '#ffffff', '#263022', '#5f6d58', '#d9e8cd', '#4f7f31', '#3f6627', '#e6f1db', '#c4dfab', '#fff', '#f4a6b8', '#263022', '#3f6627', '#5b8c3a', '#8fbf5a', '#ffffff', '#263022', '#fde3ea'),
     '& .topline { background: repeating-linear-gradient(90deg, #5b8c3a 0 30px, #f4a6b8 30px 40px, #8fbf5a 40px 70px, #ffd166 70px 80px); }'),

    # ------------------------------------------------------------ Für die Augen
    ('graustufen', 'Graustufen', 'Für die Augen', '#f2f2f2', '#333', '',
     P('#f2f2f2', '#e6e6e6', '#fafafa', '#1c1c1c', '#555555', '#c8c8c8', '#333333', '#111111', '#e0e0e0', '#bdbdbd', '#fafafa', '#333333', '#fafafa', '#111111', '#3a3a3a', '#4a4a4a', '#fafafa', '#1c1c1c', '#d6d6d6'),
     GRAY_ART + '\n& .topline { background: #333; }'),

    ('bernstein', 'Bernstein auf Schwarz', 'Für die Augen', '#0d0a05', '#ffb000', "font:800 13px sans-serif;color:#ffb000",
     P('#0d0a05', '#17110a', '#120d07', '#ffb000', '#d18f00', '#6b4a00', '#ffb000', '#ffc640', '#2a1d05', '#5c3f00', '#0d0a05', '#ffb000', '#0d0a05', '#ffc640', '#0d0a05', '#0d0a05', '#0d0a05', '#ffb000', '#4a3300',
       shadow='none', logo_book='#0d0a05', logo_spine='#ffb000'),
     '& { color-scheme: dark; } & .hero h1, & .hero .lead { color: #ffb000; } & .btn.light { color: #ffb000; border-color: #ffb000; } & .hero { border-bottom: 2px solid #6b4a00; }'),

    ('grossdruck', 'Großdruck', 'Für die Augen', '#fff', '#111', "font:800 16px 'Atkinson Hyperlegible';color:#111",
     P('#ffffff', '#f2f2f2', '#ffffff', '#111111', '#333333', '#111111', '#1f3f8a', '#14306e', '#e6ecf7', '#b9c8e6', '#fff', '#ffd400', '#111111', '#1f3f8a', '#1f3f8a', '#1f3f8a', '#ffffff', '#111111', '#ffe866',
       font='"Atkinson Hyperlegible", ' + SANS, font_read='"Atkinson Hyperlegible", ' + SANS, font_head='"Atkinson Hyperlegible", ' + SANS, fs='30px', lh='2', shadow='none', head_ls='0'),
     '''& body { font-size: 19px; } & .main-nav a { font-size: 18px; } & .btn { font-size: 18px; padding: 14px 26px; }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .res, & .qs { border: 2px solid #111; }
& .h-off { font-size: 22px; color: #111; border-bottom: 3px solid #111; } & .h-off.sub { font-size: 20px; }
& .toc a { font-size: 17px; } & .vn { font-size: .7em; } & a { text-decoration-thickness: 2px; }'''),

    ('dunkelgruen', 'Dunkelgrün', 'Für die Augen', '#12251c', '#d8c48a', '',
     P('#12251c', '#183026', '#163024', '#f1e9d2', '#c9c0a6', '#2f4a3d', '#cfe3b0', '#e2efcc', '#1f3a2d', '#3a5a47', '#12251c', '#d8c48a', '#12251c', '#e6d9a8', '#12251c', '#1f3a2d', '#12251c', '#f1e9d2', '#3b5a3f',
       shadow='none', logo_book='#12251c', logo_spine='#cfe3b0'),
     '& { color-scheme: dark; } & .topline { background: #2f4a3d; }'),

    # ------------------------------------------------------------ Im Stil von (angelehnt, ohne Logos)
    ('cocacola', 'Coca-Cola', 'Im Stil von', '#f40009', '#fff', "font:400 14px Lobster;color:#fff",
     P('#ffffff', '#f7f7f7', '#ffffff', '#1e1e1e', '#5a5a5a', '#e6e6e6', '#f40009', '#c4000a', '#fde6e7', '#f9b3b6', '#fff', '#ffffff', '#f40009', '#d1000b', '#f40009', '#c4000a', '#f40009', '#ffffff', '#ffd9db',
       font='Montserrat, ' + SANS, font_read=SERIF, font_head='Montserrat, ' + SANS, r='14px', logo_book='#f40009', logo_spine='#fff'),
     '''& .site-head .logo rect { fill: #fff; } & .qs button { background: #fff; color: #f40009; } & .main-nav a[aria-current] { color: #fff; border-color: #fff; }
& .brand, & h1 { font-family: Lobster, cursive; font-weight: 400; } & .hero h1 { font-size: clamp(40px, 6vw, 72px); }
& .hero { border-radius: 0 0 50% 50% / 0 0 60px 60px; } & .topline { background: #fff; }
& .btn.accent { color: #f40009; } & .h-off { color: #f40009; border-bottom-color: #f40009; } & .site-foot .logo path[fill] { fill: #fff; }'''),

    ('formel1', 'Formel 1', 'Im Stil von', '#15151e', '#e10600', "font:900 italic 13px 'Titillium Web';color:#fff",
     P('#15151e', '#1f1f27', '#1f1f27', '#ffffff', '#b6b6c0', '#38383f', '#e10600', '#ff2a1f', '#2a1414', '#5a1a1a', '#ffffff', '#ffffff', '#15151e', '#ff4a3f', '#15151e', '#2a0a0a', '#15151e', '#ffffff', '#5a1a1a',
       font='"Titillium Web", ' + SANS, font_read='"Titillium Web", ' + SANS, font_head='"Titillium Web", ' + SANS, r='4px', btn_r='0px', head_ls='0'),
     '''& { color-scheme: dark; }
& .topline { height: 10px; background: repeating-conic-gradient(#fff 0 25%, #15151e 0 50%) 0 0 / 10px 10px; }
& h1, & h2, & .block-h, & .h-off, & .main-nav a, & .btn, & .brand { font-style: italic; font-weight: 900; text-transform: uppercase; }
& .btn { transform: skewX(-12deg); } & .btn:hover { transform: skewX(-12deg) translateY(-1px); }
& .hero { background: linear-gradient(110deg, #15151e 55%, #e10600 55% 58%, #15151e 58%); }
& .h-off { color: #fff; border-bottom: 3px solid #e10600; } & .vn { color: #e10600; }
& .card, & .side-card { border-left: 4px solid #e10600; }'''),

    ('spotify', 'Spotify', 'Im Stil von', '#121212', '#1db954', "font:800 13px Montserrat;color:#1db954",
     P('#121212', '#181818', '#181818', '#ffffff', '#b3b3b3', '#2a2a2a', '#1db954', '#1ed760', '#1f3326', '#2f5a3e', '#000000', '#1db954', '#000000', '#1ed760', '#1db954', '#121212', '#000000', '#ffffff', '#2f5a3e',
       font='Montserrat, ' + SANS, font_read=SANS, font_head='Montserrat, ' + SANS, r='8px', btn_r='500px', shadow='none', head_ls='-.02em'),
     '''& { color-scheme: dark; } & .topline { background: #1db954; height: 3px; }
& h1, & .block-h { font-weight: 800; } & .hero { background: linear-gradient(180deg, #1a6b3a, #121212 95%); }
& .topic-tile:hover, & .book-tile:hover { background: #282828; } & .h-off { color: #fff; text-transform: none; letter-spacing: -.01em; font-size: 20px; border: 0; }'''),

    ('netflix', 'Netflix', 'Im Stil von', '#141414', '#e50914', "font:400 16px 'Bebas Neue';color:#e50914",
     P('#141414', '#1f1f1f', '#1f1f1f', '#ffffff', '#b3b3b3', '#333333', '#e50914', '#f6121d', '#2a0d0f', '#5a1418', '#ffffff', '#e50914', '#ffffff', '#ffffff', '#000000', '#141414', '#000000', '#ffffff', '#5a1418',
       font=SANS, font_read=SANS, font_head='"Bebas Neue", ' + SANS, r='4px', btn_r='4px', shadow='none', head_ls='.03em'),
     '''& { color-scheme: dark; } & .topline { display: none; }
& h1, & h2, & .block-h, & .brand { font-weight: 400; } & .hero h1 { font-size: clamp(44px, 7vw, 84px); }
& .brand { color: #e50914; font-family: var(--font-head); font-size: 28px; letter-spacing: .04em; }
& .hero { background: linear-gradient(90deg, #000 30%, rgba(229,9,20,.35)); }
& .topic-tile:hover, & .book-tile:hover { transform: scale(1.05); background: #2a2a2a; }
& .h-off { font: 400 24px var(--font-head); color: #fff; letter-spacing: .04em; border-bottom: 2px solid #e50914; }'''),

    ('nintendo', 'Nintendo', 'Im Stil von', '#fff', '#e60012', "font:900 13px Nunito;color:#e60012",
     P('#ffffff', '#f3f3f3', '#ffffff', '#222222', '#5f5f5f', '#e3e3e3', '#e60012', '#c10010', '#fde5e7', '#f8b4b9', '#fff', '#e60012', '#fff', '#e60012', '#e60012', '#ff3b47', '#ffffff', '#222222', '#ffe3e5',
       font='Nunito, ' + SANS, font_read='Nunito, ' + SANS, font_head='Nunito, ' + SANS, r='18px', btn_r='999px', shadow='0 4px 14px rgba(0,0,0,.08)', head_ls='0'),
     '''& .topline { background: #e60012; height: 6px; } & h1, & .block-h { font-weight: 900; }
& .card, & .topic-tile, & .book-tile { border: 3px solid #e3e3e3; } & .btn { font-weight: 900; }
& .h-off { color: #e60012; text-transform: none; letter-spacing: 0; font-size: 19px; font-weight: 900; border-bottom: 3px solid #fde5e7; }'''),

    ('starbucks', 'Starbucks', 'Im Stil von', '#1e3932', '#cba258', "font:700 13px Lora;color:#fff",
     P('#f2f0eb', '#e8e4da', '#ffffff', '#1e1e1e', '#5c5c5c', '#dcd7cb', '#00704a', '#1e3932', '#d4e9e2', '#a8d1c2', '#fff', '#cba258', '#1e3932', '#00704a', '#1e3932', '#00704a', '#ffffff', '#1e3932', '#f1e3c2',
       font='Montserrat, ' + SANS, font_read=SERIF, font_head='Lora, ' + SERIF, r='12px', btn_r='50px', head_ls='-.01em'),
     '''& .topline { background: #00704a; } & .btn.primary { background: #00704a; } & .btn.accent { background: #cba258; color: #1e3932; }
& .h-off { color: #1e3932; text-transform: none; letter-spacing: 0; font: 700 20px var(--font-head); border-bottom: 2px solid #d4e9e2; }'''),

    ('nasa', 'NASA', 'Im Stil von', '#0b0f1a', '#fc3d21', "font:700 12px 'Space Grotesk';color:#fff",
     P('#0b0f1a', '#121827', '#121827', '#ffffff', '#aeb6c8', '#28304a', '#fc3d21', '#ff5a40', '#1d2340', '#3a2a40', '#ffffff', '#fc3d21', '#ffffff', '#8fb3ff', '#0b3d91', '#05173d', '#0b0f1a', '#ffffff', '#33406b',
       font='"Space Grotesk", ' + SANS, font_read=SANS, font_head='"Space Grotesk", ' + SANS, r='2px', btn_r='2px', shadow='none', head_ls='.08em', logo_book='#fff', logo_spine='#fc3d21'),
     '''& { color-scheme: dark; } & .site-head .logo rect { fill: #0b3d91; }
& h1, & h2, & .block-h, & .main-nav a, & .kicker { text-transform: uppercase; letter-spacing: .1em; font-weight: 700; }
& .topline { background: linear-gradient(90deg, #0b3d91 70%, #fc3d21 70%); }
& .h-off { color: #fff; border-bottom: 2px solid #fc3d21; letter-spacing: .12em; }'''),

    ('youtube', 'YouTube', 'Im Stil von', '#fff', '#ff0000', "font:500 13px Roboto;color:#0f0f0f",
     P('#ffffff', '#f2f2f2', '#ffffff', '#0f0f0f', '#606060', '#e5e5e5', '#ff0000', '#cc0000', '#ffe5e5', '#ffb3b3', '#fff', '#ff0000', '#fff', '#065fd4', '#0f0f0f', '#272727', '#ffffff', '#0f0f0f', '#fff1a8',
       font='Roboto, Arial, sans-serif', font_read='Roboto, Arial, sans-serif', font_head='Roboto, Arial, sans-serif', r='12px', btn_r='18px', shadow='none', head_ls='0'),
     '''& .topline { display: none; } & .site-head .logo rect { fill: #ff0000; rx: 9; }
& .main-nav { gap: 8px; padding-bottom: 8px; } & .main-nav a { background: #f2f2f2; border: 0; border-radius: 8px; padding: 6px 12px; font-weight: 500; }
& .main-nav a[aria-current] { background: #0f0f0f; color: #fff; }
& .qs { background: #fff; border-color: #ccc; } & .qs button { background: #f8f8f8; color: #0f0f0f; border-left: 1px solid #ccc; }
& h1, & .block-h { font-weight: 700; } & .h-off { text-transform: none; letter-spacing: 0; font-size: 18px; font-weight: 700; color: #0f0f0f; border: 0; }'''),

    ('amazon', 'Amazon', 'Im Stil von', '#131921', '#ff9900', "font:700 13px Arial;color:#fff",
     P('#eaeded', '#f7f8f8', '#ffffff', '#0f1111', '#565959', '#d5d9d9', '#232f3e', '#131921', '#e7eef2', '#c7d4dc', '#fff', '#ff9900', '#0f1111', '#007185', '#232f3e', '#37475a', '#131921', '#ffffff', '#fdeec4',
       font='Arial, "Amazon Ember", sans-serif', font_read='Arial, sans-serif', font_head='Arial, sans-serif', r='8px', btn_r='20px', shadow='0 2px 5px rgba(15,17,17,.15)', head_ls='0', logo_spine='#ff9900'),
     '''& .topline { display: none; } & .site-head .logo rect { fill: #ff9900; } & .site-head .logo path[fill] { fill: #131921; }
& .main-nav { background: #232f3e; max-width: none; padding-left: max(20px, calc((100% - 1160px) / 2)); }
& .main-nav a { color: #fff; font-weight: 400; } & .main-nav a[aria-current] { border-color: #ff9900; color: #fff; }
& .qs { background: #fff; border: 0; } & .qs button { background: #febd69; color: #0f1111; }
& .btn.primary { background: #ffd814; color: #0f1111; } & .btn.primary:hover { background: #f7ca00; } & .btn.accent { background: #ffa41c; color: #0f1111; }
& .h-off { color: #c45500; text-transform: none; letter-spacing: 0; font-size: 18px; border-bottom: 1px solid #d5d9d9; }'''),

    ('instagram', 'Instagram', 'Im Stil von', 'linear-gradient(45deg,#fcb045,#fd1d1d,#833ab4)', '#fff', "font:700 13px Inter;color:#fff",
     P('#ffffff', '#fafafa', '#ffffff', '#262626', '#737373', '#dbdbdb', '#d62976', '#b01e62', '#fde7f1', '#f7b8d4', '#fff', '#fcb045', '#262626', '#00376b', '#833ab4', '#fd1d1d', '#ffffff', '#262626', '#fde2ec',
       font='Inter, ' + SANS, font_read='Inter, ' + SANS, font_head='Inter, ' + SANS, r='12px', btn_r='8px', shadow='none', head_ls='-.01em'),
     '''& .topline { background: linear-gradient(90deg, #833ab4, #fd1d1d, #fcb045); }
& .hero { background: linear-gradient(90deg, #6a2c95, #b4235a 55%, #e0602a); }
& .site-head .logo rect { fill: #d62976; }
& .btn.primary { background: linear-gradient(45deg, #fd1d1d, #833ab4); }
& .h-off { color: #262626; text-transform: none; letter-spacing: 0; font-size: 18px; border-bottom: 1px solid #dbdbdb; }'''),

    ('wikipedia', 'Wikipedia', 'Im Stil von', '#f8f9fa', '#3366cc', "font:400 15px 'Linux Libertine',Georgia;color:#202122",
     P('#f8f9fa', '#f8f9fa', '#ffffff', '#202122', '#54595d', '#a2a9b1', '#3366cc', '#2a4b8d', '#eaf3ff', '#c8d8f5', '#fff', '#3366cc', '#fff', '#3366cc', '#eaecf0', '#eaecf0', '#ffffff', '#202122', '#fef6e7',
       font='Arial, "Helvetica Neue", sans-serif', font_read='Arial, sans-serif', font_head='"Linux Libertine", "Georgia", "Times", serif', r='2px', btn_r='2px', shadow='none', head_ls='0'),
     LIGHT_HERO + '''
& .topline { display: none; } & body { font-size: 15px; }
& h1, & .block-h, & h2 { font-weight: 400; border-bottom: 1px solid #a2a9b1; padding-bottom: 4px; }
& .hero { border-bottom: 1px solid #a2a9b1; } & .card { border-color: #a2a9b1; }
& .h-off { font: 400 1.3em var(--font-head); text-transform: none; letter-spacing: 0; color: #202122; border-bottom: 1px solid #a2a9b1; }
& .h-off.sub { font: 700 1em var(--font); } & .h-off.sub::before { display: none; }
& .vn { color: #3366cc; }'''),

    ('notion', 'Notion', 'Im Stil von', '#fff', '#37352f', "font:700 13px Inter;color:#37352f",
     P('#ffffff', '#f7f6f3', '#ffffff', '#37352f', '#787774', '#e9e9e7', '#37352f', '#191919', '#f1f1ef', '#e3e2e0', '#fff', '#2383e2', '#fff', '#37352f', '#f7f6f3', '#f7f6f3', '#ffffff', '#37352f', '#fbf3db',
       font='Inter, ' + SANS, font_read='Inter, ' + SANS, font_head='Inter, ' + SANS, r='4px', btn_r='4px', shadow='none', head_ls='-.01em'),
     LIGHT_HERO + '\n' + NO_TOPLINE + '''
& h1 { font-weight: 700; } & .block-h { font-weight: 600; } & a { text-decoration-color: rgba(55,53,47,.4); }
& .card, & .topic-tile, & .book-tile { border: 1px solid #e9e9e7; background: #fff; } & .topic-tile:hover, & .book-tile:hover { background: #f7f6f3; transform: none; border-color: #e9e9e7; }
& .h-off { text-transform: none; letter-spacing: 0; font-size: 1.25em; font-weight: 600; color: #37352f; border: 0; }
& .h-off.sub::before { content: "▸"; background: none; width: auto; height: auto; color: #787774; }'''),

    ('windows95', 'Windows 95', 'Im Stil von', '#008080', '#c0c0c0', "font:700 12px Tahoma;color:#000",
     P('#008080', '#c0c0c0', '#c0c0c0', '#000000', '#3c3c3c', '#808080', '#000080', '#000060', '#d4d0c8', '#a0a0a0', '#ffffff', '#000080', '#ffffff', '#000080', '#000080', '#1084d0', '#c0c0c0', '#000000', '#000080',
       font='Tahoma, "MS Sans Serif", Arial, sans-serif', font_read='Tahoma, Arial, sans-serif', font_head='Tahoma, "MS Sans Serif", Arial, sans-serif', r='0px', btn_r='0px', shadow='none', head_ls='0'),
     '''& .topline { display: none; } & .site-head { border-bottom: 2px solid #808080; }
& .card, & .side-card, & .topic-tile, & .book-tile, & .num-tile, & .btn, & .theme-btn, & .res, & .settings-card {
  border: 0; box-shadow: inset -1px -1px #0a0a0a, inset 1px 1px #ffffff, inset -2px -2px #808080, inset 2px 2px #dfdfdf; background: #c0c0c0; color: #000; }
& .btn.primary, & .btn.accent, & .btn.light { background: #c0c0c0; color: #000; } & .btn:active { box-shadow: inset 1px 1px #0a0a0a, inset -1px -1px #fff, inset 2px 2px #808080; }
& .card > h2:first-child { margin: -26px -26px 14px; padding: 4px 8px; background: linear-gradient(90deg, #000080, #1084d0); color: #fff; font-size: 14px; font-weight: 700; }
& .qs, & .filter, & .bigsearch input { border-radius: 0; box-shadow: inset 1px 1px #808080, inset 2px 2px #0a0a0a, inset -1px -1px #fff; border: 0; background: #fff; }
& .reader-main { background: #fff; padding: 20px 26px; box-shadow: inset 1px 1px #808080, inset 2px 2px #0a0a0a, inset -1px -1px #fff, inset -2px -2px #dfdfdf; }
& .hero { background: #008080; } & .main-nav a[aria-current] { color: #000080; border-color: #000080; }
& .h-off { color: #000080; text-transform: none; letter-spacing: 0; font-size: 16px; border-bottom: 1px solid #808080; }
& .verse-card { background: #fff; border-left: 0; box-shadow: inset 1px 1px #808080, inset -1px -1px #fff; }'''),

    ('word', 'Microsoft Word', 'Im Stil von', '#2b579a', '#fff', "font:700 13px Calibri,Arial;color:#fff",
     P('#e6e6e6', '#f3f3f3', '#ffffff', '#000000', '#555555', '#c6c6c6', '#2b579a', '#1e3f73', '#dde6f4', '#b6c8e6', '#fff', '#2b579a', '#fff', '#0563c1', '#2b579a', '#2b579a', '#2b579a', '#ffffff', '#ffff00',
       font='Calibri, Aptos, Carlito, Arial, sans-serif', font_read='Calibri, Aptos, Carlito, Arial, sans-serif', font_head='"Calibri Light", Calibri, Aptos, Carlito, Arial, sans-serif', r='2px', btn_r='2px', shadow='none', head_ls='0', logo_book='#2b579a', logo_spine='#fff'),
     '''& .topline { display: none; } & .site-head .logo rect { fill: #fff; } & .main-nav a[aria-current] { color: #fff; border-color: #fff; }
& .qs { background: #fff; } & .qs button { background: #1e3f73; }
& .reader-main { background: #fff; padding: 72px 80px; box-shadow: 0 0 0 1px #c6c6c6, 0 2px 10px rgba(0,0,0,.18); max-width: 21cm;
  background-image: linear-gradient(90deg, #f3f3f3, #f3f3f3); background-size: 100% 22px; background-repeat: no-repeat; }
& .block-h { font-weight: 400; color: #2f5496; } & h1 { font-weight: 400; } & .chapter-head h1 { color: #2f5496; }
& .h-off { font: 400 1.25em var(--font-head); text-transform: none; letter-spacing: 0; color: #2f5496; border: 0; }
& .h-off.sub { color: #1f3763; } & .h-off.sub::before { display: none; }
& .v:target { background: #ffff00; box-shadow: none; }'''),
]

GROUP_ORDER = ['Automatisch', 'Klassisch', 'Historisch & biblisch', 'Papier & Schreibgeräte', 'Technik & Retro', 'Im Stil von', 'Natur', 'Stimmungen', 'Jahreszeiten', 'Für die Augen']


def css():
    out = ['/* Automatisch erzeugt aus tools/themes_extra.py – bitte dort ändern. */']
    for key, label, group, bg, bar, aa, tokens, extra in THEMES:
        sel = f'[data-theme="{key}"]'
        out.append(sel + ' { ' + ' '.join(f'--{k}: {v};' for k, v in tokens.items()) + ' }')
        if extra:
            out.append(extra.replace('&', sel))
    return '\n'.join(out) + '\n'


def buttons_by_group():
    groups = {}
    for key, label, group, bg, bar, aa, tokens, extra in THEMES:
        groups.setdefault(group, []).append((key, label, bg, bar, aa))
    return groups
