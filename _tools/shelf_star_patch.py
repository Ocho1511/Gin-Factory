import re, sys, math, json
sys.stdout.reconfigure(encoding='utf-8')


def star_points(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        ang = -math.pi / 2 + i * math.pi / n
        r = ro if i % 2 == 0 else ri
        pts.append(f'{cx + r * math.cos(ang):.2f},{cy + r * math.sin(ang):.2f}')
    return ' '.join(pts)


STAR = ('<svg viewBox="0 0 32 32" width="0.8em" height="0.8em" aria-hidden="true" style="display:block;margin:.1em auto">'
        '<defs><linearGradient id="wsA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dc8a"/><stop offset="1" stop-color="#d09a2e"/></linearGradient></defs>'
        f'<polygon points="{star_points(16, 17, 13, 5.6)}" fill="url(#wsA)" stroke="url(#wsA)" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<polygon points="{star_points(16, 17, 6.2, 2.6)}" fill="#fff" fill-opacity=".28"/>'
        '</svg>')


def shelf(kind):
    # Holzregal mit zwei Fachboeden und Flaschen; Farben je App
    if kind == 'gin':
        bottle, label, cap = '#dcebf1', '#1c2b45', '#d2a679'
    else:
        bottle, label, cap = '#e5a040', '#f1e4c3', '#3a2410'

    def b(x, base, h, w=4.6):
        top = base - h
        return (f'<rect x="{x + 1.5:.1f}" y="{top - 2.6:.1f}" width="{w - 3:.1f}" height="2.8" rx=".5" fill="{cap}"/>'
                f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="1.2" fill="{bottle}"/>'
                f'<rect x="{x + .5}" y="{top + h * .38:.1f}" width="{w - 1}" height="{h * .34:.1f}" fill="{label}"/>')

    return ('<svg viewBox="0 0 32 32" width="0.85em" height="0.85em" aria-hidden="true" style="display:block;margin:.05em auto">'
            '<defs>'
            '<linearGradient id="shW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9935a"/><stop offset="1" stop-color="#8f5d30"/></linearGradient>'
            '<linearGradient id="shB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1b0f"/><stop offset="1" stop-color="#3f2a17"/></linearGradient>'
            '</defs>'
            '<rect x="2.5" y="2" width="27" height="28" rx="2.6" fill="url(#shW)"/>'
            '<rect x="5" y="4.5" width="22" height="23" rx="1.2" fill="url(#shB)"/>'
            + b(7.2, 15.4, 8.4) + b(13.7, 15.4, 9.4) + b(20.2, 15.4, 7.6)
            + '<rect x="5" y="15.4" width="22" height="1.7" fill="#d8a76b"/>'
            + b(8.2, 26.2, 7.2) + b(15, 26.2, 8.2) + b(21.4, 26.2, 6.4)
            + '<rect x="5" y="26.2" width="22" height="1.5" fill="#d8a76b"/>'
            '</svg>')


NAV_FIX = {'de': 'Wunschliste', 'hi': 'इच्छा सूची', 'ko': '위시리스트', 'ja': 'ほしい物'}

targets = [('C:/wk/Gin-Factory/index.html', 'gin'), ('C:/wk/My-Whiskey-Collection/index.html', 'whisky'),
           ('C:/wk/main/index.html', 'gin_wine'), ('C:/wk/Weinkeller-App/www/index.html', 'gin_wine')]
for path, kind in targets:
    s = open(path, encoding='utf-8').read()
    pat_r = re.compile(r'(<span class="nav-icon">)🗄️?(</span><span data-i18n="nav_racks">)')
    s, n1 = pat_r.subn(lambda m: m.group(1) + shelf('gin' if kind == 'gin' else 'whisky') + m.group(2), s)
    pat_w = re.compile(r'(<span class="nav-icon">)⭐(</span><span data-i18n="nav_wish">)')
    s, n2 = pat_w.subn(lambda m: m.group(1) + STAR + m.group(2), s)
    assert n1 == 1 and n2 == 1, (path, n1, n2)
    # nav_wish Beschriftung
    lang = None
    out = []
    in_i18n = False
    for l in s.split('\n'):
        if l.startswith('const I18N = {'):
            in_i18n = True
        m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', l)
        if in_i18n and m:
            lang = m.group(1)
        m2 = re.match(r'^(\s+)nav_wish: ".*"(,?)$', l)
        if in_i18n and m2 and lang in NAV_FIX:
            l = f'{m2.group(1)}nav_wish: {json.dumps(NAV_FIX[lang], ensure_ascii=False)}{m2.group(2)}'
        out.append(l)
    s = '\n'.join(out)
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('ok', path)
