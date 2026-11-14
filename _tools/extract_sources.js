// Liest die zu uebersetzenden Texte (SX, Katalog, Rezepte, Glaeser, neue I18N-Schluessel) aus einer App und schreibt sie als flache Schluessel-Map (de/en).
// Aufruf: node extract_sources.js <index.html> <out.json>
const fs = require('fs');
const [,, file, out] = process.argv;
const s = fs.readFileSync(file, 'utf8');
function grab(startRe, endStr) {
  const m = startRe.exec(s); if (!m) return null;
  const i = m.index; const j = s.indexOf(endStr, i);
  return s.slice(i, j + endStr.length);
}
function evalConst(name, endStr) {
  const snip = grab(new RegExp('^const ' + name + ' = ', 'm'), endStr);
  if (!snip) return null;
  return new Function(snip + '; return ' + name + ';')();
}
const SX = evalConst('SX', '\n};');
const ING = evalConst('SERVE_ING', '\n};');
const TON = evalConst('SERVE_TONIC', '\n};');
const REC = evalConst('RECIPES', '\n];');
const GL = evalConst('GLASS_TXT', '\n};');
const de = {}, en = {};
if (SX) for (const k of Object.keys(SX.en)) { en['sx_' + k] = SX.en[k]; de['sx_' + k] = SX.de[k] ?? SX.en[k]; }
if (ING) for (const id of Object.keys(ING)) { de['ing_' + id] = ING[id][0]; en['ing_' + id] = ING[id][1]; }
if (TON) for (const id of Object.keys(TON)) { de['tonic_' + id + '_n'] = TON[id].n[0]; en['tonic_' + id + '_n'] = TON[id].n[1]; de['tonic_' + id + '_why'] = TON[id].why[0]; en['tonic_' + id + '_why'] = TON[id].why[1]; }
if (REC) for (const r of REC) {
  de['rec_' + r.id + '_n'] = r.n[0]; en['rec_' + r.id + '_n'] = r.n[1];
  de['rec_' + r.id + '_ing'] = r.ing.de.join('\n'); en['rec_' + r.id + '_ing'] = r.ing.en.join('\n');
  de['rec_' + r.id + '_steps'] = r.steps.de; en['rec_' + r.id + '_steps'] = r.steps.en;
  de['rec_' + r.id + '_glass'] = r.glass.de; en['rec_' + r.id + '_glass'] = r.glass.en;
}
if (GL) for (const id of Object.keys(GL)) {
  de['glass_' + id + '_title'] = GL[id].de[0]; en['glass_' + id + '_title'] = GL[id].en[0];
  de['glass_' + id + '_text'] = GL[id].de[1]; en['glass_' + id + '_text'] = GL[id].en[1];
}
// neue I18N-Schluessel: in en vorhanden, im spanischen Block (alle uebersetzten Sprachen) nicht
const i0 = s.indexOf('const I18N = {'); const blk = s.slice(i0);
function block(code) {
  const m = new RegExp('\\n' + code + ': \\{\\n').exec(blk); if (!m) return {};
  const st = m.index + m[0].length; const en_ = blk.indexOf('\n},', st); const body = blk.slice(st, en_ < 0 ? undefined : en_);
  const o = {};
  for (const l of body.split('\n')) { const mm = /^\s+([a-z_0-9]+): (".*")(,?)$/.exec(l); if (mm) { try { o[mm[1]] = JSON.parse(mm[2]); } catch (e) {} } }
  return o;
}
const bEn = block('en'), bDe = block('de'), bEs = block('es');
for (const k of Object.keys(bEn)) if (!(k in bEs)) { en[k] = bEn[k]; de[k] = bDe[k] ?? bEn[k]; }
fs.writeFileSync(out, JSON.stringify({ de, en }, null, 1), 'utf8');
console.log(file, 'keys:', Object.keys(en).length, '| sx', SX ? Object.keys(SX.en).length : 0, '| recipes', REC ? REC.length : 0, '| glasses', GL ? Object.keys(GL).length : 0, '| new i18n', Object.keys(en).filter(k => !/^(sx_|ing_|tonic_|rec_|glass_)/.test(k) || k.startsWith('rec_') && ['title','sub'].includes(k.slice(4))).length);
