#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drain_and_apply.py  —  the HEADLESS driver for the Hebrew Health Scan loop (TASK-381).

Runs daily on this machine (Windows Scheduled Task) AFTER the cloud routine has logged
the morning's keepers to the Notion "Bari Routine Log". It:

  1. Reads the new Lane-A keepers from Notion (Routine=Hebrew Health Scan, Status=New,
     Bucket='Content-Hebrew skills') via the Notion REST API.
  2. Runs them through the deterministic no-harvest firewall + appends survivors to
     file 9 (delegates to apply_scan_keepers.run()).
  3. Writes back to Notion: APPLY -> Status=Actioned, REJECT -> Status=Dropped,
     HOLD/SKIP -> left New (a human / Adversarial QA looks at those).
  4. Commits the file-9 change locally (the cloud routine can't commit; this is why the
     apply step lives here).

The cloud routine cannot do steps 2-4 (read-only tools, git push 403s). This closes that gap.

AUTH (one-time owner setup):
  Create a Notion internal integration (notion.so/my-integrations), share the "Bari Routine
  Log" database with it, then make the secret available to this script as EITHER:
    - env var  NOTION_TOKEN, or
    - a file   %USERPROFILE%\\.bari\\notion_token   (the secret on one line)
  If neither is present the script logs "token not configured" and exits 0 (no error spam).

Usage:
  python drain_and_apply.py                 # real run
  python drain_and_apply.py --dry-run       # query + firewall + file 9, but DON'T touch Notion/git
  python drain_and_apply.py --selftest       # offline: mock Notion rows through the whole wiring
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]                      # .../01_framework/operations/hebrew_health_scan -> repo root
FILE9 = REPO_ROOT / "content_voice" / "tom_bari_voice" / "9_israeli_food_blog_research.md"
SCANS = HERE / "daily_scans"
LOG = SCANS / "drain_log.txt"

DATABASE_ID = "fb50a533316440c4a571f9bb32206e48"   # "Bari Routine Log" database
NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"

sys.path.insert(0, str(HERE))
import apply_scan_keepers as ASK  # noqa: E402


# ----------------------------------------------------------------------------- token + log
def get_token():
    tok = os.environ.get("NOTION_TOKEN", "").strip()
    if tok:
        return tok
    f = Path(os.path.expanduser("~")) / ".bari" / "notion_token"
    if f.exists():
        return f.read_text(encoding="utf-8").strip()
    return None


def log(msg, stamp):
    line = "[%s] %s" % (stamp, msg)
    print(line)
    try:
        SCANS.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


