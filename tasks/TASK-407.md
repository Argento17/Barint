---
id: TASK-407
title: Additive lexicon: add חומר משמר spelling (preservatives slip through)
owner: nutrition-agent
status: RETURNED
priority: LOW
created_at: 2026-06-26
returned_at: 2026-06-27
depends_on: []
blocks: []
category_id: null
dispatched: "2026-06-27 unattended orchestrate — native Data Agent (Sonnet), worktree-isolated, BUILD lexicon variant + MEASURE cross-corpus score impact only."
orchestrator_verification: >
  RETURNED + orchestrator-VERIFIED 2026-06-27. Worktree agent-a37a0618aaa7b3be5, branch
  worktree-agent-a37a0618aaa7b3be5, commit 929e236de. Verified: (1) variant added at
  signal_extractor.py:135 (חומר משמר alongside חומר שימור in the preservative pattern);
  (2) worktree changed NO frontend JSON — only the 2 engine src files + 2 analysis scripts →
  NO published score moved (confirmed via git diff). Measurement (NOT re-scored — agent's own
  caveat): 194 live products contain "חומר משמר"; 168 already detected (carry an E-number too);
  26 net-new detections across 7 shelves; 7 estimated grade-boundary crossers AT A -4pt ASSUMED
  PENALTY (bread 2079217 B→C, 481197 A→B; brined 7290114314015 B→C, 2107798 B→C; cheese
  7290112342102 D→E; granola_v1 7290011668587 C→D; hummus 7290011800642 C→D). 2133889 sanity =
  already-detected via E202 (correct). CAVEAT FOR OWNER: the 7 grade moves are an ESTIMATE; a real
  BSIP2 re-score is required to confirm actual deltas.
  TRIPWIRE-1 (adds preservative detection → moves published scores). NOT CLOSED. PARKED for owner
  ship decision; re-score-to-confirm + deploy are owner-gated."
summary: >
  TASK-395 handoff F3. Contested/additive lexicon keyed on חומר שימור misses common חומר משמר spelling -> preservatives slip past detection (e.g. barcode 2133889). Add חומר משמר variant to the lexicon.
---

# TASK-407 — Additive lexicon: add חומר משמר spelling (preservatives slip through)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
