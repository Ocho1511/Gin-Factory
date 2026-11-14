import re, json, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:90])
    s = s.replace(a, b)


block = open('C:/wk/Gin-Factory/_tools/serve_block.js', encoding='utf-8').read()

# 1) code block before splashInit()
rep('\nsplashInit();', '\n' + block + '\nsplashInit();')

# 2) data model: cleanRecipes/cleanIdList must exist before settings init -> they are function declarations (hoisted); settings defaults
rep("email:'', font:'inter'}, safeParse(SETTINGS_KEY, {}));", "email:'', font:'inter', recipes:[], favRecipes:[], herbs:[]}, safeParse(SETTINGS_KEY, {}));\nsettings.recipes = cleanRecipes(settings.recipes); settings.favRecipes = cleanIdList(settings.favRecipes); settings.herbs = cleanIdList(settings.herbs);")
rep("  return { dv: 3, wines, wishes, drunkWines, racks: settings.racks || [], cellars: settings.cellars || [], owner: settings.owner || '', prefs: collectPrefs() };",
    "  return { dv: 3, wines, wishes, drunkWines, racks: settings.racks || [], cellars: settings.cellars || [], owner: settings.owner || '', prefs: collectPrefs(), recipes: settings.recipes || [], favRecipes: settings.favRecipes || [], herbs: settings.herbs || [] };")
rep("  settings.owner = cleanStr(d.owner, 60);\n  persistAll();\n  adoptPrefs(d.prefs);",
    "  settings.owner = cleanStr(d.owner, 60);\n  settings.recipes = cleanRecipes(d.recipes); settings.favRecipes = cleanIdList(d.favRecipes); settings.herbs = cleanIdList(d.herbs);\n  persistAll();\n  adoptPrefs(d.prefs);")
rep("  if (!settings.owner && d.owner) settings.owner = cleanStr(d.owner, 60);\n  persistAll();\n}",
    "  if (!settings.owner && d.owner) settings.owner = cleanStr(d.owner, 60);\n  settings.recipes = mergeById(settings.recipes || [], cleanRecipes(d.recipes));\n  settings.favRecipes = cleanIdList((settings.favRecipes || []).concat(d.favRecipes || []));\n  settings.herbs = cleanIdList((settings.herbs || []).concat(d.herbs || []));\n  persistAll();\n}")
rep("    tonic: cleanText(w.tonic, 200),\n", "    tonic: cleanText(w.tonic, 200),\n    serve: cleanServe(w.serve),\n")

# 3) form HTML: Perfect Serve group after tonic group
rep('''      <datalist id="dl-tonic"></datalist>
    </div>''', '''      <datalist id="dl-tonic"></datalist>
    </div>
    <div class="form-group" id="serve-group">
      <label data-i18n="serve_title">Perfect Serve (Kräuter, Garnitur, Mischung)</label>
      <div class="serve-btns">
        <button type="button" class="wine-btn" onclick="serveFill('rules')" data-i18n="serve_rules_btn">🌿 Regel-Empfehlung</button>
        <button type="button" class="wine-btn primary" onclick="serveFill('ai')" data-i18n="serve_ai_btn">🤖 KI-Empfehlung</button>
      </div>
      <div id="serve-reco"></div>
      <input id="f-serve-garnish" type="text" oninput="serveRenderReco()" data-i18n-ph="serve_garnish_ph" placeholder="Kräuter und Garnitur, mit Komma getrennt">
      <div class="form-row" style="margin-top:8px">
        <div class="form-group"><label data-i18n="serve_ratio">Mischung</label><input id="f-serve-ratio" type="text" placeholder="1:2"></div>
        <div class="form-group"><label data-i18n="serve_glass">Glas</label><input id="f-serve-glass" type="text"></div>
        <div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>
      </div>
    </div>''')

# 4) form load / clear / save / merge
rep("  document.getElementById('f-tonic').value = w.tonic||'';\n", "  document.getElementById('f-tonic').value = w.tonic||'';\n  serveWriteForm(w.serve);\n")
n = s.count("'f-photo'].forEach(id => document.getElementById(id).value = '');")
assert n == 1, n
rep("'f-photo'].forEach(id => document.getElementById(id).value = '');", "'f-photo'].forEach(id => document.getElementById(id).value = '');\n  serveWriteForm(null);")
rep("    tonic: document.getElementById('f-tonic').value.trim()||null,\n", "    tonic: document.getElementById('f-tonic').value.trim()||null,\n    serve: serveReadForm(),\n")
rep("['region','country','grape','abv','tonic',", "['region','country','grape','abv','tonic','serve',")

