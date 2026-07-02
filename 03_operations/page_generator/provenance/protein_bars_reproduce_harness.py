# -*- coding: utf-8 -*-
"""TASK-457 / P462 — Protein bars canonical reproduction harness.
Scores the 32 published protein_combined_frontend_v2 barcodes via the uniform
score_engine path (apply_protein_bar_lens wired in score_product), applies
grade-boundary proportionality, diffs vs live baseline, emits Rule-7 flat table.
"""
from __future__ import annotations

import csv
import importlib
import json
import os
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
SRC = REPO / "03_operations/bsip2/proto_v0/src"
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CORPUS_PATH = REPO / "02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json"
BASELINE_JSON = REPO / "bari-web/src/data/comparisons/protein_combined_frontend_v2.json"
FLAT_TABLE_OUT = REPO / "_rescore_staging/protein_bars_gate_b_flat_table.csv"
RESULT_JSON = REPO / "_rescore_staging/protein_bars_gate_b_result.json"

CANONICAL_FLAGS = {
    "BARI_PROTEIN_BAR_V1": "on",
    "BARI_SHELF_RELATIVE_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_RECAL_P0": "off",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
    # Published page (2026-06-21) used engine defaults FAT_TECH=on, W4=on (config off stale).
    "BARI_FAT_TECH_V1": "on",
    "BARI_GLASSBOX_W4": "on",
    "BARI_FIBER_FERMENT_V1": "off",
    "BARI_D4_SCORE_V1": "off",
}

ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1", "BARI_SODIUM_SHELF_RELATIVE_V1", "BARI_FAT_TECH_V1",
    "BARI_RECAL_P0", "BARI_RECAL_P0_YOGURT_TRIM", "BARI_GRAD_SODIUM_V1",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1", "BARI_REDLABEL_V1", "BARI_SODIUM_CEREAL",
    "BARI_D4_SCORE_V1", "BARI_PROTEIN_BAR_V1", "BARI_GLASSBOX_W4", "BARI_FIBER_FERMENT_V1",
    "BARI_GLASSBOX_W2", "BARI_GLASSBOX_D5D6", "BARI_GLASSBOX_W15", "BARI_HC_DAIRY_SATFAT_V1",
]


def load_json(p: Path) -> dict:
    return json.loads(p.read_bytes().decode("utf-8", "replace"))


def apply_flags(flags: dict) -> None:
    for k in ALL_FLAGS:
        os.environ[k] = "off"
    for k, v in flags.items():
        os.environ[k] = str(v)


def reload_engine():
    import constants
    import score_engine
    import nova_proxy
    import signal_extractor
    importlib.reload(constants)
    importlib.reload(nova_proxy)
    importlib.reload(signal_extractor)
    return importlib.reload(score_engine)


def adapt_corpus_product(product: dict) -> dict:
    adapted = dict(product)
    if "canonical_name_he" not in adapted:
        adapted["canonical_name_he"] = product.get("name", "")
    if "product_name_he" not in adapted:
        adapted["product_name_he"] = product.get("name", "")
    nn = product.get("nutrition_per_100g", {})
    if nn and "normalized_nutrition_per_100g" not in adapted:
        adapted["normalized_nutrition_per_100g"] = nn
    if "ingredients_text_he" not in adapted:
        adapted["ingredients_text_he"] = product.get("ingredients_full", "")
    if "ingredients_raw" not in adapted:
        adapted["ingredients_raw"] = product.get("ingredients_full", "")
    return adapted


