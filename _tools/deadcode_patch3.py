import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/Gin-Factory/index.html'
s = open(P, encoding='utf-8').read()
size0 = len(s.encode('utf-8'))


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, count, a[:100])
    s = s.replace(a, b)


# CSS der Vivino-Flaschenfotos
for pat in [r'^\.bottle-photo \{[^\n]*\n', r'^\.bottle-photo img \{[^\n]*\n', r'^\.bottle-year \{[^\n]*\n', r'^\.bottle-cap \{[^\n]*\n',
            r'^\.bottle-cap strong \{[^\n]*\n', r'^\.bottle-cap span \{[^\n]*\n']:
    s, n = re.subn(pat, '', s, flags=re.M)
    assert n == 1, (pat, n)
rep('.rack-preview > svg, .rack-preview > .bottle-photo {', '.rack-preview > svg {')

# verwaiste i18n-Schluessel (nirgends per t('..') / data-i18n referenziert; dynamisch nur 'occ_')
UNUSED = ('credits_topup_soon nav_ripe ripe_title ripe_sub sort_ripeness ripe_empty seg_young seg_optimal seg_peak seg_over st_wait1 st_wait st_optimal st_peak '
          'st_over1 st_over toast_enrich_prog l_from l_to toast_label_ripe drinkrule_btn drinkrule_desc drinkrule_confirm drinkrule_done confirm_enrich_temp '
          'cur_auto_kept setup_tempunit l_temp_from l_temp_to enrich_img_fail rack_add_level rack_blink_hint rack_blink_lbl rack_blink_first barcode_notfound '
          'barcode_notwine confirm_last').split()
L = s.split('\n')
i0 = next(i for i, l in enumerate(L) if l.startswith('const I18N = {'))
j0 = next(i for i in range(i0, len(L)) if L[i] == '};')
# Sicherheit: nach den bisherigen Entfernungen darf ausserhalb des I18N-Blocks keiner der Schluessel mehr vorkommen
rest = '\n'.join(L[:i0] + L[j0 + 1:])
for k in UNUSED:
    assert not re.search(r'(?<![A-Za-z0-9_])' + re.escape(k) + r'(?![A-Za-z0-9_])', rest), k
keyset = set(UNUSED)
removed = 0
new = []
for i, l in enumerate(L):
    if i0 <= i <= j0:
        m = re.match(r'^\s+([a-z_0-9]+): ', l)
        if m and m.group(1) in keyset:
            removed += 1
            continue
    new.append(l)
s = '\n'.join(new)
print('i18n-Zeilen entfernt:', removed, '(Schluessel', len(UNUSED), 'x Sprachbloecke)')
open(P, 'w', encoding='utf-8', newline='').write(s)
print('Bytes weniger:', size0 - len(s.encode('utf-8')))
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)
