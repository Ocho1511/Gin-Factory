import sys
sys.stdout.reconfigure(encoding='utf-8')


def bottle(uid, style):
    return f'''<svg viewBox="0 0 32 32" width="1em" height="1em" aria-hidden="true" style="{style}">
<defs>
<linearGradient id="gl{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c9dde8"/><stop offset=".3" stop-color="#f6fbfd"/><stop offset=".68" stop-color="#d3e5ee"/><stop offset="1" stop-color="#a9c3d3"/></linearGradient>
<linearGradient id="lq{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3f0" stop-opacity=".75"/><stop offset="1" stop-color="#7fb7cf" stop-opacity=".85"/></linearGradient>
<linearGradient id="lb{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d4a7c"/><stop offset="1" stop-color="#14213b"/></linearGradient>
<linearGradient id="ck{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6c08a"/><stop offset="1" stop-color="#b78650"/></linearGradient>
<clipPath id="bd{uid}"><path d="M13.4 5.8h5.2v6.4c0 1.8 4.2 2.6 4.2 6.6v7.8a3 3 0 0 1-3 3H12.2a3 3 0 0 1-3-3v-7.8c0-4 4.2-4.8 4.2-6.6z"/></clipPath>
</defs>
<ellipse cx="16" cy="30.7" rx="7.6" ry="1" fill="#000" opacity=".28"/>
<path d="M13.4 5.8h5.2v6.4c0 1.8 4.2 2.6 4.2 6.6v7.8a3 3 0 0 1-3 3H12.2a3 3 0 0 1-3-3v-7.8c0-4 4.2-4.8 4.2-6.6z" fill="url(#gl{uid})"/>
<g clip-path="url(#bd{uid})"><rect x="7" y="14.5" width="18" height="17" fill="url(#lq{uid})"/></g>
<rect x="9.2" y="17.8" width="13.6" height="8.6" fill="url(#lb{uid})"/>
<rect x="10.1" y="18.7" width="11.8" height="6.8" rx=".6" fill="none" stroke="#e9c46a" stroke-width=".55"/>
<path d="M11.4 21.5q1.3-1.5 2.6 0t2.6 0t2.6 0t1.3 0" stroke="#f1d27f" stroke-width=".9" fill="none" stroke-linecap="round"/>
<rect x="12.4" y="23.4" width="7.2" height="1" rx=".5" fill="#f4efe0"/>
<rect x="12.5" y="1.6" width="7" height="4.6" rx="1.3" fill="url(#ck{uid})"/>
<rect x="13" y="5.5" width="6" height="1.5" rx=".4" fill="#14213b"/>
<path d="M11 19.4v6.4" stroke="#fff" stroke-opacity=".75" stroke-width="1.1" stroke-linecap="round"/>
<path d="M14.6 8.2v2.8" stroke="#fff" stroke-opacity=".7" stroke-width=".9" stroke-linecap="round"/>
</svg>'''


if __name__ == '__main__':
    html = '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#17120a;color:#d4af5a;font:14px sans-serif;padding:24px">'
    html += '<div style="display:flex;gap:40px;align-items:flex-end">'
    html += '<div style="font-size:200px;line-height:1">' + bottle('a', 'display:block') + '</div>'
    html += '<div style="font-size:44px;line-height:1">' + bottle('b', 'display:block') + '</div>'
    html += '<div style="font-size:22px;line-height:1;text-align:center">' + bottle('c', 'display:block;margin:0 auto') + '<br><span style="font-size:11px">Bar</span></div>'
    html += '</div>'
    open('C:/wk/Gin-Factory/_tools/icon_preview.html', 'w', encoding='utf-8').write(html)
    print('ok')
