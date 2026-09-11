#!/usr/bin/env python3
"""Export selected claims to a simple subject-relation-object TSV.

The evidence-rich JSONL remains the source of truth. Base claims and optional
``data/claims.d/*.jsonl`` shards are flattened into a model-agnostic view for
initial ComplEx/DistMult-style experiments.
"""

from __future__ import annotations

import argparse
import json
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
            if not line or line.startswith("#"):
                continue
            rows.append(json.loads(line))
    return rows


def load_claims() -> list[dict]:
    rows = load_jsonl(ROOT / "data" / "claims.jsonl")
    fragment_dir = ROOT / "data" / "claims.d"
    if fragment_dir.is_dir():
        for path in sorted(fragment_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--statuses",
        default="confirmed,observation",
        help="comma-separated evidence statuses to export",
    )
    parser.add_argument(
        "--output",
        default="experiments/kge/triples.tsv",
        help="output path relative to the repository root",
    )
    parser.add_argument(
        "--include-nonpredictable",
        action="store_true",
        help="also export relations marked predictable=false",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    statuses = {x.strip() for x in args.statuses.split(",") if x.strip()}

    relation_config = load_json(ROOT / "ontology" / "relations.json")
    predictable = {
        row["id"]: bool(row.get("predictable", False))
        for row in relation_config["relations"]
    }

    claims = load_claims()
    triples: set[tuple[str, str, str]] = set()
    skipped_timeful_duplicates = 0

    for claim in claims:
        if claim.get("evidence_status") not in statuses:
            continue
        relation = claim["relation"]
        if not args.include_nonpredictable and not predictable.get(relation, False):
            continue
        triple = (claim["subject"], relation, claim["object"])
        if triple in triples and claim.get("time"):
            skipped_timeful_duplicates += 1
        triples.add(triple)

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        for subject, relation, obj in sorted(triples):
            f.write(f"{subject}\t{relation}\t{obj}\n")

    print(f"read {len(claims)} claims")
    print(f"wrote {len(triples)} triples to {output.relative_to(ROOT)}")
    if skipped_timeful_duplicates:
        print(
            "note: multiple time-stamped claims collapsed onto the same base triple; "
            "the first experiment intentionally ignores time"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
