#!/usr/bin/env python3
# 第307回: INDEX行挿入（GOV-579〜581）とREADME bullet挿入。実行後に自己削除。
import io, os, sys

ROOT = os.environ.get('GITHUB_WORKSPACE', '.')

def die(msg):
    print('ASSERT FAIL:', msg)
    sys.exit(1)

def read(p):
    return io.open(p, encoding='utf-8', newline='').read()

def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

# ---------- 1) INDEX.md ----------
ip = os.path.join(ROOT, 'docs/sources/INDEX.md')
s = read(ip)
for g in ('GOV-579', 'GOV-580', 'GOV-581'):
    if ('[%s]' % g) in s:
        die('%s already in INDEX' % g)
gov_rows = [l for l in s.split('\n') if l.startswith('- [GOV-578](gov/GOV-578.md)')]
if len(gov_rows) != 1:
    die('GOV-578 row count = %d' % len(gov_rows))
sec_old = '## 行政・公的機関（576件）'
sec_new = '## 行政・公的機関（579件）'
if s.count(sec_old) != 1:
    die('gov section header count = %d' % s.count(sec_old))
tot_old = '資料ファイル総数: 1774件 / 旧番号対応: 70件'
tot_new = '資料ファイル総数: 1777件 / 旧番号対応: 70件'
if s.count(tot_old) != 1:
    die('total line count = %d' % s.count(tot_old))

rows = [
 '- [GOV-579](gov/GOV-579.md) — 東京都公文書館・千川上水の公報掲載記録と昭和実務文書（1927〜1951・11件）— 警視庁東京府告示340号（1927・千川上水管理）・東京都告示275号（1943・板橋区長への管理者指定）・東京都告示1199号（1951・管理者指定廃止）・東京市告示188号の公報版（1940・千川上水公園新設及開園・公告5.9）・内田祥三関係資料の都市計画東京地方委員会資料（1942・保健防火道路第3号路線〔千川上水線〕計画平面図・谷田川ノ部負担区画図）・1929用途変更・1929改修板橋町・1935市道認定江古田・1936保谷臨時事業・1937道路供用石神井関町・中新井区画整理環状放射線設計変更 ／ 旧番号: — ／ 目録詳細確認（詳細頁・公報番号・MFコマまで・公報本文未見）（ai）',
 '- [GOV-580](gov/GOV-580.md) — 東京都公文書館・明治期の千川水道実務文書群（1880〜1894・43件詳細）— 地券交付（1881）・滝野川村畑持主の開設指示伺（1881）・下板橋宿外2ヶ村の変換（1884-85）・巣鴨村の地種組替（1886・字新田外6ヶ所・図面1葉添）・警視庁幅員図面照会・東京検疫局水切回答（1882）・博覧会照会2件（1880）・取締禁例改正の警視庁照会（1883）・印刷局鈔紙部減量の立会検査（1883）と王子工場減量（1888）・護岸橋梁修繕費用請求（1892）・黴毒病院の道路埋樋跡督促（1883）・本郷区・本所区真砂町引用群（1882・配水東端候補）・樋桝伏渡跡道路修繕（1882・駒込東片町〜湯島切通）・掛樋伺（1885）・統計院統計材料（1883・1885）・出桝敷借地料の府会諮問2件（1890）・消防分署構内の樋2件（1887・1891）・引用井3願（1888・山中サノ／帝国大学／二橋元長）・引入口差蓋修繕願（1894-98）＝GOV-572制限③の解消 ／ 旧番号: — ／ 目録詳細確認（詳細頁・請求番号・MFコマまで・本文未見）（ai）',
 '- [GOV-581](gov/GOV-581.md) — 東京都公文書館・谷端川改修受益者負担の公報掲載記録群（1936〜1938・9件）— 警視庁東京府公報の府告示321号（1936.5.9）・府令33号（1936.11.14・施行細則改正）・府告示768号（1936.11.28・神田上水第1負担区）・府告示802号（1936.12.10）・府告示328号公報版（1937.4.29・GOV-568④の公告日確定）・府告示431号（1937.6.8）・府告示449号（1937.6.17・第2負担区）・府令5号（1938.2.8）＋東京市告示678号（1938.12.10・西巣鴨町下水道谷端川・音羽・谷田川排水区の西巣鴨負担区決定）＝谷端川26件の掃引完結 ／ 旧番号: — ／ 目録詳細確認（詳細頁・公報番号・MFコマまで・公報本文未見）（ai）',
]
anch = gov_rows[0]
s = s.replace(anch, anch + '\n' + '\n'.join(rows), 1)
s = s.replace(sec_old, sec_new, 1)
s = s.replace(tot_old, tot_new, 1)
write(ip, s)
print('INDEX OK: +3 rows, 行政576→579, 総数1774→1777')

# ---------- 2) README.md ----------
rp = os.path.join(ROOT, 'README.md')
r = read(rp)
lines = r.split('\n')
if any(l.startswith('- **第307回:') for l in lines):
    die('bullet 第307回 already present')
bidx = [i for i, l in enumerate(lines) if l.startswith('- **第306回:')]
if len(bidx) != 1:
    die('README 第306回 anchor count = %d' % len(bidx))
bp = os.path.join(ROOT, '.307-bullet.txt')
bullet = read(bp).rstrip('\n')
if not bullet.startswith('- **第307回:'):
    die('bullet file malformed')
lines.insert(bidx[0] + 1, bullet)
write(rp, '\n'.join(lines))
print('README OK: bullet inserted after 第306回 line')

# ---------- 3) helpers の自己削除 ----------
for f in ('.307-bullet.txt', '.307-insert.py',
          os.path.join('.github', 'workflows', 'insert-307.yml')):
    fp = os.path.join(ROOT, f)
    if os.path.exists(fp):
        os.remove(fp)
        print('removed', f)
print('DONE')
