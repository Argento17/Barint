---
name: bsip2-bread-light-sprint
description: "Bread-Light stress test — run_001 (gap inventory) + run_002 (bakery archetypes + semantics layer); 6 reports each; 4 gaps remain"
metadata: 
  node_type: memory
  type: project
  originSessionId: 88339fa2-f552-455b-8eed-95c12c9cad01
---

## Bread-Light Stress Test — Two Runs Complete (2026-05-20)

### run_002 — COMPLETE (2026-05-20)

**Change:** Router v2 bakery archetypes + Bakery Semantics Layer v1 + structural classifier rebalancing
**BSIP2 traces:** `C:\Bari\02_products\bread_light\bsip2_outputs\run_bread_light_002\`
**Reports:** `C:\Bari\02_products\bread_light\reports\run_bread_light_002_*.md` (6 files)
**Scripts:** `batch_run_bread_light_002.py`, `generate_bread_light_analysis_002.py`

**Routing result:** 31/32 products now correctly route to `bread`/`cracker`/`crispbread`.
Only "פצפוצי דגנים פצ'פץ'" stays in `snack_bar_granola` (correct — it's a corn puff snack).

**Score changes vs run_001:**
| Group | Avg v1 | Avg v2 | Notes |
|-------|--------|--------|-------|
| A | 67.8 | 71.8 | Baseline correctly routing |
| B | 64.8 | 65.8 | Wholegrain halo still scoring mid-range |
| C | 65.5 | 64.0 | Seed-halo products scoring slightly lower (correct) |
| D | 70.8 | 71.4 | Fermentation gradient: 79→70→64→63 by authenticity |
| E | 62.8 | 64.0 | Engineered wellness correctly B-D |
| F | 43.4 | 42.7 | Hyper-palatable correctly low |

**Bakery Semantics Layer v1 validated:**
- `bakery_semantics.py`: flour hierarchy (FQC 1-5), fermentation quality (5 tiers), fiber source, seed role
- `grain_structure_score` (0-100): GSS=100 for genuine whole-grain sourdough, GSS=16 for isolated-fiber refined crackers
- `structural_classifier.py`: `_apply_bakery_rebalance` corrects NOVA3 gravity bias for bakery products

**Remaining gaps (priority order):**
1. **Fiber source discount not in score_engine** — isolated fiber crackers still score B (GSS=16 but no score penalty). Needs −10 to −15 to `glycemic_quality` and −5 to −8 to `nutrient_density` when `fiber_source_quality=isolated`.
2. **Undeclared sourdough % edge cases** — `מחמצת + שמרים` without declared % → `mixed_industrial` (may overstate for low-% sourdough flavor additions)
3. **FQC position-only proxy** — without declared flour %, position proxy is the only discriminator
4. **Multigrain label vs actual grain count** — engine can't distinguish 5% rye from 50% rye

---

## run_001 — Gap Inventory (2026-05-20)

**Purpose:** Controlled ontology pressure test for bread/cracker category. NOT a full bakery expansion.
**Products:** 32 synthetic BSIP1-format products across 6 stress groups (A-F)
**BSIP1 source:** `C:\Bari\03_operations\bsip1\run_bread_light_001\output\`
**BSIP2 traces:** `C:\Bari\02_products\bread_light\bsip2_outputs\run_bread_light_001\`
**Reports:** `C:\Bari\02_products\bread_light\reports\` (9 files)

### Stress Groups

| Group | Focus | Count |
|-------|-------|-------|
| A | Simple baselines — clean reference anchors | 5 |
| B | Wholegrain halo — grain tokens + isolated fiber | 6 |
| C | Seed halo — surface seeding on refined matrix | 5 |
| D | Sourdough spectrum — genuine → industrial theater | 5 |
| E | Engineered wellness — protein/keto/fiber assembly | 6 |
| F | Highly processed / kids — hyper-palatable, structural void | 5 |

### Scripts

| File | Purpose |
|------|---------|
| `create_bread_light_corpus.py` | Generates 32 BSIP1 JSON product files |
| `batch_run_bread_light_001.py` | Runs BSIP2 scoring on all 32 products |
| `generate_bread_light_analysis.py` | Generates 9 analysis reports |

### Key Findings (Ontology Gaps)

1. **No bread/cracker router archetype** — all 32 products disperse across: `default` (38%), `whole_food_fat` (34%), `snack_bar_granola` (12%), `cereal` (6%), `dairy_protein` (6%), `beverage` (3%).

2. **WFF contamination** — seeds/nuts in ingredient list trigger `whole_food_fat` routing even when seeds are position 4-7 (minor ingredient). Bread products cannot escape WFF signal without a dedicated archetype.

3. **Beverage false positive** — rice cakes ("עוגיות אורז ללא מלח") routed to `beverage` via `plant_milk_name_heuristic` false positive on "אורז" (rice). Fix: add "עוגיות"/"קרקר"/"לחם" exclusion to plant-milk bypass when product name contains solid-food signal.

4. **Dairy-protein contamination** — protein crackers with pea/whey isolate route to `dairy_protein`. Protein signal category-crosses when no bread archetype exists to absorb it.

5. **Fermentation ambiguity** — engine detects "מחמצת" token but cannot distinguish:
   - Genuine live sourdough (מחמצת חיה, no commercial yeast)
   - Traditional sourdough (מחמצת + no שמרים)
   - Industrial sourdough-style (מחמצת מגובשת 2% + שמרים = commercial yeast does leavening)
   - Sourdough theater (name only, no ingredient)
   **Recommended fix:** flag `fermentation_quality=mixed` when מחמצת + שמרים co-appear; `fermentation_role=flavor` when sourdough ingredient <10% by weight.

6. **Fiber laundering** — engine detects isolated fiber markers (inulin, psyllium) in `extracted_matrix_markers` but does NOT penalize the combination of high-fiber claim + isolated source + refined flour base. Group B products score higher than structural integrity warrants.

7. **Structural class** — classifier returns D for most bread products (correct), B for genuine sourdoughs (correct), A for rice cakes (NOVA 1 floor drives this). Works but has no bread-specific interpretation context.

### Score Range by Group

| Group | Avg Score | Range | Notes |
|-------|-----------|-------|-------|
| A | 67.8 | 36-85 | Wide spread — baseline salty cracker scored 36 (WFF routing) |
| B | 64.8 | 53-76 | Wholegrain halo products correctly scored mid-range |
| C | 65.5 | 52-81 | Nordic crispbread scores A (genuine seeds/rye), superfood cracker C |
| D | 70.8 | 62-79 | Fermentation gradient works despite engine ambiguity (17pt spread) |
| E | 62.8 | 49-71 | Keto bread scores D (NOVA 4 correct), protein crackers B |
| F | 43.4 | 29-60 | Kids/hyper-palatable correctly scored low |

### What to do next for bread expansion

1. Add `bread` and `cracker` archetypes to `router_v2.py` HARD_ANCHORS
2. Add WFF context gate for bread: seed signals suppressed when bread/cracker anchor present
3. Add "אורז" exclusion to plant-milk bypass (solid-food name suppressors)
4. Enrichment: add fermentation_quality co-occurrence check (מחמצת + שמרים = mixed)
5. Scoring: fiber source quality discount when extracted_matrix_markers + high fiber + refined flour

**Why:** Router v2 and matrix integrity engine were designed without a bread/cracker archetype. The stress test corpus exposes exactly where the current system struggles before committing to a real bread dataset.

**How to apply:** When bread expansion is started, use these reports as the pre-existing gap inventory. The 32 products in `run_bread_light_001` serve as a regression corpus for bread routing and matrix integrity.
