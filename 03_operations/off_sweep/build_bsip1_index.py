"""
Build a comprehensive BSIP1 barcode -> panel_source index from all runs.
Priority: records with explicit panel_source override NOT_FOUND records.
"""
import json
import os
import re
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPO = r"C:\Bari"
BSIP1_ROOT = os.path.join(REPO, "03_operations", "bsip1")

def build_index():
    all_files = glob.glob(os.path.join(BSIP1_ROOT, "run_*", "output", "*.json"))
    index = {}  # barcode -> {panel_source, run, file}

    for fp in all_files:
        fname = os.path.basename(fp)
        if fname == "run_summary.json":
            continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue

        bc = str(d.get("barcode") or d.get("product_barcode") or "")
        if not bc or bc == "None":
            m = re.search(r"bsip1(?:_audit)?_(\d+)\.json$", fname)
            if m:
                bc = m.group(1)
        if not bc:
            continue

        # Extract panel_source - check multiple locations
        ps = d.get("panel_source")
        if ps is None:
            src = d.get("source")
            if isinstance(src, dict):
                ps = src.get("panel_source")
        if ps is None:
            # Scan JSON text for panel_source
            text = json.dumps(d)
            m2 = re.search(r'"panel_source":\s*"([^"]+)"', text)
            if m2:
                ps = m2.group(1)
        ps = str(ps or "NOT_FOUND")

        # Determine run name from path
        parts = fp.replace("\\", "/").split("/")
        run_name = "unknown"
        for p in parts:
            if p.startswith("run_"):
                run_name = p
                break

        # Prefer records that have explicit panel_source
        if bc not in index or (index[bc]["panel_source"] == "NOT_FOUND" and ps != "NOT_FOUND"):
            index[bc] = {"panel_source": ps, "run": run_name, "file": fp}

    return index

def main():
    index = build_index()
    print(f"Total barcodes indexed: {len(index)}")

    # Count by panel_source
    sources = {}
    for v in index.values():
        ps = v["panel_source"]
        sources[ps] = sources.get(ps, 0) + 1

    off_count = sum(v for k, v in sources.items()
                   if "open_food_facts" in k.lower() or "openfoodfacts" in k.lower())
    print(f"Total OFF-sourced (panel_source=open_food_facts): {off_count}")
    print(f"Panel source distribution: {dict(list(sources.items())[:10])}")

    # Save index
    out_path = os.path.join(REPO, "03_operations", "off_sweep", "bsip1_index.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Index saved to: {out_path}")
    return index

if __name__ == "__main__":
    main()