# 5) card line (tonic favourite + garnish)
rep("  return w.tonic ? `<div class=\"wine-region\" style=\"margin-top:4px\">🥤 ${esc(w.tonic)}</div>` : '';\n}",
    "  return (w.tonic ? `<div class=\"wine-region\" style=\"margin-top:4px\">🥤 ${esc(w.tonic)}</div>` : '') + serveCardLine(w);\n}")

# 6) navigation: replace hidden Trinkreife tab by Rezepte
m = re.search(r'<button class="nav-btn" onclick="showTab\(\'trinkreife\',this\)">\s*<span class="nav-icon">[^<]*</span><span data-i18n="nav_ripe">[^<]*</span>', s)
assert m, 'nav'
s = s.replace(m.group(0), '<button class="nav-btn" onclick="showTab(\'rezepte\',this)">\n    <span class="nav-icon">🍹</span><span data-i18n="nav_recipes">Rezepte</span>')
rep('<div class="tab" id="tab-trinkreife">', '''<div class="tab" id="tab-rezepte">
  <div class="page-header">
    <h1 data-i18n="nav_recipes">Rezepte</h1>
    <div class="subtitle" data-i18n="rec_subtitle">Gin & Tonic und Cocktails</div>
  </div>
  <div id="recipes-content"></div>
</div>

<div class="tab" id="tab-trinkreife">''')
rep("  if (name === 'trinkreife') renderTrinkreife();\n", "  if (name === 'trinkreife') renderTrinkreife();\n  if (name === 'rezepte') renderRecipes();\n")
rep("  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n", "  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n  else if (a.id === 'tab-rezepte') renderRecipes();\n")

# 7) CSS
s = s.replace('</style>', '''.serve-btns { display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.serve-btns .wine-btn { flex: 1; width: auto; }
.serve-tip { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 6px 0; }
.serve-why { font-size: 12px; color: var(--text-muted); flex: 1; min-width: 120px; }
.serve-shelf { font-size: 12px; color: var(--text-muted); margin: 6px 0; }
.rec-list { padding: 0 16px; display: flex; flex-direction: column; gap: 10px; }
.rec-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; }
.rec-card summary { cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 8px; list-style: none; }
.rec-card summary::-webkit-details-marker { display: none; }
.rec-name { font-family: var(--heading-font, 'Playfair Display', serif); font-size: 16px; }
.rec-fav { background: none; border: none; font-size: 20px; cursor: pointer; color: var(--gold); }
.rec-h { font-weight: 700; font-size: 12px; margin-top: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; }
.rec-card ul { margin: 4px 0 4px 18px; padding: 0; font-size: 14px; }
.rec-card p { font-size: 14px; margin: 4px 0; }
.rec-box { margin: 16px; padding: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 14px; }
.rec-box input, .rec-box textarea, .rec-box select { width: 100%; margin-top: 8px; box-sizing: border-box; }
.shelf-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
</style>''', 1)
# keep the old Trinkreife nav rule harmless; nothing to remove

# 8) i18n (de + en; other languages fall back to en)
DE = {'nav_recipes': 'Rezepte', 'rec_subtitle': 'Gin & Tonic und Cocktails', 'serve_title': 'Perfect Serve (Kräuter, Garnitur, Mischung)',
      'serve_rules_btn': '🌿 Regel-Empfehlung', 'serve_ai_btn': '🤖 KI-Empfehlung', 'serve_garnish_ph': 'Kräuter und Garnitur, mit Komma getrennt',
      'serve_ratio': 'Mischung', 'serve_glass': 'Glas', 'serve_ice': 'Eis'}
EN = {'nav_recipes': 'Recipes', 'rec_subtitle': 'Gin & tonic and cocktails', 'serve_title': 'Perfect serve (herbs, garnish, ratio)',
      'serve_rules_btn': '🌿 Rule-based tip', 'serve_ai_btn': '🤖 AI recommendation', 'serve_garnish_ph': 'Herbs and garnish, comma separated',
      'serve_ratio': 'Ratio', 'serve_glass': 'Glass', 'serve_ice': 'Ice'}
out = []
for l in s.split('\n'):
    out.append(l)
    if l == 'de: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in DE.items()]
    elif l == 'en: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in EN.items()]
s = '\n'.join(out)
open(P, 'w', encoding='utf-8', newline='').write(s)

c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/g_s0.js', 'w', encoding='utf-8').write(c)
r = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/g_s0.js'], capture_output=True, text=True, encoding='utf-8')
print('syntax', r.returncode, r.stderr[:500])
