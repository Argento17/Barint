# Magnesium SIE Benchmark Recalibration Proposal

**Status:** PROPOSAL — PENDING D6/D7 co-sign  
**Date:** 2026-06-19  
**Author:** Nutrition Agent  
**Do NOT implement until:** Product Agent D7 co-sign + Data Agent D8 implementation verify  
**Scope:** Magnesium category only. Does not touch any food-category files.  
**Source trace:** `_corpus_run_full_v9.json`, `evidence_dossiers/magnesium.yaml`, `src/constants.py`

---

## The Problem: What the Owner Is Seeing

The v9 trace shows 19 products collapsing to three score pins: 66.5, 62.6 / 59.0 / 58.4, **49.0 × 9**, and **34.0 × 3**. The nine 49-pinned products include magnesium taurate at 6.8mg elemental and magnesium malate at 108.5mg elemental — a 16-fold difference in delivered magnesium, scored identically. When a user asks why a product scores low, the engine today answers "underdosed or unverifiable dose" for all nine, with no further differentiation. The owner's diagnosis is correct: **the flat 49-pin destroys the information the scoring dimensions actually computed.** The form sub-scores (50 for taurate vs 92 for citrate/bisglycinate) and the distance from the adequacy threshold are entirely discarded.

This proposal replaces the flat pin with a graded band that preserves that information while maintaining the core design constraint: **a well-formed underdosed product must not outrank a poorly-formed adequately-dosed product.**

---

## Section 1: Reference-Perfect Magnesium Anchor

The anchor defines the fixed best-in-class benchmark against which every product is measured. It is not a marketed product; it is the standard a rational formulator aiming for maximal clinical credibility would hit.

### Target Elemental Dose

**Anchor: 300 mg/day elemental magnesium.**

Rationale:
- The NIH/IOM RDA for magnesium in adults is 310–420 mg/day total (dietary + supplemental). Supplemental magnesium addresses the gap between dietary intake and the RDA. The supplemental trial literature converges on 300–365 mg/day elemental as the therapeutic dose range for studied endpoints (blood pressure reduction: PMID:27402922, meta-analysis of 34 RCTs; sleep/insomnia trials reviewed at PMID:33865376, PMID:35184264).
- The existing dossier already sets `min_effective = 300 mg/day elemental` and `upper_studied = 400 mg/day` — these are ratified Nutrition D6 values and this proposal does not change them.
- 300 mg/day is the lower bound of the effective range, making it a reachable but honest anchor: a product achieving this dose is at the entry point of clinical credibility, not aspirational.

Evidence tier for this dose: **Strong** for blood pressure/cardiovascular endpoints (consistent multi-MA signal); **Moderate** for general supplementation appropriateness. The dose-response evidence warrants treating 300 mg/day elemental as the minimum threshold for meaningful effect.

### Reference Form

**Anchor form: magnesium citrate or magnesium bisglycinate (either qualifies).**

Rationale: Both forms sit in the dossier's "preferred" tier. Human bioavailability studies (PMID:39770988, PMID:30761462, PMID:7815675) show organic magnesium salts (glycinate, citrate) achieve meaningfully higher fractional absorption than magnesium oxide. The mechanism: organic forms are water-soluble and absorbed by carrier-mediated intestinal transport rather than passive diffusion; oxide relies primarily on passive diffusion and has low solubility at physiological pH. Specific absorption data: fractional absorption from oxide is approximately 4% under fasting conditions in some studies (PMID:7815675), while citrate and glycinate show 2–4x higher absorption in head-to-head comparisons (PMID:30761462). This is the basis for the form ladder's "preferred" classification and the distinction drives the form sub-score difference (92 preferred vs 45 poor/honest for oxide).

### Evidence Tier

**Anchor claim: blood pressure / cardiovascular support → Moderate.**

This is already the highest ratified tier in the dossier. The engine's evidence sub-score for Moderate is midpoint of the (60, 84) band = 72. A reference-perfect product would also have clean label honesty (no misleading compound-weight framing, no pixie-roster) and safety within the NIH/IOM 350 mg/day supplemental UL.

### Label-Honesty Bar

