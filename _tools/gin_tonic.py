import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:80])
    s = s.replace(a, b)


# ---- type 'tonic' ----
rep("const VALID_TYPES = ['rot', 'weiß', 'rosé', 'sekt', 'other'];", "const VALID_TYPES = ['rot', 'weiß', 'rosé', 'sekt', 'tonic', 'other'];")
rep("const TYPES = ['alle','rot','weiß','rosé','sekt','other'];", "const TYPES = ['alle','rot','weiß','rosé','sekt','tonic','other'];")
rep("sekt:t('t_sekt'), other:t('t_other') };", "sekt:t('t_sekt'), tonic:t('t_tonic'), other:t('t_other') };")
rep("sekt:'var(--sparkling)', other:'var(--text-muted)' };\n", "sekt:'var(--sparkling)', tonic:'#5fb0c9', other:'var(--text-muted)' };\n".replace("tonic:'#5fb0c9'", "tonic:'#5fb0c9'"), count=s.count("sekt:'var(--sparkling)', other:'var(--text-muted)' };\n"))
rep("sekt:'var(--sparkling)', other:'var(--text-muted)' };", "sekt:'var(--sparkling)', tonic:'#5fb0c9', other:'var(--text-muted)' };", count=s.count("sekt:'var(--sparkling)', other:'var(--text-muted)' };")) if "tonic:'#5fb0c9'" not in s else None
# select options in both modals
s, n = re.subn(r'(<option value="sekt" data-i18n="(o|t)_sekt">[^<]*</option>)', lambda m: m.group(1) + f'\n        <option value="tonic" data-i18n="{m.group(2)}_tonic">🥤 Tonic Water</option>', s)
assert n == 2, n

# ---- data field: tonic (assigned tonic water name) ----
rep("    abv: (() => {", "    tonic: cleanText(w.tonic, 200),\n    abv: (() => {")
rep('''    <div class="form-group">
      <label data-i18n="l_location">Lagerplatz (Regal · Ebene · Platz von links)</label>''', '''    <div class="form-group" id="tonic-group">
      <label data-i18n="l_tonic">Passendes Tonic Water</label>
      <div class="input-with-scan">
        <input id="f-tonic" placeholder="" type="text" list="dl-tonic">
        <button type="button" class="mini-scan-btn" onclick="assignTonicForForm()" title="KI">🤖</button>
      </div>
      <datalist id="dl-tonic"></datalist>
    </div>
    <div class="form-group">
      <label data-i18n="l_location">Lagerplatz (Regal · Ebene · Platz von links)</label>''')
rep("  document.getElementById('f-abv').value = w.abv||'';\n", "  document.getElementById('f-abv').value = w.abv||'';\n  document.getElementById('f-tonic').value = w.tonic||'';\n")
rep("'f-abv','f-drink-from'", "'f-abv','f-tonic','f-drink-from'")
rep("    abv: parseFloat(String(document.getElementById('f-abv').value).replace(',', '.'))||null,\n", "    abv: parseFloat(String(document.getElementById('f-abv').value).replace(',', '.'))||null,\n    tonic: document.getElementById('f-tonic').value.trim()||null,\n")
rep("['region','country','grape','abv',", "['region','country','grape','abv','tonic',")

