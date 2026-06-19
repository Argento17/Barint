---
id: TASK-343
title: Phase 1 closeout: wire grammar gate into Content Agent chain + build auto-fix loop
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified by re-running both module self-tests + grep. (1) Auto-fix:
  `python -m integrations.clients.hebrew_grammar_autofix` exit 0 — deterministic fix
  הצהוב→הצהובה, re-gate is_clean=True, PASS. (2) Gate regression: `python -m
  integrations.clients.hebrew_grammar_gate` exit 0, 5/5 pairs still correct (no behavior
  change). (3) Wiring present + consistent in all 3 docs (content-agent.md Pre-Return +
  External Data Access [v1.3], file5 §3 gate order [now 6 steps: …Form/Nakdan→Grammar→Voice-
  Match], file7 Relationship/Integration). Auto-fix is high-confidence-only (medium→human),
  LLM hook documented but NOT wired (0 external calls). Only my files changed:
  content-agent.md, file5, file7, hebrew_grammar_autofix.py — no scores/engine (additive_burden
  index changes are pre-existing parallel-chat work, not this task). Committed with Phase-1 closeout.
---

# TASK-343 — Phase 1 closeout: wire grammar gate + auto-fix loop

CLOSED. Phase 1 of "Bari in Tom's Voice" is now COMPLETE (grammar gate built + wired + auto-fix;
idiom reviewer deferred). Next: Phase 2.
