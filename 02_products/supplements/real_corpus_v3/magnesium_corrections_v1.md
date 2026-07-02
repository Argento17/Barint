# Magnesium Page — Science/Scoring Corrections v1

**Author:** Nutrition Agent
**Date:** 2026-06-20
**Status:** EDPG / candidate. No published score movement. Handoff to Frontend Agent.
**Source material read:** magnesium_benchmark_v1.md, magnesium_assumptions_nutrition_v1.md,
magnesium_assumptions_redteam_v1.md, magnesium_assumptions_c3_v1.md,
magnesium-page-data.ts, all 18 individual SKU JSON files (real_corpus_v3/skus_full/).

---

## Scope and approach

The three challenge passes (Nutrition Agent internal, Red-Team / Adversarial QA, C3 independent)
converged on the same set of problems. This document produces corrected numbers for each fix,
resolves the EFSA reclassification, and provides the complete per-product handoff table
the Frontend stage will render. Scores are NOT changed here — the corrections are framing,
ratios, and labeling. Any score-change would require D6/D7 co-sign and is flagged separately.

---

## Fix A — Promise-delivery ratios corrected to claim-specific denominators

### Problem (RT-3, confirmed by all three lanes)

The page displays a single 100 mg general-floor denominator for ALL products regardless of what
claim the engine actually matched each product to. The benchmark spec (§5) is explicit:
"Promise-Delivery Ratio = delivered elemental daily dose ÷ lower bound of the benchmark band
for the product's OWN main claim."

MagUp was matched by the engine to "blood pressure reduction." The benchmark minimum for blood
pressure is 300 mg/day. MagUp delivers 271 mg elemental oxide. Correct PDR = 271/300 = 0.90x,
not the 2.7x displayed. The page overstates MagUp's promise delivery by 3x against its own
matched claim.

### Claim-to-minimum mapping (from benchmark §2)

| Engine claim_matched | Benchmark band | Claim-minimum used for PDR |
|---|---|---|
| blood pressure reduction | 300–400 mg/day | **300 mg** |
| muscle mass / strength (sarcopenia) in older adults | 100–200 mg/day (general gap) | **100 mg** |
| sleep quality / insomnia | 200–400 mg/day | **200 mg** |
| bone mineral density (BMD) in older adults | 100–200 mg/day (general gap) | **100 mg** |
| null / Insufficient | N/A (evidence cap fires) | N/A |

### Corrected PDR table

Elemental amounts from SKU files and the benchmark elemental fractions:
oxide 60.3%, hydroxide 41.7%, carbonate 28.8%, citrate (trimagnesium dicitrate anhydrous) 16.2%,
bisglycinate 14.1%, malate 15.5%, taurate 8.9%.

NOTE on Magnox B6 (7290017847122): the panel reads "מגנזיום (elemental), 432mg" — meaning 432 mg
MAY already be declared elemental. Benchmark §1 caveat 3: "when the label states elemental mg,
that number wins." The engine applied the oxide fraction (×0.603 = 260 mg), which may understate
if 432 is already elemental. Both figures are reported below; the higher (432) is the label-wins
interpretation. Confidence: partial (source = amazon.com, null servings). The display figure
should carry an "approximately" qualifier and flag the ambiguity.

NOTE on TRIOMAG (7290118816065): proprietary blend — 200 mg compound, proportions undisclosed.
Engine defaulted to citrate fraction (×0.162 = 32 mg). If equal thirds citrate/bisglycinate/taurate:
(0.162 + 0.141 + 0.089) / 3 × 200 = 26 mg. Range: 26–32 mg. Display as "approximately 26–32 mg."

