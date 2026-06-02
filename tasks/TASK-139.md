---
id: TASK-139
title: "Dairy Scoring Calibration (shared by yogurt + cheese): enricher culture-vocab + router yogurt-anchor + dairy A-ceiling ruling"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "The parent objective has been achieved: the yogurt governance stack was stress-tested, the router defect was fixed, culture detection now genuinely feeds scoring, the category was re-scored, and the final result is evidence-based rather than assumption-based."
depends_on: []
blocks: [TASK-142, TASK-143]
category_id: null
summary: >
  Resolve the three engine calibration gaps a real ingredient-bearing dairy corpus exposed in run_yogurt_003,
  governed under bari-bsip2-scoring-governance (evidence registry + label observability + rollback). One
  workstream serves BOTH yogurt and cheese (fermented dairy). 139A = Nutrition dairy A-ceiling ruling;
  139B = Data enricher FERMENTATION_TERMS extension to Israeli label vocab; 139C = Data router yogurt-anchor
  + 'יווני' olive false-positive fix. Exit: re-score run_yogurt_003 corpus, Nutrition confirms truthful
  movement, QA confirms golden corpus 12/12 PASS and no movement on frozen milk/bread/snack scores.
---

# TASK-139 — Dairy Scoring Calibration (parent)

Source of the gaps: run_yogurt_003 reconciliation
(`02_products/yogurt_system/reports/reconciliation_135_run_yogurt_003_findings.md`). Engine 0.4.0.
Governed change — published dairy scores will move; Nutrition + Product co-sign; rollback = git revert of engine modules.

## Sub-tasks
| Sub | Owner | Deliverable | Deps |
|-----|-------|-------------|------|
| **139A** | Nutrition | Dairy A-ceiling ruling: does plain live-culture dairy reach A, or is B the truthful ceiling? Evidence-registered rationale. | — |
| **139B** | Data | Extend `ingredient_enricher.py` FERMENTATION_TERMS to Israeli label vocab (`חיידק פרוביוטי`/`ביפידוס`/`BIFIDUS`/`תרבית`); regression-lock. Serves yogurt + cheese. | — |
| **139C** | Data | Fix router yogurt-anchor (flavored->dessert, crunch->cereal misroutes, 19%->target <5%) + 'יווני/Greek' olive false-positive into whole_food_fat. | — |

## Exit / DoD
- Re-score the run_yogurt_003 88-SKU corpus on the patched engine.
- Nutrition: confirms scores moved truthfully and cultures are now credited (was 0/88).
- QA: golden regression corpus **12/12 PASS**; **frozen milk/bread/snack scores unchanged** (CNO invariants).
- All changes logged to the evidence registry with rollback note. Then propose RETURNED.

---

## Return block — proposed RETURNED (parent closing re-score, Nutrition + Data, 2026-06-01)

**Outcome: re-score executed, cultures now credited, all guards green, frozen invariants
provably unmoved. A material gap was surfaced and closed in-flight (below). 0 grade-A is the
TRUTHFUL result for this corpus — not a failure. Proposing RETURNED.**

### What the re-score surfaced (the reason this was not a no-op)
Re-running `batch_run_yogurt_003.py` on the cleaned 86-SKU corpus with 139B/C/D in place
produced a distribution **byte-identical to the pre-139B baseline** (0 A, B17/C44/D24/E1).
Root cause: **TASK-139B patched the BSIP1 enricher only.** The BSIP2 scorer derives
`has_fermentation` from an INDEPENDENT list (`signal_extractor.FERMENTATION_MARKERS_HE`) and
never reads the BSIP1 flag. So run_yogurt_003 **detected 49/86 live-culture SKUs in BSIP1 yet
credited 0/86 in the score** (`fermentation_bonus_applied`=0). 139B's "feeds the already-active
EV-015 bonus" claim is false for BSIP2 scoring. Without closing this, the parent DoD
("cultures now credited") is unmeetable by re-running.

### Fix applied (governed, collision-audited)
Mirrored 139B's vocabulary into `signal_extractor.FERMENTATION_MARKERS_HE` (תרבויות,
חיידק פרוביוטי +construct/plural, חיידקי ביפידוס/יוגורט/אצידופילוס, ביפידוס/bifidus, תרבית).
Non-interpretive substring matching only — **no new rule/weight/threshold/cap**; it only lets
the already-active R-02 + WFI fermentation bonus see real labels. Logged **EV-024**.

### Re-score delta (86 SKUs, patched scorer)
| Grade | Before | After |
|---|---|---|
| A | 0 | **0** |
| B | 17 | **29** |
| C | 44 | **32** |
| D | 24 | 24 |
| E | 1 | 1 |

