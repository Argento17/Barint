---
id: TASK-498
title: Corpus barcode-glob stray-collision root cause (TASK-409 sub-item) — wrong-category records bleed into a corpus
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "MERGED LIVE PR #77 (squash). Root cause: maadanim scraper's legit 'מעדן פרוטאין' query surfaces protein bars (Shufersal loose free-text search, no acquisition-time category-form check). Fix: G13 cross-category guard in shared bsip0_gate.py (query-ownership + head-noun registries, WARN default). 37/37 tests pass; verified diff = 2 tooling files, 0 corpus/BSIP/frontend touched; precision 4/200 flagged 0 false-pos (3/5 TASK-477 + 1 bonus). Orchestrator-merged (internal). HONEST RESIDUAL (logged follow-up, not a blocker): 2/5 TASK-477 barcodes (brand נייטשר פרוטאין) not caught — needs brand→category registry that doesn't exist; + 5 candidate wafer-cookie barcodes flagged for a precision-tested follow-up. Feeds TASK-409 corpus-hygiene program."
depends_on: []
blocks: []
category_id: null
summary: >
  The corpus-building barcode search can pull records from the WRONG category into a corpus — e.g. the
  run_maadanim_001 (deli/appetizers) run held 5 protein-bar barcodes as DUPLICATE records because of an
  overlapping "protein" search query (found in TASK-477). It did NOT taint live scores (scores never read
  that BSIP1 dir; 0 numeric divergence), but it is a contamination risk for FUTURE corpus builds. Root-cause
  the barcode-glob / search that cross-picks, and add a category-aware guard so wrong-category records can't
  bleed in. FORWARD-LOOKING tooling fix only — must NOT alter any existing committed corpus or live score.
---

# TASK-498 — corpus stray-collision root cause (from TASK-409 / TASK-477)

## Investigation-first
1. Reproduce/locate the collision: run_maadanim_001 holds 5 protein-bar barcodes as duplicate records via an
   overlapping search query (documented in TASK-477 / closed). Find the corpus-building tool + the barcode-
   glob / search-query logic that pulls records into a category corpus.
2. Root-cause WHY wrong-category records get picked (query overlap? barcode-only match with no category
   filter? shared scrape pool?). Cite the exact code path.

## Fix (forward-looking tooling only)
- Add a category-aware guard so a corpus build only ingests records whose category matches the target
  (or explicitly flags/excludes cross-category barcodes), preventing future bleed. Add a test/assertion if a
  harness exists.
- HARD CONSTRAINT: do NOT alter any EXISTING committed corpus, BSIP run, or live frontend score. This is a
  fix to the TOOL for future builds. If the fix would change what an existing corpus contains, STOP and
  return as a finding (do not retroactively rewrite corpora).

## Guards
- Base off origin/master (not local HEAD — F1 divergence). Isolated worktree. OFF ban irrelevant.
- Internal tooling, non-consumer, no score change → orchestrator may merge after verify. Prove no live
  corpus/score touched (git diff scope = tooling only).

## Return: 5-part (root cause at file:line, the guard added, proof no existing corpus/score changed) +
Return Contract JSON. Propose RETURNED. Do not write CLOSED.
