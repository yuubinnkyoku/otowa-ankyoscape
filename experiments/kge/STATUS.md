# KGE 実験の現状

2026-09-10 時点の抽出・検証結果。

## 現在の規模

GitHub Actions 上で次を確認している。

- entities: **111**
- sources: **40**
- claims: **119**
- hypotheses: **15**
- `confirmed`: **63**
- `observation`: **15**
- `secondary_transcription`: **21**
- `pending`: **20**
- `confirmed` / `observation` かつ `predictable=true` の relation に限定した静的 KGE 三つ組: **50**

当初の 44 claims / 26 triples からは増えたが、KGE に安全に使う静的辺はまだ50件である。数を増やすために二次転記・未確認情報を正例へ格上げしない。

今回、既存の豊島区1999年資料から「水窪川 — flows_through → 辻広場」を既存オーラルヒストリーとは別の公的二次資料で再確認し、`confirmed` claim を1件追加した。ただし同一 base triple なので静的50 triples自体は増えない。**同じ関係を独立資料で再確認できたこと**を証拠密度として保持する。

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

である。`period` や注記から代表年を推測して埋れず、整数の `time.at` があるものだけを使う。

### 2. discovery / evidence time — その関係をいつの史料で確認できるか

`python scripts/export_discovery_kge.py` は、各 claim が引用する**このリポジトリ内の年代付き出典のうち最古年**を用いて、関係が資料集合へ現れる時点を作る。

現在の出力は、

- **37 facts**
- **1682〜2024年**
- **12 distinct years**

である。

前回の31 factsから6件増えた。内訳は、練馬区資料 `S11` の資料年を公式ページ上で確認して2024年と記録したことで5 base triplesが timeline に入ったことと、豊島区1999年資料による辻広場の独立再確認を追加したことで1 base tripleが1999年側に入ったことによる。

これは「人類がその事実を初めて発見した年」ではない。あくまで**現在このリポジトリに結び付いている資料群の中での最古の証拠年**であり、史料追加によって過去へ動く可能性がある。

Hakken 的な「過去までに知られていた関係から、後の資料に現れる関係を予測する」実験では、historical time より **discovery / evidence time を主軸**にする。

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

### discovery-time の診断

CI では `train < 2016`, `2016 <= valid < 2021`, `test >= 2021` で厳密に分割する。現在は、

```text
train                 22
valid                  1
  valid_seen            0
  valid_cold_start      1
test                  14
  test_seen             2
  test_cold_start      12
```

である。

S11の資料年確定で2024年側の事実が増えたため test の総数と cold-start は増えた。これはモデル性能が悪化したという意味ではなく、**今まで timeline から欠落していた後年資料の関係が正しく評価集合へ入った**結果である。

まだ validation と test の双方に十分な seen fact が揃う段階ではないため、現時点で MRR / Hits@K を「未来発見能力」と解釈しない。

## 研究キューを自動生成する

`python scripts/build_research_queue.py` を追加した。モデルを回す前に、現状のグラフで何を調べると時系列密度が上がるかを機械的に出す。

現在の診断は、

- temporal-predictable な保守的 base triples: **42**
- historical time が1件以上ある triples: **22**
- historical time が2年代以上ある再観測 triples: **2**
- discovery/evidence time に入れる triples: **37**
- source year 不明だけが理由で discovery timeline に入らない base triples: **5**
- conservative graph で degree <= 2 の中核水系実体: **37**

である。

特に重要なのは、**42 base triplesのうち、同一関係を2年代以上の historical time で直接再観測できているものがまだ2件しかない**ことである。現状ではモデル選定より、既存実体を別年代の一次史料で再観測する作業の方が価値が高い。

残る discovery-time 欠損5 base triplesは、

- 1956年の谷端川・千早町〜長崎区間 `flows_through` 2件
- 1956年の谷端川・要町区間 `flows_through` 2件
- 千川上水 `branches_from` 玉川上水 1件

である。前4件は `TOSHIMA_YABATA_TIMELINE`、最後の1件は `S08` の source year を推測せず保留している。Webページの最終更新日を資料作成年と同一視しない。

生成先は `experiments/kge/research-queue.md`。CIで毎回再生成し、A: source year欠損、B: historical再観測不足、C: low-degree中核実体の三方向から次の史料調査候補を出す。

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
| discovery/evidence | 37 | 42 | 1682〜2024 |

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
4. 「後世の資料が過去の状態を述べる」場合に historical time と source year を混同しないこと
5. 未確認資料は `pending` / `secondary_transcription` のまま保持し、原資料確認時だけ更新すること

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
python scripts/export_hakken_thiger_raw.py
python scripts/export_hakken_thiger_raw.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/hakken/raw-discovery
python scripts/build_research_queue.py
```

抽出時の規則は [`prompts/extract-knowledge-graph.md`](../../prompts/extract-knowledge-graph.md) を使う。
