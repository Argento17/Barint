---
id: TASK-519
title: Investigate bread engine score drift: 17/31 products don't reproduce on fresh re-score
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-07-05
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
