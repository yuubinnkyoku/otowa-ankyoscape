#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第318回: READMEに実行記録bulletを挿入しINDEXにGOV-596〜598・GAZ-187/188・BOOK-323/324行を追加するヘルパー。
使い方: python3 .318-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第317回:' 行の直後に .318-bullet.txt の1行を挿入（'- **第318回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md: GOV-595行の直後にGOV-596/597/598行、GAZ-186行の直後にGAZ-187/188行、BOOK-322行の直後にBOOK-323/324行を挿入し、
  行政・公的機関593→596件・地誌・行政史料186→188件・書籍・雑誌・メディア321→323件・資料ファイル総数1816→1823件を更新（各々1箇所であることをmust_oneで確認）。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.318-bullet.txt'

GOV596_LINE = (
    '- [GOV-596](gov/GOV-596.md) — 警察協会 編『徳川時代警察沿革誌』下巻（警察協会・1927・1443710）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 正徳3年8月の千川上水8ヶ所＋神田上水11ヶ所禁制高札採録（小石川御殿掛り溜堀・巣鴨溜堀・同咄水門・同築土手・瀧川一里塚・金井久保橋際・板橋御林橋除・長崎築土手・「以上八ケ處」）'
    '＝GAZ-117（絲綸錄「月日朱書」）に対する別系統の年代観（享保編纂と1927編纂で年代採録が食い違い確定できず・対校課題）'
    '・判読対立の量化（咄/吐水門・掛り/懸り・十一/十ヶ所・橋除/橋際）'
    '・享保7年差止文言「申興より掛り候事故…寅八月十七日安藤對馬守殿御渡」＝GOV-170撰要類集・GAZ-117絲綸錄・GOV-464憲教類典に続く同一御書付の第4テキスト（「申興」は「中興」のOCR崩れ候補）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
)
GOV597_LINE = (
    '- [GOV-597](gov/GOV-597.md) — 大原社会問題研究所 編『日本労働年鑑. 第12輯』（同研究所・1931・1448728）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 東京府議会「昭和五年度乃至八年度府都市計畫事業費(新規事業)五百二十萬九千圓＝立會川、神田上水及谷端川改修」の年度割絶対額'
    '（46万500・184万5300・196万8200・93万5000円・合計検算済み＝GOV-159比率の背後の原数値系列）'
    '・起債方法（利率4分8厘・7年度迄据置・8〜14年度償還・目黒川改修費充当19万3千円・品川海面埋立6万9千円）'
    '・昭和5年度巣鴨町下水工事の失業救済統計（労力費14万7606円・延人員8万645人・日平均220人）'
    '＝谷端川流域の巣鴨町で下水工事が失業救済事業として実施された1930年時点の年鑑記録'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・数値の一部にOCR崩れ・要原文照合）（ai）'
)
GOV598_LINE = (
    '- [GOV-598](gov/GOV-598.md) — 大阪毎日新聞社 編『日本都市大観』昭和11年版・15年版（同社・1936/1941・1207937・1207969）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 11年版「河川ハ立合川、神田上水、谷端川…豫算一億九千七十五万円デ改修」＝1936年時点の府の河川改修群里の確認'
    '・15年版の河川別予算「谷端川七百七十七万八千円・神田上水四百十三万六百廿円・立會川百四十六万円…」'
    '＝谷端川単独777万8千円の新聞社年鑑数値（GOV-161約49万円・GOV-159 trio520万9千円との約16倍乖離＝誤栽・混同・後年積み直しのいずれも確定できず対校課題として登録・断定材料にしない）'
    '・同列挙内で神田上水・立会川が1.06〜1.14倍の増額で整合するのに対し谷端川だけ桁違い＝列挙内部の不自然さの観察'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・新聞社年鑑OCR数値・要原文照合）（ai）'
)
GAZ187_LINE = (
    '- [GAZ-187](gazetteers/GAZ-187.md) — 太田為三郎 編『帝国地名辞典』下巻（三省堂・1912・762293）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 千川上水条（見出し語独立条）: 「北足立郡保谷村にて玉川上水を分ち…巣鴨村庚申塚に至る水路五里六町。是より埋樋…元祿九年起工、享保七年廢し…明和六年復舊…天明六年廢す。明治十三年更に修理を加へ…給水を受くるもの約二萬人なりし…東京市水道成るに及び廢す」'
    '＝明和6年復旧の年号つき辞典側要約（御府内備考系の過程解釈には影響せず）'
    '・「北足立郡保谷村」は同書東京市条の「北多摩郡」と矛盾＝誤記候補（GOV-228「埼玉縣新座郡」と同型の誤変形・repo初出変種）'
    '・五里六町・庚申塚の並行文言（GOV-228・GAZ-048・GAZ-051と整合）'
    '・明治13年修理後の給水約2万人・本〓区＝GOV-228の「1.7万余」との対立候補（区域・人口の両面で対校課題）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・「本〓」欠字の原本照合必須）（ai）'
)
GAZ188_LINE = (
    '- [GAZ-188](gazetteers/GAZ-188.md) — 阿部秀助 著『日本地理講義』下巻（金刺芳流堂・1910・762731）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 小石川区条: 「吉田東伍氏の說に元巢鴨村より出つる野水谷端川の末なりしが、今は千川上水の剩水を容れ、小日向臺と白山臺との間を流れ、富坂下より砲兵工廠に入り…神田川へ注ぐ、昔は之も駿河臺の西にて小川と相會せしならん」'
    '＝東伍説の地理教科書への明示帰属引用（1910年時点で「東伍説」として流通の証明・1907地名辞書→1907藤岡辞典→1910本書→1914下水道沿革誌の系譜）'
    '・本書だけの文言「駿河臺の西にて小川と相會せしならん」＝旧流路の駿河台西・小川合流の推定（仮説文言として保存）'
    '・対校として藤岡継平『日本歴史地理辞典』（1907・771424）小石川条の無帰属並行文言（「小石川の名これより起る」）を同一ファイル内併録'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・組版崩壊部の再構成〔〕明示・要原文照合）（ai）'
)
BOOK323_LINE = (
    '- [BOOK-323](books/BOOK-323.md) — 塚本哲三 等編『有朋堂文庫〔第95〕』（有朋堂書店・1915・1913680）所収の活字版『江戸名所花暦』春之部・桜の条＋吉川弘文館活字版（1911・763659）'
    '（2026-11-25・第318回・lab全文検索で取得・活字版2系統対校）'
    '— 「西久保關前、是に千川上水堀割の樋の口あり、今は絕て埋れり、此邊總て尾州侯の御鷹場なり、關前新田、保谷新田」'
    '＝樋口文言の原典側確定（2系統とも「堀割」で一致・吉川版ルビ「ほりわり」付き＝BOOK-137「六百年割」判読問題を解消）'
    '・観察時期を花暦成立期（文政10年頃〜江戸後期）に前倒し（『武蔵野』の当該文言は花暦の明示的引用ブロック内）'
    '・樋口位置の基準点（井頭弁財天道分岐→七丁→西久保関前）・看櫻順路の全形（四谷→中野→吉祥寺村→…→小金井橋）'
    '・尾州侯御鷹場と関前新田・保谷新田の併記（康楽園・GOV-251系と対照可能）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・活字版2系統対校・版本原字との照合を要する）（ai）'
)
BOOK324_LINE = (
    '- [BOOK-324](books/BOOK-324.md) — 東京高等師範学校附属小学校 編『小学校教授細目』（大日本図書・1912・938109）'
    '（2026-11-25・第318回・lab全文検索で取得）'
    '— 尋六算術の応用問題構成資料（明治41年末日調）「谷端川水源より祇園橋まで二里十八町(流程)」'
    '＝corpus 0件のrepo初出の流程値候補（2里18町≒9.8km・教材用概数として扱い測量値としない・「谷端川水源」の比定は未了）'
    '・地理科・尋三の実地観察教案「千川流域」（観察項目「谷・小川、同利用（排水、水車）畑・原野・流域、森林と雨水の保蓄、諸工場」＝1910年代の初等教育で千川が水利用・流域の教材だった一次教案）'
    '・占春園附近地図・護国寺附近観察との単元連結・郷土科観察一覧「千川筋」の文言候補（表崩壊）'
    ' ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・表組崩壊部あり・要原文照合）（ai）'
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
    assert bullet.startswith('- **第318回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第318回:' in readme:
        print('README: 第318回bullet already present; skip')
    else:
        must_one(readme, '- **第317回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第317回:')]
        assert len(hits) == 1, 'README anchor 第317回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if '[GOV-596](gov/GOV-596.md)' in index:
        print('INDEX: GOV-596 line already present; skip')
    else:
        must_one(index, '- [GOV-595](gov/GOV-595.md)')
        must_one(index, '- [GAZ-186](gazetteers/GAZ-186.md)')
        must_one(index, '- [BOOK-322](books/BOOK-322.md)')
        lines = index.split('\n')
        lines = insert_after(lines, '- [GOV-595](gov/GOV-595.md)', [GOV596_LINE, GOV597_LINE, GOV598_LINE], 'INDEX')
        lines = insert_after(lines, '- [GAZ-186](gazetteers/GAZ-186.md)', [GAZ187_LINE, GAZ188_LINE], 'INDEX')
        lines = insert_after(lines, '- [BOOK-322](books/BOOK-322.md)', [BOOK323_LINE, BOOK324_LINE], 'INDEX')
        index = '\n'.join(lines)
        # 計数更新（各箇所とも1箇所であることを確認して置換）
        index = index.replace('## 行政・公的機関（593件）', '@@GOVHEAD@@', 1)
        index = index.replace('@@GOVHEAD@@', '## 行政・公的機関（596件）', 1)
        index = index.replace('## 地誌・行政史料（186件）', '@@GAZHEAD@@', 1)
        index = index.replace('@@GAZHEAD@@', '## 地誌・行政史料（188件）', 1)
        index = index.replace('## 書籍・雑誌・メディア（321件）', '@@BOOKHEAD@@', 1)
        index = index.replace('@@BOOKHEAD@@', '## 書籍・雑誌・メディア（323件）', 1)
        index = index.replace('資料ファイル総数: 1816件', '@@TOTAL@@', 1)
        index = index.replace('@@TOTAL@@', '資料ファイル総数: 1823件', 1)
        must_one(index, '## 行政・公的機関（596件）')
        must_one(index, '## 地誌・行政史料（188件）')
        must_one(index, '## 書籍・雑誌・メディア（323件）')
        must_one(index, '資料ファイル総数: 1823件')
        # 旧計数の完全文字列が残っていないこと
        assert index.count('## 行政・公的機関（593件）') == 0
        assert index.count('## 地誌・行政史料（186件）') == 0
        assert index.count('## 書籍・雑誌・メディア（321件）') == 0
        assert index.count('資料ファイル総数: 1816件') == 0
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: GOV-596/597/598 / GAZ-187/188 / BOOK-323/324 lines inserted; counts updated 593→596・186→188・321→323・1816→1823')

    print('INSERT-318 OK')


if __name__ == '__main__':
    main()
