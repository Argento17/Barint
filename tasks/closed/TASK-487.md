---
id: TASK-487
title: Generator carbs/satFat display backfill (cheese/bread/cereals) — same false-completeness class as milk RT-1
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #69 (v2, merged; origin/master 32198372 ancestor-verified; hard_cheeses carbs 29/31 live). KEY FINDING: carbs/satFat never rendered (NUTRITION_KEYS 4-cell) → owner ruled keep golden panel; real gap = 14 over-claiming confidence labels → corrected + data backfilled from BSIP1 (OFF-clean). Off origin/master (return-1 wrong-base scrapped, v1 branch deleted). Barcode-keyed 0 protected change (only carbs/satFat+confidence+expansion.confidenceLabel on the 14); Adversarial QA PASS (14/14 relabels trace-justified, 0 missed, RT-1 nested-label fixed pre-PR). Live cheese=v5 (agent caught my v4 spec error)."
depends_on: []
blocks: []
category_id: null
summary: >
  Split from TASK-485. The generator NUTRITION_FIELD_MAP drops carbs + saturated-fat on some categories,
  so cheese/bread/cereals comparison pages show those fields blank even though the values exist in our
  BSIP1 scrape. Same false-completeness class the milk red-team (RT-1) caught and TASK-482 fixed for milk.
  FIX: correct the generator field map, backfill carbs/satFat into the affected frontend JSONs from the
  committed BSIP1 trace (NOT OFF, NOT Tzameret-as-authority), and relabel confidence honestly where any
  value is genuinely missing.
---

# TASK-487 — carbs/satFat display backfill (from TASK-485 split)

## Verified context
- Milk red-team RT-1 found carbs/satFat displaying blank while present in BSIP1 → TASK-482 fixed milk by
  backfilling from BSIP1 + relabeling confidence to standard "partial"/"ניתוח חלקי".
- TASK-485 confirmed the same generator NUTRITION_FIELD_MAP gap affects cheese/bread/cereals display and
  SPLIT the backfill here (bigger, touches confidence copy).

## Deliverable (Data owns; do NOT close — propose RETURNED)
1. Locate the generator NUTRITION_FIELD_MAP (page_generator / render-contract layer) and identify why
   carbs + saturated-fat are not mapped into the frontend nutrition block for these categories.
2. Fix the map so carbs + satFat flow through for all categories that have them.
3. Backfill the affected LIVE frontend JSONs (cheese/bread/cereals — confirm which files actually render;
   e.g. bread_frontend_v4, and the live cheese file) from the **committed BSIP1 trace only**. Source rule:
   direct product scrape / BSIP1 parse. **OFF BANNED anywhere. Tzameret is directional-only, never
   authoritative.** If a value is genuinely absent in BSIP1 for a product → leave null and relabel that
   product's confidence honestly ("partial"); do NOT fabricate, do NOT over-source.
4. Zero score/grade/rank/scoring change — this is display-completeness only. Any confidence-copy change is
   consumer-facing → two-gate + owner PR.

## Guards
- OFF ban absolute. No published-score change (tripwire-1). Confirm live-vs-dead file before editing —
  do not backfill a legacy/unrendered JSON.
- Report per-file: products backfilled, products left null (with reason), confidence relabels.

## Return: 5-part + machine-readable Return Contract. Propose RETURNED. Do not write CLOSED.

