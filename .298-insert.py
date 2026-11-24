import io, sys

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_book296 = '- [BOOK-296](books/BOOK-296.md) '
a_pap108 = '- [PAP-108](papers/PAP-108.md) '
assert idx.count(a_book296) == 1, 'BOOK-296 anchor count error'
assert idx.count(a_pap108) == 1, 'PAP-108 anchor count error'
assert '[BOOK-297](books/BOOK-297.md)' not in idx, 'BOOK-297 already present'
assert '[PAP-109](papers/PAP-109.md)' not in idx, 'PAP-109 already present'
assert '[PAP-110](papers/PAP-110.md)' not in idx, 'PAP-110 already present'
assert '[PAP-111](papers/PAP-111.md)' not in idx, 'PAP-111 already present'

book_line = '- [BOOK-297](books/BOOK-297.md) — 東京府北豊島郡中新井村『市郡合併紀念 中新井村誌』（内田喜太郎編・1933・非売品・NDL書誌ID 000000766073）— 千川上水の組合・分水村（上新街・下新街・北新井の3樋口）たる中新井村が1932年東京市郡合併直後に遺した公式村誌（国立国会図書館・東京都立中央図書館所蔵） ／ 旧番号: — ／ 所在のみ（NDL Search dcndl書誌5レコードと所蔵OPACを書誌レベルで直接確認・2026-11-24・本文は未閲覧）（ai）'
pap109 = '- [PAP-109](papers/PAP-109.md) — 谷川章雄ほか『東京都文京区 柳沢家駒込屋敷（六義館・六義園）跡 第4地点』（文京区教育委員会・2020-12-25刊・B-178・NCID BC05265190・NDL〔JP〕23507540・全国遺跡報告総覧91748）— 給水源が千川上水と考えられる上水跡5（下部構造を伴い幅約7mの鉤手状堀を掛け渡し木樋で大泉水へ給水・同軸延伸が水分石に到達・『六義園の図』と一致）と六義園初確認の外郭区画遺構（Ⅰa期=17世紀末葉〜18世紀後葉・7期変遷・『宴遊日記』照合）＝千川上水→六義園給水経路の給水末端を発掘遺構で実証したrepo初の一次記録（本駒込6-16-10・2019.9.30-12.4・240㎡） ／ 旧番号: — ／ 所在のみ（総覧レコードの遺構欄・要約本文を直接確認・2026-11-24・報告書本文は総覧にPDF登載なし）（ai）'
pap110 = '- [PAP-110](papers/PAP-110.md) — 高阪宏行「デジタル微細地誌の一つの試論 -- 東京都豊島区大塚を事例として」（日本大学文理学部情報科学研究所『年次研究報告書』2009・NAID 40017072768）— PAP-108に先行する大塚デジタル微細地誌シリーズの起点論文 ／ 旧番号: — ／ 所在のみ（CiNii Research書誌を直接確認・2026-11-24・本文は未取得）（ai）'
pap111 = '- [PAP-111](papers/PAP-111.md) — 高阪宏行「WebGIS上での微細地誌に関する動画配信 : 東京都豊島区大塚を事例として」（同誌2014・NAID 40020384325）— PAP-108の発表抄録と同題の年次研究報告書掲載版＝紀要詳細版の存在が書誌的に確定 ／ 旧番号: — ／ 所在のみ（CiNii Research書誌を直接確認・2026-11-24・本文は未取得）（ai）'

i = idx.index(a_book296)
end = idx.index('\n', i) + 1
idx = idx[:end] + book_line + '\n' + idx[end:]

i = idx.index(a_pap108)
end = idx.index('\n', i) + 1
idx = idx[:end] + pap109 + '\n' + pap110 + '\n' + pap111 + '\n' + idx[end:]

old = '## 書籍・雑誌・メディア（295件）'
assert idx.count(old) == 1, 'book section header count error'
idx = idx.replace(old, '## 書籍・雑誌・メディア（296件）')
old = '## 論文・研究報告・データ（106件）'
assert idx.count(old) == 1, 'papers section header count error'
idx = idx.replace(old, '## 論文・研究報告・データ（109件）')
old = '資料ファイル総数: 1729件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1733件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.298-bullet.txt', encoding='utf-8').read()
if not bullet.endswith('\n'):
    bullet += '\n'
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第297回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
