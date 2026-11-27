#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第368回: READMEに実行記録bulletを挿入し、INDEXにGOV-625・BLOG-356〜358行を挿入・計数更新するヘルパー。
使い方: python3 .368-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第367回:' 行の直後に .368-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-624 行の直後に GOV-625 の1行、BLOG-355 行の直後に BLOG-356〜358 の3行を挿入し、
  '## 行政・公的機関（622件）'→'（623件）'、'## ブログ・個人サイト（354件）'→'（357件）'、
  '資料ファイル総数: 1926件'→'1930件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.368-bullet.txt')

GOV_LINE = '- [GOV-625](gov/GOV-625.md) — 東京都水道歴史館「収蔵資料」頁（2026-11-27curl直接取得＝直接確認・第368回）— 神田上水の石樋の公式解説＝昭和60年（1985）水道橋から外堀通りをお茶の水へ上る道路の下から石組みの水路が発見・安山岩構築・断面寸法（下部内法12㎝表記は碑文の下幅120cmと桁差あり原文のまま記録）・『上水記』樋線図の「万年石樋」文言＝神田上水が掛樋で神田川を渡る直前の水路・東京都水道歴史館裏手の本郷給水所公苑内に移築復元（元々全体に蓋があり地下水路）＝発見年次の昭和60年説はBLOG-356碑文の昭和62〜平成元年発掘との表記差を対立として記録 ／ 旧番号: — ／ 直接確認（公式頁本文全文・第368回）（ai）'

BLOG_LINES = [
    '- [BLOG-356](blogs/BLOG-356.md) — 歴史探訪と温泉（hotyuweb）「神田上水遺構（本郷）」（2023-05-12・curl直接取得＝直接確認・第368回）— 本郷給水所公苑（本郷2-7-1）の神田上水石樋碑文（東京都水道局・内部寸法上幅150cm・下幅120cm・高120〜150cm・蓋石180×60×30cm・昭和62〜平成元年発掘）＋神田上水白堀移設復元説明板（平成27年3月東京都水道局）全文＝間知石（四角錐）・胴木基礎・石積1〜3段・新旧流路の相対年代（左=江戸時代19世紀前・中葉頃・右=幕末〜明治以降）・明治9年石蓋設置説・巻石通り呼称由来＋春日1-16-27ポケットパーク「テーマ水」の昭和62年水道橋発掘石展示（文京区説明掲示全文）＝石樋定量寸法・間知石+胴木工法・明治9年説等がrepo初出（石蓋設置年次は明治9/10/11年の対校課題） ／ 旧番号: — ／ 直接確認（curl本文全文・第368回）（ai）',
    '- [BLOG-357](blogs/BLOG-357.md) — ma-maison「神田上水の流れた道をゆく」（小石川歴史散歩・投稿年2015以降〔推定〕・curl直接取得＝直接確認・第368回）— 文京総合福祉センター（平成27年4月1日竣工・第5中学校跡地・昭和21年まで黒田小学校）敷地の白堀復原展示の独立観察＋水道歴史館東側への石樋（文京区No.49遺跡・昭和62〜平成元年外堀通り神田川分水路工事中発掘）と平成23年小日向1・2丁目遺跡白堀一部の移築復原文言＝No.49遺跡の遺跡番号と白堀移築先がrepo初出＋春日町交差点石展示の独立観察＋小日向水道町・関口水道町・水道端・水道町の範囲区分文言（「昭和31年（1966）まで」は年次誤記の可能性を注記） ／ 旧番号: — ／ 直接確認（curl本文全文・第368回）（ai）',
    '- [BLOG-358](blogs/BLOG-358.md) — TEIONE BLOG（平山貞一）「神田川（４）江戸川橋〜御茶ノ水03-巻石通り」（2017・閲覧ツールで本文全文取得・直curlは403・Wayback未収蔵・第368回）— 文京区教育委員会「神田上水旧白堀跡」説明板全文＝正式遺跡名「文京区小日向1・2丁目南遺跡」（nabunken文化財総覧WebGIS抄録=文京区No.118遺跡・龍興寺境内〔1654-1908〕・約1,150基の遺構がスニペット確認で「南」付き支持）・遺構番号15a（新白堀）・15b（旧白堀）号の対・「万年巻石蓋」複合語・現地展示範囲の構造説明＝repo初出＋神田上水の終焉過程の公式説明＝明治34年以降も砲兵工廠（小石川後楽園）の工業用水・大泉水水源として使用継続・大正初期の鉄管置換・関口大洗堰取壊しと庭園用深井戸設置に伴う昭和8〜10年（1933-35）頃の終焉＝1935年頃まで工業用水路説（都水道歴史館）を年次・原因の両面で具体化＋旧町名案内（水道町・水道端・第六天前町=神田上水堀の土手の上の第六天社） ／ 旧番号: — ／ 直接確認（閲覧ツール本文全文・第368回）（ai）',
]


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第368回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第368回:' in readme:
        print('README: 第368回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第367回:')]
        assert len(hits) == 1, 'README anchor 第367回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-356' in index:
        print('INDEX: BLOG-356 already present; skip')
    else:
        assert '## 行政・公的機関（622件）' in index, 'INDEX 行政 heading mismatch'
        assert '## ブログ・個人サイト（354件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1926件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-624]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-624 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, GOV_LINE)
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-355]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-355 found %d' % len(bhits)
        for off, nl in enumerate(BLOG_LINES, start=1):
            lines.insert(bhits[0] + off, nl)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（622件）', '## 行政・公的機関（623件）')
        index = index.replace('## ブログ・個人サイト（354件）', '## ブログ・個人サイト（357件）')
        index = index.replace('資料ファイル総数: 1926件', '資料ファイル総数: 1930件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-625 and BLOG-356..358 inserted; counts updated')


if __name__ == '__main__':
    main()
