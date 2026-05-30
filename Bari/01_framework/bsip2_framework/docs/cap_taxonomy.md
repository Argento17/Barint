# Cap Taxonomy

**Purpose:** Audit all existing hard caps in BSIP2, classify them by type, and assess whether each should remain binary (hard) or eventually become continuous (gradient). This document prevents uncontrolled cap proliferation by establishing criteria for what a cap must justify to exist and what classification it belongs to.

---

## Why cap taxonomy matters

Every hard cap introduces a scoring cliff. Every cliff is a potential gaming surface and an explainability failure. Caps are justified — they enforce structural floors below which a product cannot grade regardless of other signals — but only when the structural concern is sufficiently severe and binary in nature.

The question for each cap is not "is there a concern here?" but "is this concern severe enough and binary enough to justify a hard boundary?" If the answer is "mostly yes, but not absolutely," the cap should eventually become a steep-gradient continuous penalty.

---

## Cap classification system

| Class | Description | Should remain hard? |
|-------|-------------|-------------------|
| **Safety cap** | Protects against a product receiving a high grade when a severe structural disqualifier is present | Yes — these are architectural commitments |
| **Confidence cap** | Limits scores when data quality is insufficient to justify a high grade | Yes — data reliability, not food quality |
| **Structural moderation cap** | Limits scores when a measurable structural property (calories, sugar, sodium) exceeds a threshold that represents genuine nutritional concern | Yes for now; candidate for gradient transition |
| **Behavioral-risk cap** | Limits scores based on a behavioral hypothesis (hyper-palatability patterns, processing-related consumption risk) | Eventually continuous — behavioral hypotheses warrant gradient expression |
| **Heuristic temporary cap** | Caps added for practical reasons that may not survive rigorous review — category-level health-halo rules, red-label proxies | Review candidacy — some may become gradients or be absorbed into dimensions |

---

## Full cap inventory

---

### Confidence Caps

---

#### CC-01 — Low Confidence Ceiling
**Rule:** If confidence 40–59: final score ≤ 70
**Concern family:** Confidence (separate from CONCERNS graph)
**Rationale:** A product with significant data gaps cannot receive a grade that requires trusting signals the system does not have. Grade B or higher implies sufficient analytical certainty; low confidence disqualifies this.
**Should remain hard:** Yes. This is a data quality gate, not a food quality judgment. A score of 71 vs. 70 has no meaning when the inputs are incomplete.
**Gaming risk:** Low — data completeness is not easily manipulated.
**Explainability:** Good — "your score is capped because critical nutrition data is missing" is a complete and honest explanation.

#### CC-02 — Insufficient Confidence Ceiling
**Rule:** If confidence < 40: final score ≤ 50
**Concern family:** Confidence (separate from CONCERNS graph)
**Rationale:** Critical data absent; the analytical result is not reliable enough to display a meaningful grade.
**Should remain hard:** Yes. Displaying a grade above D when critical data is absent would be analytically irresponsible.
**Gaming risk:** Very low.
**Explainability:** Good.

---

### Safety Caps

These caps protect against a specific severe structural disqualifier producing a misleadingly high grade. They are architectural commitments.

---

#### SC-01 — Sweetener Present
**Rule:** `SWEETENER_PRESENT`: score ≤ 70
**Concern family:** Outside CONCERNS graph — fires independently
**Rationale:** Non-nutritive sweetener substitution is not nutritional quality improvement. A product using sweeteners instead of sugar should not receive grade A or high grade B — this would imply that sweetener-formulated products are preferable to their sugar-containing equivalents on a food quality basis.
**Should remain hard:** Yes. This is a normative architectural commitment (L6 signal): sweetener substitution ≠ quality improvement.
**Gaming risk:** Low — sweetener presence is a binary ingredient fact.
**Explainability:** Good — "contains non-nutritive sweetener; maximum score is 70" is complete.
**Note on bluntness:** The cap is deliberately uniform across sweetener types. The bluntness is known and accepted at the current phase. Future refinement may distinguish sweetener burden (one vs. three sweeteners) without removing the hard cap.

