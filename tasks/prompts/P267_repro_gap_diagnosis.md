# P267 / Phase-0 reproducibility gap — root-cause diagnosis (READ-ONLY) (route: C1-CURSOR)

Repo C:\Bari (local == origin/master). TASK-418. **READ-ONLY / REPORT-ONLY — make NO file edits, NO commits, NO score changes, no git stash/checkout/reset.** Your entire deliverable is a written report. OFF-BAN ABSOLUTE.

## Context — the blocker
The de-chain program (TASK-419, Stage 2) requires a **byte-identical-OFF reproducible baseline** (Phase-0 prerequisite, non-negotiable per `03_operations/bsip2/proto_v0/reports/d7_cosign_dechain_v1.md`). The reproduction diagnostic `03_operations/page_generator/provenance/_reproduce_diag.py` (run it: `python 03_operations/page_generator/provenance/_reproduce_diag.py`, reads `_reproduce_diag_result.json`) shows the current engine does NOT reproduce the published scores for three live categories — with **grade moves**, which is a hard reproducibility failure:

- **hard_cheeses** (baseline = `bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json`, run_id `run_hc_task412_rt4_fix`): 12 drift, max 12.0, 3 grade moves — bidirectional:
  - `7290110324872`: published A 81.6 → engine B 75.6 (DOWN 6.0)
  - `7290110323301`: published C 62.0 → engine B 74.0 (UP 12.0)
  - `7290110320850`: published C 62.6 → engine B 66.0 (UP 3.4)
- **cheese** (baseline = `cheese_frontend_v4.json`): 22 drift, max 5.3, 2 grade moves (all positive):
  - `3523230065467`: C 63.8 → B 68.0 ; `7290019635581`: E 32.8 → D 37.0
- **cereals** (baseline = `cereals_frontend_v2.json`): 2 drift, 1 grade move: `7290017894911` D 46.0 → C 50.0

Note: ALL 16 live configs have `flags: None`, yet most categories reproduce cleanly — so a blanket missing-flags theory is insufficient. hard_cheeses/cheese/cereals are the outliers. granola now reproduces within grade (drift 2, 0 grade moves).

## Do (diagnosis only)
For EACH of the ~6 grade-moving products above (and characterize the sub-grade drifters in aggregate), determine the ROOT CAUSE of the engine-now vs published divergence. Candidate causes to test explicitly:
1. **Flag-set mismatch** — the published run used a scoring flag (e.g. `BARI_HC_DAIRY_SATFAT_V1`, `BARI_REDLABEL_V1`, `BARI_GRAD_SODIUM_V1`) that the diag's default re-score does not apply. Check the config vs the published `run_id` provenance (`03_operations/page_generator/provenance/provenance_manifest.json`, `03_operations/spine/live_manifest.json`).
2. **Corpus/ingredient drift** — the bsip1 record the engine reads now differs (re-scrape, parser fix) from what produced the published score.
3. **Engine-version drift** — scoring logic changed since publication (a rule added/removed) so the published number is no longer engine-derivable.
4. **Non-engine adjustment** — the published score was hand-set / patched and is not reproducible by ANY engine config (a traceability defect).

## Classify each cause (this is the decision that matters)
- **SCORE-NEUTRAL FIXABLE** (causes 1 & 2, and 3 if the config can pin the exact flags/corpus that reproduce the *published* number): the repair restores reproduction WITHOUT changing any published score. Specify the exact config/flags/corpus edit that would make it reproduce.
- **REQUIRES A PUBLISHED-SCORE CHANGE** (cause 4, or 3 where the old number is genuinely unreproducible): repairing reproduction would mean adopting the engine-now score = **moving a published score = owner tripwire #1**. Do NOT propose doing this silently — flag it explicitly per product so the orchestrator can escalate to the owner.

## Return
- Per grade-moving product: root cause (with evidence: file:line / run_id / flag / trace value), classification (score-neutral-fixable vs requires-score-change), and the precise fix if score-neutral.
- Aggregate root cause for the sub-grade drifters per category.
- Bottom line: can hard_cheeses + cheese + cereals be made to reproduce their PUBLISHED scores score-neutrally? If not, list exactly which products force a tripwire.

End with the return contract (`01_framework/operations/return_contract_v1.md`); status RETURNED, not CLOSED. Read-only — evidence-cited, no writes.
