"""
Merge + dedup the multi-retailer cereals BSIP1 against the frozen Shufersal baseline
(run_cereals_005, 66 products), TASK-184.

Dedup key = barcode (the transparency-feed EAN is authoritative cross-retailer identity).
A multi-retailer product whose barcode already exists in run_cereals_005 is recorded as a
cross-retailer duplicate (it widens availability, not the corpus). Genuinely NEW barcodes
are copied into a combined BSIP1 dir for BSIP2 scoring.

Output: C:\\Bari\\03_operations\\bsip1\\run_cereals_multiretailer_001\\output\\  (NEW barcodes only)
        + dedup_report.json
"""
from __future__ import annotations
import json, pathlib, shutil
from datetime import datetime, timezone

BASE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_005\output")
RETAILERS = ["carrefour", "yohananof"]
OUT = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output")


def main():
    base_bcs = {str(json.loads(f.read_text(encoding="utf-8")).get("barcode")) for f in BASE.glob("bsip1_*.json")}
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("bsip1_*.json"):
        f.unlink()

    new, dup_vs_base, dup_cross = [], [], []
    seen = set()
    for ret in RETAILERS:
        d = pathlib.Path(rf"C:\Bari\03_operations\bsip1\run_cereals_{ret}_001\output")
        for f in sorted(d.glob("bsip1_*.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            bc = str(j.get("barcode"))
            nm = j.get("canonical_name_he", "")
            if bc in base_bcs:
                dup_vs_base.append({"barcode": bc, "name": nm, "retailer": ret})
                continue
            if bc in seen:
                dup_cross.append({"barcode": bc, "name": nm, "retailer": ret})
                continue
            seen.add(bc)
            j.setdefault("source_retailers", [ret])
            (OUT / f"bsip1_{bc}.json").write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
            new.append({"barcode": bc, "name": nm, "retailer": ret,
                        "subpool": (j.get("cereals_governance", {}).get("construct_1_granola_subpool", {}) or {}).get("subpool")})

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "baseline": "run_cereals_005 (Shufersal, 66 products)",
        "baseline_barcode_count": len(base_bcs),
        "new_unique_count": len(new),
        "duplicate_vs_baseline_count": len(dup_vs_base),
        "duplicate_cross_retailer_count": len(dup_cross),
        "new_products": new,
        "duplicates_vs_baseline": dup_vs_base,
        "duplicates_cross_retailer": dup_cross,
    }
    (OUT.parent / "dedup_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"baseline barcodes: {len(base_bcs)}")
    print(f"NEW unique multi-retailer products: {len(new)}")
    print(f"duplicates vs Shufersal baseline: {len(dup_vs_base)}")
    print(f"cross-retailer duplicates (Carrefour∩Yohananof): {len(dup_cross)}")
    if dup_vs_base:
        print("  overlap with Shufersal:")
        for d in dup_vs_base: print(f"    {d['barcode']} {d['name'][:40]} ({d['retailer']})")


if __name__ == "__main__":
    main()
