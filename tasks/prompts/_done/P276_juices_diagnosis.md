# P276 / TASK-430 juices baseline diagnosis (route: C1 Data)

## Goal (TASK-429-style, for juices)
Determine why `juices_frontend_v3.json` does NOT cleanly reproduce, and classify every drifter — so the owner
can decide whether juices joins the TASK-418 refresh or is held. Score-neutral ANALYSIS only; deploy nothing.

## Environment / isolation
- Isolated worktree **C:\bari_p276** ONLY (already created off master 7733065a). No git ops. Read-only on published.
- Engine: `03_operations/bsip2/proto_v0/src`. Pattern to follow: `03_operations/page_generator/provenance/hard_cheeses_reproduce_harness.py` + `hard_cheeses_canonical_invocation_v1.md` (TASK-429) and the diag `_reproduce_diag.py`.

## Known facts (from P268, orchestrator-verified)
- Baseline reproduces only 11/17 under the config invocation. 6 drifters, ALL DOWNWARD (engine < published):
  7290019056720 41.8→39.8, 7290006822192 40.5→39.9, 7290000136523 40.1→38.1, `7290019056737` 36.0→30.3 (grade
  D→E), 7290019056355 34.2→33.4, 7290013153418 29.1→28.5.
- `7290019056737` is BASELINE-NOT-REPRODUCIBLE (36.0 matches neither pre- nor post-D4 engine output).
- Juices drifters do NOT carry `_task405_clean` (unlike cheese/cereals) — so this is NOT the TASK-405 story.
- Config: corpus `bsip1_outputs`, flags incl `BARI_D4_SCORE_V1=on`, shelf_rel sugars_g med 9.5 scale 2.82.
- `juices_frontend_v3.json` `_meta` has NO flag_vector/source_run (only `run_id`, `provenance`). Schema = v3 (differs
  from other categories; validate_comparison_page / run_gates G1 failed on it before).

## Do
1. **Find the canonical invocation** that byte-reproduces the published v3 juices scores: dig the `_meta.run_id` +
   `provenance` to locate the source run and ITS flags/shelf-stats/corpus; test flag-vector variants (esp.
   `BARI_D4_SCORE_V1` on/off and the shelf-rel source) + corpus source (bsip1_outputs vs any bsip1_task* dir) —
   exactly like TASK-429 resolved HC's corpus fork. Report the invocation that reproduces the most, and whether
   ANY invocation reproduces all 17.
2. **Classify each of the 6 drifters** with evidence: `invocation-gap` (a flag/corpus/shelf mismatch — fixable
   like TASK-429, score-neutral), `data-refresh` (published rests on since-changed data/engine — owner-gated like
   cheese/cereals), or `genuinely-defective` (published score not reproducible by ANY clean invocation — e.g.
   `7290019056737`). For each, state which and the mechanism.
3. **Resolve `7290019056737`** specifically: what produced the published 36.0? Is it a stale flag vector, a
   pre-D4 score, or an artifact? Trace it.

## Return (`C:\bari_p276\tasks\returns\P276_return.md` + final message)
- The canonical (or best) juices invocation + how many of 17 it reproduces (drift 0).
- Per-drifter classification table (barcode, pub, engine, delta, class, mechanism).
- Verdict on `7290019056737`.
- Recommendation: can juices be refreshed clean-and-verifiable (like HC), or is it held (which products, why)?
- Return contract (`01_framework/operations/return_contract_v1.md`): artifacts w/ sha256, counts w/ named
  denominators, distribution marker. OFF BANNED. Propose RETURNED; do not close.
