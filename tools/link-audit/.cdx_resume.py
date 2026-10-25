"""Resume CDX check: unchecked URLs + retry previous errors (2 workers, gentle)."""
import json, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

IN_FILE = "all_urls.txt"
ARCHIVED = "archived_urls.txt"
UNARCHIVED = "unarchived_urls.txt"
ERRORS = "cdx_errors.txt"
LOG = "cdx_progress.jsonl"

def normalize(u):
    u = u.strip()
    if "#" in u:
        u = u.split("#", 1)[0]
    return u

def check(url):
    api = ("https://web.archive.org/cdx/search/cdx?url="
           + urllib.parse.quote(url, safe="")
           + "&limit=1&fl=timestamp,statuscode")
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(api, headers={
                "User-Agent": "otowa-ankyoscape-link-audit/1.0 (cited-link preservation audit)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace").strip()
            if body:
                snap = body.split("\n")[0].split()
                return url, "archived", snap[0]
            return url, "unarchived", ""
        except Exception as e:
            last_err = str(e)
            time.sleep(3 * (attempt + 1))
    return url, "error", last_err

def main():
    urls, seen = [], set()
    for line in open(IN_FILE, encoding="utf-8"):
        u = normalize(line)
        if not u.startswith(("http://", "https://")):
            continue
        if "web.archive.org" in u:
            continue
        if u not in seen:
            seen.add(u)
            urls.append(u)

    latest = {}
    for line in open(LOG, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        latest[d["url"]] = d["status"]

    todo = [u for u in urls if latest.get(u) in (None, "error")]
    print(f"total {len(urls)}; already ok {len(urls) - len(todo)}; todo {len(todo)}", flush=True)

    results = {}
    done = 0
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(check, u): u for u in todo}
        for fut in as_completed(futs):
            url, status, info = fut.result()
            results[url] = (status, info)
            done += 1
            if done % 50 == 0:
                print(f"{done}/{len(todo)}", flush=True)

    # append new outcomes
    with open(ARCHIVED, "a", encoding="utf-8") as af, \
         open(UNARCHIVED, "a", encoding="utf-8") as uf, \
         open(LOG, "a", encoding="utf-8") as lf:
        for url in todo:
            status, info = results[url]
            if status == "archived":
                af.write(f"{url}\t{info}\n")
            elif status == "unarchived":
                uf.write(url + "\n")
            lf.write(json.dumps({"url": url, "status": status}) + "\n")

    # rebuild errors file from latest status per URL
    for url in todo:
        latest[url] = results[url][0]
    still_err = [u for u in urls if latest.get(u) == "error"]
    err_info = {u: results[u][1] for u in still_err if u in results}
    with open(ERRORS, "w", encoding="utf-8") as ef:
        for u in still_err:
            ef.write(f"{u}\t{err_info.get(u, 'previous error')}\n")

    from collections import Counter
    c = Counter(latest[u] for u in urls)
    print("final:", dict(c), flush=True)

if __name__ == "__main__":
    main()
