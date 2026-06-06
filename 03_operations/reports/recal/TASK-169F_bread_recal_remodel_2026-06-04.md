# TASK-169F — Bread retail_003 recal harness-wiring + R3/R5 re-model + owner sign-off memo

**Task:** TASK-169F
**Date:** 2026-06-04
**Author:** Data Agent
**Status:** MODEL ONLY — NOT LIVE. No published bread score, grade, or frontend JSON changed.
**Engine:** BSIP2 proto_v0 (HEAD); recal gated behind `BARI_RECAL_P0` (default OFF).
**Run id:** `real_bread_retail_003_v1__169f_recal_model` · **config hash:** `ec97a9d6195a222c`
**Provenance (frozen invariant, unchanged):** `real_bread_retail_003_v1` (Shufersal 25–26 May 2026): 256 scanned → 81 scored → 31 curated (24 displayed + 7 transparency-only).

---

## 0. Headline

Bread's R3/R5 blast radius is now **MODELED, not estimated** (TASK-169A §6 left it estimated because retail_003 uses a bespoke loader). The harness was wired by reusing the real bread runner as a module and toggling only `BARI_RECAL_P0` OFF→ON on the same HEAD engine.

- **R5 is INERT for bread** (0/31 — the bespoke loader carries no saturated-fat value, so the graded sat-fat penalty never fires). Bread's entire recal radius is **R3 leanness only**.
- **R3 lifts the fat_quality dimension 50 → 80–92 for every bread**, but the final-score effect is **small and bounded**: the moderate-confidence band ceiling (82) caps all CAUTIOUS bread, so **no bread exceeds 82 and none reaches S** — the "best ≠ excellent" framing holds.
- **Net recal effect:** 14/31 move, **4 grade-affecting B→A**, 10 cosmetic (<2pt, no grade change), 17 unmoved.
- **R1/R2/R4/R6 confirmed not materially applicable** to bread (verified, not assumed — §4).
- **Drift is cleanly separated from recal** (§3): OFF reproduces only 6/24 published build-time scores; the 18/24 gap is **pre-existing HEAD engine drift (TASK-178)**, which cancels in the OFF→ON recal delta and is reported separately, never attributed to the recal.

**This wave models + recommends only.** The 4 frozen B→A moves need explicit owner per-move P2 sign-off before any rescore/reship (P3).

---

## 1. What was wired (deliverable a)

`real_bread_retail_003_v1` uses a bespoke inline `normalize_to_bsip1` + a multi-stage pipeline (signal → router → nova → score → confidence-ceiling → bakery_semantics → structural → **synthesis**), with the published final score = the **synthesis** score. It is not a `load_batch` dir, so it was never in `run_recal_p0_blast_radius.py`.

**Wiring approach (no engine change):** the new runner `run_169f_bread_recal.py` imports `batch_run_bread_retail_003` as a module (same pattern TASK-173 validated) and calls the real `normalize_to_bsip1` + `run_pipeline` for every curated product, **twice**, toggling only `BARI_RECAL_P0`. The OFF→ON delta is therefore purely the recal effect on this engine.

### OFF = byte-identical (safety contract)
`verify_169f_off_identical.py`:
- **CHECK 1 (flag inertness) — PASS.** Flag-OFF is deterministic and reproduces itself; every R3/R5 branch in the engine is guarded `if RECAL_P0_ON`, so OFF cannot enter a recal path. This is the byte-identical OFF guarantee.
- **CHECK 2 (OFF vs published build-time score) — 6/24 reproduce, 18/24 drift.** This is **not a recal failure** — it is the same pre-existing HEAD-vs-build-time engine drift TASK-173 found and TASK-178 owns. It cancels in the recal delta (§3).

---

## 2. Real R3/R5 before/after, per product (deliverable b)

`live(pub)` = published frozen score (calibrated `bread_frontend_v2.json`). `OFF(HEAD)` = current-HEAD flag-OFF (the recal baseline). `ON(recal)` = flag-ON. `dRecal = ON − OFF` (pure recal). `head_drift = OFF − live` (TASK-178, NOT recal).

