---
id: TASK-144
title: Diagnose why יופלה GO (clean, additive-free, 10g protein) scores only 70/B; propose a governed scoring fix going forward
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Ported engine 0.4.1 into the live page surgically (71 products updated, all 87 verdicts preserved \u2014 no builder rebuild)"
depends_on: []
blocks: []
category_id: maadanim
summary: >
  Product Owner review (2026-06-01): יופלה GO מועשר בחלבון is the cleanest item on the maadanim shelf — 3 dairy ingredients (חלב, חלבוני חלב, אבקת חלב), NO added sugar/starch/stabilizers/sweeteners/colors, 10g protein/100g (20g per 200g cup), 72 kcal, sugar=None — yet engine 0.4.0 scores it 70/B. PO believes >=85. Nutrition to: (1) pull the BSIP2 trace and pinpoint where points are lost; (2) judge if the cap is justified; (3) propose a governed scoring fix per bsip2-scoring-governance (evidence registry, activation scope, rollback). Likely connected to the dairy A-ceiling philosophy (TASK-139A ruling, DEC-005). Do NOT unilaterally edit the frozen published score (TASK-136).
---

# TASK-144 — Diagnose why יופלה GO (clean, additive-free, 10g protein) scores only 70/B; propose a governed scoring fix going forward

## Diagnosis (2026-06-01, nutrition-agent)
Full diagnosis: `02_products/maadanim/go_score_diagnosis_144.md`.

**Where the points go:** Not a cap, not a dessert ceiling. The `NOVA_PROXY_3_PROCESSED` cap (87) is
non-binding; the 69.58 is the **raw weighted dimension sum**. Three dimensions bleed points:
- `nutrient_density` 32.5 — fiber absent treated as 0 at 35% weight (dairy has no fiber by nature).
- `processing_quality` 65 + `whole_food_integrity` 60 — driven by **NOVA 3**.
- `protein_quality` 42.5 — dairy protein typed `mixed` ×0.85.

**Root cause:** OCR bleed inflated `ingredient_count` to 8 (only 3 are real ingredients; items 4–8 are
nutrition-panel text + site disclaimers). With 0 additives and 0 added sugars, the ONLY thing forcing
NOVA 3 (vs NOVA 2) is `ing_count > 5` in `nova_proxy.py:117` — i.e. NOVA 3 is wrong-on-the-data.

**Verdict:** 70/B is too low by ~6–7 pts. Corrected honest score ≈ **77/B**. **85/A is NOT justified** —
GO has no confirmed live culture (`has_fermentation:false`) and is a reconstituted/protein-enriched matrix,
so it FAILS conditions C3 + C4 of the governing **RULING-DAIRY-A-01 (TASK-139A)**. Granting A would
contradict 139A. Recommendation is consistent with 139A and DEC-005.

**Proposed governed fix (3 changes, all evidence-grounded, all reversible, none grants A):**
1. Sanitize `ingredient_count` (strip OCR/disclaimer bleed) upstream → NOVA 3→2 (+4.0 → ~73.6/B).
2. Fiber "absent vs zero" for fiber-free dairy categories (gated) → nutrient_density 32.5→50 (~76.2/B).
3. Dairy protein source typing (drop ×0.85 "mixed" for pure dairy) → ~77.0/B. (calibration, optional)
Net: 69.6 → ~77/B, grade stays B. DEC-004 gates Fix 2/3 magnitudes; full re-run + regression required.

## Implementation (2026-06-01, nutrition-agent) — engine 0.4.0 → 0.4.1
PO approved ("Approved for 77. Agree with logic."). All three fixes implemented, gated, reversible.
Full delta: `02_products/maadanim/task144_delta_report.md`. Data: `task144_delta_data.json`,
`task144_blast_radius.json`.

**GO result:** 69.6/B → **77.7/B** (rounds 78/B). NOVA 3→2, nutrient_density 32.5→50, protein_quality
42.5→50, WFI 60→85. **A NOT reached** (fails RULING-DAIRY-A-01 C3/C4). Dairy A-ceiling holds.

**Three fixes (+ a macro-plausibility companion guard):**
1. EV-026 — ingredient-bleed sanitizer (`signal_extractor.sanitize_ingredient_list`); count 8→3 → NOVA 3→2. Data hygiene, no scoring rule.
2. EV-027 — fiber "absent≠zero" for fiber-free dairy; **tight allowlist** `(dessert, dairy_protein, yogurt)`; bread/cereal/bars EXCLUDED (verified 0 changes).
3. EV-028 — dairy protein source typing (mixed→dairy, drop ×0.85); **no collision with F2/TASK-133B** (mutually exclusive gates, verified).
   Companion: macro-plausibility guard flags impossible macros (protein_g=190 OCR artifact) as insufficient_data.

**Activation scope:** maadanim run only via `BARI_TASK144_FIXES` (default OFF; `batch_run_maadanim_001.py` opts in).
Engine version bumped to **0.4.1** (`trace_writer.py`). Evidence registry updated. scoring.md updated.

**Blast radius:** cereals/bread_light = 0 changes (gate tight). Frozen isolation PROVEN: golden corpus PASS
(whole milk 85/A, go-milk 41.4/E), yogurt_003 = 0 diff vs frozen, router regression all PASS. Fix 2/3 WOULD
lift frozen yogurt/cheese (incl. 3 B→A) if enabled there — architecturally correct (milk 85/A precedent) but
OUT OF SCOPE → **escalated to Product Agent**, not deployed to frozen categories.

**Maadanim grade tally (0.4.1, 200):** A:1 · B:4 · C:53 · D:84 · E:26 · insufficient:32.
The single A is `גבינה צפתית מעודנת 5%` — a mis-binned cheese (not a dessert, false sugar signal), **NOT on
the live 87 shelf**. **Live maadanim shelf has NO A.** 21 TASK-144-attributable grade changes (mostly D→C/E→D).

**Frontend NOT touched** — `maadanim_frontend_v2.json` (87 `rowVerdict` strings) left intact for CC surgical reconcile.

## Live deployment (2026-06-01, CC — PO approved "Deploy maadanim recalibration")
0.4.1 scores/grades ported **surgically** into `maadanim_frontend_v2.json` (71 products updated; the 87
`rowVerdict` strings preserved, not rebuilt). **GO now 78/B.** Displayed shelf (76, post-137F exclusions):
**B:2 · C:23 · D:40 · E:11** (was 1/16/47/12) — all 13 grade moves upward (11 D→C, 2 E→D). **No A on the live shelf.**
Verdict re-sync: only 2 verdicts cited a now-stale claim — GO ("היחיד שמגיע ל-B" → 2 B's exist) and מילקי שוקולד
("הציון הנמוך בה" → E's score lower); both rewritten. Typecheck green.

Cross-category frozen adoption deferred → **TASK-146** (Product). Source-data anomalies → **TASK-147** (Data).

## Disposition: RETURNED → ready for CLOSED
Engine 0.4.1 deployed to the live maadanim page; rollback = unset `BARI_TASK144_FIXES`. **Central Controller to
record the maadanim baseline re-freeze at 0.4.1 + CLOSE.** (Note: supersedes the 0.4.0 sync TASK-136 was tracking
for maadanim — recommend folding TASK-136 into this re-freeze.)
