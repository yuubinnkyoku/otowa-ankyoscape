#!/usr/bin python3
# -*- coding: utf-8 -*-
# retrigger: 391 (paths filter firing)
"""第391回: READMEに実行記録bulletを挿入するヘルパー（新規sourceなしのためINDEX変更なし）。
使い方: python3 .391-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第390回:' 行の直後に .391-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: 変更なし（総数1,993件不変・本回は新規sourceなし）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.391-bullet.txt')


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第391回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第391回:' in readme:
        print('README: 第391回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第390回:')]
        assert len(hits) == 1, 'README anchor 第390回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX: 変更なし（不変確認のみ） ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    assert '資料ファイル総数: 1993件' in index, 'INDEX 総数 mismatch (expect 1993件)'
    assert '## 行政・公的機関（638件）' in index, 'INDEX 行政 heading mismatch'
    assert '## 企業・団体の公式発表（54件）' in index, 'INDEX 団体 heading mismatch'
    print('INDEX: unchanged (no new sources this round)')


if __name__ == '__main__':
    main()
