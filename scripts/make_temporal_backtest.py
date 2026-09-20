#!/usr/bin/env python3
"""Create a strict chronological backtest split from temporal KGE facts.

Unlike ``make_kge_split.py``, this script never moves later facts into the
training set to preserve coverage. That would leak future information. Instead
it reports cold-start facts separately so model quality and coverage can be
interpreted independently.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

Fact = tuple[str, str, str, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="experiments/kge/temporal/all.tsv",
        help="4-column subject/relation/object/year TSV relative to repository root",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/kge/temporal/backtest",
        help="output directory relative to repository root",
    )
    parser.add_argument(
        "--train-end",
        type=int,
        required=True,
        help="exclusive end year for training (train: year < train-end)",
    )
    parser.add_argument(
        "--val-end",
        type=int,
        required=True,
        help="exclusive end year for validation (val: train-end <= year < val-end)",
    )
    return parser.parse_args()


def load_facts(path: Path) -> list[Fact]:
    facts: list[Fact] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for line_no, row in enumerate(reader, 1):
            if not row:
                continue
            if len(row) != 4:
                raise ValueError(f"{path}:{line_no}: expected 4 columns, got {len(row)}")
            subject, relation, obj, year_text = row
            try:
                year = int(year_text)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_no}: year must be integer: {year_text!r}") from exc
            facts.append((subject, relation, obj, year))
    return facts


def write_facts(path: Path, facts: Iterable[Fact]) -> int:
    rows = list(facts)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        for subject, relation, obj, year in rows:
            writer.writerow([subject, relation, obj, year])
    return len(rows)


def vocabulary(facts: Iterable[Fact]) -> tuple[set[str], set[str]]:
    entities: set[str] = set()
    relations: set[str] = set()
    for subject, relation, obj, _ in facts:
        entities.add(subject)
        entities.add(obj)
        relations.add(relation)
    return entities, relations


def partition_seen(
    facts: list[Fact], train_entities: set[str], train_relations: set[str]
) -> tuple[list[Fact], list[Fact], dict[str, int]]:
    seen: list[Fact] = []
    cold: list[Fact] = []
    reasons = {
        "new_subject": 0,
        "new_object": 0,
        "new_relation": 0,
        "any_cold_start": 0,
    }

    for fact in facts:
        subject, relation, obj, _ = fact
        new_subject = subject not in train_entities
        new_object = obj not in train_entities
        new_relation = relation not in train_relations

        if new_subject:
            reasons["new_subject"] += 1
        if new_object:
            reasons["new_object"] += 1
        if new_relation:
            reasons["new_relation"] += 1

        if new_subject or new_object or new_relation:
            cold.append(fact)
            reasons["any_cold_start"] += 1
        else:
            seen.append(fact)

    return seen, cold, reasons


def year_range(facts: list[Fact]) -> list[int] | None:
    if not facts:
        return None
    years = [fact[3] for fact in facts]
    return [min(years), max(years)]


def main() -> int:
    args = parse_args()
    if args.train_end >= args.val_end:
        raise ValueError("--train-end must be earlier than --val-end")

    input_path = ROOT / args.input
    facts = sorted(load_facts(input_path), key=lambda x: (x[3], x[0], x[1], x[2]))
    if not facts:
        raise ValueError("temporal input contains no facts")

    train = [fact for fact in facts if fact[3] < args.train_end]
    valid = [fact for fact in facts if args.train_end <= fact[3] < args.val_end]
    test = [fact for fact in facts if fact[3] >= args.val_end]

    if not train:
        raise ValueError("training partition is empty; choose a later --train-end")

    train_entities, train_relations = vocabulary(train)
    valid_seen, valid_cold, valid_reasons = partition_seen(valid, train_entities, train_relations)
    test_seen, test_cold, test_reasons = partition_seen(test, train_entities, train_relations)

    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    counts = {
        "train": write_facts(output_dir / "train.tsv", train),
        "valid": write_facts(output_dir / "valid.tsv", valid),
        "test": write_facts(output_dir / "test.tsv", test),
        "valid_seen": write_facts(output_dir / "valid_seen.tsv", valid_seen),
        "valid_cold_start": write_facts(output_dir / "valid_cold_start.tsv", valid_cold),
        "test_seen": write_facts(output_dir / "test_seen.tsv", test_seen),
        "test_cold_start": write_facts(output_dir / "test_cold_start.tsv", test_cold),
    }

    all_entities, all_relations = vocabulary(facts)
    metadata = {
        "input": str(input_path.relative_to(ROOT)),
        "train_end_exclusive": args.train_end,
        "val_end_exclusive": args.val_end,
        "input_facts": len(facts),
        "counts": counts,
        "year_ranges": {
            "all": year_range(facts),
            "train": year_range(train),
            "valid": year_range(valid),
            "test": year_range(test),
        },
        "distinct_years": sorted({fact[3] for fact in facts}),
        "vocabulary": {
            "all_entities": len(all_entities),
            "train_entities": len(train_entities),
            "all_relations": len(all_relations),
            "train_relations": len(train_relations),
        },
        "cold_start": {
            "valid": valid_reasons,
            "test": test_reasons,
        },
        "policy": (
            "Strict chronology: later facts are never moved into train to preserve coverage. "
            "Facts with unseen entities/relations are separated for diagnostic reporting."
        ),
    }

    with (output_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