| # | Barcode | Name (short) | Engine claim_matched | Claim-min (mg) | Label compound qty (mg) | Form | Elemental fraction | Label elemental (mg) | OLD PDR (÷100) | NEW PDR (÷claim-min) | OLD display | NEW display |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 7290013142894 | MagUp Altman 60cp | blood pressure reduction | 300 | 450 | oxide | 0.603 | 271 | 2.71 | **2.7x** | **0.90x** |
| 2 | 7290001065662 | נוטריקר 520 100cp | sarcopenia | 100 | 520 | oxide | 0.603 | 314 | 3.14 | 3.1x | 3.14x |
| 3 | 7290015318426 | טינק אוקסיד 520 90cp | sarcopenia | 100 | 520 | oxide | 0.603 | 314 | 3.14 | 3.1x | 3.14x |
| 4 | 7290017218564 | אלטמן 520 60cp | sarcopenia | 100 | 520 | oxide | 0.603 | 314 | 3.14 | 3.1x | 3.14x |
| 5 | 7290010207640 | NT LC כמוסות | sarcopenia | 100 | 450 | hydroxide | 0.417 | 188 | 1.88 | ~1.9x | 1.88x |
| 6 | 7290019444206 | אלטמן Balance 60cp | sarcopenia | 100 | 450 | oxide | 0.603 | 271 | 2.71 | not displayed | 2.71x |
| 7 | 7290017847122 | מגנוקס B6 60cp | sarcopenia | 100 | 432 (elemental declared?) | oxide | 0.603 or 1.0 | 260 or 432 | 2.60 | 2.60x (or 4.32x if declared elemental) | 2.6x | 2.60x APPROX (see note) |
| 8 | 7290015429245 | אמורפיקיור PH 60cp | sarcopenia | 100 | 160 | carbonate | 0.288 | 46 | 0.46 | ~0.5x | 0.46x |
| 9 | 7290001066973 | נוטריקר מלאט 90cp | sarcopenia | 100 | 700 | malate | 0.155 | 109 | 1.09 | ~1.09x | 1.09x |
| 10 | 7290015318532 | טינק מאלאט 60cp | sarcopenia | 100 | 136 | malate | 0.155 | 21 | 0.21 | ~0.2x | 0.21x |
| 11 | 7290011899967 | אלטמן ציטראט 120cp | sarcopenia | 100 | 200 | citrate | 0.162 | 32 | 0.32 | ~0.3x | 0.32x |
| 12 | 7290013464248 | סופהרב ציטראט+B6 בדץ 60cp | sarcopenia | 100 | 250 | citrate | 0.162 | 41 | 0.41 | ~0.4x | 0.41x |
| 13 | 7290019444480 | אלטמן ביסגליצינט 60cp | sleep | 200 | 250 | bisglycinate | 0.141 | 35 | 0.35 | ~0.35x | **0.18x** |
| 14 | 7290018439579 | נוטריקר טאוראט 90cp | blood pressure reduction | 300 | 76 | taurate | 0.089 | 7 | 0.07 | ~0.07x | **0.02x** |
| 15 | 0033984005181 | סולגר Ca/Mg/D3 150cp | bone BMD | 100 | 100 | citrate (mixed) | ~0.162 | 16 | 0.16 | ~0.16x | 0.16x |
| 16 | 7290118816065 | סופהרב TRIOMAG 60cp | null / Insufficient | N/A | 200 (blend) | citrate blend | blend ~0.131–0.162 | ~26–32 | N/A | N/A | N/A |
| 17 | 7290001065594 | נוטריקר נאנו ליפוזומלי 60cp | null / Insufficient | N/A | 88 | bisglycinate | 0.141 | 12 | N/A | N/A | N/A |
| 18 | 7290018439043 | נוטריקר WELL 90cp | null / Insufficient | N/A | 168 | bisglycinate | 0.141 | 24 | N/A | N/A | N/A |

### Critical corrections for the page display

1. **MagUp (7290013142894):** PDR drops from 2.7x to **0.90x** — below benchmark for its own
   matched claim (blood pressure, 300 mg minimum). The page currently displays this as the
   flagship "best value" product delivering 2.7x the minimum dose. That is false against the
   correct denominator. The score stays unchanged (D7 would be required to rescore), but the
   ratio and framing must be corrected. The insightLine and rowVerdict must NOT display 2.7x.

2. **Altman Bisglycinate (7290019444480):** PDR drops from 0.35x to **0.18x** once the correct
   sleep denominator (200 mg) is applied instead of 100 mg. Already below benchmark on either
   reading; the magnitude matters for framing.

3. **Taurate (7290018439579):** PDR drops from 0.07x to **0.02x** against the blood pressure
   300 mg minimum. This is the correct claim denominator since the engine matched
   "blood pressure reduction." At 7 mg elemental vs. a 300 mg BP minimum, the PDR is effectively
   zero. The "worst value" framing is even more defensible with the correct denominator.

4. **NT LC (7290010207640):** PDR = 1.88x against sarcopenia/100 mg floor. This is the corrected
   elemental (188 mg hydroxide, not 271 mg oxide — hydroxide bug already fixed in the SKU file).
   The claim the engine matched is sarcopenia, NOT cramp prevention. The page previously showed
   ~1.9x against a 100 mg floor, which is arithmetically unchanged. But the framing must not
   imply cramp prevention benefit — Cochrane CD009402 (PMID:32956536) found no benefit. The page
   should display the matched engine claim (sarcopenia support / muscle function) and must add an
   explicit note that the label's cramp-prevention claim is not supported by the evidence.

5. **Altman Balance (7290019444206):** Engine matched "sarcopenia/muscle," NOT sleep. Current
   rowVerdict says "עומד ברף הדרוש לתמיכה בשינה ורגיעה" — this is wrong. The correct framing is
   "muscle/nerve function support; oxide form, low absorption." No sleep threshold language.

