/* ═══════════════════════════════════════
   PERFECT SERVE · REZEPTE · KRÄUTERREGAL
   Texte in diesem Block: Deutsch und Englisch (andere Sprachen zeigen Englisch)
═══════════════════════════════════════ */
const SX = {
  de: {
    need_name: 'Bitte erst den Namen eintragen', busy: '⏳ Empfehlung wird gesucht…', none: 'Keine Empfehlung gefunden', applied: 'Empfehlung übernommen ✓',
    in_bar: 'in deiner Bar', shop: 'Einkaufstipp', to_wish: '+ Wunschliste', fav_set: 'Als Favorit gesetzt ✓', wish_added: 'Auf die Wunschliste gesetzt ✓',
    glass_copa: 'Copa-/Ballonglas', ice_big: 'viel großes Eis', shelf_have: 'vorhanden', shelf_miss: 'fehlt',
    rec_title: 'Rezepte', rec_sub: 'Gin & Tonic und Cocktails', rec_all: 'Alle', rec_fav: '⭐ Favoriten', rec_own: 'Eigene', rec_mine: '🍸 Passt zu meiner Bar',
    rec_fits: 'Passt zu', rec_none: 'Keine Rezepte für diese Auswahl.', rec_ing: 'Zutaten', rec_steps: 'Zubereitung', rec_glass: 'Glas',
    rec_ai_title: 'Rezept für einen Gin (KI)', rec_ai_btn: '🤖 Rezept erstellen', rec_pick: 'Gin wählen…', rec_save: 'Als eigenes Rezept speichern', rec_saved: 'Rezept gespeichert ✓',
    rec_add_title: 'Eigenes Rezept anlegen', rec_name: 'Name', rec_ing_ph: 'Zutaten, eine pro Zeile', rec_steps_ph: 'Zubereitung', rec_add_btn: 'Rezept speichern',
    rec_del: 'Dieses Rezept löschen?', rec_busy: '⏳ Rezept wird erstellt…', rec_fail: 'Das hat nicht geklappt', rec_name_req: 'Bitte einen Namen eingeben',
    shelf_title: 'Mein Kräuter- und Garnitur-Regal', shelf_hint: 'Tippe an, was du zu Hause hast. Die Empfehlungen zeigen dann ✓ (vorhanden) oder 🛒 (fehlt).',
    shelf_missing: '🛒 Fehlendes auf die Wunschliste', shelf_nothing: 'Für deine Gins fehlt nichts.', shelf_done: '{n} auf die Wunschliste gesetzt ✓', shelf_wish_note: 'Kräuter/Garnitur'
  },
  en: {
    need_name: 'Please enter the name first', busy: '⏳ Looking for a recommendation…', none: 'No recommendation found', applied: 'Recommendation applied ✓',
    in_bar: 'in your bar', shop: 'Shopping tip', to_wish: '+ Wish list', fav_set: 'Set as favourite ✓', wish_added: 'Added to the wish list ✓',
    glass_copa: 'Copa / balloon glass', ice_big: 'lots of large ice', shelf_have: 'have', shelf_miss: 'missing',
    rec_title: 'Recipes', rec_sub: 'Gin & tonic and cocktails', rec_all: 'All', rec_fav: '⭐ Favourites', rec_own: 'Mine', rec_mine: '🍸 Fits my bar',
    rec_fits: 'Fits', rec_none: 'No recipes for this selection.', rec_ing: 'Ingredients', rec_steps: 'Method', rec_glass: 'Glass',
    rec_ai_title: 'Recipe for a gin (AI)', rec_ai_btn: '🤖 Create recipe', rec_pick: 'Choose a gin…', rec_save: 'Save as my recipe', rec_saved: 'Recipe saved ✓',
    rec_add_title: 'Add your own recipe', rec_name: 'Name', rec_ing_ph: 'Ingredients, one per line', rec_steps_ph: 'Method', rec_add_btn: 'Save recipe',
    rec_del: 'Delete this recipe?', rec_busy: '⏳ Creating recipe…', rec_fail: 'That did not work', rec_name_req: 'Please enter a name',
    shelf_title: 'My herb and garnish shelf', shelf_hint: 'Tap what you have at home. Recommendations then show ✓ (have) or 🛒 (missing).',
    shelf_missing: '🛒 Add missing items to the wish list', shelf_nothing: 'Nothing is missing for your gins.', shelf_done: '{n} added to the wish list ✓', shelf_wish_note: 'Herbs/garnish'
  }
};
function serveLang() { return baseLang() === 'de' ? 'de' : 'en'; }
function sx(k, vars) {
  let s = (SX[serveLang()][k] ?? SX.en[k] ?? k);
  if (vars) Object.entries(vars).forEach(([a, b]) => { s = s.split('{' + a + '}').join(b); });
  return s;
}
const sxPick = (pair) => pair[serveLang() === 'de' ? 0 : 1];

