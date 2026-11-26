#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第330回: READMEに実行記録bulletを挿入しINDEXにGAZ-196・GAZ-197・BOOK-331行を追加するヘルパー。
使い方: python3 .330-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第329回:' 行の直後に .330-bullet.txt の1行を挿入（'- **第330回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md:
  * '- [GAZ-195](gazetteers/GAZ-195.md)' 行の直後にGAZ-196・GAZ-197行を挿入し「## 地誌・行政史料（195件）」→197件を更新。
  * '- [BOOK-330](books/BOOK-330.md)' 行の直後にBOOK-331行を挿入し「## 書籍・雑誌・メディア（329件）」→330件を更新。
  * 「資料ファイル総数: 1845件」→1848件を更新。
  （各カウント・アンカーはともに1箇所であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.330-bullet.txt')

GAZ196_LINE = (
    '- [GAZ-196](gazetteers/GAZ-196.md) — kotobank「弦巻村」項（平凡社『日本歴史地名大系』（東京都の地名）世田谷区項の部分転載）（2026-11-26・第330回・当該頁の直接取得で確認）'
    '— ①永和2年（1376）吉良治家寄進状〔鶴岡八幡宮文書〕「武蔵国世田谷郷内上絃巻半分」寄進＋同日付吉良治家書下写〔鶴岡神主家伝文書〕'
    '＝GAZ-195『日本地理志料』世田ヶ谷条が引いた「鎌倉八幡宮永享元年ノ文書」の文書群（鶴岡＝鎌倉八幡宮）が弦巻の文書を実際に伝来することの独立裏付け（事典転載文言ゆえ文書本体は未確認）'
    '②吉良治家＝世田谷御所起業の人物（GAZ-195吉良家譜と接続）＝「弦巻」の文書初出が世田谷御所の領有・寄進行為と一体の系譜'
    '③「上絃巻」の上下区分地名の用例候補 ④文化庁文化遺産データベース[鶴岡八幡宮文書（二百二十四通）](https://online.bunka.go.jp/db/heritages/detail/186632)詳細頁の直接open'
    'で鶴岡八幡宮文書131通＋相承院文書93通・15巻・鎌倉〜江戸・重文指定1983-6-6・所有者鶴岡八幡宮を確認（永和2年寄進状そのものの目録確認は未了＝次回課題）'
    ' ／ 旧番号: — ／ Web事典転載・DB詳細頁の機械取得で確認（原本文書・目録本は未見）（ai）'
)

GAZ197_LINE = (
    '- [GAZ-197](gazetteers/GAZ-197.md) — 北豊島郡教育会『北豊島郡史概説』（1910・NDL次世代DL 763773・bibId 000000425679・74p・全文ZIP）（2026-11-26・第330回・lab「弦巻川」contentonly掃引54件で既収録を除いた唯一の新規本文書）'
    '— 鬼子母神条「鬼子母神は大字雜司ケ谷大行院內にあり永祿四年村内絃卷川附近毎夜星降り且柳下氏所藏の大釜三日鳴動せるを以て家人奇異ノ思ヲなすに'
    '同年五月十六日絃卷川の邊俚俗〓土と云ふ所の同氏所持田中より佛像一驅を堀出せり…爾來此釜を產湯の釜と稱し每歲五月十六日草薙祭と謂ひて祭祀を行ひたりと云ふ今之れを柳下家に秘藏せり」'
    '＝①鬼子母神（雑司ヶ谷）の佛像出現地を「絃卷川の邊」と河川名つきで明記②掘出月日（永禄4年5月16日）③產湯の釜・毎歳5月16日草薙祭・柳下家秘蔵（repo未収録の縁起細部）'
    '＋「俚俗〓土」の原字は1903年東京府『北豊島郡農業志料』（GOV-196第330回追記）のカタカナ本文「俚俗清士」と2書間判読対立（原字照合待ち）'
    '＋雑司ヶ谷地名由来の雑士柳下若狹土着説（GAZ-048風土記稿の再録）＋矢端川条「これ小石川の上流なり」・藤橋・上橋・寂法橋・東福寺橋（風土記稿巣鴨村条と同文の橋リストの再録対照・帰属川名問題の1910年用例）'
    '＋千川・水窪・水久保・音羽川の直接文言なしの陰性'
    ' ／ 旧番号: — ／ OCR全文確認（文言は原文画像との照合を要する）（ai）'
)

