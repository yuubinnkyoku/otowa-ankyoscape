#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第327回: READMEに実行記録bulletを挿入しINDEXにGOV-603・BOOK-330行を追加するヘルパー。
使い方: python3 .327-insert.py [base_dir]  （既定 base_dir='.'・テスト時はbaseコピーのディレクトリを渡す）
- README.md: '- **第326回:' 行の直後に .327-bullet.txt の1行を挿入（'- **第327回:' 行が既にあればスキップ・アンカーが一意でなければabort）。
- docs/sources/INDEX.md:
  * '- [GOV-602](gov/GOV-602.md)' 行の直後にGOV-603行を挿入し「## 行政・公的機関（600件）」→601件を更新。
  * '- [BOOK-329](books/BOOK-329.md)' 行の直後にBOOK-330行を挿入し「## 書籍・雑誌・メディア（328件）」→329件を更新。
  * 「資料ファイル総数: 1841件」→1843件を更新（当該行は「/ 旧番号対応」に続くため部分一致で置換）。
  （各カウント・アンカーはともに1箇所であることをmust_oneで確認）
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
BULLET = '.327-bullet.txt'

GOV603_LINE = (
    '- [GOV-603](gov/GOV-603.md) — ADEAC港区「テキスト一覧」（港区・postback式16テキスト）（2026-11-25・第327回・text-list採取+全本文テキストHTML掃引）'
    '— 16テキストのctl↔d番号↔mp番号↔ht数の完全マッピング（港区史第1〜8巻=mp100010系・自然編=mp100110・図説港区の歴史=mp100120・'
    '芝区誌/新修港区史/港区史上/下/赤坂区史/麻布区史=mp000010系・mp番号はテキスト毎に異なり一覧経由が実質必須）'
    '＋全16テキスト本文掃引で「千川」「弦巻」「水窪」「谷端」「音羽」（ひらがな・旧字体含む）0件の陰性確定（旧5区史・新修港区史は目次頁のみ）'
    '＋d110022の同定補訂＝titleタグ全170節頁が「港区史 通史編 近世（下）」・目次378ページ始まり＝港区史第3巻（第326回の「資料編2-1近世」同定は誤り・'
    'ADEACに資料編テキストは存在せず・d110011〜20・23〜30はnot-exist）＝第326回d110022掃引の陰性判定は第3巻分として有効に読み替え'
    '＋港区史第1巻ht001050の日頭郷比定文言（『日本地理志料』〔邨岡良弼〕巻16経由「小日向、小石川、牛込、市谷、金杉、関口、音羽、高田、雑司谷、池袋」＝'
    'GAZ-092鳥越村条との比定範囲対照・引用元はrepo未収録書誌で二次引用扱い）'
    '＋図説港区の歴史ht003590の年表（青山上水万治3年・三田上水寛文4年＝BOOK-329整合）＋港区史上目次第八章「上・下水道」887頁（本文テキスト未公開）'
    ' ／ 旧番号: — ／ テキスト一覧・本文テキストHTMLの機械的取得で確認（図版判読は未実施）（ai）'
)

BOOK330_LINE = (
    '- [BOOK-330](books/BOOK-330.md) — 村松梢風『浪人倶楽部』第一部（文昭社・昭和15〔1940〕6月28日発行・小村雪岱挿絵・'
    'NDL次世代DL 1052683・repo全体初出）（2026-11-25・第327回・lab「音羽川」掃引→全文ZIP頁別展開で取得）'
    '— 捕物逃走場面（幕末設定）の「條護國寺前を左へ曲つて一丁餘行くと音羽川といふ、狹い流れながら割りに溪の深い川がある」'
    '＋「向う岸の崖の上を椎の老木」「丸木を並べた橋が架つてゐて橋下には浮々たる水聲が聞え」「一寸都離れのした幽（寂?）な場所」'
    '＋追詰め場面「一方は幾丈にもある崖で、近付かない。只三方から取り卷いてゐるだけだ。其の下を音羽川が流れてゐる」'
    '＝護国寺前から一丁余の開渠音羽川の地形描写（狹い流れ・深い溪・崖・椎・丸木橋・雑木林の山）＝弦巻川・音羽川の旧谷景観の文学描写の復元資料候補'
    '（幕末設定の虚構ゆえ1940年の実景観察の直接証拠にはしない・音羽川1932〜34年暗渠化仮説〔README既出〕との年代対照点）'
    '＋前段「音羽の通」の呑み屋街並み・江戶川邊からの尾行＋第一話「ろくろ首」の小石川江戸川べり（料理屋「雪乃家」）〜音羽〜雑司ヶ谷の地名運用'
    '＋「音羽の屋敷町」表記＋書誌確定（ZIP奥付OCR=昭和15年6月28日発行・第一部終・定価1円50銭・発行所東京市京橋区銀座西八ノ九/ndlsearch SRU=昭和15年2冊本の第1冊・1948年10月307p再刊の別書誌）'
    ' ／ 旧番号: — ／ OCR全文確認（文言は原本画像との照合を要する・印刷頁対応は断片数字ベース）（ai）'
)


def must_one(hay, needle):
    n = hay.count(needle)
    assert n == 1, 'must_one failed: %r found %d times' % (needle[:60], n)


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第327回:**'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README.md ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第327回:' in readme:
        print('README: 第327回bullet already present; skip')
    else:
        must_one(readme, '- **第326回:')
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第326回:')]
        assert len(hits) == 1, 'README anchor 第326回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- docs/sources/INDEX.md ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()

    changed = False

    if '[GOV-603](gov/GOV-603.md)' in index:
        print('INDEX: GOV-603 line already present; skip')
    else:
        must_one(index, '- [GOV-602](gov/GOV-602.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [GOV-602](gov/GOV-602.md)')]
        assert len(hits) == 1, 'INDEX anchor GOV-602 found %d' % len(hits)
        lines.insert(hits[0] + 1, GOV603_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: GOV-603 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 行政・公的機関（600件）')
        index = index.replace('## 行政・公的機関（600件）', '## 行政・公的機関（601件）', 1)
        print('INDEX: 行政 count 600->601')

    if '[BOOK-330](books/BOOK-330.md)' in index:
        print('INDEX: BOOK-330 line already present; skip')
    else:
        must_one(index, '- [BOOK-329](books/BOOK-329.md)')
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BOOK-329](books/BOOK-329.md)')]
        assert len(hits) == 1, 'INDEX anchor BOOK-329 found %d' % len(hits)
        lines.insert(hits[0] + 1, BOOK330_LINE)
        index = '\n'.join(lines)
        changed = True
        print('INDEX: BOOK-330 line inserted after line %d' % (hits[0] + 1))
        must_one(index, '## 書籍・雑誌・メディア（328件）')
        index = index.replace('## 書籍・雑誌・メディア（328件）', '## 書籍・雑誌・メディア（329件）', 1)
        print('INDEX: 書籍 count 328->329')

    if changed:
        must_one(index, '資料ファイル総数: 1841件')
        index = index.replace('資料ファイル総数: 1841件', '資料ファイル総数: 1843件', 1)
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: counts updated (行政600->601・書籍328->329・総数1841->1843)')


if __name__ == '__main__':
    main()
