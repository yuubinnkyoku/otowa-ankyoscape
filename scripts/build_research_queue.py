#!/usr/bin/env python3
"""Build an actionable research queue from the evidence-aware graph.

The current graph is small enough that the main bottleneck is not model
capacity but evidence coverage. This script turns that bottleneck into concrete
research tasks without inventing new historical facts.

It reports three kinds of targets:

1. temporal-predictable relations that cannot enter the discovery/evidence
   timeline because every cited source currently has an unknown source year;
2. retained relations with zero or only one exact historical observation year,
   where another dated observation would improve temporal density;
3. low-degree core hydrological entities that are still weakly connected in
   the conservative graph.

Only ``confirmed`` and ``observation`` claims are used for these diagnostics.
Pending and secondary-transcription claims remain useful research leads, but
are not treated as positive training evidence here.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


CORE_TYPES = {
    "River",
    "Canal",
    "ChannelSegment",
    "Drain",
    "Pond",
    "Spring",
    "Bridge",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: each JSONL row must be an object")
            rows.append(value)
    return rows


def load_group(name: str) -> list[dict[str, Any]]:
    rows = load_jsonl(ROOT / "data" / f"{name}.jsonl")
    shard_dir = ROOT / "data" / f"{name}.d"
    if shard_dir.is_dir():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="experiments/kge/research-queue.md",
        help="Markdown output path relative to repository root",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=30,
        help="maximum rows per diagnostic table",
    )
    return parser.parse_args()


def is_int_year(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def display_triple(
    triple: tuple[str, str, str], entity_index: dict[str, dict[str, Any]]
) -> str:
    subject, relation, obj = triple
    subject_label = entity_index.get(subject, {}).get("label", subject)
    object_label = entity_index.get(obj, {}).get("label", obj)
    return f"{subject_label} — `{relation}` → {object_label}"


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    args = parse_args()
    if args.max_rows < 1:
        raise ValueError("--max-rows must be >= 1")

    entities = load_group("entities")
    sources = load_group("sources")
    claims = load_group("claims")
    relation_cfg = load_json(ROOT / "ontology" / "relations.json")

    entity_index = {row["id"]: row for row in entities}
    source_index = {row["id"]: row for row in sources}
    temporal_predictable = {
        row["id"]
        for row in relation_cfg["relations"]
        if bool(row.get("temporal_predictable", row.get("predictable", False)))
    }

    retained = [
        claim
        for claim in claims
        if claim.get("evidence_status") in {"confirmed", "observation"}
        and claim.get("relation") in temporal_predictable
    ]

    by_triple: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for claim in retained:
        triple = (claim["subject"], claim["relation"], claim["object"])
        by_triple[triple].append(claim)

    triple_rows: list[dict[str, Any]] = []
    entity_degree: dict[str, set[tuple[str, str, str]]] = defaultdict(set)

    for triple, triple_claims in by_triple.items():
        exact_years: set[int] = set()
        source_ids: set[str] = set()
        dated_source_years: set[int] = set()
        undated_source_ids: set[str] = set()

        for claim in triple_claims:
            time = claim.get("time") or {}
            year = time.get("at") if isinstance(time, dict) else None
            if is_int_year(year):
                exact_years.add(int(year))

            for source_id in claim.get("sources", []):
                if not isinstance(source_id, str):
                    continue
                source_ids.add(source_id)
                source = source_index.get(source_id)
                if source is None:
                    undated_source_ids.add(source_id)
                    continue
                source_year = source.get("year")
                if is_int_year(source_year):
                    dated_source_years.add(int(source_year))
                else:
                    undated_source_ids.add(source_id)

        for entity_id in (triple[0], triple[2]):
            entity_degree[entity_id].add(triple)

        triple_rows.append(
            {
                "triple": triple,
                "claim_count": len(triple_claims),
                "exact_years": sorted(exact_years),
                "source_ids": sorted(source_ids),
                "dated_source_years": sorted(dated_source_years),
                "undated_source_ids": sorted(undated_source_ids),
            }
        )

    blocked_discovery = [row for row in triple_rows if not row["dated_source_years"]]
    blocked_discovery.sort(
        key=lambda row: (
            len(row["undated_source_ids"]),
            display_triple(row["triple"], entity_index),
        )
    )

    reobservation = [row for row in triple_rows if len(row["exact_years"]) <= 1]
    reobservation.sort(
        key=lambda row: (
            len(row["exact_years"]),
            -row["claim_count"],
            display_triple(row["triple"], entity_index),
        )
    )

    low_degree: list[tuple[int, str, str]] = []
    for entity_id, entity in entity_index.items():
        if entity.get("type") not in CORE_TYPES:
            continue
        degree = len(entity_degree.get(entity_id, set()))
        if degree <= 2:
            low_degree.append((degree, str(entity.get("label", entity_id)), entity_id))
    low_degree.sort(key=lambda row: (row[0], row[1], row[2]))

    exact_temporal_triples = sum(1 for row in triple_rows if row["exact_years"])
    repeated_temporal_triples = sum(1 for row in triple_rows if len(row["exact_years"]) >= 2)
    discovery_eligible_triples = sum(1 for row in triple_rows if row["dated_source_years"])

    out: list[str] = []
    out.append("# 研究キュー：時系列知識グラフの密度を上げる")
    out.append("")
    out.append("この文書は `scripts/build_research_queue.py` が証拠付きグラフから生成する診断結果である。")
    out.append("モデルの予測結果ではなく、**次にどの史料・地点を確認するとグラフが強くなるか**を決めるための作業キューとして使う。")
    out.append("")
    out.append("## 現在の診断")
    out.append("")
    out.append(f"- temporal-predictable な保守的 base triples: **{len(triple_rows)}**")
    out.append(f"- historical time が1件以上ある triples: **{exact_temporal_triples}**")
    out.append(f"- historical time が2年代以上ある再観測 triples: **{repeated_temporal_triples}**")
    out.append(f"- discovery/evidence time に入れる triples: **{discovery_eligible_triples}**")
    out.append(f"- source year 不明だけが理由で discovery timeline に入らない triples: **{len(blocked_discovery)}**")
    out.append("")

    out.append("## A. source year を確定すると discovery timeline が増える候補")
    out.append("")
    out.append("ここでは claim 自体は `confirmed` / `observation` だが、引用 source の `year` がすべて未設定の関係を挙げる。")
    out.append("Webページの更新年を推測で入れず、刊行年・掲載年・作成年を資料側で確認できたときだけ更新する。")
    out.append("")
    out.append("| 関係 | 未年代 source | historical time |")
    out.append("|---|---|---|")
    for row in blocked_discovery[: args.max_rows]:
        sources_text = ", ".join(f"`{source_id}`" for source_id in row["undated_source_ids"]) or "—"
        years_text = ", ".join(map(str, row["exact_years"])) or "—"
        triple_text = markdown_escape(display_triple(row["triple"], entity_index))
        out.append(f"| {triple_text} | {sources_text} | {years_text} |")
    if not blocked_discovery:
        out.append("| — | — | — |")
    out.append("")

    out.append("## B. もう1年代の直接観察を探すと効く関係")
    out.append("")
    out.append("historical time が0〜1年代しかない temporal-predictable 関係。")
    out.append("同じ実体・同じ関係を別年代の一次史料で再確認できると、THiGER系の時系列密度改善に直結する。")
    out.append("")
    out.append("| 関係 | 現在の historical time | 現在の evidence years |")
    out.append("|---|---|---|")
    for row in reobservation[: args.max_rows]:
        historical = ", ".join(map(str, row["exact_years"])) or "—"
        evidence = ", ".join(map(str, row["dated_source_years"])) or "—"
        triple_text = markdown_escape(display_triple(row["triple"], entity_index))
        out.append(f"| {triple_text} | {historical} | {evidence} |")
    if not reobservation:
        out.append("| — | — | — |")
    out.append("")

    out.append("## C. conservative graph で degree <= 2 の中核実体")
    out.append("")
    out.append("River / Canal / ChannelSegment / Drain / Pond / Spring / Bridge のうち、予測対象の保守的辺が2本以下の実体。")
    out.append("単発地点を増やすより、これら既存実体へ独立した辺を追加できる史料を優先するとグラフ密度が上がる。")
    out.append("")
    out.append("| degree | 実体 | id |")
    out.append("|---:|---|---|")
    for degree, label, entity_id in low_degree[: args.max_rows]:
        out.append(f"| {degree} | {markdown_escape(label)} | `{entity_id}` |")
    if not low_degree:
        out.append("| — | — | — |")
    out.append("")

    out.append("## 読み方")
    out.append("")
    out.append("A は discovery/evidence time の欠損、B は historical time の疎さ、C は静的グラフの疎さを表す。")
    out.append("一つの史料確認で A と B の両方が改善する場合を最優先とし、確認できなかった場合も `pending` を正例へ格上げしない。")
    out.append("")

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(out), encoding="utf-8")

    print(f"retained temporal-predictable base triples: {len(triple_rows)}")
    print(f"historical-time triples: {exact_temporal_triples}")
    print(f"re-observed at >=2 historical years: {repeated_temporal_triples}")
    print(f"discovery/evidence eligible triples: {discovery_eligible_triples}")
    print(f"blocked by undated sources: {len(blocked_discovery)}")
    print(f"low-degree core entities (degree <= 2): {len(low_degree)}")
    print(f"wrote {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
