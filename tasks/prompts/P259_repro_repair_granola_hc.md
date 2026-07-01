# P259 / Repro repair — granola + hard_cheeses baselines don't reproduce (route: C1-CURSOR)

Repo C:\Bari (local master == origin/master). TASK-418. SCORE-NEUTRAL repair only — you are restoring the engine's ability to reproduce ALREADY-PUBLISHED scores; you must NOT introduce any new score/grade move. STAGING ONLY: no commit/push/deploy (owner-gated). OFF-ban absolute. Touch ONLY the files below (03_operations page-generator/config/conformance + the two BSIP1/config sources). Do NOT touch bari-web frontend JSON/components.

## Evidence (read first)
The 2026-07-01 de-chain activation eval found 2 categories fail to reproduce their committed published scores:
- `_rescore_staging/_dechain_activation_eval_20260701/granola_eval.json`
- `_rescore_staging/_dechain_activation_eval_20260701/hard_cheeses_eval.json`
- `_rescore_staging/_dechain_activation_eval_20260701/aggregate_activation_eval.json`
Also read the TASK-409 pattern: `03_operations/page_generator/surgical_repro_patch.py` (the tool prior repro repairs used — patch score/grade to committed-trace while preserving copy) and `03_operations/page_generator/conformance.py`.

## Two repairs
1. **granola** — 2 products (barcodes 7290011668587 and 7290014471443) recompute +16 / +20 vs the committed published score (baseline not reproduced). AND conformance HARD-3: the live_manifest still points to `granola_frontend_v1.json` while disk/route serves v2. Fix: (a) repoint the granola config/live_manifest v1 -> v2 so config == served; (b) reconcile the 2 products so the engine reproduces the committed published score via the surgical repro-patch pattern (patch to committed-trace, preserve copy) — do NOT invent a new score; if the committed value cannot be reproduced even after the manifest fix, STOP and report exactly why (do not override).
2. **hard_cheeses** — the eval reported matched=0 and a conformance path bug `C:\Bariari-web\...` (a string-concat missing a separator — likely `C:\Bari` + `ari-web`), plus baseline v4 not in the manifest. Fix the conformance path concatenation bug so the hard_cheeses baseline file resolves, add/repoint the v4 baseline in the manifest, then re-run conformance for hard_cheeses and confirm it now matches. If matched=0 was purely the path bug (data was fine), say so; if a real score divergence remains after the path fix, report it, do not override.

## Verify before returning
- Re-run `python 03_operations/page_generator/conformance.py --all` and report granola + hard_cheeses now conform (or the precise residual).
- Confirm the repair is SCORE-NEUTRAL: the served/published scores are unchanged vs origin (you restored reproducibility, you did not move a published number). Show the before/after per touched product.
- OFF=0.

End with the machine-readable return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED.
