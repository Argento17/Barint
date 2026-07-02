# Magnesium Label Audit v1 — CORRECTED (2026-06-23)

**Original Audit Date:** 2026-06-23
**Correction Date:** 2026-06-23 (TASK-384 elemental reversal finding)
**Auditor:** Data Agent
**Correction Authority:** Orchestrator-verified from actual label images (TASK-384)
**Status:** AUTHORITATIVE — supersedes the original version of this document

---

## CORRECTION NOTICE — Oxide Products Elemental Basis REVERSED (2026-06-23)

The original version of this audit (2026-06-23, same day) concluded that five oxide products
declare **COMPOUND** mass on their Israeli labels, and derived elemental via stoichiometry
(×0.603). This conclusion was REFUTED on the same day by the orchestrator's verification of
actual label images from altman.co.il:

- `tasks/_scratch_mag_labels/altman520.webp` — Altman 520
- `tasks/_scratch_mag_labels/magup.webp` — Altman MagUP
- `tasks/_scratch_mag_labels/balance.webp` — Altman Balance

**NRV% mathematics (authoritative determination):**

| Product | Declared mg | Divided by women IL NRV (280mg) | Divided by men IL NRV (350mg) | Verdict |
|---------|-------------|--------------------------------|-------------------------------|---------|
| Altman 520 | 520mg | 520/280 = 185.7% | 520/350 = 148.6% | **ELEMENTAL** — NRV% matches label %RDA |
| Altman MagUP | 450mg | 450/280 = 160.7% | 450/350 = 128.6% | **ELEMENTAL** — NRV% matches label %RDA |
| Altman Balance | 450mg | 450/280 = 160.7% | 450/350 = 128.6% | **ELEMENTAL** — NRV% matches label %RDA |

If the 520mg figure were COMPOUND mass (as originally concluded), the NRV% would be computed
on the derived elemental (314mg): 314/280 = 112.1% (women), 314/350 = 89.7% (men). These values
do NOT match any plausible label %RDA. The 185.7%/148.6% figures only make sense if 520mg IS
the elemental value. This arithmetic is deterministic and refutes the compound reading.

**The "From Magnesium Oxide" qualifier on IL labels:**

The label format "(From Magnesium Oxide) 520 מ"ג" follows the international Supplement Facts
convention in which the mg figure in the dose column is ELEMENTAL magnesium provided by the
named compound source. The "From X" clause names the compound SOURCE, not the compound MASS.
This is identical to the citrate convention "(From Magnesium Citrate) 200 מ"ג" that this
audit correctly identified as elemental. The original audit applied the convention correctly
to citrate products but incorrectly to oxide products — both follow the same format.

**Tink 520 (7290015318426):** Label declares "מגנזיום אוקסיד 520 מ"ג" WITHOUT the standard
"(From Magnesium Oxide)" qualifier and without NRV%. Analog evidence supports elemental reading
(all other IL 520mg oxide products are elemental), but the label-wins rule requires label
confirmation — not analog inference. Status: UNRESOLVED / no-score pending label confirmation
(magnesium_ul_ruling_v1.md §4, 2026-06-23).

---

## 1. Full Audit Table (Corrected)

