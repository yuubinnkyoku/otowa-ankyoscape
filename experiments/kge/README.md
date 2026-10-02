# KGE 実験

このディレクトリは `data/claims.jsonl` と `data/claims.d/*.jsonl` から再生成できる派生データだけを扱う。

```bash
python scripts/validate_graph.py
python scripts/graph_stats.py
python scripts/export_kge.py
python scripts/make_kge_split.py
```

既定の `export_kge.py` は `confirmed` / `observation` のみを対象とし、`predictable=true` の relation だけを書き出す。

`make_kge_split.py` は、validation / test 側にだけ現れる entity・relation を作らない coverage-aware split を行う。現在の規模と実際の分割結果は [STATUS.md](STATUS.md) を参照。

## HakkenOSS へ渡す

HakkenOSS を最初から fork する必要はない。HakkenOSS の `datasets.TextKGDataset` は、`subject / relation / object` のタブ区切りファイルをそのまま読める。

このリポジトリには、そのための設定例を置く。

```text
experiments/kge/hakken/otowa.yaml
```

HakkenOSS 側で試す場合は、このファイルを

```text
HakkenOSS/models/packages/kge/config/data_repo/otowa.yaml
```

へコピーし、次を設定する。

```bash
export OTOWA_KGE_ROOT=/absolute/path/to/otowa-ankyoscape/experiments/kge/split
```

設定では次の対応を使う。

```yaml
files_dict:
  train: train.tsv
  val: valid.tsv
  test: test.tsv
column_names: ["subject", "relation", "object"]
```

これは HakkenOSS が公開している `TextKGDataset` と、YAGO 等のテキスト知識グラフ設定と同じ入口を使う。したがって**最初の静的な ComplEx / DistMult 実験のために HakkenOSS 本体を改造する必要はない**。

ただし、現在のグラフはまだ小さい。HakkenOSS の既定例にある埋め込み次元512・大量の負例などをそのまま採用するのではなく、小さい埋め込み次元・少ない負例から始める。ここで高い評価値が出ても、validation / test の件数が少ないうちは史料上の発見能力を示したとは解釈しない。

証拠状態・年代・出典を持つ正本は `data/claims.jsonl` / `data/claims.d/` であり、KGE 用 TSV を手編集しない。
