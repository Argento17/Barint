---
id: TASK-566
title: integrations/clients/http.py shadows stdlib http — silently breaks transformers-dependent gates
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found 2026-07-10 during TASK-557 gate work. Any script doing sys.path.insert(0, 'integrations/clients') then importing torch/transformers fails, because integrations/clients/http.py shadows the stdlib 'http' package. hebrew_grammar_gate.py then raises 'requires transformers and torch'. This silently invalidated an orchestrator grammar-gate run whose summary counted only FLAGGED lines and printed CLEAN over 23 exceptions. Two fixes needed: (1) rename or namespace integrations/clients/http.py so it cannot shadow stdlib; (2) make hebrew_grammar_gate/hebrew_readability callers fail LOUD - a gate that errors must never be reportable as a pass. Root class: a checker whose failure mode is indistinguishable from success.
---

# TASK-566 — integrations/clients/http.py shadows stdlib http — silently breaks transformers-dependent gates

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
