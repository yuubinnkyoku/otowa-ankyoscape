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

既存の豊島区1999年資料から「水窪川 — flows_through → 辻広場」を既存オーラルヒストリーとは別の公的二次資料で再確認した。さらに東京都建設局の年代付き公式ページを `S42` として追加し、「千川上水 — branches_from → 玉川上水」を既存 `S08` とは独立に再確認した。どちらも既存 base triple の再確認なので静的50 triples自体は増えないが、**同じ関係を独立資料で再確認できたこと**を証拠密度として保持する。

## 証拠を増やすだけでは足りない

`python scripts/graph_stats.py` で、予測に使う保守的な三つ組の疎さも確認する。

現在は KGE に参加する55実体のうち、

- degree = 1: **42実体（76.4%）**
- degree <= 2: **47実体**

となっている。

つまり、実体数を増やし続けても「一度しか現れない地点」が増えるだけならリンク予測には効きにくい。今後は、すでにある河川・橋・地区・河道区間へ複数の独立した辺を結び、**同じ実体が異なる史料・年代・関係で繰り返し現れる密度**を高める必要がある。

## 静的 coverage-aware split

`python scripts/make_kge_split.py` は、学習データから実体・関係が完全に消えない範囲で既知辺を隠す。

現在の50三つ組では、要求した30% holdoutをそのまま作れず、実際には次までしか安全に分割できない。

```text
train  44
valid   2
test    4
```

要求値は `valid=5`, `test=10`。まだ評価標本が小さいので、仮に ComplEx / DistMult の評価値が高くても、河川史上の「発見能力」があるとは解釈しない。

## 時間を二種類に分ける

この調査では「時間」に二つの意味がある。

### 1. historical time — その状態・出来事がいつ存在したか

`claim.time.at` を使う。たとえば「1851年の地図で弦巻川が護国寺南西端を通る」「1956年にある区間が暗渠化された」のような、**歴史世界の時間**である。

`python scripts/export_temporal_kge.py` の現在の出力は、

- **24 facts**
- **1682〜2016年**
- **11 distinct years**

である。`period` や注記から代表年を推測して埋めず、整数の `time.at` があるものだけを使う。

### 2. discovery / evidence time — その関係をいつの史料で確認できるか

`python scripts/export_discovery_kge.py` は、各 claim が引用する**このリポジトリ内の年代付き出典のうち最古年**を用いて、関係が資料集合へ現れる時点を作る。

現在の通常出力は、

- **38 facts**
- **1682〜2024年**
- **13 distinct years**

である。

31 factsの段階から、練馬区資料 `S11` の資料年を2024年と確認して5 base triplesを追加し、豊島区1999年資料による辻広場の独立再確認で1 base tripleを追加した。東京都建設局 `S42` のページ日付を2018年と記録したことで「千川上水 — branches_from → 玉川上水」も discovery timeline に入り、2018年が distinct year に加わった。

これは「人類がその事実を初めて発見した年」ではない。あくまで**現在このリポジトリに結び付いている資料群の中での最古の証拠年**であり、史料追加によって過去へ動く可能性がある。

## source.year の意味を分離する

`source.year` は歴史上の出来事年ではなく、資料そのものの年代として扱う。意味は `source.year_kind` に記録する。

現在の ontology では `publication`, `creation`, `issue`, `page_update`, `edition`, `unknown` を区別する。古いレコードで `year_kind` が未設定の場合は、感度分析上 `unspecified` として扱う。

特に Web ページの更新年は、そのページに書かれた歴史的事実がその年に初めて知られたことを意味しない。そのため、通常版に加えて年代の採用条件を厳しくした二種類の discovery timeline を CI で生成する。

| discovery timeline | 採用する年代 | facts | distinct years |
|---|---|---:|---:|
| baseline | 年代付き source 全体 | 38 | 13 |
| no-page-update | `page_update` を除外 | 31 | 11 |
| classified-only | `page_update`, `unspecified`, `unknown` を除外 | 22 | 6 |

