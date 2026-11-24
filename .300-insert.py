import io, sys

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_pap113 = '- [PAP-113](papers/PAP-113.md) '
assert idx.count(a_pap113) == 1, 'PAP-113 anchor count error'
assert '[PAP-114](papers/PAP-114.md)' not in idx, 'PAP-114 already present'

pap114 = '- [PAP-114](papers/PAP-114.md) — テイケイトレード株式会社埋蔵文化財事業部編集『柳沢家駒込屋敷(六義館・六義園)跡第2地点 : ハイツ駒込マンション建替事業に伴う埋蔵文化財発掘調査報告書 : 東京都文京区』（ハイツ駒込マンション建替組合発行・2013年刊・NCID BB13461197・CiNii ownerCount14）— 第1〜4地点で唯一未確定だった第2地点の書誌＝29p＋図版2pのシリーズ内最薄体裁・建替組合負担による発掘という調査資金枠組みの記録（第1地点〔B-117・丸紅・2012-12-28〕・第3地点〔B-135・東急不動産・2014-08-31〕・第4地点〔B-178・2020〕と合わせ4地点の受託者・発行者・刊行年が全て確定・所在地・遺構欄は書誌に含まれず・上水文言は本文未見のため記載せず・総覧レコードはID 81312消滅のまま未特定） ／ 旧番号: — ／ 所在のみ（CiNii Books書誌JSONを直接確認・2026-11-24）（ai）'

i = idx.index(a_pap113)
end = idx.index('\n', i) + 1
idx = idx[:end] + pap114 + '\n' + idx[end:]

old = '## 論文・研究報告・データ（111件）'
assert idx.count(old) == 1, 'papers section header count error'
idx = idx.replace(old, '## 論文・研究報告・データ（112件）')
old = '資料ファイル総数: 1735件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1736件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.300-bullet.txt', encoding='utf-8').read()
if not bullet.endswith('\n'):
    bullet += '\n'
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第299回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