// ---- Katalog: Kräuter, Früchte, Gewürze (id: [de, en]) ----
const SERVE_ING = {
  lime: ['Limettenscheibe', 'Lime wedge'], lemon: ['Zitronenzeste', 'Lemon zest'], grapefruit: ['Grapefruitzeste', 'Grapefruit peel'], orange: ['Orangenzeste', 'Orange zest'],
  cucumber: ['Gurkenstreifen', 'Cucumber ribbon'], rosemary: ['Rosmarinzweig', 'Rosemary sprig'], thyme: ['Thymian', 'Thyme'], basil: ['Basilikum', 'Basil'],
  mint: ['Minze', 'Mint'], sage: ['Salbei', 'Sage'], lavender: ['Lavendel', 'Lavender'], rose: ['Rosenblüten', 'Rose petals'],
  pinkpepper: ['Rosa Pfeffer', 'Pink peppercorns'], cinnamon: ['Zimtstange', 'Cinnamon stick'], staranise: ['Sternanis', 'Star anise'], juniper: ['Wacholderbeeren', 'Juniper berries'],
  strawberry: ['Erdbeere', 'Strawberry'], raspberry: ['Himbeere', 'Raspberry'], ginger: ['Ingwerscheibe', 'Ginger slice'], cardamom: ['Kardamom', 'Cardamom pod']
};
// ---- Tonic-Stile ----
const SERVE_TONIC = {
  classic: { n: ['Klassisches Indian Tonic', 'Classic Indian tonic'], kw: ['indian', 'classic', 'original', 'premium'], why: ['Neutral-bitter, lässt den Wacholder führen', 'Neutral and bitter, lets the juniper lead'] },
  light: { n: ['Light Tonic (mild)', 'Light tonic (mild)'], kw: ['light', 'slim', 'zero', 'mild'], why: ['Zurückhaltend, lässt feine Botanicals zur Geltung kommen', 'Subtle, lets delicate botanicals shine'] },
  med: { n: ['Mediterranean Tonic', 'Mediterranean tonic'], kw: ['mediterr'], why: ['Kräuterig, passt zu Kräuter- und Zitrus-Gins', 'Herbal, suits herbal and citrus gins'] },
  elder: { n: ['Holunderblüten-Tonic', 'Elderflower tonic'], kw: ['elder', 'holunder'], why: ['Blumig-süßlich, unterstreicht florale Noten', 'Floral and lightly sweet, underlines floral notes'] },
  ginger: { n: ['Ingwer-/Gewürz-Tonic', 'Ginger / spiced tonic'], kw: ['ginger', 'ingwer', 'spice'], why: ['Würzig, passt zu Pfeffer, Zimt und Kardamom', 'Spicy, suits pepper, cinnamon and cardamom'] },
  pink: { n: ['Pink-Grapefruit-Tonic', 'Pink grapefruit tonic'], kw: ['pink', 'grapefruit', 'rosa'], why: ['Fruchtig, ergänzt rote Beeren und Pink Gins', 'Fruity, complements red berries and pink gins'] },
  citrus: { n: ['Zitrus-Tonic', 'Citrus tonic'], kw: ['citrus', 'zitrus', 'lemon', 'bitter lemon'], why: ['Frisch, verstärkt Zitrus-Botanicals', 'Fresh, boosts citrus botanicals'] }
};
// ---- Regeln: Stichwort in Botanicals/Name -> Tonic-Stile und Garnitur ----
const SERVE_RULES = [
  [/wacholder|juniper/i, { t: ['classic'], g: ['lime', 'rosemary'] }],
  [/zitr|citrus|lemon|orange|bergamot|limette|lime|pomelo|grapefruit/i, { t: ['citrus', 'med'], g: ['grapefruit', 'thyme'] }],
  [/gurke|cucumber/i, { t: ['light'], g: ['cucumber', 'mint'] }],
  [/\brose|rosen|hibiscus|bl[üu]te|flower|holunder|elder|lavendel|lavender|veilchen|violet/i, { t: ['elder', 'light'], g: ['rose', 'lavender'] }],
  [/pfeffer|pepper|ingwer|ginger|zimt|cinnamon|kardamom|cardamom|koriander|coriander|nelke|clove|muskat/i, { t: ['ginger', 'classic'], g: ['pinkpepper', 'cinnamon', 'orange'] }],
  [/beere|berry|schlehe|sloe|himbeere|raspberry|erdbeere|strawberry|frucht|fruit|cassis/i, { t: ['pink', 'light'], g: ['strawberry', 'basil'] }],
  [/kr[äa]uter|herb|basilikum|basil|thymian|thyme|rosmarin|rosemary|salbei|sage|minze|mint|oregano|dill|estragon/i, { t: ['med'], g: ['rosemary', 'thyme', 'basil'] }],
  [/lakritz|licorice|liquorice|anis|fenchel|fennel/i, { t: ['classic'], g: ['staranise'] }]
];
function serveByRules(g) {
  const text = [g.name, g.grape, g.region].filter(Boolean).join(' ');
  const tonics = [], garn = [];
  SERVE_RULES.forEach(([re, eff]) => {
    if (re.test(text)) {
      eff.t.forEach(x => { if (!tonics.includes(x)) tonics.push(x); });
      eff.g.forEach(x => { if (!garn.includes(x)) garn.push(x); });
    }
  });
  let ratio = '1:2';
  if (g.type === 'sekt') { ratio = serveLang() === 'de' ? '1:1,5' : '1:1.5'; if (!tonics.includes('classic')) tonics.unshift('classic'); }
  if (g.type === 'weiß') { if (!tonics.includes('light')) tonics.unshift('light'); if (!garn.includes('lemon')) garn.unshift('lemon'); }
  if (g.type === 'rosé') { if (!tonics.includes('pink')) tonics.unshift('pink'); if (!tonics.includes('light')) tonics.push('light'); }
  if (!tonics.length) tonics.push('classic');
  if (!garn.length) garn.push('lime', 'rosemary');
  if (tonics.length < 2) tonics.push(tonics.includes('classic') ? 'light' : 'classic');
  const mine = tonicNames();
  const tips = tonics.slice(0, 3).map(id => {
    const d = SERVE_TONIC[id];
    const bar = mine.find(n => d.kw.some(k => n.toLowerCase().includes(k)));
    return { n: bar || sxPick(d.n), why: sxPick(d.why), inBar: !!bar };
  });
  return { tips, garnish: garn.slice(0, 4).map(id => sxPick(SERVE_ING[id])), ratio, glass: sx('glass_copa'), ice: sx('ice_big') };
}
async function aiServe(g) {
  const mine = tonicNames();
  const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';
  const resp = await aiFetch(AI_PROXY_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6', max_tokens: 800,
      system: 'Du bist ein Gin-und-Tonic-Experte. Gib für den genannten Gin die perfekte Zubereitung. Antworte NUR mit einem JSON-Objekt ohne Markdown: {"tips":[{"name":"Tonic Water","why":"höchstens 12 Wörter"}],"garnish":["..."],"herbs":["..."],"ratio":"z. B. 1:2","glass":"...","ice":"..."}. tips: genau 3 passende Tonic Waters; gibt es eine Liste vorhandener Tonic Waters, nimm daraus passende (Namen EXAKT wie in der Liste) und ergänze nur bei Bedarf bekannte Marken. garnish: bis zu 3 Früchte/Gewürze, herbs: bis zu 3 frische Kräuter, passend zu den Botanicals. Alle Texte auf ' + lang + '.',
      messages: [{ role: 'user', content: `Gin: ${g.name}${g.type ? ' (Stil: ' + (TYPE_LABELS[g.type] || g.type) + ')' : ''}${g.grape ? ', Botanicals: ' + g.grape : ''}${g.region ? ', Region: ' + g.region : ''}${g.abv ? ', ' + g.abv + ' % vol.' : ''}.\nVorhandene Tonic Waters: ${mine.length ? mine.join('; ') : '(keine)'}` }]
    })
  });
  const data = await resp.json();
  if (data.type === 'error' || !data.content) return null;
  const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try {
    const j = JSON.parse(m[0]);
    const tips = (Array.isArray(j.tips) ? j.tips : []).slice(0, 3).map(x => {
      const nm = String((x && x.name) || '').trim();
      const bar = mine.find(q => q.toLowerCase() === nm.toLowerCase());
      return { n: (bar || nm).slice(0, 120), why: String((x && x.why) || '').slice(0, 160), inBar: !!bar };
    }).filter(x => x.n);
    const garnish = [].concat(Array.isArray(j.garnish) ? j.garnish : [], Array.isArray(j.herbs) ? j.herbs : []).map(x => String(x).trim()).filter(Boolean).slice(0, 6);
    if (!tips.length && !garnish.length) return null;
    return { tips, garnish, ratio: String(j.ratio || '').slice(0, 20), glass: String(j.glass || '').slice(0, 60), ice: String(j.ice || '').slice(0, 60) };
  } catch { return null; }
}

