# BSIP-S Category Framework v1
# Bari Supplement Intelligence Protocol — Per-Category Specifications
**Date:** 2026-05-30
**Status:** Design Document v1
**Scope:** 8 initial supplement categories — full scoring specs, reference doses, form hierarchies, distortion registry

---

## How to Read This Document

Each category section contains:
1. **Evidence Tier** — category-level ceiling assignment with rationale
2. **Primary Use Case** — the intended use Bari evaluates (not all possible uses)
3. **Reference Dose Range** — the clinically studied dose range for the primary use
4. **Form Hierarchy** — product-specific form quality tiers
5. **Common Distortions** — the ways this category is routinely misrepresented
6. **Scoring Notes** — category-specific DA/FQ scoring rules
7. **Population Notes** — known needs variations by population subgroup
8. **Insight Line Examples** — calibrated consumer-facing output samples

---

## Category 1 — Magnesium

### Evidence Tier: 1
**Rationale:** Multiple high-quality RCTs across multiple health outcomes. NIH ODS classifies magnesium deficiency as common in Western diets. Effects of supplementation on serum magnesium, muscle cramps, sleep quality, and blood pressure are replicated. The specific form determines actual delivery.

### Primary Use Cases
1. Deficiency correction (primary)
2. Sleep quality (well-supported, Tier 1 for elemental magnesium with good form)
3. Muscle cramping / recovery (Tier 1 for elemental magnesium)
4. Blood pressure support (Tier 2 — effect size modest, population-dependent)
5. Anxiety / mood (Tier 2 — plausible mechanism, inconsistent RCT results)

BSIP-S scores against the primary use case (deficiency correction / general adequacy). The score does not differentiate between use case sub-applications.

### Reference Dose Range
- **Men:** 320–420 mg elemental magnesium/day (RDA: 400–420 mg)
- **Women:** 270–360 mg elemental magnesium/day (RDA: 310–360 mg)
- **Supplemental target (on top of dietary):** 100–300 mg elemental/day
- **Clinical trial range:** 200–400 mg elemental/day
- **Upper Tolerable Intake (supplemental):** 350 mg elemental/day

**BSIP-S uses 200–350 mg elemental/day as the reference scoring window.**
Below 100 mg elemental: DA score = partial/insufficient.
Above 350 mg elemental: safety note triggered (at UL; not a cap trigger unless product provides >350 mg from supplement alone).

### Form Hierarchy

| Form | FQ Score | Bioavailability | Primary Evidence | Notes |
|---|---|---|---|---|
| Glycinate (bisglycinate chelate) | Optimal (100) | ~80% | Sleep, anxiety RCTs | Best tolerated; no laxative effect at moderate dose |
| Malate | Optimal (100) | ~65% | Fibromyalgia, fatigue | Good GI tolerance |
| L-Threonate (Magtein) | Optimal (100) | ~7% elemental but CNS-specific | Cognitive; crosses BBB | Require higher compound dose for adequate elemental |
| Citrate | Acceptable (70) | ~35% | General supplementation | Laxative effect possible at high dose |
| Lactate | Acceptable (70) | ~40% | General | |
| Chloride (topical excluded) | Acceptable (70) | ~30% oral | General | |
| Oxide | Low (30) | ~4% | General (cheapest form) | "500mg oxide" = ~20mg absorbed — label is deeply misleading |
| Aspartate | Low (30) | ~40% | Historical | Excitotoxicity concern at high dose |
| Sulfate (oral) | Low (30) | ~25% oral | Primarily IV/topical | Oral absorption limited; mainly GI |
| Unspecified / "magnesium" | Unknown (20) | Cannot assess | — | Apply unknown penalty |

### Common Distortions
1. **Elemental amount concealment:** Label states "500mg Magnesium Oxide." Elemental = 300mg but absorption ~12mg. The most common single distortion in this category.
2. **Form downgrade:** Product marketed with glycinate imagery but actually uses oxide or a blend with oxide as primary component.
3. **Blend obscuring form proportion:** "Magnesium blend (glycinate, malate, oxide) 400mg" — oxide could be 80% of the blend.
4. **Underdose for sleep claims:** Many sleep products include 50–80mg elemental magnesium (well below 200mg reference) while making sleep quality claims.

### Scoring Notes
- **Elemental amount is mandatory for DA scoring.** If not calculable from label, mark DA as "partial" regardless of compound dose.
- For proprietary magnesium blends: identify listed order (first = highest proportion) and apply highest-proportion form's FQ. If oxide is first, FQ = Low regardless of other forms present.
- Magnesium L-Threonate: use compound dose for DA calculation (not elemental), since elemental fraction is low by design. Reference dose for Threonate: 1,500–2,000mg compound/day.

