# KGE 実験の現状

2026-09-09 時点の最初の抽出・検証結果。

## 現在の規模

GitHub Actions 上で次を確認した。

- entities: **50**
- sources: **20**
- claims: **44**
- hypotheses: **10**
- `confirmed` / `observation` かつ予測対象 relation に限定した KGE 三つ組: **26**

年代違いで同一の三つ組になる claim は、最初の非時系列実験では一つへ畳んでいる。

## coverage-aware split

`python scripts/make_kge_split.py` の既定設定では、学習データから実体・関係が完全に消えないように既知辺を隠す。

現在の 26 三つ組では、要求した 30% holdout をそのまま作れず、実際には次までしか安全に分割できなかった。

```text
train  23
valid   1
test    2
```

これは失敗ではなく、**現時点のグラフがリンク予測を評価するにはまだ疎すぎる**ことを示す診断結果として扱う。

## ここからの目標

HakkenOSS の KGE を本格的に接続する前に、まず既存 `docs/` から抽出を続ける。

目安：

- claims: 100〜300 以上
- conservative KGE triples: 100 以上
- 各主要 relation について複数の subject / object を持たせる
- test / validation の辺を隠しても、対応する entity と relation が train に十分残る状態にする

量を増やすために未確認情報を `confirmed` へ格上げしてはならない。`pending` / `secondary_transcription` / hypothesis はそのまま残し、必要なら別条件の exploratory export で比較する。

## 再現

```bash
python scripts/validate_graph.py
python scripts/export_kge.py
python scripts/make_kge_split.py
cat experiments/kge/split/metadata.json
```

抽出時の規則は [`prompts/extract-knowledge-graph.md`](../../prompts/extract-knowledge-graph.md) を使う。
