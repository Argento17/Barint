"""
Crackers structural finalization — TASK-433 Follow-up B (orchestrator directive)
Adds `rank` (1..20 by score desc) and `_website_cluster` (shelf-filter tag) to
crackers_frontend_v1.json. Structural/data fields only — no copy authored,
no PENDING_COPY fields touched.

_website_cluster assignment is evidence-derived from the BSIP1 ingredient
text (NOT eyeballed): sums the leading percentage of whole-grain flour terms
(כוסמין מלא / חיטה מלא(ה) / שיפון מלא) with an explicit % figure in the
ingredient list. This is exactly the axis the Crackers Category Constitution
v1 Section 3 names as the primary real differentiator on this shelf
("82-98% spelt vs 33-84% refined-flour-dominant").

Clusters (evidence-derived thresholds, not arbitrary):
  whole_grain    — whole-grain flour sum >= 70% (dominant/near-exclusive flour)
  mixed_grain    — whole-grain flour sum > 0% and < 70% (present but blended
                   with refined wheat/rice flour — the "פיטנס"-style diet
                   crackers and the two other-grain blends)
  refined_white  — 0% whole-grain flour detected in ingredients (plain white
                   wheat flour crackers, incl. classic Osem/KRIT-style)

A sesame/seed-forward "seeded" cluster was considered (coordinator suggestion)
but rejected as under-evidenced: only 1/20 products (96086000966, 15% sesame)
has a seed content high enough to plausibly anchor a distinct cluster; the
rest are 0-9% or absent. Forcing a 4th bucket on 1 data point would not be
honest — it stays inside whole_grain (its dominant identity is 82% spelt
flour, sesame is a secondary ingredient at 15%).
"""

from __future__ import annotations
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_PATH = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\crackers_frontend_v1.json")
BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_crackers_conform_001\output")


def whole_grain_pct(ing: str) -> float:
    total = 0.0
    for m in re.finditer(
        r"(כוסמין מלא(?:\s*אורגני)?|חיטה מלא[ה]?|שיפון מלא)\D{0,15}?(\d+(?:\.\d+)?)\s*%",
        ing,
    ):
        total += float(m.group(2))
    return total


def assign_cluster(wg_pct: float) -> str:
    if wg_pct >= 70:
        return "whole_grain"
    if wg_pct > 0:
        return "mixed_grain"
    return "refined_white"


def main():
    data = json.loads(FRONTEND_PATH.read_text(encoding="utf-8"))
    products = data["products"]

    # Load ingredient text from BSIP1 (source of truth for the cluster signal;
    # frontend JSON's expansion.ingredients is the same text but going to the
    # BSIP1 record directly keeps this auditable against the raw enrichment).
    ing_by_bc = {}
    for f in BSIP1_DIR.glob("bsip1_*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        ing_by_bc[r["barcode"]] = r.get("ingredients_text_he") or ""

    # Sort by score desc (None last), barcode asc tiebreak — matches
    # generate_page.py's own sort convention.
    def sort_key(p):
        s = p.get("score")
        return (0 if s is None else -s, p.get("barcode", ""))

    products_sorted = sorted(products, key=sort_key)

    cluster_counts = {"whole_grain": 0, "mixed_grain": 0, "refined_white": 0}
    report = []
    for i, p in enumerate(products_sorted, start=1):
        p["rank"] = i
        bc = p["barcode"]
        ing = ing_by_bc.get(bc, "")
        wg = whole_grain_pct(ing)
        cluster = assign_cluster(wg)
        p["_website_cluster"] = cluster
        cluster_counts[cluster] += 1
        report.append({"rank": i, "barcode": bc, "score": p.get("score"), "whole_grain_pct": wg, "cluster": cluster})
        print(f"  rank={i:2d} | {bc:15s} | score={p.get('score')} | wg%={wg:5.1f} | cluster={cluster}")

    # KRIT — leave brand null per explicit orchestrator instruction (unsourced,
    # not reproducible from any scrape; do not carry forward the hand-entered
    # v3 value).
    krit_bc = "8434165658523"
    krit_p = next((p for p in products_sorted if p["barcode"] == krit_bc), None)
    if krit_p is not None:
        assert krit_p.get("brand") in (None, ""), f"KRIT brand unexpectedly set: {krit_p.get('brand')}"
        print(f"\nKRIT check ({krit_bc}): brand={krit_p.get('brand')!r} — confirmed null, not carried forward from v3 (unsourced).")

    data["products"] = products_sorted
    data["_meta"]["task433_structural_finalization"] = (
        "rank (1..20, score desc) and _website_cluster added — structural/data "
        "fields only, no copy authored. _website_cluster derived from "
        "whole-grain-flour-percentage evidence in BSIP1 ingredients_text_he "
        "(sum of explicit % for כוסמין מלא/חיטה מלא(ה)/שיפון מלא terms): "
        "whole_grain >=70%, mixed_grain >0% and <70%, refined_white =0%. "
        f"Cluster counts: {cluster_counts}. KRIT (8434165658523) brand left "
        "null — the pre-existing bread_frontend_v3.json 'KRIT' value is "
        "unsourced (not derivable from any scrape/BSIP0/BSIP1 artifact) and "
        "was NOT carried forward, per reproducibility rule."
    )

    FRONTEND_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"\nCluster counts: {cluster_counts}")
    print(f"Total: {sum(cluster_counts.values())}/20")
    print(f"\nWritten: {FRONTEND_PATH}")


if __name__ == "__main__":
    main()
