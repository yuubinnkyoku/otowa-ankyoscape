#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第309回: INDEX行挿入(1)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .309-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.309-bullet.txt')

BLOG_LINES = [
 "- [BLOG-314](blogs/BLOG-314.md) — 村上泰賢「わが国産業革命のはじまり」#72〜75「滝野川大砲製造所（1）〜（4）」（ファスニングジャーナル本紙2521〜2530号・2020）— 『陸軍歴史』巻七（『勝海舟全集』所収）の意訳経由で幕末反射炉×千川上水交渉の過程を具体的に記述: 「圦樋皆明け」要求と作事奉行の拒否回答・勘定奉行立田主水正の仲介・上流「庭の滝や泉水池」無駄引込指摘・「慶応元年九月から二ヶ月半」開削・『東京市史稿』四七引用の慶応三年火薬製造所提議「其位置は王子滝野川に撰定す」・慶応二年二月鉄製天水桶稲荷社奉納の痕跡 ／ 旧番号: — ／ 直接確認（4回分の本文全文を2026-11-25に取得。引用文言はすべて筆者（村上泰賢）による『陸軍歴史』巻七等の「意訳」で一次文言の直接採録ではない）（ai）"
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## ブログ・個人サイト（312件）', 1, 'BLOG見出し')
idx = idx.replace('## ブログ・個人サイト（312件）', '## ブログ・個人サイト（313件）')
assert_count(idx, '## ブログ・個人サイト（313件）', 1, 'BLOG見出し置換後')

assert_count(idx, '資料ファイル総数: 1787件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1787件', '資料ファイル総数: 1788件')
assert_count(idx, '資料ファイル総数: 1788件', 1, '総数行置換後')

assert idx.count('[BLOG-314]') == 0, "ASSERT FAIL: 事前重複 [BLOG-314]"

lines = idx.split('\n')
out = []
a_blog = '- [BLOG-313](blogs/BLOG-313.md)'
n_blog = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_blog):
        out.extend(BLOG_LINES); n_blog += 1
assert n_blog == 1, f"ASSERT FAIL: BLOG-313アンカー {n_blog}件"
idx2 = '\n'.join(out)
assert idx2.count('[BLOG-314]') == 1, "ASSERT FAIL: 挿入後 [BLOG-314]"
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第309回:'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第308回:') + rdm.startswith('- **第308回:') == 1, "ASSERT FAIL: 第308回アンカー"
assert rdm.count('- **第309回:') == 0, "ASSERT FAIL: 第309回bullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第308回:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第309回:') == 1
assert rdm2.count('\n- **第308回:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.309-bullet.txt', '.309-insert.py', '.github/workflows/insert-309.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-309 OK')
