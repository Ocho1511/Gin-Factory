import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()
block = open('C:/wk/Gin-Factory/_tools/gin_glass_block.js', encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:90])
    s = s.replace(a, b)


# Formular: oninput am Glas-Feld, Link unter den drei Feldern
rep('<input id="f-serve-glass" type="text"></div>', '<input id="f-serve-glass" type="text" oninput="serveGlassLink()"></div>')
rep('<div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>\n      </div>\n    </div>',
    '<div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>\n      </div>\n'
    '      <a id="serve-glass-link" class="glass-link" href="#" target="_blank" rel="noopener" style="display:none" onclick="return glassClick(this,event)"></a>\n    </div>')
# Link nach Setzen des Glas-Felds aktualisieren
rep("  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';", "  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';\n  serveGlassLink();")
rep("  if (r.glass && sv('f-serve-glass')) sv('f-serve-glass').value = r.glass;", "  if (r.glass && sv('f-serve-glass')) sv('f-serve-glass').value = r.glass;\n  serveGlassLink();")
# Karte: Glas als Link (auch wenn nur Glas gesetzt ist)
rep("  if (!s || !(s.garnish || s.ratio)) return '';\n  return `<div class=\"wine-region\" style=\"margin-top:4px\">🌿 ${esc([s.garnish, s.ratio ? '(' + s.ratio + ')' : ''].filter(Boolean).join(' '))}</div>`;",
    "  if (!s || !(s.garnish || s.ratio || s.glass)) return '';\n"
    "  const a = (s.garnish || s.ratio) ? `<div class=\"wine-region\" style=\"margin-top:4px\">🌿 ${esc([s.garnish, s.ratio ? '(' + s.ratio + ')' : ''].filter(Boolean).join(' '))}</div>` : '';\n"
    "  const g = s.glass ? `<div class=\"wine-region\" style=\"margin-top:2px\">🥂 ${glassLinkHtml(s.glass)}</div>` : '';\n"
    "  return a + g;")
# Rezepte: Glas als Link
rep("${r.glass ? `<div class=\"wine-region\">🥃 ${esc(sx('rec_glass'))}: ${esc(r.glass)}</div>` : ''}",
    "${r.glass ? `<div class=\"wine-region\">🥂 ${esc(sx('rec_glass'))}: ${glassLinkHtml(r.glass)}</div>` : ''}")
# Block einfuegen (vor serveCardLine)
rep('function serveCardLine(w) {', block + '\nfunction serveCardLine(w) {')
css = ('.glass-link { color: var(--gold); font-size: 13px; font-weight: 600; text-decoration: underline; text-underline-offset: 3px; margin: 2px 0 8px; }\n'
       '.glass-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.65); z-index: 10000; display: flex; align-items: center; justify-content: center; padding: 20px; }\n'
       '.glass-card { background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 20px 18px; max-width: 340px; width: 100%; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,.5); }\n'
       '.glass-card svg { display: block; margin: 0 auto 6px; }\n'
       '.glass-card .glass-title { font-family: var(--heading-font, "Playfair Display", serif); font-size: 20px; margin: 4px 0 8px; }\n'
       '.glass-card p { font-size: 14px; line-height: 1.5; color: var(--text-muted); margin: 0 0 12px; }\n'
       '.glass-card .glass-link { display: inline-block; margin: 0 0 14px; }\n'
       '.glass-card .wine-btn { width: 100%; }\n')
s = s.replace('</style>', css + '</style>', 1)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
