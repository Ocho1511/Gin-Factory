import json, re, sys, importlib.util, os
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
src = {f: json.load(open(os.path.join(D, f + '_source.json'), encoding='utf-8')) for f in ('gin', 'whiskey')}
ph = lambda s: sorted(re.findall(r'\{\w+\}', s))
ok = True
for code in sys.argv[1:]:
    m = importlib.import_module('tr_' + code)
    for f, spec in (('gin', m.G), ('whiskey', m.W)):
        merged = dict(m.C); merged.update(spec)
        en = src[f]['en']
        out = {k: merged[k] for k in en if k in merged}
        miss = [k for k in en if k not in merged]
        extra = [k for k in merged if k not in en and k in spec]
        bad = []
        for k, v in out.items():
            if ph(v) != ph(en[k]) or (k.endswith('_ing') and v.count('\n') != en[k].count('\n')):
                bad.append(k)
        if miss or bad:
            ok = False
        print(code, f, len(out), '/', len(en), 'missing', miss, 'bad', bad)
        with open(os.path.join(D, 'tr_%s_%s.json' % (f, code)), 'w', encoding='utf-8') as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
print('OK' if ok else 'PROBLEMS')
