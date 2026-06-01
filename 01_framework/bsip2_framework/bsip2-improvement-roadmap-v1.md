TASK-016
Status: Complete
Owner: Chief Nutrition Officer

---

# BSIP2 Improvement Roadmap v1

**Date:** 2026-05-30  
**Inputs:** Distortion Registry v1, TASK-006 Distortion Ranking, TASK-011 Nutrition Rulings Classification  
**Scope:** BSIP2 engine only. No BSIP3 redesign. No new philosophy. All items derived from real category execution.  
**Engine location:** `C:\Bari\03_operations\bsip2\proto_v0\src\`

---

## How to Read This Roadmap

Each improvement is ordered by priority. Priority is determined by: (1) live production harm today, (2) scientific integrity breach, (3) implementation cost relative to impact. Dependencies between items are explicit — do not execute out of order where a dependency chain is listed.

**Implementation complexity scale:**

| Level | Definition |
|---|---|
| Low | Single-file change, ≤ 1 sprint, targeted regression only |
| Medium | 2–3 files, 1–2 sprints, subset regression + golden corpus check |
| Medium-High | Multi-file, 2–3 sprints, full golden corpus + category corpus regression |
| High | Multi-sprint, cross-system dependency, full regression required before any publication |

---

## Improvement 01 — Snacks Dataset Reingestion and Confidence Label Correction

**Source:** BEV-056, BEV-066, DIST-005, TASK-006 Priority 3 (supporting)

### What it is

All 18 snack products in the current corpus have null nutritional values. BSIP0 captured packaging images but nutritional content was never extracted into BSIP1 enrichment. As a result, Layers 2 (Nutritional Contribution) and 3 (Metabolic Stability) are inactive for the entire snacks category. Additionally, 11 products carry `confidence: "verified"` labels that are factually incorrect — there is no verified nutritional data to support that label.

This is not a scoring philosophy question. It is a data integrity failure that is live in production.

### Expected impact

- All 18 products receive correct confidence labels (majority will shift from `verified` to `partial` or `insufficient`)
- When Layers 2–3 activate, scores are expected to shift 10–20 points for products where nutritional profile diverges from structural signals
- Date bars that currently score well on structural simplicity alone may score lower when glycemic quality and nutrient density are applied
- Products with genuinely strong nutritional profiles may score higher
- The anomaly of snacks mean score (43.50) ≈ maadanim mean score (43.78) will resolve — these two categories should not produce equivalent distributions

### Categories affected

`snack_bar_granola` — all 18 products in the current corpus

### Dependencies

```
BSIP0 nutritional data extraction for 18 products
    ↓
BSIP1 re-enrichment (ingredient_enricher.py) with nutritional fields populated
    ↓
BSIP2 batch_run_snack_bars_001.py re-execution
    ↓
build_frontend_dataset.py regeneration
    ↓
CE Advisory review of new score distribution before publication
    ↓
Confidence label audit: confirm all 11 previously mislabelled products are corrected
```

### Implementation complexity: Medium

Pipeline work spans BSIP0 through build step but no scoring engine changes are required. The complexity is in data extraction quality and the CE Advisory review of potentially significant grade changes. Estimated: 1–2 sprints including review cycle.

---

## Improvement 02 — Dairy Fiber Formula Normalization

**Source:** BEV-062, DIST-001, TASK-006 Priority 3

### What it is

The nutrient density dimension uses the formula: `0.65 × protein_score + 0.35 × fiber_score`. Dairy products are biologically fiber-free. The formula applies a structural penalty to every dairy product for not containing a nutrient it cannot biologically contain. This is not a threshold calibration question — it is a formula that asks the wrong question of the wrong product class.

The correction: for products routing to `dairy_protein` category, the nutrient density formula should be normalized to protein only: `protein_score` (effectively 100% weight on protein). This removes the fiber penalty without affecting any non-dairy category.

### Expected impact

- Every dairy product increases by 0.84–4.46 final score points (scale depends on protein level)
- Direction is certain: all dairy scores improve
- At the B/C grade boundary (score 70), a 2–4 point correction is grade-determinative
- High-protein dairy products (יופלה GO, skyr, quark, protein yogurts) are most improved — these are the products most penalised by the current formula
- Within-category rankings are preserved (all products are corrected proportionally); cross-category comparisons between dairy and non-dairy become fairer

### Categories affected

- `dairy_protein` — all yogurt, quark, skyr, kefir, cottage cheese products
- `maadanim` — dairy dessert products (all are dairy-based and affected by the same formula)

### Dependencies

```
CNO specifies correction formula (protein-only nutrient density for dairy_protein)
    ↓
