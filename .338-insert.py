#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第338回: READMEに実行記録bulletを挿入しINDEXにMAP-230・MAP-231行を追加するヘルパー。
使い方: python3 .338-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第337回:' 行の直後に .338-bullet.txt の1行を挿入（'- **第338回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-230/231の2行をMAP-229行の直後に挿入し「## 地図・絵図（229件）」→231件・
  「資料ファイル総数: 1858件」→1860件を更新（第338回のpush_filesでINDEXの行挿入・計数更新が
  済んでいる場合は検出して何もしない＝冪等）。
  （アンカー・計数文字列は一意であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.338-bullet.txt')

MAP230_LINE = '- [MAP-230](maps/MAP-230.md) — 仲田惟善著『（題簽）東都近郊圖　全』（TOKYOアーカイブ・文政8[1825]上梓・文政13[1830]改正〔奥付文言〕・請求記号050-2/東050-002・資料コード4300036994・PD・全1コマ・zoom約1.4MB）（2026-11-26・第338回・TOKYOアーカイブ「用水」掃引で取得・repo初出）— [BOOK-234](books/BOOK-234.md)（小平市史）が千川上水桜堤文言（「上水の両岸五十余町ノ間…」同80頁）の引用原典として挙げる『東都近郊図』（文政8）の所在特定。序文言「小社或ハ用水ノ如キニ至テハ畧セシモノアリ」＝用水略画の凡例文言（図上の非記載を実在否定に使う根拠にはしない）・範囲文言（東小金舟橋・南羽田神奈川・西府中日野・北大宮岩槻）＝四河川全流域を含む江戸近郊図・千川上水の口（取水口）周辺・小金井桜堤の読図候補（引用文言の図上位置確認はhuman閲覧待ち・詳細頁の年代欄表記との照合は次回） ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像リストAPI確認・読図未実施）（ai）'
MAP231_LINE = '- [MAP-231](maps/MAP-231.md) — 東京府『東京府民政史料展覧会記念絵葉書（小泉次太夫四ケ領用水堀割普請之図）』（TOKYOアーカイブ・絵葉書・写真帖・出版者東京府・袋入・請求記号/10・21B/3001/20A・資料コード1114684046・年代欄なし・PD・画像1コマ・zoom約644.6KB）（2026-11-26・第338回・TOKYOアーカイブ「用水」掃引で取得・repo初出）— 内容欄「川崎平右衛門伊奈半左衛門謝恩塔(北多摩郡小平村榎戸新田所在)＋小泉次太夫四カ領用水掘割普請之図＋西多摩郡五日市町小和田広徳寺文書・平井郷伝馬定書」＝「謝恩塔」repo初出文言＝千川上水開削請負人川崎平右衛門（定孝＝GOV-341・BOOK-234と同一人物）と関東郡代伊奈家の顕彰石塔の所在記録（同定対照＝国分寺市妙法寺の宝篋印塔〔国分寺市指定・寛政11[1799]建立〕・国立市観音寺供養塔〔寛政7〕候補・石塔の同一性は画像判読まで断定しない）＋「四ヶ領用水」repo初出用語＝多摩川両岸の二ヶ領用水＋六郷用水の総称（用水奉行小泉次大夫・慶長16[1611]完成＝千川上水・四河川とは水系が別・GAZ-057「次太夫堀」呼称の並行は本文照合まで断定しない・複製元図面の同定は判読待ち） ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁・画像リストAPI確認・画像判読未実施）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第338回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第338回:' in readme:
        print('README: 第338回bullet already present; skip')
    else:
        must_one(readme, '- **第337回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第337回:')]
        assert len(hits) == 1, 'README anchor 第337回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    if '- [MAP-230](maps/MAP-230.md)' in index:
        print('INDEX: MAP-230 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [MAP-229](maps/MAP-229.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-229](maps/MAP-229.md) — ')]
        assert len(hits) == 1, 'INDEX anchor MAP-229 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [MAP230_LINE, MAP231_LINE]
        index = '\n'.join(lines)
        must_one(index, '## 地図・絵図（229件）')
        index = index.replace('## 地図・絵図（229件）', '## 地図・絵図（231件）', 1)
        must_one(index, '資料ファイル総数: 1858件')
        index = index.replace('資料ファイル総数: 1858件', '資料ファイル総数: 1860件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: MAP-230/231 inserted + counts updated (地図229->231・総数1858->1860)')


if __name__ == '__main__':
    main()
