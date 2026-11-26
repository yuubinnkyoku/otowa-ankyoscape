#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第339回: READMEに実行記録bulletを挿入するヘルパー（READMEのみ版・INDEXはpush_filesに含め済み）。
使い方: python3 .339-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第338回:' 行の直後に .339-bullet.txt の1行を挿入（'- **第339回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.339-bullet.txt')


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第339回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第339回:' in readme:
        print('README: 第339回bullet already present; skip')
    else:
        must_one(readme, '- **第338回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第338回:')]
        assert len(hits) == 1, 'README anchor 第338回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))


if __name__ == '__main__':
    main()