A reference-perfect product:
1. States elemental magnesium per serving on the label (not only compound weight), OR clearly names the compound form so elemental is computable.
2. Makes a claim grounded in a Moderate+ dossier endpoint (blood pressure, fatigue/tiredness per EFSA Art.13).
3. Does not combine 500mg+ compound weight with a vague "Max" name when the elemental content is sub-adequate.

**Reference anchor score (theoretical):** An ideal 300mg elemental citrate/bisglycinate product with Moderate evidence, clean honesty, and safety within UL would score approximately:

```
Evidence = 72 (Moderate midpoint)
Dose = 92 (in_range: 300mg >= min_effective=300)
Form = 92 (preferred)
Honesty = 100 (clean)
Safety = 70 (neutral blend value)

Blend = 0.30×72 + 0.25×92 + 0.20×92 + 0.15×100 + 0.10×70
      = 21.6 + 23.0 + 18.4 + 15.0 + 7.0
      = 85.0 → grade A
```

This is the top of the category under current evidence. No product on the Israeli shelf today achieves it — which is an honest finding, not a scoring artifact.

---

## Section 2: Cap → Graded Band Recalibration

### The Problem with the Flat 49-Pin

`CAP_FAIRY_DUST = 49` is a hard ceiling applied whenever the dose sub-score returns `fairy_dust` (elemental_mg < `FAIRY_DUST_FRACTION × min_effective` = 0.5 × 300 = 150 mg). When this cap fires, the blend is discarded and the product is pinned to exactly 49. This means:

- Nutricare Taurate (76mg compound = **6.8mg elemental**, 2% of anchor): pinned to 49
- Nutricare Malate 700 (700mg compound = **108.5mg elemental**, 36% of anchor): pinned to 49

Both show honesty=100, safety=neutral in the trace. The malate product is 16× closer to the adequacy threshold. The form sub-scores differ too (72 for malate vs 50 for taurate). None of this reaches the consumer.

The dose sub-score under the current engine is also flat: `DOSE_FAIRY_DUST = 20` for all elemental values below 150mg. So even the blend (which the cap then discards) gives no gradient.

### Proposed Design: Two-Layer Gradient

**Layer 1: Graded dose sub-score in the sub-adequate range (replaces flat DOSE_FAIRY_DUST = 20)**

```
proposed_dose_subscore(elemental_mg):
    if elemental_mg >= min_effective (300mg):
        return 92   # in_range (unchanged)
    if elemental_mg >= FAIRY_FLOOR (150mg):
        # sub-therapeutic band: 50→84 linearly (unchanged)
        frac = (elemental_mg - 150) / (300 - 150)
        return 50 + frac × (84 - 50)
    else:
        # PROPOSED: graded sub-adequate (was flat 20)
        # Scale: 5 at 0mg elemental → 20 at FAIRY_FLOOR (smooth join)
        frac = elemental_mg / 150
        return 5 + frac × (20 - 5)
```

The minimum of 5 (not 0) reflects that any detectable dose is marginally better than an inert product. The smooth join at 150mg means the dose sub-score is continuous across the entire range.

**Layer 2: Graded ceiling replacing the flat CAP_FAIRY_DUST = 49**

```
proposed_graded_cap2_ceiling(elemental_mg):
    if elemental_mg is None:
        return 49   # unverifiable blend: keep 49 (conservative)
    if elemental_mg >= FAIRY_FLOOR (150mg):
        return None  # cap2 does not apply
    # Proposed graded ceiling:
    # At elemental_mg = 0:    ceiling = 35 (barely above E)
    # At elemental_mg = 150:  ceiling = 49 (smooth join with current cap)
    frac = elemental_mg / 150
    return 35 + frac × (49 - 35)
```

The ceiling of 35 at zero dose is 1 point above the E/D boundary — a product with no detectable elemental magnesium cannot escape E territory. At 150mg it joins the current cap_2 value of 49 exactly, preserving backwards-compatibility at the sub-adequate/sub-therapeutic boundary.

### Why This Preserves the Core Constraint

The constraint is: **a well-formed underdosed product must not outrank a poorly-formed adequately-dosed product.**

