---
name: tzameret-directional-only
description: "Owner directive 2026-06-04 — Tzameret (Israeli MoH צמרת food-composition DB) is DIRECTIONAL ONLY; known data-quality issues, never authoritative / never a value of record"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2940e96d-2a0c-49f2-b3ed-977cc6a3022c
---

Any reference to **Tzameret** (Israeli MoH "צמרת" national food-composition database) must
be treated as **DIRECTIONAL ONLY**. It has known data-quality problems — some entries are
questionable.

**Why:** the data is not reliable enough to anchor decisions; treating it as ground truth
would propagate bad composition values into reasoning/calibration.

**How to apply:**
- It is **NOT authoritative** and is **never the value of record or a calibration anchor**.
- For an actual composition value, prefer **USDA FoodData Central** (`usda_fdc`, lab-measured
  generic) and the product's own **BSIP0 scanned panel**.
- A tzameret-derived number that would inform a scoring decision needs corroboration +
  EV-### + D7 co-sign — tzameret alone is never enough.
- Already propagated (2026-06-04) into: `integrations/clients/tzameret.py` docstring,
  `usda_fdc.py` (hierarchy reworded — FDC is the authoritative-generic ref, tzameret
  directional), `integrations/README.md` (layout + status table + hard-rule #2),
  `.claude/agents/nutrition-agent.md` (row + guardrail), `.claude/agents/data-agent.md`.

Relates to [[external_integration_layer_task170]] and [[agent_capability_equip_2026_06_04]].
