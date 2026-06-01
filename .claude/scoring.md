# Bari Scoring Architecture

**Engine:** BSIP2 Prototype v0  
**Algorithm version:** 0.3.1  
**Source:** `C:\Bari\03_operations\bsip2\proto_v0\src\`  
**Last verified:** 2026-05-30

---

## Bari Repository Map â€” TWO SEPARATE LOCATIONS

All scoring, BSIP, and research work in this document lives in the **product / data workspace**: `C:\Bari`.

| Repo | Path | Use for |
|------|------|---------|
| **Product / data workspace** | `C:\Bari` | BSIP scoring assets, Python pipelines, scoring research, CE reports, nutrition docs, category rollout |
| **Website repo** | `C:\bari-web` | Next.js app, components, routes, the frontend JSON the site consumes, lint/build |

- Scoring research, BSIP outputs, CE reports, category rollout â†’ **`C:\Bari`**.
- The scoring engine and pipelines live under `C:\Bari\03_operations\`. The website consumes only the **generated JSON**, copied into `C:\bari-web\src\data\comparisons\`.
- **Never assume `C:\Bari` is the website repo**, and never edit Next.js source here â€” there is none.

---

## BSIP Pipeline Overview

```
BSIP0 â†’ BSIP1 â†’ BSIP2
```

| Layer | Role | Key scripts | Output |
|-------|------|-------------|--------|
| BSIP0 | Scraping + OCR | `bsip0/scrape/`, `bsip0/pipeline/` | Raw HTML/JSON/images per product |
| BSIP1 | Semantic enrichment | `bsip1/core/ingredient_enricher.py` | Canonical JSON per product |
| BSIP2 | Structural scoring | `bsip2/proto_v0/src/score_engine.py` | `bsip2_trace.json` per product |

---

## BSIP0 â€” Extraction Layer

- **Retailers scraped:** Shufersal, Yohananof, Carrefour, Wolt
- **Scraper:** `03_operations/bsip0/scrape/yohananof/` â€” 4-stage: discover â†’ approve â†’ scrape â†’ audit
- **OCR pipeline:** `03_operations/bsip0/pipeline/` â€” Azure-based extractor for physical label images
- **Outputs go to:** `02_products/{category}/observations_bsip0/{retailer}/`

---

## BSIP1 â€” Enrichment Layer

**Primary file:** `03_operations/bsip1/core/ingredient_enricher.py`

Enrichments performed:
- Hebrew ingredient detection (white flour, whole grain, additives, fermentation markers)
- Additive classification and burden counting
- Protein source identification
- Matrix integrity signals (whole grain ratio, fermentation presence)
- BSIP1 trust level assignment (`high`, `medium`, `low`)

**Test suite:** `bsip1/core/test_enricher.py` â€” 64 checks, run with pytest.

**Active runs:**
| Run | Category | Products |
|-----|----------|---------|
| `run_001/output/` | snack_bars | 53 |
| `run_cereals_001/output/` | breakfast_cereals | 45 |
| `run_yogurt_001/output/` | yogurt | 45 |
| `run_milk_002/output/` | milk_and_alternatives | 20 |

---

## BSIP2 â€” Scoring Engine

### Core Files

| File | Role |
|------|------|
| `score_engine.py` | Main scoring engine â€” 10 dimensions, grade, trace |
| `signal_extractor.py` | L1â€“L6 signal extraction layer |
| `matrix_integrity.py` | Matrix Integrity Engine v2 (structural food interpretation) |
| `structural_classifier.py` | Structural Class Classifier v1 â€” A-F soft assignment |
| `nova_proxy.py` | NOVA proxy inference from Hebrew ingredient text |
| `router_v2.py` | Router v2 â€” 3-stage routing (anchor â†’ context-gated signals â†’ resolution) |
| `constants.py` | All thresholds, weights, grade bounds |
| `evaluation_scope.py` | Scope assignment (imported by all batch runners) |
| `input_loader.py` | BSIP1 record loader |
| `trace_writer.py` | BSIP2 trace JSON writer |
| `category_classifier.py` | V1 category classifier (superseded by router_v2) |

### Signal Extraction Layers (L1â€“L6)

Extracted by `signal_extractor.py` before scoring:
- **L1** â€” Observed signals: raw nutrition fields, consistency checks
- **L2** â€” Derived ratios: sugar/carb ratio, sat fat/fat ratio, etc.
- **L3** â€” Ingredient signals: Hebrew term presence flags
- **L4** â€” Additive signals: burden count, specific additive types
- **L5** â€” NOVA proxy signals: processing level inference
- **L6** â€” Matrix signals: whole grain, fermentation, food structure

---

## Scoring Pipeline â€” 6 Stages

### Stage 1 â€” Feature Extraction
50+ analytical features from: nutrition panel, ingredient list, category, regulatory labels. Missing fields recorded; no imputation.

### Stage 2 â€” Dimension Scoring (10 dimensions, each 0â€“100)

| Dimension | Weight | What it measures |
|---|---|---|
| `processing_quality` | 15% (proto v0) | NOVA classification, additive burden |
| `nutrient_density` | 15% | Protein, fiber, micronutrient contribution per 100g |
| `calorie_density` | 15% | Calorie appropriateness for category |
| `glycemic_quality` | 12% | Sugar load, carbohydrate composition |
| `protein_quality` | 10% | Protein quantity and source |
| `additive_quality` | 10% | Artificial stabilizers, emulsifiers, sweeteners |
| `fat_quality` | 8% | Saturated fat proportion, fat source |
| `satiety_support` | 6% | Protein + fiber + food structure |
| `regulatory_quality` | 5% | Israeli red-label warnings |
| `whole_food_integrity` | 4% | Proximity to minimally processed whole food |

**Note:** Weights in `constants.py` are prototype values (sum to 1.0). The methodology doc describes public-facing weights which may differ from current prototype constants. Calibration is a separate phase.

### Stage 3 â€” Guardrail Evaluation

- **Veto rules:** Trans fat above threshold â†’ score floor of 20
- **Hard caps:** Binding upper limits (NOVA 4 â†’ cap, multiple red labels â†’ cap, high sugar â†’ cap, high sodium â†’ cap, additive burden â†’ cap). Most restrictive cap wins when multiple apply.
- **Soft penalties:** Subtractive adjustments for non-hard concerns
- **Floors:** 
  - `NOVA1_SINGLE_FLOOR` â€” single-ingredient NOVA 1 foods
  - `WHOLE_FOOD_FAT_FLOOR` â€” whole-food fat products (nuts, seeds)

Defined in `constants.py`: `PROCESSING_CAPS`, `SWEETENER_CAP_A/B/C`, `TRANS_FAT_VETO_THRESHOLD`.

### Stage 4 â€” Hyper-Palatability Detection

Four combination patterns, each applies a penalty:
| Pattern | Constant |
|---|---|
| Fat-sugar | `HP_FAT_SUGAR_PENALTY` |
| Fat-sodium | `HP_FAT_SODIUM_PENALTY` |
| Refined carb + fat | (carb_fat pattern) |
| Crunch-sweet | `HP_CRUNCH_SWEET_PENALTY` |

**Amplifiers:** chocolate coating, glucose syrup, emulsifiers, flavourings â†’ increase penalty.  
**Relief factors:** whole nuts, whole grains, dates â†’ partial reduction.  
**Family budget:** `HP_FAMILY_BUDGET` â€” cumulative HP penalty cap.

### Stage 5 â€” Concern Coordination

Prevents the same root concern from penalizing the score more than once.

Concern families with budget limits:
- `SUGAR_FAMILY_BUDGET`
- `SODIUM_FAMILY_BUDGET`
- `CALORIE_FAMILY_BUDGET`
- `PROCESSING_FAMILY_BUDGET`
- `FAT_QUALITY_FAMILY_BUDGET`

When multiple rules in the same family fire, the primary signal is kept at full weight; others are demoted to reduced weight.

### Stage 6 â€” Final Resolution

1. Apply all caps (most restrictive wins, with family-specific floors)
2. Apply all penalties (with per-family budget limits)
3. Enforce floors
4. Apply confidence ceiling: `CONFIDENCE_INSUFFICIENT_CEILING`, `CONFIDENCE_LOW_CEILING`
5. Clamp to [0, 100]
6. Convert to grade via `score_to_grade()`

---

## Grades

| Grade | Score range |
|-------|-------------|
| A | 85â€“100 |
| B | 70â€“84 |
| C | 55â€“69 |
| D | 40â€“54 |
| E | 0â€“39 |

---

## Router v2

**File:** `router_v2.py`

3-stage routing replaces the v1 `category_classifier.py`:
1. **Anchor stage** â€” hard product-class anchors (e.g., nuts, seeds, plain yogurt)
2. **Context-gated signals** â€” WFF contamination prevention, beverage gate, dairy-protein suppression
3. **Resolution** â€” final category assignment from signal composite

Validated against:
- `run_regression_check.py` â€” 12-case golden corpus regression
- `run_router_regression.py` â€” 12-case router regression corpus
- `generate_router_validation.py` â€” 163-product validation (82 anchored, 23 changes, 6 unstable)

**Known router gaps (from bread-light stress test):**
- No `bread` or `cracker` archetype in router v2 yet
- WFF contamination: seed-topped bread routes as WFF
- Beverage false-positive risk
- Dairy-protein false-positive risk

---

## Calorie Density Tables (category-relative scoring)

Defined in `constants.py` (`CALORIE_DENSITY_TABLES`):

| Category | Normal range (approx) |
|---|---|
| `whole_food_fat` | 350â€“900 kcal |
| `snack_bar_granola` | 150â€“500 kcal |
| `dessert` / `dairy_protein` | 80â€“350 kcal |
| `beverage` | 10â€“100 kcal |
| `bread` | 200â€“330 kcal |
| `cracker` | 380â€“480 kcal |
| `crispbread` | 300â€“380 kcal |
| `yogurt` | 60â€“250 kcal |
| `cereal` | 300â€“550 kcal |

---

## Israeli Red Label Thresholds

Source: Israeli Ministry of Health (per `constants.py`):
- Sugar: 17.5 g/100g
- Saturated fat: 5.0 g/100g
- Sodium: 600 mg/100g

---

## Batch Runners (Active)

| Script | Category |
|---|---|
| `batch_run_snack_bars_001.py` | snack_bars |
| `batch_run_cereals_001.py` | breakfast_cereals |
| `batch_run_yogurt_001.py` | yogurt |
| `batch_run_milk_004.py` | milk (canonical) |
| `batch_run_maadanim_001.py` | maadanim |
| `batch_run_bread_retail_003.py` | bread retail |

---

## Frontend Dataset Builder

`build_frontend_dataset.py` â€” transforms BSIP2 trace JSONs â†’ consumer-facing dataset JSON.

Output structure (per product):
```json
{
  "id": "...",
  "name": "...",
  "score": 72,
  "grade": "B",
  "insight_line": "...",
  "confidence_level": "full",
  "image_url": "...",
  "ingredients_he": "...",
  "nutrition": { "energy_kcal": ..., "protein_g": ..., ... }
}
```

This JSON is then transformed to `BariProductVM` in the frontend transformation layer (`src/lib/comparisons/`).

---

## Known Constraints and Gaps

| Constraint | Detail |
|---|---|
| No nutrition panel in formula | Score based on ingredients + processing, not caloric macros |
| Fermentation quality scoring gap | Engine cannot distinguish genuine sourdough from industrial sourdough-powder |
| Bread/cracker routing | No dedicated archetypes in router v2 yet |
| Weights are prototype values | `constants.py` weights â‰  methodology doc weights; calibration not complete |
| Confidence ceiling | Low-confidence products cannot score high regardless of signals |

---

## Validation Infrastructure

| Script | Purpose |
|---|---|
| `run_regression_check.py` | Golden corpus regression â€” 12 structural class anchors |
| `run_router_regression.py` | Router v2 regression â€” 12 routing cases |
| `generate_router_validation.py` | 163-product router analysis |
| `generate_router_anchor_audit.py` | Per-term anchor activation + signal-anchor agreement |
| `generate_bread_light_analysis.py` | 9 stress-test analysis outputs (routing, matrix, SC, deception, fiber, seed, fermentation) |

**Run after every engine change:** `run_regression_check.py` and `run_router_regression.py`.

---

## Sources

- `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`
- `C:\Bari\03_operations\bsip2\proto_v0\src\constants.py`
- `C:\Bari\01_framework\bsip2_framework\methodology.md`
- `C:\Bari\REPO_MAP.md`
- `C:\Bari\01_framework\bsip2_framework\signal_system.md`
- `C:\Bari\01_framework\bsip2_framework\docs\beneficial_processing.md`
- `C:\Bari\01_framework\bsip2_framework\validation\golden_products_suite.md`
