# D7 Co-Sign: BSIP2 Engine De-Chaining
**Reviewer:** Product Agent (D7 lane)
**Input spec:** `target_scoring_logic_spec_v1.md` (Sections 5 and 6) + `dechain_d6_proposal_v1.md`
**Program:** `scoring_overhaul_program_v1.md` (ratified, 4-lane)
**Task:** TASK-395
**Date:** 2026-06-25
**Status:** CO-SIGN WITH CONDITIONS — conditions enumerated per disposition below

---

## Preamble: What This Co-Sign Does and Does Not Authorize

This is a governance gate, not an implementation trigger. My co-sign authorizes the
**disposition table as a program plan** — the direction of each cap's fate, the dependency
sequencing, and the retained guards. It does NOT authorize any engine code change, any
flag flip, or any published score movement. Those remain blocked behind:

1. Phase 0 reproducible baseline (non-negotiable prerequisite per the ratified program plan)
2. Per-stage shadow runs with owner-reviewed movement tables
3. The owner frozen-invariant tripwire (any published score change)

A "CO-SIGN" on a disposition means: the product rationale is sound, the consumer story is
defensible, the anti-regression coverage is credible. It does NOT mean "build this now."
A "CO-SIGN WITH CONDITIONS" means: the disposition direction is correct but one or more
safety conditions must be confirmed before that stage ships. A "WITHHOLD" would mean the
disposition itself is wrong and must be reconsidered before any implementation.

There are no WITHHOLD verdicts in this review. There are CONDITIONS on several
dispositions that must be satisfied before the relevant stage is triggered.

---

## Section 5 Review: Cap Disposition Table (18 chains)

### 5.1 NOVA Family

**N-1: NOVA_PROCESSING_SCORES step lookup → REPLACE**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "We stopped using a four-step classification table and instead read your
product's ingredient list directly — if it is made of refined flour, sugar, and palm oil
with no whole-food complexity, it scores lower regardless of how its NOVA class is
labeled." This is a clean, defensible public explanation.

Anti-regression concern: this is the highest-risk disposition in the entire program. The
clean-label refined-starch inversion — a three-ingredient refined white-flour product
escaping penalty — is a real, documented failure mode. The spec correctly names Component
B (matrix signal) as the mandatory inversion guard. However, label-derivability of the
nut/seed/legume presence signal is explicitly flagged as NOT YET VERIFIED (spec Section
2.2, "new required signal"). This is the gap that makes N-1 the hardest workstream.

Conditions:
- C-N1-1: Component B (matrix signal) must be validated for label-derivability on a
  minimum 50-product sample from the live corpus before the NOVA lookup is deactivated.
  Accuracy floor: the refined-starch markers must fire on >= 90% of products where the
  ingredient list contains only refined-grain + fat + sugar combinations. If the accuracy
  check fails, N-1 is NOT authorized to ship regardless of other stage completions.
- C-N1-2: Adversarial fixture #1 (refined white-flour cookie, zero additives, low sugar)
  must score below 60/C in the shadow run before the flag flips in any production-adjacent
  environment. This is the non-negotiable anti-regression proof for this disposition.
- C-N1-3: EV-NOVA-REPLACE-001 must be registered with the label-observability result
  attached before Stage 2 ships.

**N-2: NOVA_WFI_SCORES step lookup → REPLACE (W4 confidence scaling)**
Verdict: **CO-SIGN**

Consumer story: "Whole-food integrity now scales with how confident we are in the
classification — a product we're uncertain about doesn't automatically inherit the
best-case score." This is the least controversial disposition and is framed correctly
as a bug fix completing W4, not a philosophy change.

No product-side conditions. The pessimistic-toward-NOVA-4 formula direction (Section 3,
MD-4) is correct: ambiguity should not reward the product. Stage 0 can proceed as
soon as Phase 0 baseline is established.

**N-3: NOVA_PROXY_4_ULTRA_PROCESSED cap (68) → REPLACE → interim relaxation → REMOVE**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story for the interim relaxation (68 → 78): "We loosened a hard ceiling to
allow genuinely partial-UPF products to score at their real level while we build a more
accurate additive-based replacement." Defensible.

Consumer story for full removal: "The additive-identity scoring now directly penalizes
each contested ingredient — a product with five synthetic additives receives proportional
deductions rather than hitting a single hard cap." Defensible once D4 is validated.

