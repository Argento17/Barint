---
id: TASK-133C
title: F1 - identity-modulated emulsifier/stabilizer penalty weights
owner: nutrition-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-01
blocker: "waiting on TASK-133A (named-additive/fragmentation taxonomy)"
depends_on: [TASK-133A]
blocks: []
category_id: null
summary: >
  ADAPT (Med-High). Replace flat emulsifier -6 with identity-modulated weights: carrageenan (E407)/CMC (E466) up; soy lecithin (E322) down toward neutral (corrects current over-penalty); native (unmodified) rice starch excluded from additive burden, modified starch unchanged. Single RCT n=60 -> keep deltas modest; note food-grade vs degraded carrageenan. No new caps (Tension-5 rule budget).
---

# TASK-133C — F1 - identity-modulated emulsifier/stabilizer penalty weights

## Plan of record — Phase C (F1)

Roadmap: [TASK-133_implementation_roadmap.md](../research/TASK-133_implementation_roadmap.md) §Phase C.

- **Code:** replace the flat emulsifier penalty with identity-modulated weights in `constants.py` /
  additive-quality + processing dimensions: carrageenan & CMC up; **soy lecithin down toward neutral**
  (corrects today's over-penalty); native starch out of additive burden; modified starch unchanged.
- **Constraint:** single RCT (n=60) → modest deltas, **no new caps** (Tension-5 rule budget); note
  food-grade vs. degraded carrageenan in the rule rationale.
- **Validation:** lecithin products tick up slightly; carrageenan-heavy (dairy-alt, deli) tick down;
  additive-burden caps (3–4→65, 5+→55) stay stable. Size: S.
- **Calibration sign-off:** [DEC-004](../decisions/decisions.json) gates the penalty deltas.
