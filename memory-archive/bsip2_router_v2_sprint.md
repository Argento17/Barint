---
name: bsip2-router-v2-sprint
description: "Router v2 hardening sprint — three-stage routing architecture, anchor system, context-gated signals, regression corpus, validation results"
metadata: 
  node_type: memory
  type: project
  originSessionId: 88339fa2-f552-455b-8eed-95c12c9cad01
---

## Router v2 — COMPLETE (2026-05-20)

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\router_v2.py`  
**Drop-in replacement for:** `category_classifier.py` (v1 preserved but superseded)

### Three-Stage Architecture

1. **Stage 1 — Hard Anchor** (`_check_anchors`): Name-only term matching. Settles routing immediately with high confidence. Ordered longest-first so specific beats generic. Exits before signal scoring.

2. **Stage 2 — Context-Gated Signal Scoring** (`_score_signals`): Scope-controlled field access:
   - `name_only` — beverage, dairy: never from ingredient text
   - `name_weighted` — most snack/cereal: 2× name + 0.5× ingredients
   - `context_gated` — WFF nuts/oils: ingredient text only fires when name has WFF identity (not granola/cereal/snack)
   - `full_text` — legacy fallback

3. **Stage 3 — Resolution** (`_resolve`): Hybrid detection, instability flagging, confidence banding.

### Key Mechanisms

**`HARD_ANCHORS`**: 19 terms across cereal, snack_bar_granola, dairy_protein, whole_food_fat, default (bread)

**`ANCHOR_EXCLUSIONS`**: Per-term blocklist. E.g., "שיבולת שועל" suppressed when "חטיף"/"חטיפי"/"ברים"/"משקה" etc. in name. Nut butter anchors suppressed when "מילוי"/"חטיף"/"שכבת" in name (filling ≠ product identity).

**`DAIRY_ANCHOR_TERMS`** + **`DAIRY_FLAVOR_SUPPRESSORS`**: Suppress "יוגורט" anchor when it appears after "בטעם" (flavor descriptor, not product type).

**`_PRIMARY_LIQUID_KW`**: "משקה"/"שתייה"/"מיץ" etc. in name → adds 0.75 boost AND returns immediately from beverage gate (prevents grain signals from outscoring explicit liquid identity).

**Plant-milk brand bypass** (pre-anchor): If brand/name_first ∈ `_KNOWN_PLANT_MILK_BRANDS` AND name has no `DAIRY_ANCHOR_TERMS`, bypass anchor stage and apply 0.75 pre-boost before beverage gate. Handles "אלפרו שיבולת שועל" (oat milk → beverage) without misrouting "אלפרו יוגורט סויה" (soy yogurt → dairy_protein).

### Validation Results (163 products, 2026-05-20)

- Anchor activations: 82 (50%)
- V1→V2 routing changes: 23 (all verified improvements — no regressions)
- Suppression events: 20 products with ≥1 suppressed signal
- Instability flags: 6
- Hybrid products: 3

Key corrections vs v1:
- 8 granola products: whole_food_fat → snack_bar_granola (ingredient nut contamination fixed)
- 2 Nestlé Fitness cereals: snack_bar_granola → cereal (anchor)
- 3 yogurt products: sauce_spread → dairy_protein (anchor)
- Cheerios, whole-grain cornflakes: whole_food_fat → cereal (anchor)

### New Files

| File | Purpose |
|------|---------|
| `router_v2.py` | Main router (drop-in for category_classifier) |
| `run_router_regression.py` | 12-case regression suite |
| `router_regression_corpus.json` | Test corpus (anchors, WFF gating, beverage, dairy) |
| `generate_router_validation.py` | 163-product validation across 4 datasets |

### Reports

- `03_operations/reports/regression/router_regression_001.md` — 12/12 PASS
- `03_operations/reports/router_validation_001.md` — full analysis

**Why:** v1 category_classifier used full-text matching, causing granola products to route to whole_food_fat (ingredient nuts/oils contaminating routing), and plant-milk/yogurt products to route incorrectly. Router v2 is required before bread/crackers category can be added.

**How to apply:** When adding new categories or routing edge cases, update `HARD_ANCHORS`, `ANCHOR_EXCLUSIONS`, and the appropriate signal list in `router_v2.py`. Always re-run `run_router_regression.py` (12/12 PASS required) and `generate_router_validation.py` after any change.
