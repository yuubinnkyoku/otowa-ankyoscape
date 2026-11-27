#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第367回: READMEに実行記録bulletを挿入し、INDEXにBLOG-351〜355行を挿入・計数更新するヘルパー。
使い方: python3 .366-insert.py [base_dir]  （既定 base_dir='.'）
- README.md: '- **第366回:' 行の直後に .367-bullet.txt の1行を挿入。
- docs/sources/INDEX.md: BLOG-350 行の直後に BLOG-351〜355 の5行を挿入し、
  '## ブログ・個人サイト（349件）'→'（354件）'、'資料ファイル総数: 1921件'→'1926件' を更新。
"""
import io
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
README = os.path.join(BASE, 'README.md')
INDEX = os.path.join(BASE, 'docs', 'sources', 'INDEX.md')
HERE = os.path.dirname(os.path.abspath(__file__))
BULLET = os.path.join(HERE, '.367-bullet.txt')

NEW_LINES = [
    '- [BLOG-351](blogs/BLOG-351.md) — 水徒然（onnbubatta）専用水道3部作「練馬区内の水道利用組合（専用水道）」＋「田柄町水道利用組合」＋「田柄水道利用組合(終)。田柄用水跡。北町お散歩」（2011年8月30日〜9月11日・直はCloudFront 403のためWaybackスナップショット（2024-05-24）で本文全文取得＝直接確認・第367回）— 天祖神社の「玉川上水分水」碑（漢詩調・田無で玉川上水の分水を受け村民協力で水路を掘り灌漑用水を導入し美田とした旨）＝千川上水と田柄灌漑用水の接続を頌徳碑レベルで裏付けるrepo初出の独立記録候補（碑文全文・建立年は現地確認待ち）＝BLOG-118・GOV-068・BLOG-331を強める根拠＋田柄水道利用組合3204㎥/日（平成22年統計・23区内屈指）・北町南水道組合解散（2010年頃）・田柄3丁目「水源地」表記・愛宕神社の用水洗い場と金魚市〔聴取〕＝地下水・専用水道への移行後の分布記録（GOV-063/081対照） ／ 旧番号: — ／ 直接確認（Wayback本文全文・第367回）（ai）',
    '- [BLOG-352](blogs/BLOG-352.md) — 水徒然（onnbubatta）「田柄川」観察4部作（謝辞暗渠・人生暗渠・ゴミ箱軍団暗渠・架橋？）（2011年8月28日〜2012年10月2日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第367回）— 田柄川沿いの暗渠群の2011-12年断面（本体緑道の水位計＝水位管理の継続・開渠残存）＋14426590の2013年追記「大きなマンホールが埋められて様子が変わった」＝暗渠道消失記録＋田柄3丁目のビールケース状橋脚の未同定遺構＝BLOG-351（用水碑文）・BLOG-118に加わる定点観察群 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第367回）（ai）',
    '- [BLOG-354](blogs/BLOG-354.md) — 水徒然（onnbubatta）「文京区後楽の水路跡」＋「続・後楽２丁目の水路跡～地籍図から判ったこと」（2016年4月・7月・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第367回・BLOG-345が参照した記事の本体）— 地籍図の青線3水路（当該水路＝春日通り〜諏訪神社側窪地・三井邸敷地直下から巻石通りへ落ちる流路・諏訪神社南側の第3水路）＝repo初出＋江戸初期の白鳥池〜小石川沼大湿地帯枠組み＋2020年8月追記＝文京区水道1丁目の地籍図記載水路跡現存〔観察〕＋「復元江戸情報地図」書誌候補＝弦巻川合流点〜神田川大湾曲部南岸の小水路群の新記録（地籍図の正式書誌特定が次の一手） ／ 旧番号: — ／ 直接確認（Wayback本文全文・第367回）（ai）',
    '- [BLOG-353](blogs/BLOG-353.md) — 水徒然（onnbubatta）「道路計画（大蛇）に飲み込まれる過去の川」（2016年3月19日）＋「心機一転春が来た 田柄の鮮やか水路敷」（2022年3月26日・直はCloudFront 403のためWaybackスナップショットで本文全文取得＝直接確認・第367回）— 平和台駅周辺の道路計画でGoogle Earth 1997年撮影分の水路跡が消滅＝repo初出＋「水路敷」道路ペイントの2022年刷新観察・寄贈蓋情報＝水路敷ペイント＝旧水路の道路管理上の名残の慣行継続（2022年時点）の記録 ／ 旧番号: — ／ 直接確認（Wayback本文全文・第367回）（ai）',
    '- [BLOG-355](blogs/BLOG-355.md) — 山の風音（yamakaze）「神田上水下部を歩く（大洗堰〜懸樋）」（2022年5月18日・EUC-JP頁をcurl直接取得＝直接確認・第367回）— 神田上水旧白堀跡の発掘調査（平成23〜24年・2011-12）記録＝白堀（開渠）の初発見・新旧2筋・伊豆石石積み護岸60m・新白堀は明治10年（1877）頃石蓋アーチ状暗渠化・発掘時点は大正期埋戻し状態・左岸のみ・『東京市史稿上水篇』川幅約3m＝repo初出でBLOG-346の「解体中の中学」＝文京区立第五中学校（旧黒田小学校跡・文京区総合福祉センター）と特定＝江戸期白堀文言群（GAZ-049・GAZ-169等）に対する初の考古学的裏付け＋巻石通りの由来「巻石蓋」（明治11年頃説併記） ／ 旧番号: — ／ 直接確認（curl本文全文・第367回）（ai）',
]


def main():
    with io.open(BULLET, encoding='utf-8') as f:
        bullet = f.read().strip('\n')
    assert bullet.startswith('- **第367回:'), 'bullet format check failed'
    assert '\n' not in bullet, 'bullet must be single line'

    # --- README ---
    with io.open(README, encoding='utf-8') as f:
        readme = f.read()
    if '- **第367回:' in readme:
        print('README: 第367回bullet already present; skip')
    else:
        lines = readme.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- **第366回:')]
        assert len(hits) == 1, 'README anchor 第366回 found %d' % len(hits)
        lines.insert(hits[0] + 1, bullet)
        with io.open(README, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(lines))
        print('README: bullet inserted after line %d' % (hits[0] + 1))

    # --- INDEX ---
    with io.open(INDEX, encoding='utf-8') as f:
        index = f.read()
    if 'BLOG-351' in index:
        print('INDEX: BLOG-351 already present; skip')
    else:
        assert '## ブログ・個人サイト（349件）' in index, 'INDEX ブログ heading mismatch'
        assert '資料ファイル総数: 1921件' in index, 'INDEX 総数 mismatch'
        lines = index.split('\n')
        hits = [i for i, l in enumerate(lines) if l.startswith('- [BLOG-350]')]
        assert len(hits) == 1, 'INDEX anchor BLOG-350 found %d' % len(hits)
        for off, nl in enumerate(NEW_LINES, start=1):
            lines.insert(hits[0] + off, nl)
        index = '\n'.join(lines)
        index = index.replace('## ブログ・個人サイト（349件）', '## ブログ・個人サイト（354件）')
        index = index.replace('資料ファイル総数: 1921件', '資料ファイル総数: 1926件')
        with io.open(INDEX, 'w', encoding='utf-8', newline='') as f:
            f.write(index)
        print('INDEX: BLOG-351..355 inserted after line %d; counts updated' % (hits[0] + 1))


if __name__ == '__main__':
    main()