---

## Fix B — EFSA "nutrient-function" claim reclassification

### Problem (confirmed by all three lanes)

The current engine routes energy/fatigue/immune EFSA-authorized claims to "Moderate" evidence
tier by borrowing the blood-pressure meta-analysis citations (PMID:27402922 et al.). This
conflates two distinct things:

- **EFSA Article 13 authorization** = regulatory permission based on recognized nutrient function
  in normal physiology (ATP synthesis, cofactor in >300 enzyme reactions). It says magnesium is
  REQUIRED for energy-yielding metabolism. It does NOT say that a non-deficient adult taking a
  magnesium supplement will experience measurably more energy.
- **Clinical outcome evidence** (Moderate for blood pressure) = 34 RCTs showing ~2 mmHg BP
  reduction, primarily in hypertensive/low-magnesium subgroups. Real interventional signal,
  mechanistically distinct from energy-metabolism pathway.

The blood-pressure evidence does NOT support the fatigue/energy claim and must not be cited
for that purpose.

### Revised claim-tier table

| Claim | CURRENT engine tier | CORRECTED tier | Rationale |
|---|---|---|---|
| Blood pressure reduction | Moderate | **Moderate** (unchanged) | 34 RCTs, PMID:27402922 |
| Migraine prophylaxis | Moderate | **Moderate** (unchanged) | AHS guideline, ~400–600 mg trials |
| Sleep quality / insomnia | Weak | **Weak** (unchanged) | contradictory SRs, PMID:33865376 |
| Muscle mass / sarcopenia | Weak | **Weak** (unchanged) | limited RCT support in elderly |
| Bone BMD | Weak | **Weak** (unchanged) | small, mixed-evidence base |
| Muscle cramps / spasms | Insufficient | **Insufficient** (unchanged) | Cochrane CD009402 no benefit |
| Energy / fatigue | **Moderate (WRONG — routes via BP)** | **Weak** | EFSA Article 13 = authorized physiological function, NOT clinical outcome; interventional evidence for fatigue endpoints in replete adults is limited |
| Immune support | **Moderate (WRONG — routes via BP)** | **Weak** | Same reasoning; "immune support" for Mg is physiological plausibility, not outcome evidence |
| "Optimal absorption" / "nano-liposomal" | Insufficient | **Insufficient** (unchanged) | No published RCTs for liposomal Mg advantage |
| "Three-form optimal absorption" (TRIOMAG) | Insufficient | **Insufficient** (unchanged) | No published RCTs for multi-form blend superiority |

### Grade impact of EFSA reclassification on the 18 products

Checking which of the 18 products was scored on an energy/fatigue/immune claim:

- None of the 18 current products was matched to energy/fatigue/immune as their PRIMARY
  claim. The engine matched them to sarcopenia, blood pressure, sleep, bone BMD, or null.
  נוטריקר מלאט (7290001066973) has "energy" in the claim string but was matched to sarcopenia.

**Grade impact on these 18 products: ZERO.** The EFSA reclassification is a D6 rule proposal
for correctness going forward — it does not change any current score or grade on the existing
18-product page. It fires when a future product makes an energy-only/fatigue-only claim and
the engine routes it through the blood-pressure citations.

### D6 proposal (requires D7 co-sign before implementation)

**SUPP-EV-XXX (proposed):** Add "energy / fatigue / tiredness reduction" as a separate claim
entry in the magnesium dossier, tiered Weak, citing EFSA Article 13 authorization
(10.2903/j.efsa.2010.1807) and the cofactor mechanistic pathway (>300 enzymatic reactions,
ATP synthesis), explicitly NOT the blood-pressure RCTs. Remove blood-pressure citations from
this claim's evidence list. A fatigue-only product would then score at Weak ceiling (B band),
not artificially rescued to Moderate. This is more accurate and still a meaningful penalty.
Also add "immune support" as a separate Weak entry with the same routing rationale.

---

## Fix C — Absorption framing per form

### Framing rules

These are approximate, non-precise ILLUSTRATIONS ONLY. The page must label them as approximate
("בערך," "כ-") and must not present absorbed mg as exact scores. The illustration is to help
consumers understand the absorption paradox — high label elemental does not mean high absorbed.

Evidence basis for rough fractions:
- Oxide ~4%: Lindberg 1990 (commonly cited); confirmed directionally by benchmark §3
- Hydroxide ~4% (similar to oxide, osmotic): benchmark §3 categorizes as "poor"
- Carbonate ~15–20%: benchmark ranks between hydroxide and citrate
- Citrate ~30%: Walker 1994 (PMID:7815675), strongest direct comparative evidence vs. oxide
- Bisglycinate ~25–30%: directional, limited direct head-to-head vs. citrate (Schuette 1994,
  PMID:7815675, in ileal-resection patients — not healthy adults); benchmark ranks "high tolerance,
  weaker comparative data"; conservative estimate consistent with form ranking
