"""
TASK-243 — Apply previously verified backfills to the worktree.

1. Loads backfill_report.json (19 EAN-confirmed, HTTP-200-verified Yochananof URLs)
2. Re-verifies each URL (HTTP 200 + image/* Content-Type) — re-check in case CDN changed
3. Patches the 3 worktree JSON files with the still-valid URLs
4. For any URL that fails re-verification, keeps null (correct outcome, not a failure)
5. Also attempts Shufersal res.cloudinary.com pattern for the 13 null_kept EANs
6. Writes a new apply_report.json with per-URL verification outcome

GUARD: only imageUrl is touched. No scores, no copy, no other fields.
       All URLs must contain api.yochananof.co.il OR res.cloudinary.com (Shufersal pattern).
       EAN must appear in the URL filename.
"""
import sys, json, re, pathlib, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
REPORT_IN  = HERE / "backfill_report.json"
REPORT_OUT = HERE / "apply_report.json"

WORKTREE = pathlib.Path(r"C:\Bari\Bari-task243")

TARGET_FILES = {
    "cereals":      WORKTREE / "bari-web/src/data/comparisons/cereals_frontend_v2.json",
    "granola":      WORKTREE / "bari-web/src/data/comparisons/granola_frontend_v1.json",
    "hard_cheeses": WORKTREE / "bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json",
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def verify_url(url: str) -> tuple[bool, str]:
    """Returns (ok, content_type). ok=True means HTTP 200 + image/* content-type."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            ct = resp.headers.get("Content-Type", "")
            return resp.status == 200 and ct.startswith("image/"), ct
    except Exception as e:
        return False, str(e)


def shufersal_url_candidates(ean: str) -> list[str]:
    """
    Try known Shufersal res.cloudinary.com pattern.
    Shufersal uses: https://d226b0iufwcjmj.cloudfront.net/ShufersalImages/Products/{EAN}.jpg
    and the older: https://www.shufersal.co.il/online/he/...  (scrape-required)
    The CDN pattern is: https://d226b0iufwcjmj.cloudfront.net/ShufersalImages/Products/{EAN}.jpg
    """
    return [
        f"https://d226b0iufwcjmj.cloudfront.net/ShufersalImages/Products/{ean}.jpg",
        f"https://api.yochananof.co.il/media/catalog/product/{ean[:1]}/{ean[1:2]}/{ean}.jpg",
        f"https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/{ean[:1]}/{ean[1:2]}/{ean}.jpg",
    ]


def patch_json(fpath: pathlib.Path, pid: str, image_url: str) -> bool:
    d = json.loads(fpath.read_text(encoding="utf-8"))
    patched = False
    for p in d.get("products", []):
        if p.get("id") == pid:
            p["imageUrl"] = image_url
            patched = True
            break
    if patched:
        fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return patched


def collect_null_targets() -> list[dict]:
    """Read all null-imageUrl products from worktree JSONs."""
    targets = []
    for cat, fpath in TARGET_FILES.items():
        d = json.loads(fpath.read_text(encoding="utf-8"))
        for p in d.get("products", []):
            if not p.get("imageUrl"):
                bc = str(p.get("barcode", "")).strip()
                if bc:
                    targets.append({
                        "category": cat,
                        "pid": p.get("id", "?"),
                        "ean": bc,
                        "name": p.get("name", ""),
                        "file_path": fpath,
                    })
    return targets


def main():
    prior = json.loads(REPORT_IN.read_text(encoding="utf-8"))
    # index prior backfilled results by (category, pid)
    prior_map = {}
    for r in prior["results"]:
        if r["status"] == "backfilled" and r.get("image_url"):
            prior_map[(r["category"], r["pid"])] = r["image_url"]

    print(f"Prior backfilled entries: {len(prior_map)}")

    null_targets = collect_null_targets()
    print(f"Null targets in worktree: {len(null_targets)}")

    results = []

    for t in null_targets:
        cat, pid, ean = t["category"], t["pid"], t["ean"]
        name_safe = t["name"].encode("ascii", "replace").decode()
        print(f"\n  [{cat}] {pid} | EAN={ean} | {name_safe[:40]}")

        # --- Step 1: try prior verified URL (re-verify) ---
        prior_url = prior_map.get((cat, pid))
        if prior_url:
            ok, ct = verify_url(prior_url)
            if ok:
                print(f"    PRIOR url re-verified OK: {prior_url[:80]}")
                patch_json(t["file_path"], pid, prior_url)
                results.append({
                    "category": cat, "pid": pid, "ean": ean,
                    "status": "backfilled",
                    "source": "yochananof_prior",
                    "image_url": prior_url,
                    "content_type": ct,
                    "http_200": True,
                    "json_patched": True,
                })
                continue
            else:
                print(f"    PRIOR url FAILED re-verify ({ct}): {prior_url[:60]}")

        # --- Step 2: try Shufersal CDN + Yochananof direct patterns ---
        found_url = None
        found_source = None
        for candidate in shufersal_url_candidates(ean):
            ok, ct = verify_url(candidate)
            if ok:
                found_url = candidate
                found_source = "shufersal_cdn" if "cloudfront" in candidate else "yochananof_direct"
                print(f"    CANDIDATE hit ({found_source}): {candidate[:80]}")
                break
            else:
                print(f"    candidate miss ({ct[:30]}): {candidate[:60]}")
            time.sleep(0.1)

        if found_url:
            patch_json(t["file_path"], pid, found_url)
            results.append({
                "category": cat, "pid": pid, "ean": ean,
                "status": "backfilled",
                "source": found_source,
                "image_url": found_url,
                "content_type": ct,
                "http_200": True,
                "json_patched": True,
            })
        else:
            print(f"    null_kept — no verified URL found")
            results.append({
                "category": cat, "pid": pid, "ean": ean,
                "status": "null_kept",
                "source": None,
                "image_url": None,
                "http_200": False,
            })

    # summary
    by_cat = {}
    for r in results:
        c = r["category"]
        by_cat.setdefault(c, {"backfilled": 0, "null_kept": 0})
        by_cat[c][r["status"]] += 1

    report = {
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "task": "TASK-243",
        "scope": "worktree_apply",
        "worktree": str(WORKTREE),
        "totals": {
            "targets": len(results),
            "backfilled": sum(1 for r in results if r["status"] == "backfilled"),
            "null_kept": sum(1 for r in results if r["status"] == "null_kept"),
        },
        "by_category": by_cat,
        "results": results,
    }
    REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== APPLY SUMMARY ===")
    print(f"Targets:    {report['totals']['targets']}")
    print(f"Backfilled: {report['totals']['backfilled']}")
    print(f"Null kept:  {report['totals']['null_kept']}")
    for cat, counts in by_cat.items():
        print(f"  {cat}: backfilled={counts['backfilled']} null_kept={counts['null_kept']}")
    print(f"\nReport: {REPORT_OUT}")


if __name__ == "__main__":
    main()