## RETURN 1 (fb2b2703) — CORRECT DIAGNOSIS, WRONG BASE → CHANGES_REQUESTED (rework off origin/master)
- **Diagnosis verified + valuable:** root cause = NUTRITION_FIELD_MAP (generate_page.py:309) never mapped carbs/satFat; 3 page_output_schema files also block them via additionalProperties:false (additive fix). Live JSONs confirmed 0 carbs/0 satFat (gap is real). BSIP1 source dirs identified per category (bread→run_bread_conform_001, cereals→run_cereals_008, cheese→run_cheese_003, brined→run_brined_cheeses_002, hard→02_products/hard_cheeses/bsip1_task412).
- **KEY FINDING (reframes task):** carbs/satFat are NOT rendered by any component — NUTRITION_KEYS (expansion-section.tsx:729-738) shows only protein/sugar/energyKcal/sodium, every category incl. golden. So the gap is NOT a visible "blank"; it's (a) internal data completeness + (b) 14 products whose confidence label over-claims "full" while satFat/carbs is null. **OWNER DECISION 2026-07-03: keep the golden 4-cell panel — do NOT add carbs/satFat as visible cells. Ship honesty fix + internal backfill only.**
- **BLOCKER = wrong base (F1 divergence):** agent cut its worktree off LOCAL HEAD (feature/homepage-mascots), not origin/master. generate_page.py + 3 schemas share origin base (portable), but the 5 frontend JSONs + view-models DIVERGED — origin/master has NEWER versions (this session's #58 rescore + #62 traceability + #63 phrasing). Merging fb2b2703's JSONs would REVERT live copy/scores. Its "0 score change" was verified vs the stale base, not live. → REDO off origin/master.
- **Process lesson:** every data/frontend dispatch MUST pin base=origin/master explicitly (crackers t486 got it right; this didn't).

## RETURN 2 dispatch — redo off origin/master (owner-scoped: 4-cell panel kept)

## RETURN 2 (460a44e0, branch fix/task487v2-carbs-satfat) + orchestrator-VERIFIED
- **Agent caught orchestrator spec error:** live cheese file = `cheese_frontend_v5.json` (cheese-page-data.ts:4 import; v5 = v4 + de-anchor e953c8d6 + TASK-483 stamp), NOT v4. v4 is stale — agent backfilled v5, left v4. (My local-tree audit read v4 because the diverged local branch lacks v5 — F1 again.)
- **Barcode-keyed verify vs origin/master (all 157 products, 5 files):** 0 illegal changes — ONLY nutrition.carbs/satFat + confidence fields moved. score/grade/rank/rowVerdict/insightLine/comparisonContext/positiveSignals/limitingFactors byte-identical → live rescore/traceability/phrasing preserved.
- **14 confidence relabels** (bread 1, cereals 4, cheese 2, brined 0, hard_cheeses 7) — full/verified→partial only where carbs/satFat genuinely null post-backfill; standard "ניתוח חלקי" pattern reused (no new copy). Backfill 155/157 carbs, 122/157 satFat; bread satFat 0/23 (BSIP1 has none corpus-wide — Israeli bread labels rarely break out satFat). OFF/Tzameret untouched. Generator+3 schemas additive; tsc 0; G7 parity 5/5; cereals+brined G1 fail PRE-EXISTING (identical before/after).
- **OWNER SCOPE-LOCK honored:** NUTRITION_KEYS untouched — carbs/satFat NOT displayed, 4-cell golden panel preserved.
- **Adversarial QA = CONDITIONAL PASS** (a10bb9fb): Track V fully green (0 field drift re-derived independently, gates PASS, tsc 0, render clean, cheese=v5 confirmed). Track C: 14/14 relabels trace-justified to BSIP1 (satFat/carbs genuinely null + was full/verified), 0 missed over-claims, OFF/Tzameret clean, 4-cell panel preserved. 0 CRIT/0 HIGH.
  - **RT-1 (MEDIUM, being fixed pre-PR):** the 14 relabeled products' nested `expansion.confidenceLabel` still held the stale full/verified string while top-level confidence_label_he was correctly flipped. Dormant (render falls back to it only when confidence_label_he empty — it isn't) so non-visible, but a 2nd field still asserting "full data" = the exact false-completeness this task kills → NOT logged as debt, fixing now. Data Agent resumed (ab61ede4) to patch expansion.confidenceLabel on the 14 to the standard partial string + re-verify only-that-field-changed.
- **RT-1 FIXED (commit 80890c8c):** 14 expansion.confidenceLabel → "ניתוח חלקי" (byte-identical to existing partial exemplars in same files). Orchestrator final barcode-keyed verify vs origin/master: change set = 14 top-confidence relabels + 14 expansion.confidenceLabel + 241 carbs/satFat field-changes; **0 illegal changes**. tsc 0, G7 parity 5/5.
- **🚀 PR #69 OPENED** https://github.com/Argento17/Barint/pull/69 (14 visible confidence downgrades = owner merge, tripwire-2). Two-gate satisfied (relabels reuse standard approved partial pattern → no new copy; Adversarial QA CONDITIONAL→now full PASS after RT-1). Stale v1 branch fix/task487-carbs-satfat-backfill DELETED on origin. CLOSE on merge; prune t487v2.