def make_scorer(eng):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope

    def score_one(rec: dict) -> dict | None:
        sig = extract_signals(rec)
        cat = classify_category(rec)
        nov = infer_nova(rec, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(rec, cat["category"])
        return eng.score_product(rec, sig, cat, nov, ev)

    return score_one


def binding_caps_str(res: dict) -> str:
    caps = []
    for c in res.get("protein_bar_caps", []):
        caps.append(c.get("rule", ""))
    bc = res.get("binding_cap")
    if bc is not None:
        caps.append(f"BASE_CAP_{bc}")
    return "|".join(caps) if caps else "none"


def main() -> int:
    apply_flags(CANONICAL_FLAGS)
    eng = reload_engine()
    score_one = make_scorer(eng)

    pub = load_json(BASELINE_JSON)
    pub_by_bc = {
        str(p["barcode"]).strip(): p
        for p in pub["products"]
        if p.get("barcode")
    }

    corpus = load_json(CORPUS_PATH)
    corpus_by_bc = {str(p["barcode"]).strip(): p for p in corpus["products"]}

    scored_rows: list[dict] = []
    errors = 0
    for bc, pub_p in pub_by_bc.items():
        raw = corpus_by_bc.get(bc)
        if raw is None:
            errors += 1
            continue
        rec = adapt_corpus_product(raw)
        try:
            res = score_one(rec)
        except Exception as e:
            errors += 1
            print(f"ERROR {bc}: {e}")
            continue
        if not res or res.get("final_score_estimate") is None:
            errors += 1
            continue
        is_pb = bool(res.get("protein_bar_lens_applied"))
        scored_rows.append({
            "barcode": bc,
            "name": pub_p.get("name", raw.get("name", "")),
            "score": res["final_score_estimate"],
            "grade": res.get("grade_estimate"),
            "is_protein_bar": bool(is_pb),
            "binding_caps": binding_caps_str(res),
            "nova": None,
            "fat": (rec.get("normalized_nutrition_per_100g") or {}).get("fat_g"),
            "sodium": (rec.get("normalized_nutrition_per_100g") or {}).get("sodium_mg"),
            "context_flag": res.get("context_flag"),
            "pub_score": pub_p.get("score"),
            "pub_grade": pub_p.get("grade"),
            "_raw_result": res,
        })

    scored_rows = eng.apply_protein_bar_grade_proportionality(scored_rows)

    matches = 0
    mismatches: list[dict] = []
    for row in scored_rows:
        ps, pg = row["pub_score"], row["pub_grade"]
        es, eg = row["score"], row["grade"]
        if es == ps and eg == pg:
            matches += 1
        else:
            mismatches.append({
                "barcode": row["barcode"],
                "name": row["name"],
                "pub_score": ps,
                "engine_score": es,
                "pub_grade": pg,
                "engine_grade": eg,
            })

    grades = [r["grade"] for r in scored_rows if r.get("grade")]
    grade_hist = dict(sorted(Counter(grades).items()))
    scores = [float(r["score"]) for r in scored_rows]
    grade_stdev = statistics.pstdev([ord(g) for g in grades]) if len(grades) > 1 else 0.0
    mc_grade, mc_count = Counter(grades).most_common(1)[0] if grades else (None, 0)

    FLAT_TABLE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with FLAT_TABLE_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["barcode", "score", "grade", "binding_caps", "nova", "fat", "sodium", "context_flag"])
        for row in sorted(scored_rows, key=lambda r: -r["score"]):
            w.writerow([
                row["barcode"], row["score"], row["grade"],
                row["binding_caps"], row["nova"], row["fat"], row["sodium"],
                row["context_flag"],
            ])

    total = len(pub_by_bc)
    passed = matches == total and errors == 0 and len(mismatches) == 0
    summary = {
        "gate": "B",
        "flag": "BARI_PROTEIN_BAR_V1=on",
        "published_count": total,
        "scored_count": len(scored_rows),
        "exact_match_score_grade": f"{matches}/{total}",
        "errors": errors,
        "PASS": passed,
        "grade_dist": grade_hist,
        "grade_stdev": round(grade_stdev, 4),
        "most_common_grade": f"{mc_grade}({mc_count})",
        "score_min": min(scores) if scores else None,
        "score_max": max(scores) if scores else None,
        "score_median": statistics.median(scores) if scores else None,
        "score_stdev": round(statistics.pstdev(scores), 4) if len(scores) > 1 else 0.0,
        "mismatches": mismatches,
        "flat_table": str(FLAT_TABLE_OUT),
    }
    RESULT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if mismatches:
        print("\nMISMATCH TABLE:")
        for m in mismatches:
            print(f"  {m['barcode']} pub={m['pub_score']}/{m['pub_grade']} "
                  f"engine={m['engine_score']}/{m['engine_grade']} {m['name'][:40]}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())