---
name: bsip1-trust-layer
description: "BSIP1 trust scoring design — observation quality + canonical reliability scoring, weighting model, score ranges"
metadata: 
  node_type: memory
  type: project
  originSessionId: d768c3ea-08b1-4862-bf0f-b4dc554878f8
---

BSIP1 has a deterministic, explainable data reliability scoring layer (NOT food quality or health scoring).

## Two-level scoring model

**Observation trust** (`core/trust.py: score_observation_trust`):
- Scored per BSIP0 observation before any merging
- Max 1.00 from 5 weighted categories:
  - Barcode quality: 0.20 (visible GS1 > product_page 13-digit > inferred > internal > absent)
  - Scrape mode: 0.20 (product_page=0.20, shelf_card_only=0.02)
  - Nutrition quality: 0.25 (full + explicit per_100g=0.25, down to absent=0.00)
  - Ingredient quality: 0.20 (clean=0.20, malformed=0.12, truncated=0.10, corrupted=0.04, absent=0.00)
  - Presence signals: 0.15 (image=0.06, allergens=0.05, price=0.04)
- Stored in audit sidecar `retailer_observations[].observation_quality_score/level/signals`

**Canonical trust** (`core/trust.py: score_canonical_trust`):
- Base = mean of observation trust scores
- Post-merge adjustments (signed, documented in module constants):
  - Positive: multi_source_confirmed_gs1 (+0.10), gs1_single_source (+0.05), nutrition_consistent (+0.05)
  - Negative: single_source (-0.05), nutrition_warnings (-0.05), nutrition_suspicious (-0.12), inferred_barcode (-0.03), internal_id_barcode (-0.05), absent_barcode (-0.08), corrupted_ingredients (-0.06), missing_ingredients (-0.05), unresolved_conflicts (-0.12), low_identity (-0.08)
- Levels: high≥0.75, medium≥0.50, low<0.50
- Stored in product: `canonical_trust_score`, `canonical_trust_level`, `canonical_risk_flags[]`

## Barcode validation statuses (validators.py)
`confirmed_gs1` | `invalid_checksum` | `inferred_from_text` | `retailer_internal_id` | `short_ean` | `weak_numeric_identifier` | `absent`
- `invalid_checksum` checked FIRST for 12/13/8-digit barcodes — overrides multi_source/gs1_image_sourced.

## High trust cap (trust.py score_canonical_trust)
After computing level from score, high is further restricted: requires confirmed_gs1 OR observation_count>=2, AND ingredient not corrupted/malformed, AND nutrition not warnings/suspicious. Single-source + inferred-barcode products are always capped at medium regardless of score.

## Current dataset results (batch_test_001, 53 products, 66 obs total / 63 scored / 3 excluded)
- 2 high (3.8%), 46 medium (86.8%), 5 low (9.4%)
- Average: 0.765, range 0.03–1.0
- High-trust products: only bsip1_4011800567613 and bsip1_5900020022325 (multi-source, confirmed_gs1, clean, consistent)
- Top risk flags: single_source_only (43), inferred_barcode_only (39), nutrition_data_absent (5)
- Excluded obs: 3 no-barcode Carrefour private-label -> fuzzy_candidate_queue.json only

## Key constraint
Trust weights are module-level constants in `core/trust.py` — change there to retune without touching logic.

**Why:** trust is data reliability ONLY. Low calorie density, unusual product names, regional brands — none of these lower trust. Only structural/observability signals count.

**How to apply:** Future merger field selection should prefer higher observation_quality_score observations when canonicalizing conflicting values (not yet implemented — framework is established first).
