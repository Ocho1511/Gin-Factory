import re, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')

CSS = '''/* Handy: Perfect-Serve-Felder untereinander, Formularzeilen unten ausrichten */
@media (max-width: 520px) { #serve-group .form-row { display: grid; grid-template-columns: 1fr; gap: 8px; } }
.form-row { align-items: flex-end; }
'''
SOFT = 'Wunsch\u00adliste'

# (Pfad, CSS ja/nein)
targets = [('C:/wk/Gin-Factory/index.html', True), ('C:/wk/My-Whiskey-Collection/index.html', True),
           ('C:/wk/main/index.html', False), ('C:/wk/Weinkeller-App/www/index.html', False), ('C:/wk/Weinkeller-live/index.html', False)]
for path, css in targets:
    s = open(path, encoding='utf-8').read()
    if css:
        assert CSS.splitlines()[0] not in s
        s = s.replace('</style>', CSS + '</style>', 1)
    lang = None
    out = []
    in_i = False
    n = 0
    for l in s.split('\n'):
        if l.startswith('const I18N = {'):
            in_i = True
        m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', l)
        if in_i and m:
            lang = m.group(1)
        m2 = re.match(r'^(\s+)nav_wish: "Wunschliste"(,?)$', l)
        if in_i and m2 and lang == 'de':
            l = f'{m2.group(1)}nav_wish: "Wunsch\\u00adliste"{m2.group(2)}'
            n += 1
        out.append(l)
    assert n == 1, (path, n)
    s = '\n'.join(out)
    open(path, 'w', encoding='utf-8', newline='').write(s)
    c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
    open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
    r = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True)
    print(path, 'syntax', r.returncode)
