#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第378回: READMEに実行記録bulletを挿入し、INDEXにBLOG-367〜374行を挿入・計数更新するヘルパー。
使い方: python3 .378-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第377回:' 行の直後に .378-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-366 行の直後に BLOG-367〜374 の8行を挿入し、
  ブログ365→373件・総数1949→1957件を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.378-bullet.txt')

ROWS = [
    '- [BLOG-367](blogs/BLOG-367.md) — わんじん「田柄川　－命の水をつなぐ河川網の形成と現代の親水体験－」（2017-10-25・wanjin.blog.fc2.com/blog-entry-215.html・2026-11-28・第378回・?no=形式レシピでcurl本文全文取得＝直接確認・repo未収録URL）— **①旧田柄川は「韮窪（現三原台）」の湧水起源・田柄谷（光が丘）まで涸れ川〔repo grep「韮窪」0件〕②田柄用水の「わずか半年」工期説（涸れ川活用・田無用水経由で開削短縮）③栗原堰から中用水（稲付川）への揚げ堀供給〔repo grep 0件〕・明治5年智清寺水争いの叙述 ④管理起点＝田柄高校前交差点のそば ⑤明治20年代の増水整備と下練馬宿方面用水路の廃止説〔repo初出候補〕⑥1943年成増飛行場建設で用水は暗渠化 ⑦「1980年代前半にはすべての流路が暗渠化」説〔repo grep新出〕＝ORG-051の幹線年次（46年起工→56年完成）と整合 ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-368](blogs/BLOG-368.md) — わんじん「田柄川　－このやり場のないもやもや感…－」（2017-11-01・wanjin.blog.fc2.com/blog-entry-216.html・2026-11-28・第378回・curl本文全文取得＝直接確認）— 管理起点の位置具体化（田柄高校前交差点東側・秋の陽公園内の「田柄川幹線埋設位置」標識＝ORG-051の石柱3本と整合）・用水路網の暗渠路密集域の観察・**「『田柄川』幹線水位状況」電光掲示板〔repo初出〕**（埼玉道=特例都道442号線交差点）・埼玉道交差北側のかつての溜井〔GOV-630下練馬村絵図「溜井」の比定保留〕・北町八丁目の用水合流（BLOG-366の車道併設終了部読図の実走裏付け） ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-369](blogs/BLOG-369.md) — わんじん「田柄川　－偉大な記録の量産…－」（2017-11-08・wanjin.blog.fc2.com/blog-entry-217.html・2026-11-28・第378回・curl本文全文取得＝直接確認）＝田柄川橋跡の橋名群 — **橋名約20件＝repo初出の橋名群**: 仲之台橋・大堰橋・大豊橋・池の上橋（北町六丁目支流合流点）・観音橋・上宿橋・阿弥陀橋・富士橋（徳川綱吉御殿跡之碑の角地）・北子橋（銘板判読不能・筆者が公開質問中）・棚橋（橋柱と銘板現存＝ORG-051の棚橋と対応候補）・高徳橋・北町橋・金乗橋・渡戸橋（東本村庚申塚・田柄用水合流点）・横寺橋・円明橋（圓明院由来）・今神橋・宮元橋・仲一橋・金越橋・神明橋＋現役の練馬北町陸橋（環八）・「御殿」小字と練馬大根起源伝承 ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-370](blogs/BLOG-370.md) — わんじん「田柄川　－対抗意識丸出し…本流と神々しい揚げ堀－」（2017-11-15・wanjin.blog.fc2.com/blog-entry-218.html・2026-11-28・第378回・curl本文全文取得＝直接確認）— **練馬区の「管理終点」の観察〔repo初出〕**（城北中央公園最北部・管理起点=田柄高校前〔BLOG-367〕と対になり行政上の田柄川両端が観察レベルで揃った）・桜川緑道の規模（賞味500m・花崗岩案内碑・親水スペース）・**栗原堰→揚げ堀の流路の具体化（田柄川と合流→桜川小学校・安養院敷地内を通過→中用水）**〔BLOG-367の位置補完〕・上板橋村役場跡（安養院の揚げ堀を挟んだ反対側）〔repo grep 0件〕・石神井川改修で堰の痕跡は消失 ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-371](blogs/BLOG-371.md) — わんじん「田柄用水　－大山詣り…－」（2017-11-22・コメント欄2019-10-18・wanjin.blog.fc2.com/blog-entry-219.html・2026-11-28・第378回・curl本文全文取得＝直接確認）— 1871年10カ村（田無・上保谷・関・上下石神井・谷原・田中・下土支田・上下練馬）灌漑目的の別名群（玉川上水北側新井筋分・田無町外八ケ村組合用水）・**田無用水「やすらぎのこみち」側からの分水・初期分水位置は田無警察署の西側→東側に移設〔repo初出候補〕**・上流部の蓋暗渠形態観察（北原交差点・北原町一丁目）・ふじ大山道道標（宝暦3年・川越街道分岐点）・**コメント欄のマーボ丼氏による50年前の開渠記憶の生証言〔repo初出〕**（北原交差点から下流は開渠・所沢街道北側沿い・ひばりヶ丘停車場線は用水横の小径＝1970年前後の実態の聴取記録） ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-372](blogs/BLOG-372.md) — わんじん「田柄用水　－執着まみれの我欲の塊－」（2017-12-13・wanjin.blog.fc2.com/blog-entry-222.html・2026-11-28・第378回・curl本文全文取得＝直接確認・第377回ノートの?no=222取得課題を解消）— **旧田柄川水路活用部（「ぐりんぐりん」蛇行）の実走観察**: 谷原四丁目20（直前に水車・説明省略）・土支田農業公園・土支田バードグリーン広場・豊渓小学校・たわらくぼ児童遊園・アポロ公園・笹目通り・豊渓歩道橋〔いずれもrepo grep 0件〕・「半年の突貫工事」の理由付け（BLOG-367と同一説を流路形態面から補強）・**用水と田柄川の分離位置＝都営光が丘第二アパート付近の読図〔repo初出候補〕**・なお?no=224は隅田川記事でスコープ外と判定（第377回ノートの見出し対応の誤りを訂正） ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-373](blogs/BLOG-373.md) — わんじん「田柄用水」下練馬宿3回（2018-01-17/24/31・wanjin.blog.fc2.com/blog-entry-228〜230.html・2026-11-28・第378回・3回ともcurl本文全文取得＝直接確認・3回を1 sourceとして採録）— 「北町支流（仮）」の命名〔BLOG-369/374の支流群との同定が課題〕・東京聖徳病院脇の水路敷→上宿で川越街道南側→北町観音堂で北側→北町浅間神社・富士塚・**北町浅間神社から500mの間に田柄川へ向かう水路5箇所**・**木下家本陣跡（→大木家本陣に引継・現UR東武練馬アパート）・内田家脇本陣跡・島野家問屋場跡（現エイトサイド新和）の位置〔repo grep 0件〕**・**「下宿水車」〔repo初出の水車名〕**・流末は東本村庚申塚の「渡戸橋」で合流（BLOG-369の橋名観察と独立一致） ／ 旧番号: — ／ 直接確認（ai）',
    '- [BLOG-374](blogs/BLOG-374.md) — わんじん「田柄川支流」練馬駐屯地東西2回（2018-02-07/14・wanjin.blog.fc2.com/blog-entry-231〜232.html・2026-11-28・第378回・2回ともcurl本文全文取得＝直接確認・2回を1 sourceとして採録）— **駐屯地西支流の流路**（平和台駅近辺源流→北町西小学校東交差点→駐屯地西側→練馬車検場前→北町中学校北東角＝「池の上橋」で合流〔BLOG-369の北町六丁目支流と一致〕）・**駐屯地東支流の2源流（1960年東京都市計画図の仲町五丁目起点・光が丘警察署北町交番横で合流）**・**「右ふじ大山道」道標を兼ねた庚申塔＝「文政四辛巳年…」「武刕豊嶋郡下練馬驛上宿」刻字〔repo初出〕**・合流点の「富士橋」の帰属問題（街道交差点側の富士橋〔BLOG-369〕との関係は断定せず） ／ 旧番号: — ／ 直接確認（ai）',
]


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第378回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第378回:' in readme:
        print('README: 第378回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第377回:')]
        assert len(hits) == 1, 'README anchor 第377回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-374' in index:
        print('INDEX: BLOG-374 already present; skip')
    else:
        assert '## ブログ・個人サイト（365件）' in index, 'INDEX blog heading mismatch'
        assert '資料ファイル総数: 1949件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits_blog = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-366]')]
        assert len(hits_blog) == 1, 'INDEX anchor BLOG-366 found %d' % len(hits_blog)
        for k, r in enumerate(ROWS):
            lines.insert(hits_blog[0] + 1 + k, r)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（365件）', '## ブログ・個人サイト（373件）')
        index = index.replace('資料ファイル総数: 1949件', '資料ファイル総数: 1957件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-367..374 inserted; counts updated')


if __name__ == '__main__':
    main()
