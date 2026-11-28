#!/usr/bin/env python3
# retrigger: 390 (paths filter firing)
# -*- coding: utf-8 -*-
"""第390回: READMEに実行記録bulletを挿入し、INDEXにGOV-640・ORG-053・ORG-054の3行を挿入・計数更新するヘルパー。
使い方: python3 .390-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第389回:' 行の直後に .390-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [GOV-639]' 行の直後に GOV-640 の1行を挿入、
  '- [ORG-052]' 行の直後に ORG-053・ORG-054 の2行を挿入し、
  '## 行政・公的機関（637件）'→'（638件）'、'## 企業・団体の公式発表（52件）'→'（54件）'、
  '資料ファイル総数: 1990件'→'1993件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.390-bullet.txt')

LINES = {}
LINES['GOV-640'] = '- [GOV-640](gov/GOV-640.md) — 練馬わがまち資料館「ねりまの川」田柄用水シリーズ最終回「田柄用水 暗きょへ」（column/3731・2024.11.1公開・元=ねりま区報昭和62年11月21日号・北沢邦彦・2026-11-28・第390回・Wayback 2025-09-28本文全文取得＝直接確認・repo grep 0件＝repo初出・GOV-630〔3632・3656・3688〕の続き）— ①**昭和18年成増飛行場建設で田柄川沿いの水田つぶれ・用水は暗きょ化・数流あった自然の川も埋立**（PAP-093の1943年流路変更・旧流路埋立説と整合する区公式側記述）＋その後の空襲で上流部も水路破損・ついに水が通わない状況②**戦後グラントハイツ化で田柄用水に再び通水するも水田は復帰せずその歴史を閉じる**③**昭和40年頃・富士街道沿いの用水の暗きょ化工事（石神井庁舎前付近はそれ以前に暗きょ）＝田柄用水の暗渠化着手年次の公的側初出文言**④**用水から南の石神井川へ向かう放水路を数か所に埋設**（水害対策）⑤**田柄川＝昭和39年護岸工事→下水道幹線として昭和46年9月工事開始**＝PAP-093「1970年代下水道幹線転用」を着工年に具体化する行政側記述⑥写真キャプション: **暗きょになった田柄用水（土支田二丁目付近）＝昭和60年頃・田柄川暗きょ化工事（錦一丁目）＝昭和54年頃**・狩野川台風浸水のグラントハイツ建物＝昭和33年⑦**「やっかい堀」呼称が田柄用水の文脈で区公式記事に現れる**（BLOG-118の伝聞と接続）・昭和7年以降北町〜錦の耕地整理・区画整理・東武練馬からグラントハイツへの引き込み線用地＝多くは旧水田・昭和33年9月狩野川台風＝水害対策上の教訓 ／ 旧番号: — ／ 直接確認（Wayback本文全文・ai）'
LINES['ORG-053'] = '- [ORG-053](org/ORG-053.md) — 公益財団法人東洋文庫ミュージアムワークショップ「見て！歩いて！古地図を楽しもう～再興された千川上水～」（2025-11-29開催・2026-11-28・第390回・Wayback 2026-04-17本文全文取得＝直接確認・repo grep 0件＝repo初出）— 講師**中村佳史氏（株式会社HUMIコンサルティング）**・第一部座学（古地図の読み方・岩崎久彌・岩崎家4代）＋第二部**東洋文庫から台東区池之端の旧岩崎邸庭園（岩崎久彌本邸）まで約5km散策**・参加費2900円・定員20人。**「このルートは、久彌の父・岩崎彌太郎が会社をつくって再興した『千川上水』の跡とも重なります」＝千川水道会社（明治13年設立・GOV-077・PAP-023）の岩崎再興説が2025年時点で公的財団の一般向け文化イベントの題号「再興された千川上水」として受容されている評価史の定点**。東洋文庫（1924年岩崎久彌創設）〜旧岩崎邸庭園〜千川上水跡を1つの文化ルートとして提示した初出例（ルート詳細は未記載のため流路観は断定せず） ／ 旧番号: — ／ 直接確認（Wayback本文全文・ai）'
LINES['ORG-054'] = '- [ORG-054](org/ORG-054.md) — 雑司が谷未来遺産（雑司が谷未来遺産推進協議会・豊島区公式頁掲載団体）「おすすめスポット」清立院・雑司が谷中央児童遊園（2026-11-28・第390回・curl本文全文取得＝直接確認・「zoushigaya-mirai＋清立院＋弦巻川」repo grep 0件＝repo初出）— **「清立院の前には、今は暗渠となった弦巻川が流れていたため、急な階段を登った先に入り口があります」＝清立院前の崖＝弦巻川暗渠とする地域団体公式ページの微地形記述〔repo初出文言〕**（清立院前「当所石橋施主木村氏」碑〔四河川の橋名・橋跡調査・BLOG-049系〕と同じ寺の地形側叙述）＋**夜はアプローチの連なった提灯に照らされる暗渠沿いの夜間景観記述**・雑司が谷中央児童遊園＝**弦巻通りに面した小さな公園**・トップ文言「雑司ヶ谷の『暗渠』である、消えた『弦巻川』を歩いて辿ってみました」（としま案内人案内＝ORG-017系と同じ活動の別媒体記録）。個人散歩記でなく団体公式頁が弦巻川暗渠の微地形を記述した点が新しく、弦巻川雑司が谷区間の地形接続の傍証資料（観察系） ／ 旧番号: — ／ 直接確認（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第390回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第390回:' in readme:
        print('README: 第390回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第389回:')]
        assert len(hits) == 1, 'README anchor 第389回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [GOV-640]' in index:
        print('INDEX: GOV-640 already present; skip')
    else:
        assert '## 行政・公的機関（637件）' in index, 'INDEX 行政 heading mismatch'
        assert '## 企業・団体の公式発表（52件）' in index, 'INDEX 団体 heading mismatch'
        assert '資料ファイル総数: 1990件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-639]')]
        assert len(ghits) == 1, 'INDEX anchor GOV-639 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['GOV-640'])
        ohits = [i for i, l in enumerate(lines) if l.startswith('- [ORG-052]')]
        assert len(ohits) == 1, 'INDEX anchor ORG-052 found %d' % len(ohits)
        lines.insert(ohits[0] + 1, LINES['ORG-053'])
        lines.insert(ohits[0] + 2, LINES['ORG-054'])
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（637件）', '## 行政・公的機関（638件）')
        index = index.replace('## 企業・団体の公式発表（52件）', '## 企業・団体の公式発表（54件）')
        index = index.replace('資料ファイル総数: 1990件', '資料ファイル総数: 1993件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-640・ORG-053・ORG-054 inserted; counts updated')


if __name__ == '__main__':
    main()
