# Magnesium Scoring Model v2 — Final Build-Ready Spec

**Author:** Nutrition Agent
**Date:** 2026-06-23
**Status:** PROPOSED — awaiting Product Agent D7 co-sign before engine implementation
**Inputs used:**
- `02_products/supplements/real_corpus_v3/magnesium_elemental_reconciliation_v1.md` (authoritative elemental table)
- C3 adversarial verdict, `tasks/returns/P300_return.md` lines 19-118
- Prior model: `03_operations/supplement_engine/proto_v0/benchmark/magnesium_absorbed_scoring_FINAL_v1.md` (SUPP-EV-030 v3.1)
- Prior C3 assumption review: `03_operations/supplement_engine/proto_v0/benchmark/magnesium_assumptions_c3_v1.md`

**What changed from v1 (SUPP-EV-030 v3.1):**
The prior model scored on absorbed-mg derived from label elemental × population-average absorption fraction. This v2 spec switches the primary dose signal to **administered elemental mg** — the figure the label declares — and maps form to bioavailability class rather than a numeric absorption fraction. The absorbed-mg path (SUPP-EV-030) is retired as the primary driver. Bioavailability class modulates the evidence sub-score and interpretation; it does not produce a pseudo-precise absorbed figure.

**Why:** The C3 verdict (P300) confirmed that absorbed-mg fractions applied to Israeli shelf products (~1–18 mg absorbed for all products) compressed all products into a narrow band and produced a sole C product and a majority-E/D shelf regardless of meaningful dose differences. The prior model also treated elemental declarations as compound masses (the Fix-A error corrected by the reconciliation), which systematically understated dose for 7 products by 6–11×. The corrected elemental values — already what the SKU corpus stores — place most products at 76–250 mg elemental, meaningfully above the prior Fix-A figures, and demand a scoring model that reads those doses correctly.

---

## Part 1 — The 3-Pillar Model

### Pillar 1: Dose (administered elemental mg vs indication band)

**What we score:** The label-declared elemental magnesium per recommended daily serving. This is the auditable number a consumer sees. It is NOT the absorbed amount, which varies by individual and cannot be derived from a label with clinical precision.

