// Gin-Factory Worker (Cloudflare Workers)
// Endpunkte (alle POST, JSON):
//   /            KI-Proxy zu Anthropic (Etikett-Scan, Nachschlagen, Preise, Tonic-Zuordnung); der API-Key bleibt im Worker
//   /sync        Cloud-Sync (KV): { op: 'pull' | 'push', code, data?, updatedAt? }
//   /barcode     Flaschen-Barcode -> Produktdaten (Open Food Facts): { ean } -> { found, name, brand, ... }
//   /ogimage     og:image einer Webseite: { url } -> { image }
//   /wineimg     (Wein-Bildsuche, für Gin abgeschaltet) -> { image: null }
//   /acct/status Konto-Status (hier: kein Guthaben-System) -> { gated: false }
//   alles andere (/credits/*, /acct/unlock, /admin/*: nur Store-Version) -> 404

const DEFAULT_ORIGINS = ['https://ocho1511.github.io', 'capacitor://localhost', 'ionic://localhost', 'http://localhost', 'https://localhost'];
const MAX_BODY = 12 * 1024 * 1024;        // Fotos für den Etikett-Scan sind groß (Base64)
const MAX_SYNC_BYTES = 4 * 1024 * 1024;   // KV erlaubt 25 MB, 4 MB reichen für eine Sammlung
const AI_PER_DAY = 400;                   // KI-Aufrufe pro Gerät/IP und Tag (Schutz vor Missbrauch)
const SYNC_CODE_RE = /^[a-z0-9]{16,40}$/i;

function allowedOrigins(env) {
  return env.ALLOWED_ORIGINS ? String(env.ALLOWED_ORIGINS).split(',').map((s) => s.trim()).filter(Boolean) : DEFAULT_ORIGINS;
}
function corsFor(request, env) {
  const origin = request.headers.get('Origin') || '';
  const ok = allowedOrigins(env).includes(origin) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
  return {
    'Access-Control-Allow-Origin': ok ? origin : allowedOrigins(env)[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Install-Id',
    'Access-Control-Expose-Headers': 'X-Credits-Left',
    'Vary': 'Origin',
  };
}
function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { 'Content-Type': 'application/json', ...cors } });
}

// ---- Tageslimit pro Gerät (X-Install-Id) bzw. IP, im KV ----
async function rateLimit(request, env) {
  if (!env.SYNC) return true;
  const id = (request.headers.get('X-Install-Id') || request.headers.get('CF-Connecting-IP') || 'anon').slice(0, 64);
  const key = 'rl:' + new Date().toISOString().slice(0, 10) + ':' + id;
  const n = parseInt((await env.SYNC.get(key)) || '0', 10) || 0;
  if (n >= AI_PER_DAY) return false;
  await env.SYNC.put(key, String(n + 1), { expirationTtl: 60 * 60 * 26 });
  return true;
}

// ---- KI-Proxy ----
async function handleAi(body, request, env, cors) {
  if (!env.ANTHROPIC_API_KEY) return json({ type: 'error', error: { message: 'ANTHROPIC_API_KEY fehlt im Worker' } }, 500, cors);
  if (!body || typeof body !== 'object' || !Array.isArray(body.messages)) return json({ type: 'error', error: { message: 'Ungültige Anfrage' } }, 400, cors);
  if (!/^claude-/.test(String(body.model || ''))) return json({ type: 'error', error: { message: 'Modell nicht erlaubt' } }, 400, cors);
  // nur die Websuche als Werkzeug zulassen, Antwortlänge begrenzen
  const safe = {
    model: body.model,
    max_tokens: Math.min(Math.max(parseInt(body.max_tokens) || 1024, 1), 4096),
    messages: body.messages,
  };
  if (body.system) safe.system = body.system;
  if (Array.isArray(body.tools)) {
    safe.tools = body.tools.filter((t) => t && t.type === 'web_search_20250305').map((t) => ({ type: t.type, name: 'web_search', max_uses: Math.min(parseInt(t.max_uses) || 3, 5) }));
    if (!safe.tools.length) delete safe.tools;
  }
  if (!(await rateLimit(request, env))) return json({ type: 'error', error: { message: 'Tageslimit erreicht' } }, 429, cors);
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify(safe),
  });
  return new Response(await r.text(), { status: r.status, headers: { 'Content-Type': 'application/json', ...cors } });
}

// ---- Cloud-Sync ----
async function handleSync(body, env, cors) {
  if (!env.SYNC) return json({ error: 'KV nicht eingerichtet' }, 500, cors);
  const code = String((body && body.code) || '').toLowerCase();
  if (!SYNC_CODE_RE.test(code)) return json({ error: 'bad_code' }, 400, cors);
  const key = 'sync:' + code;
  const cur = await env.SYNC.get(key, 'json');
  if (body.op === 'pull') {
    return json(cur ? { exists: true, updatedAt: cur.updatedAt || 0, data: cur.data } : { exists: false }, 200, cors);
  }
  if (body.op === 'push') {
    const at = Number(body.updatedAt) || 0;
    if (!body.data || typeof body.data !== 'object') return json({ error: 'no_data' }, 400, cors);
    const text = JSON.stringify({ data: body.data, updatedAt: at });
    if (text.length > MAX_SYNC_BYTES) return json({ error: 'too_big' }, 413, cors);
    // ein anderes Gerät war schneller (neuerer Stand in der Cloud): nichts überschreiben, Cloud-Stand zurückgeben
    if (cur && (cur.updatedAt || 0) > at) return json({ stored: false, newer: true, updatedAt: cur.updatedAt, data: cur.data }, 200, cors);
    await env.SYNC.put(key, text);
    return json({ stored: true, updatedAt: at }, 200, cors);
  }
  return json({ error: 'bad_op' }, 400, cors);
}

