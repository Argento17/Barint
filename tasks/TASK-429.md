---
id: TASK-429
title: Pin the ONE canonical scoring invocation that byte-reproduces published scores (Phase-0 baseline)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
closed_at: 2026-07-01
close_reason: >
  All 5 DoD items verified against artifacts by the orchestrator. Canonical HC invocation pinned and PROVEN
  to byte-reproduce hard_cheeses_frontend_v4 (31/31, max abs drift 0.000, 0 grade moves, 0 missing) by two
  independent harnesses (provenance/hard_cheeses_reproduce_harness.py canonical + config-driven _reproduce_diag
  with widened loader). Forks resolved with evidence: corpus=bsip1_task412 (bsip1_outputs mis-scored 4/12 =
  the A/85-vs-B/67 contradiction); shelf-stats=frozen EV-090 constants. Config updated score-neutral. Generalize:
  cheese/cereals/milk residual drift is owner-gated TASK-418 data refresh, not an invocation gap. Landed on
  master at 0a303e34. Open follow-up (flagged, out of Phase-0 scope): widen the production generate_page corpus
  loader to accept file_type='bsip1_enriched' so the standard path reproduces HC without a bespoke harness.
depends_on: []
blocks: [TASK-418, TASK-419]
category_id: null
work_type: build
summary: >
  The de-chain program's Phase-0 prerequisite (a byte-reproducible baseline) is unmet not because the engine
  is non-deterministic (it is deterministic — same record 3x = identical score) but because there is NO
  documented canonical scoring INVOCATION. Different valid-looking setups (flag source, shelf-relative stats
  source, corpus_dirs = bsip1_outputs vs bsip1_task412) reproduce DIFFERENT published-affecting scores for the
  same record (orchestrator invocation gave hard_cheeses 7290019635192 -> B/67; agent invocation -> A/85 =
  published). Until ONE invocation is pinned + documented + proven to byte-reproduce the CURRENT published
  frontend scores, no re-score is verifiable and no refresh / de-chain shadow can safely deploy.
---

# TASK-429 — Pin the canonical scoring invocation (Phase-0 baseline)

## Why this exists
Uncovered 2026-07-01 while trying to execute the owner-approved TASK-418 clean+refresh. Repeated agent runs
produced contradictory scores for the same record (A/85 vs B/67) and the measurement's predicted movers did
not reproduce. Root cause is NOT engine non-determinism (verified deterministic) — it is the absence of a
single, documented "how to score category X so it reproduces what's published" recipe. See TASK-418 update
2026-07-01 for the full trail.

## Definition of Done
1. **Canonical invocation documented** for hard_cheeses first (then generalize): the exact
   (a) flag set + source, (b) shelf-relative stats + source, (c) corpus_dirs / record source, (d) engine
   reload/order — that, run through the standard scoring path, **byte-reproduces every published
   `hard_cheeses_frontend_v4.json` score within ±0.1, 0 grade moves, 0 missing_from_corpus.**
2. **Resolve the two open forks** with evidence:
   - corpus: does the published v4 derive from `bsip1_outputs` or `bsip1_task412`? (config says outputs; a
     prior agent claimed task412. Prove which reproduces.)
   - shelf-stats: where do the authoritative HC shelf-relative median/scale come from, and are they frozen
     constants or recomputed? Different stats = different scores.
3. **Config completeness:** update `03_operations/page_generator/configs/hard_cheeses.json` so `scoring.flags`
   + `corpus_dirs` match the canonical invocation (the config currently omits `BARI_HC_DAIRY_SATFAT_V1` /
   `BARI_DAIRY_SAT_FAT_INFER` that v4 `_meta.flag_vector` declares ON; corpus_dirs may be stale). Score-neutral:
   the goal is to REPRODUCE published, not change it.
4. **Prove it with `_reproduce_diag.py`** (or the canonical harness): hard_cheeses row = drift 0 / grade_moves 0.
5. **Generalize check:** confirm the same documented invocation recipe reproduces the OTHER live categories that
   currently drift (cheese, cereals) OR explain per-category why (their drift was already root-caused to
   post-publication data/engine fixes — TASK-418 — which is a separate, owner-gated refresh, not an invocation gap).

