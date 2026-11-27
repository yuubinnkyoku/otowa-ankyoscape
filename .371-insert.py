#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第371回: READMEに実行記録bulletを挿入し、INDEXにGOV-628・GOV-629行を挿入・計数更新するヘルパー。
使い方: python3 .371-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第370回:' 行の直後に .371-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-627 行の直後に GOV-628・GOV-629 の2行を挿入し、
  '## 行政・公的機関（625件）'→'（627件）'、'資料ファイル総数: 1935件'→'1937件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.371-bullet.txt')

GOV_LINE_628 = '- [GOV-628](gov/GOV-628.md) — 東京都公文書館・資料名クロス検索「千川」全掃引（516件・2026-11-27実施・403解除後の初の資料名単語掃引）で新規特定した千川筋下水道行政実務群（1911〜1941・31件クラスタ）（2026-11-27・第371回・詳細頁表項目直接取得＝目録詳細確認・repo grep 0件＝repo初出）— 千川大下水改修費の明治44年市会予算（603.B4.01＋603.B3.14）・改良下水道速成費の千川筋試掘工事直営1928.10.29（312.E1.01・MF0006-0328）・千川筋下水道改修の府知事・内務大臣宛下水道築造実施認可申請1930.7.3（実測平面図・実測縦断面図・管渠流量表・314.E4.10・MF0407-0768）＝着手1930説（BLOG-077）の行政実務レベルの裏付け候補・千川排水区枝線第4号1936（319.D8.01）・第3号1937（320.D2.13・系統図・平面図・竣功検査調書）・第5号（特殊人孔構造図）・第7号1940（322.A2.01・設計書）・東京市継続改良下水道完成工事枝線管渠施行箇所図「千川排水区」1/2・2/2（昭和7〜16年・324.E7.12.4）＝1911→1925未起工（GOV-475）→1928試掘→1930認可申請→1932〜41枝線施行の実務年代列が初めて一次記録レベルで揃った・枝線各号と千川改修区間の対応は図面未見のため断定せず ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目・本文・図面は未見）（ai）'

GOV_LINE_629 = '- [GOV-629](gov/GOV-629.md) — 東京都公文書館・資料名クロス掃引の補遺＝明治5年千川筋堀割×陸軍省・明治18年千川筋巡回・昭和18年谷端公園開園告示＋甲集十七原本書誌（1872〜1943）（2026-11-27・第371回・詳細頁表項目直接取得＝目録詳細確認・repo grep 0件＝repo初出）— 「府下滝之川村千川筋堀割一件　陸軍省江回答并掛合」（明治5年1872・第三課・諸向達掛合留・旧郷村掛取扱・６号・605.D4.01・MF0558-1020）＝陸軍省の千川筋堀割関与の前年次実務（板橋火薬製造所1873〔GOV-572〕・砲兵工廠〔GOV-471〕の前段候補・目的は本文未見のため断定せず）・「北豊島郡長へ長官千川筋巡回の通知」（明治18年1885・614.A2.01・MF0512-0705）・「谷端公園開園及公園管理事務１部区長分掌の件」（東京市告示第77・78号・昭和18.3.16起案・滝野川区・325.A1.06・MF0006-0499）＝谷端川緑道系公園の戦中期行政起点候補・東京府文献叢書甲集十七（小石川志料）の都公文書館蔵原本書誌特定（DB-019・国重文・MF0190-0267）＝GAZ-083の原本側・陰性整理: 弦巻掃引194件は荏原郡弦巻村（世田谷）中心＝弦巻川スコープ外・水窪掃引38件は同名異地中心（字水窪新田はGOV-573既収録）・谷端掃引の改修系はGOV-568/571既収録・戦災復興換地確定図（谷端組合地区①②）は第372回課題 ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目・本文は未見）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第371回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第371回:' in readme:
        print('README: 第371回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第370回:')]
        assert len(hits) == 1, 'README anchor 第370回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-628' in index:
        print('INDEX: GOV-628 already present; skip')
    else:
        assert '## 行政・公的機関（625件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1935件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-627]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-627 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, GOV_LINE_628)
        lines.insert(ghits[0] + 2, GOV_LINE_629)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（625件）', '## 行政・公的機関（627件）')
        index = index.replace('資料ファイル総数: 1935件', '資料ファイル総数: 1937件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-628, GOV-629 inserted; counts updated')


if __name__ == '__main__':
    main()
