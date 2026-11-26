#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第334回: READMEに実行記録bulletを挿入しINDEXにMAP-225〜227行を追加するヘルパー。
使い方: python3 .334-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第333回:' 行の直後に .334-bullet.txt の1行を挿入（'- **第334回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-225/226/227の3行をMAP-224行の直後に挿入し「## 地図・絵図（224件）」→227件・
  「資料ファイル総数: 1850件」→1853件を更新（第334回のpush_filesでINDEXの行挿入・計数更新が
  済んでいる場合は検出して何もしない＝冪等）。
  （アンカー・計数文字列は一意であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.334-bullet.txt')

MAP225_LINE = '- [MAP-225](maps/MAP-225.md) — 『増補改正飯田町駿河台小川町絵図』（嘉永2[1849]/文久3[1863]改正・尾張屋板切絵図4・木版色刷・34.7×68.3cm・東京誌料・請求記号0412-4/東0412-004・資料コード4300035404・PD・全1コマ・zoom約1017KB）（2026-11-26・第334回・TOKYOアーカイブ「上水」67件掃引〔result_s→detail→画像API〕で取得・repo初出）— 千代田区内神田・小川町・駿河台・神保町・錦町域の切絵図で、資料解説（2011-2『江戸の町づくり』リーフレットp.10）に「神田川にかかる水道橋の隣は神田上水の掛樋で、ここから暗渠で江戸城内に入っています」文言＝千川筋市中末端域・小川町（GAZ-188「小石川の名これより起る」候補地）の尾張屋板切絵図としてrepo初（corpus「飯田町駿河台小川町」0件で既収録なしを確認済み）＝神田上水掛樋→暗渠の導水形状文言（GAZ-048/GAZ-068/BOOK-328系列）の図像側資料候補〔読図未実施〕 ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像API確認・読図未実施）（ai）'
MAP226_LINE = '- [MAP-226](maps/MAP-226.md) — 『小石川谷中本郷絵図』（安政4[1857]改・戸松昌訓図・尾張屋板切絵図21・49.2×52.2cm・東京誌料・請求記号045-17/東045-017・資料コード4300036260・PD・全1コマ）（2026-11-26・第334回・TOKYOアーカイブ「上水」67件掃引で取得・repo初出）— 小石川・本郷・谷中（上野不忍池を含む）を同一紙面に収める尾張屋板切絵図＝千川筋市中末端域（小石川・本郷）と谷端川下流（谷中・上野）の両域を含む図としてrepo初・MAP-019（近江屋・嘉永2『谷中本郷駒込小石川辺絵図』）と別系統の対校候補（戸松昌訓系は推定・板系統の同定は未実施・読図未実施） ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像API確認・読図未実施）（ai）'
MAP227_LINE = '- [MAP-227](maps/MAP-227.md) — 『玉川上水絵図』2点（一点目＝折本15.4×726.4cm・東京誌料760-20/東760-020・資料コード4300346351・PD・全23コマ・zoom取得可、二点目＝刷物・760-K1/東K小760-K001・資料コード4300346487・PD・コマ数未確認）（2026-11-26・第334回・TOKYOアーカイブ「上水」67件掃引で取得・repo初出）— 羽村取水堰〜四谷木戸約42.7kmの玉川上水全線絵図（資料解説=文化財ウィーク2012(48)・承応2[1653]開削・玉川庄右衛門・清右衛門文言）＝千川上水の分水源（玉川上水）全線図で、千川分水口（保谷樋口GOV-004・境橋BLOG-113）の図上位置確認の読図候補・MAP-205（神田上水絵図・東京誌料760-21・全10コマ）と同文庫隣番帯＝二大上水全線折本ペアの残り半分の所在固定 ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像API確認〔二点目の画像は要再確認〕・読図未実施）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第334回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第334回:' in readme:
        print('README: 第334回bullet already present; skip')
    else:
        must_one(readme, '- **第333回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第333回:')]
        assert len(hits) == 1, 'README anchor 第333回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    if '- [MAP-225](maps/MAP-225.md)' in index:
        print('INDEX: MAP-225 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [MAP-224](maps/MAP-224.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-224](maps/MAP-224.md) — ')]
        assert len(hits) == 1, 'INDEX anchor MAP-224 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [MAP225_LINE, MAP226_LINE, MAP227_LINE]
        index = '\n'.join(lines)
        must_one(index, '## 地図・絵図（224件）')
        index = index.replace('## 地図・絵図（224件）', '## 地図・絵図（227件）', 1)
        must_one(index, '資料ファイル総数: 1850件')
        index = index.replace('資料ファイル総数: 1850件', '資料ファイル総数: 1853件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: MAP-225/226/227 inserted + counts updated (地図224->227・総数1850->1853)')


if __name__ == '__main__':
    main()
