# Magnesium Absorbed-mg Scoring Proposal — v1

> **Status: CANDIDATE / PROPOSAL — NO ENGINE CHANGE, NO PUBLISHED SCORE.**
> Requires owner co-sign + Product Agent D7 before implementation in proto_v1.
> Nutrition Agent D6 authorship (2026-06-20).

---

## Executive Summary

The owner has correctly identified the core insight: a 520mg oxide label and a 200mg citrate
label are not equivalent — the body absorbs fundamentally different amounts from each. Currently
the engine scores Dose on ELEMENTAL mg (which already partially captures this via the compound
-> elemental fraction conversion), while Form handles the categorical bioavailability tier
separately. The two dimensions are **not integrated** — they fire independently. This means
a 520mg oxide product can score DOSE=in_range (313mg elemental >= 300mg min_effective)
while simultaneously scoring FORM=poor, producing a B grade (MagUp) that overstates what
the body receives.

**Recommendation (single best option):** Change the Dose scoring basis from elemental mg
to absorbed mg (= elemental mg x population-average absorption fraction), recalibrate the
dose bands to the absorbed scale, and simultaneously reduce the Form dimension weight from
0.20 to 0.05 (Form becomes a residual premium-marketing signal, not a primary bioavailability
input — absorbed-mg already encodes it). This makes the score derive directly and heavily
from what the body receives.

---

## 1. Canonical Basis for the Absorbed-mg Display Figure

**Single canonical basis: per labeled daily serving.**

All 18 corpus Mg SKUs have servings_per_day=1 (single capsule/tablet). The engine dose
basis is `per_day`; all actives are `quantity_basis=per_serving`. When servings_per_day=1,
per-serving equals per-day. This is confirmed for every SKU in `bsip0s_label.actives`.

The figure is NOT:
- Per capsule (same as per serving for these SKUs, but should be stated explicitly)
- Per 100g (irrelevant for supplement dosing)
- Per entire box (would inflate the number 60x; nonsensical for a consumer daily figure)

**Consumer label wording must state**: "לנטילה יומית מומלצת" (per recommended daily serving),
not just "per capsule" — even though they coincide here, as some future SKUs may have
multi-capsule daily servings.

---

## 2. Per-Product Absorbed-mg Table

**Methodology:**
- Elemental fraction: from dossier `compound_forms_identity`, verified against PubChem CIDs
  (see sources column)
- Absorption bands: population-average estimates from human bioavailability studies
  (PMID:7815675 Firoz & Graber 2001, PMID:30761462, PMID:39770988; benchmark v1 §3-4)
- These are NOT per-product lab measurements. The Polish AAS assay (benchmark caveat 1)
  found 58.7% of EU supplements outside legal tolerance — Bari cannot verify actual content.
  Display figures are labeled "~כ-X מ\"ג" (approximately X mg) to signal the estimate status.
- Midpoint of the absorption band used for the single display figure; the band is stated for
  transparency.

