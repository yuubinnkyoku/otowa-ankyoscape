#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第358回: READMEに実行記録bulletを挿入し、INDEXにGOV-623行を挿入・計数更新するヘルパー。
使い方: python3 .358-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第357回:' 行の直後に .358-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-622 行の直後に GOV-623 行を挿入し、
  '## 行政・公的機関（620件）'→'（621件）'、'資料ファイル総数: 1912件'→'1913件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.358-bullet.txt')

GOV623_LINE = (
    "- [GOV-623](gov/GOV-623.md) — 東京都公文書館クロス検索「余水」（13件）「洗堰」（17件）「樋線」（76件）掃引で新規特定した"
    "神田上水・千川水道系の実務＋「水車要録」簿冊レコードの書誌確定（601.C8.04・MFコマ0647-1112）— 関口町大洗堰修繕の儀官費申上"
    "（小石川区東青柳町内田常次郎・1883・614.C9.01(*123)・pkey 722018＝水窪川・護国寺門前の谷筋の東青柳町の町内者による神田上水"
    "大洗堰修繕上報の一次記録〔人物比定と上報の動機は本文未見〕）・「水車要録」簿冊（東京市＞水道改良事務所・1894〜96・国重文・"
    "16mmMF市明Ⅰ明29-008コマ0647-1112・D001-RAM・条件付利用〔複製物のみ〕＝MFコマ番号はrepo初出・GOV-618⑥b)の所属簿冊書誌）・"
    "「樋線」掃引の千川水道樋線群はGOV-588の全面重複〔確認〕・「余水」掃引は四河川直接文言なし〔陰性〕 "
    "／ 旧番号: — ／ 所在のみ（一覧頁＋詳細頁目録を機械取得・第358回）（ai）"
)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第358回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第358回:' in readme:
        print('README: 第358回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第357回:')]
        assert len(hits) == 1, 'README anchor 第357回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-623' in index:
        print('INDEX: GOV-623 already present; skip')
    else:
        assert '## 行政・公的機関（620件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1912件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-622]')]
        assert len(hits) == 1, 'INDEX anchor GOV-622 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV623_LINE)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（620件）', '## 行政・公的機関（621件）')
        index = index.replace('資料ファイル総数: 1912件', '資料ファイル総数: 1913件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-623 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
