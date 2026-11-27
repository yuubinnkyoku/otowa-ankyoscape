#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第353回: READMEに実行記録bulletを挿入し、INDEX.mdにGOV-620/BLOG-340/341行を挿入するヘルパー。
使い方: python3 .353-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第352回:' 行の直後に .353-bullet.txt の1行を挿入。
- INDEX.md: GOV-619行の直後にGOV-620行、BLOG-339行の直後にBLOG-340/341行を挿入し、
  行政617→618・ブログ338→340・総数1905→1908の計数を更新。
"""
import io
import os
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs/sources/INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.353-bullet.txt')

GOV_LINE = '- [GOV-620](gov/GOV-620.md) — 板橋区「板橋マニア 『板橋好きが案内する板橋まちガイド』を発行しました」（板橋区公式サイト・ページ番号1006722・更新2020-01-28）— 『板橋マニア』の書誌公式確定＝監修・著作: 板橋区、発行・販売: フリックスタジオ、2018年3月31日初版第一刷（正誤表2018-04-24公開）、本体1,800円＋税、2章「地図を持って歩こう」に「発見！板橋暗渠」「板橋凸凹地形散歩」「いたばし区界探検・東西南北」の3項目名（repo初出）、目次・各章試し読みPDFの公式公開、板橋メディア座談会・荒俣宏×坂本区長対談収録（全264p＝いたばしTIMES二次転記）。「発見！板橋暗渠」の実文と板橋三大暗渠の同定は未確認 ／ 旧番号: — ／ 直接確認（ai）'

BLOG_LINE_340 = '- [BLOG-340](blogs/BLOG-340.md) — 髙山英男「暗パラ裏話 ズッコケ三人組と板橋の暗渠」（毎日暗活！暗渠ハンター・2020年3月14日）— 2020-03-13日刊ゲンダイ北上次郎書評経由で『暗渠パラダイス！』（BOOK-042）[コラム3]「キャラが際立つ板橋三大暗渠」の存在を確認（repo初出）・『板橋マニア』（GOV-620）初稿は「暗渠三兄弟」擬人化設定で執筆もボツになり書き直した経緯＝ボツ初稿の着想がコラムのベースと明記・「全然個性の違う三つの暗渠が仲良く隣り合う」性質文言・板橋三大暗渠が何かは本記事に明記なし ／ 旧番号: — ／ 直接確認（2026-11-27にblog.jpで本文全文取得）（ai）'
BLOG_LINE_341 = '- [BLOG-341](blogs/BLOG-341.md) — 髙山英男「板橋暗渠番組、公開されました。」（毎日暗活！暗渠ハンター・2018年5月1日）— 『板橋マニア』（フリックスタジオ・2018年4月発売）の売行き好調と板橋区プロモーション番組『魅力発信！板橋ナビ』2018年5月1〜31日配信・「開始後3分以降はなぜか全部暗渠の話題」＝区広報で暗渠が実質主題化した記録（repo初出）・JCOM・板橋区HP・区役所ロビーで視聴可・2017年『ふるカフェ系ハルさんの休日』（BLOG-337）出演との連続 ／ 旧番号: — ／ 直接確認（2026-11-27にblog.jpで本文全文取得）（ai）'


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第353回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第353回:' in readme:
        print('README: 第353回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第352回:')]
        assert len(hits) == 1, 'README anchor 第352回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        idx = f.read()
    if '- [GOV-620]' in idx or '- [BLOG-340]' in idx:
        print('INDEX: 第353回分 already present; skip')
        return
    lines = idx.split('\n')
    g = [i for i, l in enumerate(lines) if l.startswith('- [GOV-619]')]
    assert len(g) == 1, 'INDEX anchor GOV-619 found %d' % len(g)
    lines.insert(g[0] + 1, GOV_LINE)
    b = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-339]')]
    assert len(b) == 1, 'INDEX anchor BLOG-339 found %d' % len(b)
    lines.insert(b[0] + 1, BLOG_LINE_340)
    lines.insert(b[0] + 2, BLOG_LINE_341)
    idx = '\n'.join(lines)
    idx, n1 = re.subn('## 行政・公的機関（617件）', '## 行政・公的機関（618件）', idx)
    idx, n2 = re.subn('## ブログ・個人サイト（338件）', '## ブログ・個人サイト（340件）', idx)
    idx, n3 = re.subn('資料ファイル総数: 1905件', '資料ファイル総数: 1908件', idx)
    assert n1 == 1 and n2 == 1 and n3 == 1, 'count update failed: %d %d %d' % (n1, n2, n3)
    with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
        f.write(idx)
    print('INDEX: GOV-620/BLOG-340/341 inserted, counts updated')


if __name__ == '__main__':
    main()
