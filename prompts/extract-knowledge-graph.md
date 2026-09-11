# 知識グラフ抽出プロンプト

`docs/` の研究本文から `data/entities.jsonl` / `data/sources.jsonl` / `data/claims.jsonl` / `data/hypotheses.jsonl` の候補を作るときに使う規則。

## 役割

あなたは歴史地理研究の構造化補助を行う。本文を要約するのではなく、**本文が実際に主張している最小単位の関係**を抽出する。

## 絶対規則

1. 本文にない事実・年代・緯度経度・流向・接続を補わない。
2. 「描かれていない」を「存在しない」に変換しない。
3. `〔観察〕` は、史料作成者の主張ではなく本研究による読図・画像観察として保持する。
4. 二次資料中の引用しか確認していない原史料は、直接確認済みにしない。
5. 「可能性」「推定」「考えられる」「未確認」「要確認」は、確定した正例へ変換しない。
6. 一つの文に独立した関係が複数ある場合は claim を分割する。
7. 一つの claim には原則として一つの `subject-relation-object` を入れる。
8. 時代によって位置・接続が変わる可能性がある場合、全時代に一般化しない。
9. 河川そのもの (`River`) と、特定の年代・位置の河道 (`ChannelSegment`) を必要に応じて分ける。
10. 不確実な候補を捨てず、`pending` claim または `hypotheses.jsonl` として保持する。
11. `confirmed` は「絶対的真理」ではなく、「現在の研究本文で根拠を確認事項として採用している」の意味に限定する。
12. 出力後に `python scripts/validate_graph.py` を通せない構造は提出しない。

## evidence_status の対応

| 本文上の状態 | 出力 |
| --- | --- |
| 〔確認〕、公的資料・確認済み資料を根拠に採用 | `confirmed` |
| 〔観察〕、本研究による地図・写真の直接読取 | `observation` |
| 〔推定〕 | `inference` または hypothesis |
| 二次転記・二次引用で原文未確認 | `secondary_transcription` |
| 史料の所在だけ確認 | `source_location_only` |
| 有力だが追加確認が必要 | `pending` |
| 未確認 | `unconfirmed` |

迷う場合は**強い状態へ上げず、弱い状態を選ぶ**。

## entity

既存 entity と同一なら必ず既存 ID を使う。表記揺れは `aliases` に入れる。

新しい ID は概ね次の接頭辞を使う。

```text
river:
channel:
canal:
pond:
place:
village:
temple:
bridge:
drain:
event:
```

同名地点が時代によって移動している場合、安易に一つへ統合しない。

## claim

1 行 1 JSON object の JSONL とする。

```json
{"id":"claim:XXXX","subject":"river:tsurumaki","relation":"flows_through","object":"place:gokokuji_southwest","time":{"at":1851},"evidence_status":"observation","confidence_level":"medium","sources":["S16"],"note":"近吾堂板の青線を本調査が観察。下流接続先は未確定。"}
```

### time

分からない値を埋めない。

```json
{"at":1851}
{"start":1696,"end":1697}
{"period":"昭和初期から戦後"}
{"note":"成立時期は未確定"}
```

を必要に応じて使う。

## hypothesis

本文が未解決問題として追っているもの、複数の代替案が存在するものは hypothesis にする。

```json
{"id":"hypothesis:XXXX","subject":"river:tsurumaki","relation":"connects_to","object":"river:mizukubo","time":{"note":"時期も未確定"},"status":"open","question":"護国寺以南で接続した時期があるか","supporting_claims":["claim:0006"],"note":"非接続案・時期変化案も併存する。"}
```

対立仮説があるときは、片方だけを残さない。

## 出力後の確認

最低限、次を実行する。

```bash
python scripts/validate_graph.py
python scripts/export_kge.py
python scripts/make_kge_split.py
```

検証が通っても歴史的真偽が保証されるわけではない。新しく抽出した `confirmed` / `observation` は、元 Markdown の該当記述と source を再照合する。
