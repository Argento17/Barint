---
id: TASK-130D
title: Fix unknowns[] builder gap across launch categories
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "It eliminated the unknowns[] blocker across launch categories with no score changes and isolated the remaining blockers clearly."
depends_on: [TASK-130B, TASK-130C]
blocks: [TASK-132]
category_id: null
summary: >
  Single root-cause fix for the §2.5 unknowns[] gap surfaced by TASK-130C. Adds a shared
  derive-unknowns module + an idempotent surgical normalizer that inserts a deterministic
  disclosure line (instantiating the existing hummus template) whenever a scored product
  has a null nutrition field and empty unknowns[]. No score changes, no content rewrites,
  purely-additive diffs. Eliminates all §2.5 failures across launch categories.
---

# TASK-130D — Fix unknowns[] builder gap across launch categories

Parent: TASK-130. Depends on TASK-130B (validator) + TASK-130C (audit).

## Outcome (2026-06-01) — proposed RETURNED
Files: `bari-web/scripts/lib/derive-unknowns.mjs` (shared logic),
`bari-web/scripts/normalize-corpus-unknowns.mjs` (idempotent applier).
Single root cause: launch builders never emit `unknowns[]` when a nutrition field is null.
Fix instantiates the exact disclosure template already shipped in hummus_v3
("ערכי … לא היו זמינים במקור הנתונים — …"); deterministic, scored-only, never overwrites
existing unknowns. Surgical text insertion (unknowns as first expansion child) → purely
additive diffs (bread +72, snacks +54, yogurts +39 lines, 0 deletions), CRLF + float
formatting preserved. verifyAgainstOriginal asserts no field moved but unknowns.

§2.5 result: 142 working-tree failures → 0. Handoff errors 199 → 57 (remaining are §2.7
ordering + §2.8 vocab — the other two blocker classes, untouched by design).

Finding: the committed (HEAD) §2.5 gap was actually 55 products (bread 24, snacks 18,
yogurts 13). maadanim's HEAD was already compliant (87 unknowns); its working tree carried
a stale no-unknowns regen from the modified `02_products/maadanim/build_frontend_json.py`,
which my fix restored to HEAD-equivalent (net-zero diff). Durability: normalizer must run
as a post-build step (or be called by each builder) so the gap cannot reopen on re-gen.
NOT mine: pre-existing uncommitted `_meta` drift in bari-web hummus_v3 (15/7) — left untouched.
Awaiting Controller to record CLOSED.