score_engine.py: category-conditional formula branch
    ↓
constants.py: dairy protein nutrient density weight parameter
    ↓
Run regression check on dairy subset of golden corpus
    ↓
Grade boundary audit: identify products that cross A/B or B/C boundary post-correction
    ↓
Governance notification for any grade changes before publication
```

No dependency on Improvement 01. Can run concurrently. Must complete before yogurt category launches.

### Implementation complexity: Low

Single-branch formula change in `score_engine.py`. Targeted regression on dairy products only. Estimated: 1 sprint including regression.

---

## Improvement 03 — Router v2 Bread and Cracker Archetypes

**Source:** BEV-064, DIST-003, TASK-006 (monitoring status, but bread corpus is live)

### What it is

Router v2 has no dedicated archetypes for bread or cracker product classes. The confirmed failure mode from the bread-light stress test: seed-topped bread products (sesame challah, sunflower whole grain, multi-seed sourdough) route to `whole_food_fat` because the seed signal overrides the bread classification signal. A seed-topped sourdough at 480 kcal/100g routed to WFF receives more lenient calorie density rules than its correct bread thresholds — potentially scoring 20–30 points higher than analytically valid.

The bread corpus is live in production with 24+ products. Given that seed-topped breads are common in Israeli retail, an unknown fraction of live bread scores may be analytically invalid.

New archetypes required: `bread` (grain-dominant ingredient list, typical calorie range 200–350 kcal/100g, Hebrew bread category markers) and `cracker` (thin-profile grain product, 300–500 kcal/100g range, low moisture).

### Expected impact

- Seed-topped breads currently routed to WFF receive lower scores (5–30 point reduction) when correctly evaluated under bread thresholds
- Cracker products currently falling to `default` receive correct evaluation under cracker-appropriate rules
- WFF category is cleaned of non-WFF products
- The bread category score distribution becomes analytically valid for the full corpus

### Categories affected

- `bread` — particularly seed-topped varieties
- `whole_food_fat` — contamination from misrouted bread products removed
- `cracker` (new routing target) — products currently in `default`

### Dependencies

```
CNO defines bread archetype anchor conditions:
  - Grain-dominant ingredient (flour, whole grain flour ≥ 40% by position)
  - Calorie range 200–350 kcal/100g
  - Hebrew keyword signals (לחם, חלה, שיפון, כוסמין)
CNO defines cracker archetype anchor conditions:
  - Thin-profile grain, 300–500 kcal/100g
  - Low moisture (dry product signal)
    ↓
router_v2.py: add bread and cracker anchors to Stage 1
    ↓
Run router regression suite (run_router_regression.py — must pass 12/12)
    ↓
Run bread-light validation corpus against updated router
    ↓
Audit live bread corpus: identify which products change category
    ↓
BSIP2 re-score of bread corpus under corrected routing
    ↓
CE Advisory review of score distribution changes
```

Must complete before any new bread products are added to the corpus.

### Implementation complexity: Medium

Two new anchor definitions in `router_v2.py`. Risk of new false positives (e.g., grain-based snack bars catching bread anchors) requires careful threshold design. Router regression suite and bread corpus re-score add validation overhead. Estimated: 2 sprints.

---

## Improvement 04 — Category Confidence as First-Class Output Field

**Source:** DIST-006, classification_instability.md, TASK-006 (not ranked — architectural)

### What it is

The most severe distortion in the scoring system is classification instability: the same product scoring 20–40 points apart depending on which category it is assigned to, with no visible signal in the output that category confidence is low. Currently `category_confidence` is computed internally but not written to the BSIP2 trace or the frontend dataset.

This improvement has two phases:

**Phase A (trace surfacing):** Add `category_confidence` and `secondary_category` fields to every BSIP2 trace output via `trace_writer.py`. Add corresponding fields to `build_frontend_dataset.py` output.

**Phase B (severity reduction):** When `category_confidence` is below 0.65, apply category-specific caps at reduced severity — blending the inferred category score with the `default` category score weighted by confidence. Products with `category_confidence` < 0.50 receive `default` category rules only and are flagged as "category uncertain" in trace output.

Phase A has no impact on scores. Phase B changes scores for borderline-classified products.

### Expected impact

- Phase A: every trace record gains a confidence field; operators can identify miscategorized products before publication
- Phase B: products at category boundaries with moderate confidence (e.g., date-nut balls, oat-based snacks) receive scores that reflect classification uncertainty rather than the worst-case harsh category rules
- Reduces the maximum possible miscategorization harm from 30–40 points to approximately 10–15 points for borderline cases

### Categories affected

All categories. Highest impact at boundaries: `snack_bar_granola` / `whole_food_fat`, `beverage` / `dairy_protein`, `cereal` / `snack_bar_granola`.

### Dependencies

```
Phase A:
  trace_writer.py: add category_confidence, secondary_category fields
  build_frontend_dataset.py: propagate fields to frontend JSON
  view-models/index.ts: add fields to BariProductVM if surfacing to UI
  (No scoring changes — Phase A only)

