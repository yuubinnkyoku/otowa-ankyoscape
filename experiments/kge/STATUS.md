# KGE 実験の現状

2026-09-09 時点の抽出・検証結果。

## 現在の規模

GitHub Actions 上で次を確認した。

- entities: **111**
- sources: **40**
- claims: **118**
- hypotheses: **15**
- `confirmed`: **62**
- `observation`: **15**
- `secondary_transcription`: **21**
- `pending`: **20**
- `confirmed` / `observation` かつ `predictable=true` の relation に限定した静的 KGE 三つ組: **50**
- 同条件で `time.at` が整数年の時系列 facts: **31**
- 時系列 facts の年代: **1682〜2016年、15 distinct years**
- Hakken THiGER raw schema に参加する nodes: **35**

当初の 44 claims / 26 triples からはかなり増え、**claims 100件超**という最初の目標は越えた。一方、KGE に安全に使う辺はまだ50件であり、数を増やすために二次転記・未確認情報を正例へ格上げすることはしない。

年代違いで同一の三つ組になる claim は、最初の非時系列実験では一つへ畳んでいる。時系列 export では同一三つ組でも年代を保持する。

## 証拠を増やすだけでは足りない

`python scripts/graph_stats.py` で、予測に使う保守的な三つ組の疎さも確認する。

現在は KGE に参加する55実体のうち、

- degree = 1: **42実体（76.4%）**
- degree <= 2: **47実体**

となっている。

つまり、実体数を増やし続けても「一度しか現れない地点」が増えるだけならリンク予測には効きにくい。今後は、すでにある河川・橋・地区・河道区間へ複数の独立した辺を結び、**同じ実体が異なる史料・年代・関係で繰り返し現れる密度**を高める必要がある。

## coverage-aware split

`python scripts/make_kge_split.py` は、学習データから実体・関係が完全に消えない範囲で既知辺を隠す。

現在の50三つ組では、要求した30% holdoutをそのまま作れず、実際には次までしか安全に分割できなかった。

```text
train  44
valid   2
test    4
```

要求値は `valid=5`, `test=10` だった。まだ評価標本が小さすぎるので、仮に ComplEx / DistMult の評価値が高くても、河川史上の「発見能力」があるとは解釈しない。

## 関係の意味も整理した

辺数を増やす途中で、単に数を稼ぐと意味が崩れる例も出たため修正した。

- 旧初音町の「千川」は、谷端川と別水路が物理的に接続する `connects_to` ではなく、谷端川下流区間であることを表す `part_of` とした。
- 東池袋雨水調整池が東池袋3・4丁目の浸水対策を担う関係は、物理的河道を意味する `flows_through` ではなく `serves_area` とした。

この2関係は初期KGEでは `predictable=false` とし、歴史河道のリンク予測へ誤って混入させない。この修正により、保守的KGE辺は52件から50件へ減った。**件数より意味の整合性を優先した結果**である。

## 年代付き export

`python scripts/export_temporal_kge.py` は、保守的な relation のうち `time.at` が整数年として明示されたものだけを

```text
subject    relation    object    year
```

へ落とす。

現在の出力は **31 facts / 15 distinct years / 1682〜2016年**。整数年がない保守的・予測対象 claim **21件**は除外された。`period` や注記から代表年を推測して埋めることはしない。

この31件は「時系列モデルが学習できる十分な量」という意味ではなく、**年代を捨てずに Hakken 系へ渡せる経路が実際に動いた**という段階である。

## HakkenOSS への接続

### 静的 KGE

HakkenOSS には一般的な `TextKGDataset` があり、`train / val / test` の三つ組TSVを直接読める。このリポジトリには設定例として

```text
experiments/kge/hakken/otowa.yaml
```

を置いた。

したがって静的な最初の実験は、

```text
Markdown
  ↓
evidence-aware claims
  ↓
conservative triples
  ↓
coverage-aware train/val/test
  ↓
HakkenOSS TextKGDataset
  ↓
ComplEx / DistMult
```

まで HakkenOSS 本体を改造せず試せる。

### THiGER

追加調査で、HakkenOSS の `hakken-models` 内に **THiGER 本体のモデル・学習・評価コードが公開されている**ことを確認した。THiGER は `num_timestamps` を持ち、GNN と Transformer で temporal KG を扱う実装になっている。

一方、論文で使われる **THiGERLLM** の完全な同一実装は確認できない。`THiGERLLM` というモデル名はベンチマーク生成コード等に現れるが、`class THiGERLLM` の実装は見つかっていない。LLM を使う `hakken-agents` は別系統として扱う。

詳細は [`docs/HakkenOSS接続.md`](../../docs/HakkenOSS接続.md) に整理した。

### THiGER raw schema

HakkenOSS の dataset preparation が読む raw schema に直接合わせる exporter を追加した。

```bash
python scripts/export_hakken_thiger_raw.py
```

生成物：

```text
experiments/kge/hakken/raw/edges.tsv
experiments/kge/hakken/raw/nodes_corrected.tsv
```

GitHub Actions で、

- **31 edge rows**（+ header）
- **35 nodes**（+ header）
- domain: `Bridge`, `Canal`, `ChannelSegment`, `ConstructionEvent`, `Drain`, `Place`, `River`

を確認した。

これは Hakken の raw ingestion boundary まで接続できたことを意味する。THiGER の `DatasetDeployment` が最終的に読む Parquet mapping / NumPy tensor への packaging は、HakkenOSS 側の dataset preparation と責務を分ける。

## 「未来予測」の次の評価

現在の coverage-aware split は静的リンク予測用であり、未来予測の評価には使わない。

次は年代付き31 factsについて、

```text
過去年代のみ train
次の期間を validation
さらに後年を test
```

とする**厳密な時間順 backtest**を作る。

このとき test にしか現れない entity / relation は単純な誤答とせず、cold-start として別集計する。将来的には、ある時点までの史料だけから候補リンクを順位付けし、後年史料で本当に確認されたかを見る。

## 次に増やすべきもの

次の目安は **conservative triples 100以上**。ただし、単純な件数より密度を優先する。

優先順位は次の通り。

1. 既存の `River` / `ChannelSegment` と複数地点を結ぶ `flows_through`
2. 同じ河川について複数の橋を結ぶ `bridge_over`
3. 同一地点・同一河道を異なる年代の一次史料で再観察する claim
4. 分水・支流について、`branches_from` / `flows_to` / `receives_water_from` を一つの経路として揃える
5. 暗渠化・改修は、河川全体ではなく可能なら対象 `ChannelSegment` を切って年代別に記録する

未確認資料は `pending` / `secondary_transcription` のまま残す。原資料確認が取れた時だけ、対応する claim を根拠付きで更新する。

## 再現

```bash
python scripts/validate_graph.py
python scripts/graph_stats.py
python scripts/collect_tagged_passages.py --summary-only
python scripts/export_kge.py
python scripts/make_kge_split.py
python scripts/export_temporal_kge.py
python scripts/export_hakken_thiger_raw.py
cat experiments/kge/split/metadata.json
```

抽出時の規則は [`prompts/extract-knowledge-graph.md`](../../prompts/extract-knowledge-graph.md) を使う。