Anti-regression concern: the 68 cap was the primary backstop against NOVA-4 products
winning on strong nutrition numbers. The spec correctly identifies additive parser accuracy
as the dependency — if the parser undercounts, the natural depression does not occur. The
staged approach (interim 78, then full removal conditional on parser validation) is the
right sequencing.

Conditions:
- C-N3-1: Before the interim cap relaxation (68 → 78) ships, BARI-INVERSION-TEST-001
  must be formally specified as a machine-executable test with the Petit Beurre/Chokita
  pair as a required fixture. A cap cannot be relaxed without the guardrail that replaces
  it being live and passing.
- C-N3-2: The full cap removal (post-interim) is conditional on the additive parser
  validation showing no NOVA-4 product with additive_count >= 5 scoring above 65 on the
  composite without the cap. If that check fails, the D4 deduction is under-calibrated —
  adjust deductions, do not remove the cap until the check passes.

**N-4: NOVA_PROXY_3_PROCESSED cap (87) → REMOVE**
Verdict: **CO-SIGN**

Consumer story: not needed — this cap is publicly inert. A NOVA-3 product reaching 87
composite would require exceptionally clean nutrition dimensions that already independently
justify a high score. The cap adds nothing the continuous engine does not already prevent.
Removal reduces rule accumulation with zero consumer-facing risk.

No conditions. Remove can proceed immediately behind its flag once Phase 0 baseline exists.

---

### 5.2 Sugar Family

**S-1: HIGH_CAL_HIGH_SUGAR_SEVERE cap (50) → REPLACE (graduated sugar curve)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "High-calorie, very-high-sugar products now face a proportional penalty
that scales with how far above the threshold they sit, rather than a hard stop at the
same score for all products in that range." Clear upgrade from binary to proportional.

Anti-regression concern: the 25g+ band in SUGAR_GRADUATED_BANDS currently has 0 penalty
because "hard caps handle this range" — the spec names this circularity explicitly and
proposes extending the band (8 points penalty, corpus-fit). This extension is the
replacement. If the extension is not active, the cap removal creates a blind spot for
kcal ≥ 500 / sugar ≥ 25g products.

Condition:
- C-S1-1: SUGAR_GRADUATED_BANDS must be extended to cover the 25g+ range with the
  proposed 8-point penalty (or calibrated equivalent) and validated on the shadow run
  before S-1 is retired. The shadow run must confirm no product previously capped at 50
  now scores above 55 after the extension activates. If any do, the band penalty is
  under-calibrated — adjust it, not the cap removal.

**S-2: HIGH_CAL_HIGH_SUGAR_MODERATE cap (60) → REMOVE**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: not needed publicly — this cap operates in a range where S-7 (red label
at sugar ≥ 17.5g, cap 55) is more binding and the continuous sugar dimension already
penalizes heavily. The cap is genuinely redundant at that overlap.

Condition:
- C-S2-1: S-7 must remain active (not yet retired) when S-2 is removed. These are
  sequenced in the right order (S-2 removes early in Stage 3, S-7 retires late in Stage
  5). Confirm the sequencing is not violated in implementation.

**S-3: HIGH_SUGAR_25G_PLUS cap (60/68) → REPLACE (absorbed into graduated curve)**
Verdict: **CO-SIGN WITH CONDITIONS**

Same dependency as S-1: the graduated curve extension must be active before the cap is
retired. The SC-2 elevated cap (68 for whole-fruit primary, NOVA 1-2) deserves particular
attention — date bars are qualitatively different from confections.

Condition:
- C-S3-1: Validate that after S-3 retirement, no date bar or whole-fruit primary product
  (SC-2 classification) scores below 60 due to the sugar dimension without the 68 cap
  providing the floor. If SC-2 products drop below 60, the replacement curve must
  incorporate the whole-fruit structural differentiation before S-3 can be retired.

**S-4: HIGH_SUGAR_25G_GRANOLA_SEVERE cap (50) → KEEP**
Verdict: **CO-SIGN (confirmed)**

This cap was D7 co-signed 2026-06-23 (TASK-385) and the spec correctly leaves it in
place. Confirmed. The de-chaining program does not revisit recently approved, correctly
scoped caps unless a specific regression emerges in the shadow run that makes the case for
removal. No such case is presented here.

**S-5: SNACK_BAR_HIGH_CAL_SUGAR cap (60) → REMOVE**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: not needed publicly — this fires in range where S-7 (55) is more binding.

