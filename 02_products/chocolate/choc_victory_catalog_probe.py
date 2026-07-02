"""
Quick il_prices catalog probe: find dark chocolate barcodes in Victory's
catalog that match 80% (or 75-82%) cocoa signals.

This gives us accurate barcode+name candidates before the Playwright scrape.
Run this in parallel with the main probe. Output to stdout only.
"""
from __future__ import annotations
import sys
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip

VICTORY_CHAIN_ID = "7290696200003"

print("Fetching Victory catalog from laibcatalog...", flush=True)
try:
    files = ip.list_laibcatalog_files(VICTORY_CHAIN_ID)
    pf = [f for f in files if f.type == "PriceFull"]
    if not pf:
        print("No PriceFull files found for Victory", flush=True)
        sys.exit(1)
    items = ip.fetch_items(pf[0])
    print(f"Victory catalog: {len(items)} items total", flush=True)
except Exception as e:
    print(f"Error fetching catalog: {e}", flush=True)
    sys.exit(1)

# Look for dark chocolate / dark / moist chocolate by name
CHOC_INCLUDE = ["שוקולד", "שוקולד מריר", "dark", "cocoa", "קקאו"]
CHOC_DROP = ["גלידה", "משקה", "ממרח", "שתיה", "שתייה", "פודינג", "עוגה", "ניקוי", "שמפו"]

all_choc = []
for it in items:
    name = (it.name or "").strip()
    nl = name.lower()
    if any(h.lower() in nl or h in name for h in CHOC_DROP):
        continue
    if "שוקולד" in name or "dark" in nl or "קקאו" in name:
        all_choc.append((str(it.barcode), name))

print(f"\nChocolate products in Victory catalog: {len(all_choc)}", flush=True)

# Filter for 80% or near-80%
near_80 = []
for bc, name in all_choc:
    pct_m = re.search(r'(\d{2,3})\s*%', name)
    if pct_m:
        pct = int(pct_m.group(1))
        if 70 <= pct <= 90:
            near_80.append((bc, name, pct))

print(f"\nNear-80% dark chocolate (70-90%): {len(near_80)}", flush=True)
for bc, name, pct in sorted(near_80, key=lambda x: x[2]):
    print(f"  {bc}  {pct}%  {name}", flush=True)

# Also show all dark chocolate regardless of pct
print(f"\nAll dark chocolate (מריר):", flush=True)
for bc, name in all_choc:
    if "מריר" in name or "dark" in name.lower():
        print(f"  {bc}  {name}", flush=True)

# Check specifically for the 3 Lindt barcodes
TARGET_BARCODES = ["3046920023429", "3046920023368", "3046920023443", "4820005195848"]
print(f"\nTarget barcode lookup:", flush=True)
catalog_bcs = {str(it.barcode): (it.name or "").strip() for it in items}
for bc in TARGET_BARCODES:
    if bc in catalog_bcs:
        print(f"  FOUND: {bc} = {catalog_bcs[bc]}", flush=True)
    else:
        print(f"  NOT IN CATALOG: {bc}", flush=True)
