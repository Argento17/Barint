---
id: TASK-519
title: Investigate bread engine score drift: 17/31 products don't reproduce on fresh re-score
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-05
closed_at: 2026-07-10
close_reason: >
  Diagnosis complete + orchestrator-verified (2026-07-10 unattended 3AM). ROOT CAUSE
  CONFIRMED = NOT a live bug: the 17/31 bread re-score mismatches are an artifact of
  this working branch (task506) lagging origin/master, NOT engine non-determinism and
  NOT a defect on the LIVE tree. Independently verified two load-bearing facts:
  (1) `git rev-list --left-right --count origin/master...task506` = 232 behind / 51
  ahead (worse than the diagnosis's cited 39 — branch has fallen further behind since);
  (2) `git merge-base --is-ancestor de8c7801 HEAD` = MISSING — the co-signed TASK-476
  input_loader.get_ingredients() fix (commit de8c7801, shipped to origin/master
  2026-07-03) is absent here, exactly the mechanism the diagnosis names. origin/master
  is the LIVE deploy target and is self-consistent by deploy discipline; users are
  unaffected. DoD (root-cause the drift) satisfied. The diagnosis's flagged REAL OPEN
  RISK — a deliberate reconciliation of this branch's dirty engine drafts
  (input_loader.py / router_v2.py) that carry BOTH a stale incomplete fix AND
  in-progress local-only TASK-515 yogurt anchors — is NOT closed here: it touches
  score-affecting engine files with mixed live work (tripwire-1-adjacent) and per the
  diagnosis's own recommendation needs a supervised deliberate merge, not an automated
  fix. Parked for owner as the branch-reconciliation item (see digest 2026-07-10).
depends_on: []
blocks: []
category_id: null
diagnosis: >
  ROOT CAUSE FOUND, NOT A LIVE BUG: local branch task506 is 39 commits behind
  origin/master, missing an already-shipped, co-signed fix (TASK-476, commit
  de8c7801, 2026-07-03) to input_loader.py's get_ingredients(). origin/master
  itself is fully self-consistent (verified: committed bread JSON matches a fresh
  re-score of origin/master's own engine). The apparent "drift" only shows up
  because this branch's committed bread baseline predates de8c7801 while its
  *working tree* separately carries a stale, INCOMPLETE, uncommitted draft of the
  same fix (missing {}-bracket handling that origin/master's shipped version has).
  Confirmed via a separate check that this incomplete draft caused ZERO impact on
  this session's crackers/ricecakes work (TASK-516/517/EV-104) -- the one product
  with {} in its ingredient text resolves through a different code tier that never
  reaches the incomplete function.
  REAL OPEN RISK (not yet fixed): router_v2.py's dirty working-tree draft has ALSO
  diverged from origin/master independently -- missing TASK-455's "chocolate"
  category + Rule 4 shelf de-anchor (already shipped on origin/master), while
  carrying LOCAL-ONLY in-progress TASK-515 yogurt anchors that origin/master does
  NOT have. Any careless reconciliation (e.g. blind checkout/reset of these files)
  would either regress a shipped fix or silently discard TASK-515's in-progress
  work. This needs a deliberate merge, not an automated fix -- flagging to the
  user/owner for a decision on sequencing rather than acting unilaterally on files
  with live mixed-in work.
summary: >
  Discovered as a side-effect during EV-104 pilot (crackers protein-scale calibration): re-scoring the committed bread corpus (run_bread_conform_002, 31 products) through the CURRENT engine with NO table/code changes produces 17/31 score mismatches vs the committed baseline traces. This is engine/environment drift unrelated to any deliberate change -- bread is a live published category. Needs root-cause: engine version drift, non-deterministic scoring path, or a stale baseline. Flagged by Data Agent in EV-104's pilot run_record.json, not investigated further (out of that task's scope).
---

# TASK-519 — Investigate bread engine score drift: 17/31 products don't reproduce on fresh re-score

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