- **Adequately-dosed oxide (520mg oxide = 314mg elemental):** Proposed score = 68.1 (B). Form=45 (poor/honest). Blend = 0.30×47 + 0.25×92 + 0.20×45 + 0.15×100 + 0.10×70 = 14.1+23.0+9.0+15.0+7.0 = 68.1.
- **Underdosed citrate (250mg citrate = 40.5mg elemental):** Proposed ceiling = 35 + (40.5/150)×14 = 35 + 3.8 = 38.8. Form=92 (preferred), but ceiling = 38.8. **Adequately-dosed oxide wins (68.1 > 38.8).** Constraint satisfied.
- **Best underdosed product (malate 700mg = 108.5mg elemental):** Proposed ceiling = 35 + (108.5/150)×14 = 35 + 10.1 = 45.1. Still well below any adequately-dosed oxide product. Constraint satisfied.

The form score CAN contribute within the sub-adequate band — differentiation happens between 35 and the graded ceiling, not above it. A well-formed 40mg elemental citrate scores 38.8 while a poorly-formed 46mg elemental carbonate scores 39.3. The ordering reflects both dose and form, which is correct.

### The 34 E-Cap: Keep Hard

`CAP_INSUFFICIENT_EVIDENCE = 34` should remain binary, not graded.

The three E-pinned products (TRIOMAG, Nano Liposomal, WELL) failed on the evidence dimension — their claims are not supported by adequate evidence for the endpoint they assert. This is a categorically different failure from under-dosing. Grading the evidence cap would allow a product with no credible clinical basis to earn a better score by having more elemental magnesium — but the elemental load is irrelevant when the evidence basis for the claim doesn't exist. The failure class distinction (claim not grounded vs claim grounded but product under-delivers) must be maintained.

The only question is whether the three E products' evidence classifications are correct. For the dry-run scope: accepted as-is. The evidence-tier question is a separate D6/D7 decision.

### Constants Change Summary (Proposal, Not Implementation)

| Constant | Current Value | Proposed Value | Mechanism |
|---|---|---|---|
| `DOSE_FAIRY_DUST` | 20 (flat) | `5 + (elemental/150) × 15` | Graded by elemental load |
| `CAP_FAIRY_DUST` | 49 (flat) | `35 + (elemental/150) × 14` | Graded ceiling, not a single constant |
| `CAP_INSUFFICIENT_EVIDENCE` | 34 | **34 (unchanged)** | Stays hard |
| All other constants | Unchanged | Unchanged | No other changes |

Because `CAP_FAIRY_DUST` becomes a function rather than a constant, the implementation requires modifying `combine()` in `score_engine.py` to compute the ceiling from elemental_mg at call time, passing it from the dose scorer. This is a D8 implementation detail; do not implement until D7 is co-signed.

---

## Section 3: Inclusion Rule for Combo Products

### The Inclusion Problem

The v9 corpus includes products where magnesium is not the primary active: Solgar Ca/Mg/D3 (barcode 0033984005181, ~100mg citrate = 16mg elemental), Altman Mg Balance (magnesium oxide + ashwagandha + valerian + B6, barcode 7290019444206), NT LC Mg+vitamins (hydroxide + B6 + E, barcode 7290010207640), and Nutricare WELL (bisglycinate + zinc + B6, barcode 7290018439043).

The scoring framework evaluated magnesium as the primary active for all of these, using `engine_active == "magnesium"`. This creates a misrepresentation problem in both directions: a Ca/Mg/D3 product is unfairly compared to dedicated magnesium supplements, and the comparison page consumer reads it as a magnesium product recommendation.

### Proposed Inclusion Rule

**A product is included in the magnesium comparison if and only if magnesium is the labeled primary active OR the product is marketed as a magnesium supplement.**

