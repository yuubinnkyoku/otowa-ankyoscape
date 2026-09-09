# KGE experiments

このディレクトリは、`data/claims.jsonl` から派生した知識グラフ埋め込み（KGE）実験用データを置く。

まずは以下で三つ組を生成する。

```bash
python scripts/validate_graph.py
python scripts/export_kge.py
```

生成される `triples.tsv` は派生物であり、研究上の正本ではない。出典・年代・証拠状態は `data/claims.jsonl` に保持する。

次の段階では、既知辺を train / validation / test に分割して ComplEx / DistMult で復元性能を測る。十分なデータ量が集まるまでは、未解決問題への予測スコアを史実の確率として解釈しない。
