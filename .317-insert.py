#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第317回: READMEに実行記録bulletを挿入しINDEXにGOV-595・BOOK-321/322行を追加するヘルパー。
使い方: python3 .317-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第316回:' 行の直後に .317-bullet.txt の1行を挿入（'- **第317回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: GOV-594行の直後にGOV-595行、BOOK-320行の直後にBOOK-321/322行を挿入し、
  行政・公的機関592→593件・書籍・雑誌・メディア319→321件・資料ファイル総数1813→1816件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.317-bullet.txt'

GOV595_LINE = (
    '- [GOV-595](gov/GOV-595.md) — 国立公文書館『公文雑纂 昭和九年 第四十四巻 都市計画七』「東京都市計画河川改修中変更ノ件」'
    '（1934-08-21・内閣・紙・CC0・纂02116100-01300）'
    '（2026-11-25・第317回・jpsearch谷端川+1差分の実体特定で取得）'
    '— 理由書「立会川、神田上水、谷端川の３河川改修事業は既定計画に基き工事施行中の処…其の後工事実施の都合上其の延長、幅員、深度に於て些少の変更の必要を生するに至り…」'
    '＝1934年8月時点で谷端川改修が施行中であることを伝える内閣側公文雑纂レベルの一次記録'
    '（事業決定1930.8.8〔GOV-159〕→変更要綱1934-08〔GOV-228〕・府告示系1934-08-21〔GOV-160〕の背後の内閣提出文書の存在が確定・着手昭和5年竣工昭和9年の年幅の中央省庁側中間点〔BLOG-077・GOV-581受益者負担と初めて連結する内閣側独立系統〕）'
    '・変更3要素＝延長・幅員・深度の文言（変更前後値の数値対照は課題）'
    '・3河川一組の中央手続グルーピング傍証・神田上水は変更対象外＝谷端川と神田上水の改修ステージ差の候補（特定はしない）'
    ' ／ 旧番号: — ／ メタデータ・理由書本文確認（国立公文書館デジタルアーカイブ・原本画像照合は未・文言は要照合）（ai）'
)
BOOK321_LINE = (
    '- [BOOK-321](books/BOOK-321.md) — 小野高尚 編『三才雑録 二十六』（越智真澄写・文政7〔1824〕書写・写本・11038556）'
    '（2026-11-25・第317回・lab全文検索で取得・repo初の三才雑録収録）'
    '— 享保七壬寅（1722）の年表条「八月十九日 千川上水 上」'
    '＝GAZ-083（享保7年8月19日御書付）・GOV-464（憲教類典58・8月18/19日差止触）と日付一致の覚書側文言候補（幕府側年中記録の体裁・差止関連の第3の独立系統）'
    '〔「上」の語義は本条単独では特定できず・縦書き2行混線で後字に属する可能性も排除できず原画像照合必須・事象内容は断定しない〕'
    '・干支連鎖（辛丑→壬寅→癸卯→甲辰）で年次帰属はOCRレベルで一致'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合・条の帰属正式名は未確定）（ai）'
)
BOOK322_LINE = (
    '- [BOOK-322](books/BOOK-322.md) — 竜居松之助 著『日本庭園史話』（大東出版社・1943・bibId 000000682340・1067114）'
    '（2026-11-25・第317回・lab全文検索で取得）'
    '— 「當時造られた『柳澤侯六義園全圖』によつて見るに…その東端に近い藩主の別莊六義館の前には水量豊富な千川上水の水を注ぐ大泉水を湛へ」'
    '＝江戸期六義園全図に依拠した大池への千川上水注水の庭園史側叙述'
    '（全図自体がrepo未収録の図資料で所在情報として新規・注記レベルの確認が文言の原点特定課題）'
    '〔「水量豊富」が全図の描写か1943年現勢かは判別不能＝断定しない・通水終了1907〔GOV-327〕との整合は文言の性格次第で両説可能〕'
    '＝千川×六義園観察系が伝承（BOOK-151⑦・BOOK-202第317回追記）→1931（GOV-329）→1943（本条）で通時的に4点'
    '・「千川」出現は六義園条1箇所・谷端・弦巻・水窪は0件'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合・全図依拠の叙述であることを明記）（ai）'
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
    assert bullet.startswith('- **第317回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第317回:' in readme:
        print('README: 第317回bullet already present; skip')
    else:
        must_one(readme, '- **第316回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第316回:')]
        assert len(hits) == 1, 'README anchor 第316回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[GOV-595](gov/GOV-595.md)' in index:
        print('INDEX: GOV-595 line already present; skip')
    else:
        must_one(index, '- [GOV-594](gov/GOV-594.md)')
        must_one(index, '- [BOOK-320](books/BOOK-320.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [GOV-594](gov/GOV-594.md)', [GOV595_LINE], 'INDEX')
        lines = insert_after(lines, '- [BOOK-320](books/BOOK-320.md)', [BOOK321_LINE, BOOK322_LINE], 'INDEX')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 行政・公的機関（592件）', '@@GOVHEAD@@', 1)
        index = index.replace('@@GOVHEAD@@', '## 行政・公的機関（593件）', 1)
        index = index.replace('## 書籍・雑誌・メディア（319件）', '@@BOOKHEAD@@', 1)
        index = index.replace('@@BOOKHEAD@@', '## 書籍・雑誌・メディア（321件）', 1)
        index = index.replace('資料ファイル総数: 1813件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1816件', 1)
        must_one(index, '## 行政・公的機関（593件）')
        must_one(index, '## 書籍・雑誌・メディア（321件）')
        must_one(index, '資料ファイル総数: 1816件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 行政・公的機関（592件）') == 0
        assert index.count('## 書籍・雑誌・メディア（319件）') == 0
        assert index.count('資料ファイル総数: 1813件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-595 / BOOK-321 / BOOK-322 lines inserted; counts updated 592→593・319→321・1813→1816')

    print('INSERT-317 OK')


if __name__ == '__main__':
    main()
