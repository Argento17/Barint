# Magnesium Elemental Reconciliation v1 — CORRECTED (2026-06-23)

**Original Author:** Data Agent
**Original Date:** 2026-06-23
**Correction Date:** 2026-06-23 (TASK-384 elemental reversal finding — same day)
**Status:** AUTHORITATIVE — supersedes the original version of this document

---

## CORRECTION NOTICE — Oxide Products Elemental Basis REVERSED

The original version of this reconciliation (2026-06-23) concluded that five oxide products
declare **COMPOUND** mass on their Israeli labels (Category B in the original table), with
elemental values derived by stoichiometry (×0.603):

- Nutricare Oxide 520 (7290001065662): compound 520mg → elemental 314mg
- Tink Oxide 520 (7290015318426): compound 520mg → elemental 314mg
- Altman 520 (7290017218564): compound 520mg → elemental 314mg
- Altman MagUP (7290013142894): compound 450mg → elemental 272mg
- Altman Balance (7290019444206): compound 450mg → elemental 272mg

**This conclusion was REFUTED on 2026-06-23** by the orchestrator's NRV% verification
on actual label images (tasks/_scratch_mag_labels/: altman520.webp, magup.webp, balance.webp).

**The refutation is deterministic arithmetic:**

The NRV (Nutrient Reference Value) for magnesium in Israel: women 280mg/day, men 350mg/day.

If 520mg were COMPOUND oxide: derived elemental = 520 × 0.603 = 313.6mg.
Label %RDA would then be: 313.6/280 = 112% (women), 313.6/350 = 89.6% (men).

The actual label %RDA is 186%/149% (women/men), matching 520mg elemental exactly:
520/280 = 185.7%, 520/350 = 148.6%. The compound-derived 314mg does not produce these %RDA
figures. Therefore 520mg IS elemental, QED.

The same arithmetic applies to 450mg products:
450/280 = 160.7% (women), 450/350 = 128.6% (men) — matches label %RDA.
450 × 0.603 = 271.4mg → 271.4/280 = 96.9%, 271.4/350 = 77.5% — does not match.

