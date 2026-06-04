---
id: TASK-181L
title: Glass Box W4 rework QA re-verify OFF identity plus new ON score-impact after medium split
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181K]
blocks: []
category_id: null
roadmap_impact: true
work_type: qa
cc_reviewed: 2026-06-04
close_reason: >
  CC gate PASS (2026-06-04). QA re-run delivered the decisive before/after (17-down/3-up →
  17-down/0-up) and the key finding that the downgrades come from the HP de-amplification,
  not the medium-band rule — independently re-verified OFF identity, frozen invariants hold.
  All 3 findings resolved: F2 (HP de-amp) owner-accepted KEEP after Nutrition+Product
  pressure-test; F3 fixed + re-validated under TASK-181M; F1 (materiality inert when D5D6 OFF)
  logged as a correctness item (owner scoped the follow-up to F3 only). Analysis complete and
  consequential — closing.
cc_comments:
  - flag: fyi
    note: >
      CC gate PASS on the analysis (2026-06-04). OFF safety re-verified INDEPENDENTLY (QA
      re-derived the genuine pre-W4 engine from fc6f13a~1 and diffed — current-OFF == pre-W4,
      0-diff, 342 products; not a self-baseline tautology). Frozen invariants PASS (milk 85/A,
      snack 70/B). Split is correct at the D3 layer (non-material → 0 D3 movement, verified).
  - flag: blocker
    note: >
      BEFORE/AFTER: original 17-down/3-up → new 17-down/0-up. NOT ~flat. The rework removed the
      3 upward moves but the 17 DOWNGRADES SURVIVE — because they were never caused by the D3
      medium-band scale we fixed. THREE findings for owner/Nutrition/Product:
      (F1) MATERIALITY DEGENERATE: 0/342 products classify as `material`. With BARI_GLASSBOX_D5D6
      OFF (the test state) the disclosure_profile is None, so M1/M2 can't fire, M3 falls back to 0,
      M4 piggybacks → never fires. The material/0.70 branch is dead code in the D5D6-OFF path. Split
      correct on paper, inert offline. Route Data/Nutrition: make D5D6 a hard precondition, or build
      an offline token resolver.
      (F2) THE REAL DRIVER is the HP NOVA-weight de-amplification (a SEPARATE co-signed EV-042
      mechanism, untouched by the rework): W4 removed the NOVA-class discount on hyper-palatability
      combo penalties (fat+sugar/fat+sodium/crunch+sweet), so NOVA-3 products now take the FULL HP
      penalty instead of ×0.5 → ~−3 pts → B→C. 13 hummus + 1 maadanim of the 17. This — not the
      uncertainty rule — is what moves the shelf down. Needs an owner/Nutrition/Product decision: is
      the HP de-amplification wanted, given it's the actual lever?
      (F3) the −5 non-material D6 dent flips 3 maadanim to `insufficient_data` (grade-label change,
      score unchanged) at the confidence=40 boundary — counter to the "confidence dent, never a grade
      cut" promise both signers relied on. Nutrition/Product confirm if acceptable.
      Reports: reports/glass_box/w4/qa_181l_on_impact.json. Analysis complete; held for owner.
summary: >
  Re-verify BARI_GLASSBOX_W4 OFF = byte-identical (0-diff). Produce the NEW ON score-impact analysis after the material/non-material split: expect the net-downward shelf effect to collapse toward ~flat on quality (grade moves now only from material/low-certainty products; non-material peripheral-gap products no longer move grade, their doubt shows as confidence). Report new grade-move counts vs the prior 17-down/3-up, broken down by material vs non-material. Confirm frozen invariants hold (milk 85/A, snack 70/B). Analysis only - no flag flip, no published rescore.
---

# TASK-181L — Glass Box W4 rework QA re-verify OFF identity plus new ON score-impact after medium split

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
