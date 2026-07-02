"""
Write candidate _baselines/<category>/baseline_manifest.json for 6 failing categories.
Phase 0 Step 2: define canonical flag vectors, document archaeology, write artifacts.
"""
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("C:/Bari")
BASELINES_DIR = REPO / "_baselines"
BASELINES_DIR.mkdir(exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

now = datetime.now(timezone.utc).isoformat(timespec="seconds")

manifests = {
    "bread": {
        "slug": "bread",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline manifest for bread. Archaeology determined live scores "
            "include D4 surgical patch (commit 361748722, 2026-06-22). Flag BARI_D4_SCORE_V1 "
            "is LEGITIMATE — applied to all live pages; must be in canonical engine."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_bread_conform_001\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\bread_frontend_v3.json",
        "canonical_flag_vector": {
            "BARI_RECAL_P0": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off"
        },
        "flag_classification": {
            "BARI_D4_SCORE_V1": "LEGITIMATE — surgically applied to live JSON 2026-06-22 (commit 361748722); all live pages include D4 penalties",
            "BARI_RECAL_P0": "LEGITIMATE — grain/non-dairy flag, mirrors cereals precedent",
            "BARI_FAT_TECH_V1": "LEGITIMATE — default active engine flag"
        },
        "phantom_flags": [],
        "shelf_rel": None,
        "corpus_dir_pointer_correct": True,
        "corpus_dir_note": "run_bread_conform_001 is the correct BSIP1 dir (verified: all 29 barcodes present)",
        "reproduce_result": {
            "matched": 28,
            "total": 29,
            "match_rate": "28/29",
            "remaining_diff": {
                "7290016245325": {
                    "live": 94.8, "canonical": 94.0, "diff": 0.8,
                    "cause": "engine_drift_pre_d4 — scored at engine state circa 2026-06-18 (run_bread_conform_001); current engine gives 94.0; sugars_g=null in BSIP1",
                    "grade_move": False
                }
            }
        },
        "residual_notes": [
            "1 product (7290016245325) has 0.8 diff — genuine engine drift (scored in earlier engine state). No grade move. BSIP1 sugars_g=None; current engine computes 94.0."
        ],
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    },

    "cakes": {
        "slug": "cakes",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline for cakes. Archaeology: 26 products had exactly -8pt D4 penalty "
            "(cap reached) applied via surgical patch (361748722). Missing flag = BARI_D4_SCORE_V1. "
            "Classification: LEGITIMATE. 3 residual movers from post-patch engine change."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cakes_001\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\cakes_hard_cookies_frontend_v1.json",
        "canonical_flag_vector": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_RECAL_P0": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off"
        },
        "flag_classification": {
            "BARI_D4_SCORE_V1": "LEGITIMATE — 26 products had 8pt (cap) penalty applied surgically; this was the missing flag causing 26/54 config-class mismatches",
            "BARI_SHELF_RELATIVE_V1": "LEGITIMATE — sugars shelf-relative with pinned median=29.0, scale=9.044",
            "BARI_FAT_TECH_V1": "LEGITIMATE — default active"
        },
        "phantom_flags": [],
        "shelf_rel": {"nutrient": "sugars_g", "median": 29.0, "scale": 9.044, "scale_type": "iqr"},
        "bsip1_glob": "bsip1_cakes_*.json",
        "corpus_dir_pointer_correct": True,
        "reproduce_result": {
            "matched": 62,
            "total": 65,
            "match_rate": "62/65",
            "remaining_diff": {
                "1361177": {"live": 7.9, "canonical": 9.9, "diff": 2.0, "cause": "engine_drift — D4 engine changed between surgical patch (June 22) and current state; this product had 3 contested additives in old engine, current engine computes differently", "grade_move": False},
                "5718038": {"live": 17.5, "canonical": 18.9, "diff": 1.4, "cause": "engine_drift — same as 1361177", "grade_move": False},
                "7290123330884": {"live": 9.6, "canonical": 9.8, "diff": 0.2, "cause": "rounding/float noise", "grade_move": False}
            }
        },
        "residual_notes": [
            "2 products have small engine drift from D4 calculation change post-patch (1.4-2.0 diff). No grade moves.",
            "1 product has 0.2 rounding diff. All 3 are E-grade — no consumer impact."
        ],
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    },

    "cereals": {
        "slug": "cereals",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline for cereals. Archaeology: live page scored in 3 stages: "
            "(1) run_cereals_008 with RECAL_P0+FAT_TECH; (2) D4 surgical patch (361748722); "
            "(3) TASK-387 GRAN_SUGAR_25G rescore (189ee1589, 2026-06-24) with flags "
            "RECAL_P0+FAT_TECH+GRAN_SUGAR_25G (SODIUM_CEREAL was explicitly OFF per task387 script). "
            "Config correctly points to run_cereals_008. Residual 6 movers are engine-state "
            "mismatches from multi-stage scoring compound."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cereals_008\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\cereals_frontend_v2.json",
        "canonical_flag_vector": {
            "BARI_RECAL_P0": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_GRAN_SUGAR_25G_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off"
        },
        "flag_classification": {
            "BARI_GRAN_SUGAR_25G_V1": "LEGITIMATE — Nutrition GO + Product D7 co-signed (TASK-387); 1 grade mover in rescore (ריבועי קינמון D->E); applied 2026-06-24",
            "BARI_D4_SCORE_V1": "LEGITIMATE — surgical patch applied",
            "BARI_SODIUM_CEREAL": "OFF — batch_run_cereals_task387_25g.py line 13 explicitly states 'live cereals page does NOT use this flag'; CONFIRMED",
            "BARI_RECAL_P0": "LEGITIMATE — grain flag"
        },
        "phantom_flags": [],
        "shelf_rel": None,
        "corpus_dir_pointer_correct": True,
        "corpus_dir_note": "Config correctly points to run_cereals_008. The live page _meta.run_id=run_cereals_task387_25g refers to the rescore run, not the BSIP1 source.",
        "reproduce_result": {
            "matched": 14,
            "total": 20,
            "match_rate": "14/20",
            "remaining_diff_summary": "6 products at 0.7-2.8 diff — engine-state drift from multi-stage scoring (D4 patch applied before GRAN_SUGAR rescore; compound effect)",
            "grade_movers": 0
        },
        "residual_notes": [
            "6 products have 0.7-2.8 diff from engine-state compound. No grade moves.",
            "The config.json currently has SODIUM_CEREAL=off which is CORRECT (task387 script confirms).",
            "GRAN_SUGAR_25G_V1 needs to be ADDED to the config. It is currently absent."
        ],
        "config_update_needed": "ADD BARI_GRAN_SUGAR_25G_V1=on to configs/cereals.json scoring.flags",
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    },

    "cheese": {
        "slug": "cheese",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline for cheese-spreads. Archaeology: 10/10 config-class mismatches "
            "resolved by adding BARI_D4_SCORE_V1=on (D4 surgical patch). 9 remaining 'engine' "
            "class mismatches (all 2.2 diff) are genuine pre-D4 engine drift — scored at "
            "engine state 2026-06-17, current engine gives 2.2 lower for 9 E450-containing products."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cheese_003\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\cheese_frontend_v4.json",
        "canonical_flag_vector": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off"
        },
        "flag_classification": {
            "BARI_D4_SCORE_V1": "LEGITIMATE — surgical patch applied; resolves all 10 config-class mismatches (10/10 match at 0.0)",
            "BARI_SHELF_RELATIVE_V1": "LEGITIMATE — fat_saturated shelf-relative with pinned median=16.05, scale=2.0756",
            "BARI_RECAL_P0": "LEGITIMATE — dairy recalibration flag"
        },
        "phantom_flags": [],
        "shelf_rel": {"nutrient": "fat_saturated_g", "median": 16.05, "scale": 2.0756, "scale_type": "iqr"},
        "corpus_dir_pointer_correct": True,
        "reproduce_result": {
            "matched": 44,
            "total": 53,
            "match_rate": "44/53",
            "remaining_diff_summary": "9 products all at 2.2 diff (engine drift, not flag diff). All contain E450 (phosphates, dose-dependent tier). Scored June 17 at older engine state.",
            "grade_movers": 0
        },
        "residual_notes": [
            "9 products with E450 (dose-dependent) have 2.2 engine drift — pre-D4 scoring, not fixable by any current flag.",
            "All 9 are DOWN moves (live=higher). No grade moves. No consumer impact.",
            "This drift predates the D4 surgical patch — existed in the initial 95257faca conform commit."
        ],
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    },

    "granola": {
        "slug": "granola",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline for granola. Archaeology: 1 mismatch (7290017962023, diff=1.5) "
            "is a data fix — BSIP1 has sugars_g=None but live score (69.4/B) was computed with "
            "actual sugar content from TASK-377 audit (453729c2e). BSIP1 stale data. "
            "D4 applied (0 contested additives in this product). Config correctly points to run_cereals_005."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cereals_005\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\granola_frontend_v1.json",
        "canonical_flag_vector": {
            "BARI_RECAL_P0": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off"
        },
        "flag_classification": {
            "BARI_D4_SCORE_V1": "LEGITIMATE — surgical patch applied (0 contested additives in sole mismatch product)",
            "BARI_RECAL_P0": "LEGITIMATE — grain flag"
        },
        "phantom_flags": [],
        "shelf_rel": None,
        "corpus_dir_pointer_correct": True,
        "reproduce_result": {
            "matched": 21,
            "total": 22,
            "match_rate": "21/22",
            "remaining_diff": {
                "7290017962023": {
                    "live": 69.4, "canonical": 70.9, "diff": 1.5,
                    "cause": "BSIP1 data gap — sugars_g=None in run_cereals_005/bsip1_7290017962023.json. Live score used corrected sugar data from TASK-377 audit (commit 453729c2e). Engine gives 70.9 (zero-sugar), live has 69.4 (6g sugar penalizes glycemic score).",
                    "grade_move": False,
                    "data_fix_needed": "Update BSIP1 record sugars_g from None to actual value (granola TASK-377 sourced this)"
                }
            }
        },
        "residual_notes": [
            "1 product has stale BSIP1 data (sugars_g=None). Live score used corrected sugar. BSIP1 needs update to close this gap.",
            "No grade move. granola #1 position unaffected."
        ],
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    },

    "milk": {
        "slug": "milk",
        "generated_at": now,
        "task": "TASK-395",
        "phase": "Phase-0-Step-2",
        "description": (
            "Canonical baseline for milk. Archaeology: 2/3 mismatches resolved by D4=on "
            "(surgical patch). 1 remaining (7290014760141, almond milk) is a real data correction: "
            "BSIP1 has sugars_g=None, but live score was updated to 49.7/D via TASK-378 "
            "(commit 0938ab04f) after Shufersal re-scrape confirmed 6g sugar. This is a "
            "deliberate data-fix that the BSIP1 does not reflect — causes grade move in canonical "
            "(engine gives C, live has D). Escalation item."
        ),
        "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_milk_002\\output",
        "baseline_json": "C:\\Bari\\bari-web\\src\\data\\comparisons\\milk_frontend_v1.json",
        "canonical_flag_vector": {
            "BARI_FAT_TECH_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_RECAL_P0": "off",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_REDLABEL_V1": "off",
            "BARI_DAIRY_SAT_FAT_INFER": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_CEREAL": "off"
        },
        "flag_classification": {
            "BARI_D4_SCORE_V1": "LEGITIMATE — surgical patch applied; resolves 2/3 mismatches",
            "BARI_SHELF_RELATIVE_V1": "LEGITIMATE — per MILK_CANONICAL_FLAGS (run_006_shelfrel_refreeze)"
        },
        "phantom_flags": [],
        "shelf_rel": None,
        "corpus_dir_pointer_correct": True,
        "reproduce_result": {
            "matched": 17,
            "total": 18,
            "match_rate": "17/18",
            "remaining_diff": {
                "7290014760141": {
                    "live": 49.7, "canonical": 51.5, "diff": 1.8,
                    "cause": "DATA FIX — BSIP1 sugars_g=None causes engine to score as C (51.5). Live page corrected to 49.7/D via TASK-378 (commit 0938ab04f) after real-label sugar re-scrape confirmed 6g sugar. BSIP1 must be updated for true reproducibility.",
                    "grade_move": True,
                    "grade_direction": "canonical=C, live=D",
                    "escalation": "BSIP1 data update needed for milk almond product"
                }
            }
        },
        "residual_notes": [
            "1 product (almond milk 7290014760141) has a GRADE MOVE in canonical (C) vs live (D).",
            "Cause: BSIP1 stale data (sugars_g=None), live was manually corrected.",
            "This is a not_done item: BSIP1 must be updated with correct sugar before canonical is clean.",
            "Escalate: BSIP1 data update for run_milk_002 almond milk product."
        ],
        "score_tolerance": 0.05,
        "engine_version_at_rescore": "c90d49ef6 (2026-06-23)",
        "spec_conflict_flag": None
    }
}

# Write manifests and compute hashes
for slug, manifest in manifests.items():
    out_dir = BASELINES_DIR / slug
    out_dir.mkdir(exist_ok=True)
    # Add sha256 of baseline_json
    baseline_path = Path(manifest["baseline_json"])
    if baseline_path.exists():
        manifest["baseline_json_sha256"] = sha256_file(baseline_path)
    out_path = out_dir / "baseline_manifest.json"
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {out_path}")

print("\nAll 6 baseline manifests written.")
