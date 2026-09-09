#!/usr/bin/env python3
"""Create deterministic train/validation/test splits for KGE experiments.

The holdout is coverage-aware: an edge is moved out of train only when both
its endpoint entities and its relation still occur in the remaining training
pool. This prevents the first tiny experiment from creating impossible
cold-start validation/test examples by accident.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Triple = tuple[str, str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="experiments/kge/triples.tsv")
    parser.add_argument("--output-dir", default="experiments/kge/split")
    parser.add_argument("--valid-fraction", type=float, default=0.10)
    parser.add_argument("--test-fraction", type=float, default=0.20)
    parser.add_argument("--seed", type=int, default=20260909)
    return parser.parse_args()


def load_triples(path: Path) -> list[Triple]:
    rows: list[Triple] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                raise ValueError(f"{path}:{line_no}: expected 3 TSV columns")
            rows.append((parts[0], parts[1], parts[2]))
    return sorted(set(rows))


def write_triples(path: Path, rows: list[Triple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        for s, r, o in sorted(rows):
            f.write(f"{s}\t{r}\t{o}\n")


def entity_counts(rows: list[Triple]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for s, _, o in rows:
        counts[s] += 1
        counts[o] += 1
    return counts


def relation_counts(rows: list[Triple]) -> Counter[str]:
    return Counter(r for _, r, _ in rows)


def can_hold_out(triple: Triple, entities: Counter[str], relations: Counter[str]) -> bool:
    s, r, o = triple
    if s == o:
        return entities[s] > 2 and relations[r] > 1
    return entities[s] > 1 and entities[o] > 1 and relations[r] > 1


def remove_from_counts(triple: Triple, entities: Counter[str], relations: Counter[str]) -> None:
    s, r, o = triple
    entities[s] -= 1
    entities[o] -= 1
    relations[r] -= 1


def allocate_holdout(selected: list[Triple], desired_valid: int, desired_test: int) -> tuple[list[Triple], list[Triple]]:
    if not selected:
        return [], []
    if desired_valid == 0:
        return [], selected
    if desired_test == 0:
        return selected, []
    if len(selected) == 1:
        # Prefer test for a one-edge holdout, but record the lack of validation.
        return [], selected

    total_requested = desired_valid + desired_test
    valid_count = round(len(selected) * desired_valid / total_requested)
    valid_count = max(1, min(valid_count, len(selected) - 1))
    test_count = len(selected) - valid_count
    return selected[:valid_count], selected[valid_count:valid_count + test_count]


def main() -> int:
    args = parse_args()
    if not (0 <= args.valid_fraction < 1 and 0 <= args.test_fraction < 1):
        raise ValueError("fractions must be in [0, 1)")
    if args.valid_fraction + args.test_fraction >= 1:
        raise ValueError("valid + test fractions must be < 1")

    input_path = ROOT / args.input
    triples = load_triples(input_path)
    if len(triples) < 3:
        raise ValueError("need at least 3 triples to create a split")

    desired_valid = max(1, round(len(triples) * args.valid_fraction)) if args.valid_fraction else 0
    desired_test = max(1, round(len(triples) * args.test_fraction)) if args.test_fraction else 0
    desired_total = desired_valid + desired_test

    rng = random.Random(args.seed)
    candidates = triples.copy()
    rng.shuffle(candidates)

    entities = entity_counts(triples)
    relations = relation_counts(triples)
    train_set = set(triples)
    selected: list[Triple] = []

    for triple in candidates:
        if len(selected) >= desired_total:
            break
        if triple not in train_set:
            continue
        if can_hold_out(triple, entities, relations):
            train_set.remove(triple)
            remove_from_counts(triple, entities, relations)
            selected.append(triple)

    valid, test = allocate_holdout(selected, desired_valid, desired_test)
    train = sorted(train_set)
    out_dir = ROOT / args.output_dir
    write_triples(out_dir / "train.tsv", train)
    write_triples(out_dir / "valid.tsv", valid)
    write_triples(out_dir / "test.tsv", test)

    train_entities = set()
    train_relations = set()
    for s, r, o in train:
        train_entities.update((s, o))
        train_relations.add(r)

    for bucket_name, bucket in (("valid", valid), ("test", test)):
        for s, r, o in bucket:
            if s not in train_entities or o not in train_entities or r not in train_relations:
                raise AssertionError(f"{bucket_name} contains a cold-start triple: {(s, r, o)!r}")

    metadata = {
        "seed": args.seed,
        "input_triples": len(triples),
        "train": len(train),
        "valid": len(valid),
        "test": len(test),
        "requested_valid": desired_valid,
        "requested_test": desired_test,
        "coverage_aware": True,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(metadata, ensure_ascii=False))
    if len(valid) < desired_valid or len(test) < desired_test:
        print("note: holdout size was reduced to preserve entity/relation coverage in train")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
