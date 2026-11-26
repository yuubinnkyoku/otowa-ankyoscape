#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第340回: READMEに実行記録bulletを挿入しINDEXにMAP-232〜235・BOOK-334行を追加するヘルパー。
使い方: python3 .340-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第339回:' 行の直後に .340-bullet.txt の1行を挿入（'- **第340回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-232〜235の4行をMAP-231行の直後に、BOOK-334行をBOOK-333行の直後に挿入し
  「## 地図・絵図（231件）」→235件・「## 書籍・雑誌・メディア（332件）」→333件・
  「資料ファイル総数: 1861件」→1866件を更新（第340回のpush_filesでINDEXの行挿入・計数更新が
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
BULLET = os.path.join(HERE, '.340-bullet.txt')

MAP232_LINE = '- [MAP-232](maps/MAP-232.md) — 『染井王子巣鴨辺絵図』（尾張屋板切絵図・戸松昌訓図・[金鱗堂]尾張屋清七・嘉永7[1854]・東京誌料5シート0521-13系〔42393色刷45.0×49.8cm・4300037141／42394色刷（資料解説＝『江戸の町づくり』リーフレットp.13「此辺染井村植木屋多シ」＝ソメイヨシノ文言）・4300037150／42395無彩47.7×52.4cm・4300037169／42396色刷・4300037178／42397色刷・4300037187〕・原題簽「巢鴨繪圖　全」・TOA・PD・各シート画像欄あり）（2026-11-26・第340回・TOA「巣鴨」24件掃引で取得・repo初出）— 谷端川中流（巣鴨村）＋千川末端域（滝野川）を含む尾張屋板巣鴨図＝原題簽「巢鴨繪圖　全」・刊年1854がMAP-023『巣鴨邊絵図』（1854・二次転記・原図未確認）と一致する同一図候補（異同は画像照合まで断定しない）・染井植木屋文言＝巣鴨染井花見文化の図像側背景群 ／ 旧番号: — ／ 所在のみ（アーカイブ詳細頁確認・コマ数・読図は未実施）（ai）'
MAP233_LINE = '- [MAP-233](maps/MAP-233.md) — 高田町『東京府北豊嶋郡高田町全圖』（昭和5年現在・1930.6・高田町(東京府)発行・1:4000・60×85cm・地図1枚・注記＝青焼き・TOA tilcod 0000000008-00001896・資料コード5003420400・請求記号T/43・290/5006/1930・件名＝豊島区・PD・画像欄〔全画面表示〕あり）（2026-11-26・第340回・TOA「高田」29件掃引で取得・第96回の所在未確認条件を解消）— 弦巻川の1929下水道計画→1930.12事業認可→1931暗渠化着工時系列の直前の1930.6定点図＝図上で弦巻川が開渠線として描かれるかが第一読図点・丸池・旧神田上水路・高田町下水道設計図（GOV-167）との対照候補（描線の有無だけで開渠・暗渠の実態は断定しない・青焼き＝複製本の体裁で原本の作成主体は未確認） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'
MAP234_LINE = '- [MAP-234](maps/MAP-234.md) — 東京遞信局編纂『番地界入東京府北豐島郡高田町豐多摩郡戸塚町全圖』（1920.9・第2版・1:5000・73×67cm・地図1枚色刷・遞信協會・共同刊行川流堂小林又七・TOA tilcod 0000000008-00002250・資料コード5005533996・請求記号T/36・290/5003/1920・件名＝新宿区・PD・画像欄〔全画面表示〕あり）（2026-11-26・第340回・TOA「高田」29件掃引で取得・repo初出）— MAP-157（1911年四十四年調査番地界入）とNDL 8312068（1929〜31川流堂系列）の間の中間版＝弦巻川流域（高田町＋戸塚町＝神田川上流両岸）の番地界図1911→1920→1929-31の3点系列（第2版表示＝明治44年系列の改版・版本関係は未照合）・「番地界入」の体裁上、水路は行政境界としてのみ描かれる可能性（非記載を実在否定に使わない） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'
MAP235_LINE = '- [MAP-235](maps/MAP-235.md) — 『牛込市谷大久保絵図』（尾張屋板切絵図15・戸松昌訓図・金鱗堂尾張屋清七・嘉永7[1854]／安政4[1857]改・木版無彩・45.8×49.8cm・（題簽（後））「大久保高田」・TOA tilcod 0000000013-00042323・東京誌料0443-18/東0443-018・資料コード4300036143・PD・画像欄〔全画面表示〕あり）（2026-11-26・第340回・TOA「豊嶋」掃引で取得・repo初出）— 図域＝牛込・市谷・大久保＝弦巻川・江戸川合流点の南側台地（戸山＝尾張徳川家下屋敷→陸軍戸山学校方面）＝図域の縁が高田側に達するか・水路描線の有無は未判読（MAP-158収録近吾堂板「大久保戸山高田辺之図」と同域別版元の対校候補） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'
BOOK334_LINE = '- [BOOK-334](books/BOOK-334.md) — 東京府北豊島郡西巣鴨町役場編『西巣鴨町誌』（1932・402p・20cm・TOA tilcod 0000000009-00005245・資料コード1124280764・請求記号T/43・20/3/・PD・全288コマ〔ajax画像リストAPI確認〕）（2026-11-26・第340回・TOA詳細頁・画像リストAPI・repo grep 0件＝repo初出）— 西巣鴨町（1932年東京市編入直前＝町政最終期）の公式町誌の画像公開＝GOV-207（1938年報・西巣鴨町4排水区〔谷端川138ha・音羽100ha・谷田川17ha・石神井川区〕）とrzeka「マンホール(170)」転記数値（README西巣鴨町蓋の項の一次引用経路）の出所とされる原典＝判読第一確認点は下水道章の4排水区文言・「総面積455ha」文言の有無・橋梁章（GOV-606橋々銘書地方二番組の藤橋・東福寺橋・寂法橋・上之橋・猫股橋・祇園橋の町域対応）・1932年時点の谷端川開渠/暗渠記述（文言は全て未確認＝human判読待ち） ／ 旧番号: — ／ 書誌・画像公開確認（本文文言は未確認）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第340回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第340回:' in readme:
        print('README: 第340回bullet already present; skip')
    else:
        must_one(readme, '- **第339回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第339回:')]
        assert len(hits) == 1, 'README anchor 第339回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    changed = False

    if '- [MAP-232](maps/MAP-232.md)' in index:
        print('INDEX: MAP-232 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [MAP-231](maps/MAP-231.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-231](maps/MAP-231.md) — ')]
        assert len(hits) == 1, 'INDEX anchor MAP-231 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [MAP232_LINE, MAP233_LINE, MAP234_LINE, MAP235_LINE]
        index = '\n'.join(lines)
        changed = True
        print('INDEX: MAP-232〜235 inserted')

    if '- [BOOK-334](books/BOOK-334.md)' in index:
        print('INDEX: BOOK-334 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [BOOK-333](books/BOOK-333.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-333](books/BOOK-333.md) — ')]
        assert len(hits) == 1, 'INDEX anchor BOOK-333 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [BOOK334_LINE]
        index = '\n'.join(lines)
        changed = True
        print('INDEX: BOOK-334 inserted')

    if changed:
        must_one(index, '## 地図・絵図（231件）')
        index = index.replace('## 地図・絵図（231件）', '## 地図・絵図（235件）', 1)
        must_one(index, '## 書籍・雑誌・メディア（332件）')
        index = index.replace('## 書籍・雑誌・メディア（332件）', '## 書籍・雑誌・メディア（333件）', 1)
        must_one(index, '資料ファイル総数: 1861件')
        index = index.replace('資料ファイル総数: 1861件', '資料ファイル総数: 1866件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (地図231->235・書籍332->333・総数1861->1866)')


if __name__ == '__main__':
    main()
