---
id: TASK-540
title: Harden template-fingerprint validator: decouple from author_copy.py internal constant names + re-wire to battery
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-08
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified 2026-07-09 (unattended run, branch task506). Decoupling from author_copy.py
  internal constant names is DONE: copy_constants.get_author_copy_fingerprints() resolves BOTH the
  renamed _DIM_INTERPRETATION_PHRASES and legacy names (_DIM_INTERPRETATION_BASELINE, _STRENGTH_PHRASE)
  via getattr fallback (copy_constants.py:170-189) — no import of a specific internal constant, so it no
  longer crashes against live author_copy.py. Re-wired to the battery: validate_comparison_page.py:251-276
  invokes the validator with --emit-json and treats a real FAIL as a HARD gate (appended to fails →
  RESULT: FAIL); only a validator crash/absence is a soft WARN. --emit-json interface confirmed
  (passed/banned_hits/sentence_repeat_hits/phrase_hits/mass_template_hits keys present). Controls
  re-proven against LIVE author_copy.py: negative fixture FAIL exit 1; round-2 yogurt PASS exit 0.
  NOTE: the DoD's "positive brined PASS" control is now stale — brined_cheeses genuinely carries 4
  banned mechanism-narration rows (correctly flagged, exit 1) → routed to TASK-542; the clean positive
  control is the round-2 yogurt, which PASSES. Gate behavior is correct; brined is a real content defect,
  not a validator false-positive.
summary: >
  Grok built validate_copy_authored.py (TASK-536, controls verified: catches baseline+raw-gram, passes real authored pages incl round-2 yogurt). But its fingerprint extraction imports author_copy._DIM_INTERPRETATION_BASELINE, which round-2 renamed to _DIM_INTERPRETATION_PHRASES -> crashes against live author_copy.py, hard-failing the battery. Wiring reverted; standalone validator + _fixtures/ kept. FIX (route C1-GROK/CURSOR, worktree): make constant-name resolution robust (getattr fallback / parse both names), re-prove all 4 controls (negative fixture / positive brined / incident original-yogurt / fix round-2 yogurt) against the LIVE C:/Bari author_copy.py, then re-add the battery wiring. Do AFTER TASK-533 QA finalizes author_copy.py's constant name.
---

# TASK-540 — Harden template-fingerprint validator: decouple from author_copy.py internal constant names + re-wire to battery

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
