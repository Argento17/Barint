---
id: TASK-181J
title: Glass Box W4 rework Nutrition split medium into material and non-material uncertainty supersede EV-042 plus Product co-sign
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: governance
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04). EV-042 revised in place per owner directive
  (material/non-material medium-band split): bound_value_set_4 (M1–M4 materiality test,
  codeable, incl. the worst-case-NOVA-flip test), bound_value_set_5 (D6 routing: non-material
  −5, low-conf-NOVA −10, both max-combined with D5, no double-count), revised scaling
  (medium-material 0.70 / medium-non-material 1.0 = no D3 move), bound cap-scaling, "less
  punitive" retired for confidence-first framing; PRE-REWORK BASELINE preserved (not
  overwritten). BOTH D7 co-signs now recorded and verified in the file: Nutrition (TASK-181J)
  + Product (TASK-181J, co_sign flipped PENDING→CO-SIGNED, 0 PENDING left). Frozen-invariant
  case strengthened (strictly fewer D3 moves). Governance only — no engine/score/flag/published
  data touched by 181J. Rule adopted on paper, behind BARI_GLASSBOX_W4 (default OFF); live flip
  remains a separate owner decision. Closing unblocks TASK-181K (Data re-implement).
cc_comments:
  - flag: fyi
    note: >
      CC gate PASS (2026-06-04). EV-042 revised in place (marked, not silent) — verified:
      REVISION NOTICE + new bound_value_set_4 (material/non-material test, M1–M4, codeable)
      + bound_value_set_5 (D6 routing) + PRE-REWORK BASELINE block preserving the original
      reasoning + "less punitive" line. Implements the owner directive exactly: medium-band
      split → medium-MATERIAL = 0.70 shrink, medium-NON-MATERIAL = 1.0 (D3 score does NOT
      move; doubt → D6 −5). Reconciled prior unbound items: low-conf-NOVA→D6 = −10; cap-scaling
      now bound (cap_effective = 100−(100−base)×scale; non-material loosens neither score nor
      cap). Both D3→D6 terms max-combined with D5 (no double-count). Frozen-invariant case is
      STRENGTHENED (strictly fewer D3 moves). Scope: 181J edited only the registry file (the
      feature-flags.ts M is 181I's uncommitted work, not 181J). Nutrition D7 co-signed; Product
      D7 PENDING. CLOSE GATED ON PRODUCT D7 CO-SIGN — mirrors 181F. 181K stays BLOCKED until
      Product co-signs.
summary: >
  Owner directive 2026-06-04: split the current single medium-certainty band into MATERIAL uncertainty (the unresolved/unknown signal could plausibly change the processing read - e.g. an unnamed emulsifier/stabilizer that decides processed-vs-ultra, D5 severe band, or a large unresolved fraction) and NON-MATERIAL uncertainty (visible signals already pin the read; the unresolved term is peripheral, e.g. 'spices' on an otherwise legible short whole-food list). ONLY material uncertainty may shrink the D3 score (it falls to the low-band treatment the owner already accepts). NON-MATERIAL uncertainty affects CONFIDENCE (D6) ONLY - the D3 score does not move. This honors Bari's unknown-reduces-confidence-first principle. Deliverable: a superseding evidence-registry entry revising EV-042 - define the material/non-material observable criteria, the revised score-scaling (material->shrink; non-material->no score move / scale 1.0, route doubt to D6), bind the D6 non-material deduction size, and the cap-scaling. Nutrition D7 authored; Product D7 co-sign required (routed after). No engine code, no score move, flag stays OFF.
---

# TASK-181J — Glass Box W4 rework Nutrition split medium into material and non-material uncertainty supersede EV-042 plus Product co-sign

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
