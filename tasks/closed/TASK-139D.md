---
id: TASK-139D
title: "Data: reconcile grade A-threshold (80 vs 85) — correct scoring.md to the live engine 6-grade scale"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: [TASK-142, TASK-143]
category_id: null
summary: >
  RULING-DAIRY-A-01 / EV-021 flagged a grade A-threshold inconsistency that "must be reconciled before
  grades publish": the live engine (constants.py GRADE_THRESHOLDS) and the frozen milk run_004 both use a
  6-grade scale with A≥80 (whole milk 85=A), while .claude/scoring.md carried a stale 5-grade table
  (A=85–100, no S-grade). Folded out of the closed TASK-139C, where it was out of charter. Decision:
  adopt A≥80 (engine + frozen-milk reality). Doc-only correction; no engine/score change. Product
  co-signed 2026-06-01.
---

# TASK-139D — Grade A-threshold reconciliation (80 vs 85)

Folded out of **closed** TASK-139C (router/olive fix), which never owned this. The reconciliation is a
scoring-governance decision under `bari-bsip2-scoring-governance`, co-signed by Product, implemented by Data.

## Decision
**A ≥ 80** is authoritative — the six-grade scale (S≥90 / A 80–89 / B 65–79 / C 50–64 / D 35–49 / E 0–34)
already in `constants.py GRADE_THRESHOLDS` and already applied by frozen milk run_004 (whole milk 85 = A).
`.claude/scoring.md`'s 5-grade table (A=85–100) was the stale outlier. Adopting A≥80 lets clean
live-culture dairy reach grade A organically — the identical earned mechanism as whole milk at 85/A
(RULING-DAIRY-A-01 / EV-021), with no category A-grant.

## Changes (no engine / no score change)
- `.claude/scoring.md` Grades table corrected to the engine's six-grade scale, with an authoritative-source
  note pointing at `constants.py GRADE_THRESHOLDS`.
- Evidence registry **EV-023** logged (`.json` primary_findings + `.md`): concept, label-observability
  (grade-band boundary), guards, rollback.

## Guards (hard) — PASS
- **No engine/scoring edit.** `constants.py GRADE_THRESHOLDS` unchanged (it already = A≥80). Only the
  stale doc table was corrected, so the golden regression (reads `constants.py`) is unaffected.
- **Frozen invariants unmoved:** whole milk 85→A (A≥80), snk-001 70→B (B≥65), bread retail_003 grades
  all map identically before/after — the engine already used A≥80; only the doc disagreed.
- **Rollback:** `git revert` of the scoring.md edit restores the prior table; zero score impact.

## DoD
A-threshold ratified (A≥80); scoring.md matches the engine; EV-023 logged with rollback. **Met.**

## Residual (non-blocking)
`batch_run_hummus_001.py` prints "A | 85–100" — a separate stale *display* string in a report generator,
non-authoritative (does not drive `score_to_grade`). Flagged for optional cleanup; not gating.

## State
Proposes **RETURNED** on delivery. Only the Central Controller records CLOSED.
This was the last substantive precondition on the **TASK-139 parent** A-reachability item; the parent's
closing re-score of run_yogurt_003 can now proceed under A≥80 → unblocks TASK-142 / TASK-143.

---

## Return block — proposed RETURNED (data-agent, 2026-06-01)

**Decision:** A ≥ 80 ratified (Product co-signed "Confirmed", 2026-06-01). Six-grade scale
S 90–100 / A 80–89 / B 65–79 / C 50–64 / D 35–49 / E 0–34 is authoritative.

**Applied:**
- `.claude/scoring.md` grade table corrected to the engine scale (+ authoritative-source note).
- **EV-023** logged in `bsip2_evidence_registry_v1.json` (primary_findings, 23 total) and `.md`.

**Guards PASS:** no engine/scoring change (constants.py already A≥80); golden regression unaffected;
frozen invariants (milk 85/A, bread retail_003, snk-001 70/B) unmoved; rollback = git revert of the
scoring.md edit (zero score impact).

**Unblocks:** TASK-139 parent closing re-score → TASK-142 (cheese full-cycle) / TASK-143. Only the
Central Controller records CLOSED.
