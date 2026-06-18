"""
OFF sweep v1 — read-only scan of all live category data files for Open Food Facts contamination.

Checks:
  A. JSON-level: scan file text for OFF markers
  B. Corpus-level: for each product barcode in the file, find BSIP1 record and
     check panel_source field.

Output: 03_operations/off_sweep/off_sweep_v1.md
"""

import json
import os
import re
import glob
import hashlib
import datetime

REPO = r"C:\Bari"
DATA_DIR = os.path.join(REPO, "bari-web", "src", "data")
BSIP1_ROOT = os.path.join(REPO, "03_operations", "bsip1")
OUT_DIR = os.path.join(REPO, "03_operations", "off_sweep")

OFF_MARKERS = [
    "open_food_facts",
    "openfoodfacts",
    "images.openfoodfacts.org",
    "world.openfoodfacts",
]

# Canonical (category -> data file) map, derived from reading page-data .ts imports
CATEGORY_DATA_FILES = {
    "bread":            os.path.join(DATA_DIR, "comparisons", "bread_frontend_v2.json"),
    "hummus":           os.path.join(DATA_DIR, "comparisons", "hummus_frontend_v5.json"),
    "vegetable-spreads": os.path.join(DATA_DIR, "comparisons", "hummus_frontend_v5.json"),  # same source
    "snacks":           os.path.join(DATA_DIR, "comparisons", "snacks_frontend_v2.json"),
    "yogurts":          os.path.join(DATA_DIR, "comparisons", "yogurts_frontend_v3.json"),
    "cheese":           os.path.join(DATA_DIR, "comparisons", "cheese_frontend_v3.json"),
    "breakfast-cereals": os.path.join(DATA_DIR, "comparisons", "cereals_frontend_v2.json"),
    "butter":           os.path.join(DATA_DIR, "comparisons", "butter_frontend_v2.json"),
    "granola":          os.path.join(DATA_DIR, "comparisons", "granola_frontend_v1.json"),
    "salty-snacks":     os.path.join(DATA_DIR, "comparisons", "salty_snacks_frontend_v4.json"),
    "milk (legacy)":    os.path.join(DATA_DIR, "milk-comparison.json"),
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def find_bsip1_records():
    """Build a dict: barcode_str -> list of (file_path, panel_source) tuples."""
    records = {}
    pattern = os.path.join(BSIP1_ROOT, "**", "*.json")
    files = glob.glob(pattern, recursive=True)
    for fpath in files:
        fname = os.path.basename(fpath)
        if fname == "run_summary.json":
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        # Extract barcode
        barcode = None
        if isinstance(data, dict):
            barcode = data.get("barcode") or data.get("product_barcode")
            if barcode is None:
                # Try to extract from filename
                # Pattern: bsip1_BARCODE.json or bsip1_audit_BARCODE.json
                m = re.search(r"bsip1(?:_audit)?_(\d+)\.json$", fname)
                if m:
                    barcode = m.group(1)

        if barcode is None:
            continue
        barcode = str(barcode)

        # Extract panel_source
        panel_source = (
            data.get("panel_source")
            or data.get("source", {}).get("panel_source")
            or (data.get("nutrition_source") if isinstance(data.get("nutrition_source"), str) else None)
            or "NOT_FOUND"
        )

        if barcode not in records:
            records[barcode] = []
        records[barcode].append({
            "file": fpath,
            "panel_source": panel_source,
        })

    return records

def extract_barcodes_from_json(data, data_file):
    """Extract all product barcodes from a frontend JSON file."""
    barcodes = []  # list of (barcode, name)

    products = None
    if isinstance(data, dict):
        products = (
            data.get("products")
            or data.get("items")
        )
        if products is None:
            # milk-comparison.json has products at top level
            for k, v in data.items():
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                    products = v
                    break
    elif isinstance(data, list):
        products = data

    if products is None:
        return barcodes

    for product in products:
        if not isinstance(product, dict):
            continue
        barcode = None
        name = ""

        # Try various barcode field names
        for bc_field in ["barcode", "id", "product_barcode", "ean"]:
            val = product.get(bc_field)
            if val:
                # For hummus: id may be "bsip1_7296073733324" -> extract numeric part
                bval = str(val)
                m = re.match(r"bsip1_(\d+)$", bval)
                if m:
                    barcode = m.group(1)
                else:
                    # Check if it's pure numeric
                    if re.match(r"^\d+$", bval):
                        barcode = bval
                break

        # Try name
        for name_field in ["name", "product_name", "displayTitle", "shortName"]:
            val = product.get(name_field)
            if val:
                name = str(val)
                break

        if barcode:
            barcodes.append((barcode, name))

    return barcodes

def check_json_level_off(file_path):
    """Check A: scan raw file text for OFF markers. Returns (count, list of match contexts)."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    hits = []
    text_lower = text.lower()
    for marker in OFF_MARKERS:
        if marker.lower() in text_lower:
            # Find all occurrences
            start = 0
            while True:
                pos = text_lower.find(marker.lower(), start)
                if pos == -1:
                    break
                ctx = text[max(0, pos-30):pos+len(marker)+50].replace("\n", " ")
                hits.append({"marker": marker, "context": ctx})
                start = pos + 1

    return len(hits), hits

def check_corpus_level_off(barcodes, bsip1_records, category):
    """Check B: for each barcode, look up BSIP1 record, report panel_source."""
    results = []
    for barcode, name in barcodes:
        recs = bsip1_records.get(barcode)
        if recs is None:
            results.append({
                "barcode": barcode,
                "name": name,
                "panel_source": "NO_RECORD",
                "bsip1_file": None,
                "is_off": False,
                "is_no_record": True,
            })
        else:
            # Use first record found (prefer non-audit file if multiple)
            rec = recs[0]
            ps = rec["panel_source"]
            is_off = (
                isinstance(ps, str) and (
                    "open_food_facts" in ps.lower()
                    or "openfoodfacts" in ps.lower()
                )
            )
            results.append({
                "barcode": barcode,
                "name": name,
                "panel_source": ps,
                "bsip1_file": rec["file"],
                "is_off": is_off,
                "is_no_record": False,
            })
    return results

def main():
    print("Building BSIP1 records index...")
    bsip1_records = find_bsip1_records()
    print(f"  Indexed {len(bsip1_records)} unique barcodes from BSIP1 records")

    results = {}

    # Track which data files we've already processed (hummus and veg-spreads share a file)
    processed_files = {}

    for category, data_file in CATEGORY_DATA_FILES.items():
        print(f"\nScanning: {category} -> {os.path.basename(data_file)}")

        if not os.path.exists(data_file):
            print(f"  WARNING: file not found: {data_file}")
            results[category] = {
                "data_file": data_file,
                "error": "FILE_NOT_FOUND",
            }
            continue

        # Check A: JSON-level OFF markers
        json_hit_count, json_hits = check_json_level_off(data_file)

        # Load JSON to extract barcodes
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        barcodes = extract_barcodes_from_json(data, data_file)

        # For vegetable-spreads, the file is shared with hummus.
        # Both pages see the full barcode set; note this in output.
        shared_note = None
        if category == "vegetable-spreads":
            shared_note = "Shares hummus_frontend_v5.json with hummus category"

        # Check B: corpus-level
        corpus_results = check_corpus_level_off(barcodes, bsip1_records, category)

        off_fed = [r for r in corpus_results if r["is_off"]]
        no_records = [r for r in corpus_results if r["is_no_record"]]

        results[category] = {
            "data_file": data_file,
            "data_file_basename": os.path.basename(data_file),
            "total_products_in_file": len(barcodes),
            "json_hit_count": json_hit_count,
            "json_hits": json_hits,
            "corpus_results": corpus_results,
            "off_fed_count": len(off_fed),
            "off_fed": off_fed,
            "no_record_count": len(no_records),
            "no_records": no_records,
            "shared_note": shared_note,
        }

        print(f"  Products: {len(barcodes)}, OFF (JSON markers): {json_hit_count}, OFF (corpus): {len(off_fed)}, NO_RECORD: {len(no_records)}")

    # Write output
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "off_sweep_v1.md")

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# OFF Sweep v1 — Open Food Facts Contamination Map\n\n")
        f.write(f"Generated: {now}  \n")
        f.write(f"Method: Python stdlib JSON parse + text grep of all live category data files; BSIP1 record lookup by barcode.  \n")
        f.write(f"Scope: 10 registry categories + milk (legacy). Hard-cheeses and juices excluded — not in registry index.ts.  \n\n")

        # Section 1: Category-data file map
        f.write("## Section 1: Category → Data File Map\n\n")
        f.write("| Category | Data File | Source |\n")
        f.write("|---|---|---|\n")
        for cat, r in results.items():
            note = r.get("shared_note", "") or ""
            f.write(f"| {cat} | {r.get('data_file_basename', 'N/A')} | {note} |\n")
        f.write("\n")

        # Section 2: Verdict table
        f.write("## Section 2: Verdict Table\n\n")
        f.write("| Category | Data File | Products (M) | OFF-fed B (N/M) | JSON markers A | NO_RECORD | Verdict |\n")
        f.write("|---|---|---|---|---|---|---|\n")

        total_off_fed = 0
        total_products = 0

        for cat, r in results.items():
            if "error" in r:
                f.write(f"| {cat} | {r.get('data_file_basename', '?')} | N/A | N/A | N/A | N/A | ERROR: {r['error']} |\n")
                continue

            m = r["total_products_in_file"]
            n_off = r["off_fed_count"]
            n_json = r["json_hit_count"]
            n_no_rec = r["no_record_count"]

            # Determine verdict
            if n_off > 0 or n_json > 0:
                verdict = "DIRTY"
            elif n_no_rec == m and m > 0:
                verdict = "UNKNOWN (all NO_RECORD)"
            elif n_no_rec > 0:
                verdict = "PARTIAL (some NO_RECORD)"
            else:
                verdict = "CLEAN"

            total_off_fed += n_off
            total_products += m

            f.write(f"| {cat} | {r['data_file_basename']} | {m} | {n_off}/{m} | {n_json} | {n_no_rec} | {verdict} |\n")

        f.write(f"\n**TOTAL OFF-FED across all live categories: {total_off_fed}**\n\n")

        # Section 3: Per-dirty-category details
        f.write("## Section 3: Dirty Category Details\n\n")

        dirty_cats = {cat: r for cat, r in results.items() if not "error" in r and (r["off_fed_count"] > 0 or r["json_hit_count"] > 0)}

        if not dirty_cats:
            f.write("No dirty categories found.\n\n")

        for cat, r in dirty_cats.items():
            f.write(f"### {cat}\n\n")
            f.write(f"Data file: `{r['data_file_basename']}`  \n")

            if r["json_hit_count"] > 0:
                f.write(f"\n**JSON-level OFF markers ({r['json_hit_count']} hits):**\n\n")
                for h in r["json_hits"][:20]:  # cap at 20 for readability
                    f.write(f"- Marker `{h['marker']}`: `...{h['context']}...`\n")
                f.write("\n")

            if r["off_fed_count"] > 0:
                f.write(f"\n**Corpus-level OFF-fed products ({r['off_fed_count']}/{r['total_products_in_file']}):**\n\n")
                f.write("| Barcode | Name | panel_source | BSIP1 file |\n")
                f.write("|---|---|---|---|\n")
                for p in r["off_fed"]:
                    bsip1_rel = os.path.relpath(p["bsip1_file"], REPO) if p["bsip1_file"] else "N/A"
                    f.write(f"| {p['barcode']} | {p['name'][:60]} | {p['panel_source']} | {bsip1_rel} |\n")
                f.write("\n")
            else:
                f.write("\nNo corpus-level OFF-fed products found (JSON markers only).\n\n")

        # Section 4: Per-category full corpus results (for CLEAN categories, show all to confirm)
        f.write("## Section 4: Full Corpus Results (all products, all categories)\n\n")

        for cat, r in results.items():
            if "error" in r:
                continue
            f.write(f"### {cat} ({r['data_file_basename']})\n\n")
            if r.get("shared_note"):
                f.write(f"*Note: {r['shared_note']}*\n\n")
            f.write(f"Total in file: {r['total_products_in_file']} | OFF-fed: {r['off_fed_count']} | NO_RECORD: {r['no_record_count']}\n\n")

            f.write("| Barcode | Name | panel_source | Status |\n")
            f.write("|---|---|---|---|\n")
            for p in r["corpus_results"]:
                if p["is_off"]:
                    status = "OFF-FED"
                elif p["is_no_record"]:
                    status = "NO_RECORD"
                else:
                    status = "ok"
                f.write(f"| {p['barcode']} | {p['name'][:55]} | {p['panel_source']} | {status} |\n")
            f.write("\n")

        # Section 5: NO_RECORD concentration
        f.write("## Section 5: NO_RECORD Concentrations\n\n")
        f.write("Categories with >50% NO_RECORD products cannot be confirmed clean.\n\n")
        f.write("| Category | NO_RECORD | Total | Pct |\n")
        f.write("|---|---|---|---|\n")
        for cat, r in results.items():
            if "error" in r:
                continue
            m = r["total_products_in_file"]
            n = r["no_record_count"]
            if m > 0:
                pct = round(100.0 * n / m, 1)
                flag = " <-- HIGH" if pct > 50 else ""
                f.write(f"| {cat} | {n} | {m} | {pct}%{flag} |\n")
        f.write("\n")

    print(f"\nOutput written to: {out_path}")
    return out_path, results, total_off_fed, total_products

if __name__ == "__main__":
    out_path, results, total_off_fed, total_products = main()
    print(f"\nSUMMARY: {total_off_fed} OFF-fed products across {total_products} total products in live categories")
