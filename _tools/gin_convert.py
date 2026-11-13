import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()

DE = {
'credits_info': "Etikett scannen und Gin nachschlagen verbrauchen je 1 KI-Scan. Zum Start sind 50 inklusive.",
'credits_empty_text': "Deine inklusiven KI-Scans sind verbraucht. Lade Guthaben auf, um weiter Etiketten zu scannen und Gins nachzuschlagen. Alles andere in der App funktioniert weiter.",
'credits_enrich_warn': "Für {n} Gins werden KI-Scans benötigt, du hast noch {c}. Es wird nur so weit aktualisiert, wie dein Guthaben reicht. Fortfahren?",
'fav_none': "Keine Gins für diese Auswahl.",
'nav_keller': "Bar",
'racks_sub': "Barplan", 'rack_assign_hint': "Tippe einen Gin, dann ein freies Fach zum Einsortieren.",
'rack_open_wine': "Gin öffnen", 'racks_all_placed': "Alle Gins sind einem Fach zugeordnet ✓",
'setup_racks_desc': "Definiere deine Regale mit Ebenen und Plätzen für den Barplan.",
'rack_del_confirm': "Regal \"{name}\" entfernen? (Gins bleiben erhalten)",
'hist_sub': "Getrunkene Gins",
'sync_email_body_2': "Damit stellst du deine Bar auf einem anderen Gerät wieder her: Setup → Speicherort → Cloud → Code eingeben → Verbinden.",
'search_ph': "🔍  Gin suchen…",
'sort_year': "↕ Abfüllung", 'sort_grape': "↕ Botanicals",
't_rot': "London Dry", 't_weiss': "Old Tom / Plymouth", 't_rose': "Pink / Fruchtgin", 't_sekt': "Navy Strength",
'pill_wines': "Gins",
'keller_sub_one': "Gin in deiner Sammlung", 'keller_sub_many': "Gins in deiner Sammlung",
'empty_keller': "Keine Gins gefunden.<br>Füge deinen ersten Gin hinzu!",
's_top': "Top Gins", 's_drunk': "Getrunkene Gins", 's_drunkvalue': "Wert der getrunkenen Gins",
's_nodrunk': "Noch keine Gins als getrunken markiert.",
'wish_empty': "Noch keine Wünsche.<br>Füge Gins hinzu, die du kaufen möchtest.",
'to_cellar': "→ Bar",
'm_add_title': "Gin hinzufügen", 'm_edit_title': "Gin bearbeiten",
'lookup_btn': "🔎  Gin nachschlagen (KI)", 'toast_lookup': "⏳ Gin wird nachgeschlagen…", 'toast_lookup_ok': "Gin gefunden ✓",
'setup_db': "Gin-Datenbank", 'enrich_btn': "Alle Gins aktualisieren (KI)",
'enrich_desc': "Fehlende Region, Land, Botanicals & Preis ergänzen",
'confirm_enrich': "{n} Gin(s) werden per KI aktualisiert (fehlende Angaben). Fortfahren? (kostet minimal pro Gin)",
'toast_enrich_none': "Keine Gins vorhanden", 'toast_enrich_done': "{n} Gin(s) ergänzt ✓",
'gp_updating': "Gins werden aktualisiert…", 'gp_lookup': "Gin wird nachgeschlagen…",
'l_name': "Name / Destillerie", 'l_year': "Abfüllung (Jahr)", 'l_type': "Gin-Stil", 'l_grape': "Botanicals",
'wiki_open': "Wikipedia (Gin)",
'o_rot': "🌲 London Dry", 'o_weiss': "🍯 Old Tom / Plymouth", 'o_rose': "🌸 Pink / Fruchtgin", 'o_sekt': "⚓ Navy Strength", 'o_other': "◻️ Sonstiges",
'toast_prost': "🥂 Cheers!",
'toast_nomatch': "Kein passender Gin in der Bar gefunden",
'toast_imported1': "1 Gin importiert ✓", 'toast_imported': "{n} Gins importiert ✓",
'store_back': "← Zur Bar",
'confirm_enrich_temp': "Auch bereits vorhandene Angaben durch KI-Werte ersetzen?",
'map_regions_q': "Gin-Regionen Karte", 'map_regions_open': "Gin-Regionen-Karte öffnen",
'enrich_img_fail': "Bei {n} Gins war die Bildsuche gerade nicht erreichbar – deren Bilder blieben unverändert. Bitte später noch einmal starten.",
'store_scan_btn': "📷 Gin scannen & einlagern", 'store_modal_title': "Gin einlagern",
'rack_filter_none': "Keine Gins für diesen Filter.",
'rack_remove_bottles': "{n} Flaschen werden aus dem Regal genommen und gelten danach als „nicht eingelagert“. Die Gins selbst bleiben in der Bar erhalten.",
'rack_clear_confirm': "⚠ Regal „{name}“ leeren?\n\nAlle {n} Flaschen ({w} Gins) werden aus dem Regal genommen und gelten danach als „nicht eingelagert“. Die Gins selbst bleiben in der Bar erhalten.\n\nDas lässt sich nicht automatisch rückgängig machen.",
'rack_delete': "Gin löschen",
'barcode_notwine': "Dieser Barcode gehört nicht zu einem Gin",
'barcode_year': "Bitte das Abfüllungsjahr eintragen (optional)",
'barcode_known': "{name} ist schon in der Bar. Noch eine Flasche hinzufügen?",
'barcode_miss_text': "Dieser Barcode steht nicht in der Datenbank. Die Nummer wird trotzdem am Gin gespeichert, damit die Flasche beim nächsten Scan erkannt wird. Jetzt das Etikett fotografieren?",
'shelf_unknown': "QR-Code nicht erkannt – er gehört zu keinem Regal dieser Bar",
'shelf_store_none': "Keine Gins zum Einlagern",
'mm_wish_added': "{n} Gin(s) auf die Wunschliste gesetzt ✓",
'sync_merge_confirm': "Dieses Gerät enthält bereits {n} Gins. Mit den Cloud-Daten zusammenführen? (Abbrechen = nicht verbinden)",
'import_replace_confirm': "Die {cur} Gins in der Bar werden durch die Sicherung ({n} Gins) ersetzt. Fortfahren?",
'ai_consent': "Für Etikett-Scan und Nachschlagen werden das Foto bzw. der Gin-Name über unseren Server an Anthropic (Claude, USA) zur Auswertung gesendet. Es werden keine Namen oder Konten übermittelt. Einverstanden?",
'toast_moved': "In Bar verschoben ✓",
'confirm_del': "Gin entfernen?", 'dm_title': "Gin trinken",
'dm_last': "Dies ist die letzte Flasche — der Gin wird aus der Bar entfernt.",
'pdf_sub': "{n} Gins · Stand: {d}",
}
EN = {
'credits_info': "Scanning a label and looking up a gin each use 1 AI scan. 50 are included to start.",
'credits_empty_text': "Your included AI scans are used up. Top up to keep scanning labels and looking up gins. Everything else in the app keeps working.",
'credits_enrich_warn': "AI scans are needed for {n} gins, you have {c} left. Only as many as your balance allows will be updated. Continue?",
'fav_none': "No gins for this selection.",
'nav_keller': "Bar",
'racks_sub': "Bar plan", 'rack_assign_hint': "Tap a gin, then an empty slot to place it.",
'rack_open_wine': "Open gin", 'racks_all_placed': "All gins are assigned to a slot ✓",
'setup_racks_desc': "Define your shelves with levels and slots for the bar plan.",
'rack_del_confirm': "Remove shelf \"{name}\"? (gins are kept)",
'hist_sub': "Gins you drank",
'sync_email_body_2': "Use it to restore your bar on another device: Setup → Storage → Cloud → enter code → Connect.",
'search_ph': "🔍  Search gin…",
'sort_year': "↕ Bottling year", 'sort_grape': "↕ Botanicals",
't_rot': "London Dry", 't_weiss': "Old Tom / Plymouth", 't_rose': "Pink / Fruit gin", 't_sekt': "Navy Strength",
'pill_wines': "Gins",
'keller_sub_one': "gin in your collection", 'keller_sub_many': "gins in your collection",
'empty_keller': "No gins found.<br>Add your first gin!",
's_top': "Top gins", 's_drunk': "Gins you drank", 's_drunkvalue': "Value of gins you drank",
's_nodrunk': "No gins marked as drunk yet.",
'wish_empty': "No wishes yet.<br>Add gins you want to buy.",
'to_cellar': "→ Bar",
'm_add_title': "Add gin", 'm_edit_title': "Edit gin",
'lookup_btn': "🔎  Look up gin (AI)", 'toast_lookup': "⏳ Looking up gin…", 'toast_lookup_ok': "Gin found ✓",
'setup_db': "Gin database", 'enrich_btn': "Update all gins (AI)",
'enrich_desc': "Fill in missing region, country, botanicals & price",
'confirm_enrich': "{n} gin(s) will be updated by AI (missing details). Continue? (small cost per gin)",
'toast_enrich_none': "No gins available", 'toast_enrich_done': "{n} gin(s) updated ✓",
'gp_updating': "Updating gins…", 'gp_lookup': "Looking up gin…",
'l_name': "Name / Distillery", 'l_year': "Bottling year", 'l_type': "Gin style", 'l_grape': "Botanicals",
'wiki_open': "Wikipedia (gin)",
'o_rot': "🌲 London Dry", 'o_weiss': "🍯 Old Tom / Plymouth", 'o_rose': "🌸 Pink / Fruit gin", 'o_sekt': "⚓ Navy Strength", 'o_other': "◻️ Other",
'toast_prost': "🥂 Cheers!",
'toast_nomatch': "No matching gin found in the bar",
'toast_imported1': "1 gin imported ✓", 'toast_imported': "{n} gins imported ✓",
'store_back': "← To bar",
'confirm_enrich_temp': "Also replace existing details with AI values?",
'map_regions_q': "Gin regions map", 'map_regions_open': "Open gin regions map",
'enrich_img_fail': "Image search was unreachable for {n} gins – their images were left unchanged. Please try again later.",
'store_scan_btn': "📷 Scan & store gin", 'store_modal_title': "Store gin",
'rack_filter_none': "No gins for this filter.",
'rack_remove_bottles': "{n} bottles will be taken off the shelf and count as \"not stored\". The gins themselves stay in your bar.",
'rack_clear_confirm': "⚠ Clear shelf \"{name}\"?\n\nAll {n} bottles ({w} gins) will be taken off the shelf and count as \"not stored\". The gins themselves stay in your bar.\n\nThis cannot be undone automatically.",
'rack_delete': "Delete gin",
'barcode_notwine': "This barcode does not belong to a gin",
'barcode_year': "Please enter the bottling year (optional)",
'barcode_known': "{name} is already in the bar. Add another bottle?",
'barcode_miss_text': "This barcode is not in the database. The number is still saved with the gin so the bottle is recognised next time. Photograph the label now?",
'shelf_unknown': "QR code not recognised – it does not belong to any shelf in this bar",
'shelf_store_none': "No gins to store",
'mm_wish_added': "{n} gin(s) added to the wish list ✓",
'sync_merge_confirm': "This device already contains {n} gins. Merge with the cloud data? (Cancel = do not connect)",
'import_replace_confirm': "The {cur} gins in the bar will be replaced by the backup ({n} gins). Continue?",
'ai_consent': "For label scanning and lookup, the photo or gin name is sent via our server to Anthropic (Claude, USA) for analysis. No names or accounts are transmitted. Agree?",
'toast_moved': "Moved to bar ✓",
'confirm_del': "Remove gin?", 'dm_title': "Drink gin",
'dm_last': "This is the last bottle — the gin will be removed from the bar.",
'pdf_sub': "{n} gins · as of {d}",
}


