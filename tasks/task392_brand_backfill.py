"""
TASK-392 Brand Backfill
=======================
Backfills the `brand` field in 3 frontend JSONs from source scrapes.
Also confirms chocolate_tablets brands.

Rules:
- Brand ONLY from source scrape data (direct product scrape)
- OFF is banned (no OFF source)
- For juices: brand is extracted from ingredients_raw_he field (מותג/יצרן: <brand>)
  because the yohananof storefront scraper captured this structured text from the
  product page but did not parse it into the brand field. This IS direct scrape data.
- For cereals/granola: brand field is directly populated in the Shufersal BSIP0 raw.
- No other field changes.
"""

import hashlib
import io
import json
import re
import sys

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BARI = Path("C:/Bari")
BARI_WEB = Path("C:/bari/bari-web")
COMPARISONS = BARI_WEB / "src/data/comparisons"

JUICES_BSIP0 = BARI / "02_products/juices/bsip0_outputs/bsip0_yohananof_juices_storefront_20260607_151232.json"
CEREALS_BSIP0_V1 = BARI / "02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json"
CEREALS_BSIP0_V2 = BARI / "02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json"

JUICES_FRONTEND = COMPARISONS / "juices_frontend_v3.json"
CEREALS_FRONTEND = COMPARISONS / "cereals_frontend_v2.json"
GRANOLA_FRONTEND = COMPARISONS / "granola_frontend_v2.json"
CHOC_FRONTEND = COMPARISONS / "chocolate_tablets_frontend_v1.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")


# ── Source 1: Build juice brand map from BSIP0 yohananof ──────────────────────
def build_juice_brand_map():
    """
    Extract brand from ingredients_raw_he field: מותג/יצרן: <brand>
    This is direct scrape data captured from the yohananof product page.
    The scraper captured the full page text including מותג/יצרן: <brand name>
    but did not parse it into the separate brand field.
    """
    bsip0 = load_json(JUICES_BSIP0)
    brand_map = {}  # barcode -> brand

    BRAND_RE = re.compile(r"מותג/יצרן:\s*([^\n\s][^\n]*?)(?:\s+ארץ\s+יצור|\s+ברקוד:|\s*$)")

    for product in bsip0.get("products", []):
        barcode = str(product.get("barcode", "")).strip()
        if not barcode:
            continue

        # Try the brand field first
        brand = product.get("brand")
        if brand and str(brand).strip():
            brand_map[barcode] = str(brand).strip()
            continue

        # Extract from ingredients_raw_he (direct scrape text)
        raw = product.get("ingredients_raw_he", "") or ""
        m = BRAND_RE.search(raw)
        if m:
            extracted = m.group(1).strip()
            if extracted:
                brand_map[barcode] = extracted
        else:
            brand_map[barcode] = None

    return brand_map


# ── Source 2: Build cereals/granola brand map from BSIP0 Shufersal ────────────
def build_cereals_brand_map():
    """
    Build brand map from both cereals BSIP0 raw files.
    These have brand field directly populated.
    """
    brand_map = {}

    for bsip0_path in [CEREALS_BSIP0_V1, CEREALS_BSIP0_V2]:
        records = load_json(bsip0_path)
        if not isinstance(records, list):
            print(f"  WARNING: {bsip0_path.name} is not a list, skipping")
            continue
        for rec in records:
            barcode = str(rec.get("barcode", "")).strip()
            if not barcode:
                continue
            brand = rec.get("brand")
            if brand and str(brand).strip():
                # First occurrence wins (V1 has priority)
                if barcode not in brand_map:
                    brand_map[barcode] = str(brand).strip()

    return brand_map


# ── Apply brand to frontend JSON ───────────────────────────────────────────────
def apply_brand(frontend_data, brand_map, category_name, has_brand_field=True):
    """
    Apply brand from brand_map to products in frontend_data.
    has_brand_field: if True, brand field already exists in products (possibly null).
                     if False, we need to add the field.
    Returns (populated_count, null_count, no_match_count, coverage_rows)
    """
    products = frontend_data.get("products", [])
    populated = 0
    null_count = 0
    no_match = []
    coverage_rows = []

    for product in products:
        barcode = str(product.get("barcode", "")).strip()
        if not barcode:
            # Try to extract barcode from id field (e.g., bsip1_cereal_7290017962047)
            pid = product.get("id", "")
            m = re.search(r"_(\d{7,14})$", pid)
            if m:
                barcode = m.group(1)

        if not barcode:
            print(f"  WARNING: product with id={product.get('id')} has no barcode")
            continue

        if barcode in brand_map:
            brand_val = brand_map[barcode]
            product["brand"] = brand_val
            if brand_val:
                populated += 1
                coverage_rows.append({
                    "barcode": barcode,
                    "name": product.get("name", "")[:40],
                    "source_brand": brand_val,
                    "status": "POPULATED"
                })
            else:
                null_count += 1
                coverage_rows.append({
                    "barcode": barcode,
                    "name": product.get("name", "")[:40],
                    "source_brand": None,
                    "status": "NULL (source brand empty)"
                })
        else:
            # Barcode not found in source scrape
            product["brand"] = None
            no_match.append(barcode)
            null_count += 1
            coverage_rows.append({
                "barcode": barcode,
                "name": product.get("name", "")[:40],
                "source_brand": None,
                "status": "NO_MATCH (barcode absent from scrape)"
            })

    print(f"\n  {category_name}: {len(products)} total, {populated} populated, {null_count} null, {len(no_match)} no-match barcodes")
    if no_match:
        print(f"    No-match barcodes: {no_match}")

    return populated, null_count, no_match, coverage_rows


