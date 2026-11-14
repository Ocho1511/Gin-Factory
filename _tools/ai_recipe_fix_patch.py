import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')

APPS = [
    ('C:/wk/Gin-Factory/index.html', "sx('rec_pick')", "sx('rec_pick')"),
    ('C:/wk/My-Whiskey-Collection/index.html', "t('sx_rec_pick')", "t('sx_rec_pick')"),
]
for path, pick, _ in APPS:
    s = open(path, encoding='utf-8').read()

    def rep(a, b, count=1):
        global s
        c = s.count(a)
        assert c == count, (path, c, a[:90])
        s = s.replace(a, b)

    # 1) Kein Gin gewaehlt: nicht mehr still abbrechen, sondern Hinweis + Auswahl hervorheben
    rep("  const w = wines.find(x => x.id === id);\n  if (!w) return;\n  recAiBusy = true;",
        "  const w = wines.find(x => x.id === id);\n"
        "  if (!w) {   // nichts gewaehlt: Rueckmeldung geben statt still abzubrechen\n"
        f"    showToast({pick});\n"
        "    const sel = sv('rec-ai-gin');\n"
        "    if (sel) { sel.focus(); sel.style.outline = '2px solid var(--gold)'; setTimeout(() => { sel.style.outline = ''; }, 1600); }\n"
        "    return;\n"
        "  }\n"
        "  recAiGin = id;\n"
        "  recAiBusy = true;")
    # 2) Auswahl bleibt beim Neuzeichnen erhalten
    rep('<option value="${esc(w.id)}">${esc(w.name)}</option>`).join(\'\')}</select>',
        '<option value="${esc(w.id)}"${w.id === recAiGin ? \' selected\' : \'\'}>${esc(w.name)}</option>`).join(\'\')}</select>')
    rep("let recFilter = 'all'", "var recAiGin = '';\nlet recFilter = 'all'")
    open(path, 'w', encoding='utf-8', newline='').write(s)
    c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
    open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
    print(path, 'syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
