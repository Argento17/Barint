---
id: TASK-456
title: De-anchor train finish: reconcile protein_bars (config repoint) + hard_cheeses (barcode normalize) corpora, then de-anchor + ship
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: protein_bars
summary: >
  Last 2 de-anchor cars are corpus-reconciliation, not missing data. protein_bars: config corpus_dirs points at bsip2 output (rerank/run_record only, no bsip1 products) -> repoint to canonical bsip1 (02_products/snack_bars/canonical_bsip1 or score_bars_task362_*). hard_cheeses: run uses HC-/hardcheese_ barcode prefixes -> 24/31 reconcile after norm, 7 stragglers to inspect. Reconcile all live barcodes re-scorable, then de-anchor (BARI_REDLABEL_CONTINUOUS_V1=on, corpus-pinned) + Content/QA + ship. Do not ship a half-scored page (all-or-flag per missing-data-discard).
---

# TASK-456 — De-anchor train finish: reconcile protein_bars + hard_cheeses, then de-anchor + ship

## Outcome (2026-07-02)
Reconciliation DONE for both (corpora now proven traceable). De-anchor outcome differs per car:

### hard_cheeses — RECONCILED, de-anchor NO-OP → nothing to ship
- All 31/31 live barcodes reconcile to `bsip1_task412` (the 7 "stragglers" were format-variant false positives, all present under bare barcodes). Loader gap fixed via a file_type bridge (bsip1_enriched→product), not a code change.
- Config already carried `BARI_REDLABEL_V1: on` → the continuous flag is a no-op. **0 score-moves, 0 grade-flips, 0.000 drift vs live v4.** Grade dist unchanged A1/B26/C4. Like bread: nothing to ship. (Corpus traceability confirmed — value for [[corpus_traceability_program]].)

### protein_bars — de-anchor HELD (fails the reproduction gate)
- 32/32 reconciled. True corpus = SHA-pinned `protein_combined_corpus_task365_33_...json` (the brief's candidates covered only 2/32 — Data corrected).
- **Engine gap found:** the approved protein-bar lens `apply_protein_bar_lens()` (polyol tiers, isolate-stacking penalties, PROTEIN_BAR_WEIGHTS, bar-specific caps) is **NEVER called from `score_engine.py`** (only referenced in a comment ~line 2334). The generic engine path silently substitutes default weights/caps → a false 26/32 D/E collapse. Data correctly halted and drove the real lens (`batch_run_protein_bars_task365.py`, the path that MADE the live page).
- **Reproduction FAILS:** flag-OFF lens reproduces live SCORES but NOT live GRADES — 2 products grade C at flag-off where live shows D (same score). So of the 5 flag-on "D→C flips", only **3 are genuine de-anchor** (7290112915382/913487/915351, +7.4/+10/+8.6); **2 are driver-vs-live grade-boundary artifacts** (7290019766230, 7290019401544 — already C at flag-off; flag actually lowers their score). The de-anchor delta cannot be cleanly isolated from the driver's grade-boundary discrepancy → shipping would mislabel drift as de-anchor + re-baseline 2 products. Held per the TASK-429 reproduction discipline + [[uniform_baseline_clean_up_doctrine]].

## Follow-up (real engine debt, routes to Nutrition/Data)
Wire `apply_protein_bar_lens` into the uniform `score_engine.py` path AND resolve why its grade-boundary logic diverges from the live protein_bars grades, so flag-off byte-reproduces the published page (scores AND grades). THEN protein_bars re-scores canonically with standard traces + standard QA, and its genuine 3-flip de-anchor ships cleanly. Two approved-but-worktree-absent files (`rescore_task365_inplace.py`, `batch_run_protein_bars_task365.py`, on master@6871d374) should be merged into the shared pipeline branch as part of that wiring.

status note: reconciliation deliverable COMPLETE; protein_bars de-anchor BLOCKED on the engine-wiring + grade-reproduction follow-up above.
