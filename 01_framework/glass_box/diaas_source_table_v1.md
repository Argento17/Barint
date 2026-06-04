---
document: diaas_source_table_v1
task: TASK-179P
phase: Research (Phase 1 of 3)
status: PENDING_NUTRITION_REVIEW
created_at: 2026-06-04
---

# DIAAS Protein Source Table v1

**Purpose:** Evidence base for the Glass Box W1.5 DIAAS protein-quality signal (TASK-179P). Covers ~8 protein sources present on Israeli food shelves across the hummus, maadanim, yogurt, and snack-bar corpora. Nutrition Agent uses this table to define the D2 credit rule and the disclosure-gated D5/D6 flag rule (Phase 2). No scores are assigned in this document.

**Reference standard:** FAO/WHO (2013) *Dietary Protein Quality Evaluation in Human Nutrition*. FAO Food and Nutrition Paper 92. Rome: FAO. This is the canonical definition of DIAAS. The scoring pattern used throughout is the **older-child/adult reference pattern (≥3 years)** unless otherwise noted, consistent with general-population Israeli food labeling context. When infant values differ materially, they are noted separately.

**Completeness threshold (FAO/WHO 2013):**
- DIAAS ≥ 75: high-quality / complete (the protein meets or approaches the reference amino acid requirement for all indispensable amino acids)
- DIAAS ≥ 100: excellent quality
- DIAAS < 75: does not meet the threshold for a quality claim; labeled "incomplete" in this table

**Evidence tier definitions** used in the notes follow the Bari standard: Strong / Moderate / Weak / Insufficient / Contested.

---

## 1. DIAAS Summary Table

| # | Protein source | Hebrew name | DIAAS range (older child/adult) | Limiting amino acid | Completeness tier | Evidence quality |
|---|---|---|---|---|---|---|
| 1 | Whey protein isolate (WPI) | חלבון מי גבינה מבודד | **106–114** | None (all IAA ≥ reference) | **Complete — Excellent** | Strong |
| 2 | Casein / milk protein concentrate | קזאין / חלבוני חלב | **100–117** | None | **Complete — Excellent** | Strong |
| 3 | Whole egg (cooked) | ביצה שלמה (מבושלת) | **108–113** | None | **Complete — Excellent** | Strong |
| 4 | Egg white (cooked) | חלבון ביצה | **108–115** | None (lysine is abundant; leucine slightly lower but above reference) | **Complete — Excellent** | Moderate–Strong |
| 5 | Soy protein isolate (SPI) | חלבון סויה מבודד | **78–98** | Methionine+cysteine (SAA) | **Complete — High quality** | Strong |
| 6 | Pea protein isolate/concentrate (PPC) | חלבון אפונה מבודד | **52–67** | Methionine+cysteine (SAA) | **Incomplete** | Strong |
| 7 | Rice protein concentrate/isolate | חלבון אורז | **37–58** | Lysine | **Incomplete** | Moderate |
| 8 | Oat protein concentrate | חלבון שיבולת שועל | **56–67** | Lysine (for ≥3yr); aromatic AA (for infants, DIAAS ~41) | **Incomplete** | Moderate |

**Table notes:**
- All values are for the older child/adult scoring pattern (≥3 years) per FAO/WHO 2013, except where infant values noted. Values represent the range from multiple published studies; single-study point estimates within the range are noted in Section 2.
- "Limiting amino acid" is the IAA with the lowest ratio to the reference pattern — the bottleneck that prevents the source from meeting ≥75 on its own.
- Completeness tier is a binary: ≥75 = complete, <75 = incomplete. This is the threshold the D2 credit rule uses.
- Pea and rice are frequently combined in commercial "protein blends" because their limiting amino acids are complementary (pea: low methionine/cysteine; rice: low lysine). A blend can achieve DIAAS ≥75. However, the blend DIAAS depends on proportions that Israeli labels almost never disclose — this is the canonical D5 disclosure gap flagged in the six_dimension_contract_v1 §D5/G3.

---

## 2. Per-Source Evidence Notes

