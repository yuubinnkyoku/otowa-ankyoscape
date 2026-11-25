#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第320回: READMEに実行記録bulletを挿入しINDEXにMAP-223行を追加するヘルパー。
使い方: python3 .320-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第319回:' 行の直後に .320-bullet.txt の1行を挿入（'- **第320回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: MAP-222行の直後にMAP-223行を挿入し、
  地図・絵図222→223件・資料ファイル総数1825→1826件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.320-bullet.txt'

MAP223_LINE = (
    '- [MAP-223](maps/MAP-223.md) — 「六義園全図並八景十二境和歌」（川崎千乕 写・明治22〔1889〕・NDL書誌ID 000007299948・pid/8369260・IIIF画像4コマ・PDM・請求番号亥-104・DOI 10.11501/8369260）'
    '（2026-11-25・第320回・jpsearch→IIIFマニフェストで取得）'
    '— NDL所蔵の六義園全図写し（全図＋八景十二境和歌・全4コマ）と東京国立博物館COLBASE「慶信／六義園全図」（A-7078・CC BY）の所在記録'
    '＝BOOK-322の「柳澤侯六義園全圖」・PAP-109の『六義園の図』（大泉水給水遺構との一致が発掘で裏付けられた絵図）の所在候補（仮説）'
    '＝「千川上水の水を注ぐ大泉水」文言の図上照合がIIIFで可能になった段階の所在固定'
    '〔竜居言及図・PAP-109引用図との同一性と図中の水系注記の判読は未実施〕'
    ' ／ 旧番号: — ／ 書誌・IIIF所在確認（マニフェスト・コマ構成まで直接確認・図の判読は未実施）（ai）'
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
    assert bullet.startswith('- **第320回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第320回:' in readme:
        print('README: 第320回bullet already present; skip')
    else:
        must_one(readme, '- **第319回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第319回:')]
        assert len(hits) == 1, 'README anchor 第319回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[MAP-223](maps/MAP-223.md)' in index:
        print('INDEX: MAP-223 line already present; skip')
    else:
        must_one(index, '- [MAP-222](maps/MAP-222.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [MAP-222](maps/MAP-222.md)', [MAP223_LINE], 'INDEX')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 地図・絵図（222件）', '@@MAPHEAD@@', 1)
        index = index.replace('@@MAPHEAD@@', '## 地図・絵図（223件）', 1)
        index = index.replace('資料ファイル総数: 1825件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1826件', 1)
        must_one(index, '## 地図・絵図（223件）')
        must_one(index, '資料ファイル総数: 1826件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 地図・絵図（222件）') == 0
        assert index.count('資料ファイル総数: 1825件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: MAP-223 line inserted; counts updated 222→223・1825→1826')

    print('INSERT-320 OK')


if __name__ == '__main__':
    main()