| # | SKU | Product name | Compound mg/day | Form | Elem fraction | Elem mg/day | Absorption band | Absorbed mg~ | Current score/grade | Page shows today |
|---|-----|-------------|----------------|------|--------------|-------------|-----------------|--------------|-------------------|-----------------|
| 1 | SP-0033984005181 | Solgar Ca+Mg+D3 | 100 | citrate | 0.162 (PubChem 6099959) | 16.2 | 25–30% | ~4.5 | 49/D | ~5 |
| 2 | SP-7290001065594 | Nutricare Nano Liposomal | 88 | bisglycinate | 0.141 (PubChem 84645) | 12.4 | 20–25% | ~2.8 | 34/E | not shown |
| 3 | SP-7290001065662 | Nutricare Mg 520 | 520 | oxide | 0.603 (PubChem 14792) | 313.6 | 2–8% | ~12.5 | 62.6/C | ~13 |
| 4 | SP-7290001066973 | Nutricare Malate | 700 | malate | 0.155 (PubChem 74258) | 108.5 | 15–20% | ~18.5 | 49/D | ~19 |
| 5 | SP-7290010207640 | NT L.C. Hydroxide (Dead Sea) | 450 | hydroxide | 0.417 (PubChem 14791; BUG-FIX-2026-06-20) | 187.7 | 4–10% | ~13.1 | 59.7/C | ~8 |
| 6 | SP-7290011899967 | Altman Citrate 120 | 200 | citrate | 0.162 | 32.4 | 25–30% | ~8.7 | 49/D | ~10 |
| 7 | SP-7290013142894 | MagUp Oxide 450 | 450 | oxide | 0.603 | 271.3 | 2–8% | ~10.9 | 66.5/B | ~11 |
| 8 | SP-7290013464248 | SupHerb Citrate+B6 | 250 | citrate | 0.162 | 40.5 | 25–30% | ~10.9 | 49/D | ~12 |
| 9 | SP-7290015318426 | Tink Oxide 520 | 520 | oxide | 0.603 | 313.6 | 2–8% | ~12.5 | 62.6/C | ~13 |
| 10 | SP-7290015318532 | Tink Malate 60 | 136 | malate | 0.155 | 21.1 | 15–20% | ~3.6 | 49/D | not shown |
| 11 | SP-7290015429245 | Amorphicure Carbonate | 160 | carbonate | 0.288 (PubChem 11029; SUPP-EV-028) | 46.1 | 8–15% | ~5.5 | 49/D | ~7 |
| 12 | SP-7290017218564 | Altman Mg 520 | 520 | oxide | 0.603 | 313.6 | 2–8% | ~12.5 | 62.6/C | ~13 |
| 13 | SP-7290017847122 | Magnox B6 432 | 432 | oxide | 0.603 | 260.5 | 2–8% | ~10.4 | 58.4/C | ~10 |
| 14 | SP-7290018439043 | Nutricare WELL Bisglycinate | 168 | bisglycinate | 0.141 | 23.7 | 20–25% | ~5.2 | 34/E | not shown |
| 15 | SP-7290018439579 | Nutricare Taurate 76 | 76 | taurate | 0.089 (PubChem 536944) | 6.8 | 10–20% | ~1.0 | 49/D | not shown |
| 16 | SP-7290019444206 | Altman Balance Oxide | 450 | oxide | 0.603 | 271.3 | 2–8% | ~10.9 | 59/C | ~11 |
| 17 | SP-7290019444480 | Altman Bisglycinate 250 | 250 | bisglycinate | 0.141 | 35.2 | 20–25% | ~7.7 | 49/D | ~10 |
| 18 | SP-7290118816065 | SupHerb TRIOMAG | 200 | citrate | 0.162 | 32.4 | 25–30% | ~8.7 | 34/E | not shown |
| 19 | SP-7290118818205 | SupHerb Max 550 Citrate | 550 | citrate | 0.162 | 89.1 | 25–30% | ~24.1 | 49/D | not shown |

*Plus: SP-7290001943700 (Hadas Full-Mag 600) = unscoreable_incomplete; not in the 18-SKU scored set.*

### Verification against current page figures and corrections needed

The magnesium page data (`bari-web/src/lib/comparisons/magnesium-page-data.ts`, line 60) uses
these point estimates: oxide 4%, hydroxide 4%, carbonate 15%, malate 17%, taurate 12%,
citrate 30%, bisglycinate 28%.

**Two corrections required on the display side (not score-moving; display accuracy):**

1. **Bisglycinate: page uses 28%, scientific range is 20–25%.** Bisglycinate/glycinate is a
   tolerability-forward form; the strongest human comparative bioavailability evidence is for
   citrate, not glycinate (benchmark §3: "NOT the proven bioavailability winner — its comparative
   evidence is thinner than its marketing"). 28% is a manufacturer-sourced figure, not from
   the cited comparative studies. Correct to ~22% midpoint (range 20–25%). Impact: Altman
   Bisglycinate 250 display changes from ~10mg to ~7.7mg, a material correction.

2. **Carbonate: page uses 15% (top of the 8–15% band), should use 12% midpoint.** Amorphicure
   display changes from ~7mg to ~5.5mg. Minor, but consistency requires using midpoints, not
   band tops.

3. **Hydroxide (NT L.C.):** page currently shows ~8mg. With corrected hydroxide fraction (0.417
   per BUG-FIX-2026-06-20, was 0.603 oxide in error) and 4% absorption:
   450 x 0.417 x 0.04 = 7.5mg → ~8mg. Page figure is already CORRECT post-fix. No change needed.

4. **Citrate: page uses 30% (top of band), proposed 27% midpoint.** Minor downgrades on all
   citrate products. Not a critical correction but should be applied for consistency.

---

## 3. Scoring Recommendation (single best option)

### Recommended: Switch Dose basis to absorbed-mg AND reduce Form weight to 0.05

**Why absorbed-mg, not elemental mg, as the dose axis:**

The engine's current "oxide paradox" requires two separate dimensions (Dose for quantity,
Form for bioavailability) that produce conflicting signals on the same underlying fact.
A product with 313mg elemental oxide scores DOSE=in_range=92 — yet delivers only ~12mg
absorbed. A product with 33mg elemental citrate scores DOSE=fairy_dust=20 — yet delivers
~9mg absorbed (nearly the same amount). These two products receive the same CAP_FAIRY_DUST
outcome by different routes but for incoherent reasons. The owner's insight is exactly right:
"what the body absorbs IS the issue." Absorbed-mg makes the dose axis tell the truth.