### 2.1 Whey Protein Isolate (WPI)
**DIAAS:** 106–114 (older child/adult); values range from ~100 at the low end to 114 in pig ileal cannulation studies.

**Evidence:**
- Brouns et al. (2022) / Mathai et al. (2017, BJN): WPI consistently shows DIAAS > 100; leucine content is exceptionally high, supporting the "excellent" classification. The 2017 BJN paper (PMID 28382889) directly measured SID of all IAAs in pigs and confirmed WPI and WPC well above the completeness threshold.
- Bandegan et al. (2017), Nosworthy et al. (2023, JSFA, PMID 37357639): Whey protein isolate DIAAS ≥ 100 held across multiple thermal processing conditions; heat-treated whey maintained DIAAS ≥ 100.
- FAO/WHO (2013) illustrative calculations: WPI cited as an example of an excellent-quality reference protein.

**Evidence tier: Strong.** Multiple independent pig-model and human studies; consistent results; FAO/WHO 2013 confirms.

**Practical note:** WPI and WPC both qualify as "complete." WPC has marginally lower DIAAS than WPI (~100–106) due to lower SID values, but both cross the ≥75 threshold. Israeli label terms: "חלבון מי גבינה מבודד" (WPI), "חלבוני מי גבינה" (whey proteins, general — includes WPC). Both qualify for D2 credit under Rule A if declared.

---

### 2.2 Casein / Milk Protein Concentrate (MPC)
**DIAAS:** ~100–117 (older child/adult). Skim milk powder (SMP), which is predominantly casein + whey, scores 100–117 depending on the study.

**Evidence:**
- PMID 28382889 (Brouns/BJN 2017): SID values for milk protein concentrate are high; all IAA well above reference. Casein's slower digestion relative to whey does not affect DIAAS (DIAAS measures availability, not rate).
- FAO/WHO (2013): Milk protein used as the benchmark "excellent quality" reference example.
- PMID 40075933 (2025, Animals): Skim milk powder DIAAS confirmed high in pig model.
- Comprehensive overview (PMID 33133540, 2020, Food Sci Nutr): "Casein and egg proteins are classified as excellent quality with DIAAS above 100."

**Evidence tier: Strong.** Consistent across multiple in vivo pig studies; benchmark protein in the FAO 2013 framework.

**Practical note:** Casein appears on Israeli maadanim labels as "קזאין," "חלבוני חלב," or "חלבוני גבינה." It is structurally complete. Yogurt and dairy dessert products containing declared dairy protein (not "protein blend") qualify for D2 credit.

---

### 2.3 Whole Egg (cooked)
**DIAAS:** ~108–113 (older child/adult); consistently "excellent" across forms (fried, boiled, scrambled).

**Evidence:**
- PMID 39703894 (2024, J Nutritional Science): Ileal cannulation study in pigs showing all cooked-egg forms had DIAAS > 100. "Eggs have 'excellent' protein quality for individuals older than 6 months."
- PMID 33133540 (2020): "Egg proteins are classified as excellent quality proteins with an average DIAAS above 100."
- FAO/WHO (2013): Egg used as a reference protein in the original DIAAS framework examples.

**Evidence tier: Strong.** Multiple in vivo pig ileal studies; consistent; FAO endorsed.

**Practical note:** Whole egg appears in snack bars and maadanim as "ביצה שלמה," "ביצים." Always complete. The 2024 pig-model paper also confirmed that adding egg to lower-DIAAS plant-protein meals raises the meal DIAAS above 75 (additive principle).

---

### 2.4 Egg White (cooked)
**DIAAS:** ~108–115 (older child/adult). Slightly less leucine than whole egg, but all IAA above the reference threshold.

**Evidence:**
- PMID 39703894 (2024): Egg white and whole egg had indistinguishable DIAAS in the pig model.
- PMID 33133540 (2020, comprehensive overview): Egg proteins (including egg white) consistently above DIAAS 100.
- PMID 34203642 (2021, Nutrients): "Based on DIAAS, egg white protein (EGG) has an excellent score, comparable to that of whey protein but with a lower amount of leucine."

