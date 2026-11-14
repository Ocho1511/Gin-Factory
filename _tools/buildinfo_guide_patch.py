import re, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:100])
    s = s.replace(a, b)


BUILD_DATE = '2026-11-15'

# 1) Last Build im Kontaktbereich, ganz unten
rep('        <div class="contact-copyright">© 2026 Thomas Knecht. All rights reserved.</div>\n      </div>\n    </details>',
    '        <div class="contact-copyright">© 2026 Thomas Knecht. All rights reserved.</div>\n        <div class="contact-build" id="last-build"></div>\n      </div>\n    </details>')
rep('.contact-copyright {\n  font-size: 11px;\n  font-weight: 700;\n  color: var(--text-muted);\n  margin-top: 12px;\n}',
    '.contact-copyright {\n  font-size: 11px;\n  font-weight: 700;\n  color: var(--text-muted);\n  margin-top: 12px;\n}\n.contact-build { font-size: 11px; font-weight: 600; color: var(--text-dim, var(--text-muted)); margin-top: 6px; }')

# 2) Konstanten frueh (vor dem ersten applyI18n-Aufruf) + Funktionen
rep("const AI_PROXY_URL = 'https://weinkeller-scan-proxy.ocho1511.workers.dev';",
    "const AI_PROXY_URL = 'https://weinkeller-scan-proxy.ocho1511.workers.dev';\n"
    "// Letzter Build: bei jeder Veroeffentlichung auf das aktuelle Datum setzen (ISO). Anzeige: Einstellungen > Kontakt, ganz unten.\n"
    "const BUILD_DATE = '" + BUILD_DATE + "';\n"
    "// Anleitung, Datenschutz und Support liegen neben der App: im Web relativ (egal, wo sie gehostet wird); die native App hat sie nicht lokal und nimmt die Webadresse.\n"
    "const PAGES_URL = 'https://ocho1511.github.io/Gin-Factory/';\n"
    "const siteUrl = (p) => (isNativeApp() ? PAGES_URL : '') + p;")
rep("function applyI18n() {",
    "function applyGuideLink() {\n"
    "  const a = document.getElementById('guide-link');\n"
    "  if (a) a.href = siteUrl('anleitung-' + baseLang() + '.html');\n"
    "  const pv = document.getElementById('privacy-link'); if (pv) pv.href = siteUrl('datenschutz.html');\n"
    "  const sp = document.getElementById('support-link'); if (sp) sp.href = siteUrl('support.html');\n"
    "}\n"
    "// 'Last Build: <Datum>' (Datum in der Landesform der gewaehlten Sprache; das Wort 'Last Build:' bleibt in allen Sprachen gleich)\n"
    "function applyBuildInfo() {\n"
    "  const el = document.getElementById('last-build');\n"
    "  if (!el) return;\n"
    "  let d = BUILD_DATE;\n"
    "  try { d = new Date(BUILD_DATE + 'T12:00:00').toLocaleDateString(dateLocale(), { day: '2-digit', month: '2-digit', year: 'numeric' }); } catch (e) {}\n"
    "  el.textContent = 'Last Build: ' + d;\n"
    "}\n"
    "function applyI18n() {")
rep("  applyOwnerTitles();\n  fitNavLabels();\n  const active = document.querySelector('.tab.active');",
    "  applyOwnerTitles();\n  applyGuideLink();\n  applyBuildInfo();\n  fitNavLabels();\n  const active = document.querySelector('.tab.active');")

# 3) Setup: Datenschutz / Anleitung / Support (eigene Seiten dieser App)
rep('''      <a class="export-card" href="https://ocho1511.github.io/Weinkeller/datenschutz.html" target="_blank" rel="noopener" style="text-decoration:none; color:inherit">
        <div class="export-icon">🔒</div>
        <div class="export-info">
          <div class="title" data-i18n="setup_privacy">Datenschutzerklärung</div>
        </div>
      </a>
      <a class="export-card" href="https://ocho1511.github.io/Weinkeller/support.html" target="_blank" rel="noopener" style="text-decoration:none; color:inherit; margin-top:10px">''',
    '''      <a class="export-card" id="privacy-link" href="datenschutz.html" target="_blank" rel="noopener" style="text-decoration:none; color:inherit">
        <div class="export-icon">🔒</div>
        <div class="export-info">
          <div class="title" data-i18n="setup_privacy">Datenschutzerklärung</div>
        </div>
      </a>
      <a class="export-card" id="guide-link" href="anleitung.html" target="_blank" rel="noopener" style="text-decoration:none; color:inherit; margin-top:10px">
        <div class="export-icon">📖</div>
        <div class="export-info">
          <div class="title" data-i18n="setup_guide">Anleitung</div>
        </div>
      </a>
      <a class="export-card" id="support-link" href="support.html" target="_blank" rel="noopener" style="text-decoration:none; color:inherit; margin-top:10px">''')

# 4) i18n: setup_guide (de/en; andere Sprachen fallen auf en zurueck)
out = []
for l in s.split('\n'):
    out.append(l)
    if l == 'de: {':
        out.append('  setup_guide: "Anleitung",')
    elif l == 'en: {':
        out.append('  setup_guide: "Guide",')
s = '\n'.join(out)

# 5) Titel mit Eigentuemername: Markenname 'Gin-Factory' in allen Sprachen (nicht 'Weinkeller')
s, n = re.subn(r'(\n  (?:[a-z]{2}(?:-[A-Za-z]+)?): \[)"[^"\n]*", ("[^"\n]*", "[^"\n]*"\],)', lambda m: m.group(1) + '"{o}\'s Gin-Factory", ' + m.group(2), s)
print('TITLE_PATTERNS-Zeilen geaendert:', n)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
