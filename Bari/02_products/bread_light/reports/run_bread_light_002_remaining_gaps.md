# Bread-Light — Remaining Ontology Gaps After run_002

**Date:** 2026-05-20

## Gaps Resolved in run_002

| Gap | Resolution |
|-----|-----------|
| No bread/cracker/crispbread routing | Router v2 adds 3 bakery archetypes with hard anchors |
| WFF contamination from seeds in ingredients | WFF context gate extended with bakery exclusion list |
| Rice cake → beverage false positive | `עוגיות` added to solid-food exclusion |
| Dairy-protein contamination (protein crackers) | Anchors fire before protein signals |
| Fermentation ambiguity (all מחמצת = same) | `classify_fermentation_quality` adds 5-tier discrimination |
| Structural class misread for bakery products | `_apply_bakery_rebalance` corrects NOVA3 gravity bias |

## Gaps Remaining After run_002

### Gap 1: Fiber Laundering — Score Engine Not Yet Updated

**Status:** Detected but not penalized.

The Bakery Semantics Layer correctly classifies fiber source quality:
- Products with isolated fiber (inulin, psyllium) get `fiber_source_quality=isolated`
- The `grain_structure_score` correctly reflects this (GSS=16 for isolated-only products)

**What is NOT happening:** The score engine does not yet apply a fiber source discount
to the `glycemic_quality` or `nutrient_density` dimensions based on fiber quality.

**Affected products (fiber_source_quality=isolated):**

| Product                          | Score | Grade | FQC | GSS  | NOVA |
|----------------------------------|-------|-------|-----|------|------|
| קרקרים "מולטיגריין" עשיר בסיבים  | 68.1  | B     | 5   | 16.0 | 3    |
| קרקר "בטא-גלוקן" תומך בלב        | 65.8  | B     | 5   | 16.0 | 3    |
| קרקר "סיבים+" אינולין וסיליום    | 67.0  | B     | 5   | 16.0 | 3    |
| לחם "ללא גלוטן" עמילן תפוחי אדמה | 52.3  | C     | 5   | 16.0 | 3    |
| לחם "קטו" דל פחמימות             | 49.0  | D     | 3   | 41.0 | 4    |

**Recommended fix:** In `score_engine.py`, when `bakery_semantics.fiber_source_quality=isolated`:
- Apply a −10 to −15 point discount to `glycemic_quality` dimension score
- Apply a −5 to −8 point discount to `nutrient_density` dimension score
- Add a note to `score_notes`: `fiber_source_discount: isolated fiber, not structural grain`

### Gap 2: Sourdough + Undeclared Percentage = Overestimated Fermentation

**Status:** Partially resolved; edge cases remain.

When a product contains both 'מחמצת' and 'שמרים' but does not declare the
sourdough percentage, `classify_fermentation_quality` assigns `mixed_industrial`
(partial benefit). For products where commercial yeast clearly dominates and
sourdough is a trace flavor ingredient, this overstates the fermentation quality.

*No ambiguous fermentation cases in current corpus.*

### Gap 3: FQC Position-Only Proxy for Mixed Flour Products

**Status:** Known limitation — percentage data not available for synthetic corpus.

When declared flour percentages are absent, `interpret_flour_hierarchy` uses ingredient
position as a proxy (first flour = dominant). This is a reasonable heuristic but
can misclassify products where the second flour is declared at a high percentage.

For a real bread corpus, declared percentages would be available for most products
and the percentage-based branch of `interpret_flour_hierarchy` would activate.

### Gap 4: 'Multigrain' Label vs Actual Grain Count

**Status:** Not addressed in run_002; needs enrichment.

- **קרקרים "מולטיגריין" עשיר בסיבים**: FQC=5, score=68.1
- **קרקרים "5 דגנים" ושיפון**: FQC=3, score=63.4
- **לחם "7 דגנים" תעשייתי**: FQC=3, score=53.0

Products claiming 5-7 grain types typically have refined wheat as the dominant flour
with small amounts of each 'grain' added for label diversity. The current engine cannot
count distinct grain types or distinguish 5% rye from 50% rye.

### Gap 5: Score Engine Not Bakery-Aware for Calorie Density

**Status:** Partially addressed via calorie density tables; needs validation.

Router v2 now correctly routes to `bread`/`cracker`/`crispbread`, and `constants.py`
has dedicated calorie density tables for these categories. However, the score engine
has not been updated to use `bakery_semantics` context when computing dimension scores.

Specifically: a cracker with FQC=5 (pure refined) and GSS=16 should score lower on
`processing_quality` than the current NOVA 3 flat assignment suggests.

## Priority Ranking for Next Sprint

| Priority | Gap | Estimated Impact |
|----------|-----|-----------------|
| 1 | Fiber source discount in score_engine | B→C for 3-5 isolated-fiber products |
| 2 | Bakery-aware score engine context | FQC signal propagation to processing_quality |
| 3 | Percentage-absent fermentation disambiguation | mixed_industrial → flavor_only edge cases |
| 4 | Multigrain grain count enrichment | minor; requires real corpus data |