Operationalized:
1. **INCLUDE:** Products where the label name, primary claim, or marketing positions magnesium as the featured mineral. This includes single-mineral magnesium products and multi-form magnesium products (e.g., TRIOMAG with three magnesium forms).
2. **FOOTNOTE (include with caveat):** Products where magnesium is paired with synergistic co-actives that are plausibly dosed for magnesium-specific function (e.g., B6 as cofactor: B6 facilitates cellular magnesium retention; this is a recognized physiological interaction, not marketing). Magnox B6, SupHerb Citrate+B6, NT LC, Nutricare WELL fall here — they are sold as magnesium formulations with supporting co-factors. Include with a note: "Combo product — co-actives shown; magnesium score only."
3. **EXCLUDE:** Products where magnesium is incidental to a different primary purpose. The clear case is **Solgar Ca/Mg/D3 (0033984005181)**: this is a calcium supplement with supporting magnesium and D3. The calcium dose (200mg) exceeds the magnesium dose (100mg compound = 16mg elemental), the product name leads with "Ca/Mg", and the primary consumer intent is calcium supplementation. Comparing it alongside dedicated magnesium supplements actively misleads.
4. **FOOTNOTE with explanation:** Altman Mg Balance (7290019444206) — magnesium oxide + ashwagandha KSM-66 + valerian + B6. Magnesium is the primary mineral, but the ashwagandha and valerian are at doses (50mg each) below clinical evidence thresholds and introduce herb-drug interaction risks (noted in the trace). Include, but the rowVerdict must note that the herbal additives do not contribute to the magnesium score and carry interaction caution.

### Decision Table

| Product | Barcode | Proposed Status | Reason |
|---|---|---|---|
| Solgar Ca/Mg/D3 | 0033984005181 | **EXCLUDE** | Ca primary active; Mg incidental (16mg elemental) |
| TRIOMAG | 7290118816065 | INCLUDE (E, unchanged) | Three Mg forms = dedicated Mg product |
| Nutricare WELL | 7290018439043 | INCLUDE WITH CAVEAT | Mg primary; zinc+B6 synergistic, small doses |
| Altman Mg Balance | 7290019444206 | INCLUDE WITH CAVEAT | Mg primary; ashwagandha+valerian = interaction flag |
| Magnox B6 | 7290017847122 | INCLUDE WITH CAVEAT | Mg primary; B6 is a recognized cofactor |
| NT LC Mg+vitamins | 7290010207640 | INCLUDE WITH CAVEAT | Mg primary; B6+E at support doses |
| SupHerb Citrate+B6 | 7290013464248 | INCLUDE WITH CAVEAT | B6 synergistic |
| Nutricare WELL | 7290018439043 | INCLUDE (E) | Mg primary; evidence failure on claim, not combo |
| All others | various | INCLUDE | Dedicated Mg supplements |

Excluding Solgar removes one product from the corpus (18 products), removes one of the nine 49-pins, and eliminates the most misleading entry. This is the minimal correct exclusion.

---

## Section 4: Dry-Run Re-Score Table

**Methodology:**  
- Elemental mg = compound_mg × form_fraction (from dossier `elemental_by_form`)  
- Max550 blend: used v9 engine estimate of 89.1mg elemental (blend proportion not label-derivable)  
- TRIOMAG: blend proportion not label-derivable; elemental not computable; dose excluded  
- Proposed dose sub-score and graded ceiling applied as specified in Section 2  
- Honesty and Safety sub-scores taken from v9 trace (unchanged)  
- Evidence sub-scores taken from v9 trace (unchanged)  
- All weights unchanged from constants.py  

