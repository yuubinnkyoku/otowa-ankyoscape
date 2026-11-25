#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第321回: READMEに実行記録bulletを挿入しINDEXにGOV-599〜601・BOOK-325〜327行を追加するヘルパー。
使い方: python3 .321-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第320回:' 行の直後に .321-bullet.txt の1行を挿入（'- **第321回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: '- [GOV-598](gov/GOV-598.md)' 行の直後にGOV-599/600/601行を、
  '- [BOOK-324](books/BOOK-324.md)' 行の直後にBOOK-325/326/327行を挿入し、
  書籍・雑誌・メディア323→326件・行政・公的機関596→599件・資料ファイル総数1826→1832件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.321-bullet.txt'

GOV599_LINE = (
    '- [GOV-599](gov/GOV-599.md) — 農商務省『第二回(明治十四年)内国勧業博覧会事務報告』（農商務省・1883・801873）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 事務日録「明治13年11月17日 會塲內ハ千川上水ヲ引用スル」决定・「明治14年2月26日 千川上水無稅通水ノ儀該會社ヨリ願出之ヲ許可ス」・「同6月30日 會塲内ヘ引用ノ千川上水無代價通水」'
    '＝上野・第二回博覧会（1881）会場用水の千川上水引水の公式事務報告レベル文言（OCR日付の月帰属は要原文照合）'
    '・褒賞記事「水道會社發起人岩崎彌太郥ヘ銀牌」（會社名記載なし＝千川水道会社〔明治13年岩崎彌太郥發起〕と断定しない対校候補）'
    '＝BOOK-218「1881候補・断定保留」を強める確定情報・上野方面千川給水系列（GOV-599→GOV-323/BOOK-161〔1890〕→GOV-600〔1938〕）の起点'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・事務日録の日付対応は要原文照合）（ai）'
)

GOV600_LINE = (
    '- [GOV-600](gov/GOV-600.md) — 帝室博物館『帝室博物館略史』（帝室博物館・1938・1839532）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 附属動物園章「園內ノ使用水ハ千川上水ヲ利用シテヰル。本園創立當時ハ水量十二時間ニ二千五百三十九立方尺ヲ算シテヰタガ…十二時間ニ四千六百二十七立方尺、卽チ石數ニシテ七百二十三石七斗餘トシテ引繼ギ今日マデ之レヲ使用シテヰル」'
    '＝上野動物園（1882創立）の千川上水利用の1938年刊行時点文言・水量2,539→4,627立方尺/12hの定量化'
    '＝BOOK-161「動物園7,520余立方尺」との数値口径対校課題（「今日マデ使用」が1938年現勢か明治記録の引き写しかは要原画像照合）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)

GOV601_LINE = (
    '- [GOV-601](gov/GOV-601.md) — 東京府『東京府水害統計 明治43年』（東京府・1911・798828）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 明治43年8月豪雨の出水河川列挙（江戶川・中川・目黑川…千川上水…神田上水…石神井川等）'
    '＝1910年時点の府統計レベルで千川上水が現役の水害対象河川として列挙された文言候補'
    '（OCR列崩壊のため列挙配列・欄構成は原画像照合必須・「上水」呼称の統計書用例の1910年定点）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・表組大崩壊・文言候補扱い）（ai）'
)

BOOK325_LINE = (
    '- [BOOK-325](books/BOOK-325.md) — 社団法人日本動力協會 編『日本の発電所 東部日本篇』（日本動力協會・1937・1257046）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 内閣印刷局王子分室（王子発電所・ユングストローム水輪機550kW）罐水冷却水章'
    '「當局では深さ300米及350米の2箇の鑿井を有し、更に千川上水を導入濾過して之に充てゝゐる」'
    '＝昭和12年時点で印刷局王子工場の千川上水導入が現役だった技術資料文言・300m/350m深井併用の確認'
    '＝印刷局抄紙部の千川水利（替水約定BOOK-220→分配堰碑BLOG-095→木樋断片ORG-050→〔本条1937〕→取水停止昭和45/46系）の中間定点'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)

BOOK326_LINE = (
    '- [BOOK-326](books/BOOK-326.md) — 大町桂月『杖の跡』（至誠堂書店・1916・948875）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 「小金井の山櫻の區域盡きて、境橋架れる處より、玉川上水分派し…これを千川上水と稱す。大正四年、この上水べりに櫻と楓との若木を植る付けたりと聞く」'
    '＝千川堤植栽の伝聞文言（GOV-056大正4年説と整合・BLOG-101碑文大正3年議建説との年次対校点）'
    '・目次「千川の櫻」独立見出し＋「東長崎驛と練馬驛との間に、千川の櫻あり」'
    '＝千川堤桜の名所化の1916年文学証言（BOOK-180〔1918〕・BOOK-153〔1919〕に先行）'
    '・「一小溝路…これ千川上水也」等の植栽直後現地観察'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)

BOOK327_LINE = (
    '- [BOOK-327](books/BOOK-327.md) — 『日本橋区史 第1冊』（日本橋区・1916・951551）'
    '（2026-11-25・第321回・lab全文検索→全文ZIPで取得）'
    '— 各町誌・南茅場町条の名勝旧蹟列挙「醫王山智泉院・禿池址・明德稻荷・千川上水址・茅塲址・文七元結塚…其角宅址・荻生徂徠宅址等」'
    '＋里俗「裏茅塲町の內を千川屋敷」'
    '＝日本橋・南茅場町に「千川上水址」を旧蹟列挙した区史レベル文言'
    '（1943都版「千川上水阯」GOV-339庚申塚条とは別系統の「址」記録＝市街東西両端の「阯/址」対照点。実体は未特定で湊引水説の決定的史料とはしない）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
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
    assert bullet.startswith('- **第321回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第321回:' in readme:
        print('README: 第321回bullet already present; skip')
    else:
        must_one(readme, '- **第320回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第320回:')]
        assert len(hits) == 1, 'README anchor 第320回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[GOV-599](gov/GOV-599.md)' in index or '[BOOK-325](books/BOOK-325.md)' in index:
        print('INDEX: GOV-599 or BOOK-325 line already present; skip')
    else:
        must_one(index, '- [GOV-598](gov/GOV-598.md)')
        must_one(index, '- [BOOK-324](books/BOOK-324.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [GOV-598](gov/GOV-598.md)', [GOV599_LINE, GOV600_LINE, GOV601_LINE], 'INDEX-GOV')
        lines = insert_after(lines, '- [BOOK-324](books/BOOK-324.md)', [BOOK325_LINE, BOOK326_LINE, BOOK327_LINE], 'INDEX-BOOK')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 書籍・雑誌・メディア（323件）', '@@BOOKHEAD@@', 1)
        index = index.replace('@@BOOKHEAD@@', '## 書籍・雑誌・メディア（326件）', 1)
        index = index.replace('## 行政・公的機関（596件）', '@@GOVHEAD@@', 1)
        index = index.replace('@@GOVHEAD@@', '## 行政・公的機関（599件）', 1)
        index = index.replace('資料ファイル総数: 1826件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1832件', 1)
        must_one(index, '## 書籍・雑誌・メディア（326件）')
        must_one(index, '## 行政・公的機関（599件）')
        must_one(index, '資料ファイル総数: 1832件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 書籍・雑誌・メディア（323件）') == 0
        assert index.count('## 行政・公的機関（596件）') == 0
        assert index.count('資料ファイル総数: 1826件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-599〜601・BOOK-325〜327 lines inserted; counts updated 323→326・596→599・1826→1832')

    print('INSERT-321 OK')


if __name__ == '__main__':
    main()
