#!/usr/bin/env python3
"""Validate the evidence-aware knowledge graph data.

No third-party packages are required. Base JSONL files and optional ``*.d``
fragment directories are loaded together. The validator checks structure and
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
            value["__path__"] = str(path.relative_to(ROOT))
            rows.append(value)
    return rows


def load_group(base_name: str) -> list[dict[str, Any]]:
    """Load data/<name>.jsonl plus data/<name>.d/*.jsonl in filename order."""
    base = ROOT / "data" / f"{base_name}.jsonl"
    rows = load_jsonl(base)
    fragment_dir = ROOT / "data" / f"{base_name}.d"
    if fragment_dir.is_dir():
        for path in sorted(fragment_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def where(row: dict[str, Any]) -> str:
    return f"{row.get('__path__', '?')}:{row.get('__line__', '?')}"


def require_keys(row: dict[str, Any], keys: Iterable[str], errors: list[str]) -> None:
    for key in keys:
        if key not in row:
            errors.append(f"{where(row)}: missing key {key!r}")


def unique_index(rows: list[dict[str, Any]], errors: list[str]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for row in rows:
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            errors.append(f"{where(row)}: id must be a non-empty string")
            continue
        if row_id in index:
            errors.append(
                f"{where(row)}: duplicate id {row_id!r}; first seen at {where(index[row_id])}"
            )
        else:
            index[row_id] = row
    return index


def ontology_ids(
    ontology: dict[str, Any], key: str, errors: list[str]
) -> set[str]:
    """Read an ontology list of objects with unique non-empty ``id`` fields."""
    values = ontology.get(key)
    if not isinstance(values, list):
        errors.append(f"ontology/evidence.json: {key!r} must be a list")
        return set()

    ids: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            errors.append(f"ontology/evidence.json: {key}[{index}] must be an object")
            continue
        value_id = value.get("id")
        if not isinstance(value_id, str) or not value_id:
            errors.append(
                f"ontology/evidence.json: {key}[{index}].id must be a non-empty string"
            )
            continue
        if value_id in ids:
            errors.append(f"ontology/evidence.json: duplicate {key} id {value_id!r}")
            continue
        ids.add(value_id)
    return ids


def validate_time(value: Any, row_where: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{row_where}: time must be an object")
        return
    allowed = {"at", "start", "end", "period", "note"}
    unknown = set(value) - allowed
    if unknown:
        errors.append(f"{row_where}: unknown time keys: {sorted(unknown)}")
    for key in ("at", "start", "end"):
        if key in value and not isinstance(value[key], (int, str)):
            errors.append(f"{row_where}: time.{key} must be an integer year or string")
    if "start" in value and "end" in value:
        if isinstance(value["start"], int) and isinstance(value["end"], int) and value["start"] > value["end"]:
            errors.append(f"{row_where}: time.start is later than time.end")


def validate_source_refs(
    source_ids: Any,
    row_where: str,
    source_index: dict[str, dict[str, Any]],
    errors: list[str],
    *,
    required: bool,
) -> None:
    if source_ids is None and not required:
        return
    if not isinstance(source_ids, list) or (required and not source_ids):
        errors.append(f"{row_where}: sources must be {'a non-empty ' if required else 'a '}list")
        return
    for source_id in source_ids:
        if source_id not in source_index:
            errors.append(f"{row_where}: unknown source {source_id!r}")


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
    allowed_source_year_kinds = ontology_ids(
        evidence_ontology, "source_year_kinds", errors
    )

    entities = load_group("entities")
    sources = load_group("sources")
    claims = load_group("claims")
    hypotheses = load_group("hypotheses")

    entity_index = unique_index(entities, errors)
    source_index = unique_index(sources, errors)
    claim_index = unique_index(claims, errors)
    unique_index(hypotheses, errors)

    for row in entities:
        require_keys(row, ("id", "type", "label"), errors)
        if row.get("type") not in allowed_entity_types:
            errors.append(f"{where(row)}: unknown entity type {row.get('type')!r}")
        aliases = row.get("aliases", [])
        if not isinstance(aliases, list) or not all(isinstance(x, str) for x in aliases):
            errors.append(f"{where(row)}: aliases must be a list of strings")

    for row in sources:
        require_keys(
            row,
            ("id", "title", "year", "source_class", "url", "primary_source_checked"),
            errors,
        )
        row_where = where(row)
        if row.get("source_class") not in allowed_source_classes:
            errors.append(f"{row_where}: unknown source_class {row.get('source_class')!r}")
        if not isinstance(row.get("primary_source_checked"), bool):
            errors.append(f"{row_where}: primary_source_checked must be boolean")
        if row.get("source_class") == "primary" and row.get("primary_source_checked") is not True:
            errors.append(f"{row_where}: a source classified as primary must be directly checked")

        year = row.get("year")
        if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
            errors.append(f"{row_where}: year must be an integer or null")
        year_kind = row.get("year_kind")
        if year_kind is not None and year_kind not in allowed_source_year_kinds:
            errors.append(
                f"{row_where}: invalid year_kind {year_kind!r}; "
                f"expected one of {sorted(allowed_source_year_kinds)}"
            )

    for row in claims:
        require_keys(
            row,
            ("id", "subject", "relation", "object", "evidence_status", "sources"),
            errors,
        )
        row_where = where(row)
        if row.get("subject") not in entity_index:
            errors.append(f"{row_where}: unknown subject entity {row.get('subject')!r}")
        if row.get("object") not in entity_index:
            errors.append(f"{row_where}: unknown object entity {row.get('object')!r}")
        if row.get("relation") not in allowed_relations:
            errors.append(f"{row_where}: unknown relation {row.get('relation')!r}")
        if row.get("evidence_status") not in allowed_statuses:
            errors.append(f"{row_where}: unknown evidence_status {row.get('evidence_status')!r}")
        if row.get("confidence_level", "unknown") not in allowed_confidence:
            errors.append(f"{row_where}: invalid confidence_level {row.get('confidence_level')!r}")
        validate_time(row.get("time"), row_where, errors)

        source_ids = row.get("sources")
        validate_source_refs(source_ids, row_where, source_index, errors, required=True)

        # A secondary transcription must never masquerade as direct primary-source verification.
        if row.get("evidence_status") == "secondary_transcription" and isinstance(source_ids, list):
            for source_id in source_ids:
                source = source_index.get(source_id)
                if source and source.get("source_class") == "primary" and source.get("primary_source_checked") is True:
                    errors.append(
                        f"{row_where}: secondary_transcription points directly to a checked primary source; "
                        "use the secondary source that supplied the transcription instead"
                    )

    for row in hypotheses:
        require_keys(
            row,
            ("id", "subject", "relation", "object", "status", "question", "supporting_claims"),
            errors,
        )
        row_where = where(row)
        if row.get("subject") not in entity_index:
            errors.append(f"{row_where}: unknown subject entity {row.get('subject')!r}")
        if row.get("object") not in entity_index:
            errors.append(f"{row_where}: unknown object entity {row.get('object')!r}")
        if row.get("relation") not in allowed_relations:
            errors.append(f"{row_where}: unknown relation {row.get('relation')!r}")
        if row.get("status") not in {"open", "supported", "rejected", "resolved"}:
            errors.append(f"{row_where}: invalid hypothesis status {row.get('status')!r}")
        validate_time(row.get("time"), row_where, errors)
        supporting = row.get("supporting_claims")
        if not isinstance(supporting, list):
            errors.append(f"{row_where}: supporting_claims must be a list")
        else:
            for claim_id in supporting:
                if claim_id not in claim_index:
                    errors.append(f"{row_where}: unknown supporting claim {claim_id!r}")
        validate_source_refs(row.get("sources"), row_where, source_index, errors, required=False)

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