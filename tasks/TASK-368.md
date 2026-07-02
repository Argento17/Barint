---
id: TASK-368
title: D4 Glass Box headline-score ACTIVATION impact analysis (owner go/no-go prerequisite)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-21
depends_on: [TASK-364]
blocks: []
category_id: null
summary: >
  Owner wants to pursue activating the D4 additive layer into the headline score (currently annotate-only/presentation-only by design). Tripwire-1: published scores would move. Deliverable = impact analysis ONLY, publishes nothing: contested-additive exposure surface across all 12 live corpora + candidate penalty design + marginal-delta-score simulation net of NOVA/existing additive signals + prerequisite gates (TASK-179X engagement gate). Owner decides actual flip after numbers.
---

## Analysis DELIVERED (2026-06-21) — awaiting OWNER go/no-go (tripwire-1)
Script: `tasks/task368_d4_impact_analysis.py` (read-only, published nothing). Key numbers (trace-derived from 15 live frontend JSONs, 555 products):
- **74/555 (13%) carry ≥1 contested additive**; concentrated in cakes_cookies (51), cheese_spreads (10), cookies_coffee (10). 10 of 15 categories = 0.
- **60/74 (81%) are ALREADY NOVA-4** → D4 scoring would mostly DOUBLE-COUNT the processing cap, not add new discrimination. Only 13 NOVA-3 products get genuine new signal.
- **Grade blast radius tiny:** 4–5 of 555 products change grade across all 3 penalty designs (bounded −3/−5/−8 caps). Option C (tier-weighted + cosmetic_mup) most targeted.
- **E300/E330 scoring would add 118 products** (mostly hummus/bread) at LOW confidence = noise, not signal.
- **BLOCKING prerequisite: TASK-261 (EV-051 double-count boundary / Product D7) is IN_PROGRESS** — must close first so D4's marginal contribution is provable net of NOVA+EV-045. TASK-179X engagement gate = CLOSED by owner override (debt carried).
- **Finding (separate): constants.py ↔ library SYNC GAP** — E471 is `likely-neutral` in constants.py but `contested` in the library (EV-061 D7 2026-06-15); E300/E330 still `functional` in constants.py (library=contested EV-101). Needs a sync task before any D4 surfacing.

**Orchestrator recommendation to owner: DEFER D4 scoring activation** (keep annotate-only). Mostly double-count, tiny blast radius, blocked by TASK-261, E300/E330 add noise at LOW confidence. If GO later: close TASK-261 first → Option C with a combined NOVA-4 cap → exclude E300/E330 until 2028 replication. Status stays IN_PROGRESS pending owner decision.

# TASK-368 — D4 Glass Box headline-score ACTIVATION impact analysis (owner go/no-go prerequisite)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
