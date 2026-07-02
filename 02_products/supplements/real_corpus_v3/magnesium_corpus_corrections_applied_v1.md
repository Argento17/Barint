# Magnesium Corpus Corrections Applied v1

**Author:** Data Agent
**Date:** 2026-06-23
**Task:** TASK-384
**Authoritative input:** `magnesium_elemental_reconciliation_v1.md` (orchestrator-verified against altman.co.il labels)
**Scope:** 5 SKU files in `skus_full/`. No engine changes. No page changes. No other category data touched.

---

## Summary

4 categories of corrections applied to 5 SKU JSON files per owner-approved brief.

| # | SKU ID | Barcode | Action | Key change |
|---|--------|---------|--------|-----------|
| C1 | SP-7290001943700 | 7290001943700 | Form+dose fix + outcome flip | outcome: unscoreable_incomplete → scored; form: null → bisglycinate; elemental: null → 122 mg |
| C2 | SP-7290118818205 | 7290118818205 | Discard | outcome: scored → discard_recommended |
| C3a | SP-7290015429245 | 7290015429245 | Mark unresolved | verification_status: candidate → unresolved_needs_panel |
| C3b | SP-7290118816065 | 7290118816065 | Mark unresolved | verification_status: candidate → unresolved_needs_panel |
| C3c | SP-0033984005181 | 0033984005181 | Mark unresolved | verification_status: candidate → unresolved_needs_panel |

---

## Correction C1 — Full-Mag SP-7290001943700

**Action:** Set form=bisglycinate (Albion), elemental quantity=122 mg/capsule, outcome=scored.

**Prior state:** outcome=unscoreable_incomplete, form=null, quantity=null. The engine's worst-case logic
assumed oxide (fraction=0.603), giving 600×0.603=361.8mg > 350mg UL → hazard possible, unscoreable.

**Correction basis:** Multiple IL sources (tevaworld.com, drugstore.co.il, vitamins4all.co.il — all HTTP 200)
confirm the label reads "600mg magnesium bisglycinate compound / 122mg elemental magnesium". The convention
"מגנזיום (ממגנזיום ביסגליצינאט) 122 מ"ג" on a two-line label declares 122mg as the elemental value.

**Safety gate recheck:** 122mg elemental bisglycinate < 350mg UL (SUPP-EV-024). PASS. The prior
unscoreable flag is fully resolved by the form confirmation.

**Elemental basis:** label_stated_elemental. Compound=600mg bisglycinate; elemental=122mg per serving (1 capsule).

---

## Correction C2 — Max 550 SP-7290118818205

**Action:** Set outcome=discard_recommended.

**Reason:** The product states 550mg as a compound "oxide and citrate complex" but does not disclose
the oxide:citrate ratio on any accessible Israeli source (maxpharm.co.il, biogaya.co.il, or otherwise).
Without the ratio, elemental magnesium is unknowable:
- Oxide fraction = 0.603 → if all-oxide: 550×0.603 = 332mg elemental
- Citrate fraction = 0.162 → if all-citrate: 550×0.162 = 89mg elemental
- Range = 89–332mg — a 3.7× spread spanning sub-UL to near-UL

This is not a rounding issue. The elemental dose is materially unknowable. Applies the
missing-data discard rule (memory: missing_data_discard_rule). Per reconciliation doc
Section 5 discard-candidates.

The prior score of 49/D is invalidated. It was computed with dose=N/A and the blend/honesty cap
correctly fired, but the underpinning elemental ambiguity was not escalated to discard-level at
scoring time. The discard_recommended flag blocks this product from the scored corpus.

---

## Corrections C3a / C3b / C3c — Three Unresolved SKUs

These three products are NOT discarded and NOT scored-from-resolved-data. They are flagged
`verification_status=unresolved_needs_panel` with a detailed reason. Their `outcome` field is
preserved from the prior pipeline run (all three were `scored`) — that outcome is contingent on
panel resolution and should not be treated as authoritative until each is promoted.

### C3a — Amorphicure SP-7290015429245 (barcode 7290015429245)

**Issue:** Label reads "160 מ"ג מגנזיום (carbonate)" without an explicit elemental qualifier
("אלמנטרי" or "from carbonate" format). If compound: 160×0.288=46mg elemental. If elemental: 160mg.
3.5× uncertainty is material for dose scoring.

**Action needed:** Physical label photo or amorphicure.co.il full supplement-facts panel confirming
elemental vs compound declaration.

**Class:** elemental_vs_compound_ambiguous