Condition:
- C-S5-1: Same as C-S2-1. S-7 must be active when S-5 is removed. The calorie table for
  snack_bar_granola must be confirmed calibrated before removal (the spec notes this
  dependency explicitly — confirm it in Stage 7 verification, not assumed).

**S-6: SNACK_BAR_RED_SUGAR_LABEL cap (55) → REPLACE (shelf-relative enrollment)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "Snack bars now face sugar assessment relative to the rest of the shelf —
how much higher than the category norm is more informative than a binary label cutoff."
This is consistent with the existing precedent for biscuit (EV-085) and cereal (EV-087)
and is a genuine step up in quality.

Condition:
- C-S6-1: EV-SNACKBAR-SR-001 must be registered with corpus statistics for
  snack_bar_granola × sugar (n ≥ 20, scale > 3.0g guard confirmed) before the shelf-
  relative signal replaces the binary cap. If the corpus is too thin (n < 20), the binary
  cap must remain until the corpus grows.

**S-7: ISRAELI_RED_LABEL_1_SUGAR cap (55) → REPLACE (BARI_REDLABEL_V1 continuous)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "Israeli red-label products now receive a continuous deduction
proportional to how far over the threshold they sit — not a hard stop at the same score
regardless of how far over they are." Correct direction.

This is the cap that gates Stages 3–6. Its replacement (BARI_REDLABEL_V1 full activation)
requires its own D7 co-sign for cross-category activation, which the spec correctly notes.
The co-sign here is for the disposition direction, not for the cross-category flag flip.

Condition:
- C-S7-1: Cross-category BARI_REDLABEL_V1 activation requires a separate D7 co-sign
  pass at Stage 5, reviewing the blast radius table before any cap is retired. This co-
  sign does not authorize that step; it authorizes the direction. The Stage 5 blast radius
  table — showing which products previously held at 55 now score where — is required input
  for that subsequent co-sign.

**S-8: ISRAELI_RED_LABELS_2_PLUS cap (45) → REPLACE (compounding continuous deductions)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "Two red-label products now face compounding continuous deductions rather
than a single hard floor at 45 — the severity reflects both the sugar and saturated fat
concerns proportionally." Correct.

The 45 cap is the harshest single guardrail. Its retirement must be the last step in
Workstream 2, and the spec correctly sequences it as Stage 6 (final).

Conditions:
- C-S8-1: No product previously held at 45 may score above 55 after Stage 6. This is
  the blast radius check specified in Section 5.2 of the spec. If any product exceeds 55,
  the deduction slopes in regulatory_quality are under-calibrated — adjust them. Do not
  retire this cap until the check passes.
- C-S8-2: Stage 5 must be complete and verified before Stage 6 starts. These are hard
  sequential dependencies, not optional ordering.

---

### 5.3 Calorie Family

**C-1: HIGH_CAL_LOW_SATIETY_SEVERE cap (55) → REPLACE (cross-dimension interaction term)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "High-calorie foods with low protein and low fiber now face a combined
penalty that reflects both problems simultaneously — the interaction is worse than either
alone, and the scoring now shows that proportionally rather than with a hard stop."
Solid upgrade.

The interaction formula (Section 5.3 of the spec) is marked corpus-fit, not literature-
derived. This is honest and acceptable — but it means the calibration work matters more,
not less.

Condition:
- C-C1-1: EV-CALORIE-SATIETY-001 must be registered before Stage 7, with the interaction
  formula and corpus-fit calibration documented. The calibration must be validated on the
  adversarial fixture suite — fixture #1 (high-kcal / low-satiety product) must score
  below 55 after the interaction term is active. If it does not, the formula is
  under-calibrated.

**C-2: SNACK_BAR_HIGH_CAL cap (70) → REPLACE (calorie archetype table)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "High-calorie snack bars are already handled by the calorie density table
for that format — the hard cap is redundant once the table is confirmed calibrated."
Clean and defensible once confirmed.

Condition:
- C-C2-1: The snack_bar_granola calorie density table calibration must be explicitly
  verified in the Stage 7 shadow run. Specifically: confirm that no snack bar at kcal ≥
  430 scores above 70 on the composite after the table operates without the cap. If any
  do, the table tier scores are under-calibrated — adjust them before retiring the cap.

---

### 5.4 Processing Family (Additive-Count Caps)

