---
id: TASK-179O
title: Glass Box W1 — final go-live QA pass (full integrated path)
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179N]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  Final go-live QA PASS — clear to flip NEXT_PUBLIC_GLASSBOX_D5D6=on. CC verified report exists
  (03_operations/qa/reports/qa_glassbox_d5d6_golive.md). All green: OFF byte-identical on hummus/maadanim/
  vegetable-spreads (0 glass-box strings flag-OFF); flag-ON renders the one displayed gated product correctly
  (pepper-spread bsip1_7290104721533 → ניתוח חלקי + "חלק מהערכים התזונתיים לא הופיעו בתווית", grade B
  unchanged); hummus/maadanim no-op is expected-correct (gated ids filtered out, wiring proven live on
  veg-spreads); copy fidelity + L411 unification, no leakage; published grades unchanged (glassBox additive,
  FE flag display-only); tsc/lint/build clean OFF and ON. COMMIT-HYGIENE (escalated to owner): the website
  working tree intermixes the Glass Box go-live set with PRE-EXISTING unrelated TASK-169 recal edits
  (cheese_frontend_v2.json, bread/cheese/maadanim-page-data, corpus.ts, build_frontend_json.py, a maadanim
  verdict reframe) — the go-live commit must be SCOPED to Glass Box only; the TASK-169 edits need separate
  sign-off. Flip = scoped Glass Box commit + NEXT_PUBLIC_GLASSBOX_D5D6=on in deploy env + deploy (owner's git/deploy domain).
summary: >
  Final go-live QA gate for Glass Box D5/D6 (owner approved flip-after-QA). Independently verify the FULL
  integrated path (engine → glassBox JSON → frontend) behind NEXT_PUBLIC_GLASSBOX_D5D6: (1) flag OFF = live
  routes byte-identical to today; (2) flag ON renders correctly on the REAL routes — hummus/maadanim are an
  expected no-op (all displayed products unconstrained), vegetable-spreads shows the one real demote
  (pepper-spread → ניתוח חלקי + mapped disclosure lines), null-render parity holds anywhere a withhold shows;
  (3) Content's exact Hebrew via the code→map, no leakage (no raw numbers/engine terms, no intent attribution);
  (4) no regression on other categories; (5) published JSON grades unchanged (FE flag is display-only);
  (6) tsc/lint/build clean. Verdict PASS/FAIL for the flip. Verification only; no code/score change.
---

# TASK-179O — Final go-live QA pass (Glass Box W1)

Part of TASK-179 (Glass Box), Wave 1 go-live. Chain: 179N integration → **179O (this, final QA)** →
owner-approved flag flip. On PASS the orchestrator flips NEXT_PUBLIC_GLASSBOX_D5D6 ON for go-live.
Domain agent proposes RETURNED; this is the authoritative go-live gate.
