---
id: TASK-169A
title: P0 — recalibration design + blast-radius model (category-relative protein, R2/R3/R4/R5/R6)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
summary: >
  P0 of TASK-169. Nutrition designs the shared-engine recalibration (category-relative protein scale per category, leanness reward in fat_quality, NOVA proxy refinement for cultured/fortified dairy + jarred spreads, red-label sat-fat cap->graded penalty, veg-spread category-fit rubric) with evidence-registry entries + rollback; Data then implements in a MODELING harness (not shipped) and produces before/after diffs across cheese/hummus/salad AND frozen milk/bread/snack/yogurt + golden-corpus regression delta. No live score ships from P0 — owner approves the model before P1 engine edits.
---

# TASK-169A — P0 — recalibration design + blast-radius model (category-relative protein, R2/R3/R4/R5/R6)

## P0 outcome (2026-06-02) — design done, model done, AT OWNER DECISION GATE

- **Design spec:** `01_framework/bsip2_framework/recalibration_p0_design_v1.md` (Nutrition).
- **Blast-radius model:** `02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.md` + data dir (Data).
- **Rollback verified:** all P0 changes gated behind `BARI_RECAL_P0`; flag OFF = byte-identical to HEAD on run_cheese_003 (59/59, 0 mismatch). Golden + router regressions clean OFF and ON.

### Model results (flag ON)
- cottage 1% 74.9/B → 97.8/S · white+garlic 76.9/B → 88.3/A (**R7 inversion resolved**) · cottage 9% 52/C → 89.1/A · napoleon 16% 68.3/B → 81.5/A · veg-spreads +10–12 (clean, none breach 80).
- **Frozen:** snack_bars 0 changes (snk-001 = 70/B HELD ✔). milk: 1 A-crossing (high-protein lactose-free 74.1→87.3, **breaches frozen 85/A ceiling**). yogurt: 15 A-crossings, 3 reach S.

### Finding: combined stack OVERSHOOTS
Directions correct but magnitude too high (dairy mass-produces S). **R1+R2+R4 alone put cottage 1% at 89.76 ≈ the owner's 90/A target** — the R7 +8 fermentation bonus is the dominant overshoot driver and leaks to fluid milk (causes the 85/A breach). R3/R5/R6 well-behaved. Two clear issues: drop/restrict R7; tighten R4 (napoleon garlic+dill 16% wrongly NOVA-demoted to A — flavored-variant exclusion needed).

### Blocking on owner decisions before Nutrition re-tunes + Product co-signs (D7)
1. Drop R7 (R1+R2+R4 already hits the cottage target) vs keep+restrict it.
2. Milk 85/A ceiling breach (1 product) — accept / veto / retune.
3. Yogurt: 15 A's + 3 S's — accept or cap.
4. R4 flavored-variant exclusion (treated as a required fix, not optional).
- Evidence-registry entries EV-029–032 (+EV-027/024 extensions) to be authored before P1 merge.
- **Coverage gap:** bread retail_003 uses a bespoke loader, not in the harness (small radius: R3+R5 only) — dedicated re-model in P1 before any bread frozen sign-off.

## v1.1 re-model (2026-06-02) — design v1.1 implemented, overshoot CORRECTED

Implemented the spec's § v1.1 REVISION (R7 culture-gate + R4 flavored-variant fix; R1/R2/R3/R5/R6 untouched). Outputs: `02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.1.md` + `*_v1.1.json`.

**All acceptance checks PASS:**
- Flag OFF byte-identical (59/59, 0 mismatch on score/grade/every dimension).
- **cottage 1% = 89.8/A** (no +8) — owner 90/A target hit; was 97.8/S in v1.
- **white+garlic inversion resolved** (cottage 89.8 ≥ white+garlic 84.3).
- **Both fluid-milk +8 leaks GONE** — `חלב נטול לקטוז 2%` 87.3/A→**79.3/B** (85/A ceiling leak CLOSED); 0 milk A-crossings; no residual R1-curve milk A-crossing in corpus.
- **napoleon 16% שום שמיר stays NOVA 3 → 74.5/B, does NOT reach A** (was 81.5/A).
- **yogurt bonus retained (legitimately gated):** 35 yogurts +8; 14 A / 3 S (P2 owner review, no hard cap).
- Golden 0 FAIL/1 WARN (flag-insensitive); router all PASS OFF+ON.
- **cheese now 0 S** (v1 had 4) — dairy mass-S overshoot corrected by gating R7.

**Router reconciliation (flagged):** live router emits NO `milk_dairy` and NO top-level `yogurt` category — milk/cheese/yogurt all route to `dairy_protein`; cottage 1% has `subtype=None`. Implemented spec INTENT against real vocabulary (yogurt subtypes; fluid-milk hard-exclude by name token; aged-cheese by name marker; cottage/white-cheese excluded). Fixed `חלב`-in-`חלבון` substring trap via token-aware matching. Aged-cheese subtypes the spec named are not emitted by the router → caught by name marker (flagged for Nutrition/P1).

**One observation (not a leak):** flavored white cheese `גבינה לבנה 5%+שמיר ושום` reaches 84.3/A via the **Path A declared-culture +8** (legitimate, unchanged HEAD behavior) on a lean 5% white cheese; R4 keeps it NOVA 3. Whether to exclude flavored variants from Path A too is a separate Nutrition design call.

**Frozen sign-off table** (deliverable 2) is in the v1.1 report §4. No prior frozen invariant breached: milk 85/A HELD, snk-001 70/B HELD; yogurt A/S is a new owner-reviewable distribution (no prior numeric ceiling). Bread still not wired (bespoke loader) — small R3+R5-only radius, estimated, not blocking.