Phase B (after Phase A validated):
  score_engine.py: confidence-weighted category rule application
  constants.py: CATEGORY_CONFIDENCE_THRESHOLD = 0.65
  Run full golden corpus regression
  Audit all products near category boundaries for score changes
```

Phase A does not depend on any other improvement. Phase B should run after Improvement 03 (router archetypes) to avoid compounding category changes.

### Implementation complexity: Medium (Phase A) / Medium-High (Phase B)

Phase A is a trace-writer addition — low risk. Phase B modifies how category rules are applied and requires careful threshold calibration to avoid unintended effects across all categories. Estimated: Phase A = 1 sprint; Phase B = 2 sprints.

---

## Improvement 05 — Structural Emptiness Partial Mitigation (Matrix Poverty Flag)

**Source:** DIST-007, structural_emptiness_concept.md, TASK-006 (monitoring)

### What it is

The calorie density dimension currently rewards low calorie density — which is correct for nutrient-dense low-calorie foods but incorrect for products that are nutritionally absent. A diet mousse at 40 kcal/100g of flavoured water and modified starch receives a high calorie density score for being calorically empty. The dimension is inverted for this class of products.

The matrix poverty flag detects when very low calorie density co-occurs with very low protein, fiber, and fat simultaneously — the signature of structural emptiness rather than genuine nutritional efficiency. When the flag fires, calorie density credit is withheld and replaced with a small negative signal.

Proposed matrix poverty thresholds (CNO to confirm per category):
- < 80 kcal/100g AND < 3g protein AND < 1.5g fiber AND < 1g fat → matrix poverty flag active

### Expected impact

- Structurally empty products (diet mousse, gelatin desserts, flavoured gelatin snacks) score 5–15 points lower
- Genuinely low-calorie nutritious products (plain yogurt ~60–80 kcal, cottage cheese ~80 kcal) pass the protein threshold and are unaffected
- The flag applies in any category where it is triggered; no category-specific exemption

### Categories affected

`dessert` (diet variants confirmed in corpus analysis — TASK-009 identified 12 diet variants in מעדנים at 13.3%). `beverage` when live. Limited effect on `snack_bar_granola`, `bread`, or `dairy_protein` in current corpus.

### Dependencies

```
CNO defines matrix poverty thresholds per category
  (single threshold set vs. category-specific variants TBD)
    ↓
score_engine.py: matrix_poverty_flag detection logic
signal_extractor.py: matrix poverty signals as L2 derived metrics
    ↓
Regression on dessert and beverage product subsets
    ↓
