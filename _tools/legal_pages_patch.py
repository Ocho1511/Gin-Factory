import re, sys
sys.stdout.reconfigure(encoding='utf-8')

D = 'C:/wk/Gin-Factory/datenschutz.html'
S = 'C:/wk/Gin-Factory/support.html'

d = open(D, encoding='utf-8').read()
pairs_d = [
    ('Stand: 31. Oktober 2026', 'Stand: 15. November 2026'),
    ('zur Verwaltung einer privaten Weinsammlung', 'zur Verwaltung einer privaten Gin-Sammlung'),
    ('<h2>3. Deine Weindaten</h2>', '<h2>3. Deine Gin-Daten</h2>'),
    ('Deine Weine, Wunschliste, Trinkhistorie, Regalpläne', 'Deine Gins, Tonic Waters, Wunschliste, Rezepte, Trinkhistorie, Regalpläne'),
    ('deine Weindaten (Weine, Wunschliste, Historie, Regale, Anzeigename)', 'deine Gin-Daten (Gins, Tonic Waters, Wunschliste, Rezepte, Historie, Regale, Anzeigename)'),
    ('(Etikett scannen, Wein nachschlagen)', '(Etikett scannen, Gin nachschlagen)'),
    ('„Wein nachschlagen"', '„Gin nachschlagen"'),
    ('<strong>eingegebene Weinname</strong>', '<strong>eingegebene Gin-Name</strong>'),
    ('um Weindaten zu erkennen und zu ergänzen', 'um Gin-Daten zu erkennen und zu ergänzen und passende Tonic Waters, Kräuter und Rezepte zu empfehlen'),
    ('um Name und Marke des Weins zu finden', 'um Name und Marke des Gins zu finden'),
    ('Im Kellerplan und in der Weinliste werden gezeichnete Flaschen angezeigt. Gibst du selbst eine Bild-Adresse bei einem Wein ein', 'Im Barplan und in der Gin-Liste werden gezeichnete Flaschen angezeigt. Gibst du selbst eine Bild-Adresse bei einem Gin ein'),
    ('Die Region eines Weins (Karte) und das Traubensymbol (Wikipedia)', 'Die Region eines Gins (Karte) und das Wacholderbeeren-Symbol (Wikipedia), ebenso „Glas ansehen" (Bildersuche)'),
]
for a, b in pairs_d:
    assert d.count(a) >= 1, a
    d = d.replace(a, b)
open(D, 'w', encoding='utf-8', newline='').write(d)

s = open(S, encoding='utf-8').read()
pairs_s = [
    ('Stand / Updated: 25. Oktober 2026', 'Stand / Updated: 15. November 2026'),
    ('Meine Weine sind weg – was kann ich tun?', 'Meine Gins sind weg – was kann ich tun?'),
    ('Deine Weine liegen lokal auf deinem Gerät', 'Deine Gins liegen lokal auf deinem Gerät'),
    ('Wer den Code kennt, kann deine Weine sehen', 'Wer den Code kennt, kann deine Gins sehen'),
    ('Etikett scannen und Wein nachschlagen nutzen eine KI', 'Etikett scannen, Gin nachschlagen, Perfect Serve und Rezepte per KI nutzen eine KI'),
    ('Foto bzw. Weinname zur Auswertung', 'Foto bzw. Gin-Name zur Auswertung'),
    ('<strong>My wines are gone.</strong> Your wines are stored on your device.', '<strong>My gins are gone.</strong> Your gins are stored on your device.'),
    ('Label scan and wine lookup use an AI service.', 'Label scan, gin lookup, perfect serve and recipes use an AI service.'),
]
for a, b in pairs_s:
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
open(S, 'w', encoding='utf-8', newline='').write(s)

for name, txt in (('datenschutz', d), ('support', s)):
    left = [m.group(0) for m in re.finditer(r'.{25}(?:[Ww]ein|[Ww]ine|Vivino|Keller|[Cc]ellar|Trauben|[Gg]rape|Rebsort).{25}', txt)]
    print(name, 'Reste:', left)
