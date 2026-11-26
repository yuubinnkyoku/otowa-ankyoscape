#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第341回: READMEに実行記録bulletを挿入しINDEXにGOV-609〜611・MAP-236〜240行を追加するヘルパー。
使い方: python3 .341-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第340回:' 行の直後に .341-bullet.txt の1行を挿入（'- **第341回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: GOV-609〜611の3行をGOV-608行の直後に、MAP-236〜240の5行をMAP-235行の直後に挿入し
  「## 地図・絵図（235件）」→240件・「## 行政・公的機関（606件）」→609件・
  「資料ファイル総数: 1866件」→1874件を更新（既に済んでいる場合は検出して何もしない＝冪等）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.341-bullet.txt')

GOV609_LINE = '- [GOV-609](gov/GOV-609.md) — 東京府淀橋土木事務所編纂『東京府豐多摩北豐島兩郡道路橋梁明細書』（1909.11・宮本印刷所・58p・23cm・TOA tilcod 0000000009-00247796・資料コード7113303709・請求記号T/514.0/5017/1909・PD・画像欄〔全画面表示〕あり）（2026-11-26・第341回・TOA「豊嶋」143件掃引で取得・repo grep 0件＝repo初出）— 豊多摩・北豊島両郡の橋梁名簿＝谷端川・千川・弦巻川・水窪川架橋群の1909年定点候補＝GOV-606橋々銘書・GOV-607藤橋・GOV-608千川下流橋梁群・GAZ-002巣鴨3橋（1918）の対照史料候補（収録橋の母集団の範囲・書式は本文未確認＝判読第一確認点は谷端川・千川の橋がどこまで載るか・橋名1909定点〜猫俣橋1933構造図への接続） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・本文文言は未確認）（ai）'
GOV610_LINE = '- [GOV-610](gov/GOV-610.md) — 東京市臨時市域拡張部『北豊島郡各町村現状調査』3冊（巻次第1-7・第8-13・第14-20・請求記号T/40・31/2/G1-7・G8-13・G14-20）＋『市域拡張調査資料 [北豊島郡]』合綴2冊（第1-10・第11-20・注記＝合綴・T/0・317/421/G4・G5）のTOAレコード群（1931・各1冊・23cm・いずれもPD・画像欄〔全画面表示〕あり・tilcod 0000000009-00040388/40279/40297/00005301/00005302）（2026-11-26・第341回・TOA「豊嶋」掃引で取得）— 既収録GOV-45x各町村現状調査群の原画像がweb公開されているルートの所在記録＝分冊の町村構成（掃引時観察では第1-7＝南千住〜西巣鴨・第8-13＝王子・板橋・高田・長崎等・第14-20＝中新井・上板橋・練馬群等）が目次確認で確定すれば谷端川（滝野川・巣鴨・西巣鴨・上板橋）・千川（王子・中新井）・弦巻川・谷端川源流（高田・長崎）の該当町村だけの狙い撃ち判読が可能になる候補（町村構成は観察レベルで断定しない） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・本文文言は未確認）（ai）'
GOV611_LINE = '- [GOV-611](gov/GOV-611.md) — 東京市豊島区『東京市豊島区事務報告書・東京市豊島区財産表 昭和9年』（1935.2・54p・24cm・TOA tilcod 0000000009-00054468・資料コード3121121599・請求記号T/43・31/3010/34・PD・画像欄〔全画面表示〕あり）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo grep 0件＝repo初出）— 区成立（1932）直後の豊島区政年報＋区有財産表＝弦巻川暗渠化着工（1931〜）直後の行政側定点で水路関係の区帰属・区有財産の候補（財産表の項目形式・水路の記載有無は全て未確認＝human判読待ち・昭和10年以降の継続巻の有無も未確認） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・本文文言は未確認）（ai）'