// ---- Formular: Perfect Serve ----
let serveTips = [], serveSrc = '';
const sv = (id) => document.getElementById(id);
function serveGinFromForm() {
  const v = id => (sv(id) ? sv(id).value.trim() : '');
  return { name: v('f-name'), type: v('f-type'), grape: v('f-grape'), region: v('f-region'), abv: v('f-abv') };
}
function cleanServe(s) {
  if (!s || typeof s !== 'object') return null;
  const tips = (Array.isArray(s.tips) ? s.tips : []).slice(0, 4).map(x => ({ n: cleanStr(x && x.n, 120).trim(), why: cleanStr(x && x.why, 160).trim(), inBar: !!(x && x.inBar) })).filter(x => x.n);
  const o = { garnish: cleanText(s.garnish, 240), ratio: cleanText(s.ratio, 20), glass: cleanText(s.glass, 60), ice: cleanText(s.ice, 60), tips, src: ['rules', 'ai', 'own'].includes(s.src) ? s.src : null };
  return (o.garnish || o.ratio || o.glass || o.ice || tips.length) ? o : null;
}
function serveReadForm() {
  const v = id => (sv(id) ? sv(id).value.trim() : '');
  const s = { garnish: v('f-serve-garnish'), ratio: v('f-serve-ratio'), glass: v('f-serve-glass'), ice: v('f-serve-ice'), tips: serveTips, src: serveSrc || 'own' };
  return cleanServe(s);
}
function serveWriteForm(s) {
  s = s || {};
  if (sv('f-serve-garnish')) sv('f-serve-garnish').value = s.garnish || '';
  if (sv('f-serve-ratio')) sv('f-serve-ratio').value = s.ratio || '';
  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';
  if (sv('f-serve-ice')) sv('f-serve-ice').value = s.ice || '';
  serveTips = Array.isArray(s.tips) ? s.tips.slice() : [];
  serveSrc = s.src || '';
  serveRenderReco();
}
function serveIngId(name) {
  const n = String(name || '').trim().toLowerCase();
  if (!n) return null;
  return Object.keys(SERVE_ING).find(id => SERVE_ING[id].some(x => x.toLowerCase() === n || n.includes(x.toLowerCase()) || x.toLowerCase().includes(n))) || null;
}
function serveRenderReco() {
  const box = sv('serve-reco');
  if (!box) return;
  const fav = (sv('f-tonic') ? sv('f-tonic').value.trim().toLowerCase() : '');
  let html = serveTips.map((x, i) => `<div class="serve-tip">
      <button type="button" class="filter-chip ${fav && x.n.toLowerCase() === fav ? 'active' : ''}" onclick="serveSetFav(${i})">🥤 ${esc(x.n)} ${x.inBar ? '✓' : '🛒'}</button>
      <span class="serve-why">${esc(x.why)}${x.inBar ? '' : ' · ' + esc(sx('shop'))}</span>
      ${x.inBar ? '' : `<button type="button" class="wine-btn" onclick="serveWishTonic(${i})">${esc(sx('to_wish'))}</button>`}
    </div>`).join('');
  const shelf = settings.herbs || [];
  const items = (sv('f-serve-garnish') ? sv('f-serve-garnish').value : '').split(',').map(x => x.trim()).filter(Boolean);
  if (shelf.length && items.length) {
    html += '<div class="serve-shelf">' + items.map(it => { const id = serveIngId(it); return id ? (shelf.includes(id) ? '✓ ' : '🛒 ') + esc(it) : esc(it); }).join(' · ') + '</div>';
  }
  box.innerHTML = html;
}
function serveApply(r, src) {
  if (sv('f-serve-garnish')) sv('f-serve-garnish').value = (r.garnish || []).join(', ');
  if (r.ratio && sv('f-serve-ratio')) sv('f-serve-ratio').value = r.ratio;
  if (r.glass && sv('f-serve-glass')) sv('f-serve-glass').value = r.glass;
  if (r.ice && sv('f-serve-ice')) sv('f-serve-ice').value = r.ice;
  serveTips = r.tips || [];
  serveSrc = src;
  serveRenderReco();
  showToast(sx('applied'));
}
async function serveFill(mode) {
  const g = serveGinFromForm();
  if (!g.name) { showToast(sx('need_name')); return; }
  if (g.type === 'tonic') return;
  if (mode === 'ai') {
    showToast(sx('busy'));
    let r = null;
    try { r = await aiServe(g); } catch (e) { if (e && (e.noCredits || e.noConsent)) return; }
    if (!r) { showToast(sx('none')); return; }
    serveApply(r, 'ai');
  } else {
    serveApply(serveByRules(g), 'rules');
  }
}
function serveSetFav(i) {
  const x = serveTips[i];
  if (!x) return;
  sv('f-tonic').value = x.n;
  serveRenderReco();
  showToast(sx('fav_set'));
}
function serveWishTonic(i) {
  const x = serveTips[i];
  if (!x) return;
  if (!wishes.some(w => (w.name || '').toLowerCase() === x.n.toLowerCase())) {
    wishes.push({ id: Date.now().toString() + i, name: x.n, year: null, type: 'tonic', region: null, country: null, grape: null, note: sx('shop'), done: false });
    saveWishes();
  }
  showToast(sx('wish_added'));
}
// Anzeige auf der Karte: Favorit-Tonic, Garnitur
function serveCardLine(w) {
  const s = w.serve;
  if (!s || !(s.garnish || s.ratio)) return '';
  return `<div class="wine-region" style="margin-top:4px">🌿 ${esc([s.garnish, s.ratio ? '(' + s.ratio + ')' : ''].filter(Boolean).join(' '))}</div>`;
}

