#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第363回: READMEに実行記録bulletを挿入するヘルパー（READMEのみ版・INDEX変更なし）。
使い方: python3 .363-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第362回:' 行の直後に .363-bullet.txt の1行を挿入。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.363-bullet.txt')


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第363回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第363回:' in readme:
        print('README: 第363回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第362回:')]
        assert len(hits) == 1, 'README anchor 第362回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))


if __name__ == '__main__':
    main()
