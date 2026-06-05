---
name: bsip2-run-yogurt-003
description: "run_yogurt_003 (Shufersal) — resolved the OFF ingredient blocker (0%→90%, insufficient 48%→0%) but NO-GO to retire DEC-005; exposed 3 engine calibration gaps (all resolved TASK-139); parent re-score found a BSIP1→BSIP2 culture-credit propagation gap; B/78.7 is the truthful 0-A ceiling"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8fdd3b58-a591-4444-b034-e3523c3ab130
---

run_yogurt_003 executed 2026-06-01 (data-agent, TASK-135). Full real BSIP0→BSIP2 cycle from
**Shufersal** product pages, engine 0.4.0 unmodified, no manual score edits.

**Why it matters:** this RESOLVED the run_yogurt_002 / TASK-135A blocker. OFF was ingredient-blind
(0% ingredients, 48% INSUFFICIENT). Shufersal gives **90% ingredient + 90% nutrition coverage, 0%
INSUFFICIENT, differentiated NOVA (2/3/4)**, Hebrew names + gtin13 barcodes. Shufersal is the
validated yogurt source — confirms the [[bsip0-retailer-access-001]] Shufersal path and reuses the
maadanim Shufersal scraper pattern.

**How to apply:** Shufersal is GO for any future Israeli packaged-food category needing ingredients.
But run_yogurt_003 is **NON-AUTHORITATIVE evidence — not a shippable shelf.** DEC-005 manual shelf
stays LIVE; TASK-135 stays BLOCKED (blocker reclassified from "no data source" to "engine
calibration"). Do NOT promote this run to frontend.

## Numbers (88 scored)
- Score median 57 (vs manual shelf 72, OFF 70); ceiling 78/B; **0 grade-A**; B17/C46/D24/E1
- 60% NOVA 4 — engine now sees added sugar / modified starch (E-1442) / stabilizers in real labels
- Machine run scores LOWER but MORE truthfully than OFF (which over-credited because blind)

## Three calibration gaps a real ingredient corpus exposed (the new blocker)
1. **Router yogurt-anchor gap** — 17/88 (19%, live 18/88=20%) misrouted: flavored "GO" → dessert, crunch →
   cereal/granola, and "זית ירוק יווני" (olives) false-positive via "יווני/Greek" include token →
   whole_food_fat. ✅ **RESOLVED (TASK-139C, RETURNED 2026-06-01):** added 8 yogurt sub-brand anchors
   (`יופלה go`/`מולר מיקס`/`מולר פרוטאין`/`מולר פרופ`/`דנונה פרו|ביו|יווני`/`דנונ.פרו`) to dairy_protein
   above the topping/dessert anchors; dairy-head topping suppression (yogurt+`קראנצ קורנפלקס`); olives
   excluded at curation (`זית` before the `יווני` include, `יווני` kept for real Greek yogurts; corpus
   88→86). **Misroute 20%→0% (0/86), golden 12/12 PASS, frozen milk/cereals/bread/hummus/snacks 0 changes.**
   ⚠️ Global router → reclassifies 8 LIVE maadanim products dessert/snack→dairy_protein (protein/mix spoon
   yogurts — a correction of pre-existing inconsistency); shipped JSON unchanged; folds into the pending
   maadanim re-score (Gap 3 / dairy↔dessert boundary, needs Nutrition/Product co-sign). Report:
   `02_products/yogurt_system/reports/router_misroute_fix_139C.md`.
2. **Enricher culture-vocabulary gap** — was 0/88 fermentation markers. Israeli labels write
   `חיידק פרוביוטי`/`ביפידוס`/`BIFIDUS`/`תרבית`; old FERMENTATION_TERMS only matched
   `תרבויות`/`ביפידובקטריום`/`לקטובציל`. ✅ **RESOLVED (TASK-139B, RETURNED 2026-06-01):** extended
   `FERMENTATION_TERMS` in `03_operations/bsip1/core/ingredient_enricher.py` (NOT `core/…` — monorepo
   path) with the observed Israeli vocab (non-interpretive substring matching, no new scoring rule).
   Detection **0/88 → 49/88 has_live_cultures** (51/88 any marker). Feeds active EV-015 bonus, satisfies
   EV-021 C3. Guards held: golden regression 11P/1W(pre-existing)/0F, enricher tests 64/64, frozen
   milk/bread/snack 0 new markers (collision-audited). Logged **EV-022**. Re-run:
   `enrich_runner.py --run run_yogurt_003` (run now registered in RUNS). ⚠️ Future maadanim re-score
   will newly credit cultures (~30 SKUs) — correct dairy behavior, flagged for Nutrition/Product.
3. **Dairy A-ceiling** — Nutrition/Product philosophy call: is mainstream Israeli yogurt's true ceiling
   B (engine's read), or should plain live-culture yogurt reach A (manual shelf assumption)?
   **RULED (TASK-139A, RETURNED pending Product co-sign):** A IS reachable — plain, additive-free,
   live-culture dairy (yogurt + white cheese) inherits the frozen **milk** precedent, NOT the snack-bar
   B-ceiling. B is the truthful ceiling for the sweetened/stabilized mainstream (~60%), not the category.
   The "0 A" is mostly the Gap 2 culture-detection bug, not philosophy — fixing it yields ~2–5 *earned*
   A's. Exact condition = C1–C6 (no added sugar · no engineered additives · culture confirmed+credited ·
   intact dairy matrix · correct routing · verified conf). Registered **EV-021**. ⚠️ A-threshold (80 vs
   85) must be reconciled before 139B publishes grades. Ruling:
   `02_products/yogurt_system/reports/dairy_a_ceiling_ruling_139A.md`.

## TASK-139 parent closing re-score (2026-06-01) — propagation gap + truthful ceiling
**Non-obvious gotcha:** culture detection lives in TWO independent layers. TASK-139B patched only
the **BSIP1 enricher** (`ingredient_enricher.py FERMENTATION_TERMS`). The **BSIP2 scorer** derives
`has_fermentation` from its OWN list (`signal_extractor.FERMENTATION_MARKERS_HE`) and never reads
the BSIP1 flag. So 139B detected 49/86 live-culture SKUs in BSIP1 but credited **0/86 in the score**
(`fermentation_bonus_applied`=0; distribution identical to pre-139B). The parent re-score caught it.
**Fix:** mirrored 139B's vocab into `signal_extractor.FERMENTATION_MARKERS_HE` (collision-audited:
0 has_fermentation flips on all frozen/non-dairy corpora; frozen milk 85/A + snk-001 70/B unmoved by
an OLD-vs-NEW toggle isolation test). Logged **EV-024**. Delta: B17→29, C44→32, D24=, E1=, median
55.7→56.1, ceiling 78.2→78.7/B, has_fermentation 3→34, **A 0→0**.