MAP236_LINE = '- [MAP-236](maps/MAP-236.md) — 東京逓信管理局『東京府北豊島郡長崎村豊多摩郡落合村』（1911.7・1:5000・色刷・100×80cm(折りたたみ20cm)・逓信協会・TOA tilcod 0000000008-00001482・資料コード1128751409・請求記号DT/40・29/3003/・PD・全1コマzoom約1.3MB〔ajax確認〕）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo初出）— GAZ-002「谷端川ハ長崎村より出ル細流」の源流域（長崎村）＋千川上水池域・神田川下落合側を同一図面に収める明治44年定点図＝MAP-157系列（1911）・MAP-008地籍図（1912）と同年の谷頭部読図対象（水路・池の描かれ方が第一読図点・未実施） ／ 旧番号: — ／ 所在のみ（詳細頁・ajax確認・読図は未実施）（ai）'
MAP237_LINE = '- [MAP-237](maps/MAP-237.md) — 木谷彰佑著『大東京市豊島區全圖』（旧字新町界新町名番地入・色刷40×55cm・縮尺決定不能・東京交通社・TOA tilcod 0000000008-00255339・資料コード7112493467・請求記号T/43・290/5027/1932・PD・全1コマzoom約1.3MB〔ajax確認〕・詳細頁の出版年欄は空欄で1932は請求記号末尾による〔推定・要年確認〕）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo初出）— 区成立（1932）直後の新旧町名対照（旧字新町界新町名番地入）を図面自体に持つ豊島区全区図＝区制移行期の新旧区割対照材料・MAP-233（1930.6高田町全圖）とMAP-160（1932.12）の間の全区定点（図郭・水路描線は未判読・読図は未実施） ／ 旧番号: — ／ 所在のみ（詳細頁・ajax確認・読図は未実施）（ai）'
MAP238_LINE = '- [MAP-238](maps/MAP-238.md) — 東部遞信局編纂『東京府北豐嶋郡上板橋村』（1917.8・大正6年1月調査・1:5000・色刷94×64cm・遞信協會・共同刊行川流堂小林又七・カバー題「番地界入東京府北豐島郡上板橋村全圖」・TOA tilcod 0000000008-00002249・資料コード5005533987・請求記号T/44・290/5005/1917・PD・画像欄〔全画面表示〕あり）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo初出）— 谷端川中流域（上板橋村）の大正6年（1917.1調査）番地界図＝1911系列と1922.9板橋町全圖（MAP-239）の間の補完点（番地界体裁＝水路は地番境界としてのみ描かれる可能性・非記載を実在否定に使わない・コマ数は次回ajax確認・読図は未実施） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'
MAP239_LINE = '- [MAP-239](maps/MAP-239.md) — 東京遞信局編纂『東京府北豐島郡板橋町』（1922.9・大正11年8月調査・第2版＝第1版の先行存在が版表示から確認できる〔所在は未確認〕・1:5000・色刷78×61cm・遞信協會・共同刊行川流堂小林又七・カバー題「番地界入東京府北豐島郡板橋町全圖」・TOA tilcod 0000000008-00002247・資料コード5005533969・請求記号T/44・290/5004/1922・PD・画像欄〔全画面表示〕あり）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo初出）— 谷端川下流・千川末端域（板橋町）の大正11年番地界図＝MAP-238（1917.8上板橋村）と隣接対で番地界図1911→1917→1922→1929-31（NDL 8312068）の時系列・MAP-115（1922.6雨水流下係数図）と同年（コマ数は次回ajax確認・読図は未実施） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'
MAP240_LINE = '- [MAP-240](maps/MAP-240.md) — 東京逓信管理局編『東京府北豊島郡王子町』（1911.11・1:5000・64×100cm・遞信協會・TOA tilcod 0000000008-00001447・資料コード1128265828・請求記号DT/42・29/3001/・PD・画像欄〔全画面表示〕あり）（2026-11-26・第341回・TOA「豊嶋」掃引で取得・repo初出）— 千川上水系統の前提地域（王子町＝滝野川西隣・石神井川沿い・音無川域）の明治44年図＝千川の流末・分水の環境前提（本図内の千川関連描線の有無は読図まで断定しない・MAP-157系列と同年・コマ数は次回ajax確認） ／ 旧番号: — ／ 所在のみ（詳細頁確認・コマ数・読図は未実施）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第341回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第341回:' in readme:
        print('README: 第341回bullet already present; skip')
    else:
        must_one(readme, '- **第340回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第340回:')]
        assert len(hits) == 1, 'README anchor 第340回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    changed = False

    if '- [GOV-609](gov/GOV-609.md)' in index:
        print('INDEX: GOV-609 line already present; skip')
    else:
        must_one(index, '- [GOV-608](gov/GOV-608.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-608](gov/GOV-608.md) — ')]
        assert len(hits) == 1, 'INDEX anchor GOV-608 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [GOV609_LINE, GOV610_LINE, GOV611_LINE]
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GOV-609〜611 inserted')

    if '- [MAP-236](maps/MAP-236.md)' in index:
        print('INDEX: MAP-236 line already present; skip')
    else:
        must_one(index, '- [MAP-235](maps/MAP-235.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [MAP-235](maps/MAP-235.md) — ')]
        assert len(hits) == 1, 'INDEX anchor MAP-235 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [MAP236_LINE, MAP237_LINE, MAP238_LINE, MAP239_LINE, MAP240_LINE]
        index = '\n'.join(lines)
        changed = True
        print('INDEX: MAP-236〜240 inserted')

    if changed:
        must_one(index, '## 地図・絵図（235件）')
        index = index.replace('## 地図・絵図（235件）', '## 地図・絵図（240件）', 1)
        must_one(index, '## 行政・公的機関（606件）')
        index = index.replace('## 行政・公的機関（606件）', '## 行政・公的機関（609件）', 1)
        must_one(index, '資料ファイル総数: 1866件')
        index = index.replace('資料ファイル総数: 1866件', '資料ファイル総数: 1874件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (地図235->240・行政606->609・総数1866->1874)')


if __name__ == '__main__':
    main()
