"""Draw a brand-stratified ~25-SKU representative sample of the addressable shelf.
Stratified so measured yield reflects the REAL shelf brand mix (no Altman cherry-pick)."""
import json, pathlib, collections, math

HERE = pathlib.Path(__file__).resolve().parent
addr = json.loads((HERE / "_addressable_shelf.json").read_text(encoding="utf-8"))
rows = addr["rows"]
TARGET = 25

by_brand = collections.defaultdict(list)
for r in rows:
    by_brand[r["brand_bucket"]].append(r)

# proportional allocation, at least 1 per brand present, capped at availability
total = len(rows)
alloc = {}
for b, items in by_brand.items():
    alloc[b] = max(1, round(TARGET * len(items) / total))
# trim/expand to hit TARGET
while sum(alloc.values()) > TARGET:
    b = max(alloc, key=lambda k: alloc[k] if alloc[k] > 1 else -1)
    alloc[b] -= 1
while sum(alloc.values()) < TARGET:
    b = max(by_brand, key=lambda k: len(by_brand[k]) - alloc[k])
    alloc[b] += 1

sample = []
for b, n in alloc.items():
    # spread across actives within the brand
    items = sorted(by_brand[b], key=lambda r: r["active"])
    step = max(1, len(items) // n)
    picked = items[::step][:n]
    sample.extend(picked)

sample = sample[:TARGET]
print(f"sample n={len(sample)}  alloc={alloc}")
for r in sample:
    print(f"  {r['barcode']}  {r['brand_bucket']:<8} {r['active']:<12} {r['name_he'][:46]}")

(HERE / "_sample.json").write_text(
    json.dumps({"n": len(sample), "alloc": alloc, "rows": sample},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {HERE/'_sample.json'}")