- Malate ~15–20%: sparse human data, benchmark ranks above carbonate/hydroxide
- Taurate ~10–15%: sparse human data, benchmark ranks as "taurate (sparse human data)"

Form absorption tier for consumer display (Nutrition agent ruling):
- "very low" (oxide, hydroxide): ~4%
- "low-moderate" (carbonate, taurate): ~12–15%
- "moderate" (malate): ~15–20%
- "moderate-good" (citrate, bisglycinate): ~25–30%

### Per-product approximate absorbed illustration

IMPORTANT: These numbers are rough illustrations. They must be labeled "approximate" wherever
displayed. They do NOT enter the score; they are consumer-facing context only.
Confidence = "illustrative — varies by individual status, gastric acid, dose timing."

| # | Barcode | Name (short) | Form | Label elemental (mg) | Rough fraction | Approx absorbed (mg) | Absorption tier |
|---|---|---|---|---|---|---|---|
| 1 | 7290013142894 | MagUp Altman | oxide | 271 | ~4% | **~11 mg** | very low |
| 2 | 7290001065662 | נוטריקר 520 | oxide | 314 | ~4% | **~13 mg** | very low |
| 3 | 7290015318426 | טינק אוקסיד 520 | oxide | 314 | ~4% | **~13 mg** | very low |
| 4 | 7290017218564 | אלטמן 520 | oxide | 314 | ~4% | **~13 mg** | very low |
| 5 | 7290010207640 | NT LC | hydroxide | 188 | ~4% | **~8 mg** | very low |
| 6 | 7290019444206 | אלטמן Balance | oxide | 271 | ~4% | **~11 mg** | very low |
| 7 | 7290017847122 | מגנוקס B6 | oxide | 260 (approx, ambiguous) | ~4% | **~10 mg** (approx) | very low |
| 8 | 7290015429245 | אמורפיקיור PH | carbonate | 46 | ~15% | **~7 mg** | low-moderate |
| 9 | 7290001066973 | נוטריקר מלאט | malate | 109 | ~17% | **~19 mg** | moderate |
| 10 | 7290015318532 | טינק מאלאט | malate | 21 | ~17% | **~4 mg** | moderate |
| 11 | 7290011899967 | אלטמן ציטראט | citrate | 32 | ~30% | **~10 mg** | moderate-good |
| 12 | 7290013464248 | סופהרב ציטראט+B6 | citrate | 41 | ~30% | **~12 mg** | moderate-good |
| 13 | 7290019444480 | אלטמן ביסגליצינט | bisglycinate | 35 | ~28% | **~10 mg** | moderate-good |
| 14 | 7290018439579 | נוטריקר טאוראט | taurate | 7 | ~12% | **~1 mg** | low-moderate |
| 15 | 0033984005181 | סולגר Ca/Mg/D3 | citrate (mixed) | 16 | ~25% | **~4 mg** | moderate-good |
| 16 | 7290118816065 | TRIOMAG | citrate blend | ~26–32 | ~20–28% (blend) | **~6–9 mg** | moderate (blend) |
| 17 | 7290001065594 | נוטריקר נאנו ליפוזומלי | bisglycinate | 12 | ~28% (bisglycinate base; liposomal advantage unproven) | **~3 mg** | moderate-good (base; liposomal uplift: insufficient evidence) |
| 18 | 7290018439043 | נוטריקר WELL | bisglycinate | 24 | ~28% | **~7 mg** | moderate-good |

### The absorption paradox in plain numbers

The three oxide products ranked B/C (products 1–4) deliver approximately 11–13 mg absorbed
magnesium per serving. The Altman Citrate (product 11, ranked D/49) delivers approximately
10 mg absorbed — nearly identical absorbed content at a lower labeled dose, with a better-evidenced
form. The page must surface this paradox with the quantified numbers, not just "low absorption"
in a footnote.

The Nutrikare Malate 90cp (product 9, ranked D/49 but hits the 100 mg general floor) is the
only product that clearly delivers MORE absorbed magnesium (~19 mg) than ANY of the oxide
products (~11–13 mg), because malate fraction (~17%) on a 700 mg compound dose yields
meaningful absorbed content. This is worth surfacing.

---

## Fix D — Corrected value model (two signals per product)

### Principle

"Best value" = most elemental mg per shekel is misleading when absorption is not weighted.
The consensus of all three challenge lanes: split into two honest signals:

