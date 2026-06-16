# BSIP2 Rescore Rollout Spread Analysis v1
**TASK-278 | Data Agent | 2026-06-14 | ANALYSIS ONLY — zero score movement**

*Supersedes the partial Phase 3 draft (2026-06-14 earlier pass). Previous pass had path_not_found on bread/snack_bars/butter/yogurt, and misclassified hard_cheeses as COSMETIC due to a metric error. This version corrects all paths and recomputes with the correct absorption definition.*

---

## Purpose

Determine whether a shelf-relative differentiator would **LAND** (adds real information because the shelf has genuine quality spread and products are not floor-saturated) or be **COSMETIC** (absorbed because products are pinned at the absolute score floor or because the relative term is redundant). This classification drives the rollout candidate shortlist.

## Reference Pilots

| Pilot | Classification | Decisive Evidence |
|-------|----------------|-------------------|
| Yogurt | LAND | Sugar med=5.3g, IQR=5.8, robust_scale=4.3; bimodal; score stdev=16.52; 0% floored; 0% scaling absorption |
| Cookies/Biscuits | COSMETIC | 53.4% final_score <= floor+3; 19% scaling absorption; relative term absorbed into floor |

## Classification Methodology

Two independent absorption tests. Either failing = COSMETIC.

1. **Floor saturation** (`pct_floored`): % of scored products with `final_score_estimate <= 33` (absolute floor 30 + buffer 3). A shelf-relative penalty cannot move a floored product lower. Threshold: >= 40% = COSMETIC.
2. **Penalty scaling absorption** (`pct_scaling_absorbed`): % where `total_penalty_before_scaling - total_penalty_after_scaling > 3pts`. The engine scales large penalties down near the floor, absorbing the relative increment. Threshold: >= 30% = COSMETIC.

**Critical correction applied (vs earlier pass):** `score_after_cap - final_score_estimate > 5` is NOT absorption when `penalty_before == penalty_after`. Hard cheeses have a uniform HP_FAT_SODIUM_COMBO penalty (~6pts) applied identically to all 37 products — verified by checking each trace. No scaling occurs. This is a domain deduction that preserves relative ordering, not absorption. Corrected metric: hard_cheeses = 0.0% scaling absorbed (was incorrectly reported as 97.3%).

**Brined special case:** SODIUM_LOAD_GENERAL_GRAD + SODIUM_SHELF_SURCHARGE already implements a graduated sodium shelf-relative term. Adding a new relative term would be redundant, not additive. Classification = COSMETIC on the basis of redundancy, not floor saturation.

**N-A conditions:** (a) < 5 scored products, (b) key nutrient null in > 80% of traces, (c) score-free display category (TASK-235), (d) no committed BSIP2 run.

---

## Main Comparison Table

All values trace-derived from committed bsip2_trace.json files at the listed run directories. `robust_scale = max(IQR/1.349, 1.4826*MAD, 1.4)`.

