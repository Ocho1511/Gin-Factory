import sys, math
sys.stdout.reconfigure(encoding='utf-8')

SIZE = 'width="0.8em" height="0.8em" aria-hidden="true" style="display:block;margin:.1em auto"'


def arrow(cx, up, fill):
    # runde Pfeile: Kopf 13 breit, Schaft 4.6 breit
    if up:
        pts = [(cx, 4), (cx + 6.5, 12), (cx + 2.3, 12), (cx + 2.3, 27), (cx - 2.3, 27), (cx - 2.3, 12), (cx - 6.5, 12)]
    else:
        pts = [(cx, 28), (cx + 6.5, 20), (cx + 2.3, 20), (cx + 2.3, 5), (cx - 2.3, 5), (cx - 2.3, 20), (cx - 6.5, 20)]
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{fill}" stroke-width="1.6" stroke-linejoin="round"/>'


def export_icon():
    return (f'<svg viewBox="0 0 32 32" {SIZE}><defs>'
            '<linearGradient id="exA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fe0cf"/><stop offset="1" stop-color="#2b9d90"/></linearGradient>'
            '<linearGradient id="exB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dc8a"/><stop offset="1" stop-color="#d09a2e"/></linearGradient>'
            '</defs>' + arrow(9.5, True, 'url(#exA)') + arrow(22.5, False, 'url(#exB)') + '</svg>')


def history_icon():
    return (f'<svg viewBox="0 0 32 32" {SIZE}><defs>'
            '<linearGradient id="hiA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dc8a"/><stop offset="1" stop-color="#c9a24b"/></linearGradient>'
            '</defs>'
            '<circle cx="17" cy="16" r="11" fill="#2b4a7c" fill-opacity=".35"/>'
            '<path d="M6.2 16A10.8 10.8 0 1 1 9.4 23.7" fill="none" stroke="url(#hiA)" stroke-width="2.8" stroke-linecap="round"/>'
            '<path d="M1.6 12.2L6.4 17.6L10.6 12.4z" fill="#f1d27f" stroke="#f1d27f" stroke-width="1.2" stroke-linejoin="round"/>'
            '<path d="M17 9.5V16.4L21.6 19.2" fill="none" stroke="#f4efe0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '</svg>')


def setup_icon():
    teeth = ''.join(f'<rect x="13.7" y="2.4" width="4.6" height="6" rx="1.2" transform="rotate({i * 45} 16 16)"/>' for i in range(8))
    return (f'<svg viewBox="0 0 32 32" {SIZE}><defs>'
            '<linearGradient id="seA" gradientUnits="userSpaceOnUse" x1="0" y1="2" x2="0" y2="30"><stop offset="0" stop-color="#c3cfdc"/><stop offset="1" stop-color="#7b8ba1"/></linearGradient>'
            '</defs>'
            f'<g fill="url(#seA)">{teeth}'
            '<path fill-rule="evenodd" d="M16 5.9a10.1 10.1 0 1 0 .01 0zM16 11.7a4.3 4.3 0 1 1-.01 0z"/></g>'
            '</svg>')


if __name__ == '__main__':
    html = '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#17120a;color:#d4af5a;font:14px sans-serif;padding:24px">'
    for fn in (history_icon, export_icon, setup_icon):
        html += '<div style="display:flex;gap:30px;align-items:flex-end;margin-bottom:20px"><div style="font-size:150px;line-height:1">' + fn().replace('id="', 'id="b') .replace('url(#', 'url(#b') + '</div>'
        html += '<div style="font-size:19px;line-height:1">' + fn() + '</div></div>'
    open('C:/wk/Gin-Factory/_tools/nav_preview.html', 'w', encoding='utf-8').write(html)
    print('ok')
