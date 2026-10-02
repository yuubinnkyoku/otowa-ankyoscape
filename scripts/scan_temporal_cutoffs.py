#!/usr/bin/env python3
"""Scan chronological split boundaries and report seen/cold-start coverage.

This is a diagnostic, not a train/test splitter. It searches pairs of year
boundaries from the observed temporal facts and ranks them by how many future
facts can actually be evaluated without unseen entities or relations.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Fact = tuple[str, str, str, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="experiments/kge/temporal/all.tsv",
        help="4-column subject/relation/object/year TSV relative to repository root",
    )
    parser.add_argument("--top", type=int, default=12, help="number of candidate splits to print")
    parser.add_argument(
        "--output",
        default="experiments/kge/temporal/cutoff-scan.json",
        help="JSON result path relative to repository root",
    )
    return parser.parse_args()


def load_facts(path: Path) -> list[Fact]:
    rows: list[Fact] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for line_no, row in enumerate(reader, 1):
            if len(row) != 4:
                raise ValueError(f"{path}:{line_no}: expected 4 columns")
            subject, relation, obj, year_text = row
            rows.append((subject, relation, obj, int(year_text)))
    return rows


def vocab(facts: list[Fact]) -> tuple[set[str], set[str]]:
    entities: set[str] = set()
    relations: set[str] = set()
    for subject, relation, obj, _ in facts:
        entities.add(subject)
        entities.add(obj)
        relations.add(relation)
    return entities, relations


def seen_count(facts: list[Fact], entities: set[str], relations: set[str]) -> int:
    return sum(
        1
        for subject, relation, obj, _ in facts
        if subject in entities and obj in entities and relation in relations
    )


def main() -> int:
    args = parse_args()
    facts = sorted(load_facts(ROOT / args.input), key=lambda x: (x[3], x[0], x[1], x[2]))
    if not facts:
        raise ValueError("no temporal facts")

    years = sorted({fact[3] for fact in facts})
    # Boundaries are observed years after the first. A fact exactly at a
    # boundary belongs to the later partition, matching make_temporal_backtest.py.
    boundaries = years[1:]
    candidates: list[dict[str, object]] = []

    for i, train_end in enumerate(boundaries):
        train = [fact for fact in facts if fact[3] < train_end]
        if not train:
            continue
        train_entities, train_relations = vocab(train)

        for val_end in boundaries[i + 1 :]:
            valid = [fact for fact in facts if train_end <= fact[3] < val_end]
            test = [fact for fact in facts if fact[3] >= val_end]
            if not valid or not test:
                continue

            valid_seen = seen_count(valid, train_entities, train_relations)
            test_seen = seen_count(test, train_entities, train_relations)
            future_total = len(valid) + len(test)
            future_seen = valid_seen + test_seen

            candidates.append(
                {
                    "train_end_exclusive": train_end,
                    "val_end_exclusive": val_end,
                    "train": len(train),
                    "valid": len(valid),
                    "test": len(test),
                    "valid_seen": valid_seen,
                    "test_seen": test_seen,
                    "future_seen": future_seen,
                    "future_total": future_total,
                    "future_seen_fraction": round(future_seen / future_total, 4),
                    "train_entities": len(train_entities),
                    "train_relations": len(train_relations),
                }
            )

    # Prefer splits that retain evaluable facts on both future partitions,
    # then more total seen facts, then a larger training graph.
    candidates.sort(
        key=lambda row: (
            int(row["valid_seen"] > 0) + int(row["test_seen"] > 0),
            int(row["future_seen"]),
            float(row["future_seen_fraction"]),
            int(row["train"]),
        ),
        reverse=True,
    )

    top = candidates[: max(args.top, 0)]
    result = {
        "input_facts": len(facts),
        "distinct_years": years,
        "candidate_count": len(candidates),
        "top_candidates": top,
        "interpretation": (
            "A split is suitable for ordinary temporal link-prediction evaluation only if "
            "valid_seen and test_seen are non-zero. Cold-start facts remain historically useful "
            "but need a separate evaluation protocol."
        ),
    }

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
