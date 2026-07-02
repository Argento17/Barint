# P275 / TASK-418 trace regen + C0 gate matrix (route: C1 Data)

## Goal
Close provenance + run the deterministic C0 gate matrix so the refreshed bundle is deploy-ready. The frontend
JSON scores were re-scored (HC = cleaned corpus; cheese/cereals = current-engine TASK-405 drift), so the
stored `bsip2_trace.json` files are stale for the MOVED products → `validate_comparison_page.py` (score==trace)
would mismatch. Regenerate traces for the movers, then run the full gate matrix.

## Isolation
Worktree **C:\bari_p270** ONLY. NO git commands. Read-only on the MAIN tree. Deploy nothing.

## Do
1. **Regenerate traces for the moved products** from the CURRENT on-disk corpus (HC corpus is already cleaned +
   stamped `_task418_hc_clean` by P273; cheese/cereals corpus unchanged) using each category's canonical
   invocation:
   - hard_cheeses: TASK-429 canonical (corpus `bsip1_task412`, the 7-flag vector, EV-090 shelf-stats, loader
     accepting bsip1_enriched). Write per-product `bsip2_trace.json` for the 8 movers (min) into a NEW run dir
     `02_products/hard_cheeses/bsip2_outputs/run_hc_task418_clean/products/<id>/` (do not overwrite
     run_hc_task412_rt4_fix). Ideally emit all 31 for a self-consistent source_run.
   - cheese, cereals: their config invocation on the current corpus; emit traces for their moved barcodes into
     a parallel `run_*_task418` dir.
   Each regenerated trace's `final_score_estimate`/`grade_estimate` MUST equal the patched frontend JSON value
   (±0.1). If any mover's fresh trace ≠ patched JSON, STOP and report the barcode.
2. **Run the C0 gate matrix** (worktree paths) and capture verbatim results:
   - `validate_comparison_page.py --json <frontend> --traces <run_dir/products>` for each of the 3 pages.
   - `run_gates.py` for each of the 3 pages.
   - `rank_check.py` (or `validate_comparison_page` gate 6) for each of the 3 pages.
3. **Label every failure** as **NEW (introduced by this refresh)** vs **PRE-EXISTING (fails on live master too)**
   — for each failure, run the same gate against the ORIGINAL master JSON to determine which. The Adversarial QA
   gate already noted cheese/cereals G1 (brand/limitingFactors) + cheese "חלבון נמוך" are PRE-EXISTING; confirm.

## Return (`C:\bari_p270\tasks\returns\P275_return.md` + final message)
- Trace regen: # traces written per category, and a table proving fresh-trace score == JSON score for every mover.
- **Gate matrix:** rows = {hard_cheeses, cheese, cereals}, cols = {validate_comparison_page pass/fail + which of
  the 7 checks, run_gates overall + failing G#, rank_check}. Each failure labeled NEW vs PRE-EXISTING with the
  master-comparison evidence.
- Deploy-readiness verdict: is the refresh itself gate-clean (no NEW failures)? List any NEW failure as a blocker.
- Return contract (`01_framework/operations/return_contract_v1.md`): artifacts w/ sha256, counts w/ named
  denominators, distribution marker. Propose RETURNED. OFF BANNED; invent nothing.
