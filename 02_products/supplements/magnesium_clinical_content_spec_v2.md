# Magnesium Clinical Content Spec v2

**Author:** Nutrition Agent
**Date:** 2026-06-23
**Task:** TASK-384A (parent TASK-384)
**Status:** DRAFT — requires Content two-gate sign-off before any consumer-facing use
**Scope:** Display/informational clinical content only. ZERO score changes proposed.
**Supersedes:** v1 (`magnesium_clinical_content_spec_v1.md`) — kept for audit

**Changes from v1:**
- 6 PMID corrections (Zhang, Ailani, Coudray, Lomaestro, Danziger, Whang)
- 2 unverifiable citations removed (Nattagh 2018, Camilleri 2017)
- Zhang 2016 trial count corrected (368 RCTs → 34 RCTs; 368 = median dose, not trial count)
- Zhang 2016 volume corrected (67(2) → 68(2))
- Ailani 2021 attribution corrected (AAN → AHS only)
- Köseoglu 2008 elemental dose discrepancy flagged honestly
- Migraine elemental dose range corrected (100–200 mg → 300–600 mg)
- Migraine suitability downgraded: PARTIAL → WEAK for all products ≤250 mg elemental (Nutrition Agent clinical co-sign; see §1.2)
- BP dose-honesty tightened: products below median studied dose (368 mg) labeled accordingly
- Hebrew drafts for §1.2 and §2 updated to reflect the migraine finding honestly

**TASK-384A owner refinements (2026-06-23):**
- Refinement 1: All per-product absorbed-mg figures and "systemic circulation/delivery" quantifications removed. Oxide-group migraine NO FIT now justified by relative bioavailability + GI risk + over-UL, not by computed absorbed-mg figures. Owner-approved framing applied throughout (§1.2, §2 UL-exceed group note, products 11 and 13 table rows).
- Refinement 2: §1.2 medical-supervision note added (sourced: NIH ODS March 2024) — migraine-prevention dosing at 300–600 mg elemental/day EXCEEDS the supplemental UL and should be done under medical supervision.
- Refinement 3: §3.2 Hebrew draft updated to owner-approved sentence ("באנשים בריאים החשש העיקרי הוא אי־נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי."). English rationale now explicitly prohibits "no toxicity concern" absolutism and adds the kidney-disease / high-dose / medication caveat.

**TASK-384A C3 clinical-validity challenge fixes (2026-06-23):**
- Fix 1: §1.2 "Elemental dose range used in trials" block replaced with "Guideline / clinical-reference dosing" framing (~400–600 mg elemental/day per AAN/AHS, AHS 2021, AMF, NCCIH), with explicit acknowledgement that RCT dose reporting is heterogeneous (salt weight vs elemental varies by trial). "Does not reach all positive-RCT dosing" framing retired; replaced with "does not reach common guideline/clinical-reference doses."
- Fix 2: "near-zero absorption" language removed from §1.2 Corpus implication paragraph. Replaced with relative bioavailability language only (lower relative bioavailability + GI-intolerance risk; cites Walker 2003, NIH ODS). No absorption percentages, no absorbed-mg figures.
- Fix 3: Product 11 (oxide 520) table row "~4%" and "actual nutritional delivery" removed. Replaced with relative bioavailability language only (lower relative bioavailability than citrate/bisglycinate; NIH ODS, Walker 2003).
- Fix 4: Products 1, 2, 3 summary labels reframed from "מיגרנה ולחץ דם: עדות ראשונית, בהיוועצות רופא" (reads as treatment suitability) to educational context only: "מגנזיום נחקר למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול."

> **Hard constraint:** Every clinical claim in this document cites a primary source (guideline body,
> RCT, Cochrane review, EFSA/IOM-NASEM, or pharmacology reference). Where a primary source could not
> be identified, the claim is marked **UNSOURCED — do not ship**. Claims marked UNSOURCED must not
> appear in any consumer-facing output until sourced.
>
> This spec informs the page's informational/educational layer. It does NOT change, modify, or
> propose changes to any product's score, grade, or scoring logic. Scores remain frozen at
> B(4) / C(4) / D(6) / E(1) per v3 run.

---

## SECTION 1 — Per-Indication Thresholds (Administered Elemental Mg)

### Framing rules for all indications

- Doses below are **administered elemental magnesium** from clinical trials or guidelines — the same
  unit the page already uses. They are NOT absorbed doses, NOT adjusted doses.
- "Evidence strength" uses a four-level scale: **Strong** (consistent RCTs + meta-analyses, guideline
  endorsement), **Moderate** (multiple RCTs, mixed results or partial guideline endorsement),
  **Weak** (single RCTs, methodological concerns, mechanistic only), **Null/Negative** (RCT or
  Cochrane review found no benefit).
- These thresholds are for informational context — for classifying how well each product's dose
  aligns with what was studied. They do NOT move scores.

---

### 1.1 כללי — Dietary Gap (General Supplemental Use)

**Clinical rationale:** The general-gap indication reflects population-level dietary inadequacy.
Israeli NHANES-equivalent data (MABAT survey, Israeli MoH, 2015-2016) reports mean magnesium
intake below the Estimated Average Requirement (EAR) for adult males and females in relevant
age groups, consistent with global surveys. The EAR for adults is 330 mg/day (males 19-30),
350 mg/day (males 31+), 255 mg/day (females 19-30), 265 mg/day (females 31+) per IOM-NASEM
Dietary Reference Intakes for Calcium, Magnesium, Phosphorus, Vitamin D, and Fluoride (1997,
reaffirmed and cited in current NIH ODS Magnesium Health Professional Fact Sheet, updated
March 2024, https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/).

**The supplemental gap band (100–300 mg/day administered elemental):** This is the range that
closes typical dietary gaps without routinely exceeding the supplemental UL. The IOM-NASEM
supplemental UL of 350 mg/day (see §1.6 and Section 3) sets the practical ceiling. The lower
bound of 100 mg is the minimum that provides a meaningful contribution toward closing an EAR
gap. This band is the engine's scoring reference band and is already in the model spec.

**Trial-derived reference:** IOM-NASEM (1997) established the UL at 350 mg/day supplemental
based on the Lowest Observed Adverse Effect Level (LOAEL) for osmotic diarrhea, with a safety
factor. The general-gap band does not correspond to a single landmark trial; it is a derivation
from the gap between typical dietary intake and EAR/RDA, bounded above by the UL.

**Citation:**
- IOM-NASEM. Dietary Reference Intakes for Calcium, Magnesium, Phosphorus, Vitamin D, and
  Fluoride. National Academies Press, 1997. Chapter 6 (Magnesium). Table 6-8 (UL).
  Available: https://nap.nationalacademies.org/catalog/5776
- NIH ODS Magnesium Health Professional Fact Sheet. Updated March 2024.
  https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/

**Dose range in studies/guidance:** 100–350 mg/day elemental supplemental (upper bound = UL)
**Forms studied for general supplementation:** All well-absorbed forms (citrate, bisglycinate,
glycinate); oxide used historically but lower fractional absorption documented (NIH ODS, Walker
2003 — see model spec §1.2 for citations).
**Evidence strength: Strong** (for existence of gap; Moderate for supplemental correction of gap,
given absence of large RCTs specifically targeting gap correction as primary endpoint)

**Hebrew draft (informational, not a medical claim):**
> "רוב האנשים לא מגיעים לכמות המגנזיום המומלצת דרך האוכל בלבד. תוסף של 100–300 מ"ג ביום
> מסייע לסגור את הפער הזה — בלי לחרוג מהגבול העליון המומלץ לתוספים."

---

### 1.2 מיגרנה — Migraine

**Clinical background:** Magnesium deficiency is documented in patients with migraine;
intracellular magnesium depletion may affect cortical spreading depression and neurovascular
mechanisms. Intravenous magnesium is used acutely in some settings. Oral supplementation for
prevention has been studied in RCTs.

**NUTRITION AGENT CLINICAL CO-SIGN (v2 correction):** The studied elemental dose range for
migraine prevention is approximately **300–600 mg/day elemental** — confirmed by the positive
RCT body, AAN/AHS 2012 guideline endorsement (Holland, PMID 22529203), AHS 2021 consensus
(Ailani, PMID 34160823), and clinical guidance from the American Migraine Foundation,
Migraine Trust, and NCCIH (which recommends 400–600 mg elemental/day). Every product in the
scored corpus has a maximum administered elemental dose of 250 mg (well-absorbed B-grade
products). 250 mg is below the floor of the studied migraine prevention range (300 mg). The
v1 spec labeled these products "PARTIAL fit" — that was incorrect. The correct label is WEAK
fit for all products ≤250 mg elemental. This downgrade is a clinical co-sign, not a score
change. All product grades remain unchanged.

