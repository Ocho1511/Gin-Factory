import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()
size0, lines0 = len(s.encode('utf-8')), s.count('\n') + 1
log = []


def rep(a, b, count=1, note=None):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:100])
    s = s.replace(a, b)


def rerep(pattern, repl, count=1, flags=re.S):
    global s
    s, n = re.subn(pattern, repl, s, flags=flags)
    assert n == count, (n, count, pattern[:100])


def _lines():
    return s.split('\n')


def del_func(name):
    """Top-Level-Funktion samt direkt davor stehenden //-Kommentaren entfernen."""
    global s
    L = _lines()
    idx = [i for i, l in enumerate(L) if re.match(r'^(?:async\s+)?function\s+' + re.escape(name) + r'\s*\(', l)]
    assert len(idx) == 1, (name, idx)
    i = idx[0]
    if L[i].rstrip().endswith('}') and L[i].count('{') == L[i].count('}'):
        j = i
    else:
        j = next(k for k in range(i + 1, len(L)) if L[k].startswith('}'))
    a = i
    while a > 0 and L[a - 1].startswith('//'):
        a -= 1
    del L[a:j + 1]
    s = '\n'.join(L)
    log.append('func ' + name)


def del_const(name, end_re=None):
    """const/let-Zeile (ggf. mehrzeilig bis end_re) samt vorangehenden //-Kommentaren entfernen."""
    global s
    L = _lines()
    idx = [i for i, l in enumerate(L) if re.match(r'^(?:const|let|var)\s+' + re.escape(name) + r'\b', l)]
    assert len(idx) == 1, (name, idx)
    i = idx[0]
    if end_re:
        j = next(k for k in range(i, len(L)) if re.match(end_re, L[k]))
    else:
        j = i
    a = i
    while a > 0 and L[a - 1].startswith('//'):
        a -= 1
    del L[a:j + 1]
    s = '\n'.join(L)
    log.append('const ' + name)


# ============================ CSS ============================
rep('''/* Gin-Factory: Gin reift nicht -> Trinkreife/Temperatur ausblenden */
.nav-btn[onclick*="trinkreife"], #drinkrule-btn, .form-row:has(#f-drink-from), .form-row:has(#f-temp-from),
.form-group:has([data-i18n="setup_tempunit"]), .wine-ripeness, .wine-temp { display: none !important; }
''', '')
# Reife-Balken auf der Karte
rerep(r'\.wine-ripeness \{.*?\n\}\n\.wine-ripeness-bar \{.*?\n\}\n\.ripeness-jung \{[^\n]*\n\.ripeness-optimal \{[^\n]*\n\.ripeness-peak \{[^\n]*\n\.ripeness-over \{[^\n]*\n', '')
# Regal: Reife-Punkt, Legende, Blink-Schalter
for pat in [r'\.rack-ripe \{[^\n]*\n', r'\.rack-slot\.tiny \.rack-ripe \{[^\n]*\n', r'\.wine-temp, \.ripeness-temp \{[^\n]*\n',
            r'\.rack-legend \{[^\n]*\n', r'\.rack-legend span \{[^\n]*\n', r'\.rack-ripe-dot \{[^\n]*\n',
            r'\.rack-toolbar \{[^\n]*\n', r'\.rack-toolbar-lbl \{[^\n]*\n', r'\.rack-toggle \.rack-ripe-dot \{[^\n]*\n',
            r'\.rack-toggle \{[^\n]*\n', r'\.rack-toggle \.rt-dot \{[^\n]*\n', r'\.rack-toggle \.rt-dot::after \{[^\n]*\n',
            r'\.rack-toggle\.active \{[^\n]*\n', r'\.rack-toggle\.active \.rt-dot \{[^\n]*\n', r'\.rack-toggle\.active \.rt-dot::after \{[^\n]*\n',
            r'\.rack-blink-hint \{[^\n]*\n', r'@keyframes rackBlink \{[^\n]*\n', r'@keyframes rackDot \{[^\n]*\n',
            r'\.rack-box\.blink-on [^\n]*\n', r'\.rack-slot\.blinking \{ border-radius[^\n]*\n', r'\.rack-slot\.blinking \.rack-ripe \{ animation: rackDot[^\n]*\n']:
    rerep('^' + pat, '', 1, flags=re.M)
