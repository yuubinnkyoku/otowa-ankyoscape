#!/usr/bin/env python3
"""Validate the evidence-aware knowledge graph seed data.

No third-party packages are required. The validator checks structure and
cross-references only; it cannot determine whether a historical claim is true.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable

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
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: each JSONL row must be an object")
            value["__line__"] = line_no
            rows.append(value)
    return rows


def require_keys(row: dict[str, Any], keys: Iterable[str], path: Path, errors: list[str]) -> None:
    for key in keys:
        if key not in row:
            errors.append(f"{path}:{row.get('__line__', '?')}: missing key {key!r}")


def unique_index(rows: list[dict[str, Any]], path: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for row in rows:
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            errors.append(f"{path}:{row.get('__line__', '?')}: id must be a non-empty string")
            continue
        if row_id in index:
            errors.append(f"{path}:{row.get('__line__', '?')}: duplicate id {row_id!r}")
        else:
            index[row_id] = row
    return index


def validate_time(value: Any, where: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{where}: time must be an object")
        return
    allowed = {"at", "start", "end", "period", "note"}
    unknown = set(value) - allowed
    if unknown:
        errors.append(f"{where}: unknown time keys: {sorted(unknown)}")
    for key in ("at", "start", "end"):
        if key in value and not isinstance(value[key], (int, str)):
            errors.append(f"{where}: time.{key} must be an integer year or string")
    if "start" in value and "end" in value:
        if isinstance(value["start"], int) and isinstance(value["end"], int) and value["start"] > value["end"]:
            errors.append(f"{where}: time.start is later than time.end")


def main() -> int:
    errors: list[str] = []

    entity_ontology = load_json(ROOT / "ontology" / "entities.json")
    relation_ontology = load_json(ROOT / "ontology" / "relations.json")
    evidence_ontology = load_json(ROOT / "ontology" / "evidence.json")

    allowed_entity_types = {x["id"] for x in entity_ontology["entity_types"]}
    allowed_relations = {x["id"] for x in relation_ontology["relations"]}
    allowed_statuses = {x["id"] for x in evidence_ontology["evidence_statuses"]}
    allowed_source_classes = set(evidence_ontology["source_classes"])
    allowed_confidence = {"high", "medium", "low", "unknown"}

    entities_path = ROOT / "data" / "entities.jsonl"
    sources_path = ROOT / "data" / "sources.jsonl"
    claims_path = ROOT / "data" / "claims.jsonl"
    hypotheses_path = ROOT / "data" / "hypotheses.jsonl"

    entities = load_jsonl(entities_path)
    sources = load_jsonl(sources_path)
    claims = load_jsonl(claims_path)
    hypotheses = load_jsonl(hypotheses_path)

    entity_index = unique_index(entities, entities_path, errors)
    source_index = unique_index(sources, sources_path, errors)
    claim_index = unique_index(claims, claims_path, errors)
    unique_index(hypotheses, hypotheses_path, errors)

    for row in entities:
        require_keys(row, ("id", "type", "label"), entities_path, errors)
        if row.get("type") not in allowed_entity_types:
            errors.append(
                f"{entities_path}:{row['__line__']}: unknown entity type {row.get('type')!r}"
            )
        aliases = row.get("aliases", [])
        if not isinstance(aliases, list) or not all(isinstance(x, str) for x in aliases):
            errors.append(f"{entities_path}:{row['__line__']}: aliases must be a list of strings")

    for row in sources:
        require_keys(
            row,
            ("id", "title", "year", "source_class", "url", "primary_source_checked"),
            sources_path,
            errors,
        )
        if row.get("source_class") not in allowed_source_classes:
            errors.append(
                f"{sources_path}:{row['__line__']}: unknown source_class {row.get('source_class')!r}"
            )
        if not isinstance(row.get("primary_source_checked"), bool):
            errors.append(
                f"{sources_path}:{row['__line__']}: primary_source_checked must be boolean"
            )
        if row.get("source_class") == "primary" and row.get("primary_source_checked") is not True:
            errors.append(
                f"{sources_path}:{row['__line__']}: a source classified as primary must be directly checked"
            )

    for row in claims:
        require_keys(
            row,
            ("id", "subject", "relation", "object", "evidence_status", "sources"),
            claims_path,
            errors,
        )
        where = f"{claims_path}:{row['__line__']}"
        if row.get("subject") not in entity_index:
            errors.append(f"{where}: unknown subject entity {row.get('subject')!r}")
        if row.get("object") not in entity_index:
            errors.append(f"{where}: unknown object entity {row.get('object')!r}")
        if row.get("relation") not in allowed_relations:
            errors.append(f"{where}: unknown relation {row.get('relation')!r}")
        if row.get("evidence_status") not in allowed_statuses:
            errors.append(f"{where}: unknown evidence_status {row.get('evidence_status')!r}")
        if row.get("confidence_level", "unknown") not in allowed_confidence:
            errors.append(f"{where}: invalid confidence_level {row.get('confidence_level')!r}")
        validate_time(row.get("time"), where, errors)

        source_ids = row.get("sources")
        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"{where}: sources must be a non-empty list")
        else:
            for source_id in source_ids:
                if source_id not in source_index:
                    errors.append(f"{where}: unknown source {source_id!r}")

        # A secondary transcription must never masquerade as direct primary-source verification.
        if row.get("evidence_status") == "secondary_transcription" and isinstance(source_ids, list):
            for source_id in source_ids:
                source = source_index.get(source_id)
                if source and source.get("primary_source_checked") is True:
                    errors.append(
                        f"{where}: secondary_transcription points to a source marked primary_source_checked=true"
                    )

    for row in hypotheses:
        require_keys(
            row,
            ("id", "subject", "relation", "object", "status", "question", "supporting_claims"),
            hypotheses_path,
            errors,
        )
        where = f"{hypotheses_path}:{row['__line__']}"
        if row.get("subject") not in entity_index:
            errors.append(f"{where}: unknown subject entity {row.get('subject')!r}")
        if row.get("object") not in entity_index:
            errors.append(f"{where}: unknown object entity {row.get('object')!r}")
        if row.get("relation") not in allowed_relations:
            errors.append(f"{where}: unknown relation {row.get('relation')!r}")
        if row.get("status") not in {"open", "supported", "rejected", "resolved"}:
            errors.append(f"{where}: invalid hypothesis status {row.get('status')!r}")
        validate_time(row.get("time"), where, errors)
        supporting = row.get("supporting_claims")
        if not isinstance(supporting, list):
            errors.append(f"{where}: supporting_claims must be a list")
        else:
            for claim_id in supporting:
                if claim_id not in claim_index:
                    errors.append(f"{where}: unknown supporting claim {claim_id!r}")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "OK: "
        f"{len(entities)} entities, {len(sources)} sources, "
        f"{len(claims)} claims, {len(hypotheses)} hypotheses"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
