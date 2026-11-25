#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第308回: INDEX行挿入(3)+計数更新+README bullet挿入+ヘルパー削除（自己削除型）
Usage: python3 .308-insert.py [base_dir]   (引数なし=repo root)
"""
import os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
TEST = (base != '.')
IDX = os.path.join(base, 'docs/sources/INDEX.md')
RDM = os.path.join(base, 'README.md')
BUL = os.path.join(base, '.308-bullet.txt')

GOV_LINES = [
 "- [GOV-582](gov/GOV-582.md) — 東京都財務局「環状七号線地下河川（仮称）基本検討委託」公告（2026-11-24希望制指名競争入札・希望申請11/27まで・開札12/16）— 神田川・白子川・石神井川・目黒川・呑川の各流域の施設配置・基本構造の検討・施工計画・履行期間2027-12-10まで・参加資格＝土木・水系関係調査業務A等級・関連業務の治水対策検討＝パシフィックコンサルタンツ・基礎調査＝エイト日本技術開発（治水対策検討の受注文言はrepo初出＝GOV-291計画検討委員会から基本検討段階への移行・開札後の受注者確認はGOV-148開札12/02と並ぶ監視点）・同公告の「仙川下流部調節池基礎調査」は世田谷区鎌田の野川支川で千川上水（Senkawa Aqueduct）と同名異川 ／ 旧番号: — ／ 直接確認（建設通信新聞Digital 2026-11-25記事本文・公告一次テキストは未閲覧）（ai）",
 "- [GOV-583](gov/GOV-583.md) — 豊島区プレスリリース「官民学連携シンポジウム『種子屋街道の歴史を今に伝える 種子屋街道に芽吹く地域の未来』を11月28日に開催」（PR TIMES配信2026-11-20）— 種子屋街道（repo初出の街道名＝旧中山道と千川上水に挟まれた巣鴨〜西巣鴨〜滝野川三軒家の種苗商家集積地の通称）の官民学シンポジウム＝報告①横山恵美「江戸・東京の特産物と種子屋」（BOOK-064湧水調査ノートの著者）・第2部＝区指定文化財「榎本家店舗兼住宅および新座敷」（西巣鴨3-19-2）の文化財保存修理事業見学会・プレス本文に水系文言なし（地名・交通史・土地利用系リード） ／ 旧番号: — ／ 直接確認（PR TIMES配信本文・区公式詳細頁は未取得）（ai）",
]

BLOG_LINES = [
 "- [BLOG-313](blogs/BLOG-313.md) — 滝野川探検隊「種屋街道（たねやかいどう）」頁（2021-12-31公開・榎本氏2004年4月作成の三軒家マップの転載・原記事article/000070〔2017-06-10〕と文言一致確認）— 千川上水分配堰の碑（滝野川6-9-2）の説明文「昭和12年（1937）暗渠化されました」＝千川上水の暗渠化年次対校群（BLOG-043滝野川区間「昭和3年」説・BLOG-092上石神井・中村橋「昭和30年代」記憶・GOV-072練馬区「昭和25年頃着手」説・BLOG-312大山「昭和3-4年ころ」）への中流域の年次観測（断定せず）＋「明治15年（1879）」西暦誤記（年号は北区公式1882年建立と一致）＋碑所在地6-9-2（北区公式6-9-1との番地差）＋鎌倉橋の位置「滝野川7丁目と上池袋4丁目間」＋「近年までバス停に名が有りました」＋種苗屋街道の碑（巣鴨3-21-21）・瀧野川人参牛蒡の碑（滝野川6-21-25）の石碑2件（JA東京農協法50周年記念事業・repo初出・水系文言なし）＋導入文「中山道と千川上水に囲まれた土地」（GOV-583の行政側対応）＝加藤家水車・谷端の牧場・板橋駅東口1953年等はREADME既収録のため未再録 ／ 旧番号: — ／ 直接確認（当該頁とarticle/000070本文の両方を2026-11-25に直接取得し文言一致を確認）（ai）",
]

def assert_count(text, needle, n, what):
    c = text.count(needle)
    assert c == n, f"ASSERT FAIL: {what}: count({needle!r})={c}, want {n}"

# ---- INDEX.md ----
idx = open(IDX, encoding='utf-8').read()

assert_count(idx, '## 行政・公的機関（579件）', 1, 'GOV見出し')
idx = idx.replace('## 行政・公的機関（579件）', '## 行政・公的機関（581件）')
assert_count(idx, '## 行政・公的機関（581件）', 1, 'GOV見出し置換後')

assert_count(idx, '## ブログ・個人サイト（311件）', 1, 'BLOG見出し')
idx = idx.replace('## ブログ・個人サイト（311件）', '## ブログ・個人サイト（312件）')
assert_count(idx, '## ブログ・個人サイト（312件）', 1, 'BLOG見出し置換後')

assert_count(idx, '資料ファイル総数: 1784件', 1, '総数行')
idx = idx.replace('資料ファイル総数: 1784件', '資料ファイル総数: 1787件')
assert_count(idx, '資料ファイル総数: 1787件', 1, '総数行置換後')

for tag in ['[GOV-582]', '[GOV-583]', '[BLOG-313]']:
    assert idx.count(tag) == 0, f"ASSERT FAIL: 事前重複 {tag}"

lines = idx.split('\n')
out = []
a_gov = '- [GOV-581](gov/GOV-581.md)'
a_blog = '- [BLOG-312](blogs/BLOG-312.md)'
n_gov = n_blog = 0
for ln in lines:
    out.append(ln)
    if ln.startswith(a_gov):
        out.extend(GOV_LINES); n_gov += 1
    elif ln.startswith(a_blog):
        out.extend(BLOG_LINES); n_blog += 1
assert n_gov == 1, f"ASSERT FAIL: GOV-581アンカー {n_gov}件"
assert n_blog == 1, f"ASSERT FAIL: BLOG-312アンカー {n_blog}件"
idx2 = '\n'.join(out)
for tag in ['[GOV-582]', '[GOV-583]', '[BLOG-313]']:
    assert idx2.count(tag) == 1, f"ASSERT FAIL: 挿入後 {tag}"
open(IDX, 'w', encoding='utf-8').write(idx2)

# ---- README.md ----
rdm = open(RDM, encoding='utf-8').read()
bullet = open(BUL, encoding='utf-8').read().rstrip('\n')
assert bullet.startswith('- **第308回:'), "ASSERT FAIL: bullet先頭"
assert rdm.count('\n- **第307回・続き:') + rdm.startswith('- **第307回・続き:') == 1, "ASSERT FAIL: 第307回・続きアンカー"
assert rdm.count('- **第308回:') == 0, "ASSERT FAIL: 第308回bullet既存"
lines = rdm.split('\n')
out = []
ins = 0
for ln in lines:
    out.append(ln)
    if ln.startswith('- **第307回・続き:'):
        out.append(bullet); ins += 1
assert ins == 1, f"ASSERT FAIL: bullet挿入 {ins}件"
rdm2 = '\n'.join(out)
assert rdm2.count(bullet) == 1
assert rdm2.count('\n- **第308回:') == 1
assert rdm2.count('\n- **第307回・続き:') == 1
open(RDM, 'w', encoding='utf-8').write(rdm2)

# ---- ヘルパー削除（本番のみ） ----
if not TEST:
    for f in ['.308-bullet.txt', '.308-insert.py', '.github/workflows/insert-308.yml']:
        p = os.path.join(base, f)
        if os.path.exists(p):
            os.remove(p)
print('INSERT-308 OK')
