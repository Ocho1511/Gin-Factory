import re, math, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'


def glass(gid):
    g = f'url(#{gid})'
    # rosemary sprig: stem from inside the glass up past the rim
    x0, y0, x1, y1 = 39, 30, 48.5, 12
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    needles = []
    n = 9
    for i in range(n):
        t = 0.22 + 0.78 * i / (n - 1)
        px, py = x0 + dx * t, y0 + dy * t
        ln = 4.2 - 1.6 * (i / (n - 1))
        for side in (-1, 1):
            ex = px + ux * ln * 0.75 + side * nx * ln * 0.6
            ey = py + uy * ln * 0.75 + side * ny * ln * 0.6
            needles.append(f'<path d="M{px:.1f} {py:.1f} L{ex:.1f} {ey:.1f}"/>')
    tipx, tipy = x1 + ux * 2.2, y1 + uy * 2.2
    needles.append(f'<path d="M{x1} {y1} L{tipx:.1f} {tipy:.1f}"/>')
    sprig = ('<g fill="none" stroke="#86c79a" stroke-width="1.5" stroke-linecap="round">'
             f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#6fb286" stroke-width="1.7"/>' + ''.join(needles) + '</g>')
    return f'''<g>
          <path d="M21.5 23 Q36 28 50.5 23 C50.5 35 44.5 41.5 36 41.5 C27.5 41.5 21.5 35 21.5 23 Z" fill="rgba(180,225,200,.20)"/>
          <path d="M19.5 17 C19 33 26.5 42.5 36 42.5 C45.5 42.5 53 33 52.5 17" fill="none" stroke="{g}" stroke-width="2.2" stroke-linecap="round"/>
          <ellipse cx="36" cy="17" rx="16.5" ry="3.6" fill="none" stroke="{g}" stroke-width="1.8"/>
          <rect x="34.9" y="42" width="2.2" height="15" rx="1" fill="{g}"/>
          <ellipse cx="36" cy="58" rx="11.5" ry="2.8" fill="rgba(212,175,90,.12)" stroke="{g}" stroke-width="2"/>
          <g fill="rgba(255,255,255,.10)" stroke="{g}" stroke-width="1.2" stroke-linejoin="round">
            <rect x="27.5" y="25.5" width="7.5" height="7.5" rx="1.6" transform="rotate(-10 31 29)"/>
            <rect x="34" y="28.5" width="7" height="7" rx="1.6" transform="rotate(8 37 32)"/>
          </g>
          {sprig}
          <g fill="{g}" opacity=".9"><circle cx="30" cy="38" r=".9"/><circle cx="43" cy="37" r=".8"/><circle cx="26.5" cy="31" r=".7"/></g>
        </g>'''


s = open(P, encoding='utf-8').read()
cnt = 0
for gid in ('spG', 'hbG'):
    pat = re.compile(r'(<svg[^>]*>\s*<defs>\s*<linearGradient id="%s".*?</defs>\s*<circle [^>]*/>\s*<circle cx="36" cy="36" r="29.5"[^>]*/>\s*)(.*?)(\s*</svg>)' % gid, re.S)
    s, n = pat.subn(lambda m: m.group(1) + glass(gid) + m.group(3), s, count=1)
    cnt += n
assert cnt == 2, cnt
open(P, 'w', encoding='utf-8', newline='').write(s)

# --- PNG icons rendered from the same artwork ---
import fitz
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="72" height="72">
<defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dfa0"/><stop offset=".5" stop-color="#d4af5a"/><stop offset="1" stop-color="#a98532"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1f17"/><stop offset="1" stop-color="#17120a"/></linearGradient></defs>
<rect width="72" height="72" fill="url(#bg)"/>
<circle cx="36" cy="36" r="33" fill="rgba(212,175,90,.06)" stroke="url(#gg)" stroke-width="2"/>
<circle cx="36" cy="36" r="29.5" fill="none" stroke="url(#gg)" stroke-width=".8" opacity=".8"/>
{glass('gg')}
</svg>'''
open('C:/wk/Gin-Factory/_tools/logo.svg', 'w', encoding='utf-8').write(svg)
doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
page = doc[0]
for name, px in (('icon-192.png', 192), ('icon-512.png', 512), ('apple-touch-icon.png', 180)):
    z = px / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
    pix.save('C:/wk/Gin-Factory/' + name)
    print(name, pix.width, pix.height)
print('ok')