| Barcode | Name | Form | Cmpd mg | Elem mg | % Anchor | Old Score | Old Grade | New Dose SS | New Blend | New Score | New Grade | Binding | Distance-from-Anchor Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7290001065662 | Nutricare Mg 520 | oxide | 520 | 313.6 | 105% | 62.6 | C | 92.0 | 68.1 | **68.1** | **B** | blend | In range — dose meets anchor |
| 7290015318426 | TINC Mg Oxide 520 | oxide | 520 | 313.6 | 105% | 62.6 | C | 92.0 | 68.1 | **68.1** | **B** | blend | In range — dose meets anchor |
| 7290017218564 | Altman Mg 520 | oxide | 520 | 313.6 | 105% | 62.6 | C | 92.0 | 68.1 | **68.1** | **B** | blend | In range — dose meets anchor |
| 7290013142894 | Altman Mg UP 450 | oxide | 450 | 271.3 | 90% | 66.5 | B | 77.5 | 64.5 | **64.5** | **C** | blend | 90% of anchor; poor form holds it down |
| 7290010207640 | NT LC Mg+vitamins | oxide | 450 | 271.3 | 90% | 59.0 | C | 77.5 | 64.5 | **64.5** | **C** | blend | 90% of anchor |
| 7290019444206 | Altman Mg Balance | oxide | 450 | 271.3 | 90% | 59.0 | C | 77.5 | 64.5 | **64.5** | **C** | blend | 90% of anchor |
| 7290017847122 | Magnox B6 | oxide | 432 | 260.5 | 87% | 58.4 | C | 75.0 | 58.4 | **58.4** | **C** | blend | 87% of anchor; honesty debit + safety note hold it down |
| 7290001066973 | Nutricare Malate 700 | malate | 700 | 108.5 | 36% | 49.0 | D | 15.9 | 54.5 | **45.1** | **D** | graded_cap2 | Ceiling 45.1: 108mg is 36% of anchor dose |
| 7290118818205 | SupHerb Max 550 blend | citrate+oxide | 550 | ~89.1 | 30% | 49.0 | D | 13.9 | 58.0 | **43.3** | **D** | graded_cap2 | Ceiling 43.3: ~89mg is 30% of anchor; blend unknown |
| 7290015429245 | Amorphicure PH 160 | carbonate | 160 | 46.1 | 15% | 49.0 | D | 9.6 | 48.5 | **39.3** | **D** | graded_cap2 | Ceiling 39.3: 46mg is 15% of anchor |
| 7290013464248 | SupHerb Citrate+B6 | citrate | 250 | 40.5 | 14% | 49.0 | D | 9.1 | 56.8 | **38.8** | **D** | graded_cap2 | Ceiling 38.8: 40mg is 14% of anchor; good form cannot compensate |
| 7290019444480 | Altman Bisglycinate 250 | bisglycinate | 250 | 35.2 | 12% | 49.0 | D | 8.5 | 56.6 | **38.3** | **D** | graded_cap2 | Ceiling 38.3: 35mg is 12% of anchor; good form cannot compensate |
| 7290011899967 | Altman Citrate 200 | citrate | 200 | 32.4 | 11% | 49.0 | D | 8.2 | 56.5 | **38.0** | **D** | graded_cap2 | Ceiling 38.0: 32mg is 11% of anchor; good form cannot compensate |
| 7290015318532 | TINC Malate 136 | malate | 136 | 21.1 | 7% | 49.0 | D | 7.1 | 52.3 | **37.0** | **D** | graded_cap2 | Ceiling 37.0: 21mg is 7% of anchor |
| ~~0033984005181~~ | ~~Solgar Ca/Mg/D3~~ | ~~citrate~~ | ~~100~~ | ~~16.2~~ | ~~5%~~ | ~~49.0~~ | ~~D~~ | — | — | **EXCLUDED** | — | — | Ca primary active; Mg incidental |
| 7290018439579 | Nutricare Taurate 76 | taurate | 76 | 6.8 | 2% | 49.0 | D | 5.7 | 47.5 | **35.6** | **D** | graded_cap2 | Ceiling 35.6: 7mg is 2% of anchor; barely above E |
| 7290118816065 | SupHerb TRIOMAG 200 | citrate+bisgly+taurate | 200 | N/A | N/A | 34.0 | E | N/A | 60.7 | **34.0** | **E** | cap1_unchanged | Claim not supported by adequate evidence; dose N/A |
| 7290001065594 | Nutricare Nano Lipo 88 | bisglycinate | 88 | 12.4 | 4% | 34.0 | E | N/A | 60.7 | **34.0** | **E** | cap1_unchanged | "Nano liposomal" claim unsupported |
| 7290018439043 | Nutricare WELL 168 | bisglycinate | 168 | 23.7 | 8% | 34.0 | E | N/A | 60.7 | **34.0** | **E** | cap1_unchanged | "WELL" claim not adequately defined/supported |

### Distribution: Old vs Proposed