#### SC-02 — Trans Fat (Veto)
**Rule:** Trans fat detected: score = 0 (full veto)
**Concern family:** `general`
**Rationale:** Industrially produced trans fats have no safe level of consumption at a population level. A veto (not a cap) is the correct response — no grade above E can be justified for a product containing industrial trans fats.
**Should remain hard:** Yes. The scientific basis for the veto is strong and consensus-level.
**Gaming risk:** Very low.
**Explainability:** Perfect — "contains trans fat" is a complete explanation.

#### SC-03 — Multiple Red Labels (2+)
**Rule:** `ISRAELI_RED_LABELS_2_PLUS`: score ≤ 45
**Concern family:** `SUGAR_LOAD` (when sugar is one of the red labels); `regulatory`
**Rationale:** Two or more Israeli red warning labels represent regulatory confirmation of multiple severe nutritional concerns. A product carrying two structural warnings from a regulatory process cannot grade above E/low-D territory.
**Should remain hard:** Yes. The regulatory process has already made the structural determination.
**Gaming risk:** Low — regulatory label removal requires genuine reformulation.
**Explainability:** Good.

---

### Structural Moderation Caps

These caps fire when a measurable nutritional property exceeds a threshold associated with genuine concern. They are binary implementations of what are ultimately continuous quality gradients.

---

#### SMC-01 — High Sugar (25g+)
**Rule:** `HIGH_SUGAR_25G_PLUS`: score ≤ 60
**Concern family:** `SUGAR_LOAD`
**Rationale:** Sugar concentration above 25g/100g represents a structural concern regardless of calorie context.
**Should remain hard for now:** Yes, at the current calibration phase. The 25g threshold is experimentally reasonable; the concern is real.
**Candidate for gradient:** Yes, eventually. The jump from 24.9g (no cap) to 25.1g (cap at 60) is not analytically defensible as a hard boundary. A steep gradient beginning at ~18–20g and reaching full cap effect at 30+ g would be more precise.
**Gaming risk:** High — a product reformulated from 25.2g to 24.8g sugar has made no meaningful nutritional change but escaped the cap.
**Explainability:** Moderate — "your product contains 28g sugar per 100g, above our structural threshold" works; "29g vs. 24g" gap is harder to explain as a hard boundary.

#### SMC-02 — High Cal + High Sugar (Severe)
**Rule:** `HIGH_CAL_HIGH_SUGAR_SEVERE`: score ≤ 50
**Concern family:** `SUGAR_LOAD`
**Trigger:** kcal ≥ 500 AND sugar ≥ 25g/100g
**Rationale:** The combination of high calorie density and high sugar represents a more severe structural concern than either alone. A 50-cap places the product firmly in grade D.
**Should remain hard:** Yes for now — this combination is genuinely severe; a grade above D is hard to justify.
**Candidate for gradient:** Moderate. The dual-threshold nature (both conditions must be met) already provides more discrimination than a single threshold. The primary gaming surface is the kcal boundary (499 vs. 501), which is the same problem as SMC-01.
**Gaming risk:** High on the kcal boundary.
**Explainability:** Good — the combination is clearly articulable.

#### SMC-03 — High Cal + High Sugar (Moderate)
**Rule:** `HIGH_CAL_HIGH_SUGAR_MODERATE`: score ≤ 60
**Concern family:** `SUGAR_LOAD`
**Trigger:** kcal ≥ 470 AND sugar ≥ 20g/100g
**Rationale:** Softer version of SMC-02 — staggered threshold provides a step function that reduces but does not eliminate cliff behavior.
**Should remain hard:** Provisionally yes; it is part of the staggered cap structure.
**Candidate for gradient:** This entire group (SMC-01, SMC-02, SMC-03) is a candidate for replacement with a single two-dimensional gradient surface that scores the combination continuously. This is a significant architectural change deferred to a later phase.

#### SMC-04 — High Calorie, Low Satiety (Severe)
**Rule:** `HIGH_CAL_LOW_SATIETY_SEVERE`: score ≤ 55
**Concern family:** `CALORIE_LOAD`
**Trigger:** kcal ≥ 500 AND protein < 6g AND fiber < 3g
**Rationale:** A product at very high calorie density with minimal protein and fiber delivers caloric burden without compensating structural nutrition.
**Should remain hard:** Yes for now.
**Candidate for gradient:** Moderate. The three-condition trigger (all must be met) provides some discrimination. The primary issue is the hard kcal boundary.