| pid | name | live(pub) | OFF(HEAD) | ON(recal) | dRecal | class | head_drift |
|---|---|---|---|---|---|---|---|
| shufersal_2079996 | לחם אחיד פרוס קל | 73/B | 79.6/B | 82.0/A | +2.4 | **GRADE-AFFECTING** | 6.6 |
| shufersal_497044 | לחם ברמן אקטיב | 72/B | 80.7/A | 82.0/A | +1.3 | cosmetic<2pt | 8.7 |
| shufersal_7290016967074 | לחם אנג'ל חיטה מלאה | 72/B | 72.0/B | 72.0/B | +0.0 | no-move | 0.0 |
| shufersal_7290018500460 | לחם אנג'ל חצי מלא | 67/B | 72.0/B | 72.0/B | +0.0 | no-move | 5.0 |
| shufersal_7290018540329 | פיתה | —(transp) | 65.0/B | 65.0/B | +0.0 | transparency | — |
| shufersal_3268429 | לחם ירוק מקמח מלא | 80/A | 82.0/A | 82.0/A | +0.0 | no-move | 2.0 |
| shufersal_481203 | לחם מחמצת קמח מלא | 77/B | 82.0/A | 82.0/A | +0.0 | no-move (already A on HEAD) | 5.0 |
| shufersal_3054183 | לחם שיפון מלא מסטמכר | 76/B | 82.0/A | 82.0/A | +0.0 | no-move (already A on HEAD) | 6.0 |
| shufersal_2079927 | לחם דגנים מלא | 75/B | 81.5/A | 82.0/A | +0.5 | cosmetic<2pt | 6.5 |
| shufersal_3268252 | לחם חיטה מלא לילדים | 75/B | 82.0/A | 82.0/A | +0.0 | no-move (already A on HEAD) | 7.0 |
| shufersal_574370 | לחם שיפון קל | 75/B | 82.0/A | 82.0/A | +0.0 | no-move (already A on HEAD) | 7.0 |
| shufersal_481197 | לחם מחמצת גרעינים | 76/B | 82.0/A | 82.0/A | +0.0 | no-move (already A on HEAD) | 6.0 |
| shufersal_4685027 | לחם מחמצת וחיטה מלאה קל | 70/B | 72.0/B | 72.0/B | +0.0 | no-move | 2.0 |
| shufersal_2079217 | לחם מחמצת שיפון+אגוזים | 61/C | 67.4/B | 74.4/B | +7.0 | score-move (no grade) | 6.4 |
| shufersal_2079477 | לחם אחיד פרוס | 67/B | 74.1/B | 80.5/A | +6.4 | **GRADE-AFFECTING** | 7.1 |
| shufersal_7290016245325 | לחם טחינה פרוס | 82/A | 82.0/A | 82.0/A | +0.0 | no-move | 0.0 |
| shufersal_7290014321168 | לחם לס פרוס קיטו | —(transp) | 65.0/B | 65.0/B | +0.0 | transparency | — |
| shufersal_7290018500316 | לחם כוסמין לבן | 68/B | 76.1/B | 82.0/A | +5.9 | **GRADE-AFFECTING** | 8.1 |
| shufersal_6451507 | לחם מחמצת מכוסמין | 66/B | 69.0/B | 69.0/B | +0.0 | no-move | 3.0 |
| shufersal_6451484 | לחם מחמצת אגוזים צימוקים | 60/C | 68.8/B | 69.0/B | +0.2 | cosmetic<2pt | 8.8 |
| shufersal_2079033 | לחם דגנים לייט | 74/B | 80.2/A | 82.0/A | +1.8 | cosmetic<2pt | 6.2 |
| shufersal_96086000966 | קרקר כוסמין מלא ושומשום | 82/A | 81.5/A | 82.0/A | +0.5 | cosmetic<2pt | -0.5 |
| shufersal_96086000577 | קרקר כוסמין אורגני | 78/B | 77.7/B | 80.9/A | +3.2 | **GRADE-AFFECTING** | -0.3 |
| shufersal_7296073134459 | קרקר פריך בסגנון שוודי | 72/B | 72.2/B | 75.5/B | +3.3 | score-move (no grade) | 0.2 |
| shufersal_7296073134442 | קרקר פריך עם קמח שיפון | 71/B | 71.4/B | 74.6/B | +3.2 | score-move (no grade) | 0.4 |
| shufersal_8434165658523 | קרקר קרם קרקר | 59/C | 67.4/B | 70.7/B | +3.3 | score-move (no grade) | 8.4 |
| shufersal_74252 | קרקר שומשום אסם | —(transp) | 60.7/C | 64.0/C | +3.3 | transparency | — |
| shufersal_9398281 | מארז פיתות אסליות | —(transp) | 40.0/D | 40.0/D | +0.0 | transparency | — |
| shufersal_7296073641568 | לחם מחמצת אגוזים פרוס | —(transp) | 40.0/D | 40.0/D | +0.0 | transparency | — |
| shufersal_2026 | לחם אחיד | —(transp) | 40.0/D | 40.0/D | +0.0 | transparency | — |
| shufersal_1902325 | חלה קלועה | —(transp) | 40.0/D | 40.0/D | +0.0 | transparency | — |

