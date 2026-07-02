"""
Update _baselines/_ledger_v1.json with Phase 0 canonical rescore results.
"""
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("C:/Bari")
ledger_path = REPO / "_baselines" / "_ledger_v1.json"
results_path = REPO / "_baselines" / "rescore_results_v1.json"

results = json.loads(results_path.read_text(encoding="utf-8"))
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

now = datetime.now(timezone.utc).isoformat(timespec="seconds")

# categories is a LIST - build a slug->index map
cat_index = {}
for i, cat in enumerate(ledger["categories"]):
    cat_index[cat["slug"]] = i

updates = {
    "bread": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["bread"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_bread_conform_001\\output",
            "baseline_sha256": results["baseline_sha256"].get("bread"),
            "matched": 28, "total": 29,
            "movers": 1, "grade_movers": 0, "up_moves": 0, "down_moves": 1,
            "diff_min": 0.8, "diff_med": 0.8, "diff_max": 0.8, "diff_sd": 0.0,
            "residual_cause": "engine_drift_pre_d4 — 0.8 for barcode 7290016245325 (sugars_g=None in BSIP1)",
            "phantom_flags": [],
            "spec_conflict": "BARI_D4_SCORE_V1 reclassified from de-chain to LEGITIMATE (surgical patch 361748722)"
        }
    },
    "cakes": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["cakes"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cakes_001\\output",
            "baseline_sha256": results["baseline_sha256"].get("cakes"),
            "matched": 62, "total": 65,
            "movers": 3, "grade_movers": 0, "up_moves": 3, "down_moves": 0,
            "diff_min": 0.2, "diff_med": 1.4, "diff_max": 2.0, "diff_sd": 0.917,
            "residual_cause": "engine_drift — 3 E-grade products; no grade moves",
            "missing_flag_found": "BARI_D4_SCORE_V1 — resolved 26-product/8pt gap; classified LEGITIMATE",
            "phantom_flags": [],
            "spec_conflict": "BARI_D4_SCORE_V1 reclassified from de-chain to LEGITIMATE"
        }
    },
    "cereals": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["cereals"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cereals_008\\output",
            "baseline_sha256": results["baseline_sha256"].get("cereals"),
            "matched": 14, "total": 20,
            "movers": 6, "grade_movers": 0, "up_moves": 4, "down_moves": 2,
            "diff_min": 0.7, "diff_med": 1.45, "diff_max": 2.8, "diff_sd": 0.857,
            "residual_cause": "engine_state_compound — multi-stage scoring drift (D4 patch before GRAN_SUGAR rescore); 0.7-2.8; no grade moves",
            "missing_flags_found": "BARI_GRAN_SUGAR_25G_V1 — absent from configs/cereals.json; LEGITIMATE per TASK-387 D7",
            "phantom_flags": [],
            "config_update_needed": "ADD BARI_GRAN_SUGAR_25G_V1=on to configs/cereals.json",
            "spec_conflict": "BARI_D4_SCORE_V1 reclassified; BARI_SODIUM_CEREAL confirmed OFF (task387 batch script line 13)"
        }
    },
    "cheese-spreads": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["cheese"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cheese_003\\output",
            "baseline_sha256": results["baseline_sha256"].get("cheese"),
            "matched": 44, "total": 53,
            "movers": 9, "grade_movers": 0, "up_moves": 0, "down_moves": 9,
            "diff_min": 2.2, "diff_med": 2.2, "diff_max": 2.2, "diff_sd": 0.0,
            "residual_cause": "engine_drift_pre_d4 — 9 E450-containing products scored June 17; uniform 2.2 down-drift; no grade moves",
            "phantom_flags": [],
            "spec_conflict": "BARI_D4_SCORE_V1 reclassified from de-chain to LEGITIMATE"
        }
    },
    "granola": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["granola"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_cereals_005\\output",
            "baseline_sha256": results["baseline_sha256"].get("granola"),
            "matched": 21, "total": 22,
            "movers": 1, "grade_movers": 0, "up_moves": 1, "down_moves": 0,
            "diff_min": 1.5, "diff_med": 1.5, "diff_max": 1.5, "diff_sd": 0.0,
            "residual_cause": "data_gap — barcode 7290017962023 sugars_g=None in BSIP1; live score used TASK-377 corrected data",
            "phantom_flags": [],
            "bsip1_data_update_needed": "run_cereals_005: barcode 7290017962023 sugars_g"
        }
    },
    "milk": {
        "status": "CANONICAL_BASELINE_CANDIDATE",
        "task395_phase0": {
            "run_at": now,
            "canonical_flags": results["canonical_flags"]["milk"],
            "bsip1_dir": "C:\\Bari\\03_operations\\bsip1\\run_milk_002\\output",
            "baseline_sha256": results["baseline_sha256"].get("milk"),
            "matched": 17, "total": 18,
            "movers": 1, "grade_movers": 1, "up_moves": 1, "down_moves": 0,
            "diff_min": 1.8, "diff_med": 1.8, "diff_max": 1.8, "diff_sd": 0.0,
            "residual_cause": "data_gap — barcode 7290014760141 (almond milk) sugars_g=None in BSIP1; canonical=51.5/C; live=49.7/D (TASK-378 corrected)",
            "grade_mover": "7290014760141: live=D canonical=C — ESCALATION REQUIRED before canonical can be clean",
            "phantom_flags": [],
            "bsip1_data_update_needed": "run_milk_002: barcode 7290014760141 sugars_g=6g (TASK-378 Shufersal verified)"
        }
    }
}