| Category | Run | n | Sugar med (g) | Sugar IQR | Sugar scale | Sat_fat med (g) | Sat_fat scale | Sodium med (mg) | Sodium scale | % Floored | Score stdev | % Scaling absorbed | Candidate nutrient | Class |
|----------|-----|---|---------|---------|-------|---------|-------|---------|--------|---------|---------|----------|---------|-------|
| yogurt | run_yogurt_006_shipcfg2 | 87 | 5.3 | 5.8 | 4.3 | 2.0 | 1.4 | 48 | 11.9 | 0.0 | 16.52 | 0.0 | sugar | **LAND** (ref.) |
| juices | run_juices_yohananof_002 | 28 | 8.2 | 6.9 | 5.5 | null | null | 10 | 5.9 | 7.1 | 23.81 | 0.0 | sugar | **LAND** |
| hard_cheeses | run_hard_cheeses_001 | 37 | 0.5 | 1.0 | 1.4 | 17.5 | 5.9 | 620 | 296.5 | 2.7 | 17.35 | 0.0 | sat_fat | **LAND** |
| cereals | run_cereals_synthesis_001 | 45 | 14.0 | 11.0 | 8.9 | 1.2 | 1.4 | 280 | 274.3 | 11.1 | 17.03 | 0.0 | sugar | **LAND** |
| salty_snacks | run_salty_snacks_002 | 54 | 2.5 | 2.0 | 1.5 | 2.0 | 3.0 | 560 | 140.8 | 7.4 | 16.51 | 0.0 | sodium | **LAND** |
| milk | run_005_headpin | 20 | 4.9 | 1.5 | 2.2 | 0.3 | 1.5 | 45 | 14.8 | 0.0 | 15.07 | 0.0 | sat_fat | **LAND** |
| cheese_spreads | run_cheese_004 | 59 | 3.0 | 1.6 | 1.4 | 5.4 | 9.5 | 350 | 81.5 | 1.7 | 14.47 | 0.0 | sat_fat | **LAND** |
| maadanim | run_maadanim_001 | 200 | 9.7 | 11.9 | 8.9 | 3.0 | 3.5 | 60 | 89.0 | 18.0 | 13.39 | 2.5 | sugar | **LAND** |
| hummus | run_hummus_002 | 69 | null (0/69) | null | null | null (0/69) | null | 393 | 89.0 | 0.0 | 9.86 | 0.0 | sodium | **LAND** |
| cookies_coffee | run_cookies_005_shelfrel_pilot | 58 | 21.5 | 6.9 | 5.1 | 7.4 | 4.0 | 220 | 77.1 | 53.4 | 13.35 | 19.0 | sugar | **COSMETIC** (ref.) |
| snack_bars | run_snack_bars_001 | 53 | 19.4 | 22.4 | 17.3 | 3.2 | 3.4 | 142 | 127.5 | 43.4 | 15.7 | 9.4 | sugar | **COSMETIC** |
| butter | butter_run_003 | 39 | 0.1 | 0.6 | 1.4 | 50.5 | 2.2 | 11 | 470.7 | 0.0 | 9.64 | 0.0 | sat_fat | **COSMETIC** |
| brined_cheeses | run_brined_005 | 48 | 2.0 | 2.0 | 1.4 | null | null | 1000 | 229.8 | 0.0 | 9.45 | 0.0 | (redundant) | **COSMETIC** |
| bread | real_bread_retail_003_v1 | 256 | null (7/256) | null | null | null (0/256) | null | 382 | 51.9 | 0.0 | 13.77 | 0.0 | sodium | **N-A** |
| frozen_vegetables | run_frozen_vegetables_001 | 53 | 1.4 | 1.1 | 1.4 | null | null | 24 | 29.7 | 0.0 | 10.92 | 0.0 | N-A | **N-A** |
| granola | no_run | — | — | — | — | — | — | — | — | — | — | — | N-A | **N-A** |

---

## Ranked Shortlist — Best Rollout Candidates

Ranked by: `composite = score_stdev * (1 - pct_floored / 100)`. Higher = more real spread surviving to consumer.