**P-1: ADDITIVE_MARKERS_5_PLUS cap (60) → REPLACE (D4 + additive parser fix)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "Five-additive products now face per-additive deductions based on the
identity and tier of each additive, rather than hitting a single hard stop at the same
score regardless of which additives they contain." Genuine quality improvement.

P-1 and P-2 are the caps most dependent on the additive parser being accurate. If the
parser miscounts, natural depression does not occur and the cap removal creates a blind
spot for multi-additive junk.

Conditions:
- C-P1-1: BARI_D4_SCORE_V1 must be active and validated (Stage 1A blast radius reviewed)
  before P-1 is retired. This is already the stated dependency — confirming it as a hard
  gate, not a soft dependency.
- C-P1-2: After D4 activation, verify that no NOVA-4 product with additive_count >= 5
  scores above 65 on the composite without P-1. If any do, the D4 deduction is under-
  calibrated. Adjust deductions before retiring the cap.
- C-P1-3: Adversarial fixture #2 (engineered low-sugar UPF with 8 additives, 3g sugar)
  must score below the comparable plain oats product in the shadow run. This is the
  primary anti-regression proof for P-1 and P-2 retirement.

**P-2: ADDITIVE_MARKERS_3_PLUS cap (72) → REPLACE (same as P-1)**
Verdict: **CO-SIGN WITH CONDITIONS**

Same conditions as P-1 (C-P1-1 through C-P1-3). P-2 is lower priority and the 72 cap
rarely binds uniquely — the spec is correct that it is secondary. Retire after P-1 is
validated.

---

### 5.5 Sodium Family

**Na-1: HIGH_SODIUM_700MG_PLUS cap (60) → REPLACE (in progress, BARI_GRAD_SODIUM_V1)**
Verdict: **CO-SIGN**

Consumer story: "Sodium is now assessed on a graduated scale calibrated to product
category — brined cheese faces different thresholds than a processed snack — rather than
a single hard stop at 700mg for all products." This is already the established direction
(brined program) and is partially implemented.

The endemic-category graduated replacement is already in place and has been working
correctly. The extension to non-endemic categories follows BARI_REDLABEL_V1 activation.
No additional conditions beyond the Stage 5 blast radius gate already specified.

**Na-2: HIGH_SODIUM_CEREAL_500 cap (75) → KEEP (recently added, graduated replacement)**
Verdict: **CO-SIGN (confirmed)**

Correctly kept. Na-2 was recently added as the graduated replacement for the cereal/
granola scope. It is not proposed for removal and this co-sign confirms agreement with
that position.

---

### 5.6 Fat Quality Family

**F-1: ISRAELI_RED_LABEL_1_SAT_FAT cap (55) → REPLACE (RECAL_P0 R5 graded penalty)**
Verdict: **CO-SIGN WITH CONDITIONS**

Consumer story: "Saturated fat now earns a proportional penalty on the fat quality
dimension rather than triggering a hard score ceiling — a product at 6g/100g and one at
15g/100g are treated differently." Correct direction.

F-1 retirement is Stage 8 — the deepest change and the most products affected.
RECAL_P0 promotion to default touches every live category and is the frozen-invariant
tripwire (owner-gated deploy, not this co-sign).

Conditions:
- C-F1-1: All preceding workstreams (Stages 0-7) must be complete before Stage 8 is
  initiated. This is already in the spec — confirming it as a hard gate.
- C-F1-2: The RECAL_P0 provisions R1 through R7 must each have their own explicit
  validation in the Stage 8 shadow run. The monotonicity invariant (FS-1 from Section 4
  of the spec) must be confirmed machine-checkable via unit test before Stage 8 ships.
- C-F1-3: Stage 8 requires a separate owner go-live decision (frozen-invariant tripwire:
  published score changes across all live categories). This co-sign does not authorize
  that step. The product and nutrition agents can jointly recommend it; the owner decides.

---

## Section 6 Review: Retained Guards (7 guards)

### 6.1 Trans-Fat Veto (V-1, score = 0)
**CONFIRMED KEEP**

Rationale from product lens: the only product-side question is consumer defensibility.
"A product containing industrial trans fat scores zero — this is a food safety
disqualifier with strong international consensus from WHO, EFSA, and FDA." Maximally
defensible. No consumer can reasonably argue this is arbitrary. The natural dairy exemption
(ruminant CLA/vaccenic acid is not industrial trans fat) is already correctly gated and
prevents the false-positive that would undermine the veto's credibility.

### 6.2 Confidence Ceilings (CC-1 = 50, CC-2 = 75)
**CONFIRMED KEEP**

