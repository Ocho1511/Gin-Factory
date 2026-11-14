import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
m = re.search(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, re.S)
js = m.group(1)
# I18N-Block (Sprachtexte) fuer die Funktionssuche ausblenden
i0 = js.index('const I18N = {')
j0 = js.index('\n};', js.index('\nzh:', i0))
code_wo_i18n = js[:i0] + js[j0:]
html_part = s[:m.start()] + s[m.end():]
hay = code_wo_i18n + '\n' + html_part
# Top-Level-Funktionen
funcs = re.findall(r'^(?:async\s+)?function\s+([A-Za-z0-9_$]+)\s*\(', code_wo_i18n, re.M)
dead = []
for f in funcs:
    n = len(re.findall(r'(?<![A-Za-z0-9_$])' + re.escape(f) + r'(?![A-Za-z0-9_$])', hay))
    if n <= 1:
        dead.append(f)
# Top-Level-Konstanten/let
consts = re.findall(r'^(?:const|let|var)\s+([A-Za-z0-9_$]+)\s*=', code_wo_i18n, re.M)
deadc = []
for c in consts:
    n = len(re.findall(r'(?<![A-Za-z0-9_$])' + re.escape(c) + r'(?![A-Za-z0-9_$])', hay))
    if n <= 1:
        deadc.append(c)
# CSS-Klassen im Style-Block, die nirgends im HTML/JS vorkommen
css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
classes = set(re.findall(r'\.([A-Za-z][A-Za-z0-9_-]+)', re.sub(r'/\*.*?\*/', '', css, flags=re.S)))
text_wo_css = s.replace(css, '')
deadcss = sorted(c for c in classes if not re.search(r'(?<![A-Za-z0-9_-])' + re.escape(c) + r'(?![A-Za-z0-9_-])', text_wo_css) and not c.startswith(('show', 'active')))
print(json.dumps({'file': path, 'functions_total': len(funcs), 'dead_functions': dead, 'dead_consts': deadc, 'css_classes_total': len(classes), 'dead_css_classes': deadcss}, ensure_ascii=False, indent=1))
