#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第307回: INDEX行挿入(7)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .307-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.307-bullet.txt')

BOOK_LINES = [
 "- [BOOK-313](books/BOOK-313.md) — 豊島区立郷土資料館 編『豊島区立郷土資料館常設展図録』（昭和59年（1984）6月・95p・26cm・水道歴史館開架書架H H218・貸出不可）— 弦巻川・谷端川流域区の郷土資料館の1984年段階の常設展示図録＝展示構成の中の地形・河川系単元の有無は本文未見のため断定せず（生活と文化〔PAP-054・112・118〜121〕と同館の展示系の比較対象） ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌の直接確認・2026-11-24・本文は未閲覧）（ai）",
 "- [BOOK-314](books/BOOK-314.md) — 東京都新宿区立新宿歴史博物館 編『「柏木・角筈一目屏風」の世界』（平成2年（1990）1月・113p+図1枚・26cm・水道歴史館開架書架F F312・貸出不可・平成17年（2005）7月第2刷）— 柏木・角筈＝千川上水中流域（淀橋周辺）を描く江戸期一目屏風の研究書＝千川上水描画の有無と屏風の成立年代は本文未見のため断定せず（ro-da目録キーワード「江戸／江戸時代／水道／歴史／水道史／東京／江戸上水／神田上水／神田川／淀橋」） ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌〔キーワード欄含む〕の直接確認・2026-11-24・本文は未閲）（ai）",
 "- [BOOK-315](books/BOOK-315.md) — 神田川ネットワーク 編著『神田川再発見 歩けば江戸・東京の歴史と文化が見えてくる』（東京新聞出版局・平成20年（2008）12月・207p・26cm・水道歴史館開架書架D D299・貸出不可）— [GOV-560](../gov/GOV-560.md)第16回議事録（H20.11.27）の「大松委員から発刊のお知らせ」の書誌特定＝水窪川・弦巻川の水系接続の前提川（神田川）の市民研究書・四河川への言及の有無は本文未見 ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌と議事録文言の対照による確認・2026-11-24・本文は未閲）（ai）",
 "- [BOOK-316](books/BOOK-316.md) — 岩垣顕 著『神田川遡上』（街と暮らし社・平成18年（2006）3月・167p・21cm・水道歴史館開架書架D D284・貸出不可）— 神田川を下流から水源へ遡る紀行・歴史作品＝谷頭側への視線は四河川研究と同方向だが水窪川・弦巻川への言及の有無は本文未見 ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌の直接確認・2026-11-24・本文は未閲）（ai）",
 "- [BOOK-317](books/BOOK-317.md) — 阿部貴弘 著『土木遺産さんぽ : まち歩きで学ぶ 江戸・東京の歴史』（理工図書・令和6年（2024）12月・251p・21cm・水道歴史館開架書架B B366・貸出不可）— 2024年新刊＝千川上水経由区間（内藤新宿ほか）の遺産解説の可能性（キーワード「神田上水／神田川／内藤新宿」・千川上水への言及の有無は本文未見） ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌〔キーワード欄含む〕の直接確認・2026-11-24・本文は未閲）（ai）",
 "- [BOOK-318](books/BOOK-318.md) — 本田創 著『失われた川を読む・紡ぐ・愉しむ 東京暗渠学 改訂版』（実業之日本社・令和5年（2023）11月・304p・21cm・水道歴史館開架書架D D351・貸出不可）— BOOK-001/083シリーズの別書・改訂版＝用水史網羅型の解説書候補（キーワード「神田川／玉川上水／幡ヶ谷分水／三田用水／葛西用水」・四河川項目の有無は本文未見） ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌〔キーワード欄含む〕の直接確認・2026-11-24・本文は未閲）（ai）",
]

PAP_LINES = [
 "- [PAP-122](papers/PAP-122.md) — 水久保（大久保）克英「幕末期滝野川大砲製造所建設と村落 千川用水拡張工事を中心にして」（東京都北区教育委員会『文化財研究紀要』）— 幕末期の千川用水拡張工事と滝野川村を論じる学術研究＝BLOG-127（王子分水・慶応元年）・BLOG-226（滝野川反射炉）の同主題の学術論文系候補・ro-da目録（F265『第5集』1991・mokuji「大久保克英 著」）とnabunken論文検索（巻次6・北区・item/109640）の2経路で所在確認＝巻次と著者名の表記差異は本文未見のため併記（repo「大久保克英」「水久保」「見廻取締」初出） ／ 旧番号: — ／ 所在のみ（ro-da F265のmokuji欄とnabunken論文検索の直接確認・2026-11-24・本文は未閲覧・nabunken詳細頁は429で未取得）（ai）",
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## 書籍・雑誌・メディア（311件）', 1, 'BOOK見出し')
idx = idx.replace('## 書籍・雑誌・メディア（311件）', '## 書籍・雑誌・メディア（317件）')
assert_count(idx, '## 書籍・雑誌・メディア（317件）', 1, 'BOOK見出し置換後')

assert_count(idx, '## 論文・研究報告・データ（119件）', 1, 'PAP見出し')
idx = idx.replace('## 論文・研究報告・データ（119件）', '## 論文・研究報告・データ（120件）')
assert_count(idx, '## 論文・研究報告・データ（120件）', 1, 'PAP見出し置換後')

assert_count(idx, '資料ファイル総数: 1777件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1777件', '資料ファイル総数: 1784件')
assert_count(idx, '資料ファイル総数: 1784件', 1, '総数行置換後')

for tag in ['[BOOK-313]', '[BOOK-314]', '[BOOK-315]', '[BOOK-316]', '[BOOK-317]', '[BOOK-318]', '[PAP-122]']:
    assert idx.count(tag) == 0, f"ASSERT FAIL: 事前重複 {tag}"

lines = idx.split('\n')
out = []
a_book = '- [BOOK-312](books/BOOK-312.md)'
a_pap = '- [PAP-121](papers/PAP-121.md)'
n_book = n_pap = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_book):
        out.extend(BOOK_LINES); n_book += 1
    elif ln.startswith(a_pap):
        out.extend(PAP_LINES); n_pap += 1
assert n_book == 1, f"ASSERT FAIL: BOOK-312アンカー {n_book}件"
assert n_pap == 1, f"ASSERT FAIL: PAP-121アンカー {n_pap}件"
idx2 = '\n'.join(out)
for tag in ['[BOOK-313]', '[BOOK-314]', '[BOOK-315]', '[BOOK-316]', '[BOOK-317]', '[BOOK-318]', '[PAP-122]']:
    assert idx2.count(tag) == 1, f"ASSERT FAIL: 挿入後 {tag}"
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第307回・続き:**'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第306回:') + rdm.startswith('- **第306回:') == 1, "ASSERT FAIL: 第306回行存在"
assert rdm.count('\n- **第307回:') + rdm.startswith('- **第307回:') == 1, "ASSERT FAIL: 第307回本流アンカー"
assert rdm.count('- **第307回・続き:') == 0, "ASSERT FAIL: 第307回・続きbullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第307回:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第307回・続き:') == 1
assert rdm2.count('\n- **第307回:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.307-bullet.txt', '.307-insert.py', '.github/workflows/insert-307.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-307 OK')
