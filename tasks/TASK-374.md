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

## LIVE FILE (v2) — render works, NOT ship-clean yet (2026-06-22)
The protein-bars page actually renders from `protein_combined_frontend_v2.json` (32
products, UNTRACKED — an in-flight bars-rework migration; loader switched v1→v2 in the
working tree; HEAD still imports v1). Content Agent rewrote 38 strings → 0 HIGH on the
(then) gate; render-verified live at localhost:3000/hashvaot/protein-bars (clean copy
served). Independent judge: **CONDITIONAL PASS, 23/32**. Caught the agent AGAIN swapping
calques — this time bare-word closers (`סביר.`/`מהונדס.` ×8) + a grade-token leak (`C.`)
+ 3 sibling-calques. Gate hardened a 3rd time (BARE + GRADE + T4s detectors; selftest
15 flagged). Remaining to ship-clean v2 (cross-lane):
- Naturalness refine: 7 HIGH (bare-word closers + grade token) + sibling calques — content lane.
- Firewall (pre-existing bars-rework copy): `בריא יותר מהממוצע` (health claim) + `צריך
  לאכול במודעות` (prescriptive) — content rephrase; health claim may need nutrition-agent.
- Data integrity (data-agent / bars-rework): pb-013 & pb-014 share a display name;
  `_meta.product_count` 32 vs fix_note "33 remain"; pb-032 null fiber (handled OK).
- v2 is untracked bars-rework — committing it must be coordinated with that task, not unilateral.

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
- ~~**Protein-bars copy regeneration**~~ — **DONE 2026-06-22, two-gate PASSED.**
  Content Agent (dispatched) rewrote 24 strings → 0 HIGH. Independent Adversarial QA
  judge: CONDITIONAL PASS (7/16; 4 HIGH blockers — the agent had traded `X, לא Y` for a
  NEW calque family `עובד כ-X; פחות כ-Y` + 2 T4 metaphors + 1 META opener). **Gate
  hardened** to catch those (T1b/META detectors + T4→HIGH; selftest 12 flagged lines).
  Content Agent refine cycle → 0 HIGH on hardened gate. Independent judge RE-JUDGE:
  **PASS, 16/16 F1≥4 AND F2≥4, 0 CRITICAL.** Orchestrator verified: 0 HIGH, JSON valid,
  numbers + scores/grades identical to baseline. 2 non-blocking MEDIUM polish notes
  (round 33.7→34 in prot-003 verdict; prot-002 closer slightly soft) → content-agent.
  This proved the two-gate works: Layer 1 said clean, the independent judge caught the
  swapped calque, the gate learned it (Phase-4 cadence trigger 3).
- Optional: a runnable Layer-2 LLM-judge harness (independence already covered by the
  two-gate, so lower priority).
- Committed on branch `task-374-toms-voice`: d98406d8 (Phases 0/1/1.5), ebb796bf
  (Phase 2), + Phase 4 commit. Not pushed (owner-gated).
- Phase 1.5 fingerprint recalibration pass (default texture → connected prose; punch
  = seasoning-when-earned).
- Phases 2–4 (syntax sub-blacklist, category golden, harvest cadence).
- Nothing committed yet (owner-gated).