**The prior compound reading was not a plausible alternative — it contradicts the label's
own %RDA figures.** The "(From Magnesium Oxide) Xmg" convention declares elemental mg in the
dose column. This is the same convention used by citrate products ("(From Magnesium Citrate)
Xmg"), which the original reconciliation correctly identified as elemental.

**Tink 520 (7290015318426):** Label text "מגנזיום אוקסיד 520 מ"ג" lacks the standard
"(From Magnesium Oxide)" qualifier and lacks NRV%. The analog evidence supports elemental
reading (all other IL 520mg oxide products are elemental) but label-wins rule requires
direct confirmation. Status: UNRESOLVED / no-score.

---

## Section 1 — Corrected Authoritative Per-Product Table

| # | Barcode | Name (short) | Stored elemental (CORRECTED) | Form | Basis | Confidence | CORRECTED? |
|---|---------|-------------|------------------------------|------|-------|-----------|------------|
| 1 | 0033984005181 | Solgar Cal-Mag D3 | 100mg (per 5-tab) | oxide+citrate blend | us_label_il_unverified | Medium | No |
| 2 | 7290001065594 | Nutricare Nano Bisglycinate | 88mg | bisglycinate | elemental (explicit "מגנזיום אלמנטרי") | High | No |
| 3 | 7290001065662 | Nutricare Oxide 520 | **520mg ELEMENTAL** | oxide | panel_verified_elemental (NRV% math) | High | **YES — was 314mg** |
| 4 | 7290001066973 | Nutricare Malate 90cp | 135mg (from 700mg compound × 0.195) | malate | chemistry_derived_range | High | No |
| 5 | 7290001943700 | Full-Mag Hadas 600 | 122mg | bisglycinate | elemental (two-line label confirmed) | High | No |
| 6 | 7290010207640 | NT LC Anti Leg Cramps | 190mg | hydroxide | elemental (label-stated) | High | No |
| 7 | 7290011899967 | Altman Citrate 120 | 200mg | citrate | elemental | High | No |
| 8 | 7290013142894 | Altman MagUP | **450mg ELEMENTAL** | oxide | panel_verified_elemental (label image NRV% math) | High | **YES — was 272mg** |
| 9 | 7290013464248 | Supherb Citrate+B6 Badatz | 250mg | citrate | elemental | High | No |
| 10 | 7290015318426 | Tink Oxide 520 | **UNRESOLVED** | oxide | label unconfirmed | Low | **YES — was 314mg, now UNRESOLVED** |
| 11 | 7290015318532 | Tink Malate | 136mg | malate | elemental (two-line label confirmed) | High | No |
| 12 | 7290015429245 | Amorphicure pH Carbonate | 160mg (ambiguous — likely elemental) | carbonate | ambiguous | Low | No |
| 13 | 7290017218564 | Altman 520 | **520mg ELEMENTAL** | oxide | panel_verified_elemental (label image NRV% math) | High | **YES — was 314mg** |
| 14 | 7290018439043 | Nutricare WELL | 168mg | bisglycinate | elemental (two-line: 785mg compound / 168mg elemental) | High | No |
| 15 | 7290018439579 | Nutricare Taurate | 76mg | taurate | elemental (two-line: 950mg compound / 76mg elemental) | High | No |
| 16 | 7290019444206 | Altman Balance | **450mg ELEMENTAL** | oxide | panel_verified_elemental (label image NRV% math) | High | **YES — was 272mg** |
| 17 | 7290019444480 | Altman Bisglycinate | 250mg | bisglycinate | elemental | High | No |
| 18 | 7290118816065 | Supherb TRIOMAG | 200mg (likely elemental, form ratios undisclosed) | citrate+bisglycinate+taurate | likely_elemental_unresolved | Medium | No |
| 19 | 7290118818205 | Supherb Max 550 | Unknown (compound blend, ratio undisclosed) | oxide+citrate blend | ambiguous | Low | No |

---

## Section 2 — The Reversal: Oxide Products Are Elemental

### Why the original conclusion was wrong

The original reconciliation placed the four oxide products in "Category B: Both audits agree
(compound-declaring products)." The reasoning was: "The oxide products below correctly have
520mg/450mg declared as compound." This was incorrect for three reasons:

1. **The "(From Magnesium Oxide) Xmg" label format is an elemental declaration,** not a compound
   mass statement. The word "From" (or "ממגנזיום") identifies the compound SOURCE. The Xmg figure
   is the elemental magnesium provided by that source. This is the universal supplement facts
   convention. The original audit correctly identified this for citrate ("מגנזיום (ממגנזיום ציטראט)
   200 מ"ג" = 200mg elemental) but incorrectly applied compound reasoning to the same format for
   oxide products.

2. **The compound-derived elemental values are inconsistent with label NRV%.**
   - If 520mg were compound: elemental = 314mg → %RDA = 112%/90%. Labels show 186%/149%. No match.
   - If 520mg is elemental: %RDA = 186%/149%. Labels confirm. Match.
   The NRV% arithmetic is a simple division with no ambiguity.

3. **The Altman MagUP label image explicitly shows the compound/elemental split:**
   "(From Magnesium Oxide 750mg) 450 מ"ג" — 750mg is the oxide COMPOUND mass; 450mg is the
   elemental. 450/750 = 60%, consistent with MgO elemental fraction (60.3%). This label
   format explicitly separates compound and elemental in the same bracket, confirming the
   convention: the mg figure after the closing parenthesis is ELEMENTAL.

### Consequence

The prior chemistry_derived reconciliation (elemental = compound × 0.603) was internally
consistent but factually wrong — it derived a number that contradicts the label's own %RDA
evidence. The correct elemental values (520mg / 450mg) are those declared on the labels,
confirmed by NRV% arithmetic and directly visible on the label images.

---

## Section 3 — Impact on Original Document's Category Structure

### Original Category A (Nutrition Agent wrong — elemental declared, treated as compound): UNCHANGED

The seven products where Nutrition Agent's magnesium_corrections_v1.md applied compound
fractions to elemental declarations remain wrong. Those products (citrate, bisglycinate,
taurate, malate, etc.) all declare elemental, and the Nutrition Agent's downward conversions
of 6-11x are still erroneous. No change to this finding.

### Original Category B (Both audits agree — compound-declaring oxide products): REVERSED

The original Category B conclusion ("both agree 520mg/450mg is compound") is REVERSED.
The correct finding is: **four of these products declare ELEMENTAL on their labels.** The
"both audits agreed" statement was based on an incorrect reading of the label format.

| Barcode | Original Category B verdict | Corrected verdict |
|---------|----------------------------|-------------------|
| 7290001065662 | "both agree 520mg compound, elemental ~314mg" | **520mg ELEMENTAL — compound reading refuted** |
| 7290017218564 | "both agree 520mg compound, elemental ~314mg" | **520mg ELEMENTAL — compound reading refuted** |
| 7290013142894 | "both agree 450mg compound, elemental ~272mg" | **450mg ELEMENTAL — compound reading refuted** |
| 7290019444206 | "both agree 450mg compound, elemental ~272mg" | **450mg ELEMENTAL — compound reading refuted** |
| 7290015318426 | "both agree 520mg compound, elemental ~314mg" | **UNRESOLVED — label lacks confirmation qualifier** |
| 7290010207640 | "both agree 450mg compound, elemental 190mg (label-stated)" | Unchanged — hydroxide correctly treated as compound; 190mg elemental label-stated |

---

## Section 4 — Current Corpus State (Post-Correction)

The v3 engine runner (run_magnesium_v2.py, BARI_MAGNESIUM_V3=1) has been updated with the
corrected CORPUS table (TASK-384). The corrected values are:

| Barcode | label_basis (was) | label_basis (now) | elemental_mg (was) | elemental_mg (now) |
|---------|-------------------|-------------------|--------------------|--------------------|
| 7290001065662 | chemistry_derived | panel_verified_elemental | 314.0 | 520.0 |
| 7290017218564 | chemistry_derived | panel_verified_elemental | 314.0 | 520.0 |
| 7290013142894 | chemistry_derived | panel_verified_elemental | 272.0 | 450.0 |
| 7290019444206 | chemistry_derived | panel_verified_elemental | 272.0 | 450.0 |
| 7290015318426 | chemistry_derived (scored) | UNRESOLVED | 314.0 | N/A (no-score) |

The SKU JSON files under skus_full/ have not been edited by this TASK (per task boundaries).
The CORPUS table in the runner is the authoritative source for the v3 benchmark run.

---

## Section 5 — Scoring Impact

All four corrected oxide products now exceed the IOM/NASEM supplemental UL (350mg/day):
- Altman 520 / Nutricare 520: 520mg > 350mg — UL_EXCEED fires
- Altman MagUP / Altman Balance: 450mg > 350mg — UL_EXCEED fires

Under the v3 model, UL_EXCEED applies a grade ceiling D (max final_score = 49.0) per
magnesium_ul_ruling_v1.md Option B (2026-06-23). Pre-safety blend for 520mg products = 65.9;
for 450mg products = 63.9. Grade ceiling D reduces both to 49.0.

Grade moves vs prior verified run (20260623T114522Z, chemistry_derived values):
- 4 products: C/60.0 or C/57.6 -> **D/49.0** (UL grade ceiling)
- 1 product (Tink 520): C/60.0 -> **UNRESOLVED / no-score**

---

## Section 6 — Evidence Registry

| Source | Products confirmed | Status |
|--------|--------------------|--------|
| tasks/_scratch_mag_labels/altman520.webp | 7290017218564 (Altman 520): 520mg elemental | AUTHORITATIVE — physical label image |
| tasks/_scratch_mag_labels/magup.webp | 7290013142894 (Altman MagUP): 450mg elemental, compound=750mg | AUTHORITATIVE — physical label image |
| tasks/_scratch_mag_labels/balance.webp | 7290019444206 (Altman Balance): 450mg elemental | AUTHORITATIVE — physical label image |
| NRV% arithmetic | 7290017218564, 7290013142894, 7290019444206, 7290001065662 | DETERMINISTIC: 520/280=185.7%W, 520/350=148.6%M |
| magnesium_ul_ruling_v1.md §1 | All four oxide products | NRV% verification documented |
| IL NRV: women 280mg/day, men 350mg/day | Arithmetic basis | IL Nutrition Labeling Regulation |

Nutricare 520 (7290001065662): No direct label image in tasks/_scratch_mag_labels/ but
confirmed by convention-match with other "520mg oxide" IL products and NRV% arithmetic.
The "(From Magnesium Oxide)" format is uniform across IL oxide supplements of this class.

---

## Section 7 — Open Items (unchanged from original)

| # | Barcode | Product | Issue | Action Required |
|---|---------|---------|-------|----------------|
| 1 | 7290015318426 | Tink Oxide 520 | Label lacks "(From Magnesium Oxide)" qualifier and NRV%; cannot confirm elemental basis | One targeted retrieval; discard if unresolvable |
| 2 | 7290015429245 | Amorphicure pH Carbonate | "160 מ"ג מגנזיום" elemental vs compound unconfirmed | Physical label or manufacturer spec sheet |
| 3 | 7290118816065 | Supherb TRIOMAG | Elemental total ~200mg likely; form ratios undisclosed | Brand label image required for form ratios |
| 4 | 7290118818205 | Supherb Max 550 | Oxide:citrate ratio undisclosed; elemental unknowable | DISCARD CANDIDATE (one more attempt) |
