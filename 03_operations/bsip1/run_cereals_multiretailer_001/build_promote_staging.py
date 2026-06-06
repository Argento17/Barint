"""
TASK-184 — Build the promote-ready staging dataset for run_cereals_multiretailer_001.

Curation EXCLUSIONS applied for the LIVE promote path (owner directive 2026-06-05 +
both sign-offs):
  1. EV-045c -> flag-AND-DROP: the 6 savory "Fitness" crackers are EXCLUDED (not merely
     flagged). Scoping reuses fitness_noncereal_flag() (the canonical EV-045c rule):
     drop a Fitness-brand SKU IFF the BSIP1 record carries the
     'fitness_savory_cracker_suspect' flag. Genuine Fitness corn flakes / protein granola
     do NOT carry the flag and are retained.
  2. HOLD the 81.2/A "גרנולה בתוספת חלבון" (barcode 7290116532769) OUT (Nutrition: the A is a
     data-completeness artifact).
  3. EXCLUDE BSIP2-insufficient_data products (cannot be displayed as a graded cereal).

Output: BariProductVM-shaped records matching the LIVE schema
(bari-web/src/data/comparisons/cereals_frontend_v1.json), with insightLine + rowVerdict
left EMPTY (Content Agent authors next). Adds a top-level "category" field per record.

This is curation + packaging only. NO score/engine change (engine byte-identical to
run_cereals_005). Does NOT touch bari-web. Reads BSIP1 outputs + BSIP2 traces.
"""
from __future__ import annotations
import json, pathlib

RUN = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001")
BSIP1_OUT = RUN / "output"
BSIP2 = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001\products")
DEDUP = json.loads((RUN / "dedup_report.json").read_text(encoding="utf-8"))
STAGING_OUT = RUN / "promote_staging.json"

HELD_A_BARCODE = "7290116532769"  # owner: hold the 81.2/A out of live

def confidence_for(b1: dict, trace: dict) -> str:
    """verified|partial|insufficient, per data_sufficiency (BSIP2) + ingredient observability."""
    if trace.get("data_sufficiency") == "insufficient":
        return "insufficient"
    # OFF candidate panels: clean ingredient text => verified; macros-only => partial.
    if b1.get("ingredient_text_quality") == "clean" and b1.get("ingredients_list"):
        return "verified"
    return "partial"

def confidence_label(conf: str) -> str:
    return {"verified": "נתונים מלאים", "partial": "נתונים חלקיים",
            "insufficient": "נתונים חסרים"}[conf]

def round_or_none(v):
    return round(v, 1) if isinstance(v, (int, float)) else None

records = []
excluded = {"ev_045c_savory_fitness_cracker": [], "held_A_artifact": [],
            "insufficient_data": []}
counts = {"granola": 0, "standard_cereal": 0}

