"""
TASK-378 Phase 2 — Sugar null-guard diagnosis across remaining categories.
Reads raw BSIP0 outputs and bsip1 JSON files to diagnose whether sugar is
absent from the panel or a parser miss.
"""
import json, sys, pathlib, re

ROOT = pathlib.Path(r"C:\Bari\02_products")

# ── Target products per category ─────────────────────────────────────────────
TARGETS = {
    "juices": ["7290013153395", "7290110114886"],
    "cookies_coffee": ["7290119043149", "7290017962139", "7290013453068",
                       "7296073453840", "7296073453857"],
    "milk_and_alternatives": ["7290000051352", "5411188124689",
                               "7290014760141", "7290110325619"],
    "hummus": ["6666307", "6666444"],
    "brined_cheeses": ["369617"],
    "cakes_hard_cookies": ["5431920"],
    "breakfast_cereals": ["7297488098688"],
}

# ── Find BSIP0 JSON files per category ───────────────────────────────────────
def find_bsip0_files(cat_dir: pathlib.Path):
    bsip0_dir = cat_dir / "bsip0_outputs"
    if not bsip0_dir.exists():
        return []
    return list(bsip0_dir.glob("*.json"))


def load_products_from_file(fpath: pathlib.Path):
    """Load products list from a BSIP0 JSON, handling both array and dict-with-products."""
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
    except Exception as e:
        return [], str(e)
    if isinstance(data, list):
        return data, None
    if isinstance(data, dict):
        if "products" in data:
            return data["products"], None
        # It might be a single product
        if "barcode" in data:
            return [data], None
    return [], "unknown_structure"


def get_sugar_from_rows(rows):
    """Check if any row in raw_source.rows is a sugar label."""
    for row in (rows or []):
        lbl = row.get("label", "")
        if "סוכר" in lbl or "sugar" in lbl.lower():
            return row.get("value"), lbl
    return None, None


def diagnose_category(cat_name, barcodes):
    cat_dir = ROOT / cat_name
    bsip0_files = find_bsip0_files(cat_dir)

    # Load all products from all BSIP0 files in this category
    all_products = {}
    for fpath in bsip0_files:
        products, err = load_products_from_file(fpath)
        if err:
            print(f"  [WARN] {fpath.name}: {err}")
            continue
        for p in products:
            bc = str(p.get("barcode", "")).strip()
            if bc:
                all_products[bc] = (p, fpath.name)

    print(f"\n{'='*70}")
    print(f"CATEGORY: {cat_name}")
    print(f"  BSIP0 files: {[f.name for f in bsip0_files]}")
    print(f"  Total products in BSIP0: {len(all_products)}")

    for bc in barcodes:
        print(f"\n  --- Barcode {bc} ---")
        if bc not in all_products:
            print(f"    [MISS] Not found in any BSIP0 file")
            # Try BSIP1
            bsip1_dir = cat_dir / "bsip1_outputs"
            if bsip1_dir.exists():
                bsip1_files = list(bsip1_dir.glob(f"*{bc}*.json"))
                if bsip1_files:
                    b1 = json.loads(bsip1_files[0].read_text(encoding="utf-8"))
                    print(f"    [BSIP1 fallback] sugars_g={b1.get('sugars_g')} carbs_g={b1.get('carbohydrates_g')}")
            continue

        p, source_file = all_products[bc]
        nutr = p.get("nutrition", {}) or {}

        # Canonical keys in the BSIP0 output
        sugar_raw = nutr.get("sugar_raw") or nutr.get("sugars_raw")
        carbs_raw = nutr.get("carbs_raw") or nutr.get("carbohydrates_g") or nutr.get("carbs")
        energy    = nutr.get("energy_kcal_raw") or nutr.get("energy_kcal")

        print(f"    source_file: {source_file}")
        print(f"    sugar_raw: {repr(sugar_raw)}")
        print(f"    carbs_raw: {repr(carbs_raw)}")
        print(f"    energy:    {repr(energy)}")

        # Check raw_source rows
        raw_source = p.get("nutrition_raw_source") or p.get("nutrition_raw") or {}
        rows = raw_source.get("rows", [])
        sugar_val, sugar_lbl = get_sugar_from_rows(rows)
        basis_info = raw_source.get("selection", {}) or {}

        print(f"    raw_source rows: {len(rows)}")
        for row in rows:
            print(f"      label={repr(row.get('label',''))} value={repr(row.get('value',''))}")
        print(f"    basis_selected: {repr(basis_info.get('selected_basis', '?'))}")
        print(f"    basis_header:   {repr(basis_info.get('selected_table_header', '?'))}")
        print(f"    insufficient:   {basis_info.get('insufficient', '?')}")

        if sugar_val is not None:
            print(f"    [SUGAR IN RAW] label={repr(sugar_lbl)} value={repr(sugar_val)}")
            print(f"    DIAGNOSIS: PARSER MISS — sugar row exists but was not mapped to sugar_raw")
        elif len(rows) == 0:
            print(f"    DIAGNOSIS: No raw rows captured — check scraper path")
        else:
            print(f"    DIAGNOSIS: GENUINELY ABSENT — no sugar row in panel")

        # Also load BSIP1 for current score
        bsip1_dir = cat_dir / "bsip1_outputs"
        if bsip1_dir.exists():
            bsip1_files = list(bsip1_dir.glob(f"*{bc}*.json"))
            if bsip1_files:
                b1 = json.loads(bsip1_files[0].read_text(encoding="utf-8"))
                print(f"    [BSIP1] sugars_g={b1.get('sugars_g')} carbs_g={b1.get('carbohydrates_g')} energy_kcal={b1.get('energy_kcal')}")


if __name__ == "__main__":
    import io
    out = io.StringIO()
    orig_stdout = sys.stdout
    sys.stdout = out
    for cat, bcs in TARGETS.items():
        diagnose_category(cat, bcs)
    sys.stdout = orig_stdout
    result = out.getvalue()
    pathlib.Path(r"C:\Bari\02_products\_parsing_audit\task378_phase2_result.txt").write_text(
        result, encoding="utf-8"
    )
    print("Written to task378_phase2_result.txt")
