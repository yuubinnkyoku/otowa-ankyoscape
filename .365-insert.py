#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第365回: READMEに実行記録bulletを挿入し、INDEXにBLOG-344行を挿入・計数更新するヘルパー。
使い方: python3 .365-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第364回:' 行の直後に .365-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-343 行の直後に BLOG-344 行を挿入し、
  '## ブログ・個人サイト（342件）'→'（343件）'、'資料ファイル総数: 1914件'→'1915件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.365-bullet.txt')

BLOG344_LINE = (
    "- [BLOG-344](blogs/BLOG-344.md) — 水徒然（onnbubatta）「中板橋の牧場名残（エンガ堀エンド）と水車の遺構」"
    "（2012年5月1日・直はCloudFront 403のためWayback 2024-05-18スナップショットで本文全文取得＝直接確認・第365回）— "
    "エンガ堀中板橋〜弥生町区間の2012年観察＋「ものの本」引用の川幅1.5m・名のある橋2箇所・板を持参して渡る"
    "「携帯橋」習俗＝repo初出（引用元書名未特定）＋吉川牧場跡地＝弥生小学校＝repo grep新出（BLOG-145の籾山・積田牧場に"
    "加わる別系統のエンガ堀沿い牧場記録）＋大谷口仮排水機場・下水道局出先機関の滑り台階段＝repo初出〔観察〕＋"
    "弥生町「瀬田水車」遺構（刻み目入り長方形石材2基・通称「坊主巻き」からの引水伝承・豊敬稲荷の地図）＝repo grep新出"
    "（石神井川系のため周辺記録と位置づけ）＋「農村語彙稿むさしの」の「えんが」語源情報 ／ 旧番号: — ／ "
    "直接確認（Wayback本文全文・第365回）（ai）"
)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第365回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第365回:' in readme:
        print('README: 第365回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第364回:')]
        assert len(hits) == 1, 'README anchor 第364回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-344' in index:
        print('INDEX: BLOG-344 already present; skip')
    else:
        assert '## ブログ・個人サイト（342件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1914件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-343]')]
        assert len(hits) == 1, 'INDEX anchor BLOG-343 found %d' % len(hits)
        lines.insert(hits[0] + 1, BLOG344_LINE)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（342件）', '## ブログ・個人サイト（343件）')
        index = index.replace('資料ファイル総数: 1914件', '資料ファイル総数: 1915件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-344 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
