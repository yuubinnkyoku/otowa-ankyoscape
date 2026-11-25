#!/usr/bin/env python3
# 第314回bot用: README.mdの「- **第313回:**」行の直後に .314-bullet.txt の1行を挿入し、
# docs/sources/INDEX.md にGOV-590・ORG-050行を挿入して計数を更新する。
# 冪等: READMEに既に「第314回:」の行がある場合は何もしない。
# アンカー不在・計数不整合の場合は非ゼロ終了（失敗を可視化し、クリーンアップは行わない）。
import io, sys

README = 'README.md'
INDEX = 'docs/sources/INDEX.md'
BULLET = '.314-bullet.txt'

GOV_LINE = '- [GOV-590](gov/GOV-590.md) — 江戸東京博物館収蔵・小林源次郎撮影の千川上水関係スライド・写真群（12点・jpsearch掃引で発見・ToMuCo詳細頁全件確認）— 「野川・仙川・千川 上水スライド 千川上水」8点〔96651004〜96651011・1970年=昭和45年・ポジ・静止画フィルム・うち1点「柳橋辺り」＝1971年通水終了直前の本流景観〕＋「玉川上水スライド 千川上水取入口」3点〔96651151〜53・2点は昭和43年3月=1968年・1点は昭和30〜50年代〕＋「玉川上水写真 流水なき千川上水路」〔96651181・ステレオ写真・備考「昭和50年前半」＝断流後の無流水の水路を伝えるrepo初出の写真記録候補〕〔江戸博デジタルアーカイブズ対応詳細頁237755〜762・237902〜904・237932併記〕 ／ 旧番号: — ／ 書誌確認（収蔵品目録メタデータ・画像内容は未確認）（ai）'
ORG_LINE = '- [ORG-050](org/ORG-050.md) — 日本写真保存センター「写真原板データベース」の千川上水木樋断片写真（1点・jpsearch API経由で所在のみ収録）— 標題「〔左〕千川上水の末流を妙（抄）紙部構内へ引くために用いられた木樋の断片　王子駅付近で発掘された　大蔵省印刷局王子工場蔵」（レコードID 00076-00077-0004）＝千川上水末端を抄紙部（王子）へ引いた木樋の発掘遺物の写真記録の存在を示す（photo-archive.jpは2026-11-25時点で接続不能・jpsearch収録メタデータが唯一の根拠・復旧後に本文確認＝木樋による江戸市中送水と印刷局抄紙部給水を結ぶ末端構造物の物的資料候補） ／ 旧番号: — ／ 所在のみ（jpsearchメタデータ・写真実体は未確認）（ai）'

t = io.open(README, encoding='utf-8').read()
if any(l.startswith('- **第314回:') for l in t.split('\n')):
    print('README already has round-314 bullet; skip insertion')
    sys.exit(0)
if not any(l.startswith('- **第313回:') for l in t.split('\n')):
    sys.exit('README anchor line "- **第313回:" not found; abort')

idx = io.open(INDEX, encoding='utf-8').read()
def must_one(s, label):
    c = idx.count(s)
    if c != 1:
        sys.exit('INDEX assertion failed for %s (count=%d); abort' % (label, c))
must_one('- [GOV-589](gov/GOV-589.md)', 'GOV-589 row')
must_one('- [ORG-049](org/ORG-049.md)', 'ORG-049 row')
must_one('## 行政・公的機関（587件）', 'gov header 587')
must_one('## 企業・団体の公式発表（49件）', 'org header 49')
must_one('資料ファイル総数: 1805件', 'total 1805')
if '- [GOV-590](gov/GOV-590.md)' in idx or '- [ORG-050](org/ORG-050.md)' in idx:
    sys.exit('INDEX already has GOV-590/ORG-050; abort')

lines = idx.split('\n')
out = []
for l in lines:
    out.append(l)
    if l.startswith('- [GOV-589](gov/GOV-589.md)'):
        out.append(GOV_LINE)
    elif l.startswith('- [ORG-049](org/ORG-049.md)'):
        out.append(ORG_LINE)
idx2 = '\n'.join(out)
idx2 = idx2.replace('## 行政・公的機関（587件）', '## 行政・公的機関（588件）')
idx2 = idx2.replace('## 企業・団体の公式発表（49件）', '## 企業・団体の公式発表（50件）')
idx2 = idx2.replace('資料ファイル総数: 1805件', '資料ファイル総数: 1807件')
io.open(INDEX, 'w', encoding='utf-8', newline='').write(idx2)

b = io.open(BULLET, encoding='utf-8').read().rstrip('\n').rstrip('\r')
lines = t.split('\n')
for i, l in enumerate(lines):
    if l.startswith('- **第313回:'):
        lines.insert(i + 1, b)
        break
io.open(README, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('inserted round-314 bullet after round-313 line + INDEX rows/counts updated')
