import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:100])
    s = s.replace(a, b)


rep('/* Regalkarte: Aktionsknöpfe und Blink-Schalter als Raster (Tabelle) statt untereinander */', '/* Regalkarte: Aktionsknöpfe als Raster (Tabelle) statt untereinander */')
# .ripeness-loc heisst jetzt .slot-chips (Platz-Chips eines Gins auf der Karte)
rep('.card-slots .ripeness-loc {', '.card-slots .slot-chips {')
rep('.ripeness-loc {', '.slot-chips {')
rep('<div class="ripeness-loc">${h}</div>', '<div class="slot-chips">${h}</div>')
# Nachschlagen: keine Trinkfenster-Logik mehr
rep(" Das Trinkfenster beginnt nie vor dem Jahrgang, und drinkTo liegt immer nach drinkFrom.", '')
rep("    const y = parseInt(year);\n    if (info && drinkYearOk(y)) info.drinkFrom = ruleFrom(y, info.drinkFrom);\n", '')
rep("    if (active.id === 'tab-trinkreife') renderTrinkreife();\n", "    if (active.id === 'tab-rezepte') renderRecipes();\n")
rep("// Beim Eintragen von Jahrgang/Name: Trinkfenster sofort lokal, Preis+Rest per KI/Web", "// Beim Eintragen von Jahrgang/Name: Preis und Rest per KI/Web")
rep("Fehlende Region, Land, Rebsorte, Trinkfenster & Preis ergänzen</div>", "Fehlende Region, Land, Botanicals & Preis ergänzen</div>")
rep("// Automatisch gefundene Flaschenbilder (Vivino, KI-Bildsuche, Webseiten) gehören Dritten", "// Automatisch gefundene Flaschenbilder (KI-Bildsuche, Webseiten) gehören Dritten")
# Vivino-Freisteller (gedrehte Flaschenfotos im Regal): gibt es ohne Vivino nicht mehr
rep('''// Nur echte Flaschen-Freisteller (Vivino "_pb_") eignen sich zum Drehen; andere Bilder bleiben außen vor.
function isBottleCutout(u) { return /images\\.vivino\\.com\\/thumbs\\/[^"'\\s]*_pb_/i.test(u || ''); }
''', '')
s, n = re.subn(r"// Flasche fürs Regal: echtes Flaschenfoto.*?\nfunction bottleVisual\(w, W, mode\) \{.*?\n\}\n", "// Flasche fürs Regal: die gezeichnete Flasche (Farbe nach Gin-Stil)\nfunction bottleVisual(w, W, mode) { return bottleSvg(TYPE_FILL[w.type] || TYPE_FILL.other, W, w, mode); }\n", s, count=1, flags=re.S)
assert n == 1
s, n = re.subn(r"// Große Flasche für die Vorschau \(Antippen\):.*?\nfunction bottlePreviewHtml\(w\) \{.*?\n\}\n", "// Große Flasche für die Vorschau (Antippen) mit beschriftetem Etikett\nfunction bottlePreviewHtml(w) { return bottleVisual(w, 232, 'full'); }\n", s, count=1, flags=re.S)
assert n == 1
rep("const pw = g.w, cut = isBottleCutout(shownImage(pw));", "const pw = g.w;")
rep("${cut ? '' : esc(pw.name) + (pw.year ? ' · ' + pw.year : '') + (g.n > 1 ? ' ×' + g.n : '')}<span${cut ? ' style=\"margin-top:0;font-size:12px\"' : ''}>${esc(formatLocation(pw))}</span>",
    "${esc(pw.name) + (pw.year ? ' · ' + pw.year : '') + (g.n > 1 ? ' ×' + g.n : '')}<span>${esc(formatLocation(pw))}</span>")
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
