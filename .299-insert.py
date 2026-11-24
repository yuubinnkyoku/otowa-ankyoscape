import io, sys

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_pap111 = '- [PAP-111](papers/PAP-111.md) '
assert idx.count(a_pap111) == 1, 'PAP-111 anchor count error'
assert '[PAP-112](papers/PAP-112.md)' not in idx, 'PAP-112 already present'
assert '[PAP-113](papers/PAP-113.md)' not in idx, 'PAP-113 already present'

pap112 = '- [PAP-112](papers/PAP-112.md) — 大成エンジニアリング『柳沢家駒込屋敷（六義館・六義園）跡』（B-117・丸紅株式会社発行・2012-12-28刊・NCID BB18778816・NDL〔JP〕22582261・全国遺跡報告総覧88646）— シリーズ番号最小・発行年最早（2011.11〜2012.12調査）から第1回調査〔第1地点〕に相当と解される報告書：前田家下屋敷→元禄8(1695)柳沢吉保45,862坪拝領→元文4(1739)南東側上地・田安宗武拝領→御駕籠之者大繩地→岩崎弥太郎購入の屋敷変遷と、54・55号堀溝（18世紀前葉比定＝前田家/柳沢家所産推定）・28号区画溝（延享4年頃の大繩地区画溝推定）＝溝跡3・地下室4・土坑19・植栽痕22等・遺物総数7,538点の遺構群（本駒込6-373番地・190㎡・上水関連文言なし＝陰性） ／ 旧番号: — ／ 所在のみ（総覧レコードの遺構欄・要約本文を直接確認・2026-11-24・報告書本文は総覧にPDF登載なし）（ai）'
pap113 = '- [PAP-113](papers/PAP-113.md) — 大成エンジニアリング『柳沢家駒込屋敷（六義館・六義園）跡第3地点』（B-135・東急不動産発行・2014-08-31刊・NCID BB2091060X・全国遺跡報告総覧48073・総覧抄録91937）— 『寛永江戸全図』の鳥居淡路下屋敷→明暦大火後前田家中屋敷（天和3=1683上地）→柳沢家下屋敷（元禄8=1695）→元文4(1739)南側二万坪上地・田安家拝領→延享4(1747)御駕籠之者大繩地の屋敷変遷に加え、屋敷境界の溝・道路状遺構（溝8・道路5）の検出と本郷台地東端の埋没谷・北東から南西に傾斜する谷地形の一次記述（本駒込6-13-21・200㎡・上水関連文言なし＝陰性） ／ 旧番号: — ／ 所在のみ（総覧レコード・抄録の遺構欄・要約本文を直接確認・2026-11-24・報告書本文は総覧にPDF登載なし）（ai）'

i = idx.index(a_pap111)
end = idx.index('\n', i) + 1
idx = idx[:end] + pap112 + '\n' + pap113 + '\n' + idx[end:]

old = '## 論文・研究報告・データ（109件）'
assert idx.count(old) == 1, 'papers section header count error'
idx = idx.replace(old, '## 論文・研究報告・データ（111件）')
old = '資料ファイル総数: 1733件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1735件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.299-bullet.txt', encoding='utf-8').read()
if not bullet.endswith('\n'):
    bullet += '\n'
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第298回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
