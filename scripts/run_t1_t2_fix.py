"""
TASK-244 Data Integrity Pass: T1 + T2 fixes on cakes and biscuit frontend JSONs.

T1: Remove 4 misclassified "עוגת קראנץ" products from biscuits page.
    Discard all 4 (not cake-quality data; cake corpus already has category coverage).
    Keep ambiguous 3 (7290118423904, 7290118422617, 7290019816034) — genuine biscuit/cookie formats.

T2: Fix cakes _meta.run_id from "run_cakes_001" to "run_cakes_shelfrel_001" (audit trail fix).
    Biscuit barcodes 7296073453857 and 313184: FE scores match pilot_ev098 and run_cakes_001
    respectively — canonical cakes run is shelfrel_001 but these are biscuit-category products;
    their FE value origin is tracked below.

Scores NOT changed on biscuits (engine frozen, no rescore).
"""
import json, sys, pathlib, hashlib, datetime
sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"C:\Bari")
BISCUIT_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
CAKES_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cakes_hard_cookies_frontend_v1.json"

# Load both files
with open(BISCUIT_PATH, "r", encoding="utf-8") as f:
    biscuit = json.load(f)
with open(CAKES_PATH, "r", encoding="utf-8") as f:
    cakes = json.load(f)

# ── T1: Remove definite misclassifications ────────────────────────────────────
T1_REMOVE = {"7290119040568", "7290119040612", "7290119040513", "7290119040667"}
# Ambiguous decisions:
# 7290118423904 (קרמוגית קראנץ שוקו וניל) → KEEP: Oreo-type sandwich cream biscuit format
# 7290118422617 (קרמוגית קראנץ קרם וניל) → KEEP: same format, genuine biscuit
# 7290019816034 (מאגדת מיני קראנץ עוגיות) → KEEP: mini coated biscuit pieces, name says "עוגיות"

original_biscuit_count = len(biscuit["products"])
removed_products = []
kept_products = []

for p in biscuit["products"]:
    if p["barcode"] in T1_REMOVE:
        removed_products.append({"barcode": p["barcode"], "name": p.get("name",""),
                                  "score": p.get("score"), "grade": p.get("grade"),
                                  "disposition": "DISCARDED — misclassified cake (עוגת קראנץ / layered filled pastry, not biscuit)"})
    else:
        kept_products.append(p)

new_biscuit_count = len(kept_products)
print(f"T1: Removed {len(removed_products)} products from biscuit page")
print(f"  Original count: {original_biscuit_count}")
print(f"  New count: {new_biscuit_count}")
for r in removed_products:
    print(f"  REMOVED: {r['barcode']} | {r['name'][:50]} | {r['score']}/{r['grade']} | {r['disposition']}")

# Recompute grade distribution after T1
new_grade_dist = {}
for p in kept_products:
    g = p["grade"]
    new_grade_dist[g] = new_grade_dist.get(g, 0) + 1
print(f"  New grade distribution: {new_grade_dist}")

