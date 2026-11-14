import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:110])
    s = s.replace(a, b)


def rerep(pattern, repl, count=1, flags=re.S):
    global s
    s, n = re.subn(pattern, lambda m: repl, s, flags=flags)
    assert n == count, (n, count, pattern[:110])


# 1) SX-Objekt, sx(), sxPick raus; sx() liest jetzt aus I18N
rerep(r"const SX = \{\n.*?\n\};\nfunction serveLang\(\) \{[^\n]*\}\nfunction sx\(k, vars\) \{\n.*?\n\}\nconst sxPick = [^\n]*\n",
      "// Alle Sprachtexte der Perfect-Serve-/Rezept-/Glas-Funktionen stehen in I18N (Schlüssel sx_*, ing_*, tonic_*, rec_*, glass_*).\n"
      "function sx(k, vars) { return t('sx_' + k, vars); }\n"
      "// Nur noch für das Suchwort 'Glas Gin' und den Dezimaltrenner; alle Sprachtexte kommen aus t().\n"
      "function serveLang() { return baseLang() === 'de' ? 'de' : 'en'; }\n"
      "// Sprachname (deutsch) für die KI-Anfragen: 'Antworte auf …'\n"
      "function aiLangName() {\n"
      "  return ({ de: 'Deutsch', en: 'Englisch', es: 'Spanisch', sv: 'Schwedisch', da: 'Dänisch', fi: 'Finnisch', ru: 'Russisch', it: 'Italienisch', fr: 'Französisch',\n"
      "    pl: 'Polnisch', hu: 'Ungarisch', cs: 'Tschechisch', sk: 'Slowakisch', ro: 'Rumänisch', hr: 'Kroatisch', pt: 'Portugiesisch', no: 'Norwegisch',\n"
      "    nl: 'Niederländisch', el: 'Griechisch', uk: 'Ukrainisch', ja: 'Japanisch', ko: 'Koreanisch', zh: 'Chinesisch', hi: 'Hindi' })[baseLang()] || 'Englisch';\n"
      "}\n")

# 2) Katalog nur noch als Id-Menge; Namen aus I18N
rerep(r"// ---- Katalog: Kräuter, Früchte, Gewürze \(id: \[de, en\]\) ----\nconst SERVE_ING = \{\n.*?\n\};\n",
      "// ---- Katalog: Kräuter, Früchte, Gewürze (Namen: I18N ing_<id>) ----\n"
      "const SERVE_ING = { lime: 1, lemon: 1, grapefruit: 1, orange: 1, cucumber: 1, rosemary: 1, thyme: 1, basil: 1, mint: 1, sage: 1, lavender: 1, rose: 1,\n"
      "  pinkpepper: 1, cinnamon: 1, staranise: 1, juniper: 1, strawberry: 1, raspberry: 1, ginger: 1, cardamom: 1 };\n"
      "function ingName(id) { return t('ing_' + id); }\n")
rerep(r"// ---- Tonic-Stile ----\nconst SERVE_TONIC = \{\n.*?\n\};\n",
      "// ---- Tonic-Stile: Schlüsselwörter zum Erkennen eigener Tonics (Name/Begründung: I18N tonic_<id>_n / tonic_<id>_why) ----\n"
      "const SERVE_TONIC = {\n"
      "  classic: { kw: ['indian', 'classic', 'original', 'premium'] },\n"
      "  light: { kw: ['light', 'slim', 'zero', 'mild'] },\n"
      "  med: { kw: ['mediterr'] },\n"
      "  elder: { kw: ['elder', 'holunder'] },\n"
      "  ginger: { kw: ['ginger', 'ingwer', 'spice'] },\n"
      "  pink: { kw: ['pink', 'grapefruit', 'rosa'] },\n"
      "  citrus: { kw: ['citrus', 'zitrus', 'lemon', 'bitter lemon'] }\n"
      "};\n")
