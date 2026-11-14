import re, sys
sys.stdout.reconfigure(encoding='utf-8')
path = sys.argv[1]
names = sys.argv[2:]
s = open(path, encoding='utf-8').read()
lines = s.split('\n')
# Funktionsgrenzen (Top-Level: Zeile beginnt mit 'function'/'async function' und schliesst mit '}' in Spalte 0)
starts = [(i, re.match(r'^(?:async\s+)?function\s+([A-Za-z0-9_$]+)', l).group(1)) for i, l in enumerate(lines) if re.match(r'^(?:async\s+)?function\s+[A-Za-z0-9_$]+', l)]
def end_of(i):
    # einzeilig?
    if lines[i].rstrip().endswith('}') and lines[i].count('{') == lines[i].count('}'):
        return i
    for j in range(i + 1, len(lines)):
        if lines[j].startswith('}'):
            return j
    return i
for n in names:
    hit = [(i, e) for i, e in [(i, nm) for i, nm in starts] if e == n]
    if not hit:
        print(n, ': NICHT als Top-Level-Funktion gefunden'); continue
    i = hit[0][0]; j = end_of(i)
    refs = [k + 1 for k, l in enumerate(lines) if re.search(r'(?<![A-Za-z0-9_$])' + re.escape(n) + r'(?![A-Za-z0-9_$])', l) and not (i <= k <= j)]
    print(f'{n}: Zeilen {i+1}-{j+1} ({j-i+1}), Verweise ausserhalb: {refs[:12]}')
