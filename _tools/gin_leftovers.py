import re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:70])
    s = s.replace(a, b)


# --- ABV field: form input (placed in the hidden drink-window row's place: new row before price) ---
rep('''    <div class="form-row">
      <div class="form-group">
        <label id="price-label">Preis (€)</label>''', '''    <div class="form-row">
      <div class="form-group">
        <label data-i18n="l_abv">Alkoholgehalt (% vol.)</label>
        <input id="f-abv" placeholder="" type="number" min="0" max="100" step="0.1">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label id="price-label">Preis (€)</label>''')
# data model
rep("    ...cleanTemps(w),\n", "    ...cleanTemps(w),\n    abv: (() => { const n = parseFloat(String(w.abv ?? '').replace(',', '.')); return Number.isFinite(n) && n > 0 && n <= 100 ? Math.round(n * 10) / 10 : null; })(),\n")
# edit form load / clear / save / merge
rep("  document.getElementById('f-drink-from').value = w.drinkFrom||'';\n", "  document.getElementById('f-abv').value = w.abv||'';\n  document.getElementById('f-drink-from').value = w.drinkFrom||'';\n")
rep("'f-drink-from','f-drink-to','f-temp-from','f-temp-to','f-price','f-image'", "'f-abv','f-drink-from','f-drink-to','f-temp-from','f-temp-to','f-price','f-image'")
rep("    drinkFrom: parseInt(document.getElementById('f-drink-from').value)||null,\n", "    abv: parseFloat(String(document.getElementById('f-abv').value).replace(',', '.'))||null,\n    drinkFrom: parseInt(document.getElementById('f-drink-from').value)||null,\n")
rep("['region','country','grape','locRegal','locEbene','locPlatz','drinkFrom'", "['region','country','grape','abv','locRegal','locEbene','locPlatz','drinkFrom'")
# AI lookup fills ABV
rep("    setIfEmpty('f-grape', info.grape);\n    setIfEmpty('f-drink-from', info.drinkFrom);", "    setIfEmpty('f-grape', info.grape);\n    setIfEmpty('f-abv', info.abv);\n    setIfEmpty('f-drink-from', info.drinkFrom);", count=2)
rep("    if (info.grape) document.getElementById('f-grape').value = info.grape;\n", "    if (info.grape) document.getElementById('f-grape').value = info.grape;\n    if (info.abv && !document.getElementById('f-abv').value) document.getElementById('f-abv').value = info.abv;\n")
# AI prompts: ask for abv
rep("drinkFrom (immer null), drinkTo (immer null), tempFrom (immer null), tempTo (immer null), ", "abv (Alkoholgehalt in % vol. als Zahl, z. B. 43.0, oder null), drinkFrom (immer null), drinkTo (immer null), tempFrom (immer null), tempTo (immer null), ")
rep("drinkFrom, drinkTo, tempFrom und tempTo sind immer null (Gin reift nicht).", "abv ist der Alkoholgehalt in % vol. als Zahl oder null. drinkFrom, drinkTo, tempFrom und tempTo sind immer null (Gin reift nicht).", count=s.count("drinkFrom, drinkTo, tempFrom und tempTo sind immer null (Gin reift nicht)."))
# cards: show ABV next to year
rep("${w.year||'–'} · ${TYPE_LABELS[w.type]||TYPE_LABELS.other||''}${w.grape", "${w.year||'–'} · ${TYPE_LABELS[w.type]||TYPE_LABELS.other||''}${w.abv?' · '+w.abv+'%':''}${w.grape")
rep("<div class=\"wine-year\">${w.year||''} ${w.grape?'· '+esc(w.grape):''}</div>", "<div class=\"wine-year\">${w.year||''}${w.abv?' · '+w.abv+'%':''} ${w.grape?'· '+esc(w.grape):''}</div>")

# --- export / import headers (gin terms; import still accepts old wine headers) ---
rep("const EXPORT_HEADERS = ['Name','Jahrgang','Typ','Region','Land','Rebsorte','Regal','Ebene','Platz','Flaschen','Bewertung','Preis','Trinken ab','Trinken bis','Notiz'];",
    "const EXPORT_HEADERS = ['Name','Abfüllung','Stil','Region','Land','Botanicals','Regal','Ebene','Platz','Flaschen','Bewertung','Preis','Alkohol %','Notiz'];")
rep("w.rating||'',w.price||'',w.drinkFrom||'',w.drinkTo||'',w.note||'']);", "w.rating||'',w.price||'',w.abv||'',w.note||'']);")
rep("    name: col('name'), year: col('jahrgang'), type: col('typ'),\n    region: col('region'), country: col('land'), grape: col('rebsorte'), location: col('lagerplatz'),",
    "    name: col('name'), year: Math.max(col('abfüllung'), col('jahrgang')), type: Math.max(col('stil'), col('typ')),\n    region: col('region'), country: col('land'), grape: Math.max(col('botanicals'), col('rebsorte')), abv: Math.max(col('alkohol %'), col('abv')), location: col('lagerplatz'),")
rep("drinkFrom: get(cols, 'drinkFrom'), drinkTo: get(cols, 'drinkTo'), note: get(cols, 'note')", "abv: get(cols, 'abv'), note: get(cols, 'note')")
rep("head: [['Name','Jahrgang','Typ','Region','Rebsorte','Lagerplatz','Fl.','Bew.','Preis']]", "head: [['Name','Abfüllung','Stil','Region','Botanicals','Lagerplatz','Fl.','Bew.','Preis']]")

# --- image search: no Vivino (wine only) for gin; keep AI direct image + og:image ---
rep("const viv = (meta && meta.noVivino) ? null : await vivinoImageFor(crit, meta);", "const viv = null;   // Gin-Factory: Vivino kennt nur Wein -> übersprungen")

# --- barcode: never reject spirits as 'not wine' ---
rep("    if (d.notWine) { document.getElementById('f-ean').value = ''; showToast(t('barcode_notwine')); return; }\n", "    // Gin-Factory: der Server-Filter 'notWine' gilt nur für Wein und wird ignoriert\n")

# --- i18n: l_abv in all languages (en text for others; de own) ---
AB = {'de': 'Alkoholgehalt (% vol.)', 'en': 'ABV (% vol.)'}
out = []
lang = None
for l in s.split('\n'):
    m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', l)
    if m:
        lang = m.group(1)
        out.append(l)
        out.append('  l_abv: "%s",' % AB.get(lang, AB['en']))
        continue
    out.append(l)
s = '\n'.join(out)
open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok')