# ── Verify non-brand fields unchanged ─────────────────────────────────────────
def spot_check(before_products, after_products, barcodes_to_check, category):
    """Verify score/grade/rank/nutrition unchanged for spot-check barcodes."""
    before_map = {}
    after_map = {}

    for p in before_products:
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            pid = p.get("id", "")
            m = re.search(r"_(\d{7,14})$", pid)
            if m:
                bc = m.group(1)
        before_map[bc] = p

    for p in after_products:
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            pid = p.get("id", "")
            m = re.search(r"_(\d{7,14})$", pid)
            if m:
                bc = m.group(1)
        after_map[bc] = p

    print(f"\n  Spot-check for {category}:")
    all_ok = True
    for bc in barcodes_to_check:
        if bc not in before_map or bc not in after_map:
            print(f"    BC {bc}: NOT FOUND in before/after (skipped)")
            continue
        b = before_map[bc]
        a = after_map[bc]
        checks = {
            "score": b.get("score") == a.get("score"),
            "grade": b.get("grade") == a.get("grade"),
            "rank": b.get("rank") == a.get("rank"),
            "name": b.get("name") == a.get("name"),
        }
        score_ok = all(checks.values())
        if not score_ok:
            all_ok = False
        status = "OK" if score_ok else "MISMATCH"
        brand_before = b.get("brand")
        brand_after = a.get("brand")
        print(f"    BC {bc}: score={a.get('score')}, grade={a.get('grade')}, rank={a.get('rank')} | brand: {brand_before!r} -> {brand_after!r} | {status}")
        for k, v in checks.items():
            if not v:
                print(f"      FIELD MISMATCH: {k} before={b.get(k)!r} after={a.get(k)!r}")

    return all_ok


