#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第323回: READMEに実行記録bulletを挿入しINDEXにBOOK-328・GOV-602行を追加するヘルパー。
使い方: python3 .323-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第322回:' 行の直後に .323-bullet.txt の1行を挿入（'- **第323回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: '- [BOOK-327](books/BOOK-327.md)' 行の直後にBOOK-328行を・'- [GOV-601](gov/GOV-601.md)' 行の直後にGOV-602行を挿入し、
  書籍326→327件・行政599→600件・資料ファイル総数1836→1838件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.323-bullet.txt'

BOOK328_LINE = (
    '- [BOOK-328](books/BOOK-328.md) — 下谷区『下谷区史〔本編〕』（下谷区・1935・1920866）'
    '（2026-11-25・第323回・lab全文検索→全文ZIPで取得）'
    '— 千川上水廃止再興章の全文試読: ①明和6年2月出願の願人3人のうち孫兵衞・幸左衞門が離反し千川善藏と浅草阿部川町三郎兵衞が加入（repo初出の願人交代記録）'
    '②牧野大隅守成賢・山川下総守貞幹・根岸九郎左衞門鎮衞の堀割の功での賞賜＋天明6年閏10月廃止の明記'
    '③『曳尾庵随筆』引用文言（repo grep新出書名）＋水役金＝町方小間1間に付き1歩（天明2年8月開始・天明6年5-8月半減・武家地100石=小間2間分）'
    '④御府内備考車坂町条転写の水銭404文/月＝GAZ-114写本側204文との数値対立の新例＋「野方用水」呼称（repo grep新出）'
    '⑤廃止時の上水請負人貸附金2万90両余免除と人名群（神田相生町長十郎・宇助・平永町長右衞門・佐久間町幸右衞門/吉兵衞・小川村名主彌次郎＝repo初出・GOV-218の2,753両系との金額対立は断定せず）'
    '⑥千川文書の刊行抄出（本郷4丁目→浅草寺御殿30町余・巣鴨→鳥越橋5,100間・惣間数1万2884間=5里34町44間・下谷御組合戸樋94間/240間余・龍樋・知行高32万3000石の大名リスト＝GOV-567との文言照合が次回課題）'
    '⑦明治千川水道の下谷ルート（滝野川堰→王子→巣鴨陰樋→駕籠町→曙町→本郷3丁目分流→車坂→浅草・明治40年6月廃止）'
    '⑧市区改正「萬世橋下水渠」「藍染川→荒川排水路」計画（842間暗渠・不忍池放流・芝浦送致）＋谷端川辺泥炭層「ケトウ」観察'
    '（OCR表組崩壊甚大箇所あり・文言・数値はすべて原画像照合必須）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・くずし字崩壊大・文言は要原文照合）（ai）'
)

GOV602_LINE = (
    '- [GOV-602](gov/GOV-602.md) — 東京都公文書館・クロス検索「架橋願」（全15コレクション0件）・「徳川昭武」（collection_04のみ）'
    '（2026-11-25・第323回・POSTレシピで取得）'
    '— 382008「徳川昭武橋梁自費橋梁架換願」（明治15年1-3月・回議録〔道路・橋梁・下水等之甲・土木課〕・612.B4.09(054)・MF府明Ⅱ明15-057・コマ0006-0619）'
    '＝GOV-591⑦a「徳川昭武自費架橋願 15年1月回議録に付て看るへし」の参照先回議録の本体特定（次回課題①の解消）'
    '＋425489「徳川昭武新小梅橋落成届 代理山中新」（612.B5.02(039)・MF府明Ⅱ明15-059・コマ0577-1196）＝橋名「新小梅橋」確定（repo初出）'
    '＝参照文言→架換願→落成届の3点が目録レベルで揃った明治15年の橋梁行政実務チェーン'
    '＋架換対象河川は本文未見のため断定しない（MF府明Ⅱ明15-057/059の閲覧が次回課題）'
    '＋382033外囲修繕届・小梅村堤敷使用願（明治17・614.D5.08）等の周辺実務群'
    ' ／ 旧番号: — ／ 目録詳細確認（都公文書館クロス検索・詳細頁の請求番号・MF・コマまで確認・本文は未見）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def insert_after(lines, prefix, new_lines, label):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, 'anchor %r found %d times (abort)' % (prefix, len(hits))
    pos = hits[0] + 1
    for off, nl in enumerate(new_lines):
        lines.insert(pos + off, nl)
    print('%s: inserted %d line(s) after %s (line %d)' % (label, len(new_lines), prefix, hits[0] + 1))
    return lines


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第323回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第323回:' in readme:
        print('README: 第323回bullet already present; skip')
    else:
        must_one(readme, '- **第322回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第322回:')]
        assert len(hits) == 1, 'README anchor 第322回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    book_done = '[BOOK-328](books/BOOK-328.md)' in index
    gov_done = '[GOV-602](gov/GOV-602.md)' in index
    if book_done and gov_done:
        print('INDEX: BOOK-328・GOV-602 lines both present; skip')
        index_unchanged = True
    else:
        index_unchanged = False
        lines = index.split('\n')
        if not book_done:
            must_one(index, '- [BOOK-327](books/BOOK-327.md)')
            lines = insert_after(lines, '- [BOOK-327](books/BOOK-327.md)', [BOOK328_LINE], 'INDEX-BOOK')
        if not gov_done:
            must_one(index, '- [GOV-601](gov/GOV-601.md)')
            lines = insert_after(lines, '- [GOV-601](gov/GOV-601.md)', [GOV602_LINE], 'INDEX-GOV')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 書籍・雑誌・メディア（326件）', '@@BOOKHEAD@@', 1)
        index = index.replace('@@BOOKHEAD@@', '## 書籍・雑誌・メディア（327件）', 1)
        index = index.replace('## 行政・公的機関（599件）', '@@GOVHEAD@@', 1)
        index = index.replace('@@GOVHEAD@@', '## 行政・公的機関（600件）', 1)
        index = index.replace('資料ファイル総数: 1836件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1838件', 1)
        must_one(index, '## 書籍・雑誌・メディア（327件）')
        must_one(index, '## 行政・公的機関（600件）')
        must_one(index, '資料ファイル総数: 1838件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 書籍・雑誌・メディア（326件）') == 0
        assert index.count('## 行政・公的機関（599件）') == 0
        assert index.count('資料ファイル総数: 1836件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BOOK-328・GOV-602 lines inserted; counts updated 326→327・599→600・1836→1838')

    print('INSERT-323 OK')


if __name__ == '__main__':
    main()
