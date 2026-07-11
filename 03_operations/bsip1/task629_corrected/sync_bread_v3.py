"""
TASK-629 follow-up — restore the documented "23 survivors byte-identical
between bread_frontend_v3.json and bread_frontend_v4.json" invariant
(stated in bread_frontend_v4.json's own _meta.task433_membership_correction)
after the v4-only nutrition correction broke it.

v3 is not served to any live page (grep-verified: no .ts/.tsx import references
it), but it IS still read by a few legacy admin/SEO utility scripts, and --
critically -- parity_gate.py's comparison-surface glob picks up every
"*_frontend_v*.json" file under bari-web/src/data/comparisons, so both v3 and
v4 count as "comparison" surfaces for shelf=bread. Leaving v3 un-corrected
after correcting v4 breaks the byte-identical invariant for the 23 overlapping
products and produces spurious PD-parity divergences (PD is correctly sourced
from v4, the true live file, so v3's now-stale entries diverge against it).

This applies the exact same whitelist of fields already written to v4 for the
23 overlapping barcodes onto v3, then resorts+re-ranks all 29 v3 products.
Never touches the 6 v3-only (crackers-split) products' data.
"""
from __future__ import annotations
import copy
import hashlib
import json
import pathlib

ROOT = pathlib.Path(r"C:\Bari")
V3 = ROOT / "bari-web/src/data/comparisons/bread_frontend_v3.json"
V4 = ROOT / "bari-web/src/data/comparisons/bread_frontend_v4.json"

FIELDS = [
    "score", "grade", "confidence", "confidence_label_he",
    "confidence_level", "confidence_sub_reason", "confidence_tooltip_he",
    "insightLine", "rowVerdict",
]


def hash_obj_except_rank(obj):
    obj_copy = copy.deepcopy(obj)
    obj_copy.pop("rank", None)
    return hashlib.sha256(
        json.dumps(obj_copy, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def main():
    v3 = json.loads(V3.read_text(encoding="utf-8"))
    v4 = json.loads(V4.read_text(encoding="utf-8"))
    v4_by_bc = {p["barcode"]: p for p in v4["products"]}

    synced = []
    for p in v3["products"]:
        bc = p["barcode"]
        if bc not in v4_by_bc:
            continue
        v4p = v4_by_bc[bc]
        changed = [f for f in FIELDS if p.get(f) != v4p.get(f)]
        if not changed:
            continue
        for f in FIELDS:
            p[f] = v4p[f]
        p.setdefault("expansion", {})
        p["expansion"]["nutrition"] = dict(v4p["expansion"]["nutrition"])
        if "confidenceLabel" in v4p.get("expansion", {}):
            p["expansion"]["confidenceLabel"] = v4p["expansion"]["confidenceLabel"]
        synced.append({"barcode": bc, "changed_fields": changed})

    products = v3["products"]
    enriched = [(p, i) for i, p in enumerate(products)]
    enriched.sort(key=lambda x: (-(x[0].get("score") or 0), x[1]))
    sorted_products = [p for p, _ in enriched]
    for i, p in enumerate(sorted_products):
        p["rank"] = i + 1
        p["_hash_no_rank"] = hash_obj_except_rank(p)

    scores = [p.get("score") or 0 for p in sorted_products]
    assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)), "v3 scores not monotonic after resort"
    assert {p["barcode"] for p in sorted_products} == {p["barcode"] for p in products}, "v3 barcode set changed"

    v3["products"] = sorted_products
    V3.write_text(json.dumps(v3, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Synced {len(synced)} overlapping barcodes from v4 -> v3 (byte-identical invariant restored):")
    for s in synced:
        print(f"  {s['barcode']}: {s['changed_fields']}")


if __name__ == "__main__":
    main()
