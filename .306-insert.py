#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第306回: INDEX行挿入(10)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .306-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.306-bullet.txt')

MAP_LINES = [
 "- [MAP-213](maps/MAP-213.md) — 東京都水道歴史館 樋線図第2種『神田橋御門ヨリ新シ橋辺迄 絵図（神中）』（K0085・東京府水道掛か・明治4〜11年〔1871〜78〕候補・70×44cm）— MAP-209（神上）の下流側隣接図＝神田橋御門→新シ橋（あたらしばし）間の千代田区内神田・岩本町・神田須田町（神田川に沿う市中配水域）。本収録で第2種の神田系4点が網羅 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-214](maps/MAP-214.md) — 東京都水道歴史館 樋線図第2種『本町・両国橋・永代橋辺迄 絵図（神下）』（K0086・東京府水道掛か・明治4〜11年〔1871〜78〕候補・73×68cm）— 神田上水の給水範囲が日本橋地域（中央区日本橋本町・東日本橋・日本橋人形町周辺）に達した明治初頭の配水区域図＝MAP-213（神中）の下流側 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-215](maps/MAP-215.md) — 東京都水道歴史館 樋線図第2種『鍛冶橋御門外ヨリ日本橋辺 絵図面（神下々）』（K0087・東京府水道掛か・明治4〜11年〔1871〜78〕候補・64.8×35.5cm）— 神田上水の市中配水の南東縁＝中央区日本橋・京橋・八重洲周辺。第2種神田系の最終図葉 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-216](maps/MAP-216.md) — 東京都水道歴史館 樋線図第4種『玉川・神田 虎ノ門内ヨリ幸橋内・大名小路・西丸下・神田橋内・常盤橋内ニ至ル（辰）』（K0119・東京府水道掛か・明治前期〔明治初年候補〕・102×54cm）— 江戸城西丸下・大手前＝明治政府機関集積地周辺（千代田区大手町・丸の内・霞が関・日比谷公園周辺）の玉川×神田両上水併記図 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-217](maps/MAP-217.md) — 東京都水道歴史館 樋線図第4種『神田・玉川 比丘尼橋ヨリ松尾町ヲ経テ霊岸島ニ至ル（未）』（K0122・東京府水道掛か・明治前期〔明治初年候補〕・81×39cm）— 玉川上水の京橋・八丁堀地域（中央区京橋・八丁堀・新川周辺）＝第4種の東縁配水記録・MAP-215と同地区の別種図面 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-218](maps/MAP-218.md) — 東京都水道歴史館 樋線図第4種『神田 龍閑橋ヨリ常盤橋外・馬喰町・小網町・浜町ニ至ル（戌）』（K0125・東京府水道掛か・明治前期〔明治初年候補〕・54×38cm）— 龍閑橋（神田川架橋点）起点の区間図＝神田川筋と神田上水樋線の市中併走を直接読める候補図・MAP-214（第2種・神下）と同地区の別種図面 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-219](maps/MAP-219.md) — 東京都水道歴史館 樋線図第4種『玉川・神田 一石橋ヨリ江戸橋・亀島町ニ至ル（亥）』（K0126・東京府水道掛か・明治前期〔明治初年候補〕・91×89cm大型図）— 日本橋川の一石橋→江戸橋・亀島町＝日本橋（神田上水）・茅場町（玉川上水）の併記終端図で、本収録で第4種の神田系6点が網羅 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-220](maps/MAP-220.md) — 東京都水道歴史館 樋線図第5種『牛込区西五軒町（上水樋線之図）』（K0221・東京市水道改良事務所・明治中期〜後期・51×36cm）— 第5種99点中で牛込区唯一の図葉・95番図。題箋の小石川区表記を牛込と朱書訂正＝区境・台帳管理の記録情報でMAP-072の「K0221欠番の理由は未確認」が解消（水道改良事務所成立1891以降の神田・玉川上水最末期の区別図） ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
 "- [MAP-221](maps/MAP-221.md) — 東京都水道歴史館 樋線図第5種『小石川区内 上水樋線之図（全体図）（第九号）』（K0225・東京市水道改良事務所・明治中期〜後期・77×93cm）— 水窪川・弦巻川・谷端川起点域を含む小石川区（現文京区西部）全域の樋線と敷地内井戸の配置を一図に収める第306回最重要図＝MAP-073〜077（個別図5点）とGOV-010（砲兵工廠K0224）を全体図から読む補助線。本収録で第5種の小石川・牛込系の掃引完了 ／ 旧番号: — ／ 所在のみ（ro-da API目録の書誌と説明文の直接確認・2026-11-24・読図は未実施）（ai）",
]

BOOK_LINES = [
 "- [BOOK-312](books/BOOK-312.md) — 羽村市郷土博物館『羽村市郷土博物館紀要』第35号（令和3年（2021）3月・93p・21cm・水道歴史館開架書架B B042-35・貸出不可）— 目次「小石川上水・神田上水から玉川上水へ」（角田清美 著）＝第305回に所在未確認だった35号の所在解決（ro-da書誌APIのq=羽村検索で直接確認）・羽村紀要34〜38号・40号の掃引網羅で「小石川上水」呼称の取扱いは本文未見のため断定せず ／ 旧番号: — ／ 所在のみ（ro-daアーカイブAPI書誌検索の書誌・目次の直接確認・2026-11-24・本文は未取得）（ai）",
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## 地図・絵図（212件）', 1, 'MAP見出し')
idx = idx.replace('## 地図・絵図（212件）', '## 地図・絵図（221件）')
assert_count(idx, '## 地図・絵図（221件）', 1, 'MAP見出し置換後')

assert_count(idx, '## 書籍・雑誌・メディア（310件）', 1, 'BOOK見出し')
idx = idx.replace('## 書籍・雑誌・メディア（310件）', '## 書籍・雑誌・メディア（311件）')
assert_count(idx, '## 書籍・雑誌・メディア（311件）', 1, 'BOOK見出し置換後')

assert_count(idx, '資料ファイル総数: 1764件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1764件', '資料ファイル総数: 1774件')
assert_count(idx, '資料ファイル総数: 1774件', 1, '総数行置換後')

for tag in ['[MAP-213]', '[MAP-214]', '[MAP-215]', '[MAP-216]', '[MAP-217]', '[MAP-218]', '[MAP-219]', '[MAP-220]', '[MAP-221]', '[BOOK-312]']:
    assert idx.count(tag) == 0, f"ASSERT FAIL: 事前重複 {tag}"

lines = idx.split('\n')
out = []
a_map = '- [MAP-212](maps/MAP-212.md)'
a_book = '- [BOOK-311](books/BOOK-311.md)'
n_map = n_book = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_map):
        out.extend(MAP_LINES); n_map += 1
    elif ln.startswith(a_book):
        out.extend(BOOK_LINES); n_book += 1
assert n_map == 1, f"ASSERT FAIL: MAP-212アンカー {n_map}件"
assert n_book == 1, f"ASSERT FAIL: BOOK-311アンカー {n_book}件"
idx2 = '\n'.join(out)
assert idx2.count('[MAP-221](maps/MAP-221.md)') == 1
assert idx2.count('[BOOK-312](books/BOOK-312.md)') == 1
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第306回:**'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第305回:') + rdm.startswith('- **第305回:') == 1, "ASSERT FAIL: 第305回アンカー"
assert rdm.count('- **第306回:') == 0, "ASSERT FAIL: 第306回bullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第305回:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第306回:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.306-bullet.txt', '.306-insert.py', '.github/workflows/insert-306.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-306 OK')
