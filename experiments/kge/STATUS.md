# KGE 実験の現状

2026-09-10 時点の抽出・検証結果。

## 現在の規模

GitHub Actions 上で次を確認している。

- entities: **111**
- sources: **41**
- claims: **120**
- hypotheses: **15**
- `confirmed`: **64**
- `observation`: **15**
- `secondary_transcription`: **21**
- `pending`: **20**
- `confirmed` / `observation` かつ `predictable=true` の relation に限定した静的 KGE 三つ組: **50**

当初の 44 claims / 26 triples からは増えたが、KGE に安全に使う静的辺はまだ50件である。数を増やすために二次転記・未確認情報を正例へ格上げしない。

既存の豊島区1999年資料から「水窪川 — flows_through → 辻広場」を既存オーラルヒストリーとは別の公的二次資料で再確認した。さらに東京都建設局の年代付き公式ページを `S42` として追加し、「千川上水 — branches_from → 玉川上水」を既存 `S08` とは独立に再確認した。どちらも既存 base triple の再確認なので静的50 triples自体は増えないが、独立資料による証拠密度を保持する。

## 証拠を増やすだけでは足りない

`python scripts/graph_stats.py` で、予測に使う保守的な三つ組の疎さも確認する。

現在は KGE に参加する55実体のうち、

- degree = 1: **42実体（76.4%）**
- degree <= 2: **47実体**

となっている。

単発の地点を増やすだけではリンク予測には効きにくい。今後は、すでにある河川・橋・地区・河道区間へ複数の独立した辺を結び、**同じ実体が異なる史料・年代・関係で繰り返し現れる密度**を高める。

## 静的 coverage-aware split

現在の50三つ組では、学習側から実体・関係を消さないように分割すると次までしか安全に holdout できない。

```text
train  44
valid   2
test    4
```

要求値は `valid=5`, `test=10`。評価標本が小さいため、ComplEx / DistMult の値が高くても河川史上の「発見能力」とは解釈しない。

## 時間を二種類に分ける

### 1. historical time

`claim.time.at`。その状態・出来事が歴史上いつ存在したかを表す。

現在：**24 facts / 1682〜2016年 / 11 distinct years**。

`period` や注記から代表年を推測せず、整数の `time.at` があるものだけを使う。

### 2. discovery / evidence time

各 claim が引用する年代付き source のうち、現在のリポジトリで最古のものを用いて「この資料集合ではいつその関係を確認できるか」を表す。

現在の baseline：**37 facts / 1682〜2024年 / 12 distinct years**。

これは社会全体での真の発見年ではない。古い史料が後から追加されれば過去へ動く、**corpus-first evidence year** である。

## source.year の意味を分離する

`source.year` は歴史上の出来事年ではなく、資料そのものの年代として扱う。意味は `source.year_kind` に記録する。

現在の ontology では `publication`, `creation`, `issue`, `page_update`, `edition`, `unknown` を区別する。古いレコードで `year_kind` が未設定の場合は感度分析上 `unspecified` として扱う。

今回この検査によって、`S34`「豊島区史年表 1895年谷端川新規水車設立願」の **1895年が source の刊行年ではなく年表項目の出来事年**として入っていたことを検出した。`S34.year` は `null` に戻し、1895年は claim 側の historical time にだけ残した。その結果、discovery timeline から人工的な1895年が消えた。

同時に、temporal graph で実際に利用される年代付き source の意味を確認し、`G02` を `publication`、`S40` を `issue`、`ZOSHIGAYA_SEWER_2008` と `BUNKYO_HATSUNE` を `publication` として整理した。

現在の年代付き source の内訳は、`publication=15`, `issue=2`, `page_update=3`, `unspecified=8`。残る `unspecified` 8件は、現在の保守的 temporal graph では **0件も使われていない**。

## discovery/evidence time の感度分析

CI では年代の採用条件を変えた三種類を毎回生成する。

| timeline | 除外する source 年代 | facts | distinct years |
|---|---|---:|---:|
| baseline | なし | **37** | **12** |
| no-page-update | `page_update` | **30** | **10** |
| classified-only | `page_update`, `unspecified`, `unknown` | **30** | **10** |

`classified-only` に残る年は **1682, 1836, 1851, 1999, 2000, 2001, 2008, 2014, 2016, 2021**。

現在 `classified-only` と `no-page-update` が同一になったのは、未分類年代を持つ source が残っていても、それらが retained temporal graph の関係には使われていないためである。これは source-date 監査が現在の予測用グラフまで一通り到達したことを意味する。

## 厳密な時間順 backtest

`make_temporal_backtest.py` は未来の辺を coverage のために train へ戻さない。後年に初登場する実体・関係は cold-start として別集計する。

### historical-time

`train < 1930`, `1930 <= valid < 1960`, `test >= 1960`：

```text
train                 15
valid                  4
  valid_seen            0
  valid_cold_start      4
test                   5
  test_seen             0
  test_cold_start       5
```

relation は train に6種類すべて現れるが、後期の実体が学習時点に存在せず通常の temporal link prediction として評価できる seen fact がない。historical time は歴史地形の状態変化には必要だが、現状では Hakken 型未来リンク評価には弱い。

### discovery-time

`train < 2016`, `2016 <= valid < 2021`, `test >= 2021`：

