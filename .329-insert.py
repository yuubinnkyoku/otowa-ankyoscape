#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第329回: READMEに実行記録bulletを挿入するヘルパー。
使い方: python3 .329-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第328回:' 行の直後に .329-bullet.txt の1行を挿入（'- **第329回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- 本回は新規source登録なしのため docs/sources/INDEX.md は変更しない。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.329-bullet.txt')


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第329回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第329回:' in readme:
        print('README: 第329回bullet already present; skip')
    else:
        must_one(readme, '- **第328回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第328回:')]
        assert len(hits) == 1, 'README anchor 第328回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))


if __name__ == '__main__':
    main()