### C3b — TRIOMAG SP-7290118816065 (barcode 7290118816065)

**Issue:** The 200mg total is likely elemental per IL convention ("מספקת 200 מ"ג" = "provides 200mg"),
but the blend form ratios (citrate:bisglycinate:taurate) are not disclosed on any accessible IL source.
Form ratios are required to resolve the form sub-score beyond "MID" and to verify per-form bioavailability
weighting. The elemental ambiguity is LOW; the form-ratio gap is the primary unresolved issue.

**Action needed:** Supherb brand label image or Super-Pharm supplement-facts panel with form ratios.

**Class:** blend_form_ratios_undisclosed

### C3c — Solgar Cal-Mag D3 SP-0033984005181 (barcode 0033984005181)

**Issue:** Panel sourced from solgar.com (US English label: 5-tab serving, 100mg magnesium as
oxide+citrate). No IL Hebrew label independently confirmed. Solgar is a global brand; the US label
value is unlikely to differ materially. Priority LOW per reconciliation doc.

**Action needed:** Israeli Hebrew supplement-facts panel from shufersal.co.il, super-pharm.co.il,
or physical label photo to confirm 100mg magnesium per 5-tab serving matches US label.

**Class:** il_label_unverified_us_source_only

---

## Correction C4 — Oxide Panel Evidence (Altman 520 / Nutricare 520)

**Task:** Confirm one official oxide panel showing 520mg is the COMPOUND mass, not elemental.

**Result: CONFIRMED — two IL sources independently verified.**

### Source A — Altman 520 (barcode 7290017218564)

- **URL:** https://www.altman.co.il/shop/magnesium/magnesium-520/
- **HTTP status:** 200 (live fetch 2026-06-23)
- **Exact Hebrew label text:** `"מגנזיום (From Magnesium oxide) 520 מ"ג"`
- **Reading:** The `(From Magnesium oxide)` qualifier is the standard Supplement Facts compound-
  declaration format. "מגנזיום X מ"ג FROM Magnesium oxide" means: the compound used is magnesium
  oxide, and the COMPOUND mass is 520mg. Elemental = 520 × 0.603 = 313.6mg.
- **Serving size:** 1 capsule daily

### Source B — Nutricare Oxide 520 (barcode 7290001065662)

- **URL:** https://www.maxpharm.co.il/products/520-100
- **HTTP status:** 200 (live fetch 2026-06-23)
- **Exact Hebrew label text:** `"מגנזיום (ממגנזיום אוקסיד) 520 מ"ג"`
- **Reading:** `ממגנזיום אוקסיד` = "from magnesium oxide" — compound-mass declaration. Compound=520mg,
  elemental ≈ 313mg (×0.603).
- **Serving size:** 1 capsule daily

**Conclusion:** Both IL sources confirm the compound-mass reading that C3 flagged. The 520mg figure
represents the magnesium oxide compound. The elemental (~313–314mg) is within UL (350mg). The engine's
SUPP-EV-030 path that stores compound and derives elemental internally is correct for these products.
No SKU corrections are needed for Altman 520 or Nutricare 520 — their stored amounts (520mg compound)
are already correct.

This evidence is the IL-source confirmation required by the brief. It is recorded here as the corpus
note; the reconciliation_v1.md Section 7 evidence registry already lists both URLs as HTTP 200.

---

## Files Edited

1. `skus_full/SP-7290001943700.json` — Full-Mag 600 (C1: form+dose fix, outcome flip)
2. `skus_full/SP-7290118818205.json` — Max 550 (C2: discard_recommended)
3. `skus_full/SP-7290015429245.json` — Amorphicure pH (C3a: unresolved_needs_panel)
4. `skus_full/SP-7290118816065.json` — TRIOMAG (C3b: unresolved_needs_panel)
5. `skus_full/SP-0033984005181.json` — Solgar Cal-Mag D3 (C3c: unresolved_needs_panel)

## Files NOT Edited

- Engine files (`run_full.py`, scoring modules) — untouched per brief
- Any other category's SKU files — untouched
- Frontend page / comparison JSON — untouched (page is OFFLINE)
- Other corpus documents — not modified by this correction pass

## What Is NOT Done (next stage)

- Full corpus re-score — not done; that is the next stage (requires Nutrition Agent + Product Agent
  co-sign per TASK-384 scope)
- Promotion of unresolved SKUs to verified — awaits physical label photos
- Page re-generation — page is OFFLINE; publishing requires owner+Product co-sign (tripwire 1)
