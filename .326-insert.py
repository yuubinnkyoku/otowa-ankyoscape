#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第326回: READMEに実行記録bulletを挿入するヘルパー（INDEX変更なし・新規sourceなし）。
使い方: python3 .326-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第325回:' 行の直後に .326-bullet.txt の1行を挿入（'- **第326回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
BULLET = '.326-bullet.txt'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第326回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第326回:' in readme:
        print('README: 第326回bullet already present; skip')
    else:
        must_one(readme, '- **第325回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第325回:')]
        assert len(hits) == 1, 'README anchor 第325回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))


if __name__ == '__main__':
    main()
