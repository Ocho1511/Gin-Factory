import re, sys, json, subprocess, html
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:100])
    s = s.replace(a, b)


# --- 1) Autovervollaendigung: Botanicals/Regionen/Laender fuer Gin statt Weintrauben/Weinregionen ---
BOT = {
    'de': ['Wacholder', 'Koriandersamen', 'Angelikawurzel', 'Süßholz', 'Iriswurzel', 'Zitronenschale', 'Orangenschale', 'Grapefruitschale', 'Limette', 'Bergamotte', 'Pomelo',
           'Kardamom', 'Zimt', 'Kassia', 'Muskatnuss', 'Ingwer', 'Schwarzer Pfeffer', 'Rosa Pfeffer', 'Paradieskörner', 'Kubebenpfeffer', 'Nelke', 'Lavendel', 'Rose',
           'Holunderblüte', 'Kamille', 'Hibiskus', 'Gurke', 'Minze', 'Basilikum', 'Thymian', 'Rosmarin', 'Salbei', 'Olive', 'Preiselbeere', 'Schlehe', 'Himbeere',
           'Erdbeere', 'Lakritz', 'Fenchel', 'Anis', 'Sternanis', 'Mandel', 'Tonkabohne', 'Vanille', 'Zitronenverbene', 'Wermut', 'Beifuß', 'Tannenspitzen', 'Zirbelkiefer'],
    'en': ['Juniper', 'Coriander seed', 'Angelica root', 'Liquorice', 'Orris root', 'Lemon peel', 'Orange peel', 'Grapefruit peel', 'Lime', 'Bergamot', 'Pomelo',
           'Cardamom', 'Cinnamon', 'Cassia', 'Nutmeg', 'Ginger', 'Black pepper', 'Pink pepper', 'Grains of paradise', 'Cubeb', 'Clove', 'Lavender', 'Rose',
           'Elderflower', 'Chamomile', 'Hibiscus', 'Cucumber', 'Mint', 'Basil', 'Thyme', 'Rosemary', 'Sage', 'Olive', 'Cranberry', 'Sloe', 'Raspberry',
           'Strawberry', 'Liquorice', 'Fennel', 'Anise', 'Star anise', 'Almond', 'Tonka bean', 'Vanilla', 'Lemon verbena', 'Wormwood', 'Mugwort', 'Pine tips', 'Stone pine'],
}
REG = {
    'de': ['London', 'Plymouth', 'Schottland', 'Islay', 'Highlands', 'England', 'Cornwall', 'Norfolk', 'Yorkshire', 'Wales', 'Irland', 'Katalonien', 'Barcelona', 'Menorca',
           'Andalusien', 'Segovia', 'Niederlande', 'Schiedam', 'Belgien', 'Deutschland', 'Schwarzwald', 'Hamburg', 'Berlin', 'Bayern', 'Rheinland', 'Frankreich',
           'Italien', 'Südtirol', 'Piemont', 'Österreich', 'Tirol', 'Schweiz', 'USA', 'Kalifornien', 'Oregon', 'New York', 'Kentucky', 'Texas', 'Australien',
           'Tasmanien', 'Victoria', 'Neuseeland', 'Japan', 'Kyoto', 'Hokkaido', 'Indien', 'Südafrika', 'Kapstadt', 'Schweden', 'Dänemark', 'Norwegen', 'Finnland'],
    'en': ['London', 'Plymouth', 'Scotland', 'Islay', 'Highlands', 'England', 'Cornwall', 'Norfolk', 'Yorkshire', 'Wales', 'Ireland', 'Catalonia', 'Barcelona', 'Menorca',
           'Andalusia', 'Segovia', 'Netherlands', 'Schiedam', 'Belgium', 'Germany', 'Black Forest', 'Hamburg', 'Berlin', 'Bavaria', 'Rhineland', 'France',
           'Italy', 'South Tyrol', 'Piedmont', 'Austria', 'Tyrol', 'Switzerland', 'USA', 'California', 'Oregon', 'New York', 'Kentucky', 'Texas', 'Australia',
           'Tasmania', 'Victoria', 'New Zealand', 'Japan', 'Kyoto', 'Hokkaido', 'India', 'South Africa', 'Cape Town', 'Sweden', 'Denmark', 'Norway', 'Finland'],
}


def js_arr(a):
    return '[' + ', '.join("'" + x.replace("'", "\\'") + "'" for x in a) + ']'


s, n = re.subn(r"const DB_GRAPES = \[\n.*?\];\nconst DB_REGIONS = \[\n.*?\];\n",
               lambda m: ("// Botanicals und Herkunftsregionen für die Autovervollständigung (de/en; andere Sprachen nehmen Englisch)\n"
                          "const DB_GRAPES = { de: " + js_arr(BOT['de']) + ", en: " + js_arr(BOT['en']) + " };\n"
                          "const DB_REGIONS = { de: " + js_arr(REG['de']) + ", en: " + js_arr(REG['en']) + " };\n"), s, count=1, flags=re.S)