| # | Barcode | Product Name | Declared Amount | Elemental vs Compound | Form(s) | Confidence | Evidence Path | CORRECTED? |
|---|---------|-------------|-----------------|----------------------|---------|-----------|---------------|------------|
| 1 | 0033984005181 | Solgar Calcium Magnesium with Vitamin D3 150 tabs | 100mg per tablet | **ELEMENTAL** — US supplement facts "Magnesium (As magnesium oxide, magnesium citrate) 500mg" per 5-tab = 100mg elemental per tab | oxide + citrate blend (ratios undisclosed) | Medium (US label; no IL Hebrew label verified) | US label confirmed via iHerb/WebSearch; IL label unverified | No |
| 2 | 7290001065594 | Nutricare Nano Bisglycinate 60cp | 88mg | **ELEMENTAL** — label explicitly: "88 מ"ג מגנזיום אלמנטרי" | bisglycinate (nano liposomal) | High | maxpharm.co.il HTTP 200 | No |
| 3 | 7290001065662 | Nutricare Oxide 520 100cp | 520mg | **ELEMENTAL** — "(From Magnesium Oxide) 520 מ"ג" per IL convention; NRV% arithmetic confirms (520/280=185.7%W, 520/350=148.6%M). Prior "compound" reading REFUTED. | oxide | High | maxpharm.co.il HTTP 200 + NRV% math (TASK-384, 2026-06-23) | **YES — was COMPOUND, now ELEMENTAL** |
| 4 | 7290001066973 | Nutricare Malate 90cp | 700mg compound | **COMPOUND MASS** — label: "700 מ"ג של מגנזיום מלאט" = 700mg OF malate compound. Elemental ~137mg (700×0.195) | malate | High | tevagil.co.il + maxpharm.co.il HTTP 200 | No |
| 5 | 7290001943700 | Full-Mag Hadas 600 60cp | 600mg compound / 122mg elemental | **COMPOUND declared + ELEMENTAL separately stated** — two-line label: 600mg bisglycinate compound provides 122mg elemental | bisglycinate (Albion USA) | High | tevaworld.com + drugstore.co.il + vitamins4all.co.il HTTP 200 | No |
| 6 | 7290010207640 | NT LC Anti Leg Cramps 50cp | 450mg compound / 190mg elemental | **COMPOUND declared + ELEMENTAL stated** — label: "450 מ"ג מגנזיום הידרוקסיד — 190 מ"ג מגנזיום אלמנטרי" | hydroxide (Dead Sea / Magnox) | High | navehpharma.com HTTP 200 | No |
| 7 | 7290011899967 | Altman Citrate 120cp | 200mg | **ELEMENTAL** — "(From Magnesium Citrate) 200 מ"ג" = elemental per IL/US convention | citrate | High | altman.co.il HTTP 200 | No |
| 8 | 7290013142894 | Altman MagUP 60cp | 450mg | **ELEMENTAL** — "(From Magnesium Oxide 750mg) 450 מ"ג"; NRV% confirms: 450/280=160.7%W, 450/350=128.6%M. Prior "compound" reading REFUTED. | oxide + potassium chloride | High | altman.co.il label image (tasks/_scratch_mag_labels/magup.webp, TASK-384, 2026-06-23) | **YES — was COMPOUND, now ELEMENTAL** |
| 9 | 7290013464248 | Supherb Citrate+B6 Badatz 60cp | 250mg | **ELEMENTAL** — "(as Magnesium Citrate) 250 מ"ג" = elemental per IL/US convention | citrate | High | biogaya.co.il + vitaminglobal.com HTTP 200 | No |
| 10 | 7290015318426 | Tink Oxide 520 90cp | 520mg | **UNRESOLVED** — label declares "מגנזיום אוקסיד 520 מ"ג" WITHOUT the "(From Magnesium Oxide)" elemental qualifier and WITHOUT NRV%. Cannot confirm elemental basis by NRV math. Analog evidence (all other IL 520mg oxide products are elemental) supports elemental reading but label-wins rule requires confirmation. | oxide | Low (label unconfirmed) | tinc.co.il HTTP 200 (panel text without NRV%) | **YES — was COMPOUND (314mg), now UNRESOLVED** |
| 11 | 7290015318532 | Tink Malate 60cp | 136mg elemental | **ELEMENTAL** — two-line label: 850mg malate compound / 136mg elemental (bella-natura.net confirmed) | malate | High | bella-natura.net HTTP 200 | No |
| 12 | 7290015429245 | Amorphicure pH Carbonate 160cp | 160mg | **AMBIGUOUS** — "160 מ"ג מגנזיום בכמוסה" without explicit "from carbonate" qualifier. IL convention implies elemental; no supplement facts panel found. | carbonate (amorphous) | Low | amorphicure.co.il + biogaya.co.il HTTP 200 | No |
| 13 | 7290017218564 | Altman 520 60cp | 520mg | **ELEMENTAL** — label "(From Magnesium oxide) 520 מ"ג"; NRV% math: 520/280=185.7%W, 520/350=148.6%M. Prior "compound" reading REFUTED. | oxide (Dead Sea) | High | altman.co.il label image (tasks/_scratch_mag_labels/altman520.webp, TASK-384, 2026-06-23) | **YES — was COMPOUND, now ELEMENTAL** |
| 14 | 7290018439043 | Nutricare WELL 90cp | 168mg elemental | **ELEMENTAL** — "785mg bisglycinate provides 168mg elemental" (multiple IL sources) | bisglycinate | High | vitamins4all + v-care + maxpharm HTTP 200 | No |
| 15 | 7290018439579 | Nutricare Taurate 90cp | 76mg elemental | **ELEMENTAL** — "950mg taurate compound / 76mg elemental" (multiple IL sources) | taurate | High | barcode-matched IL retailer descriptions | No |
| 16 | 7290019444206 | Altman Balance 60cp | 450mg | **ELEMENTAL** — "(From Magnesium oxide) 450 מ"ג"; NRV% confirms 450/280=160.7%W. Prior "compound" reading REFUTED. | oxide + KSM-66/valerian/B6 | High | altman.co.il label image (tasks/_scratch_mag_labels/balance.webp, TASK-384, 2026-06-23) | **YES — was COMPOUND, now ELEMENTAL** |
| 17 | 7290019444480 | Altman Bisglycinate 60cp | 250mg | **ELEMENTAL** — "(as Magnesium Bisglycinate) 250 מ"ג" = elemental per IL/US convention | bisglycinate | High | altman.co.il HTTP 200 | No |
| 18 | 7290118816065 | Supherb TRIOMAG 60cp | 200mg | **LIKELY ELEMENTAL, UNRESOLVED** — "מספקת 200 מ"ג" per IL convention likely elemental; form ratios undisclosed | citrate + bisglycinate + taurate blend | Medium | biogaya.co.il HTTP 200 | No |
| 19 | 7290118818205 | Supherb Max 550 60cp | 550mg | **COMPOUND BLEND** — 550mg compound oxide+citrate blend; ratio undisclosed; elemental unknowable | oxide + citrate blend | Low | maxpharm.co.il HTTP 200 | No |

