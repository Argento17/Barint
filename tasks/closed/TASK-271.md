---
id: TASK-271
title: Restore frozen milk 85/A: engine drift since f075d9e (W4 default-on + others) broke no-regression net
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
depends_on: []
blocks: []
category_id: null
summary: >
  Committed engine cannot reproduce frozen milk run_005_headpin (top 85/A -> 64-65). VERIFIED multi-factor: BARI_GLASSBOX_W4 default-on (TASK-181S 2026-06-05, EV-042 D3 de-moralization pulls NOVA-1 processing 95->neutral) is ONE confirmed factor but W4=off+RECAL_P0=on only restores 7/20, top trio still broken -> more code drift since freeze commit f075d9e. NOT caused by P56 (stash-test clean). Live milk page safe (frozen frontend data); the BROKEN no-regression net blocks proving any scoring change is milk-safe. W4 was shipped deliberately -> fix is entangled, owner-gated (frozen invariant). Next: f075d9e->HEAD audit of score_engine.py milk-affecting changes, classify regression-vs-intended, propose minimal isolation fix.
---

# TASK-271 — Restore frozen milk 85/A: engine drift since f075d9e (W4 default-on + others) broke no-regression net

<!-- opened with new_task.py; fill in context / scope / the deliverable -->


## CLOSE (orchestrator, 2026-06-13)
close_reason: Frozen invariant RESTORED + verified — milk top trio (whole 3.4%/natural 4%/goat) = 85/A ALL HELD; invariants 6/6 PASS; D7 (Product) GRANTED-with-conditions, all 3 met: (C1) exact 85/A not approximate, (C2) marginal diff proves P60 moves ONLY the 3 trio products (17 others byte-identical), (C3) cream excluded from whitelist. Fix = dairy-single-token NOVA-1 exemption in nova_proxy.py (EV pending), W4 untouched. **NORMALIZED per owner 2026-06-13 ('don't put so much effort on milk, big sweep soon'):** the 17 plant-alternative drinks still carry pre-existing W4/text_fallback drift vs their published scores — NOT the named frozen invariant, NOT caused by P60 — deferred to the big milk sweep. No deploy.
