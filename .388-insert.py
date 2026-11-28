#!/usr/bin/env python3
# retrigger: 388 (paths filter firing)
# -*- coding: utf-8 -*-
"""第388回: READMEに実行記録bulletを挿入し、INDEXにPAP-126の1行を挿入・計数更新するヘルパー。
使い方: python3 .388-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第387回:' 行の直後に .388-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: '- [PAP-125]' 行の直後に PAP-126 の1行を挿入し、
  '## 論文・研究報告・データ（123件）'→'（124件）'、'資料ファイル総数: 1988件'→'1989件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.388-bullet.txt')

LINES = {}
LINES['PAP-126'] = '- [PAP-126](papers/PAP-126.md) — 安斎忠雄「農業土木遺産を訪ねて 江戸・武蔵野の命脈--玉川上水・野火止用水・千川用水」『土地改良 : 大地に刻む農の文化』42巻1号 pp.54-59・土地改良建設協会・2004-01（ISSN 09162577・NDL書誌ID 6837599・CiNii crid 1520573329823863424）（2026-11-28・第388回・CiNii/NDL OpenSearch書誌確認・repo grep 0件＝repo初出）— 千川用水を玉川上水・野火止用水と並置する「江戸・武蔵野の命脈」＝農業土木遺産の枠組みで扱った全国誌解説記事で、千川の評価史レーン（江戸名所図会〜BOOK-060〜PAP-083）の2004年の定点候補（本文未取得のため断定せず・「命脈」語の千川への適用例と千川上水/千川用水呼称の使われ方が確認ポイント・シリーズ他回の有無は未確認） ／ 旧番号: — ／ 所在のみ（CiNii OpenSearch RSSメタデータ・NDL書誌・本文未取得）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n').rstrip(' ')
    assert bullet.startswith('- **第388回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第388回:' in readme:
        print('README: 第388回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第387回:')]
        assert len(hits) == 1, 'README anchor 第387回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '- [PAP-126]' in index:
        print('INDEX: PAP-126 already present; skip')
    else:
        assert '## 論文・研究報告・データ（123件）' in index, 'INDEX 論文 heading mismatch'
        assert '資料ファイル総数: 1988件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        ghits = [i for i, l in enumerate(lines) if l.startswith('- [PAP-125]')]
        assert len(ghits) == 1, 'INDEX anchor PAP-125 found %d' % len(ghits)
        lines.insert(ghits[0] + 1, LINES['PAP-126'])
        index = '\n'.join(lines)
        index = index.replace('## 論文・研究報告・データ（123件）', '## 論文・研究報告・データ（124件）')
        index = index.replace('資料ファイル総数: 1988件', '資料ファイル総数: 1989件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: PAP-126 inserted; counts updated')


if __name__ == '__main__':
    main()
