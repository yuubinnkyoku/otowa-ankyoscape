#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第310回: INDEX行挿入(7)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .310-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.310-bullet.txt')

BLOG_LINES = [
 "- [BLOG-315](blogs/BLOG-315.md) — 大竹道茂「江戸東京野菜通信」R6.11.30第1回種子屋街道シンポジウム参加記（2024-12-04）— 五代目・榎本泰吉の2024年2月死去（96歳）と娘・加藤佑子の挨拶・「カネト商報」品種名（東京練馬中長丸尻大根10文字・東京大長練馬長尻澤庵大根12文字）・榎本家店舗の屋根保存修理の観察（街道面＝建設当時の古瓦・北面＝新瓦・沢潟家紋＋カネト社章の瓦・隣接駐車場＝種の取引記録を納めた石蔵跡）・渡邊正好（渡辺早生ゴボウ育種家・種子は東京種苗㈱で販売）と榎本泰吉の交友証言・種子地蔵前の見学会待機（山本洋空の滝野川ゴボウ栽培地案内） ／ 旧番号: — ／ 直接確認（2026-11-25に本文全文取得〔頁はShift_JIS〕）（ai）",
 "- [BLOG-316](blogs/BLOG-316.md) — 成島哲子「種子(たね)屋街道」（takitan.com固定頁・2025-04-18・初出＝雑誌「月虹」2025年6月終刊号の転載）— 江戸期の滝野川種子屋元祖三家＝枡屋（榎本）孫八・越部半右衛門・榎本重左衛門＝「三軒家」地名由来説（repo初出・由来語りとして対校対象）・大正5年東京種子同業組合設立→戦時種苗統制で昭和18年解散（同初出）・平成3年種子蔵解体時の豊島区立郷土資料館への寄贈→友の会古文書サークル有志5名が30年かけR3.3に約6万4千点の整理完了→R4.12.1一般財団法人榎本種苗歴史文化財団設立（整理の点数・人員・年次は初出）・「種子屋街道」の命名は大正大学「よみがえれ『種子屋街道』」プロジェクト〔聞き書き文言〕 ／ 旧番号: — ／ 直接確認（2026-11-25に本文全文取得）（ai）",
 "- [BLOG-317](blogs/BLOG-317.md) — NPO いけぶくろねっと告知「種子屋街道の歴史…大正大学 11月29日」（2026-11-04投稿）— 第2回シンポジウム＝R7.11.29説の根拠告知（豊島区広報r0711/2511131356〔R7.11.13〕のURL引用）・テーマ「種子屋街道の歴史を今に伝える地域に根差した種子屋の役割〜これまでとこれから〜」・報告者＝横山恵美・近藤友宏・吉田尚也（PR TIMES〔GOV-583〕の「古田尚也」と表記対立）・討議＝政金裕太・見学会＝角野茂勝・投稿日と内容年度の不整合は観察記録・区広報・区文化財頁（2305161242）のURL群 ／ 旧番号: — ／ 直接確認（2026-11-25に本文全文取得）（ai）"
]