# ---- cards: tonic line ----
rep("function typeGrape(w) {", '''// Tonic-Zuordnung: Gin zeigt sein Tonic, ein Tonic Water zeigt die Gins, die es nutzen
function tonicLine(w) {
  if (w.type === 'tonic') {
    const nm = (w.name || '').trim().toLowerCase();
    const gins = wines.filter(x => x.type !== 'tonic' && x.tonic && x.tonic.trim().toLowerCase() === nm).map(x => x.name);
    return gins.length ? `<div class="wine-region" style="margin-top:4px">🍸 ${esc(t('tonic_pairs'))}: ${esc(gins.join(', '))}</div>` : '';
  }
  return w.tonic ? `<div class="wine-region" style="margin-top:4px">🥤 ${esc(w.tonic)}</div>` : '';
}
function typeGrape(w) {''')
rep("<div class=\"wine-year\">${w.year||''}${w.abv?' · '+w.abv+'%':''} ${w.grape?'· '+esc(w.grape):''}</div>", "<div class=\"wine-year\">${w.year||''}${w.abv?' · '+w.abv+'%':''} ${w.grape?'· '+esc(w.grape):''}</div>${tonicLine(w)}")
rep("${w.abv?' · '+w.abv+'%':''}${w.grape?' · '+esc(w.grape):''}${regionCountry", "${w.abv?' · '+w.abv+'%':''}${w.grape?' · '+esc(w.grape):''}${w.tonic&&w.type!=='tonic'?' · 🥤 '+esc(w.tonic):''}${regionCountry") if "${w.abv?' · '+w.abv+'%':''}${w.grape?' · '+esc(w.grape):''}${regionCountry" in s else None

# ---- AI assignment ----
rep("async function lookupWine() {", '''// Tonic Water per KI einem Gin zuordnen: bevorzugt aus den eigenen Tonic Waters, sonst eine Empfehlung
function tonicNames() { return wines.filter(x => x.type === 'tonic').map(x => x.name); }
async function aiPickTonic(gin) {
  const mine = tonicNames();
  const lang = { de: 'Deutsch', en: 'Englisch' }[baseLang()] || 'Englisch';
  const resp = await aiFetch(SCAN_PROXY_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 400,
      system: 'Du bist ein Gin-und-Tonic-Experte. Wähle für den genannten Gin das am besten passende Tonic Water (Geschmacksprofil, Botanicals, Stil). Gibt es eine Liste vorhandener Tonic Waters, wähle bevorzugt daraus und nenne den Namen EXAKT wie in der Liste; passt keines gut oder ist die Liste leer, empfiehl ein bekanntes Tonic Water (Marke + Sorte). Antworte NUR mit einem JSON-Objekt ohne Markdown: {"tonic": "Name", "fromList": true oder false, "reason": "kurze Begründung, höchstens 15 Wörter, auf ' + lang + '"}.',
      messages: [{ role: 'user', content: `Gin: ${gin.name}${gin.type ? ' (Stil: ' + (TYPE_LABELS[gin.type] || gin.type) + ')' : ''}${gin.grape ? ', Botanicals: ' + gin.grape : ''}${gin.region ? ', Region: ' + gin.region : ''}${gin.abv ? ', ' + gin.abv + ' % vol.' : ''}.\\nVorhandene Tonic Waters: ${mine.length ? mine.join('; ') : '(keine)'}` }]
    })
  });
  const data = await resp.json();
  if (data.type === 'error' || !data.content) return null;
  const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\\n');
  const m = text.match(/\\{[\\s\\S]*\\}/);
  if (!m) return null;
  try {
    const j = JSON.parse(m[0]);
    if (!j || !j.tonic) return null;
    let name = String(j.tonic).trim();
    const hit = mine.find(x => x.toLowerCase() === name.toLowerCase());
    if (hit) name = hit;
    return { tonic: name.slice(0, 200), fromList: !!hit, reason: String(j.reason || '').slice(0, 200) };
  } catch { return null; }
}
async function assignTonicForForm() {
  const v = id => (document.getElementById(id) ? document.getElementById(id).value.trim() : '');
  const name = v('f-name');
  if (!name) { showToast(t('toast_name')); return; }
  if (v('f-type') === 'tonic') return;
  showToast(t('tonic_busy'));
  try {
    const r = await aiPickTonic({ name, type: v('f-type'), grape: v('f-grape'), region: v('f-region'), abv: v('f-abv') });
    if (!r) { showToast(t('tonic_none_found')); return; }
    document.getElementById('f-tonic').value = r.tonic;
    showToast(r.reason ? r.tonic + ' – ' + r.reason : r.tonic);
  } catch (e) { if (!(e && (e.noCredits || e.noConsent))) showToast(t('tonic_none_found')); }
}
let tonicBulkRunning = false;
async function assignTonicsAll() {
  if (tonicBulkRunning) return;
  const targets = wines.filter(w => w.type !== 'tonic' && !w.tonic);
  if (!targets.length) { showToast(t('tonic_bulk_none')); return; }
  if (!confirm(t('tonic_bulk_confirm', { n: targets.length, m: tonicNames().length }))) return;
  tonicBulkRunning = true;
  let done = 0;
  try {
    for (const w of targets) {
      showToast(t('tonic_bulk_prog', { done: done + 1, total: targets.length }));
      const r = await aiPickTonic(w);
      if (r) { w.tonic = r.tonic; done++; save(); }
    }
  } catch (e) { /* Guthaben leer / keine Einwilligung: bisherige Zuordnungen bleiben */ }
  tonicBulkRunning = false;
  save(); rerenderActive && rerenderActive();
  showToast(t('tonic_bulk_done', { n: done }));
}

async function lookupWine() {''')
# datalist of own tonic waters in the form
rep("  document.getElementById('f-abv').value = w.abv||'';\n", "  document.getElementById('f-abv').value = w.abv||'';\n  try { document.getElementById('dl-tonic').innerHTML = tonicNames().map(n => `<option value=\"${esc(n)}\">`).join(''); } catch (e) {}\n")
# setup: bulk button
rep('''      <div class="export-card" id="drinkrule-btn"''', '''      <div class="export-card" id="tonic-bulk-btn" onclick="assignTonicsAll()" style="margin-top:10px">
        <div class="export-icon">🥤</div>
        <div class="export-info">
          <div class="title" data-i18n="tonic_bulk_title">Tonic Waters zuordnen (KI)</div>
          <div class="desc" data-i18n="tonic_bulk_desc">Passendes Tonic Water für alle Gins ohne Zuordnung finden</div>
        </div>
      </div>
      <div class="export-card" id="drinkrule-btn"''')

