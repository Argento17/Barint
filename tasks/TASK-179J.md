---
id: TASK-179J
title: Glass Box W1 go-live — Product locks final D5/D6 thresholds + accepts WARN-2
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179I]
blocks: []
category_id: null
roadmap_impact: true
work_type: decision
close_reason: >
  Thresholds LOCKED final (−10/−20/0 · NULL_FLOOR=30 · DEMOTE_CEILING_BOUND=60), no adjustment — Product
  verified against raw pilot JSON (of 32 maadanim withholds only 1 was a genuinely-graded product going null;
  31 already-ungraded relabels; zero promotions; EV-036 kept 163/200 unchanged). Nutrition co-sign does NOT
  re-open. WARN-2 ACCEPTED on the record (4 hummus 72–75/B + 1 maadanim 45/D → לא נוקד = honest, never "fail").
  Verdict GO-WITH-CONDITION: C1 = לא נוקד wording + null-render parity (Content 179K done; Frontend confirms);
  C2 = Data fixes WARN-1 (Proof B wrong example SKU). Production flag-flip = owner's final call (Product
  recommends flip). Memo: 01_framework/glass_box/w1_golive_threshold_lock_v1.md.
summary: >
  Go-live gate: Product reviews the real pilot diff and LOCKS the final D6 numbers (demote −10/−20,
  NULL_FLOOR=30, DEMOTE_CEILING_BOUND=60) as final or adjusts them, and formally ACCEPTS (or rejects)
  WARN-2 — flag-ON removes published-equivalent grades from real pilot products (4 hummus B→לא נוקד,
  1 maadanim D→לא נוקד). Authorizes the flag-ON go-live posture. Decision deliverable; no code.
---

# TASK-179J — Product locks thresholds + accepts WARN-2 (Glass Box W1 go-live)

Part of TASK-179 (Glass Box), Wave 1 go-live. Inputs: pilot proofs + QA report
(`03_operations/bsip2/proto_v0/reports/glass_box/`, `03_operations/qa/reports/qa_glassbox_d5d6_w1.md`).
Domain agent proposes RETURNED; the flag-ON flip itself remains the owner's final call.
