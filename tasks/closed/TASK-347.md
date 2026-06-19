---
id: TASK-347
title: Phase 2+3 WS-Data remediation: fix parsing gaps for the dropdown (clean malformed, compute rank, re-derive nulls from scrape)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: [TASK-345]
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified (scoped DoD met). INDEPENDENTLY CONFIRMED the tripwire-1 invariant:
  value-level diff of all 10 live JSONs vs HEAD → score changes=0, grade changes=0 (all 10
  tracked; my first check had a Windows backslash path bug giving false "NO-OLD", corrected).
  OFF=0 in products. The 5 audit-scoped malformed cleaned (spot-checked cereals 7297488199590 →
  "אורז לבן (95%), סוכר, מלח", clean). rank/categoryTotal on 407 (cereals[0] rank 1/20). Sugar
  re-derived from raw scrape cereals 19/20 + granola 22/25; sodium granola 5/5 + milk 16/18; the
  rest genuine label gaps (hard_cheeses sugar 26, juices sodium 15, milk sugar 10, 2 milk sodium)
  → stay null per missing-data rule. d4_additives added to milk 18 + juices 21 ([] where no
  additives). Artifacts: 10 JSONs + tasks/task347_remediate.py. Staging only, no push.
  ⚠️ NEW FINDING (out of 347's scope): the audit UNDERCOUNTED malformed — live cookies_coffee +
  snacks also have nutrition-panel text appended to ingredients (cereal-specific markers missed
  them). → broader sweep TASK-348.
---

# TASK-347 — WS-Data remediation

CLOSED + verified (scores unchanged, OFF=0, scoped fixes done) + committed. Broader malformed
sweep (cookies_coffee/snacks panel-in-ingredients) → TASK-348.