**Truthful 0-A finding (Nutrition sign-off):** crediting cultures yields **NO grade-A** — and that
is correct, not a bug. NOVA dist = 0×N1 / 4×N2 / 36×N3 / 48×N4. The only 4 clean NOVA-2 plain/goat
yogurts have **empty ingredient panels** (C3 culture-confirmation impossible) and are dimensionally
capped 65–72/B by low `nutrient_density` (10–26)/`protein_quality`, not by any cap. All higher
scorers are NOVA-3/4 engineered/sweetened (fail C1/C2). **B/78.7 is the truthful ceiling for this
corpus.** This UPHOLDS 139A's qualitative ruling but **corrects its quantitative "~2–5 earned A's"
to 0** for run_yogurt_003. **How to apply:** before any future dairy re-score, mirror culture vocab
into BOTH layers; don't assume BSIP1 enrichment reaches the score. Open Nutrition question: goat-MILK
85/A vs goat-YOGURT 66.7/B — is the yogurt `nutrient_density` band too harsh vs the milk table?

TASK-139 parent proposed **RETURNED** (CC records CLOSED; Product co-sign required for the 12 C→B
movement before any live yogurt grade publishes). 139B was CLOSED on BSIP1-only detection — its
score-crediting DoD was actually completed here; CC to decide bookkeeping. See [[bsip2-task133-and-maadanim-drift]].

## Files
- Scraper: `03_operations/bsip0/scrape/shufersal_yogurt/01_scrape_yogurt.py`
- BSIP1 builder+curation: `…/shufersal_yogurt/02_build_bsip1_yogurt.py` → `03_operations/bsip1/run_yogurt_003/output/` (88) + curation_report.json
- BSIP2 batch: `03_operations/bsip2/proto_v0/src/batch_run_yogurt_003.py` → `02_products/yogurt_system/bsip2_outputs/run_yogurt_003/` (88 traces) + NON_AUTHORITATIVE.md
- Findings + GO/NO-GO: `02_products/yogurt_system/reports/reconciliation_135_run_yogurt_003_findings.md`
- Source assessment (prior subtask): `…/reports/source_assessment_135_run_yogurt_003.md`

[[project-maadanim-001]] [[bsip0-retailer-access-001]]
