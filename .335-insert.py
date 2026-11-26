#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第335回: READMEに実行記録bulletを挿入しINDEXにGOV-606〜608行を追加するヘルパー。
使い方: python3 .335-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第334回:' 行の直後に .335-bullet.txt の1行を挿入（'- **第335回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: GOV-606/607/608の3行をGOV-605行の直後に挿入し「## 行政・公的機関（603件）」→606件・
  「資料ファイル総数: 1853件」→1856件を更新（第335回のpush_filesでINDEXの行挿入・計数更新が
  済んでいる場合は検出して何もしない＝冪等）。
  （アンカー・計数文字列は一意であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.335-bullet.txt')

GOV606_LINE = '- [GOV-606](gov/GOV-606.md) — 東京都公文書館「橋々銘書・朱引内６２橋外２５・６冊の内」（明治4年1871・請求605.C6.02・資料ID 000114513・MF府明Ⅱ明04-023 コマ0190-0549・複写可・dasasp03画像公開）（2026-11-26・第335回・GETレシピ復旧で「千川橋」「橋銘」掃引・repo初出・目録レベルで本文未確認）— 構成pkey: 618103「橋々銘書 小石川千川橋より浅草新鳥越橋迄 朱引内４橋・朱引外４５橋」＋618104「千川橋 橋番人無し・**従前武家持・天保７年申石橋に掛替** １橋」＝千川橋の天保7年（1836）石橋化の従前記録＋618181「二十八番組 **里俗千川橋**」＝里俗呼称の府側明記＋618207「橋銘并間数書上 地方二番組」29橋中**藤橋・東福寺橋・寂法橋・上之橋**（GAZ-197矢端川条・GAZ-048小谷端川の橋4と一致＝谷端川上流4橋の明治4年の実在裏付け）・**猫股橋**（谷端川橋戸町の猫俣橋／千川の猫股橋の2系統同名橋問題に1871年の生存記録候補）・**祇園橋**（BOOK-324「谷端川水源より祇園橋まで二里十八町」の比定課題への対照資料候補）・駒塚橋・面影橋＋618206「地方一番組」（渋谷橋・広尾橋・笄橋・宮益橋・金王下橋・水車橋・庚申橋等＝渋谷川系・隣接水系の記録）＋618208「地方三番組」＋618153「常務局」・618205「地方一番組より五番組迄」＋起点の達＝568765「橋銘の義…元番組にて１人づつ東京府へ出勤すべき旨、当番より達 ４月２日」明治2年1869（久能木文書ノ内・市中御改正御用留・604.A3.14）＝橋銘調査が明治2年の市中御改正に遡る（番組内の橋の所在・朱引内外の計数は本文未確認で断定しない・dasasp03のIIIF判読はhuman確認待ち・庚申橋は玉川上水・千住等の同名異橋に注意） ／ 旧番号: — ／ 目録詳細確認（詳細頁・一覧頁・本文は未見）（ai）'
GOV607_LINE = '- [GOV-607](gov/GOV-607.md) — 東京都公文書館・藤橋（谷端川）と宮仲（巣鴨村字宮仲）の実務公文書群5件（1876〜1917）（2026-11-26・第335回・GETレシピで「藤橋」「宮仲」掃引・repo初出・目録レベルで本文・図面は未確認）— ①明治9年1876「第九大区二小区小林助左衛門巣鴨村字宮仲の**藤橋大破**に関する願書却下願」（pkey 322630）＋「第九大区二小区**藤橋修繕願**」（322719・管民願伺届録・第4部〈土木（掛）〉9〜10月乾・607.C6.03・MF府明Ⅱ明09-020 コマ0521-0895）＝谷端川の藤橋の大破→修繕願→却下の実務チェーン ②明治42年1909「**藤橋へ瓦斯管架設認可** 北豊島郡巣鴨村地内 東京瓦斯株式会社」（437088・文書類纂・土木・第3類・橋梁・第1巻・629.A3.06・コマ0336-0856）＝1909年の藤橋の現役記録 ③大正3年1914「**下水路新設願**〔巣鴨村大字巣鴨字宮仲地内〕後藤二三郎外5名」（1185984・道路冊の2・301.E3.03・コマ0006-0415）④大正6年1917「**不用水路敷無代下付【図面】**〔宮仲２３２３　２３２４〕（図面添付冊）」（1080310・官有地冊の4・302.D5.03・コマ0621-1070）＝谷端川低地（宮仲）の下水路整備と用廃水路の宅地化過程（1876橋大破→1909橋の現役→1914下水路新設→1917不用水路下付の変遷列・各詳細は本文・図面未確認） ／ 旧番号: — ／ 目録詳細確認（詳細頁・本文・図面は未見）（ai）'
GOV608_LINE = '- [GOV-608](gov/GOV-608.md) — 東京都公文書館・千川下流（小石川）の橋梁実務群3件（1877・1901・1933）（2026-11-26・第335回・GETレシピで「千川橋」「猫俣橋」掃引・repo初出・目録レベルで本文・図面は未確認）— ①明治10年1877「第四大区八小区**小石川掃除町２１番地地先より同２０番地地先へ渡る千川養水流末へ架渡**」**橋銘呼名の義伺**（481565・管民願伺届・第4部〈土木掛〉9月・608.C4.07・MF府明Ⅱ明10-016 コマ0006-0512）＝「千川養水流末」の1877年府側文言＋掃除町地先の橋の命名実務 ②明治34年1901「小石川区**千川橋架換工事**の監督に従ひ其落成を速めし勤労尠からさるに依り手当として特に給与す 技手 崇島貞俊、技手補 狩野文平」（965639・第1種秘書＊甲進退録・601.D9.06）＝1901年の千川橋架換・落成を裏付ける人事記録＝千川橋年代列（1880.10.4流失→明治13〜14架換）への1901年追加（人名2件repo grep新出） ③昭和8年1933.6.2起案「**東京市電氷川下町・大塚仲町間軌道工事方法変更（小石川区）【猫俣橋橋上軌道構造図】東京市電気局**」3件（1212258/1212259/1212260・東京府土木庶務課・鉄道・軌道・索道・自動車道路冊の36・317.B6.04・資料ID 000138308・MF府昭08-093 コマ0822-0934）＝1933年時点の猫俣橋（猫股橋）の実在と市電軌道上の位置を伝える図面記録＝BLOG-210千川の猫股橋・GAZ-048谷端川橋戸町の猫俣橋の2系統同名橋問題への最重要対照図面候補（橋下の水路の同定は図面確認まで断定しない・1930-34千川改修と同時期） ／ 旧番号: — ／ 目録詳細確認（詳細頁・一覧頁・本文・図面は未見）（ai）'


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第335回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第335回:' in readme:
        print('README: 第335回bullet already present; skip')
    else:
        must_one(readme, '- **第334回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第334回:')]
        assert len(hits) == 1, 'README anchor 第334回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    if '- [GOV-606](gov/GOV-606.md)' in index:
        print('INDEX: GOV-606 line already present; skip (already pushed in commit 1)')
    else:
        must_one(index, '- [GOV-605](gov/GOV-605.md) — ')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-605](gov/GOV-605.md) — ')]
        assert len(hits) == 1, 'INDEX anchor GOV-605 found %d' % len(hits)
        lines[hits[0] + 1:hits[0] + 1] = [GOV606_LINE, GOV607_LINE, GOV608_LINE]
        index = '\n'.join(lines)
        must_one(index, '## 行政・公的機関（603件）')
        index = index.replace('## 行政・公的機関（603件）', '## 行政・公的機関（606件）', 1)
        must_one(index, '資料ファイル総数: 1853件')
        index = index.replace('資料ファイル総数: 1853件', '資料ファイル総数: 1856件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-606/607/608 inserted + counts updated (行政603->606・総数1853->1856)')


if __name__ == '__main__':
    main()
