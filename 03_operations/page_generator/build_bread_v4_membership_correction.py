"""
bread_frontend_v4.json builder — TASK-433 Follow-up A (orchestrator directive)
MEMBERSHIP CORRECTION ONLY. Zero re-score. Starts from the PUBLISHED, signed-off
bread_frontend_v3.json (NOT from run_bread_conform_002, which is discarded for
shipping because it re-scored and drifted one product -0.8 pts — orchestrator
ruled the 23 survivors' v3 scores are signed-off truth and must not move).

What this script does:
  1. Load bread_frontend_v3.json verbatim.
  2. Remove the 6 cracker product objects (now a standalone category, TASK-433).
  3. For the remaining 23: copy EVERY field byte-identical from v3 EXCEPT:
       - rank: renumbered 1..23 in the existing score-descending order
       - brand: injected via the shared brand_extractor.py helper IF a
         confirmed token literally appears in the product's `name` field AND
         the product does not already carry a brand (never overwrites an
         existing value; never invents beyond the shared helper's token list)
  4. Update _meta.product_count -> 23 and add a run note. All other _meta
     keys carried forward unchanged (run_id/corpus_dirs/flag_vector/engine_sha
     describe the ORIGINAL v3 scoring run, which is still the truth source —
     this file does not re-run scoring, so those provenance fields correctly
     still point at the v3 scoring lineage).
  5. Self-verify: diff every one of the 23 survivors' score+grade in v4 against
     v3 -> must be 0.000 drift / 0 grade moves by construction. Print proof.
"""

from __future__ import annotations
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\03_operations\bsip1\core")
from brand_extractor import extract_brand

V3_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v3.json")
V4_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v4.json")

CRACKERS_REMOVED = {
    "96086000966", "96086000577", "7296073134459",
    "7296073134442", "8434165658523", "74252",
}


def main():
    v3 = json.loads(V3_PATH.read_text(encoding="utf-8"))
    v3_products = v3["products"]
    print(f"v3 total products: {len(v3_products)}")

    survivors_v3 = [p for p in v3_products if str(p.get("barcode")) not in CRACKERS_REMOVED]
    removed = [p for p in v3_products if str(p.get("barcode")) in CRACKERS_REMOVED]
    print(f"crackers removed: {len(removed)} -> {sorted(str(p['barcode']) for p in removed)}")
    print(f"survivors: {len(survivors_v3)}")
    assert len(survivors_v3) == 23, f"expected 23 survivors, got {len(survivors_v3)}"
    assert len(removed) == 6, f"expected 6 removed, got {len(removed)}"

    # Sort by score desc (existing order in v3 is already score-desc; re-derive
    # defensively rather than trust file order, since rank renumbering must be
    # exact).
    def sort_key(p):
        s = p.get("score")
        return (0 if s is None else -s, str(p.get("barcode", "")))

    survivors_sorted = sorted(survivors_v3, key=sort_key)

    brand_report = []
    v4_products = []
    for i, p in enumerate(survivors_sorted, start=1):
        new_p = dict(p)  # shallow copy; nested dicts (expansion, d4_additives) NOT mutated below
        old_rank = new_p.get("rank")
        new_p["rank"] = i

        existing_brand = new_p.get("brand")
        if not existing_brand:
            derived = extract_brand(new_p.get("name"), None)
            if derived:
                new_p["brand"] = derived
                brand_report.append({
                    "barcode": new_p["barcode"], "name": new_p["name"],
                    "brand": derived, "source": "name_literal_match (newly filled)",
                })
        else:
            brand_report.append({
                "barcode": new_p["barcode"], "name": new_p["name"],
                "brand": existing_brand, "source": "already_present_in_v3 (untouched)",
            })

        v4_products.append(new_p)
        print(f"  rank {old_rank}->{i} | {new_p['barcode']} | score={new_p['score']} grade={new_p['grade']} | brand={new_p.get('brand')}")

    # --- Self-verify: byte-identical proof (score + grade) ---
    print("\n=== 23/23 byte-identical proof (v4 vs v3, per barcode) ===")
    zero_drift = 0
    grade_moves = 0
    for new_p, old_p in zip(v4_products, sorted(survivors_v3, key=sort_key)):
        bc = new_p["barcode"]
        score_drift = round((new_p.get("score") or 0) - (old_p.get("score") or 0), 6)
        grade_same = new_p.get("grade") == old_p.get("grade")
        if score_drift == 0:
            zero_drift += 1
        if not grade_same:
            grade_moves += 1
        print(f"  {bc} | v3_score={old_p.get('score')} v4_score={new_p.get('score')} drift={score_drift} | v3_grade={old_p.get('grade')} v4_grade={new_p.get('grade')} same={grade_same}")

    print(f"\nZero-drift count: {zero_drift}/23")
    print(f"Grade moves: {grade_moves}")
    verdict = "PASS — 23/23 byte-identical, 0 grade moves" if zero_drift == 23 and grade_moves == 0 else "FAIL"
    print(f"VERDICT: {verdict}")

    # Also verify full-object byte-identity (every field except rank/brand)
    print("\n=== full-object diff check (fields other than rank/brand) ===")
    full_identical = 0
    for new_p, old_p in zip(v4_products, sorted(survivors_v3, key=sort_key)):
        a = {k: v for k, v in new_p.items() if k not in ("rank", "brand")}
        b = {k: v for k, v in old_p.items() if k not in ("rank", "brand")}
        if a == b:
            full_identical += 1
        else:
            diffs = [k for k in set(list(a.keys()) + list(b.keys())) if a.get(k) != b.get(k)]
            print(f"  {new_p['barcode']}: NON-IDENTICAL fields (excl rank/brand): {diffs}")
    print(f"Full-object identical (excl. rank/brand): {full_identical}/23")

    # --- Build v4 ---
    v4_meta = dict(v3["_meta"])
    v4_meta["product_count"] = 23
    v4_meta["task433_membership_correction"] = (
        "Crackers split to standalone category (TASK-433); membership correction "
        "only, no re-score; 23 survivors byte-identical to bread_frontend_v3.json "
        "(scores/grades/expansion/d4_additives/insightLine/rowVerdict untouched). "
        "6 cracker products removed (barcodes: " + ", ".join(sorted(CRACKERS_REMOVED)) + "). "
        "rank renumbered 1..23 in existing score-desc order. brand injected via "
        "deterministic name-literal-match ONLY where not already present "
        "(brand_extractor.py) — never invented, never overwrote an existing value."
    )

    v4 = {"_meta": v4_meta, "products": v4_products}
    V4_PATH.write_text(
        json.dumps(v4, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"\nWritten: {V4_PATH}")
    print(f"Brand report ({len(brand_report)} entries): {json.dumps(brand_report, ensure_ascii=False)}")

    return zero_drift, grade_moves, full_identical


if __name__ == "__main__":
    zero_drift, grade_moves, full_identical = main()
    ok = (zero_drift == 23 and grade_moves == 0 and full_identical == 23)
    sys.exit(0 if ok else 1)
