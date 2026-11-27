#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第370回: READMEに実行記録bulletを挿入し、INDEXにBOOK-338・GOV-627行を挿入・計数更新するヘルパー。
使い方: python3 .370-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第369回:' 行の直後に .370-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BOOK-337 行の直後に BOOK-338 の1行、GOV-626 行の直後に GOV-627 の1行を挿入し、
  '## 書籍・雑誌・メディア（336件）'→'（337件）'、'## 行政・公的機関（624件）'→'（625件）'、
  '資料ファイル総数: 1933件'→'1935件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.370-bullet.txt')

BOOK_LINE = '- [BOOK-338](books/BOOK-338.md) — 文京区教育委員会『小日向一・二丁目南遺跡』発掘調査報告書（平成26年〔2014年〕3月刊・PAP-124参考文献1)で書誌特定）（2026-11-27・第370回・repo grep 0件＝repo初出）— 神田上水白堀跡の発掘調査（平成23〜24年・文京区総合福祉センター建設に伴う）の報告書本体＝山中リュウ執筆の第4章（白堀遺構まとめ）を含むことがPAP-124本文から確認・白堀の発掘石垣高0.9〜1m文言の典拠＝BLOG-355〜358説明板群・nabunken文化財総覧WebGIS抄録ID 144724（文京区No.118遺跡・龍興寺境内1654-1908・約1,150基の遺構）に対応・本文は未確認（現物所在・総覧レコード特定が次の一手）・万年石樋断面の典拠「御茶ノ水分水路工事の報告書」とは別冊候補（混同注意） ／ 旧番号: — ／ 書誌特定（PAP-124参考文献経由・本文未確認）（ai）'

GOV_LINE = '- [GOV-627](gov/GOV-627.md) — 東京都水道歴史館「講演会『小日向一・二丁目南遺跡出土の神田上水白堀跡』」（2016年2月13日・水道歴史館3階レクチャーホール・無料事前申込制）（2026-11-27・第370回・open_url本文全文取得＝直接確認・repo grep 0件＝repo初出）— 白堀跡発掘の公表講演の公式記録＝講演者は文京区教育委員会主任学芸員 池田悦夫（発掘担当学芸員）・「江戸のまちの成り立ちや、文京区の地形、地質の特色から神田上水の歴史についてひも解き、神田上水白堀跡の発見から分かることについて、発掘当時の貴重な写真・データをもとにお話しいただきました」の記録文言＝発掘（2011-12）→報告書（2014-03・BOOK-338）→公表講演（2016-02・水道歴史館）→説明板・復原（平成27年3月都水道局）の公表年次チェーンの補強 ／ 旧番号: — ／ 直接確認（open_url本文全文・第370回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第370回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第370回:' in readme:
        print('README: 第370回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第369回:')]
        assert len(hits) == 1, 'README anchor 第369回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BOOK-338' in index:
        print('INDEX: BOOK-338 already present; skip')
    else:
        assert '## 書籍・雑誌・メディア（336件）' in index, 'INDEX 書籍 heading mismatch'
        assert '## 行政・公的機関（624件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1933件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-337]')]
        assert len(bhits) == 1, 'INDEX anchor BOOK-337 found %d' % len(bhits)
        lines.insert(bhits[0] + 1, BOOK_LINE)
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-626]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-626 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, GOV_LINE)
        index = '\n'.join(lines)
        index = index.replace('## 書籍・雑誌・メディア（336件）', '## 書籍・雑誌・メディア（337件）')
        index = index.replace('## 行政・公的機関（624件）', '## 行政・公的機関（625件）')
        index = index.replace('資料ファイル総数: 1933件', '資料ファイル総数: 1935件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BOOK-338, GOV-627 inserted; counts updated')


if __name__ == '__main__':
    main()