**Evidence tier: Moderate–Strong.** Fewer standalone egg-white DIAAS studies than whole egg; values are consistent and robust but the specific egg-white vs. whole-egg distinction has limited direct studies. The DIAAS is effectively equivalent to whole egg in all published reports.

**Gap note:** Some Israeli products use "חלבון ביצה" (egg white), which is chemically egg albumen. No uncertainty about completeness; the gap is merely the smaller study count specifically for egg white as opposed to whole egg.

---

### 2.5 Soy Protein Isolate (SPI)
**DIAAS:** ~78–98 (older child/adult). Range reflects processing differences and study variation.

**Evidence:**
- PMID 28382889 (2017, BJN): SID of all IAA in SPI > SPI flour; DIAAS for SPI ≥ 75, classifying as "high quality." Methionine+cysteine (SAA) is the limiting amino acid but still above 75 in most studies.
- PMID 40075933 (2025, Animals): Confirmed SPI DIAAS in the high-quality range using pig model.
- PMID 37357639 (2023, JSFA): "non-heated rapeseed protein isolate had a reduced DIAAS... compared with soy protein isolate" — indirect confirmation that SPI is higher.
- PMID 33133540 (2020): "Whey and soy proteins are classified as high-quality protein with an average DIAAS ≥75."

**Evidence tier: Strong.** Multiple pig-model in vivo studies from different labs; consistent finding that SPI crosses the ≥75 threshold.

**Caveat:** There is meaningful range (78–98) across studies reflecting different processing conditions, SID measurement methods (pig vs. rat vs. in vitro), and reference patterns. The ≥75 classification is robust. However, the lower end of the range (78) is close to the threshold, and some in vitro estimates have landed below 75. Nutrition should note this in the D2 credit rule.

**Israeli label:** "חלבון סויה מבודד" or "חלבון סויה." Soy appears in hummus and snack bars. As an isolate, it crosses the ≥75 threshold and qualifies for D2 credit.

---

### 2.6 Pea Protein Isolate/Concentrate (PPC)
**DIAAS:** ~52–67 (older child/adult). Consistently below 75.

**Evidence:**
- PMID 28382889 (2017, BJN): Pea protein concentrate DIAAS below soy and dairy; methionine+cysteine limiting. PDCAAS-like values overestimated quality vs DIAAS.
- PMID 40075933 (2025): PPC confirmed below 75 in pig model.
- PMID 37357639 (2023, JSFA): "rice and pea protein concentrates had DIAAS < 75."
- PMID 33133540 (2020): Pea classified in "no quality claim category (DIAAS <75)."

**Evidence tier: Strong.** Consistent across multiple independent pig-model studies; pea's incomplete status is a well-established finding.

**Practical note:** Pea protein is widely used in Israeli snack bars and vegan products. When declared alone (e.g., "חלבון אפונה"), it does not qualify for D2 credit (incomplete). When combined with rice in a "protein blend" without proportions, the blend's DIAAS is unknown (feeds G3/D5 gap). The SAA-limitation of pea (met+cys) is complemented by rice (high SAA, low lysine) — a paired blend can achieve completeness if formulated at the right ratio, but that ratio is never disclosed on Israeli labels.

---

### 2.7 Rice Protein Concentrate/Isolate
**DIAAS:** ~37–58 (older child/adult). Consistently below 75; highly variable depending on brown vs. white rice and processing.

**Evidence:**
- PMID 40075933 (2025, Animals): White rice DIAAS measured at lower range in pig model; lysine limiting.
- PMID 37357639 (2023, JSFA): Brown rice protein concentrate DIAAS < 75; below pea and soy.
- PMID 33133540 (2020): "Rice proteins are classified in the no quality claim category (DIAAS < 75)."
- PMID 29200310 (2018, JSF Review): Notes that non-meat plant proteins have more variable amino acid composition; rice is at the lower end.

**Evidence tier: Moderate.** Consistent direction (below 75), but range is wide (37–58) and varies by rice type (brown vs. white), processing (concentrate vs. isolate), and method (pig in vivo vs. in vitro). The available studies are pig-model based, which is the FAO-endorsed method.