// ---- Kräuterregal (in den Einstellungen gespeichert, wird mit dem Cloud-Stand synchronisiert) ----
function toggleHerb(id) {
  if (!SERVE_ING[id]) return;
  const a = settings.herbs || [];
  settings.herbs = a.includes(id) ? a.filter(x => x !== id) : a.concat(id);
  saveRecipesData();
  renderRecipes();
}
function shelfMissingToWish() {
  const have = new Set(settings.herbs || []);
  const need = new Set();
  wines.forEach(w => {
    if (w.type === 'tonic' || !w.serve || !w.serve.garnish) return;
    w.serve.garnish.split(',').forEach(x => { const id = serveIngId(x); if (id && !have.has(id)) need.add(id); });
  });
  if (!need.size) { showToast(sx('shelf_nothing')); return; }
  let n = 0;
  need.forEach(id => {
    const nm = sxPick(SERVE_ING[id]);
    if (!wishes.some(w => (w.name || '').toLowerCase() === nm.toLowerCase())) {
      wishes.push({ id: Date.now().toString() + id, name: nm, year: null, type: 'other', region: null, country: null, grape: null, note: sx('shelf_wish_note'), done: false });
      n++;
    }
  });
  saveWishes();
  showToast(sx('shelf_done', { n }));
}

