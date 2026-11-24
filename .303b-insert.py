import io, sys

def append_section(path, adds_path):
    adds = open(adds_path, encoding='utf-8').read().rstrip('\n')
    t = open(path, encoding='utf-8').read().rstrip('\n')
    assert adds[:60] not in t, 'already appended: ' + path
    open(path, 'w', encoding='utf-8').write(t + '\n\n' + adds + '\n')
    print('appended', path)

# ---------- docs/sources/gov/GOV-080.md (frontmatter + append) ----------
p = 'docs/sources/gov/GOV-080.md'
t = open(p, encoding='utf-8').read()
old = 'status: スニペット確認'
assert t.count(old) == 1, 'GOV-080 status anchor error'
t = t.replace(old, 'status: 直接確認（2026-11-12スニペット。2026-11-24第303回補遺: Accept-Language: ja付きcurlで本文全文取得・施設数値（開園平成元年4月・面積546.59平方メートル・要町3-17-5）確定）')
old = 'tags: [千川親水公園, 千川上水, 豊島区, 千川児童遊園, 暗渠管, 平成元年, 水流復活]'
assert t.count(old) == 1, 'GOV-080 tags anchor error'
t = t.replace(old, 'tags: [千川親水公園, 千川上水, 豊島区, 千川児童遊園, 暗渠管, 平成元年, 水流復活, 開園, 平成元年4月, 要町3-17-5, 546.59平方メートル, 千川駅, 造景, 第303回]')
open(p, 'w', encoding='utf-8').write(t)
append_section(p, '.303b-adds-gov080.md')

# ---------- docs/sources/gov/GOV-156.md (append) ----------
append_section('docs/sources/gov/GOV-156.md', '.303b-adds-gov156.md')

# ---------- 第303回ノート (append) ----------
append_section('docs/2026-11-24（第303回）・千川上水整備基本計画別冊14157-2〜7の完全取得と橋名群の抽出・速記録四河川走査陰性確定.md', '.303b-adds-note.md')

# ---------- docs/sources/INDEX.md: GOV-080行の確認区分・内容更新 ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
old = '- [GOV-080](gov/GOV-080.md) — 豊島区「千川親水公園」施設案内（平成元年水流復活・暗渠管内流下・旧千川児童遊園の一部・都借地） ／ 旧番号: — ／ スニペット確認（ai）'
assert idx.count(old) == 1, 'INDEX GOV-080 anchor error'
new = '- [GOV-080](gov/GOV-080.md) — 豊島区「千川親水公園」施設案内（開園平成元年4月・面積546.59平方メートル・要町3-17-5・平成元年水流復活・暗渠管内流下・園内表面流は「造られた」造景・旧千川児童遊園の一部から転用・都借地） ／ 旧番号: — ／ 直接確認（ai）'
idx = idx.replace(old, new)
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md: 第303回bullet末尾に補遺文言を挿入 ----------
readme = open('README.md', encoding='utf-8').read()
anchor = '。詳細は[第303回ノート]'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
assert '同日補遺' not in readme, 'README already patched'
ins = '＋同日補遺: [GOV-080](docs/sources/gov/GOV-080.md)（千川親水公園）を直接確認に格上げ（**開園＝平成元年4月・面積546.59平方メートル・要町3-17-5・最寄駅千川駅**・「**ほとんど全域に流れが造られ**」＝園内の表面流は「造られた」造景で実流は暗渠管側であることを区側本文が示唆・旧千川児童遊園から「生まれ変わりました」の転用文言全文確認・豊島区公式頁は**Accept-Language: ja付きcurlで200応答する処方を確立**＝第24回以来の遮断を解消）＋[GOV-156](docs/sources/gov/GOV-156.md)にtopics頁「井戸地下室調査について」（2017・豊玉立坑のニューマチックケーソン工事で**酸素欠乏症等防止規則による半径1km圏内の井戸・地下室調査が義務**の告知）を追記'
readme = readme.replace(anchor, ins + anchor)
open('README.md', 'w', encoding='utf-8').write(readme)
print('README patched')
