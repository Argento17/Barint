# D6 Ratification — Shadow Run Open Decisions (OD-1 through OD-4)
**Proposal Class:** D6 (Nutrition Agent — design ratification)
**Required co-sign:** Product Agent (D7) on all four ODs before Data Agent may implement
**Task:** TASK-395
**Date authored:** 2026-06-25
**Status:** D6 RATIFICATION — design only. No engine code changed. No scores changed.
**Depends on:**
- `shadow_run_plan_v1.md` (Part A, OD-1..OD-4 — authored by Data Agent)
- `target_scoring_logic_spec_v1.md` (§2 NOVA replacement + §2.3 combining formula)
- `matrix_signal_redesign_v3.md` (v5.1 signal, NC-2 confirmed)

---

## Preamble

The four open decisions below are **shadow-run design values only**. They govern the BSIP_DECHAIN_V1 candidate engine that runs behind a default-OFF flag. No published score changes until the owner reviews the movement table and gates a deploy. Product Agent D7 co-signs after this ratification; owner reviews results before any deploy. I am not self-certifying these as final production values — the shadow run is explicitly designed to generate the empirical distribution that will let us calibrate further.

Each ratification entry states: the decision, my verdict (RATIFY or REVISE), the value I am confirming or proposing, the nutritional justification, expected directional effect on scores, and honest confidence labeling.

---

## OD-1 — Flat Per-Additive Penalty (Component A)

**Question:** When `BARI_D4_SCORE_V1` is off, what flat penalty per additive marker should Component A use in `processing_load_score = max(0, 100 − additive_count × P)`, clamped [10, 95]?

**Recommended by Data Agent:** P = 14

### Ruling: RATIFY — P = 14

**Justification:**

The flat penalty of 14 is the correct value for this shadow run's purpose, with one important precision note on what it is and is not.

**What P = 14 is:** a corpus-calibrated interim approximation of the identity-differentiated tier penalties (20/15/8/3) that will activate when BARI_D4_SCORE_V1 is on. At P = 14, the flat penalty is roughly the weighted average of the tier distribution across a realistic Israeli retail ingredient set, where most additive markers in NOVA-4 products fall into Tier 2 (moderate-concern synthetics: emulsifiers, stabilizers, flavor carriers) rather than Tier 1 (contested high-risk) or Tier 3 (plant-derived prebiotics). P = 14 ≈ 0.70 × 15 + 0.30 × 8 — a reasonable center-of-mass for a typical processed-food additive profile. Evidence tier for this approximation: **Corpus-fit** (not literature-derived at this precision).

**Benchmark check on the anchor cases Data Agent cites:**

- 3-additive product: `100 − (3 × 14) = 58` → processing_load_score = 58. Combined with a neutral matrix score (Component B ≈ 50): combined_pre_nova = 0.60 × 58 + 0.40 × 50 = 54.8. After NOVA-4 high-confidence modifier (−10): candidate_processing_quality ≈ 45. This is directionally correct. A product with 3 additives and NOVA-4 classification should score in the low-to-mid C range on this dimension, not in D as the old step-lookup produced, and not in B as a NOVA-2 misclassification would give. The continuous signal does what it is supposed to do.