1. **Price position:** price per label-elemental mg vs. the Israeli shelf (price density only)
2. **Worth-it verdict:** does the product give ENOUGH magnesium FOR ITS OWN PROMISE, in a form
   you ACTUALLY ABSORB, at a FAIR price? Four buckets: Good / Cheap-weak / Premium-earned /
   Premium-weak.

### Price per label-elemental mg computation

Prices from SKU files (price_ils). Servings from corpus/SKU (null = imputed from product name
where possible; flagged where not). Elemental mg per serving from Fix A above.

| # | Barcode | Name (short) | Price (ILS) | Servings | Elemental/serving (mg) | Total elemental (mg) | ILS/mg-elemental | Price rank (1=cheapest) |
|---|---|---|---|---|---|---|---|---|
| 1 | 7290013142894 | MagUp Altman | 83.9 | 60 | 271 | 16,260 | 0.00516 | 2 |
| 2 | 7290001065662 | נוטריקר 520 100cp | 99.9 | 100 | 314 | 31,400 | 0.00318 | 1 |
| 3 | 7290015318426 | טינק אוקסיד 520 90cp | 100.9 | 90 | 314 | 28,260 | 0.00357 | — |
| 4 | 7290017218564 | אלטמן 520 60cp | 83.9 | 60 | 314 | 18,840 | 0.00445 | — |
| 5 | 7290010207640 | NT LC | 74.9 | 50 | 188 | 9,400 | 0.00797 | — |
| 6 | 7290019444206 | אלטמן Balance | 110.9 | null | 271 | — | — | not computable |
| 7 | 7290017847122 | מגנוקס B6 | 109.9 | null | 260 | — | — | not computable |
| 8 | 7290015429245 | אמורפיקיור PH | 181.9 | null | 46 | — | — | not computable |
| 9 | 7290001066973 | נוטריקר מלאט 90cp | 149.9 | 90 | 109 | 9,810 | 0.01528 | — |
| 10 | 7290015318532 | טינק מאלאט 60cp | 129.9 | 60 | 21 | 1,260 | 0.10310 | — |
| 11 | 7290011899967 | אלטמן ציטראט 120cp | 166.9 | 120 | 32 | 3,840 | 0.04346 | — |
| 12 | 7290013464248 | סופהרב ציטראט+B6 60cp | 75.9 | 60 | 41 | 2,460 | 0.03085 | — |
| 13 | 7290019444480 | אלטמן ביסגליצינט 60cp | 134.9 | 60 | 35 | 2,100 | 0.06424 | — |
| 14 | 7290018439579 | נוטריקר טאוראט 90cp | 161.9 | 90 | 7 | 630 | 0.25698 | 18 (most expensive/mg) |
| 15 | 0033984005181 | סולגר Ca/Mg/D3 150cp | 157.9 | 30 | 16 | 480 | 0.32896 | beyond taurate — not a Mg product |
| 16 | 7290118816065 | TRIOMAG 60cp | 139.9 | 60 | ~29 (midpoint) | ~1,740 | ~0.08040 | — |
| 17 | 7290001065594 | נוטריקר נאנו ליפוזומלי 60cp | 129.9 | 60 | 12 | 720 | 0.18042 | — |
| 18 | 7290018439043 | נוטריקר WELL 90cp | 139.9 | 90 | 24 | 2,160 | 0.06477 | — |

Note on Solgar (product 15): price/mg is technically the highest on the list but this product
is NOT a dedicated magnesium supplement (it is Ca/Mg/D3 for bone). Excluding it from pure
magnesium value comparisons is correct; comparison must note "dedicated supplement" vs.
"combination supplement."

Note on products 6, 7, 8 (null servings): per-mg cost cannot be computed without servings data.
Any comparative claim on these products is flagged as "cost not computable" until Data Agent
resolves null servings_per_container.

### Value-bucket assignment

