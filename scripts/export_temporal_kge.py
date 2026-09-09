#!/usr/bin/env python3
"""Export conservative claims with an explicit integer year as 4-column TSV.

HakkenOSS TextKGDataset treats a four-column dataset as temporal when the
columns are subject, relation, object, date. This exporter deliberately omits
claims whose date is only a period/range/note; it never guesses a year.
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
            if line and not line.startswith("#"):
                rows.append(json.loads(line))
    return rows


def load_claims() -> list[dict]:
    rows = load_jsonl(ROOT / "data" / "claims.jsonl")
    shard_dir = ROOT / "data" / "claims.d"
    if shard_dir.is_dir():
        for path in sorted(shard_dir.glob("*.jsonl")):
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
        default="experiments/kge/temporal/all.tsv",
        help="output path relative to repository root",
    )
    parser.add_argument(
        "--include-nonpredictable",
        action="store_true",
        help="also export relations marked predictable=false",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    statuses = {s.strip() for s in args.statuses.split(",") if s.strip()}
    relation_cfg = load_json(ROOT / "ontology" / "relations.json")
    predictable = {
        row["id"]: bool(row.get("predictable", False))
        for row in relation_cfg["relations"]
    }

    claims = load_claims()
    rows: set[tuple[int, str, str, str]] = set()
    skipped_without_exact_year = 0

    for claim in claims:
        if claim.get("evidence_status") not in statuses:
            continue
        relation = claim["relation"]
        if not args.include_nonpredictable and not predictable.get(relation, False):
            continue
        time = claim.get("time") or {}
        year = time.get("at") if isinstance(time, dict) else None
        # bool is a subclass of int; exclude it explicitly.
        if not isinstance(year, int) or isinstance(year, bool):
            skipped_without_exact_year += 1
            continue
        rows.add((year, claim["subject"], relation, claim["object"]))

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        for year, subject, relation, obj in sorted(rows):
            f.write(f"{subject}\t{relation}\t{obj}\t{year}\n")

    years = sorted({row[0] for row in rows})
    print(f"read {len(claims)} claims")
    print(f"wrote {len(rows)} temporal facts to {output.relative_to(ROOT)}")
    if years:
        print(f"year range: {years[0]}..{years[-1]} ({len(years)} distinct years)")
    print(f"skipped conservative predictable claims without exact integer year: {skipped_without_exact_year}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
