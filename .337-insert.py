#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第337回: READMEに実行記録bulletを挿入するヘルパー（INDEX編集なし・第337回は新規採番なし）。
使い方: python3 .337-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第336回:' 行の直後に .337-bullet.txt の1行を挿入（'- **第337回:' 行が既にあれば
  スキップ・アンカーが一意でなければabort）。（アンカー文字列は一意であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.337-bullet.txt')


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第337回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第337回:' in readme:
        print('README: 第337回bullet already present; skip')
    else:
        must_one(readme, '- **第336回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第336回:')]
        assert len(hits) == 1, 'README anchor 第336回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))


if __name__ == '__main__':
    main()
