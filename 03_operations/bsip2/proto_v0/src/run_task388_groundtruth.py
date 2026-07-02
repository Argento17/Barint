#!/usr/bin/env python3
"""
TASK-388 — Ground-truth phosphate impact, using the ENGINE'S OWN detector.

Reconciles the 89-vs-35 discrepancy between the two prior measurement passes.
Root cause found by orchestrator: the prior calibrated script matched phosphate
via Hebrew words ONLY (match_patterns_he), but the real engine
detect_additives_d4() matches BOTH the E-number form (e450 / e-450 / ה-450)
AND the Hebrew words. So the prior pass under-counted (missed "E450"/"450").

This script calls the real detect_additives_d4() so detection is engine-faithful,
then measures the incremental -1 phosphate penalty on the live displayed corpus.

EXPLORE only: no score changed, no flag flipped, no JSON edited.
Output: C:\\Bari\\_task388_groundtruth.json
"""
from __future__ import annotations
import json, os, sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SRC = Path(__file__).resolve().parent
os.chdir(SRC); sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from score_engine import detect_additives_d4

LIVE_MANIFEST = REPO / "03_operations" / "spine" / "live_manifest.json"

# Same BSIP1 source map the agent + run_task371 used.
BSIP1_SOURCES = {
    "brined_cheeses":    [("03_operations/bsip1/run_brined_cheeses_002/output", "bsip1_brinedcheese_*.json")],
    "cakes":             [("03_operations/bsip1/run_cakes_001/output", "bsip1_cakes_*.json")],
    "breakfast-cereals": [("03_operations/bsip1/run_cereals_008/output", "*.json")],
    "cheese-spreads":    [("03_operations/bsip1/run_cheese_003/output", "*.json")],
    "cookies_coffee":    [("03_operations/bsip1/run_cookies_001/output", "*.json"),
                          ("03_operations/bsip1/run_cakes_001/output",   "*.json")],
    "granola":           [("03_operations/bsip1/run_cereals_005/output", "*.json")],
    "hard_cheeses":      [("02_products/hard_cheeses/bsip1_outputs",     "*.json")],
    "hummus":            [("02_products/hummus/canonical_bsip1",          "*.json")],
    "juices":            [("02_products/juices/bsip1_outputs",            "*.json")],
    "milk":              [("03_operations/bsip1/run_milk_002/output",     "*.json")],
    "snacks":            [("03_operations/bsip1/run_001/output",          "*.json")],
    "bread":             [("03_operations/bsip1/run_bread_conform_001/output", "*.json")],
}

def _grade(s):
    if s is None: return "?"
    s = float(s)
    return "S" if s>=90 else "A" if s>=80 else "B" if s>=65 else "C" if s>=50 else "D" if s>=35 else "E"

def build_index():
    idx = {}
    for _cat, sources in BSIP1_SOURCES.items():
        for rel, glob in sources:
            d = REPO / rel
            if not d.exists(): continue
            for f in d.glob(glob):
                try:
                    p = json.loads(f.read_text(encoding="utf-8"))
                    bc = str(p.get("barcode","") or "").strip()
                    ing = p.get("ingredients_text_he") or p.get("ingredients_raw") or ""
                    if bc and ing and len(ing) > 3 and bc not in idx:
                        idx[bc] = ing
                except Exception:
                    pass
    return idx

def load_live():
    man = json.loads(LIVE_MANIFEST.read_text(encoding="utf-8"))
    seen = {}
    for f in man.get("files", []):
        path = Path(f["path"])
        if path.exists():
            seen[f["category"]] = path
    out = []
    for cat in sorted(seen):
        data = json.loads(seen[cat].read_text(encoding="utf-8"))
        prods = data.get("products", data if isinstance(data, list) else [])
        for p in prods:
            if not isinstance(p, dict): continue
            bc = str(p.get("barcode") or p.get("id") or "").strip()
            score = p.get("score") or p.get("bariScore")
            grade = p.get("grade") or p.get("bariGrade") or (_grade(score) if score is not None else "?")
            name = p.get("name") or p.get("productName") or bc or "?"
            out.append({"barcode": bc, "name": name, "category": cat,
                        "score": score, "grade": grade})
    return out

def main():
    idx = build_index()
    prods = load_live()
    total = len(prods)
    matched = 0
    no_ing = []
    phos_eng = []          # engine-faithful (E-number OR Hebrew)
    phos_hebrew_only = []  # what the prior pass would catch (name_he source present)
    phos_enum_only = []    # only catchable via E-number (the missed set)
    movers = []
    cat_phos = defaultdict(int); cat_total = defaultdict(int)
    rows = []

    for p in prods:
        cat_total[p["category"]] += 1
        ing = idx.get(p["barcode"], "")
        if not ing:
            no_ing.append(p["barcode"]);
            continue
        matched += 1
        findings = detect_additives_d4(ing)
        e450 = next((f for f in findings if f["e_number"] == "E450"), None)
        if not e450:
            continue
        phos_eng.append(p["barcode"])
        cat_phos[p["category"]] += 1
        src = e450["match_source"]   # 'e_number' | 'name_he' | 'both'
        if src in ("name_he", "both"):
            phos_hebrew_only.append(p["barcode"])
        if src == "e_number":
            phos_enum_only.append(p["barcode"])
        if p["score"] is not None:
            new = round(max(0.0, float(p["score"]) - 1), 1)
            ng = _grade(new)
            row = {"barcode": p["barcode"], "name": p["name"], "category": p["category"],
                   "score_off": p["score"], "grade_off": p["grade"],
                   "score_on": new, "grade_on": ng, "match_source": src,
                   "grade_change": p["grade"] != ng}
            rows.append(row)
            if p["grade"] != ng:
                movers.append(row)

    dist_off = dict(sorted(Counter(p["grade"] for p in prods).items()))
    dist_on = Counter(p["grade"] for p in prods)
    for m in movers:
        dist_on[m["grade_off"]] -= 1; dist_on[m["grade_on"]] += 1
    dist_on = dict(sorted(dist_on.items()))

    result = {
        "corpus_total": total,
        "matched_to_ingredients": matched,
        "unmatched_no_ingredient_text": total - matched,
        "phosphate_engine_faithful": len(phos_eng),
        "phosphate_hebrew_word_match": len(phos_hebrew_only),
        "phosphate_only_via_enumber_MISSED_by_prior_pass": len(phos_enum_only),
        "grade_movers_count": len(movers),
        "baseline_grade_dist": dist_off,
        "phosphate_minus1_grade_dist": dist_on,
        "phosphate_by_category": {c: f"{cat_phos[c]}/{cat_total[c]}" for c in sorted(cat_total)},
        "grade_movers": movers,
        "all_phosphate_rows_count": len(rows),
    }
    with open(r"C:\Bari\_task388_groundtruth.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    # ascii-safe console summary
    print("corpus_total:", total, "matched:", matched, "unmatched:", total-matched)
    print("phosphate ENGINE-FAITHFUL:", len(phos_eng))
    print("phosphate hebrew-word match (prior pass would catch):", len(phos_hebrew_only))
    print("phosphate ONLY via E-number (prior pass MISSED):", len(phos_enum_only))
    print("grade movers (-1):", len(movers))
    print("by category:", {c: f"{cat_phos[c]}/{cat_total[c]}" for c in sorted(cat_total) if cat_phos[c]})
    return 0

if __name__ == "__main__":
    sys.exit(main())