---

## 2. Corrected Elemental Values (v3 engine inputs)

The TASK-384 elemental reversal changes the v3 engine inputs for four products:

| Barcode | Product | OLD elemental (prior audit) | NEW elemental (corrected) | Basis |
|---------|---------|----------------------------|--------------------------|-------|
| 7290001065662 | Nutricare Oxide 520 | 314mg (chemistry_derived, 520×0.603) | **520mg** (panel_verified_elemental) | IL label "(From Magnesium Oxide) 520 מ"ג" + NRV% math |
| 7290017218564 | Altman 520 | 314mg (chemistry_derived, 520×0.603) | **520mg** (panel_verified_elemental) | Label image + NRV% math (altman520.webp, TASK-384) |
| 7290013142894 | Altman MagUP | 272mg (chemistry_derived, 450×0.603) | **450mg** (panel_verified_elemental) | Label image + NRV% math (magup.webp, TASK-384) |
| 7290019444206 | Altman Balance | 272mg (chemistry_derived, 450×0.603) | **450mg** (panel_verified_elemental) | Label image + NRV% math (balance.webp, TASK-384) |
| 7290015318426 | Tink Oxide 520 | 314mg (chemistry_derived) | **UNRESOLVED** | Label lacks "(From Magnesium Oxide)" qualifier and NRV%; label-wins rule: no analog inference |

---

## 3. Consequence for Scoring

All four corrected oxide products now declare >350mg elemental (Altman 520 / Nutricare 520:
520mg; Altman MagUP / Altman Balance: 450mg). Both values exceed the IOM/NASEM supplemental UL
of 350mg/day. Under the v3 model (BARI_MAGNESIUM_V3=1), UL_EXCEED fires the grade ceiling D
mechanism (max final_score = 49.0 per magnesium_ul_ruling_v1.md §3).

The prior chemistry-derived elemental values (314mg / 272mg) were BELOW the 350mg UL, so
UL_EXCEED did not fire in prior runs. This correction is the source of the grade moves
C→D for four products in the v3 authoritative run (TASK-384).

---

## 4. Original Audit Sections Retained

The original audit's findings for products NOT corrected above remain valid and are not repeated
here for brevity. The original document's conclusions about:
- citrate/bisglycinate/malate/taurate/hydroxide products declaring elemental = CORRECT
- Solgar blend = elemental per US label = CORRECT
- Amorphicure/TRIOMAG/Max 550 ambiguous status = UNCHANGED
- Full-Mag Hadas form resolution (bisglycinate/122mg) = CORRECT

---

## 5. Evidence Registry

| Source | Products | Confirmation |
|--------|---------|-------------|
| tasks/_scratch_mag_labels/altman520.webp | 7290017218564 (Altman 520) | Label image: "(From Magnesium oxide) 520 מ"ג" + NRV% arithmetic |
| tasks/_scratch_mag_labels/magup.webp | 7290013142894 (Altman MagUP) | Label image: "(From Magnesium Oxide 750mg) 450 מ"ג" + NRV% arithmetic |
| tasks/_scratch_mag_labels/balance.webp | 7290019444206 (Altman Balance) | Label image: same convention as MagUP + NRV% arithmetic |
| NRV% arithmetic (TASK-384 orchestrator verification) | All four oxide products | Elemental reading: 520/280=185.7%W, 520/350=148.6%M; 450/280=160.7%W, 450/350=128.6%M |
| IL NRV reference | Women: 280mg/day, Men: 350mg/day | IL Nutrition Labeling Regulation, consistent with EU RDA 375mg |
| magnesium_ul_ruling_v1.md §1 | All four oxide products | Ruling documents NRV% verification |

---

## 6. Return Contract

```json
{
  "run_id": "magnesium_label_audit_v1_corrected_2026-06-23",
  "correction_trigger": "TASK-384 elemental reversal — orchestrator-verified NRV% math on label images",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\magnesium_label_audit_v1.md",
      "action": "rewritten",
      "description": "Oxide products corrected from COMPOUND to ELEMENTAL; Tink 520 moved to UNRESOLVED"
    }
  ],
  "counts": {
    "products_corrected": "4 (Nutricare Oxide 520, Altman 520, Altman MagUP, Altman Balance — compound->elemental)",
    "products_status_changed": "1 (Tink 520 — compound/chemistry_derived -> UNRESOLVED)",
    "products_unchanged": "14/19"
  },
  "not_done": [
    "Tink 520 label confirmation still required (analog inference insufficient)",
    "Amorphicure 160mg elemental/compound confirmation still required",
    "Supherb TRIOMAG form ratios still undisclosed",
    "Supherb Max 550 oxide:citrate ratio still undisclosed (discard candidate)"
  ]
}
```