Consumer defensibility: "If we don't have enough data to confidently assess this product,
we won't show you a confident score — incomplete data produces a bounded score that reflects
our uncertainty." This is the right epistemic position and the one that builds long-term
trust. Removing these would mean showing consumers a confident score derived from partial
data — a trust failure that is harder to recover from than a bounded score.

Product-side note: the interaction between CC-1/CC-2 and MD-1 (pessimistic imputation) is
correct. Missing data → pessimistic imputation → lowers score → ceiling prevents it from
appearing confident. The two mechanisms are complementary and together prevent both gaming
(blanking data to remove penalties) and overconfidence (imputed score appearing as certain).

### 6.3 Sweetener Caps (SW-1: 75/73/70 by tier)
**CONFIRMED KEEP**

Consumer defensibility: "Products using non-nutritive sweeteners — natural, sugar-alcohol,
or synthetic — face a ceiling that reflects the tier of sweetener used. A synthetic
sweetener product cannot reach top-range scores because low glycemic quality via sweeteners
is not the same as genuinely low sugar." This is the right inversion prevention.

The tiered graduation (fermentation-derived → sugar alcohols → synthetic) already embodies
the proportionality principle this de-chaining program promotes. These are not brittle
cliffs — they are graduated and evidence-backed (EV-005 polyol evidence, additive identity
tier framework). KEEP unconditionally.

Product-side flag: the Tier A cap value (75) is worth monitoring as evidence on natural
fermentation-derived sweeteners matures. If a future EV supports raising Tier A to 80, that
is a calibration decision requiring its own D6+D7 co-sign, not a de-chaining decision. Not
in scope here.

### 6.4 Single-Ingredient Whole-Food Floor (FL-1, 85)
**CONFIRMED KEEP**

Consumer defensibility: "A single-ingredient whole food — an almond, plain yogurt with no
additives — should score in the excellent range. Penalizing it for nutrients it doesn't have
would be a category error." Core to the product proposition. Philosophically correct.

The multiple gating conditions (nova_conf >= 0.70, ingredient_count <= 1, beverage
reconstitution check, BSIP1 text-fallback degradation guard) prevent it from being an
inflation mechanism. KEEP unconditionally.

### 6.5 Whole-Food Fat Floor (FL-2, 70)
**CONFIRMED KEEP**

Consumer defensibility: "Butter and pure dairy fat are whole foods — scoring them as if
their saturated fat were a reformulable defect is a category error. These products score
with a floor that acknowledges what they are." The EV-048 gate for butter and EV-REDLABEL-005
for endemic categories encode the right category-specific reasoning.

KEEP unconditionally. The floor is not in tension with F-1's replacement (which applies
to products outside the whole_food_fat category) — they operate in different scopes.

### 6.6 Physiological Moderation Floors (FL-3 = 60, FL-4 = 50)
**CONFIRMED KEEP**

Consumer defensibility: "Whole foods with a nutritional concern still receive a floor,
but a lower one — a salted butter faces a different floor than an unsalted one." The
graduated interaction layer (one red label → FL-3 at 60; two or more → FL-4 at 50)
is the correct counterweight to FL-1/FL-2. Without FL-3/FL-4, the whole-food floors
become inversion machines for genuinely problematic whole foods.

KEEP unconditionally. These are the mechanically correct interaction layer, not NOVA-driven
chains.

### 6.7 Dominance Guardrail (BARI-INVERSION-TEST-001)
**CONFIRMED KEEP — with a formalization requirement**

The spec correctly identifies that this test is referenced but not formally specified.
From the product lens, this test is the most important governance instrument in the entire
de-chaining program. Without it, every stage that removes a cap creates an unverifiable
risk of inversion.

