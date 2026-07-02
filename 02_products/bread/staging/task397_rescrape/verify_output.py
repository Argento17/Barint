"""Verify the rescrape_results.json output."""
import hashlib, json
from pathlib import Path
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = Path(__file__).parent / "rescrape_results.json"
data = p.read_bytes()
sha = hashlib.sha256(data).hexdigest()
print(f"File: {p}")
print(f"SHA256: {sha}")
print(f"Size: {len(data)} bytes")

obj = json.loads(data)
print(f"\ntask: {obj['task']}")
print(f"run_id: {obj['run_id']}")
print(f"generated_at: {obj['generated_at']}")
print(f"OFF ban note: {obj['off_ban_note']}")
print(f"\nRetailers reachable: {obj['reachable_retailers']}")
print(f"Retailers blocked: {obj['blocked_retailers']}")
print(f"Nutrition accessible: {obj['nutrition_accessible_retailers']}")
print(f"\nCounts:")
for k, v in obj["counts"].items():
    print(f"  {k}: {v}")

# Verify integrity
all_discard = all(prod["discard_candidate"] for prod in obj["products"])
any_fat = any(prod["real_fat_g"] is not None for prod in obj["products"])
all_null_fat = all(prod["real_fat_g"] is None for prod in obj["products"])
priority_barcodes = {p["barcode"] for p in obj["products"] if p["is_priority_implausible"]}

print(f"\nIntegrity checks:")
print(f"  All products discard_candidate=true: {all_discard}")
print(f"  Any real_fat_g non-null (should be False): {any_fat}")
print(f"  All real_fat_g null: {all_null_fat}")
print(f"  Priority implausible barcodes: {sorted(priority_barcodes)}")
print(f"  Total products: {len(obj['products'])}")

# Sample product entry
print(f"\nSample entry (74252):")
for prod in obj["products"]:
    if prod["barcode"] == "74252":
        print(json.dumps({k: v for k, v in prod.items() if k != "retailer_attempts"}, ensure_ascii=False, indent=2))
        break
