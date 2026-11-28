#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第381回: READMEに実行記録bulletを挿入し、INDEXにBLOG-388〜393の6行を挿入・計数更新するヘルパー。
使い方: python3 .381-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第380回:' 行の直後に .381-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-387 行の直後に BLOG-388〜393 の6行を挿入し、
  '## ブログ・個人サイト（386件）'→'（392件）'、'資料ファイル総数: 1970件'→'1976件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.381-bullet.txt')

LINES = {}
LINES['BLOG-388'] = '- [BLOG-388](blogs/BLOG-388.md) — Natrium.jp「エンガ掘と周辺の水路敷群（下流端〜要町通り）」（engabori/enga01・撮影2017/4/29ほか）（2026-11-28・第381回・curl本文全文取得＝直接確認・canal_lot目次走査で検出＝repo初出）— **エンガ掘の別称「エガ掘・江川」説〔伝聞〕**・千川上水からの分水点「豊島南長崎六郵便局北側」説〔観察・BLOG-103/GOV-072と対校〕・**耕整橋南側の石神井川合流点排水口＝現役暗渠〔観察〕**・エンガ掘緑道（大谷口北口〜小竹向原）の整備現況・向原トンネル付近旧流路〔推定〕・武蔵野病院前支流の水路敷残存・昭和22年空中写真の小竹向原駅北側田んぼ間水路〔読図〕 ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'
LINES['BLOG-389'] = '- [BLOG-389](blogs/BLOG-389.md) — Natrium.jp「エンガ掘と周辺の水路敷群（大谷口の支流）」（engabori/enga02・撮影2017/4-5月）（2026-11-28・第381回・curl本文全文取得＝直接確認・repo初出）— **大谷口給水所の沿革年次列＝昭和6年給水塔完成→昭和47年まで現役→平成17年取壊→平成23年ポンプ棟〔repo初出〕**・砧浄水場→荒玉水道→王子方面給水の系統説明・**「千川上水の漏水が谷に流れていた」〔伝聞・漏水説の傍証候補〕**・山崎橋の月を模した照明＝山崎田んぼの故事に倣う〔BLOG-124の三日月意匠説の独立傍証候補〕・大谷口氷川神社（延宝2年1674記録・16世紀遡行可能性）〔repo初出〕・日大板橋病院西谷の平成14〜21年改良事業・溜池伝承・パステル宮の下商店街 ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'
LINES['BLOG-390'] = '- [BLOG-390](blogs/BLOG-390.md) — Natrium.jp「エンガ掘と周辺の水路敷群（要町通り〜千川通り）その1・その2」（engabori/enga03・撮影2017年6-7月・2024/6/1追記）（2026-11-28・第381回・curl本文全文取得＝直接確認・repo初出）— **「ねりまの文化財60号」引用で千川上水と支流が明豊中学校付近で立体交差していた〔repo初出文言〕**・**長崎悪水吐＝千川上水の下をくぐる立体交差〔伝聞〕＋東長崎2号踏切跡からの開渠上流部の2024年現地観察〔repo初出〕**・千川通り側から見た分水口〔BLOG-103と対校〕・豊島千早4丁目・練馬小竹町1丁目・板橋向原1丁目の3区境合流点・寛文〜明和年間の上板橋村地蔵尊・庚申塔群・大成小学校+千川小学校→さくら小学校合併説〔BLOG-131対校〕 ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'
LINES['BLOG-391'] = '- [BLOG-391](blogs/BLOG-391.md) — Natrium.jp「エンガ掘と周辺の水路敷群（小茂根の支流）」（engabori/komone・撮影2017/5-6月）（2026-11-28・第381回・curl本文全文取得＝直接確認・repo初出）— **小茂根地名＝昭和40年住居表示で小山町・茂呂町・根ノ上町の頭文字合成〔repo初出〕**・根ノ上遺跡（弥生環濠集落復元）・**イチョウ並木＝開渠跡（昭和38年空中写真で道路中央に開渠）〔読図〕**・小竹換気所・谷頭=小竹みどり公園説〔推定〕・要町通り=都道441号・放射36号線の延伸状況・「さぶろく四季の道」遊歩道〔repo初出〕 ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'
LINES['BLOG-392'] = '- [BLOG-392](blogs/BLOG-392.md) — Natrium.jp「妙正寺川・井草川の水路敷群（井草川上流とその支流）その1〜その3」（igusa/igusa02・撮影2011/7/23ほか）（2026-11-28・第381回・curl本文全文取得＝直接確認・第380回課題の本文確認）— **井草川上流は千川上水と六ヶ村分水（井草分水）の双方から導水〔伝聞・repo初出文言〕**・千川上水からの分水支流の合流点〔観察〕・上石神井車両基地あたりの分水口＝痕跡なし〔観察〕・井草八幡宮前・元文5年1740庚申の年銘青面金剛庚申塔〔観察〕 ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'
LINES['BLOG-393'] = '- [BLOG-393](blogs/BLOG-393.md) — Natrium.jp「妙正寺川・井草川の水路敷群（江古田川周辺の水路敷）その2」（egota/egota/index_02・撮影2020年2月）（2026-11-28・第381回・curl本文全文取得＝直接確認・repo初出）— 市杵島神社のかつての湧水伝承・**中新井村大字中新井字弁天＝字名と弁天分水の名の由来候補〔推定・由来側の新観察〕**（BLOG-166/320対校）・弁天分水の下流端＝中新井公園東側・豊玉二小との間〔観察〕・千川通り側の水路敷残存・桜の碑（清戸道・千川上水桜並木→桜台地名＝BLOG-144対校）・下徳「殿」橋の橋名看板実物〔観察〕・「徳殿」小名由来（ねりまの地名今むかし16＝BLOG-385と相互整合） ／ 旧番号: — ／ 直接確認（curl本文全文・第381回）（ai）'

ORDER = ['BLOG-388', 'BLOG-389', 'BLOG-390', 'BLOG-391', 'BLOG-392', 'BLOG-393']


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第381回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第381回:' in readme:
        print('README: 第381回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第380回:')]
        assert len(hits) == 1, 'README anchor 第380回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [BLOG-388]' in index:
        print('INDEX: BLOG-388 already present; skip')
    else:
        assert '## ブログ・個人サイト（386件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1970件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-387]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-387 found %d' % len(bhits)
        pos = bhits[0] + 1
        for k in ORDER:
            lines.insert(pos, LINES[k])
            pos += 1
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（386件）', '## ブログ・個人サイト（392件）')
        index = index.replace('資料ファイル総数: 1970件', '資料ファイル総数: 1976件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-388..393 inserted; counts updated')


if __name__ == '__main__':
    main()
