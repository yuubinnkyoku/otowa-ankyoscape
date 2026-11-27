#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第366回: READMEに実行記録bulletを挿入し、INDEXにBLOG-345〜350行を挿入・計数更新するヘルパー。
使い方: python3 .366-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第365回:' 行の直後に .366-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-344 行の直後に BLOG-345〜350 の6行を挿入し、
  '## ブログ・個人サイト（343件）'→'（349件）'、'資料ファイル総数: 1915件'→'1921件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.366-bullet.txt')

NEW_LINES = [
    "- [BLOG-345](blogs/BLOG-345.md) — 水徒然（onnbubatta）「沢蔵司稲荷近辺の麗しい水路跡」（2016年2月27日・直はCloudFront 403のためWaybackスナップショットで本文全文・コメント欄取得＝直接確認・第366回）— 沢蔵司稲荷西方（小石川2丁目）私有地内の石造り水路跡（落差・架橋・下水道局プレート）＝repo初出＋「続・後楽2丁目の水路跡」記事の地籍図に当該水路が青線で記載（出発点=春日通り・富坂警察と礫川小の間・終点=沢蔵司稲荷窪地）＝repo初出＋コメント欄の水道工事店従業員（nori-p）による「礫川小の水路（下水道）に私道の住宅排水を流していた」実務証言＝現役雑排水ラインの生証言・repo初出＋藤橋（ふじはし）親柱の2015年再訪確認＝BLOG-322（2011年）に続く第2の独立観察＋BOOK-026（私版東京図絵）の礫川小6〜7m崖記述の「2016年記事」出典が本記事と確定 ／ 旧番号: — ／ 直接確認（Wayback本文全文・コメント欄・第366回）（ai）",
    "- [BLOG-346](blogs/BLOG-346.md) — 水徒然（onnbubatta）「久世山・音羽・小日向など」（2012年4月17日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第366回）— 「解体中の中学で神田上水白堀の遺構が発掘されたと新聞で読んだ」＝伝聞・repo初出（原報道の特定が課題）＋水窪川が神田川に注ぐ辺りの桜木町の小町名（GAZ-080嘉永期桜木町と対照）＋湧水の20年ぶり再訪での水量減少観察・今宮神社南の水流・八幡坂の洗い場・水道端図書館言及 ＝水窪川最下流（江戸川橋〜合流点）の2012年定点観察 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第366回）（ai）",
    "- [BLOG-347](blogs/BLOG-347.md) — 水徒然（onnbubatta）「水窪川周辺を川下り。日光・日の出・サンシャイン」（2013年6月17日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第366回）— 水窪川源流部（東池袋4丁目・造幣局南西角の井戸〜日の出町）の2013年実況観察＋日光広場の看板文言「1990年の設置・地下に貯水槽」＝BLOG-106〜110の辻広場整備史に看板レベルの設置年次を追加＋補助81号線（昭和21年計画決定）と一帯のフェンス・小公園（BLOG-066/184と整合）＋巣鴨プリズン排水口跡の2013年探索目撃（BLOG-099/107の対校定点）＋水窪川支流構造の疑問形整理 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第366回）（ai）",
    "- [BLOG-348](blogs/BLOG-348.md) — 水徒然（onnbubatta）「区境の気になる水路？」（2011年8月23日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第366回）— 向原ゴルフセンター付近の区境水路の住宅地図上の線が平成2年→近年で半減した対校観察＋品川電線の開渠が2011年時点で既に消滅＝BLOG-329（品川電線工場と水車仮説）の独立裏付け＋練馬区「こもれび」の水路敷・谷戸区民調査隊募集（貫井特集・2011年）・田柄用水PDFの記録 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第366回）（ai）",
    "- [BLOG-349](blogs/BLOG-349.md) — 水徒然（onnbubatta）「煉瓦が導く小石川砲兵工廠の谷戸」（2015年9月2日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第366回）— 小石川トンネル射撃場（旧東京砲兵工廠射撃場・明治16〜18年頃完成推定・1999年返還）北端の窪地＝明治迅速地図に後楽園台地（中央大学〜戦没者墓苑〜礫川公園）の2本の谷が描かれる＝repo初出の谷構造データ（比定は筆者も保留・神田川支流説を併記）＋牛天神石段脇側溝の流水（2015年）・後楽園〜ラクーア付近の明治期古地図の水路判読 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第366回）（ai）",
    "- [BLOG-350](blogs/BLOG-350.md) — 水徒然（onnbubatta）「猫ちゃに導かれて未舗装暗渠」（2013年4月9日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第366回）— 板橋区熊野町の谷端川緑道への未舗装暗渠道合流（手前に大きめの石・「小便禁止」看板）の2013年定点観察＝BLOG-069（2022年）・BLOG-114（2026年）に加わる合流部データ（支流の比定は未解決） ／ 旧番号: — ／ 直接確認（Wayback本文全文・第366回）（ai）",
]


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第366回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第366回:' in readme:
        print('README: 第366回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第365回:')]
        assert len(hits) == 1, 'README anchor 第365回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-345' in index:
        print('INDEX: BLOG-345 already present; skip')
    else:
        assert '## ブログ・個人サイト（343件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1915件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-344]')]
        assert len(hits) == 1, 'INDEX anchor BLOG-344 found %d' % len(hits)
        for off, nl in enumerate(NEW_LINES, start=1):
            lines.insert(hits[0] + off, nl)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（343件）', '## ブログ・個人サイト（349件）')
        index = index.replace('資料ファイル総数: 1915件', '資料ファイル総数: 1921件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-345..350 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
