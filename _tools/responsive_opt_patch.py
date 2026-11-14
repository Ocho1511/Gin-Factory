import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')

CSS = '''/* Glas-Karte: nie hoeher als der Bildschirm (Handy quer), kleine Zeichnung bei wenig Hoehe */
.glass-card { max-height: 100%; overflow-y: auto; box-sizing: border-box; }
@media (max-height: 520px) { .glass-card { padding: 12px 16px; } .glass-card svg { width: 84px; height: 84px; } .glass-card p { font-size: 13px; margin-bottom: 8px; } .glass-card .glass-title { margin: 0 0 4px; } .glass-card .glass-link { margin-bottom: 8px; } }
'''

for path in ('C:/wk/Gin-Factory/index.html', 'C:/wk/My-Whiskey-Collection/index.html'):
    s = open(path, encoding='utf-8').read()

    def rep(a, b, count=1):
        global s
        c = s.count(a)
        assert c == count, (path, c, a[:80])
        s = s.replace(a, b)

    # 1) CSS
    s = s.replace('</style>', CSS + '</style>', 1)
    # 2) Leistenschrift darf auf sehr schmalen Handys (<370 px) weiter schrumpfen
    rep("    while (el.scrollWidth > room() && size > 8 && guard++ < 6) { size -= 0.5; el.style.fontSize = size + 'px'; }",
        "    const minSize = innerWidth < 370 ? 6.5 : 8;   // sehr schmale Handys (320 px): lange Woerter wie 'Statistiche' duerfen kleiner werden\n"
        "    while (el.scrollWidth > room() && size > minSize && guard++ < 9) { size -= 0.5; el.style.fontSize = size + 'px'; }")
    # 3) Suche entprellen
    rep('oninput="renderKeller()"', 'oninput="renderKellerDebounced()"')
    rep('function fitNavLabels() {', "let _searchTimer = 0;\nfunction renderKellerDebounced() { clearTimeout(_searchTimer); _searchTimer = setTimeout(renderKeller, 120); }   // nicht bei jedem Tastendruck die ganze Liste neu bauen\nfunction fitNavLabels() {")
    open(path, 'w', encoding='utf-8', newline='').write(s)
    c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
    open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
    print(path, 'syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