- 5-additive product: `100 − (5 × 14) = 30` → clamped to 30 (below the [10, 95] clamp's relevant bound). Combined with neutral matrix: combined_pre_nova = 0.60 × 30 + 0.40 × 50 = 38. After NOVA-4 modifier: ~28, clamped to the N-3 interim cap floor before any other guard. This is aggressive — a 5-additive product lands solidly in D to E territory on processing_quality, which correctly reflects a heavily additive-loaded product. However, I note that for products where the 5 additives are all low-risk (e.g., citric acid, lactic acid, ascorbic acid, natural color, acidity regulator), P = 14 is punishing too hard relative to the eventual D4 calibration (where all 5 would be Tier 4 at 3 points each → `100 − 15 = 85`). This is the expected cost of the flat fallback. The shadow run will make this visible in the top-movers table, and it is a finding we want to see — it confirms the case for BARI_D4_SCORE_V1.

**Why not lower (P = 10)?** P = 10 produces a 3-additive processing_load_score of 70 and a 5-additive score of 50. Combined with a neutral matrix score and NOVA-4 modifier, a 5-additive NOVA-4 product lands around 44 on processing_quality. This is too permissive: the signal loses most of its force against the 5+ additive products that the P-1/P-2 caps were designed to catch. The shadow run needs the candidate engine to demonstrate it can hold ground without the caps, not to soft-pedal the signal.

**Why not higher (P = 18)?** P = 18 produces a 3-additive score of 46, approaching near-D territory on processing_quality alone before the matrix and NOVA modifier have had any say. For products with 3 modest additives (e.g., emulsifier, preservative, color), this is over-penalizing relative to the evidence. The evidence-backed tier hierarchy says only Tier 1 additives warrant the 20-point penalty; treating every additive at near-Tier-1 levels distorts the signal.

**P = 14 is also coherent with the sensitivity analysis offer in OD-1:** I do not require the harness to run a sensitivity table at this stage. P = 14 is the right single value for the shadow run. If the movement table shows systematic surprises (large movers in categories with mostly low-risk additives), we adjust P for Stage 1 with the full D4 identity differentiation. That is the correct sequencing.

**Expected directional effect:**
- Products with 0 additives: processing_load_score = 95 (clamped max). No change from products already at max.
- Products with 1–2 additives: small reduction from max, moderate scores (72–86). Mild downward pressure.
- Products with 3–4 additives: moderate depression (44–58 before matrix/NOVA). Meaningful downward displacement for the "borderline-processed" products.
- Products with 5+ additives: strong depression (≤30 before matrix, effectively D-range on this dimension). Will interact with N-3 interim cap (68) and the composite guardrails.
- Products with missing ingredient text (Component A only fallback): additive_marker_count = 0 → processing_load_score = 95. This is intentionally permissive for the fallback path; the MD-2 pessimistic imputation (category p75 additive count) is not yet active in this shadow run, so missing-ingredient products will show an artificially high Component A. The shadow run should flag these as a coverage gap.

---

## OD-2 — Component A / Component B Blend Weights (0.60 / 0.40)

**Question:** Confirm or modify the 0.60 / 0.40 split between Component A (additive load) and Component B (matrix structure) in `combined = 0.60 × processing_load_score + 0.40 × matrix_score`.

**Recommended by Data Agent:** 0.60 / 0.40 as in target spec §2.3.

### Ruling: RATIFY — 0.60 Component A / 0.40 Component B

**Justification:**

The 0.60/0.40 split is nutritionally defensible and correctly reflects the relative precision of the two signals at this stage of the engine's development.

**The case for additive load as the larger driver (0.60):**

Component A (additive count) is directly and precisely label-observable. The additive_marker_count signal is already in signal_extractor.py, is QA-verified, and has a well-characterized precision boundary: if the ingredient text names an additive, we detect it; if it uses an obscure synonym, we miss it, but the false-negative rate is bounded by the lexicon coverage we have already validated. The relationship between additive count and processing degree has solid evidence support: additive count is a validated proxy for industrial processing intensity across the NOVA literature (Monteiro 2019; the EPIC-Oxford and NutriNet-Sante cohorts where additive count correlated with UPF classification accuracy). Evidence tier for additive count as a processing signal: **Moderate to Strong (direction); Corpus-fit (the linear-penalty parameterization).**

**The case for matrix signal as the meaningful but non-dominant component (0.40):**

Component B (matrix balance) adds genuine structural information that additive count cannot capture: the clean-label refined-starch product. A product made from refined flour, sugar, and palm oil with zero additives scores 95 on Component A but should not score 95 on processing_quality. Component B correctly pulls it toward 10–20 (three refined markers, no whole-food markers → matrix_score ≈ 14 per target spec §2.4). At 0.40 weight, this depression is: 0.40 × 14 = 5.6 points pulled against 0.60 × 95 = 57 → combined = 62.6, before the NOVA modifier. That product ends up around 52–62 on processing_quality depending on NOVA confidence. This is correctly in the C range — better than a genuine NOVA-4 additive-heavy product, but not the A it would wrongly receive if Component A were the sole driver.

**Why not 0.50/0.50?**

At equal weighting, Component B's higher variance (from position-weight fallbacks where stated_pct is absent) would carry more influence on the composite than its precision warrants at this stage. The `shadow_read_mode_breakdown_v1.json` artifact will tell us what fraction of products use position-weight fallbacks for their matrix signal. Until we know that distribution, giving Component B equal weight risks amplifying position-inference errors into the composite score at scale. 0.40 is a meaningful weight that captures the structural signal while limiting the variance amplification.

**Why not 0.70/0.30?**

Dropping Component B to 0.30 materially reduces its ability to catch the clean-label refined-starch inversion — the primary reason we are building the matrix signal at all. A palm-oil + flour + sugar product at 0.30 weight for Component B would score: 0.70 × 95 + 0.30 × 14 = 70.7 → after NOVA modifier → ~61, landing solidly in C. That is too high for a product with no redeeming structural complexity. The 0.40 weight is the minimum that makes the matrix signal a genuine guard against the inversion.

**The 0.60/0.40 split is labeled corpus-fit per target spec §2.3, which is the honest statement.** I am not claiming this ratio is literature-derived. It is a calibrated judgment that reflects the relative precision of the two signals and their respective roles. The shadow run will produce the empirical distribution that allows us to verify this calibration. If the read-mode breakdown shows that >40% of products rely on position-weight inference for Component B, and those products show unexpectedly large and apparently arbitrary movements, we should revisit the weight in Stage 1 with harder data.

**Expected directional effect:**
- Products with stated percentages (stated_pct path): Component B is well-grounded; 0.40 weight is appropriate. These products will show the cleanest A/B/C/D column movements.
- Products with position-only inference (no stated_pct): Component B is noisier; the 0.40 weight amplifies position-inference error. These are the products to watch in the top-movers anomaly table.
- Component B fallback products (unparseable text → Component B = None): the formula correctly degrades to Component A only. These are correctly flagged as `COMPONENT_B_NONE` in the anomaly report.

---

## OD-3 — NOVA Subordination Modifier Magnitudes (NOVA-4 = −10, NOVA 1-2 = +5, NOVA-3 = 0)

**Question:** Confirm the NOVA modifier magnitudes applied confidence-scaled on top of the combined Component A+B score.

**Recommended by Data Agent:** NOVA-4 at high confidence = −10; NOVA 1-2 at high confidence = +5; NOVA-3 = 0. All confidence-scaled via the existing `_w4_confidence_scale()` helper.

### Ruling: RATIFY — NOVA-4 = −10, NOVA 1-2 = +5, NOVA-3 = 0, all confidence-scaled

**Justification:**

These are the correct magnitudes for a shadow run that wants to demonstrate NOVA as "meaningful but subordinate." Let me be precise about what each magnitude achieves and why I am confirming them rather than adjusting.

**On NOVA-4 = −10 (depression, not a cliff):**

At high confidence, a −10 modifier on top of the A+B combined score means a NOVA-4 product with Component A=58, Component B=50, combined=54.8 would score 44.8 — moving it from mid-C to low-C approaching D. This is appropriate. The old NOVA-4 step-lookup was a fixed score of 35 on processing_quality. The new candidate at −10 modifier does not force NOVA-4 products to 35; it depresses them from wherever their structural signals land. A NOVA-4 product with 5 additives and a refined matrix might land at 28–30 (Component A + B combined ~38, minus 10 = 28). A NOVA-4 product that is misclassified by NOVA but has only 1 modest additive and a decent matrix signal (combined ~75) would score 65 — still a C, but not the punishing 35 the old table imposed. This is the correct de-chaining behavior: NOVA as a modifier respects what the structural signals already say rather than overriding them.

At medium confidence (confidence_scale ≈ 0.6): modifier = −6. This correctly attenuates NOVA's influence when the classification is uncertain. The direction is pessimistic (the existing `_w4_confidence_scale()` helper, applied in the pessimistic direction) — which is the right posture. We should not give NOVA-4 a free pass at medium confidence; we should proportionally credit it.

**Data Agent's concern (in the OD-3 rationale) that −10 might be "too small":** this concern is valid but premature. A NOVA-4 product with Component A score = 90 (0 or 1 additive, essentially clean-label) still scoring 80 on processing_quality after the modifier would be a genuine problem — it would mean the de-chained engine is failing the Petit Beurre / Chokita test (the BARI-INVERSION-TEST-001 adversarial fixture). However, the answer is not to increase the modifier to −15 now, because doing so would conflate two problems: (1) the modifier is correctly sized but Component A is set too permissive for the 0-additive path and (2) the modifier is actually undersized. The shadow run will disambiguate. If NOVA-4 products with 0 additives and clean-label refined matrices are scoring above 70 on processing_quality, the root cause is that Component B is not catching the refined matrix (coverage gap or formula gap), not that −10 is insufficient. The fix for that is Component B, not an inflated NOVA modifier.

Increasing to −15 now risks making NOVA a dominant input again under the wrong products — specifically, genuine minimally-processed products that get a NOVA-4 classification through a contaminating ingredient. At −15, high-confidence NOVA-4 overrides a genuinely good structural signal by 15 points. The target spec explicitly rejects this: "not a cliff, a moderate additional depression."

I will note for the product agent and owner: if the shadow run shows that Component B cannot catch refined-matrix clean-label products (i.e., the position-only inference path produces noise, not a systematic downward pull), we should revisit the modifier upward to −15 in Stage 1 as a stopgap while the matrix signal is hardened. That is a Stage 1 calibration decision, not a shadow-run design decision.

**On NOVA 1-2 = +5 (incremental push, not a floor):**

The +5 bonus for NOVA 1-2 at high confidence provides a modest upward lift for genuine minimally-processed products. The old step-lookup was 95 (NOVA-1) or 85 (NOVA-2). The new candidate gives such products the full Component A signal (near-95 for 0 additives) + the full Component B signal (near-95 for whole-food dominant ingredients) + a +5 confirmation bonus → clamped at 95. This is the right behavior: the +5 doesn't do much for products that are already well-scored by the structural signals (they are already near the 95 ceiling); it matters for genuinely whole-food NOVA-2 products that have a few additives or a mixed matrix and would otherwise land at ~80, moving them to ~85. The bonus is directionally correct and small enough not to distort.

**On NOVA-3 = 0:**

NOVA-3 is the most heterogeneous class. A sourdough bread with a small emulsifier is NOVA-3. A protein bar made entirely from isolated proteins and synthetic additives is sometimes classified NOVA-3. Assigning a modifier (positive or negative) to NOVA-3 would paper over this heterogeneity. The correct behavior is for Component A and Component B to differentiate these products — the matrix signal and additive count already capture what matters. NOVA-3 gets no modifier, and any NOVA-3 product's processing_quality score should be determined almost entirely by its structural signals. This is the cleanest expression of the "NOVA as modifier, not determinant" principle.

**Expected directional effect:**
- NOVA-4 at high confidence: additional −10 depression on the combined score. Products near grade boundaries (combined landing in 50–60) may move from C to D after the modifier if they are also low-matrix and additive-heavy.
- NOVA-4 at medium confidence: modifier ≈ −6. Smaller movement; meaningful but not decisive.
- NOVA-4 at low confidence: modifier ≈ −3 to −4. Effectively a directional hint; the structural signals dominate.
- NOVA 1-2 at high confidence: +5 bonus. Most products in this class are already near-ceiling on Components A and B; the bonus will register only for genuinely mixed NOVA-2 products.
- NOVA-3: no modifier. All differentiation through Components A and B.

---

## OD-4 — N-3 NOVA-4 Composite Cap at 68 (Interim Guard)

**Question:** Should the N-3 NOVA-4 composite cap (68) remain active at 68 during the shadow run, or be changed?

**Recommended by Data Agent:** Keep at 68.

### Ruling: RATIFY — Keep the N-3 cap at 68 for the shadow run

**Justification:**

This is the clearest of the four decisions. The cap should stay at 68 during the shadow run, and the Data Agent's rationale is correct: the shadow run's value depends on seeing what the candidate engine produces with the existing safety structure still in place. Changing the cap during the shadow run would conflate "the candidate engine under the interim guard" with "the candidate engine exposed," making the movement table harder to read.

**The specific diagnostic value of keeping the cap at 68:**

The anomaly report (`shadow_anomaly_report_v1.json`) will classify every NOVA-4 product where the cap fires in Column D as a finding. Within that classification, the harness distinguishes: (a) "cap is binding and the continuous score would be above 68 without it" from (b) "cap fires but the continuous score is already below 68 — coincidental." Class (a) tells us where the candidate engine is under-penalizing relative to the intent of the cap. Class (b) tells us where the cap is redundant. After the shadow run, if the proportion of class (b) products is high (say >70% of NOVA-4 products where the cap fires have a continuous score already below 68), that is the empirical evidence that the candidate engine makes the cap redundant — which is exactly the condition target spec §5.1 sets for its removal. We cannot generate that evidence without running the shadow with the cap in place.

**The target spec disposition (§5.1, N-3) is also correct:**

Stage 1B raises the cap to 78 (interim). The shadow run is not Stage 1B — it is the simulation that precedes Stage 1B. Running the shadow with the cap at 68 correctly preserves the stage sequence: shadow run at 68 → results reviewed by owner → Stage 1B decision (raise to 78 or go straight to removal based on shadow results).

**What this means for interpreting the shadow movement table:**

The shadow run's Column D scores for NOVA-4 products are scores under the interim guard. Any product whose Column D score equals exactly 68 should be checked in the anomaly report to see whether the cap is binding (continuous score > 68) or coincidental (continuous score ≤ 68). The owner and Product Agent should review the count of binding-cap products before deciding on Stage 1B.

**Expected directional effect:**

The cap at 68 will act as a ceiling for any NOVA-4 product whose Component A + Component B + NOVA modifier combined still exceeds 68. Given P = 14 and the −10 modifier, a NOVA-4 product would need: combined_pre_nova > 78 to have the cap bind at 68 after the modifier. That requires Component A ≈ 90+ (0-1 additives) AND Component B ≈ 60+ (modest whole-food presence). This is the clean-label refined-starch problem — products that have few additives and some whole-food ingredients but are structurally NOVA-4. These are exactly the products the cap was designed to protect against. If the cap binds for many such products in Column D, it reveals Component B is not catching them — a Stage 1 calibration priority.

---

## Cross-OD Notes for the Shadow Run Analyst

**Note on the D4-off path for Component A:** Several products in the corpus will have additive_marker_count = 0 because they have clean labels or because the ingredient parser does not detect their additives (vocabulary gaps). These products will score 95 on Component A regardless of P = 14. This is correctly conservative in the upper direction — it will produce COMPONENT_B_NONE and clean-label false-negatives in the column D results. The shadow run should flag all products with additive_marker_count = 0 + NOVA-4 classification as a cross-check: these are the candidates for the BARI-INVERSION-TEST-001 adversarial fixtures.

**Note on missing-ingredient-text fallback (Component B = None):** The design specifies the formula degrades to `combined = processing_load_score` (Component A only) when Component B returns None. This is the correct fallback but it means these products get 0 benefit from the matrix signal. The shadow run should report: how many products fall into the `component_b_read_mode: no_markers` path? If this is >20% of the corpus, the Component B coverage is too thin to serve as a genuine structural guard, and we need to expand the marker lexicon before Stage 2.

**Note on interaction between OD-1 and OD-3:** The P = 14 flat penalty and the −10 NOVA-4 modifier are complementary for additive-heavy NOVA-4 products but compete for effect on clean-label NOVA-4 products. The shadow run should specifically report: how many NOVA-4 products have additive_marker_count ≤ 1 AND score above 60 in Column D? These are the products where the de-chained engine is most exposed if Component B fails to catch the structural processing.

---

## Summary Table

| OD | D6 Verdict | Value Ratified | Confidence Label |
|---|---|---|---|
| OD-1 Flat penalty P | RATIFY | **P = 14** | Corpus-fit (interim approximation of D4 tier average) |
| OD-2 A/B blend weights | RATIFY | **0.60 / 0.40** | Corpus-fit (reflects relative signal precision at this stage) |
| OD-3 NOVA modifier magnitudes | RATIFY | **NOVA-4 = −10, NOVA 1-2 = +5, NOVA-3 = 0, confidence-scaled** | Corpus-fit (magnitude); Evidence-backed (direction: NOVA as modifier, not determinant) |
| OD-4 N-3 interim cap | RATIFY | **Keep at 68 for shadow run** | Governance (correct stage sequencing; empirical evidence from shadow determines Stage 1B disposition) |

All four values: Product Agent D7 co-sign required before Data Agent implements. Owner reviews shadow movement table before any deploy. These values are shadow-run design parameters only.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/d6_ratify_shadow_ods_v1.md",
      "action": "created",
      "sha256": "pending — orchestrator runs Get-FileHash after write"
    }
  ],
  "counts": {
    "open_decisions_reviewed": "4/4 (OD-1, OD-2, OD-3, OD-4 — denominator: shadow_run_plan_v1.md Part A)",
    "verdicts_ratify": "4/4 — all recommended values ratified without revision",
    "verdicts_revise": "0/4",
    "cross_od_notes_for_analyst": "3 (additive_marker_count=0+NOVA-4 class, Component B coverage %, clean-label NOVA-4 exposure count)",
    "evidence_tiers_applied": "Corpus-fit (OD-1 magnitude, OD-2 weights); Evidence-backed (OD-3 direction, NOVA literature); Governance (OD-4 stage-sequencing rationale)",
    "d7_cosign_required": "yes — all 4 ODs; Data Agent must not implement until Product Agent confirms"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/shadow_run_plan_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v3.md", "exit_code": 0}
  ],
  "not_done": [
    "Product Agent D7 co-sign on all four ODs — required before Data Agent implementation",
    "Shadow run not executed — these are design ratifications only; no movement table exists yet",
    "Stage 1B cap disposition (raise to 78 or remove) — deferred pending shadow run results and owner review",
    "BARI_D4_SCORE_V1 activation — explicitly excluded from this shadow run; flat P=14 is the approved interim fallback",
    "SHA256 of this file — orchestrator runs Get-FileHash after write"
  ],
  "self_check": "Acceptance test: Product Agent D7 co-signs all four ODs (or revises any with a countervailing ruling). Data Agent then implements BARI_DECHAIN_V1 with: P=14, weights 0.60/0.40, NOVA-4 modifier=-10, NOVA 1-2 modifier=+5, NOVA-3=0 (all confidence-scaled), N-3 cap retained at 68. Shadow run executes; Column A cross-check passes (all Column A scores match committed baseline, exit code 0 from self-gate). Shadow movement table and anomaly report are produced and reviewed by the owner before any deploy decision. No score is published from this ratification — this document is design authorization only."
}
```
