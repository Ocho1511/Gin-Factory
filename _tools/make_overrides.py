"""Erzeugt i18n/i18n_overrides_gin.json (Wein-Reste -> Gin). merge_i18n.py wendet die Datei nach dem Zusammenfuehren an."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
D = 'C:/wk/Gin-Factory/_tools/i18n/'
ov = {}


def put(c, k, v):
    ov.setdefault(c, {})[k] = v


SYNC = {
    'sv': 'Din synkkod för Gin-Factory (förvara den säkert):',
    'da': 'Din synk-kode til Gin-Factory (opbevar den sikkert):',
    'fi': 'Gin-Factory-synkronointikoodisi (säilytä turvassa):',
    'ru': 'Ваш код синхронизации Gin-Factory (храните в надёжном месте):',
    'it': 'Il tuo codice di sync di Gin-Factory (conservalo al sicuro):',
    'fr': 'Votre code de sync Gin-Factory (conservez-le en lieu sûr) :',
    'pl': 'Twój kod synchronizacji Gin-Factory (przechowuj go bezpiecznie):',
    'hu': 'A Gin-Factory szinkronkódod (őrizd meg biztonságosan):',
    'cs': 'Váš synchronizační kód Gin-Factory (uchovejte jej v bezpečí):',
    'sk': 'Váš synchronizačný kód Gin-Factory (uchovajte ho v bezpečí):',
    'ro': 'Codul tău de sincronizare Gin-Factory (păstrează-l în siguranță):',
    'hr': 'Vaš kôd za sinkronizaciju Gin-Factory (čuvajte ga na sigurnom):',
    'pt': 'O seu código de sincronização do Gin-Factory (guarde-o em segurança):',
    'no': 'Din synk-kode for Gin-Factory (oppbevar den trygt):',
    'nl': 'Jouw synccode voor Gin-Factory (bewaar hem veilig):',
    'hi': 'आपका Gin-Factory सिंक कोड (कृपया इसे सुरक्षित रखें):',
}
NOM = {
    'de': 'Keine Gins für diese Filter.', 'en': 'No gins match these filters.',
    'es': 'Ninguna ginebra coincide con estos filtros.', 'sv': 'Inga ginsorter matchar filtren.',
    'da': 'Ingen gin matcher disse filtre.', 'fi': 'Ei ginejä näillä suodattimilla.',
    'ru': 'Нет джинов по этим фильтрам.', 'it': 'Nessun gin corrisponde a questi filtri.',
    'fr': 'Aucun gin ne correspond à ces filtres.', 'pl': 'Brak ginów dla tych filtrów.',
    'hu': 'Nincs a szűrőknek megfelelő gin.', 'cs': 'Žádné giny neodpovídají filtrům.',
    'sk': 'Žiadne giny nezodpovedajú filtrom.', 'ro': 'Niciun gin nu corespunde acestor filtre.',
    'hr': 'Nema ginova za ove filtre.', 'pt': 'Nenhum gin corresponde a estes filtros.',
    'no': 'Ingen gin matcher disse filtrene.', 'nl': 'Geen gins voor deze filters.',
    'el': 'Κανένα τζιν δεν ταιριάζει με αυτά τα φίλτρα.', 'uk': 'Немає джинів за цими фільтрами.',
    'ja': 'この条件に一致するジンはありません。', 'ko': '이 필터에 맞는 진이 없어요.',
    'zh': '没有符合这些筛选条件的金酒。', 'hi': 'इन फ़िल्टर से कोई जिन मेल नहीं खाती।',
}
OWN = {
    'es': 'Déjalo vacío para el título estándar. Nombre → "Gin-Factory de Nombre".',
    'sv': 'Lämna tomt för standardtiteln. Namn → „Namns Gin-Factory".',
    'da': 'Lad være tom for standardtitlen. Navn → „Navns Gin-Factory".',
    'fi': 'Jätä tyhjäksi oletusotsikkoa varten. Nimi → „Nimen Gin-Factory".',
    'ru': 'Оставьте пустым для стандартного заголовка. Имя → „Gin-Factory: Имя".',
    'it': 'Lascia vuoto per il titolo predefinito. Nome → „Gin-Factory di Nome".',
    'fr': 'Laissez vide pour le titre par défaut. Nom → « Gin-Factory de Nom ».',
    'pl': 'Pozostaw puste dla domyślnego tytułu. Nazwa → „Gin-Factory: Nazwa".',
    'hu': 'Hagyd üresen az alapértelmezett címhez. Név → „Név Gin-Factory-ja".',
    'cs': 'Nechte prázdné pro výchozí název. Jméno → „Gin-Factory: Jméno".',
    'sk': 'Nechajte prázdne pre predvolený názov. Meno → „Gin-Factory: Meno".',
    'ro': 'Lasă gol pentru titlul implicit. Nume → „Gin-Factory al lui Nume".',
    'hr': 'Ostavite prazno za zadani naslov. Ime → „Gin-Factory: Ime".',
    'pt': 'Deixe vazio para o título padrão. Nome → „Gin-Factory de Nome".',
    'no': 'La stå tomt for standardtittelen. Navn → „Navns Gin-Factory".',
    'nl': 'Laat leeg voor de standaardtitel. Naam → „Gin-Factory van Naam".',
    'el': 'Αφήστε κενό για τον προεπιλεγμένο τίτλο. Όνομα → "Gin-Factory: Όνομα".',
    'uk': "Залиште порожнім для стандартної назви. Ім'я → \"Gin-Factory: Ім'я\".",
    'ja': '空欄の場合は標準のタイトルになります。名前 → "名前のGin-Factory"。',
    'ko': '비워 두면 기본 제목이 표시돼요. 이름 → "이름의 Gin-Factory".',
    'zh': '留空则使用默认标题。名称 → "名称的Gin-Factory"。',
    'hi': 'डिफ़ॉल्ट शीर्षक के लिए खाली छोड़ें। नाम → "नाम की Gin-Factory"।',
}
for c, v in SYNC.items():
    put(c, 'sync_email_body_1', v)
for c, v in NOM.items():
    put(c, 'ripe_nomatch', v)
for c, v in OWN.items():
    put(c, 'setup_owner_desc', v)
put('fi', 'shelf_how_many', 'Kuinka monta pulloa ginia ”{name}” varastoidaan?')
put('ko', 'toast_rack_removed', '"{name}" 진을 칸에서 제거했어요 ✓')
json.dump(ov, open(D + 'i18n_overrides_gin.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({c: len(v) for c, v in ov.items()})