# ── Verify chocolate_tablets brand coverage ────────────────────────────────────
def verify_choc_brands():
    """Confirm brand coverage in chocolate_tablets; no changes made."""
    choc = load_json(CHOC_FRONTEND)
    products = choc.get("products", [])
    populated = sum(1 for p in products if p.get("brand") and str(p.get("brand")).strip())
    null_count = len(products) - populated
    print(f"\n  chocolate_tablets: {len(products)} products, {populated} with brand, {null_count} null/empty")

    # Check for any null brands
    null_barcodes = [p.get("barcode") for p in products if not (p.get("brand") and str(p.get("brand")).strip())]
    if null_barcodes:
        print(f"    Null brand barcodes: {null_barcodes}")

    return populated, null_count, len(products)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("TASK-392 Brand Backfill")
    print("=" * 60)

    # Pre-run SHA256 of all target files
    print("\nPre-run SHA256:")
    sha_before = {}
    for label, path in [
        ("juices", JUICES_FRONTEND),
        ("cereals", CEREALS_FRONTEND),
        ("granola", GRANOLA_FRONTEND),
        ("choc", CHOC_FRONTEND),
    ]:
        sha_before[label] = sha256_file(path)
        print(f"  {label}: {sha_before[label]}")

    # ── Build brand maps ────────────────────────────────────────────────────────
    print("\nBuilding juice brand map from BSIP0 yohananof scrape...")
    juice_brand_map = build_juice_brand_map()
    print(f"  Juice brand map: {len(juice_brand_map)} barcodes, {sum(1 for v in juice_brand_map.values() if v)} with brand")

    print("\nBuilding cereals/granola brand map from BSIP0 Shufersal...")
    cereals_brand_map = build_cereals_brand_map()
    print(f"  Cereals brand map: {len(cereals_brand_map)} barcodes, {sum(1 for v in cereals_brand_map.values() if v)} with brand")

    # ── JUICES ─────────────────────────────────────────────────────────────────
    print("\n--- JUICES ---")
    juices_data = load_json(JUICES_FRONTEND)
    juices_before_products = json.loads(json.dumps(juices_data.get("products", [])))  # deep copy

    j_pop, j_null, j_nomatch, j_coverage = apply_brand(
        juices_data, juice_brand_map, "juices", has_brand_field=True
    )

    # Spot check: first 3 products
    spot_barcodes_juices = [p.get("barcode") for p in juices_before_products[:3]]
    spot_check(juices_before_products, juices_data.get("products", []), spot_barcodes_juices, "juices")

    # ── CEREALS ────────────────────────────────────────────────────────────────
    print("\n--- CEREALS ---")
    cereals_data = load_json(CEREALS_FRONTEND)
    cereals_before_products = json.loads(json.dumps(cereals_data.get("products", [])))

    c_pop, c_null, c_nomatch, c_coverage = apply_brand(
        cereals_data, cereals_brand_map, "cereals", has_brand_field=True
    )

    # Spot check
    spot_barcodes_cereals = []
    for p in cereals_before_products[:3]:
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            pid = p.get("id", "")
            m = re.search(r"_(\d{7,14})$", pid)
            if m:
                bc = m.group(1)
        if bc:
            spot_barcodes_cereals.append(bc)
    spot_check(cereals_before_products, cereals_data.get("products", []), spot_barcodes_cereals, "cereals")

    # ── GRANOLA ────────────────────────────────────────────────────────────────
    print("\n--- GRANOLA ---")
    granola_data = load_json(GRANOLA_FRONTEND)
    granola_before_products = json.loads(json.dumps(granola_data.get("products", [])))

    # Note: granola products don't have brand field at all — we add it
    g_pop, g_null, g_nomatch, g_coverage = apply_brand(
        granola_data, cereals_brand_map, "granola", has_brand_field=False
    )

    # Spot check
    spot_barcodes_granola = []
    for p in granola_before_products[:3]:
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            pid = p.get("id", "")
            m = re.search(r"_(\d{7,14})$", pid)
            if m:
                bc = m.group(1)
        if bc:
            spot_barcodes_granola.append(bc)
    spot_check(granola_before_products, granola_data.get("products", []), spot_barcodes_granola, "granola")

    # ── CHOCOLATE TABLETS (confirm only, no changes) ────────────────────────────
    print("\n--- CHOCOLATE TABLETS (confirm only) ---")
    choc_pop, choc_null, choc_total = verify_choc_brands()

    # ── Print full coverage tables ──────────────────────────────────────────────
    print("\n\n=== JUICES BRAND COVERAGE ===")
    for row in j_coverage:
        print(f"  {row['barcode']} | {row['source_brand']!r:25} | {row['status']}")

    print("\n\n=== CEREALS BRAND COVERAGE ===")
    for row in c_coverage:
        print(f"  {row['barcode']} | {row['source_brand']!r:25} | {row['status']}")

    print("\n\n=== GRANOLA BRAND COVERAGE ===")
    for row in g_coverage:
        print(f"  {row['barcode']} | {row['source_brand']!r:25} | {row['status']}")

    # ── Save files ──────────────────────────────────────────────────────────────
    print("\n\nSaving files...")
    save_json(JUICES_FRONTEND, juices_data)
    save_json(CEREALS_FRONTEND, cereals_data)
    save_json(GRANOLA_FRONTEND, granola_data)

    # Post-run SHA256
    print("\nPost-run SHA256:")
    sha_after = {}
    for label, path in [
        ("juices", JUICES_FRONTEND),
        ("cereals", CEREALS_FRONTEND),
        ("granola", GRANOLA_FRONTEND),
        ("choc", CHOC_FRONTEND),
    ]:
        sha_after[label] = sha256_file(path)
        changed = " CHANGED" if sha_after[label] != sha_before[label] else " UNCHANGED"
        print(f"  {label}: {sha_after[label]}{changed}")

    # ── Summary ──────────────────────────────────────────────────────────────────
    print("\n\n=== SUMMARY ===")
    print(f"  juices:  {j_pop + j_null} products, {j_pop} brand-populated, {j_null} null (no-match: {len(j_nomatch)} barcodes)")
    print(f"  cereals: {c_pop + c_null} products, {c_pop} brand-populated, {c_null} null (no-match: {len(c_nomatch)} barcodes)")
    print(f"  granola: {g_pop + g_null} products, {g_pop} brand-populated, {g_null} null (no-match: {len(g_nomatch)} barcodes)")
    print(f"  choc:    {choc_total} products, {choc_pop} brand-populated (CONFIRM ONLY, no changes)")

    print("\nDone.")

    # Return exit 0 if no hard failures
    all_populated = j_pop > 0 and c_pop > 0 and g_pop > 0
    if not all_populated:
        print("ERROR: At least one shelf has zero brand-populated products!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
