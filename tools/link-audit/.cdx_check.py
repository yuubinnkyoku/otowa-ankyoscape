"""Check cited URLs against the Wayback Machine CDX API for existing snapshots."""
import sys, time, json, urllib.parse, urllib.request
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
            with urllib.request.urlopen(req, timeout=25) as r:
                body = r.read().decode("utf-8", "replace").strip()
            if body:
                snap = body.split("\n")[0].split()
                return url, "archived", snap[0]
            return url, "unarchived", ""
        except Exception as e:
            last_err = str(e)
            time.sleep(2 * (attempt + 1))
    return url, "error", last_err

def main():
    urls = []
    seen = set()
    for line in open(IN_FILE, encoding="utf-8"):
        u = normalize(line)
        if not u.startswith(("http://", "https://")):
            continue
        if "web.archive.org" in u:
            continue
        if u not in seen:
            seen.add(u)
            urls.append(u)

    print(f"checking {len(urls)} urls", flush=True)
    done = 0
    arch_f = open(ARCHIVED, "a", encoding="utf-8")
    unarch_f = open(UNARCHIVED, "a", encoding="utf-8")
    err_f = open(ERRORS, "a", encoding="utf-8")
    log_f = open(LOG, "a", encoding="utf-8")

    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(check, u): u for u in urls}
        for fut in as_completed(futs):
            url, status, info = fut.result()
            done += 1
            if status == "archived":
                arch_f.write(f"{url}\t{info}\n")
            elif status == "unarchived":
                unarch_f.write(url + "\n")
            else:
                err_f.write(f"{url}\t{info}\n")
            log_f.write(json.dumps({"url": url, "status": status}) + "\n")
            log_f.flush()
            if done % 50 == 0:
                print(f"{done}/{len(urls)}", flush=True)
                arch_f.flush(); unarch_f.flush(); err_f.flush()

    for f in (arch_f, unarch_f, err_f, log_f):
        f.close()
    print("done", flush=True)

if __name__ == "__main__":
    main()
