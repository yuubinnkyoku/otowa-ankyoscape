#!/usr/bin/env python3
# retrigger: 385 (paths filter firing)
# -*- coding: utf-8 -*-
"""第385回: READMEに実行記録bulletを挿入し、INDEXにGOV-635・MAP-242の2行を挿入・計数更新するヘルパー。
使い方: python3 .385-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第384回:' 行の直後に .385-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [GOV-634]' 行の直後に GOV-635 の1行、'- [MAP-241]' 行の直後に MAP-242 の1行を挿入し、
  '## 地図・絵図（241件）'→'（242件）'、'## 行政・公的機関（632件）'→'（633件）'、
  '資料ファイル総数: 1982件'→'1984件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.385-bullet.txt')

LINES = {}
LINES['GOV-635'] = '- [GOV-635](gov/GOV-635.md) — 東京都公文書館クロス検索「水路敷を道路敷」「換地確定図」掃引（2026-11-28・第385回・GETレシピ・詳細頁表項目直接取得・repo grep 0件＝repo初出）— 大正6年「地種目組替 冊の18」（資料ID 000126790・請求302.D4.27・MF 0332-0665・D875）の水路消滅実務3件＝①豊多摩郡井萩村大字上井草字中通南「用悪水路敷を道路敷に充用」1917-10-06起案〔pkey 1196116・千川上水井草分水流域の用悪水路の道路転用＝BLOG-392・GOV-689の実務側補完〕②北豊島郡志村大字小豆沢字東耕地1686番地先〔天神前89番地先・宇都宮金之烝・pkey 1196147〜49・1917-09-05〕③北豊島郡滝ノ川町大字滝ノ川字東大原303〜300番の1号〔鈴木常吉・pkey 1196157/58・1917-10-02〕＋千川上水沿いの中野区江古田4丁目道路敷・中新井町第二土地区画整理組合「第二工区換地確定図」1941-03-12起案〔pkey 1086684・辰経発・国有地籍冊の9・MF 0354-0663〕・陰性: 換地確定図15件掃引で戦災復興換地確定図は6組合のみ（弦巻・水窪・音羽・巣鴨の組合地区図なし＝谷端のみ）・悪水吐42件完結（四河川関連は既収録3件のみ）・枝線第1号・第6号・千川第2号は目録上不在 ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目直接取得・本文・図面は未見）（ai）'
LINES['MAP-242'] = '- [MAP-242](maps/MAP-242.md) — Google My Maps「首都高速蓋on蓋」（mid=1du6aGTX1j7Hs42fY6P59VB1UzN_5uR4s・作成者・作成日不明）（2026-11-28・第385回・KMLエンドポイント`maps/d/kml?forcekml=1&mid=…&nl=0`で全placemark取得＝66,444 bytes・71 placemarks・repo grep 0件＝repo初出）— 首都高速が旧川の暗渠上を通る箇所を掲載する第三者作成地図＝弦巻川2箇所（東池袋〜南池袋付近35.7187〜94N/139.7245〜67E・江戸川橋付近=水道端〜関口35.7108〜121N/139.7301〜11E〔BLOG-076・107と同じ地区〕）と千川上水1箇所（豊玉北〜桜台境界35.7495〜502N/139.7116〜131E）のplacemark座標・説明欄はmymaps.usercontentホストの写真のみ（判読未了）・作成者・典拠不明のため位置の傍証資料（推定）としてのみ扱う・第383回ノートの「BLOG-394のMy Mapsリンク」帰属の誤りを訂正（BLOG-394頁はOSMピン6件のみ） ／ 旧番号: — ／ 直接確認（KML取得・座標・名称列確認・写真画像は未判読）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第385回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第385回:' in readme:
        print('README: 第385回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第384回:')]
        assert len(hits) == 1, 'README anchor 第384回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-635]' in index:
        print('INDEX: GOV-635 already present; skip')
    else:
        assert '## 地図・絵図（241件）' in index, 'INDEX 地図 heading mismatch'
        assert '## 行政・公的機関（632件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1982件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-634]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-634 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['GOV-635'])
        mhits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-241]')]
        assert len(mhits) == 1, 'INDEX anchor MAP-241 found %d' % len(mhits)
        lines.insert(mhits[0] + 1, LINES['MAP-242'])
        index = '\n'.join(lines)
        index = index.replace('## 地図・絵図（241件）', '## 地図・絵図（242件）')
        index = index.replace('## 行政・公的機関（632件）', '## 行政・公的機関（633件）')
        index = index.replace('資料ファイル総数: 1982件', '資料ファイル総数: 1984件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-635, MAP-242 inserted; counts updated')


if __name__ == '__main__':
    main()