# Update biscuit meta
biscuit["products"] = kept_products
biscuit["_meta"]["product_count"] = new_biscuit_count
biscuit["_meta"]["scored_count"] = new_biscuit_count
biscuit["_meta"]["grade_distribution"] = new_grade_dist
biscuit["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
biscuit["_meta"]["integrity_pass"] = {
    "task": "TASK-244",
    "date": "2026-06-15",
    "t1_removed": [{"barcode": r["barcode"], "name": r["name"], "disposition": r["disposition"]} for r in removed_products],
    "t1_ambiguous_kept": [
        {"barcode": "7290118423904", "reason": "קרמוגית = Oreo-type cream sandwich biscuit; biscuit format"},
        {"barcode": "7290118422617", "reason": "קרמוגית = Oreo-type cream sandwich biscuit; biscuit format"},
        {"barcode": "7290019816034", "reason": "מאגדת מיני קראנץ עוגיות = mini coated biscuit pieces; name=עוגיות"}
    ],
    "t2_biscuit_score_note": "7296073453857=31.5/E and 313184=34.9/E in FE; 313184 trace value is 35.3/D in both run_cakes_001 and shelfrel_001; canonical biscuit run is run_cookies_005+pilot_ev098; these barcodes were new-batch products from run_cakes_001_cookies subset; scores are NOT changed (engine frozen)"
}

# Update page_copy filter counts
for f in biscuit.get("page_copy", {}).get("filters", []):
    fid = f.get("id")
    if fid == "all":
        f["count"] = new_biscuit_count
    elif fid == "grade_c":
        f["count"] = new_grade_dist.get("C", 0)
    elif fid == "grade_d":
        f["count"] = new_grade_dist.get("D", 0)
    elif fid == "grade_e":
        f["count"] = new_grade_dist.get("E", 0)

# Update hero count
if biscuit.get("page_copy", {}).get("hero"):
    biscuit["page_copy"]["hero"]["productCount"] = new_biscuit_count
    biscuit["page_copy"]["hero"]["scoredCount"] = new_biscuit_count

# ── T2: Fix cakes _meta.run_id ────────────────────────────────────────────────
old_run_id = cakes["_meta"]["run_id"]
cakes["_meta"]["run_id"] = "run_cakes_shelfrel_001"
cakes["_meta"]["run_id_corrected_from"] = old_run_id
cakes["_meta"]["run_id_correction_note"] = (
    "TASK-244 audit: all 65 FE scores match run_cakes_shelfrel_001 (65/65 exact); "
    "run_cakes_001 gives 29 mismatches and 3 grade flips. "
    "Canonical source is run_cakes_hard_cookies_shelfrel_001 (BARI_SHELF_RELATIVE_V1=on, "
    "BARI_FAT_TECH_V1=on, generated 2026-06-15T15:47:02Z). "
    "_meta.run_id label was wrong; scores and grades are unchanged."
)
cakes["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(f"\nT2: Cakes _meta.run_id fixed: '{old_run_id}' → 'run_cakes_shelfrel_001'")

# ── Verify v1 protected 56 all still present ────────────────────────────────
with open(ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v1.json", "r", encoding="utf-8") as f:
    v1_data = json.load(f)
v1_barcodes = {p["barcode"] for p in v1_data["products"]}
new_biscuit_barcodes = {p["barcode"] for p in kept_products}
missing_protected = v1_barcodes - new_biscuit_barcodes
print(f"\nProtected v1 verification: {len(v1_barcodes)} v1 products, {len(v1_barcodes - missing_protected)} present in new corpus")
if missing_protected:
    print(f"  ALERT: Missing protected products: {missing_protected}")
else:
    print(f"  OK: All 56 protected v1 products still present")

# ── Write outputs ────────────────────────────────────────────────────────────
with open(BISCUIT_PATH, "w", encoding="utf-8") as f:
    json.dump(biscuit, f, ensure_ascii=False, indent=2)
print(f"\nWrote updated biscuit file: {BISCUIT_PATH}")

with open(CAKES_PATH, "w", encoding="utf-8") as f:
    json.dump(cakes, f, ensure_ascii=False, indent=2)
print(f"Wrote updated cakes file: {CAKES_PATH}")

# ── Compute SHA256 of outputs ────────────────────────────────────────────────
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

biscuit_sha = sha256_file(BISCUIT_PATH)
cakes_sha = sha256_file(CAKES_PATH)
print(f"\nSHA256:")
print(f"  cookies_coffee_frontend_v2.json: {biscuit_sha}")
print(f"  cakes_hard_cookies_frontend_v1.json: {cakes_sha}")

# ── T3: Caveat stats on final biscuit corpus ─────────────────────────────────
SUGAR_THRESHOLD = 17.5
SATFAT_THRESHOLD = 5.0
both = 0
one_only = 0
neither = 0
null_total = 0
null_list = []

for p in kept_products:
    nutr = p.get("expansion", {}).get("nutrition", {})
    sugar = nutr.get("sugar")
    satfat = nutr.get("satFat")
    if sugar is None or satfat is None:
        null_total += 1
        null_list.append(p["barcode"])
        continue
    cs = sugar > SUGAR_THRESHOLD
    cf = satfat > SATFAT_THRESHOLD
    if cs and cf:
        both += 1
    elif cs or cf:
        one_only += 1
    else:
        neither += 1

print(f"\n=== T3: Caveat stats on final {new_biscuit_count}-product biscuit corpus ===")
print(f"  Thresholds: sugar > {SUGAR_THRESHOLD} g/100g AND satFat > {SATFAT_THRESHOLD} g/100g")
print(f"  (a) Crosses BOTH thresholds: {both}")
print(f"  (b) Crosses ONE threshold only: {one_only}")
print(f"  (c) Crosses NEITHER: {neither}")
print(f"  Products with null sugar or satFat (excluded from threshold check): {null_total}")
print(f"  Null barcodes: {null_list}")
print(f"  Subtotal with data: {both + one_only + neither}")
print(f"  Total check: {both + one_only + neither + null_total} == {new_biscuit_count}")

# Final verification
print(f"\n=== Final verification ===")
print(f"  Biscuit count: {new_biscuit_count} (was {original_biscuit_count}, removed {len(removed_products)})")
print(f"  Cakes count: {len(cakes['products'])} (unchanged)")
print(f"  Protected v1 in new biscuit: {len(v1_barcodes & new_biscuit_barcodes)}/56")
print(f"  Engine NOT run (no rescore)")
print(f"  Score changes: NONE (engine frozen)")
