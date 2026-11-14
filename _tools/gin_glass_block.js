// ---- Glas-Info: eigene Zeichnungen (lizenzfrei, offline) + kurze Erklaerung ----
// Alles bis showGlass() sind Funktionen ohne Verweis auf spaeter definierte Konstanten (werden schon beim ersten Rendern genutzt)
function glassId(name) {
  const n = String(name || '').toLowerCase();
  if (/copa|ballon|balloon|gin.?glas|gin glass/.test(n)) return 'copa';
  if (/flöte|floete|flute|sekt|champagner/.test(n)) return 'flute';
  if (/martini|nick/.test(n)) return 'martini';
  if (/coupe|schale/.test(n)) return 'coupe';
  if (/highball|longdrink|collins/.test(n)) return 'highball';
  if (/tumbler|rocks|old.?fashioned|becher/.test(n)) return 'tumbler';
  return null;
}
function glassViewText() { return serveLang() === 'de' ? 'Glas ansehen' : 'See the glass'; }
function glassUrl(name) {
  const q = String(name || '').trim() + (serveLang() === 'de' ? ' Glas Gin' : ' glass gin');
  return 'https://www.google.com/search?tbm=isch&q=' + encodeURIComponent(q);
}
function glassLinkHtml(name) {
  return `<a class="glass-link" href="${glassUrl(name)}" target="_blank" rel="noopener" data-glass="${esc(name)}" onclick="return glassClick(this,event)">${esc(name)} · ${esc(glassViewText())} ↗</a>`;
}
function glassClick(a, ev) {
  ev.stopPropagation();
  const name = a.getAttribute('data-glass') || '';
  if (glassId(name)) { ev.preventDefault(); showGlass(name); return false; }
  return true;   // unbekanntes Glas: normale Bildersuche
}
function serveGlassLink() {
  const a = sv('serve-glass-link'), v = sv('f-serve-glass') ? sv('f-serve-glass').value.trim() : '';
  if (!a) return;
  if (!v) { a.style.display = 'none'; return; }
  a.href = glassUrl(v); a.setAttribute('data-glass', v); a.textContent = '🔍 ' + glassViewText() + ': ' + v + ' ↗'; a.style.display = 'inline-block';
}
const GLASS_DRAW = {
  copa: '<path d="M24 18C12 32 14 62 50 62s38-30 26-44z" fill="url(#gg)"/><path d="M17.6 42C20 56 32 62 50 62s30-6 32.4-20z" fill="url(#gl)"/><rect x="31" y="22" width="17" height="19" rx="3.4" fill="#fff" fill-opacity=".6" transform="rotate(-10 40 31)"/><rect x="50" y="27" width="16" height="17" rx="3.4" fill="#fff" fill-opacity=".5" transform="rotate(11 58 36)"/><path d="M62 10L74 40" stroke="#5a8f4a" stroke-width="1.6" stroke-linecap="round"/><g stroke="#6fb066" stroke-width="1.4" stroke-linecap="round"><path d="M64 15l-5-1M66 20l-6-1M68 25l-6 0M70 30l-5 1M63 12l4-3M65 17l5-2M67 22l5-2M69 27l5-2"/></g><rect x="47.4" y="62" width="5.2" height="22" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="86" rx="19" ry="3.6" fill="url(#gg)"/><path d="M22 28c-3 10 0 20 8 27" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
  highball: '<path d="M35 8h30l-2.4 80q-.2 5-5 5H42.4q-4.8 0-5-5z" fill="url(#gg)"/><path d="M36.4 30h27.2l-1.6 58q-.2 4-4.6 4H42.6q-4.4 0-4.6-4z" fill="url(#gl)"/><rect x="40" y="18" width="14" height="16" rx="3" fill="#fff" fill-opacity=".6" transform="rotate(-8 47 26)"/><rect x="48" y="36" width="13" height="15" rx="3" fill="#fff" fill-opacity=".5" transform="rotate(9 54 43)"/><circle cx="46" cy="64" r="1.6" fill="#fff" fill-opacity=".8"/><circle cx="54" cy="72" r="1.2" fill="#fff" fill-opacity=".8"/><circle cx="49" cy="80" r="1.5" fill="#fff" fill-opacity=".8"/><path d="M60 8q12 0 11 14-5-2-11-2z" fill="#8cc66a"/><path d="M40 14l1.8 70" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="94" rx="17" ry="2.2" fill="#000" opacity=".25"/>',
  tumbler: '<path d="M25 26h50l-4 58q-.4 5-5 5H34q-4.6 0-5-5z" fill="url(#gg)"/><path d="M27.4 50h45.2l-1.6 34q-.4 4-5 4H34q-4.6 0-5-4z" fill="url(#gl)"/><rect x="32" y="32" width="20" height="22" rx="4" fill="#fff" fill-opacity=".6" transform="rotate(-9 42 43)"/><rect x="50" y="38" width="18" height="19" rx="4" fill="#fff" fill-opacity=".5" transform="rotate(10 59 47)"/><path d="M30 34l2.6 44" stroke="#fff" stroke-opacity=".7" stroke-width="2.4" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="91" rx="24" ry="2.6" fill="#000" opacity=".25"/>',
  coupe: '<path d="M18 28q0 28 32 28t32-28z" fill="url(#gg)"/><path d="M22 36q2 18 28 18t28-18z" fill="url(#gl)"/><rect x="47.6" y="55" width="4.8" height="28" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="86" rx="16" ry="3.6" fill="url(#gg)"/><path d="M24 32c1 8 5 14 11 17" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/><path d="M64 24q10-8 14 2-7-3-10 5z" fill="#f2d26b"/>',
  martini: '<path d="M14 22h72L50 60z" fill="url(#gg)"/><path d="M22 28h56L50 54z" fill="url(#gl)"/><rect x="47.6" y="58" width="4.8" height="26" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="87" rx="17" ry="3.4" fill="url(#gg)"/><path d="M40 20l8 24" stroke="#c9a24b" stroke-width="1.6" stroke-linecap="round"/><circle cx="46" cy="36" r="4.6" fill="#8aa84a"/><circle cx="46" cy="36" r="1.6" fill="#c24a3a"/><path d="M20 24l28 30" stroke="#fff" stroke-opacity=".6" stroke-width="2" fill="none" stroke-linecap="round"/>',
  flute: '<path d="M39 8h22l-2 50q-.3 7-9 7t-9-7z" fill="url(#gg)"/><path d="M40.4 24h19.2l-1.2 34q-.3 6.4-8.4 6.4t-8.4-6.4z" fill="url(#gl)"/><circle cx="48" cy="34" r="1.4" fill="#fff" fill-opacity=".85"/><circle cx="53" cy="42" r="1.2" fill="#fff" fill-opacity=".85"/><circle cx="49" cy="50" r="1.4" fill="#fff" fill-opacity=".85"/><circle cx="52" cy="28" r="1" fill="#fff" fill-opacity=".85"/><rect x="47.4" y="64" width="5.2" height="20" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="86" rx="14" ry="3.2" fill="url(#gg)"/><path d="M42 14l1.2 40" stroke="#fff" stroke-opacity=".7" stroke-width="2" fill="none" stroke-linecap="round"/>'
};
const GLASS_TXT = {
  copa: {
    de: ['Copa-/Ballonglas', 'Das klassische Gin-Tonic-Glas aus Spanien: ein weiter Kelch mit langem Stiel. Er bietet Platz für große Eiswürfel und Garnitur, und die Öffnung lässt die Botanicals duften. Am Stiel halten, damit der Gin kühl bleibt.'],
    en: ['Copa / balloon glass', 'The classic gin and tonic glass from Spain: a wide bowl on a long stem. It leaves room for large ice cubes and garnish, and the wide opening releases the botanicals\' aroma. Hold it by the stem to keep the gin cold.']
  },
  highball: {
    de: ['Highball-Glas', 'Hoch und schmal. Es hält Eis und Kohlensäure lange kühl und spritzig, passend für Gin & Tonic mit viel Tonic, Tom Collins und andere Longdrinks.'],
    en: ['Highball glass', 'Tall and narrow. It keeps ice and fizz cold and lively for a long time, suited to gin and tonic with plenty of tonic, the Tom Collins and other long drinks.']
  },
  tumbler: {
    de: ['Tumbler (Rocks-Glas)', 'Ein kurzes, breites Glas mit schwerem Boden. Passend für Gin pur auf Eis und für Negroni, Gimlet oder Basil Smash.'],
    en: ['Tumbler (rocks glass)', 'A short, wide glass with a heavy base. Suited to gin on the rocks and to the Negroni, Gimlet or Basil Smash.']
  },
  coupe: {
    de: ['Coupe', 'Eine flache Schale auf Stiel für Cocktails ohne Eis, etwa Gimlet, Southside oder Bee\'s Knees. Am Stiel gehalten, wärmt die Hand das Getränk nicht.'],
    en: ['Coupe', 'A shallow bowl on a stem for cocktails served without ice, such as the Gimlet, Southside or Bee\'s Knees. Held by the stem, your hand does not warm the drink.']
  },
  martini: {
    de: ['Martiniglas', 'Das V-förmige Glas für Dry Martini und andere gerührte Gin-Cocktails ohne Eis. Der lange Stiel hält das Getränk kalt, die Olive oder Zitronenzeste gehört an den Rand.'],
    en: ['Martini glass', 'The V-shaped glass for the dry martini and other stirred gin cocktails without ice. The long stem keeps the drink cold, and the olive or lemon twist goes on the rim.']
  },
  flute: {
    de: ['Sektflöte', 'Ein hohes, schmales Glas für Schaumwein. Beim French 75 kommen Gin, Zitrone und Zuckersirup mit Sekt oder Champagner hinein.'],
    en: ['Champagne flute', 'A tall, narrow glass for sparkling wine. The French 75 combines gin, lemon and sugar syrup topped with sparkling wine or champagne.']
  }
};
function showGlass(name) {
  const id = glassId(name);
  if (!id) return;
  const lang = serveLang() === 'de' ? 'de' : 'en';
  const [title, text] = GLASS_TXT[id][lang];
  const more = lang === 'de' ? 'Mehr Bilder ansehen ↗' : 'See more pictures ↗';
  const close = lang === 'de' ? 'Schließen' : 'Close';
  const old = document.getElementById('glass-overlay'); if (old) old.remove();
  const o = document.createElement('div');
  o.id = 'glass-overlay'; o.className = 'glass-overlay';
  o.innerHTML = `<div class="glass-card" role="dialog" aria-label="${esc(title)}">
    <svg viewBox="0 0 100 100" width="150" height="150" aria-hidden="true"><defs>
      <linearGradient id="gg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bcd4e0"/><stop offset=".3" stop-color="#f4fafc"/><stop offset=".7" stop-color="#d3e5ee"/><stop offset="1" stop-color="#9fbacb"/></linearGradient>
      <linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9e8f2" stop-opacity=".85"/><stop offset="1" stop-color="#86bdd2" stop-opacity=".95"/></linearGradient>
    </defs>${GLASS_DRAW[id]}</svg>
    <div class="glass-title">${esc(title)}</div>
    <p>${esc(text)}</p>
    <a class="glass-link" href="${glassUrl(name)}" target="_blank" rel="noopener">${more}</a>
    <button type="button" class="wine-btn primary" id="glass-close">${close}</button>
  </div>`;
  o.addEventListener('click', e => { if (e.target === o) o.remove(); });
  document.body.appendChild(o);
  document.getElementById('glass-close').onclick = () => o.remove();
}
