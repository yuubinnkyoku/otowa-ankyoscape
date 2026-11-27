#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第373回: READMEに実行記録bulletを挿入し、INDEXにBLOG-360行を挿入・計数更新するヘルパー。
使い方: python3 .373-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第372回:' 行の直後に .373-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-359 行の直後に BLOG-360 の1行を挿入し、
  '## ブログ・個人サイト（358件）'→'（359件）'、'資料ファイル総数: 1937件'→'1938件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.373-bullet.txt')

BLOG_LINE_360 = '- [BLOG-360](blogs/BLOG-360.md) — なりますチャンネル「【散策記】田柄天祖神社と田柄用水：水と共に生きた地域の歴史を紐解く」（2026-06-22投稿・2026-11-16更新・2026-11-27・第373回・curl直接取得＝直接確認・repo grep 0件＝repo初出）— **田柄天祖神社（練馬区田柄）の「上練馬村玉川上水分水紀念碑」碑名・上部「水神宮」刻字＝repo初出**・明治4年1871田柄用水開削→**明治26年1893玉川上水分水増量実現（20年越し請願）の年次＝repo初出**（典拠は本文未示のため一次史料確認は保留）・階段前の小さな橋＝用水流路跡〔観察〕・けやき憩いの森約47m現存区間＝BLOG-328空堀観察の寸法側補完・田柄町水道組合の井戸6箇所・PFAS水質検査対応〔2026年現況〕＝BLOG-351の3204㎥/日補完・BLOG-351の天祖神社比定を田柄天祖神社へ前進させる候補（愛宕神社金魚市等の地域文脈一致・同一碑の断定は碑文採録まで保留）・碑は田柄用水（田無用水分水系）の頌徳碑で千川上水への言及なし＝BLOG-351「千川上水と田柄灌漑用水の接続」解釈の修正・弱め候補（両用水の共通上流＝玉川上水の点は残る） ／ 旧番号: — ／ 直接確認（curl本文全文・第373回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第373回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第373回:' in readme:
        print('README: 第373回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第372回:')]
        assert len(hits) == 1, 'README anchor 第372回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-360' in index:
        print('INDEX: BLOG-360 already present; skip')
    else:
        assert '## ブログ・個人サイト（358件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1937件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-359]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-359 found %d' % len(bhits)
        lines.insert(bhits[0] + 1, BLOG_LINE_360)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（358件）', '## ブログ・個人サイト（359件）')
        index = index.replace('資料ファイル総数: 1937件', '資料ファイル総数: 1938件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-360 inserted; counts updated')


if __name__ == '__main__':
    main()
