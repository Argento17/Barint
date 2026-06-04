---
id: TASK-179I
title: Glass Box W1 — surface D5/D6 states on pilot pages + preview (Frontend)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179G, TASK-179H]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  D5/D6 consumer presentation built behind frontend flag NEXT_PUBLIC_GLASSBOX_D5D6 (default OFF). CC gate
  verified: all FE files present; grep confirms ZERO glass-box content in live src/data/comparisons/*.json
  (no live score/JSON touched); tsc/lint/build clean; screenshots produced. Visual confirmed (mobile shot):
  clean single-ingredient חומוס מוקפא stays 85/A (single-ingredient protection visible); withhold → calm
  לא נוקד chip (dash, no number) + "אין מספיק מידע בתווית כדי לדרג"; demote → grade kept + ניתוח חלקי flag +
  "מה לא צוין בתווית" plain note. Calm register, no accusation, no raw numbers (Q2/Q4 honored). Preview route:
  /dev/glass-box-preview with NEXT_PUBLIC_GLASSBOX_D5D6=on. Shots: 03_operations/bsip2/proto_v0/reports/glass_box/preview_shots/.
cc_comments:
  - flag: fyi
    text: "Go-live data-shape dependency (NOT this task): for real go-live, Data must emit a per-product `glassBox` object in the frontend JSON (gateState + plain-language partialNote / withholdReason / disclosureNotes — the coded D5 findings translated to consumer Hebrew), and Content must own/approve that final wording. The VM contract (BariGlassBoxVM) is already in place to receive it."
summary: >
  Wave 1 presentation: build the consumer-facing rendering of the two new D5/D6 states on the pilot
  comparison pages (hummus + maadanim) behind a frontend feature gate — the `ניתוח חלקי` partial-disclosure
  flag (demote) and the `לא נוקד` withhold state (null, shown instead of a grade), driven by the engine's
  new D5/D6 output fields. Per DEC-006 Q4: drilldown shows plain-language findings, never raw numbers or
  internal terms; calm register (governance §9 — "לא צוין"/"לא ניתן לאמת", never accusatory). Hard constraint:
  do NOT modify live published scores or comparison JSON — render from a flag-ON pilot/preview dataset behind
  the gate; OFF = current UI unchanged. Deliver a visual PREVIEW the owner can review for the flag-ON go-live
  decision. Reuse shared components; mobile-first.
---

# TASK-179I — Surface D5/D6 states + preview (Frontend)

**Part of:** TASK-179 (Glass Box), Wave 1. **Chain:** 179G build → 179H QA PASS → **179I (this, presentation)**
→ post-pilot Product D7 review (numbers + P3 spec reconcile + WARN-2 acceptance) → flag-ON go-live (owner/D10).
Domain agent proposes RETURNED. Engine output + spec: `d5_d6_rule_spec_v1.md`; pilot replay tables in
`03_operations/bsip2/proto_v0/reports/glass_box/`. Constraint: presentation only, no live score/JSON change,
behind a feature gate; produce a reviewable preview (the "nice visual") for the go-live decision.