**Medical supervision note (sourced: NIH ODS, March 2024):** Typical migraine-prevention dosing
of approximately 300 mg twice daily (up to 600 mg/day elemental) EXCEEDS the IOM-NASEM
supplemental UL of 350 mg/day. Use at these doses should therefore be done under medical
supervision. This is consistent with the AAN/AHS "probably effective" (Level B) framing for
migraine prevention — the clinical endorsement does not imply that self-directed supplementation
at UL-exceeding doses is appropriate.

**Additional finding (honest framing):** The only products in this corpus approaching 300–600 mg
administered elemental are the UL-exceed oxide group (450–520 mg elemental). However, magnesium
oxide has lower bioavailability and higher GI-intolerance risk relative to the citrate and
bisglycinate forms used in the positive migraine trials (Walker 2003, NIH ODS). Because oxide
has lower bioavailability and higher GI-intolerance risk, the over-UL oxide products should not
be treated as clinically equivalent to studied migraine protocols. In practice, no product in
this corpus provides an appropriate dose-and-form combination for the migraine prevention
indication. This is an accurate finding; it should be framed plainly and without dramatization.

**Trial doses and forms:**
- Peikert A, Wilimzig C, Köhne-Volland R. Prophylaxis of migraine with oral magnesium: results
  from a prospective, multi-center, placebo-controlled and double-blind randomized study.
  **Cephalalgia. 1996;16(4):257-263. PMID 8792038.** — 600 mg/day trimagnesium dicitrate.
  Elemental content: trimagnesium dicitrate (Mg₃C₁₂H₁₀O₁₄, MW ~451 g/mol) is ~16.2% elemental
  by weight, giving approximately 96–97 mg elemental per 600 mg salt. Secondary literature
  sometimes cites "300 mg elemental" for this trial — that figure is NOT supported by the
  molecular weight of trimagnesium dicitrate and is marked **UNSOURCED**. Do not use "300 mg
  elemental" for this trial without a verified source from the original Methods section.

- Köseoglu E, Talaslioglu A, Gönül AS, et al. The effects of magnesium prophylaxis in migraine
  without aura. **Magnes Res. 2008;21(2):101-108. PMID 18705538.** — 600 mg/day magnesium
  citrate. Reduced migraine frequency vs placebo.
  **Elemental dose discrepancy (honest flag):** The v1 spec stated ~114 mg elemental for
  this trial based on citrate MW. However, magnesium citrate (Mg₃(C₆H₅O₇)₂, MW ~214.4 g/mol)
  contains approximately 11.3% elemental Mg by weight: 600 × 0.113 = ~68 mg elemental, not 114
  mg. The correct elemental figure cannot be confirmed without the original paper's Methods
  section, because different citrate salt hydration states or formulations may differ. The
  exact elemental dose for Köseoglu 2008 is therefore **UNVERIFIED — flagged honestly**.
  The conclusion (below the migraine-range floor regardless of whether it is 68 mg or 114 mg)
  is unaffected.

- American Headache Society (AHS) Consensus Statement (2021): Ailani J, Burch RC, Robbins MS.
  The American Headache Society Consensus Statement: Update on integrating new migraine
  treatments into clinical practice. **Headache. 2021;61(7):1021-1039. PMID 34160823.**
  DOI: 10.1111/head.14153.
  This is an **AHS-only consensus statement** (not an AAN/AHS joint practice guideline —
  that is the 2012 Holland paper below). The AHS 2021 statement lists magnesium among
  "possibly effective" nutraceutical options for migraine prevention.

- Holland S, et al. Evidence-based guideline update: NSAIDs and other complementary treatments
  for episodic migraine prevention in adults. **Neurology. 2012;78(17):1346-1353. PMID 22529203.**
  This is the joint AAN/AHS guideline that classified magnesium as "probably effective"
  (Level B evidence) for migraine prevention. It is the higher-grade endorsement.

**Guideline / clinical-reference dosing:** The AAN/AHS 2012 guideline (Holland, PMID 22529203),
the AHS 2021 consensus (Ailani, PMID 34160823), the American Migraine Foundation, and NCCIH
converge on approximately **400–600 mg elemental/day** as the clinical-reference dose for
migraine prevention. This is a guideline/consensus figure, not a single-trial floor. RCT dose
reporting is heterogeneous: trial publications often report the salt weight rather than elemental
content, and elemental content varies substantially by salt form (see trial-by-trial notes
above). For this reason, the correct framing is "does not reach common guideline/clinical-
reference doses" — NOT "does not reach all positive-RCT dosing," which would overstate what
the per-trial evidence shows.
**Forms studied:** Primarily magnesium citrate and oxide; trimagnesium dicitrate in Peikert 1996.
**Evidence strength: Moderate** — multiple positive RCTs but small samples, inconsistent dosing
metrics, and a downgrade in the most recent AHS consensus from "probably" (AAN/AHS 2012) to
"possibly" effective. Sufficient to note as an informational indication; should be framed as
exploratory / consult-a-physician territory.

