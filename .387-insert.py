#!/usr/bin/env python3
# retrigger: 387 (paths filter firing)
# -*- coding: utf-8 -*-
"""第387回: READMEに実行記録bulletを挿入し、INDEXにGOV-637・GOV-638の2行を挿入・計数更新するヘルパー。
使い方: python3 .387-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第386回:' 行の直後に .387-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [GOV-636]' 行の直後に GOV-637・GOV-638 の2行を挿入し、
  '## 行政・公的機関（634件）'→'（636件）'、'資料ファイル総数: 1986件'→'1988件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.387-bullet.txt')

LINES = {}
LINES['GOV-637'] = '- [GOV-637](gov/GOV-637.md) — 東京都公文書館クロス検索「水車」語掃引（www経路・2,798件・28頁全走査・2026-11-28・第387回・詳細頁表項目直接取得・repo grep 0件＝repo初出）＝石神井村鴨下家・速見家の水車実務群（1886〜1912・9件）＋板橋町浮田久三郎廃業届（1911）・大泉村見留きく器械増加願（1908）— ①鴨下家（関村分水・千川上水沿いの石神井村。BLOG-094の明治17年路図「鴨下」水車・BLOG-383の鴨下米穀店・関口水車の観察系）の水車営業が**継年期願（1886・pkey 499548／1891・由左衛門・448534／1896・332301）→器械変更（1895・992089/992120／1909・269326）→水揚堰修繕許可（1912・鴨下栄蔵・233748）まで26年間の行政一次記録**で追える〔水揚堰＝揚水堰でBLOG-370の栗原堰→揚げ堀系の対照候補・続柄と同一水車かは本文未見で比定保留〕②速見家（速見文次郎1895・992121/992156→親権者速見よう1910・249754）＝BLOG-383の速水水車の家系側候補③板橋町浮田久三郎の水車廃業届（1911・215435）＝GOV-617の下板橋宿水車群（1872〜74）の廃業側終端記録候補・大泉村橋戸見留きくの器械増加願許可（1908・278780）・陰性: 北多摩郡の板橋宗三郎は同名の別人・立会川（戸長田中肇・1886）は新河岸川・白子川水系候補で見送り ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目直接取得・本文・図面は未見）（ai）'
LINES['GOV-638'] = '- [GOV-638](gov/GOV-638.md) — 東京都公文書館クロス検索「水車」語掃引＝神田上水系の水車実務4件＋人名簿1件（1881〜1899・2026-11-28・第387回・詳細頁表項目直接取得・repo初出）— ①**「神田上水白堀通水車水口差塞の義通知」2件（明治14年1881・砲兵工廠宛・植物御苑宛・pkey 370592/370593・611.C5.06・MF府明Ⅱ明14-019）＝白堀沿いの民間水車（通水車）の取水口が1881年に塞がれた一次文言で、PAP-124の白堀断面復元・BLOG-356〜359/375の江戸川公園・大洗堰研究に行政実務側の対照を追加**②水道改良事務所取扱水車営業人名簿（明治元〜21年台帳・738807・617.B6.12）で**渡辺一敏の所属が「戸塚村・角筈村」（神田上水沿い）と特定＝GOV-618第360回追記③の渡辺姓系列（1894年水車要録）の村落側が初めて判明し、BLOG-094の渡辺水車（鴨下・富士見台1＝千川上水側）との比定は別系統候補が強まった（断定せず）**③渡辺一敏の水車回し堀破損による神田上水助水引入口（伊地知）閉鎖願（1897・212886・601.D3.13）＝BLOG-386の助水堀現況に行政側対照④神田上水路水車水料簿冊（1899・565992・601.D5.21）＝GOV-618①iの千川系水料金（1882）と対になる水料記録の所在 ／ 旧番号: — ／ 目録詳細確認（詳細頁表項目直接取得・本文は未見）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第387回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第387回:' in readme:
        print('README: 第387回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第386回:')]
        assert len(hits) == 1, 'README anchor 第386回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-637]' in index:
        print('INDEX: GOV-637 already present; skip')
    else:
        assert '## 行政・公的機関（634件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1986件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-636]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-636 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['GOV-638'])
        lines.insert(ghits[0] + 1, LINES['GOV-637'])
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（634件）', '## 行政・公的機関（636件）')
        index = index.replace('資料ファイル総数: 1986件', '資料ファイル総数: 1988件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-637, GOV-638 inserted; counts updated')


if __name__ == '__main__':
    main()
