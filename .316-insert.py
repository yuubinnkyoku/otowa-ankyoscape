#!/usr/bin/env python3
# 第316回bot用: README.mdの「- **第315回:**」行の直後に .316-bullet.txt の1行を挿入し、
# docs/sources/INDEX.md にGOV-593/594・BOOK-319/320行を挿入して計数を更新する。
# 冪等: READMEに既に「第316回:」の行がある場合は何もしない。
# アンカー不在・計数不整合の場合は非ゼロ終了（失敗を可視化し、クリーンアップは行わない）。
import io, sys

README = 'README.md'
INDEX = 'docs/sources/INDEX.md'
BULLET = '.316-bullet.txt'

GOV593_LINE = u'- [GOV-593](gov/GOV-593.md) — 東京市『東京市下水道事業年報』第12回（1932刊・1077024）・第13回（1935刊・1077034）・第14回（1935刊・1077040）（2026-11-25・第316回・lab全文検索で取得）— 昭和3年決定の追加速成事業としての千川改修＝工費五百七十四萬六百九十五圓・「昭和七年度迄ニ完成」文言と第14回の「二年度の繰延べ…來年度を以て之を完成」進捗文言・第14回のみ完全形の経由町名列「小石川區氷川下町、白山御殿町、久堅町、戶崎町、八千代町、柳町、初音町、餌差町、下富坂町等ヲ經テ陸軍東京工廠構内ヲ貫通シ神田川ニ流入スル千川筋」〔repo初出・昭和5年度以降の千川筋暗渠化の経由地の旧町名列挙〕・第13回図録写真「千川改修工事 砲兵工廠下及吐口ヲ望ム」のキャプション記録〔1931-33年時点の千川末端の写真記録候補・画像実体は未確認〕・総説の神田・玉川・千川3上水併記文言（GOV-166第15/16回の先行巻） ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
GOV594_LINE = u'- [GOV-594](gov/GOV-594.md) — 東京市区改正委員会『東京市区改正委員会議事録 第3巻』（1900・784703）（2026-11-25・第316回・lab全文検索で取得）— 水道規則審議中の発言「且千川上水ノ如キ水路ハ買上クルコトニ爲シタシ」（二十四番佐藤）＝明治20年代後半の公的審議の場での千川上水買上げ構想の言語記録・「松田知事在職ノ當時千川上水會社ヲ許可シタルコトアレハ今之ヲ止ムルコトハ出來マシ併シ其水ヲ引クコトハ難カラ」（十九番銀林）＝千川上水會社許可の回想〔「松田知事」の同定は留保〕・「神奈川縣管內ニ屬スル分」＝1893年多摩三郡移管前の管轄前提文言（GOV-324第2巻の同シリーズ次巻・784704〜784711も同書誌で公開済み） ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合）（ai）'
BOOK319_LINE = u'- [BOOK-319](books/BOOK-319.md) — 東京帝国大学 編『東京帝国大学理学部附属植物園案内』（東京帝国大学・1923・961316）（2026-11-25・第316回・lab全文検索で取得）— 「池ヲ隔テタル高地ノ中腹ニハ、白山御殿ノ大瀑ノ在リシ跡アリ。當時、千川上水ノ水ヲ引キテ瀧ヲ落シタリト云フ」＝大瀑跡への千川上水引水の伝聞文言（「ト云フ」付き・「大瀑」repo grep初出）・船繫松（明治32年まで存続・枯死）・網干坂（氷川神社との境の坂路の旧称）＝大瀑跡特定の基準となる1923年時点の園内ランドマーク記録（BOOK-320の総堀引水と合わせ白山御殿の外部堀給水＋園内滝落水を千川系統とする説明が昭和初期ガイド類で揃った〔伝聞・二次資料のため幕府期文書での確証とは区別〕） ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合・「ト云フ」は伝聞文言として明記）（ai）'
BOOK320_LINE = u'- [BOOK-320](books/BOOK-320.md) — 一高史談会 編『大東京史蹟案内』（育英書院・1932・1190953）（2026-11-25・第316回・lab全文検索で取得）— 白山御殿条「承應元年(1652)…周圍の總堀へは千川の水を引いて」＋「正德三年(1713)この館を廢し、御藥園及旗下士の宅地とした」＝総堀引水源を千川とする叙述＋御薬園転用の廃クロニクル・独立の千川上水条「保谷村上保谷新田から分れ…五里五十五町餘…元祿九年(1696)に引いた…享保七年(1723)十月に一度この上水を中止し…安永九年(1780)に再興し…天明六年(1766)再び中止し」＝沿革定型の1932年時点の編纂記録〔享保七年=1722・天明六年=1786との西暦併記の不一致は原書表記のまま記録〕・石神井城址条末尾「氷川神社前の道を南方へ進み、西武電車を越えるとまもなく舊千川上水のほとりに出る」＝1932年時点の豊島園周辺で旧千川上水路が散策ランドマークとして観察されていた記録〔通水終了1971の約40年前の水路の見え方の資料候補〕 ／ 旧番号: — ／ OCR全文確認（次世代デジタルライブラリー・文言は要原文照合・年次不一致は原書表記のまま記録）（ai）'

