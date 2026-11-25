"""Erzeugt website/build/bibel.json aus den RTF-Dateien im Ordner Bibelprojekt.

Aufruf (aus dem Ordner Bibelprojekt):
    python -I website/tools/build_data.py

Die Original-RTF-Dateien werden nur gelesen, nie verändert.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from rtfruns import paragraphs, plain  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]          # .../Bibelprojekt
OUT = ROOT / 'website' / 'build' / 'bibel.json'

# (Anzeigename, gesprochener Name wie in den Verweisen, Abkürzung)
BOOKS = [
    ('1. Mose', 'erster Mose', '1Mo'), ('2. Mose', 'zweiter Mose', '2Mo'), ('3. Mose', 'dritter Mose', '3Mo'),
    ('4. Mose', 'vierter Mose', '4Mo'), ('5. Mose', 'fünfter Mose', '5Mo'), ('Josua', 'Josua', 'Jos'),
    ('Richter', 'Richter', 'Ri'), ('Ruth', 'Ruth', 'Ru'), ('1. Samuel', 'erster Samuel', '1Sa'),
    ('2. Samuel', 'zweiter Samuel', '2Sa'), ('1. Könige', 'erster Könige', '1Kö'), ('2. Könige', 'zweiter Könige', '2Kö'),
    ('1. Chronika', 'erster Chronika', '1Ch'), ('2. Chronika', 'zweiter Chronika', '2Ch'), ('Esra', 'Esra', 'Esr'),
    ('Nehemia', 'Nehemia', 'Ne'), ('Esther', 'Esther', 'Est'), ('Hiob', 'Hiob', 'Hi'), ('Psalmen', 'Psalm', 'Ps'),
    ('Sprüche', 'Sprüche', 'Spr'), ('Prediger', 'Prediger', 'Pr'), ('Hohes Lied', 'Hohes Lied', 'Hoh'),
    ('Jesaja', 'Jesaja', 'Jes'), ('Jeremia', 'Jeremia', 'Jer'), ('Klagelieder', 'Klagelieder', 'Klg'),
    ('Hesekiel', 'Hesekiel', 'Hes'), ('Daniel', 'Daniel', 'Da'), ('Hosea', 'Hosea', 'Hos'), ('Joel', 'Joel', 'Joe'),
    ('Amos', 'Amos', 'Am'), ('Obadja', 'Obadja', 'Ob'), ('Jona', 'Jona', 'Jon'), ('Micha', 'Micha', 'Mi'),
    ('Nahum', 'Nahum', 'Nah'), ('Habakuk', 'Habakuk', 'Hab'), ('Zephanja', 'Zephanja', 'Ze'), ('Haggai', 'Haggai', 'Hag'),
    ('Sacharja', 'Sacharja', 'Sach'), ('Maleachi', 'Maleachi', 'Mal'),
    ('Matthäus', 'Matthäus', 'Mat'), ('Markus', 'Markus', 'Mar'), ('Lukas', 'Lukas', 'Luk'),
    ('Johannes', 'Johannes', 'Joh'), ('Apostelgeschichte', 'Apostelgeschichte', 'Apg'), ('Römer', 'Römer', 'Rö'),
    ('1. Korinther', 'erster Korinther', '1Ko'), ('2. Korinther', 'zweiter Korinther', '2Ko'), ('Galater', 'Galater', 'Gal'),
    ('Epheser', 'Epheser', 'Eph'), ('Philipper', 'Philipper', 'Php'), ('Kolosser', 'Kolosser', 'Kol'),
    ('1. Thessalonicher', 'erster Thessalonicher', '1Th'), ('2. Thessalonicher', 'zweiter Thessalonicher', '2Th'),
    ('1. Timotheus', 'erster Timotheus', '1Ti'), ('2. Timotheus', 'zweiter Timotheus', '2Ti'), ('Titus', 'Titus', 'Tit'),
    ('Philemon', 'Philemon', 'Phm'), ('Hebräer', 'Hebräer', 'Heb'), ('Jakobus', 'Jakobus', 'Jak'),
    ('1. Petrus', 'erster Petrus', '1Pe'), ('2. Petrus', 'zweiter Petrus', '2Pe'), ('1. Johannes', 'erster Johannes', '1Jo'),
    ('2. Johannes', 'zweiter Johannes', '2Jo'), ('3. Johannes', 'dritter Johannes', '3Jo'), ('Judas', 'Judas', 'Jud'),
    ('Offenbarung', 'Offenbarung', 'Off'),
]

GREEN = (0, 176, 80)            # Versnummer
PROSE = (38, 38, 38)            # Fließtext
POEM = (0, 0, 102)              # poetischer Text
RED = (255, 0, 0)               # verschobene Farbmarkierung (Exportfehler, ohne Bedeutung)
DIVISION = (112, 48, 160)       # Psalmen: "Erstes Buch (Psalm 1 bis 41)"
OUTLINE = (192, 0, 0)           # Übersicht am Buchanfang
warnings = []
fixes = []


def clean(t):
    return re.sub(r'[ \t]+', ' ', t.replace(' ', ' ')).strip()


def parse_book(path, num):
    src = path.read_text(encoding='latin-1')
    title = ''
    outline = []            # [kapitel, ebene, text]
    chapters = {}           # nr -> [absatz]
    cur = None
    pending = []
    in_body = False
    out_ch = None

    last_verse = [0]

    def start_chapter(n):
        nonlocal cur
        last_verse[0] = 0
        if n in chapters:
            warnings.append(f'{BOOKS[num-1][2]}: Kapitel {n} doppelt')
        chapters[n] = list(pending)
        pending.clear()
        cur = chapters[n]

    for props, runs in paragraphs(src):
        tabs = sum(r[3].count('\t') for r in runs if r[0] is None)
        runs = [r for r in runs if r[3].strip('\t')]
        if not runs:
            continue
        colors = {r[0] for r in runs}
        txt = plain(runs)
        if any(r[2] == 36 for r in runs):
            title = clean(txt)
            continue
        if any(r[2] == 32 and r[1] for r in runs):          # Kapitelüberschrift im Bibeltext
            in_body = True
            m = re.search(r'(\d+)', txt)
            start_chapter(int(m.group(1)))
            continue
        if not in_body and GREEN in colors:                  # Buch mit nur einem Kapitel
            in_body = True
            start_chapter(1)
        if not in_body:
            if colors <= {(192, 80, 77)}:                    # "Übersicht"
                continue
            if colors == {DIVISION}:
                pending.append(['d', clean(txt)])
                continue
            if re.match(r'(Kapitel|Psalm) \d+$', clean(txt)):  # auch wenn in der Vorlage nicht fett (z. B. Richter 5)
                out_ch = int(re.search(r'\d+', txt).group())
                continue
            outline.append([out_ch or 1, max(tabs - 1, 0), clean(txt)])
            continue

        # --- Bibeltext ---
        if colors == {DIVISION}:
            pending.append(['d', clean(txt)])
            continue
        if not (colors & {GREEN, PROSE, POEM}):              # Überschrift (z. B. Psalm-Überschrift)
            cur.append(['h', clean(txt)])
            continue
        kind = 'q' if (props.get('li') == 432 or POEM in colors and PROSE not in colors) else 'p'
        para = [kind]
        buf = ''
        i = 0
        while i < len(runs):
            rgb, b, fs, t = runs[i]
            if rgb == GREEN and t.strip().isdigit():
                if buf.strip():
                    para.append(buf)
                buf = ''
                digits = t.strip()
                expected = last_verse[0] + 1
                # Exportfehler: Die Rot-Markierung schneidet Ziffern aus der Versnummer heraus
                # (z. B. grün "1" + rot "4200" = Vers 14, Text "200 ...").
                if int(digits) != expected and i + 1 < len(runs) and runs[i + 1][0] == RED:
                    nxt = runs[i + 1][3]
                    exp = str(expected)
                    if exp.startswith(digits) and (digits + nxt).startswith(exp):
                        rest = (digits + nxt)[len(exp):]
                        digits = exp
                        runs[i + 1] = (PROSE, False, 24, rest)
                        fixes.append(f'{BOOKS[num-1][2]} {sorted(chapters)[-1]}:{exp}')
                last_verse[0] = int(digits)
                para.append(int(digits))
            else:
                buf += t
            i += 1
        if buf.strip():
            para.append(buf)
        # Leerzeichen normalisieren
        para = [p if isinstance(p, int) else re.sub(r'\s+', ' ', p.replace(' ', ' ')) for p in para]
        for i in range(1, len(para)):
            if isinstance(para[i], str) and i > 1 and isinstance(para[i-1], int):
                para[i] = para[i].lstrip()
        if len(para) > 1 and isinstance(para[1], str):
            para[1] = para[1].lstrip()
        if len(para) > 1:
            para[-1] = para[-1].rstrip() if isinstance(para[-1], str) else para[-1]
            cur.append(para)

    n_ch = max(chapters) if chapters else 0
    ch_list = []
    for c in range(1, n_ch + 1):
        if c not in chapters:
            warnings.append(f'{BOOKS[num-1][2]}: Kapitel {c} fehlt')
        ch_list.append(chapters.get(c, []))
    # Versfolge prüfen
    gaps = []
    for ci, ch in enumerate(ch_list, 1):
        vs = [x for p in ch for x in p[1:] if isinstance(x, int)]
        for a, b in zip(vs, vs[1:]):
            if b != a + 1:
                gaps.append(f'{ci}:{a}->{b}')
        if vs and vs[0] != 1:
            gaps.append(f'{ci}: beginnt mit {vs[0]}')
    if gaps:
        warnings.append(f'{BOOKS[num-1][2]}: Lücken/Sprünge {gaps}')
    return title, outline, ch_list


def parse_overview(path):
    infos, cur = [], None
    for _, runs in paragraphs(path.read_text(encoding='latin-1')):
        t = clean(plain(runs))
        m = re.match(r'(Bibelbuch|Schreiber|Wo geschrieben|Wann fertig|Zeitspanne): (.*)', t)
        if not m:
            continue
        if m.group(1) == 'Bibelbuch':
            cur = {}
            infos.append(cur)
        cur[m.group(1)] = m.group(2)
    return infos


def parse_glossary(path):
    entries = []
    for props, runs in paragraphs(path.read_text(encoding='latin-1')):
        runs = [r for r in runs if r[3].strip()]
        if not runs or any(r[2] == 36 for r in runs) or (runs[0][0] == (128, 0, 0) and len(runs) == 1):
            continue
        if runs[0][1]:
            i = 0
            term = ''
            while i < len(runs) and runs[i][1]:
                term += runs[i][3]
                i += 1
            entries.append([clean(term).rstrip('.').strip(), clean(plain(runs[i:]))])
        elif entries:
            entries[-1][1] += '\n' + clean(plain(runs))
    return entries


SPOKEN = sorted({b[1] for b in BOOKS} | {'Da'}, key=len, reverse=True)   # "Da" = Daniel (so im Original)
REF_RE = re.compile(r'^((?:' + '|'.join(map(re.escape, SPOKEN)) +
                    r') \d+(?: Vers \d+)?(?:(?:, | bis )\d+)*)\s*(.*)$')


def parse_concordance(path):
    words = []
    for props, runs in paragraphs(path.read_text(encoding='latin-1')):
        runs = [r for r in runs if r[3].strip()]
        if not runs or any(r[2] in (36,) for r in runs) or runs[0][0] == (128, 0, 0):
            continue
        t = clean(plain(runs))
        if t.startswith('[Hinweis]'):
            continue
        if runs[0][1]:                           # fett am Absatzanfang = neues Stichwort (auch "Jakobus 2")
            head = ''
            for r in runs:
                if not r[1]:
                    break
                head += r[3]
                if ',' in head:
                    break
            word, sep, _ = head.partition(',')
            words.append([clean(word), []])
            t = clean(t[t.index(',') + 1:]) if sep else clean(t[len(head):])
        if not words or not t:
            continue
        m = REF_RE.match(t)
        sm = re.match(r'(siehe(?: auch)? [A-ZÄÖÜ][\wäöüß]*(?: [A-ZÄÖÜ][\wäöüß]*)?)\s*(.*)$', t)
        if sm and not REF_RE.match(sm.group(2) or 'x') and sm.group(2):
            sm = None
        if sm:                                   # Querverweis innerhalb der Konkordanz
            words[-1][1].append(['', sm.group(1)])
            if sm.group(2):
                m = REF_RE.match(sm.group(2))
        if m:
            ref, snip = re.sub(r'^Da ', 'Daniel ', m.group(1)), m.group(2)
            w = words[-1][0].replace('.', '')
            # Exportfehler bei Zahl-Stichwörtern: "Psalm 91 Vers 7" + "1000 werden …" ohne Leerzeichen
            if w.isdigit() and ref.endswith(w) and not ref.endswith(' ' + w):
                ref, snip = ref[:-len(w)], w + ' ' + snip
                fixes.append(f'Konkordanz {words[-1][0]}: {ref}')
            words[-1][1].append([ref, snip])
        elif sm:
            pass
        else:                                    # unbekanntes Format: als Hinweistext behalten (App verlinkt Stellen darin)
            words[-1][1].append(['', t])
            warnings.append(f'Konkordanz: als Hinweis übernommen: {t[:60]}')
    return words


def parse_article(path):
    title, items = '', []
    for props, runs in paragraphs(path.read_text(encoding='latin-1')):
        runs = [r for r in runs if r[3].strip()]
        if not runs:
            continue
        t = clean(plain(runs))
        if any(r[2] == 36 for r in runs):
            title = title or t
            items.append(['t', t])
        elif all(r[1] for r in runs):
            items.append(['h', t])
        else:
            items.append(['p', t])
    return title, items


def main():
    files = {int(m.group(1)): p for p in ROOT.glob('nwt_*_X.rtf') if (m := re.match(r'nwt_(\d\d)_', p.name))}
    infos = parse_overview(next(ROOT.glob('nwt_Übersicht*_X.rtf')))
    books = []
    for n in range(1, 67):
        title, outline, chs = parse_book(files[n], n)
        name, spoken, abbr = BOOKS[n - 1]
        books.append({'n': n, 'name': name, 'spoken': spoken, 'abbr': abbr, 'title': title,
                      'nt': n >= 40, 'info': infos[n - 1] if n - 1 < len(infos) else {},
                      'outline': outline, 'ch': chs})
    data = {
        'quelle': 'Neue-Welt-Übersetzung (RTF-Export), lokal aufbereitet',
        'books': books,
        'glossar': parse_glossary(next(ROOT.glob('nwt_Worterkl*_X.rtf'))),
        'konkordanz': parse_concordance(next(ROOT.glob('nwt_Konkordanz*_X.rtf'))),
        'extras': [dict(zip(('title', 'items'), parse_article(next(ROOT.glob(g))))) | {'id': i}
                   for i, g in (('vorwort', 'nwt_Abk*_X.rtf'), ('anhangA', 'nwt_Anhang A*_X.rtf'),
                                ('anhangB', 'nwt_Anhang B*_X.rtf'))],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    OUT.write_text(js, encoding='utf-8')

    verses = sum(1 for b in books for ch in b['ch'] for p in ch for x in p[1:] if isinstance(x, int))
    print(f'Bücher: {len(books)}, Kapitel: {sum(len(b["ch"]) for b in books)}, Verse: {verses}')
    print(f'Glossar: {len(data["glossar"])}, Konkordanz: {len(data["konkordanz"])} Wörter, '
          f'{sum(len(w[1]) for w in data["konkordanz"])} Stellen')
    print(f'Datei: {OUT} ({OUT.stat().st_size/1e6:.1f} MB)')
    print(f'Automatisch korrigierte Exportfehler: {len(fixes)} {fixes}')
    print(f'Warnungen: {len(warnings)}')
    for w in warnings[:60]:
        print('  ', w)


if __name__ == '__main__':
    main()
