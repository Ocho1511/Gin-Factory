# Auftrag Anleitungen (Guides) in 24 Sprachen

Apps: **Gin-Factory** (C:\wk\Gin-Factory) und **My Whiskey Collection** (C:\wk\My-Whiskey-Collection).
Sprachcodes: de, en, es, sv, da, fi, ru, it, fr, pl, hu, cs, sk, ro, hr, pt, no, nl, el, uk, ja, ko, zh, hi.

## Vorlage
Die Whiskey-App hat Anleitungen `anleitung-<code>.html` (je ~25 KB, 13 Abschnitte, Inhaltsverzeichnis, Sprachauswahl oben, gleiches CSS) und `anleitung.html` (= deutsche Fassung). Diese sind die Vorlage für Aufbau, Stil, CSS und Sprachumschalter.

## Aufgabe je Sprache `<code>` (zwei Teile)

### Teil A – Whiskey-Anleitung erweitern (Datei in C:\wk\My-Whiskey-Collection\anleitung-<code>.html, nur bearbeiten, nicht neu schreiben)
Zwei neue Abschnitte nach dem Abschnitt „Wunschliste" einfügen und Nummerierung (Überschriften UND Inhaltsverzeichnis, `id`/`href`-Anker) konsistent fortschreiben:
1. **Perfect Serve und Gläser**: Im Formular „Whisky hinzufügen/bearbeiten" gibt es den Block Perfect Serve. Zwei Knöpfe: *Regel-Empfehlung* (offline, kostenlos, nach Typ/Torf/Sherry/Bourbon…) und *KI-Empfehlung* (kostet einen KI-Scan). Ergebnis: bis zu drei Genussarten (pur, mit ein paar Tropfen Wasser, auf Eis, Highball, Cocktail) mit Begründung; Antippen setzt eine als Favorit. Felder: Mixer & Garnitur, Wasser/Mischung, Glas, Eis, passende Speisen. Das Glas (z. B. Glencairn-Glas) ist ein Link „Glas ansehen": öffnet eine Karte mit Zeichnung und kurzer Erklärung (Glencairn, Tumbler, Highball, Coupe, Julep-Becher, Irish-Coffee-Glas) und einen Link zu mehr Bildern. Auf der Whisky-Karte stehen Favorit, Garnitur und Glas.
2. **Rezepte und Zutatenregal**: Reiter „Rezepte" (statt des früheren Trinkreife-Reiters): 12 Klassiker (Old Fashioned, Manhattan, Whisky Sour, Highball, Mint Julep, Penicillin, Rob Roy, Boulevardier, Irish Coffee, Rusty Nail, Paper Plane, Gold Rush) mit Zutaten und Zubereitung; Filter Alle / Favoriten (⭐) / Eigene / „Passt zu meiner Bar"; eigene Rezepte anlegen; „Rezept für diesen Whisky (KI)" erzeugt ein Rezept, das man speichern kann; Zutatenregal: antippen, was man zu Hause hat; die Empfehlungen zeigen ✓ (vorhanden) oder 🛒 (fehlt); „Fehlendes auf die Wunschliste" legt fehlende Zutaten dort an. Rezepte, Favoriten und Regal werden mit dem Cloud-Sync gesichert.
Außerdem: im Abschnitt Setup/Export den Hinweis ergänzen, dass im Kontaktbereich (aufklappbar) der Name des Entwicklers und „Last Build: Datum" steht. Den Abschnitt 'Trinkreife' o. Ä. gibt es nicht mehr (falls irgendwo erwähnt: streichen).

