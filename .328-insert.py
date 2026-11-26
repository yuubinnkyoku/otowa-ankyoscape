#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第328回: READMEに実行記録bulletを挿入しINDEXにGOV-604・GAZ-195行を追加するヘルパー。
使い方: python3 .328-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第327回:' 行の直後に .328-bullet.txt の1行を挿入（'- **第328回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md:
  * '- [GOV-603](gov/GOV-603.md)' 行の直後にGOV-604行を挿入し「## 行政・公的機関（601件）」→602件を更新。
  * '- [GAZ-194](gazetteers/GAZ-194.md)' 行の直後にGAZ-195行を挿入し「## 地誌・行政史料（194件）」→195件を更新。
  * 「資料ファイル総数: 1843件」→1845件を更新（当該行は「/ 旧番号対応」に続くため部分一致で置換）。
  （各カウント・アンカーはともに1箇所であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.328-bullet.txt')

GOV604_LINE = (
    '- [GOV-604](gov/GOV-604.md) — 東京都公文書館デジタルアーカイブ クロス検索「水久保」掃引（23件・詳細頁21件・高田町雑司ヶ谷字水久保系）（2026-11-25・第328回・POSTレシピ復旧で取得・いずれも目録レベル・図面・本文は未確認）'
    '— ①昭和8年（1933）「雑種財産引受【平面図（公図写） 新旧水路敷実測丈量図 構造図 縦断面図】〔（北豊島郡高田町大字雑司ヶ谷字水久保新田）用悪水路〕《東京税務監督局》」（pkey 1084884/85・申土庶・国有地籍 冊の7=316.B4.08）＝'
    '弦巻川・水窪川核心エリア（水久保新田〜現・豊島区日出町1丁目161-1〜188）の水路の新旧水路敷実測丈量図の現存（repo初出の水路文言・流路・新旧の内容は図面未確認で断定しない）'
    '②王子電気軌道目白線の土地収用公告群（大正9・10・11・13年・pkey 1087254/1087344/45/1087479/80/1087643/44＝字水久保新田166-1外6筆・水久保189外29筆・字水原622-1外10筆の耕地番号列挙）＋'
    '停留場設置届（大正15年文書年度・pkey 1209729〜31＝大塚駅前・向原・水久保・雑司ケ谷・鬼子母神前の5停留場・「水久保停留場設計図」現存）＝BLOG-001の水久保停留場昭和14年統合説の行政側原本候補'
    '（線路系統・位置対応は図面確認まで断定しない） ③昭和3年（1928）「図面謄写〔高田町雑司ヶ谷水久保234 三杉稲荷〕《高田町役場》」（pkey 1083221・辰土発・国有地籍）＝三杉稲荷の遷座前所在地=水久保234番地の行政文書目録文言（repo初出・BLOG-151の1967年遷座〔もと日出町の都電通り沿い〕の対照資料）'
    ' ④無届移動地申告・注意〔高田町大字雑司谷字亀原 水久保新田 鶴巻 威光 水原 西原 御堂杉 中谷戸 池谷戸浅井原〕《板橋税務署 日本染色（株）外23名》（大正12〜昭和7年・pkey 1089491・雑件 高田町 冊の1）＝'
    '弦巻川流域の染色工場の移動地申告＋雑司谷の字名群9つの一括列挙（「御堂杉」「亀原」「西原」「池谷戸浅井原」はrepo初出の字名候補＝対照表に新行・「威光」はGAZ-002氷柱ヶ谷条・「中谷戸」はBLOG-049の実務文書レベルの追加用例）'
    ' ⑤水久保巡査派出所建物の不動産寄付受領（昭和7年・pkey 1298949/1299094・参事会議原議・会議録）＝水久保冠の警察施設名の一次記録'
    ' ⑥同名異地整理（和田堀内村永福寺字水久保・南多摩田井村・瑞穂町・上大崎村清水久保はスコープ外）＋「音羽」97件（文京区音羽の近代行政群＝スコープ外）・「水窪」38件（GOV-573既収録の1080476/77以外は同名異地）・「弦巻」78件（荏原郡世田谷側中心）・「弦巻用水」「鼠ヶ谷」0件の陰性'
    ' ／ 旧番号: — ／ 検索結果一覧・詳細頁目録の機械取得で確認（原本・図面画像は未確認）（ai）'
)

