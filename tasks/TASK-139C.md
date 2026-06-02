---
id: TASK-139C
title: "Data: fix router yogurt-anchor misroutes (19% -> <5%) + 'יווני/Greek' olive false-positive"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "It solved the exact problem it was created for (20% \u2192 0% yogurt misroutes) while passing regression tests and leaving all frozen categories unchanged."
depends_on: []
blocks: [TASK-142, TASK-143]
category_id: null
summary: >
  run_yogurt_003 misrouted 17/88 (19%): flavored 'GO' yogurts -> dessert, crunch/granola-topped -> cereal,
  and 'זית ירוק יווני' (green olives) false-positive into whole_food_fat via the 'יווני/Greek' include token.
  Tighten the yogurt anchor and the Greek include token so dairy routes to the dairy/yogurt archetype.
  Validate against the run_yogurt_003 corpus and the golden regression set.
---

# TASK-139C — Router yogurt-anchor fix

## Changes
1. Strengthen yogurt anchor so flavored/drinkable/'GO' yogurts and crunch-topped yogurts route to the dairy/yogurt archetype, not dessert/cereal.
2. Constrain the `יווני`/Greek include token so it does not pull olives (`זית ירוק יווני`) into whole_food_fat.

## Validation
- run_yogurt_003 misroute rate **19% -> <5%**.
- Golden regression corpus **12/12 PASS**; no new misroutes in other categories.
- Verify exact router file/lines before editing (3-stage router: anchor->signal->resolution).

## DoD
Misroute target met; regression green. Then propose RETURNED.

## Return block — proposed RETURNED (2026-06-01, data-agent)

**Outcome:** all targets met. Report: `02_products/yogurt_system/reports/router_misroute_fix_139C.md`.

| Check | Result |
|-------|--------|
| run_yogurt_003 misroute | 20% (18/88) → **0% (0/86)** ✅ |
| Golden router regression | **12/12 PASS** ✅ |
| No new misroutes elsewhere | milk_002 / cereals / bread / hummus / snacks = **0 changes** ✅ |

**Changes (no scoring logic touched):**
- `router_v2.py`: 8 yogurt sub-brand anchors → dairy_protein (above topping/dessert
  anchors); dairy-head topping suppression; drinkable (`משקה`) exclusion on the new
  anchors (keeps the beverage boundary; frozen milk category untouched).
- `01_scrape_yogurt.py` + `02_build_bsip1_yogurt.py`: olives (`זית`) excluded before
  the `יווני`/greek include; `יווני` kept for real Greek yogurts. Corpus rebuilt 88→86.

**⚠️ Requires Nutrition/Product co-sign before any maadanim re-score:** the global
router change reclassifies **8 live maadanim products** (dessert/snack → dairy_protein),
all genuine protein/mix-in spoon yogurts — a correction of pre-existing inconsistency,
not a regression. Shipped maadanim JSON is unchanged. This is the dairy↔dessert boundary
(Gap 3 / TASK-139A) and folds into the already-pending maadanim re-score (TASK-139B).

**Handoff:** re-running `batch_run_yogurt_003.py` on the cleaned corpus is left to the
consuming task (TASK-135/142). Only the Central Controller records CLOSED.

---

## State note — scope broadening to CEREALS (2026-06-01, data-agent)

⚠️ **Registry conflict surfaced.** This task was assigned a broadened scope (add the
run_cereals_002 7.6% misroute — same router root cause as yogurt) AFTER it had already
been recorded `CLOSED` (yogurt-only) by the Central Controller. Per Registry First, I did
**not** change `status:`. The cereals engine work below is complete and validated; it needs
a Central-Controller registry decision to record (reopen TASK-139C, or open a follow-up task).

**Root cause (shared):** router_v2 had no category anchor that survives grain/nut/topping/
flavor tokens. The yogurt fix used 8 brittle brand anchors; the durable fix below
generalizes to both categories.

**Change implemented (ROUTING ONLY — no scoring weights/thresholds/caps/NOVA touched):**
- `router_v2.py` Stage 2c **category prior**: reads the BSIP1 acquisition-shelf subtype
  (`bsip_cereal_subtype` / `bsip_yogurt_subtype`) and adds `CATEGORY_PRIOR_BOOST = 2.0`
  to that category. Signal-path only (never overrides a Stage-1 hard anchor); runs AFTER
  the beverage gate (drinkables still route to beverage). No-op when subtype is absent or
  an "other"/"unknown" bucket → fully backward compatible. All 7 cereal misroutes were
  signal-driven (anchor_override=False), so this is sufficient and safe.

**Before / after misroute:**
| Category | Before | After | Gate <5% |
|---|---|---|---|
| run_cereals_002 | 7.6% (7/92) | **0.0% (0/92)** | ✅ |
| run_yogurt_003 | 0.0% (0/86) | **0.0% (0/86)** | ✅ (held) |

**Regression (both suites, before == after):**
- `run_router_regression.py` → **12/12 PASS**
- `run_regression_check.py` → all PASS + **1 pre-existing WARN** (soy-drink structural_class
  B-vs-C, "acceptable as secondary" — present before this change, unrelated).

**Score-correction note (NOT a scoring change):** 6 of the 7 cereals now score under the
`cereal` calorie-density table instead of the inflated WFF/bread tables they misrouted into
(grade dist B10→B12, C48→C46, D25→D26, E2→E1; A unchanged at 7). This is the QA-CER-001
correction. `פתיתים אורגנים כוסמין` (7290011830144) stays **81.5/A** even after correct
routing → confirms the audit's finding that routing barely moves scores; its A is the
separately-flagged **QA-CER-W1** NOVA-proxy question for Nutrition, not a routing defect.

**Olive `יווני` curation:** verified in place (`01_scrape_yogurt.py` + `02_build_bsip1_yogurt.py`
NONYOGURT_RE excludes `זית|זיתים|olive`); 0 olive products in the yogurt corpus. ✅

**Live state:** nothing promoted. run_cereals_002 frontend package stays NON-AUTHORITATIVE.
Unblocks TASK-142/143 interpretation; does not itself ship a shelf.

**Standing ⚠️ carried forward (unchanged from yogurt return block):** the global router
change reclassifies 8 live maadanim products (dessert/snack → dairy_protein) — requires
Nutrition/Product co-sign before any maadanim re-score (folds into TASK-139B). Shipped
maadanim JSON unchanged.
