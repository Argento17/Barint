"""
replay_parse.py — Offline BSIP0 extraction from stored raw pages.

Runs the existing yogurt-parser logic (shared bsip0_nutrition) against stored
raw pages with zero network access. Proves replay: parsed-from-store output
must match the BSIP1 run_yogurt_006 corpus fields.

Usage:
  python replay_parse.py [--fixtures] [--corpus-dir DIR]

  --fixtures:  Load the 222 frozen-veg fixtures into the store and parse them
               (proof-of-concept for offline replay).
  --corpus-dir: Path to BSIP1 corpus for match checking. Default:
                ../bsip1/run_yogurt_006/output
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STORE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STORE_DIR))

# Shared BSIP0 nutrition parser (same one the yogurt scraper uses)
_SHARED_DIR = STORE_DIR.parent / "scrape" / "_shared"
sys.path.insert(0, str(_SHARED_DIR))
from bsip0_nutrition import parse_nutrition_list, extract_nutrition_raw, nutrition_implausible  # noqa: E402

from store import store_page, latest_content, manifest_entries, all_barcodes  # noqa: E402


FROZEN_VEG_FIXTURES = Path(
    r"C:\Bari\03_operations\bsip0\scrape\shufersal_frozen_vegetables"
)
# VM alternate path
_VM_FIXTURES = Path("/opt/bari/fixtures/shufersal_frozen_vegetables")
if not FROZEN_VEG_FIXTURES.exists() and _VM_FIXTURES.exists():
    FROZEN_VEG_FIXTURES = _VM_FIXTURES

CORPUS_DIR = Path(
    r"C:\Bari\02_products\frozen_vegetables\bsip1_outputs"
)

RETRY_BARCODES = [
    "7290008316037",
    "7290000364209",
    "7290011876708",
    "7290018755808",
    "7290018755815",
    "7290113763043",
    "7290113763128",
    "7290114312479",
    "7290116743486",
    "7290116936604",
    "7290001594568",
    "7290001594575",
    "7290001594858",
    "7290001594865",
    "7290019398233",
]


def _parse_product_from_html(
    html: str, code: str, source_url: str = ""
) -> dict | None:
    """Parse BSIP0-shaped dict from stored HTML. Mirrors existing scraper logic."""
    soup = BeautifulSoup(html, "html.parser")

    ld_name, ld_sku, ld_gtin, ld_images = "", "", "", []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                ld_name = ld.get("name", "")
                ld_sku = ld.get("sku", "")
                ld_gtin = ld.get("gtin13", ld.get("gtin", ""))
                ld_images = ld.get("image", [])
                if isinstance(ld_images, str):
                    ld_images = [ld_images]
                break
        except Exception:
            pass

    nutr_raw = parse_nutrition_list(soup)
    nutr_src = extract_nutrition_raw(soup)

    ingredients_raw = ""
    ingr_label = soup.find(string=re.compile(r"\u05e8\u05db\u05d9\u05d1"))
    if ingr_label:
        parent = ingr_label.find_parent()
        container = parent.find_parent() if parent else None
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"\u05e8\u05db\u05d9\u05d1[\u05d9\u05dd:]*\s*(.*)", full_text, re.DOTALL)
            if m:
                ingredients_raw = m.group(1).strip()[:1000]
    if not ingredients_raw:
        for section in soup.find_all("li"):
            text = section.get_text(separator=" ", strip=True)
            m = re.search(r"\u05e8\u05db\u05d9\u05d1[\u05d9\u05dd:]*\s+(.{30,})", text)
            if m:
                ingredients_raw = m.group(1)[:1000]
                break
    # Trim trailing nutrition table text
    _NUTR_MARKER = "\u05e2\u05e8\u05db\u05d9\u05dd \u05ea\u05d6\u05d5\u05e0\u05ea\u05d9\u05d9\u05dd"
    if _NUTR_MARKER in ingredients_raw:
        ingredients_raw = ingredients_raw.split(_NUTR_MARKER)[0].strip()
    _NUTR_MARKER2 = "\u05de\u05d0\u05e4\u05d9\u05d9\u05e0\u05d9\u05dd \u05e0\u05d5\u05e1\u05e4\u05d9\u05dd"
    if _NUTR_MARKER2 in ingredients_raw:
        ingredients_raw = ingredients_raw.split(_NUTR_MARKER2)[0].strip()

    claims_raw = ""
    claim_keywords = [
        "\u05dc\u05dc\u05d0 \u05e1\u05d5\u05db\u05e8",
        "\u05d3\u05dc \u05e1\u05d5\u05db\u05e8",
        "\u05e4\u05e8\u05d5\u05d1\u05d9\u05d5\u05d8\u05d9",
        "\u05d7\u05dc\u05d1\u05d5\u05df",
        "\u05e2\u05e9\u05d9\u05e8 \u05d1",
        "\u05dc\u05dc\u05d0 \u05ea\u05d5\u05e1\u05e4\u05ea",
    ]
    for section in soup.find_all(["li", "div", "p"]):
        text = section.get_text(separator=" ", strip=True)
        if any(kw in text for kw in claim_keywords):
            claims_raw += " " + text[:200]

    name = ld_name or ""
    barcode = ld_gtin or ld_sku or code

    result = {
        "retailer_id": "shufersal",
        "retailer_name": "\u05e9\u05d5\u05e4\u05e8\u05e1\u05dc",
        "source_url": source_url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": "",
        "barcode": barcode,
        "category_raw": "",
        "subcategory_raw": "replay_parse",
        "nutrition": {
            "energy_kcal_raw": nutr_raw.get("energy", ""),
            "protein_raw": nutr_raw.get("protein", ""),
            "carbs_raw": nutr_raw.get("carbs", ""),
            "fat_raw": nutr_raw.get("fat", ""),
            "fiber_raw": nutr_raw.get("fiber", ""),
            "sodium_raw": nutr_raw.get("sodium", ""),
            "sugar_raw": nutr_raw.get("sugar", ""),
            "saturated_fat_raw": nutr_raw.get("saturated_fat", ""),
        },
        "nutrition_raw_source": nutr_src,
        "ingredients_raw": ingredients_raw,
        "ingredients_language": "he" if ingredients_raw and any("\u05d0" <= c <= "\u05ea" for c in ingredients_raw) else "",
        "claims_raw": claims_raw.strip()[:400],
        "image_urls": [u for u in ld_images[:3] if u],
        "extraction_method": "replay_parse",
        "extraction_confidence": "high" if (nutr_raw and ingredients_raw) else ("medium" if nutr_raw else "low"),
        "acquisition_query": "replay",
        "acquisition_tier": "replay",
    }
    return result


def load_fixtures_into_store() -> list[str]:
    """Load the 222 frozen-veg HTML fixtures into the raw store for replay testing."""
    notes: list[str] = []
    pdir = FROZEN_VEG_FIXTURES / "product_pages"
    if not pdir.exists():
        notes.append(f"Fixtures not found at {pdir}")
        return notes

    count = 0
    for fpath in sorted(pdir.iterdir()):
        if fpath.suffix != ".html":
            continue
        code = fpath.stem.replace("P_", "")
        content = fpath.read_bytes()
        store_page(
            content=content,
            retailer="shufersal",
            category="frozen_vegetables",
            page_id=code,
            url=f"file://{fpath}",
            barcode_hint=code,
            http_status=200,
            fetch_engine="fixture",
        )
        count += 1
    notes.append(f"Loaded {count} frozen-veg fixtures into raw_store")
    return notes


def run_replay_parse(
    retailer: str, category: str
) -> tuple[list[dict], list[str]]:
    """Parse all stored pages for a retailer/category offline. Returns (products, notes)."""
    notes: list[str] = []
    products: list[dict] = []
    entries = manifest_entries(retailer, category)

    if not entries:
        notes.append(f"  No manifest entries for {retailer}/{category}")
        return products, notes

    # Deduplicate: keep only latest per page_id
    by_id: dict[str, dict] = {}
    for e in entries:
        pid = e.get("page_id", "")
        if pid and (pid not in by_id or e["fetch_ts"] > by_id[pid]["fetch_ts"]):
            by_id[pid] = e

    notes.append(f"  Parsing {len(by_id)} unique pages from store...")
    for page_id, entry in by_id.items():
        fpath = STORE_DIR / entry["filename"]
        if not fpath.exists():
            notes.append(f"  MISSING file: {entry['filename']}")
            continue
        html = fpath.read_text(encoding="utf-8")
        prod = _parse_product_from_html(html, page_id, entry.get("url", ""))
        if prod:
            products.append(prod)
        else:
            notes.append(f"  PARSE FAIL: {page_id}")

    notes.append(f"  Parsed {len(products)} products from {len(by_id)} pages")
    return products, notes


def load_bsip1_corpus(corpus_dir: Path | None = None) -> dict[str, dict]:
    """Load BSIP1 corpus by barcode."""
    if corpus_dir is None or not corpus_dir.exists():
        return {}
    corpus: dict[str, dict] = {}
    for fpath in sorted(corpus_dir.iterdir()):
        if fpath.suffix != ".json":
            continue
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            bc = data.get("barcode", "")
            if bc:
                corpus[bc] = data
        except Exception:
            pass
    return corpus


def _safe_str(val) -> str:
    if val is None:
        return ""
    return str(val)


def compare_with_corpus(
    parsed_products: list[dict],
    corpus: dict[str, dict],
) -> list[dict]:
    """Compare parsed-from-store output with BSIP1 corpus fields.

    Returns a list of match/mismatch report dicts.
    """
    reports: list[dict] = []

    CORPUS_FIELDS = [
        ("name_he", "canonical_name_he"),
        ("barcode", "barcode"),
    ]
    NUTRITION_FIELDS = [
        ("energy_kcal_raw", "energy_kcal"),
        ("fat_raw", "fat_g"),
        ("saturated_fat_raw", "fat_saturated_g"),
        ("protein_raw", "protein_g"),
        ("carbs_raw", "carbohydrates_g"),
        ("fiber_raw", "dietary_fiber_g"),
        ("sodium_raw", "sodium_mg"),
        ("sugar_raw", "sugars_g"),
    ]

    for prod in parsed_products:
        bc = prod.get("barcode", "")
        if bc not in corpus:
            reports.append({
                "barcode": bc,
                "name": prod.get("name_he", ""),
                "in_corpus": False,
                "match": None,
                "fields": [],
            })
            continue

        cp = corpus[bc]
        fields: list[dict] = []

        # Compare identity fields
        for parsed_key, corpus_key in CORPUS_FIELDS:
            pv = _safe_str(prod.get(parsed_key, ""))
            cv = _safe_str(cp.get(corpus_key, ""))
            fields.append({
                "field": parsed_key,
                "parsed": pv,
                "corpus_value": cv,
                "match": pv == cv,
            })

        # Compare nutrition fields (numeric normalization: "87" == 87.0)
        _UNIT_SUFFIXES = [" מג", " גרם", " ג", " קל"]
        def _strip_unit(s: str) -> str:
            for u in _UNIT_SUFFIXES:
                if s.endswith(u):
                    return s[: -len(u)].strip()
            return s
        def _num_match(a, b) -> bool:
            a = _strip_unit(_safe_str(a))
            b = _strip_unit(_safe_str(b))
            try:
                return float(a) == float(b) if a and b else a == b
            except (ValueError, TypeError):
                return a == b

        nutr = prod.get("nutrition", {})
        cp_nutr = cp.get("normalized_nutrition_per_100g", {})
        for parsed_key, corpus_key in NUTRITION_FIELDS:
            pv = _safe_str(nutr.get(parsed_key, ""))
            cv = _safe_str(cp_nutr.get(corpus_key, ""))
            fields.append({
                "field": f"nutrition.{parsed_key}",
                "parsed": pv,
                "corpus_value": cv,
                "match": _num_match(pv, cv),
            })

        # Compare ingredients
        p_ingr = _safe_str(prod.get("ingredients_raw", ""))
        c_ingr = _safe_str(cp.get("ingredients_raw", ""))
        fields.append({
            "field": "ingredients_raw",
            "parsed": p_ingr[:100],
            "corpus_value": c_ingr[:100],
            "match": p_ingr == c_ingr,
        })

        all_match = all(f["match"] for f in fields)
        reports.append({
            "barcode": bc,
            "name": prod.get("name_he", ""),
            "in_corpus": True,
            "match": all_match,
            "mismatch_count": sum(1 for f in fields if not f["match"]),
            "fields": fields,
        })

    return reports


def print_report_table(reports: list[dict]):
    """Print a match/mismatch summary table."""
    total = len(reports)
    in_corpus = sum(1 for r in reports if r["in_corpus"])
    matched = sum(1 for r in reports if r.get("match"))
    mismatched = sum(1 for r in reports if r.get("in_corpus") and not r.get("match"))
    not_in_corpus = sum(1 for r in reports if not r["in_corpus"])

    print(f"\n{'='*70}")
    print(f"REPLAY PARSE MATCH/MISMATCH REPORT")
    print(f"{'='*70}")
    print(f"Total parsed from store:     {total}")
    print(f"  In BSIP1 corpus:           {in_corpus}")
    print(f"    Full match:              {matched}")
    print(f"    Mismatch:                {mismatched}")
    print(f"  Not in corpus (new):       {not_in_corpus}")

    if mismatched > 0:
        print(f"\n{'='*70}")
        print("MISMATCH DETAILS:")
        print(f"{'='*70}")
        for r in reports:
            if r.get("in_corpus") and not r.get("match"):
                print(f"\n  Barcode: {r['barcode']} ({r['name']})")
                print(f"  Mismatched fields: {r['mismatch_count']}")
                for f in r["fields"]:
                    if not f["match"]:
                        print(f"    {f['field']}:")
                        print(f"      parsed:  {f['parsed'][:60]}")
                        print(f"      corpus:  {f['corpus_value'][:60]}")

    return {
        "total": total,
        "in_corpus": in_corpus,
        "matched": matched,
        "mismatched": mismatched,
        "not_in_corpus": not_in_corpus,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Offline BSIP0 replay parser")
    parser.add_argument("--fixtures", action="store_true",
                        help="Load frozen-veg fixtures into store first")
    parser.add_argument("--corpus-dir", type=str, default=str(CORPUS_DIR),
                        help="Path to BSIP1 corpus directory")
    args = parser.parse_args()

    notes: list[str] = []

    # Step 1: Optionally load fixtures
    if args.fixtures:
        print("Loading frozen-veg fixtures into raw store...")
        notes.extend(load_fixtures_into_store())

    # Step 2: Parse from store
    print("\nReplay-parsing frozen-veg pages from store...")
    fv_products, fv_notes = run_replay_parse("shufersal", "frozen_vegetables")
    notes.extend(fv_notes)

    # Step 3: Load BSIP1 corpus
    corpus_dir = Path(args.corpus_dir)
    print(f"\nLoading BSIP1 corpus from {corpus_dir}...")
    corpus = load_bsip1_corpus(corpus_dir)
    print(f"  Loaded {len(corpus)} corpus entries")

    # Step 4: Compare
    print(f"\nComparing {len(fv_products)} parsed products with corpus...")
    reports = compare_with_corpus(fv_products, corpus)

    # Step 5: Print report
    stats = print_report_table(reports)

    # Step 6: Output JSON report
    report_path = STORE_DIR / "replay_report.json"
    report_data = {
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "notes": notes,
        "stats": stats,
        "reports": reports,
    }
    report_path.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFull report written to: {report_path}")

    # Step 7: Check if any live yogurt pages were fetched
    yogurt_products, _ = run_replay_parse("shufersal", "yogurt")
    print(f"\nYogurt pages in store: {len(yogurt_products)}")

    if yogurt_products:
        print("Comparing yogurt products with BSIP1 corpus...")
        y_reports = compare_with_corpus(yogurt_products, corpus)
        y_stats = print_report_table(y_reports)
        y_report_path = STORE_DIR / "replay_yogurt_report.json"
        y_data = {
            "run_ts": datetime.now(timezone.utc).isoformat(),
            "stats": y_stats,
            "reports": y_reports,
        }
        y_report_path.write_text(json.dumps(y_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Yogurt report: {y_report_path}")
    else:
        print("(No yogurt pages in store — live fetch was not possible)")


if __name__ == "__main__":
    main()