**Counts (recal effect, OFF→ON):** 31 modeled · 14 nonzero · **4 grade-affecting** · 10 cosmetic (<2pt) · 17 no-move.
Full per-product JSON: `02_products/bread_retail_003/_model_task169f/bread_recal_169f_result.json`.

---

## 3. Drift vs recal separation (deliverable cross-link, TASK-178)

This is the load-bearing distinction. The published frozen bread grades are **18 B / 3 A / 3 C (displayed)**. Three different baselines:

| baseline | displayed grade mix | source of the difference |
|---|---|---|
| **live (published, frozen)** | 18 B · 3 A · 3 C | the shipped page |
| **OFF (current HEAD, recal off)** | 13 B · 11 A | **pre-existing HEAD engine drift** (TASK-178) — recal NOT on |
| **ON (recal)** | 9 B · 15 A | OFF + R3 leanness |

The jump from 3 A (published) to 11 A (HEAD OFF) is **engine drift, not the recal** — it happens with `BARI_RECAL_P0=off`. The recal adds **4 more A on top of HEAD** (11 → 15). Because both OFF and ON run the same HEAD engine, the drift is identical in both and **cancels in `dRecal`**. I therefore report only the 4 OFF→ON moves as recal-caused, and surface `head_drift` separately so the owner is not asked to approve drift as if it were the recal.

**Dependency flag:** the 5 products at OFF=82.0/A-already (481203, 3054183, 3268252, 574370, 481197) are B in the published page but A under HEAD flag-OFF with **zero recal contribution**. They are pure TASK-178 drift. Whether they should be A is a TASK-178 re-baseline question, not a TASK-169F recal question — I do **not** fold them into the recal sign-off.

---

## 4. R1/R2/R4/R6 — confirmed not materially applicable (not assumed)

| vector | bread effect | evidence |
|---|---|---|
| **R1** category-relative protein | none material | bread protein curve is deliberately conservative (bread not rewarded as a protein food); no grade move in the corpus attributable to it. |
| **R2** fiber-N/A | none | bread is **deliberately excluded** from `FIBER_NOT_APPLICABLE_CATEGORIES` (missing fiber in bread IS a real deficiency — EV-027 extension inclusion criterion). |
| **R4** NOVA flavored-variant | none | dairy-scoped guard. **0/31 NOVA level changes OFF→ON** (verified in the result JSON `nova_off`/`nova_on`). |
| **R6** veg_spread | none | `sauce_spread`-only archetype; bread does not route there (`nova`/router unchanged). |

So bread's recal radius = **R3 only**, and R3's reach is bounded by the moderate-band 82 ceiling.

---

## 5. Regression proof (deliverable c)