for p in DEDUP["new_products"]:
    bc = p["barcode"]
    subpool = p["subpool"]
    b1 = json.loads((BSIP1_OUT / f"bsip1_{bc}.json").read_text(encoding="utf-8"))
    cid = b1["canonical_product_id"]
    trace = json.loads((BSIP2 / cid / "bsip2_trace.json").read_text(encoding="utf-8"))
    name = b1["canonical_name_he"]

    # --- EXCLUSION 1: EV-045c flag-AND-DROP (reuse fitness_noncereal_flag scoping) ---
    raw = json.dumps(b1, ensure_ascii=False)
    is_ev045c = "fitness_savory_cracker_suspect" in raw
    if is_ev045c:
        excluded["ev_045c_savory_fitness_cracker"].append({"barcode": bc, "name": name})
        continue

    # --- EXCLUSION 2: held 81.2/A artifact ---
    if bc == HELD_A_BARCODE:
        excluded["held_A_artifact"].append({"barcode": bc, "name": name})
        continue

    # --- EXCLUSION 3: BSIP2 insufficient_data (not displayable as a graded cereal) ---
    if trace.get("data_sufficiency") == "insufficient":
        excluded["insufficient_data"].append({"barcode": bc, "name": name})
        continue

    # --- Build the BariProductVM record ---
    conf = confidence_for(b1, trace)
    nn = b1.get("normalized_nutrition_per_100g", {})
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")
    gov = b1.get("cereals_governance", {})

    # NOTE: sugars are present in OFF panels but the LIVE frozen records carry sugar=null
    # (Shufersal scrape did not expose sugar). We carry the real OFF sugar value here since
    # it is observed data; null only when truly absent.
    nutrition = {
        "energyKcal": round_or_none(nn.get("energy_kcal")),
        "protein": round_or_none(nn.get("protein_g")),
        "sugar": round_or_none(nn.get("sugars_g")),
        "fat": round_or_none(nn.get("fat_g")),
        "fiber": round_or_none(nn.get("dietary_fiber_g")),
        "sodium": round_or_none(nn.get("sodium_mg")),
    }

    # Do NOT fabricate ingredients: empty string when no panel text.
    ingredients = (b1.get("ingredients_text_he") or "").strip()

    category = "granola" if subpool == "granola" else "breakfast-cereals"
    counts[subpool] += 1

    records.append({
        "id": cid,
        "name": name,
        "imageUrl": b1.get("image_url") or "",
        "score": int(round(score)) if isinstance(score, (int, float)) else None,
        "grade": grade,
        "insightLine": "",          # Content Agent authors
        "confidence": conf,
        "expansion": {
            "nutrition": nutrition,
            "ingredients": ingredients,
            "confidenceLabel": confidence_label(conf),
            "servingNote": "ל-100 גרם",
        },
        "rowVerdict": "",           # Content Agent authors
        "_subpool": subpool,
        "_isChildrens": bool(gov.get("construct_2_childrens", {}).get("is_childrens_product", False)),
        "_wholeGrainClaim": bool(gov.get("construct_3_whole_grain", {}).get("whole_grain_claim_present", False)),
        "category": category,
    })

# stable order: granola first then standard, by score desc within each
records.sort(key=lambda r: (r["category"] != "granola", -(r["score"] or 0)))

cat_split = {}
for r in records:
    cat_split[r["category"]] = cat_split.get(r["category"], 0) + 1

staging = {
    "_meta": {
        "run_id": "run_cereals_multiretailer_001",
        "task": "TASK-184",
        "generated_by": "data-agent",
        "schema": "BariProductVM[] (promote staging — insightLine/rowVerdict EMPTY, Content authors)",
        "engine": "proto_v0 algorithm_version 0.4.1, BARI_RECAL_P0=on — byte-identical to run_cereals_005",
        "provenance": "il_prices (Carrefour 7290055700007 / Yochananof 7290455000004) identity + "
                      "Open Food Facts candidate panels (EDPG candidate). Dedup vs run_cereals_005 (66).",
        "promote_count": len(records),
        "promote_split_by_category": cat_split,
        "subpool_split": counts,
        "excluded_for_live": {k: len(v) for k, v in excluded.items()},
        "exclusion_detail": excluded,
        "notes": [
            "EV-045c is enforced flag-AND-DROP here (live promote path): savory Fitness crackers EXCLUDED.",
            "Genuine Fitness corn flakes / protein granola (14.8g fat) are NOT flagged and are RETAINED.",
            "81.2/A 7290116532769 HELD OUT per Nutrition (data-completeness artifact).",
            "ADD-ONLY: the existing 66 live products and their scores are untouched; this stages new products only.",
            "insightLine + rowVerdict are intentionally empty; Content Agent authors before frontend merge.",
        ],
    },
    "products": records,
}

STAGING_OUT.write_text(json.dumps(staging, ensure_ascii=False, indent=2), encoding="utf-8")

print("PROMOTE COUNT:", len(records))
print("SPLIT BY CATEGORY:", cat_split)
print("SUBPOOL SPLIT:", counts)
print("EXCLUDED:", {k: len(v) for k, v in excluded.items()})
print("EV-045c dropped:", [x["barcode"] for x in excluded["ev_045c_savory_fitness_cracker"]])
print("Held A dropped:", [x["barcode"] for x in excluded["held_A_artifact"]])
print("Insufficient dropped:", [x["barcode"] for x in excluded["insufficient_data"]])
# sanity: confirm genuine Fitness retained
ret = {r["id"].replace("bsip1_cereal_",""): r["name"] for r in records}
for bc in ["5900020041142", "7613035758834", "7613033548192", "7613037686906"]:
    print("RETAINED genuine Fitness", bc, "->", ret.get(bc, "*** MISSING ***"))
print("Held A present in staging?", HELD_A_BARCODE in ret)
print("STAGING FILE:", STAGING_OUT)
