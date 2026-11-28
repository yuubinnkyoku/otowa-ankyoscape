#!/usr/bin/env python3
# retrigger: 383 (paths filter firing)
# -*- coding: utf-8 -*-
"""第383回: READMEに実行記録bulletを挿入し、INDEXにGOV-633/GOV-634の2行を挿入・計数更新するヘルパー。
使い方: python3 .383-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第382回:' 行の直後に .383-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-632 行の直後に GOV-633・GOV-634 の2行を挿入し、
  '## 行政・公的機関（630件）'→'（632件）'、'資料ファイル総数: 1977件'→'1979件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.383-bullet.txt')

LINES = {}
LINES['GOV-633'] = '- [GOV-633](gov/GOV-633.md) — 東京都公文書館クロス検索「堀割」（400件）「悪水」（556件）「排水区」（976件）「用悪水路」（189件）の初クロス掃引（第372回以来の回送課題を403解除後に実施・全頁走査）（2026-11-28・第383回・詳細頁表項目直接取得＝目録詳細確認・repo grep 0件＝repo初出）— ①**戦災復興土地区画整理換地確定図（谷端組合地区）①②の詳細確定**（pkey 000458213・cls=collection_13〔地図〕・昭和29年7月20日換地処分=1954・地図4枚60×84cm・縮尺1/600・北区滝野川7丁目・作成者谷端組合・各図69-243〜246・マイラー原図の複写物・請求番号「戦災復興－谷端組合地区」・複写可）＝谷端川旧流路（西三軒家〜北谷端〜滝野川7丁目）の1954年確定図・復興区画整理の行政側一次図面群（図面本文は未見）②下板橋宿石神井川悪水吐堰変換願（1886・pkey 490251・615.C4.16・MF府明Ⅱ明19-046）＝下板橋宿の石神井川への悪水吐堰変換の一次記録（出端川・谷端川放水路の前史候補・対象堰位置は本文未見）③橋場町639番地高田万五郎の養悪水路変換願（1885・pkey 484826・614.B3.10・「養悪水路」文言repo初出）④**上練馬村大字上練馬字田柄久保5442番地崎の悪水路敷廃止下付（1895・pkey 340243・621.A5.14・MF府明Ⅱ明28-026）＝田柄川系の水路消滅実務の一次記録**⑤下板橋字金沢の砲兵工科学校管理換受道路敷地及悪水路図・水路付替敷丈量三斜図回送（1918・pkey 1088704・陸軍東京経理部・302.B8.15・MF府大07-038）＝下板橋字金沢の軍関連水路付替実測図群⑥滝野川村字西三軒家〜字北谷端悪水吐水路御買上地所取調書の個別書誌確定（明治14年5月・pkey 822458・第2種水道千川上水道書類並図面第139号*093・601.A8.14・MF市明Ⅰ明18-001 0006-0500＝GOV-572対応文書の所在確定・GOV-592②字名調書と一致）⑦参考: 玉川上水路より神田上水堀筋への通船堀割測量廻村（1870・pkey 298561・605.B3.18）＝旧神田上水注ぎ込み系の明治初年実務候補 ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目・本文・図面は未見）（ai）'
LINES['GOV-634'] = '- [GOV-634](gov/GOV-634.md) — 東京都公文書館クロス検索「排水区」掃引で新規特定した千川・音羽排水区枝線工事の副次的簿冊レコード群（1932〜1942）（2026-11-28・第383回・詳細頁表項目直接取得＝目録詳細確認・repo grep 0件＝repo初出）— ①**東京市継続改良下水道完成工事 枝線管渠施行箇所図「音羽排水区」1/2・2/2（1932・pkey 1240717/1240718・324.E7.12.4）＝GOV-628の千川排水区図と同簿冊の姉妹図**（音羽排水区＝水窪川・音羽川流域の下水道処理区の公文書側の明示）②音羽排水区第1分区の下水道敷設平面図（1936・pkey 1239541・河港課・319.C7.03・MF府昭11-038）③音羽排水区枝線第2号工事の精算報告並工費増額追認＋精算書・使用材料調書・員数表・系統図・平面図（1937-38・pkey 1239996/1239998〜1240002・320.D3.06・MF市昭12-106）④千川排水区枝線第3号工事の精算書・**竣功検査調書**・材料費精算内訳書・系統図・平面図（1937・pkey 1239887〜1239891・320.D2.13）⑤**枝線第4号工事（其1）の施行（1936.9.30起案・pkey 1378912）→工事一部変更（1937×2）→精算・年度割変更（1937-38・pkey 1378908〜1378911）の実務年次チェーン**（319.D8.01・MF市昭11-143）⑥枝線第5号工事の精算書・**線路詳細図・特殊人孔構造図**（1938・pkey 1240233/1240234・320.C7.05）⑦枝線第7号工事（請負1部直営）の精算書・員数表・工事一部変更・線路詳細図・系統図・工事費支出年割変更（1940-42・pkey 1240533〜1240539・1240541〜1240543・322.A1.17/A2.01）＝**千川筋下水道の枝線ごとの管渠線形・人孔構造まで遡れる一次図面群の所在**（枝線第1・2・6号の簿冊所在は未解決・図面判読はhuman回送） ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目・本文・図面は未見）（ai）'

ORDER = ['GOV-633', 'GOV-634']


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第383回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第383回:' in readme:
        print('README: 第383回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第382回:')]
        assert len(hits) == 1, 'README anchor 第382回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-633]' in index:
        print('INDEX: GOV-633 already present; skip')
    else:
        assert '## 行政・公的機関（630件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1977件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-632]')]
        assert len(bhits) == 1, 'INDEX anchor GOV-632 found %d' % len(bhits)
        pos = bhits[0] + 1
        for k in ORDER:
            lines.insert(pos, LINES[k])
            pos += 1
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（630件）', '## 行政・公的機関（632件）')
        index = index.replace('資料ファイル総数: 1977件', '資料ファイル総数: 1979件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-633/634 inserted; counts updated')


if __name__ == '__main__':
    main()
