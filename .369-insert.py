#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第369回: READMEに実行記録bulletを挿入し、INDEXにPAP-124・GOV-626・BLOG-359行を挿入・計数更新するヘルパー。
使い方: python3 .369-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第368回:' 行の直後に .369-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: PAP-123 行の直後に PAP-124 の1行、GOV-625 行の直後に GOV-626 の1行、
  BLOG-358 行の直後に BLOG-359 の1行を挿入し、
  '## 論文・研究報告・データ（121件）'→'（122件）'、'## 行政・公的機関（623件）'→'（624件）'、
  '## ブログ・個人サイト（357件）'→'（358件）'、'資料ファイル総数: 1930件'→'1933件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.369-bullet.txt')

PAP_LINE = '- [PAP-124](papers/PAP-124.md) — 神吉和夫「神田上水の幹線ルートにおける流量と流れ」（2014・土木学会附属土木図書館学術論文等公開PDF 69-04-0063）（2026-11-27・第369回・PDF直接取得＝本文文言は検索スニペット確認・repo grep 0件＝repo初出）— 神田上水（弦巻川・水窪川の前提水路）の工学的再構成論文＝大洗堰流量107立方尺/秒（2.97㎥/s）時に神田上水26立方尺/秒（0.72㎥/s）・流速毎秒八寸四分（0.25m/s）の定量推定・万年石樋断面（高120-150cm・上部内法約150cm・下部内法約120cm）の御茶ノ水分水路工事発掘報告書由来の確認＝BLOG-356碑文と寸法一致の第3独立層・嘉永2年「水道橋脇掛樋其外石垣樋枡普請一件」内法幅六尺深五尺（GOV-244の嘉永2〜3年分冊対応）・『東京市史稿』附図「神田玉川両上水全図」の万年樋内法上口五尺敷四尺五寸深四尺・「玉川神田両上水平面圖」（都水道局所蔵）の流量観測記録・慶長13年江戸図（内藤昌）重ね合わせの小石川大沼迂回「神田明神山岸」経由ルートと成立年代再検討・『明治以前日本土木史』大正8年大洗堰修築記録引用＝万年石樋寸法の4層対校が本回最大の前進（PDFはStandard暗号で抽出不能・刊行物名は69-04採番からの推定） ／ 旧番号: — ／ PDF直接取得・文言はスニペット確認（第369回）（ai）'

GOV_LINE = '- [GOV-626](gov/GOV-626.md) — 千代田区文化財サイト「神田上水懸樋跡」（文化財サイン・か行・2024年4月12日更新・場所神田駿河台二丁目11先・2026-11-27・第369回・open_url本文全文取得＝直接確認・repo grep 0件＝repo初出）— 文京区側説明板群（BLOG-356〜358）の対岸側にあたる千代田区の公式説明板本文＝万治年間1658-1661の懸樋架替→「俗に万年樋」と呼称の由来自記載・慶長年間（1596-1615）整備着手「説」・井の頭池・善福寺池・妙正寺池水源→関口堰→小日向台→小石川後楽園→水道橋下流の流路概略・懸樋越水後の暗渠（埋樋）化・給水範囲の四至（南は京橋川・東は永代橋より大川以西・北は神田川・西は大手町から一橋門外）・牛込門外（飯田橋）までは江戸川・牛込門外から下流は神田川とする呼称区分の明文＝給水範囲四至と江戸川/神田川呼称区分はrepo初出の公式文言 ／ 旧番号: — ／ 直接確認（open_url本文全文・第369回）（ai）'

BLOG_LINE = '- [BLOG-359](blogs/BLOG-359.md) — テレビ東京「出没！アド街ック天国」公式サイト 2024年3月2日放送「江戸川橋」20位 関口大洗堰跡（2026-11-27・第369回・open_url本文全文取得＝直接確認・repo grep 0件＝repo初出）— 「江戸で初めての本格的な上水道「神田上水」の取水口だった大洗堰。江戸初期に現在の神田川に造られ、**昭和8年に撤去された**。現在、江戸川橋のたもとにある「江戸川公園内」の池に**大洗堰の一部が復元されている**」＝BLOG-358文京区教委説明板「関口大洗堰取壊し…昭和8〜10年（1933-35）頃」のうち1933年側を支持するメディア由来の独立傍証（典拠記載なしのため断定せず）＋江戸川公園の池への一部復元はrepo初出の現況記録（復元部位・年次は未記載） ／ 旧番号: — ／ 直接確認（open_url本文全文・第369回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第369回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第369回:' in readme:
        print('README: 第369回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第368回:')]
        assert len(hits) == 1, 'README anchor 第368回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'PAP-124' in index:
        print('INDEX: PAP-124 already present; skip')
    else:
        assert '## 論文・研究報告・データ（121件）' in index, 'INDEX 論文 heading mismatch'
        assert '## 行政・公的機関（623件）' in index, 'INDEX 行政 heading mismatch'
        assert '## ブログ・個人サイト（357件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1930件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        phits = [i for i, l in enumerate(lines) if l.startswith('- [PAP-123]')]
        assert len(phits) == 1, 'INDEX anchor PAP-123 found %d' % len(phits)
        lines.insert(phits[0] + 1, PAP_LINE)
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-625]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-625 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, GOV_LINE)
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-358]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-358 found %d' % len(bhits)
        lines.insert(bhits[0] + 1, BLOG_LINE)
        index = '\n'.join(lines)
        index = index.replace('## 論文・研究報告・データ（121件）', '## 論文・研究報告・データ（122件）')
        index = index.replace('## 行政・公的機関（623件）', '## 行政・公的機関（624件）')
        index = index.replace('## ブログ・個人サイト（357件）', '## ブログ・個人サイト（358件）')
        index = index.replace('資料ファイル総数: 1930件', '資料ファイル総数: 1933件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: PAP-124, GOV-626, BLOG-359 inserted; counts updated')


if __name__ == '__main__':
    main()