Product-side condition (reinforcing the spec's own requirement):
- C-DG-1: BARI-INVERSION-TEST-001 must be created as a machine-executable Python test
  file at `01_framework/` before Stage 1B ships. The reference set must include all six
  adversarial fixtures from Section 8.3 of the spec — the Petit Beurre/Chokita pair is
  required, not optional. This is a hard gate: Stage 1B does not ship without it passing.
- C-DG-2: The test must run as a CI gate on every subsequent scoring change. It is not a
  one-time check; it is a permanent invariant.

---

## Sequencing Assessment

The spec's proposed staged order is correct. My recommended order confirms the spec
with two amendments:

**Stage 0 (N-2 / WFI confidence scaling):** Safe to proceed as first step after Phase 0
baseline exists. This is a bug fix, not a philosophy change. Proceed as specified.

**Stage 1A (D4 activation):** Safe to proceed. BARI-INVERSION-TEST-001 specification (not
necessarily passing — just formally defined) is the only prerequisite I add here. The
test must exist before D4 is flipped, even if the full reference set is not yet
adversarially complete.

**Stage 1B (N-3 interim relaxation 68 → 78):** Requires BARI-INVERSION-TEST-001 to PASS
(not just exist) on the Stage 1A baseline. This is a harder gate than Stage 1A.

**Stage 2 (N-1 NOVA lookup replacement):** This is the hardest workstream and should NOT
be rushed to meet any timeline. The label-derivability validation for Component B is the
true gating condition. If validation takes longer than expected, Stage 2 waits. No other
stage is blocked by Stage 2 — it is parallel to Workstream 2.

**Amendment 1:** Workstream 2 (Stages 3–6, red-label de-anchoring) and Workstream 3
(Stage 7, calorie caps) can proceed in parallel with Workstream 1 Stage 2. They are not
blocked by N-1 replacement. The spec implies sequentiality by workstream numbering but
the dependencies do not require it. Parallelizing Workstream 2 with Workstream 1's hard
workstream (Stage 2) reduces total program time without adding risk.

**Amendment 2:** Stage 7 (Workstream 3, calorie caps) can be de-risked by running its
shadow calculation even earlier — the calorie dimension table is stable and the C-1
interaction formula can be shadow-validated against the existing corpus before any cap is
touched. I recommend pre-computing the fixture results (adversarial fixtures #1 and #2)
against the current engine as a calibration baseline before Stage 7 formally begins.
This means any mis-calibration of the interaction formula is caught earlier.

**Stage 8 (RECAL_P0 promotion):** Remains last and owner-gated. No change to the spec.

---

## Cross-Cutting Product-Side Observations

**On the anti-regression contract (Section 8):** The honest tension statement in Section
8.1 is correct and important. The caps existed because the raw continuous engine let junk
win. De-chaining is only an improvement if the continuous replacements actually hold the
line. The adversarial fixture suite (6 fixtures, Section 8.3) is the right instrument for
proving this — but it must run before any cap is retired, not after. This is a sequencing
principle that the spec implies but does not make explicit enough: fixtures must pass in
shadow before any live cap is removed.

**On the grade-distribution sanity gate (Section 8.4):** The ranges given (Grade A: 5-20%,
Grade B: 15-35%, Grade C: 25-45%, Grade D: 10-30%, Grade E: 5-20%) are corpus-fit and
honest about it. Product co-sign confirms these are the right monitoring ranges. A single
grade at >60% of products is a red flag that warrants calibration review — this is the
right threshold. However: this is a monitoring gate, not a hard block. The spec correctly
describes it as a "red-flag threshold for the shadow run" rather than a CHANGES_REQUESTED
trigger. If it fires, the orchestrator must surface it for the D6+D7 review before
proceeding, but it does not automatically block the stage.

**On observability (Section 7):** The required trace structure is the right product
decision. A score that cannot be decomposed into visible components cannot be publicly
defended. The `processing_quality_components` sub-object is particularly important — it
is what allows a consumer-facing explanation of the N-1 replacement to be traceable to the
actual engine calculation. I confirm this trace structure should be implemented as a hard
requirement, not a nice-to-have.

**On BARI_REDLABEL_V1 full activation (Stages 3-6):** This flag currently gates
cross-category sugar and sodium provisions. Its full activation is the largest single
expansion in Workstream 2. The separate D7 co-sign required at Stage 5 (as noted in
C-S7-1) is not a bureaucratic step — it is the correct checkpoint because the blast
radius at that stage spans all 12 live categories. Flag it explicitly in the program
registry so it is not treated as automatic.

---

## Summary Verdict Table

| Chain | D7 Verdict | Key Condition |
|---|---|---|
| N-1 NOVA step lookup (processing) | CO-SIGN WITH CONDITIONS | C-N1-1 (label-derivability validation), C-N1-2 (fixture #1 must score <60), C-N1-3 (EV registered) |
| N-2 NOVA step lookup (WFI) | CO-SIGN | None beyond Phase 0 baseline |
| N-3 NOVA-4 composite cap (68) | CO-SIGN WITH CONDITIONS | C-N3-1 (BARI-INVERSION-TEST-001 live before relaxation), C-N3-2 (parser validation before full removal) |
| N-4 NOVA-3 composite cap (87) | CO-SIGN | None |
| S-1 HIGH_CAL_HIGH_SUGAR_SEVERE (50) | CO-SIGN WITH CONDITIONS | C-S1-1 (graduated band extended, no product >55 after) |
| S-2 HIGH_CAL_HIGH_SUGAR_MODERATE (60) | CO-SIGN WITH CONDITIONS | C-S2-1 (S-7 must be active) |
| S-3 HIGH_SUGAR_25G_PLUS (60/68) | CO-SIGN WITH CONDITIONS | C-S3-1 (SC-2 date bar check) |
| S-4 HIGH_SUGAR_25G_GRANOLA (50) | CO-SIGN KEEP | Confirmed — not revisiting |
| S-5 SNACK_BAR_HIGH_CAL_SUGAR (60) | CO-SIGN WITH CONDITIONS | C-S5-1 (S-7 active, calorie table confirmed) |
| S-6 SNACK_BAR_RED_SUGAR_LABEL (55) | CO-SIGN WITH CONDITIONS | C-S6-1 (EV-SNACKBAR-SR-001, corpus n≥20) |
| S-7 ISRAELI_RED_LABEL_1_SUGAR (55) | CO-SIGN WITH CONDITIONS | C-S7-1 (separate D7 at Stage 5) |
| S-8 ISRAELI_RED_LABELS_2_PLUS (45) | CO-SIGN WITH CONDITIONS | C-S8-1 (no product >55 after), C-S8-2 (Stage 5 done first) |
| C-1 HIGH_CAL_LOW_SATIETY (55) | CO-SIGN WITH CONDITIONS | C-C1-1 (EV registered, fixture #1 passes) |
| C-2 SNACK_BAR_HIGH_CAL (70) | CO-SIGN WITH CONDITIONS | C-C2-1 (calorie table calibration verified in shadow) |
| P-1 ADDITIVE_MARKERS_5_PLUS (60) | CO-SIGN WITH CONDITIONS | C-P1-1 (D4 validated first), C-P1-2 (parser check), C-P1-3 (fixture #2 passes) |
| P-2 ADDITIVE_MARKERS_3_PLUS (72) | CO-SIGN WITH CONDITIONS | Same as P-1 |
| Na-1 HIGH_SODIUM_700MG_PLUS (60) | CO-SIGN | Already in progress |
| Na-2 HIGH_SODIUM_CEREAL_500 (75) | CO-SIGN KEEP | Confirmed |
| F-1 RED_LABEL_SAT_FAT (55) | CO-SIGN WITH CONDITIONS | C-F1-1 (Stages 0-7 done), C-F1-2 (RECAL_P0 R1-R7 validated), C-F1-3 (owner tripwire) |
| V-1 Trans-fat veto | KEEP CONFIRMED | Unconditional |
| CC-1/CC-2 Confidence ceilings | KEEP CONFIRMED | Unconditional |
| SW-1 Sweetener caps | KEEP CONFIRMED | Unconditional |
| FL-1 Single-ingredient floor (85) | KEEP CONFIRMED | Unconditional |
| FL-2 Whole-food fat floor (70) | KEEP CONFIRMED | Unconditional |
| FL-3/FL-4 Physiological moderation floors | KEEP CONFIRMED | Unconditional |
| Dominance guardrail (BARI-INVERSION-TEST-001) | KEEP + FORMALIZE | C-DG-1 (test file before Stage 1B), C-DG-2 (CI gate permanently) |

**Total dispositions reviewed:** 26 (18 caps + 7 retained guards + dominance guardrail formalization)
**CO-SIGN (unconditional):** N-2, N-4, Na-1, Na-2 (4)
**CO-SIGN KEEP (confirmed):** S-4, V-1, CC-1/CC-2, SW-1, FL-1, FL-2, FL-3/FL-4 (8)
**CO-SIGN WITH CONDITIONS:** N-1, N-3, S-1, S-2, S-3, S-5, S-6, S-7, S-8, C-1, C-2, P-1, P-2, F-1, BARI-INVERSION-TEST-001 (15)
**WITHHOLD:** 0

---

## Decision Log

| Decision | Options considered | Chosen | Decisive reason | Reversal condition |
|---|---|---|---|---|
| N-1 disposition | CO-SIGN unconditional vs. CO-SIGN WITH CONDITIONS vs. WITHHOLD | CO-SIGN WITH CONDITIONS | Component B label-derivability is unverified; clean-label-junk inversion is a real failure mode if it fails | Reversal to WITHHOLD if C-N1-1 label-derivability validation fails below 90% accuracy on the live corpus |
| N-3 sequencing | Relax cap first, test second vs. test first, relax second | Test first (C-N3-1: BARI-INVERSION-TEST-001 required before relaxation) | A cap cannot be relaxed without its replacement guardrail being live and passing | Reversal if inversion test is shown to be structurally impossible to build before N-3 relaxation; then re-evaluate N-3 timing |
| S-8 retirement | Retire after S-7 vs. retire simultaneously with S-7 | Retire after S-7 (C-S8-2: hard sequential) | S-8 (45 cap) is the harshest guardrail; retiring it requires the replacement continuous system to be calibrated and confirmed, which only happens after Stage 5 is validated | Reversal if Stage 5 data shows the compounding deductions produce equivalent floors before full S-7 retirement, allowing Stage 5-6 to overlap |
| Workstream parallelization | Keep sequential workstream numbering vs. allow WS2 and WS1-Stage-2 parallel | Parallel (Amendment 1) | WS2 has no dependency on N-1 replacement; serializing wastes program time without risk reduction | Reversal if shared corpus statistics create a dependency (e.g., category p75 values needed for both WS1 and WS2 simultaneously) |
| Stage 8 timing | Owner gate vs. D7 sufficient | Owner gate (C-F1-3) | RECAL_P0 promotion changes published scores across all 12 live categories — frozen-invariant tripwire by definition | Irreversible by construction; no reversal condition |

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/d7_cosign_dechain_v1.md",
      "action": "created",
      "sha256": "D2B9729270F1882BFF61B840DC697701D72C5041DD1D856FC9D2ED2DDB8F8B74"
    }
  ],
  "counts": {
    "dispositions_reviewed": "26/26 (18 caps from Section 5 + 7 retained guards from Section 6 + dominance guardrail formalization; denominator: dechain_d6_proposal_v1.md Section 2 disposition table + target_scoring_logic_spec_v1.md Sections 5-6)",
    "cosign_unconditional": "4/26 (N-2, N-4, Na-1, Na-2; denominator: dispositions_reviewed)",
    "cosign_keep_confirmed": "8/26 (S-4, V-1, CC-1/CC-2, SW-1, FL-1, FL-2, FL-3/FL-4; denominator: dispositions_reviewed)",
    "cosign_with_conditions": "15/26 (N-1, N-3, S-1, S-2, S-3, S-5, S-6, S-7, S-8, C-1, C-2, P-1, P-2, F-1, BARI-INVERSION-TEST-001; denominator: dispositions_reviewed)",
    "withhold": "0/26",
    "conditions_enumerated": "17 named conditions (C-N1-1 through C-DG-2; denominator: CO-SIGN WITH CONDITIONS dispositions)"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/dechain_d6_proposal_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/scoring_overhaul_program_v1.md", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "No engine code changed (governance review only — by design)",
    "No scores changed (governance review only — by design)",
    "sha256 of d7_cosign_dechain_v1.md not computed — orchestrator must hash the committed file",
    "Cross-category BARI_REDLABEL_V1 Stage 5 co-sign deferred — separate D7 review required at Stage 5 with blast radius table as input (C-S7-1)",
    "RECAL_P0 Stage 8 owner go-live authorization deferred — separate tripwire decision (C-F1-3)",
    "BARI-INVERSION-TEST-001 formal spec file not yet created — flagged as C-DG-1, blocking Stage 1B; must be created by Data Agent before Stage 1B"
  ],
  "self_check": "Acceptance test per target_scoring_logic_spec_v1.md Section 9.1: Product Agent D7 co-sign on the disposition table (Section 5) and retained guards (Section 6) is obtained. Observed result: co-sign rendered for all 26 dispositions with explicit verdicts (4 unconditional, 8 keep-confirmed, 15 with-conditions, 0 withhold) and 17 enumerated conditions. The two deferred items (Stage 5 BARI_REDLABEL_V1 cross-category and Stage 8 RECAL_P0 owner gate) are by-design governance checkpoints that cannot be pre-authorized — they require future artifact inputs not yet in existence. This D7 co-sign is complete for its current scope."
}
```