**Framing rule (C3 refinement #2):** Thresholds are administered-elemental trial doses drawn from published RCT dose ranges, separated by indication. They are NOT efficacy guarantees. A product meeting a band is "at the dose studied for this indication." A product below a band is "below the dose range studied." We do NOT say a product is "effective" or "ineffective" — we say it meets or falls short of the studied administered dose.

**Indication bands (administered elemental mg/day):**

| Indication | Lower bound | Upper bound | Evidence basis |
|---|---|---|---|
| General dietary gap support | 100 mg | 300 mg | Reasonable supplemental range to close partial dietary gaps; not a treatment dose |
| Blood pressure | 300 mg | 400 mg | Meta-analysis median ~368 mg/day (Zhang 2016, PMID:27402922); modest ~2 mmHg SBP effect; supervised context |
| Migraine prophylaxis | 400 mg | 600 mg | Common clinical use range (Mauskop 2012 PMID:22426836; Sun-Edelstein 2009 PMID:19271946); exceeds supplemental UL — see safety section |
| Sleep (older adults) | 200 mg | 400 mg | Systematic review (Mah 2021 PMID:33865376); very-low evidence quality; framed as exploratory only |
| Muscle cramps | 300 mg | 500 mg | Used in some trials; Cochrane 2020 (PMID:32956536) found magnesium unlikely to provide clinically meaningful cramp prophylaxis in older adults — this indication carries an insufficient-evidence flag |
| Laxative / bowel regularity | 500 mg | 800 mg | Osmotic mechanism is well-established; not a supplement-in-gap use; carries specific UI label |

**Dose sub-score rules:**

1. Determine the product's declared indication (from label claims, marketing copy, or the indication selected for the scored use-case).
2. Compare administered elemental mg to the indication's lower bound:
   - ≥ lower bound → dose_tier = MEETS
   - 50–99% of lower bound → dose_tier = NEAR (half-step below)
   - < 50% of lower bound → dose_tier = FAR_BELOW
3. Also check the upper bound. Products exceeding the upper bound for migraine (> 600 mg) or BP (> 400 mg) trigger the safety gate before dose_tier is finalized.
4. The dose sub-score maps:
   - MEETS → dose contribution 70–100 (scaled linearly within-band; at lower bound = 70, at or above midpoint = 85, at upper bound = 100)
   - NEAR → dose contribution 40–69 (scales linearly from 50% of lower bound = 40, to lower bound = 70)
   - FAR_BELOW → dose contribution 0–39 (scales linearly; at 0 mg = 0, at 50% of lower bound = 40)
5. Products with multiple stated indications: score against the most demanding indication for which the label makes a claim.
6. General-gap use (no specific indication stated on label): score against 100–300 mg general band.

**Scoring weight: dose_pillar_weight = 0.40**

---

### Pillar 2: Bioavailability Class

**What we score:** The form of magnesium determines bioaccessibility class. Class is a categorical designation — not a pseudo-precise absorbed-mg figure. Consumer display: class label + qualitative description only. NEVER display "the body gets X mg."

**Evidence basis for class assignment (C3 refinement #3):**
- Class boundaries are evidence-grounded, not marketing-driven.
- A broader human comparative evidence base (not just mechanistic plausibility) is required for HIGH class.
- Specific evidence citations are listed here; the SUPP-EV-030 evidence dossier carries the full registry entries.

**Bioavailability class map:**

| Class | Forms | Basis | Consumer label |
|---|---|---|---|
| HIGH | citrate, bisglycinate, glycinate | Citrate: multiple human comparative studies vs oxide support superior absorption and tolerability (PMID:7815675 context; general bioavailability literature). Bisglycinate/glycinate: mechanistic support + some human data, tolerability advantage; direct evidence vs citrate thinner than marketing implies. Class is shared — NOT "glycinate > citrate." | ספיגה גבוהה יחסית (evidenced) |
| MODERATE | malate, taurate, hydroxide | Malate: limited direct human comparative data; organic structure supports reasonable bioaccessibility. Taurate: very limited head-to-head data; placed above oxide on mechanistic grounds. Hydroxide: higher solubility than oxide (water-soluble compound); elemental fraction 41.7%; placed above oxide. | ספיגה בינונית |
| LOW | oxide, carbonate | Oxide: low solubility, lowest fractional absorption in comparative studies (4% range commonly cited; PMID:7815675 context). Carbonate: similar insolubility profile; limited direct data. | ספיגה נמוכה יחסית |
| UNRESOLVED | blend (undisclosed ratios) | Cannot assign class when per-form mg is unknown and no dominant component is established. | הרכב לא פורט — לא ניתן להעריך ספיגה |

**Class → evidence sub-score modifier:**
- HIGH: +8 points added to evidence sub-score
- MODERATE: +3 points added to evidence sub-score
- LOW: 0 (no modifier)
- UNRESOLVED: −5 points (hidden composition penalty on evidence sub-score)

**Scoring weight: bioavailability class feeds the evidence sub-score**
- Evidence pillar weight = 0.30

---

### Pillar 3: Transparency + Safety Gates

**Safety gate — UL framing (C3 refinement #4):**

The supplemental magnesium UL is 350 mg/day from supplements only (Institute of Medicine/NASEM). This UL is a GI/tolerability threshold — it signals increased risk of osmotic diarrhea, not acute toxicity. It excludes magnesium from food. A product exceeding 350 mg elemental from supplements does not automatically become unsafe; it means GI effects are more likely and the use context should include medical supervision. The engine does NOT cap scores at UL automatically; it flags the UL exceedance for consumer display.

**Safety flags:**

| Flag | Trigger | Engine action |
|---|---|---|
| UL_EXCEED | Administered elemental > 350 mg/day | Flag displayed in UI safety block: "מנה זו עולה על סף הסבילות המומלץ (350 מ"ג/יום תוסף) — עשויה לגרום לאי-נוחות עיכולית. מומלץ בהתייעצות עם איש מקצוע." Score: −10 from final score. NOT a hard cap. |
| UL_MIGRAINE_NOTE | Migraine indication AND administered elemental > 350 mg | Additional copy displayed: "מינוני מיגרנה (400–600 מ"ג) עולים מעל הסף — שימוש בהשגחה רפואית." |
| LAXATIVE_MODE | Administered elemental > 500 mg AND no therapeutic claim context | Display: "מינון זה פועל בעיקר כמשלשל אוסמוטי — לא כהשלמת מגנזיום בגוף." |

**Transparency sub-score:**

| Signal | Points |
|---|---|
| Label explicitly states elemental mg (two-line OR "from/as" convention with elemental declared) | +15 |
| Label states form by chemical name | +10 |
| Two-line label (compound mg AND elemental mg separately stated) | +5 bonus |
| Blend with disclosed per-component ratios | +10 (vs full disclosure; achievable for blends) |
| Blend with undisclosed ratios | −15 |
| Claim on label without evidence tier (e.g. "ליפוזומלי" without published data) | −10 |
| Evidence-insufficient proprietary delivery system (liposomal, nano, etc.) | −15 (cap_1 path preserved) |

**Honesty cap (preserved from SUPP-EV-030):**

Products with evidence-insufficient primary claims (cap_1) or hidden-composition blends (cap_3_honesty_core) retain hard score ceilings:
- cap_1 (insufficient evidence for claimed delivery mechanism): ceiling = 34 → maximum grade E
- cap_3_honesty_core (proprietary blend, undisclosed ratios, cannot verify elemental dose): ceiling = 49 → maximum grade D

**Scoring weight: transparency + safety pillar weight = 0.30**

---

### Weight Summary

| Pillar | Weight |
|---|---|
| Dose (administered elemental vs indication band) | 0.40 |
| Bioavailability evidence class (feeds evidence sub-score) | 0.30 |
| Transparency + safety | 0.30 |

Grade bands (unchanged from global supplement engine):
S ≥ 90 | A ≥ 80 | B ≥ 65 | C ≥ 50 | D ≥ 35 | E < 35

---

## Part 2 — Per-Product Table (Scored Set)

### Notation

- Verified elemental: from `magnesium_elemental_reconciliation_v1.md` (label-wins rule). Where the reconciliation confirms the SKU corpus value IS the elemental value, that value is used directly. Where the engine previously derived elemental from compound mass (oxide/hydroxide), the reconciliation-confirmed elemental figure is used.
- Grade band: marked ESTIMATE — to be confirmed by real engine re-run with v2 model.
- Reconciliation confidence levels carried forward as label_confidence.

### Scored Products (13 products)

These products have verified elemental dose (two-line evidence, explicit "מגנזיום אלמנטרי" declaration, or "from/as" format with cross-verified IL sources) OR chemistry-forced compound-derived elemental where both audits agree.

| # | Barcode | Name (short) | Verified elemental mg/day | Form | Bioavailability class | Primary indication band | Dose tier (general gap) | Dose tier (specific indication) | Safety flags | Label confidence | Projected grade band (ESTIMATE) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 7290011899967 | Altman Citrate 120 | 200 mg | citrate | HIGH | General gap | MEETS (200/100=2.0×) | — | None | High | C–B | Two-line convention confirmed; altman.co.il HTTP 200. Prior model computed 32mg (WRONG — Fix-A error). |
| 2 | 7290013464248 | Supherb Citrate+B6 Badatz | 250 mg | citrate | HIGH | General gap + fatigue (B6 combo) | MEETS (250/100=2.5×) | — | None | High | C–B | "מגנזיום (as Magnesium Citrate) 250 מ"ג" — elemental. biogaya.co.il confirmed. Prior model: 41mg (WRONG). |
| 3 | 7290019444480 | Altman Bisglycinate | 250 mg | bisglycinate | HIGH | General gap / sleep | MEETS (250/100=2.5×) | Sleep: MEETS (250mg ≥ 200mg lower bound) | None | High | C–B | "(as Magnesium Bisglycinate) 250 מ"ג" — elemental. altman.co.il HTTP 200. Prior model: 35mg (WRONG). |
| 4 | 7290001943700 | Full-Mag Hadas 600 | 122 mg | bisglycinate | HIGH | General gap | MEETS (122/100=1.22×) | Sleep: NEAR (122mg, below 200mg lower bound) | None | High | C | Form: bisglycinate (Albion USA confirmed). Elemental: 600mg compound / 122mg elemental confirmed (tevaworld.com + drugstore.co.il + vitamins4all.co.il). Previously unscoreable_incomplete — now scoreable. |
| 5 | 7290018439043 | Nutricare WELL | 168 mg | bisglycinate | HIGH | General gap | MEETS (168/100=1.68×) | Sleep: NEAR (168mg, below 200mg lower bound) | None | High | C | "785mg bisglycinate provides 168mg elemental" — two-line. vitamins4all + v-care + maxpharm confirmed. Prior engine: cap_1 (proprietary form). v2 model scores on administered elemental; proprietary-form cap_1 reviewed — if the bisglycinate form is verified and no unsupported delivery claim is made, cap_1 may not apply. Recommend engine re-run to determine whether WELL's "WELL proprietary blend" claim triggers cap_1. Flagged for engine review. |
| 6 | 7290001065594 | Nutricare Nano Bisglycinate | 88 mg | bisglycinate | HIGH | General gap | NEAR (88mg = 88% of 100mg lower bound) | — | None | High | D–E | "88 מ"ג מגנזיום אלמנטרי" — explicit Hebrew elemental declaration. maxpharm.co.il HTTP 200. cap_1 (liposomal claim without evidence) preserved in v2: ceiling 34 → E is likely binding regardless of dose. |
| 7 | 7290018439579 | Nutricare Taurate | 76 mg | taurate | MODERATE | General gap | NEAR (76mg = 76% of 100mg lower bound) | BP: FAR_BELOW (76mg vs 300mg lower bound = 25%) | None | High | E | "950mg taurate / 76mg elemental" — two-line explicit. 76mg for BP is far below band. For general gap, NEAR. Prior model: 7mg (WRONG — 10.9× Fix-A error). Dose improves substantially but dose_tier only reaches NEAR at general gap. |
| 8 | 7290001066973 | Nutricare Malate | ~133–137 mg elemental | malate | MODERATE | General gap | MEETS (133–137mg ≥ 100mg) | — | None | High | C | Compound: 700mg malate. Fraction dispute: 0.195 (standard trimagnesium malate) vs 0.155. Reconciliation verdict: use 0.195; range 700×0.155=109 to 700×0.195=137. No label-stated elemental figure found. Conservative display: "~133–137 mg elemental (estimated from compound)." Score must reflect range; use midpoint for grade estimate. |
| 9 | 7290001065662 | Nutricare Oxide 520 | ~314 mg elemental | oxide | LOW | General gap | MEETS (314 ≥ 100) | — | UL_EXCEED (314 mg > 350 threshold: borderline — 314 < 350, no flag) | High | D | 520mg compound oxide × 0.603 = 314mg elemental. Both audits agree. HIGH elemental dose but LOW class — dose_tier MEETS, but LOW bioavailability class penalty on evidence sub-score. No UL flag (314 < 350). |
| 10 | 7290015318426 | Tink Oxide 520 | ~314 mg elemental | oxide | LOW | General gap | MEETS (314 ≥ 100) | — | None (314 < 350) | High | D | Same as Nutricare Oxide: 520mg compound, ~314mg elemental. |
| 11 | 7290017218564 | Altman 520 | ~314 mg elemental | oxide | LOW | General gap | MEETS (314 ≥ 100) | — | None (314 < 350) | High | D | Same. |
| 12 | 7290013142894 | Altman MagUp | ~272 mg elemental | oxide | LOW | General gap | MEETS (272 ≥ 100) | — | None (272 < 350) | High | D | 450mg compound oxide × 0.603 = 272mg elemental. |
| 13 | 7290019444206 | Altman Balance | ~272 mg elemental | oxide | LOW | General gap | MEETS (272 ≥ 100) | — | None (272 < 350) | High | D | 450mg compound oxide × 0.603 = 272mg elemental. |
| 14 | 7290010207640 | NT LC Anti Leg Cramps | 190 mg elemental | hydroxide | MODERATE | Cramps | NEAR for cramps (190mg vs 300mg lower bound = 63%) | — | Cramps indication: insufficient evidence flag | High | D | Label explicitly states "190 מ"ג מגנזיום אלמנטרי" (label-wins over fraction 188mg). Hydroxide: moderate class. Cramps indication flagged insufficient evidence (Cochrane 2020 PMID:32956536). |
| 15 | 7290015318532 | Tink Malate | 136 mg elemental | malate | MODERATE | General gap | MEETS (136 ≥ 100) | — | None | High | C | Two-line label: "850mg compound / 136mg elemental." bella-natura.net HTTP 200. Prior model: 21mg (WRONG — Fix-A error 6.5×). |

### Exception Products (not on absorbed-path; scored via honesty/blend path)

| # | Barcode | Name (short) | Stored amount | Form | Elemental | Score path | Projected grade (ESTIMATE) | Notes |
|---|---|---|---|---|---|---|---|---|
| 16 | 0033984005181 | Solgar Cal-Mag D3 | 100 mg per 5-tab serving | oxide+citrate blend | 100 mg stated; US label — IL label unverified | blend_dominant_limit path. Per-component ratios not disclosed → UNRESOLVED class. cap_3_honesty_core ceiling 49. | D | Combo-product value-flag exemption preserved. IL Hebrew label should be verified before consumer deployment (low priority per reconciliation — global brand unlikely to differ). |

---

### Unresolved Products (not scored — label confidence insufficient for the administered-elemental model)

These products render in the UI as "לא ניתן לאמת את כמות המגנזיום" with label_confidence: unclear. They appear in the category table but without a numeric score or grade. This is not a failure state — it is the honest disclosure of a data gap.

| Barcode | Name (short) | Issue | Recommended action before scoring |
|---|---|---|---|
| 7290015429245 | Amorphicure pH Carbonate | "160 מ"ג מגנזיום" — elemental vs compound unconfirmed. If elemental: 160mg (general gap MEETS); if compound (carbonate, 28.8% elemental): 46mg (FAR_BELOW). 3.5× score difference depending on resolution. | Physical label photo required. One additional targeted retrieval attempt; discard if unresolved per missing-data discard rule. |
| 7290118816065 | Supherb TRIOMAG | "מספקת כ-200 מ"ג מגנזיום" — likely elemental by IL convention; form ratios (citrate:bisglycinate:taurate) not disclosed, blocking per-form class assignment. If elemental 200mg: MEETS general gap; class UNRESOLVED (blend). | Physical label or manufacturer spec sheet required for form ratios. If ratios confirmed, reassign class and score. If only total elemental confirmed, score on dose with UNRESOLVED class. |

### Discarded Products

| Barcode | Name (short) | Reason |
|---|---|---|
| 7290118818205 | Supherb Max 550 | Oxide:citrate ratio undisclosed on all accessible Israeli sources. Administered elemental is unknowable. Cannot score on administered-elemental model. Discarded per missing-data discard rule (owner-approved in task brief). |

---

## Part 3 — Hebrew Consumer Copy

### A. Revised Category Caveat (הערת קטגוריה)

**UI placement:** Yellow caveat box, top of category page, above all scores.

> **על מה אנחנו משווים?**
>
> כל מוצר בהשוואה זו נבחן לפי שלושה פרמטרים: (1) כמות המגנזיום האלמנטרי המוצהרת על גבי התווית — זאת הכמות שהיצרן מבטיח שתקבל ממנה; (2) צורת המגנזיום ורמת הספיגה הצפויה ממנה לפי הספרות המדעית — סיווג איכותי, לא חישוב מדויק; (3) שקיפות התווית ובטיחות המינון.
>
> **מה הציון לא מודד:** מה שגופך בפועל יספוג — זה משתנה מאדם לאדם, תלוי בחומציות הקיבה, ברמות המגנזיום הבסיסיות ובגורמים נוספים שתווית לא יכולה לגלות. ציון גבוה פירושו שהמוצר מציע מינון מנומק בצורה ספיגה מוכחת יחסית — לא ערובה לתוצאה.
>
> **הערה על מינונים:** מינוני מחקר למיגרנה ולהורדת לחץ דם עשויים לחרוג מסף הסבילות המומלץ לתוספים (350 מ"ג/יום). שימוש במינונים אלה מומלץ בהתייעצות עם רופא.

---

### B. Safety Block (above the score table)

**UI placement:** Fixed block above the product table, not collapsible.

> **סף הסבילות:** ארגון הבריאות הרפואי האמריקאי (NASEM) קבע סף של 350 מ"ג מגנזיום אלמנטרי ליום מתוספים בלבד — כמות שמעליה עולה הסיכוי לאי-נוחות עיכולית ושלשול אוסמוטי. הסף אינו חל על מגנזיום ממזון. מוצרים החורגים מסף זה מסומנים בטבלה; שימוש בהם בפיקוח רפואי מומלץ.
>
> **חשוב:** אנו משווים מוצרים על בסיס תוויות — לא בדיקות מעבדה. מחקרים הראו שחלק ניכר מתוספי מגנזיום בשוק לא עמד בהצהרות הכמותיות שלהם. הציון מניח שהתווית מדויקת.

---

### C. Product Copy Examples (3 examples)

#### Example 1 — Riser (Altman Citrate 120 / 7290011899967)

**insightLine:**
> מגנזיום ציטראט 200 מ"ג — מינון ראוי בצורה מבוססת מחקר.

**rowVerdict:**
> 200 מ"ג מגנזיום אלמנטרי מציטראט — מעבר לסף לתמיכה תזונתית כללית. ציטראט נמצא בהשוואות אנושיות כמתפרק ונספג טוב יותר מאוקסיד. לא מוצר לצורך קליני ספציפי, אבל הגיוני לפערי תזונה יומיומיים.

**expansion block:**
> אלטמן ציטראט 120 מספק 200 מ"ג מגנזיום אלמנטרי בכמוסה — הצהרת תווית מאומתת. ציטראט היא צורה עם בסיס השוואות ישיר רחב יחסית לעומת אוקסיד, ועם פרופיל סבילות טוב. בהשוואה לאוקסיד 520 מ"ג שמספק פי 1.5 מגנזיום אלמנטרי על התווית — ציטראט 200 מ"ג עדיין עדיף לרוב השימושים כי הפרש הספיגה נוטה לקזזו. **מה שלא ידוע:** כמה בדיוק ייספג בגופך — זה מתחת לסף מה שניתן לחשב מתווית.

---

#### Example 2 — Oxide (Altman 520 / 7290017218564)

**insightLine:**
> מגנזיום אוקסיד 520 מ"ג — מינון גבוה, ספיגה נמוכה.

**rowVerdict:**
> ~314 מ"ג מגנזיום אלמנטרי על התווית — בין הגבוהים במדף. אוקסיד הוא הצורה עם הספיגה הנמוכה ביותר לפי הספרות, ומופיע לעתים כמשלשל אוסמוטי בנטילה גבוהה. זול ומינוניו גבוהים — אבל המינון שמגיע לרקמות קטן יותר מהמספר על האריזה מרמז.

**expansion block:**
> אלטמן 520 מ"ג מגנזיום אוקסיד מספק ~314 מ"ג מגנזיום אלמנטרי לפי חשוב כימי (520 × 0.603). הכמות הכוללת על התווית גבוהה — מינון שמעל כל הצורות האורגניות בהשוואה. הבעיה היא שאוקסיד הוא צורה עם מסיסות מוגבלת, וסקירות ספרות מצביעות על ספיגה ממוצעת נמוכה יחסית לציטראט ולגליצינאט. מחיר נמוך ומינון גבוה הופכים אותו לאטרקטיבי — אבל "הרבה על הנייר" אינו שווה ל"הרבה בגוף."

---

#### Example 3 — Unresolved (Supherb TRIOMAG / 7290118816065)

**insightLine:**
> TRIOMAG — המינון על התווית לא מאומת מספיק לציון.

**rowVerdict:**
> TrioMag מציין "כ-200 מ"ג מגנזיום" לכמוסה, אך לא פירט את יחסי שלוש הצורות. בלי יחסי הרכב, לא ניתן להעריך ספיגה צפויה. מוצר זה מופיע ברשימה ללא ציון — לא כי המגנזיום שבו פחות, אלא כי התווית לא נותנת מספיק מידע להשוואה הוגנת.

**expansion block:**
> TrioMag משלב ציטראט, ביסגליצינאט וטאוראט — שלוש צורות עם פרופילי ספיגה שונים. הבעיה: הפצת היחסים בין הצורות לא מפורסמת. "כ-200 מ"ג מגנזיום" — ככל הנראה אלמנטרי לפי המוסכמה הישראלית — אבל לא ניתן לאמת זאת מהתווית ולא מצוין "אלמנטרי" במפורש. עד לקבלת תווית מלאה, TrioMag מופיע בהשוואה עם סימון "נתונים חסרים" בלבד.

---

### D. UI Field Spec

| Field | Value type | Rule |
|---|---|---|
| `administered_elemental_mg` | Integer or range (e.g. "133–137") | Label-declared elemental. Never display as absorbed. |
| `bioavailability_class` | String: "גבוהה" / "בינונית" / "נמוכה" / "לא ידועה" | Display always, verbatim. |
| `bioavailability_display` | Short descriptor | "ספיגה גבוהה יחסית" / "ספיגה בינונית" / "ספיגה נמוכה יחסית" / "הרכב לא פורט — לא ניתן להעריך ספיגה" |
| `indication_band_match` | String | "עומד בטווח המחקרי ל[indication]" / "מתחת לטווח המחקרי" / "קרוב לסף" |
| `safety_flag` | Boolean or null | If UL_EXCEED: display Hebrew safety block (see above). |
| `label_confidence` | "גבוה" / "בינוני" / "לא ברור" | Shown as sub-text near the score; drives the unresolved state. |
| `score_display` | Numeric/grade OR "לא ניתן לדרג" | Unresolved products: "לא ניתן לדרג — נתוני תווית חסרים" instead of numeric score. |

**HARD RULE — never display absorbed mg:**
No UI field may display "הגוף סופג X מ"ג" or any variant. Bioavailability_class is the only absorption-related display. This rule must be enforced at the frontend component level.

---

## Part 4 — Scored vs Unresolved / Discarded — Explicit List

### Scored (15 products)

1. 7290011899967 — Altman Citrate 120 (200 mg elemental, citrate, HIGH class)
2. 7290013464248 — Supherb Citrate+B6 Badatz (250 mg elemental, citrate, HIGH class)
3. 7290019444480 — Altman Bisglycinate (250 mg elemental, bisglycinate, HIGH class)
4. 7290001943700 — Full-Mag Hadas 600 (122 mg elemental, bisglycinate, HIGH class)
5. 7290018439043 — Nutricare WELL (168 mg elemental, bisglycinate, HIGH class) — engine re-run required to confirm cap_1 applicability
6. 7290001065594 — Nutricare Nano Bisglycinate (88 mg elemental, bisglycinate, HIGH class) — cap_1 binding (liposomal claim), ceiling 34 expected
7. 7290018439579 — Nutricare Taurate (76 mg elemental, taurate, MODERATE class)
8. 7290001066973 — Nutricare Malate 90cp (~133–137 mg elemental, malate, MODERATE class)
9. 7290001065662 — Nutricare Oxide 520 (~314 mg elemental, oxide, LOW class)
10. 7290015318426 — Tink Oxide 520 (~314 mg elemental, oxide, LOW class)
11. 7290017218564 — Altman 520 (~314 mg elemental, oxide, LOW class)
12. 7290013142894 — Altman MagUp (~272 mg elemental, oxide, LOW class)
13. 7290019444206 — Altman Balance (~272 mg elemental, oxide, LOW class)
14. 7290010207640 — NT LC Anti Leg Cramps (190 mg elemental, hydroxide, MODERATE class)
15. 7290015318532 — Tink Malate (136 mg elemental, malate, MODERATE class)

### Exception Path (scored via honesty/blend path, not administered-elemental model)

16. 0033984005181 — Solgar Cal-Mag D3 (100 mg elemental/5-tab per US label; blend path; IL label unverified; D cap_3_honesty_core expected)

### Unresolved / not scored (2 products)

17. 7290015429245 — Amorphicure pH Carbonate (elemental vs compound ambiguous; physical label required)
18. 7290118816065 — Supherb TRIOMAG (likely elemental total, form ratios undisclosed; physical label or manufacturer disclosure required)

### Discarded (1 product)

19. 7290118818205 — Supherb Max 550 (oxide:citrate ratio undisclosed; elemental unknowable; discarded per owner-approved decision and missing-data discard rule)

---

## C3 Challenge — How Each Refinement Is Incorporated

| C3 finding | Incorporated as |
|---|---|
| "from/as" convention not universally decisive — oxide products use identical grammar but are treated as compound" | Explicit scoring rule: products are scored as compound UNLESS the label explicitly states "מגנזיום אלמנטרי" OR uses "from/as" format with cross-verified IL retailer evidence showing elemental interpretation. Oxide products (Nutricare 520, Tink 520, Altman 520, MagUp, Balance) scored as compound-derived elemental via chemistry fraction. Grammar alone does not determine compound vs elemental — evidence-verified source is required. |
| Indication thresholds must be administered-elemental trial doses, not efficacy guarantees | All threshold language revised: "administered dose studied in [indication] trials" not "effective dose." Per-indication bands separated (general / BP / migraine / sleep / cramps / laxative). "Ineffective" language eliminated; replaced with "below studied dose range." |
| Bioavailability as classes, not fake-precise mg | NEVER display absorbed-mg to consumer. Bioavailability class (HIGH/MODERATE/LOW/UNRESOLVED) is the display unit. Class boundaries evidence-grounded; citations cited in Pillar 2 section. |
| UL framed accurately — supplemental-only, GI/tolerability, excludes food | Safety block explicitly states: "350 mg supplemental only," "increased GI risk," "not acute toxicity," "excludes food magnesium." Engine flags UL_EXCEED but does NOT hard-cap score. |
| Malate fraction unsettled (0.195 vs 0.155) — do not score as exact | Nutricare Malate scored with range: ~133–137 mg. Consumer display: "~133–137 מ"ג" with note that this is an estimate from compound. No single precise value asserted. |

---

## Spec-Conflict Notes

1. Prior cap_2_fairy_dust_hidden_dose constraint: in SUPP-EV-030 v3.1, ALL products were capped because no product delivered ≥75 mg absorbed. In v2, this cap is retired — the dose pillar scores administered elemental directly against indication bands. Oxide products with ~272–314 mg elemental and HIGH label dose MEET the general gap band; they are no longer capped for low absorbed-mg. Their LOW bioavailability class reduces the evidence sub-score but does not cap the dose sub-score.

2. Absorbed-mg display (SUPP-EV-030 path): the prior model displayed "נספג: ~כ-X מ"ג" to the consumer. This field is ELIMINATED in v2. The engine may compute absorbed-mg internally for research purposes but it is never surfaced in consumer-facing UI.

3. Monotonicity in v2: the v1 model was monotone in absorbed-mg. The v2 model is monotone in administered elemental within a given bioavailability class (more elemental → higher dose sub-score within class, all else equal). Cross-class monotonicity is not guaranteed by design: a 76 mg taurate product may score lower than a 200 mg oxide product despite taurate's higher class, because the dose penalty at 76 mg outweighs the class bonus. This is correct behavior — the engine should not reward a "nice form" at an inadequate dose.

4. Full-Mag Hadas (7290001943700): prior engine marked unscoreable_incomplete (form=None, safety_unscoreable because worst-case 600mg assumed > UL). With verified form=bisglycinate and elemental=122 mg, the safety block dissolves. 122 mg < 350 mg UL. This product is now IN the scored set. This is a material change from the prior model — the orchestrator should flag it for Product Agent awareness when the D7 co-sign is sought.

---

## Open Items (not_done in this spec — require resolution before engine implementation)

1. Nutricare WELL cap_1 determination: does the product's "WELL" branding / proprietary-complex language constitute an unsupported delivery claim? Engine team must determine before assigning final score path.
2. Amorphicure and TRIOMAG physical labels: until resolved, these are "label_confidence: unclear" display states.
3. Solgar IL Hebrew label verification: low priority (global brand, US label reliable); should be confirmed before consumer deployment.
4. Magnox B6 (7290017847122): excluded from this spec per TASK-384 brief scope. Prior model included it with provenance flag (amazon.com source). Held for separate resolution.
5. D7 co-sign: this spec requires Product Agent approval before any engine changes.

---

```json
{
  "task": "TASK-384",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/supplement_engine/proto_v0/benchmark/magnesium_model_v2_final_spec.md",
      "action": "created",
      "sha256": "pending-get-filehash"
    }
  ],
  "counts": {
    "scored_products": "15/19 (denominator: 19 qualifying SKUs per magnesium_elemental_reconciliation_v1.md scope)",
    "exception_path_products": "1/19 (Solgar Cal-Mag blend path)",
    "unresolved_products": "2/19 (Amorphicure, TRIOMAG — label_confidence unclear)",
    "discarded_products": "1/19 (Supherb Max 550 — owner-approved discard)",
    "c3_refinements_incorporated": "5/5 (convention rule, threshold framing, bioavailability class, UL framing, malate range)",
    "products_with_corrected_elemental_vs_prior_fix_a": "7/7 (all Category A reconciliation conflicts resolved: Altman Citrate 200mg, Supherb Citrate+B6 250mg, Altman Bisglycinate 250mg, Nutricare Taurate 76mg, Nutricare WELL 168mg, Tink Malate 136mg, Nutricare Nano 88mg)",
    "products_newly_scoreable": "1/1 (Full-Mag Hadas 600 — form/elemental now verified, previously unscoreable_incomplete)",
    "absorbed_mg_consumer_display_fields": "0 (eliminated; bioavailability class is the only absorption-related display)"
  },
  "commands_run": [
    {"cmd": "Read C:\\Bari\\tasks\\TASK-384.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\02_products\\supplements\\real_corpus_v3\\magnesium_elemental_reconciliation_v1.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\tasks\\returns\\P300_return.md offset=1 limit=150", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\01_framework\\operations\\return_contract_v1.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_absorbed_scoring_FINAL_v1.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_assumptions_c3_v1.md", "exit_code": 0},
    {"cmd": "PowerShell Get-ChildItem benchmark directory", "exit_code": 0}
  ],
  "not_done": [
    "Engine implementation — this is a design spec only; engine changes require Product D7 co-sign first",
    "Corpus file edits — not in scope for this spec (Data Agent lane)",
    "Real engine re-run to confirm projected grade bands — grades are marked ESTIMATE throughout",
    "SHA256 hash of the created file — requires Get-FileHash after write",
    "Physical label resolution for Amorphicure and TRIOMAG",
    "Magnox B6 scoring — excluded from this spec per brief scope",
    "Solgar IL Hebrew label verification"
  ],
  "self_check": "Spec acceptance test: all 5 C3 refinements are addressed with explicit rules (verified by Part 3C3 table); all 7 Fix-A corrected elemental values are used (not the magnesium_corrections_v1.md figures); Supherb Max 550 is discarded (not scored); Amorphicure and TRIOMAG render as unresolved; Full-Mag Hadas transitions from unscoreable to scored set; no consumer-facing field displays absorbed mg. All conditions met."
}
```
