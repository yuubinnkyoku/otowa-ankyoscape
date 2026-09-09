#!/usr/bin/env python3
"""Summarize evidence-aware graph size and KGE sparsity.

The report is diagnostic: it helps decide what to extract next and whether a
link-prediction score would be meaningful. It does not assign truth values.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line and not line.startswith("#"):
                rows.append(json.loads(line))
    return rows


def load_group(name: str) -> list[dict]:
    rows = load_jsonl(ROOT / "data" / f"{name}.jsonl")
    shard_dir = ROOT / "data" / f"{name}.d"
    if shard_dir.is_dir():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entities = load_group("entities")
    sources = load_group("sources")
    claims = load_group("claims")
    hypotheses = load_group("hypotheses")

    relation_cfg = load_json(ROOT / "ontology" / "relations.json")
    predictable = {r["id"] for r in relation_cfg["relations"] if r.get("predictable")}
    conservative_status = {"confirmed", "observation"}

    evidence = Counter(c.get("evidence_status", "missing") for c in claims)
    relations_all = Counter(c.get("relation", "missing") for c in claims)
    relations_conservative: Counter[str] = Counter()
    entity_degree: Counter[str] = Counter()
    triples: set[tuple[str, str, str]] = set()

    for claim in claims:
        if claim.get("evidence_status") not in conservative_status:
            continue
        relation = claim.get("relation")
        if relation not in predictable:
            continue
        triple = (claim["subject"], relation, claim["object"])
        triples.add(triple)

    for subject, relation, obj in triples:
        relations_conservative[relation] += 1
        entity_degree[subject] += 1
        entity_degree[obj] += 1

    participating_entities = set(entity_degree)
    leaf_entities = {e for e, degree in entity_degree.items() if degree == 1}
    low_degree_entities = {e for e, degree in entity_degree.items() if degree <= 2}

    report = {
        "entities": len(entities),
        "sources": len(sources),
        "claims": len(claims),
        "hypotheses": len(hypotheses),
        "evidence_status": dict(evidence.most_common()),
        "relations_all": dict(relations_all.most_common()),
        "conservative_predictable_triples": len(triples),
        "conservative_relations": dict(relations_conservative.most_common()),
        "participating_entities": len(participating_entities),
        "degree_1_entities": len(leaf_entities),
        "degree_le_2_entities": len(low_degree_entities),
        "degree_1_fraction": round(len(leaf_entities) / len(participating_entities), 4)
        if participating_entities
        else 0.0,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(
        f"graph: {report['entities']} entities, {report['sources']} sources, "
        f"{report['claims']} claims, {report['hypotheses']} hypotheses"
    )
    print("evidence:")
    for key, value in evidence.most_common():
        print(f"  {key}: {value}")
    print(f"conservative predictable triples: {len(triples)}")
    print("conservative relations:")
    for key, value in relations_conservative.most_common():
        print(f"  {key}: {value}")
    print(
        "sparsity: "
        f"{len(participating_entities)} participating entities; "
        f"degree=1 {len(leaf_entities)} ({report['degree_1_fraction']:.1%}); "
        f"degree<=2 {len(low_degree_entities)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