// ---- Rezepte ----
const RECIPES = [
  { id: 'gt', n: ['Gin & Tonic', 'Gin & tonic'], styles: ['rot', 'weiß'], glass: { de: 'Ballonglas', en: 'Balloon glass' },
    ing: { de: ['5 cl Gin', '10–15 cl Tonic Water', 'Viel Eis', 'Limettenscheibe'], en: ['5 cl gin', '10–15 cl tonic water', 'Lots of ice', 'Lime wedge'] },
    steps: { de: 'Glas mit Eis füllen, Gin dazugeben, langsam mit Tonic auffüllen und einmal kurz umrühren. Mit Limette garnieren.', en: 'Fill the glass with ice, add the gin, top slowly with tonic and stir once. Garnish with lime.' } },
  { id: 'gt_med', n: ['Mediterraner G&T', 'Mediterranean G&T'], styles: ['rot'], glass: { de: 'Ballonglas', en: 'Balloon glass' },
    ing: { de: ['4 cl Gin', '12 cl Mediterranean Tonic', 'Viel Eis', 'Rosmarinzweig', 'Grapefruitzeste'], en: ['4 cl gin', '12 cl Mediterranean tonic', 'Lots of ice', 'Rosemary sprig', 'Grapefruit peel'] },
    steps: { de: 'Rosmarin kurz klatschen, Grapefruitzeste über dem Glas ausdrücken, Eis, Gin und Tonic zugeben.', en: 'Slap the rosemary, express the grapefruit peel over the glass, add ice, gin and tonic.' } },
  { id: 'gt_pink', n: ['Pink Gin & Tonic', 'Pink gin & tonic'], styles: ['rosé'], glass: { de: 'Ballonglas', en: 'Balloon glass' },
    ing: { de: ['4 cl Pink Gin', '10 cl Light Tonic', 'Eis', 'Erdbeere', 'Basilikum'], en: ['4 cl pink gin', '10 cl light tonic', 'Ice', 'Strawberry', 'Basil'] },
    steps: { de: 'Erdbeere und Basilikum ins Glas, Eis und Gin dazu, mit Tonic auffüllen.', en: 'Put strawberry and basil in the glass, add ice and gin, top with tonic.' } },
  { id: 'navy_gt', n: ['Navy-Strength G&T', 'Navy strength G&T'], styles: ['sekt'], glass: { de: 'Highball', en: 'Highball' },
    ing: { de: ['4 cl Navy Strength Gin', '8 cl Tonic Water', 'Eis', 'Limettenzeste'], en: ['4 cl navy strength gin', '8 cl tonic water', 'Ice', 'Lime zest'] },
    steps: { de: 'Weniger Tonic als üblich (etwa 1:1,5), damit der starke Gin nicht untergeht.', en: 'Use less tonic than usual (about 1:1.5) so the strong gin is not lost.' } },
  { id: 'negroni', n: ['Negroni', 'Negroni'], styles: ['rot', 'sekt'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['3 cl Gin', '3 cl Campari', '3 cl roter Wermut', 'Orangenzeste'], en: ['3 cl gin', '3 cl Campari', '3 cl red vermouth', 'Orange peel'] },
    steps: { de: 'Alle Zutaten im Mixglas mit Eis kaltrühren, auf frisches Eis abseihen, Orangenzeste ausdrücken.', en: 'Stir all ingredients with ice, strain over fresh ice, express an orange peel.' } },
  { id: 'martini', n: ['Dry Martini', 'Dry Martini'], styles: ['rot', 'sekt'], glass: { de: 'Martiniglas', en: 'Martini glass' },
    ing: { de: ['6 cl Gin', '1 cl trockener Wermut', 'Zitronenzeste oder Olive'], en: ['6 cl gin', '1 cl dry vermouth', 'Lemon twist or olive'] },
    steps: { de: 'Mit Eis lange kaltrühren, ins gekühlte Glas abseihen, Zeste darüber ausdrücken.', en: 'Stir long with ice, strain into a chilled glass, express a lemon twist over it.' } },
  { id: 'gimlet', n: ['Gimlet', 'Gimlet'], styles: ['rot'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['6 cl Gin', '2 cl Limettensaft', '1,5 cl Zuckersirup'], en: ['6 cl gin', '2 cl lime juice', '1.5 cl sugar syrup'] },
    steps: { de: 'Mit Eis kräftig shaken, in die gekühlte Coupe abseihen.', en: 'Shake hard with ice, strain into a chilled coupe.' } },
  { id: 'collins', n: ['Tom Collins', 'Tom Collins'], styles: ['weiß', 'rot'], glass: { de: 'Highball', en: 'Highball' },
    ing: { de: ['4,5 cl Gin', '3 cl Zitronensaft', '1,5 cl Zuckersirup', 'Sodawasser', 'Zitronenscheibe'], en: ['4.5 cl gin', '3 cl lemon juice', '1.5 cl sugar syrup', 'Soda water', 'Lemon slice'] },
    steps: { de: 'Gin, Saft und Sirup shaken, auf Eis abseihen, mit Soda auffüllen.', en: 'Shake gin, juice and syrup, strain over ice, top with soda.' } },
  { id: 'southside', n: ['Southside', 'Southside'], styles: ['rot'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['5 cl Gin', '2,5 cl Limettensaft', '2 cl Zuckersirup', 'Minzblätter'], en: ['5 cl gin', '2.5 cl lime juice', '2 cl sugar syrup', 'Mint leaves'] },
    steps: { de: 'Alles mit Eis shaken und doppelt abseihen.', en: 'Shake everything with ice and double strain.' } },
  { id: 'french75', n: ['French 75', 'French 75'], styles: ['rot'], glass: { de: 'Flöte', en: 'Flute' },
    ing: { de: ['3 cl Gin', '1,5 cl Zitronensaft', '1 cl Zuckersirup', '6 cl Sekt oder Champagner'], en: ['3 cl gin', '1.5 cl lemon juice', '1 cl sugar syrup', '6 cl sparkling wine'] },
    steps: { de: 'Gin, Saft und Sirup shaken, in die Flöte abseihen, mit Schaumwein auffüllen.', en: 'Shake gin, juice and syrup, strain into a flute, top with sparkling wine.' } },
  { id: 'bees', n: ["Bee's Knees", "Bee's Knees"], styles: ['weiß', 'rot'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['5 cl Gin', '2 cl Zitronensaft', '2 cl Honigsirup'], en: ['5 cl gin', '2 cl lemon juice', '2 cl honey syrup'] },
    steps: { de: 'Mit Eis shaken und in die gekühlte Coupe abseihen.', en: 'Shake with ice and strain into a chilled coupe.' } },
  { id: 'martinez', n: ['Martinez', 'Martinez'], styles: ['weiß'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['4,5 cl Old Tom Gin', '4,5 cl roter Wermut', '1 Barlöffel Maraschino', '2 Dashes Orange Bitters'], en: ['4.5 cl Old Tom gin', '4.5 cl red vermouth', '1 bar spoon maraschino', '2 dashes orange bitters'] },
    steps: { de: 'Mit Eis rühren, in die gekühlte Coupe abseihen, Orangenzeste darüber ausdrücken.', en: 'Stir with ice, strain into a chilled coupe, express an orange peel over it.' } },
  { id: 'basil_smash', n: ['Gin Basil Smash', 'Gin basil smash'], styles: ['rot', 'weiß'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['6 cl Gin', '3 cl Zitronensaft', '2 cl Zuckersirup', 'Eine Handvoll Basilikum'], en: ['6 cl gin', '3 cl lemon juice', '2 cl sugar syrup', 'A handful of basil'] },
    steps: { de: 'Basilikum im Shaker leicht andrücken, übrige Zutaten und Eis dazu, kräftig shaken, auf frisches Eis doppelt abseihen.', en: 'Lightly muddle the basil in a shaker, add the rest and ice, shake hard, double strain over fresh ice.' } }
];
function cleanRecipes(a) {
  if (!Array.isArray(a)) return [];
  return a.slice(0, 200).map(r => ({
    id: cleanStr(r && r.id, 40).trim() || ('r' + Date.now() + Math.floor(Math.random() * 1000)),
    name: cleanStr(r && r.name, 120).trim(), ing: cleanStr(r && r.ing, 2000), steps: cleanStr(r && r.steps, 4000), gin: cleanStr(r && r.gin, 120)
  })).filter(r => r.name);
}
function cleanIdList(a) { return Array.isArray(a) ? Array.from(new Set(a.map(x => cleanStr(x, 40).trim()).filter(Boolean))).slice(0, 300) : []; }
function saveRecipesData() { saveSettings(); touchData(); }
let recFilter = 'all', recMine = false, aiRecipe = null, recAiBusy = false;
function setRecFilter(f) { recFilter = f; renderRecipes(); }
function toggleRecMine() { recMine = !recMine; renderRecipes(); }
function toggleRecFav(id) {
  const a = settings.favRecipes || [];
  settings.favRecipes = a.includes(id) ? a.filter(x => x !== id) : a.concat(id);
  saveRecipesData(); renderRecipes();
}
function saveOwnRecipe() {
  const name = sv('rec-n').value.trim();
  if (!name) { showToast(sx('rec_name_req')); return; }
  settings.recipes = (settings.recipes || []).concat({ id: 'r' + Date.now(), name: name.slice(0, 120), ing: sv('rec-i').value.slice(0, 2000), steps: sv('rec-s').value.slice(0, 4000), gin: '' });
  saveRecipesData();
  showToast(sx('rec_saved'));
  renderRecipes();
}
function deleteOwnRecipe(id) {
  if (!confirm(sx('rec_del'))) return;
  settings.recipes = (settings.recipes || []).filter(r => r.id !== id);
  settings.favRecipes = (settings.favRecipes || []).filter(x => x !== id);
  saveRecipesData(); renderRecipes();
}
async function createAiRecipe() {
  if (recAiBusy) return;
  const id = sv('rec-ai-gin') ? sv('rec-ai-gin').value : '';
  const w = wines.find(x => x.id === id);
  if (!w) return;
  recAiBusy = true;
  showToast(sx('rec_busy'));
  try {
    const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';
    const resp = await aiFetch(AI_PROXY_URL, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6', max_tokens: 900,
        system: 'Du bist ein Barkeeper. Erstelle ein gutes Rezept (Cocktail oder besonderer Gin & Tonic), das den genannten Gin in Szene setzt. Antworte NUR mit einem JSON-Objekt ohne Markdown: {"name":"...","ingredients":["Menge Zutat", "..."],"steps":["..."],"glass":"..."}. Alle Texte auf ' + lang + '.',
        messages: [{ role: 'user', content: `Gin: ${w.name}${w.type ? ' (Stil: ' + (TYPE_LABELS[w.type] || w.type) + ')' : ''}${w.grape ? ', Botanicals: ' + w.grape : ''}${w.abv ? ', ' + w.abv + ' % vol.' : ''}.` }]
      })
    });
    const data = await resp.json();
    const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
    const m = text.match(/\{[\s\S]*\}/);
    const j = m ? JSON.parse(m[0]) : null;
    if (!j || !j.name || !Array.isArray(j.ingredients)) { showToast(sx('rec_fail')); }
    else { aiRecipe = { name: String(j.name).slice(0, 120), ing: j.ingredients.map(String).join('\n').slice(0, 2000), steps: (Array.isArray(j.steps) ? j.steps.map(String).join(' ') : String(j.steps || '')).slice(0, 4000), gin: w.name }; }
  } catch (e) { if (!(e && (e.noCredits || e.noConsent))) showToast(sx('rec_fail')); }
  recAiBusy = false;
  renderRecipes();
}
function saveAiRecipe() {
  if (!aiRecipe) return;
  settings.recipes = (settings.recipes || []).concat(Object.assign({ id: 'r' + Date.now() }, aiRecipe));
  aiRecipe = null;
  saveRecipesData(); showToast(sx('rec_saved')); renderRecipes();
}
function renderRecipes() {
  const el = sv('recipes-content');
  if (!el) return;
  const lang = serveLang();
  const favs = new Set(settings.favRecipes || []);
  const gins = wines.filter(w => w.type !== 'tonic');
  const types = new Set(gins.map(w => w.type));
  const all = RECIPES.map(r => ({ id: r.id, name: sxPick(r.n), ing: r.ing[lang], steps: r.steps[lang], glass: r.glass[lang], styles: r.styles, own: false }))
    .concat((settings.recipes || []).map(r => ({ id: r.id, name: r.name, ing: String(r.ing || '').split('\n').filter(Boolean), steps: r.steps, glass: '', styles: [], own: true, gin: r.gin })));
  let list = all.filter(r => recFilter === 'all' || (recFilter === 'fav' && favs.has(r.id)) || (recFilter === 'own' && r.own));
  if (recMine) list = list.filter(r => r.own || r.styles.some(s => types.has(s)));
  const chip = (id, label) => `<button class="filter-chip ${recFilter === id ? 'active' : ''}" onclick="setRecFilter('${id}')">${label}</button>`;
  const cards = list.map(r => {
    const fits = gins.filter(w => r.styles.includes(w.type)).slice(0, 5).map(w => w.name);
    return `<details class="rec-card"><summary><span class="rec-name">${esc(r.name)}</span>
        <button type="button" class="rec-fav" onclick="event.preventDefault();toggleRecFav('${esc(r.id)}')" aria-label="fav">${favs.has(r.id) ? '⭐' : '☆'}</button></summary>
      ${fits.length ? `<div class="wine-region">🍸 ${esc(sx('rec_fits'))}: ${esc(fits.join(', '))}</div>` : ''}
      ${r.gin ? `<div class="wine-region">🍸 ${esc(r.gin)}</div>` : ''}
      <div class="rec-h">${esc(sx('rec_ing'))}</div><ul>${r.ing.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
      <div class="rec-h">${esc(sx('rec_steps'))}</div><p>${esc(r.steps || '')}</p>
      ${r.glass ? `<div class="wine-region">🥃 ${esc(sx('rec_glass'))}: ${esc(r.glass)}</div>` : ''}
      ${r.own ? `<button type="button" class="wine-btn danger" onclick="deleteOwnRecipe('${esc(r.id)}')">🗑</button>` : ''}
    </details>`;
  }).join('');
  const herbs = settings.herbs || [];
  const shelf = Object.keys(SERVE_ING).map(id => `<button class="filter-chip ${herbs.includes(id) ? 'active' : ''}" onclick="toggleHerb('${id}')">${esc(sxPick(SERVE_ING[id]))}</button>`).join('');
  el.innerHTML = `
    <div class="filter-scroll">${chip('all', esc(sx('rec_all')))}${chip('fav', esc(sx('rec_fav')))}${chip('own', esc(sx('rec_own')))}
      <button class="filter-chip ${recMine ? 'active' : ''}" onclick="toggleRecMine()">${esc(sx('rec_mine'))}</button></div>
    <div class="rec-list">${cards || `<div class="empty-state">${esc(sx('rec_none'))}</div>`}</div>
    <div class="rec-box"><div class="stats-title">${esc(sx('rec_ai_title'))}</div>
      <select id="rec-ai-gin"><option value="">${esc(sx('rec_pick'))}</option>${gins.map(w => `<option value="${esc(w.id)}">${esc(w.name)}</option>`).join('')}</select>
      <button class="scan-btn" style="margin-top:8px" onclick="createAiRecipe()">${esc(sx('rec_ai_btn'))}</button>
      ${aiRecipe ? `<div class="rec-card open"><div class="rec-name">${esc(aiRecipe.name)}</div><ul>${aiRecipe.ing.split('\n').map(x => `<li>${esc(x)}</li>`).join('')}</ul><p>${esc(aiRecipe.steps)}</p>
        <button class="wine-btn primary" onclick="saveAiRecipe()">${esc(sx('rec_save'))}</button></div>` : ''}</div>
    <div class="rec-box"><div class="stats-title">${esc(sx('rec_add_title'))}</div>
      <input id="rec-n" placeholder="${esc(sx('rec_name'))}">
      <textarea id="rec-i" rows="4" placeholder="${esc(sx('rec_ing_ph'))}"></textarea>
      <textarea id="rec-s" rows="3" placeholder="${esc(sx('rec_steps_ph'))}"></textarea>
      <button class="scan-btn" onclick="saveOwnRecipe()">${esc(sx('rec_add_btn'))}</button></div>
    <div class="rec-box"><div class="stats-title">${esc(sx('shelf_title'))}</div>
      <div class="legend-text">${esc(sx('shelf_hint'))}</div>
      <div class="shelf-chips">${shelf}</div>
      <button class="scan-btn" style="margin-top:8px" onclick="shelfMissingToWish()">${esc(sx('shelf_missing'))}</button></div>`;
}
