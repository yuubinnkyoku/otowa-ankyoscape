#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第322回: READMEに実行記録bulletを挿入しINDEXにGAZ-190〜193行を追加するヘルパー。
使い方: python3 .322-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第321回:' 行の直後に .322-bullet.txt の1行を挿入（'- **第322回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: '- [GAZ-189](gazetteers/GAZ-189.md)' 行の直後にGAZ-190/191/192/193行を挿入し、
  地誌・行政史料189→193件・資料ファイル総数1832→1836件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.322-bullet.txt'

GAZ190_LINE = (
    '- [GAZ-190](gazetteers/GAZ-190.md) — 『東京市史稿』市街篇 第十四（東京市役所編纂・昭和9年刊・3450788）'
    '（2026-11-25・第322回・lab全文検索→全文ZIPで取得）'
    '— 御府内沿革書図據ニ拠ル霊岸島川口町「八町堀千川屋鋪」条＝柳澤出羽守殿上ケ屋敷4,612坪の元禄12己卯年（1699）2月3日町屋代地請取文言'
    '（立合い＝松前伊豆守組・保田越前守組与力同心平塚伊右衞門・生田三郎左衞門・鈴木孫左衞門＋町年寄布施半右衞門・奈良屋市右衞門＝いずれもrepo初出）'
    '＋湯島の神田上水86間5尺埋樋文言＝GAZ-122の市街篇側採録（対校点のみ）'
    '＋「千川屋鋪」の語義はOCR列崩壊のため断定しない（江戸川筋の立地）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)

GAZ191_LINE = (
    '- [GAZ-191](gazetteers/GAZ-191.md) — 『東京市史稿』市街篇 第十八（東京市役所編纂・昭和9年刊・3450793）'
    '（2026-11-25・第322回・lab全文検索→全文ZIPで取得）'
    '— 白山前町千川屋鋪の正徳4年2月27日名主六之丞預り・同3月22日千川德兵衞・太兵衞渡しの両証文言'
    '（3月22日の日次・「外ニ下水坪十七坪五合」＝下水付帯用地の坪数・立合人嶋田佐渡守内小倉半内・小林久左衞門組鈴木・高林又兵衞組村井がrepo初出）'
    '＝GAZ-049⑫（書上体）の年代・人名の証文側対校本＋「南伏屋修理」（本冊）vs「南伏屋賴母」（GAZ-053宝永元年証文）の判読対立'
    '＋正徳4年＝甲午の干支対立（GAZ-049⑫の注記）に証文側2票 ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)

GAZ192_LINE = (
    '- [GAZ-192](gazetteers/GAZ-192.md) — 『東京市史稿』市街篇 第二十（東京市役所編纂・昭和9年刊・3450797）'
    '（2026-11-25・第322回・lab全文検索→全文ZIPで取得）'
    '— 「千川上水其他廢止」事蹟章（pp.501-504と読める・上水篇への案内文言つき）＝①柳營日次記「（享保7年8月）十七日庚午」条（差止側の引用はrepo初出）'
    '②石川近江守茂總?被渡御書付「中興〓懸り」判読＝中奥/中興判読対立の第3テキスト'
    '③撰要永久錄の水筋文言「武藏野保田新田〓板橋庚申塚・巢鴨・谷中・上野下谷・淺草筋に相掛り」（水元〜末端給水区の列挙・repo初出・GOV-378と同一資料の享保7年の触）'
    '④三正綜覽拠りの9月3日乙酉千川・青山三田廃止令・9月5日丁亥本所上水廃止（8月触→9月令→10月実施の三層構造候補）'
    '⑤有德院殿御實紀「この十月より千川の上水を引ことをとゞめらる」等の実施文言（repo初出）'
    '⑥國朝舊章錄の火消組合＋千川上水停止の併記条（引用元repo初出） ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・表組崩壊大・文言は要原文照合）（ai）'
)

GAZ193_LINE = (
    '- [GAZ-193](gazetteers/GAZ-193.md) — 『東京市史稿』市街篇 第二十一（東京市役所編纂・昭和9年刊・3450801）'
    '（2026-11-25・第322回・lab全文検索→全文ZIPで取得）'
    '— 神田旅籠町の昌平橋外堀井の渡預繪圖證文＋後日注記「安永九庚子年五月九日 旅籠町之者共（より）請負人加東屋甚五郞に渡ス」'
    '「天明三卯年 千川上水請負人に引渡こ相成い。右錠鍵加東屋甚五郞に相渡、先預り之者不殘消印濟」'
    '＝安永9年5月9日の日次がrepo初出（GOV-441「安永9年5月」と月次整合）＋天明三卯年 vs GOV-441「天明四辰年五月」の年次対立の新witness（対校表記・断定しない）'
    '＋享保11年2月18日の証文側立合人名（吉澤藤七郎・矢部伊右衞門・鈴木伊勢守内＝GAZ-130未収録・repo初出）'
    '＋昌平橋外揚場の土屋小左衞門拝借文言（享保11年2月4日・浅草門跡旧地）＋神田仲町系はGAZ-041重複のため不採録（第317回判定を踏襲）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
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
    assert bullet.startswith('- **第322回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第322回:' in readme:
        print('README: 第322回bullet already present; skip')
    else:
        must_one(readme, '- **第321回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第321回:')]
        assert len(hits) == 1, 'README anchor 第321回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[GAZ-190](gazetteers/GAZ-190.md)' in index:
        print('INDEX: GAZ-190 line already present; skip')
    else:
        must_one(index, '- [GAZ-189](gazetteers/GAZ-189.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [GAZ-189](gazetteers/GAZ-189.md)', [GAZ190_LINE, GAZ191_LINE, GAZ192_LINE, GAZ193_LINE], 'INDEX-GAZ')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 地誌・行政史料（189件）', '@@GAZHEAD@@', 1)
        index = index.replace('@@GAZHEAD@@', '## 地誌・行政史料（193件）', 1)
        index = index.replace('資料ファイル総数: 1832件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1836件', 1)
        must_one(index, '## 地誌・行政史料（193件）')
        must_one(index, '資料ファイル総数: 1836件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 地誌・行政史料（189件）') == 0
        assert index.count('資料ファイル総数: 1832件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GAZ-190〜193 lines inserted; counts updated 189→193・1832→1836')

    print('INSERT-322 OK')


if __name__ == '__main__':
    main()