def esc(v):
    return json.dumps(v, ensure_ascii=False)


i0 = s.index('const I18N = {')
i1 = s.index('\n};', s.index('\nzh:', i0))
head, block, tail = s[:i0], s[i0:i1], s[i1:]
out = []
lang = None
hits = 0
for l in block.split('\n'):
    m = re.match(r'^([a-z]{2}(?:-[A-Za-z]+)?): \{$', l)
    if m:
        lang = m.group(1)
    m2 = re.match(r'^(\s+)([a-z_0-9]+): (".*"|\'.*\')(,?)$', l)
    if m2 and lang:
        k = m2.group(2)
        d = DE if lang == 'de' else EN
        if k in d:
            l = f'{m2.group(1)}{k}: {esc(d[k])}{m2.group(4)}'
            hits += 1
    out.append(l)
s = head + '\n'.join(out) + tail
print('i18n replacements', hits)

R = [
('Du bist ein Wein-Experte', 'Du bist ein Gin-Experte'),
('Du bist ein Weinetikett- und Trinkreife-Experte', 'Du bist ein Gin-Etikett-Experte'),
('Du bist ein Weinetikett-Experte', 'Du bist ein Gin-Etikett-Experte'),
('(Endverbraucher, 0,75-l-Flasche)', '(Endverbraucher, 0,7-l-Flasche)'),
('type (rot/weiß/rosé/sekt/other)', 'type (rot = London Dry, weiß = Old Tom/Plymouth/Genever, rosé = Pink/Fruchtgin/Flavoured, sekt = Navy Strength, other = sonstiger Gin)'),
('region (Anbaugebiet oder null)', 'region (Herkunftsregion oder null)'),
('grape (Hauptrebsorte oder null)', 'grape (wichtigste Botanicals, kommagetrennt, max. 5, oder null)'),
('grape (Rebsorte oder null)', 'grape (wichtigste Botanicals, kommagetrennt, max. 5, oder null)'),
('Weingut + Weinname', 'Destillerie + Gin-Name'),
('year (Jahrgang als Zahl oder null)', 'year (Abfüllungsjahr als Zahl oder null)'),
('Analysiere dieses Weinetikett', 'Analysiere dieses Gin-Etikett'),
('Du bist ein Preisvergleich für Wein', 'Du bist ein Preisvergleich für Gin'),
('für genau den genannten Wein bei Online-Weinhändlern', 'für genau den genannten Gin bei Online-Gin-Shops'),
('Wein: ${', 'Gin: ${'),
('Nenne Typ, Region, Land, Hauptrebsorte, ein geschätztes Trinkfenster,', 'Nenne Stil, Region, Land, Botanicals,'),
('die Seite des Weinguts oder ein Wein-Shop/Vivino', 'die Seite der Destillerie oder ein Gin-Shop'),
('Du liest Beschriftungen von Weinregalen', 'Du liest Beschriftungen von Regalen'),
]
for a, b in R:
    c = s.count(a)
    s = s.replace(a, b)
    print(c, a[:50])