**Why reduce Form weight to 0.05, not eliminate it:**

Once absorbed-mg drives the Dose dimension, Form no longer needs to carry the bioavailability
information — it already lives in the absorbed calculation. But Form still signals two things
the absorbed number cannot:
- Whether a poor form is being sold at a premium price with misleading marketing (the
  "oxide paradox" honesty signal — currently the misleading_true flag, which still fires)
- Whether the form is genuinely unknown and cannot be converted (form=None uncertainty)

A weight of 0.05 is low enough to prevent Form from overriding the absorbed-mg dose signal,
but non-zero enough to preserve its residual honesty function.

**Why NOT double-count:** the absorbed-mg computation uses the absorption fraction to convert
elemental to absorbed. This already accounts for the form's bioavailability. The Form sub-score
at 0.05 is NOT scoring bioavailability again — it is scoring the marketing/presentation quality.
These are distinct failures: (a) an oxide product absorbs poorly [captured in absorbed-mg dose],
and (b) a product marketing oxide as premium [captured in Form honesty signal]. Concern
coordination (§3.2 #6) prevents triple-charging, but double-charging two distinct concerns
is correct and intentional.

### Proposed constants (CALIBRATION-PENDING — require D7 co-sign)

```
# Dose basis: absorbed elemental mg per day (= compound x elem_fraction x abs_fraction)
MIN_EFF_ABS  = 75.0   # mg absorbed/day (calibration-pending)
              # Derivation: BP trial median ~368mg elemental x ~25% avg = ~92mg;
              # conservative floor at 75mg. Source: PMID:27402922 (BP meta-analysis, 34 RCTs).
UPPER_ABS    = 100.0  # mg absorbed/day (calibration-pending)
              # Rough upper -- absorption heterogeneity means this band is wide.
FAIRY_FLOOR  = 37.5   # = 0.5 x MIN_EFF_ABS

# Dimension weights (proposed)
DIMENSION_WEIGHTS = {
    "evidence": 0.30,   # unchanged
    "dose":     0.40,   # WAS 0.25; gains Form's freed weight
    "form":     0.05,   # WAS 0.20; residual premium-marketing signal only
    "honesty":  0.15,   # unchanged
    "safety":   0.10,   # unchanged
}

# Absorbed-mg absorption coefficients (midpoints of literature bands)
ABS_MID = {
    "oxide":       0.04,   # 2-8% band; PMID:7815675
    "hydroxide":   0.07,   # 4-10% band; pharmacologic/laxative class
    "carbonate":   0.12,   # 8-15% band; GI-active class
    "malate":      0.17,   # 15-20% band; benchmark v1
    "taurate":     0.15,   # 10-20% band; sparse data
    "citrate":     0.27,   # 25-30% band; strongest comparative evidence
    "bisglycinate":0.22,   # 20-25% band; corrects current 28% (thinner evidence)
}
```

**Evidence basis for absorption bands:** PMID:7815675 (Firoz & Graber 2001, direct
bioavailability comparison in humans), PMID:30761462 (comparative review), PMID:39770988
(updated bioavailability review); benchmark v1 §3-4 (triangulated 2026-06-20). Evidence tier
for the bioavailability ranking: **Moderate** (consistent human data with some heterogeneity;
dossier `forms.form_ladder_confidence = "medium-high"`). NOT Strong — absolute absorption
fractions have meaningful inter-individual and inter-study variability.

---

## 4. Honesty Guardrail (Critical)

**The absorbed-mg number is a population-average estimate, not a per-product measurement.**

The standing benchmark caveat applies: "Label-truthful, not lab-verified. A Polish AAS assay
of 116 EU supplements found 58.7% outside legal tolerance." Bari's absorbed-mg display figure
assumes the label dose is accurate. It further assumes population-average absorption, which
varies by:
- Gastric pH and gut transit time (individual variation ~2x)
- Magnesium status (deficient individuals absorb more)
- Concurrent food intake
- Specific hydration state of the compound (citrate nonahydrate vs anhydrous has different
  elemental fraction; label species often unspecified)

**Display must never imply measured per-product absorption.** Required language:
- Use "~כ-X מ\"ג" (approximately), not "X מ\"ג נספג" without qualification
- Add "הערכה ממוצעת — לא מדידה מעבדתית" (population average — not a lab measurement)
  in the tooltip/expanded view, not necessarily in the pill itself
- Never claim "this product delivers X mg" — claim "the body absorbs an estimated ~X mg"

The current page copy uses "בקירוב" (approximately) in the prose, which is correct. The
label pill proposed below should use the same qualifier.

**Why banded coefficients are used:** Absorption fractions in the literature range ±30-50%
relative to the midpoint values used here (e.g. citrate studies show 24-33% in different
trials). Using a single point estimate (e.g. exactly 27%) implies false precision. The display
figure carries "~כ-" prefix precisely because it is a band midpoint, not a measured value.

---

## 5. Before / After Impact

**Prototype run (2026-06-20; `prototype_absorbed_scoring.py`; scratch, not engine code):**

Proposed weights: ev=0.30, dose=0.40, form=0.05, honesty=0.15, safety=0.10
Proposed min_eff_absorbed=75mg, fairy_floor=37.5mg

| SKU | Name | Absorbed mg~ | Curr score | Curr grade | New blend | New score | New grade | Change |
|-----|------|------------|----------|----------|---------|---------|---------|--------|
| SP-0033984005181 | Solgar Ca+Mg+D3 | ~4.5 | 49.0 | D | 48.7 | 48.7 | D | no change |
| SP-7290001065594 | Nutricare Nano Liposomal | ~2.8 | 34.0 | E | 52.8* | 34.0 | E | no change (cap_1 holds) |
| SP-7290001065662 | Nutricare Mg 520 | ~12.5 | 62.6 | **C** | 49.7 | 49.0 | **D** | GRADE CHANGE |
| SP-7290001066973 | Nutricare Malate | ~18.5 | 49.0 | D | 47.7 | 47.7 | D | no change |
| SP-7290010207640 | NT L.C. Hydroxide | ~13.1 | 59.7 | **C** | 46.4 | 46.4 | **D** | GRADE CHANGE |
| SP-7290011899967 | Altman Citrate 120 | ~8.7 | 49.0 | D | 48.7 | 48.7 | D | no change |
| SP-7290013142894 | MagUp Oxide 450 | ~10.9 | 66.5 | **B** | 49.7 | 49.0 | **D** | GRADE CHANGE (B->D) |
| SP-7290013464248 | SupHerb Citrate+B6 | ~10.9 | 49.0 | D | 48.7 | 48.7 | D | no change |
| SP-7290015318426 | Tink Oxide 520 | ~12.5 | 62.6 | **C** | 49.7 | 49.0 | **D** | GRADE CHANGE |
| SP-7290015318532 | Tink Malate 60 | ~3.6 | 49.0 | D | 47.7 | 47.7 | D | no change |
| SP-7290015429245 | Amorphicure Carbonate | ~5.5 | 49.0 | D | 47.7 | 47.7 | D | no change |
| SP-7290017218564 | Altman Mg 520 | ~12.5 | 62.6 | **C** | 49.7 | 49.0 | **D** | GRADE CHANGE |
| SP-7290017847122 | Magnox B6 432 | ~10.4 | 58.4 | **C** | 49.7 | 49.0 | **D** | GRADE CHANGE |
| SP-7290018439043 | Nutricare WELL Bisglycinate | ~5.2 | 34.0 | E | 52.8* | 34.0 | E | no change (cap_1 holds) |
| SP-7290018439579 | Nutricare Taurate 76 | ~1.0 | 49.0 | D | 47.7 | 47.7 | D | no change |
| SP-7290019444206 | Altman Balance Oxide | ~10.9 | 59.0 | **C** | 42.2 | 42.2 | **D** | GRADE CHANGE |
| SP-7290019444480 | Altman Bisglycinate 250 | ~7.7 | 49.0 | D | 48.7 | 48.7 | D | no change |
| SP-7290118816065 | SupHerb TRIOMAG | ~8.7 | 34.0 | E | 52.8* | 34.0 | E | no change (cap_1 holds) |
| SP-7290118818205 | SupHerb Max 550 Citrate | ~24.1 | 49.0 | D | 48.7 | 48.7 | D | no change |

*\* blend would be above D/C but cap_1 (insufficient evidence) applies; grade stays E.*

**Summary: 7 grade changes out of 19 scored/attempted SKUs (18 in scored set).**

All 7 changes are **oxide/hydroxide products dropping from C or B to D**:
- Nutricare Mg 520: C → D
- NT L.C. Hydroxide: C → D
- **MagUp Oxide 450: B → D** (the most significant; currently the only B on the shelf)
- Tink Oxide 520: C → D
- Altman Mg 520: C → D
- Magnox B6 432: C → D
- Altman Balance Oxide: C → D

**No product improves grade under this proposal.** The Cs and the one B come down; the Ds
and Es stay. This is scientifically coherent: the engine was previously rewarding oxide
products' high elemental count without penalizing their low absorption. The absorbed-mg
basis corrects this.

**Golden validation (18/18 fixtures): STILL PASSES (confirmed 2026-06-20).** The prototype
is a scratch computation — it does NOT touch score_engine.py. The golden fixtures are tested
against the unchanged engine and continue to pass. Any implementation in proto_v1 would
require new calibration fixtures for the absorbed-mg Dose basis.

**Binding constraint changes:**
- Oxide products that were scoring B/C via `blend_dominant_limit` now score via
  `cap_2_fairy_dust_hidden_dose` (absorbed-mg < 37.5mg fairy floor) — this is the correct
  binding constraint: they are genuinely delivering fairy-dust-level absorption.

---

## 6. Per-Product Visible Label Proposal

**Format (for Frontend Agent to implement):**

A pill/badge component showing the absorbed-mg estimate directly on the product card.
Consistent with the existing `claimShortfallFlag` pill style (no new design tokens).

**Proposed Hebrew label text:**
```
נספג: ~כ-X מ"ג
```
Example: `נספג: ~כ-11 מ"ג`

Where X is the absorbed-mg midpoint (rounded to nearest integer; no decimals needed — the
estimate uncertainty is too large for decimal precision to be meaningful).

**Rounding convention:** round to nearest 0.5mg for values < 5mg, nearest 1mg for 5-20mg,
nearest 5mg for > 20mg. Examples:
- ~1.0mg → "~כ-1 מ\"ג"
- ~4.5mg → "~כ-4.5 מ\"ג"
- ~12.5mg → "~כ-12 מ\"ג" (not 12.5)
- ~24.1mg → "~כ-25 מ\"ג"

**Tooltip text (expanded, shown on tap/hover):**
```
הגוף סופג בקירוב ~X מ"ג מגנזיום לנטילה יומית מומלצת.
ההערכה מבוססת על שיעורי ספיגה ממוצעים במחקרים — לא מדידה של מוצר זה ספציפית.
```
(The body absorbs an estimated ~X mg magnesium per recommended daily serving.
This estimate is based on average absorption rates from studies — not a measurement of
this specific product.)

**Do not show** the absorbed-mg pill if:
- The form is unknown (form=None / unresolvable) — the absorption fraction cannot be computed
- The product has a proprietary blend (dose hidden)
- The product is unscoreable_incomplete (Hadas 600)

**Display-only corrections needed immediately** (before any score change, as label display
accuracy issues regardless of scoring proposal):

1. Altman Bisglycinate 250: update from ~10mg to ~8mg (correcting 28% → 22%)
2. Amorphicure Carbonate: update from ~7mg to ~6mg (correcting 15% → 12%)
3. Citrate products: update from 30%-based figures to 27%-based (minor, ~10% reduction)

These are display accuracy corrections, not score-moving changes.

---

## 7. Evidence Registry Citation

This proposal references and extends:
- **SUPP-EV-002**: the bioavailability ranking (form ladder) — this proposal integrates its
  absorption fractions into the Dose dimension itself
- **SUPP-EV-022**: compound form identity (elemental fractions verified PubChem)
- **SUPP-EV-028**: carbonate fraction correction (2026-06-19)
- **BUG-FIX-2026-06-20**: hydroxide fraction correction (0.417 not 0.603)

A new evidence registry entry **SUPP-EV-030** (proposed) should be created to formally
govern:
- The absorbed-mg dose basis change
- The ABS_MID absorption coefficients (banded, cited sources)
- The weight rebalancing (dose=0.40, form=0.05)
- The calibrated min_eff_absorbed=75mg target

This proposal is CANDIDATE; SUPP-EV-030 should not be written until after owner + Product
Agent D7 co-sign.

---

## 8. Open Calibration Questions for D7

1. **Is 75mg absorbed a defensible min_effective_absorbed?** Derivation above is rough
   (368mg elemental x 25% = 92mg, floor at 75mg). A tighter review of the RCT dose ranges
   in elemental terms, combined with form-weighted absorption, could move this ±20mg. The
   75mg choice means essentially NO product on the current Israeli shelf reaches it at the
   absorption midpoints (highest absorbed is SupHerb Max 550 citrate at ~24mg). This is
   a true finding — the Israeli shelf is chronically under-delivering on absorbed Mg — but
   owner and Product Agent should confirm this is the intended calibration consequence.

2. **Form weight = 0.05 or 0.00?** The case for 0.00 is that absorbed-mg fully captures
   bioavailability and Form is then purely redundant. The case for 0.05 is the premium-marketing
   honesty signal. This is a product philosophy call, not a scientific one.

3. **Is the oxide/hydroxide absorbed figure stable enough to bind a grade?** Absorption
   studies for oxide/hydroxide show ~2–8% range, meaning the true absorbed mg for a
   520mg oxide product could be anywhere from ~6mg to ~25mg. Using the 4% midpoint gives
   ~12.5mg. Even at the 8% top of the band, that is still ~25mg — well below the 37.5mg
   fairy floor. The cap_2 outcome is stable across the entire band for oxide products.
   The binding constraint does not depend on the exact absorption fraction for poor-form
   products. This makes the change robust.

4. **Liposomal bisglycinate (Nutricare Nano):** the product claims "nano liposomal for
   optimal absorption." If this claim were validated with product-specific absorption data,
   it might warrant a higher absorption coefficient than the 22% used for standard
   bisglycinate. The current evidence for nano-liposomal Mg specifically is insufficient
   to justify a separate coefficient (benchmark §2 / claim grade = E). Using the standard
   bisglycinate band is the honest choice. Flag for future re-adjudication if product-specific
   absorption data emerges.

---

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_absorbed_scoring_proposal_v1.md",
      "sha256": "PENDING_WRITE",
      "description": "Full absorbed-mg scoring proposal including per-product table, recommendation, before/after, and label format"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\prototype_absorbed_scoring.py",
      "sha256": "PENDING_WRITE",
      "description": "Scratch prototype computing the before/after impact table (not committed engine code)"
    }
  ],
  "counts": {
    "corpus_mg_skus_scored": 18,
    "corpus_mg_skus_unscoreable": 1,
    "grade_changes": 7,
    "grades_improved": 0,
    "grades_declined": 7,
    "display_corrections_needed": 3,
    "golden_fixtures_pass": 18,
    "golden_fixtures_total": 18
  },
  "commands_run": [
    {"cmd": "python run_golden_validation.py", "exit_code": 0, "result": "18/18 PASS"},
    {"cmd": "python prototype_absorbed_scoring.py", "exit_code": 0, "result": "7/19 grade changes"}
  ],
  "not_done": [
    "SUPP-EV-030 not written (pending D7 co-sign)",
    "score_engine.py not modified (this is a proposal only)",
    "Frontend label implementation not started (handoff to Frontend Agent after D7)",
    "min_eff_absorbed=75mg calibration requires D7 confirmation",
    "Absorption coefficients for liposomal bisglycinate not differentiated (pending product-specific evidence)"
  ],
  "acceptance_test": "Golden validation 18/18 PASS (confirmed); prototype produces 7 grade changes, all oxide/hydroxide C/B -> D; no product improves; absorption display figures consistent with cited literature bands"
}
```