#### SMC-05 — High Sodium (700mg+)
**Rule:** `HIGH_SODIUM_700MG_PLUS`: score ≤ 60
**Concern family:** `SODIUM_LOAD`
**Rationale:** 700mg sodium/100g is a high concentration threshold above which the product delivers a significant sodium contribution even at normal serving sizes.
**Should remain hard:** Provisionally yes.
**Candidate for gradient:** Yes. The 700mg threshold is arbitrary in the sense that a product at 690mg is not meaningfully different from one at 710mg. A gradient starting at ~400mg and reaching full cap effect at 900mg+ would be more defensible.
**Gaming risk:** High on the 700mg boundary.
**Note on condiments:** This cap is problematic for condiments (miso, soy sauce, preserved vegetables) used in small quantities. The cap is correct per-100g but contextually misleading for this product type. See `evaluation_scope.md`.

#### SMC-06 — Saturated Fat Red Label
**Rule:** `ISRAELI_RED_LABEL_1` (saturated fat): score ≤ 55
**Concern family:** `FAT_QUALITY`
**Rationale:** An Israeli regulatory red label for saturated fat is a regulatory determination that a structural threshold has been exceeded.
**Should remain hard:** Yes — regulatory label cap should respect the regulatory determination.
**Note:** The regulatory threshold is the gaming surface, not the BSIP2 threshold. If a product reformulates to escape the Israeli red label, it has genuinely changed its nutritional profile.

#### SMC-07 — Saturated Fat Red Label (Sugar context)
**Rule:** `ISRAELI_RED_LABEL_1` (sugar context): score ≤ 55
**Concern family:** `SUGAR_LOAD`
Same analysis as SMC-06.

---

### Behavioral-Risk Caps

These caps fire based on behavioral hypotheses (L5 signals) — population-level patterns, not individual facts.

---

#### BRC-01 — NOVA 4 Ultra-Processed
**Rule:** `NOVA_PROXY_4_ULTRA_PROCESSED`: score ≤ 60
**Concern family:** `PROCESSING_LOAD`
**Rationale:** Ultra-processed foods (NOVA 4) as a class are associated at population level with poorer health outcomes. A product inferred as NOVA 4 cannot grade above B.
**Should remain hard:** Yes for now, but this cap carries the highest epistemic risk. The NOVA inference is a proxy classification (L3 signal with imperfect confidence). Applying a hard cap based on an inference introduces classification error into a binary outcome.
**Candidate for gradient:** Yes, eventually. The correct model is: NOVA 4 certainty → hard cap. NOVA 4 with low classification confidence → gradient penalty proportional to confidence. This is an L3-confidence-weighted L4 response.
**Gaming risk:** Low on the actual cap (because gaming the NOVA proxy requires removing the specific ingredient markers that trigger it — which is genuine reformulation). Moderate for the cliff behavior (borderline NOVA 3/4 products).
**Explainability:** Good when explained as "ingredients indicate ultra-processing"; weaker when NOVA inference confidence is low.

#### BRC-02 — NOVA 3 Processed
**Rule:** `NOVA_PROXY_3_PROCESSED`: score ≤ 75
**Concern family:** `PROCESSING_LOAD`
**Rationale:** NOVA 3 represents processed food with additive or formulation complexity. The cap at 75 is mild (allows grade A bottom range or grade B top) and reflects a moderate concern.
**Should remain hard:** The 75 cap is permissive. It limits only the very top of the scale, allowing most grade B products to score freely. Should remain hard as a ceiling for now.
**Candidate for gradient:** This cap may eventually be absorbed into the processing quality dimension's continuous scoring.

#### BRC-03 — Additive Markers 3+
**Rule:** `ADDITIVE_MARKERS_3_PLUS`: score ≤ 65
**Concern family:** `PROCESSING_LOAD`
**Rationale:** Three or more distinct additive markers represent a processing burden that warrants a cap.
**Should remain hard:** Provisionally.
**Candidate for gradient:** Yes. The difference between 3 markers and 4 markers is not meaningfully harder than 2 markers and 3 markers. A continuous penalty that deepens with marker count would be more defensible.
**Gaming risk:** Moderate — a manufacturer could remove one additive marker to escape the cap.

