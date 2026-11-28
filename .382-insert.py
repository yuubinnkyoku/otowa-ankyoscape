#!/usr/bin/env python3
# retrigger: 382 (paths filter firing)
# -*- coding: utf-8 -*-
"""第382回: READMEに実行記録bulletを挿入し、INDEXにBLOG-394の1行を挿入・計数更新するヘルパー。
使い方: python3 .382-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第381回:' 行の直後に .382-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-393 行の直後に BLOG-394 の1行を挿入し、
  '## ブログ・個人サイト（392件）'→'（393件）'、'資料ファイル総数: 1976件'→'1977件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.382-bullet.txt')

LINES = {}
LINES['BLOG-394'] = '- [BLOG-394](blogs/BLOG-394.md) — Natrium.jp「水路敷ペイントその2（田柄用水）」（suirojiki/suirojiki_02・撮影2012/5/4・2013/1/2・2018/2/10・2021/8/21・2022/5/5・2022/8/16）（2026-11-28・第382回・curl本文全文取得＝直接確認・repo初出URL）— **田柄川・田柄用水水系の公図「水路敷」水色ペイントの全面定点記録（平和台・田柄町内・土支田・谷原・三原台・石神井公園駅北側の6区画・187番目までのプロット言及）＝repo初出の観察体系**・**韮窪（三原台一丁目17番地）＝田柄川上流端の谷頭〔観察・BLOG-367の韮窪起源説と整合〕**・**三原台二丁目1番地は2016年暗渠撤去工事でペイント消滅〔観察〕**・**田柄二丁目2番地の水路敷は2015年区画整理で廃止〔観察・公図水路敷の消滅実例〕**・土支田二丁目14番地は区画整理歩道化で消滅〔観察〕・土支田一丁目18番地に6連続ペイント・谷原六丁目24-25番地に連続4ペイント＋練馬清掃工場前ジグザグ水路敷・**再舗装後のペイント復活事例（田柄三丁目・2022/5/5）＝維持行為の実態記録**・**石神井町四丁目9-10番地＝田柄川水系で最も上流の水路敷ペイント＋「石神井公園駅方向から開削された用水路の跡」〔BLOG-383と呼応〕**・田柄地区の方位限界（北=田柄四丁目19番地・南=三丁目17番地・西=三丁目28-29番地）・東田柄橋跡すぐ西側の北向き水路敷 ／ 旧番号: — ／ 直接確認（curl本文全文・第382回）（ai）'

ORDER = ['BLOG-394']


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第382回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第382回:' in readme:
        print('README: 第382回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第381回:')]
        assert len(hits) == 1, 'README anchor 第381回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [BLOG-394]' in index:
        print('INDEX: BLOG-394 already present; skip')
    else:
        assert '## ブログ・個人サイト（392件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1976件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-393]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-393 found %d' % len(bhits)
        pos = bhits[0] + 1
        for k in ORDER:
            lines.insert(pos, LINES[k])
            pos += 1
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（392件）', '## ブログ・個人サイト（393件）')
        index = index.replace('資料ファイル総数: 1976件', '資料ファイル総数: 1977件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-394 inserted; counts updated')


if __name__ == '__main__':
    main()
