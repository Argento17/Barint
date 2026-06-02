# TASK-139C (broadened) — Router category-prior fix: yogurt + cereals

**Owner:** data-agent · **Date:** 2026-06-01 · **Engine:** proto_v0 / 0.4.0
**Scope:** ROUTING ONLY — no scoring weights, thresholds, caps, NOVA logic, or grade bounds touched.
**Files changed:** `03_operations/bsip2/proto_v0/src/router_v2.py` (additive Stage 2c).

---

## Root cause (one gap, two categories)

router_v2 had no category anchor that survives an incidental grain/nut/topping/flavor
token dominating name+ingredients. The yogurt fix (prior return block) used 8 brittle
brand anchors. The durable, general fix carries the **BSIP0 acquisition-shelf identity**
forward as a soft prior — every product was scraped *as* yogurt or *as* cereal, and BSIP1
records that as a non-null subtype field.

All 7 cereal misroutes were **signal-driven** (`anchor_override=False`), so a Stage-2 boost
is sufficient and never has to override a genuine hard anchor.

## Change (router_v2.py, Stage 2c)

- New `CATEGORY_PRIOR_SUBTYPE_FIELDS` = {`bsip_cereal_subtype`→`cereal`, `bsip_yogurt_subtype`→`dairy_protein`}.
- `_category_prior(product)` returns the shelf category when a real (non-null, non-"other")
  subtype is present.
- In `classify_category`, after Stage 2 signals + beverage gate, before resolution:
  add `CATEGORY_PRIOR_BOOST = 2.0` to the prior category.
- **Guarantees:** signal-path only (hard anchors still exit first and win); runs *after* the
  beverage gate (drinkables stay beverage — dairy↔beverage / frozen milk boundary unchanged);
  no-op when the subtype field is absent → fully backward compatible (0 corpus products take
  the plant-milk bypass path, so the main-path placement covers all of them).
- Boost sized vs the observed misroute set: strongest incidental wrong-category stack was
  whole_food_fat ≈1.88; 2.0 makes shelf identity decisive yet beatable by a much stronger
  genuine signal mass.

## Before / after misroute

| Category | Before | After | Gate <5% |
|---|---|---|---|
| run_cereals_002 | 7.6% (7/92) | **0.0% (0/92)** | PASS |
| run_yogurt_003 | 0.0% (0/86) | **0.0% (0/86)** | PASS (held) |

The 7 corrected cereals (all now `cereal`): `כוסמין מלא 100%`, `דגני טבעות תירס ואורז`,
`מוזלי קראנצ'י בוטנ+שקדים`, `פתיתים אורגנים כוסמין`, `מוזלי בוטנים לוז שקדים`,
`כריות נוגט`, `צ'יריוס טעם דבש ושקדים`.

## Regression (both suites, before == after)

- `run_router_regression.py` → **12/12 PASS**.
- `run_regression_check.py` → all PASS + **1 pre-existing WARN** (soy-drink structural_class
  B-vs-C, "acceptable as secondary"; present before this change, unrelated).
- No new misroutes in frozen categories (milk/bread/snack/hummus) — golden + router corpora
  green; the prior is a no-op for any product without a subtype field.

## Score-correction note (NOT a scoring change)

6 of 7 cereals now score under the `cereal` calorie-density table instead of the inflated
WFF/bread tables they misrouted into. Cereals grade dist B10→B12, C48→C46, D25→D26, E2→E1;
A unchanged (7). This is exactly the QA-CER-001 correction.

`פתיתים אורגנים כוסמין` (7290011830144) stays **81.5/A** even after correct routing —
confirming the TASK-135 audit finding that routing barely moves scores. Its A is the
separately-flagged **QA-CER-W1** NOVA-proxy question (shaped/whole-grain flake reads NOVA 1)
for Nutrition review — not a routing defect, and not changed here.

## Standing escalation (carried forward, unchanged)

The router change reclassifies 8 live maadanim products (dessert/snack → dairy_protein),
all genuine protein/mix-in spoon yogurts — a correction of pre-existing inconsistency.
**Requires Nutrition/Product co-sign before any maadanim re-score** (folds into TASK-139B).
Shipped maadanim JSON unchanged.

## Live state

Nothing promoted. run_cereals_002 frontend package stays NON-AUTHORITATIVE. This unblocks
TASK-142/143 interpretation; it does not itself ship a shelf.

*data-agent · TASK-139C broadened · 2026-06-01 · engine 0.4.0, scoring untouched.*
