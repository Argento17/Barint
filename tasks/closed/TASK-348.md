---
id: TASK-348
title: Phase 2+3: comprehensive malformed-ingredient sweep across all 10 live pages
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified + committed. Broad sweep cleaned 20 malformed ingredient strings
  (juices 13 = panel text PREPENDED; cookies_coffee 4 + snacks 3 = appended); 3 files changed,
  7 already clean. INDEPENDENTLY CONFIRMED: malformed-in-ingredients across all 10 live = 0
  (re-scan on the ingredients field only, not copy fields — the agent's noted rowVerdict/caveat
  marker hits are legit copy, not ingredients); value-level diff on the 3 changed files = 0 score
  / 0 grade changes (tripwire-1 holds); juices[0] now "מיץ תפוזים" (clean). OFF=0. Staging.
  Artifacts: juices_v3 + cookies_coffee_v2 + snacks_v3 + tasks/task348_remediate.py.
---

# TASK-348 — comprehensive malformed-ingredient sweep

CLOSED + verified (malformed→0, scores unchanged, OFF=0) + committed. Dropdown data layer now clean.
