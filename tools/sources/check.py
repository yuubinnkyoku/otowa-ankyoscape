#!/usr/bin/env python3
"""資料ファイル群の整合チェック。

使い方: python3 tools/sources/check.py
- 必須フィールド・語彙（status / verified_by）の検証
- ID と旧番号の重複検出
- INDEX.md が最新か（再生成して比較）
"""
import pathlib, re, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import parse_fm, SRC

STATUS = {"直接確認", "二次転記", "所在のみ"}
VERIFIED = {"human", "ai", "both", "未判定"}
REQUIRED = ["id", "title", "category", "tags", "status", "verified_by"]

def main():
    errors = []
    ids = {}; olds = {}
    for p in sorted(SRC.rglob("*.md")):
        if p.name == "INDEX.md": continue
        fm = parse_fm(p.read_text(encoding="utf-8"))
        rel = str(p.relative_to(SRC))
        for k in REQUIRED:
            if not fm.get(k): errors.append(f"{rel}: 必須フィールド {k} がない")
        if fm.get("id") in ids: errors.append(f"{rel}: ID {fm.get('id')} が {ids[fm['id']]} と重複")
        ids[fm.get("id")] = rel
        if fm.get("status") and fm["status"] not in STATUS: errors.append(f"{rel}: status が語彙外: {fm['status']}")
        if fm.get("verified_by") and fm["verified_by"] not in VERIFIED: errors.append(f"{rel}: verified_by が語彙外: {fm['verified_by']}")
        for o in fm.get("old_ids", []):
            if o in olds:
                prev_rel, prev_series = olds[o]
                # 分割（旧1件→新2件）は、同じ series を持つ場合のみ許す
                if not (prev_series and prev_series == fm.get("series")):
                    errors.append(f"{rel}: 旧番号 {o} が {prev_rel} と重複")
            olds[o] = (rel, fm.get("series"))
    idx = SRC / "INDEX.md"
    before = idx.read_text(encoding="utf-8") if idx.exists() else ""
    subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "build.py")], check=True, capture_output=True)
    after = idx.read_text(encoding="utf-8")
    if before != after: errors.append("INDEX.md が古かったため再生成した（生成物との差分あり）")
    if errors:
        print("NG:"); [print(" -", e) for e in errors]; sys.exit(1)
    print(f"OK: {len(ids)} files, {len(olds)} old-id mappings, INDEX up to date")

if __name__ == "__main__":
    main()
