#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第374回: READMEに実行記録bulletを挿入し、INDEXにGOV-630・GOV-631・ORG-051行を挿入・計数更新するヘルパー。
使い方: python3 .374-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第373回:' 行の直後に .374-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-629 行の直後に GOV-630・GOV-631 の2行、ORG-050 行の直後に ORG-051 の1行を挿入し、
  '## 行政・公的機関（627件）'→'（629件）'、'## 企業・団体の公式発表（50件）'→'（51件）'、
  '資料ファイル総数: 1938件'→'1941件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.374-bullet.txt')

GOV_LINE_630 = '- [GOV-630](gov/GOV-630.md) — 練馬わがまち資料館「ねりまの川」田柄用水3本 — 経路・開発・水田利用の形（column/3632・3656・3688・2024.7〜9.1再録・北沢邦彦・ねりま区報昭和62年6〜8月号連載の再編・2026-11-27・第374回・直はサイトメンテ中のためWaybackスナップショットで本文全文取得＝直接確認・repo grep 0件＝repo初出）— 経路: 田柄用水=田柄四丁目天祖神社前の東西道路に沿い東流し旧川越街道を経て北町一丁目で田柄川に合流（道路下に埋設）・天祖神社前に用水の石橋が現存（令和4年写真）・田無橋場バス停=玉川上水分水路の集束地点 ／ 開発: 明治3年通船計画（明治5年5月中止）で分水口廃止→新堀用水（小平監視所）経由切替・土支田の小島家の明治4年正月増水計画文書（水田増=税増の趣旨）・村別水田拡張面積（田無25・上保谷25・関1・上石神井2町5反・下石神井7・田中4・下土支田9・上練馬3・下練馬4町歩）・明治4年5月完成（4月25日とも）・費用1,350両・名称変遷（玉川上水北側新井筋分水→田柄田用水→田柄用水）・明治10年玉川上水引水50%制限・明治15年上/下練馬村との水利用協定・工場用水の水系連関（火薬製造所・王子製紙・印刷局抄紙部は初め千川上水や石神井川の水を利用したが足りず田柄用水系統の増水を働きかけ=千川上水水利史〔BOOK-220替水約定・BLOG-095分配堰碑・GOV-058抄紙部給水〕の隣接系統側裏付け）・明治26年大幅増水+王子村外22か村との水利用契約書・**明治26年11月・水神を祀る記念碑建立（現田柄四丁目天祖神社所在）=BLOG-360「上練馬村玉川上水分水紀念碑」の公的側裏付け（同一碑と推定されるが断定は碑文採録まで保留）** ／ 水田利用: 埼玉県行政文書（保谷市史所収）・合計80町5反歩79.8ha（石神井川沿い60余町歩+田柄川沿い16町歩）・明治8年武蔵国郡村誌「柳沢用水」=repo初出候補・安政6年上練馬村絵図の田柄一丁目水田・下練馬村絵図（石神井公園ふるさと文化館所蔵）の北町帯状水田・**下練馬村絵図「溜井」（上練馬村境=現北町八丁目南西付近）=遊歴雑記「練馬下田柄村の池」（約1町四方・用水のため掘設）の符合=repo初出**・田柄川の谷の西先端=土支田三丁目付近・明治2年土支田村絵図の自然水路・明治44年1万分の1地形図で光が丘西端まで水田地帯 ／ 旧番号: — ／ 直接確認（Wayback本文全文3頁・第374回）（ai）'
GOV_LINE_631 = '- [GOV-631](gov/GOV-631.md) — 練馬わがまち資料館「ねりまの地名今むかし 現町名12＜田柄 たがら＞」（column/1163・2021.11.1公開・桑島新一・ねりま区報昭和60年3月11日掲載の再構成・2026-11-27・第374回・直はサイトメンテ中のためWaybackスナップショットで本文全文取得＝直接確認・repo grep 0件＝repo初出）— 江戸期の田柄は約2倍広さ（東は北町自衛隊付近〔下田柄〕〜西は光が丘〔上田柄〕・上/下練馬村跨り）・**寛永16年1639検地帳に見られる古い地名・由来は定かでない**・『四神地名録』田柄条「畑在所にて田方一分ばかり、風土すぐれず広きといふのみ」の応用（GAZ-084/085既収録の田柄条引用）・年貢率低い・明治4年玉川上水分水引入成功・**「田柄用水記念碑」の区史跡指定表記（田柄4-27天祖神社）**・昭和7年板橋区練馬田柄町・30年代からの宅地化で「やっかい堀」・**47年ごろから暗渠化工事（GOV-075の47年度着工・ORG-051の46年9月起工と併せ3説併記）**・「練馬だいこんコース」（練馬大根を流れで洗ったことにちなむ緑道愛称）=repo初出・昭和42年住居表示・桑島新一「田柄川今昔」の著作存在 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第374回）（ai）'
ORG_LINE_051 = '- [ORG-051](org/ORG-051.md) — 東京都立田柄高等学校「TGR光が丘今昔」水系関連8回（第十二代校長 加藤竜吾・2021-08〜11・全86回地域史連載の水系回＝田柄橋・光が丘の地形・主なしの松・土支田八丁堀・お玉が池・田柄川その1/2・田柄水道・2026-11-27・第374回・本文8頁全文直接取得・repo grep 0件＝repo初出）— **①田柄川幹線の区域別暗渠化年次（昭和46年9月起工→48年北町二丁目練馬駐屯地官舎裏着手→田柄〜光が丘〜北町一丁目52年完成→錦地区56年完成）＝repo初出の精度（GOV-075の47年度大々的着工・PAP-008の幹線直径と整合）②狩野川台風（昭和33年）のグラントハイツ浸水 ③「厄介堀」第2語源（田柄用水守るための掘削掃除除草の維持負担由来=BLOG-118の汚水氾濫由来と対立併記）④お玉が池（白子川支流）の明細書上帳（明治9年・東西11間20m南北21間38m周囲66間）と東京府志料（明治7年・御玉ヶ池周囲60間）の寸法文言・1943年成増飛行場建設で谷ごと埋め立て（場所=グラントハイツ下士官クラブ跡ヒマラヤ杉付近）⑤八丁堀児童公園案内文全文（寛文3年1663頃・武蔵国土支田村字八丁堀・約八丁900m由来・旭町一丁目町会+光が丘第一自治会）・八丁堀は田柄用水以前から・丈八尺大水車が並ぶ・八丁堀三吉囃子（区教委指定無形文化財）⑥「田柄用水七つの謎」（練馬区教委2003・平田2004）の研究の存在 ⑦武蔵国土支田村小島家文書（練馬区教委1993編）に万延元年1860記録・明治2年完成説vs明治4年5月開通説の本文内対立（西暦誤記「1969年」は原文まま）・慶応元年下土支田村村高578石8斗2合108戸654人 ⑧棚橋（旧大山道の橋・平成15年まで欄干現存→環八工事でメモリアル化）・田柄橋（グラントハイツ〜豊島園通り・秋の陽公園前横断歩道付近）の橋名群・秋の陽公園の「田柄川幹線埋設位置」石柱3本 ⑨「主なし」語源説（大水で流されるため誰も住まなかった土地）・篠崎善七撮影の昭和初期写真 ⑩田柄水道（正式名称・初代理事長上野徳次郎・愛染院墓地阿弥陀堂横顕彰碑昭和49年建立・桔梗屋の昭和38年深井戸地下200m）＝BLOG-351/360の組合側補完（区議長上野徳次郎GOV-075と同姓同名・別人物候補）・成増飛行場建設で田柄川は土管で地中に埋めた観察・行政上の田柄川=秋の陽公園〜桜川一丁目合流まで4.5kmで田無〜光が丘は「ドブ川」扱い・都中小河川緊急整備五ヵ年計画で43年から川幅6m拡幅 ／ 旧番号: — ／ 直接確認（本文8頁全文・第374回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第374回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第374回:' in readme:
        print('README: 第374回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第373回:')]
        assert len(hits) == 1, 'README anchor 第373回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-630' in index:
        print('INDEX: GOV-630 already present; skip')
    else:
        assert '## 行政・公的機関（627件）' in index, 'INDEX 行政 heading mismatch'
        assert '## 企業・団体の公式発表（50件）' in index, 'INDEX 企業団体 heading mismatch'
        assert '資料ファイル総数: 1938件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-629]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-629 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, GOV_LINE_630)
        lines.insert(ghits[0] + 2, GOV_LINE_631)
        ohits = [i for i, l in enumerate(lines) if l.startswith('- [ORG-050]')]
        assert len(ohits) == 1, 'INDEX anchor ORG-050 found %d' % len(ohits)
        lines.insert(ohits[0] + 1, ORG_LINE_051)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（627件）', '## 行政・公的機関（629件）')
        index = index.replace('## 企業・団体の公式発表（50件）', '## 企業・団体の公式発表（51件）')
        index = index.replace('資料ファイル総数: 1938件', '資料ファイル総数: 1941件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-630/631 + ORG-051 inserted; counts updated')


if __name__ == '__main__':
    main()