ORG_LINES = [
 "- [ORG-046](org/ORG-046.md) — 大正大学プレスリリース「よみがえれ！！伝統野菜で地域活性 巣鴨の地、『種子屋（たねや）街道』としての歴史紹介！！」（2022-03-31）— 種子屋街道紹介看板5枚を南門広場中心に設置（監修＝松本洋幸准教授）＝BLOG-315「説明案内板2022年3月設置」の大学側原本・観光庁「地域の観光資源の磨き上げを通じた域内連携促進に向けた実証事業」・（公社）農林水産・食品産業技術振興協会「種苗資源の保護に係る取組み支援事業」等の事業名（repo初出） ／ 旧番号: — ／ 直接確認（2026-11-25に本文取得）（ai）",
 "- [ORG-047](org/ORG-047.md) — 大正大学地域構想研究所レポート 齋藤知明「中山道の歴史を掘り起こし、新しく『種子地蔵縁日』開催」（2022-11-01）— 種子地蔵＝大正大学が2022年5月に南門へ建立（21世紀の新造構築物・「参拝のしおり」植木鉢文言「種子屋通りの歴史を顕彰」＋一粒万倍＝PAP-027の構築物調査と接続候補）・第1回種子地蔵縁日＝2022-11-04（マーケット「種子屋街道さんぽ市」）・稲荷湯×長屋カフェ（同年6月リノベ）プレイベント ／ 旧番号: — ／ 直接確認（2026-11-25に本文取得）（ai）",
 "- [ORG-048](org/ORG-048.md) — 同レポート 齋藤知明「地域の歴史を価値あるものに変えること」（2024-04-01）— 第2回種子地蔵縁日＝2023-11-11・2021年12月プレイベント「種子屋街道さんぽ市」＝種子屋街道系イベントの初回年次文言・観光庁インバウンド観光コンテンツ造成支援事業・LocatoneサウンドAR観光ガイド「くノ一戦隊〜巣鴨の街を取り戻せ〜」（日本語・英語版・モニターツアー＝巣鴨地蔵通り商店街〜庚申塚商栄会＝旧中山道）・江戸東京野菜の種の配布（日本農林社協賛）・一粒万倍シール ／ 旧番号: — ／ 直接確認（2026-11-25に本文取得）（ai）",
 "- [ORG-049](org/ORG-049.md) — ＪＡ東京中央会「東京農業歴史めぐり 旧中山道はタネ屋街道」（掲載年表示なし・©2018）— 明治中期・巣鴨とげぬき地蔵〜板橋区清水町約6kmにタネ屋問屋9戸・小売店20戸の数値文言＋寛永20年（1643）代官所申告の書き付けに諏訪の種行商人が榎本種苗店（豊島区西巣鴨）に仕入れに来た模様の由緒文言（馬12〜3頭・「萬種物」の旗・1643年と店名の併記は時代考証的に疑義あり＝原文どおり観察記録）・真性寺（巣鴨3-21-21・江戸六地蔵） ／ 旧番号: — ／ 直接確認（2026-11-25に本文取得）（ai）"
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## ブログ・個人サイト（313件）', 1, 'BLOG見出し')
idx = idx.replace('## ブログ・個人サイト（313件）', '## ブログ・個人サイト（316件）')
assert_count(idx, '## ブログ・個人サイト（316件）', 1, 'BLOG見出し置換後')

assert_count(idx, '## 企業・団体の公式発表（45件）', 1, 'ORG見出し')
idx = idx.replace('## 企業・団体の公式発表（45件）', '## 企業・団体の公式発表（49件）')
assert_count(idx, '## 企業・団体の公式発表（49件）', 1, 'ORG見出し置換後')

assert_count(idx, '資料ファイル総数: 1788件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1788件', '資料ファイル総数: 1795件')
assert_count(idx, '資料ファイル総数: 1795件', 1, '総数行置換後')

for t in ['[BLOG-315]', '[BLOG-316]', '[BLOG-317]', '[ORG-046]', '[ORG-047]', '[ORG-048]', '[ORG-049]']:
    assert idx.count(t) == 0, f"ASSERT FAIL: 事前重複 {t}"

lines = idx.split('\n')
out = []
a_blog = '- [BLOG-314](blogs/BLOG-314.md)'
n_blog = 0
a_org = '- [ORG-045](org/ORG-045.md)'
n_org = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_blog):
        out.extend(BLOG_LINES); n_blog += 1
    if ln.startswith(a_org):
        out.extend(ORG_LINES); n_org += 1
assert n_blog == 1, f"ASSERT FAIL: BLOG-314アンカー {n_blog}件"
assert n_org == 1, f"ASSERT FAIL: ORG-045アンカー {n_org}件"
idx2 = '\n'.join(out)
for t, m in [('[BLOG-315]', 1), ('[BLOG-316]', 1), ('[BLOG-317]', 1), ('[ORG-046]', 1), ('[ORG-047]', 1), ('[ORG-048]', 1), ('[ORG-049]', 1)]:
    assert idx2.count(t) == m, f"ASSERT FAIL: 挿入後 {t} count={idx2.count(t)}"
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第310回:'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第309回:') + rdm.startswith('- **第309回:') == 1, "ASSERT FAIL: 第309回アンカー"
assert rdm.count('- **第310回:') == 0, "ASSERT FAIL: 第310回bullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第309回:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第310回:') == 1
assert rdm2.count('\n- **第309回:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.310-bullet.txt', '.310-insert.py', '.github/workflows/insert-310.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-310 OK')