## Hard constraints
- **Isolated git worktree ONLY.** Do NOT run in the main tree. Multiple overlapping background agents writing
  the main tree corrupted state on 2026-07-01 ([[lane_dispatch_wipes_shared_tree]] + detached-pipeline hazard).
  One worker, one worktree, synchronous, no detached background pipelines.
- **Score-neutral:** reproduce published scores; do NOT change any published score. If a published score
  provably cannot be reproduced by ANY clean invocation (i.e. it rests on since-fixed polluted data — the
  cheese/cereals case), that is a TASK-418 owner-gated refresh, NOT this task — flag it, don't "fix" it here.
- OFF-ban absolute.

## Unblocks
- **TASK-418** (clean+refresh hard_cheeses/juices): once the canonical baseline exists, the clean's moves are
  verifiable against it and can deploy with owner sign-off. Owner already approved the targeted clean
  (2026-07-01); it stalled only on verification.
- **TASK-419** (de-chain Stage 2): the byte-identical-OFF shadow requires this reproducible baseline.

## Notes / leads
- Start from `03_operations/page_generator/provenance/_reproduce_diag.py` (has the scoring harness:
  apply_flags / make_scorer / resolve_records) and each frontend's `_meta.flag_vector`.
- Agent a4f223f6 (2026-07-01) produced a plausible-correct HC run (2 grade movers 4122270/7290110320850 C->B,
  HC gates PASS) but UNVERIFIED against a canonical baseline — treat as a lead, not truth.
- All 16 live configs carry `flags: None` at top level; real flags live in `scoring.flags` and/or the frontend
  `_meta`. The mismatch between config flags and `_meta.flag_vector` is the likely core of the invocation gap.

## RESOLUTION (2026-07-01, worktree `task429/canonical-repro` off f530bc87)
**PROVEN — byte-reproduces `hard_cheeses_frontend_v4` 31/31, max abs drift 0.000, 0 grade moves, 0 missing.**
Full write-up: `03_operations/page_generator/provenance/hard_cheeses_canonical_invocation_v1.md`.

- **DoD #1 canonical invocation documented** — flags (7-vector), shelf-stats (frozen constants EV-090,
  median 18.0/scale 1.40), corpus (`bsip1_task412`), engine fix (constants.py:702=67.0), loader
  (`file_type ∈ {product, bsip1_enriched}`), reload order. Proven by `_t429_reproduce.py`.
- **DoD #2 forks resolved with evidence** — (a) corpus = `bsip1_task412` (covers 31/31; `bsip1_outputs`
  covers 12/31 and mis-scores 4 of the 12 — THIS was the A/85-vs-B/67 contradiction). (b) shelf-stats =
  frozen constants, not recomputed.
- **DoD #3 config completeness** — `configs/hard_cheeses.json`: `corpus_dirs → bsip1_task412`; `scoring.flags`
  set to the exact canonical vector (added `BARI_DAIRY_SAT_FAT_INFER` + `BARI_HC_DAIRY_SATFAT_V1`, dropped
  inert off-flags). Provenance comments added. Score-neutral.
- **DoD #4 proven via `_reproduce_diag`** — config-driven diag with loader widened to accept `bsip1_enriched`:
  hard_cheeses row = repro=31 drift=0 grade_moves=0 nocorpus=0 maxd=0.0.
- **DoD #5 generalize** — recipe reproduces categories with no post-publication change (choc bars/tablets/
  snacks/HC exact). cheese (22 drifters, all `_task405_clean`, +drift) and cereals/granola/milk (2 SKUs each,
  small +drift) are since-applied data/engine cleans = owner-gated **TASK-418** refresh, NOT an invocation
  gap. Flagged, not fixed here (score-neutral honored).

**Open item for the standard path:** the generic corpus loader (`_reproduce_diag.py` and, if it shares the
filter, `generate_page`) drops `file_type='bsip1_enriched'` records. HC's 79 shufersal records are enriched,
so the standard path needs the one-line filter widening to reproduce HC without a bespoke harness. Diagnosed;
production loader NOT modified in this task (out of Phase-0 scope — flag for TASK-418/419).

Proposed status: ready to CLOSE once the config change + provenance doc land on the working line (unblocks
TASK-418 verification and TASK-419 shadow baseline).
