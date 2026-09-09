#!/usr/bin/env python3
"""Collect evidence-tagged passages from the research Markdown.

This does not turn prose into historical facts. It creates a reproducible queue
of passages containing markers such as ``〔確認〕`` or ``〔観察〕`` so that a
human/LLM extraction pass can review them against the graph ontology.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TAG_RE = re.compile(r"〔([^〕\n]{1,40})〕")
DEFAULT_EXCLUDES = {
    "分割前README全文.md",
    "知識グラフ実験.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        help="optional JSONL output path relative to repository root",
    )
    parser.add_argument(
        "--include-archive",
        action="store_true",
        help="include docs/分割前README全文.md",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="print counts only and do not emit JSONL to stdout",
    )
    return parser.parse_args()


def paragraphs(lines: list[str]):
    start: int | None = None
    buf: list[str] = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = i
            buf.append(line.rstrip("\n"))
            continue
        if buf:
            yield start or i, i - 1, "\n".join(buf)
            start, buf = None, []
    if buf:
        yield start or len(lines), len(lines), "\n".join(buf)


def collect(include_archive: bool) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        if path.name in DEFAULT_EXCLUDES and not (
            include_archive and path.name == "分割前README全文.md"
        ):
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for start, end, text in paragraphs(lines):
            markers = sorted(set(TAG_RE.findall(text)))
            if not markers:
                continue
            rows.append(
                {
                    "path": str(Path("docs") / rel),
                    "line_start": start,
                    "line_end": end,
                    "markers": markers,
                    "text": text,
                }
            )
    return rows


def main() -> int:
    args = parse_args()
    rows = collect(args.include_archive)
    marker_counts: Counter[str] = Counter()
    file_counts: Counter[str] = Counter()
    for row in rows:
        marker_counts.update(row["markers"])
        file_counts[row["path"]] += 1

    print(f"tagged passages: {len(rows)}")
    print("markers:")
    for marker, count in marker_counts.most_common():
        print(f"  {marker}: {count}")
    print("top files:")
    for path, count in file_counts.most_common(10):
        print(f"  {path}: {count}")

    if args.output:
        output = ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} candidates to {output.relative_to(ROOT)}")
    elif not args.summary_only:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
