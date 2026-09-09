# KGE 実験

このディレクトリは `data/claims.jsonl` から再生成できる派生データだけを扱う。

```bash
python scripts/validate_graph.py
python scripts/export_kge.py
python scripts/make_kge_split.py
```

既定の `export_kge.py` は `confirmed` / `observation` のみを対象とし、`predictable=true` の relation だけを書き出す。

`make_kge_split.py` は、validation / test 側にだけ現れる entity・relation を作らない coverage-aware split を行う。現在の規模と実際の分割結果は [STATUS.md](STATUS.md) を参照。

HakkenOSS の ComplEx / DistMult を接続する場合も、ここで作る TSV を入力境界とし、Hakken 側の形式へ変換する。証拠状態・年代・出典を持つ正本は `data/claims.jsonl` であり、TSV を手編集しない。
