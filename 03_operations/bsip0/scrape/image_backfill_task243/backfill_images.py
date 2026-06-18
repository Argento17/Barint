"""
TASK-243 — Yochananof image backfill for 32 null imageUrl products
(cereals, granola, hard_cheeses — yogurts already clean).

Strategy: for each EAN, search yochananof.co.il by barcode via Playwright,
extract the first catalog image whose filename embeds that EAN, HTTP-200 verify,
then patch the 3 frontend JSON files in-place.

Guard: ONLY accept images where the EAN appears in the image filename
       (EAN-confirmed match). Non-matching products stay null.
       No OFF. No name-only guessing.
"""
import sys, json, re, pathlib, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

HERE = pathlib.Path(__file__).parent
REPORT_PATH = HERE / "backfill_report.json"

TARGET_FILES = {
    "cereals":      pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v2.json"),
    "granola":      pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\granola_frontend_v1.json"),
    "hard_cheeses": pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v2.json"),
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def close_popup(page):
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK", "סגור"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(400)
                return
        except Exception:
            pass


def decode_yoh_image(src: str) -> str:
    """Unwrap Next.js /_next/image?url= proxy to get the real api.yochananof.co.il URL."""
    if "_next/image" in src:
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(src).query)
        inner = qs.get("url", [None])[0]
        if inner:
            return urllib.parse.unquote(inner)
    return src


def find_ean_image(page, ean: str) -> str | None:
    """Search Yochananof by EAN; return first catalog image URL embedding EAN, or None."""
    url = f"https://yochananof.co.il/category?search={ean}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        print(f"    goto fail ({ean}): {e}")
        return None

    page.wait_for_timeout(2500)
    close_popup(page)

    # scroll to trigger lazy-load
    for _ in range(3):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(600)

    # extract all img srcs (Next.js wraps real URLs in /_next/image?url= proxy)
    raw_srcs = page.evaluate(
        """() => Array.from(document.querySelectorAll('img'))
               .map(i => i.currentSrc || i.src || '')
               .filter(s => s.length > 0)"""
    )

    for raw in raw_srcs:
        real = decode_yoh_image(raw)
        # only catalog images
        if "catalog/product" not in real:
            continue
        fname = real.split("/")[-1].split("?")[0]
        if re.search(r'(?:^|[_])' + re.escape(ean) + r'(?:[_.]|$)', fname):
            return real  # return the real api.yochananof.co.il URL

    return None


def http_200(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception:
        return False


def collect_targets():
    """Return list of dicts: {category, pid, ean, name, file_path}."""
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


def patch_json(fpath: pathlib.Path, pid: str, image_url: str):
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


def main():
    targets = collect_targets()
    print(f"Targets: {len(targets)} null-image products across {len(TARGET_FILES)} categories")

    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1000}, user_agent=UA)

        for i, t in enumerate(targets, 1):
            ean, pid, cat = t["ean"], t["pid"], t["category"]
            name_safe = t["name"].encode("ascii", "replace").decode()
            print(f"  [{i}/{len(targets)}] {cat} | {ean} | {name_safe[:35]}")

            img_url = find_ean_image(page, ean)
            verified = False
            if img_url:
                verified = http_200(img_url)
                if not verified:
                    print(f"    -> found url but HTTP failed: {img_url[:80]}")
                    img_url = None

            status = "backfilled" if (img_url and verified) else "null_kept"
            print(f"    -> {status}" + (f": {img_url[:80]}" if img_url else " (no EAN-confirmed match)"))

            rec = {
                "category": cat,
                "pid": pid,
                "ean": ean,
                "status": status,
                "image_url": img_url,
                "http_200": verified,
            }
            results.append(rec)

            if img_url and verified:
                ok = patch_json(t["file_path"], pid, img_url)
                rec["json_patched"] = ok

            time.sleep(0.3)

        browser.close()

    # summary
    by_cat = {}
    for r in results:
        c = r["category"]
        by_cat.setdefault(c, {"backfilled": 0, "null_kept": 0})
        by_cat[c][r["status"]] += 1

    report = {
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "task": "TASK-243",
        "totals": {
            "targets": len(results),
            "backfilled": sum(1 for r in results if r["status"] == "backfilled"),
            "null_kept": sum(1 for r in results if r["status"] == "null_kept"),
        },
        "by_category": by_cat,
        "results": results,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== SUMMARY ===")
    print(f"Total targets:   {report['totals']['targets']}")
    print(f"Backfilled:      {report['totals']['backfilled']}")
    print(f"Null kept:       {report['totals']['null_kept']}")
    for cat, counts in by_cat.items():
        print(f"  {cat}: backfilled={counts['backfilled']} null_kept={counts['null_kept']}")
    print(f"\nReport: {REPORT_PATH}")


if __name__ == "__main__":
    main()
