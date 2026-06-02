# run_cheese_003 — Factory Findings (Cottage / White Cheese, cheese-spreads)

**Date:** 2026-06-02 · **Task:** TASK-142 (resumed after TASK-142A/EV-029) · **Engine:** proto_v0 / 0.4.1 **UNMODIFIED**
**Supersedes:** run_cheese_002 (INVALID — scored on EV-029-corrupt fat) and run_cheese_001 (pre-router-fix diagnostic).

## What changed
The TASK-142A parser fix (shared `bsip0_nutrition.py`, EV-029) was wired into the cheese scrape. This run is a
full re-scrape → re-build BSIP1 → re-score on **corrected fat/saturated** data, engine untouched.

- **Re-scrape (2026-06-02):** 117 products; corrupt 2026-06-01 raw **replaced**. BSIP0 plausibility gate **PASS (0.0% implausible)**.
- **BSIP1 run_cheese_003/output:** 59 included, 54 displayable (data-sufficient), 5 withheld.
- **BSIP2 run_cheese_003:** 59 scored, 0 errors.

## The fix is validated end-to-end
| Gate | run_cheese_001/002 (corrupt) | run_cheese_003 (corrected) |
|------|------|------|
| COV-006 plausibility | 31.9% implausible (**FAIL**) | **0.0% implausible (PASS)** |
| fat ≤ 0.5 in any pool | 62/116 products | **0** |
| saturated > total fat | endemic | **0** |
| cream-cheese fat reading | falsely 0.5 g | **real 25–32 g** |
| saturated-fat capture | 0% | near-complete |

## Sub-pool grades on REAL fat (displayable n=54)
| Pool | n | Median | Range | Grades |
|------|---|--------|-------|--------|
| cottage | 11 | 69.4 | 52.0–74.9 | B 8 / C 3 |
| white_cheese_quark | 18 | 68.6 | 48.0–82.0 | B 11 / C 5 / A 1 / D 1 |
| labaneh | 1 | 52.0 | — | C 1 |
| cream_cheese_spread | 24 | 52.0 | 25.2–68.3 | C 16 / D 6 / B 1 / E 1 |

Overall: median **55.0**, grades A 1 / B 20 / C 25 / D 7 / E 1.

**Score shift vs run_002 is expected, not a regression.** Cream-cheese median 60.7 → 52.0 and overall 65.0 → 55.0
because high-fat spreads are now scored on real 25–32% fat where the bug had read 0.5 g. This is the corrected truth.

## A-ceiling holds on real fat
Exactly **one** product reaches grade A — גבינה טבורוג 5% (82.0) — and it is **WITHHELD**
(`a_eligible_pre_routing=false`; fails C1 added-sugar, C2 engineered-additives, C3 no confirmed live culture,
C4 non-intact matrix). **0** products are A-eligible pre-routing. The conservative dairy A-ceiling functions
correctly on corrected data. (run_002 had 6 macro-A's at 85 on the corrupt corpus; far fewer reach A on real fat,
and the lone one is still withheld — the ceiling binds either way.)

## Routing
Misroute **1.7%** (1/59): גבינת עזים 32% שומן → snack_bar_granola (high-fat goat soft cheese). Same single residual
as run_002. Under the 5% gate; not hand-tuned (engine frozen). Optional future goat-cheese signal.

## The 5 withheld (transparency-tier) — a truth the bug had been masking
גבינת שמנת 30% (+ 3 flavour variants) and גבינה לאבנה 5% א.ח.נוכרי are withheld because the **Shufersal source
panel itself omits total fat, protein and total carbohydrates** (lists only energy/sodium/sugar/saturated-fat).
Verified against the live page (P_554969): the `nutritionList` has no total-fat/protein/carbs row. The parser
captured everything present.

**Why run_002 showed "0 insufficient":** the old broken parser mislabeled the **saturated-fat** row as total fat,
fabricating a fat value that made these partial panels look data-complete. Exposing them as insufficient is the
correct behavior (parallels the run_yogurt_003 ingredient-panel finding). They are withheld from display, so
INSUFFICIENT is **0% on the displayable set (54)**.

## DoD scorecard
- Coverage ≥90% — **MET** (displayable 100%; full corpus 91.5%)
- INSUFFICIENT 0% displayable — **MET** (0/54; 5 partial-panel products withheld)
- Misroute <5% — **MET** (1.7%)
- Fat sane across all 4 sub-pools — **MET**
- COV-006 plausibility — **MET** (0.0%)
- A-ceiling withhold on real fat — **MET**
- Sub-pool structure applied + documented — **MET**
- QA green (engine unchanged) — **MET**
- Frontend package ready — **MET** (factory_run_003; 52/59 display-approved; **NON-AUTHORITATIVE**)

## Guards honored
Engine 0.4.1 unmodified (fix is BSIP0 data-ingestion only); no published/frozen scores changed; constructs are
label-observable classification/disclosure layers; frontend package NON-AUTHORITATIVE and NOT promoted.

## Remaining gate
Nutrition/Product grade-publication sign-off (Stage 6) — confirm the corrected per-pool grades and the 1
A-ceiling-withheld macro-A. Human gate, not a data/QA failure.
