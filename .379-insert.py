#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第379回: READMEに実行記録bulletを挿入し、INDEXにBLOG-375・BLOG-376行を挿入・計数更新するヘルパー。
使い方: python3 .379-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第378回:' 行の直後に .379-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-374 行の直後に BLOG-375・BLOG-376 の2行を挿入し、
  '## ブログ・個人サイト（373件）'→'（375件）'、'資料ファイル総数: 1957件'→'1959件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.379-bullet.txt')

BLOG_LINE_375 = '- [BLOG-375](blogs/BLOG-375.md) — 歴史探訪と温泉（hotyuweb）「江戸史蹟散歩 江戸川公園／大洗堰」（xrea旧サイト・Shift_JIS・2004年頃〔推定・断定せず〕）（2026-11-28・第379回・curl本文全文取得（Shift_JIS→UTF-8）＝直接確認・repo grep 0件＝repo初出〔BLOG-356は同サイトの神田上水遺構〔本郷〕別記事〕）— 江戸川公園・大洗堰周辺の説明板6点全文転写＝①「大洗堰の由来碑について」（平成3年・文京区役所）＝大正8年公園整備→昭和12年江戸川（神田川）改修で堰体失われ→翌13年堰部材再利用で由来碑建立→由来碑も失われ碑文のみ近年発見→平成3年再設置＝「取水口は昭和8年にふさがれた」（BLOG-358/359）と別過程として対校可能な堰体喪失の年次列がrepo初出（断定せず・GOV-303の昭和12年改修進捗表と接続）②「角落」板の流量調節石柱（昭和58年説明板）＝取水口の石柱と昭和8年廃止時撤去→移設の文言がrepo初出（PAP-124の「角落」語と接続）③大洗堰跡（昭和62年・区教委）＝給水先二筋区分（内堀内大名屋敷／本町方面・日本橋の北の町屋）④芭蕉延宝5〜8年居住と藤堂藩改修請負説（平成6年・都みどりの推進委員会）＝BOOK-204/205への平成6年設置説明板レベルの伝承記録⑤大井玄洞治水の年次細目（明治43年洪水→大正2年着手・同8年完成・昭和3年胸像）＝BOOK-139・BLOG-189に補完⑥『江戸の今昔』（昭和7年）「関口の大瀧」＝取水口閉塞直前の水質悪化実況（「昔日の如く水清らかならず」）がrepo初出・一休橋・水神社縁起も記す ／ 旧番号: — ／ 直接確認（curl本文全文・第379回）（ai）'

BLOG_LINE_376 = '- [BLOG-376](blogs/BLOG-376.md) — Natrium.jp「田柄用水・田柄川」シリーズ4頁（tagara01〜04・撮影2012〜2018・執筆2015年頃）（2026-11-28・第379回・curlで4頁本文全文取得＝直接確認・既収録25頁に未収録＝repo初出・目次頁403・「その2」相当頁404でシリーズ構成は未完結＝次回再試行課題）— 田柄用水の全流路実地観察＝土支田区間の枯れ川（旧谷）と用水の付け替え読図（アポロ公園90°転回・俵久保字名・長久保道・地蔵通りS字カーブ・土支田農業公園）がrepo初出・けやき憩いの森の「練馬区登録史跡」看板の存在（BLOG-328に補完）・富士町交差点の北側迂回（付け替え推定）・昭和31年米軍空中写真で田無用水との分水口確認＝BLOG-278（musasinowalker）と独立の全流路観察・東田柄橋の標柱と水位掲示板＝橋名調査への追加候補・ハッスル通り商店街（1965年創立）・元禄9年笠付き青面金剛像・延亨2年青面金剛像・宝暦14年「上練馬村神明ヶ谷戸講中」庚申塔＝「神明ヶ谷戸」字名と上練馬村講中の石造物がrepo初出（BLOG-360の「上練馬村」碑刻字と同村の字名資料）・田柄川北側の水路群（阿弥陀堂脇の蓋暗渠・昭和22年空中写真・赤塚新町三丁目の谷）＝BLOG-366の赤塚新町流れと対校 ／ 旧番号: — ／ 直接確認（curl本文全文・第379回）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第379回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第379回:' in readme:
        print('README: 第379回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第378回:')]
        assert len(hits) == 1, 'README anchor 第378回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-375' in index:
        print('INDEX: BLOG-375 already present; skip')
    else:
        assert '## ブログ・個人サイト（373件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1957件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        bhits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-374]')]
        assert len(bhits) == 1, 'INDEX anchor BLOG-374 found %d' % len(bhits)
        lines.insert(bhits[0] + 1, BLOG_LINE_375)
        lines.insert(bhits[0] + 2, BLOG_LINE_376)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（373件）', '## ブログ・個人サイト（375件）')
        index = index.replace('資料ファイル総数: 1957件', '資料ファイル総数: 1959件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-375, BLOG-376 inserted; counts updated')


if __name__ == '__main__':
    main()