**Gap note:** The variability in DIAAS for rice protein (37 vs 58) is meaningful. Studies differ by source (brown vs. white), degree of isolation, and thermal history. Nutrition should set a single conservative value (e.g., ≤58) for the D2 rule rather than a midpoint.

**Israeli label:** "חלבון אורז," "חלבוני אורז." Does not qualify for D2 credit alone. Often paired with pea in "protein blends" on snack bars.

---

### 2.8 Oat Protein Concentrate
**DIAAS:** ~56–67 (older child/adult, lysine limiting); ~41 for infants (aromatic AA limiting).

**Evidence:**
- PMID 28573795 (2018, JSFA): "For children (6 months to 3 years) and children older than 3 years, the most limiting AA in oat protein concentrate was Lys, for which the DIAAS was 56 and 67... To satisfy the daily human AA requirement, oat protein needs to be complemented by other proteins of higher quality."
- PMID 33133540 (2020): "Oat proteins are classified in the no quality claim category (DIAAS <75)."
- PMID 36986077 (2023, Nutrients): Oat compared with canary seed using in vitro digestion; DIAAS confirms oat below 75.

**Evidence tier: Moderate.** The 2018 paper is the primary direct measurement using pig in vivo model; the direction is consistent. Fewer studies than for dairy/egg/soy. Note that oat protein in commercial snack-bar products is typically a minor fraction relative to oat flakes; the DIAAS entry here refers to a concentrated/isolated oat protein source.

**Practical note:** "Oat protein" as a declared isolated ingredient in snack bars does not qualify for D2 credit (incomplete, DIAAS ~56–67). Oat flakes as a whole food are a different matrix (the protein is embedded in the whole-grain matrix; DIAAS for oat flakes as a food is in the same range but the fiber/matrix context differs from isolated oat protein).

---

## 3. Evidence Notes — Cross-Source Issues

### 3.1 Study method variability
DIAAS values are measured in ileal-cannulated pigs (gold standard per FAO/WHO 2013), growing-rat model (older, less preferred — values tend to be higher), or in vitro methods (newer, standardization ongoing). The table above uses pig-model values where available; in vitro values are used as supporting evidence only. This is consistent with FAO/WHO 2013 guidance that pig is the preferred in vivo proxy for human ileal digestion.

**Implication for Nutrition rule:** Use pig-model values as the primary basis. For pea and rice where variability is wide, choose the conservative (lower) end of the range when setting the D2 threshold. The ≥75 completeness cutoff is a binary gate — sources with DIAAS 78–100 are all "complete"; sources with DIAAS ≤67 are all "incomplete." The threshold is not close-call for most sources (clear exception: SPI at 78–98, where the low end is marginal).

### 3.2 Protein blend ambiguity (the canonical D5 gap)
The most common declaration on Israeli snack-bar and maadanim labels is "תערובת חלבונים (חלבון אפונה, חלבון אורז)" or similar — a two-source blend without proportions. The DIAAS of such a blend depends entirely on the pea:rice ratio:
- At pea:rice ≈ 70:30, the complementarity fully compensates and the blend DIAAS can reach ≥75.
- At off-ratio proportions, one source's deficiency is not corrected.

Since Israeli labels essentially never disclose the ratio, the blend DIAAS cannot be computed. This is the structural disclosure gap G3 defined in d5_d6_rule_spec_v1.md §1.2. Rule B (D5 flag, no penalty) handles this case.

### 3.3 Soy protein isolate borderline status
SPI's DIAAS range of 78–98 spans from "safely above 75" to "well above." The SAA (methionine+cysteine) limitation is real but mild at the isolate level. The 2017 BJN paper confirmed SPI as "high quality" in the FAO terminology. However, some in vitro DIAAS estimates have placed SPI at or below 75. Nutrition should set a clear rule: pig-model SPI = complete; if the product declares only "soy protein" without specifying isolate vs. flour (soy flour DIAAS is lower, ~55–65), the lower value applies.

### 3.4 Processing effects on DIAAS
Heat treatment generally increases DIAAS for plant proteins (PMID 37357639: heat-treated rapeseed > non-heated; similar patterns for soy). For dairy and egg proteins, normal food processing does not materially reduce DIAAS. This is relevant because Israeli food production involves typical industrial processing; the DIAAS values above are for food-grade processed materials, not raw source.

