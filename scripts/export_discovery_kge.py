#!/usr/bin/env python3
"""Export a Hakken-style corpus evidence timeline.

``export_temporal_kge.py`` uses the historical validity/event year stored in a
claim's ``time.at``. That answers "when did this state/event occur?" but it is
not the same axis as Hakken's "when did this relation enter the literature?".

This exporter instead dates each retained relation by the earliest integer
``year`` among its cited source records. If the same base triple appears in
multiple retained claims, the earliest known source year in *this repository's
corpus* is used. This is deliberately called a corpus evidence year, not the
true first historical discovery date.

Sources may optionally carry ``year_kind`` (for example ``publication`` or
``page_update``). ``--exclude-year-kinds`` makes it possible to test how much a
backtest depends on weak artifact dates such as website update years without
discarding those dates from the evidence catalogue itself.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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
        "--statuses",
        default="confirmed,observation",
        help="comma-separated evidence statuses to export",
    )
    parser.add_argument(
        "--relation-policy",
        choices=("temporal", "static"),
        default="temporal",
        help="temporal uses temporal_predictable; static uses predictable",
    )
    parser.add_argument(
        "--include-nonpredictable",
        action="store_true",
        help="ignore relation policy and export all retained relations",
    )
    parser.add_argument(
        "--exclude-year-kinds",
        default="",
        help=(
            "comma-separated source year_kind values to ignore, e.g. page_update; "
            "sources without year_kind remain eligible for backward compatibility"
        ),
    )
    parser.add_argument(
        "--output",
        default="experiments/kge/discovery/all.tsv",
        help="output path relative to repository root",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    statuses = {s.strip() for s in args.statuses.split(",") if s.strip()}
    excluded_year_kinds = {
        value.strip() for value in args.exclude_year_kinds.split(",") if value.strip()
    }

    relation_cfg = load_json(ROOT / "ontology" / "relations.json")
    policy_key = "temporal_predictable" if args.relation_policy == "temporal" else "predictable"
    allowed = {
        row["id"]: bool(row.get(policy_key, row.get("predictable", False)))
        for row in relation_cfg["relations"]
    }

    sources = load_group("sources")
    claims = load_group("claims")
    source_years: dict[str, tuple[int | None, str | None]] = {}
    source_year_kind_counts: Counter[str] = Counter()
    for source in sources:
        source_id = source.get("id")
        if not isinstance(source_id, str):
            raise ValueError("source id must be a string")
        year = source.get("year")
        year_value = year if isinstance(year, int) and not isinstance(year, bool) else None
        year_kind = source.get("year_kind")
        if year_kind is not None and not isinstance(year_kind, str):
            raise ValueError(f"source {source_id!r} year_kind must be a string when present")
        source_years[source_id] = (year_value, year_kind)
        if year_value is not None:
            source_year_kind_counts[year_kind or "unspecified"] += 1

    first_evidence: dict[tuple[str, str, str], int] = {}
    skipped_relation_policy = 0
    skipped_without_dated_source = 0
    excluded_source_refs = 0

    for claim in claims:
        if claim.get("evidence_status") not in statuses:
            continue

        relation = claim.get("relation")
        if not isinstance(relation, str):
            raise ValueError(f"claim {claim.get('id', '?')} has invalid relation")
        if not args.include_nonpredictable and not allowed.get(relation, False):
            skipped_relation_policy += 1
            continue

        cited_years: list[int] = []
        for source_id in claim.get("sources", []):
            if source_id not in source_years:
                continue
            year, year_kind = source_years[source_id]
            if year is None:
                continue
            if year_kind in excluded_year_kinds:
                excluded_source_refs += 1
                continue
            cited_years.append(year)

        if not cited_years:
            skipped_without_dated_source += 1
            continue

        triple = (claim["subject"], relation, claim["object"])
        year = min(cited_years)
        previous = first_evidence.get(triple)
        if previous is None or year < previous:
            first_evidence[triple] = year

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        for (subject, relation, obj), year in sorted(
            first_evidence.items(), key=lambda item: (item[1], item[0][0], item[0][1], item[0][2])
        ):
            f.write(f"{subject}\t{relation}\t{obj}\t{year}\n")

    years = sorted(set(first_evidence.values()))
    print(f"read {len(sources)} sources and {len(claims)} claims")
    print(f"relation policy: {args.relation_policy} ({policy_key})")
    if excluded_year_kinds:
        print(f"excluded source year kinds: {', '.join(sorted(excluded_year_kinds))}")
    else:
        print("excluded source year kinds: none")
    print("dated source year kinds:")
    for kind, count in sorted(source_year_kind_counts.items()):
        print(f"  {kind}: {count}")
    print(f"wrote {len(first_evidence)} corpus-first evidence facts to {output.relative_to(ROOT)}")
    if years:
        print(f"evidence-year range: {years[0]}..{years[-1]} ({len(years)} distinct years)")
    print(f"skipped retained claims by relation policy: {skipped_relation_policy}")
    print(f"skipped retained claims without an eligible dated cited source: {skipped_without_dated_source}")
    if excluded_year_kinds:
        print(f"source references ignored by year-kind filter: {excluded_source_refs}")
    print(
        "note: year means earliest eligible dated source currently linked in this repository, "
        "not a proven first discovery date"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