| timeline | train | valid | test | valid_seen | test_seen | test_cold_start |
|---|---:|---:|---:|---:|---:|---:|
| baseline | **21** | **2** | **14** | **0** | **2** | **12** |
| no-page-update | **21** | **1** | **8** | **0** | **2** | **6** |
| classified-only | **21** | **1** | **8** | **0** | **2** | **6** |

重要なのは、test 側の seen fact 2件が、Web更新年と未分類年代を除外した `classified-only` でも残ること。一方、validation は1件あるが cold-start なので `valid_seen=0` のままである。

したがって **2件が残ったことは評価データの健全性確認であって、モデルの未来発見能力の証拠ではない**。cutoff を動かしても validation と test の双方に十分な seen fact を確保できないため、現段階で MRR / Hits@K を未来発見能力として解釈しない。

## 研究キューを自動生成する

`python scripts/build_research_queue.py` は、次にどの史料・地点を確認すればグラフが強くなるかを毎回診断する。

現在：

- temporal-predictable base triples: **42**
- historical time がある triples: **22**
- 2年代以上で直接再観測された triples: **2**
- discovery/evidence eligible triples: **37**
- source year 不明のため blocked: **5**
- degree <= 2 の中核水系実体: **37**
- `year_kind` 未分類の年代付き source: **8**
- そのうち temporal graph で使用: **0**
- source/event year 衝突の優先確認候補: **0**

source-date 汚染の優先確認は現在0まで減った。次の主な欠損は5関係である。

1. 1956年の谷端川・千早町〜長崎区間 `flows_through` 2件
2. 1956年の谷端川・要町区間 `flows_through` 2件
3. 谷端川 — `flows_through` → 巣鴨村大字巣鴨字新田928（historical time 1895）1件

前4件は `TOSHIMA_YABATA_TIMELINE` が依拠する当時の区公報の号数・発行日・ページを直接確認する必要がある。5件目は `S34` の年表項目について、1895年という出来事年とは別に、その年表自体の資料年代またはより直接的な原史料を探す。

ただし、より大きなボトルネックは **42 base triplesのうち同一関係を2年代以上で直接再観測できているものが2件しかないこと**である。source year の穴埋めだけでなく、既存の河川・橋・地点を別年代の一次史料で再観測する作業を優先する。

生成先は `experiments/kge/research-queue.md`。A: source year欠損、B: historical再観測不足、C: low-degree実体、D: source年代の意味未分類、の四方向から候補を出す。

## HakkenOSS への接続

### 静的 KGE

HakkenOSS の `TextKGDataset` に三つ組 TSV を渡す設定例：

```text
experiments/kge/hakken/otowa.yaml
```

### THiGER raw schema

```bash
# historical time
python scripts/export_hakken_thiger_raw.py

# discovery / evidence time
python scripts/export_discovery_kge.py
python scripts/export_hakken_thiger_raw.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/hakken/raw-discovery
```

現在の exporter 出力：

| 軸 | edge rows | nodes | 年代範囲 |
|---|---:|---:|---|
| historical | **24** | **30** | 1682〜2016 |
| discovery/evidence baseline | **37** | **42** | 1682〜2024 |

THiGER の packaged dataset は HakkenOSS 側の dataset preparation に任せ、こちらでは証拠つき `claims` から再生成できる raw ingestion boundary を責務とする。

## THiGER と THiGERLLM

```text
THiGER        : HakkenOSS にモデル・学習・評価コードあり
THiGERLLM     : 論文上の構成。完全に同一の OSS 実装は未確認
hakken-agents : LLM を使う抽出・entity resolution 系。別系統
```

## 次に増やすべきもの

目標は単なる100 triplesではなく、**時間をまたいで同じ語彙が繰り返し現れる100 triples**にする。

優先順位は、同じ水窪川・弦巻川・谷端川や既存の橋・地点を複数年代の地図・地誌で同じ relation として再観測すること。そのうえで `flows_through`, `flows_to`, `source_of`, `supplies`, `branches_from` を中心に relation ごとの例数を増やす。

未確認資料は `pending` / `secondary_transcription` のまま保持し、Hakken / KGE の出力は史実ではなく**次に確認すべき河道・接続・史料候補の順位付け**に使う。

## 再現

```bash
python scripts/validate_graph.py
python scripts/graph_stats.py
python scripts/collect_tagged_passages.py --summary-only
python scripts/export_kge.py
python scripts/make_kge_split.py
python scripts/export_temporal_kge.py
python scripts/scan_temporal_cutoffs.py
python scripts/make_temporal_backtest.py --train-end 1930 --val-end 1960
python scripts/export_discovery_kge.py
python scripts/export_discovery_kge.py \
  --exclude-year-kinds page_update \
  --output experiments/kge/discovery/no-page-update.tsv
python scripts/export_discovery_kge.py \
  --exclude-year-kinds page_update,unspecified,unknown \
  --output experiments/kge/discovery/classified-only.tsv
python scripts/make_temporal_backtest.py \
  --input experiments/kge/discovery/classified-only.tsv \
  --output-dir experiments/kge/discovery/classified-only-backtest \
  --train-end 2016 --val-end 2021
python scripts/export_hakken_thiger_raw.py
python scripts/export_hakken_thiger_raw.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/hakken/raw-discovery
python scripts/build_research_queue.py
```

抽出時の規則は [`prompts/extract-knowledge-graph.md`](../../prompts/extract-knowledge-graph.md) を使う。
