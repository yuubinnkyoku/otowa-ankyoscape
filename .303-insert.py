import io, sys

def append_section(path, adds_path):
    adds = open(adds_path, encoding='utf-8').read().rstrip('\n')
    t = open(path, encoding='utf-8').read().rstrip('\n')
    assert adds[:30] not in t, 'already appended: ' + path
    open(path, 'w', encoding='utf-8').write(t + '\n\n' + adds + '\n')
    print('appended', path)

# ---------- docs/sources/gov/GOV-084.md (frontmatter + append) ----------
p = 'docs/sources/gov/GOV-084.md'
t = open(p, encoding='utf-8').read()
old = 'tags: [武蔵野市, 千川上水, 清流復活, 管理移譲, 境橋, 吉祥寺橋, 護岸, 橋, 都市公園, 資料編, Wayback, 第301回]'
assert t.count(old) == 1, 'GOV-084 tags anchor error'
t = t.replace(old, 'tags: [武蔵野市, 千川上水, 清流復活, 管理移譲, 境橋, 吉祥寺橋, 護岸, 橋, 都市公園, 資料編, Wayback, 第301回, 第303回]')
old = 'status: 直接確認（2026-11-12、公式PDF全文〔テキスト取得範囲〕。2026-11-24第301回追記:「別冊」資料編の所在を特定しかし本文抽出は不能）'
assert t.count(old) == 1, 'GOV-084 status anchor error'
t = t.replace(old, 'status: 直接確認（2026-11-12、公式PDF全文〔テキスト取得範囲〕。2026-11-24第301回追記:「別冊」資料編の所在を特定しかし本文抽出は不能。第303回追記: 別冊14157-2〜7の完全取得・本文抽出に成功してGOV-578に資料化）')
open(p, 'w', encoding='utf-8').write(t)
append_section(p, '.303-adds-gov084.md')

# ---------- docs/sources/gov/GOV-577.md (frontmatter + append) ----------
p = 'docs/sources/gov/GOV-577.md'
t = open(p, encoding='utf-8').read()
old = ', 第302回]'
assert t.count(old) == 1, 'GOV-577 tags anchor error'
t = t.replace(old, ', 第302回, 第303回]')
old = 'status: 原文一次確認（速記録全文86,954字をr.jna.ai経由で取得して2026-11-24に確認・BLOG-312引用文言との全文一致を検証済み・gikaiへの直接curlはWAF 403）'.replace('r.jna.ai', 'r.jina.ai')
assert t.count(old) == 1, 'GOV-577 status anchor error'
t = t.replace(old, 'status: 原文一次確認（速記録全文86,954字をr.jina.ai経由で取得して2026-11-24に確認・BLOG-312引用文言との全文一致を検証済み・gikaiへの直接curlはWAF 403。第303回: 全文の四河川走査を実施）')
open(p, 'w', encoding='utf-8').write(t)
append_section(p, '.303-adds-gov577.md')

# ---------- docs/sources/gov/GOV-156.md (append) ----------
append_section('docs/sources/gov/GOV-156.md', '.303-adds-gov156.md')

# ---------- docs/四河川の橋名・橋跡調査.md (append) ----------
append_section('docs/四河川の橋名・橋跡調査.md', '.303-adds-bridges.md')

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_gov577 = '- [GOV-577](gov/GOV-577.md) '
assert idx.count(a_gov577) == 1, 'GOV-577 anchor count error'
assert '[GOV-578](gov/GOV-578.md)' not in idx, 'GOV-578 already present'

gov578 = '- [GOV-578](gov/GOV-578.md) — 武蔵野市「千川上水整備基本計画」別冊群（14157-2〜7.pdf・平成22年5月）— ①第5章土地利用計画（表5-1ゾーニング・図5-1〜12区間①〜③走査図1:1000・コイの侵入防止柵〔小魚だけが通り抜けられる隙間〕・供養塔周辺の環境整備エリア）②第6章整備の優先順位と施設デザイン（区間②優先・都市公園区間＝総合的モデル整備区間・区間③は都市計画道路3-1-12号線の区域内＝関連機関と協議・調整・サイン19種60基・ベンチ31基〔本編の19種61基・ベンチ35基と食い違い〕・表6-1/6-2）③施設配置計画図（1:1000）の橋名ラベル群＝ほたる橋・鎮守橋・よしくぼ橋〔かな表記〕・三郡橋・西窪橋（repo初出橋名候補）＋樋口橋・柳橋・庚申橋・千川橋・関前橋・千川小学校前・武蔵野大学前・電通研究所前・更新橋・北裏橋・桂橋・東北裏橋・吉祥寺橋＋「既設供養塔（石橋供養塔）」ラベル＋施設名石「千川上水清流の復活」「千川上水遊歩道」 ④概要版（基本方針遊・景・生・代表断面流路幅1.5m水深20cm/1.7m水深25cm・ミシシッピアカミミガメ文言） ⑤「意見への対応」9項目（屋敷林〔八幡町3丁目・関前南4・3丁目・北町5・3丁目〕・武蔵野自然観察園・NTT社宅跡地の境界林を文言として記載・区間③都市計画道路区域内の対応） ／ 旧番号: — ／ 直接確認（Wayback 20221228224110id_スナップショット6冊PDFの完全取得・自作抽出器〔FlateDecode＋ToUnicode〕による本文抽出・2026-11-24）（ai）'

i = idx.index(a_gov577)
end = idx.index('\n', i) + 1
idx = idx[:end] + gov578 + '\n' + idx[end:]

old = '## 行政・公的機関（575件）'
assert idx.count(old) == 1, 'gov section header count error'
idx = idx.replace(old, '## 行政・公的機関（576件）')
old = '資料ファイル総数: 1746件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1747件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.303-bullet.txt', encoding='utf-8').read()
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第302回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