rep("    return { n: bar || sxPick(d.n), why: sxPick(d.why), inBar: !!bar };", "    return { n: bar || t('tonic_' + id + '_n'), why: t('tonic_' + id + '_why'), inBar: !!bar };")
rep("garnish: garn.slice(0, 4).map(id => sxPick(SERVE_ING[id])),", "garnish: garn.slice(0, 4).map(ingName),")

# 3) KI: Antwortsprache fuer alle 24 Sprachen
rep("  const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';\n  const resp = await aiFetch(AI_PROXY_URL, {", "  const lang = aiLangName();\n  const resp = await aiFetch(AI_PROXY_URL, {")
rep("    const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';\n    const resp = await aiFetch(AI_PROXY_URL, {", "    const lang = aiLangName();\n    const resp = await aiFetch(AI_PROXY_URL, {")
rep("  const lang = { de: 'Deutsch', en: 'Englisch' }[baseLang()] || 'Englisch';", "  const lang = aiLangName();")

# 4) Namen -> Id ueber alle Sprachen
rerep(r"function serveIngId\(name\) \{\n.*?\n\}\n",
      "// Zutatennamen aller Sprachen (kleingeschrieben), damit ein Eintrag auch nach einem Sprachwechsel erkannt wird\n"
      "let _ingNames = null;\n"
      "function ingNameMap() {\n"
      "  if (_ingNames) return _ingNames;\n"
      "  const m = {};\n"
      "  Object.keys(SERVE_ING).forEach(id => { m[id] = []; Object.keys(I18N).forEach(l => { const v = I18N[l] && I18N[l]['ing_' + id]; if (v) m[id].push(String(v).toLowerCase()); }); });\n"
      "  return (_ingNames = m);\n"
      "}\n"
      "function serveIngId(name) {\n"
      "  const n = String(name || '').trim().toLowerCase();\n"
      "  if (n.length < 2) return null;\n"
      "  const map = ingNameMap();\n"
      "  return Object.keys(SERVE_ING).find(id => map[id].some(x => x === n || n.includes(x) || x.includes(n))) || null;\n"
      "}\n")

# 5) Glaeser
rerep(r"function glassId\(name\) \{\n.*?\n\}\n",
      "// Welches Glas ist gemeint? Erst nach Stichwörtern (de/en), dann nach den Glasnamen aller Sprachen (glass_<id>_title, Teile vor/nach '/')\n"
      "let _glassNames = null;\n"
      "function glassNameMap() {\n"
      "  if (_glassNames) return _glassNames;\n"
      "  const m = {};\n"
      "  ['copa', 'highball', 'tumbler', 'coupe', 'martini', 'flute'].forEach(id => {\n"
      "    m[id] = [];\n"
      "    Object.keys(I18N).forEach(l => { const v = I18N[l] && I18N[l]['glass_' + id + '_title']; if (v) String(v).toLowerCase().split(/[\\/(),·]+/).map(x => x.trim()).filter(x => x.length >= 2).forEach(x => m[id].push(x)); });\n"
      "  });\n"
      "  return (_glassNames = m);\n"
      "}\n"
      "function glassId(name) {\n"
      "  const n = String(name || '').toLowerCase();\n"
      "  if (/copa|ballon|balloon|gin.?glas|gin glass/.test(n)) return 'copa';\n"
      "  if (/flöte|floete|flute|sekt|champagner/.test(n)) return 'flute';\n"
      "  if (/martini|nick/.test(n)) return 'martini';\n"
      "  if (/coupe|schale/.test(n)) return 'coupe';\n"
      "  if (/highball|longdrink|collins/.test(n)) return 'highball';\n"
      "  if (/tumbler|rocks|old.?fashioned|becher/.test(n)) return 'tumbler';\n"
      "  const map = glassNameMap();\n"
      "  return Object.keys(map).find(id => map[id].some(x => n.includes(x) || (n.length >= 3 && x.includes(n)))) || null;\n"
      "}\n")
