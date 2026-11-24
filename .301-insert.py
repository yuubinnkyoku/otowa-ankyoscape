import io, sys

# ---------- docs/sources/INDEX.md ----------
idx = open('docs/sources/INDEX.md', encoding='utf-8').read()
a_pap114 = '- [PAP-114](papers/PAP-114.md) '
assert idx.count(a_pap114) == 1, 'PAP-114 anchor count error'
assert '[PAP-115]' not in idx, 'PAP-115 already present'

pap_rows = [
'- [PAP-115](papers/PAP-115.md) — 橋口定志「鎌倉街道中道と江戸氏・松原氏」（豊島区立郷土資料館研究紀要『生活と文化』第24号・2015年3月27日発行）— 目録確認の中世系論文＝江戸氏・松原氏と鎌倉街道中道の主題が谷端川鎌倉橋＝古道鎌倉街道の文脈（GOV-128矢島勝昭の鎌倉街道志向）に接続する資料候補 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページをWaybackスナップショット〔20261025085057〕で直接確認・2026-11-24・掲載頁・本文は未閲覧）（ai）',
'- [PAP-116](papers/PAP-116.md) — 髙木謙一「【資料紹介】『高田地区関連文書類』の概要について」（『生活と文化』第26号・2017年3月21日発行）— 弦巻川・水窪川上流域の高田地区の文書類の資料紹介＝同筆者の第23号「高田」地域土地利用論（明治42年地租名寄帳分析）の系譜〔観察〕 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
'- [PAP-117](papers/PAP-117.md) — 山本昂伯「東京癈兵院での生活」（『生活と文化』第27号・2018年3月20日発行）— 西巣鴨の東京癈兵院（現巣鴨公園一帯＝谷端川北方台地）の生活史＝PAP-108微細地誌事例②・BOOK-109乞食橋文言（廃兵院の西）・GOV-161池袋駅前広場の丘陵ランドマーク列挙に接続 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
'- [PAP-118](papers/PAP-118.md) — 及川将基「開港初期における外国人の遊歩と江戸北郊地域」（『生活と文化』第29号・2020年3月18日発行）— 江戸北郊遊歩記ジャンルの研究＝弦巻川・水窪川の谷頭（音羽・目白方面）への言及可能性は本文未見のため断定せず ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
'- [PAP-119](papers/PAP-119.md) — 井坂綾・岩﨑茜「戦前戦中期の目白・南長崎の暮らし─玉蟲和子氏聞き取り調査報告─」（『生活と文化』第29号・2020年3月18日発行）— 目白＝弦巻川（丸池系）・水窪川（諏訪山系）の谷頭、南長崎＝千川上水の南側という生活史の聞き取り調査報告＝弦巻川の暗渠化・転換期を含む年代の生活記録候補 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
'- [PAP-120](papers/PAP-120.md) — 高田萌恵「太田道灌が結ぶ妙義神社」（『生活と文化』第30号・2021年3月20日発行）— 高田地区（弦巻川・水窪川上流域）の妙義神社と太田道灌の伝承 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
'- [PAP-121](papers/PAP-121.md) — 及川将基「天保10年徳川家祥の江戸北郊訪問─『春のみかり』『雑司ヶ谷御供の記』（東京大学史料編纂所所蔵史談会本「天保日録」所収）」（『生活と文化』第33号・2024年3月22日発行）— 天保10年＝1839年・雑司ヶ谷・目白方面（弦巻川・水窪川の谷頭地帯）の訪問記研究＝PAP-054で同号収録として名前のみ既出→単独登録・原本所在（東大史料編纂所）が書誌注記で確定 ／ 旧番号: — ／ 所在のみ（区刊行物目録ページ〔Wayback〕で直接確認・2026-11-24・本文は未閲覧）（ai）',
]

i = idx.index(a_pap114)
end = idx.index('\n', i) + 1
idx = idx[:end] + '\n'.join(pap_rows) + '\n' + idx[end:]