### Teil B – Gin-Anleitung NEU (C:\wk\Gin-Factory\anleitung-<code>.html)
Aus der soeben erweiterten Whiskey-Anleitung die **Gin-Anleitung** ableiten (gleicher Aufbau, gleiches CSS, Sprachumschalter verweist auf anleitung-<code>.html, „← Zur Sammlung" verlinkt index.html, Titel „Anleitung – Gin-Factory"). Inhaltliche Anpassungen:
- Whiskey → Gin, Destillerie bleibt Destillerie/Hersteller. Stile statt Typen: **London Dry, Old Tom / Plymouth, Pink / Fruchtgin, Navy Strength, Tonic Water, Sonstiges**. Felder: Name/Destillerie, Abfüllung (Jahr), Flaschen, Bestand (Min/Max), Gin-Stil, Region, Land, **Botanicals**, **Alkoholgehalt (% vol.)**, **Passendes Tonic Water**, Perfect Serve, Lagerplatz (Regal · Ebene · Platz), Preis, Flaschenbild, Eigenes Foto, Bewertung, Notiz. (Kein Alter/Fass mehr.)
- Die App heißt „Gin-Factory", der Hauptreiter „Bar" (Sammlung = deine Gins). Reiter: Bar, Statistik, Rezepte, Historie, Regale, Wunschliste, Export/Import, Setup.
- **Tonic Water als eigene Kategorie**: Tonics wie Gins anlegen (Stil „Tonic Water"); die KI ordnet einem Gin das passende Tonic zu (🤖 im Feld „Passendes Tonic Water", oder in den Einstellungen „Tonic Waters zuordnen (KI)" für alle Gins auf einmal). Auf der Tonic-Karte steht „Passt zu: …".
- **Perfect Serve für Gin**: Knöpfe Regel-Empfehlung / KI-Empfehlung; bis zu drei Tonic-Empfehlungen mit Begründung; „✓ in deiner Bar" oder „🛒 Einkaufstipp" mit Knopf „+ Wunschliste"; Antippen setzt das Tonic als Favorit; Kräuter und Garnitur (Rosmarin, Thymian, Basilikum, Gurke, Grapefruitzeste, rosa Pfeffer …), Mischung (z. B. 1:2), Glas, Eis. Gläser mit Info-Karte: Copa-/Ballonglas, Highball, Tumbler, Coupe, Martiniglas, Sektflöte.
- **Rezepte**: 13 Klassiker (Gin & Tonic, Mediterraner G&T, Pink Gin & Tonic, Navy-Strength-G&T, Negroni, Dry Martini, Gimlet, Tom Collins, Southside, French 75, Bee's Knees, Martinez, Gin Basil Smash); Filter Alle / Favoriten / Eigene / „Passt zu meiner Bar"; eigene Rezepte; „Rezept für diesen Gin (KI)"; **Kräuter- und Garnitur-Regal** (antippen, was man hat; ✓/🛒; „Fehlendes auf die Wunschliste").
- Wunschliste, Regale (Ebenen/Plätze, QR-Etiketten), Historie, Statistik, Export/Import, Setup (Anzeigename, Währung, Sprache, Schriftart, Konfetti & Sound, Cloud-Sync mit Sync-Code, KI-Guthaben, Datenschutz, Anleitung, Support, Kontakt mit „Last Build"), KI/Datenschutz/Kosten: übernehmen und auf Gin anpassen. Unter „Setup" auch den Knopf „Anleitung" erwähnen.
- Keine Trinkreife, keine Trinktemperatur, kein Trinkfenster, keine Fass-/Altersangaben, kein Vivino.

## Zitieren der App-Beschriftungen
Namen von Reitern, Knöpfen und Feldern müssen **exakt so** geschrieben werden wie in der App in der jeweiligen Sprache. Quelle: die App-Dateien enthalten im Block `const I18N = {` je Sprache einen Block `<code>: {`. Verwende für Schlüssel wie nav_*, o_*, t_*, l_*, setup_*, serve_*, tonic_*, rec_*, sx_*, glass_* die dortigen Werte. Die neuen Übersetzungen liegen zusätzlich als Dateien C:\wk\Gin-Factory\_tools\i18n\tr_gin_<code>.json und tr_whiskey_<code>.json (Schlüssel wie in den Apps, z. B. sx_rec_title, rec_gt_n, glass_copa_title, tonic_classic_n); nutze diese für Namen von Rezepten, Gläsern, Tonic-Stilen und neuen Knöpfen. Wo der Name eines Knopfes nur in de/en existiert, übersetze ihn sinngemäß und konsistent.

## Qualität
- Natürliche, freundliche Sprache; Du-Form (bzw. in der Zielsprache übliche Anrede wie in der vorhandenen Anleitung).
- Gültiges HTML (UTF-8), CSS unverändert aus der Vorlage; keine externen Ressourcen.
- Nach dem Schreiben prüfen: Datei öffnet sich (kein Abbruch mitten im Tag), `<h2>`-Zahl stimmt mit dem Inhaltsverzeichnis überein, alle Anker funktionieren, Sprachumschalter enthält alle 24 Codes.
- Zusätzlich für Gin und Whiskey: `anleitung.html` = Kopie der deutschen Fassung (nur der Agent für Sprache `de` legt sie an).
