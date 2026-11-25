#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第319回: READMEに実行記録bulletを挿入しINDEXにMAP-222・GAZ-189行を追加するヘルパー。
使い方: python3 .319-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第318回:' 行の直後に .319-bullet.txt の1行を挿入（'- **第319回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-221行の直後にMAP-222行、GAZ-188行の直後にGAZ-189行を挿入し、
  地図・絵図221→222件・地誌・行政史料188→189件・資料ファイル総数1823→1825件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.319-bullet.txt'

MAP222_LINE = (
    '- [MAP-222](maps/MAP-222.md) — 大鳥圭介 著『武蔵国並東京古今沿革圖識』（丸善・1886・767817）'
    '（2026-11-25・第319回・lab全文ZIP＋ページ座標JSONで取得）'
    '— 第10図版余白通史の「○四代將軍承應二年神田上水玉川上水ヲ通ス（年号欠落）七年ニ止ム牛込ヨリ御茶ノ水ノ筋ヲ堀割リ…」＝承応2年（1653）神田・玉川上水通水の図識レベル年代記録'
    '（座標隣接で一文連続性を確認・第18図版の開化事蹟年譜表「神田上水玉川上水ヲ都下ニ引ク」と整合）'
    '・千川ルート旁の図上注記「千川上水」「ハ安永」「九年一成リ天明」＝千川上水安永九年（1780）成立メモの1886年図資料側での存在が座標クラスタで確定'
    '〔「七年ニ止ム」の帰属は〔A〕千川注記に連結し「天明七年ニ止ム」＝天明七年説（GAZ-002北豊島郡誌別伝系統）への傍証候補／〔B〕余白通史側の独立文言（y座標約1700pxの乖離が課題）の2仮説対立＝原画像照合まで断定しない・天明六年説主流（GOV-171・GAZ-041〜049・BOOK-320）への対校資料〕'
    '・第14図版「江戸洪水記」引用の天明六年七月洪水「小日向邊床上五寸ヨリ一尺五寸マテ」＝小日向床上浸水記録候補（千川再停止の年代記系と同年の大水という観察のみ記録）'
    '・全48コマで弦巻川・水窪川・谷端川・音羽0件の陰性'
    ' ／ 旧番号: — ／ OCR全文＋座標JSON確認（原画像照合を要する・文言復元部は推定）（ai）'
)
GAZ189_LINE = (
    '- [GAZ-189](gazetteers/GAZ-189.md) — 平凡社 編『大百科事典』第28巻（索引）（平凡社・1935・1265721）'
    '（2026-11-25・第319回・lab全文検索で取得）'
    '— 索引全文掃引でrepo初出の見出し所在を確認: 千川上水=15-136（参照13-41C・27-27E・隣接見出しに千貫樋15-137）'
    '・谷端川=9-320E・神田上水=6-174＋淀橋26-36・淀橋淨水場27-88H・音羽(東京)=4-166'
    '・弦巻川・音羽川は索引0件の陰性・水窪川27-430Eは同頁の「水窪」27-430（静岡）に隣接＝静岡側同名異川の可能性が高く東京の水窪川とは断定しない'
    '＝1935年事典レベルで千川上水・谷端川が独立見出しを持つ一方で谷頭小河川が不在の認識格差の同一書内対比'
    '（本文巻はデジタル化なし＝見出し所在のみの収録で内容記述はしない）'
    ' ／ 旧番号: — ／ 所在のみ（索引巻OCR全文確認・本文巻未見）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def insert_after(lines, prefix, new_lines, label):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, 'anchor %r found %d times (abort)' % (prefix, len(hits))
    pos = hits[0] + 1
    for off, nl in enumerate(new_lines):
        lines.insert(pos + off, nl)
    print('%s: inserted %d line(s) after %s (line %d)' % (label, len(new_lines), prefix, hits[0] + 1))
    return lines


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第319回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第319回:' in readme:
        print('README: 第319回bullet already present; skip')
    else:
        must_one(readme, '- **第318回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第318回:')]
        assert len(hits) == 1, 'README anchor 第318回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[MAP-222](maps/MAP-222.md)' in index:
        print('INDEX: MAP-222 line already present; skip')
    else:
        must_one(index, '- [MAP-221](maps/MAP-221.md)')
        must_one(index, '- [GAZ-188](gazetteers/GAZ-188.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [MAP-221](maps/MAP-221.md)', [MAP222_LINE], 'INDEX')
        lines = insert_after(lines, '- [GAZ-188](gazetteers/GAZ-188.md)', [GAZ189_LINE], 'INDEX')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 地図・絵図（221件）', '@@MAPHEAD@@', 1)
        index = index.replace('@@MAPHEAD@@', '## 地図・絵図（222件）', 1)
        index = index.replace('## 地誌・行政史料（188件）', '@@GAZHEAD@@', 1)
        index = index.replace('@@GAZHEAD@@', '## 地誌・行政史料（189件）', 1)
        index = index.replace('資料ファイル総数: 1823件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1825件', 1)
        must_one(index, '## 地図・絵図（222件）')
        must_one(index, '## 地誌・行政史料（189件）')
        must_one(index, '資料ファイル総数: 1825件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 地図・絵図（221件）') == 0
        assert index.count('## 地誌・行政史料（188件）') == 0
        assert index.count('資料ファイル総数: 1823件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: MAP-222 / GAZ-189 lines inserted; counts updated 221→222・188→189・1823→1825')

    print('INSERT-319 OK')


if __name__ == '__main__':
    main()
