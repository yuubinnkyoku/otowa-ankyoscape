#!/usr/bin/env python3
# retrigger: 389 (paths filter firing)
# -*- coding: utf-8 -*-
"""第389回: READMEに実行記録bulletを挿入し、INDEXにGOV-639の1行を挿入・計数更新するヘルパー。
使い方: python3 .389-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第388回:' 行の直後に .389-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [GOV-638]' 行の直後に GOV-639 の1行を挿入し、
  '## 行政・公的機関（636件）'→'（637件）'、'資料ファイル総数: 1989件'→'1990件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.389-bullet.txt')

LINES = {}
LINES['GOV-639'] = '- [GOV-639](gov/GOV-639.md) — 東京都公文書館クロス検索「水番」掃引（200件・第1頁走査）＝神田上水廃止後の白堀・関口筋の実務4件（1871〜1883・2026-11-28・第389回・詳細頁表項目直接取得・repo grep 0件＝repo初出）— ①**玉川上水水源涸水時の「白堀通り各村分水口」を定例に倣い「三分通」に差塞ぐ様各水番人へ達する伺（1883・pkey 715330・往復録・乙・613.A6.08・MF府明Ⅱ明16-026・コマ0006-0319）＝白堀通り筋の各村分水口に渇水時の通水制限の「定例」が存在した一次文言候補**でGOV-623の白堀筋丈量の村々通達（角筈・高田・上下落合・中野等）に渇水時運用の側を追加（「三分通」の意味と各村の特定は本文未見）②**庁中達（1871-08-17・pkey 598155・605.C4.10・MF府明Ⅱ明04-014・コマ0006-0082）＝小日向水道町・小日向東古川町・小日向西古川町・小日向松ヶ枝町・関口水道町・小石川水道町・小石川表町・小石川仲町・小石川金富町・小日向台町の10か町地主が従来負担してきた白堀通り藻刈人足・堤草刈・不浄物取捨・水番人給等の出金を自今其儀に及ばぬとする達＝白堀維持の負担者リスト（10町）とその終了（明治4年8月）を1件で記録**しGOV-237（明治2年藻刈・渡賃銭負担）の負担構造の終焉側に接続（「券邸」は目録表記のまま要照合）③**関口水道町水車持ち半兵衛の江戸川上掛樋大破洩水→修繕中仮樋仕度願（1875・pkey 878800・607.A5.06・MF府明Ⅱ明08-063・コマ0484-1095・宛先＝神田上水関口村水番人杉山喜三郎）＝明治8年の関口水車の存在の行政記録**で関口水車通時系列（1776→1864→1875→1881→1912地籍）の中間datapoint＋江戸川上の掛樋の大破・仮樋の運用実務④**関口町水番人杉山喜三郎へ「上水車分水」に付届（1877・pkey 510664・608.C4.02・MF府明Ⅱ明10-012・コマ0640-1031）＝関口の水車分水の行政手続きの実例**で杉山喜三郎の1875〜1883（大洗堰修繕・GOV-623）の関口側窓口実務像を水車分水側から補強（届出人は本文未見） ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目直接取得・本文は未見）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第389回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第389回:' in readme:
        print('README: 第389回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第388回:')]
        assert len(hits) == 1, 'README anchor 第388回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-639]' in index:
        print('INDEX: GOV-639 already present; skip')
    else:
        assert '## 行政・公的機関（636件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1989件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-638]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-638 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['GOV-639'])
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（636件）', '## 行政・公的機関（637件）')
        index = index.replace('資料ファイル総数: 1989件', '資料ファイル総数: 1990件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-639 inserted; counts updated')


if __name__ == '__main__':
    main()
