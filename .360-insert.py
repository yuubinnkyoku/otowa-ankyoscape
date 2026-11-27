#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第360回: READMEに実行記録bulletを挿入し、INDEXにGOV-624行を挿入・計数更新するヘルパー。
使い方: python3 .360-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第359回:' 行の直後に .360-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: GOV-623 行の直後に GOV-624 行を挿入し、
  '## 行政・公的機関（621件）'→'（622件）'、'資料ファイル総数: 1913件'→'1914件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.360-bullet.txt')

GOV624_LINE = (
    "- [GOV-624](gov/GOV-624.md) — 東京都下水道局「下水道幹線（第二千川幹線）から河川への放流状況について」"
    "（2022-10-25ニュース＋資料PDF2頁・本文全文抽出＝直接確認・第360回）— 千川幹線の水位高（2021.9.24・"
    "文京区小石川四丁目の公共ます設置工事）を理由とする第二千川幹線への流下経路切替・規定外の流出の確認"
    "（2022.5.26）と切替解消・現地調査で想定構造と齟齬・管路一部閉塞を確認（2022.9月末・原因調査完了2022.10.24）"
    "＝第二千川幹線の放流先は神田川水道橋分水路（文京区後楽一丁目三番地付近）で吐口は潮位で常時水没"
    "〔千川幹線の水位・位置問題（GOV-082千川増強幹線・BLOG-134人孔接続）の2021〜22年の実務例・流下経路図は画像で未判読〕 "
    "／ 旧番号: — ／ 直接確認（ニュース本文＋資料PDF本文抽出・第360回）（ai）"
)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第360回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第360回:' in readme:
        print('README: 第360回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第359回:')]
        assert len(hits) == 1, 'README anchor 第359回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'GOV-624' in index:
        print('INDEX: GOV-624 already present; skip')
    else:
        assert '## 行政・公的機関（621件）' in index, 'INDEX 行政 heading mismatch'
        assert '資料ファイル総数: 1913件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-623]')]
        assert len(hits) == 1, 'INDEX anchor GOV-623 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV624_LINE)
        index = '\n'.join(lines)
        index = index.replace('## 行政・公的機関（621件）', '## 行政・公的機関（622件）')
        index = index.replace('資料ファイル総数: 1913件', '資料ファイル総数: 1914件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-624 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
