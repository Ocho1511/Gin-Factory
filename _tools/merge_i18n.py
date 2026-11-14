"""Traegt die Gin-Uebersetzungen in jeden Sprachblock von const I18N ein.
Quellen (in C:/wk/Gin-Factory/_tools/i18n/):
  gin_source.json           {de:{key:text}, en:{key:text}}  (165 Schluessel)
  extras_gin_source.json    {de:{...}, en:{...}}            (zusaetzliche Schluessel, optional)
  tr_gin_<code>.json        {key:text} je Sprache (22 Sprachen)
  tr_extras_gin_<code>.json {key:text} je Sprache (optional, wird automatisch eingelesen, wenn vorhanden)
Regeln: de/en aus der Quelle, 'us' (und Varianten) nehmen die en-Werte; vorhandene Schluessel werden nicht doppelt angelegt
(auch nicht ueberschrieben; Abweichungen werden gemeldet); Werte als JSON-escaped Strings.
Aufruf: python merge_i18n.py [--check]
"""
import re, sys, json, os, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = 'C:/wk/Gin-Factory/'
P = BASE + 'index.html'
D = BASE + '_tools/i18n/'
LANGS24 = 'de en es sv da fi ru it fr pl hu cs sk ro hr pt no nl el uk ja ko zh hi'.split()


def load(path):
    return json.load(open(path, encoding='utf-8')) if os.path.exists(path) else None


src = load(D + 'gin_source.json')
extras = load(D + 'extras_gin_source.json') or {'de': {}, 'en': {}}
values = {}   # lang -> {key: text}
values['de'] = dict(src['de']); values['de'].update(extras.get('de', {}))
values['en'] = dict(src['en']); values['en'].update(extras.get('en', {}))
for code in LANGS24:
    if code in ('de', 'en'):
        continue
    v = {}
    a = load(D + 'tr_gin_%s.json' % code)
    b = load(D + 'tr_extras_gin_%s.json' % code)
    if a: v.update(a)
    if b: v.update(b)
    values[code] = v
ALL_KEYS = list(values['de'].keys())

s = open(P, encoding='utf-8').read()
L = s.split('\n')
i0 = next(i for i, l in enumerate(L) if l.startswith('const I18N = {'))
j0 = next(i for i in range(i0, len(L)) if L[i] == '};')
blocks = []   # (lang, start_index, end_index)
cur = None
for i in range(i0 + 1, j0):
    m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', L[i])
    if m:
        cur = [m.group(1), i, None]; blocks.append(cur)
    elif L[i] in ('},', '}') and cur and cur[2] is None:
        cur[2] = i
assert all(b[2] is not None for b in blocks), 'Blockende nicht gefunden'
print('Sprachbloecke:', [b[0] for b in blocks])


def esc(v):
    return json.dumps(v, ensure_ascii=False)


added_total = 0
diffs = []
report = {}
# von hinten nach vorn einfuegen, damit Indizes gueltig bleiben
for lang, a, b in sorted(blocks, key=lambda x: -x[1]):
    existing = {}
    for k in range(a + 1, b):
        m = re.match(r'^\s+([a-z_0-9]+): (.*?),?$', L[k])
        if m: existing[m.group(1)] = m.group(2)
    base = values.get(lang)
    if base is None:
        base = values['en']          # 'us' und Varianten: en-Werte
    new_lines = []
    for key in ALL_KEYS:
        if key in existing:
            # Abweichung melden (de/en-Pruefung)
            if lang in ('de', 'en'):
                want = esc(values[lang][key])
                if existing[key].strip() != want:
                    diffs.append((lang, key, existing[key][:60], values[lang][key][:60]))
            continue
        if key not in base:
            continue                       # (noch) keine Uebersetzung: t() faellt auf en zurueck
        new_lines.append('  %s: %s,' % (key, esc(base[key])))
    report[lang] = (len(new_lines), len(existing))
    L[a + 1:a + 1] = new_lines
    added_total += len(new_lines)

s2 = '\n'.join(L)
if '--check' not in sys.argv:
    open(P, 'w', encoding='utf-8', newline='').write(s2)
print('Zeilen eingefuegt:', added_total)
print('je Sprache (neu, vorhanden):', report)
print('Abweichende vorhandene de/en-Werte (nicht ueberschrieben):', len(diffs))
for d in diffs[:20]:
    print('  ', d)
