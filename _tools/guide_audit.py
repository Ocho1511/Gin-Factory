import re, sys, os
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8')
LANGS = 'de en es sv da fi ru it fr pl hu cs sk ro hr pt no nl el uk ja ko zh hi'.split()
APPS = {'gin': 'C:/wk/Gin-Factory', 'whiskey': 'C:/wk/My-Whiskey-Collection'}
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'col', 'area', 'base', 'wbr', 'source', 'track', 'embed', 'param'}


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.err = []; self.ids = set(); self.hrefs = []; self.h2 = 0; self.toc = 0; self.intoc = False; self.options = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'a' and a.get('href', '').startswith('#'): self.hrefs.append(a['href'][1:])
        if tag == 'h2': self.h2 += 1
        if tag == 'div' and 'toc' in (a.get('class') or ''): self.intoc = True
        if tag == 'option': self.options.append(a.get('value', ''))
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag:
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.err.append('unclosed <' + self.stack.pop() + '>')
                self.stack.pop()
            else:
                self.err.append('stray </' + tag + '>')
        else:
            self.stack.pop()


def audit(app, path):
    probs = []
    for code in LANGS + ['']:
        fn = os.path.join(path, 'anleitung' + ('-' + code if code else '') + '.html')
        if not os.path.exists(fn):
            probs.append((code or 'default', 'FEHLT')); continue
        s = open(fn, encoding='utf-8').read()
        p = P(); p.feed(s)
        if p.err: probs.append((code or 'default', 'tags: ' + ', '.join(p.err[:3])))
        if p.stack: probs.append((code or 'default', 'offene Tags: ' + ','.join(p.stack[:4])))
        if not s.rstrip().lower().endswith('</html>'): probs.append((code or 'default', 'endet nicht mit </html>'))
        if p.h2 != 15: probs.append((code or 'default', f'h2={p.h2}'))
        missing = [h for h in p.hrefs if h not in p.ids]
        if missing: probs.append((code or 'default', 'fehlende Anker: ' + ','.join(missing[:4])))
        langs_in_switch = [o.replace('anleitung-', '').replace('.html', '') for o in p.options]
        if set(LANGS) - set(langs_in_switch): probs.append((code or 'default', 'Umschalter unvollständig: ' + ','.join(sorted(set(LANGS) - set(langs_in_switch)))))
        if 'Last Build' not in s: probs.append((code or 'default', 'kein Hinweis "Last Build"'))
        if re.search(r'lang="%s"' % (code or 'de'), s) is None: probs.append((code or 'default', 'html lang passt nicht'))
        if app == 'gin' and re.search(r'whisk|bourbon|scotch|glencairn|\bwein\b|\bwine\b|vivino', s, re.I):
            m = re.search(r'whisk|bourbon|scotch|glencairn|\bwein\b|\bwine\b|vivino', s, re.I)
            probs.append((code or 'default', 'Whiskey/Wein-Wort: ' + m.group(0)))
    return probs


for app, path in APPS.items():
    pr = audit(app, path)
    print('==', app, '| Dateien erwartet 25 | Probleme:', len(pr))
    for c, t in pr: print('  ', c, t)
