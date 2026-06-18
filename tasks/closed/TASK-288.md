---
id: TASK-288
title: Commit blessed engine diff (EV-086/097/099, 5 files) after no-regression proof — release platform P-BASE prereq
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  Engine committed at f1d1275e (5 files: score_engine/signal_extractor/nova_proxy/router_v2/
  evaluation_scope). All EV-086/096/097/099 D6/D7-co-signed. No-regression proven by P-ENG:
  milk frozen 20/20 byte-id (A:3/B:1/C:5/D:10/E:1, max 85/A) + engine_invariants 342/342 PASS.
  Brined tripwire RESOLVED by owner (2026-06-16): "smallest patch, indifferent" — brined NOT
  re-run/re-frozen (deferred shadow corpus; live run_brined_005 page UNCHANGED = no consumer-facing
  move, no published-score change). Closes the uncommitted-engine integrity gap; HEAD now reproduces
  the live go-live pages. Shadow APPROVED baseline promoted on this engine (89555a47).
summary: >
  EV-086/097/099 engine work is D6/D7-blessed (TASK-280/284) but uncommitted. Prove brined 48/48 byte-id + engine_invariants 342 PASS + milk frozen 20/20 byte-id, THEN commit the 5 modified engine files as one commit. No new methodology. Reversible.
---

# TASK-288 — Commit blessed engine diff (EV-086/097/099, 5 files) after no-regression proof — release platform P-BASE prereq

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