---

## 4. Research Return

**What was built:** An 8-source amino acid completeness table with DIAAS ranges, limiting amino acids, and completeness tiers for all protein sources commonly declared on Israeli food labels across the Bari corpus (hummus, maadanim, yogurt, snack bars).

**Primary sources used:**
1. FAO/WHO (2013). *Dietary Protein Quality Evaluation in Human Nutrition*. FAO Food and Nutrition Paper 92. — canonical framework; defines DIAAS and completeness thresholds. [Not in PubMed; cited as standard.]
2. Brouns et al. / PMID 28382889 (2017, British Journal of Nutrition) — pig-model DIAAS for WPI, WPC, MPC, SMP, PPC, SPI, wheat. **Strong anchor.**
3. PMID 33133540 (2020, Food Science and Nutrition) — comprehensive overview of 17 protein sources (5 animal + 12 plant); key classification evidence.
4. PMID 28573795 (2018, JSFA) — oat protein concentrate DIAAS measured in pigs; primary oat-specific evidence.
5. PMID 40075933 (2025, Animals) — pig-model DIAAS for white rice, wheat, PPC, SPI, SMP; recent confirmation.
6. PMID 37357639 (2023, JSFA) — rapeseed heat treatment with whey, soy, rice, pea comparisons; confirms protein ranking.
7. PMID 39703894 (2024, Journal of Nutritional Science) — egg DIAAS in multiple cooked forms; pig model.
8. PMID 34203642 (2021, Nutrients) — egg white protein DIAAS vs. whey and casein.

**Gaps for Nutrition to note:**
1. **Egg white vs whole egg:** Fewer dedicated egg-white DIAAS studies; values effectively equivalent to whole egg in all published reports but the N is small. Low practical risk — both are clearly excellent.
2. **Soy protein isolate vs. soy flour:** The ≥75 classification holds robustly for SPI; soy flour falls below 75. Many Israeli labels declare "סויה" generically. Nutrition rule should differentiate.
3. **Oat protein in whole-food context vs. isolate:** DIAAS data is for oat protein concentrate as an isolated ingredient. Oat flakes consumed as a whole food have a different protein availability profile (matrix effects); the DIAAS table applies to declared "oat protein" as an isolated ingredient, not to whole oat products.
4. **Rice protein variability:** Brown vs. white rice protein and degree of isolation produce a wide DIAAS range (37–58). A conservative approach (use ≤58 as the upper bound for incomplete tier) is recommended.
5. **No direct Israeli shelf measurement:** All DIAAS values are from international published literature; no Israeli-specific ileal digestibility data exists. This is a structural gap in the field, not just in our corpus. The international pig-model data is the field standard and is directly applicable.
6. **Casein concentration in dairy products:** Products declaring "חלבוני גבינה" or "חלבוני חלב" contain a mix of casein and whey; both are complete. No issue with classification.

**Confidence level:** High for animal sources (whey, casein, whole egg, egg white) — evidence is strong, consistent, and benchmarked by FAO. Moderate for plant sources (soy, pea, rice, oat) — direction is consistent across studies; specific numeric values carry wider confidence intervals due to source and method variation.

---

## Nutrition Rule Definition (Phase 2)

**Phase 2 author:** Nutrition Agent · **Date:** 2026-06-04 · **Evidence entry:** EV-040 (BSIP2 engine registry)

### Rule A — Complete-protein D2 credit

**Trigger:** The ingredient panel (after D5 pre-processing P1+P2) names exactly one protein source from the complete-protein whitelist below, and that source has DIAAS ≥ 75 per this table.

**Complete-protein whitelist (Israeli label terms):**
- חלבון מי גבינה מבודד / חלבוני מי גבינה (WPI / whey proteins, general)
- קזאין / חלבוני חלב / חלבוני גבינה (casein / milk protein concentrate / cheese proteins)
- ביצה שלמה / ביצים (whole egg)
- חלבון ביצה (egg white — same DIAAS classification as whole egg)
- חלבון סויה מבודד (SPI only — see soy-form constraint below)

