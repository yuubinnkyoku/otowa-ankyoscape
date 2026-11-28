#!/usr/bin/env python3
# retrigger: 384 (paths filter firing)
# -*- coding: utf-8 -*-
"""第384回: READMEに実行記録bulletを挿入し、INDEXにBOOK-339/BOOK-340/PAP-125の3行を挿入・PAP-093行を更新・計数更新するヘルパー。
使い方: python3 .384-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第383回:' 行の直後に .384-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BOOK-338 行の直後に BOOK-339・BOOK-340 の2行、PAP-124 行の直後に PAP-125 の1行を挿入し、
  PAP-093 行を本文取得版に置換、'## 書籍・雑誌・メディア（337件）'→'（339件）'、'## 論文・研究報告・データ（122件）'→'（123件）'、
  '資料ファイル総数: 1979件'→'1982件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.384-bullet.txt')

PAP093_OLD = '- [PAP-093](papers/PAP-093.md) — 井上孝夫「田柄川流域開発史」『千葉大学教育学部研究紀要』第62巻（千葉大学教育学部・発行年未確認）— 谷端川源流部の谷頭低地を含む旧田柄村・田柄川流域の開発史研究。NDL書誌直接確認・本文未取得 ／ 旧番号: — ／ 所在のみ（NDL書誌確認・本文未取得・発行年は巻号からの推定を要する）（ai）'
PAP093_NEW = '- [PAP-093](papers/PAP-093.md) — 井上孝夫「田柄川流域開発史」『千葉大学教育学部研究紀要』第62巻Ⅱ（人文・社会科学系）pp.255-264（千葉大学教育学部・2014年3月）（第384回: 千葉大OPAC直URLは403だがWayback Machine 2024-09-06収蔵版の暗号化PDF〔AESV2・778,391bytes〕を自作復号器で全復号し全10頁本文テキスト抽出＝「所在のみ」から「本文取得」に格上げ・図1〜3は判読未了）— 谷端川（田柄川）流域の開発史研究＝石神井川合流点（板橋区都立城北中央公園の先）まで全区間「田柄川」記述（BLOG-118別称説を強める）・「田枯」「田涸」語源説（本文§3）・下田柄の池（十方庵遊歴雑記「練馬下田柄村の池」1町=109m四方・寛政4年下練馬村絵図の西側）・田柄用水開削の実務（明治4年正月申請・10月品川県報告・田無村ほか8カ村〔谷原村離脱〕・約17.2km・約1,342両・小島家文書479-482頁・名称変遷「田無村ほか8カ村組合用水→玉川上水新井筋分水→田柄田用水→田柄用水」・完成時期4説併置）・天保10年「土支田村下組絵図」の「悪水」（排水路）記載・千川家（徳兵衛・太兵衛の千川名字・帯刀・「千川水路取締」・下練馬宿中宿「千川屋」・阿弥陀堂墓誌3代〜11代・9代善造明治23年「千川水路見廻役」・家系略譜〔豊島区立郷土資料館1995史料集Ⅰ〕との不一致）・成増飛行場（1943）建設時の流路変更（光が丘〜田柄2丁目南交差点=旧流路1本沿い・北町5丁目大堰まで新ルート掘削・旧流路と池端の池は埋立・「1メートル5円で町会請負・青年団が掘った」田中氏証言・用水の滑走路横断トンネル化）・1970年代下水道幹線転用・田柄川緑道化・水田の時代（明治25年〜大正末）・松林寺の消滅（1881地形図→1909消失） ／ 旧番号: — ／ 本文取得（Wayback収蔵版暗号化PDF自作復号・全10頁テキスト抽出・図版未判読）（ai）'

LINES = {}
LINES['BOOK-339'] = '- [BOOK-339](books/BOOK-339.md) — 山之内光治編『練馬村の変遷図集 : 絵図と地図』（2008年6月刊・出版者〔山之内光治〕・NDLBibID 000009799126・JPNO 21506029）（2026-11-28・第384回・PAP-093参考文献・NDL OpenSearch書誌直接確認・repo grep 0件＝repo初出）— PAP-093〔図1〕が翻案図に用いた寛政4年（1792）筆写「下練馬村絵図」等の練馬村の絵図・変遷地図の一次図集＝GOV-630（下練馬村絵図・溜井）・BLOG-366（下田柄の池）の比定問題の図版原本側（本文・図版は未取得） ／ 旧番号: — ／ 書誌確認（NDL OpenSearch・本文未取得）（ai）'
LINES['BOOK-340'] = '- [BOOK-340](books/BOOK-340.md) — 瓜生左門編『田柄用水をたずねて』（練馬区小学校教育会社会科部・1997年・全8頁）（2026-11-28・第384回・PAP-093参考文献による実在確認・NDL OpenSearch書誌なし・repo grep 0件＝repo初出）— 田柄用水を主題にした教育実践パンフレット（BOOK-213と同様の引用内証のみの稀覯資料）・wanjin田柄用水シリーズ（BLOG-367〜370）やNatrium田柄用水中流（BLOG-383/384）の観察系と対校可能な1997年時点の記録候補（実物・所蔵は未確認） ／ 旧番号: — ／ 書誌内証（PAP-093参考文献・NDL書誌なし・本文未取得）（ai）'
LINES['PAP-125'] = '- [PAP-125](papers/PAP-125.md) — 吉成勝好「地域開発教材としての田柄川」『練馬区小学校教育会研究集録・昭和58年度』（1984）（2026-11-28・第384回・PAP-093参考文献による実在確認・NDL OpenSearch書誌なし・repo grep 0件＝repo初出）— 田柄川（谷端川上流）を地域開発教材とした教育実践記事・BLOG-367「1980年代前半に全流路暗渠化」説の時代と重なる教材記録として当時の川の状態の傍証候補（吉成1978〔PAP-093§5の用水命名理由③の出典〕との関係は未確認・実物は未取得） ／ 旧番号: — ／ 書誌内証（PAP-093参考文献・NDL書誌なし・本文未取得）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第384回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第384回:' in readme:
        print('README: 第384回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第383回:')]
        assert len(hits) == 1, 'README anchor 第383回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [BOOK-339]' in index:
        print('INDEX: BOOK-339 already present; skip')
    else:
        assert PAP093_OLD in index, 'INDEX PAP-093 old line not found'
        index = index.replace(PAP093_OLD, PAP093_NEW)
        assert '## 書籍・雑誌・メディア（337件）' in index, 'INDEX 書籍 heading mismatch'
        assert '## 論文・研究報告・データ（122件）' in index, 'INDEX 論文 heading mismatch'
        assert '資料ファイル総数: 1979件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-338]')]
        assert len(bhits) == 1, 'INDEX anchor BOOK-338 found %d' % len(bhits)
        pos = bhits[0] + 1
        for k in ['BOOK-339', 'BOOK-340']:
            lines.insert(pos, LINES[k])
            pos += 1
        phits = [i for i, l in enumerate(lines) if l.startswith('- [PAP-124]')]
        assert len(phits) == 1, 'INDEX anchor PAP-124 found %d' % len(phits)
        lines.insert(phits[0] + 1, LINES['PAP-125'])
        index = '\n'.join(lines)
        index = index.replace('## 書籍・雑誌・メディア（337件）', '## 書籍・雑誌・メディア（339件）')
        index = index.replace('## 論文・研究報告・データ（122件）', '## 論文・研究報告・データ（123件）')
        index = index.replace('資料ファイル総数: 1979件', '資料ファイル総数: 1982件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BOOK-339/340, PAP-125 inserted; PAP-093 updated; counts updated')


if __name__ == '__main__':
    main()