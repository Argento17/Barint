---
id: TASK-179M
title: Glass Box W1 go-live — Data wires glassBox object into pilot frontend JSON
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179J, TASK-179K, TASK-179L]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  glassBox object wired ADDITIVELY into the two pilot FE JSONs — hummus_frontend_v4.json (64 products:
  61 unconstrained / 1 demote / 2 withhold) + maadanim_frontend_v2.json (84: 83 / 1 / 0). CC verified:
  glassBox present on all products, published score/grade fields intact (128 in hummus); Data proved
  additivity (snapshot → strip glassBox → byte-identical). Reproducible generator wire_glassbox_frontend.py.
  Emits CODED disclosureCodes (proportions|compound|generic_additive|protein_source|missing_field), not Hebrew
  prose (frontend maps via 179K copy). WARN-1 fixed in proof_B. KEY: actual live blast radius is SMALLER than
  the worst-case Product accepted — only 2 hummus → לא נוקד, 0 maadanim withholds, and both demotes keep their
  grade letter (flag-only). Locked numbers untouched; no engine/score change.
cc_comments:
  - flag: verify
    text: "Frontend (179N): BariGlassBoxVM (view-models/index.ts ~L93-102) is prose-oriented; extend it with the CODED fields Data emits — disclosureCodes[], gatedScore, gatedGrade, withheld (keep gateState). Map codes→Hebrew via w1_disclosure_copy_v1.md (179K). Nothing renders until NEXT_PUBLIC_GLASSBOX_D5D6 is ON."
summary: >
  Go-live wiring: Data emits a per-product `glassBox` object into the pilot frontend JSON (hummus + maadanim)
  carrying the engine's flag-ON D5/D6 result — gateState (unconstrained·demote·withhold), the gated outcome
  (demoted grade / null), and the CODED disclosure-gap findings — ADDITIVE to the existing published grade,
  so the frontend flag (NEXT_PUBLIC_GLASSBOX_D5D6) is the live switch AND the rollback (flag OFF = existing
  grade rendered, glassBox ignored, pages unchanged). Consumer Hebrew strings stay Content-owned (179K),
  mapped in the frontend from the gap codes — Data emits codes, not prose. Numbers are locked (179J/179L).
  Also fixes WARN-1 (proof_B wrong example SKU). No published grade value changes; glassBox is additive metadata.
---

# TASK-179M — Data wires glassBox into pilot JSON (Glass Box W1 go-live)

Part of TASK-179 (Glass Box), Wave 1 go-live. Chain: 179J/K/L (lock+copy+spec) → **179M (this, wiring)** →
Frontend integration (read glassBox + map codes→Content copy + L411 unify + null-parity) → final QA → owner flip.
Engine flag-ON output: `03_operations/bsip2/proto_v0/reports/glass_box/_pilot_{hummus,maadanim}_on.json`.
VM contract already in place: `BariGlassBoxVM`. Domain agent proposes RETURNED.
