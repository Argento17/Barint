---
id: TASK-179H
title: Glass Box W1 — independent QA verification of D5/D6 build
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179G]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  Independent QA PASS (conditional for flag-ON go-live); no hard fails. QA reconstructed the pristine
  pre-edit engine from git HEAD and diffed vs current under flag OFF → 0-diff / 342 products (didn't trust
  the build's own baseline); milk 85/A + snk-001 70/B hold under OFF; "OFF changes nothing vs current
  engine" = TRUE (milk's published-trace deltas are RECAL, not Glass Box). Flag ON zero-promotion re-derived
  independently. P3 token-aware deviation = PASS (faithful to spec intent). Verdict report:
  03_operations/qa/reports/qa_glassbox_d5d6_w1.md. Three follow-ups carried (none blocking the build, which
  stays OFF): see cc_comments.
cc_comments:
  - flag: fyi
    text: "WARN-2 (the go-live decision point): flipping BARI_GLASSBOX_D5D6 ON removes published-equivalent grades from real pilot products — 4 hummus 72–75/B → לא נוקד, 1 maadanim 45/D → לא נוקד (panel-absent / severe+thin). Correct per spec §2.3, but consumer-facing grade removals; Product+owner must consciously accept this at the flag-ON go-live gate."
  - flag: verify
    text: "P3 doc-vs-code reconciliation: amend spec d5_d6_rule_spec_v1.md §1.1 P3 to the token-aware rule the engine implements, + formal Nutrition sign-off, at the post-pilot co-sign."
  - flag: verify
    text: "WARN-1 (doc defect, Data to fix before the proof is cited): proof_B_flag_on_pilot_diff.md §3 example names the wrong withheld product (חומוס לבן ענק שופרסל is actually unchanged 85/A); the real 4 hummus withholds are plain חומוס / חומוס ענק SKUs. Counts are correct."
summary: >
  Independent QA verification of the Glass Box D5/D6 engine build (TASK-179G) — the go-live-gate proof.
  Re-verify Proof A (flag OFF = byte-identical, 0-diff on golden + frozen corpora; frozen invariants
  milk 85/A + snk-001 70/B preserved; resolve the self-baseline anchoring nuance — confirm milk under
  RECAL+GlassboxOFF still matches published, and snk/bread hold). Re-verify Proof B (flag ON pilot,
  hummus+maadanim: ZERO promotions, demote/null-only, EV-036 prevents over-demotion). Assess Data's three
  deviations — especially P3 token-aware refinement (sound? needs Nutrition formal sign?). Produce a
  QA verdict (PASS/WARN/FAIL) with any hard-fails/warnings. Verification only — no code change; flag stays OFF.
---

# TASK-179H — Independent QA verification of D5/D6 (Glass Box W1)

**Part of:** TASK-179 (Glass Box), Wave 1. **Chain:** 179G build → **179H (this, independent verification)**
→ Frontend (surface flag/confidence on pilot) → post-pilot Product D7 review of the numbers + P3 blessing →
flag-ON go-live (separate D10 / owner gate). Domain agent proposes RETURNED; this verdict is the authoritative
go-live-gate proof. Build: `score_engine.py` + `constants.py` (flag `BARI_GLASSBOX_D5D6`). Proofs to re-verify:
`03_operations/bsip2/proto_v0/reports/glass_box/proof_A_*.md` + `proof_B_*.md`. Spec: `d5_d6_rule_spec_v1.md`;
evidence EV-035…039.
