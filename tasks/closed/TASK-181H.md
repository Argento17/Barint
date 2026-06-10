---
id: TASK-181H
title: Glass Box W4 QA OFF byte-identity verification plus ON score-impact analysis for owner go-live review
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181G]
blocks: []
category_id: null
close_reason: >
  CC close-readiness gate PASS (2026-06-04). QA delivered its job: OFF byte-identity
  re-verified (0-diff, 342 products), frozen invariants confirmed to hold ON (milk 85/A,
  snack 70/B), and the ON score-impact analysis surfaced the MATERIAL FINDING that drove the
  whole rework — W4-ON was net-downward (17 grade moves down / 3 up; all medium-band, low band
  crossed zero). That finding led the owner to split the medium band (material/non-material),
  now bound in the revised EV-042 (TASK-181J, both D7 co-signs in). This task's analysis was
  of the PRE-rework build; the post-rework impact numbers are produced fresh by TASK-181L.
  No flag flipped, no published data rescored. Analysis complete and consequential — closing.
roadmap_impact: true
work_type: qa
cc_reviewed: 2026-06-04
cc_comments:
  - flag: fyi
    note: >
      CC gate (2026-06-04): OFF safety re-verified — 0-diff across 342 products (also
      byte-identical to the pre-W4 W2 baseline); constants.py frozen tables intact; no
      published JSON touched by the W4 build. Frozen invariants HOLD when ON: milk top
      85/A, snack ceiling 70/B (no snack reaches A); the single milk-corpus grade move is
      Alpro Choco Soy (NOVA-4 non-dairy, non-frozen, moved UP E→D). No tripwire breach.
      Report: reports/glass_box/w4/qa_181h_on_impact.json.
  - flag: blocker
    note: >
      MATERIAL FINDING for the owner go-live decision (NOT an engine bug; the formula is
      the co-signed EV-042 one and behaves correctly). Turning W4 ON is NET-DOWNWARD on the
      displayed shelf: 17 grade moves DOWN vs 3 UP. "Pull toward neutral / less punitive"
      is true ONLY for NOVA-4 (base 35 < neutral 50). For NOVA-1/2/3 (base > 50) the same
      pull lowers the score — the displayed hummus shelf is mostly NOVA-3, so it drops
      (B→C, C→D). EV-042's + 181G's "less punitive" framing understates this. Two unbound
      magnitudes still need NUTRITION sign-off before any go-live: (1) the D6
      low-confidence deduction = 10 pts (EV-042 left it "may"/unspecified); (2) the
      Data-derived cap-scaling formula (loosens the NOVA-3/4 ceiling). NOVA-2 null note +
      the milk E→D mover are QA-cleared. Recommend Nutrition + Product reconcile the
      "less punitive" characterization against this 17-down distribution before the owner
      go-live gate. Held — do not go live; do not close W4 program — pending owner direction.
summary: >
  Verify BARI_GLASSBOX_W4 OFF = byte-identical (0-diff on all golden/frozen corpora incl. milk run_005_headpin, snack 70/B, bread). Then produce the ON score-impact analysis: which products' D3 sub-score / caps / grades move when ON (esp. low/medium-confidence NOVA assignments moving toward neutral 50), and confirm frozen invariants do not breach (spec 4.3). This analysis is the input to the SEPARATE owner go-live decision (flag flip = frozen-invariant tripwire). Does not flip live.
---

# TASK-181H — Glass Box W4 QA OFF byte-identity verification plus ON score-impact analysis for owner go-live review

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