Median 55.7→**56.1**; ceiling 78.2→**78.7/B**. BSIP2 `has_fermentation` 3→**34**;
**12 live-culture SKUs C→B.** No A manufactured.

### Nutrition truthfulness sign-off — 0 A is correct
- **No SKU satisfies RULING-DAIRY-A-01 C1–C6** in run_yogurt_003. NOVA dist: **0×N1, 4×N2,
  36×N3, 48×N4.**
- The only 4 clean NOVA-2 plain/goat yogurts (incl. natural goat yogurt — the milk-goat=85/A
  analog) have **empty ingredient panels** → C3 (culture *confirmation*) is impossible, and
  they are dimensionally capped **65–72/B** by low `nutrient_density` (10–26)/`protein_quality`,
  **not** by any cap and **not** by missing culture credit.
- Every higher scorer (≤78.7) is a NOVA-3/4 engineered/sweetened yogurt → fails C1/C2.
- ⇒ **B/78.7 is the truthful ceiling for this corpus.** Forcing an A would be the category
  A-grant C1–C6 explicitly forbids. This **upholds 139A's qualitative ruling** (B truthful for
  the mainstream; A reachable in principle, earned only) and **corrects its quantitative
  "~2–5 earned A's" estimate to 0** for this corpus.

### QA guards — PASS
- **Collision audit:** 0 `has_fermentation` flips on every frozen/non-dairy corpus
  (milk_001/002, snacks run_001, bread_light_001, bread_retail_003 [262-file scan],
  cereals_001/002, hummus_001).
- **Frozen isolation** (OLD-vs-NEW marker toggle, in-memory full-pipeline recompute):
  **milk_004 top = 85.0/A unchanged · snacks top = 70.0/B (snk-001) unchanged · 0 SKUs moved
  by this patch.** (Note: a 7/41 movement vs the *stored* frozen traces is pre-existing
  **committed TASK-133 0.4.0** engine drift, not this change — the named CNO ceilings hold.)
- **Golden structural regression:** 11 PASS / 1 WARN (`anchor_soy_drink`, pre-existing &
  change-independent) / 0 FAIL.
- **Router regression:** 12/12 PASS.

### Rollback
Working-tree edit (uncommitted). Restore the `FERMENTATION_MARKERS_HE` block in
`signal_extractor.py` → reverts `has_fermentation` to 3/86 and the distribution to
B17/C44/D24/E1. run_yogurt_003 BSIP2 output is NON-AUTHORITATIVE; re-score is idempotent.

### For the Central Controller / Product (decisions, not mine to record)
1. **Product co-sign** the published-candidate movement (12 SKUs C→B via culture credit;
   still 0 A) — 139A flagged this consequence; here it is realized.
2. **Registry bookkeeping:** TASK-139B was recorded **CLOSED on BSIP1-only detection**; its
   score-crediting DoD was actually completed by THIS parent fix. CC to decide: reopen 139B,
   open a 139E, or note-in-parent. Per Registry First I did **not** alter 139B's `status:`.
3. **Standing ⚠️ (unchanged from 139B/C):** the global router + culture vocab will reclassify/
   credit ~8 live **maadanim** SKUs on a future re-score — Nutrition/Product co-sign before that
   page moves. Shipped maadanim JSON untouched.

### Open / non-blocking
- **Nutrition calibration question:** goat-milk 85/A vs goat-yogurt 66.7/B — is yogurt
  `nutrient_density` scored too harshly vs the milk table? Separate investigation; does not gate
  this re-score (the clean candidates lack panels regardless).
- BSIP1 49 vs BSIP2 34 `has_fermentation`: ~15 SKUs use culture vocab still unmirrored (all
  NOVA-3/4 sweetened → cannot reach A).
- 2 orphan trace dirs (the 139C-excluded `זית ירוק יווני` olives) remain under
  `run_yogurt_003/products/`; `run_summary.json` correctly excludes them. Cosmetic deletion was
  declined by the destructive-op guard — flag for manual cleanup.

**DoD status:** re-score done ✅ · cultures credited (0→34 scored, 49 detected) ✅ · Nutrition
truthfulness sign-off ✅ (0 A is truthful) · golden regression green ✅ · frozen invariants
unmoved by this change ✅ · EV-024 logged with rollback ✅. **Proposing RETURNED — only the
Central Controller records CLOSED, and the Product co-sign in item 1 must precede any live
yogurt grade publication. Unblocks TASK-142 / TASK-143.**