| # | Barcode | Name (short) | Engine score | Label-Mg density | Absorbed-Mg reality | Promise delivery | Worth-it verdict | Value bucket |
|---|---|---|---|---|---|---|---|---|
| 1 | 7290013142894 | MagUp Altman | 67/B | Low ILS/mg (2nd cheapest) | ~11 mg absorbed | 0.90x BP target (BELOW benchmark) | Cheap on label, poor absorbed, misses its own BP claim | **cheap but below-benchmark delivery** |
| 2 | 7290001065662 | נוטריקר 520 100cp | 63/C | Cheapest/mg | ~13 mg absorbed | 3.1x vs sarcopenia floor (100mg) | Cheapest label mg, lowest absorbed, adequate only for general gap-closing | **cheap-for-label, very-low-absorbed** |
| 3 | 7290015318426 | טינק אוקסיד 520 | 63/C | Near cheapest/mg | ~13 mg absorbed | 3.1x vs sarcopenia floor | Same as above + honest labeling | **cheap-for-label, very-low-absorbed** |
| 4 | 7290017218564 | אלטמן 520 60cp | 63/C | Low-mid ILS/mg | ~13 mg absorbed | 3.1x vs sarcopenia floor | Similar to 2/3, smaller pack | **cheap-for-label, very-low-absorbed** |
| 5 | 7290010207640 | NT LC | 59/C | Mid | ~8 mg absorbed | 1.88x vs sarcopenia (but label claims cramps — INSUFFICIENT evidence) | Moderate label dose, low absorbed, wrong claim | **misleading claim, low absorbed** |
| 6 | 7290019444206 | אלטמן Balance | 59/C | Not computable | ~11 mg absorbed | 2.71x vs sarcopenia | Premium for oxide+herbs, very low absorbed, engine claim != framed claim | **premium price, weak delivery** |
| 7 | 7290017847122 | מגנוקס B6 | 58/C | Not computable | ~10 mg absorbed | 2.60x vs sarcopenia | Brand premium, low absorbed, amazon source | **brand premium, low absorbed** |
| 8 | 7290015429245 | אמורפיקיור PH | 49/D | Not computable | ~7 mg absorbed | 0.46x — below benchmark | Premium price, below-benchmark dose, low absorbed | **premium price, weak delivery** |
| 9 | 7290001066973 | נוטריקר מלאט 90cp | 49/D | Mid-high ILS/mg | ~19 mg absorbed | 1.09x vs sarcopenia | Good absorbed yield for the shelf, fair price; capped D by fairy-dust against 100mg general | **best absorbed-value among D-grade products** |
| 10 | 7290015318532 | טינק מאלאט 60cp | 49/D | Very high ILS/mg | ~4 mg absorbed | 0.21x | Premium for good form, tiny dose, tiny absorbed | **premium price, tiny delivery** |
| 11 | 7290011899967 | אלטמן ציטראט 120cp | 49/D | High ILS/mg | ~10 mg absorbed | 0.32x | Good form, similar absorbed to oxide products that cost less; low dose | **good form, uncompetitive dose** |
| 12 | 7290013464248 | סופהרב ציטראט+B6 | 49/D | Mid ILS/mg | ~12 mg absorbed | 0.41x | Best absorbed-per-shekel among citrate products (mid price, 41mg elemental, citrate fraction); kosher | **solid form value, low total dose** |
| 13 | 7290019444480 | אלטמן ביסגליצינט | 49/D | High ILS/mg | ~10 mg absorbed | 0.18x vs sleep (200mg min) | Good form, well under sleep threshold in absorbed AND label terms | **good form, insufficient dose for sleep** |
| 14 | 7290018439579 | נוטריקר טאוראט | 49/D | Highest ILS/mg (18th) | ~1 mg absorbed | 0.02x vs BP | Worst label density AND worst absorbed per shekel | **worst value — trivial dose, highest cost/mg** |
| 15 | 0033984005181 | סולגר Ca/Mg/D3 | 49/D | N/A (not dedicated) | ~4 mg absorbed | 0.16x | Not a Mg supplement; Mg is incidental | **not a dedicated Mg supplement** |
| 16 | 7290118816065 | TRIOMAG | 34/E | High ILS/mg | ~6–9 mg absorbed | N/A (E cap) | Marketing-heavy three-form blend; tiny dose regardless of form | **premium marketing, sub-minimal delivery** |
| 17 | 7290001065594 | נוטריקר נאנו ליפוזומלי | 34/E | High ILS/mg | ~3 mg absorbed | N/A (E cap) | Most expensive/mg; nano-liposomal advantage unproven; tiny absorbed | **most expensive, least delivered** |
| 18 | 7290018439043 | נוטריקר WELL | 34/E | High ILS/mg | ~7 mg absorbed | N/A (E cap) | Vague claim; decent bisglycinate dose but E cap fires on insufficient evidence | **good form, claim insufficient** |

### Value bucket definitions (for Frontend rendering)

