#!/usr/bin/env python3
# 第315回bot用: README.mdの「- **第314回:**」行の直後に .315-bullet.txt の1行を挿入し、
# docs/sources/INDEX.md にGOV-591・592行を挿入して計数を更新し、
# docs/谷端川.md に仁王橋追記段落を「したがって、現在は次のように区別する。」行の直前に挿入する。
# 冪等: READMEに既に「第315回:」の行がある場合は何もしない。
# アンカー不在・計数不整合の場合は非ゼロ終了（失敗を可視化し、クリーンアップは行わない）。
import io, sys

README = 'README.md'
INDEX = 'docs/sources/INDEX.md'
TANIWA = 'docs/谷端川.md'
BULLET = '.315-bullet.txt'

GOV591_LINE = u'- [GOV-591](gov/GOV-591.md) — 東京都公文書館・クロス検索「千川水路」49件の全走査（2026-11-25・第315回・POSTレシピ復旧で取得）— repo未収録44件＝大正3年「千川水路を府費にて暗梁式とし以て中仙道の副道とする」1件〔1186200・1914・板橋町・両郡長＝BLOG-321引用の大正3年3月請願の府側簿冊記録候補・「暗梁」repo grep新出〕・下練馬村千川水路上の練馬停車場新設道路橋設計図〔1207086・1915・武蔵野鉄道・図面〕・明治17年「位置変換」（流路変換）実務群5件〔823058/823135/823420/720646-47・1884・下板橋宿・金井窪村・滝野川村の用地買上→開鑿費納付→堀割及橋梁架設（請負人川島磯五郎）→残金還付〕・明治30年代の水路費予算・決算・官木伐採・雑木枝葉伐採事件〔314371-73/439067/329330・1899-1900・郡長管理期〕・印刷局負担の護岸橋梁修繕費の会計往復群〔403762/403795/387971-72/388006・1888-89〕・水車営業・堰上・修繕群7件〔410326/369139/370642/370626+28/704812/881770・1880-87・岩崎喜之助repo初出〕・悪水吐捨兼用水路新設の検査出張〔704789・1881〕・「潜り下水」改築費回送2件〔369133/369134・1881・repo grep新出〕・水賦金悉皆差出の王子村外22ヶ村諭達依頼〔706240・1882〕・「徳川昭武自費架橋願 15年1月回議録に付て看るへし」参照文言〔424758・1881・徳川昭武repo全grep新出〕・水災録の下板橋宿堤防損所〔482769・1885〕・木製掛樋模様替照会〔999457・1882・図面あり＝999456の先行文書〕 ／ 旧番号: — ／ 目録詳細確認（詳細頁・請求番号・MFコマまで・本文未見）（ai）'
GOV592_LINE = u'- [GOV-592](gov/GOV-592.md) — 東京都公文書館・クロス検索の補遺群「仁王橋・高田村・田柄川・谷頭ほか」（2026-11-25・第315回・POSTレシピで取得）— 仁王橋修補の1880年府側記録〔697907・明治13.2.18・滝野川村堀割小路字御代之台・村民願出→当局（印刷局）費用で修補・「堀割小路」repo grep新出・谷端川.mdに相互参照追記〕・高田村の分水堰欠崩修繕願出〔715959・1883・大沢民五郎〕と用水変換出願〔463074・1885・醍醐惣左衛門等〕・市町村制施行順序取調書の字名調書〔557852・1888-89・池袋村4字＋滝野川村7字（北谷端・南谷端・御代ノ台・平尾・鴻ノ台・東西三軒家）の一次列挙・画像公開あり〕・昭和49年田柄川遊水池対策の都調整会議4件〔1756992/1757093/1757095/1757096・1974.11.16〜29・首脳部会議＋調整会議・企画審議室引継〕・井荻町大字下井草字谷頭を含む第5工区区画整理の国有地無償編入2件〔1084637-38・1932・元道路・水路・土場敷〕 ／ 旧番号: — ／ 目録詳細確認（詳細頁・請求番号・MFコマまで・本文未見）（ai）'

TANIWA_PARA = [
u'また、東京都公文書館の往復録に、1880年（明治13年）2月18日付で北豊島郡滝野川村の堀割小路字御代之台に架設の仁王橋の修補について、村民から願い出たことを受け、当局（印刷局）費用を以て該橋梁を修補した旨の申進が印刷局よりなされた記録が現存する（610.A6.01 往復録甲号・MF府明Ⅱ明13-021・コマ0442-0950）。〔確認・目録文言〕  ',
u'これは上記の東京府志料の仁王橋（千川用水ニ架ス・長8間3尺・幅1間・木造・仁王塚説）に対し、橋の所在を堀割小路字御代之台と特定する情報と、修補費を当局（印刷局）が負担した（＝千川用水の維持費負担体制）ことの新情報を与える府側の一次記録の目録情報である。志料の仁王橋と同一の橋である可能性が高いが、本文未見のため比定の断定は保留する。〔確認／仮説の補強〕  ',
u'出典：[GOV-592](sources/gov/GOV-592.md)',
u'',
]

t = io.open(README, encoding='utf-8').read()
if any(l.startswith(u'- **第315回:') for l in t.split('\n')):
    print('README already has round-315 bullet; skip insertion')
    sys.exit(0)
if not any(l.startswith(u'- **第314回:') for l in t.split('\n')):
    sys.exit('README anchor line "- **第314回:" not found; abort')

idx = io.open(INDEX, encoding='utf-8').read()
def must_one(s, label):
    c = idx.count(s)
    if c != 1:
        sys.exit('INDEX assertion failed for %s (count=%d); abort' % (label, c))
must_one(u'- [GOV-590](gov/GOV-590.md)', 'GOV-590 row')
must_one(u'## 行政・公的機関（588件）', 'gov header 588')
must_one(u'資料ファイル総数: 1807件', 'total 1807')
if u'- [GOV-591](gov/GOV-591.md)' in idx or u'- [GOV-592](gov/GOV-592.md)' in idx:
    sys.exit('INDEX already has GOV-591/592; abort')

lines = idx.split('\n')
out = []
for l in lines:
    out.append(l)
    if l.startswith(u'- [GOV-590](gov/GOV-590.md)'):
        out.append(GOV591_LINE)
        out.append(GOV592_LINE)
idx2 = '\n'.join(out)
idx2 = idx2.replace(u'## 行政・公的機関（588件）', u'## 行政・公的機関（590件）')
idx2 = idx2.replace(u'資料ファイル総数: 1807件', u'資料ファイル総数: 1809件')
io.open(INDEX, 'w', encoding='utf-8', newline='').write(idx2)

tan = io.open(TANIWA, encoding='utf-8').read()
if u'堀割小路' not in tan:
    if tan.count(u'したがって、現在は次のように区別する。') != 1:
        sys.exit('谷端川.md anchor "したがって、現在は次のように区別する。" not unique; abort')
    lines = tan.split('\n')
    for i, l in enumerate(lines):
        if l.startswith(u'したがって、現在は次のように区別する。'):
            lines[i:i] = TANIWA_PARA
            break
    io.open(TANIWA, 'w', encoding='utf-8', newline='').write('\n'.join(lines))

b = io.open(BULLET, encoding='utf-8').read().rstrip('\n').rstrip('\r')
lines = t.split('\n')
for i, l in enumerate(lines):
    if l.startswith(u'- **第314回:'):
        lines.insert(i + 1, b)
        break
io.open(README, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('inserted round-315 bullet after round-314 line + INDEX rows/counts + 谷端川.md 仁王橋 paragraph')
