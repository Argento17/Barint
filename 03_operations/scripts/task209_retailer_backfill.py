"""
TASK-209: Retailer field backfill for all live frontend JSON files.
Run from C:\Bari root.

Categories confirmed as shufersal via BSIP0 scrape directories:
- hummus:   03_operations/bsip0/scrape/shufersal_hummus/   ✓
- yogurts:  03_operations/bsip0/scrape/shufersal_yogurt/   ✓
- cereals:  03_operations/bsip0/scrape/shufersal_cereals/  ✓
- granola:  03_operations/bsip0/scrape/shufersal_cereals/  ✓ (same shelf)
- maadanim: 03_operations/bsip0/scrape/shufersal_maadanim/ ✓
- cheese:   03_operations/bsip0/scrape/shufersal_cheese/   ✓
- bread:    02_products/bread_retail_003 bsip0 raw: retailer_id = 'shufersal' ✓

Snacks: BSIP1 source_retailers evidence shows Yohananof (primary) + Carrefour.
No shufersal_snacks directory exists. Per-product retailer assigned from canonical
bsip1 source_retailers (dominant retailer per product).
snk-006 (bsip1_7290118427858) is carrefour_israel only → retailer = 'carrefour'
All 17 others have yohananof as a source → retailer = 'yohananof'
"""

import json
import sys

BASE = "C:/Bari/bari-web/src/data/comparisons"

# Files where all products are confirmed shufersal
SHUFERSAL_FILES = [
    f"{BASE}/hummus_frontend_v5.json",
    f"{BASE}/yogurts_frontend_v2.json",
    f"{BASE}/cereals_frontend_v1.json",
    f"{BASE}/granola_frontend_v1.json",
    f"{BASE}/maadanim_frontend_v3.json",
    f"{BASE}/cheese_frontend_v2.json",
    f"{BASE}/bread_frontend_v2.json",
]

# Snacks: per-product mapping from bsip1 source_retailers evidence
# snk-006 is carrefour_israel only; all others have yohananof as source
SNACKS_FILE = f"{BASE}/snacks_frontend_v2.json"
SNACKS_RETAILER_MAP = {
    "snk-001": "yohananof",
    "snk-002": "yohananof",
    "snk-003": "yohananof",
    "snk-004": "yohananof",   # also in carrefour; yohananof is listed first
    "snk-005": "yohananof",
    "snk-006": "carrefour",   # carrefour_israel only in bsip1
    "snk-007": "yohananof",
    "snk-009": "yohananof",
    "snk-010": "yohananof",
    "snk-011": "yohananof",
    "snk-012": "yohananof",
    "snk-013": "yohananof",
    "snk-015": "yohananof",
    "snk-016": "yohananof",
    "snk-017": "yohananof",
    "snk-018": "yohananof",
    "snk-019": "yohananof",   # also in carrefour; yohananof is listed first
    "snk-020": "yohananof",
}

total_updated = 0

print("=== TASK-209 Retailer Backfill ===\n")

# Update shufersal files
for path in SHUFERSAL_FILES:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    products = d.get("products", [])
    for p in products:
        p["retailer"] = "shufersal"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    total_updated += len(products)
    category = path.split("/")[-1]
    print(f"[shufersal] {category}: {len(products)} products updated")

# Update snacks file with per-product retailers
with open(SNACKS_FILE, encoding="utf-8") as f:
    d = json.load(f)
products = d.get("products", [])
unmapped = []
for p in products:
    pid = p.get("id")
    retailer = SNACKS_RETAILER_MAP.get(pid)
    if retailer:
        p["retailer"] = retailer
    else:
        unmapped.append(pid)
        p["retailer"] = "unknown"

if unmapped:
    print(f"\nWARNING: Unmapped snack IDs: {unmapped}")

with open(SNACKS_FILE, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
total_updated += len(products)
print(f"\n[mixed] snacks_frontend_v2.json: {len(products)} products updated")
yoh_count = sum(1 for p in products if p.get("retailer") == "yohananof")
car_count = sum(1 for p in products if p.get("retailer") == "carrefour")
print(f"  - yohananof: {yoh_count}, carrefour: {car_count}")

print(f"\n=== Total products updated: {total_updated} ===")

# Verification pass
print("\n=== Verification ===")
import glob
ALL_FILES = SHUFERSAL_FILES + [SNACKS_FILE]
missing_total = 0
for path in ALL_FILES:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    prods = d.get("products", [])
    missing = sum(1 for p in prods if not p.get("retailer"))
    category = path.split("/")[-1]
    if missing > 0:
        print(f"FAIL {category}: {missing} products still missing retailer")
        missing_total += missing
    else:
        null_count = sum(1 for p in prods if p.get("retailer") is None)
        print(f"PASS {category}: all {len(prods)} products have retailer field")

if missing_total == 0:
    print("\nVERIFICATION PASSED: 0 missing retailer across all 8 files")
else:
    print(f"\nVERIFICATION FAILED: {missing_total} products still missing retailer")
    sys.exit(1)
