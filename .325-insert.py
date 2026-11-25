#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第325回: READMEに実行記録bulletを挿入しINDEXにMAP-224・BOOK-329行を追加するヘルパー。
使い方: python3 .325-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第324回:' 行の直後に .325-bullet.txt の1行を挿入（'- **第325回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md:
  * '- [MAP-223](maps/MAP-223.md)' 行の直後にMAP-224行を挿入し「## 地図・絵図（223件）」→224件を更新。
  * '- [BOOK-328](books/BOOK-328.md)' 行の直後にBOOK-329行を挿入し「## 書籍・雑誌・メディア（327件）」→328件を更新。
  * 「資料ファイル総数: 1839件」→1841件を更新。
  （各カウント・アンカーはともに1箇所であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.325-bullet.txt'

MAP224_LINE = (
    '- [MAP-224](maps/MAP-224.md) — 『東京市史稿 上水篇』一、綴図（東京都公文書館蔵・資料番号図1-2-3-1・港区史第2巻104-105頁掲載'
    '・ADEAC港区zu000570-110021・単図3533×2261px・インターネット公開）'
    '（2026-11-25・第325回・jpsearch→ADEAC目録→Deep Zoomタイル取得＋AI画像解析）'
    '— 上水篇第1の綴図の図像レベル初アクセス（NDL上水篇全巻は送信制限のため代替経路）:'
    'AI画像解析（vision・タイル9枚+全体縮小）で図上の「千川」「上水」（複数タイルで独立再現）・「弦巻」「水窪」・「水門」「春日町」'
    '「日光道」「内藤伊賀守」「西長寺」「東長寺」「本陣」「高札場」等の文言を観察'
    '（vision小タイル判読ゆえ誤読・候補語迎合の危険を含み千川・上水・弦巻・水窪の複数タイル再現性だけを記録の核とする＝原図の実物判読まで確定しない）'
    '＝千川上水本流と弦巻・水窪方面の水系が同一紙面に乗りうる江戸期水路図の公開所在としてrepo初'
    '（日光道・内藤伊賀守=四谷・内藤新宿側と整合・図の範囲・年代は要原図確認・BLOG-113千川上水絵図〔上水篇第1付録〕との図面対校は次回課題）'
    ' ／ 旧番号: — ／ 電子画像+AI画像解析（原図判読は要実物確認）（ai）'
)

BOOK329_LINE = (
    '- [BOOK-329](books/BOOK-329.md) — 港区『港区史 第2巻 通史編 近世（上）』（港区・令和3〔2021〕・ADEAC港区mp100010-110021'
    '・全510頁画像＋全文テキストHTML公開）（2026-11-25・第325回・ADEAC texthtmlで取得）'
    '— 「江戸の上水道」節（103-106頁）の「後に一七世紀末までには、玉川上水から分水して、三田・千川・青山の諸上水ができ…四上水が加わった（図1-2-3-1）」'
    '＝21世紀自治体史による千川上水の四上水枠組みでの位置づけ文言（元禄9年開削通説と整合する概括）'
    '＋図1-2-3-1『東京市史稿 上水篇』一、綴図（=MAP-224）のキャプション「『東京市史稿 上水篇』一から転載」'
    '＋図1-2-3-2「貞享上水図」港区域＝NDL上水篇付図（pid/10337861）から転載・一部加筆という情報＝NDL附図に貞享上水図が含まれるという内容判別'
    '（附図自体は送信制限で未見・玉川上水四ツ谷分水A-I記号・青山上水万治3年1660・三田上水寛文4年1664・享保7年1722廃止の年次列挙も収録）'
    '＋ht000630「江戸の下水道」（README既出の大下水定義文言）の書籍級登録化'
    '（第2巻全体の弦巻・水窪・谷端・音羽の直接文言の全走査・資料編2-1/2-2の掃引は未了・次回課題）'
    ' ／ 旧番号: — ／ 全文テキストHTML確認（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第325回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第325回:' in readme:
        print('README: 第325回bullet already present; skip')
    else:
        must_one(readme, '- **第324回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第324回:')]
        assert len(hits) == 1, 'README anchor 第324回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    changed = False

    if '[MAP-224](maps/MAP-224.md)' in index:
        print('INDEX: MAP-224 line already present; skip')
    else:
        must_one(index, '- [MAP-223](maps/MAP-223.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-223](maps/MAP-223.md)')]
        assert len(hits) == 1, 'INDEX anchor MAP-223 found %d' % len(hits)
        lines.insert(hits[0] + 1, MAP224_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: MAP-224 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 地図・絵図（223件）')
        index = index.replace('## 地図・絵図（223件）', '## 地図・絵図（224件）', 1)
        print('INDEX: 地図 count 223->224')

    if '[BOOK-329](books/BOOK-329.md)' in index:
        print('INDEX: BOOK-329 line already present; skip')
    else:
        must_one(index, '- [BOOK-328](books/BOOK-328.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-328](books/BOOK-328.md)')]
        assert len(hits) == 1, 'INDEX anchor BOOK-328 found %d' % len(hits)
        lines.insert(hits[0] + 1, BOOK329_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: BOOK-329 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 書籍・雑誌・メディア（327件）')
        index = index.replace('## 書籍・雑誌・メディア（327件）', '## 書籍・雑誌・メディア（328件）', 1)
        print('INDEX: 書籍 count 327->328')

    if changed:
        must_one(index, '資料ファイル総数: 1839件')
        index = index.replace('資料ファイル総数: 1839件', '資料ファイル総数: 1841件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (地図223->224・書籍327->328・総数1839->1841)')


if __name__ == '__main__':
    main()