assert n == 1
rep("  fillDatalist('dl-grape', DB_GRAPES);\n  fillDatalist('dl-region', DB_REGIONS);\n  fillDatalist('dl-country', DB_COUNTRIES[baseLang()] || DB_COUNTRIES.de);",
    "  const bl = baseLang() === 'de' ? 'de' : 'en';\n  fillDatalist('dl-grape', DB_GRAPES[bl]);\n  fillDatalist('dl-region', DB_REGIONS[bl]);\n  fillDatalist('dl-country', DB_COUNTRIES[baseLang()] || DB_COUNTRIES.en);")
# Gin-Laender ergaenzen (Schottland, Niederlande, Belgien, Irland, Indien, Skandinavien)
rep("'Polen','Luxemburg','England','Kanada'", "'Polen','Luxemburg','England','Schottland','Wales','Irland','Niederlande','Belgien','Schweden','Dänemark','Norwegen','Finnland','Indien','Kanada'")
rep("'Poland','Luxembourg','England','Canada'", "'Poland','Luxembourg','England','Scotland','Wales','Ireland','Netherlands','Belgium','Sweden','Denmark','Norway','Finland','India','Canada'")
rep("'Polonia','Luxemburgo','Inglaterra','Canadá'", "'Polonia','Luxemburgo','Inglaterra','Escocia','Gales','Irlanda','Países Bajos','Bélgica','Suecia','Dinamarca','Noruega','Finlandia','India','Canadá'")
rep("// WEINDATENBANK (Autovervollständigung + KI-Nachschlagen)", "// GIN-DATENBANK (Autovervollständigung + KI-Nachschlagen)")
rep("<!-- WEINDATENBANK (Autovervollständigung) -->", "<!-- GIN-DATENBANK (Autovervollständigung) -->")
rep("ADD WINE MODAL", "ADD GIN MODAL")

# --- 2) Tooltip des Trinken-Knopfs aus den Sprachtexten ---
rep('id="fab-drink" title="Wein trinken (Scan)">', 'id="fab-drink" title="Gin trinken (Scan)">')
rep("  applyGuideLink();\n  applyBuildInfo();\n  fitNavLabels();", "  applyGuideLink();\n  applyBuildInfo();\n  const fd = document.getElementById('fab-drink'); if (fd) fd.title = t('dm_title');\n  fitNavLabels();")
# Anfragetext: Abfuellung statt Jahrgang
rep("' (Jahrgang ' + year + ')'", "' (Abfüllung ' + year + ')'")

# --- 3) Statische HTML-Vorgaben (vor applyI18n sichtbar) mit den deutschen Gin-Texten abgleichen ---
m = re.search(r'\nde: \{\n(.*?)\n\},?\nen: \{', s, re.S)
de = {}
for line in m.group(1).split('\n'):
    mm = re.match(r'^\s+([a-z_0-9]+): (".*"),?$', line)
    if mm:
        de[mm.group(1)] = json.loads(mm.group(2))
html_end = s.index('<script>')
head, tail = s[:html_end], s[html_end:]
WINE = re.compile(r'Wein|Rebsort|Jahrgang|Rotwein|Weißwein|Weingut|Weintyp|Trinkreife|[Ww]ine')
changed = []


def fix_text(mt):
    key, txt = mt.group(2), mt.group(4)
    if key in de and WINE.search(txt) and '<' not in de[key]:
        new = html.escape(de[key], quote=False)
        changed.append((key, txt[:30], new[:30]))
        return mt.group(1) + new + mt.group(5)
    return mt.group(0)


head = re.sub(r'(<[^>]*data-i18n="([a-z_0-9]+)"([^>]*)>)([^<]*)(</)', fix_text, head)


def fix_ph(mp):
    key, txt = mp.group(3), mp.group(1)
    if key in de and WINE.search(txt):
        changed.append((key, txt[:30], de[key][:30]))
        return mp.group(0).replace('placeholder="' + txt + '"', 'placeholder="' + html.escape(de[key]) + '"')
    return mp.group(0)


head = re.sub(r'placeholder="([^"]*)"([^>]*?)data-i18n-ph="([a-z_0-9]+)"', fix_ph, head)
# <div data-i18n="barcode_miss_text">...</div> usw. mit mehrzeiligem/langem Text wird ueber fix_text mit erfasst
s = head + tail
print('HTML-Vorgaben angeglichen:', len(changed))
for c in changed:
    print('  ', c)
left = [l.strip()[:110] for l in head.split('\n') if WINE.search(l)]
print('HTML-Zeilen mit Wein-Begriffen danach:', len(left)); print('\n'.join(left[:15]))
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