# Apply updates - try both slug forms (cheese vs cheese-spreads)
slug_aliases = {
    "cheese-spreads": "cheese",
    "bread": "bread",
    "cakes": "cakes",
    "cereals": "cereals",
    "granola": "granola",
    "milk": "milk"
}

for ledger_slug, update_data in updates.items():
    # Try to find this slug in the ledger list
    idx = cat_index.get(ledger_slug)
    if idx is None:
        # Try the alias
        for alias_slug, canonical_slug in slug_aliases.items():
            if canonical_slug == ledger_slug or alias_slug == ledger_slug:
                idx = cat_index.get(alias_slug) or cat_index.get(canonical_slug)
                if idx is not None:
                    break
    if idx is not None:
        ledger["categories"][idx].update(update_data)
        print(f"Updated ledger entry for {ledger_slug} (index {idx})")
    else:
        print(f"WARNING: slug {ledger_slug} not found in ledger; keys={list(cat_index.keys())}")

# Add phase0 summary at top level
ledger["last_phase0_run"] = now
ledger["phase0_summary"] = {
    "run_at": now,
    "categories_processed": 6,
    "total_products": 207,
    "total_matched": 186,
    "total_movers": 21,
    "total_grade_movers": 1,
    "total_up_moves": 9,
    "match_rate": "186/207 (89.9%)",
    "grade_mover_detail": "milk only: 7290014760141 D->C (stale BSIP1 sugars_g=None; ESCALATION REQUIRED)",
    "spec_conflict": "BARI_D4_SCORE_V1 was in de-chain list but is LIVE in all pages via surgical patch 361748722. Must be reclassified as LEGITIMATE in canonical flag vectors.",
    "not_done": [
        "cereals: configs/cereals.json missing BARI_GRAN_SUGAR_25G_V1=on",
        "milk: BSIP1 7290014760141 sugars_g=None causes grade mover (D->C); needs correction",
        "granola: BSIP1 7290017962023 sugars_g=None; 1.5 score drift",
        "bread: BSIP1 7290016245325 sugars_g=None; 0.8 score drift (no grade move)",
        "cheese: 9 E450 products have 2.2 engine drift from June 17 scoring; irrecoverable without full re-run",
        "cereals: 6 products have 0.7-2.8 compound engine-state drift; no grade moves",
        "all: BARI_D4_SCORE_V1 spec-conflict needs owner acknowledgment"
    ]
}

ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

h = hashlib.sha256()
h.update(ledger_path.read_bytes())
print(f"\nLedger written: {ledger_path}")
print(f"SHA256: {h.hexdigest()}")
print(f"Size: {ledger_path.stat().st_size} bytes")
