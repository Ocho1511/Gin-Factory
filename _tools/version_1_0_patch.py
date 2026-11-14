import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/wk/'


def rd(p): return open(W + p, encoding='utf-8').read()
def wr(p, s): open(W + p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, a, b, count=1, label=''):
    c = s.count(a)
    assert c == count, (label, c, a[:80])
    return s.replace(a, b)


# ---- 1) Whiskey-Web-App: Version 1.0 ----
s = rd('My-Whiskey-Collection/index.html')
s = rep(s, "const APP_VERSION = '2.0';", "const APP_VERSION = '1.0';", label='whiskey version')
wr('My-Whiskey-Collection/index.html', s)

# ---- 2) Gin-Web-App: APP_VERSION + Versionsanzeige im Setup (wie Whiskey) ----
w = rd('My-Whiskey-Collection/index.html')
# setup_version je Sprache aus dem Whiskey-Sprachblock
ver = {}
lang = None
for l in w[w.index('const I18N = {'):].split('\n'):
    m = re.match(r'^([a-z]{2}): \{$', l)
    if m: lang = m.group(1)
    m2 = re.match(r'^(\s+)setup_version: (".*")(,?)$', l)
    if m2 and lang: ver.setdefault(lang, m2.group(2))
    if l.startswith('};') and lang == 'hi': break
assert len(ver) == 24, len(ver)

g = rd('Gin-Factory/index.html')
g = rep(g, "const BUILD_DATE = '", "const APP_VERSION = '1.0';   // = MARKETING_VERSION im iOS-Projekt (Gin-Factory-App/ios/App/App.xcodeproj): bei jeder neuen App-Version beide aendern\nconst BUILD_DATE = '", label='gin const')
g = rep(g, '''          <div class="title" data-i18n="setup_support">Support &amp; Hilfe</div>
        </div>
      </a>
    </div>''', '''          <div class="title" data-i18n="setup_support">Support &amp; Hilfe</div>
        </div>
      </a>
      <div class="app-version" id="app-version"></div>
    </div>''', label='gin version div')
g = g.replace('</style>', '.app-version { text-align: center; font-size: 12px; font-weight: 600; color: var(--text-dim, var(--text-muted)); margin-top: 18px; }\n</style>', 1)
g = rep(g, "function applyBuildInfo() {\n  const el = document.getElementById('last-build');",
        "function applyBuildInfo() {\n  const av = document.getElementById('app-version');\n  if (av) av.textContent = t('setup_version') + ' ' + APP_VERSION;\n  const el = document.getElementById('last-build');", label='gin apply')
out = []; lang = None; n = 0
for l in g.split('\n'):
    out.append(l)
    m = re.match(r'^([a-z]{2}): \{$', l)
    if m and l.endswith('{') and l[:2] in ver and g.index('const I18N = {') < g.index(l + '\n'):
        pass
g2 = []; in_i = False; lang = None
for l in g.split('\n'):
    if l.startswith('const I18N = {'): in_i = True
    g2.append(l)
    m = re.match(r'^([a-z]{2}): \{$', l)
    if in_i and m:
        lang = m.group(1)
        g2.append('  setup_version: %s,' % ver[lang]); n += 1
assert n == 24, n
g = '\n'.join(g2)
wr('Gin-Factory/index.html', g)

# ---- 3) iOS-Huellen ----
p = rd('My-Whiskey-Collection-App/ios/App/App.xcodeproj/project.pbxproj')
p = rep(p, 'MARKETING_VERSION = 2.0;', 'MARKETING_VERSION = 1.0;', count=2, label='whiskey pbxproj')
wr('My-Whiskey-Collection-App/ios/App/App.xcodeproj/project.pbxproj', p)

cm = rd('Gin-Factory-App/codemagic.yaml')
orig = rd('Weinkeller-App/codemagic.yaml')
m_o = re.search(r"      - name: Pr[^\n]*Versionsnummer[^\n]*\n        script: \|\n(?:          [^\n]*\n)+", orig)
m_g = re.search(r"      - name: Versionsnummer pruefen\n        script: \|\n(?:          [^\n]*\n)+", cm)
assert m_o and m_g
cm = cm.replace(m_g.group(0), m_o.group(0))
wr('Gin-Factory-App/codemagic.yaml', cm)

# Syntaxpruefung der Web-Apps
for f in ('Gin-Factory/index.html', 'My-Whiskey-Collection/index.html'):
    s = rd(f)
    c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
    open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
    print(f, 'syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
print('ok')
