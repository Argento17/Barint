# Project Rescore — Rollout Plan v1
**Task:** TASK-278 · **Date:** 2026-06-14 · **Author:** Orchestrator
**Status:** DRAFT — awaiting owner approval + first-category pick. NO published-score movement until each category's owner go-live (tripwire-1).

## Basis
- Mechanism **validated**: shelf-relative differentiator LANDS on shelves with real quality spread (yogurt: 61/88 move, 0 absorbed), is COSMETIC on floor-saturated shelves (biscuits: absorbed).
- Classification from `rollout_spread_analysis_v1.md` (P104, orchestrator spot-verified: hard_cheeses, yogurt, cookies). **Discriminator = floor saturation / scaling-absorption, not nutrient IQR.**
- Owner philosophy locked: ONE absolute scale; relative refines within-shelf; firm absolute floor holds Anti-Immunity. Each enrollment = its own EV + Nutrition/Product D7 + no-regression + owner go-live.

## Target set (LAND categories), routed BY NUTRIENT
| # | Category | Nutrient | Why | Notes |
|---|----------|----------|-----|-------|
| 1 | **cereals** | sugar | stdev~17, IQR 11, 11% floored, live category, sugar = real lever | **Recommended FIRST go-live** (sugar mechanism already built+piloted) |
| 2 | juices | sugar | highest spread (stdev~24); sugar is THE juice lever | re-verify traces at enrollment |
| 3 | maadanim | sugar | large corpus, real spread | sugar |
| 4 | hard_cheeses | sat_fat | stdev~17, not floored | **first SAT-FAT enrollment** (new nutrient calibration) |
| 5 | cheese_spreads | sat_fat | spread present | sat_fat |
| 6 | salty_snacks | sodium | sodium is the lever | **first general-mechanism SODIUM** (distinct from EV-056 dairy) |
| 7 | hummus | sodium | weakest (sugar/satfat null) | low priority |

**Deferred / special:** **yogurt** — validated, but its public page is owner-sensitive (relaunch rejected, TASK-256) → owner decides if/when. **milk** — frozen invariant, informational only, NEVER moved.

**Excluded — COSMETIC (no score rescore; at most copy/framing de-anchor):** cookies, snack_bars, butter, brined_cheeses (brined already has EV-056 graduated sodium).
**Excluded — N-A:** bread (no sugar data; sodium = separate future proposal), frozen_vegetables (score-free by design), granola (no committed run).

## Nutrient sequencing
Sugar is fully built + piloted → prove on **cereals** (then juices/maadanim). THEN extend to **sat_fat** (hard_cheeses, cheese_spreads) and **sodium** (salty_snacks) — each new nutrient needs its own band calibration + floor decision + D7.

## Two reusable prerequisites (build ONCE, before category #1 publishes)
- **PRE-A — Category-specific scoping.** The differentiator scopes by router `category`, but shelves share buckets (yogurt/milk/cheese all = `dairy_protein`). Need clean per-shelf scoping (router subtype, or corpus-tagged/per-run scope) so an enrollment can't bleed across a shared bucket. Design + small eng (Nutrition + Data), D7-governed.
- **PRE-B — Exact-flag no-regression discipline.** Reusable gate: rescore the target's committed run with its EXACT committed flag set + the new flag → confirm ONLY the intended nutrient-driven movements; PLUS full cross-corpus baseline diff (all published byte-identical flag-off). Codify as a script (the yogurt pilot exposed that flag-replication, not engine drift, caused 54 spurious diffs — this prevents that).

## Per-category go-live process (the repeatable unit)
1. Nutrition enrollment proposal: shelf stats (median/IQR/robust_scale) + asymmetric bands (P>B) + floor decision + ≥2 named inversions → draft EV-0NN.
2. Product D7 co-sign.
3. Wire scope (PRE-A) + exact-flag pilot rescore (PRE-B), measured-not-published.
4. Orchestrator verify: lands? no-regression clean? before/after distribution.
5. **Owner go-live review (tripwire-1)** → publish + de-anchor page copy.

## Recommended execution order
PRE-A + PRE-B (foundation) → **cereals/sugar** (first go-live, end-to-end proof of the repeatable unit) → juices/maadanim (sugar) → hard_cheeses/cheese_spreads (sat_fat) → salty_snacks/hummus (sodium). yogurt + copy-only de-anchor of COSMETIC pages = separate owner calls.