rep('''@media (prefers-reduced-motion: reduce) {
  .rack-slot.blinking { animation: none; box-shadow: 0 0 0 2px rgba(255,90,90,.9); }
  .rack-slot.blinking .rack-ripe { animation: none; }
}
''', '')
rep('.rack-slot.moving > :not(.rack-ripe):not(.rack-slot-count) { opacity: .55; }', '.rack-slot.moving > :not(.rack-slot-count) { opacity: .55; }')
rep(', .rack-toggle:active', '', 1) if ', .rack-toggle:active' in s else None
# Trinkreife-Reiter
rerep(r'/\* ── TRINKREIFE TAB ── \*/\n.*?(?=/\* ── WISHLIST TAB ── \*/)', '')
for pat in [r'#trinkreife-list \{ display: grid; grid-template-columns: repeat\(2[^\n]*\n', r'#trinkreife-list > \.empty-state[^\n]*\n',
            r'\.ripeness-card \{ margin: 0 8px 12px 16px; \}\n', r'#trinkreife-list > :nth-child\(even\) \.ripeness-card, #trinkreife-list > \.ripeness-card:nth-child\(even\) \{ margin: 0 16px 12px 8px; \}\n',
            r'#trinkreife-list \{ grid-template-columns: repeat\(3[^\n]*\n',
            r'\.ripeness-card, #trinkreife-list > :nth-child\(even\) \.ripeness-card[^\n]*\n']:
    rerep('^[ 	]*' + pat, '', 1, flags=re.M)   # innerhalb der @media-Bloecke eingerueckt

# ============================ HTML ============================
rep('''<div class="tab" id="tab-trinkreife">
  <div class="page-header">
    <h1 data-i18n="ripe_title">Trinkreife</h1>
    <div class="subtitle" data-i18n="ripe_sub">Wann trinken?</div>
  </div>
  <div class="filter-scroll" id="ripe-filter-type" style="padding-bottom:8px"></div>
  <div class="filter-scroll" id="ripe-filter-status"></div>
  <div id="trinkreife-list"></div>
</div>

''', '')
rep('''     TRINKREIFE TAB
════════════════════════════════════════ -->
<div class="tab" id="tab-rezepte">''', '''     REZEPTE TAB
════════════════════════════════════════ -->
<div class="tab" id="tab-rezepte">''')
rep('''    <div class="form-group" style="margin-top:14px">
      <label data-i18n="setup_tempunit">Temperatureinheit</label>
      <select id="setup-tempunit" onchange="setTempUnit(this.value)">
        <option value="C">°C (Celsius)</option>
        <option value="F">°F (Fahrenheit)</option>
      </select>
    </div>
''', '')
rep('''      <div class="export-card" id="drinkrule-btn" onclick="recalcDrinkWindows()" style="margin-top:10px">
        <div class="export-icon">📅</div>
        <div class="export-info">
          <div class="title" data-i18n="drinkrule_btn">Trinkfenster neu berechnen</div>
          <div class="desc" data-i18n="drinkrule_desc">Trinken ab = Jahrgang + 1; Trinken bis nach Weinart und Rebsorte</div>
        </div>
      </div>
''', '')
rep('''    <div class="form-row">
      <div class="form-group">
        <label data-i18n="l_from">Trinken ab</label>
        <input id="f-drink-from" placeholder="" type="number">
      </div>
      <div class="form-group">
        <label data-i18n="l_to">Trinken bis</label>
        <input id="f-drink-to" placeholder="" type="number">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label data-i18n="l_temp_from">Trinktemperatur ab (°C)</label>
        <input id="f-temp-from" placeholder="" type="number" min="0" max="30" step="any">
      </div>
      <div class="form-group">
        <label data-i18n="l_temp_to">bis (°C)</label>
        <input id="f-temp-to" placeholder="" type="number" min="0" max="30" step="any">
      </div>
    </div>
''', '')

# ============================ JS: Funktionen/Konstanten entfernen ============================
for f in ['cleanTemps', 'serveTempText', 'applyTempLabels', 'setTempUnit', 'fixDrinkWindow', 'maturationOffset', 'recalcDrinkWindows',
          'fixFormDrinkWindow', 'autoFillDrinkWindow', 'wineCriteria', 'formCriteria', 'wineNameMatches', 'vivinoImageFor',
          'getRipenessInfo', 'ripeInfo', 'toggleRackBlink', 'ripeStatusKey', 'ripeOverdue', 'setRipeFilterType', 'setRipeFilterStatus',
          'renderTrinkreife', 'onVintageInput']:
    del_func(f)
