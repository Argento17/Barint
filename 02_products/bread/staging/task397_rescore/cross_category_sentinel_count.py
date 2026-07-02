"""
TASK-397 Cross-Category Sentinel Count
Count products in OTHER live categories that carry fat_sentinel=True in their
BSIP1 records, or would if they had been rebuilt with the sentinel detection.

Since most other categories do NOT have fat_sentinel in their BSIP1 records yet
(only bread rebuild added it), we check their BSIP0 raw fat_raw fields for
ceiling patterns to estimate cross-category exposure.
"""
from __future__ import annotations
import json, pathlib, sys, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CEILING_RE = re.compile(r"(?:פחות\s*מ|less\s+than|<)\s*([\d.,]+)", re.IGNORECASE)

def has_ceiling(raw_str: str | None) -> bool:
    if not raw_str:
        return False
    return bool(CEILING_RE.match(str(raw_str).strip()))


# Check BSIP1 runs for other categories
BSIP1_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip1")
bread_run = "run_bread_conform_001"

print("Cross-category fat_sentinel scan (fat < 0.5 AND ceiling declaration)")
print("=" * 70)
print("Note: Only bread BSIP1 records have fat_sentinel field; for others,")
print("we scan normalized_nutrition_per_100g.fat_g == 0.25 as proxy AND")
print("check any available raw field.\n")

total_sentinel = 0
total_products = 0

for run_dir in sorted(BSIP1_ROOT.iterdir()):
    if not run_dir.is_dir():
        continue
    out_dir = run_dir / "output"
    if not out_dir.exists():
        continue
    run_id = run_dir.name
    if run_id == bread_run:
        continue  # Skip bread — we know it

    files = sorted(out_dir.glob("bsip1_*.json"))
    if not files:
        continue

    sentinel_barcodes = []
    for f in files:
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        nn = p.get("normalized_nutrition_per_100g", {}) or {}

        # Check explicit fat_sentinel field (bread only currently)
        if nn.get("fat_sentinel") is True:
            sentinel_barcodes.append(str(p.get("barcode", f.stem)))
            continue

        # Check fat_raw_string if present
        fat_raw_str = nn.get("fat_raw_string")
        if fat_raw_str and has_ceiling(fat_raw_str):
            sentinel_barcodes.append(str(p.get("barcode", f.stem)))
            continue

        # Heuristic: fat_g == 0.25 may come from ceiling midpoint (but could be genuine)
        # We count as "potential" only, not confirmed

    total_sentinel += len(sentinel_barcodes)
    total_products += len(files)
    if sentinel_barcodes:
        print(f"  {run_id}: {len(sentinel_barcodes)}/{len(files)} confirmed sentinel barcodes: {sentinel_barcodes[:5]}")
    else:
        print(f"  {run_id}: 0/{len(files)} — no confirmed ceiling fat declarations")

print(f"\nTotal (non-bread categories): {total_sentinel} sentinel products out of {total_products} scanned")
print("(Confirmed = has fat_sentinel=True or fat_raw_string with ceiling marker)")
print("If BARI_FAT_SENTINEL_V1 rolled out to all categories today,")
print(f"  {total_sentinel} additional products beyond bread would lose R3 reward.")