s, n1 = re.subn(r'drinkFrom \(Jahr als Zahl oder null\), drinkTo \(Jahr als Zahl oder null\), tempFrom \([^)]*\), tempTo \([^)]*\), ',
                'drinkFrom (immer null), drinkTo (immer null), tempFrom (immer null), tempTo (immer null), ', s)
s, n2 = re.subn(r'drinkFrom \(Jahr als Zahl, ab dem der Wein.*?nutze null\.',
                'drinkFrom, drinkTo, tempFrom und tempTo sind immer null (Gin reift nicht). Wenn etwas nicht erkennbar ist, nutze null.', s, flags=re.S)
print('drink strips', n1, n2)

css = '''
/* Gin-Factory: Gin reift nicht -> Trinkreife/Temperatur ausblenden */
.nav-btn[onclick*="trinkreife"], #drinkrule-btn, .form-row:has(#f-drink-from), .form-row:has(#f-temp-from),
.form-group:has([data-i18n="setup_tempunit"]), .wine-ripeness, .wine-temp { display: none !important; }
:root { --wine: #1f6b4f; --wine-light: #2e8f6b; }
'''
s = s.replace('</style>', css + '</style>', 1)
s = s.replace('<option value="ripeness" data-i18n="sort_ripeness">↕ Trinkreife (dringendste zuerst)</option>', '')
s = s.replace('<span class="nav-icon">🍾</span>', '<span class="nav-icon">🍸</span>', 1)
open(P, 'w', encoding='utf-8', newline='').write(s)

m = 'C:/wk/Gin-Factory/manifest.webmanifest'
t = open(m, encoding='utf-8').read()
t = re.sub(r'"description": ".*?"', '"description": "Deine persönliche Gin-Factory – Bestand, Botanicals, Regale und mehr."', t)
open(m, 'w', encoding='utf-8').write(t)
print('done')