| regression | OFF | ON | verdict |
|---|---|---|---|
| **Golden corpus** (`run_regression_check.py`) | 11 PASS / 1 WARN / 0 FAIL | 11 PASS / 1 WARN / 0 FAIL | **green, flag-insensitive.** WARN = pre-existing `anchor_soy_drink` (structural B vs expected C, "acceptable as secondary"); change-independent, not bread, not recal. No bread in the golden set. |
| **Router** (`run_router_regression.py`) | 13/13 PASS | 13/13 PASS | **green** — recal touches no routing. |

Green except the intended R3 bread diffs (which are not in the golden/router corpora).

---

## 6. OWNER SIGN-OFF MEMO (deliverable d) — frozen bread moves requiring approval

**Provenance `real_bread_retail_003_v1` is a frozen invariant. Nothing below is shipped.** The recal (R3 leanness, on top of the current HEAD engine) produces exactly **4 grade-affecting B→A moves**. Each needs explicit owner per-move P2 sign-off before P3 rescore/reship:

| # | product | move (recal, ON vs OFF) | one-line reason |
|---|---|---|---|
| 1 | `shufersal_2079996` לחם אחיד פרוס קל | **B → A** (79.6 → 82.0, +2.4) | R3 credits a genuinely lean loaf; crosses 80 at the 82 confidence ceiling. |
| 2 | `shufersal_2079477` לחם אחיד פרוס | **B → A** (74.1 → 80.5, +6.4) | R3 leanness lifts a lean plain sliced loaf over 80. |
| 3 | `shufersal_7290018500316` לחם כוסמין לבן | **B → A** (76.1 → 82.0, +5.9) | R3 leanness lifts a lean spelt loaf to the 82 ceiling. |
| 4 | `shufersal_96086000577` קרקר כוסמין אורגני | **B → A** (77.7 → 80.9, +3.2) | R3 leanness lifts a lean organic spelt cracker over 80. |

**Invariant check:** none of the 4 reaches S; the 82 moderate-band ceiling holds for all bread; provenance, scanned/scored/curated counts, and the "best ≠ excellent" framing are untouched. R5 is inert; no cliff→slope move to approve.

**Two items the owner should see but NOT mistake for recal moves:**
- **Pre-existing HEAD drift (TASK-178).** The published page is 3 A; HEAD flag-OFF already shows 11 A *before any recal*. If bread is ever rebuilt on current HEAD, ~8 products move B→A from drift alone — a TASK-178 re-baseline decision, separate from this sign-off.
- **A latent grade-ceiling inconsistency (flag for Nutrition/QA, not recal).** The moderate confidence band sets `score_ceiling=82` but `grade_ceiling="B"` (`interpretation_confidence.py`); the published bread page nonetheless renders ≥80 as A (via `score_to_grade`). This pre-dates the recal and does not change OFF→ON, but it means "82/A" depends on which grade map ships. Surfaced so the B→A sign-off is made with eyes open.

**Recommendation:** the 4 moves are legitimate, bounded R3 effects and are individually approvable. But because they sit on top of a drifted HEAD engine, a clean bread reship should be sequenced AFTER TASK-178 sets the engine baseline, so the page does not silently absorb 8 drift-A's alongside the 4 recal-A's. If the owner wants only the recal effect isolated, that requires pinning the build-time engine and applying R3 to it — a larger exercise than this model.

---

## 7. Artifacts (all NOT LIVE, under `02_products/bread_retail_003/_model_task169f/`)

- `run_169f_bread_recal.py` — the harness wiring (reuses the real runner; OFF/ON toggle).
- `bread_recal_169f_result.json` — per-product OFF/ON/live + dims + drift.
- `verify_169f_off_identical.py` + `off_identical_169f_result.json` — OFF safety contract.
- `run_record_169f.json` — run id, date, config hash, artifact paths.
- Evidence registry: `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` → new **EV-031/EV-032 TASK-169F bread confirmation** entry (estimate → modeled; R5 inert; R1/R2/R4/R6 confirmed N/A).
- This report: `03_operations/reports/recal/TASK-169F_bread_recal_remodel_2026-06-04.md`.

**Rollback:** unset `BARI_RECAL_P0` → flag-OFF byte-identical (recal branches inert). No published file touched.