for c in ['tempUnit', 'tempToDisplay', 'tempFromInput', 'tempKeep', 'serveTempHtml', 'drinkYearOk', 'ruleFrom', 'autoDrink',
          'RIPE_PRIO', 'RIPE_CLASS', 'ripeFilterType', 'ripeFilterStatus', 'NAME_STOP', 'NAME_GRAPES']:
    del_const(c)
del_const('MATURATION_GRAPE', r'^\};')
del_const('MATURATION_TYPE')

# ============================ JS: Verwendungen bereinigen ============================
# cleanWine
rep("  const dw = fixDrinkWindow(yearV, w.type, w.grape, cleanInt(w.drinkFrom, 1000, 2300), cleanInt(w.drinkTo, 1000, 2300));\n", '')
rep("    drinkFrom: dw.from, drinkTo: dw.to,\n    ...cleanTemps(w),\n", '')
# settings / Einstellungen
rep("racks:[], cellars:[], blinkUrgent:false, blinkOver:false, blinkPeak:false, blinkOptimal:false, celeb:'both'", "racks:[], cellars:[], celeb:'both'")
rep("const PREF_KEYS = ['lang', 'currency', 'font', 'celeb', 'tempUnit', 'blinkUrgent', 'blinkOver', 'blinkPeak', 'blinkOptimal'];", "const PREF_KEYS = ['lang', 'currency', 'font', 'celeb'];")
rep("  if (p.tempUnit === 'C' || p.tempUnit === 'F') o.tempUnit = p.tempUnit;\n  ['blinkUrgent', 'blinkOver', 'blinkPeak', 'blinkOptimal'].forEach(k => { if (typeof p[k] === 'boolean') o[k] = p[k]; });\n", '')
rep(" set('setup-tempunit', settings.tempUnit === 'F' ? 'F' : 'C');", '')
rep("  applyTempLabels();\n  updateCreditsUI();", "  updateCreditsUI();")
rep("  // Englisch (US): Fahrenheit als Standard; beim Wechsel weg von US zurück auf Celsius\n  if (l === 'us' && was !== 'us') settings.tempUnit = 'F';\n  else if (was === 'us' && l !== 'us' && settings.tempUnit === 'F') settings.tempUnit = 'C';\n", '')
rep("  const tu = document.getElementById('setup-tempunit'); if (tu) tu.value = settings.tempUnit === 'F' ? 'F' : 'C';\n  applyTempLabels(); rerenderActive();", "  rerenderActive();")
rep("  const was = settings.lang;\n  settings.lang = l;", "  settings.lang = l;")
rep("    document.getElementById('setup-tempunit').value = tempUnit();\n", '')
# Reiter
rep("  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n", '')
rep("  if (name === 'trinkreife') renderTrinkreife();\n", '')
rep("(name === 'keller' || name === 'trinkreife') ? 'flex' : 'none'", "name === 'keller' ? 'flex' : 'none'")
rep("  if (active && active.id === 'tab-trinkreife') renderTrinkreife();\n  else if (active && active.id === 'tab-racks')", "  if (active && active.id === 'tab-racks')")
# Sortierung nach Reife
rerep(r"  else if \(sortMode === 'ripeness'\) \{\n    const rmap = new Map\(list\.map\(w => \[w, getRipenessInfo\(w\)\]\)\);.*?\n    \}\);\n  \}\n", '')
# Karte
rep("    const ripe = getRipenessInfo(w);\n", '')
rep("      ${serveTempHtml(w, 'wine-temp')}\n", '')
rep("""      ${ripe ? `
      <div class="wine-ripeness">
        <div class="wine-ripeness-bar ${ripe.cls}" style="width:${ripe.pct}%"></div>
      </div>` : ''}
""", '')
rep('<div class="icon">🍷</div><p>${t(\'empty_keller\')}</p>', '<div class="icon">${ginIco()}</div><p>${t(\'empty_keller\')}</p>')
# Bearbeiten-Formular
rep("  document.getElementById('f-drink-from').value = w.drinkFrom||'';\n  document.getElementById('f-drink-to').value = w.drinkTo||'';\n  document.getElementById('f-temp-from').value = tempToDisplay(w.tempFrom);\n  document.getElementById('f-temp-to').value = tempToDisplay(w.tempTo);\n", '')
rep("  autoDrink = { from: null, to: null };\n", '')
rep("'f-abv','f-tonic','f-drink-from','f-drink-to','f-temp-from','f-temp-to','f-price'", "'f-abv','f-tonic','f-price'")
rep("    drinkFrom: parseInt(document.getElementById('f-drink-from').value)||null,\n    drinkTo: parseInt(document.getElementById('f-drink-to').value)||null,\n", '')
rerep(r"    tempFrom: tempKeep\([^\n]*\n", '')
rep("'locRegal','locEbene','locPlatz','drinkFrom','drinkTo','tempFrom','tempTo','price'", "'locRegal','locEbene','locPlatz','price'")
# Etikett-Scan
rerep(r"    \{ const yy = parseInt\(document\.getElementById\('f-year'\)\.value\); const df = ruleFrom[^\n]*\n    if \(info\.drinkTo\)[^\n]*\n    fixFormDrinkWindow\(\);\n    if \(info\.tempFrom != null\)[^\n]*\n    if \(info\.tempTo != null\)[^\n]*\n    showToast\(info\.drinkFrom \|\| info\.drinkTo \? t\('toast_label_ripe'\) : t\('toast_label'\)\);\n", "    showToast(t('toast_label'));\n")
# Nachschlagen / Preis
rerep(r"    setIfEmpty\('f-drink-from', info\.drinkFrom\);\n    setIfEmpty\('f-drink-to', info\.drinkTo\);\n    fixFormDrinkWindow\(\);\n    setIfEmpty\('f-temp-from'[^\n]*\n    setIfEmpty\('f-temp-to'[^\n]*\n", '', 2)
rep("    const img = await resolveWineImage(info, formCriteria());\n", "    const img = await resolveWineImage(info);\n", 2)
rep("info.region || info.land || info.grape || info.drinkFrom || info.drinkTo || info.tempFrom != null || info.price != null", "info.region || info.land || info.grape || info.price != null")
# Bildauflosung ohne Vivino
rerep(r"async function resolveWineImage\(info, crit, meta\) \{\n  if \(autoImagesOff\(\)\) return null;[^\n]*\n  const viv = null;[^\n]*\n  if \(viv\) \{[^\n]*\n", "async function resolveWineImage(info) {\n  if (autoImagesOff()) return null;   // Store-Version: keine automatischen Fremdbilder\n")
rep("// Reihenfolge: Vivino-Flaschenbild (alle Kriterien gebündelt) → KI-Direktbild → og:image der Wein-Seite. Gibt nur eine NACHWEISLICH ladbare URL zurück (sonst null).\n// crit = { name, year, region, country, grape }\n",
    "// Reihenfolge: KI-Direktbild → og:image der Seite zum Gin. Gibt nur eine NACHWEISLICH ladbare URL zurück (sonst null).\n")
