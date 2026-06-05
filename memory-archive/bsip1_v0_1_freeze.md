---
name: bsip1-v0-1-freeze
description: "BSIP1 v0.1 freeze location, energy_kj design decision, and final dataset numbers"
metadata: 
  node_type: memory
  type: project
  originSessionId: d768c3ea-08b1-4862-bf0f-b4dc554878f8
---

BSIP1 v0.1 was frozen on 2026-05-17.

**Freeze location:** `C:\Bari\bsip1_concept\freezes\bsip1_v0_1\`

Contains: schemas, config/brand_variants.yaml, core modules, batch_test_001 reports (10 files), 5 sample products + 5 sample audits, README, CHANGELOG.

## energy_kj design decision

`energy_kj` was removed from the compact product (`normalized_nutrition_per_100g`) and from `inferred_fields`. It is stored as `energy_kj_derived` in `audit.energy_normalization` only.

**Why:** BSIP2 must not confuse observed nutrition with derived companion values. energy_kj is a deterministic derivation (kcal × 4.184) — not observed data.

**How to apply:** If BSIP2 ever needs kJ, read it from the audit sidecar. Never re-derive it in BSIP2 without checking the audit first.

## Final dataset numbers (batch_test_001)

- 66 observations total (63 scored, 3 no-barcode excluded)
- 53 canonical products: 10 multi-retailer, 43 single-retailer
- 53/53 schema valid
- Trust: 2 high / 46 medium / 5 low
- High trust: only bsip1_4011800567613 and bsip1_5900020022325

## What is NOT in scope (confirmed at freeze)

- BSIP2 health/nutrition scoring, NOVA, recommendations
- Auto-merging no-barcode products (fuzzy_candidate_queue.json — manual only)
- ML matching, vector search, probabilistic identity resolution
