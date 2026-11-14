import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()
i0 = s.index('const I18N = {')
j0 = s.index('\n};', s.index('\nhi:', i0))
blk = s[i0:j0].split('\n')
starts = [(i, m.group(1)) for i, l in enumerate(blk) for m in [re.match(r'^([a-z]{2}): \{$', l)] if m]
W = {
 'de': r'(wein|rebsort|jahrgang|trinkreife|reife|vivino|winzer|sommelier|korken|keller|sekt\b|champagner|traube)',
 'en': r'(wine|winery|grape|vintage|vivino|sommelier|cork|cellar|ripeness|drinking window)',
 'es': r'(vino|bodega|uva\b|uvas|cosecha|a[ñn]ada|vivino|sommelier|corcho|cava\b|madurez)',
 'sv': r'(\bvin\b|viner|vinet|druva|årgång|vivino|sommelier|kork|källare|mognad)',
 'da': r'(\bvin\b|vine\b|vinen|drue|årgang|vivino|sommelier|prop\b|kælder|modenhed)',
 'fi': r'(viini|rypäle|vuosikerta|vivino|sommelier|korkki|kellari|kypsyys)',
 'ru': r'(вин[оауеы]\b|вина\b|вин\b|винн|виноград|урожай|vivino|сомелье|пробк|погреб|зрелост)',
 'it': r'(\bvino|\bvini\b|vigneto|\buva\b|annata|vivino|sommelier|tappo|cantina|maturit)',
 'fr': r'(\bvin\b|\bvins\b|domaine|cépage|millésime|vivino|sommelier|bouchon|\bcave\b|maturité)',
 'pl': r'(wino\b|wina\b|\bwin\b|winn|szczep|rocznik|vivino|sommelier|korek|piwnic|dojrzałoś)',
 'hu': r'(\bbor\b|borok|bort\b|szőlő|évjárat|pincészet|vivino|sommelier|dugó|pince\b|érettség)',
 'cs': r'(víno|vína|\bvín\b|odrůd|ročník|vivino|someliér|sommelier|korek|sklep|zralost)',
 'sk': r'(víno|vína|\bvín\b|odrod|ročník|vivino|someliér|sommelier|korok|pivnic|zrelosť)',
 'ro': r'(\bvin\b|vinuri|struguri|recoltă|vivino|somelier|dop\b|pivniț|maturitate)',
 'hr': r'(\bvino|\bvina\b|grož|berba|vivino|sommelier|čep\b|podrum|zrelost)',
 'pt': r'(vinho|\buva\b|uvas|colheita|safra|vivino|sommelier|rolha|adega|maturidade)',
 'no': r'(\bvin\b|viner|vinen|drue|årgang|vivino|sommelier|kork|kjeller|modenhet)',
 'nl': r'(wijn|druif|druiven|jaargang|oogstjaar|vivino|sommelier|kurk|kelder|rijpheid)',
 'el': r'(κρασ|οινοπ|οίνο|σταφυλ|vivino|σομελιέ|φελλ|κελάρ|ωριμ)',
 'uk': r'(вин[оауеи]\b|вина\b|вин\b|винн|виноград|врожай|vivino|сомельє|корк|погріб|стиглість)',
 'ja': r'(ワイン|ブドウ|ぶどう|ヴィンテージ|ヴィヴィーノ|vivino|ソムリエ|コルク|セラー|熟成|飲み頃)',
 'ko': r'(와인|포도|빈티지|vivino|소믈리에|코르크|셀러|숙성)',
 'zh': r'(葡萄|红酒|年份|酒庄|vivino|侍酒|软木|酒窖|成熟|适饮)',
 'hi': r'(वाइन|अंगूर|विंटेज|vivino|सोमेलियर|कॉर्क|सेलर|परिपक्व)',
}
found = {}
for k, (i, code) in enumerate(starts):
    end = starts[k + 1][0] if k + 1 < len(starts) else len(blk)
    pat = re.compile(W[code], re.I)
    for l in blk[i + 1:end]:
        m = re.match(r'^\s+([A-Za-z_0-9]+): (".*"),?$', l)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        mm = pat.search(val)
        if mm:
            found.setdefault(key, {})[code] = (mm.group(0), val)
print('Schluessel mit Wein-Woertern:', len(found), ' Sprachen:', len(starts))
if '-v' in sys.argv:
    for key, langs in sorted(found.items()):
        for c, (w, v) in langs.items():
            print(' ', c, key, '[%s]' % w, v[:110])
else:
    per = {}
    for key, langs in found.items():
        for c in langs:
            per[c] = per.get(c, 0) + 1
    print(per)
    for key, langs in sorted(found.items()):
        print(' ', key, '->', ', '.join('%s(%s)' % (c, w[0]) for c, w in langs.items()))
json.dump({k: {c: v[1] for c, v in l.items()} for k, l in found.items()}, open('C:/wk/Gin-Factory/_tools/i18n/_scan_hits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
