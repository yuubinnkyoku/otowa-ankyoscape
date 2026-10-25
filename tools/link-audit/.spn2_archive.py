"""SPN2 archiving for unarchived cited URLs (Python equivalent of .spn2_archive.ps1).

Keys are read from stdin (two lines: access key, secret key) and kept only in
process memory. Progress is appended to spn2_progress.jsonl so runs can resume.
"""
import sys, time, json, urllib.parse, urllib.request, urllib.error

import os
URLS_FILE = os.environ.get("SPN2_URLS_FILE", "unarchived_urls.txt")
SHARED_PROGRESS = "spn2_progress.jsonl"
PROGRESS = os.environ.get("SPN2_PROGRESS", SHARED_PROGRESS)
RESULTS = "spn2_results.csv"
DELAY_S = float(os.environ.get("SPN2_DELAY_S", "5"))
SHARD = os.environ.get("SPN2_SHARD")  # e.g. "0/2"

def submit(url, auth_header):
    # NOTE: urllib requests through this VM's egress proxy lose the
    # Authorization header (SPN2 replies 401); curl works, so submit via curl.
    import subprocess
    retries = 0
    while True:
        try:
            r = subprocess.run(
                ["curl", "-s", "-m", "60", "-X", "POST", "https://web.archive.org/save/",
                 "-H", f"Authorization: {auth_header}",
                 "-H", "Accept: application/json",
                 "-H", "User-Agent: otowa-ankyoscape-link-audit/1.0",
                 "--data-urlencode", f"url={url}",
                 "--data-urlencode", "if_not_archived_within=30d",
                 "-w", "\n%{http_code}"],
                capture_output=True, text=True, timeout=90)
            out = r.stdout.strip()
            body, _, code = out.rpartition("\n")
            if code == "429" and retries < 3:
                retries += 1
                time.sleep(10 * retries)
                continue
            if code == "200":
                resp = json.loads(body)
                return resp.get("job_id", ""), resp.get("status", "pending")
            return "", f"ERROR:{code}"
        except Exception as e:
            return "", f"ERROR:{type(e).__name__}"

def main():
    access = sys.stdin.readline().strip()
    secret = sys.stdin.readline().strip()
    if not access or not secret:
        print("keys missing on stdin", flush=True)
        sys.exit(1)
    auth_header = f"LOW {access}:{secret}"

    urls = [l.strip() for l in open(URLS_FILE, encoding="utf-8") if l.strip()]

    done_ok = set()
    for src in {SHARED_PROGRESS, PROGRESS}:
        try:
            for line in open(src, encoding="utf-8"):
                line = line.strip()
                if line:
                    d = json.loads(line)
                    if d.get("status") and not d["status"].startswith("ERROR"):
                        done_ok.add(d["url"])
        except FileNotFoundError:
            pass

    todo = [u for u in urls if u not in done_ok]
    if SHARD:
        idx, n = (int(x) for x in SHARD.split("/"))
        todo = todo[idx::n]
    print(f"total {len(urls)}; already submitted {len(urls) - len(todo) if not SHARD else 'shared'}; todo {len(todo)} (shard {SHARD})", flush=True)

    pf = open(PROGRESS, "a", encoding="utf-8")
    for i, url in enumerate(todo, 1):
        job_id, status = submit(url, auth_header)
        pf.write(json.dumps({"url": url, "job_id": job_id, "status": status}) + "\n")
        pf.flush()
        if i % 10 == 0:
            print(f"{i}/{len(todo)} last: {status}", flush=True)
        if i < len(todo):
            time.sleep(DELAY_S)
    pf.close()

    if SHARD or "SPN2_URLS_FILE" in os.environ:
        print("shard done", flush=True)
        return
    # final CSV in the same shape as the .ps1 output (latest entry per URL)
    latest = {}
    for line in open(PROGRESS, encoding="utf-8"):
        line = line.strip()
        if line:
            d = json.loads(line)
            latest[d["url"]] = d
    import csv
    with open(RESULTS, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL", "JobId", "Status"])
        for u in urls:
            d = latest.get(u, {})
            w.writerow([u, d.get("job_id", ""), d.get("status", "")])
    ok = sum(1 for d in latest.values() if d.get("status") and not d["status"].startswith("ERROR"))
    print(f"done; submitted ok: {ok}", flush=True)

if __name__ == "__main__":
    main()