# ---- i18n (de + en; all other languages fall back to en via t()) ----
DE = {
 't_tonic': 'Tonic Water', 'o_tonic': '🥤 Tonic Water', 'l_tonic': 'Passendes Tonic Water',
 'tonic_pairs': 'Passt zu', 'tonic_busy': '⏳ Passendes Tonic wird gesucht…', 'tonic_none_found': 'Kein Tonic gefunden',
 'tonic_bulk_title': 'Tonic Waters zuordnen (KI)', 'tonic_bulk_desc': 'Passendes Tonic Water für alle Gins ohne Zuordnung finden',
 'tonic_bulk_confirm': 'Für {n} Gin(s) wird per KI ein passendes Tonic Water gewählt (aus deinen {m} Tonic Waters, sonst als Empfehlung). Fortfahren?',
 'tonic_bulk_prog': '⏳ Tonic zuordnen {done}/{total}…', 'tonic_bulk_done': '{n} Zuordnung(en) gespeichert ✓',
 'tonic_bulk_none': 'Alle Gins haben schon ein Tonic',
}
EN = {
 't_tonic': 'Tonic Water', 'o_tonic': '🥤 Tonic Water', 'l_tonic': 'Matching tonic water',
 'tonic_pairs': 'Pairs with', 'tonic_busy': '⏳ Finding a matching tonic…', 'tonic_none_found': 'No tonic found',
 'tonic_bulk_title': 'Assign tonic waters (AI)', 'tonic_bulk_desc': 'Find a matching tonic water for every gin without one',
 'tonic_bulk_confirm': 'AI will pick a matching tonic water for {n} gin(s) (from your {m} tonic waters, otherwise as a recommendation). Continue?',
 'tonic_bulk_prog': '⏳ Assigning tonic {done}/{total}…', 'tonic_bulk_done': '{n} pairing(s) saved ✓',
 'tonic_bulk_none': 'All gins already have a tonic',
}
out = []
for l in s.split('\n'):
    out.append(l)
    if l == 'de: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in DE.items()]
    elif l == 'en: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in EN.items()]
s = '\n'.join(out)
open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok')
