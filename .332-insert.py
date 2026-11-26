#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第332回: READMEに実行記録bulletを挿入しINDEXにGOV-605・BOOK-332行を追加するヘルパー。
使い方: python3 .332-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第331回:' 行の直後に .332-bullet.txt の1行を挿入（'- **第332回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md:
  * '- [GOV-604](gov/GOV-604.md)' 行の直後にGOV-605行を挿入し「## 行政・公的機関（602件）」→603件を更新。
  * '- [BOOK-331](books/BOOK-331.md)' 行の直後にBOOK-332行を挿入し「## 書籍・雑誌・メディア（330件）」→331件を更新。
  * 「資料ファイル総数: 1848件」→1850件を更新。
  （各カウント・アンカーはともに1箇所であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.332-bullet.txt')

GOV605_LINE = (
    '- [GOV-605](gov/GOV-605.md) — 東京都公文書館デジタルアーカイブ 詳細頁「復命書　宮仲１８８４より蟹窪６７２間の地上物件調査の件　物件調書掲載〔北豊島郡巣鴨町大字巣鴨１８８９〕《西尾由太郎　８０件名》」'
    '（pkey 1204912/1204913＝同一件名の重複採録・昭和18年度1943・東京府経理課・収録先「土地収用　補償２．１．第１２号西巣鴨町　冊の１６０」・請求番号325.C8.07・MF府昭18-082 コマ0413-0657・複写可・原本電子コピー不可）'
    '（2026-11-26・第332回・新UIクロス検索POSTレシピ復旧で「蟹窪」掃引・repo初出・目録レベルで物件調書本文は未確認）'
    '— 内容注記「**住所地：北豊島郡巣鴨町大字巣鴨字宮仲１８８４番地～大字池袋字蟹窪６７２番地**」＝'
    '①**大字池袋字蟹窪672番地の1943年用例**（GOV-370の1920年629-1/755-1に続く番地つき字名用例＝水窪川源流窪地の字蟹窪の地番体系が戦時中まで稼働していたことを示す目録文言）'
    '②**巣鴨字宮仲1884番地の番地つき用例（repo初出）**＝谷端川低地側の宮仲と水窪川源流側の蟹窪を結ぶ区間の地上物件調査'
    '（件名「宮仲１８８４より蟹窪６７２**間**」の「間」は区間の読みが自然〔観察〕・物件調書80件名・調査目的〔戦時収用・防空等〕は本文未確認で断定しない・MF複写で本文確認可能）'
    ' ／ 旧番号: — ／ 詳細頁目録の機械取得で確認（本文・図面は未確認）（ai）'
)

BOOK332_LINE = (
    '- [BOOK-332](books/BOOK-332.md) — 東京地下鐵道株式會社『東京地下鐵道史』坤（印刷/発行昭和9年6月20日・乾坤二巻・発賣所實業之日本社・NDL次世代DL 1235045・全文ZIP＋座標JSON）'
    '（2026-11-26・第332回・第316回ノート③保留候補の本文/座標側確認で新規収録）'
    '— 第12圖の2「工事實施に依つて得た地質圖(上野萬世橋間)」（折丁コマ36-37）の座標JSON（1235045_0000037.json・93ブロック）で'
    '「**元祿時代千川上水路**」（id48・x4560-4598・断面x軸上で旅篭町〔x2514〕→仲町〔x3917〕と假1萬世橋〔x4629〕の間・萬世橋〔x5652〕西方・神田川は萬世橋の東）'
    '「古代-下水路」「堀抜井戸」注記＋「神田區」「花房町」「末廣町」「旅篭町」「仲町」ラベルを確認＝'
    '**1930年代地下鉄建設（上野萬世橋間＝営業区間表の第2工區）の地質観測断面が江戸期千川上水路を時代名つき埋没水路として万世橋西方に表示**＝'
    'GAZ-193（神田旅籠町・昌平橋外堀井の渡・安永9年5月9日→天明3年千川上水請負人引渡）・GOV-395（旅籠町の安永9年差止文言）の旅籠町文言群と'
    'BOOK-328の明治千川水道神田給水ルート・「神田區萬世橋下水渠」の末端域の位置的裏付け＋'
    '田村與吉（東京市前河港課技術係長）への旧図・文献調査委嘱（第8〜11圖）と工事観測の合流が時代名つき旧水路表示の制度的背景〔確認: 本文OCRは要照合〕＋'
    '対照課題: 第12圖の1（淺草上野間）の「江戸時代上水路」ラベル＝千川の浅草御殿給水（BOOK-320）の候補（断定しない・原画像判読が前提）'
    ' ／ 旧番号: — ／ OCR・座標JSON確認（図面ゆえ判読文言はhuman原画像照合まで確定しない）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第332回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第332回:' in readme:
        print('README: 第332回bullet already present; skip')
    else:
        must_one(readme, '- **第331回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第331回:')]
        assert len(hits) == 1, 'README anchor 第331回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    changed = False

    if '[GOV-605](gov/GOV-605.md)' in index:
        print('INDEX: GOV-605 line already present; skip')
    else:
        must_one(index, '- [GOV-604](gov/GOV-604.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-604](gov/GOV-604.md)')]
        assert len(hits) == 1, 'INDEX anchor GOV-604 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV605_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GOV-605 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 行政・公的機関（602件）')
        index = index.replace('## 行政・公的機関（602件）', '## 行政・公的機関（603件）', 1)
        print('INDEX: 行政 count 602->603')

    if '[BOOK-332](books/BOOK-332.md)' in index:
        print('INDEX: BOOK-332 line already present; skip')
    else:
        must_one(index, '- [BOOK-331](books/BOOK-331.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-331](books/BOOK-331.md)')]
        assert len(hits) == 1, 'INDEX anchor BOOK-331 found %d' % len(hits)
        lines.insert(hits[0] + 1, BOOK332_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: BOOK-332 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 書籍・雑誌・メディア（330件）')
        index = index.replace('## 書籍・雑誌・メディア（330件）', '## 書籍・雑誌・メディア（331件）', 1)
        print('INDEX: 書籍 count 330->331')

    if changed:
        must_one(index, '資料ファイル総数: 1848件')
        index = index.replace('資料ファイル総数: 1848件', '資料ファイル総数: 1850件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (行政602->603・書籍330->331・総数1848->1850)')


if __name__ == '__main__':
    main()
