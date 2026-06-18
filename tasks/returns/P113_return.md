# P113 Return — TASK-278 Phase-6: D6 Yogurt × Sugar Enrollment Proposal

**Agent:** nutrition-agent
**Date:** 2026-06-14
**Task:** TASK-278 Phase-6
**Status:** RETURNED

---

## Summary

D6 enrollment proposal completed for yogurt × sugar shelf-relative scoring. Router analysis identified that `dairy_protein` contains multiple non-yogurt sub-categories (milk, hard cheese, brined cheese, cream cheese, kefir, cottage) that must be excluded from a yogurt-specific sugar SR enrollment. Option A scope guard (category_subtype in CULTURED_YOGURT_SUBTYPES) is recommended — no router edit required. Sugar stats match P103 pilot calibration exactly (divergence = 0.0). Two named inversions identified from run_yogurt_006 committed traces. Anti-Immunity proof: 62 + 3 = 65 < 70. Engine files untouched, 342 PASS, 0 published score movement.

---

## Return Contract

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "authoritative_run": "run_yogurt_006",
  "corpus_n_total": 88,
  "corpus_n_yogurt_only": 87,
  "scope_guard_recommendation": "Option A — category_subtype in CULTURED_YOGURT_SUBTYPES; no router edit needed; subtype already populated by router_v2.py HARD_ANCHORS for all yogurt products",
  "router_change_needed": false,
  "router_change_description": null,
  "yogurt_sugar_stats": {
    "n_with_sugars_g": 74,
    "median_g": 5.45,
    "IQR_g": 5.80,
    "MAD_g": 2.55,
    "robust_scale": 4.299,
    "scale_formula": "max(IQR/1.349, 1.4826×MAD, 1.4)",
    "scale_primary": "IQR-primary (IQR/1.349=4.299 > 1.4826×MAD=3.781)",
    "divergence_from_p103_pilot": "small — 0.0g deviation (exact match: same corpus, same stats)"
  },
  "bands": {
    "P_max": 6,
    "B_max": 3,
    "floor_value": 62,
    "floor_threshold_g": 12.0,
    "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 PASS"
  },
  "named_inversions": [
    {
      "barcode_a": "7290110321697",
      "name_a": "יופלה GO אפרסק",
      "sugars_a": 9.8,
      "score_a": 61.2,
      "grade_a": "C",
      "barcode_b": "7290102397600",
      "name_b": "מולר מיקס שקדים ובוטנים",
      "sugars_b": 13.6,
      "score_b": 62.4,
      "grade_b": "C",
      "why": "B scores 1.2 pts above A despite 3.8g more sugar. Root cause: B has fewer additive categories and no MULTIPLE_ADDED_SUGAR_MARKERS penalty. SR corrects: A z=1.01→+1pt, B z=1.90→+4pt → A(60.2)>B(58.4) after SR."
    },
    {
      "barcode_a": "7290102396740",
      "name_a": "יוגורט אפרסק+תות 0%",
      "sugars_a": 4.5,
      "score_a": 36.4,
      "grade_a": "D",
      "barcode_b": "7290102393060",
      "name_b": "יוגורט מולר מיקס גליליות",
      "sugars_b": 14.0,
      "score_b": 43.5,
      "grade_b": "D",
      "why": "B scores 7.1 pts above A despite 9.5g more sugar. Root cause: A has NOVA 4 high-confidence (0.82), 17 ingredients, 6 additive categories → heavier backbone penalty despite lower sugar. SR partially corrects: A z=-0.22→0pts, B z=1.99→+4pt → gap reduced from 7.1 to 3.1 pts."
    }
  ],
  "ev_number": "EV-088",
  "enrollment_doc": "02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "d7_open_questions": [
    "Scope guard option A vs B confirmation — is category_subtype sufficient for all production yogurt products?",
    "P_max: 6 pts (standardized, this proposal) vs 8 pts (pilot value) — D7 decides",
    "Floor value: 62 (proposed) — confirm adequacy vs full corpus range",
    "Near-median relief threshold: 0.5 z-units (proposed) vs 0.3 (picks up 4.5g products near median)",
    "Null-sugars treatment: median imputation (pilot behavior, yields +2 relief) vs no adjustment — confirm",
    "Router change: if any yogurt product lacks category_subtype field in production, Option B (dedicated router category) may be needed"
  ],
  "not_done": []
}
```

---

## Machine-Readable Return Contract

```json
{
  "artifacts_claimed": [
    {
      "path": "02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md",
      "sha256": "8559ace6a4c3d428cbcebd3b8cb33d76bb53a47c1881f68a2ae915dfff172c6c"
    }
  ],
  "counts": {
    "corpus_n_total": 88,
    "corpus_n_yogurt_only": 87,
    "n_with_sugars_g_denominator_88": 74,
    "scope_guard_options_evaluated": 4,
    "scope_guard_options_recommended": 1,
    "named_inversions_required": 2,
    "named_inversions_found": 2,
    "engine_invariants_cases": 342,
    "engine_invariants_failures": 0,
    "off_data_uses": 0,
    "engine_files_modified": 0
  },
  "commands_run": [
    {"command": "python 03_operations/shadow/engine_invariants.py", "exit_code": 0, "result": "342 PASS 0 failures"}
  ],
  "claims_verified_by_agent": true,
  "propose": "RETURNED"
}
```

---

## Router Analysis Summary

`dairy_protein` in `router_v2.py` contains the following subtypes via HARD_ANCHORS:
- **Yogurt family:** yogurt, greek_yogurt, protein_yogurt, bio_yogurt, froop_yogurt, yogurt_mixin (all in CULTURED_YOGURT_SUBTYPES)
- **Kefir:** kefir (excluded from yogurt scope)
- **Cottage:** cottage (excluded)
- **Cheese spreads:** cream_cheese, cheese_spread (excluded)
- **Hard cheese:** hard_cheese, soft_ripened (excluded)
- **Brined cheese:** feta_brined, bulgarian_brined, halloumi_brined (excluded — governed by EV-056)

Score engine already uses `CULTURED_YOGURT_SUBTYPES` constant (constants.py) for the fermentation bonus gate. The same constant can gate yogurt SR enrollment — zero new infrastructure needed.

No engine files (score_engine.py, constants.py, router_v2.py) were read for modification or modified. This is design-only.
