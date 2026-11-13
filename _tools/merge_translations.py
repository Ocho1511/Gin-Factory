import re, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
D = 'C:/wk/Gin-Factory/_tools/'
P = 'C:/wk/Gin-Factory/index.html'
en = json.load(open(D + 'en_source.json', encoding='utf-8'))
ph = lambda v: sorted(re.findall(r'\{[a-z]+\}|<br>|\n|→|←|✓|⚠', v))
langs = ['es','sv','da','fi','ru','it','fr','pl','hu','cs','sk','ro','hr','pt','no','nl','el','uk','ja','ko','zh','hi']
good = {}
for c in langs:
    try:
        t = json.load(open(f'{D}tr_{c}.json', encoding='utf-8'))
    except Exception as e:
        print(c, 'INVALID JSON', e); continue
    miss = [k for k in en if k not in t]
    extra = [k for k in t if k not in en]
    bad = [k for k in en if k in t and ph(en[k]) != ph(t[k])]
    # placeholder check ignores symbols the translator may legitimately drop only for emoji-less keys; report
    print(c, 'keys', len(t), 'missing', miss, 'extra', extra, 'ph-mismatch', bad)
    if not miss:
        good[c] = {k: t[k] for k in en}
s = open(P, encoding='utf-8').read()
out = []
lang = None
hits = 0
for l in s.split('\n'):
    m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', l)
    if m:
        lang = m.group(1)
    m2 = re.match(r'^(\s+)([a-z_0-9]+): (".*"|\'.*\')(,?)$', l)
    if m2 and lang in good and m2.group(2) in good[lang]:
        l = f'{m2.group(1)}{m2.group(2)}: {json.dumps(good[lang][m2.group(2)], ensure_ascii=False)}{m2.group(4)}'
        hits += 1
    out.append(l)
if '--apply' in sys.argv:
    open(P, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('would replace' if '--apply' not in sys.argv else 'replaced', hits, 'langs', len(good))