**Effect:** +3 raw score points applied to the D2 ingredient-evidence sub-score. This is the defined magnitude: it is bounded to ≤ 0.5 grade band (the A→B threshold spans 15 points; +3 is approximately one-fifth of a grade band, which is a mild credit). The +3 cannot on its own move a product from one letter grade to the next; it modulates D2 within-grade positioning. The magnitude does not override D1 nutritional weakness — a product with poor macronutrient profile (D1) still scores poorly regardless of protein source quality.

**Rationale for +3:** The Research table shows clear binary separation: complete sources (DIAAS ≥ 100 for animal proteins, 78–98 for SPI) versus incomplete sources (DIAAS ≤ 67 for pea, rice, oat). The +3 credit is calibrated to be informative (it is a real D2 signal) but non-decisive (it cannot single-handedly change a grade). A product with an excellent nutritional panel that also declares a complete protein source earns marginally higher D2 standing — which is scientifically accurate. A product that relies on pea/rice blends for protein but has an otherwise strong panel does not lose points for protein incompleteness — it receives no D2 credit (neutral, not penalized), and Rule B flags the disclosure gap through D5/D6 only.

**Implementation guard:** Rule A fires at most once per product. If a product declares multiple named complete sources (e.g., "חלבון מי גבינה מבודד + קזאין"), Rule A credit is awarded once — the source quality is already "complete" and doubling the credit for a two-source blend would overweight the signal.

### Rule B — Disclosure gap D5/D6 flag

**Trigger:** The ingredient panel contains any of the following generic protein declarations without a single specific complete source being named:
- תערובת חלבונים (protein blend)
- חלבון צמחי (plant protein, generic)
- מי גבינה without the מבודד qualifier (generic whey, not specifying isolate — lower DIAAS possible)
- Any parenthetical blend of ≥2 protein sources without proportions, e.g., "תערובת חלבונים (חלבון אפונה, חלבון אורז)" — the canonical pea+rice case
- "חלבון" followed by a generic category term that does not name the source

**Effect:** D5 disclosure-gap annotation: "פרטי החלבון לא הופיעו בתווית" (protein source details were not shown on the label). This annotation enters the D5 disclosure profile as a G3 structural gap. If the D5-band reaches `partial` or worse (which it may independently from other gap types), the existing EV-037 mechanism applies (−10 confidence reduction via D6). Rule B does not add a standalone quality deduction — it adds a disclosure finding only.

**What Rule B is not:** Rule B does not penalize a product for having incomplete protein. It records that Bari cannot evaluate protein quality because the label does not provide enough information. The annotation is factual: "we cannot tell." This is distinct from a negative verdict.

**Consumer-facing language (D5 surface, plain Hebrew):** "מקור החלבון לא צוין בתווית — לא ניתן להעריך את איכות הספיגה שלו."

### Edge cases resolved

**1. Soy form distinction (SPI vs. soy flour):**
- "חלבון סויה מבודד" → Rule A credit applies. SPI DIAAS = 78–98 (pig model); the ≥75 threshold is met robustly. The variability is acknowledged (EV-040 evidence_strength: Strong for isolate form).
- "סויה" (generic soy ingredient, likely whole soy or flour) → No Rule A credit. Soy flour DIAAS = ~55–65 (below the ≥75 threshold). When the label does not specify "מבודד" (isolate), apply the conservative classification: incomplete.
- "חלבון סויה" without "מבודד" → No Rule A credit. Applies the same conservative rule: without isolate specification, assume the lower-DIAAS form.
- Rationale: The Research table (§3.3) documents the meaningful gap between SPI (~78–98) and soy flour (~55–65). The label term "מבודד" (isolated) is the required discriminating signal. Absent it, the conservative classification prevents false credit.

