"""
TASK-212B: Frontend data normalization.
- Fix product-count mismatches
- Backfill barcode fields
- Identify orphans for archiving
- Define BariProductVM v4 schema
"""
import json, re, shutil, sys, os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

COMPARISONS = Path(r"C:\Bari\bari-web\src\data\comparisons")
BSIP1_ROOTS = [
    Path(r"C:\Bari\03_operations\bsip1"),
    Path(r"C:\Bari\02_products"),
]

# ── Live files (imported by frontend) ──────────────────────────────
LIVE_FILES = [
    "bread_frontend_v2.json",
    "butter_frontend_v2.json",
    "cereals_frontend_v2.json",
    "cheese_frontend_v3.json",
    "granola_frontend_v1.json",
    "hard_cheeses_frontend_v2.json",
    "hummus_frontend_v5.json",
    "juices_frontend_v3.json",
    "maadanim_frontend_v3.json",
    "olive_oil_frontend_v1.json",
    "salty_snacks_frontend_v2.json",
    "snacks_frontend_v2.json",
    "yogurts_frontend_v3.json",
]

# ── Files to archive (orphans / historical) ────────────────────────
ORPHAN_FILES = [
    "butter_frontend_v1.json",       # superseded by v2
    "cereals_frontend_v1.json",      # superseded by v2
    "cheese_frontend_v1.json",       # superseded by v2/v3
    "cheese_frontend_v2.json",       # superseded by v3
    "hard_cheeses.json",             # dangerous orphan duplicate (0 images, divergent scores)
    "hard_cheeses_frontend_v1.json", # superseded by v2
    "hummus_frontend_v3.json",       # superseded by v4/v5
    "hummus_frontend_v4.json",       # superseded by v5
    "juices_frontend_v1.json",       # superseded by v2/v3
    "juices_frontend_v2.json",       # superseded by v3
    "maadanim_frontend_v2.json",     # superseded by v3
    "salty_snacks_frontend_v1.json", # superseded by v2
    "yogurts_frontend_v2.json",      # superseded by v3
]

# ── SNK label -> bsip1 PID mapping (from run_snackbars_007_headpin.py) ──
SNK_LABEL_MAP = {
    "snk-001": "bsip1_7290011498870",
    "snk-002": "bsip1_8423207210287",
    "snk-003": "bsip1_7290011498894",
    "snk-004": "bsip1_7290011498948",
    "snk-005": "bsip1_8423207208260",
    "snk-006": "bsip1_8423207206495",
    "snk-007": "bsip1_5900020039590",
    "snk-009": "bsip1_8410076610379",
    "snk-010": "bsip1_8410076610386",
    "snk-011": "bsip1_16000423534",
    "snk-012": "bsip1_16000548404",
    "snk-013": "bsip1_8423207207362",
    "snk-015": "bsip1_7290011498894",
    "snk-016": "bsip1_8423207209885",
    "snk-017": "bsip1_8423207208680",
    "snk-018": "bsip1_8423207210928",
    "snk-019": "bsip1_8410076610492",
    "snk-020": "bsip1_8410076610508",
}

# ── Build BSIP1 index: canonical_product_id -> barcode ──────────────
def build_bsip1_index():
    index = {}
    for root in BSIP1_ROOTS:
        for f in root.rglob("bsip1_*.json"):
            try:
                d = json.loads(f.read_text("utf-8"))
                cpid = d.get("canonical_product_id") or d.get("id")
                barcode = d.get("barcode")
                if cpid and barcode:
                    index[cpid] = barcode
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
    return index

# ── Extract barcode from image URL ─────────────────────────────────
def extract_barcode_from_image_url(url):
    if not url:
        return None
    # Shufersal Cloudinary: ..._P_{BARCODE}_1.png
    m = re.search(r'_P_(\d{8,14})_1\.', url)
    if m:
        return m.group(1)
    # OpenFoodFacts: .../products/761/303/768/6906/front_en...
    m = re.search(r'/products/(\d)/(\d{3})/(\d{3})/(\d{4})/', url)
    if m:
        return m.group(1) + m.group(2) + m.group(3) + m.group(4)
    # Yohananof: .../{BARCODE}_s1_...
    m = re.search(r'/(\d{8,14})_s\d_', url)
    if m:
        return m.group(1)
    # Carrefour: .../images/carrefour/...
    m = re.search(r'/(\d{13})\.[a-z]+$', url)
    if m:
        return m.group(1)
    # Shufersal direct: images.shufersal.co.il
    m = re.search(r'/(\d{8,14})\.(?:jpg|png|jpeg)', url)
    if m:
        return m.group(1)
    return None

# ── Extract barcode from product ID ────────────────────────────────
def extract_barcode_from_id(pid):
    if not pid:
        return None
    # bsip1_<barcode>, bsip1_yogurt_<barcode>, bsip1_snack_<barcode>, bsip1_cereal_<barcode>
    m = re.match(r'bsip1_(?:yogurt_|snack_|cereal_)?(\d{8,14})$', pid)
    if m:
        return m.group(1)
    # shufersal_<digits>
    m = re.match(r'shufersal_(\d{8,14})$', pid)
    if m:
        return m.group(1)
    return None

