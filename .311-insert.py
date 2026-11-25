#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第311回: INDEX行挿入(3)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .311-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.311-bullet.txt')

GOV_LINES = [
 "- [GOV-584](gov/GOV-584.md) — 豊島区報道発表「11月29日にシンポジウム『種子屋街道の歴史を今に伝える地域に根差した種子屋の役割～これまでとこれから～』を開催！」（令和7年11月13日発信・ページID54722）— 第2回種子屋街道シンポジウム（R7.11.29・大正大学）の区側一次告知＝主催=榎本種苗歴史文化財団・共催=豊島区/大正大学/協同組合伝統技法研究会・後援4団体（巣鴨信金・日本農林社・日本種苗協会・住友林業＝第3回にあった種苗会館・東京種苗は後援に不在）・加藤祐子理事の「本シンポジウムで、その種を蒔きたい」コメント（BLOG-315「佑子」と表記対立）・種子屋街道の行政側定義注記「江戸時代から戦前までの期間、豊島区巣鴨から北区滝野川にかけての旧中山道沿いにあった多くの種子屋が軒を連ねた地域」（repo初出文言）・第2部=榎本家店舗（西巣鴨3-19-2）の文化財保存修理事業見学会（角野茂勝） ／ 旧番号: — ／ 直接確認（2026-11-25に区公式報道発表本文全文取得）（ai）",
 "- [GOV-585](gov/GOV-585.md) — 豊島区文化財ニュース第16号「榎本家店舗兼住宅および新座敷が豊島区有形文化財に指定されました」（ページID44399・更新日2023年6月8日）— 初代榎本留吉＝弘化元（1844）年に滝野川村（現北区）の種苗業3家の1軒から分家し巣鴨庚申塚で開業（BLOG-316「三軒家」地名由来説の行政側対応文言・各家の比定は本文未見のため行わず）・建築詳細（店舗=木造つし二階建て切妻造り切落桟瓦葺き＋北側住居=木造平屋建て寄棟造り・新座敷=木造二階建て入母屋造り引掛桟瓦葺き＋洋館付属・廊下で接合）・新座敷=四代留吉結婚を機に棟札から昭和11（1936）年竣工・店舗兼住宅=伝承と建築的特徴から明治40（1907）年頃推定・昭和20（1945）年4月13日空襲で奇跡的に焼失免除・所有=東京種苗株式会社・「西巣鴨地域の歴史を象徴する『種子屋通り』を偲ばせる建物」文言（建築史・土地利用系） ／ 旧番号: — ／ 直接確認（2026-11-25に区文化財ニュース本文全文取得）（ai）",
 "- [GOV-586](gov/GOV-586.md) — 東京都公文書館・クロス検索「中新井」685件の全走査（2026-11-25・GOV-580制限④の解消）— 千川関係の新規9件＝水車稼家取設願写（1874・深野惣左衛門・矢島弥平次）・堰板払除及堀浚方請書（1877・「水車人」文言がrepo grep新出）・千川水路土揚敷堀崩上申・土砂浚上申（1882・中新井村戸長・岩堀修照）・千川水道敷地修繕願（1883・中新井村2030番地深野惣左衛門）・溜井并砂利取場見分旅費（1884）・葭生地の用水敷等組替伺（1892・農商務大臣へ）・樹木払下並植付寄附【千川用水土場敷】現状図・予定図（1914・長崎・下練馬村）・上水道敷設事業準備の土地立入測量許可告示（1925・警視庁東京府公報・府告示331）＝明治10年代の中新井村側の千川水路の水車操業・維持実務の連続記録群（本文未見・目録詳細確認） ／ 旧番号: — ／ 目録詳細確認（詳細頁・請求番号・MFコマまで・本文未見）（ai）",
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## 行政・公的機関（581件）', 1, 'GOV見出し')
idx = idx.replace('## 行政・公的機関（581件）', '## 行政・公的機関（584件）')
assert_count(idx, '## 行政・公的機関（584件）', 1, 'GOV見出し置換後')

assert_count(idx, '資料ファイル総数: 1795件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1795件', '資料ファイル総数: 1798件')
assert_count(idx, '資料ファイル総数: 1798件', 1, '総数行置換後')

for t in ['[GOV-584]', '[GOV-585]', '[GOV-586]']:
    assert idx.count(t) == 0, f"ASSERT FAIL: 事前重複 {t}"

lines = idx.split('\n')
out = []
a_gov = '- [GOV-583](gov/GOV-583.md)'
n_gov = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_gov):
        out.extend(GOV_LINES); n_gov += 1
assert n_gov == 1, f"ASSERT FAIL: GOV-583アンカー {n_gov}件"
idx2 = '\n'.join(out)
for t, m in [('[GOV-584]', 1), ('[GOV-585]', 1), ('[GOV-586]', 1)]:
    assert idx2.count(t) == m, f"ASSERT FAIL: 挿入後 {t} count={idx2.count(t)}"
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第311回:'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第310回:') + rdm.startswith('- **第310回:') == 1, "ASSERT FAIL: 第310回アンカー"
assert rdm.count('- **第311回:') == 0, "ASSERT FAIL: 第311回bullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第310回:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第311回:') == 1
assert rdm2.count('\n- **第310回:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.311-bullet.txt', '.311-insert.py', '.github/workflows/insert-311.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-311 OK')
