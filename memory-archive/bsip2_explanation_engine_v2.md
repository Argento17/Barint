---
name: bsip2-explanation-engine-v2
description: Explanation engine v2 spec and implementation status for snack bars; 9 banned phrases; all 18 products rebuilt against real BSIP2 trace data
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

All 18 snack bar explanations rebuilt on 2026-05-29 against real BSIP2 trace data.

**Why:** Prior explanations described product-type patterns, not individual products. 22% were Generic, 12% Unsupported/Misleading, 44% Plausible. Primary failure: genericity.

**Status:** COMPLETE — `snacks_frontend_v2.json` updated. Zero banned phrases. All insightLines contain specific ingredient percentages or g-values.

## Core v2 Rules

**Six required questions per explanation** (in `explanation_engine_v2.md`):
1. Most specific structural fact (ingredient name + %)
2. Most specific limiting nutritional fact (g value + category comparison)
3. Sibling comparison ≥5 points (required when same NOVA tier)
4. What would consumer most likely be wrong about
5. Claim vs composition gap (if name/label makes a claim)
6. Single change that most improves score

**9 banned phrases** — all prohibited, no exceptions:
עיבוד מרבי | בסיס מהונדס | ריבוי ממתיקים | מיצוב פיטנס | מוצר מעובד מאוד | בעיית סוכר | חלבון נמוך | מרכיבים רבים | ציון בסיסי

## Factual Corrections Made During Rebuild

- **snk-001**: ingredient count corrected 4→3 (no cacao, no coconut in actual product: תמרים 76%, מחית שקדים 22%, שקדים טחונים)
- **snk-011 & snk-012**: removed false "סוכר מוסף" claim — both products have zero added sugar; all sugar from dates and raisins
- **snk-015**: ingredient count corrected 5→4 (תמרים, חמאת בוטנים, בוטנים, מלח)
- **snk-005**: corrected description from "קמח + סירופ כבסיס" to reflect actual first ingredient: חיטה מלאה 38.3%
- **snk-016**: removed "מיצוב פיטנס" from positiveSignals (was a banned phrase in a positive slot)

## Key Structural Finding (snk-011, snk-012)

Products containing only natural flavoring ("חומרי טעם וריח טבעיים") with otherwise clean ingredient lists receive NOVA4 classification solely from that one marker. This is architecturally correct but counterintuitive — worth noting in consumer-facing disclosures.

## Production Engine Confirmed

The BSIP2 trace data comes from `C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products\<barcode>\bsip2_trace.json`. These are manual CE traces (proto_v0 format), not the Python prototype. Trace files contain real ingredient lists, nutritional data, NOVA evidence, caps applied.

**How to apply:** When writing future explanations for any category, source all numerical claims from the bsip2_trace.json `L1_observed_signals.ingredient_list` and nutrition fields. Never write ingredient claims without trace verification.