rep("function glassViewText() { return serveLang() === 'de' ? 'Glas ansehen' : 'See the glass'; }\n", '')
rep("${esc(glassViewText())}", "${esc(t('glass_view'))}")
rep("'🔍 ' + glassViewText() + ': '", "'🔍 ' + t('glass_view') + ': '")
rerep(r"const GLASS_TXT = \{\n.*?\n\};\n(?=function showGlass)", '')
rep("  const lang = serveLang() === 'de' ? 'de' : 'en';\n  const [title, text] = GLASS_TXT[id][lang];\n  const more = lang === 'de' ? 'Mehr Bilder ansehen ↗' : 'See more pictures ↗';\n  const close = lang === 'de' ? 'Schließen' : 'Close';\n",
    "  const title = t('glass_' + id + '_title'), text = t('glass_' + id + '_text');\n  const more = t('glass_more'), close = t('glass_close');\n")

# 6) Kraeuterregal / Rezepte
rep("    const nm = sxPick(SERVE_ING[id]);", "    const nm = ingName(id);")
rerep(r"const RECIPES = \[\n.*?\n\];\n",
      "// Rezepte: nur Id und passende Gin-Stile; Name/Zutaten/Zubereitung/Glas stehen in I18N (rec_<id>_n / _ing / _steps / _glass)\n"
      "const RECIPES = [\n"
      "  { id: 'gt', styles: ['rot', 'weiß'] }, { id: 'gt_med', styles: ['rot'] }, { id: 'gt_pink', styles: ['rosé'] }, { id: 'navy_gt', styles: ['sekt'] },\n"
      "  { id: 'negroni', styles: ['rot', 'sekt'] }, { id: 'martini', styles: ['rot', 'sekt'] }, { id: 'gimlet', styles: ['rot'] },\n"
      "  { id: 'collins', styles: ['weiß', 'rot'] }, { id: 'southside', styles: ['rot'] }, { id: 'french75', styles: ['rot'] },\n"
      "  { id: 'bees', styles: ['weiß', 'rot'] }, { id: 'martinez', styles: ['weiß'] }, { id: 'basil_smash', styles: ['rot', 'weiß'] }\n"
      "];\n")
rep("  const lang = serveLang();\n  const favs = new Set(settings.favRecipes || []);", "  const favs = new Set(settings.favRecipes || []);")
rep("const all = RECIPES.map(r => ({ id: r.id, name: sxPick(r.n), ing: r.ing[lang], steps: r.steps[lang], glass: r.glass[lang], styles: r.styles, own: false }))",
    "const all = RECIPES.map(r => ({ id: r.id, name: t('rec_' + r.id + '_n'), ing: t('rec_' + r.id + '_ing').split('\\n').filter(Boolean), steps: t('rec_' + r.id + '_steps'), glass: t('rec_' + r.id + '_glass'), styles: r.styles, own: false }))")
rep("${esc(sxPick(SERVE_ING[id]))}</button>`).join('');", "${esc(ingName(id))}</button>`).join('');")

# 7) Fehlstelle im US-Block: barcode_miss_text stand dort auf Hindi (alter Merge-Fehler); t() faellt jetzt auf Englisch zurueck
rerep(r"(I18N\.us = \{\n)  barcode_miss_text: \"[^\n]*\n", r"\1".replace('\\1', '') if False else "I18N.us = {\n", 1, flags=0) if False else None
m = re.search(r"I18N\.us = \{\n  barcode_miss_text: \"[^\n]*\n", s)
assert m, 'US-Block'
s = s.replace(m.group(0), "I18N.us = {\n")

open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
r = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True)
print('syntax', r.returncode, r.stderr[:400])
print('Verweise auf entfernte Namen:', {n: len(re.findall(r'(?<![A-Za-z0-9_$])' + n + r'(?![A-Za-z0-9_$])', s)) for n in ['SX', 'sxPick', 'GLASS_TXT', 'glassViewText']})