a_book297 = '- [BOOK-297](books/BOOK-297.md) '
assert idx.count(a_book297) == 1, 'BOOK-297 anchor count error'
assert '[BOOK-298](books/BOOK-298.md)' not in idx, 'BOOK-298 already present'
book298 = '- [BOOK-298](books/BOOK-298.md) — 『東京府北豊島郡志村大観』（志村尋常高等小学校編・志村役場・1916・143p・19cm・資料コード1124273760・請求記号T/44・20/14/）— TOKYOアーカイブで画像公開中（パブリックドメイン・tilcod=0000000009-00005237）＝千川上水終点部・板橋台地の旧志村村の村誌で『北豊島郡誌』（GAZ-002・1918）に先行・中新井村誌（BOOK-297）と並ぶ北豊島郡村誌の類型 ／ 旧番号: — ／ 所在のみ（TOKYOアーカイブ詳細頁を直接確認・2026-11-24・本文判読はhuman目視待ち）（ai）'
i = idx.index(a_book297)
end = idx.index('\n', i) + 1
idx = idx[:end] + book298 + '\n' + idx[end:]

a_blog311 = '- [BLOG-311](blogs/BLOG-311.md) '
assert idx.count(a_blog311) == 1, 'BLOG-311 anchor count error'
assert '[BLOG-312](blogs/BLOG-312.md)' not in idx, 'BLOG-312 already present'
blog312 = '- [BLOG-312](blogs/BLOG-312.md) — kotakemol04（越後屋たぬき）「現在千川上水暗渠部に水は流れていません」（2015-08-23・FC2直接取得）— 平成26年11月13日都議会環境・建設委員会（河野〔ゆうき〕板橋区選出都議×中島河川部長）問答の全文引用＝伊勢橋から下流約15kmを都が使用許可・維持管理・平成17年度から老朽化調査開始→損傷・土砂堆積判明→平成22年に通水停止（年次のrepo初出文言）・平成18年に開渠区間約5km（武蔵野市〜練馬区）を地方分権一括法で地元区市へ財産譲与・板橋区大山のヒューム管埋設（昭和3-4年ころ暗渠化＝河野委員の発言ベース）・大山入口まで約3,000立米/日流下→板橋区役所〜JR板橋間で渇水（河野委員の照会による数値伝達）・暗渠部管理系入札群（補修2件・基本調査委託・埋設物台帳作成測量〔千川上水全区間〕・善福寺川導水路調査委託〔導水管内径600mm〕）・石神井川放流口看板の「通水停止中」文言（2015年8月撮影）＝BLOG-129（令和2年回答「現在停止」）の先行記事・通水・管理系譜のmermaid図つき ／ 旧番号: — ／ 直接確認（FC2本文を直接取得・2026-11-24・議事録原文はgikai.metro.tokyo.lg.jp 403で未確認）（ai）'
i = idx.index(a_blog311)
end = idx.index('\n', i) + 1
idx = idx[:end] + blog312 + '\n' + idx[end:]

old = '## 論文・研究報告・データ（112件）'
assert idx.count(old) == 1, 'papers section header count error'
idx = idx.replace(old, '## 論文・研究報告・データ（119件）')
old = '## 書籍・雑誌・メディア（296件）'
assert idx.count(old) == 1, 'books section header count error'
idx = idx.replace(old, '## 書籍・雑誌・メディア（297件）')
old = '## ブログ・個人サイト（310件）'
assert idx.count(old) == 1, 'blogs section header count error'
idx = idx.replace(old, '## ブログ・個人サイト（311件）')
old = '資料ファイル総数: 1736件'
assert idx.count(old) == 1, 'total count error'
idx = idx.replace(old, '資料ファイル総数: 1745件')
open('docs/sources/INDEX.md', 'w', encoding='utf-8').write(idx)
print('INDEX updated')

# ---------- README.md ----------
bullet = open('.301-bullet.txt', encoding='utf-8').read()
if not bullet.endswith('\n'):
    bullet += '\n'
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第300回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