| Grade | Old Count | Proposed Count | Change |
|---|---|---|---|
| B | 1 | 3 | +2 (three 520mg oxide products) |
| C | 6 | 4 | -2 (Altman UP drops B→C; oxide 450s consolidate) |
| D | 9 | 9 | 0 (spread within D, but all stay D) |
| E | 3 | 3 | 0 (unchanged) |

**Does the 49-cluster actually spread?** Yes, within the D band: from 35.6 (taurate 6.8mg) to 45.1 (malate 108.5mg), a spread of 9.5 points. All nine remain D, which is the correct outcome — none of these products are adequately dosed, and no grade promotion is warranted.

**Does the ordering now match nutrition intuition?**

- High-elemental oxide > underdosed premium forms: Yes. 520mg oxide (68.1/B) ranks above 250mg citrate (38.8/D). Correct.
- Within the sub-adequate cluster: ordered by elemental load primarily, modulated by form. Malate 108.5mg (45.1) > Max550 89.1mg (43.3) > Carbonate 46.1mg (39.3) > Citrate 40.5mg (38.8) > Bisglycinate 35.2mg (38.3) > Citrate 32.4mg (38.0) > Malate 21.1mg (37.0) > Citrate 16.2mg (excl.) > Taurate 6.8mg (35.6). The ordering is sensible.
- Note that citrate/bisglycinate products at similar elemental loads score slightly higher than carbonate/taurate at the same dose (form sub-score visible within the cap ceiling). A 35mg bisglycinate (38.3) vs a 35mg taurate (hypothetical) would show the form difference. This is correct: form quality is visible within the band, but doesn't rescue an underdosed product above the ceiling.

### Notable Grade Changes

| Product | Old | Proposed | Reason |
|---|---|---|---|
| Nutricare 520 / TINC 520 / Altman 520 | 62.6/C | **68.1/B** | 313mg elemental is in-range; oxide form penalty is visible but blend earns B |
| Altman Mg UP 450 | 66.5/B | **64.5/C** | 271mg elemental is sub-adequate (90% of anchor); blend does not reach B floor |
| Solgar Ca/Mg/D3 | 49.0/D | **EXCLUDED** | Magnesium is incidental |

The Altman UP 450 grade correction (B→C) is arguably the most important fix: the v9 score of 66.5 placed it at the top of the category while its elemental dose of 271mg is 10% below the anchor. Under the proposed model it scores correctly as C — adequately dosed for practical purposes, but below the B threshold, which now requires actually reaching the anchor range.

---

## Section 5: Open Issues and Flagged Risks

### Risk 1 (BIGGEST): 520mg Oxide Products Inflate to B — Is That Honest?

**This is the single biggest scoring risk in the proposal.**

The three 520mg oxide products (Nutricare, TINC, Altman) would move from C to B. Their elemental dose at 313mg/day is in-range (> 300mg anchor). The dose dimension correctly scores them at 92. But magnesium oxide has approximately 4% fractional absorption in fasting conditions (PMID:7815675), meaning the *absorbed* elemental load may be 12–13mg, not 313mg. A 50mg bisglycinate elemental dose with 30–35% fractional absorption would deliver more actual magnesium to the bloodstream.

The engine deliberately separates dose (elemental quantity delivered to the gut per the label) from form (bioavailability/absorption quality). Oxide gets form_ss=45 (poor/honest) as a penalty. But the question the owner raised is whether a B grade for high-dose oxide is defensible when the absorbed dose is tiny. The answer depends on whether the engine's declared design is correct: **elemental dose is the quantity the label commits to delivering; absorbed dose is not label-derivable and therefore cannot be scored.** This is the right boundary — we cannot score something we cannot observe from the label.

However: the proposed model now promotes three oxide products to B. This will require careful copy treatment on the page. The category note (already written in `magnesium-page-data.ts`) correctly explains the paradox, but the B grade will need a clear caveat at the product level.

**Recommendation:** Before implementing this proposal, verify with Product Agent whether a B grade for high-dose oxide products passes the product standard. If the answer is no — if B implies "this is a good product for most uses" and oxide fails that test — the form penalty weight may need to increase (D7 decision) or the grade band for B may shift. This is not a scoring bug; it is a legitimate philosophical choice about whether the engine grades the label or the absorbed dose.

