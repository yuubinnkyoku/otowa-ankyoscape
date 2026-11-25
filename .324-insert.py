#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第324回: READMEに実行記録bulletを挿入しINDEXにGAZ-194行を追加するヘルパー。
使い方: python3 .324-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第323回:' 行の直後に .324-bullet.txt の1行を挿入（'- **第324回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: '- [GAZ-193](gazetteers/GAZ-193.md)' 行の直後にGAZ-194行を挿入し、
  地誌・行政史料193→194件・資料ファイル総数1838→1839件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.324-bullet.txt'

GAZ194_LINE = (
    '- [GAZ-194](gazetteers/GAZ-194.md) — 『東京市史稿』市街編39〜55（東京都編・1952-64・9640901〜9640918・全14巻一括掃引）'
    '（2026-11-25・第324回・lab全文ZIPで取得）'
    '— 白山前町千川屋敷（鋪）の頽勢時代〜明治初年の実務文言群＝'
    '①市街編41の天保14卯年8月23日「千川宇兵衞屋敷上地小石川白山前貳百三拾貳坪餘」町屋敷書抜'
    '（GOV-175〔147〕の天保14年8月22・23日の拝領地引渡文書群と同日付の独立採録・屋敷232坪余が同時点側で裏付け）'
    '②市街編45「頽勢時代（七）請負地拂下事蹟」の測量請取「表田舎間拾五間五尺・同斷南之方十九間壹尺・此坪貳百三拾貳坪五合四勺六才」'
    '＋「裏巾同拾四間貳尺・裏行北之方十壹間壹尺餘」＝千川屋敷の拂下時測量232坪5合4勺6才'
    '（元禄9年惣坪238坪7合〔GOV-175〕との約6坪差の生じた時期・理由は断定せず・間口15間5尺は元禄9・天保14・拂下の3時点で一致）'
    '＋目次でも千川屋敷が芝土手跡町・靈岸橋際埋立地などと並ぶ町級の独立項目'
    '③市街編42の頽勢時代上納金「同千川屋鋪金三分銀拾匁九分九厘四毛」＋直前の「よねた衣笠房次郎」並記'
    '（GAZ-038町鑑の衣笠房次郎・坪三之助並記と整合する13番組系町内秩序の反映候補・GOV-210嘉永3年地代11両との額の不一致は別賦課か確定せず）'
    '④市街編40の町並測量表に「小石川白山前町千川屋鋪同拜領屋鋪分」が独立計上単位（OCR列崩壊のため数値対応づけはせず）'
    '⑤市街編48の番組構成表で千川屋鋪が白山前町と並ぶ構成単位（番組番号の対応は保留・GAZ-037大江戸志9番組火消・GAZ-038町鑑13番組かとの続柄は確定しない）'
    '⑥市街編50の明治2年町名改正の扱い「同所白山前町千川屋敷〇米」（〇米・〇木・〇朱の丸印記号の凡例は原画像未確認で意味は断定しない）'
    '＝千川屋敷が正徳4年（GAZ-191）→天保14年上地（GOV-175+市街編41）→頽勢時代の町並測量・上納金・番組計上（市街編40・42・48）'
    '→拂下測量（市街編45）→明治2年町名改正（市街編50）と独立計上単位として通時的に扱われた系列が単一の編纂物内で揃った'
    '＋市街編51〜54（9640914〜17）はlab本文未公開（公開後に再掃引）＋市街編44=GOV-396既収録'
    '＋四河川の直接文言は13巻中0件の陰性（9640908「戶川道」は青山千駄ヶ谷の小路名で誤検出）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第324回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第324回:' in readme:
        print('README: 第324回bullet already present; skip')
    else:
        must_one(readme, '- **第323回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第323回:')]
        assert len(hits) == 1, 'README anchor 第323回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[GAZ-194](gazetteers/GAZ-194.md)' in index:
        print('INDEX: GAZ-194 line already present; skip')
    else:
        must_one(index, '- [GAZ-193](gazetteers/GAZ-193.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GAZ-193](gazetteers/GAZ-193.md)')]
        assert len(hits) == 1, 'INDEX anchor GAZ-193 found %d' % len(hits)
        lines.insert(hits[0] + 1, GAZ194_LINE)
        index = '\n'.join(lines)
        print('INDEX: GAZ-194 line inserted after line %d' % (hits[0] + 1))
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        must_one(index, '## 地誌・行政史料（193件）')
        index = index.replace('## 地誌・行政史料（193件）', '## 地誌・行政史料（194件）', 1)
        must_one(index, '資料ファイル総数: 1838件')
        index = index.replace('資料ファイル総数: 1838件', '資料ファイル総数: 1839件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (地誌193→194・総数1838→1839)')


if __name__ == '__main__':
    main()
