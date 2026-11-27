#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第356回: READMEに実行記録bulletを挿入し、INDEXにGOV-622行を挿入・計数更新するヘルパー。
使い方: python3 .356-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第355回:' 行の直後に .356-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-621 行の直後に GOV-622 行を挿入し、
  '## 行政・公的機関（619件）'→'（620件）'、'資料ファイル総数: 1911件'→'1912件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.356-bullet.txt')

GOV622_LINE = (
    "- [GOV-622](gov/GOV-622.md) — 東京都公文書館クロス検索「養水」掃引（98件・2026-11-27実施・第356回初回）"
    "で新規特定した千川・神田上水系の田養水実務8項目（詳細頁書誌）— 下石神井村豊田安五郎外12名田養水旧復願"
    "（1882・612.B5.01・府明Ⅱ明15-059）・神田上水路并助水路各村田養水草堰取設着手実地検査巡回旅費"
    "（1881・611.C3.01・府明Ⅱ明14-006＝GOV-366「助水堀筋」の明治期実務候補）・関口町神田上水田養水分水願聞届"
    "（1874・606.B5.04）・王子村外21〜23ヶ村養水群（1875×2・1881・607.A5.04/611.D8.08＝GOV-053/GOV-587⑥/"
    "GOV-588④の前後段）・石神井村養水赤羽村/稲附村水掛反別（1882上報・614.C9.01）・橋場町其外養水費連合会決議"
    "（1879・610.D7.09・水系帰属未確定）＝いずれも公開件名レベルで本文（MF）は未確認 ／ 旧番号: — ／ 所在のみ"
    "（一覧頁＋詳細頁目録を機械取得・第356回）（ai）"
)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第356回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第356回:' in readme:
        print('README: 第356回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第355回:')]
        assert len(hits) == 1, 'README anchor 第355回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-622' in index:
        print('INDEX: GOV-622 already present; skip')
    else:
        assert '## 行政・公的機関（619件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1911件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-621]')]
        assert len(hits) == 1, 'INDEX anchor GOV-621 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV622_LINE)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（619件）', '## 行政・公的機関（620件）')
        index = index.replace('資料ファイル総数: 1911件', '資料ファイル総数: 1912件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-622 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
