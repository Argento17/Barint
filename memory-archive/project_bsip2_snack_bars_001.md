---
name: project-bsip2-snack-bars-001
description: "BSIP2 snack_bars inaugural run (run_snack_bars_001) — architecture validation results, routing bugs found and fixed, anomaly breakdown, pending gaps"
metadata: 
  node_type: memory
  type: project
  originSessionId: e98ff19c-3c0d-4e26-8e96-38583f14e9c8
---

BSIP2 `run_snack_bars_001` completed 2026-05-19. 53 products, 0 pipeline errors.

**Why:** Architecture validation — not a new scrape. First BSIP2 run for snack_bars. Validates routing, NOVA proxy, caps/floors against 8 architectural questions.

**Score landscape:** B:1, C:12, D:12, E:23, insufficient_data:5. No S or A. Top scorer: date bar (תמר) 70/B. 58% NOVA4. 79% of products capped.

**Routing distribution (post-fix):** snack_bar_granola:36, whole_food_fat:11, cereal:6.

**Two routing bugs found and fixed in `category_classifier.py`:**
1. `plant_milk_name_heuristic` (Fallback C) fired on solid oat bar ("חטיפי פיטנס שיבולת שועל") → misrouted to `beverage`. Fixed by adding snack form indicators (חטיף, חטיפי, ברים, גרנולה, מצופה, דגנים) to `PLANT_MILK_SOLID_EXCLUSIONS`.
2. Name-match on "יוגורט" → misrouted yogurt-flavored wafer bar to `dairy_protein`. Fixed by adding `DAIRY_FLAVOR_SUPPRESSORS` — when "בטעם" precedes a dairy keyword, the weight is reduced to 15% of normal.

**Anomaly engine after fix:** CRITICAL:0, HIGH:40, MEDIUM:22, LOW:0.
- HIGH: 26 HIGH_CONF_LOW_SCORE, 9 ROUTING_UNSTABLE, 4 VANILLA_NOVA4, 1 WFF ingredient contamination
- MEDIUM: 13 DOUBLE_RED_LABEL, 6 WHOLE_FOOD_FAT_NOVA4 (new rule added), 3 NON_FAT_WHOLE_FOOD

**New anomaly rule added:** `WHOLE_FOOD_FAT_NOVA4` (MEDIUM) — fires when whole_food_fat archetype assigned to a NOVA4 product (oxymoronic routing).

**Key architectural findings:**
- Granola instability: Nature Valley Crunchy routes to `cereal` (0.54 conf) not `snack_bar_granola` → gets cap=82 vs 45-68 → inflated C grade vs expected D. Needs `granola_bar` archetype.
- Protein bar: no dedicated routing, Nature Valley Protein lands in whole_food_fat/snack_bar_granola → D grade (correct but category label wrong).
- Fiber laundering: NOT detectable — `ingredients_raw` empty in BSIP1 source (data gap, not BSIP2 gap).
- NOVA dominance: expected and correct for this corpus.
- Cap/floor system: fully explainable, every guardrail named and traceable.

**BSIP1 source:** `C:\Bari\03_operations\bsip1\run_001\output` (53 products).
**Output:** `C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001\products\`
**Analysis:** `C:\Bari\02_products\snack_bars\reports\snack_bars_regression_analysis.md`
**Batch runner:** `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_snack_bars_001.py`

**How to apply:** When starting snack_bars-related BSIP2 work, this is the current baseline. Any future run should use the fixed category_classifier. The `granola_bar` archetype gap is the highest-priority architectural debt before next category expansion.
