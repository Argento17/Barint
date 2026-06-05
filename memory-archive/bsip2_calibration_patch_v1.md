---
name: bsip2-calibration-patch-v1
description: "BSIP2 Robustness Calibration Patch v1 — 5 new confidence deductions, supplement quarantine, FP audit, 4 reports"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Calibration patch completed 2026-05-25. Addresses overconfidence identified in Robustness Sprint v1.

**Why:** Sprint v1 found 5 products where confidence was too high relative to data quality. Sprint also identified supplement products (G3/G4) misrouted to dairy_protein. Philosophy: "When data quality drops, confidence should drop faster than score ambition."

**How to apply:** When touching `interpretation_confidence.py`, `graceful_degradation.py`, or `router_v2.py`, re-run `run_calibration_patch.py` to validate regressions vs the 5 target cases.

## Files modified

- `interpretation_confidence.py` — added `_detect_supplement_candidate()` + 5 new deduction types
- `graceful_degradation.py` — supplement quarantine rule + routing_concern_kw extended
- `router_v2.py` — `_check_supplement_quarantine()` additive field on all routing paths

## New deductions in `interpretation_confidence.py`

| Deduction | Amount | Trigger |
|:----------|:-------|:--------|
| `ingredient_text_absent` | -14 | List present but `ingredients_text_he` empty |
| `product_name_empty` | -20 | No meaningful product name |
| `product_name_very_short` | -14 | ≤2 meaningful words |
| `product_name_short_no_anchor` | -8 | ≤4 words, no hard anchor |
| `anchor_secondary_tension` | -12 | Anchor overrode strong sec_conf ≥ 0.50, eligible pair |
| `anchor_secondary_tension_mild` | -6 | Anchor overrode sec_conf ≥ 0.35, eligible pair |
| `kcal_implausible_extra` | -10 | kcal outside ±40% of macro-implied range |
| `supplement_candidate` | -22 | Protein powder / meal replacement detected |

Anchor tension only applies for eligible pairs (HYBRID_ELIGIBLE_PAIRS + {cracker,cereal}).

## New output field: `is_supplement_candidate: bool`

## graceful_degradation changes

- Supplement candidate + high/very_high band → UNCERTAINTY
- Supplement candidate + moderate/low band → INSUFFICIENT
- High band + routing concern in `additional_reductions` → CAUTIOUS
  - Routing concern keywords: router_instability, hybrid_routing, anchor_secondary_tension,
    supplement_candidate, product_name_empty, product_name_very_short,
    product_name_short_no_anchor, ingredient_text_absent

## router_v2 changes

- `_check_supplement_quarantine(name, ing_text)` — detects name signals + whey+sport/maltodextrin combos
- `supplement_quarantine` field added to all `classify_category()` return paths

## Target case results (all 5 ✓)

| ID | Before | After | Key deduction |
|:---|:-------|:------|:--------------|
| C2 | very_high/Full | high/Cautious | ingredient_text_absent -14 |
| D3 | very_high/Full | high/Cautious | anchor_secondary_tension_mild -6 (snack_bar sec_conf=0.41) |
| F3 | very_high/Full | high/Cautious | product_name_short_no_anchor -8 |
| G3 | high/Cautious  | low/Insufficient [SUPPL] | supplement_candidate -22 + kcal_implausible -10 |
| H1 | very_high/Full | high/Cautious | anchor_secondary_tension -12 (snack_bar sec_conf=0.53) |

## Supplement quarantine cases

- G3 (אבקת חלבון ספורט): detected via name signal "אבקת חלבון" → Insufficient
- G4 (שייק חלבון תחליף ארוחה): detected via name signal "שייק חלבון" + "תחליף ארוחה" → Insufficient
- H4 (אבקת שייק חלבון שוקולד): detected via name signal "שייק חלבון" → Insufficient (moderate band)

## False Positive Audit (post-patch)

9 false positives identified and fixed:
- `product_name_short_no_anchor` fired on 7 products with explicit identity keywords (משקה, חטיף, ממרח)
  → Fixed: `_IDENTITY_EXEMPT` set suppresses penalty when name contains a category-identity word
- `kcal_implausible_extra` fired on B4 (protein_g=None) and B7 (carbohydrates_g=None) via `or 0` pattern
  → Fixed: all three macros must be non-None before check runs

D5 (`תערובת אגוזים`, "mix", 4 words, no identity keyword) — intentional TP, stays Cautious.

## Clean baseline regression check (Group A — post FP fixes)

- A1/A2/A3: very_high/Full ✓
- A4 (Oatly oat drink, "משקה" identity keyword): high/Full ✓ (regression fully fixed)
- A5: high/Full ✓

## Reports generated

Location: `C:\Bari\03_operations\reports\robustness\`

- `robustness_calibration_patch_001.md` — full before/after table for all 50 products
- `confidence_overstatement_cases_001.md` — 5 target cases with full trace
- `supplement_quarantine_001.md` — supplement detection logic + G3/G4/H4 case studies
- `false_positive_confidence_audit_001.md` — FP root causes, fixes, and post-fix deduction table

## Runner

`run_calibration_patch.py` — re-runs corpus, compares vs sprint v1 baseline, generates 4 reports.

[[bsip2_robustness_sprint_v1]]