Confirm no false positives on high-scoring whole-food products (plain yogurt, tahini)
```

No external dependency. Can run after Improvements 01–03 are stable.

### Implementation complexity: Medium

Signal detection is a derived calculation (L2) from existing nutritional fields. The risk is false positives on whole-food products with legitimately low calorie density. Threshold calibration requires empirical review of which products are flagged. Estimated: 1–2 sprints including threshold validation.

---

## Improvement 06 — Minimum Sibling Gap Implementation

**Source:** BEV-020, TASK-011 (Under Review — not yet implemented)

### What it is

Products with fewer than 2 structural differences — product families (the GO series, the Milky series, the Danone Pro series) where variants differ by one flavour addition — currently can score within 1–2 points of each other. This creates false precision that implies analytical distinctions that do not exist in the data. The current D-band clustering in snacks (39–47 range with micro-gaps of 1–2 points between similar products) is the documented production instance of this problem.

The minimum sibling gap rule: when two products have the same base ingredient structure and differ only by flavour additions or fat level, the score gap between them must be at least 5 points. If the calculated gap is less than 5, the lower-scoring sibling is reduced to create the minimum separation.

Implementation approach: sibling pair detection in the batch runner using ingredient list similarity scoring; gap enforcement as a post-scoring adjustment recorded in the trace.

### Expected impact

- Eliminates 1–2 point micro-rankings between structurally similar products
- Particularly visible in the GO series (מועשר vs. flavoured variants), Milky series, and Danone Pro series
- Some products in the D-band may shift down 2–4 points to enforce sibling separation
- Sibling gap enforcement is recorded explicitly in the trace — operators can see when it was applied

### Categories affected

`snack_bar_granola` (primary — most severe clustering documented here). `maadanim` (GO series, Milky series, Danone Pro series all present). `dairy_protein` (yogurt variant families when live).

### Dependencies

```
CNO defines structural similarity criteria:
  - Same brand + same base formula = siblings
  - Flavour variant ≠ structural difference
  - Fat-level variant (0.7% vs. full-fat) = structural difference (permitted score gap)
    ↓
batch_runner: sibling pair detection logic
score_engine.py: post-scoring gap enforcement with trace annotation
    ↓
Improvement 01 (snacks reingestion) must complete first
  (sibling detection requires accurate nutritional data for comparison)
    ↓
Regression on sibling-containing corpora (snacks, maadanim)
```

### Implementation complexity: Medium

Sibling detection logic is the harder part (requires robust ingredient fingerprinting). Gap enforcement itself is a simple post-processing step. Must sequence after Improvement 01 to have valid nutritional context for sibling comparison. Estimated: 2 sprints.

---

## Improvement 07 — NOVA Proxy Confidence Weighting

**Source:** BEV-021, BEV-053, cap_taxonomy.md, DIST-006 (NOVA misclassification failure mode)

### What it is

The NOVA 4 hard cap (score ≤ 60) applies at full severity regardless of how confident the NOVA proxy classification is. A product classified as NOVA 4 with 58% confidence faces the same hard cap as a product classified with 95% confidence. This is a binary outcome on an inference with uncertainty.

The improvement applies the NOVA 4 cap as a function of NOVA proxy confidence:
- `nova_confidence` ≥ 0.80: full cap applies (score ≤ 60) — current behaviour
- `nova_confidence` 0.50–0.79: blended penalty — partial cap proportional to confidence
- `nova_confidence` < 0.50: no NOVA-specific cap; processing quality dimension penalty applies normally

This does not change the scientific position (NOVA 4 = concern); it adjusts the cap severity to reflect the analytical certainty of the classification.

### Expected impact

- Products with ambiguous NOVA 3/4 classification (borderline ultra-processed) may score 3–10 points higher at the blended confidence range
- Products with clear NOVA 4 signals (high confidence: artificial flavours + emulsifiers + modified starch + preservatives) are unaffected — they remain capped at 60
- Eliminates the worst-case harm of a confident-but-wrong NOVA 4 classification

### Categories affected

All categories containing NOVA 3/4 boundary products — `snack_bar_granola`, `maadanim`, `bread` (industrial bread). Minimal effect on `dairy_protein` and `whole_food_fat` which are predominantly NOVA 1–2.

### Dependencies

```
nova_proxy.py: confirm nova_confidence is computable and reliable
  (currently computed internally — must verify confidence scale is well-calibrated)
    ↓
score_engine.py: NOVA cap application reads nova_confidence
constants.py: NOVA_CONFIDENCE_FULL_CAP_THRESHOLD = 0.80
    ↓
Validation corpus: 20+ products with known NOVA status for confidence calibration
    ↓