# Alle-Gins-aktualisieren (KI): Bild-Schritt (Vivino) entfaellt, Temperatur-/Trinkfenster-Ergaenzung entfaellt
rerep(r"let enrichRunning = false, enrichRetryMs = \[8000, 16000\];[^\n]*\n", "let enrichRunning = false;\n")
rep("  // Alle Weine durchlaufen: fehlende Felder ergänzen UND Flaschenbild erneuern (auch vorhandene/tote Bilder ersetzen)\n", "  // Alle Gins durchlaufen: fehlende Felder (Region, Land, Botanicals, Preis) ergänzen; fehlendes Flaschenbild per KI-Direktbild / og:image\n")
rep("  // Gibt es schon Trinktemperaturen: bewusst fragen, ob sie (auch selbst eingetragene) durch KI-Werte ersetzt werden sollen; sonst werden nur fehlende ergänzt\n  const overwriteTemp = targets.some(w => w.tempFrom != null) && confirm(t('confirm_enrich_temp'));\n", "  const missingFields = (w) => !w.region || !w.country || !w.grape || !w.price;\n")
rep("    const needAi = overwriteTemp ? targets.length : targets.filter(w => !w.region || !w.country || !w.grape || !w.drinkFrom || !w.drinkTo || w.tempFrom == null || !w.price).length;", "    const needAi = targets.filter(missingFields).length;")
rep("  let updated = 0, imgFailed = 0;", "  let updated = 0;")
rerep(r"        // 1\) Flaschenbild zuerst \(schnell, Vivino;.*?\n        \}   // Store-Version: Bilder bleiben unangetastet \(auch von der Web-App synchronisierte\)\n        // 2\) Langsamen KI-Websuche-Aufruf nur, wenn Textfelder fehlen \(sonst überspringen → Lauf bleibt schnell\)\n        const needsFields = [^\n]*\n",
      "        // Langsamen KI-Websuche-Aufruf nur, wenn Textfelder oder das Bild fehlen (sonst überspringen → Lauf bleibt schnell)\n        const needsFields = missingFields(w);\n")