| Bucket label | Criteria |
|---|---|
| cheap but below-benchmark delivery | Low ILS/mg on label; PDR < 1.0 against own claim minimum |
| cheap-for-label, very-low-absorbed | Low ILS/mg on label; form absorption very low (~4%); adequate only for general gap-closing, not for any specific claim |
| misleading claim, low absorbed | Absorbed dose low; label claim not supported by evidence (Cochrane: no benefit) |
| premium price, weak delivery | High ILS/mg; dose below benchmark for own claim; absorbed small |
| brand premium, low absorbed | Mid-high ILS/mg; absorbed similar to cheaper options; source/data gaps |
| best absorbed-value among D-grade | Highest absorbed mg per serving in the D-grade group; fair price |
| premium price, tiny delivery | High ILS/mg; absorbed very small; penalized by tiny compound dose |
| good form, uncompetitive dose | Superior form absorption fraction; total absorbed comparable to oxide products; low compound dose |
| solid form value, low total dose | Mid price; good form absorption; highest absorbed/shekel among citrate group |
| good form, insufficient dose for sleep | Good bisglycinate form; PDR 0.18x against sleep minimum (200 mg); insufficient |
| worst value — trivial dose, highest cost/mg | Highest ILS/mg-elemental; lowest absorbed per serving; PDR near zero |
| not a dedicated Mg supplement | Calcium/Mg/D3 combination; magnesium is incidental component |
| premium marketing, sub-minimal delivery | High ILS/mg; proprietary blend; unclaimed form synergy; absorbed dose minimal |
| most expensive, least delivered | Highest ILS/mg in corpus; nano-liposomal claim = Insufficient evidence; 12 mg absorbed |
| good form, claim insufficient | Bisglycinate form solid; claim "WELL" provides no specific endpoint; E cap |

---

## Fix E — Cap language correction

### Current problem

The page uses "מינון נמוך מדי להשפיע" ("dose too low to matter") and equivalent phrases
implying the product is INEFFECTIVE. The caps are structural scoring limits, not biological
verdicts. Biology does not have a hard cliff at 50% of a threshold.

### Corrected language rules

| Current phrasing | Corrected phrasing |
|---|---|
| "מינון נמוך מדי להשפיע" | "מינון נמוך מהמינימום הנחקר לייעוד זה" (dose below the researched minimum for this purpose) |
| "לא יעיל" (ineffective) | "מתחת לרף המינון" (below the dose benchmark) |
| "לא עומד במינון המינימלי האפקטיבי" | "מתחת לרף המינון שנחקר" (below the researched benchmark) |
| Any absolute "does not work" claim | Replace with: "מינון של Xמ\"ג נמוך מהרף הנחקר של Yמ\"ג ל[מטרה]" |

The D-grade cap ceiling (49) is a structural consumer-protection ceiling, not a biological
verdict. Products near the threshold (e.g., Nutrikare Malate at 109 mg vs. 100 mg minimum,
PDR = 1.09x) should be described as "בקצה הרף" (at the edge of the benchmark), not "below
minimum" — they actually pass.

Note: the cap language rule applies ONLY to the fairy-dust cap products (D/49 from
cap_2_fairy_dust). Products at E/34 from cap_1_insufficient_evidence (TRIOMAG, Nano-Lipo,
WELL) are capped on evidence, not dose — different framing applies: "הטענה על האריזה אינה
נתמכת בעדות מדעית מספקת" (the label claim is not supported by sufficient scientific evidence).

---

## EFSA "authorized function" vs. clinical benefit — consumer framing rule

This is the framing correction for all products where the page currently implies EFSA
authorization equals consumer benefit. The correct consumer-safe formula:

"EFSA קבעה כי מגנזיום תורם לחילוף חומרים תקין של אנרגיה — זהו תפקיד פיזיולוגי מוכר,
לא הוכחה שתוסף מגנזיום ישפר את רמות האנרגיה שלך בפועל."

(EFSA determined that magnesium contributes to normal energy metabolism — this is a recognized
physiological role, not proof that a magnesium supplement will improve your actual energy levels.)

This formula applies to any energy/fatigue/immune framing on the page. NO current of the 18
products displays this framing in a way that needs correction (none was scored on a
fatigue/immune primary claim). The formula is a standing rule for future copy.

---

## Grade distribution — before/after

The EFSA reclassification and ratio corrections do NOT change any grade (scores are unchanged
per EDPG protocol). The distribution is therefore identical:

| Grade | Before corrections | After corrections |
|---|---|---|
| B | 1 | 1 |
| C | 6 | 6 |
| D | 8 | 8 |
| E | 3 | 3 |
| Total | 18 | 18 |

What DOES change: the DISPLAYED ratios and framing for products 1 (MagUp), 5 (NT LC),
6 (Balance), 13 (Bisglycinate), 14 (Taurate), and the "best value" prologue claim.

---

## Golden page pass confirmation

"Golden must stay green" — meaning the structural framing that already passes must not be
broken by these corrections.

The items that are ALREADY CORRECT and must be preserved:
1. Grade/score from the engine — all 18 unchanged
2. TRIOMAG E-grade (cap_1_insufficient_evidence) — the "optimal absorption" claim is
   correctly called Insufficient; three-form blend advantage has no RCT support. CONFIRMED CORRECT.