`classified-only` は、年代の意味を明示的に分類済みで、かつ Web 更新日ではない source だけを使う保守的な感度分析である。現在残る年代は **1682, 1851, 1999, 2000, 2001, 2021** の6時点である。

## 厳密な時間順 backtest

`make_temporal_backtest.py` は未来の辺を学習側へ移動して coverage を稼がない。後年に初登場する実体・関係は cold-start として別集計する。

### historical-time の診断

`train < 1930`, `1930 <= valid < 1960`, `test >= 1960` では、

```text
train                 15
valid                  4
  valid_seen            0
  valid_cold_start      4
test                   5
  test_seen             0
  test_cold_start       5
```

となった。relation は train に6種類すべて現れるが、後期の実体が学習時点に存在しないため、通常の temporal link prediction として評価できる seen fact がない。

これは historical-time を捨てる理由ではない。歴史地形の状態変化を扱う軸としては必要だが、**現在のデータ量では Hakken 型の未来リンク評価用データとして弱い**という診断である。

### discovery-time の感度分析

CI では `train < 2016`, `2016 <= valid < 2021`, `test >= 2021` を基準に三種類の timeline を比較する。

| timeline | train | valid | test | valid_seen | test_seen | test_cold_start |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 22 | 2 | 14 | 0 | 2 | 12 |
| no-page-update | 22 | 1 | 8 | 0 | 2 | 6 |
| classified-only | 14 | 0 | 8 | 0 | 2 | 6 |

重要なのは、**test 側の seen fact 2件は `page_update` と未分類年代をすべて除外した `classified-only` でも残る**ことである。したがって、この2件が単純に Web 更新年や年代種別未確認の source によって人工的に作られたものではないことは確認できた。

ただし `classified-only` では2016〜2020年に採用可能な fact がなく、validation は0件になる。これはむしろ、現在の資料密度ではモデル比較・ハイパーパラメータ選択を含む通常の temporal link prediction 評価が成立していないことを示す。**2件が残ったことは評価データの健全性確認であって、モデルの未来発見能力の証拠ではない。**

cutoff scan では `classified-only` に対し `train < 2001 / valid < 2021` とした場合でも `train=12 / valid=2 / test=8` だが `valid_seen=0 / test_seen=2` である。現状では cutoff を動かしても validation と test の両方に十分な seen fact を作れない。

## 研究キューを自動生成する

`python scripts/build_research_queue.py` は、モデルを回す前に現状のグラフで何を調べると時系列密度と年代信頼性が上がるかを機械的に出す。

現在の診断は、

- temporal-predictable な保守的 base triples: **42**
- historical time が1件以上ある triples: **22**
- historical time が2年代以上ある再観測 triples: **2**
- discovery/evidence time に入れる triples: **38**
- source year 不明だけが理由で discovery timeline に入らない base triples: **4**
- conservative graph で degree <= 2 の中核水系実体: **37**
- `year_kind` 未分類の年代付き source: **14**
- そのうち temporal graph で実際に使われる source: **5**
- source year と historical time が同年で、意味の確認を優先する source: **4**

である。

最後の4件は即「誤り」と判定するものではない。たとえば同時代刊行物なら source year と historical time が一致するのは当然ありうる。ここでは、**出来事年を source year に誤ってコピーしていないかを優先確認する対象**として検出している。

現在の要確認4件は `G02`（1836年『江戸名所図会』）、`ZOSHIGAYA_SEWER_2008`、`S34`（1895年谷端川水車設立願を掲げる区史年表）、`S40`（2016年東京都議会記録）である。加えて `BUNKYO_HATSUNE` は未分類年代を持ち、temporal graph の2関係で使われている。

