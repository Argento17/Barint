"""Final verification of all changes."""
import json, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")

BISCUIT_PATH = "C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json"
CAKES_PATH = "C:/Bari/bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json"
V1_PATH = "C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json"

with open(BISCUIT_PATH, "r", encoding="utf-8") as f:
    biscuit = json.load(f)
with open(CAKES_PATH, "r", encoding="utf-8") as f:
    cakes = json.load(f)
with open(V1_PATH, "r", encoding="utf-8") as f:
    v1 = json.load(f)

biscuit_products = biscuit["products"]
cakes_products = cakes["products"]
v1_barcodes = {p["barcode"] for p in v1["products"]}
biscuit_barcodes = {p["barcode"] for p in biscuit_products}

print("=== FINAL VERIFICATION ===")
print()

# V1: Count check
missing_protected = v1_barcodes - biscuit_barcodes
print(f"Protected v1 check: {len(v1_barcodes)} v1 products, {len(v1_barcodes & biscuit_barcodes)} in biscuit corpus")
if missing_protected:
    print(f"  FAIL — missing: {missing_protected}")
else:
    print(f"  PASS — all 56 protected v1 products present")

# T1: Removed products
T1_REMOVED = {"7290119040568", "7290119040612", "7290119040513", "7290119040667"}
still_in = T1_REMOVED & biscuit_barcodes
print(f"\nT1 removal check: 4 misclassified עוגת קראנץ removed")
if still_in:
    print(f"  FAIL — still present: {still_in}")
else:
    print(f"  PASS — all 4 removed")

# T1: Ambiguous kept
T1_AMBIGUOUS_KEPT = {"7290118423904", "7290118422617", "7290019816034"}
missing_ambig = T1_AMBIGUOUS_KEPT - biscuit_barcodes
print(f"\nT1 ambiguous KEEP check: 3 products should remain")
if missing_ambig:
    print(f"  FAIL — missing: {missing_ambig}")
else:
    print(f"  PASS — all 3 ambiguous products kept")

# Corpus count
print(f"\nBiscuit corpus count: {len(biscuit_products)} (was 122, removed 4)")
if len(biscuit_products) == 118:
    print(f"  PASS — 118 products")
else:
    print(f"  FAIL — expected 118, got {len(biscuit_products)}")

# Grade distribution
grade_dist = {}
for p in biscuit_products:
    g = p["grade"]
    grade_dist[g] = grade_dist.get(g, 0) + 1
print(f"\nGrade distribution: {grade_dist}")
meta_dist = biscuit["_meta"]["grade_distribution"]
if grade_dist == meta_dist:
    print(f"  PASS — meta matches computed: {meta_dist}")
else:
    print(f"  FAIL — meta={meta_dist} vs computed={grade_dist}")

# T2: Cakes run_id
print(f"\nCakes _meta.run_id: {cakes['_meta']['run_id']}")
if cakes["_meta"]["run_id"] == "run_cakes_shelfrel_001":
    print(f"  PASS — correct canonical run")
else:
    print(f"  FAIL — expected 'run_cakes_shelfrel_001'")

# T2: Biscuit score corrections
print(f"\nT2 biscuit score corrections:")
for p in biscuit_products:
    if p["barcode"] in ["313184", "7296073453857"]:
        corr = p.get("_score_correction", {})
        print(f"  {p['barcode']}: score={p['score']} grade={p['grade']}")
        print(f"    corrected from: {corr.get('from_score')}/{corr.get('from_grade')}")
        print(f"    canonical_run: {corr.get('canonical_run')}")
        if p["barcode"] == "313184" and p["score"] == 35.3 and p["grade"] == "D":
            print(f"    PASS — 35.3/D (was 34.9/E)")
        elif p["barcode"] == "7296073453857" and p["score"] == 32.7 and p["grade"] == "E":
            print(f"    PASS — 32.7/E (was 31.5/E)")
        else:
            print(f"    CHECK NEEDED")

# T3: Caveat stats
SUGAR_THRESHOLD = 17.5
SATFAT_THRESHOLD = 5.0
both = one_only = neither = null_total = 0
for p in biscuit_products:
    nutr = p.get("expansion", {}).get("nutrition", {})
    sugar = nutr.get("sugar")
    satfat = nutr.get("satFat")
    if sugar is None or satfat is None:
        null_total += 1
        continue
    cs = sugar > SUGAR_THRESHOLD
    cf = satfat > SATFAT_THRESHOLD
    if cs and cf:
        both += 1
    elif cs or cf:
        one_only += 1
    else:
        neither += 1

print(f"\n=== T3 CAVEAT STATS (final {len(biscuit_products)}-product corpus) ===")
print(f"  Thresholds: sugar>{SUGAR_THRESHOLD} AND satFat>{SATFAT_THRESHOLD}")
print(f"  (a) BOTH thresholds crossed: {both}")
print(f"  (b) ONE threshold only: {one_only}")
print(f"  (c) NEITHER: {neither}")
print(f"  Null (unverifiable): {null_total}")
print(f"  Total: {both + one_only + neither + null_total} == {len(biscuit_products)}")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

print(f"\n=== SHA256 ARTIFACTS ===")
print(f"  cookies_coffee_frontend_v2.json: {sha256_file(BISCUIT_PATH)}")
print(f"  cakes_hard_cookies_frontend_v1.json: {sha256_file(CAKES_PATH)}")