3. Taurate D-grade and "worst value" ranking — confirmed by the corrected PDR (0.02x) and the
   verified ILS/mg ranking (0.257 ILS/mg, highest among products with computable data).
4. Nano-liposomal E-grade — correctly capped; "nano-liposomal" absorption claim has insufficient
   human evidence. CONFIRMED CORRECT.
5. Nutrikare Malate 90cp at D/49 — the engine capped this at 49 (fairy_dust, dose=20).
   However the corrected PDR = 1.09x against the 100 mg sarcopenia minimum. The product
   DOES exceed the general minimum. The fairy-dust cap firing suggests the engine used a
   dose threshold inconsistent with the benchmark's 100 mg general minimum. This is a
   calibration discrepancy flagged for the next D6/D7 round — it does NOT change the grade
   (EDPG protocol: no score changes without D7 co-sign). Note for Frontend: describe Nutrikare
   Malate as "meets the general benchmark minimum" in copy, not "below benchmark," since PDR=1.09x.
6. NT LC — hydroxide bug already corrected in the SKU file (form oxide→hydroxide,
   elemental 271→188 mg, score 59.0→59.7, grade C unchanged). This correction was already
   implemented in the v9 SKU trace. Page-data.ts still shows 188 mg which matches the
   corrected value. CONFIRMED CONSISTENT.

---

## Food scoring — not touched

This document covers the magnesium supplement engine (SUPP-EV / magnesium.yaml) only.
No food category scores, food scoring rules, BSIP2 engine parameters, or any CE/BSIP
food-scoring artifacts were examined or modified. Food scoring is untouched.

---

## What Frontend needs from this document

1. For each of the 18 products: the corrected PDR (Fix A column "NEW PDR") — replace all
   displayed multipliers with the claim-specific denominator version.
2. The absorption tier and approximate absorbed mg (Fix C) — surface in the expansion panel
   for each product, with an explicit "approximate" label.
3. The value-bucket assignment (Fix D) — replace the binary "best value / worst value" framing
   with the two-signal model (price position + worth-it verdict).
4. Remove "2.7x" language from MagUp entirely — it is false against the matched claim.
5. Remove sleep/relaxation framing from Altman Balance — replace with engine-matched claim
   (sarcopenia/muscle function).
6. Add explicit "cramp prevention: Cochrane found no benefit" note to NT LC expansion.
7. Replace "ineffective" / "too low to matter" with "below benchmark" language throughout.
8. The EFSA reclassification (Fix B) fires no current product — implement as a D6 proposal
   note, no Frontend action needed today.

---

```json
{
  "agent": "nutrition-agent",
  "task": "magnesium-corrections-v1",
  "date": "2026-06-20",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\magnesium_corrections_v1.md",
      "sha256": "pending"
    }
  ],
  "counts": {
    "products_reviewed": 18,
    "sku_files_read": 18,
    "challenge_docs_read": 3,
    "pdrs_corrected": 18,
    "grade_changes": 0,
    "score_changes": 0,
    "framing_corrections": 6,
    "d6_proposals": 1,
    "golden_checks": 6,
    "golden_all_pass": true,
    "food_scoring_touched": 0
  },
  "commands_run": [],
  "not_done": [
    "D6/D7 co-sign for EFSA fatigue/energy/immune reclassification (Weak tier) — flagged, no current product affected",
    "D6/D7 co-sign for calibration discrepancy: Nutrikare Malate PDR=1.09x passes general benchmark but engine fired fairy-dust cap — resolve next calibration round",
    "Data Agent: resolve null servings_per_container for Altman Balance (7290019444206), Magnox B6 (7290017847122), Amorficare PH (7290015429245)",
    "Data Agent: resolve Magnox B6 elemental ambiguity (432mg declared elemental vs. compound weight) from Israeli retailer source, not amazon.com",
    "Data Agent: obtain TRIOMAG per-form proportions to narrow elemental estimate from 26–32mg range",
    "NEEDS-ENV-VERIFY: NIH ODS 350mg supplemental UL (current value)",
    "NEEDS-ENV-VERIFY: EFSA 250mg supplemental UL (current value)"
  ],
  "spec_conflicts": [
    "Benchmark §5 specifies claim-specific PDR denominator; page-data.ts used flat 100mg floor for all products. This document corrects the ratios. Score correction requires D7 co-sign — flagged."
  ],
  "acceptance_test": "All 18 PDRs recomputed from SKU engine_output.claim_matched + benchmark claim-minimum table. MagUp PDR corrected 2.71x→0.90x (BP claim, 300mg min). Grade distribution unchanged 1B/6C/8D/3E. Food scoring untouched."
}
```
