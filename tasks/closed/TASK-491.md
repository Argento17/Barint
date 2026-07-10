---
id: TASK-491
title: Content-authoring template — bake the antithesis-scan-ALL-forms rule into the content lane's self-audit (recurring miss, caught 4× this session)
owner: content-agent
status: CLOSED
priority: LOW
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "MERGED LIVE — docs PR #74 (voice files 5+7: all-forms antithesis scan + self-check line) + code-gate PR #75 (naturalness_gate.py _T1_VELO non-comma ולא + _ALA standalone אלא, carve-outs coded, 4 escapees now flag, 21 samples unchanged, selftest PASS). Both diff-verified internal-only (0 consumer/score). The recurring antithesis-miss (4× this session) now closed at BOTH human-guidance and automated-enforcement level. Orchestrator-merged (internal)."
depends_on: []
blocks: []
category_id: null
summary: >
  Process fix. Content lanes' self-audit for owner-banned define-by-negation ("X, not Y") has repeatedly
  scanned ONLY comma-prefixed לא, missing the non-comma ולא and אלא forms. QA has caught this class 4×+ this
  session (TASK-477 RT-M1, TASK-484, TASK-461 chocbars/cakes/hardcheese, TASK-490). Bake the all-forms scan
  into the durable content-authoring guidance so it stops recurring — NOT just a per-dispatch instruction.
---

# TASK-491 — content-template antithesis-scan-all-forms (process, internal)

## Deliverable (find the right home, then edit; do NOT close — propose RETURNED)
1. Locate the durable content-authoring self-audit guidance the content lanes read — likely under
   `content_voice/tom_bari_voice/` (voice system, 9 files) and/or the owner-phrasing rule reference
   (no_x_not_y_phrasing). Find where the "no X-not-Y / antithesis" rule is stated and where a content author
   would run their pre-return self-check.
2. Add an explicit ALL-FORMS scan rule + the exact regex the QA gate uses:
   `[,;]?\s*ו?לא\s` (covers comma-לא AND non-comma ולא) + standalone `\bאלא\b` + English "X, not Y".
   State plainly: the recurring miss is the NON-comma `ולא` form — scan it every time. Cite the 4× recurrence
   so the rationale is durable.
3. If a content-authoring checklist / return template exists, add the all-forms residual-antithesis scan as a
   required pre-return self-check line.

## Guards
- Documentation/process only. ZERO consumer copy, ZERO score, ZERO code-behavior change. Base off origin/master.
- Do NOT rewrite any live product copy here — this is about the AUTHORING GUIDANCE, not any page.
- Internal non-consumer → orchestrator may merge after verify.

## Return: 5-part (which file(s) updated, exact rule text added, where the self-check line lives) + Return
Contract JSON. Propose RETURNED.

## DOCS DONE — merged PR #74 (squash). Files 5_banned_phrases + 7_voice_match_gate updated w/ 4-form scan + self-check line 11. Verified docs-only diff, orchestrator-merged (internal).
## CODE-GATE FOLLOW-UP (the real enforcement gap the agent surfaced) — dispatched
- integrations/clients/naturalness_gate.py `_T1_CLOSER = re.compile(r"[,—]\s*לא\s+\S+")` catches ONLY comma/dash — misses non-comma ולא, the exact 4× escapee. Fix the coded gate to mirror the doc's forms + carve-outs (earned bare "...זה לא." fragment MUST stay clean). Keep 491 open until this lands.