Golden corpus regression + NOVA borderline product audit
```

NOVA confidence values must be validated against the known golden corpus before the blended penalty is applied in production.

### Implementation complexity: Medium

The nova_proxy.py confidence values may need recalibration before this improvement produces reliable results. One sprint for the cap weighting logic; one sprint for confidence validation. Total: 2 sprints.

---

## Improvement 08 — Gradient Caps for Four Cliff-Edge Thresholds

**Source:** BEV-053, cap_taxonomy.md, DIST-008

### What it is

Four hard caps implement scoring cliffs where a difference of 0.1g/100g in a nutrient produces a binary outcome — full cap versus uncapped. These thresholds are gaming surfaces and are scientifically indefensible as hard boundaries for continuous inputs:

| Cap | Current threshold | Gaming exposure |
|---|---|---|
| `HIGH_SUGAR_25G_PLUS` | Cliff at 25g sugar/100g | Products reformulated from 25.2g to 24.8g escape the cap entirely |
| `HIGH_SODIUM_700MG_PLUS` | Cliff at 700mg sodium/100g | Same problem; also distorts condiment evaluation |
| `ADDITIVE_MARKERS_3_PLUS` | Cliff at 3 markers | Removing one additive escapes cap regardless of remaining burden |
| `NOVA_PROXY_4` | Full cap at NOVA 4 | Addressed separately in Improvement 07 |

Each cliff is replaced by a gradient: a smooth penalty curve that begins at a lower threshold, increases continuously, and reaches full cap effect well above the current single threshold.

Proposed gradient parameters (CNO to confirm):
- Sugar: gradient from 18g → full cap effect at 32g
- Sodium: gradient from 500mg → full cap effect at 900mg
- Additive markers: stepped deepening penalty per marker (3 markers = −10pts; 4 = −18pts; 5+ = current BRC-04 cap)

### Expected impact

- Products near current thresholds receive scores proportional to their actual distance from concern thresholds
- Gaming by micro-reformulation to just below a cliff no longer produces a binary score jump
- Most products far above thresholds are unaffected (gradient reaches full cap effect before the range they occupy)
- Some products just above current thresholds may score 2–5 points higher; products further above are approximately unchanged

### Categories affected

Sugar gradient: `snack_bar_granola`, `maadanim`, `dessert`. Sodium gradient: `sauce_spread`, `bread`. Additive gradient: `maadanim`, `snack_bar_granola`. All categories affected to varying degrees.

### Dependencies

```
CNO defines gradient parameters for each of the three caps:
  - Start threshold (where gradient begins)
  - End threshold (where full cap effect applies)
  - Curve shape (linear vs. logarithmic)
    ↓
constants.py: gradient curve parameters replace binary threshold values
score_engine.py: cap application logic reads gradient instead of cliff
    ↓
Full golden corpus regression (all categories simultaneously affected)
    ↓
Category corpus regression for snack_bar_granola, maadanim, sauce_spread
    ↓
Confirm current cap analysis remains directionally valid (no products escape concern classification)
```

This improvement touches all categories simultaneously. Do not run concurrently with Improvement 02 or 03 — isolate changes for regression manageability.

### Implementation complexity: Medium-High

Three caps redesigned simultaneously. Full regression required across all live categories. Gradient parameter design is non-trivial — must confirm gradient products don't escape the intended concern classification range. Estimated: 3 sprints including full regression cycle.

---

## Improvement 09 — Dimension Weight Calibration

**Source:** BEV-065, DIST-004, TASK-011 (BEV-065 classified Structural — Under Review)

### What it is

The 10 dimension weights in `constants.py` are prototype values. The published methodology document uses different weights. No calibration against a validated corpus has been completed. Every score produced by BSIP2 carries an implicit claim that the weights reflect analytical intent — this claim is currently false.

This improvement defines a calibration protocol:
1. Assemble a golden calibration corpus: 40–60 products with CNO-defined intended grades (A through E)
2. Run the engine with current prototype weights; measure deviation from intended grades
3. Iterate weight adjustments until the corpus produces intended grades with ≤ 5 point mean deviation
4. Document the calibrated weights as final; update the methodology document to match
5. Re-run all live category corpora with calibrated weights; audit grade changes

### Expected impact

- Unknown until calibration is run. Could be minor (weights close to intent) or substantial (weights substantially diverge)
- All live category scores are affected simultaneously
- This is the highest-risk improvement for widespread grade changes across all categories
- After calibration, Bari can truthfully claim that published methodology weights match the engine

### Categories affected

All live categories simultaneously: maadanim, bread, snacks, yogurts, milk-comparison.

### Dependencies

```
CNO defines calibration corpus: 40–60 products with intended grades
  (requires product-by-product grade intent from CNO — significant time investment)
    ↓
Calibration study runs (iterative — may require 3–5 rounds)
    ↓
