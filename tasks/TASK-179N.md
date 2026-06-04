---
id: TASK-179N
title: Glass Box W1 go-live — Frontend integrates glassBox on live pilot pages
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179M, TASK-179K]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  Integration complete + correct (CC verified): BariGlassBoxVM extended with coded fields; new
  glass-box-copy.ts maps codes→Content's Hebrew (179K); shared components render demote/withhold on the real
  routes behind NEXT_PUBLIC_GLASSBOX_D5D6; L411 withhold-reason unified; null-render parity confirmed
  (Product C1); tsc/lint/build all clean; OFF = byte-identical (0 glass-box strings in flag-OFF HTML).
  STRATEGIC FINDING (escalated to owner, not a defect): every product D5/D6 gates is independently filtered
  OUT of the curated hummus/maadanim displayed sets (raw-chickpea, pudding-powder exclusions; pepper-spread
  belongs to vegetable-spreads) → flag-ON is a no-op on those two pages (all displayed products unconstrained).
  The one displayed gated product (pepper-spread demote) lives on vegetable-spreads. Implication: heavy curation
  pre-removes opaque products, so D5/D6's consumer value is latent on curated category pages and lands on
  broader shelves. Go-live meaning is now an owner decision; final QA + flip held pending it.

summary: >
  Go-live integration: Frontend wires the live pilot comparison pages (hummus + maadanim) to read the
  `glassBox` object now in their JSON and render the D5/D6 states WHEN NEXT_PUBLIC_GLASSBOX_D5D6 is ON.
  Extend BariGlassBoxVM with the coded fields Data emits (disclosureCodes[], gatedScore, gatedGrade,
  withheld); build the code→Hebrew mapping from Content's final copy (179K, w1_disclosure_copy_v1.md);
  render demote (grade + ניתוח חלקי + "מה לא צוין בתווית" lines) and withhold (לא נוקד chip + canonical
  reason). Apply the L411 withhold-reason unification and confirm null-render parity (Product C1). Flag
  default OFF = pages byte-identical to today (rollback path). Build + lint must pass.
---

# TASK-179N — Frontend integrates glassBox on live pilot pages (Glass Box W1 go-live)

Part of TASK-179 (Glass Box), Wave 1 go-live. Chain: 179M wiring → **179N (this, integration)** → final QA →
owner flip. Inputs: glassBox in `bari-web/src/data/comparisons/{hummus_frontend_v4,maadanim_frontend_v2}.json`;
copy `01_framework/glass_box/w1_disclosure_copy_v1.md`; VM `bari-web/src/lib/view-models/index.ts`.
Domain agent proposes RETURNED. Presentation only; flag default OFF; no score change.