rerep(r"            if \(!w\.drinkFrom && info\.drinkFrom\)[^\n]*\n            if \(!w\.drinkTo && info\.drinkTo\)[^\n]*\n            \{ const fx = fixDrinkWindow[^\n]*\n            if \(\(w\.tempFrom == null \|\| overwriteTemp\)[^\n]*\n", '')
rep("            // Falls Vivino kein Bild hatte: KI-Direktbild / og:image als Rückfall (mit jetzt ggf. ergänzten Kriterien)\n            if (!w.image && !autoImagesOff()) { const alt = await resolveWineImage(info, wineCriteria(w), { noVivino: true }); if (alt) { w.image = alt; changed = true; } }",
    "            // KI-Direktbild / og:image, falls noch kein Bild da ist\n            if (!w.image && !autoImagesOff()) { const alt = await resolveWineImage(info); if (alt) { w.image = alt; changed = true; } }")
rep("  showToast(imgFailed ? t('toast_enrich_done', {n: updated}) + '<br>' + t('enrich_img_fail', {n: imgFailed}) : t('toast_enrich_done', {n: updated}));", "  showToast(t('toast_enrich_done', {n: updated}));")
rep('''// ═══════════════════════════════════════
// TRINKREIFE
// ═══════════════════════════════════════
function goToFilter(type) {''','''// ═══════════════════════════════════════
// NAVIGATION: Filter bzw. Gin in der Bar anspringen
// ═══════════════════════════════════════
function goToFilter(type) {''')
# Import (Spaltenindex)
rep("rating: col('bewertung'), price: col('preis'),\n    drinkFrom: col('trinken ab'), drinkTo: col('trinken bis'), note: col('notiz')", "rating: col('bewertung'), price: col('preis'), note: col('notiz')")
# Start: Listener
rep("document.getElementById('f-year').addEventListener('change', onVintageInput);", "document.getElementById('f-year').addEventListener('change', maybeAutoLookup);")
rep("document.getElementById('f-grape').addEventListener('change', autoFillDrinkWindow);\ndocument.getElementById('f-type').addEventListener('change', autoFillDrinkWindow);\n", '')
# KI-Prompts: Felder, die immer null waren
n_before = s.count('drinkFrom')
s = re.sub(r"drinkFrom \(immer null\), drinkTo \(immer null\), tempFrom \(immer null\), tempTo \(immer null\), ", '', s)
s = re.sub(r" drinkFrom, drinkTo, tempFrom und tempTo sind immer null \(Gin reift nicht\)\.", '', s)
log.append('prompts cleaned: drinkFrom mentions %d -> %d' % (n_before, s.count('drinkFrom')))

# ============================ Regal: Blinken, Reife-Punkt, Legende ============================
rerep(r"  // Trinkreife-Punkt an jeder Flasche; auf Wunsch blinken Weine nach Trinkreife \(jede Gruppe einzeln wählbar\)\n  const BLINKS = .*?\n  \}\);\n(?=  const sw = rackStoreFilter)", '')
rerep(r"</div><div class=\"rack-toolbar\"><span class=\"rack-toolbar-lbl\">\$\{t\('rack_blink_lbl'\)\}</span>`\n    \+ BLINKS\.map\(.*?\.join\(''\)\n    \+ `</div>`\n    \+ \(blinkOn\.Urgent \? .*?: ''\)\n    \+ `<div class=\"rack-box\$\{blink \? ' blink-on' : ''\}\">",
      "</div>`\n    + `<div class=\"rack-box\">")
rerep(r"        let topKey = null, urgent = false;[^\n]*\n        entries\.forEach\(x => \{ const ri = ripeInfo[^\n]*\n        const dot = topKey [^\n]*\n", '')
rep("${urgent ? ' blinking' : ''}${slotW < 30", "${slotW < 30")
rep("${bottleVisual(w, slotW, slotMode)}${badge}${dot}</div>", "${bottleVisual(w, slotW, slotMode)}${badge}</div>")
rerep(r"  html \+= `<div class=\"rack-legend\">` \+ \['young', 'optimal', 'peak', 'over'\]\.map\([^\n]*\n\n", "\n")

open(P, 'w', encoding='utf-8', newline='').write(s)
size1, lines1 = len(s.encode('utf-8')), s.count('\n') + 1
print('\n'.join(log))
print('Zeilen %d -> %d (%d weniger), Bytes %d -> %d (%d weniger)' % (lines0, lines1, lines0 - lines1, size0, size1, size0 - size1))
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
r = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True)
print('syntax', r.returncode, r.stderr[:400])