### Population Notes
- Athletes / heavy exercisers: higher loss through sweat → upper end of reference range more appropriate
- Older adults: absorption decreases with age → form quality more critical
- GI conditions (Crohn's, celiac): absorption impaired; glycinate generally best-tolerated

### Insight Line Examples
- Optimal: `"400מ\"ג ביסגליצינט — הצורה הנספגת ביותר. 200מ\"ג מגנזיום אלמנטרי למנה"`
- Partial: `"500מ\"ג תחמוצת מגנזיום: אחוז ספיגה נמוך (~4%). בפועל: כ-20מ\"ג נספג למנה"`
- Insufficient: `"תערובת מגנזיום 300מ\"ג — יחס הצורות לא מפורט. אין אפשרות להעריך ספיגה"`

---

## Category 2 — Vitamin D

### Evidence Tier: 1
**Rationale:** Vitamin D deficiency is prevalent in Israel (high indoor lifestyle, certain populations). Supplementation effects on 25(OH)D serum levels are directly measurable. Bone health, immune function, and mood effects have strong RCT support for deficient populations. D3 vs. D2 superiority is established in comparative studies.

### Primary Use Cases
1. Deficiency correction (primary)
2. Bone health maintenance (Tier 1)
3. Immune support (Tier 1 for deficient individuals; Tier 2 for replete)
4. Mood / depression (Tier 2 — benefit in deficient, inconsistent in replete)

### Reference Dose Range
- **Maintenance (non-deficient):** 600–2,000 IU/day (15–50 mcg)
- **Deficiency correction:** 4,000–10,000 IU/day (100–250 mcg) — typically supervised
- **Upper Tolerable Intake:** 4,000 IU/day (NIH ODS); 100 mcg (EFSA)
- **Israeli Ministry of Health guidance:** 800–1,000 IU/day general population; 2,000 IU/day for deficiency risk

**BSIP-S reference window for maintenance products:** 800–2,000 IU/day.
Products above 4,000 IU/day: safety note triggered.
Products above 10,000 IU/day: safety override cap at 50.

### Form Hierarchy

| Form | FQ Score | Relative Efficacy | Notes |
|---|---|---|---|
| D3 (cholecalciferol) | Optimal (100) | Baseline | Raises 25(OH)D ~70% more effectively than D2 |
| Calcifediol (25-OH-D3, Hy-D) | Optimal (100) | Superior onset | Pre-converted; fast serum response; used in clinical deficiency |
| D3 + K2 (MK-7) combination | Optimal (100) | Synergistic | K2 directs calcium; prevents arterial calcification; supported combination |
| D2 (ergocalciferol) | Low (30) | ~30% less effective at raising serum levels | Shorter half-life; less appropriate for long-term maintenance |
| D3 in low-quality oil base | Acceptable (70) | Fat-soluble; depends on absorption vehicle | Fat-soluble vitamin requires dietary fat for absorption; quality of carrier matters |

### Common Distortions
1. **D2 in products marketed without form specification:** Most consumers assume vitamin D is D3. D2 is cheaper; some mass-market products use D2.
2. **Low-dose maintenance claims:** "Supports bone health" with 200 IU — below any clinical threshold.
3. **K2 omission in high-dose D3 products:** >2,000 IU/day D3 without K2 may increase calcium deposition in soft tissue. Not a mandatory add-on for lower doses but relevant for product completeness claim.
4. **IU vs. mcg confusion:** Label may list "25 mcg" which appears low but equals 1,000 IU. DA scoring must normalize to IU for comparison.

### Scoring Notes
- Verify D3 vs. D2. If unspecified, apply FQ = Unknown (20) and partial confidence.
- K2 co-formulation: note as a positive signal in expansion, but does not alter DA or FQ scoring for D.
- Products >4,000 IU: add safety note. Products >10,000 IU: apply safety override cap.

### Population Notes
- Veiled/covered women: deficiency risk significantly higher; upper reference range more relevant
- Dark skin: lower cutaneous synthesis → higher supplemental needs
- Elderly: reduced skin synthesis; often higher dose appropriate
- Exclusively breastfed infants: require supplementation (not in scope for BSIP-S v1, which scores adult products)

### Insight Line Examples
- Optimal: `"2,000 יחב\"ל ויטמין D3 + K2 (MK-7). D3 נספג 70% טוב יותר מ-D2. K2 מכוון את הסידן למקום הנכון"`
- Partial: `"ויטמין D ללא ציון סוג. ייתכן D2 (פחות יעיל) — לא ניתן לאמת"`
- Insufficient: `"200 יחב\"ל D — מתחת לסף הקליני. מינון נמוך מדי לתמיכה משמעותית"`

---

## Category 3 — Multivitamins

### Evidence Tier: 2
**Rationale:** No RCT demonstrates benefit of multivitamin supplementation in well-nourished general populations for longevity, disease prevention, or cognitive outcomes. However, multivitamins demonstrably correct specific deficiencies when present. The evidence for deficiency populations (elderly, dietary restrictions, pregnancy) is Tier 1. For the general "health insurance" framing: Tier 2. Category ceiling set at 2 (ceiling = 80).

### Primary Use Cases
1. Micronutrient gap coverage (primary BSIP-S use case)
2. Pregnancy support (specialized — prenatal vitamins require separate form considerations)
3. Elderly nutritional support
4. Restricted diet coverage (vegan, vegetarian)

### Reference Dose Range
For multivitamins, BSIP-S evaluates each primary ingredient individually against its category-specific reference dose. There is no single "multivitamin dose."

**Primary ingredients scored in a standard multivitamin:**

| Nutrient | Form Quality Key | Reference/RDA (Adult) | Common Distortion |
|---|---|---|---|
| Vitamin D | D3 > D2 | 800–2,000 IU | D2 in mass-market products |
| Vitamin B12 | Methylcobalamin > Cyanocobalamin | 2.4 mcg (RDA); 250–1,000 mcg common in supplements | Cyanocobalamin is cheaper; MTHFR individuals convert poorly |
| Folate (B9) | Methylfolate > Folic acid | 400 mcg DFE (RDA); 400–800 mcg typical | Folic acid standard; MTHFR converts poorly |
| Vitamin B6 | P-5-P > Pyridoxine HCl | 1.3–1.7 mg (RDA); avoid >100mg UL | High-dose B6 neurotoxicity risk |
| Zinc | Bisglycinate/picolinate > Oxide | 8–11 mg elemental (RDA) | Oxide form in cheapest products |
| Magnesium | Glycinate > Oxide | 200–350 mg elemental | Oxide in nearly all mass-market multivitamins |
| Vitamin A | Beta-carotene safer than preformed | 700–900 mcg RAE | Preformed high dose; teratogenic risk in pregnancy |
| Iron | Bisglycinate > Sulfate | 8–18 mg; men often don't need iron supplementation | Iron in men's multivitamins is often unnecessary; constipation risk |
| Iodine | Potassium iodide standard | 150 mcg | Rarely missing; usually adequate in any multivitamin |
| Selenium | Selenomethionine > Selenite | 55 mcg | |

### Form Quality for Multivitamins
FQ is calculated as a weighted average across primary ingredients. Products using methylated B vitamins (methylfolate, methylcobalamin, P-5-P) and chelated minerals (bisglycinate zinc, glycinate magnesium) receive FQ = Optimal. Products using synthetic vitamins and oxide minerals receive FQ = Low.

### Common Distortions
1. **"100% RDA" marketing with low-bioavailability forms:** A product providing 100% RDA as zinc oxide delivers ~10% of listed zinc. The 100% RDA claim is technically compliant but practically misleading.
2. **Megadosing on certain B vitamins:** Products with 5,000% DV for B12 signal poor formulation philosophy — therapeutic excess without clinical basis.
3. **Iron in men's formulas:** Many men's multivitamins include iron; most men do not benefit and may be harmed by iron accumulation. BSIP-S notes this as a formulation concern in LI.
4. **Decorative premium ingredients at trace doses:** "With CoQ10, Lutein, Resveratrol" at 1–5mg — far below any therapeutic range. Each decorative ingredient triggers LI deduction.
5. **Proprietary "Whole Food Matrix":** Implies a food-based product but is often a synthetic vitamin encapsulated with fruit powder at irrelevant amounts.

### Scoring Notes
- Multivitamin DA = weighted average across 5 primary micronutrients. Select the 5 highest-weight nutrients for the category (Vitamin D, B12, Folate, Zinc, Magnesium).
- Decorative ingredients: any ingredient at <10% of reference dose → 5-point LI deduction per ingredient, capped at -20 points total.
- Pregnancy-specific note: BSIP-S v1 does not specialize in prenatal scoring. Prenatal products are scored as standard multivitamins. Expansion panel notes to consult healthcare provider.

---

## Category 4 — Fish Oil (EPA/DHA)

### Evidence Tier: 1
**Rationale:** EPA and DHA are essential fatty acids with strong RCT evidence for triglyceride reduction (REDUCE-IT, STRENGTH trials). Cardiovascular event reduction is more contested post-2018 (STRENGTH showed no benefit; REDUCE-IT showed benefit with vascepa/icosapentaenoic acid only). BSIP-S scores against the non-contested primary outcome: triglyceride support and omega-3 adequacy. Evidence tier: 1.

### Primary Use Cases
1. Omega-3 adequacy (primary — EPA+DHA intake)
2. Triglyceride support (Tier 1 at 2–4g/day EPA+DHA)
3. Cardiovascular support (Tier 1 for triglycerides; Tier 2 for event prevention)
4. Anti-inflammatory support (Tier 2 — effect in clinical inflammatory conditions; Tier 3 for general wellness)
5. Cognitive support (Tier 2 — DHA particularly for neurodevelopment; adult cognition inconsistent)

### Reference Dose Range
- **General omega-3 adequacy (AHA):** 500mg EPA+DHA/day combined
- **Triglyceride lowering (AHA/FDA):** 2,000–4,000 mg EPA+DHA/day
- **Cardiovascular support:** 1,000 mg EPA+DHA/day (lower end)
- **Upper practical limit (FDA GRAS):** 3,000 mg EPA+DHA/day from supplements

**BSIP-S scores against the active molecule dose: mg EPA+DHA combined, not total fish oil.**

**Reference scoring window:** 500–3,000 mg EPA+DHA/day.

### Form Hierarchy

| Form | FQ Score | Bioavailability | Notes |
|---|---|---|---|
| re-Esterified Triglyceride (rTG) | Optimal (100) | ~50% better than EE | Best absorbed; premium products; requires processing to convert from EE |
| Natural Triglyceride (TG) form | Optimal (100) | Excellent; gold standard historically | Wild fish oil in TG form; absorbed ~70% better than EE with fat |
| Phospholipid (krill oil) | Optimal (100) | Very high; also delivers choline | EPA+DHA in krill is lower per dose but absorption compensates partially |
| Free Fatty Acid (FFA) | Optimal (100) | Fastest absorption; rare commercially | |
| Ethyl Ester (EE) | Acceptable (70) | Standard commercial form | Requires dietary fat for absorption; ~70% of TG absorption with fat |
| Concentrated EE | Acceptable (70) | Same as EE; higher EPA/DHA per capsule | Most prescription fish oils (Lovaza) are EE |

### The EPA/DHA Concentration Calculation
**Critical:** Consumers must compare mg EPA+DHA per serving, not mg total fish oil.

Standard 1,000mg fish oil softgel: typically 300mg EPA+DHA (30% concentration).
High-concentration product: 700–800mg EPA+DHA per 1,000mg capsule (70–80% concentration).

**"1,000mg Omega-3" does not equal "1,000mg EPA+DHA."** BSIP-S surfaces this calculation explicitly in every fish oil expansion panel.

### Oxidation
Rancid fish oil is a real quality concern. Peroxide value (POV) >5 mEq/kg indicates significant oxidation. This is not observable from the label. BSIP-S:
- Rewards IFOS certification (which measures POV) with maximum TR score
- Flags uncertified products in expansion as: "אין אימות עצמאי לרמת חמצון — ייתכן שמן מחומצן"
- Does not deduct points for oxidation alone (unobservable without testing)

### Common Distortions
1. **"1,000mg Fish Oil" headline:** Obscures that actual EPA+DHA may be 180/120 or 300 total. Most common distortion in this category.
2. **Ratio manipulation:** Very high DHA, very low EPA, or vice versa. Some products optimize for cost, not evidence-based ratio.
3. **Capsule count inflation:** "Take 3 capsules daily" with only 300mg EPA+DHA per capsule = 900mg total — close to threshold but requiring 3 capsules.
4. **Krill vs fish oil equivalence claim:** Some krill products claim equivalence at lower EPA+DHA doses due to absorption. Plausible mechanism but insufficient head-to-head RCT confirmation.

### Scoring Notes
- DA is calculated on EPA+DHA combined in mg, not total omega-3, not total fish oil.
- If EPA+DHA individual amounts are not listed but total omega-3 is: apply partial DA confidence (not all omega-3 is EPA+DHA; ALA does not convert meaningfully).
- IFOS certification → TR = 100.
- No certification → TR maximum 75.
- Serving size check: if "recommended dose" is 3+ capsules, evaluate DA at full recommended dose.

---

## Category 5 — Creatine

### Evidence Tier: 1
**Rationale:** Creatine monohydrate is one of the most extensively researched sports supplements in history. 500+ independent studies. ISSN Position Stand (2017, updated 2021) confirms efficacy and safety for athletic performance, strength, and potentially cognitive function. Dose and form are well-established. Evidence tier: 1 (highest confidence in any supplement category).

### Primary Use Cases
1. Athletic performance / strength (Tier 1)
2. Muscle mass support (Tier 1 combined with resistance training)
3. Recovery (Tier 1)
4. Cognitive support (Tier 2 — growing evidence, not yet primary use case)

### Reference Dose Range
- **Maintenance:** 3–5g creatine monohydrate/day
- **Loading protocol:** 20g/day for 5–7 days, then 3–5g/day maintenance
- **Saturation target:** 3g/day achieves full saturation in ~28 days without loading
- **Upper practical dose:** 5g/day maintenance; loading at 20g/day is safe and accelerates saturation

**BSIP-S reference scoring window:** 3–5g/day creatine monohydrate (or equivalent form).

### Form Hierarchy

| Form | FQ Score | Evidence | Notes |
|---|---|---|---|
| Creatine Monohydrate | Optimal (100) | 99%+ of all RCTs | The only form with definitive evidence. Micronized = same molecule, finer particle |
| Creatine HCl | Acceptable (70) | Limited head-to-head | Claimed to require lower dose; no RCT confirmation of superior outcomes |
| Buffered Creatine (Kre-Alkalyn) | Acceptable (70) | One head-to-head showing no superiority over monohydrate | Typically sold at premium without evidence advantage |
| Creatine Malate | Acceptable (70) | Limited data | Mechanically plausible; insufficient head-to-head |
| Creatine Ethyl Ester | Low (30) | RCT showing CEE inferior to monohydrate | Converts to creatinine; absorbed poorly; actively worse than monohydrate |
| "Advanced" proprietary forms | Unknown (20) | No comparative data | Avoid until evidence emerges |

### Common Distortions
1. **Premium form marketing at premium price:** HCl, Kre-Alkalyn, and similar forms are sold at 2–4× the price of monohydrate with no demonstrated efficacy advantage. The premium formulation is the distortion.
2. **Low dose for "advanced" forms:** "500mg Creatine HCl equivalent to 3g monohydrate" — claim not supported by RCT.
3. **Blended products diluting dose:** Pre-workouts or protein powders "with creatine" often provide 1–2g creatine — below effective maintenance dose.
4. **Loading protocol requirement disguised:** Some products list a "serving" that is a maintenance dose but don't disclose that saturation takes 4 weeks at that dose.

### Scoring Notes
- Creatine monohydrate at 3–5g/day: DA = Adequate (100). This is the simplest scoring case in BSIP-S.
- Creatine in a blend: calculate creatine dose as fraction of blend if proprietary, apply blend penalty.
- Vegetarian/vegan note: creatine synthesis from dietary precursors is lower; supplementation benefit is more pronounced. Note in expansion where relevant.

### Insight Line Examples
- Optimal: `"5 גרם קריאטין מונוהידרט למנה — הצורה עם 99% מהמחקרים. מינון מדויק בטווח הקליני"`
- Acceptable: `"קריאטין HCl — מינון נמוך יותר נדרש לכאורה. אין ראיות לתוצאות טובות יותר ממונוהידרט"`
- Distortion: `"2 גרם קריאטין בתוך פורמולה — מתחת למינון האפקטיבי (3–5 גרם/יום)"`

---

## Category 6 — Protein Powder

### Evidence Tier: 1
**Rationale:** Protein adequacy has robust evidence across athletic performance, muscle protein synthesis, and satiety. Protein powder is evaluated as a protein delivery vehicle, not as an enhancement. DIAAS (Digestible Indispensable Amino Acid Score) is the gold standard for protein quality. Evidence tier: 1 for protein adequacy; the category does not claim therapeutic outcomes beyond protein delivery.

### Primary Use Cases
1. Protein intake augmentation (primary — filling daily protein gap)
2. Muscle protein synthesis support (Tier 1 with resistance training)
3. Satiety support (Tier 2 — protein effect on satiety is real but less relevant to powder specifically)

### Reference Dose Range
- **Per-serving protein:** 20–40g complete protein per serving (goal: hit daily target)
- **Daily protein target (athletic):** 1.6–2.2g protein/kg body weight (ISSN position)
- **Daily protein target (general maintenance):** 0.8–1.2g/kg

BSIP-S does not score to a single reference dose — protein powder is a dietary supplement to augment total daily protein. DA evaluation focuses on:
1. Protein per serving (actual g, not "protein blend" g)
2. Protein quality (DIAAS-assessed source)
3. Amino acid spiking absence (label integrity)

### Protein Quality Assessment (replaces traditional DA for this category)

**DIAAS reference values (approximate):**

| Source | DIAAS | Quality Tier |
|---|---|---|
| Whey isolate | ~1.08–1.15 | Optimal |
| Whey concentrate | ~0.97–1.10 | Optimal |
| Casein (micellar) | ~1.05 | Optimal |
| Egg white | ~1.10 | Optimal |
| Milk protein | ~1.05 | Optimal |
| Soy isolate | ~0.91–1.0 | Acceptable |
| Pea isolate | ~0.82 | Acceptable |
| Rice protein | ~0.59 | Low (alone) |
| Rice + Pea 50/50 blend | ~0.87–0.95 | Acceptable |
| Collagen / gelatin | ~0.0 (not a complete protein) | Low |
| Hemp | ~0.63 | Low (alone) |

**DIAAS cannot be calculated from the label alone.** BSIP-S uses source type as a proxy for form quality.

### Amino Acid Spiking Flag

Amino spiking is the practice of adding free-form amino acids (glycine, taurine, creatine, glutamine) to inflate the total nitrogen reading on protein tests, overstating protein content per serving.

**Indicators of amino spiking:**
- Glycine or taurine listed in top 5 ingredients
- Large discrepancy between label protein (g/serving) and independently tested protein
- "Amino acid blend" listed as a significant ingredient in a protein powder
- ConsumerLab or similar tests showing protein content 10%+ below labeled amount

BSIP-S flags amino spiking as a major LI deduction (-30 to -40 points on LI dimension).

### Common Distortions
1. **Amino spiking:** As above — the most serious integrity failure in this category.
2. **"32g protein blend" serving with 25g actual protein:** Total blend weight includes non-protein ingredients; actual protein content is lower.
3. **Collagen marketed as protein:** Collagen scores 0 on DIAAS (lacks tryptophan); it is not a complete protein and should not be compared to whey or casein for muscle protein synthesis.
4. **Heavy metals in plant proteins:** Consumer Reports studies found cadmium, lead, arsenic, and mercury in measurable amounts in many plant-based protein powders. NSF certification specifically mitigates this.
5. **Serving size manipulation:** Large scoop sizes (50g) make protein per serving look high; compare protein density (g protein / g total serving weight).

### Scoring Notes
- DA adapted: score protein per serving against 20–40g target range. <15g: DA = partial. <10g: DA = insufficient.
- FQ = protein source quality tier (see DIAAS table above).
- Collagen as primary source: FQ = Low regardless of marketing language.
- Heavy metal risk: if no third-party certification for a plant-based protein powder, flag in expansion.

---

## Category 7 — Probiotics

### Evidence Tier: 2
**Rationale:** Probiotic evidence is highly strain- and condition-specific. L. rhamnosus GG for antibiotic-associated diarrhea: Tier 1. S. boulardii for C. difficile prevention: Tier 1. General "gut health" or "immune support" claims: Tier 2–3. Because no single strain/condition pairing defines the category and most products make general wellness claims, the category ceiling is set at Tier 2 (80). Exception handling for Tier 1 evidence-matched products is documented below.

### Primary Use Cases
1. Gut microbiome support (general — Tier 2)
2. Antibiotic-associated diarrhea prevention (AAD — Tier 1 for specific strains)
3. Traveler's diarrhea prevention (Tier 1 for S. boulardii)
4. IBS symptom relief (Tier 1 for specific strains, particularly L. plantarum 299v)
5. Immune support (Tier 2 — plausible mechanism; inconsistent across strains)

### Reference Dose Range
- **General:** 1 billion – 50 billion CFU/day (range in studies)
- **AAD prevention:** 5 billion – 40 billion CFU/day of proven strains (L. rhamnosus GG studies)
- **Key insight:** CFU count without strain identity is meaningless. Strain > count.

**BSIP-S cannot score dose adequacy for probiotics without strain identification.**

If strain is not specified → DA = insufficient (20 points maximum). CFU count without strain identity is decorative information.

### Strain Evidence Tiers (selected)

| Strain | Code | Evidence | Primary Use |
|---|---|---|---|
| Lactobacillus rhamnosus GG | ATCC 53103 | Tier 1 | AAD prevention; GI recovery |
| Saccharomyces boulardii | CNCM I-745 | Tier 1 | Traveler's diarrhea; C. diff |
| Lactobacillus plantarum | 299v | Tier 1 | IBS bloating |
| Bifidobacterium longum | BB536 | Tier 1/2 | Allergy; immune |
| Lactobacillus acidophilus | NCFM | Tier 1/2 | General GI; IBS |
| Bifidobacterium infantis | 35624 | Tier 1 | IBS (Align product strain) |
| Lactobacillus reuteri | DSM 17938 | Tier 1/2 | Infant colic; adult gut |
| Generic "L. acidophilus" (no code) | — | Tier 2 | No research-specific strain |
| Generic "Probiotic Blend" | — | Not assessable | — |

### Survivability Scoring

| Survivability Feature | Impact |
|---|---|
| Enteric-coated capsule (pharmaceutical grade) | +10 points to FQ (survivability bonus) |
| Delayed-release capsule | +10 points to FQ |
| Refrigerated + shelf-stable certification | +5 points to FQ |
| CFU guaranteed at expiry (not just manufacture) | +10 points to TR |
| No survivability claim or feature | No bonus |

### Common Distortions
1. **High CFU generic strains:** "100 Billion CFU" with unspecified or generic strains. CFU is irrelevant without strain identity.
2. **"Probiotic blend" without strain codes:** Strain name without research code (e.g., "Lactobacillus acidophilus" without NCFM) cannot be matched to evidence.
3. **Manufacture-date CFU guarantee:** 50 billion CFU at manufacture may be 2 billion at purchase if stored improperly. Expiry-date guarantee is the honest measure.
4. **Dead probiotics:** Products without enteric coating, stored in warm conditions, past optimal shelf life — viable CFU may approach zero.
5. **Refrigeration requirements ignored at retail:** Some probiotic brands require refrigeration but are displayed at room temperature on retail shelves.

### Scoring Notes
- If strain is named with research code → can score DA against strain-specific reference dose.
- If strain is named without code → treat as partially assessable; apply Tier 2 evidence with conservative DA.
- CFU guarantee at expiry > CFU at manufacture: +10 TR.
- No strain code on any ingredient → DA = 20 (insufficient), confidence = insufficient.

---

## Category 8 — Sleep Supplements

### Evidence Tier: 2
**Rationale:** Sleep supplement is a category defined by intended use, not by a single active ingredient. Products range from melatonin-only (Tier 1 evidence) to complex blends with valerian, GABA, L-theanine, 5-HTP, magnesium, and adaptogenic herbs at varying evidence quality. The category average is Tier 2. Exception: melatonin-only products qualify for Tier 1 scoring.

### Primary Use Cases
1. Sleep onset support (primary — melatonin Tier 1)
2. Sleep quality improvement (magnesium Tier 1; L-theanine Tier 2)
3. Stress/anxiety reduction supporting sleep (ashwagandha Tier 2; L-theanine Tier 2)
4. REM support (5-HTP Tier 2 — serotonin precursor; timing-sensitive)

### Ingredient Evidence Reference

| Ingredient | Evidence Tier | Reference Dose | Notes |
|---|---|---|---|
| Melatonin | Tier 1 | 0.5–3 mg for sleep onset; 5 mg for jet lag | Higher doses not more effective; can impair sleep architecture |
| Magnesium (glycinate/malate) | Tier 1 | 200–350 mg elemental | Sleep quality RCTs; use glycinate for sleep |
| L-Theanine | Tier 2 | 100–400 mg | Relaxation without sedation; GABA-A modulation |
| 5-HTP | Tier 2 | 100–300 mg (evening) | Serotonin precursor; timing-critical; SSRIs contraindicated |
| Ashwagandha (KSM-66 extract) | Tier 2 | 300–600 mg | Cortisol reduction; sleep onset benefit in stressed adults |
| Valerian root extract | Tier 2/3 | 300–600 mg | Inconsistent RCTs; one systematic review showing modest benefit |
| GABA | Tier 2/3 | 100–300 mg | Blood-brain barrier crossing disputed; peripheral vs. CNS effect |
| Passionflower | Tier 2/3 | 250–500 mg | Small studies; anxiety-related sleep benefit |
| Lemon Balm | Tier 3 | 300–600 mg | Limited data; GABA-T inhibition claimed |
| Lavender (oral) | Tier 2 | 80 mg (Silexan) | Specific preparation with anxiolytic evidence; standardized extract only |
| CBD | Tier 2 | 25–75 mg | Growing evidence for anxiety/sleep; regulatory complexity in Israel |

### Melatonin Dosing — Critical Note

The common market assumption is "more melatonin = better sleep." This is demonstrably incorrect:
- 0.5mg melatonin has been shown equally or more effective than 5mg for sleep onset in multiple studies
- High-dose melatonin (5–10mg) may disrupt circadian rhythm with chronic use
- Pharmacological dose (10mg) is primarily used in clinical research or specific conditions

**BSIP-S DA scoring for melatonin:**
- 0.5–3 mg: DA = Adequate (100)
- 3–5 mg: DA = Near-adequate (80) — borderline clinically useful
- 5–10 mg: DA = Partial (55) — above evidence range for routine use
- >10 mg: Safety note triggered ("מעל המינון הנחקר לשימוש יומיומי")

**Products with melatonin >10 mg:** Apply safety override note. Cap at 70 regardless of other scores.

### Common Distortions
1. **Melatonin overdosing for marketing:** 10mg melatonin products appear "stronger." They are not more effective and may disrupt natural melatonin production.
2. **Underdosed blend with strong label claims:** "Advanced sleep formula" with 10 ingredients each at <15% of reference dose. Every ingredient is decorative; LI score collapses.
3. **GABA claims without BBB acknowledgment:** Products claiming GABA "crosses the blood-brain barrier" without evidence — this is a contested claim. BSIP-S flags it.
4. **5-HTP without SSRIs/MAOIs warning:** 5-HTP can precipitate serotonin syndrome in combination with serotonergic drugs. A mandatory disclosure trigger in BSIP-S.
5. **"Proprietary Sleep Complex":** Melatonin dose often hidden in blend — critical because melatonin dosing matters more than almost any other ingredient in this category.

### Multi-Ingredient Scoring Logic
Score each ingredient individually against its reference dose and evidence tier. Apply the multi-ingredient composite formula from Scoring Architecture Section 10. The category ceiling applies to the composite.

**Exception:** If the product contains exclusively melatonin (no other active ingredients), apply Tier 1 ceiling (100). All blended sleep supplements: Tier 2 ceiling (80).

### Safety Notes for Sleep Supplements

| Scenario | Action |
|---|---|
| 5-HTP present | Mandatory disclosure: "5-HTP — לא לשימוש עם SSRI, MAO inhibitors" |
| Melatonin >5 mg | Note: "מינון גבוה מהנחקר לשינוי יומיומי. לא הוכח כיעיל יותר מ-1–3 מ\"ג" |
| Valerian + alcohol warning | Optional note (relevant for driving / machinery) |
| Passionflower at high dose | Note extended effect on CNS depressants |
| St. John's Wort (if present) | Mandatory: "עשב היפריקום מעכב אנזימי CYP3A4 — מקיים אינטראקציות תרופתיות רחבות" |

---

## Appendix A — Category Score Ceiling Summary

| Category | Evidence Tier | Score Ceiling | Notes |
|---|---|---|---|
| Creatine | 1 | 100 | Highest-confidence supplement category |
| Vitamin D | 1 | 100 | |
| Magnesium | 1 | 100 | |
| Fish Oil | 1 | 100 | |
| Protein Powder | 1 | 100 | Scored as protein adequacy, not enhancement |
| Probiotics | 2 | 80 | Exception: Tier 1 strain × condition match → noted in expansion |
| Multivitamins | 2 | 80 | |
| Sleep Supplements | 2 | 80 | Exception: melatonin-only → Tier 1 ceiling |

---

## Appendix B — Cross-Category Distortion Registry

**D-S-001: Compound vs. elemental confusion (Minerals)**
Products list compound dose; elemental is the relevant amount for DA scoring. Most prevalent in magnesium and zinc. BSIP-S always surfaces elemental calculation.

**D-S-002: CFU count without strain identity (Probiotics)**
CFU count is a meaningless number without strain identity. A product with 100 Billion CFU of an unresearched strain is inferior to 5 Billion CFU of L. rhamnosus GG for AAD prevention.

**D-S-003: Proprietary blends obscuring active dose**
Affects all categories. Proprietary blend = mandatory transparency penalty. No exception.

**D-S-004: High CFU/dose headline with inadequate active concentration**
"1,000mg fish oil" (300mg EPA+DHA), "100 Billion CFU" (generic strains), "500mg Magnesium" (oxide, 20mg absorbed). The headline number is always the compound/total; the relevant number is the active moiety.

**D-S-005: Premium form marketing for unproven superiority (Creatine)**
HCl, Kre-Alkalyn, and similar forms are sold at premium price without head-to-head superiority evidence over monohydrate. BSIP-S applies FQ = Acceptable (70) to all non-monohydrate forms.

**D-S-006: Decorative ingredients at trace doses (Multivitamins, Sleep Blends)**
Ingredients at <10% of reference dose inflate the ingredient list without contributing bioactive benefit. BSIP-S flags each decorative ingredient and deducts from LI.

**D-S-007: Melatonin dose inflation (Sleep)**
10mg > 5mg > 3mg in consumer perception. 0.5–1mg is equally effective for most adults. High-dose melatonin products receive reduced DA scores and a mandatory note.

**D-S-008: Collagen marketed as protein (Protein Powder)**
Collagen lacks tryptophan; DIAAS ≈ 0; not a complete protein. Products comparing collagen to whey for muscle protein synthesis receive LI = 40 for misleading comparison.

**D-S-009: GMP certification conflated with content verification**
GMP certifies manufacturing process, not label accuracy. Not a substitute for third-party content verification. BSIP-S does not award TR points for GMP alone.

**D-S-010: Manufacture-date CFU guarantee (Probiotics)**
50 billion CFU at manufacture may be far fewer at expiry. Only expiry-date CFU guarantees receive full TR credit.

---

## Appendix C — Israeli Market Context

**Supplement regulation in Israel:**
Supplements are regulated under the Food Law (1994) and Ministry of Health regulations. Health claims require Ministry approval. Structure/function claims are partially permitted. The market is less strictly regulated than pharmaceuticals, creating significant room for the distortions catalogued above.

**Key Israeli supplement market observations:**
- Local brands (Super-Pharm, Lavie, Solgar Israel) often import formulations with limited Israeli Ministry of Health oversight of label accuracy
- Import products may use US or EU-standard labeling (IU, mg) without Israeli Ministry Hebrew translation; BSIP-S should normalize all units
- Shufersal, Rami Levy, and Super-Pharm are primary distribution channels; product pages are the primary data source
- Israeli supplement market is growing significantly (2020–2025); consumer sophistication is increasing; Bari has an opportunity to fill the information vacuum

**Hebrew terminology standard for BSIP-S outputs:**
- Dose: מינון
- Form: צורה
- Bioavailability: ספיגה / זמינות ביולוגית
- Elemental: אלמנטרי
- Proprietary blend: תמהיל קנייני
- Evidence: ראיות מחקריות
- Third-party certified: מאומת על ידי גוף עצמאי
- Reference dose: מינון קליני מומלץ
- Upper tolerable intake: מגבלת הצריכה הבטוחה
