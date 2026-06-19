---
id: TASK-341
title: PROJECT Bari-in-Tom's-Voice — PHASE 1: Hebrew-correctness layer (grammar gate + idiom check + context lock + auto-fix)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  CORE delivered + orchestrator-verified + committed (master 4cf418f2f). Independently ran
  `python -m integrations.clients.hebrew_grammar_gate` → exit 0, 5/5: passes clean masc+masc,
  fem+fem, and real Bari construct-state copy; FLAGS real gender mismatches (הגבינה הצהוב high,
  היוגורט הטעימה medium). Built on dicta-il/dictabert-morph (MIT, safe to embed); HspellPy
  (AGPL) NOT imported — verified. Reader-context lock built. No scores/engine/content_voice
  touched (only 2 new files under integrations/clients/). PROBE outcomes: (a) idiom reviewer —
  Dicta-LM 3.0 not yet public, 2.0 too slow as a gate (2-8min/string), Claude isn't an
  *independent* Hebrew judge → DEFER 1b (human harvest loop covers idiom; revisit when 3.0 has
  a hosted endpoint); (b) auto-fix loop designed (high-confidence flags only), build later;
  (c) gate WIRING into the content-agent gate sequence = reviewed follow-on, not done.
  NOTE: Agent-tool worktree isolation left the main checkout on feature/admin-blog-editor;
  orchestrator restored master (both were at the same commit, no loss) — avoid worktree
  isolation for in-repo builds going forward.
---

# TASK-341 — PHASE 1: Hebrew-correctness layer

CLOSED core (grammar gate + reader-context lock). Follow-ons (separate small tasks):
wire the gate into the content-agent gate sequence; build the auto-fix loop; idiom reviewer
deferred pending a viable sovereign endpoint.
