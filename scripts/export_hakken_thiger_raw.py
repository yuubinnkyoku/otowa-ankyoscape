#!/usr/bin/env python3
"""Export a 4-column temporal graph to HakkenOSS THiGER raw TSV files.

HakkenOSS's ``hakken-models`` dataset preparation pipeline expects two raw
files:

* ``edges.tsv`` with columns
  ``subject_id, subject_domain, relation_type, object_id, object_domain, year, number_of_occurrences``
* ``nodes_corrected.tsv`` with columns
  ``node_id, node_domain, node_name, node_domain_id``

Without ``--input``, this script derives a historical-time graph directly from
``claims`` using ``time.at``. With ``--input``, it converts an already exported
four-column TSV (subject, relation, object, year), which is useful for the
corpus-evidence/discovery timeline produced by ``export_discovery_kge.py``.

The distinction matters: a historical event year answers "when did this state
exist?", while an evidence year answers "when did this relation enter the
currently assembled corpus?". Hakken-style future-discovery backtests should
normally use the latter.
"""

from __future__ import annotations

import argparse
import csv
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
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: each JSONL row must be an object")
            rows.append(row)
    return rows


def load_group(base_name: str) -> list[dict[str, Any]]:
    rows = load_jsonl(ROOT / "data" / f"{base_name}.jsonl")
    shard_dir = ROOT / "data" / f"{base_name}.d"
    if shard_dir.is_dir():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--statuses",
        default="confirmed,observation",
        help="comma-separated evidence statuses to export when deriving from claims",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/kge/hakken/raw-historical",
        help="output directory relative to repository root",
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
        help="ignore relation policy when deriving directly from claims",
    )
    parser.add_argument(
        "--input",
        help=(
            "optional 4-column TSV relative to repository root: "
            "subject, relation, object, year; bypasses claim-date derivation"
        ),
    )
    return parser.parse_args()


def read_temporal_tsv(path: Path) -> Counter[tuple[str, str, str, int]]:
    facts: Counter[tuple[str, str, str, int]] = Counter()
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 4:
                raise ValueError(f"{path}:{line_no}: expected 4 tab-separated columns")
            subject, relation, obj, year_text = parts
            try:
                year = int(year_text)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_no}: invalid integer year {year_text!r}") from exc
            facts[(subject, relation, obj, year)] += 1
    return facts


def main() -> int:
    args = parse_args()
    statuses = {s.strip() for s in args.statuses.split(",") if s.strip()}

    relation_cfg = load_json(ROOT / "ontology" / "relations.json")
    policy_key = "temporal_predictable" if args.relation_policy == "temporal" else "predictable"
    allowed = {
        row["id"]: bool(row.get(policy_key, row.get("predictable", False)))
        for row in relation_cfg["relations"]
    }

    entities = load_group("entities")
    claims = load_group("claims")

    entity_index: dict[str, dict[str, Any]] = {}
    for entity in entities:
        entity_id = entity.get("id")
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("entity id must be a non-empty string")
        if entity_id in entity_index:
            raise ValueError(f"duplicate entity id: {entity_id}")
        entity_index[entity_id] = entity

    skipped_without_exact_year = 0
    skipped_relation_policy = 0

    if args.input:
        input_path = ROOT / args.input
        fact_counts = read_temporal_tsv(input_path)
        source_mode = f"input TSV {input_path.relative_to(ROOT)}"
    else:
        # Count repeated evidence for the exact same time-stamped fact. Hakken's
        # raw schema includes number_of_occurrences; using retained claim count
        # preserves duplicate support without duplicate edge rows.
        fact_counts: Counter[tuple[str, str, str, int]] = Counter()
        for claim in claims:
            if claim.get("evidence_status") not in statuses:
                continue

            relation = claim.get("relation")
            if not isinstance(relation, str):
                raise ValueError(f"claim {claim.get('id', '?')} has invalid relation")
            if not args.include_nonpredictable and not allowed.get(relation, False):
                skipped_relation_policy += 1
                continue

            time = claim.get("time") or {}
            year = time.get("at") if isinstance(time, dict) else None
            # bool is a subclass of int; exclude it explicitly.
            if not isinstance(year, int) or isinstance(year, bool):
                skipped_without_exact_year += 1
                continue

            subject = claim.get("subject")
            obj = claim.get("object")
            if subject not in entity_index:
                raise ValueError(f"claim {claim.get('id', '?')} references unknown subject {subject!r}")
            if obj not in entity_index:
                raise ValueError(f"claim {claim.get('id', '?')} references unknown object {obj!r}")

            fact_counts[(subject, relation, obj, year)] += 1
        source_mode = "claims time.at"

    for subject, relation, obj, _ in fact_counts:
        if subject not in entity_index:
            raise ValueError(f"temporal fact references unknown subject {subject!r}")
        if obj not in entity_index:
            raise ValueError(f"temporal fact references unknown object {obj!r}")
        if relation not in allowed:
            raise ValueError(f"temporal fact references unknown relation {relation!r}")

    used_entity_ids = sorted(
        {entity_id for subject, _, obj, _ in fact_counts for entity_id in (subject, obj)}
    )

    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    edges_path = output_dir / "edges.tsv"
    nodes_path = output_dir / "nodes_corrected.tsv"

    with edges_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "subject_id",
                "subject_domain",
                "relation_type",
                "object_id",
                "object_domain",
                "year",
                "number_of_occurrences",
            ]
        )
        for (subject, relation, obj, year), count in sorted(
            fact_counts.items(), key=lambda item: (item[0][3], item[0][0], item[0][1], item[0][2])
        ):
            subject_entity = entity_index[subject]
            object_entity = entity_index[obj]
            writer.writerow(
                [
                    subject,
                    subject_entity["type"],
                    relation,
                    obj,
                    object_entity["type"],
                    year,
                    count,
                ]
            )

    with nodes_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["node_id", "node_domain", "node_name", "node_domain_id"])
        for entity_id in used_entity_ids:
            entity = entity_index[entity_id]
            domain = entity.get("type")
            label = entity.get("label")
            if not isinstance(domain, str) or not domain:
                raise ValueError(f"entity {entity_id} has invalid type/domain")
            if not isinstance(label, str) or not label:
                raise ValueError(f"entity {entity_id} has invalid label")
            writer.writerow([entity_id, domain, label, domain])

    years = sorted({year for _, _, _, year in fact_counts})
    domains = sorted({str(entity_index[entity_id]["type"]) for entity_id in used_entity_ids})

    print(f"read {len(entities)} entities and {len(claims)} claims")
    print(f"source mode: {source_mode}")
    if not args.input:
        print(f"relation policy: {args.relation_policy} ({policy_key})")
    print(f"wrote {len(fact_counts)} Hakken THiGER edge rows to {edges_path.relative_to(ROOT)}")
    print(f"wrote {len(used_entity_ids)} Hakken THiGER nodes to {nodes_path.relative_to(ROOT)}")
    if years:
        print(f"year range: {years[0]}..{years[-1]} ({len(years)} distinct years)")
    print(f"domains: {', '.join(domains)}")
    if not args.input:
        print(f"skipped retained claims by relation policy: {skipped_relation_policy}")
        print(f"skipped retained claims without exact integer year: {skipped_without_exact_year}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
