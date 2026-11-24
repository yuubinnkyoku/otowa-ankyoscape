import io, sys

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_gov576 = '- [GOV-576](gov/GOV-576.md) '
assert idx.count(a_gov576) == 1, 'GOV-576 anchor count error'
assert '[GOV-577](gov/GOV-577.md)' not in idx, 'GOV-577 already present'

gov577 = '- [GOV-577](gov/GOV-577.md) — 東京都議会環境・建設委員会速記録第十三号（平成26年11月13日・第九委員会室）— 千川上水の河野（ゆう）委員×中島河川部長問答の一次原文（BLOG-312引用の全文一致を検証）＝法定外公共物・伊勢橋から下流暗渠約15kmを都が使用許可・維持管理・平成17年度老朽化調査→損傷・土砂堆積→補修→平成22年通水停止・平成18年開渠約5kmの区市財産譲与・清流復活支援と通水可能性の継続調査検討＋「千川上水」と銘記されたマンホールが大山周辺に「まだある」（河野委員2014年観察・repo初出文言候補）・大山駅周辺まちづくりマスタープラン言及・補助229号線＝千川通りが千川上水緑道と並行の幅員5.5m狭隘路で2013年10月緑道一体歩道整備（用地97%・430m）＋環七地下調節池×白子川地下調節池を内径12.5m・延長約5.5km・貯留約68万m³トンネルで連結する2014年時点初期スペック（神田川・石神井川・白子川の3流域融通・時間100mm対応）・境川河川整備計画原案（2014年9月）の都管理区間76万立米調節池・白子川地下調節池H21事業再開→3.2kmシールド2014年1月完了→H26年度末暫定取水→H28年度末完成 ／ 旧番号: — ／ 原文一次確認（速記録全文86,954字をr.jna.ai経由で取得・2026-11-24）（ai）'.replace('r.jna.ai', 'r.jina.ai')

i = idx.index(a_gov576)
end = idx.index('\n', i) + 1
idx = idx[:end] + gov577 + '\n' + idx[end:]

old = '## 行政・公的機関（574件）'
assert idx.count(old) == 1, 'gov section header count error'
idx = idx.replace(old, '## 行政・公的機関（575件）')
old = '資料ファイル総数: 1745件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1746件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.302-bullet.txt', encoding='utf-8').read()
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第301回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
