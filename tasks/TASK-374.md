---
id: TASK-374
title: Project Tom's Voice — natural-Hebrew content quality program (naturalness rejection gate)
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-22
depends_on: []
blocks: []
category_id: null
summary: >
  Lift Bari Hebrew from mediocre to excellent for the content-first strategy. Centerpiece: an independent automated LLM-judge Naturalness Gate that rejects translationese (the defect no existing gate catches). Pilot on protein-bars/snacks/granola. Phased: baseline -> naturalness gate -> translationese taxonomy+detector -> category golden -> harvest cadence.
---

# TASK-374 — Project Tom's Voice — natural-Hebrew content quality program (naturalness rejection gate)

Charter: `content_voice/tom_bari_voice/PROJECT_TOMS_VOICE_CHARTER.md`. Memory: `project_toms_voice`.

## Owner rulings (2026-06-22)
- Scope: pilot on protein-bars / snacks / granola, then roll across live categories.
- Critic: automated **independent** LLM-judge gate is the centerpiece.
- Target register: *opinionated substance in natural connected Hebrew* — NOT "calm"
  (AI over-corrects to neutral mush), NOT punchy-calqued. Two failure modes: F1
  translationese-punch + F2 neutral-bland.
- Repair (not retire) the "X לא תמיד אומר Y" calque → "X הוא לא בהכרח Y".
- Pro/con labels in owner rewrites = editing shorthand; final copy stays prose.

## Progress
- **Phase 0 — DONE.** Translationese taxonomy T1–T7 + closer meta-finding
  (`10_translationese_taxonomy.md`); 8 owner gold rewrites + 12 flagged live lines
  (`phase0_owner_gold_examples.md`); fingerprint calque repaired (files 2/4); logged
  as Harvest #5 (file 8).
- **Phase 1 — Layer 1 DONE + verified.** `integrations/clients/naturalness_gate.py`
  (deterministic T1–T7 pre-filter), `python -m ... ` self-test PASS (7/7 flagged
  lines HIGH; 6/6 gold lines clean incl. guards). Wired into Content Agent self-check
  (gate 5.6) + External Data Access table.
- **Phase 1 — Layer 2 SPEC DONE.** Two-axis LLM-judge rubric + prompt + thresholds +
  integration (`11_naturalness_gate.md`); wired into Adversarial QA Track C as the
  independent Naturalness judge.

## Phase 1 pilot result (protein-bars, 2026-06-22)
- Layer 1 run live across all 90 consumer strings in `protein_bars_frontend_v1.json`
  (`content_voice/tom_bari_voice/_phase1_pilot_run.py` → `_phase1_pilot_report.md`):
  **18 HIGH-block · 6 medium · 66 clean.** All 18 HIGH are genuine T1 `X, לא Y`
  calques (zero false positives); the shelf systematically leans on that one tell.
  F2 signal mostly low/medium — stance is present; the defect is F1 translationese.
- F2 "calm-trap" negative test ADDED to the gate self-test (a hedge-only paragraph
  must read f2_risk=high; a verdict line must read low) — `python -m ...` PASS.

## Phase 1.5 — DONE (2026-06-22): fingerprint recalibration
Root-cause fix so the agent stops *generating* the calque. `2_voice_fingerprint.md`:
§0.5 new default-register section (opinionated substance in connected prose; F1+F2
failure modes; punch = seasoning-when-earned; keeps stance as F2 guard; supersedes
conflicting punch-default rules); §1 opener broadened (calm-orienting OR scene);
§5 rhythm flipped to connected-prose default; §3 "(!)" → seasoning-only + gate-monitored.
Logged in file 8 (Harvest #5, APPLIED).

## Foundation complete — remaining program work (separate dispatches)
- Route protein-bars corrected copy through the Content Agent + two-gate
  (orchestrator does NOT author inline — content_signoff_hard_rule). The gate now
  blocks the 18 HIGH lines until fixed.
- Wire Layer 2 (LLM judge) as a runnable harness on an independent lane (or confirm
  it runs inside Adversarial QA Track C per agent doc).
- ~~Phase 2 (syntax sub-blacklist in file 5)~~ — **DONE 2026-06-22**: file 5 §1.5
  translationese sub-blacklist (T1–T7 + F1/F2 framing + calibration guards) added; gate
  order updated (5.6 naturalness pre-filter, 7 independent judge).
- ~~Phase 4 (standing harvest cadence)~~ — **DONE 2026-06-22**: file 8 cadence protocol
  (per-batch / per-redline / gate-miss triggers; promotion + calibration thresholds;
  rides the existing two-gate, no separate scheduled job).
- **Phase 3 (category golden: snacks/granola) — BLOCKED on lane.** Requires authoring
  NEW gold copy = consumer-facing content authoring → must go through the Content Agent
  + two-gate (content_signoff_hard_rule); orchestrator must NOT author inline. Needs an
  explicit dispatch authorization from the owner.
- **Protein-bars copy regeneration** (fix the 18 HIGH calques the gate caught) — same
  lane constraint: Content Agent dispatch through the two-gate.
- Optional: a runnable Layer-2 LLM-judge harness (independence already covered by the
  two-gate, so lower priority).
- Committed on branch `task-374-toms-voice`: d98406d8 (Phases 0/1/1.5), ebb796bf
  (Phase 2), + Phase 4 commit. Not pushed (owner-gated).
- Phase 1.5 fingerprint recalibration pass (default texture → connected prose; punch
  = seasoning-when-earned).
- Phases 2–4 (syntax sub-blacklist, category golden, harvest cadence).
- Nothing committed yet (owner-gated).
