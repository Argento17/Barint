---
id: TASK-468
title: Milk score refresh: align published milk_frontend_v1 to current engine (2 known movers, owner-sanctioned tripwire-1)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-02
closed_at: 2026-07-03
close_reason: >
  Two-part resolution. (1) Score-align debt: PR #50 (merged 8dac7c2f) refreshed milk's audit traces +
  _meta to match the 2 moves already live from the de-anchor sweep; production-verified; no new score
  shipped. (2) Systematic-regen rework (owner ask 2026-07-03): P478 ran the full spine and PROVED the
  pipeline reproduces all 18 milk scores/grades exactly (G-repro PASS — MILK_CANONICAL_FLAGS canonical)
  with copy carried verbatim (G-freeze PASS), BUT the generator CANNOT reproduce the hand-curated gold-
  standard page — its output DEGRADES it (confidence verified→partial, label full-data→under-review,
  limitingFactors/positiveSignals emptied, servingNote per-100ml→per-100g). Orchestrator-verified.
  Resolution: milk stays hand-curated; no regen ships; #50 is the correct end state. Finding preserved
  (tasks/returns/P478_contract.md); generator-can't-match-gold-standard → engine parity backlog. The 2
  live milk COPY defects (legacy milk-comparison.json 48/D; milk-product-insights.ts almonds) stay routed
  to the owner copy lane.
depends_on: []
blocks: []
category_id: milk
summary: >
  Owner GO 2026-07-02 (after TASK-429 classified milk drift as post-publication engine/data fixes, not invocation gap). Known drift at master HEAD flags-off: bsip1_7290110324926 +0.2, 7290110325619 +4.1 (C10 diagnostic). Step-A reproduction gate mandatory (canonical MILK_CANONICAL_FLAGS invocation must reproduce published 16/18 exact + exactly these 2 drifters, else BLOCKED). Rebuild-from-live candidate (swap score/grade/rank only), root-cause the +4.1 with named mechanism, copy-impact audit REPORT-ONLY (owner description freeze), G1-G8 vs origin/master baseline, owner merges (tripwire-2). work_type: go_live - close needs red_team_cleared.
---

## REWORK OUTCOME (2026-07-03): pipeline reproduces SCORES but CANNOT reproduce the gold-standard page — BLOCKED (correct result)
P478 (Grok) ran the full spine (rescore_all→copy_stage→run_gates) and self-reported BLOCKED; orchestrator
verified: **G-repro PASS 18/18** (the pipeline reproduces every live milk score+grade exactly — proves
MILK_CANONICAL_FLAGS is the canonical invocation), **G-freeze PASS** (copy carried verbatim, author_set
empty). BUT **G-metaonly FAIL**: the generator's product payload diverges from the live page on 18/18
products in CONSUMER-VISIBLE ways, all DEGRADATIONS — confidence verified→partial, confidence_label
"נתונים מלאים"→"נתונים בבדיקה" (full data → under review), limitingFactors + positiveSignals emptied
([]), servingNote "ל-100 מ״ל"→"ל-100 גרם" (per-100ml → per-100g, WRONG for a liquid). The live
milk_frontend_v1 is a HAND-CURATED gold-standard artifact the current generator cannot faithfully emit;
a "pure pipeline regen" would make the page worse. **Resolution: milk stays hand-curated (correct); the
pipeline confirms its scores are canonical; #50's verification-debt fix (merged 8dac7c2f) is the right
end state. No pipeline regen ships.** Finding preserved: tasks/returns/P478_contract.md. Worktree reset;
recommend closing TASK-468 (both the score-align debt #50 AND this rework question are resolved).

## REWORK (owner ruling 2026-07-03): systematic, not hand-patched
PR #50 (merged 8dac7c2f) refreshed milk by hand-editing `_meta` into the JSON. Owner rejected the
METHOD — milk must be a reproducible output of the uniform pipeline (`rescore_all → copy_stage →
run_gates`), not an artisanal spot-patch. **P478 → C1-GROK** (branch `refresh/task468-milk-systematic`
off 8dac7c2f): regenerate `milk_frontend_v1.json` + traces + `_meta` through the spine; four proof
gates — G-repro (pipeline reproduces the 18 live scores/grades exactly, else BLOCKED), G-freeze
(`author_set.json` empty = zero copy authored, gold-standard copy carried verbatim), G-metaonly
(production delta vs live = `_meta`-only), G-trace (score==trace 18/18). Net production change ≈ nil;
the deliverable is the PROOF milk regenerates from config, replacing the hand-typed `_meta`.
The 2 CRITICAL live copy defects (legacy milk-comparison.json 48/D; milk-product-insights.ts almonds)
stay routed to the owner's copy lane — untouched here (freeze).

# TASK-468 — Milk score refresh: align published milk_frontend_v1 to current engine (2 known movers, owner-sanctioned tripwire-1)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