// ---- Barcode (Open Food Facts) ----
async function handleBarcode(body, cors) {
  const ean = String((body && body.ean) || '').replace(/\D/g, '');
  if (!/^\d{8,14}$/.test(ean)) return json({ found: false, error: 'bad_ean' }, 400, cors);
  try {
    const r = await fetch(`https://world.openfoodfacts.org/api/v2/product/${ean}.json?fields=product_name,brands,quantity,categories_tags,abv,alcohol_by_volume`, {
      headers: { 'User-Agent': 'Gin-Factory/1.0 (barcode lookup)' },
    });
    if (!r.ok) return json({ found: false }, 200, cors);
    const j = await r.json();
    if (!j || j.status !== 1 || !j.product) return json({ found: false }, 200, cors);
    const p = j.product;
    const name = String(p.product_name || '').trim();
    const brand = String(p.brands || '').split(',')[0].trim();
    if (!name && !brand) return json({ found: false }, 200, cors);
    const cats = (p.categories_tags || []).join(' ').toLowerCase();
    // Stil grob aus Name/Kategorien (rot = London Dry, weiß = Old Tom/Plymouth, rosé = Pink/Frucht, sekt = Navy Strength)
    let type = null;
    const nm = (name + ' ' + cats).toLowerCase();
    if (/navy/.test(nm)) type = 'sekt';
    else if (/old tom|plymouth|genever/.test(nm)) type = 'weiß';
    else if (/pink|rose|fruit|flavou?red|sloe/.test(nm)) type = 'rosé';
    else if (/london dry|gin/.test(nm)) type = 'rot';
    const abv = parseFloat(p.abv || p.alcohol_by_volume) || null;
    return json({ found: true, name, brand, type, abv }, 200, cors);
  } catch (e) {
    return json({ found: false }, 200, cors);
  }
}

// ---- og:image einer Seite ----
function publicHttpUrl(u) {
  let x;
  try { x = new URL(u); } catch { return null; }
  if (x.protocol !== 'http:' && x.protocol !== 'https:') return null;
  const h = x.hostname.toLowerCase();
  if (h === 'localhost' || h.endsWith('.local') || h.endsWith('.internal') || /^\d{1,3}(\.\d{1,3}){3}$/.test(h) || h.includes(':') || !h.includes('.')) return null;   // keine internen Ziele
  return x;
}
async function handleOgImage(body, cors) {
  const u = publicHttpUrl(body && body.url);
  if (!u) return json({ image: null }, 200, cors);
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 6000);
  try {
    const r = await fetch(u.toString(), { signal: ctl.signal, redirect: 'follow', headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Gin-Factory/1.0)', 'Accept': 'text/html' } });
    if (!r.ok || !/html/i.test(r.headers.get('Content-Type') || '')) return json({ image: null }, 200, cors);
    const html = (await r.text()).slice(0, 400000);
    const m = html.match(/<meta[^>]+(?:property|name)=["'](?:og:image(?::secure_url)?|twitter:image)["'][^>]*content=["']([^"']+)["']/i)
      || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]*(?:property|name)=["'](?:og:image|twitter:image)["']/i);
    if (!m) return json({ image: null }, 200, cors);
    let img = m[1].replace(/&amp;/g, '&').trim();
    try { img = new URL(img, u).toString(); } catch { return json({ image: null }, 200, cors); }
    return json({ image: /^https?:\/\//i.test(img) ? img : null }, 200, cors);
  } catch (e) {
    return json({ image: null }, 200, cors);
  } finally { clearTimeout(timer); }
}

export default {
  async fetch(request, env) {
    const cors = corsFor(request, env);
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405, cors);
    const len = parseInt(request.headers.get('Content-Length') || '0', 10);
    if (len > MAX_BODY) return json({ error: 'Anfrage zu groß' }, 413, cors);
    let body;
    try { body = await request.json(); } catch { return json({ error: 'Ungültiger Request-Body' }, 400, cors); }
    const path = new URL(request.url).pathname.replace(/\/+$/, '') || '/';
    switch (path) {
      case '/': return handleAi(body, request, env, cors);
      case '/sync': return handleSync(body, env, cors);
      case '/barcode': return handleBarcode(body, cors);
      case '/ogimage': return handleOgImage(body, cors);
      case '/wineimg': return json({ image: null }, 200, cors);
      case '/acct/status': return json({ gated: false }, 200, cors);
      default: return json({ error: 'not_found' }, 404, cors);
    }
  },
};
