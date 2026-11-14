import re, sys
sys.stdout.reconfigure(encoding='utf-8')

ICON = ('<svg viewBox="0 0 32 32" width="0.8em" height="0.8em" aria-hidden="true" style="display:block;margin:.1em auto">'
        '<defs>'
        '<linearGradient id="stA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1d27f"/><stop offset="1" stop-color="#c9a24b"/></linearGradient>'
        '<linearGradient id="stB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fd3c2"/><stop offset="1" stop-color="#2b8f84"/></linearGradient>'
        '<linearGradient id="stC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c4f2"/><stop offset="1" stop-color="#5f86c4"/></linearGradient>'
        '</defs>'
        '<rect x="3.5" y="17" width="6.6" height="11" rx="1.7" fill="url(#stA)"/>'
        '<rect x="12.7" y="10" width="6.6" height="18" rx="1.7" fill="url(#stB)"/>'
        '<rect x="21.9" y="3.5" width="6.6" height="24.5" rx="1.7" fill="url(#stC)"/>'
        '<rect x="2" y="29" width="28" height="1.3" rx=".65" fill="#8f8a7a" opacity=".55"/>'
        '</svg>')

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    old = '<span class="nav-icon">📊</span>'
    assert s.count(old) == 1, (path, s.count(old))
    s = s.replace(old, '<span class="nav-icon">' + ICON + '</span>')
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('ok', path)
