---
id: TASK-181K
title: Glass Box W4 rework Data re-implement material non-material split behind BARI_GLASSBOX_W4 OFF byte-identical
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181J]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04). Revised rule re-implemented to EV-042: flat
  medium=0.70 replaced by the material/non-material split (medium-material 0.70 / medium-non-
  material 1.0 = no D3 move + D6 −5). OFF byte-identity INDEPENDENTLY verified (0-diff, 4
  corpora / 342 products). Engine-only change (score_engine.py 252/88); no constants/JSON/
  flag/published data touched; frozen tables + classifier intact. ON smoke confirms the fix:
  medium-non-material products no longer move on D3 (NOVA-4 35.0 / NOVA-1 95.0, vs 39.5 / 81.5
  under 181G); hummus 3/3 + maadanim 25/25 medium-non-material now zero D3 movement; material
  products still move. Flag not flipped, no grade moved. 3 implementation details flagged for
  QA (181L) confirmation — see cc_comments. Closing unblocks TASK-181L (QA re-run).
cc_comments:
  - flag: verify
    note: >
      3 implementation details for 181L to confirm (all safe-by-construction): (1) M3
      unresolved-fraction >30% has no true token list at the D3 stage, so it falls back to a
      conservative proxy (bare-generic + unnamed-compound markers) — fires via the
      unnamed-compound sub-branch + M1; pure token-% path leans toward non-material (no-move)
      on legible lists. (2) M4 worst-case-flip piggybacks on an M1/M3 observable (fires when
      class<4 AND an unresolved token could be the flipping marker) rather than re-deriving a
      class flip independently. (3) D6 max-combine implemented as deduct only
      max(0, d3_target − d5_applied) so net = max(d3,d5) per token (verified: severe-D5 −20
      absorbs the −10, no double-count). QA confirm the materiality rate matches intent.
summary: >
  Re-implement the D3 rule in score_engine.py to the revised rule from 181J: replace the flat medium=0.70 score-pull with the material/non-material split - material uncertainty shrinks the score (low-band treatment), non-material uncertainty does NOT move the D3 score (routes to D6/confidence only). Keep everything behind BARI_GLASSBOX_W4 (default OFF); OFF = byte-identical to current baseline (re-run verify_glassbox_w4_off_identical.py, 0-diff). Re-emit the impact preview. Does NOT flip the flag, rescore published data, or touch frozen invariants.
---

# TASK-181K — Glass Box W4 rework Data re-implement material non-material split behind BARI_GLASSBOX_W4 OFF byte-identical

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Return block (proposed RETURNED — 2026-06-04, data-agent)

Re-implemented the revised EV-042 (TASK-181J) D3 rule in `score_engine.py` behind
`BARI_GLASSBOX_W4` (default OFF). The flat medium=0.70 scale is replaced by the
material/non-material split. OFF byte-identical (0-diff). No flag flip, no published
rescore, frozen invariants untouched. Built strictly to EV-042 bound values. Proposing
RETURNED for the CC close-readiness gate. **TASK-181L (QA re-run) unblocks now.**

- File changed: `03_operations/bsip2/proto_v0/src/score_engine.py` (engine only).
- OFF byte-identity: PASS 0-diff — hummus(69) / maadanim(200) / snack_bars(53) / golden_milk(20).
- 5 pieces in: materiality M1–M4 (`_d3_uncertainty_materiality`); scale selector
  (`_w4_confidence_scale`, medium→0.70 material / 1.0 non-material); bound cap-scaling
  (`cap_effective = 100−(100−base_cap)×scale`); D6 routing (non-material −5, low −10,
  max-combined with D5, never summed); `uncertainty_materiality` in the struct.
- ON smoke: NOVA-4 medium-non-material → 35.0 (no move; was 39.5 under 181G); NOVA-1 → 95.0
  (no move; was 81.5). hummus 3/3 + maadanim 25/25 medium-non-material no longer move on D3.
