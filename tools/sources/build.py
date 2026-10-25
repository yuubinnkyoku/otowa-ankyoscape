#!/usr/bin/env python3
"""資料ファイル群（docs/sources/）から出典索引 INDEX.md を生成する。

使い方: python3 tools/sources/build.py
- docs/sources/<category>/*.md の frontmatter を読み、カテゴリ別索引と
  旧番号→新番号の対応表を docs/sources/INDEX.md に書き出す。
- frontmatter は単純な key: value / key: [a, b] 形式のみを対象とする。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "docs" / "sources"
CAT_JA = {"maps": "地図・絵図", "gazetteers": "地誌・行政史料", "books": "書籍・雑誌・メディア",
          "papers": "論文・研究報告・データ", "gov": "行政・公的機関", "org": "企業・団体の公式発表",
          "blogs": "ブログ・個人サイト", "lost-web": "消失サイト保存版"}
CAT_ORDER = ["maps", "gazetteers", "books", "papers", "gov", "org", "blogs", "lost-web"]

def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not mm: continue
        k, v = mm.group(1), mm.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            fm[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
        else:
            fm[k] = v.strip('"')
    return fm

LEGEND = """## 判定記号

- ◎: 複数の流れ・水面がはっきり描かれ、時代比較の基準にできる
- ○: 対象の流れが確認できる
- ▲: 淡い線など、候補はあるが確定できない
- △: 池・谷筋・関連地形など、水系の手がかりは間接的に確認できる
- ×: 対象地域は描かれているが、その流れは確認できない
- —: 対象地域が範囲外、またはその川の存在を前提にできない
- ?: 未確認・未読・判定保留"""

def _sort_year(f):
    y = str(f.get("year_label") or f.get("year") or "")
    m = re.search(r"(\d{3,4})", y)
    if m: return (int(m.group(1)), f["id"])
    if "明治後期" in y: return (1905, f["id"])
    if "大正" in y: return (1920, f["id"])
    return (9999, f["id"])

def _strip(text):
    return re.sub(r"\[([^\]]*)\]\((?!http)[^)]*\.md\)", r"\1", text)

def _memo(f):
    m = re.search(r"読図メモ: (.+)", f.get("_body", ""))
    if not m: return ""
    return _strip(m.group(1).strip())

def _field(body, label):
    m = re.search(label + r": (.+)", body)
    return _strip(m.group(1).strip()) if m else ""

def build_map_list(items):
    maps = [f for f in items if f.get("category") == "maps"]
    by_sec = {}
    for f in maps: by_sec.setdefault(f.get("section", "main"), []).append(f)
    out = ["# 地図一覧（自動生成）", "",
           "このファイルは `tools/sources/build.py` が `docs/sources/maps/` の資料ファイルから自動生成する。**手で編集しない**。地図の追加・判定の変更は資料ファイル側で行い、再生成する。",
           "移行前の手書き一覧と網羅性監査（監査表1〜3）は [地図一覧-監査記録-2026-10-25](地図一覧-監査記録-2026-10-25.md) に凍結保存した。河川別の時系列は各河川の文書（水窪川・弦巻川・谷端川・人参川）で手書き管理する。", "",
           LEGEND, "", "## 年代順一覧", "",
           "| 年代 | 地図 | 水窪川 | 弦巻川 | 谷端川 | 人参川候補 | 読図メモ |",
           "| --- | --- | :---: | :---: | :---: | :---: | --- |"]
    for f in sorted(by_sec.get("main", []), key=_sort_year):
        y = f.get("year_label") or f.get("year") or ""
        r = (f.get("readings") or ["?", "?", "?", "?"]) + ["?", "?", "?", "?"]
        out.append(f"| {y} | [{f['title']}](sources/maps/{f['id']}.md) | {r[0]} | {r[1]} | {r[2]} | {r[3]} | {_memo(f)} |")
    out += ["", "## 未確認の江戸初期地図", "", "| 地図 | おおよその年代 | 確認したい範囲・理由 |", "| --- | --- | --- |"]
    for f in sorted(by_sec.get("candidate", []), key=_sort_year):
        out.append(f"| [{f['title']}](sources/maps/{f['id']}.md) | {f.get('year','')} | {_field(f.get('_body',''), '確認したい範囲・理由')} |")
    out += ["", "## 周辺水路（上水）の図", "", "| 図 | 年代・所在 | 状態・言及箇所 |", "| --- | --- | --- |"]
    for f in sorted(by_sec.get("water", []), key=_sort_year):
        out.append(f"| [{f['title']}](sources/maps/{f['id']}.md) | {_field(f.get('_body',''), '年代・所在（地図一覧の表記）') or f.get('year','')} | {_field(f.get('_body',''), '状態・言及箇所')} |")
    out += ["", "## 境内図・他地域の図など", "", "| 図 | 位置づけ |", "| --- | --- |"]
    for f in sorted(by_sec.get("precinct", []), key=lambda x: x["id"]):
        pos = _field(f.get("_body", ""), "位置づけ（地図一覧の表記）")
        if not pos:
            m = re.search(r"## 位置づけ（地図一覧から移行）\n\n(.+)", f.get("_body", ""))
            pos = _strip(m.group(1).strip()) if m else ""
        out.append(f"| [{f['title']}](sources/maps/{f['id']}.md) | {pos} |")
    out += ["", "## 現代の参照地図", "", "| 地図 | メモ |", "| --- | --- |"]
    for f in sorted(by_sec.get("modern", []), key=lambda x: x["id"]):
        body_lines = [l for l in f.get("_body", "").splitlines() if l.strip() and not l.startswith("#")]
        out.append(f"| [{f['title']}](sources/maps/{f['id']}.md) | {_strip(body_lines[0]) if body_lines else ''} |")
    out.append("")
    return "\n".join(out)

MAPLIST = ROOT / "docs" / "地図一覧.md"

def main():
    items = []
    for p in sorted(SRC.rglob("*.md")):
        if p.name in ("INDEX.md",): continue
        _txt = p.read_text(encoding="utf-8")
        fm = parse_fm(_txt)
        fm["_body"] = _txt
        if not fm.get("id"): continue
        fm["_path"] = str(p.relative_to(SRC))
        items.append(fm)
    items.sort(key=lambda f: f["id"])
    out = ["# 出典索引（自動生成）", "",
           "この索引は `docs/sources/` 以下の資料ファイルから `tools/sources/build.py` で生成したものです。手で編集しないでください。書誌の正は各資料ファイルにあります。", ""]
    for cat in CAT_ORDER:
        sub = [f for f in items if f.get("category") == cat]
        if not sub: continue
        out.append(f"## {CAT_JA.get(cat, cat)}（{len(sub)}件）"); out.append("")
        for f in sub:
            old = ", ".join(f.get("old_ids", [])) or "—"
            st = f.get("status", ""); vb = f.get("verified_by", "")
            out.append(f"- [{f['id']}]({f['_path']}) — {f.get('title','')} ／ 旧番号: {old} ／ {st}（{vb}）")
        out.append("")
    out.append("## 旧番号対応表"); out.append("")
    out.append("| 旧番号 | 新番号 |"); out.append("|---|---|")
    pairs = []
    for f in items:
        for o in f.get("old_ids", []): pairs.append((o, f["id"]))
    for o, n in sorted(pairs): out.append(f"| {o} | {n} |")
    out.append("")
    out.append(f"資料ファイル総数: {len(items)}件 / 旧番号対応: {len(pairs)}件")
    (SRC / "INDEX.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    MAPLIST.write_text(build_map_list(items), encoding="utf-8")
    print(f"INDEX.md generated: {len(items)} items, {len(pairs)} old-id mappings; 地図一覧.md regenerated")

if __name__ == "__main__":
    main()
