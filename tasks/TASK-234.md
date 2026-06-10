---
id: TASK-234
title: "Salty-snacks v4 red-team remediation — systematize the 0.5g trans-declaration guard (corpus-wide), fix beet-cracker NOVA/ingredient contradiction, correct implausible kcal/fiber"
owner: data-agent
status: CLOSED
closed_at: 2026-06-10
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-231, TASK-229]
blocks: [TASK-232]
roadmap_impact: true
work_type: data-remediation
close_reason: "Orchestrator+QA verified. RT-2: 0.5g trans-declaration artifact systematized corpus-wide — 9 products de-artifacted, re-scored on UNCHANGED engine (Bamba 61→63, Apropo Italiano 42→43, matching red-team predictions). RT-7: NOVA/ingredientCount contradiction resolved — runtime VM now suppresses novaGroup when ingredientCount=0 (0 contradictions ship). MEDIUM: fabricated 38g fiber corrected (Click 25→14/E); 3 unrecoverable kcal-basis chips dropped (41→38). Final: 38 products, grades B11 C16 D4 E7, 0 score==0, all consumer strings is_clean, tsc+build clean. No engine/cap/veto change. RT-3 (veto philosophy) routed to Nutrition as non-blocking."

# TASK-234 — Salty-snacks v4 red-team remediation

Red-team challenge (`02_products/salty_snacks/reports/red_team_salty_snacks_v4.md`) returned
CONDITIONAL PASS (no CRITICAL — QA Hard Rule 9 gate satisfied), but 4 HIGH + 5 MEDIUM. The
score-quality items below are in-lane data corrections (no scoring-engine change). Branch
`salty-snacks-v4`.

> **Attribution note (2026-06-10):** these corrections shipped into `salty_snacks_frontend_v4.json`
> via the TASK-233B shared-core regeneration (the generator source carries 234's
> `BASIS_ERROR_EXCLUDE` + fiber/kcal/trans fixes). Live deltas surfaced by that regen — count 41→38;
> scores 7290000066318 61→63, 7290104500572 42→43, 7290112494313 25→14; grade 7290000066332 C→B
> (disk→runtime alignment). QA verified engine unchanged / score-neutral / no methodology change —
> these are **234's** corrected-input deltas, not 233's. Do not revert. This task should own them in
> its return block.

## Fix these

- **RT-2 (HIGH) — the 0.5g trans artifact is CORPUS-WIDE.** We fixed only the two products where the
  bad per-100g value happened to compute to a veto. But OFF `trans-fat_serving = 0.5g` is the
  Israeli "<1g" THRESHOLD DECLARATION, and wherever it was divided by a non-100g serving it yields a
  bogus per-100g trans (0.625 / 0.6 / 0.4 / 1.25 …). במבה קלאסי (−20) and אפרופו איטליאנו (−20) carry
  the same signature and are penalized on fake data. **Systematize the guard:** detect the
  0.5g-serving-declaration-scaled artifact wherever it appears (not just `trans == 0.5` exact),
  neutralize trans to 0.0 at BSIP1 with a `data_corrections` log entry, re-score every affected
  product on the UNCHANGED engine. Report the full corrected list + score deltas.
- **RT-7 (HIGH) — beet-cracker NOVA/ingredient contradiction.** BSIP1 = NOVA-4 + 15-item ingredient
  list; frontend = NOVA-3 / ingredientCount 0. Make published novaGroup, ingredientCount, and
  ingredient text internally consistent for `7290112968807`; scan the corpus for any other
  novaGroup-vs-ingredientCount mismatch.
- **MEDIUM — implausible per-100g values (basis errors):** 3 "chips" at 128–145 kcal/100g (real ≈
  450–550) and a product at ~38g fiber/100g. Verify against source, correct the per-100g basis, or
  omit if unrecoverable. Re-score affected items.

## Out of scope (route elsewhere)
- RT-3 (whether a hard trans-veto should fire on absence-of-PHVO data): scoring-philosophy →
  Nutrition/owner (noted in TASK-229).
- NOVA-2-by-absence labelling (31/32 NOVA-2 with no ingredients): already disclosed to consumers; a
  methodology question for Nutrition, not a data bug.

## Acceptance criteria
- [ ] All 0.5g-declaration trans artifacts neutralized corpus-wide; affected products re-scored (list + deltas)
- [ ] Beet-cracker novaGroup/ingredientCount/ingredients consistent; corpus scanned for other mismatches
- [ ] Implausible kcal/fiber corrected or omitted; affected re-scored
- [ ] No scoring-engine change; every imageUrl still 200; all consumer strings still is_clean; tsc+build clean
- [ ] Corpus regenerated; grade distribution reported (pre vs post)

## Return block
Products corrected for the trans artifact (+ deltas), the NOVA/ingredient resolution, kcal/fiber
corrections, new grade distribution, and gate confirmation. Do NOT close — RETURN for orchestrator
verification + re-QA.
