#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第375回: READMEに実行記録bulletを挿入し、INDEXにBLOG-361〜365行を挿入・計数更新するヘルパー。
使い方: python3 .375-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第374回:' 行の直後に .375-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-360 行の直後に BLOG-361〜365 の5行を挿入し、
  '## ブログ・個人サイト（359件）'→'（364件）'、'資料ファイル総数: 1941件'→'1946件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.375-bullet.txt')

ROWS = []
ROWS.append('- [BLOG-361](blogs/BLOG-361.md) — pakashi89「「しもしゃく祭り」と千川上水橋梁」（2024-08-01・note.com・2026-11-27・第375回・本文全文取得＝直接確認・repo grep 0件＝repo初出）— **上井草の千川上水橋梁の竣工「1927年・西武新宿線開業の前年」説＝BLOG-090の1926年説と対立併記（村山線開業1927年基準では内部不整合・原典未確認で断定せず）**・**2024年時点の開渠で水の存在を確認できなかった観察（BLOG-090の「水が顔を出す」記述との時期差は観察時期不明のため評価保留）**・**西武新宿線高架化により橋梁・開渠がひっそり撤去されるという予測〔推定〕**・区境（練馬区・杉並区）で行政が機能しないのではという推測・下石神井商店街の「今は暗渠になった千川上水」「桜並木と蛍」「大雨で店の中まで浸水」の伝聞・鉄橋周辺の夏草と荒れの現況 ／ 旧番号: — ／ 直接確認（ai）')
ROWS.append('- [BLOG-362](blogs/BLOG-362.md) — pakashi89「石神井と失われた川」（2024-09-19・note.com・2026-11-27・第375回・本文全文取得＝直接確認・repo grep「沼辺」0件＝repo初出）— **「沼辺の十字路」の地名（練馬区HP・けやき憩いの森近くの交差点の地蔵）と昭和31年（1956）白黒写真に田柄用水と橋が写っている記述**・田柄用水の石橋跡（？）の2024年観察・**成増飛行場建設で上流部水路破損→一時通水不能→戦後グラントハイツ化で再通水**〔ORG-051の「土管で地中に埋めた」観察・BLOG-328と対校〕・**富士街道沿いの暗渠化「昭和40年頃」・田柄川緑道化「昭和56年（1981）」〔repo grep新出〕＝ORG-051（幹線46年9月起工）・GOV-075（47年度）・GOV-631（47年ごろ）と対象・時期のずれが残る対立併記（用水暗渠化と幹線整備の区別整理が課題）**・棚橋の名残の観察（ORG-051の棚橋と同橋名・現物対応は未確認） ／ 旧番号: — ／ 直接確認（ai）')
ROWS.append('- [BLOG-363](blogs/BLOG-363.md) — 土偶子「【ぶら近所】千川上水施餓鬼亡霊供養塔」（2024-09-14・note.com/tasty_willet454・2026-11-27・第375回・本文全文取得＝直接確認・碑文言・明治41年3月建立はBLOG-094で既収録＝重複）— **台座の寄進村名群（石神井村・武蔵野村吉祥寺・関村・竹下村・西久保村・土支田村・保谷村）と石工「寅吉」〔写真判読・repo初出〕＝明治41年の供養塔建立が千川上水沿い複数村の共同事業だったことを示す一次側材料**・**所在住所の区市表記のずれ（練馬区関町南4-2 vs 武蔵野市吉祥寺北町3-15-8・境界上水に由来する曖昧さ）**・「ねりまの文化財60号」（repo所在のみ）の該当記述の間接確認（水難供養・明治41年3月）・吉祥寺橋〜東北裏橋間の2024年現況（開渠・井口家屋敷林・畑）・「この辺りに堰もあって落ちて死ぬ人もいた」伝聞・**1960年代の大雨溢水→西武新宿線運転中止の個人記憶〔聴取〕** ／ 旧番号: — ／ 直接確認（ai）')
ROWS.append('- [BLOG-364](blogs/BLOG-364.md) — 吉田「ひとくち散歩記録「田中橋」」（2022-12-05・note.com/osanpoyoshida・2026-11-27・第375回・本文全文取得＝直接確認・repo grep「田中橋」0件＝橋名repo初出）— **練馬区関町南の千川上水に架かる「田中橋」＝名板なし・親柱に直書き・木材風に加工した石材〔2022年観察〕**（田中水車〔上石神井1-8〕とは別物で関係は保留）・武蔵関駅から約1km・橋の下流（西）側の雑木林のような場所・**廃橋（橋の先に家の形跡・出入りに利用か）と廃墟の2022年観察（比定は未解決）** ／ 旧番号: — ／ 直接確認（ai）')
ROWS.append('- [BLOG-365](blogs/BLOG-365.md) — Code for Nerima「練馬区の地図にない川を探索しよう（南西部、千川上水編）」（2018-04-22・note.com/code4nerima・筆者ながしま・2026-11-27・第375回・本文全文取得＝直接確認・repo grep「立野橋」0件＝repo初出）— **下石神井の西武新宿線・千川通り・井草通りの交わる踏切の脇の千川上水暗渠の出口〔2018年観察〕**・**立野橋交差点の角の千川上水と庚申塔の案内版（暗渠であることのにぎわい説明・設置者・設置年は本文に明示なし）**・青梅街道を渡った先の開渠の突然の出現（「昭和にタイムスリップ」）・吉祥寺通り交差点から取水口まで4.5km・暗渠の入り口の音景観（開渠のせせらぎと暗渠内の低音の同時聴取）＝千川上水中流の開渠・暗渠分布の2018年断面（BLOG-102・GOV-072・BLOG-336と対校） ／ 旧番号: — ／ 直接確認（ai）')


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第375回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第375回:' in readme:
        print('README: 第375回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第374回:')]
        assert len(hits) == 1, 'README anchor 第374回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-361' in index:
        print('INDEX: BLOG-361 already present; skip')
    else:
        assert '## ブログ・個人サイト（359件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1941件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-360]')]
        assert len(hits) == 1, 'INDEX anchor BLOG-360 found %d' % len(hits)
        for off, row in enumerate(ROWS):
            lines.insert(hits[0] + 1 + off, row)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（359件）', '## ブログ・個人サイト（364件）')
        index = index.replace('資料ファイル総数: 1941件', '資料ファイル総数: 1946件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-361..365 inserted; counts updated')


if __name__ == '__main__':
    main()