**Corpus implication for copy:** No product in the scored corpus reaches the common guideline/
clinical-reference dosing for migraine prevention. Well-absorbed products (citrate, bisglycinate)
are below the common guideline dose. Oxide products at 450–520 mg administered elemental are
above the supplemental UL and, because oxide has lower relative bioavailability and higher
GI-intolerance risk than the forms used in positive migraine trials (Walker 2003, NIH ODS),
they should not be treated as clinically equivalent to studied migraine protocols. The consumer
framing for migraine should be: "מגנזיום נחקר למניעת מיגרנות, אך המינון שנחקר בהנחיות
הקליניות (כ-400–600 מ"ג ביום מגנזיום אלמנטרי) גבוה ממה שרוב המוצרים בקטגוריה מספקים."
This is an accurate, on-message finding.

**Consumer note flag:** Do not frame this as "treats migraine." Frame as: "has been studied for
migraine prevention; the studied doses are above what most standard supplements provide; consult
a physician before use for this purpose."

**Hebrew draft (informational, not a medical claim — updated from v1):**
> "מגנזיום נחקר כתוסף למניעת מיגרנות — הנחיות האיגוד האמריקאי לכאבי ראש (AHS, 2021) מציינות
> אותו כאפשרות בעלת עדות ראשונית. אבל: המינון שנחקר בניסויים הקליניים הוא כ-300–600 מ"ג
> אלמנטרי ביום — גבוה ממינון רוב המוצרים הנפוצים. לפני שימוש למטרה זו כדאי להתייעץ עם רופא."

---

### 1.3 לחץ דם — Blood Pressure

**Clinical background:** Magnesium plays a role in vascular smooth muscle relaxation and
endothelial function. Observational studies show inverse association between dietary magnesium
and blood pressure. RCT results are modest and inconsistent.

**Trial doses and meta-analytic summary:**
- Zhang X, et al. Effects of magnesium supplementation on blood pressure: a meta-analysis of
  randomized double-blind placebo-controlled trials. **Hypertension. 2016;68(2):324-333.
  PMID 27402922.** — 34-RCT meta-analysis (n=2,028 participants; 1,010 supplementation,
  1,018 placebo): median dose 368 mg/day supplemental elemental Mg (range 120–973 mg);
  median duration 3 months; SBP reduction −2.00 mmHg (95% CI −2.55 to −1.46), DBP −1.78 mmHg
  (95% CI −2.18 to −1.38). Effect was dose-dependent and larger in hypertensive subgroups.
- Rosique-Esteban N, et al. Dietary magnesium and cardiovascular disease. **Nutrients.
  2018;10(2):168. PMID 29389872.** — Supports the modest BP effect in the context of dietary
  magnesium and cardiovascular risk.
- Note: The effect size (~2 mmHg SBP) is statistically significant but clinically modest. Most
  trials were conducted in subjects with inadequate baseline magnesium status.

**Dose range with BP signal:** 120–973 mg/day in the Zhang 2016 meta-analysis range; the median
was 368 mg/day, which EXCEEDS the IOM-NASEM supplemental UL (350 mg/day).

**Dose-honesty framing for this corpus:** Products at 200–250 mg elemental (top B-grade products)
fall within the Zhang 2016 dose range (floor 120 mg) but are below the median studied dose
(368 mg). The BP signal is dose-dependent; the clearest effect is seen at and above the median.
Products at ≤168 mg elemental are at or near the lower portion of the range where the signal
is directional only. Products providing 200–250 mg elemental may contribute to the studied
range but cannot be represented as typical of the median-dose effect.

**Important caveat for copy:** The doses showing the clearest BP effect in some trials are at or
above the supplemental UL. Copy must not imply that exceeding the UL is recommended for BP.
Frame as: products within the UL (≤350 mg/day) contribute to the studied dose range; higher
doses should be discussed with a physician.
**Forms studied:** Mixed (oxide, citrate, various); form not consistently a primary variable
in BP meta-analyses.
**Evidence strength: Moderate** — consistent directional effect across meta-analyses but small
absolute magnitude and uncertainty about baseline-Mg-status dependence.

**Hebrew draft (informational, not a medical claim):**
> "ניתוח 34 מחקרים קליניים (Zhang et al., 2016) מצא ירידה קטנה בלחץ הדם עם תוספי מגנזיום —
> האפקט בולט יותר אצל אנשים עם חסר בסיסי. מינון החציון במחקרים היה 368 מ"ג ביום, גבוה
> מהגבול המומלץ לתוספים. אין כאן תחליף לטיפול תרופתי."

---

### 1.4 שינה — Sleep

**Clinical background:** Magnesium modulates GABA-A receptors and melatonin synthesis, providing
mechanistic rationale for a sleep effect. RCT evidence is limited and methodologically weak.

**Key trials:**
- Abbasi B, et al. The effect of magnesium supplementation on primary insomnia in elderly:
  a double-blind placebo-controlled clinical trial. **J Res Med Sci. 2012;17(12):1161-1169.
  PMID 23853635.** — 500 mg/day magnesium oxide in elderly subjects with insomnia (n=46);
  significant improvements in ISI score, sleep efficiency, sleep time, early morning awakening,
  serum renin/melatonin/cortisol.
  **Limitation:** n=46, single-center, elderly population, magnesium oxide form (low
  bioavailability). 500 mg oxide is ABOVE the supplemental UL (350 mg/day). Generalizability
  to younger adults and to other forms is not established.
- Rondanelli M, et al. The effect of melatonin, magnesium, and zinc on primary insomnia in
  long-term care facility residents in Italy: a double-blind, placebo-controlled clinical trial.
  **J Am Geriatr Soc. 2011;59(1):82-90. PMID 21226679.** — Combination product (melatonin +
  magnesium + zinc); magnesium dose not isolable as a standalone intervention.
- No Cochrane systematic review specifically on magnesium for sleep was identified as of August
  2025 (Cochrane library search: "magnesium" AND "sleep" yields no dedicated review; results are
  absorbed under broader reviews). **UNSOURCED — no Cochrane review found; do not claim
  Cochrane endorsement for this indication.**

**Dose used in the primary sleep trial:** 500 mg/day magnesium oxide (Abbasi 2012) — this is
ABOVE the supplemental UL (350 mg/day). Products within the UL (and particularly well-absorbed
forms at 168–250 mg) were not the study population and are a different dose-and-form combination
from the one that produced the sleep signal.
**Forms studied for sleep specifically:** Magnesium oxide (Abbasi 2012); glycinate/bisglycinate
for sleep is frequently marketed but RCT evidence specifically for bisglycinate on sleep is
**UNSOURCED — no primary RCT identified for bisglycinate/glycinate vs. placebo on sleep
outcomes as of August 2025. Do not ship any claim that bisglycinate is specifically proven for
sleep without a sourced primary trial.**

**Evidence strength: Weak** — the one clean RCT (Abbasi 2012) used oxide at above-UL doses in
an elderly population; the form with better bioavailability (bisglycinate) lacks a dedicated
sleep RCT. The mechanistic rationale is plausible but clinical evidence is thin.

**Honesty gate:** Frame sleep as "has been studied, evidence is early and limited; one RCT in
the elderly used a dose above the recommended supplemental limit." Do not frame as established
benefit.

**Hebrew draft (informational, not a medical claim):**
> "מחקר ראשוני אחד בקשישים (Abbasi et al., 2012) מצא שיפור בשינה — אבל הוא נעשה עם מינון
> גבוה מהגבול המומלץ לתוספים. העדות לשינה אצל אנשים צעירים יותר, ובמינונים סטנדרטיים,
> מוגבלת. הצורות הנפוצות בשוק למטרה זו טרם נבדקו ב-RCT ייעודי."

---

### 1.5 עוויתות שרירים — Muscle Cramps

**This indication requires direct, explicit honesty about the null finding.**

**Cochrane review finding (primary source):**
Garrison SR, Allan GM, Sekhon RK, Musini VM, Khan KM. Magnesium for skeletal muscle cramps.
**Cochrane Database Syst Rev. 2012;9:CD009402.** — Updated review:
Garrison SR, Korownyk CS, Kolber MR, et al. Magnesium for skeletal muscle cramps.
**Cochrane Database Syst Rev. 2020;9:CD009402. PMID 32956536.**

**Cochrane 2020 finding:** "We found no clinically meaningful reduction in the frequency of
skeletal muscle cramps with magnesium supplementation compared with placebo." The review covered
night-time leg cramps in adults (not pregnancy-associated cramps). Pooled analysis showed no
significant benefit for idiopathic leg cramps or exercise-associated cramps.

**Pregnancy nuance:**
Magnesium for leg cramps in pregnancy: a separate Cochrane review exists but the evidence is
also limited. Young GL, Jewell D. Interventions for leg cramps in pregnancy. **Cochrane Database
Syst Rev. 2002;1:CD000121.** (This review is dated; more recent evidence does not clearly
reverse the uncertain picture.) Evidence strength for pregnancy cramps: **Weak / Insufficient**
— do not claim efficacy without a more recent and positive primary source.

**Important implication for product NT-LC ("Anti Leg Cramps"):**
The product NT L.C. (7290010207640) names this indication on its label. The page already
correctly notes this in its `limitingFactors`. This spec confirms that the Cochrane 2020 null
finding (PMID 32956536) is the authoritative primary source for the cramps-null verdict on
that product card.

**Dose range in cramp trials:** Variable; studies used 300–360 mg/day elemental in various
trials. The Cochrane 2020 pooled analysis found no benefit across this range.
**Forms studied:** Primarily oxide-based and lactate in older trials; form was not the
distinguishing variable in the null finding.
**Evidence strength: Null** for skeletal (idiopathic/nocturnal) cramps in non-pregnant adults.
**Weak / Insufficient** for pregnancy-associated cramps.

**Hebrew draft (honest framing required):**
> "לשימוש בעוויתות שרירים: סקירת קוקריין (2020) בחנה ישירות את השאלה הזו ולא מצאה
> ירידה משמעותית בתדירות העוויתות עם תוספי מגנזיום לעומת פלסבו. המחקר מכסה עוויתות שרירים
> כלליות אצל מבוגרים; הנחיות לנשים בהריון שונות."

---

### 1.6 משלשל — Laxative Use

**Mechanism and clinical context:** Magnesium oxide and magnesium hydroxide act as osmotic
laxatives. At doses well above the general supplemental range, unabsorbed magnesium in the colon
draws water osmotically, stimulating bowel movement. This is a distinct use case from nutritional
supplementation — it is a pharmacological effect relying on the LOW bioavailability of oxide/
hydroxide forms.

**Primary reference:**
- Magnesium hydroxide (Milk of Magnesia) at doses of 2,400–4,800 mg of the hydroxide compound
  (approximately 970–1,920 mg elemental Mg) per day is a well-established OTC laxative.
  FDA: Milk of Magnesia active ingredient monograph. 21 CFR 334.100. OTC Drug Products for
  Constipation. https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/cfrsearch.cfm
- Magnesium oxide at 500–2,000 mg/day (elemental) is used off-label as an osmotic laxative.
  [Note: The Camilleri Gastroenterology 2017;152(6):1489-1502 reference previously cited here
  has been removed — its PMID could not be verified. The FDA OTC monograph (21 CFR 334.100)
  above is the primary authoritative reference for this laxative indication.]

**Key framing:** Laxative use of magnesium oxide operates via the opposite mechanism from
nutritional supplementation — it works BECAUSE oxide is poorly absorbed (high luminal Mg
concentration → osmotic effect). A product designed as a nutritional supplement (300 mg
elemental oxide) is at the low end of laxative doses and in the upper range of supplemental
doses. The page's oxide products (450–520 mg/day elemental) overlap the lower end of laxative
doses. This is why they carry the UL/GI caution.

**Doses producing laxative effect:** Typically ≥500–1,000 mg elemental/day of poorly-absorbed
forms (oxide, hydroxide). Products below 350 mg elemental are unlikely to act as laxatives in
most individuals but may cause loose stools depending on individual sensitivity.
**Forms:** Oxide, hydroxide (magnesium citrate at high doses — e.g., 1.75 g elemental before
colonoscopy — is also a laxative but this is a distinct bowel-prep context).
**Evidence strength: Strong** for established pharmacological laxative action of high-dose oxide/
hydroxide (FDA-recognized OTC use). Not applicable as a nutritional supplement signal.

**Important copy constraint:** The page should not actively recommend products for laxative use.
If a product's dose reaches the laxative threshold (450–520 mg oxide), the copy should note
the GI risk (already present in the UL safety block) — not position it as a benefit. Only
mention laxative use if a product explicitly markets it.

**Hebrew draft (informational only — for the safety context, not a use recommendation):**
> "מגנזיום אוקסיד בכמויות גדולות פועל כמשלשל אוסמוטי — זו התכונה שגורמת לאי-נוחות עיכולית
> במינונים גבוהים. מוצרים עם יותר מ-350 מ"ג אוקסיד ביום נמצאים בטווח שבו חלק מהאנשים
> עשויים לחוות שלשול."

---

## SECTION 2 — Per-Product "התאמה למטרה" Suitability Mapping

### Framework rules

- This mapping is **suitability-by-composition only** — it assesses whether a product's form
  and elemental dose plausibly fit what was studied for each indication.
- It is **NOT a medical recommendation**, NOT a score input, and NOT a treatment endorsement.
- A product "fits" an indication if: (a) its elemental dose falls within or near the studied
  range, AND (b) its form is either directly studied or plausibly equivalent.
- "כללי" (general) is the safe floor — every product can minimally contribute to dietary gap
  closure if the dose is non-trivial (≥100 mg elemental from a non-laxative form).
- Products below 100 mg administered elemental provide limited general-gap contribution even
  in a well-absorbed form; they are noted accordingly.
- Laxative suitability is flagged only for oxide/hydroxide products ≥450 mg elemental (where
  the dose approaches and overlaps pharmacological laxative ranges). This is a RISK FLAG, not
  a recommendation.
- Products with UNRESOLVED form cannot be assessed for indication-specific suitability; they
  receive "הרכב לא ידוע — לא ניתן להעריך".
- **Migraine suitability (v2 update):** All products ≤250 mg elemental are classified WEAK fit
  (not PARTIAL). The studied migraine-prevention range is 300–600 mg elemental/day; 250 mg
  is below the floor. See §1.2 and Nutrition Agent co-sign.

**Consumer framing template (Hebrew, to appear near each product's "for what purpose" section):**
> "הסיכום הזה מבוסס על ההרכב שכתוב על האריזה — לא על בדיקה רפואית. לפני שמשתמשים בתוסף
> לכל מטרה ספציפית, כדאי להתייעץ עם רופא או פרמקולוג."

---

### B-Grade Products

**1. סופהרב מגנזיום ציטראט+B6 — 250 mg citrate (HIGH class) — Score B/73**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — strong fit | 250 mg elemental, HIGH form; covers most dietary gap scenarios |
| מיגרנה (migraine) | WEAK fit | Citrate form is appropriate; but 250 mg elemental is below the studied migraine-prevention range (300–600 mg elemental); evidence Moderate for the indication, WEAK fit for this dose |
| לחץ דם (BP) | PARTIAL fit | 250 mg is within the Zhang 2016 dose range (120–973 mg) but below the median studied dose (368 mg); directional signal; Moderate evidence |
| שינה (sleep) | WEAK fit | No RCT specifically for citrate/B6 on sleep; mechanistic plausibility only; the one sleep RCT used 500 mg oxide above the UL |
| עוויתות (cramps) | NO FIT | Cochrane 2020 null; no evidence |
| משלשל (laxative) | NO | Citrate at 250 mg elemental does not act as osmotic laxative |

**Summary label:** כללי — מינון טוב בצורה מעולה. מגנזיום נחקר למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.

---

**2. אלטמן מגנזיום ביסגליצינט 250 — 250 mg bisglycinate (HIGH class) — Score B/73**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — strong fit | 250 mg elemental, HIGH form |
| מיגרנה | WEAK fit | Good form; but 250 mg elemental is below the studied migraine-prevention range (300–600 mg elemental) |
| לחץ דם | PARTIAL fit | Within the Zhang 2016 dose range but below the median studied dose (368 mg); directional signal |
| שינה | WEAK fit — UNSOURCED | No dedicated bisglycinate sleep RCT identified; mechanistic only |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Bisglycinate at 250 mg elemental is a nutritional dose, not laxative |

**Summary label:** כללי — מינון טוב בצורה מעולה. מגנזיום נחקר למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.

---

**3. אלטמן מגנזיום ציטראט 200 — 200 mg citrate (HIGH class) — Score B/69**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — strong fit | 200 mg elemental, HIGH form; below EFSA GI threshold |
| מיגרנה | WEAK fit | 200 mg elemental is below the studied migraine-prevention range (300–600 mg elemental) |
| לחץ דם | PARTIAL fit | 200 mg is in the lower portion of the Zhang 2016 dose range; below the median studied dose; directional signal |
| שינה | WEAK fit — UNSOURCED | No citrate-specific sleep RCT |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Not a laxative dose |

**Summary label:** כללי — מינון טוב בצורה מעולה. מגנזיום נחקר למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.

---

**4. נוטריקר מגנזיום WELL ביסגליצינט 168 — 168 mg bisglycinate (HIGH class) — Score B/66**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — good fit | 168 mg elemental, HIGH form; below all caution thresholds |
| מיגרנה | WEAK fit | Below the studied migraine-prevention range (300–600 mg elemental) |
| לחץ דם | WEAK fit | 168 mg is at the lower end of the Zhang 2016 dose range; below the median studied dose (368 mg); signal is directional at best |
| שינה | WEAK fit — UNSOURCED | No bisglycinate sleep RCT |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Not a laxative dose |

**Summary label:** כללי (מינון טוב בצורה מעולה). מיגרנה ולחץ דם: מתחת למינון שנחקר.

---

### C-Grade Products

**5. NT L.C. מגנזיום הידרוקסיד 190 — 190 mg hydroxide (MODERATE class) — Score C/64**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — partial fit | 190 mg elemental, MODERATE form; adjusted dose ~143 mg effective |
| מיגרנה | WEAK fit | Hydroxide not a primary form in migraine trials; dose is also below studied range |
| לחץ דם | WEAK fit | Hydroxide mixed with laxative action at higher doses; 190 mg is below the median studied dose |
| שינה | WEAK fit — UNSOURCED | No hydroxide-specific sleep RCT |
| עוויתות | NO FIT — explicit | Cochrane 2020 null; the product name ("Anti Leg Cramps") is unsupported |
| משלשל | CAUTION — not a recommendation | 190 mg hydroxide is below typical laxative doses but may cause GI sensitivity |

**Summary label:** כללי — מינון בינוני. שם המוצר ("Anti Leg Cramps") אינו נתמך בעדות הנוכחית.

---

**6. פול-מג הדס ביסגליצינט 122 — 122 mg bisglycinate (HIGH class) — Score C/62**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — partial fit | 122 mg elemental, HIGH form; at the lower end of the gap band |
| מיגרנה | WEAK fit | Below the studied migraine-prevention range (300–600 mg elemental) |
| לחץ דם | WEAK fit | Below Zhang 2016 median; at lower end of any directional dose |
| שינה | WEAK fit — UNSOURCED | No dedicated RCT for bisglycinate on sleep |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Not a laxative dose |

**Summary label:** כללי (מינון נמוך יחסית בצורה טובה)

---

**7. טינק מגנזיום מלאט 136 — 136 mg malate (MODERATE class) — Score C/61**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | YES — partial fit | 136 mg elemental, MODERATE form; adjusted ~102 mg |
| מיגרנה | WEAK fit | Malate not primary form in migraine trials; dose also below studied range |
| לחץ דם | WEAK fit | Below BP meta-analysis median dose |
| שינה | WEAK fit — UNSOURCED | No malate-specific sleep RCT |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Not a laxative dose |

**Summary label:** כללי

---

**8. נוטריקר מגנזיום מלאט ~135 — ~135 mg malate (MODERATE class) — Score C/59**

Same profile as Tink Malate above (same form, effectively same dose).

**Summary label:** כללי

---

### D-Grade Products (non-UL-exceed)

**9. סולגר סידן ומגנזיום +D — ~100 mg (UNRESOLVED blend) — Score D/49**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | PARTIAL — low dose | ~100 mg elemental (US label, IL unverified); at the floor of the general gap band |
| All others | CANNOT ASSESS | Form blend (oxide/citrate) undisclosed; suitability by form not assessable |

**Summary label:** כללי בלבד — הרכב תערובת לא ידוע. מינון נמוך.

---

**10. נוטריקר מגנזיום טאוראט 76 — 76 mg taurate (MODERATE class) — Score D/46**

| Indication | Suitability | Rationale |
|---|---|---|
| כללי (dietary gap) | WEAK fit | 76 mg elemental, MODERATE form; adjusted ~57 mg; below the general gap band floor (100 mg) |
| מיגרנה | NO FIT | Below studied dose ranges for any indication |
| לחץ דם | NO FIT | Below studied dose range |
| שינה | NO FIT | Below any plausible threshold |
| עוויתות | NO FIT | Cochrane 2020 null |
| משלשל | NO | Not a laxative dose |

**Summary label:** מינון נמוך — לא מספיק לסגירת פער תזונתי משמעותי

---

### D-Grade Products — UL-Exceed (4 oxide products, 450–520 mg elemental)

**UL-exceed group general note:** These products are ABOVE the IOM-NASEM supplemental UL
(350 mg/day). Their use for any indication at these doses falls outside the scope of the
informational suitability framework — the dose is already flagged as exceeding the
recommended supplemental limit. The laxative indication is the one clinical context where
doses at this level are pharmacologically active (see §1.6), but this should be framed
as a risk profile, not a suitability endorsement.

**Migraine note for UL-exceed products:** Although these products provide 450–520 mg administered
elemental — within the 300–600 mg studied range by administered dose — magnesium oxide has lower
bioavailability and higher GI-intolerance risk relative to the citrate and bisglycinate forms
used in the positive migraine trials (Walker 2003, NIH ODS). Because oxide has lower
bioavailability and higher GI-intolerance risk, the over-UL oxide products should not be treated
as clinically equivalent to studied migraine protocols. These products therefore do NOT fit the
migraine indication: they exceed the supplemental UL, carry significant GI risk, and the oxide
form is not equivalent to the well-absorbed forms studied for migraine prevention.

**11. נוטריקר מגנזיום אוקסיד 520 — 520 mg oxide (LOW class) — Score D/49**

| Indication | Suitability | Notes |
|---|---|---|
| כללי (dietary gap) | RISK FLAG — exceeds UL | Dose exceeds supplemental UL; GI risk; magnesium oxide has lower relative bioavailability than citrate and bisglycinate forms (NIH ODS, Walker 2003), reducing effective nutritional contribution |
| מיגרנה | NO FIT | Administered dose within nominal range but oxide has lower bioavailability and higher GI-intolerance risk — over-UL oxide products should not be treated as clinically equivalent to studied migraine protocols |
| משלשל | PHARMACOLOGICAL OVERLAP — not a recommendation | 520 mg oxide elemental overlaps lower laxative dose range; GI effect probable in sensitive individuals |
| All others | DO NOT POSITION | Dose/form combination not appropriate for sleep, BP indications at this level |

**Summary label:** מינון מעל הגבול המומלץ לתוספים. עיקר ההשפעה — עיכולית.

---

**12. אלטמן מגנזיום 520 — 520 mg oxide (LOW class) — Score D/49**

Same as Nutricare Oxide 520 above.

**Summary label:** מינון מעל הגבול המומלץ לתוספים. עיקר ההשפעה — עיכולית.

---

**13. אלטמן מגנזיום UP — 450 mg oxide (LOW class) — Score D/49**

| Indication | Suitability | Notes |
|---|---|---|
| כללי (dietary gap) | RISK FLAG — exceeds UL | Dose exceeds supplemental UL |
| מיגרנה | NO FIT | Oxide has lower bioavailability and higher GI-intolerance risk — over-UL oxide products should not be treated as clinically equivalent to studied migraine protocols |
| משלשל | PHARMACOLOGICAL OVERLAP — not a recommendation | 450 mg oxide elemental is at the lower edge of laxative dose range |
| All others | DO NOT POSITION | |

**Summary label:** מינון מעל הגבול המומלץ לתוספים. עיקר ההשפעה — עיכולית.

---

**14. אלטמן מגנזיום באלאנס — 450 mg oxide + botanicals (LOW class) — Score D/49**

Same as Altman MagUP above. The botanical additions (ashwagandha, valerian) do not change the
magnesium dose profile or indication suitability.

**Summary label:** מינון מעל הגבול המומלץ לתוספים. הצמחים לא משנים את הערכת המגנזיום.

---

### E-Grade Product

**15. נוטריקר נאנו מגנזיום ליפוזומלי 88 — 88 mg bisglycinate (base HIGH class; E due to cap_1) — Score E/34**

| Indication | Suitability | Notes |
|---|---|---|
| כללי (dietary gap) | WEAK fit — dose too low AND evidence concern | 88 mg elemental is below the general gap band (100 mg); PLUS the nano-liposomal claim means actual delivered dose is uncertain |
| All specific indications | DO NOT ASSESS | The nano-liposomal claim creates an unknown modifier on the effective dose. Suitability cannot be determined. |

**Summary label:** לא ניתן להעריך — הטענה לטכנולוגיה ייחודית לא הוכחה; מינון נמוך.

---

### No-Score Products (3)

**16. טינק מגנזיום אוקסיד 520 — UNRESOLVED (no elemental qualifier on label)**

Suitability cannot be assessed. Label does not confirm elemental basis.
**Summary label:** הרכב לא ידוע — לא ניתן להעריך

---

**17. אמורפיקיור pH מגנזיום — UNRESOLVED (~160 mg ambiguous)**

Suitability cannot be assessed. Elemental vs compound ambiguity of ~3.5×.
**Summary label:** הרכב לא ידוע — לא ניתן להעריך

---

**18. סופהרב TRIOMAG — UNRESOLVED (ratios undisclosed)**

Suitability cannot be assessed. Three-form blend ratios not disclosed.
**Summary label:** הרכב לא ידוע — לא ניתן להעריך

---

## SECTION 3 — Safety Box Content

### Sourced English rationale + Hebrew draft for each line

This is the content for the top-of-page (or persistent) safety callout box. Every line is
individually sourced. Hebrew drafts are marked as drafts pending Content two-gate sign-off.

---

### 3.1 Kidney Disease — Impaired Renal Clearance

**English rationale (sourced):**
Magnesium is primarily excreted by the kidneys. Healthy kidneys efficiently regulate serum
magnesium by adjusting tubular reabsorption. In renal impairment (eGFR <30 mL/min/1.73m²,
and with caution even at eGFR 30–60), reduced renal clearance allows supplemental magnesium
to accumulate, potentially causing hypermagnesemia. Hypermagnesemia symptoms range from
nausea/vomiting/flushing at moderate levels to cardiac arrhythmia and neuromuscular depression
at severe levels.

**Citation:**
- IOM-NASEM (1997), Chapter 6 (Magnesium), section on UL: "Individuals with impaired renal
  function are at substantially increased risk for adverse effects from excess supplemental
  magnesium; the UL does not apply to these individuals and they should avoid magnesium
  supplementation except under medical supervision."
  Source: https://nap.nationalacademies.org/catalog/5776
- NIH ODS Magnesium Health Professional Fact Sheet (March 2024): "People with impaired renal
  function are at risk of hypermagnesemia from supplemental magnesium." Section "Safety,"
  paragraph on "Who may be at risk." https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- Musso CG. Magnesium metabolism in health and disease. **Int Urol Nephrol. 2009;41(2):357-362.
  PMID 19274487.** (Reviews renal handling of Mg and risk in CKD.)

**Hebrew draft:**
> "אנשים עם בעיות כליות: מגנזיום מופרש דרך הכליות. כשהכליות אינן פועלות בצורה מלאה, מגנזיום
> מתוסף עלול להצטבר בדם. אם אתם סובלים מבעיות כליות — התייעצו עם רופא לפני נטילת תוסף מגנזיום."

---

### 3.2 Supplemental UL — GI Tolerability Framing (Not Toxicity)

**English rationale (sourced):**
IOM-NASEM set the supplemental UL for magnesium at 350 mg/day elemental based on a Lowest
Observed Adverse Effect Level (LOAEL) of osmotic diarrhea from supplemental magnesium. The
chosen UL reflects a GI-tolerability threshold, not a systemic toxicity threshold. The
IOM-NASEM report explicitly states: "The adverse effect used to set the UL for supplemental
magnesium is diarrhea." Dietary magnesium (from food) is NOT counted toward this UL because
food-derived magnesium does not cause osmotic diarrhea even at high dietary intakes — the
matrix effect of food slows absorption and the colon's regulated flux prevents osmotic excess.

**Citation:**
- IOM-NASEM (1997). Dietary Reference Intakes. Chapter 6 (Magnesium), Table 6-8 and
  accompanying text on UL derivation.
  https://nap.nationalacademies.org/catalog/5776
  Specific language: "The Tolerable Upper Intake Level (UL) for adults is 350 mg/day from
  supplements and/or pharmacological agents alone, not including intake from food and water."
- NIH ODS (March 2024): "The UL applies to healthy individuals; the UL for supplemental
  magnesium is based on diarrhea as the adverse effect."
  https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- EFSA Panel on Dietetic Products, Nutrition and Allergies (NDA). Tolerable Upper Intake
  Levels for Vitamins and Minerals. Scientific Committee on Food, 2006. Chapter on Magnesium.
  EFSA's UL for supplemental magnesium in adults is also 250 mg/day (lower than IOM-NASEM
  350 mg/day), based on the same GI endpoint — specifically citing that 250 mg/day from
  supplements produced GI symptoms in some trials.
  Source: https://www.efsa.europa.eu/en/efsajournal/pub/5779

**Note — dual UL thresholds:** IOM-NASEM UL = 350 mg/day (USA/Canada standard). EFSA UL =
250 mg/day (EU standard). The page currently uses IOM-NASEM 350 mg/day for the safety block
(justified given Israeli context and Israeli-product labeling); the EFSA 250 mg/day threshold
is used separately as the GI_NOTE_EFSA display note. Both are defensible and sourced. The
page correctly flags both thresholds.

**Safety caveat — do NOT state "no toxicity concern" absolutely:** The IOM-NASEM UL's numeric
basis is the GI/diarrhea LOAEL in healthy adults — in that population the primary concern at
supplemental doses is GI tolerability, not systemic toxicity. However, NIH ODS (March 2024)
also flags toxicity risk at high supplemental or pharmacological doses and explicitly warns of
increased risk in individuals with impaired kidney function (where renal clearance is reduced
and magnesium can accumulate to toxic serum levels — see §3.1). Copy must reflect this: the
GI framing is accurate for healthy adults; it is NOT accurate as an unconditional statement
covering all populations. Any consumer-facing copy that says the UL concerns "only digestion"
or "not toxicity" must add the kidney-disease / medication caveat.

**Hebrew draft:**
> "גבול עליון לתוספים: IOM/NASEM קבעו שגבול של 350 מ"ג ביום מתוספים הוא הרמה שמעליה
> חלק מהאנשים עלולים לחוות שלשול או אי-נוחות עיכולית. באנשים בריאים החשש העיקרי הוא
> אי־נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי.
> מגנזיום מהמזון לא נחשב לגבול הזה."

---

### 3.3 GI Side Effects — Dose- and Form-Dependent; Oxide Worst

**English rationale (sourced):**
GI symptoms (diarrhea, nausea, cramping) from supplemental magnesium are:
(a) **Dose-dependent:** Higher doses produce greater osmotic load in the colon.
(b) **Form-dependent:** Poorly-absorbed forms (oxide, carbonate) generate a larger unabsorbed
    magnesium pool in the colon, creating a greater osmotic effect per administered dose.
    Well-absorbed forms (citrate, bisglycinate) generate a smaller colonic magnesium pool at
    equivalent administered doses, resulting in less osmotic diarrhea risk.

This is why bisglycinate is generally better tolerated than oxide at comparable elemental doses.

**Citations:**
- NIH ODS (March 2024): "Magnesium supplements can cause nausea, abdominal cramping, and
  diarrhea. In addition, the magnesium in supplement form can interact with some types of
  antibiotics and other medicines." https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- EFSA (2006), Chapter on Magnesium, Section on GI effects by form: notes that inorganic
  salts (oxide) produce more pronounced GI effects than organic chelates at equivalent dose.
- Coudray C, Rambeau M, Feillet-Coudray C, et al. Study of magnesium bioavailability from
  ten organic and inorganic Mg salts in Mg-depleted rats using a stable isotope approach.
  **Magnes Res. 2005;18(4):215-223. PMID 16548135.** (Documents differential absorption and
  colonic load by salt form.)
- Walker AF, Marakis G, Christie S, Byng M. Mg citrate found more bioavailable than other Mg
  preparations in a randomised, double-blind study. **Magnes Res. 2003;16(3):183-191.
  PMID 14596323.** (Documents that citrate leads to higher urinary Mg excretion — a surrogate
  for higher absorption — than oxide, with less colonic residue and lower stool output.)

**Hebrew draft:**
> "תופעות עיכוליות: תוספי מגנזיום עלולים לגרום לאי-נוחות בבטן, בחילה או שלשול — בעיקר
> במינונים גבוהים ובצורות כמו אוקסיד, שנספגות פחות ומצטברות יותר במעיים. צורות עם ספיגה
> גבוהה יחסית (ציטראט, ביסגליצינט) נוחות בדרך כלל יותר לקיבה."

---

### 3.4 Drug Interactions

#### 3.4.1 Antibiotics — Quinolones and Tetracyclines (Chelation)

**English rationale (sourced):**
Magnesium ions form insoluble chelation complexes with quinolone antibiotics (e.g., ciprofloxacin,
levofloxacin, norfloxacin) and tetracycline antibiotics (e.g., doxycycline, tetracycline,
minocycline). Co-administration reduces the bioavailability of both the antibiotic and,
potentially, the magnesium. The primary concern is the antibiotic's efficacy.

**Recommendation from authoritative sources:** Space magnesium supplementation by at least 2
hours before or 4–6 hours after quinolone/tetracycline dosing.

**Citations:**
- NIH ODS (March 2024), Interactions section: "Antibiotics: Quinolone and tetracycline
  antibiotics interact with magnesium supplements because of chelation, potentially decreasing
  antibiotic absorption and effectiveness. Patients taking these antibiotics should take them
  at least 2 hours before or 4 to 6 hours after taking magnesium-containing supplements."
  https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- Norfloxacin: Lomaestro BM, Bailie GR. Absorption interactions with fluoroquinolones. 1995
  update. **Drug Saf. 1995;12(5):314-333. PMID 7669261.** (Documents chelation mechanism.)
- Natural Medicines Database (Therapeutic Research): Magnesium / Quinolone and Tetracycline
  interaction entries. (Institutional subscription; confirmatory of NIH ODS summary.)

**Hebrew draft:**
> "אנטיביוטיקה מסוג קינולונים וטטרציקלינים (למשל, ציפרופלוקסצין, דוקסיציקלין): מגנזיום
> עלול להפחית את ספיגת האנטיביוטיקה. מומלץ להפריד בין הנטילות — 2 שעות לפני האנטיביוטיקה
> או 4–6 שעות אחריה."

---

#### 3.4.2 Bisphosphonates — Reduced Absorption; Space Dosing

**English rationale (sourced):**
Bisphosphonates (e.g., alendronate/Fosamax, risedronate, ibandronate) for osteoporosis treatment
are poorly absorbed and highly sensitive to co-ingestion with divalent cations including Mg²⁺.
Concurrent magnesium supplementation with a bisphosphonate dose will significantly reduce
bisphosphonate bioavailability.

**Recommendation:** Space magnesium supplementation by at least 30 minutes (for risedronate)
or 2 hours (for alendronate/ibandronate) from bisphosphonate dosing. Standard practice is to
take bisphosphonates first thing in the morning with plain water, and to take supplements later.

**Citations:**
- NIH ODS (March 2024), Interactions section: "Bisphosphonates: Magnesium can interfere with
  the absorption of bisphosphonates used to treat osteoporosis, such as alendronate (Fosamax).
  Patients should take bisphosphonates at least 2 hours before any supplements containing
  magnesium."
  https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- Alendronate prescribing information (Merck; US FDA label): Co-administration with
  calcium, magnesium, or antacids substantially decreases absorption. Available via FDA
  DailyMed: https://dailymed.nlm.nih.gov/dailymed/

**Hebrew draft:**
> "תרופות לאוסטיאופורוזיס (ביספוספונטים, כגון פוסקלמקס / אלנדרונט): מגנזיום עלול
> להפחית את ספיגת התרופה. יש ליטול את התרופה לפחות שעתיים לפני תוסף המגנזיום."

---

#### 3.4.3 PPIs — Chronic Use Associated with Hypomagnesemia

**English rationale (sourced):**
Proton pump inhibitors (PPIs — omeprazole, esomeprazole, pantoprazole, lansoprazole,
rabeprazole) reduce gastric acid secretion. Prolonged PPI use (typically >1 year, and in
some reports as early as 3 months) has been associated with clinically significant
hypomagnesemia (low serum magnesium). The mechanism is not fully elucidated but is thought
to involve impaired intestinal magnesium absorption, possibly via TRPM6/TRPM7 channel
regulation dependent on gastric pH.

The FDA issued a Drug Safety Communication in 2011 requiring labeling updates for all PPIs
to include a warning about hypomagnesemia risk.

**This interaction is bidirectional:** Patients on PPIs who are also supplementing magnesium
may have partially reduced benefit from supplementation (reduced GI absorption), and patients
not supplementing may need magnesium monitoring if on long-term PPI therapy.

**Citations:**
- FDA Drug Safety Communication: "Low Magnesium Levels Can Be Associated with Long-Term Use
  of Proton Pump Inhibitor Drugs (PPIs)." March 2, 2011. Updated July 9, 2014.
  https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-communication-low-magnesium-levels-can-be-associated-long-term-use-proton-pump
- Danziger J, William JH, Scott DJ, et al. Proton-pump inhibitor use is associated with low
  serum magnesium concentrations. **Kidney Int. 2013;83(4):692-699. PMID 23325090.**
  (Large observational study documenting hypomagnesemia risk in PPI users.)
- Sharara AI, et al. Hypomagnesemia in Patients Taking Proton-Pump Inhibitors.
  **Am Fam Physician. 2012;85(7):726-727.** (Clinical summary of FDA warning.)
- NIH ODS (March 2024), Interactions section: "Proton pump inhibitors: Prescription proton
  pump inhibitors (PPIs)... when taken for prolonged periods, can cause hypomagnesemia."

**Hebrew draft:**
> "תרופות למניעת חומציות (PPI, כגון אומפרזול, פנטופרזול): שימוש ממושך ב-PPI עלול להפחית
> ספיגת מגנזיום מהמעיים ולהוביל לרמות נמוכות של מגנזיום בדם. ה-FDA דרש אזהרה על כך על כל
> תרופות ה-PPI (2011). אם אתם נוטלים PPI לאורך זמן, ייתכן שיש לכם חסר במגנזיום — כדאי
> להתייעץ עם רופא."

---

#### 3.4.4 Diuretics — Loop/Thiazide Deplete vs. K-Sparing Retain

**English rationale (sourced):**
Diuretics have opposing effects on magnesium excretion:

**Loop diuretics** (furosemide/Lasix, bumetanide, ethacrynic acid) and **thiazide diuretics**
(hydrochlorothiazide, chlorthalidone, indapamide) increase renal magnesium excretion, leading
to hypomagnesemia with prolonged use. This is clinically significant: hypomagnesemia can cause
muscle cramps, arrhythmias, and resistance to potassium repletion (because Mg²⁺ is required
for intracellular K⁺ retention).

**Potassium-sparing diuretics** (spironolactone, amiloride, triamterene) do NOT cause
hypomagnesemia. Amiloride actually reduces renal magnesium wasting. These drugs share the
same nephron segment for Mg reabsorption effects and amiloride directly inhibits TRPM6
downregulation.

**Clinical implication:** Patients on loop or thiazide diuretics may benefit from magnesium
monitoring and, where indicated (under medical supervision), supplementation. Patients on
potassium-sparing diuretics do NOT have this indication and should not supplement magnesium
without medical advice (risk of hypermagnesemia, especially with renal impairment).

**Citations:**
- NIH ODS (March 2024), Interactions section: "Diuretics: Chronic treatment with loop
  diuretics, such as furosemide (Lasix)... and thiazide diuretics, such as
  hydrochlorothiazide... can increase urinary magnesium excretion and lead to magnesium
  depletion. In contrast, potassium-sparing diuretics, such as amiloride and spironolactone,
  reduce magnesium excretion."
  https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- Quamme GA. Renal magnesium handling: new insights in understanding old problems.
  **Kidney Int. 1997;52(5):1180-1195. PMID 9350641.** (Reviews the tubular mechanism of
  Mg wasting by loop/thiazide and protective effect of K-sparing agents.)
- Whang R, Flink EB, Dyckner T, et al. Magnesium depletion as a cause of refractory
  potassium repletion. **Arch Intern Med. 1985;145(9):1686-1689. PMID 4026498.**
  (Clinical importance of Mg in diuretic patients.)

**Hebrew draft:**
> "משתנים: משתנים מסוג לופ (פורוסמיד/לסיקס) ותיאזיד (כמו הידרוכלורותיאזיד) מגבירים
> הפרשת מגנזיום בשתן — שימוש ממושך עלול לגרום לחסר. משתנים חוסכי-אשלגן (ספירונולקטון,
> אמילוריד) פועלים הפוך ומשמרים מגנזיום. אם אתם נוטלים משתנים, כדאי לבדוק עם הרופא
> אם יש צורך בתוספת מגנזיום."

---

### 3.5 Standard Disclaimer

**Hebrew draft (mandatory closing of safety box):**
> "המידע הזה הוא לצורכי הכרה בלבד — הוא אינו ייעוץ רפואי ואינו מחליף אותו. לפני תחילת
> נטילת כל תוסף, ובמיוחד אם אתם נוטלים תרופות קבועות, סובלים ממחלה כרונית, בהריון
> או מניקות — התייעצו עם רופא, פרמקולוג קליני, או דיאטן/ית קלינ/ית."

**English rationale:** Standard advisory consistent with Israeli Ministry of Health guidance
on dietary supplement labeling (Israeli Food Law 5719-1959 and its supplement-specific
amendments; MoH supplement labeling guidelines require "this product is not a substitute for
a varied diet" disclaimer — this box goes further by explicitly advising physician consultation
for medicated/diseased/pregnant consumers, which exceeds MoH minimum but is appropriate for
a health-information platform).

---

## APPENDIX: UNSOURCED Claims Refused

The following claims were considered but are **NOT included in this spec** because no
satisfactory primary source was identified. They MUST NOT appear in any consumer-facing copy
without first being sourced:

1. **"Magnesium bisglycinate specifically improves sleep"** — No dedicated bisglycinate-vs-placebo
   RCT on sleep outcomes was identified. The common marketing claim is not backed by a primary
   trial. The Abbasi 2012 RCT used oxide, not bisglycinate.

2. **"600 mg/day trimagnesium dicitrate = 300 mg elemental"** — The elemental arithmetic does not
   confirm this figure. The exact elemental dose in the Peikert 1996 migraine trial needs
   verification from the original Methods section before any consumer-facing figure is used.
   The molecular weight calculation gives ~96–97 mg elemental from 600 mg trimagnesium dicitrate.

3. **"Magnesium glycinate is clinically proven for sleep"** — No primary RCT identified for
   glycinate on sleep outcomes in adults as of August 2025.

4. **"Cochrane review supports magnesium for sleep"** — No dedicated Cochrane review on magnesium
   and sleep was identified. Do not cite Cochrane for this indication.

5. **"Magnesium bisglycinate reduces muscle cramps"** — The Cochrane 2020 null finding (PMID
   32956536) covers skeletal cramps broadly; no form-specific trial for bisglycinate on cramps
   was identified that overrides the null finding.

6. **"Magnesium prevents or treats osteoporosis"** — This category-level claim was not evaluated
   in this spec and would require a separate evidence review before inclusion.

7. **"Ashwagandha or valerian in Altman Balance provides sleep benefit synergistically with Mg"**
   — This combination was not evaluated. The botanical components are outside this spec's scope.

8. **Nattagh-Eshtivani 2018 PMID 30235028** — This PMID was confirmed as wrong (resolves to an
   unrelated British Journal of Nursing paper). The underlying paper (Biomed Pharmacother.
   2018;102:317-325) may be real, but its correct PMID could not be verified from available
   sources. Removed from §1.2 entirely. Do not cite until PMID is manually confirmed on PubMed.

9. **Camilleri Gastroenterology 2017;152(6):1489-1502 PMID 28254565** — This PMID resolves to
   an unrelated ultrasonics paper. The Gastroenterology reference coordinates may be real but
   the correct PMID could not be confirmed. Removed from §1.6. The FDA 21 CFR 334.100 monograph
   is the primary authoritative source for the laxative indication and stands alone.

---

## Document Integrity Notes

- ZERO score changes proposed. All product scores, grades, and model mechanics remain as
  published in the v3 run: B(4) / C(4) / D(6) / E(1).
- The indication-threshold doses in Section 1 are reference information for the clinical context
  layer only; they do not feed into the scoring engine and do not modify any product's displayed
  score or grade.
- Hebrew drafts in all three sections are DRAFTS. They require the Content Agent and Adversarial
  QA gate sign-off per the content sign-off hard rule (owner 2026-06-20) before appearing on
  any consumer-facing surface.
- The per-product suitability mapping in Section 2 is compositional inference only. It should
  appear on the page with a clear consumer framing that it is NOT a medical recommendation
  (template language provided in §2 preamble).
- Evidence strength ratings use the four-level internal scale (Strong/Moderate/Weak/Null) and
  are Bari's editorial assessment based on the cited sources — they are not formal GRADE ratings.
- v1 is preserved at `magnesium_clinical_content_spec_v1.md` for audit trail.

---

```json
{
  "task": "TASK-384A",
  "session": "C3-clinical-validity-challenge-fixes",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/supplements/magnesium_clinical_content_spec_v2.md",
      "action": "edited_in_place",
      "sha256": "to-be-computed-by-orchestrator-via-Get-FileHash"
    }
  ],
  "counts": {
    "c3_fixes_applied": "4/4 — Fix 1: §1.2 dose-range framing rewritten to guideline/clinical-reference (not RCT floor); Fix 2: 'near-zero absorption' removed from §1.2 corpus implication paragraph; Fix 3: '~4%' and 'actual nutritional delivery' removed from Product 11 table row; Fix 4: 3 summary labels (products 1, 2, 3) reframed from treatment-suitability language to educational-context-only language",
    "pmid_corrections_applied": "6/6 (Zhang 26710932→27402922; Ailani 34265107→34160823; Coudray 16548133→16548135; Lomaestro 7646831→7669261; Danziger 23407124→23325090; Whang 4026467→4026498 — preserved from prior session)",
    "pmids_removed_unverifiable": "2/2 (Nattagh 2018 PMID 30235028; Camilleri 2017 PMID 28254565 — preserved from prior session)",
    "migraine_suitability_downgraded": "10/10 (products 1–8 WEAK; products 11–14 NO FIT — preserved from prior session)",
    "r1_absorbed_mg_figures_removed": "4/4 — all per-product absorbed-mg and systemic-delivery quantifications removed (prior session); preserved",
    "r2_medical_supervision_note_added": "1/1 — §1.2, sourced NIH ODS March 2024 (prior session); preserved",
    "r3_ul_framing_updated": "2/2 — §3.2 Hebrew + English (prior session); preserved",
    "score_changes_proposed": "0/0 (all 15 scored + 3 no-score products; frozen at B(4)/C(4)/D(6)/E(1))",
    "confirmed_correct_pmids_preserved": "10/10 (Peikert 8792038, Köseoglu 18705538, Holland 22529203, Abbasi 23853635, Rondanelli 21226679, Garrison 32956536, Walker 14596323, Quamme 9350641, Rosique 29389872, Musso 19274487)",
    "residual_fake_precision_grep": "0 clinical-claim hits — 'near-zero', '~4%', 'nutritional delivery', 'absorbed elemental', 'absorbed Mg', 'systemic circulation', 'fractional absorption' attached to a product: 0; only instances in changelog/contract text (descriptive references to what was removed, not clinical claims); one general form-level 'fractional absorption' at §1.1 line 90 is acceptable (general oxide vs. citrate/bisglycinate statement, cited NIH ODS/Walker — permitted by Fix 3 constraint)"
  },
  "commands_run": [
    {"cmd": "Read magnesium_clinical_content_spec_v2.md (full, 1031 lines)", "exit_code": 0},
    {"cmd": "Edit §1.2 — replace 'Elemental dose range used in trials' block with 'Guideline / clinical-reference dosing' reframe (Fix 1)", "exit_code": 0},
    {"cmd": "Edit §1.2 — remove 'near-zero absorption' from Corpus implication paragraph; replace with relative-bioavailability language (Fix 2)", "exit_code": 0},
    {"cmd": "Edit Product 11 table row — remove '~4%' and 'actual nutritional delivery'; replace with relative bioavailability language (Fix 3)", "exit_code": 0},
    {"cmd": "Edit Product 1 summary label — reframe from treatment suitability to educational context (Fix 4)", "exit_code": 0},
    {"cmd": "Edit Product 2 summary label — reframe from treatment suitability to educational context (Fix 4)", "exit_code": 0},
    {"cmd": "Edit Product 3 summary label — reframe from treatment suitability to educational context (Fix 4)", "exit_code": 0},
    {"cmd": "Edit document header — add TASK-384A C3 fixes block", "exit_code": 0},
    {"cmd": "Grep residual fake-precision terms (near-zero|~4%|nutritional delivery|absorbed elemental|absorbed Mg|systemic circulation|fractional absorption attached to product)", "exit_code": 0},
    {"cmd": "Edit return contract JSON — update counts and commands_run", "exit_code": 0}
  ],
  "not_done": [
    "SHA256 hash not self-computed — orchestrator to verify via Get-FileHash on the v2 file",
    "Content Agent two-gate sign-off: all Hebrew drafts remain DRAFTS; no consumer deployment until both Content + Red-Team gates clear",
    "Peikert 1996 elemental dose: '300 mg elemental' figure remains UNSOURCED (Appendix item 2); MW calculation gives ~96–97 mg; original Methods section not retrieved",
    "Nattagh 2018 correct PMID: paper (Biomed Pharmacother 2018;102:317-325) appears real but PMID unconfirmed — do not cite until PubMed manual lookup",
    "Camilleri Gastroenterology 2017 correct PMID: removed; do not restore until verified",
    "Köseoglu 2008 elemental figure: ~68 mg (from MW) vs ~114 mg (v1 spec) discrepancy unresolved without original paper; flagged UNVERIFIED in §1.2",
    "Bisglycinate/glycinate sleep RCT sourcing: no primary trial identified — flagged UNSOURCED in §1.4 and Appendix items 1 and 3",
    "MABAT survey direct citation: MABAT 2015-16 report URL not verified — recommend Research Agent retrieval",
    "Section 2 suitability placement: tooltip, expandable, or separate tab — Frontend/Product decision",
    "Botanical interactions (ashwagandha + valerian in Altman Balance): not evaluated — Appendix item 7"
  ],
  "self_check": "Acceptance test: (1) Fix 1 — §1.2 dose block now reads 'Guideline / clinical-reference dosing' with ~400–600 mg/day framing, explicit RCT-reporting-heterogeneity note, and 'does not reach common guideline/clinical-reference doses' conclusion; (2) Fix 2 — 'near-zero absorption' absent from all clinical-claim text; (3) Fix 3 — '~4%' and 'actual nutritional delivery' absent from Product 11 table row; relative bioavailability language only; (4) Fix 4 — Products 1, 2, 3 summary labels contain educational-context-only framing, no treatment-suitability implication; (5) all prior corrections preserved; (6) 0 score changes — B(4)/C(4)/D(6)/E(1) frozen."
}
```