特に重要なのは、**42 base triplesのうち、同一関係を2年代以上の historical time で直接再観測できているものがまだ2件しかない**ことである。現状ではモデル選定より、既存実体を別年代の一次史料で再観測する作業の方が価値が高い。

残る discovery-time 欠損4 base triplesはすべて1956年の谷端川暗渠工事関係で、

- 千早町〜長崎区間 `flows_through` 2件
- 要町区間 `flows_through` 2件

である。現在の `TOSHIMA_YABATA_TIMELINE` は出来事年1956年を示すが、discovery/evidence time に使う資料側の年をまだ確定していない。このタイムラインが依拠する当時の区公報について、号数・発行日・ページを直接確認する作業を `docs/open-questions/谷端川1956年暗渠工事の区公報原典確認.md` に分離している。

生成先は `experiments/kge/research-queue.md`。CIで毎回再生成し、A: source year欠損、B: historical再観測不足、C: low-degree中核実体、D: source年代の意味未分類、の四方向から次の史料調査候補を出す。

## HakkenOSS への接続

### 静的 KGE

HakkenOSS の `TextKGDataset` に、このリポジトリの三つ組 TSV を渡せる。設定例は

```text
experiments/kge/hakken/otowa.yaml
```

に置く。

### THiGER raw schema

HakkenOSS の `hakken-models` が読む raw schema に対し、二種類の時間軸を別ディレクトリへ出力する。

```bash
# 歴史世界の時間
python scripts/export_hakken_thiger_raw.py

# 資料上の発見・証拠時間
python scripts/export_discovery_kge.py
python scripts/export_hakken_thiger_raw.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/hakken/raw-discovery
```

現在の出力は次の通り。

| 軸 | edge rows | nodes | 年代範囲 |
|---|---:|---:|---|
| historical | 24 | 30 | 1682〜2016 |
| discovery/evidence baseline | 38 | 43 | 1682〜2024 |

生成物はそれぞれ、

```text
experiments/kge/hakken/raw-historical/
experiments/kge/hakken/raw-discovery/
```

に置く。

THiGER の packaged dataset は HakkenOSS 側の dataset preparation に任せ、こちらでは証拠つき `claims` から再生成できる raw ingestion boundary を責務とする。

## THiGER と THiGERLLM

HakkenOSS の `hakken-models` には **THiGER 本体のモデル・学習・評価コード**がある。一方、論文で説明される **THiGERLLM** と完全に同一の実装は確認できていない。

したがって、

```text
THiGER        : OSS 実装を直接試せる
THiGERLLM     : 論文上の構成。完全な同一実装は未確認
hakken-agents : LLM を使う抽出・entity resolution 系。別系統
```

として区別する。

## 次に増やすべきもの

目標は単なる100 triplesではなく、**時間をまたいで同じ語彙が繰り返し現れる100 triples**にする。

優先するのは、

1. 水窪川・弦巻川・谷端川そのものを、複数年代の地図・地誌から同じ relation で記録すること
2. 既存の橋・地点について別年代の一次史料を追加し、future 側でも train 既知の entity が再登場するようにすること
3. `flows_through`, `flows_to`, `source_of`, `supplies`, `branches_from` を中心に、relation ごとの例数を増やすこと
4. `source.year_kind` を未分類のまま放置せず、資料の刊行年・作成年・号の年・Web更新年を区別すること
5. 「後世の資料が過去の状態を述べる」場合に historical time と source/evidence time を混同しないこと
6. 未確認資料は `pending` / `secondary_transcription` のまま保持し、原資料確認時だけ更新すること

この方針なら、Hakken の出力を「史実」として採用するのではなく、**次に確認すべき河道・接続・史料候補の順位付け**として使える。

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
python scripts/scan_temporal_cutoffs.py \
  --input experiments/kge/discovery/all.tsv \
  --output experiments/kge/discovery/cutoff-scan.json
python scripts/make_temporal_backtest.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/discovery/backtest \
  --train-end 2016 --val-end 2021
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
