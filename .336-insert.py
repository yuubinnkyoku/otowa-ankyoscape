#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第336回: READMEに実行記録bulletを挿入しINDEXにMAP-228・MAP-229行を追加するヘルパー。
使い方: python3 .336-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第335回:' 行の直後に .336-bullet.txt の1行を挿入（'- **第336回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-228/229の2行をMAP-227行の直後に挿入し「## 地図・絵図（227件）」→229件・
  「資料ファイル総数: 1856件」→1858件を更新（第336回のpush_filesでINDEXの行挿入・計数更新が
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
BULLET = os.path.join(HERE, '.336-bullet.txt')

MAP228_LINE = '- [MAP-228](maps/MAP-228.md) — 『玉川上水誌』（TOKYOアーカイブ・折本13.7×825cm・東京誌料760-2/東760-002・資料コード4300346342・PD・全30コマ・zoom約619.6〜708.7KB）（2026-11-26・第336回・TOKYOアーカイブ「用水」掃引で取得・repo初出）— 玉川上水の「誌」（記録・誌類）＝MAP-227（玉川上水絵図・東京誌料760-20）と同文庫760番台の対資料で、分水源（玉川上水）の管理・沿革記録の候補（年代欄なし・編纂年代は本文判読まで断定しない・千川上水の分水文言の有無は判読待ち）・NDLサーチ連携書誌R100000086-I0000000015_00054520 ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像リストAPI確認・本文判読未実施）（ai）'
MAP229_LINE = '- [MAP-229](maps/MAP-229.md) — 『五郡用水鑑』（TOKYOアーカイブ・刷物23.5×62cm・東京誌料760-C2/東C760-C002・資料コード4300346450・PD・全1コマ・zoom約826.4KB）（2026-11-26・第336回・TOKYOアーカイブ「用水」掃引で取得・repo初出）— 「用水」掃引で検出した刷物1枚。「五郡」がどの五郡かは本文判読まで断定できない（repoの「五郡」用例＝隣接五郡82町村編入〔GOV-259〕・埼玉県1896年郡統合〔GOV-330保谷村郡変換〕に直接つなぐ証拠なし・横長刷物の体裁から用水の組合・取極め類の可能性もある〔推定〕・同文庫・同分類のMAP-228と同時で、多摩側の用水〔玉川上水・千川用水〕関係の可能性も否定できない）・判読では郡名列挙・対象水路名・年紀を先に確認する・NDL title検索0件・ndlsearch any検索R100000086-I0000000015_00228098の1件を確認 ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像リストAPI確認・本文判読未実施）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第336回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第336回:' in readme:
        print('README: 第336回bullet already present; skip')
    else:
        must_one(readme, '- **第335回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第335回:')]
        assert len(hits) == 1, 'README anchor 第335回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    if '- [MAP-228](maps/MAP-228.md)' in index:
        print('INDEX: MAP-228 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [MAP-227](maps/MAP-227.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-227](maps/MAP-227.md) — ')]
        assert len(hits) == 1, 'INDEX anchor MAP-227 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [MAP228_LINE, MAP229_LINE]
        index = '\n'.join(lines)
        must_one(index, '## 地図・絵図（227件）')
        index = index.replace('## 地図・絵図（227件）', '## 地図・絵図（229件）', 1)
        must_one(index, '資料ファイル総数: 1856件')
        index = index.replace('資料ファイル総数: 1856件', '資料ファイル総数: 1858件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: MAP-228/229 inserted + counts updated (地図227->229・総数1856->1858)')


if __name__ == '__main__':
    main()