| Rank | Category | Composite | Score stdev | % Floored | Candidate nutrient | Primary note |
|------|----------|-----------|-------------|-----------|-------------------|--------------|
| #1 | **juices** | 22.1 | 23.81 | 7.1% | sugar | Highest stdev across all categories. Sugar IQR=6.9, clean signal. Thin corpus (n=28) — monitor. |
| #2 | **hard_cheeses** | 16.9 | 17.35 | 2.7% | sat_fat | NOT sugar (near-zero, IQR=1.0). Sat_fat IQR=8g, scale=5.9. Large real spread. |
| #3 | **yogurt** | 16.5 | 16.52 | 0.0% | sugar | Reference pilot, confirmed LANDS. Page frozen (TASK-256) pending factory rebuild. |
| #4 | **salty_snacks** | 15.3 | 16.51 | 7.4% | sodium | Sodium IQR=190mg, scale=140.8. Sugar is low-variance (scale=1.5, at floor). |
| #5 | **cereals** | 15.1 | 17.03 | 11.1% | sugar | Sugar IQR=11.0, scale=8.9. Strong. TASK-189 (sodium gap) does not block sugar rollout. |
| #6 | **milk** | 15.1 | 15.07 | 0.0% | sat_fat | Frozen invariant (run_005_headpin). No rescore without owner authorization. |
| #7 | **cheese_spreads** | 14.2 | 14.47 | 1.7% | sat_fat | Sat_fat scale=9.5 (strongest in portfolio). Full-fat vs light vs plant-based split. |
| #8 | **maadanim** | 11.0 | 13.39 | 18.0% | sugar | Large corpus (200). Sugar scale=8.9. Borderline floored (18%) — 82% still reachable. |
| #9 | **hummus** | 9.9 | 9.86 | 0.0% | sodium | Sugar/sat_fat null in all traces. Score spread from ingredient quality. Sodium IQR tight (33mg). Weakest LAND. |

---

## Non-Sugar Nutrient Notes (for scoring rule planning)

Categories where a **non-sugar** nutrient is the better lever — important for routing to the correct D6/D7 proposal:

| Category | Right lever | Why not sugar |
|----------|-------------|--------------|
| hard_cheeses | sat_fat | Sugar near-zero for cheese; IQR=1.0 at scale floor. Sat_fat IQR=8g, scale=5.9. |
| cheese_spreads | sat_fat | Sugar sparse (34/59). Sat_fat scale=9.5 (full-fat vs light vs plant-based). |
| milk | sat_fat | Fat type/source is the categorical axis (3.4%/natural 4%/goat). Sugar mostly lactose, sparse (9/20). |
| salty_snacks | sodium | Sugar IQR=2.0, scale=1.5 (floor). Sodium IQR=190mg, scale=140.8. |
| brined_cheeses | (graduated mechanism already live) | SODIUM_LOAD_GENERAL_GRAD + SODIUM_SHELF_SURCHARGE is the shelf-relative sodium term. |
| hummus | sodium (with caution) | Only nutrient available. But tight IQR=33mg; score spread from ingredient quality, not a single nutrient. |

---

## COSMETIC Classifications — Detailed Rationale

**cookies_coffee (run_cookies_005_shelfrel_pilot) — COSMETIC (reference pilot):**
53.4% of 58 products have `final_score_estimate <= 33`. Floored products cannot move lower; the relative penalty is absorbed by the floor. 19% of products show penalty scaling (pen_before >> pen_after). Confirmed empirically: Lotus biscuit gains +6 from relative term but stays at floor.

**snack_bars (run_snack_bars_001) — COSMETIC:**
43.4% floored — nearly identical mechanism to cookies. Sugar IQR is wide (22.4g) but reflects a bimodal corpus: date/nut bars (~6g) vs chocolate bars (~30g). The high-sugar group is already at the floor and cannot be penalised further. Note: traces from run_snack_bars_001 (full L1 signals). Authoritative run_snackbars_007_headpin stores flat score/grade only (no L1 signals in JSON). Scoring is deterministic; run_001 values are representative.

**butter (butter_run_003) — COSMETIC:**
Score range = 24.8pts (compressed). Sat_fat IQR = 3g (all butter is 48-52g sat_fat/100g). 0% floored but genuine clustering — not an artifact. Owner ruling applies: "butter clustering is an honest finding; never add signals to manufacture differentiation that doesn't exist." No lever produces meaningful differentiation.

**brined_cheeses (run_brined_005) — COSMETIC:**
0% floored, 0% scaling absorption. Score stdev=9.45, range=39.4. NOT floor-saturated. Classification is COSMETIC because SODIUM_LOAD_GENERAL_GRAD + SODIUM_SHELF_SURCHARGE already implements a graduated sodium shelf-relative mechanism (EV-056). Adding a new relative term would be redundant. The mechanism exists; this category is DONE on the sodium axis.