Calibrated constants.py weights approved by CNO
    ↓
Methodology document updated to match calibrated weights
    ↓
Full golden corpus regression + all live category corpora
    ↓
CE Advisory review of all grade changes across all categories
    ↓
Governance notification for all products whose grade changes
```

This improvement must not run concurrently with any other improvement that changes scores. Sequence it last among improvements that affect scores (after Improvements 01–08 are stable). Otherwise calibration will be invalidated by a subsequent change.

### Implementation complexity: High

Research-intensive. The implementation itself (updating `constants.py`) is trivial. The work is in defining the calibration corpus, running the iterative calibration, and managing grade changes across all categories simultaneously. Estimated: 3–4 sprints including CE Advisory review cycle.

---

## Improvement 10 — Fermentation Explicit Positive Signal Credit

**Source:** BEV-023, BEV-069, TASK-011 (BEV-069 classified Structural — Future Work)

### What it is

Fermentation is documented as structurally beneficial processing: protein pre-digestion, anti-nutrient reduction, lactose reduction, B vitamin production. Currently, fermented products benefit implicitly from NOVA 1–2 routing but receive no explicit positive credit. A genuine sourdough bread and a commercial yeast bread are both NOVA 2; the fermentation distinction does not produce a scoring difference.

This improvement adds a fermentation positive signal to the processing quality dimension. When BSIP1 detects confirmed fermentation markers (live yogurt cultures, genuine sourdough-class lactic acid fermentation, kefir fermentation), the processing quality dimension receives a positive adjustment of 5–10 points.

The critical implementation challenge: distinguishing genuine fermentation from industrial sourdough theater ("שמרים תעשייתיים עם מחמצת כשמות שני") requires BSIP1 enrichment to detect fermentation authenticity markers, not just the presence of the word "sourdough" on the label.

### Expected impact

- Genuine sourdough whole grain bread: 5–10 point improvement on processing quality dimension
- Traditional plain yogurt and kefir: incremental improvement (already benefit from NOVA routing; the additional positive signal adds 3–6 points)
- Industrial sourdough-flavored products: no improvement — the detection gate requires authentic fermentation markers
- Creates meaningful score differentiation between genuine sourdough and commercial-yeast bread within the same NOVA class

### Categories affected

`bread` (sourdough sub-group), `dairy_protein` (plain yogurt, kefir — incremental), `maadanim` (naturally fermented dairy products — incremental).

### Dependencies

```
BSIP1 validation:
  ingredient_enricher.py: confirm fermentation marker detection is reliable
  Validate against bread corpus (genuine sourdough vs. industrial)
  Validate against yogurt corpus (authentic cultures vs. label-only claim)
    ↓
signal_extractor.py: new L3 fermentation_confirmed signal
score_engine.py: processing quality positive adjustment when fermentation_confirmed
    ↓
Validation corpus: 20+ products with confirmed fermentation status
    ↓
Golden corpus regression + bread and dairy corpus regression
    ↓