GAZ195_LINE = (
    '- [GAZ-195](gazetteers/GAZ-195.md) — 邨岡良弼（村岡檪斎）『日本地理志料』巻之十六（東陽堂・1903・NDL次世代DL 762751・巻14-17収録・全文ZIP該当条直見）（2026-11-25・第328回・第327回課題④［GOV-603引用元の原文確認］の解消・OCR崩壊ゆえ文言候補・原字照合必須）'
    '— ①小日向条「山岡浚明曰、日頭方ニ廢、今ノ小日向村、盖其遺名、因謂、殘篇風土記。載日頭〓、長祿ノ江戶圖、作小日向村、北條分限報、江戶小日向內、小日向彈正知行、'
    '按圖亘小日向、小石川、牛込、市谷、金杉、關口、音羽、高田、雜司カ谷、池袋ノ諸邑、盖其域也」＝和名抄豊島郡日頭郷比定の山岡浚明帰属文言＋'
    '長祿江戶圖・北條分限報の出典構造が原文側で確定＝GOV-603（港区史第1巻ht001050引用）の引用元文言の実在確認＝GAZ-092鳥越村条（小日向単独比定）との比定範囲対照資料'
    ' ②荏原郡世田ヶ谷条「鎌倉八幡宮永享元年ノ文書、世田谷内弦卷村」＋「按圖亘弦卷、用賀、經堂在家、深澤、野毛、等等力ノ諸邑、稱菅刈ノ莊」＝世田谷側「弦巻」の永享元年（1429）文書言及候補（同名異地・対照表に新行・文書本体は未確認）'
    ' ③雑司ヶ谷条の法明寺系譜文言（東鑑治承4年威光寺→正嘉元年改日宗→今ノ名＝「威光」語の寺名由来系の関心・OCR崩壊大） ④岩淵郷条の比定域列挙（豊島・王子・瀧野川・梶原・上坂橋・下板橋・十条・稲付・神谷・赤羽根・岩淵・袋＝王子・滝野川を含む岩淵郷考証の対照点）'
    ' ⑤巻14-17で「千川」「谷端」「水窪」「水久保」「音羽川」「弦巻川」の川名文言0件の陰性（「音羽」は比定邑列挙のみ・世田谷「弦卷」は邑名）'
    ' ／ 旧番号: — ／ OCR全文確認（〓等の崩壊箇所は原字照合前提）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第328回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第328回:' in readme:
        print('README: 第328回bullet already present; skip')
    else:
        must_one(readme, '- **第327回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第327回:')]
        assert len(hits) == 1, 'README anchor 第327回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    changed = False

    if '[GOV-604](gov/GOV-604.md)' in index:
        print('INDEX: GOV-604 line already present; skip')
    else:
        must_one(index, '- [GOV-603](gov/GOV-603.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-603](gov/GOV-603.md)')]
        assert len(hits) == 1, 'INDEX anchor GOV-603 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV604_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GOV-604 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 行政・公的機関（601件）')
        index = index.replace('## 行政・公的機関（601件）', '## 行政・公的機関（602件）', 1)
        print('INDEX: 行政 count 601->602')

    if '[GAZ-195](gazetteers/GAZ-195.md)' in index:
        print('INDEX: GAZ-195 line already present; skip')
    else:
        must_one(index, '- [GAZ-194](gazetteers/GAZ-194.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GAZ-194](gazetteers/GAZ-194.md)')]
        assert len(hits) == 1, 'INDEX anchor GAZ-194 found %d' % len(hits)
        lines.insert(hits[0] + 1, GAZ195_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GAZ-195 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 地誌・行政史料（194件）')
        index = index.replace('## 地誌・行政史料（194件）', '## 地誌・行政史料（195件）', 1)
        print('INDEX: 地誌 count 194->195')

    if changed:
        must_one(index, '資料ファイル総数: 1843件')
        index = index.replace('資料ファイル総数: 1843件', '資料ファイル総数: 1845件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (行政601->602・地誌194->195・総数1843->1845)')


if __name__ == '__main__':
    main()