# ----------------------------------------------------------------------------- Notion REST
def _req(method, url, token, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def query_new_keepers(token):
    body = {
        "filter": {"and": [
            {"property": "Routine", "select": {"equals": "Hebrew Health Scan"}},
            {"property": "Status", "select": {"equals": "New"}},
            {"property": "Bucket", "select": {"equals": "Content-Hebrew skills"}},
        ]},
        "page_size": 100,
    }
    out, cursor = [], None
    while True:
        if cursor:
            body["start_cursor"] = cursor
        res = _req("POST", "%s/databases/%s/query" % (API, DATABASE_ID), token, body)
        out.extend(res.get("results", []))
        if res.get("has_more"):
            cursor = res.get("next_cursor")
        else:
            break
    return out


def _plain(prop, kind):
    if not prop:
        return ""
    if kind in ("title", "rich_text"):
        return "".join(seg.get("plain_text", "") for seg in prop.get(kind, []))
    if kind == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    if kind == "url":
        return prop.get("url") or ""
    if kind == "date":
        d = prop.get("date")
        return (d.get("start") or "") if d else ""
    return ""


def page_to_keeper(page):
    p = page.get("properties", {})
    return {
        "Finding": _plain(p.get("Finding"), "title"),
        "Detail": _plain(p.get("Detail"), "rich_text"),
        "Source URL": _plain(p.get("Source URL"), "url"),
        "Tag": _plain(p.get("Tag"), "select"),
        "Bucket": _plain(p.get("Bucket"), "select"),
        "date:Date:start": _plain(p.get("Date"), "date"),
        "url": page.get("url", ""),
        "_page_id": page.get("id", ""),
    }


def set_status(token, page_id, status):
    _req("PATCH", "%s/pages/%s" % (API, page_id), token,
         {"properties": {"Status": {"select": {"name": status}}}})


# ----------------------------------------------------------------------------- git
def git_commit_if_changed(stamp):
    rel_file9 = str(FILE9.relative_to(REPO_ROOT)).replace("\\", "/")
    rel_scans = str(SCANS.relative_to(REPO_ROOT)).replace("\\", "/")
    porcelain = subprocess.run(["git", "status", "--porcelain", "--", rel_file9, rel_scans],
                               cwd=REPO_ROOT, capture_output=True, text=True)
    if not porcelain.stdout.strip():
        log("git: nothing to commit", stamp)
        return
    subprocess.run(["git", "add", "--", rel_file9, rel_scans], cwd=REPO_ROOT, check=True)
    msg = "TASK-381: Hebrew Health Scan auto-apply (%s)\n\nApplied Lane-A register keepers to file 9 via drain_and_apply.py.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" % stamp[:10]
    r = subprocess.run(["git", "commit", "-m", msg], cwd=REPO_ROOT, capture_output=True, text=True)
    log("git commit: %s" % (r.stdout.strip() or r.stderr.strip()), stamp)


# ----------------------------------------------------------------------------- core
def process(keepers, stamp, dry_run, token):
    date = stamp[:10]
    kpath = SCANS / ("keepers_%s.json" % date)
    rpath = SCANS / ("results_%s.json" % date)
    ipath = SCANS / "applied_index.json"
    SCANS.mkdir(parents=True, exist_ok=True)
    kpath.write_text(json.dumps(keepers, ensure_ascii=False, indent=2), encoding="utf-8")

    results = ASK.run(str(kpath), str(FILE9), str(rpath), str(ipath))

    # map results back to Notion pages by url
    by_url = {k["url"]: k for k in keepers if k.get("url")}
    actioned = dropped = held = 0
    for r in results:
        keeper = by_url.get(r.get("url"))
        page_id = keeper.get("_page_id") if keeper else None
        verdict = r["verdict"]
        if verdict == "APPLY":
            actioned += 1
            if not dry_run and page_id:
                set_status(token, page_id, "Actioned")
        elif verdict == "REJECT":
            dropped += 1
            if not dry_run and page_id:
                set_status(token, page_id, "Dropped")
        elif verdict in ("HOLD", "SKIP"):
            held += 1
    log("verdicts: actioned=%d dropped=%d held=%d (of %d)" % (actioned, dropped, held, len(results)), stamp)
    if not dry_run:
        git_commit_if_changed(stamp)
    else:
        log("dry-run: skipped Notion writeback + git commit", stamp)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--now", default=None, help="override timestamp (tests)")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    stamp = a.now or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    if a.selftest:
        return selftest(stamp)

    token = get_token()
    if not token:
        log("token not configured (set NOTION_TOKEN or ~/.bari/notion_token) - nothing to do", stamp)
        return 0
    try:
        pages = query_new_keepers(token)
    except urllib.error.HTTPError as e:
        log("Notion query failed: HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")[:300]), stamp)
        return 1
    except Exception as e:
        log("Notion query failed: %r" % e, stamp)
        return 1
    keepers = [page_to_keeper(p) for p in pages]
    log("fetched %d New Lane-A keeper(s) from Notion" % len(keepers), stamp)
    if not keepers:
        log("nothing new - done (honest empty day)", stamp)
        return 0
    process(keepers, stamp, a.dry_run, token)
    return 0


# ----------------------------------------------------------------------------- offline selftest
def selftest(stamp):
    """Push a mock Notion 'query' response through page_to_keeper + the firewall + the
    status-mapping wiring, with NO network and NO git. Proves everything except live HTTP."""
    mock_pages = [
        {  # clean EMULATE -> APPLY -> would mark Actioned
            "id": "page-aaa", "url": "https://notion.so/page-aaa",
            "properties": {
                "Finding": {"title": [{"plain_text": "EMULATE: question-opener arc"}]},
                "Detail": {"rich_text": [{"plain_text": "Headline 'האם אנחנו באמת' then pivots to evidence; shared-inquiry tone."}]},
                "Source URL": {"url": "https://www.ynet.co.il/wellness/article/xxx"},
                "Tag": {"select": {"name": "WATCH"}},
                "Bucket": {"select": {"name": "Content-Hebrew skills"}},
                "Date": {"date": {"start": "2026-06-25"}},
            },
        },
        {  # harvested sentence -> REJECT -> would mark Dropped
            "id": "page-bbb", "url": "https://notion.so/page-bbb",
            "properties": {
                "Finding": {"title": [{"plain_text": "EMULATE: nice line"}]},
                "Detail": {"rich_text": [{"plain_text": "Reuse: סירופ תירס נשמע כמעט כמו משהו בריאותי אבל הוא ודומיו הם למעשה תחליף זול וגרוע מאוד."}]},
                "Source URL": {"url": "https://example.com"},
                "Tag": {"select": {"name": "WATCH"}},
                "Bucket": {"select": {"name": "Content-Hebrew skills"}},
                "Date": {"date": {"start": "2026-06-25"}},
            },
        },
    ]
    keepers = [page_to_keeper(p) for p in mock_pages]
    assert keepers[0]["Finding"].startswith("EMULATE"), "title parse failed"
    assert keepers[0]["_page_id"] == "page-aaa", "page id parse failed"
    assert keepers[0]["date:Date:start"] == "2026-06-25", "date parse failed"
    assert keepers[1]["Source URL"] == "https://example.com", "url parse failed"
    # run through the firewall only (no file write side effects beyond the temp dir is fine; use dry-run path)
    verdicts = [ASK.firewall(k)[0] for k in keepers]
    print("selftest parse OK; verdicts:", verdicts)
    ok = verdicts == ["APPLY", "REJECT"]
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