---

## N-A Classifications

**bread (real_bread_retail_003_v1):** 256 scored products, 0% floored, stdev=13.77. Real score spread exists. BUT: sugar null in 97% of traces; sat_fat null in 100%. The bread BSIP0 panel captures fiber/sodium/fermentation, not sugar. Sodium available (70% coverage, IQR=60mg). N-A for sugar rollout. Bread-specific sodium relative term is a separate future proposal.

**frozen_vegetables (run_frozen_vegetables_001):** Category is score-free for display (TASK-235 ruling: use-case segment bands, no A/B/C/D). Scores exist in the pipeline but are not consumer-facing. Rollout is N-A.

**granola (no run):** No dedicated BSIP2 run. Granola products are embedded inside run_cereals_synthesis_001 but not separately tagged. TASK-189 (sodium scoring gap) open. N-A pending a labeled granola sub-corpus or a cereals run with sub-category tagging.

---

## Key Finding

**The mechanism works on categories with real nutrient spread AND low floor saturation.** The cookies failure is category-specific: 53.4% of products sit at absolute penalty floor from HP_FAT_SUGAR + HP_FAT_SODIUM + NOVA cap stacking — no headroom for relative differentiation.

**The nutrient matters more than the category:** sugar is not always the lever (hard_cheeses, salty_snacks, milk, cheese_spreads all need a different nutrient). The rollout must be routed by candidate_nutrient, not by category alone.

**Hard_cheeses is correctly LAND** (not COSMETIC as the earlier pass stated). The 97.3% "pinned" reading from `sac - fse > 5` was the uniform HP_FAT_SODIUM_COMBO penalty of ~6pts — not penalty scaling absorption. Corrected metric = 0.0% absorption. Score stdev=17.35, range=46.6, 2.7% floored. A sat_fat shelf-relative term would LAND.

---

## Rollout Priority Recommendation

Based on this analysis, the recommended rollout order (pending D6/D7 approvals per required governance):

1. **cereals x sugar** — highest leverage LAND at ranking #5 with sugar as candidate. Already next in factory pipeline. Not subject to any frozen invariant.
2. **juices x sugar** — highest composite score (22.1) but thin corpus (n=28). Run first as a data point.
3. **cheese_spreads x sat_fat** — strong sat_fat spread, low floor saturation.
4. **maadanim x sugar** — large corpus, good sugar spread.
5. **hard_cheeses x sat_fat** — real spread, but requires a sat_fat relative term proposal (not sugar).
6. **salty_snacks x sodium** — strong sodium spread, but requires a sodium relative term.

Categories that should NOT proceed with rollout: cookies_coffee, snack_bars, butter, brined_cheeses, granola, frozen_vegetables.

---

## Open Items / Not Done

1. Bread sodium lever requires a separate rule proposal — not addressed here.
2. Hummus: sugar/sat_fat null. If BSIP0 enrichment extended to capture these, classification may change.
3. Snack_bars headpin: run_snackbars_007_headpin lacks L1 signals in stored flat JSON. A future run should store full traces.
4. Granola: needs labeled sub-corpus or sub-category tag in cereals run.
5. TASK-189 (cereals sodium gap): must be resolved before any sodium rollout to cereals, but does not affect sugar rollout.
6. Milk is frozen (run_005_headpin invariant). LAND classification is informational only — no rescore without owner authorization.

---

*Document: `01_framework/bsip2_framework/project_rescore/rollout_spread_analysis_v1.md`*
*Generated: 2026-06-14. ANALYSIS ONLY. No engine edits, no score movement, no published changes.*
*Source data: `spread_analysis_raw_v1.json` + corrected per-category trace inspection scripts.*
