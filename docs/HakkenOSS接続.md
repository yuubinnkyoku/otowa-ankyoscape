# HakkenOSS 接続メモ

この文書は、`otowa-ankyoscape` の証拠つき知識グラフを Sony Research の [HakkenOSS](https://github.com/SonyResearch/HakkenOSS) へ接続する際に、**実際に公開コードで確認できた境界**を整理する。

## 結論

現在は HakkenOSS を fork しなくても、次の経路まで接続できる。

1. 静的リンク予測：`TextKGDataset` に三つ組 TSV を渡し、ComplEx / DistMult 等を試す。
2. 時系列モデル：`hakken-models` の THiGER 用 raw schema に年代付き TSV を変換し、Hakken 側の dataset preparation / training へ渡す。
3. Hakken 型の未来発見評価：歴史上の出来事年とは別に、**資料上でその関係を確認できる年（discovery / evidence time）**を作り、時間順 backtest を行う。
4. discovery/evidence time 自体の信頼性を、`source.year_kind` と複数の年代採用方針で感度分析する。

ただし、論文でいう **THiGERLLM と、OSS に実装されている THiGER を同一視しない**。

---

## 1. 静的 KGE: TextKGDataset

HakkenOSS の `models/packages/datasets/datasets/data_repo/text.py` には汎用の `TextKGDataset` があり、三列なら

```text
subject    relation    object
```

として読み込む。

このリポジトリでは、

```bash
python scripts/export_kge.py
python scripts/make_kge_split.py
```

で生成した TSV を Hakken 側へ渡す設定例を

```text
experiments/kge/hakken/otowa.yaml
```

に置いている。

HakkenOSS 参照：
- [`TextKGDataset`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/datasets/datasets/data_repo/text.py)
- [YAGO の `TextKGDataset` 設定例](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/kge/config/data_repo/yago.yaml)

---

## 2. TextKGDataset は4列の時系列 KG も読める

同じ `TextKGDataset` は `column_names` が4列なら temporal KG と判定し、

```text
subject    relation    object    date
```

を `subject / relation / object / timestamp` の4次元 fact tensor へ変換する。

このため、`otowa-ankyoscape` 側には

```bash
python scripts/export_temporal_kge.py
```

を用意した。推測で年代を補わないため、`time.at` が**整数年として明示されている** claim だけを出力する。

設定例：

```text
experiments/kge/hakken/otowa-temporal.yaml
```

ただし、**4列を読めることと、すべての KGE モデルが時間を利用することは別問題**である。ComplEx / DistMult の通常設定に4列を渡しただけで「未来予測」になるとは考えない。

---

## 3. HakkenOSS には THiGER 本体が公開されている

`hakken-models` には `THiGER` クラスが存在する。

HakkenOSS の docstring では THiGER を

> Temporal Hierarchical Graph Embedding Representation (THiGER) model for temporal KGs.

と定義し、GNN で局所的なグラフ構造、Transformer で時系列依存を扱う実装になっている。コンストラクタには `num_entities`, `num_relations`, `num_timestamps` が入り、Transformer の `max_seq_len` に timestamp 数を使う。

参照：
- [`hakken_models/models/thiger/base.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/models/thiger/base.py)
- [`train_thiger.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/steps/thiger/train_thiger.py)
- [パイプライン CLI の `train_thiger`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/scripts/run_pipeline.py)

したがって、**少なくとも THiGER の学習・評価コードは OSS リポジトリ内に存在する。**

---

## 4. ただし THiGERLLM の完全実装は確認できない

Hakken 論文では THiGER と LLM の知識を組み合わせた **THiGERLLM** が重要な構成として説明される。

一方、2026-09-09 時点で HakkenOSS のコード検索から確認できた `THiGERLLM` という文字列は、ベンチマーク結果生成スクリプト中のモデル名などに限られ、`class THiGERLLM` のような実装は確認できない。

HakkenOSS には別に `hakken-agents` があり、OpenAI / OpenRouter / Ollama 等の LLM を使った文書からの entity / fact extraction はできる。しかし、これをそのまま論文の THiGERLLM と同一のモデルとみなさない。

```text
THiGER          : OSS 内にモデル実装あり
THiGERLLM       : 論文上の構成。完全な同一実装は OSS 内で未確認
hakken-agents   : LLM を使う抽出・entity resolution 系。THiGERLLM とは別物
```

---

## 5. THiGER 用 raw schema へ直接出力する

HakkenOSS の `hakken-models` dataset preparation pipeline は raw data として以下を読む。

### `edges.tsv`

```text
subject_id
subject_domain
relation_type
object_id
object_domain
year
number_of_occurrences
```

### `nodes_corrected.tsv`

```text
node_id
node_domain
node_name
node_domain_id
```

参照：
- [`load_facts_df.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/steps/dataset/load_facts_df.py)
- [`load_nodes_df.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/steps/dataset/load_nodes_df.py)
- [`dataset_preparation.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/pipelines/dataset_preparation.py)

このリポジトリでは `scripts/export_hakken_thiger_raw.py` が同じ schema を生成する。入力する時間軸によって出力先を分ける。

### historical time

```bash
python scripts/export_hakken_thiger_raw.py
```

生成先：

```text
experiments/kge/hakken/raw-historical/edges.tsv
experiments/kge/hakken/raw-historical/nodes_corrected.tsv
```

既定では `confirmed` / `observation`、`temporal_predictable=true`、`time.at` が整数年の claim を使う。

現在は **24 edge rows / 30 nodes / 1682〜2016年（11 distinct years）**。

### discovery / evidence time

まず、年代付き出典から「現在の資料集合で最初に確認できる年」を作る。

```bash
python scripts/export_discovery_kge.py
```

次に、その4列 TSV を THiGER raw schema へ変換する。

```bash
python scripts/export_hakken_thiger_raw.py \
  --input experiments/kge/discovery/all.tsv \
  --output-dir experiments/kge/hakken/raw-discovery
```

生成先：

```text
experiments/kge/hakken/raw-discovery/edges.tsv
experiments/kge/hakken/raw-discovery/nodes_corrected.tsv
```

現在の baseline は **38 edge rows / 43 nodes / 1682〜2024年（13 distinct years）**。

`--input` を使った場合、入力 TSV は

```text
subject    relation    object    year
```

の4列とする。これにより、Hakken raw 変換処理と「年をどう定義するか」を分離できる。

---

## 6. 「歴史上の年」と「発見された年」は別物

ここがこの調査で最も重要な区別の一つである。

たとえば、1956年の暗渠工事について2026年刊行の資料で初めて知った場合、

```text
historical time = 1956
source/evidence time = 2026
```

となる。

Hakken 論文が狙う「その時点までの知識から未来の発見を予測する」に近い評価では、**historical time をそのまま使うと未来情報が過去へ移動してしまう**。後世の資料が古い出来事を述べているからである。

そこで `export_discovery_kge.py` は、各採用 claim に紐づく年代付き source の最古年を使う。

ただし、その年は

> 現在 `otowa-ankyoscape` に登録されている資料集合の中で、その関係を確認できる最古年

であって、社会全体・研究史全体での「真の初出年」ではない。古い史料が後から追加されれば年は過去へ動く。この corpus incompleteness は、評価結果と一緒に明示する。

### source.year_kind

さらに、`source.year` の数字だけでは「その年が何を意味するか」が曖昧なので、ontology に `source.year_kind` を導入した。

```text
publication : 本・論文・記事・報告書・公開資料そのものの刊行・公開年
creation    : 写真・地図・原史料など資料そのものの作成年
issue       : 公報・議会速記録など号／会議に対応する年
page_update : Webページの更新年
edition     : 版・改訂版の刊行年
unknown     : 年代の意味を確定できていない
```

古いレコードで `year_kind` 自体が未設定の場合は、exporter 内で `unspecified` として扱う。これは ontology 上の確定値ではなく、**未分類レコードを感度分析から除外可能にするための合成カテゴリ**である。

---

## 7. discovery/evidence time の感度分析

未来予測評価では、Web更新日や意味未分類の年代に結果が依存していないかを分けて確認する。

現在 CI では三種類を生成する。

| timeline | 除外する source 年代 | facts | distinct years |
|---|---|---:|---:|
| baseline | なし | 38 | 13 |
| no-page-update | `page_update` | 31 | 11 |
| classified-only | `page_update`, `unspecified`, `unknown` | 22 | 6 |

`classified-only` に残る年代は **1682, 1851, 1999, 2000, 2001, 2021**。これは、現時点で意味を明示的に分類済みかつ Web 更新年ではない source だけに寄せた保守的な slice である。

同じ `train < 2016 / valid < 2021 / test >= 2021` で比較すると、

| timeline | train | valid | test | valid_seen | test_seen | test_cold_start |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 22 | 2 | 14 | 0 | 2 | 12 |
| no-page-update | 22 | 1 | 8 | 0 | 2 | 6 |
| classified-only | 14 | 0 | 8 | 0 | 2 | 6 |

**test_seen の2件は、Web更新日だけでなく未分類年代も除外した `classified-only` でも残る。** したがって、この2件が弱い source date の採用だけで人工的に生じたわけではないことは確認できる。

ただし `classified-only` では validation が0件である。これはモデルの性能を示す結果ではなく、現状の資料密度では通常の temporal link prediction 評価がまだ成立していないことを示す。seen 2件の生存は、あくまで**評価データ側の健全性確認**として扱う。

---

## 8. THiGER の packaged dataset は raw TSV とは別形式

THiGER の学習側で使う `DatasetDeployment` は、最終的には次の構造を読む。

```text
target_root/
├─ mappings/
│  ├─ nodes_map.parquet
│  ├─ relations_map.parquet
│  ├─ timestamps_map.parquet
│  └─ domains_map.parquet
└─ tensors/
   ├─ train.npy
   ├─ val.npy
   └─ test.npy
```

fact tensor は `[subject_idx, relation_idx, object_idx, timestamp_idx]` の4列を扱える。

参照：
- [`DatasetDeployment`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/datasets/deployment.py)
- [`build_tensors.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/steps/dataset/build_tensors.py)
- [`build_mappings.py`](https://github.com/SonyResearch/HakkenOSS/blob/main/models/packages/hakken-models/hakken_models/steps/dataset/build_mappings.py)

今は `otowa-ankyoscape` 側で Parquet / NumPy まで複製せず、**Hakken の raw ingestion boundary までをこちらの責任範囲**とする。HakkenOSS のパイプライン仕様が変わっても、証拠つき `claims` を正本として再生成できるようにするためである。

---

## 9. 時間順 backtest

未来発見を試すならランダム split を使わない。

`scripts/make_temporal_backtest.py` は、

```text
train : year < train_end
valid : train_end <= year < val_end
test  : val_end <= year
```

と時間順を固定し、未来の辺を coverage のために train へ戻さない。後年にしか現れない entity / relation は cold-start として別集計する。

historical time の `train < 1930 / valid < 1960` では、valid 4件・test 5件が**すべて cold-start**になった。この軸は歴史状態の復元には必要だが、現状のグラフでは未来リンク予測評価に向かない。

discovery/evidence time では test 側に seen fact が2件あるが、三種類の年代方針のどれでも validation に十分な seen fact がない。cutoff scan で `classified-only` の比較的良い候補 `train < 2001 / valid < 2021` を使っても `train=12 / valid=2 / test=8`, `valid_seen=0 / test_seen=2` である。

したがって、現段階で MRR や Hits@K を「未来発見能力」として解釈しない。モデルを本格評価する前に、**同じ実体・同じ relation が複数年代に再登場する資料密度**を増やすことを優先する。

---

## 10. ChatGPT との役割分担

この構成では、ChatGPT は Hakken の出力をそのまま史実へ変換する役ではない。

```text
Markdown・史料メモ
        ↓
ChatGPT: entity / relation / evidence status / source year semantics を抽出
        ↓
証拠つき claims
        ↓
Hakken / THiGER: 未知リンク候補を順位付け
        ↓
ChatGPT: 根拠経路・反証候補・探すべき史料を整理
        ↓
一次史料・地図・地形で人間が確認
```

特に「水窪川と弦巻川の接続」「音羽谷西側流路の成立」「谷端川側との旧河道」などでは、モデルスコアを結論ではなく**調査順位**として使う。

---

## 現在の境界

```mermaid
flowchart LR
    A[Markdown・一次史料メモ] --> B[evidence-aware claims]
    B --> C[静的3列 TSV]
    B --> D[historical-time 4列 TSV]
    B --> E[discovery-time baseline]
    E --> E1[no-page-update]
    E --> E2[classified-only]
    C --> F[Hakken TextKGDataset / KGE]
    D --> G[THiGER raw historical]
    E --> H[THiGER raw discovery]
    E1 --> V[年代感度分析]
    E2 --> V
    G --> I[Hakken dataset preparation]
    H --> I
    I --> J[THiGER]
    B --> K[未解決仮説]
    F --> L[候補リンク]
    J --> L
    L --> M[史料で反証・確認]
```

重要なのは、**モデル出力を史実へ直接昇格させないこと**である。候補リンクは「次にどの史料・地点を調べるか」を決める探索順位として使う。
