---
id: TASK-133C
title: F1 - identity-modulated emulsifier/stabilizer penalty weights
owner: nutrition-agent
status: RETURNED
priority: MEDIUM
created_at: 2026-06-01
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

## Implementation status — 2026-06-01 (structural build COMPLETE)

Report: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md).

- **Key finding:** the F1 *directions are already live*. The EV-003 `sprint1` correction in
  `signal_extractor.py` already tiers emulsifiers (carrageenan/CMC → +2 count = stronger
  penalty; lecithin-only → −1 = relief), and `ADDITIVE_MARKER_PATTERNS` already differentiate
  native `עמילן` (not an additive) from modified `עמילן מוקשה/משונה` (counts as thickener).
- **Built:** 133A's taxonomy now supplies **exact identity** — `tax_emulsifier_concern` /
  `tax_emulsifier_benign` / `tax_native_starch` / `tax_modified_starch` emitted + traced;
  `ADDITIVE_IDENTITY_DELTAS` constants + `_identity_additive_deltas()` hook in the engine,
  **defaulted to neutral (no-op)** so they do **not double-count** `sprint1`. **No new caps.**
  Food-grade vs. degraded carrageenan noted in rationale.
## Return block — 2026-06-01 (proposed RETURNED → Controller to record CLOSED)

DEC-004 **DECIDED**. Calibration finding: F1 deltas set **neutral/0** — the live EV-003 `sprint1`
tiering already realizes F1's directions in proto_v0 (carrageenan/CMC penalized; lecithin-only
carries **no** emulsifier penalty so it is not over-penalized; native vs. modified starch already
differentiated). The taxonomy now supplies exact identity for any future tuning; **no new caps**;
no additional delta warranted (avoids cross-category destabilization + double-count). `processing_analysis.md`
updated (the former flat `Emulsifiers: −6` replaced by identity tiering). Verified: no live-page
score change. Awaiting Central Controller to record CLOSED.