Confirm industrial sourdough products do NOT receive the credit
```

This improvement cannot be executed until BSIP1 fermentation detection is validated — it is gated on upstream enrichment accuracy. It is the only item in this roadmap with a BSIP1 dependency.

### Implementation complexity: High

Two-pipeline dependency (BSIP1 enrichment validation + BSIP2 signal update). The core technical risk is false positives — industrial products falsely credited with fermentation improvement. A validation corpus with authenticated fermentation status is required before any scoring application. Estimated: 3 sprints including BSIP1 validation.

---

## Summary Table

| # | Improvement | Score impact | Categories affected | Key dependency | Complexity |
|---|---|---|---|---|---|
| 01 | Snacks data reingestion + confidence fix | 10–20pts (direction mixed) | snack_bar_granola | BSIP0 data extraction | Medium |
| 02 | Dairy fiber formula normalization | +0.84–4.46pts per product | dairy_protein, maadanim | None | Low |
| 03 | Router v2 bread/cracker archetypes | −5–30pts (seed breads) | bread, WFF, cracker | CNO archetype definitions | Medium |
| 04 | Category confidence output + severity reduction | −0 to −15pts (borderline products) | All | Router stable (after 03) | Med / Med-High |
| 05 | Matrix poverty flag | −5–15pts (empty products) | dessert, beverage | None | Medium |
| 06 | Minimum sibling gap | −2–4pts (lower sibling) | snack_bar_granola, maadanim | Improvement 01 | Medium |
| 07 | NOVA proxy confidence weighting | +3–10pts (borderline NOVA 3/4) | snack_bar_granola, maadanim, bread | Nova confidence validation | Medium |
| 08 | Gradient caps (3 caps) | ±2–5pts (near-threshold products) | All | None; isolate from other changes | Med-High |
| 09 | Dimension weight calibration | Unknown — potentially significant | All | All score-affecting improvements complete | High |
| 10 | Fermentation positive credit | +3–10pts (genuine fermented products) | bread, dairy_protein, maadanim | BSIP1 fermentation detection validated | High |

---

## Sequencing Recommendation

The improvements fall into four execution phases. Do not collapse phases — regression contamination from concurrent score changes makes causation impossible to isolate.

**Phase 1 — Data integrity (no scoring engine changes):**
Improvement 01 (snacks reingestion). Corrects live data errors before any scoring logic changes.

**Phase 2 — Targeted formula fixes (bounded, low regression risk):**
Improvement 02 (dairy fiber) + Improvement 03 (router archetypes). Both are bounded changes affecting specific product subsets. Run concurrently; regression suites are non-overlapping.

**Phase 3 — Scoring logic improvements (broader regression impact):**
Improvement 04 (confidence output + severity reduction), Improvement 05 (matrix poverty flag), Improvement 06 (sibling gap), Improvement 07 (NOVA confidence weighting). Each requires full regression. Run sequentially within this phase — one improvement stable before the next begins.

**Phase 4 — System-wide recalibration (requires all prior phases stable):**
Improvement 08 (gradient caps), Improvement 09 (weight calibration), Improvement 10 (fermentation credit). These affect all categories simultaneously or have upstream dependencies. Run last and with the most comprehensive regression coverage.

---

## Open Issues

**OI-001 — Improvement 09 (weight calibration) is sequenced last but is a prerequisite for scientific integrity claims.**  
Every score produced before calibration carries a methodology discrepancy. The correct scientific position is to complete calibration early. The practical constraint is that calibration will be invalidated by any subsequent scoring change. The roadmap resolves this by sequencing calibration after all other score-affecting improvements are stable. If this sequencing is unacceptable, an alternative is to define the calibration corpus immediately (CNO-only work, no engine changes) and hold it ready for execution at the start of Phase 4.

**OI-002 — Improvement 10 (fermentation credit) is gated on BSIP1 enrichment validation.**  
The timeline for BSIP1 fermentation detection validation is not defined in this roadmap. If BSIP1 validation does not proceed in parallel with Phase 2–3 improvements, Improvement 10 will be indefinitely deferred. CNO should initiate a BSIP1 fermentation validation sprint to unlock this improvement.

**OI-003 — Improvements 02 and 03 both affect the bread category simultaneously.**  
The dairy fiber fix (Improvement 02) does not affect bread; the router archetype fix (Improvement 03) does affect bread. These can run concurrently, but the bread corpus re-score from Improvement 03 should complete first before any CE Advisory presentation of bread category scores. Sequencing: complete Improvement 03 bread corpus re-score, then present combined Improvement 02 + 03 results for dairy and bread categories in a single CE Advisory review.

**OI-004 — Phase 3 has four improvements that each require full regression.**  
Running Improvements 04, 05, 06, and 07 sequentially in Phase 3 means four separate regression cycles. This is the correct approach for traceability but it implies a 4–6 sprint Phase 3. If timeline is a constraint, 04 (confidence output, Phase A only) and 05 (matrix poverty) have the lowest regression scope and can be batched in a single sprint. 06 and 07 should remain separate.

---

## Recommended Next Step

Execute Phase 1 immediately: begin BSIP0 nutritional data extraction for the 18 snack products. This unblocks Improvement 01 and is the prerequisite for Improvement 06 (sibling gap). No scoring engine changes are required — Phase 1 is purely a data pipeline task.

In parallel, CNO should draft the bread and cracker archetype anchor conditions (Improvement 03 prerequisite) and the dairy fiber formula specification (Improvement 02). Both are CNO-only documents — they require no engineering input to prepare and will unblock Phase 2 the moment Phase 1 completes.

---

*TASK-016 — Chief Nutrition Officer*  
*2026-05-30*
