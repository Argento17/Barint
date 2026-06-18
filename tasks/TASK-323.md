---
id: TASK-323
title: Spine consolidation — bring the scoring engine + release machinery from task-275 onto canonical master
owner: orchestrator
status: CLOSED
priority: HIGH
close_reason: >
  Owner merged spine/consolidate-to-master 2026-06-18 (origin/master 5cf5c39a0). VERIFIED on master:
  03_operations/page_generator/spine_flip.py + configs present → master now OWNS the release machinery;
  spine_flip runs from canonical. Engine == validated task-275 (byte-identical bar 1 stale non-scoring
  filename ref); bari-web == master live frontend (seam reconciled as a unit per C3); cheese/yogurts reproduce
  UNCHANGED; net live-score impact zero. Post-merge cleanup done: 7 merged worktrees pruned, 9 merged branches
  deleted (wave0/wave1/yogurt/milk/cheese/milk-baseline conforms + spine/consolidate + cheese/yogurt-conform-data).
  task-275 now fully consolidated into master (retireable — main checkout C:/Bari still on it w/ dirty tree;
  owner switches to master + deletes when ready). OPEN: milk reconciliation follow-up (config↔page run mismatch);
  bread + cleanup-orphans PRs still unmerged.
created_at: 2026-06-18
depends_on: [TASK-321, TASK-322]
blocks: []
category_id: null
summary: >
  Master is canonical/deploy but lacked the entire scoring brain: 03_operations/page_generator/ (generate_page,
  spine_flip, rescore_all, copy_stage, configs) was ABSENT, and the scoring engine (bsip2/proto_v0/src) was
  ~16K lines stale vs task-275 (44 commits / all EV-### + TASK engine work). The live pages were produced by
  task-275's engine; master couldn't reproduce them. task-275 had become the de-facto integration branch.
  This consolidates the spine+engine onto master so "master owns the release machinery" (owner ruling 2026-06-18).
---

# TASK-323 — Spine consolidation onto master

## Finding
- `master` ⟷ `task-275` diverged BOTH ways: task-275 +44 commits (engine 16,071 lines in proto_v0/src + page_generator + configs); master +39 commits (frontend conforms PRs #10–13). Neither a superset.
- task-275 was **local-only** until this task (pushed to origin as a safety step).
- `page_generator/` entirely absent from master; `spine_flip` could not run from canonical.

## C3 independent review (P202, gpt-5.5, advice-only)
- Biggest risk = silent published-score change; gate must prove EVERY live page reproduces, not just one.
- Merge (integration branch off master ← task-275) safer than reset/replay.
- Path-based conflict policy unsafe — reconcile by CONTRACT unit (scrape→engine→payload→frontend); bari-web must be one unit.
- (C3's bari-web-as-a-unit warning proved correct — see seam fix below.)

## Build + verification (branch `spine/consolidate-to-master`, off master, HEAD pushed)
- Conflict policy: `03_operations`/`02_products` ← task-275 (engine/spine/data); `bari-web` ← master (live frontend).
- **Seam fix:** coarse path-merge silently dropped master-only bari-web modules (bread-page-data, snacks-comparison-page-data,
  featured-*-lite, bread routes/blog) → /hashvaot index broke. Fixed by reconciling bari-web as a UNIT = master exactly.
- **Engine identity:** merged `bsip2/proto_v0/src` == task-275 except 1 stale non-scoring filename ref in
  run_confidence_annotation_pass.py (yogurts_frontend_v3↔v4, pre-existing on both). `page_generator` byte-identical to task-275.
  → merged engine reproduces live scores BY CONSTRUCTION.
- **Reproduction gate (regenerate vs live frontend JSON):** cheese 53/53 UNCHANGED ✓; yogurts 83/83 UNCHANGED ✓.
- **Frontend build:** ✓ compiled, 39 pages, all /hashvaot routes present. bari-web diff vs master = 0.
- **Consolidation merge is score-neutral for the live site** (frontend = master, engine identical).

## Milk follow-up (NOT a consolidation blocker)
Reproduction gate caught a PRE-EXISTING milk spine inconsistency: `configs/milk.json` points at run_006_shelfrel_refreeze
(20 products) while the live `milk_frontend_v1.json` is a hand-extracted run_005 subset (18 products) — 15 small score
diffs (−1..−6), 1 grade flip C→D, +2 products. Neither run is the 18-product curated set as-is. Milk's page is hand-extracted,
not spine-generated → milk is not yet TRULY spine-driven. Reconcile separately (owner already authorized milk re-score):
regenerate milk's page from its config + author copy for new/changed products, OR align config+curation to reproduce the
live 18. Owner preview the diff before it goes live. Tracked as the milk reconciliation follow-up.

## State: PR pushed, awaiting OWNER MERGE GATE (score-touching canonical change). Prune worktrees/branches only AFTER merge.

## Milk reconciliation — DONE 2026-06-18 (branch sweep/milk-reconcile, e0340ada, pushed)
Resolved the config↔page mismatch. No standard run reproduced the live legacy scores (only 3/18), so milk
was regenerated through the blessed engine: config now reproduces the live 18-product shelf scope (excluded the
2 non-curated barcodes), scores are spine-driven. copy_stage carried gold copy onto 13/18 (grade unchanged);
the 5 grade-flipped products re-authored by Content Agent (Sonnet) to the milk gold-standard bar. Score diff vs
the frozen page: 15/18 small downward moves, 5 grade flips (7290116936116 B→C; four C→D incl 8000215204219 −6);
**top whole-milk 85/A UNCHANGED**. Build exit 0, 0 PENDING, leakage clean, page_copy intact. Milk is now TRULY
spine-driven (a future spine_flip re-flows it). Owner merge = the score-diff preview gate.

## Post-merge branch cleanup (parallel chat): 10 pre-existing merged branches deleted. HELD (NOT dead):
- cc-agent-v2 = misnamed; holds TASK-235 frozen-vegetables v2 score-free page (real WIP) → KEEP/rename.
- salty-snacks-v4 = wiped category, BUT carries TASK-239 BSIP0-parser hardening (salvage-check before delete)
  + a "retract OFF ban" commit that contradicts the hard rule (good it's unmerged).