**2. Pea + rice blend (canonical D5 gap):**
- A declared pea+rice blend cannot receive Rule A credit regardless of the blend's theoretical achievable DIAAS.
- Rationale: DIAAS of pea+rice depends entirely on the pea:rice ratio. At pea:rice ≈ 70:30 the blend can reach ≥75; at off-ratio proportions it cannot. Israeli labels essentially never disclose this ratio. Granting Rule A credit on a theoretical blend achievability would fabricate a quality claim Bari cannot verify. The correct routing is Rule B: flag the disclosure gap.
- This is a principled asymmetry: the engine gives credit only for what the label declares, not for what might be true given optimal formulation.

**3. Collagen / gelatin:**
- "חלבון קולגן" and "ג'לטין" are incomplete proteins (DIAAS not in table — limiting on multiple IAA, especially tryptophan). No Rule A credit.
- These are already handled by d5_d6_rule_spec_v1.md §1.2 G3 as "disclosed-but-low-quality SIGNAL routed to D2, not a D5 gap."
- EV-040 confirms: collagen/gelatin declarations are noted in the D2 profile as a negative ingredient-evidence signal (protein source declared but incomplete), but they do not trigger Rule B (the source is named, which is a disclosure positive). The D2 signal is a mild negative, bounded and not decisive.

**4. Generic "מי גבינה" (whey, non-specific):**
- "מי גבינה" without "מבודד" typically refers to liquid whey, whey concentrate, or unspecified whey — DIAAS range varies but can be slightly lower than WPI.
- Decision: No Rule A credit for generic "מי גבינה." The Research note (§2.1) states "both WPI and WPC qualify as complete" for the whey entry, but Israeli labels that say "מי גבינה" without qualification could include liquid whey (lower protein density, lower DIAAS confidence). The conservative approach: only "חלבון מי גבינה מבודד" or "חלבוני מי גבינה" (specifically the protein fraction) earns Rule A credit.
- However, generic "מי גבינה" in a protein context does not trigger Rule B either — it is a named ingredient, even if not a complete-protein whitelist member. It is simply not credited.

**5. Multiple complete sources declared together:**
- Rule A credit fires once only, regardless of how many whitelist sources are named.
- Rationale: protein completeness is binary above ≥75. A product with two complete sources (e.g., whey + casein) is not doubly complete; it is complete. One credit, not two.

### Co-sign

Nutrition D7 co-sign: 2026-06-04.

Rule A magnitude (+3 raw score points) requires Product D7 co-sign before engine activation. The +3 is a mild D2 credit; it is not zero-impact (borderline products in wide-band scoring could move a few points), and any D2 sub-score rule that can move the headline grade in edge cases requires the full D7 dual sign-off per governance Hard Rule 8 and TASK-179P scope.

Rule B (D5 annotation + existing EV-037 D6 path) inherits existing Product approval from EV-037 and does not require a separate co-sign for the annotation itself. The D6 confidence reduction that may result from Rule B is governed by EV-037, which is already co-signed.

---

## Product D7 Co-sign (Rule A magnitude)

**Product D7 co-sign (Rule A magnitude): +3 accepted. 2026-06-04.**

Assessment: +3 is approximately one-fifth of a grade band (grade-band span = 15 points), making it decision-affecting as a real D2 signal without being capable of deciding between grades on its own. Three specific concerns reviewed:

1. **Gaming vector:** The whitelist requires a specific named declared source (חלבון מי גבינה מבודד, קזאין, ביצה שלמה, חלבון ביצה, חלבון סויה מבודד). A token WPI addition to earn the credit requires naming it as a declared ingredient — visible and auditable. The "fires once" guard eliminates compound-source stacking. Gaming path is costly and observable; the vector is acceptable.

2. **Frozen invariants:** BARI_GLASSBOX_W15 is off until this co-sign. All frozen runs (milk run_005_headpin / snack 70/B ceiling / bread provenance) are static frozen artifacts and are not live-recalculated; post-activation the +3 applies to future scoring passes only, not to frozen runs. No invariant conflict.

3. **D1 relationship:** +3 to D2 sub-score is structurally independent of D1 nutritional quality. It does not override a weak D1 signal. The calibration is correct relative to D1 weight.

BARI_GLASSBOX_W15 may be activated once Data agent Phase 3 verification (OFF byte-identity proof) is confirmed by QA.
