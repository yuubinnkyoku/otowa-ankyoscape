#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第377回: READMEに実行記録bulletを挿入し、INDEXにBLOG-366・ORG-052行を挿入・計数更新するヘルパー。
使い方: python3 .377-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第376回:' 行の直後に .377-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-365 行の直後に BLOG-366、ORG-051 行の直後に ORG-052 を挿入し、
  ブログ364→365件・企業団体51→52件・総数1947→1949件を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.377-bullet.txt')

ROWS_BLOG = '- [BLOG-366](blogs/BLOG-366.md) — わんじん「水の行方を追って」『田柄用水 －田柄地区流域の開発史－』（2017-12-20・wanjin.blog.fc2.com/?no=223・2026-11-28・第377回・curl本文全文取得＝直接確認・repo未収録URL＝BLOG-080に続く同ブログ第2採録）— **①田柄四丁目20の水車の所在地文言＝repo grep新出**（そのそばで光が丘公園の運動広場から始まる流れが注ぎ込む〔観察〕）②天祖神社内の水神社と「田柄用水」記念碑の2017年現地観察（BLOG-360の2026年観察・GOV-630の明治26年11月建立公的記録・BLOG-326の平成19年祀り直しと通時整合）③**「下田柄の池」の位置＝東京メトロ有楽町線あたり・現在の北保健相談所の西あたり・人工の溜井（農業用水安定供給）＝repo初出の位置具体化**（GOV-630の下練馬村絵図「溜井」北町八丁目南西付近との比定は保留）④十方庵遊歴雑記「練馬下田柄村の池」1町四方（約1万㎡）の二次引用＝GOV-630と整合 ⑤**井上孝夫（千葉大学教育学部）「田柄川流域開発史」（同紀要第62巻＝PAP-093本文未取得）の「田柄＝田涸れ由来説」が2017年二次引用で確認＝repo初出の語源説文言** ⑥用水と田柄川の合流位置＝田柄川緑道の車道併設終了部・新大宮バイパス延伸付近〔2017年読図〕 ⑦1932年東京市編入1か月前の地主組合結成による耕地整理名義の宅地開発 ／ 旧番号: — ／ 直接確認（ai）'
ROWS_ORG = '- [ORG-052](org/ORG-052.md) — 建設通信新聞Digital 公式ブログ「【大豊建設】千川増強幹線工事シールドマシン発進式 雨水幹線新設で地域の浸水軽減に期待」（2019-09-18・kensetsunews.com/web-kan/367030・2026-11-28・第377回・curl本文全文取得＝直接確認・repo grep「発進式」四河川文言0件＝repo初出）— **①シールドマシン発進式の実施（安全祈願祭・関係者約30人・下水道局7人参加）＝repo初出**・施工者＝大豊建設東京土木支店（作業所長 生形浩之）・発進スイッチ＝東京都下水道局第一基幹施設再構築事務所工事第二課 毛利光夫課長と竹内清常務執行役員支店長 ②**仕上がり内径3750mm・延長2525m・工期2021年3月まで・工事場所＝豊島区上池袋1・文京区千石2ほか・既存管と新設幹線で1時間75mm対応＝GOV-082と規格・目的が完全整合** ③**発注者説明「（既設の）千川幹線沿いは、起伏がなく地盤が低い地域のため、浸水被害が起きやすい。13年には大塚付近で浸水被害が多発した」＝repo初出の当局側発言記録**（BLOG-134の2013年南大塚被害131件対応）④施工実務＝トンネル内5%急勾配区間・高摩擦車輪・緊急制御装置・水道管近接の慎重施工・GPS連携運行管理・現場見学会意向 ／ 旧番号: — ／ 直接確認（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第377回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第377回:' in readme:
        print('README: 第377回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第376回:')]
        assert len(hits) == 1, 'README anchor 第376回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-366' in index:
        print('INDEX: BLOG-366 already present; skip')
    else:
        assert '## ブログ・個人サイト（364件）' in index, 'INDEX blog heading mismatch'
        assert '## 企業・団体の公式発表（51件）' in index, 'INDEX org heading mismatch'
        assert '資料ファイル総数: 1947件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits_blog = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-365]')]
        assert len(hits_blog) == 1, 'INDEX anchor BLOG-365 found %d' % len(hits_blog)
        lines.insert(hits_blog[0] + 1, ROWS_BLOG)
        hits_org = [i for i, l in enumerate(lines) if l.startswith('- [ORG-051]')]
        assert len(hits_org) == 1, 'INDEX anchor ORG-051 found %d' % len(hits_org)
        lines.insert(hits_org[0] + 1, ROWS_ORG)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（364件）', '## ブログ・個人サイト（365件）')
        index = index.replace('## 企業・団体の公式発表（51件）', '## 企業・団体の公式発表（52件）')
        index = index.replace('資料ファイル総数: 1947件', '資料ファイル総数: 1949件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-366 + ORG-052 inserted; counts updated')


if __name__ == '__main__':
    main()
