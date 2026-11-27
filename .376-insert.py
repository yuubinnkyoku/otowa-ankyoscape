#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第376回: READMEに実行記録bulletを挿入し、INDEXにGOV-632行を挿入・計数更新するヘルパー。
使い方: python3 .376-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第375回:' 行の直後に .376-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-631 行の直後に GOV-632 の1行を挿入し、
  '## 行政・公的機関（629件）'→'（630件）'、'資料ファイル総数: 1946件'→'1947件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.376-bullet.txt')

ROWS = []
ROWS.append('- [GOV-632](gov/GOV-632.md) — 練馬区公式「練馬の今昔 道と街道」富士街道・沼辺の十字路（2024.4.10更新・ページ番号186-424-575・総務部情報公開課・2026-11-27・第376回・curl本文全文取得＝直接確認・repo grep当該頁0件＝repo初出・BLOG-362の練馬区HP掲載頁特定課題を解消）— **昭和31年（1956）撮影の田柄用水と橋の写真の資料番号23-1009の特定**（平成9年=23-1010・平成29年9月=23-1406・沼辺地蔵=27-0715の各資料番号も確定）・**「『沼辺』とは、上石神井村の小名で、現在の石神井台二丁目から六丁目の一部をいいます」の行政側定義文言＝repo初出**・石神井台三丁目33番付近の石神井学園前交差点・**「手前の橋は、現在は暗きょになった田柄用水に架かっていました」＝富士街道横断部の田柄用水が1956年時点で開渠・橋を有していた区公式写真記録**・ほこらの沼辺地蔵は現在も同位置に現存（平成29年9月写真） ／ 旧番号: — ／ 直接確認（ai）')


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第376回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第376回:' in readme:
        print('README: 第376回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第375回:')]
        assert len(hits) == 1, 'README anchor 第375回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-632' in index:
        print('INDEX: BLOG-361 already present; skip')
    else:
        assert '## 行政・公的機関（629件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1946件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-631]')]
        assert len(hits) == 1, 'INDEX anchor GOV-631 found %d' % len(hits)
        for off, row in enumerate(ROWS):
            lines.insert(hits[0] + 1 + off, row)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（629件）', '## 行政・公的機関（630件）')
        index = index.replace('資料ファイル総数: 1946件', '資料ファイル総数: 1947件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-632 inserted; counts updated')


if __name__ == '__main__':
    main()