#### BRC-04 — Additive Markers 5+
**Rule:** `ADDITIVE_MARKERS_5_PLUS`: score ≤ 55
**Concern family:** `PROCESSING_LOAD`
**Rationale:** Five or more additive markers represent a high processing burden.
**Should remain hard:** Yes for now — this level of additive burden is a meaningful structural concern.
**Candidate for gradient:** Part of the same continuous-additive-burden gradient that BRC-03 would feed into.

---

### Heuristic Temporary Caps

These caps were added for practical or proxy reasons and may not survive rigorous review unchanged.

---

#### HTC-01 — Snack Bar High Calorie (Health-Halo)
**Rule:** `SNACK_BAR_HIGH_CAL`: score ≤ 70 for snack bar category with ≥ 430 kcal
**Concern family:** `CALORIE_LOAD`
**Rationale:** Health-halo risk in the snack bar category. Products marketed as health foods while delivering confectionery-level calorie density cannot receive a "good" grade.
**Should remain hard:** Yes, but this cap is the most heuristic in the system. The 70 ceiling is a policy decision about what grade a calorie-dense snack bar should be able to achieve, not a structural analytical finding.
**Candidate for gradient:** This cap is a candidate for replacement with a category-specific steeper calorie density penalty curve rather than a hard cap. The effect would be similar but without the cliff.
**Gaming risk:** High — the 430 kcal boundary is a clear reformulation target.
**Explainability:** Moderate — "snack bars above 430 kcal are capped at 70" is explainable but requires category context.

#### HTC-02 — Snack Bar Red Sugar Label
**Rule:** `SNACK_BAR_RED_SUGAR_LABEL`: score ≤ 55
**Concern family:** `SUGAR_LOAD`
**Rationale:** A snack bar carrying a red sugar label represents the health-halo failure in its most explicit form.
**Should remain hard:** Yes — the regulatory label is a binary external determination.
**Review note:** This cap overlaps significantly with the general `ISRAELI_RED_LABEL_1` (sugar) cap at 55. The snack bar specificity may be redundant.

#### HTC-03 — Snack Bar High Cal + High Sugar
**Rule:** `SNACK_BAR_HIGH_CAL_SUGAR`: score ≤ 60 for snack bar with ≥ 470 kcal AND sugar ≥ 15g
**Concern family:** `SUGAR_LOAD`
**Rationale:** Snack-bar-specific version of the calorie-sugar interaction rule with a lower sugar threshold (15g vs 20g) justified by the category health-halo concern.
**Should remain hard:** Provisionally.
**Gaming risk:** High — dual threshold.
**Review note:** The 15g sugar threshold for snack bars is notably lower than the general interaction rules. The additional strictness is intentional but should be explicitly reviewed when threshold calibration is undertaken.

---

## Cap proliferation guard

**Current total hard caps:** 17 distinct rules producing hard score ceilings (not counting family budget clamps and floors).

**Proliferation rule (proposed):**
Before adding a new hard cap:
1. Identify which of the five cap classes it belongs to
2. Confirm it cannot be expressed as a continuous penalty or steeper dimension gradient
3. Confirm it does not overlap with an existing cap in the same concern family
4. Document which existing cap it would replace if the rule count is already above the proliferation limit

**Proposed proliferation limit:** No more than 20 distinct hard cap rules across all concern families. Current count is 17. The limit should be enforced by design review, not by technical restriction.

---

## Caps that are strongest candidates for eventual gradient transition

| Cap | Class | Why gradient eventually | Priority |
|-----|-------|------------------------|----------|
| `HIGH_SUGAR_25G_PLUS` | SMC | Single threshold; high gaming risk | High |
| `HIGH_SODIUM_700MG_PLUS` | SMC | Single threshold; problematic for condiments | High |
| `ADDITIVE_MARKERS_3_PLUS` | BRC | Count-based; gradient more defensible | Medium |
| `ADDITIVE_MARKERS_5_PLUS` | BRC | Pair with 3+ into continuous penalty | Medium |
| `NOVA_PROXY_4` | BRC | Should be confidence-weighted | Medium |
| `SNACK_BAR_HIGH_CAL` | HTC | Health-halo logic via steeper calorie curve is cleaner | Low |