# ── Resolve snk-XXX label ──────────────────────────────────────────
def resolve_snk_label(pid):
    if pid in SNK_LABEL_MAP:
        bsip1_pid = SNK_LABEL_MAP[pid]
        return extract_barcode_from_id(bsip1_pid)
    return None

# ── Backfill barcode for a single product ──────────────────────────
def backfill_barcode(product, bsip1_index):
    pid = product.get("id", "")
    if product.get("barcode"):
        return  # already has barcode
    barcode = None
    method = None

    # 1) Try snk-XXX label map
    barcode = resolve_snk_label(pid)
    if barcode:
        method = "snk_map"

    # 2) Try ID prefix stripping
    if not barcode:
        barcode = extract_barcode_from_id(pid)
        if barcode:
            method = "id_prefix"

    # 3) Try image URL
    if not barcode:
        barcode = extract_barcode_from_image_url(product.get("imageUrl", ""))
        if barcode:
            method = "image_url"

    # 4) Try BSIP1 index
    if not barcode:
        barcode = bsip1_index.get(pid)
        if barcode:
            method = "bsip1_index"

    product["barcode"] = barcode
    product["source_traceability_status"] = "resolved" if barcode else "missing_barcode"

# ── Fix count mismatches ───────────────────────────────────────────
def fix_product_count(data):
    meta = data.get("_meta", {})
    products = data.get("products", [])
    actual = len(products)
    if meta.get("product_count") != actual:
        old = meta.get("product_count")
        meta["product_count"] = actual
        return old, actual
    return None, None

# ── Normalize a single file ────────────────────────────────────────
def normalize_file(path, bsip1_index):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    changes = {"path": str(path), "count_fixed": None, "barcodes_resolved": 0, "barcodes_missing": 0}

    # Fix count
    old_ct, new_ct = fix_product_count(data)
    if old_ct is not None:
        changes["count_fixed"] = {"old": old_ct, "new": new_ct}

    # Backfill barcodes
    for product in data.get("products", []):
        backfill_barcode(product, bsip1_index)
        if product.get("barcode"):
            changes["barcodes_resolved"] += 1
        else:
            changes["barcodes_missing"] += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return changes

# ── Archive orphan files ───────────────────────────────────────────
def archive_orphans():
    archive_dir = COMPARISONS / "archive"
    archive_dir.mkdir(exist_ok=True)
    moved = []
    for fn in ORPHAN_FILES:
        src = COMPARISONS / fn
        if src.exists():
            dst = archive_dir / fn
            shutil.move(str(src), str(dst))
            moved.append(fn)
    return moved

# ── Main ───────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("TASK-212B: Frontend Data Normalization")
    print("=" * 60)

    # Phase 1: Build BSIP1 index
    print("\nPhase 1: Building BSIP1 index...")
    bsip1_index = build_bsip1_index()
    print(f"  Indexed {len(bsip1_index)} BSIP1 products")

    # Phase 2: Normalize live files
    print("\nPhase 2: Normalizing live files...")
    all_changes = []
    for fn in LIVE_FILES:
        path = COMPARISONS / fn
        if not path.exists():
            print(f"  SKIP {fn} (not found)")
            continue
        changes = normalize_file(path, bsip1_index)
        all_changes.append(changes)
        ct = changes["count_fixed"]
        ct_str = f"count {ct['old']}->{ct['new']}" if ct else "count OK"
        print(f"  {fn}: {ct_str}, +{changes['barcodes_resolved']} barcodes, {changes['barcodes_missing']} missing")

    # Phase 3: Archive orphans
    print("\nPhase 3: Archiving orphan files...")
    moved = archive_orphans()
    for fn in moved:
        print(f"  MOVED {fn} -> archive/")

    # Summary
    total_resolved = sum(c["barcodes_resolved"] for c in all_changes)
    total_missing = sum(c["barcodes_missing"] for c in all_changes)
    total_fixed = sum(1 for c in all_changes if c["count_fixed"])

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Count fixes: {total_fixed} files")
    for c in all_changes:
        if c["count_fixed"]:
            print(f"    {Path(c['path']).name}: {c['count_fixed']['old']} -> {c['count_fixed']['new']}")
    print(f"  Barcodes resolved: {total_resolved}")
    print(f"  Barcodes still missing: {total_missing}")
    print(f"  Orphans archived: {len(moved)}")
    print()

    # Print still-missing by file
    print("Files needing manual barcode resolution:")
    for c in all_changes:
        if c["barcodes_missing"] > 0:
            print(f"  {Path(c['path']).name}: {c['barcodes_missing']} products still missing barcode")
    print()

if __name__ == "__main__":
    main()