BOOK331_LINE = (
    '- [BOOK-331](books/BOOK-331.md) — 柏崎具元『事跡合考』（瀬名貞雄編・斎藤幸孝写・文化2年〔1805〕写・上下5巻・大田南畝・近藤正齋旧蔵本による写本・森銑三らの調査で完本・'
    'TOKYOアーカイブ画像公開＝東京都立図書館東京誌料文庫・請求記号023-39-1/東023-039-001・資料コード4300923046・パブリックドメイン・詳細頁0000000005-00253218/19）（2026-11-26・第330回・都立図書館デジタルアーカイブ横断検索「上水」20件の全件突合で検出・repo初出）'
    '— アーカイブ資料解説（『江戸地誌とその周辺』図録解説p.6由来）文言「大道寺友山の『落穂集追加』に増補したもの。江戸城の沿革、大名屋敷のこと、社寺の由来、町方普請のこと、'
    '吉原の起源、歌舞伎のこと、上水のこと、聖堂のこと等々江戸に関する諸々の事実を考証している」＝repoで引用書目・引用文言としてのみ存在した『落穂集（追加）』系'
    '（GAZ-017上水篇参考書目・GAZ-093落穂集追加引用・GAZ-099引用書目）の実物が都立で画像公開されている所在記録＋「上水のこと」を考証対象と明記＝'
    '上水章の文言走査がhuman目視で可能になった段階（本文未見・千川上水言及の有無は未確認）'
    '＋同検索の陰性整理（三十六花撰「東都押上水仙花」=false positive・広重浮世絵群=見送り済・上水北小日向小石川辺絵図=MAP-158既収録・東京市水道局系近代刊行物=現代水道スコープ外）'
    ' ／ 旧番号: — ／ アーカイブ詳細頁・書誌・解説文言の機械取得で確認（本文画像の文言走査は未実施）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第330回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第330回:' in readme:
        print('README: 第330回bullet already present; skip')
    else:
        must_one(readme, '- **第329回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第329回:')]
        assert len(hits) == 1, 'README anchor 第329回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    changed = False

    if '[GAZ-196](gazetteers/GAZ-196.md)' in index:
        print('INDEX: GAZ-196 line already present; skip')
    else:
        must_one(index, '- [GAZ-195](gazetteers/GAZ-195.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GAZ-195](gazetteers/GAZ-195.md)')]
        assert len(hits) == 1, 'INDEX anchor GAZ-195 found %d' % len(hits)
        lines.insert(hits[0] + 1, GAZ196_LINE)
        lines.insert(hits[0] + 2, GAZ197_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GAZ-196/197 lines inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 地誌・行政史料（195件）')
        index = index.replace('## 地誌・行政史料（195件）', '## 地誌・行政史料（197件）', 1)
        print('INDEX: 地誌 count 195->197')

    if '[BOOK-331](books/BOOK-331.md)' in index:
        print('INDEX: BOOK-331 line already present; skip')
    else:
        must_one(index, '- [BOOK-330](books/BOOK-330.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-330](books/BOOK-330.md)')]
        assert len(hits) == 1, 'INDEX anchor BOOK-330 found %d' % len(hits)
        lines.insert(hits[0] + 1, BOOK331_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: BOOK-331 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 書籍・雑誌・メディア（329件）')
        index = index.replace('## 書籍・雑誌・メディア（329件）', '## 書籍・雑誌・メディア（330件）', 1)
        print('INDEX: 書籍 count 329->330')

    if changed:
        must_one(index, '資料ファイル総数: 1845件')
        index = index.replace('資料ファイル総数: 1845件', '資料ファイル総数: 1848件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (地誌195->197・書籍329->330・総数1845->1848)')


if __name__ == '__main__':
    main()
