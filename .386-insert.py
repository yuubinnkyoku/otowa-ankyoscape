#!/usr/bin/env python3
# retrigger: 386 (paths filter firing)
# -*- coding: utf-8 -*-
"""第386回: READMEに実行記録bulletを挿入し、INDEXにGOV-636・BLOG-395の2行を挿入・計数更新するヘルパー。
使い方: python3 .386-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第385回:' 行の直後に .386-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [GOV-635]' 行の直後に GOV-636 の1行、'- [BLOG-394]' 行の直後に BLOG-395 の1行を挿入し、
  '## 行政・公的機関（633件）'→'（634件）'、'## ブログ・個人サイト（393件）'→'（394件）'、
  '資料ファイル総数: 1984件'→'1986件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.386-bullet.txt')

LINES = {}
LINES['GOV-636'] = '- [GOV-636](gov/GOV-636.md) — 東京都公文書館クロス検索「谷端」「溜井」「揚堀」「水窪」「弦巻」「逆サ川」語掃引（2026-11-28・第386回・GETレシピ・詳細頁表項目直接取得・repo grep 0件＝repo初出）— ①明治21〜22年「市町村制施行順序取調書」の滝野川村字平尾北谷端・字谷津の分界段別地価戸数人口の表・図面〔pkey 557855・請求604.B4.05・MF 0477-0707・D385・**画像公開（i-repository・図面判読は未了）**＝谷端の字界・飛地の明治22年確定過程の一次史料・BLOG-069・GOV-633と接続〕②滝野川町「逆サ川前耕地」字名の地籍実務群16件（1912〜1932）＝**「逆サ川」字名の公文書側実在〔repo grep 0件〕**・詳細4件確認（大正8年官有道路敷公用廃止〔pkey 1080635・内容注記が「字北谷端2288」・図面34枚〕・大正7年不用道路敷〔1080458〕・**大正2年王子電気軌道の土地寄附〔1088079〕**・**大正15年西巣鴨〜滝ノ川町1.3第13号線の残地売収〔1205532〕**）・語源（逆流・付け替え等）は本文未見のため断定せず＝対照表の「逆川」（出井川通称・石神井川）とは別系統の字名資料・陰性: 揚堀は千住1件のみ（田柄用水揚げ堀の行政文書は目録上不在）・溜井は中新井村（GOV-586既収録）のみ・水窪は大森清水窪・八王子等の同名異地名が大半・弦巻は荏原郡弦巻村（世田谷）が大半＝谷端川系の重要pkey（谷端川改修告示群・矩形渠設計図等）は既収録と確認 ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目直接取得・本文・図面は未見・557855のみ画像公開）（ai）'
LINES['BLOG-395'] = '- [BLOG-395](blogs/BLOG-395.md) — mark60「ぶらっと遡上探索」千川上水シリーズ Scene-921〜928（2024年12月〜2025年1月・全8話・freedomwalk.blog.fc2.com/blog-entry-1098〜1105）（2026-11-28・第386回・curl本文全文取得＝直接確認・repo未収録シリーズ〔BLOG-148/150/301は同ブログの谷端川・石神井川シリーズ〕）— 千川上水公園から取水口までの全流路遡上と**38橋の諸元表（名称・構造種別・分水堰/河口からの距離・橋長・幅員・完成）＝repo初出の「分水堰からの距離」軸の定量観察**・**九頭龍橋＝「崩れ橋」当て字説〔repo grep 0件＝橋名由来記録〕＋九頭竜弁財天への庚申塔・供養塔の遷座叙述**・**大山西町の「伏越」マン蓋2種〔千川上水×下水路の立体交差の現地遺構〕**・**巣鴨駅前「千川上水空気弁・都北部公園」角型マン蓋（分配堰〜六義園送水ルート）**・**開渠橋梁の竣工年次群〔GOV-084/578の行政図面にない観測値〕**（西室橋1939・更新橋1957・北裏橋1984・桂橋1987・鎮守/樋口/蛍橋1989・東北浦橋1991〔親柱表記と旧地名「北裏」の表記ずれ考察〕・西北浦橋1992）・**千川上水橋梁＝1径間鈑桁・約12m・竣工1926年（T15）の第三記録〔BLOG-090の1926年説 vs BLOG-361の1927年説の対立に新観測・断定せず〕**・伊勢橋の「暗渠への通水停止・善福寺川切替通水」観察〔BLOG-090と整合〕・江古田二又の「（千）」境界石の移設先＝旭丘地域集会所〔BLOG-032の境界石群の所在具体化〕・上石千川児童遊園の「なんちゃって水車」・下石神井調圧水槽600トン〔repo grep 0件〕・天保11年庚申塔＋石橋供養塔（武蔵野大学前）の現地対比 ／ 旧番号: — ／ 直接確認（curl本文全文・第386回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第386回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第386回:' in readme:
        print('README: 第386回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第385回:')]
        assert len(hits) == 1, 'README anchor 第385回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-636]' in index:
        print('INDEX: GOV-636 already present; skip')
    else:
        assert '## 行政・公的機関（633件）' in index, 'INDEX 行政 heading mismatch'
        assert '## ブログ・個人サイト（393件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1984件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-635]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-635 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['GOV-636'])
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-394]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-394 found %d' % len(bhits)
        lines.insert(bhits[0] + 1, LINES['BLOG-395'])
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（633件）', '## 行政・公的機関（634件）')
        index = index.replace('## ブログ・個人サイト（393件）', '## ブログ・個人サイト（394件）')
        index = index.replace('資料ファイル総数: 1984件', '資料ファイル総数: 1986件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-636, BLOG-395 inserted; counts updated')


if __name__ == '__main__':
    main()