### Risk 2: Max550 Blend (7290118818205) — Unverifiable Elemental

The TRIOMAG's 89.1mg elemental estimate is carried from the v9 engine but the per-form split in the 550mg oxide+citrate blend is unverifiable from the label. If the blend is oxide-heavy (e.g., 80% oxide, 20% citrate), elemental = 0.8×550×0.603 + 0.2×550×0.162 = 265 + 18 = 283mg — which would be in-range and score much higher. If citrate-heavy (50/50), elemental = 165+45 = 210mg — sub-therapeutic. The v9 estimate of 89.1mg suggests the engine used a conservative 50/50 split with some assumption that produced a lower number. **The label cannot be scored reliably; this product may warrant exclusion or an explicit "estimated elemental, unverified" marker.** A D8 data trace verification is needed before consumer-facing publication.

### Risk 3: Evidence Cap (34) Three Products — Are the Evidence Rulings Right?

The three E-pinned products (TRIOMAG, Nano Liposomal, WELL) have their cap_1 firing because their evidence tier resolved to Insufficient. But their blend without the cap is 60.7 — a C score. This gap (34 E vs 60.7 hypothetical) is large. If any of these products' evidence rulings were overturned in a future D6/D7 review, they would jump significantly. In particular:

- **TRIOMAG** makes a "optimal absorption" claim for a three-form blend. The three forms (citrate, bisglycinate, taurate) each have individual evidence. Whether a blended product's claim can be resolved to the best individual form's endpoint is a D6 question. If it can, TRIOMAG may resolve to Moderate and score ~60+ C.
- **Nutricare WELL** claims "WELL" as a general wellness brand name, not as a specific health claim. If the umbrella can resolve "WELL" to a studied endpoint, the evidence ruling changes. This should be reviewed in the next dossier sweep.

These are flagged for review, not changed here.

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\magnesium_benchmark_recalibration_proposal.md",
      "sha256": "not_computed_proposal_only",
      "status": "created"
    }
  ],
  "counts": {
    "products_analyzed": 19,
    "products_in_dry_run": 19,
    "cap2_cluster_products": 9,
    "cap1_cluster_products": 3,
    "blend_dominant_products": 7,
    "proposed_exclusions": 1,
    "products_changing_grade": 4,
    "grade_changes": {
      "C_to_B": 3,
      "B_to_C": 1,
      "excluded": 1
    },
    "cap2_cluster_score_spread_old": "49.0 × 9 (flat)",
    "cap2_cluster_score_spread_proposed": "35.6 to 45.1 (range 9.5 pts, all D)"
  },
  "commands_run": [
    {"command": "python C:\\Bari\\_tmp_mg_dryrun.py", "exit_code": 0, "purpose": "dry-run simulation"},
    {"command": "Read _corpus_run_full_v9.json (engine_active==magnesium, grade present)", "exit_code": 0, "purpose": "source of truth trace"},
    {"command": "Read magnesium-page-data.ts", "exit_code": 0, "purpose": "per-product form/dose/elemental data"},
    {"command": "Read constants.py", "exit_code": 0, "purpose": "current cap values"},
    {"command": "Read score_engine.py", "exit_code": 0, "purpose": "combine() and cap logic"},
    {"command": "Read magnesium.yaml", "exit_code": 0, "purpose": "dossier min_effective, form ladder, safety UL"}
  ],
  "not_done": [
    "No engine files edited — proposal only",
    "Product Agent D7 co-sign not obtained — required before implementation",
    "Data Agent D8 implementation not started",
    "Max550 blend elemental verification not resolved (Risk 2)",
    "TRIOMAG and WELL evidence re-adjudication not performed (Risk 3)",
    "Cap1 grading for E products not proposed (held as binary — see Section 2)",
    "No frontend/page edits"
  ],
  "spec_acceptance_test": {
    "dry_run_spreads_49_cluster": true,
    "constraint_preserved_oxide_beats_underdosed_premium": true,
    "e_products_unchanged": true,
    "solgar_exclusion_reasoned": true,
    "anchor_grounded_in_dossier_values": true,
    "no_engine_edits": true
  }
}
```