t = io.open(README, encoding='utf-8').read()
if any(l.startswith(u'- **第316回:') for l in t.split('\n')):
    print('README already has round-316 bullet; skip insertion')
    sys.exit(0)
if not any(l.startswith(u'- **第315回:') for l in t.split('\n')):
    sys.exit('README anchor line "- **第315回:" not found; abort')

idx = io.open(INDEX, encoding='utf-8').read()
def must_one(s, label):
    c = idx.count(s)
    if c != 1:
        sys.exit('INDEX assertion failed for %s (count=%d); abort' % (label, c))
must_one(u'- [GOV-592](gov/GOV-592.md)', 'GOV-592 row')
must_one(u'- [BOOK-318](books/BOOK-318.md)', 'BOOK-318 row')
must_one(u'## 行政・公的機関（590件）', 'gov header 590')
must_one(u'## 書籍・雑誌・メディア（317件）', 'book header 317')
must_one(u'資料ファイル総数: 1809件', 'total 1809')
for row in (u'- [GOV-593](gov/GOV-593.md)', u'- [GOV-594](gov/GOV-594.md)', u'- [BOOK-319](books/BOOK-319.md)', u'- [BOOK-320](books/BOOK-320.md)'):
    if row in idx:
        sys.exit('INDEX already has %s; abort' % row)

lines = idx.split('\n')
out = []
for l in lines:
    out.append(l)
    if l.startswith(u'- [GOV-592](gov/GOV-592.md)'):
        out.append(GOV593_LINE)
        out.append(GOV594_LINE)
    elif l.startswith(u'- [BOOK-318](books/BOOK-318.md)'):
        out.append(BOOK319_LINE)
        out.append(BOOK320_LINE)
idx2 = '\n'.join(out)
idx2 = idx2.replace(u'## 行政・公的機関（590件）', u'## 行政・公的機関（592件）')
idx2 = idx2.replace(u'## 書籍・雑誌・メディア（317件）', u'## 書籍・雑誌・メディア（319件）')
idx2 = idx2.replace(u'資料ファイル総数: 1809件', u'資料ファイル総数: 1813件')
io.open(INDEX, 'w', encoding='utf-8', newline='').write(idx2)

b = io.open(BULLET, encoding='utf-8').read().rstrip('\n').rstrip('\r')
lines = t.split('\n')
for i, l in enumerate(lines):
    if l.startswith(u'- **第315回:'):
        lines.insert(i + 1, b)
        break
io.open(README, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('inserted round-316 bullet after round-315 line + INDEX rows GOV-593/594 & BOOK-319/320 + counts 590->592/317->319/1809->1813')
