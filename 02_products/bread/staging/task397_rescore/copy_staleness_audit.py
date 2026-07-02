"""
TASK-397 Copy Staleness Audit
Find bread products in the live frontend JSON whose copy praises fat/leanness
as a positive signal.  These need copy re-audit after the sentinel re-score.
"""
from __future__ import annotations
import json, pathlib, sys, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Patterns that indicate copy praising fat or leanness positively
LEANNESS_PRAISE_PATTERNS = [
    # Hebrew fat/leanness positive phrases
    re.compile(r"(?:שומן\s*נמוך|דל\s*שומן|פחות\s*שומן|עם\s*מעט\s*שומן|נמוך\s*בשומן)", re.IGNORECASE),
    re.compile(r"(?:רזה|רזות|lean|low[\-\s]fat)", re.IGNORECASE),
    re.compile(r"(?:כמעט\s*ללא\s*שומן|ללא\s*שומן|fat[\-\s]free)", re.IGNORECASE),
    re.compile(r"(?:שומן.*פחות\s*מ|שומן.*מינימ|שומן.*נמוך)", re.IGNORECASE),
    # Score-driver praise for fat quality (e.g. "fat quality: 90.5" or "איכות שומן גבוהה")
    re.compile(r"(?:fat.quality|איכות\s*שומן|fat_quality)[^\d]*9[0-9]", re.IGNORECASE),
    # leanness mentions
    re.compile(r"leanness|דלות\s*שומן", re.IGNORECASE),
]

FRONTEND_JSONS = [
    pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v3.json"),
    pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v2.json"),
]

# Sentinel barcodes (22 affected products)
SENTINEL_BARCODES = {
    '2079033','2079217','2079927','3054183','3268252','3268429',
    '481197','481203','497044','574370','6451484','6451507',
    '7290014321168','7290016245325','7290016967074','7290018500460',
    '7296073134442','7296073134459','74252','8434165658523',
    '96086000577','96086000966'
}


def scan_text(text: str, patterns: list) -> list[str]:
    hits = []
    for p in patterns:
        m = p.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def extract_copy_fields(obj, path="") -> list[tuple[str, str]]:
    """Recursively extract all string fields from a JSON object."""
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            results.extend(extract_copy_fields(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            results.extend(extract_copy_fields(v, f"{path}[{i}]"))
    elif isinstance(obj, str) and len(obj) > 5:
        results.append((path, obj))
    return results


stale_products = {}

for fp in FRONTEND_JSONS:
    if not fp.exists():
        print(f"Not found: {fp}")
        continue

    data = json.loads(fp.read_text(encoding="utf-8"))
    print(f"\nScanning: {fp.name}")

    # Navigate to products
    products = []
    if isinstance(data, list):
        products = data
    elif "products" in data:
        products = data["products"]
    elif "clusters" in data:
        for cl in data.get("clusters", []):
            products.extend(cl.get("products", []))

    for prod in products:
        barcode = str(prod.get("barcode", prod.get("id", "?")))
        if barcode not in SENTINEL_BARCODES:
            continue  # Only check sentinel products

        # Collect all text
        copy_fields = extract_copy_fields(prod)
        stale_fields = []
        for field_path, text_val in copy_fields:
            hits = scan_text(text_val, LEANNESS_PRAISE_PATTERNS)
            if hits:
                stale_fields.append({
                    "field": field_path,
                    "text_snippet": text_val[:120],
                    "triggers": hits,
                })

        if stale_fields:
            key = f"{fp.name}:{barcode}"
            stale_products[key] = {
                "file": fp.name,
                "barcode": barcode,
                "name": prod.get("name", prod.get("name_he", "?")),
                "stale_fields": stale_fields,
            }

print("\n" + "=" * 80)
print("COPY STALENESS AUDIT — Fat/Leanness Praise in Sentinel Products")
print("=" * 80)
if stale_products:
    for key, info in stale_products.items():
        print(f"\nFile: {info['file']}")
        print(f"  Barcode: {info['barcode']} | Name: {info['name']}")
        for sf in info["stale_fields"]:
            print(f"  Field: {sf['field']}")
            print(f"  Triggers: {sf['triggers']}")
            print(f"  Snippet: {sf['text_snippet'][:80]}")
else:
    print("\nNo copy found that explicitly praises fat/leanness as a positive driver.")
    print("Note: the copy gates (G6) and verdict model may mention fat in context")
    print("without it being a primary leanness claim. The sentinel barcodes' verdicts")
    print("should still be re-audited after the score move to ensure the fat dimension")
    print("is no longer cited as a strength where it fired R3.")

print(f"\nSentinel barcodes checked: {len(SENTINEL_BARCODES)}")
print(f"Files scanned: {len([f for f in FRONTEND_JSONS if f.exists()])}")
print(f"Stale product+file combinations: {len(stale_products)}")
