"""Minimaler RTF-Tokenizer für die WTS5-Exporte der Neue-Welt-Übersetzung.

Liefert Absätze als Liste von Läufen (rgb, fett, schriftgröße, text).
Die Farbtabelle unterscheidet sich je Datei, daher wird über RGB-Werte
statt über \\cfN-Indizes gearbeitet.
"""
import re

TOKEN = re.compile(r'\\u(-?\d+)\?|\\([a-zA-Z]+)(-?\d+)? ?|\\([^a-zA-Z])|([{}])|([^\\{}\r\n]+)|[\r\n]+')


def parse_colortbl(s):
    m = re.search(r'\{\\colortbl([^}]*)\}', s)
    cols = []
    for entry in m.group(1).split(';')[:-1]:
        r = re.search(r'\\red(\d+)', entry)
        g = re.search(r'\\green(\d+)', entry)
        b = re.search(r'\\blue(\d+)', entry)
        cols.append((int(r.group(1)), int(g.group(1)), int(b.group(1))) if r else None)
    return cols


def _events(s):
    cols = parse_colortbl(s)
    s = s[s.index('{\\stylesheet'):]
    s = re.sub(r'\{\\info.*?\}\}\}\}', '', s, flags=re.S)
    stack = []
    st = {'cf': 0, 'b': False, 'fs': 24, 'skip': False}
    para = {'qc': False, 'li': 0, 'fi': 0}

    def col():
        return cols[st['cf']] if st['cf'] < len(cols) else None

    for m in TOKEN.finditer(s):
        u, word, num, sym, brace, text = m.groups()
        if brace == '{':
            stack.append(dict(st))
            continue
        if brace == '}':
            if stack:
                st = stack.pop()
            continue
        if st['skip']:
            continue
        if u is not None:
            yield ('t', chr(int(u) % 65536), col(), st['b'], st['fs'])
        elif word:
            n = int(num) if num else None
            if word == 'cf':
                st['cf'] = n or 0
            elif word == 'b':
                st['b'] = (n is None or n != 0)
            elif word == 'fs':
                st['fs'] = n
            elif word == 'par':
                yield ('par', dict(para))
            elif word == 'pard':
                para = {'qc': False, 'li': 0, 'fi': 0}
            elif word in ('qc', 'li', 'fi'):
                para[word] = True if word == 'qc' else n
            elif word == 'tab':
                yield ('t', '\t', None, st['b'], st['fs'])
            elif word == 'line':
                yield ('t', '\n', None, st['b'], st['fs'])
            elif word == 'stylesheet':
                st['skip'] = True
            elif word == 'plain':
                st.update(cf=0, b=False, fs=24)
        elif sym:
            if sym == '*':
                st['skip'] = True
            elif sym in '\\{}':
                yield ('t', sym, col(), st['b'], st['fs'])
            elif sym == '~':
                yield ('t', '\u00a0', None, st['b'], st['fs'])
        elif text:
            yield ('t', text, col(), st['b'], st['fs'])


def paragraphs(s):
    """Absätze als (props, [(rgb, bold, fs, text), ...]); gleiche Läufe zusammengefasst."""
    cur = []
    for ev in _events(s):
        if ev[0] == 'par':
            yield ev[1], cur
            cur = []
        else:
            _, t, rgb, b, fs = ev
            if cur and cur[-1][:3] == (rgb, b, fs):
                cur[-1] = (rgb, b, fs, cur[-1][3] + t)
            else:
                cur.append((rgb, b, fs, t))
    if cur:
        yield {}, cur


def plain(runs):
    return ''.join(r[3] for r in runs)
