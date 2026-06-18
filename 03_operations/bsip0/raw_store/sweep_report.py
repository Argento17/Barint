"""
sweep_report.py — Listing sweep diff for BSIP0.5.

Barcodes discovered on Shufersal yogurt listings vs barcodes in the
run_yogurt_006 BSIP1 corpus -> new_candidates.json + delisted_candidates.json.

REPORT ONLY — nothing is added to any corpus.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "https://www.shufersal.co.il"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}
PAGE_SIZE = 48
MAX_PAGES = 3
FETCH_DELAY = 1.5

CORPUS_DIR = Path(r"C:\Bari\03_operations\bsip1\run_yogurt_006\output")
_VM_CORPUS = Path("/opt/bari/corpus/run_yogurt_006/output")
if not CORPUS_DIR.exists() and _VM_CORPUS.exists():
    CORPUS_DIR = _VM_CORPUS
OUTPUT_DIR = Path(__file__).resolve().parent

# Yogurt search queries mirroring the existing scraper's query plan
SEARCH_QUERIES = [
    "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8",
    "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05d9\u05d5\u05d5\u05e0\u05d9",
    "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05d1\u05d9\u05d5",
    "\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d4",
    "\u05d9\u05d5\u05e4\u05dc\u05d4",
    "\u05d3\u05e0\u05d5\u05e0\u05d4",
    "\u05de\u05d5\u05dc\u05e8",
    "\u05e1\u05e7\u05d9\u05e8",
    "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8 \u05e4\u05e8\u05d5",
]

CATEGORY_URLS = [
    f"{BASE}/online/he/c/A4001?pageSize={PAGE_SIZE}",
    f"{BASE}/online/he/c/A4003?pageSize={PAGE_SIZE}",
]

# Exclude signals (mirror the yogurt scraper)
EXCLUDE_SIGNALS = [
    "\u05de\u05e9\u05e7\u05d4", "\u05e9\u05ea\u05d9\u05d4", "\u05e9\u05ea\u05d9\u05d9\u05d4",
    "drink", "\u05e9\u05d9\u05d9\u05e7", "smoothie", "\u05db\u05e4\u05d9\u05e8", "kefir",
    "\u05d0\u05d9\u05e8\u05d0\u05df", "ayran", "\u05dc\u05d0\u05e1\u05d9", "lassi",
    "\u05d0\u05e7\u05d8\u05d9\u05de\u05dc", "actimel", "\u05d9\u05e7\u05d5\u05dc\u05d8", "yakult",
    "\u05de\u05e2\u05d3\u05df", "\u05de\u05d9\u05dc\u05e7\u05d9", "\u05de\u05d5\u05e1",
    "\u05e4\u05d5\u05d3\u05d9\u05e0\u05d2", "\u05d1\u05e8\u05d5\u05dc\u05d4",
    "\u05e4\u05e0\u05d4 \u05e7\u05d5\u05d8\u05d4",
    "\u05e7\u05d9\u05e0\u05d5\u05d7", "\u05db\u05e4\u05e1\u05d5\u05dc", "\u05d8\u05d1\u05dc\u05d9\u05d5\u05ea",
    "\u05d2\u05dc\u05d9\u05d3\u05d4", "ice cream", "\u05d7\u05de\u05d0\u05d4",
    "\u05e9\u05de\u05e0\u05ea", "\u05d2\u05d1\u05d9\u05e0\u05d4 \u05e6\u05d4\u05d5\u05d1\u05d4",
    "\u05d2\u05d1\u05d9\u05e0\u05d4 \u05dc\u05d1\u05e0\u05d4", "\u05e7\u05d5\u05d8\u05d2",
]

INCLUDE_SIGNALS = [
    "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8", "yogurt", "yoghurt",
    "\u05e1\u05e7\u05d9\u05e8", "skyr",
    "\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9\u05d4", "activia",
    "\u05d1\u05d9\u05d5", "bio",
    "\u05e4\u05e8\u05d5 ", "pro ", "go ",
]


def _get(url: str) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=25, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _is_maintenance(content: bytes | str) -> bool:
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    signals = ["maintenance", "\u05d0\u05ea\u05e8 \u05d1\u05ea\u05d7\u05d6\u05d5\u05e7\u05d4"]
    return len(text) < 5000 and any(s in text.lower() for s in signals)


def _is_excluded(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in EXCLUDE_SIGNALS)


def _looks_like_yogurt(name: str) -> bool:
    nl = name.lower()
    return any(sig.lower() in nl for sig in INCLUDE_SIGNALS)


def _extract_barcode_from_pdp(code: str) -> str | None:
    """Fetch a PDP to extract the barcode from JSON-LD."""
    url = f"{BASE}/online/he/p/{code.lower()}"
    r = _get(url)
    if not r or r.status_code != 200:
        return None
    try:
        soup = BeautifulSoup(r.text, "html.parser")
        for script in soup.find_all("script", type="application/ld+json"):
            if script.string:
                ld = json.loads(script.string)
                if ld.get("@type") == "Product":
                    return ld.get("gtin13", ld.get("sku", ""))
    except Exception:
        pass
    return None


def run_listing_sweep() -> dict:
    """Enumerate Shufersal yogurt listings and return discovered barcodes with metadata."""
    import time

    discovered: dict[str, dict] = {}
    notes: list[str] = []

    def log(msg: str):
        print(msg, flush=True)
        notes.append(msg)

    log("Listing sweep: Shufersal yogurt")
    log("NOTE: Shufersal is CAPTCHA-gated from non-IL IP — results reflect proxy/NAT status.")

    for query in SEARCH_QUERIES:
        for page in range(MAX_PAGES):
            url = (
                f"{BASE}/online/he/search?q={requests.utils.quote(query)}"
                f"&pageSize={PAGE_SIZE}&currentPage={page}"
            )
            r = _get(url)
            if not r or r.status_code != 200 or _is_maintenance(r.content):
                log(f"  BLOCKED or empty: '{query}' page {page}")
                break
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("li", attrs={"data-product-name": True})
            new_page = 0
            for li in items:
                d = li.attrs
                name = d.get("data-product-name", "").strip()
                code = d.get("data-product-code", "").strip()
                if not name or not code:
                    continue
                if d.get("data-food", "false").lower() != "true":
                    continue
                if _is_excluded(name):
                    continue
                if not _looks_like_yogurt(name):
                    continue
                if code not in discovered:
                    discovered[code] = {
                        "code": code,
                        "name": name,
                        "query": query,
                        "page": page,
                        "barcode": None,
                    }
                    new_page += 1
            log(f"  '{query}' page {page}: {len(items)} items, {new_page} new (total {len(discovered)})")
            if new_page == 0:
                break
            time.sleep(FETCH_DELAY)

    for cat_url in CATEGORY_URLS:
        for page in range(MAX_PAGES):
            sep = "&" if "?" in cat_url else "?"
            url = f"{cat_url}{sep}currentPage={page}" if page > 0 else cat_url
            r = _get(url)
            if not r or r.status_code != 200 or _is_maintenance(r.content):
                log(f"  BLOCKED or empty: cat page {page}")
                break
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("li", attrs={"data-product-name": True})
            new_page = 0
            for li in items:
                d = li.attrs
                name = d.get("data-product-name", "").strip()
                code = d.get("data-product-code", "").strip()
                if not name or not code:
                    continue
                if _is_excluded(name):
                    continue
                if not _looks_like_yogurt(name):
                    continue
                if code not in discovered:
                    discovered[code] = {
                        "code": code,
                        "name": name,
                        "query": f"category",
                        "page": page,
                        "barcode": None,
                    }
                    new_page += 1
            log(f"  cat page {page}: {len(items)} items, {new_page} new (total {len(discovered)})")
            if new_page == 0:
                break
            time.sleep(FETCH_DELAY)

    log(f"\nTotal unique product codes discovered: {len(discovered)}")

    # Try to resolve barcodes for a sample of codes (first ~20)
    log("\nResolving barcodes from PDP pages (sample)...")
    sample_codes = list(discovered.keys())[:20]
    resolved = 0
    for code in sample_codes:
        bc = _extract_barcode_from_pdp(code)
        if bc:
            discovered[code]["barcode"] = bc
            resolved += 1
        time.sleep(FETCH_DELAY)
    log(f"  Resolved {resolved}/{len(sample_codes)} barcodes")

    sweep_result = {
        "retailer": "shufersal",
        "category": "yogurt",
        "sweep_ts": __import__("datetime").datetime.now().isoformat(),
        "total_discovered": len(discovered),
        "barcodes_resolved": resolved,
        "products": list(discovered.values()),
        "notes": notes,
    }

    return sweep_result


def load_corpus_barcodes() -> tuple[set[str], dict[str, str]]:
    """Load BSIP1 corpus barcodes. Returns (barcodes_set, barcode_to_name_dict)."""
    barcodes: set[str] = set()
    barcode_to_name: dict[str, str] = {}
    if not CORPUS_DIR.exists():
        return barcodes, barcode_to_name
    for fpath in CORPUS_DIR.iterdir():
        if fpath.suffix != ".json":
            continue
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            bc = data.get("barcode", "")
            if bc:
                barcodes.add(bc)
                barcode_to_name[bc] = data.get("canonical_name_he", "")
        except Exception:
            pass
    return barcodes, barcode_to_name


def diff_sweep(
    sweep_result: dict, corpus_barcodes: set[str], corpus_names: dict[str, str]
) -> dict:
    """Compute new and delisted candidates."""
    discovered_map: dict[str, dict] = {}
    for p in sweep_result.get("products", []):
        bc = p.get("barcode") or p.get("code", "")
        if bc:
            discovered_map[bc] = p

    discovered_barcodes = set(discovered_map.keys())
    new_candidates = discovered_barcodes - corpus_barcodes
    delisted_candidates = corpus_barcodes - discovered_barcodes

    new_list = []
    for bc in sorted(new_candidates):
        info = discovered_map.get(bc, {})
        new_list.append({
            "barcode_or_code": bc,
            "name": info.get("name", ""),
            "barcode_resolved": info.get("barcode"),
        })

    delisted_list = []
    for bc in sorted(delisted_candidates):
        delisted_list.append({
            "barcode": bc,
            "corpus_name": corpus_names.get(bc, ""),
        })

    return {
        "corpus_barcodes": len(corpus_barcodes),
        "listed_barcodes": len(discovered_barcodes),
        "new_candidates": len(new_list),
        "delisted_candidates": len(delisted_list),
        "new_candidates_detail": new_list,
        "delisted_candidates_detail": delisted_list,
    }


def main():
    print("=" * 60)
    print("SWEEP REPORT: Shufersal yogurt listing sweep")
    print("=" * 60)

    # Load corpus
    corpus_barcodes, corpus_names = load_corpus_barcodes()
    print(f"\nBSIP1 corpus ({CORPUS_DIR}): {len(corpus_barcodes)} barcodes")

    # Run listing sweep
    print("\nRunning listing sweep...")
    sweep_result = run_listing_sweep()

    # Compute diff
    print("\nComputing diff...")
    diff = diff_sweep(sweep_result, corpus_barcodes, corpus_names)

    # Print summary
    print(f"\n{'='*60}")
    print(f"CORPUS:   {diff['corpus_barcodes']} barcodes")
    print(f"LISTED:   {diff['listed_barcodes']} barcodes")
    print(f"NEW:      {diff['new_candidates']} products")
    print(f"DELISTED: {diff['delisted_candidates']} products")
    print(f"{'='*60}")

    # Write reports
    sweep_path = OUTPUT_DIR / "sweep_result.json"
    sweep_path.write_text(json.dumps(sweep_result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFull sweep result: {sweep_path}")

    new_path = OUTPUT_DIR / "new_candidates.json"
    new_path.write_text(json.dumps(diff["new_candidates_detail"], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"New candidates: {new_path} ({diff['new_candidates']} products)")

    delisted_path = OUTPUT_DIR / "delisted_candidates.json"
    delisted_path.write_text(json.dumps(diff["delisted_candidates_detail"], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Delisted candidates: {delisted_path} ({diff['delisted_candidates']} products)")

    # Return dict for inspection
    return diff


if __name__ == "__main__":
    main()
