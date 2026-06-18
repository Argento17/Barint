---
id: TASK-329
title: additive_burden index: reconcile EV-002/EV-003 double-count (display-only)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
depends_on: []
blocks: []
category_id: null
close_reason: >
  P209 (C1-CURSOR) verified by orchestrator against the artifact. Ran the module --single on the live
  cakes 2472148 trace: index 13.0→9.0, deduped_against_ev002=2 (E466/CMC + E407/carrageenan both excluded
  from EV-003; EV-002 ×3 kept authoritative). Overlap set independently confirmed by P210 (C2) = {E466,E407,E433}.
  Scope verified: git diff --stat = method_additive_burden.py ONLY (+50/-3); score_engine/constants/configs
  diff EMPTY (representation-only, no scoring path). OFF-ban null behavior preserved. Return contract present.
  Note (non-blocking): --calibrate denominator 821 vs P176's 898 is pre-existing calibration-scope state
  (cakes barcode present in 3 run dirs), not caused by the dedupe.
summary: >
  Fix method_additive_burden.py double-count: CMC(E466)/carrageenan(E407) score under BOTH EV-002 at-risk (x3) AND EV-003 high-risk emulsifier (x2). Dedupe so an additive counted in EV-002 is excluded from EV-003. Representation-only module; no scoring path touched.
---

# TASK-329 — additive_burden index: reconcile EV-002/EV-003 double-count (display-only)

CLOSED 2026-06-18 — see close_reason. Display-only reconcile; no scoring path, no spine, no deploy.
