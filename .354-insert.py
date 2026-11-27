#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第354回: READMEに実行記録bulletを挿入し、INDEX.mdにBLOG-342行を挿入するヘルパー。
使い方: python3 .354-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第353回:' 行の直後に .354-bullet.txt の1行を挿入。
- INDEX.md: BLOG-341行の直後にBLOG-342行を挿入し、
  ブログ340→341・総数1908→1909の計数を更新。
"""
import io
import os
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs/sources/INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.354-bullet.txt')

BLOG_LINE_342 = '- [BLOG-342](blogs/BLOG-342.md) — 髙山英男「「蓋on蓋」に夢中。」（毎日暗活！暗渠ハンター・2020年9月25日）— 「蓋on蓋」＝暗渠の蓋（A部分）の上空に高架（B部分）が被さる二重蓋構造の定義文言、例示写真＝板橋区役所付近・高速都心環状線と千川上水の蓋on蓋（repo初出＝千川上水×首都高の重複蓋構造の実観察）、首都高×水路の全貌地図（Google My Maps・mid=1du6aGTX1j7Hs42fY6P59VB1UzN_5uR4s・精度向上のため更新継続）と一覧表の存在・各地点写真の公開予告、B=首都高に限った調査枠組み ／ 旧番号: — ／ 直接確認（2026-11-27にblog.jpで本文全文取得・記事ID 24797518を特定）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第354回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第354回:' in readme:
        print('README: 第354回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第353回:')]
        assert len(hits) == 1, 'README anchor 第353回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        idx = f.read()
    if '- [BLOG-342]' in idx:
        print('INDEX: 第354回分 already present; skip')
        return
    lines = idx.split('\n')
    b = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-341]')]
    assert len(b) == 1, 'INDEX anchor BLOG-341 found %d' % len(b)
    lines.insert(b[0] + 1, BLOG_LINE_342)
    idx = '\n'.join(lines)
    idx, n2 = re.subn('## ブログ・個人サイト（340件）', '## ブログ・個人サイト（341件）', idx)
    idx, n3 = re.subn('資料ファイル総数: 1908件', '資料ファイル総数: 1909件', idx)
    assert n2 == 1 and n3 == 1, 'count update failed: %d %d' % (n2, n3)
    with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
        f.write(idx)
    print('INDEX: BLOG-342 inserted, counts updated')


if __name__ == '__main__':
    main()
