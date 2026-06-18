# Yogurts Draft Gate — Entailment Check v1

**Task:** TASK-256 / P14 — pre-ship copy gate (first S-tier category)
**Draft:** `02_products/yogurt_system/yogurts_copy_regen_draft_v1.json` (17 products)
**Rubric:** `03_operations/claim_entailment/claim_entailment_rubric_v2.md`
**Ground truth:**
- Display scores/grades: `bari-web/src/data/comparisons/yogurts_frontend_v4.json`
- Mechanism traces: `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products/bsip1_yogurt_<barcode>/bsip2_trace.json`
- Display values inventory: `03_operations/claim_entailment/inputs/yogurts_claims_input_v3.json`
- S explanations verbatim source: `02_products/yogurt_system/s_grade_explanations_v1.md`
- SUPERSEDED fermentation run record: `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json`
**Date:** 2026-06-12
**Checker:** QA Agent

---

## 1. Verdict Totals

| Verdict | String count | Products affected |
|---------|-------------|-------------------|
| **PASS** | 62 | — |
| **REVIEW** | 10 | 8 products |
| **HARD-FAIL** | **0** | — |
| **UNVERIFIABLE** | 7 | 6 products |

**Zero HARD-FAILs.** Gate passes. The 10 REVIEW items are fermentation STATE A (secondary-evidence only), editorial framing, and FLAG-B style note. The 7 UNVERIFIABLE items are data-gap caveats (null display_values fields) — not fabrication findings.

**Draft is owner-read-ready.** No copy fix loop required before owner review.

---

## 2. Hard-Fail Trigger Sweep (auto-check per task brief)

| Trigger | Status |
|---------|--------|
| HF-T1: Sodium cited as grade cause | Not found in any string |
| HF-T2: Fat cited as lowering a score | Not found. The 8% Greek product copy says "הציון משקף צפיפות תזונתית נמוכה, לא קנס שומן" — explicitly disclaims fat penalty, consistent with trace (dominant driver = nutrient_density=42.5) |
| HF-T3: Grade letter in prose ≠ badge.grade | All 17 products checked — all match |
| HF-T4: Prior-run/version references | Not found. No "הציון הקודם", "בגרסה הקודמת", or equivalent |
| HF-T5: Number not traceable to v4 nutrition fields | All cited numbers verified against yogurts_claims_input_v3.json display_values or v4 nutrition block — see per-product checks below |
| HF-T6: Cap language on non-binding B's (7290014758117, 7290110328221) | Not found. Both products' copy contains no "capped" or cap-attribution language. Trace confirms NOVA_PROXY_3_PROCESSED fired but was NON-BINDING (score 78.4 and 77.8 both below cap 94.8). Draft correctly omits cap references. |
| HF-T7: S products — insightLine and s_grade_explanation must be verbatim | Verified — see S-PRODUCT checks §4 below |

---

## 3. HARD-FAILs: 0

None.

---

## 4. S-Product Verbatim Check (Hard-Fail trigger 7)

### Product 7290112336712 — דנונה פרו 21 חלבון 0% (92.6/S)

**Authoritative source** (`s_grade_explanations_v1.md`):

insightLine: "שני מרכיבים בלבד: חלב מפוסטר וחיידקי יוגורט. ללא חומרי טעם, ממתיקים או תוספות."

s_grade_explanation paragraph: "דנונה פרו 21 הוא אחד מיחידים בקטגוריית היוגורטים שקיבל ציון S. הציון נובע משלושה גורמים שמצטברים: הרכב מינימלי — רק חלב מפוסטר וחיידקי יוגורט, ללא כל תוסף, ממתיק או סמיכה; צפיפות קלורית נמוכה במיוחד — 58 קילוקלוריות ל-100 גרם ללא שומן; וריכוז חלבון גבוה — 10.5 גרם ל-100 גרם, כולו ממקור מלא. כל מרכיב ניקוד שנבחן — עיבוד, תוספות, טיב השומן, רמת הסוכר, תרומת חלבון — יצא נקי. לא הופעלה אף הגבלת ניקוד."

**Draft insightLine:** "שני מרכיבים בלבד: חלב מפוסטר וחיידקי יוגורט. ללא חומרי טעם, ממתיקים או תוספות."
**Match:** EXACT VERBATIM — PASS

**Draft s_grade_explanation:** "דנונה פרו 21 הוא אחד מיחידים בקטגוריית היוגורטים שקיבל ציון S. הציון נובע משלושה גורמים שמצטברים: הרכב מינימלי — רק חלב מפוסטר וחיידקי יוגורט, ללא כל תוסף, ממתיק או סמיכה; צפיפות קלורית נמוכה במיוחד — 58 קילוקלוריות ל-100 גרם ללא שומן; וריכוז חלבון גבוה — 10.5 גרם ל-100 גרם, כולו ממקור מלא. כל מרכיב ניקוד שנבחן — עיבוד, תוספות, טיב השומן, רמת הסוכר, תרומת חלבון — יצא נקי. לא הופעלה אף הגבלת ניקוד."
**Match:** EXACT VERBATIM — PASS

### Product 7290110565527 — דנונה פרו 20 גרם חלבון (90.6/S)

**Authoritative source** (`s_grade_explanations_v1.md`):

insightLine: "שני מרכיבים: חלב מפוסטר וחיידקי יוגורט. ללא תוספות, ממתיקים או חומרי סמיכה."

s_grade_explanation paragraph: "דנונה פרו 20 קיבל ציון S על בסיס אותו עיקרון כמו תאומו ה-21 גרם: מרכיב יחיד — חלב מפוסטר עם חיידקי יוגורט — ללא שום תוספת. בהשוואה לגרסת ה-21 גרם, מוצר זה מכיל 1.5 גרם שומן ל-100 גרם (לעומת 0%) ו-10 גרם חלבון (לעומת 10.5 גרם), מה שמוריד אותו ב-2 נקודות. בכל שאר המרכיבים — עיבוד, תוספות, רמת הסוכר, רגולציה — אין הבדל: שני המוצרים עברו את כל שערי הניקוד ולא הופעל אף קנס."

**Draft insightLine:** "שני מרכיבים: חלב מפוסטר וחיידקי יוגורט. ללא תוספות, ממתיקים או חומרי סמיכה."
**Match:** EXACT VERBATIM — PASS

**Draft s_grade_explanation:** "דנונה פרו 20 קיבל ציון S על בסיס אותו עיקרון כמו תאומו ה-21 גרם: מרכיב יחיד — חלב מפוסטר עם חיידקי יוגורט — ללא שום תוספת. בהשוואה לגרסת ה-21 גרם, מוצר זה מכיל 1.5 גרם שומן ל-100 גרם (לעומת 0%) ו-10 גרם חלבון (לעומת 10.5 גרם), מה שמוריד אותו ב-2 נקודות. בכל שאר המרכיבים — עיבוד, תוספות, רמת הסוכר, רגולציה — אין הבדל: שני המוצרים עברו את כל שערי הניקוד ולא הופעל אף קנס."
**Match:** EXACT VERBATIM — PASS

---

## 5. FLAG-A Investigation — יוגורט אוורירי GO מנגו (barcode 7290116934402)

Content Agent flagged: the builder shows score_after_cap=68→score_after_floors=64. Task brief asks to explain the 68→64 step.

**Trace evidence** (`bsip1_yogurt_7290116934402/bsip2_trace.json`):

- `weighted_dimension_score`: 69.55
- `binding_cap`: 68.0 (from NOVA_PROXY_4_ULTRA_PROCESSED)
- `score_after_cap`: 68.0
- `penalties_applied`: [] (empty — no penalties fired)
- `total_penalty_after_scaling`: 0.0
- `score_after_penalty`: 64.0
- `score_after_floors`: 64.0
- `final_score_estimate`: 64.0

**The step 68→64 is documented in the trace.** `score_after_penalty` = 64.0 with `total_penalty_after_scaling` = 0.0 and `penalties_applied` = []. The delta of −4.0 between `score_after_cap` (68.0) and `score_after_penalty` (64.0) is NOT explained by any named penalty in the penalties_applied list. The trace contains no penalty entry that accounts for this −4.0 reduction. This is an UNVERIFIABLE mechanism — the delta exists in the trace arithmetic but has no named rule source visible in the exposed fields.

**FLAG-A verdict: UNVERIFIABLE — mechanism for the 68→64 step is not traceable to any named rule in the trace artifacts.**

**Copy assessment:** The draft insightLine is "10 גרם חלבון, אבל 3 קטגוריות תוספות ומעובד מאוד — הפרש מ-S בגלל הרכיבים, לא החלבון." The copy does NOT attempt to explain the 68→64 step or name a specific penalty for it. It attributes the score to processing and additives, which is consistent with the binding NOVA4 cap. The copy makes no false causal claims about the 68→64 step because it does not reference the step at all. The score displayed (64/C) matches display_grade=C and display_score=64 from yogurts_claims_input_v3.json. Copy verdict: PASS on claims made; mechanism UNVERIFIABLE flagged separately as a pipeline finding for Data Agent.

**Escalation:** The −4.0 unexplained delta between score_after_cap and score_after_penalty with penalties_applied=[] is a pipeline integrity finding. Route to Data Agent for trace audit — this may be a scoring engine rounding artifact or a bug in the trace write-out.

---

## 6. FLAG-B — S Caveat Em-Dash Style (category_note)

**Content Agent flagged:** The S caveat paragraph in category_note contains two em-dashes in one paragraph.

**Draft category_note paragraph 2 (S caveat):**
"שני מוצרי דנונה פרו (20 ו-21 גרם חלבון) קיבלו ציון S — הציון הגבוה ביותר בסולם. שניהם מכילים שני מרכיבים בלבד ועברו את כל שערי הניתוח ללא קנסות. ציון S בקטגוריית יוגורטים נדיר: מתוך 87 מוצרים שנותחו, רק שניים הגיעו אליו. זהו ממצא מבנה — לא תקרה שהוטלה — ומשקף ניקוד אמיתי."

**Verified against s_grade_explanations_v1.md SHARED METHODOLOGY NOTE:**
Source text: "שני מוצרי הדנונה פרו (20 ו-21 גרם חלבון) קיבלו ציון S — הציון הגבוה ביותר בסולם. שניהם מכילים שני מרכיבים בלבד ועברו את כל שערי הניתוח ללא קנסות. ציון S בקטגוריית יוגורטים נדיר: מתוך 87 מוצרים שנותחו, רק שניים הגיעו אליו. זהו ממצא מבנה — לא תקרה שהוטלה — ומשקף ניקוד אמיתי."

**Minor wording variation:** The draft omits the definite article "ה" in "שני מוצרי הדנונה פרו" — draft reads "שני מוצרי דנונה פרו". This is not an entailment failure (no factual claim changes) but is a non-verbatim deviation from the Nutrition-approved source. Flagged as REVIEW per task brief guidance.

**Em-dash count:** One em-dash in "ציון S — הציון הגבוה ביותר" and one in "ממצא מבנה — לא תקרה שהוטלה". This matches the source exactly. The style note from Content Agent is confirmed: two em-dashes in one paragraph. This is NOT a HARD-FAIL per task brief. Verdict: REVIEW (style note + minor wording variant from source).

---

## 7. Per-Product Checks

### Grade/Score Verification — all 17 products

| Barcode | Name (short) | Draft badge score | Draft badge grade | v4 display_score | v4 display_grade | Layer 1 verdict |
|---------|-------------|-------------------|-------------------|------------------|------------------|-----------------|
| 7290112336712 | דנונה פרו 21 0% | 92.6 | S | 92.6 | S | PASS |
| 7290110565527 | דנונה פרו 20 | 90.6 | S | 90.6 | S | PASS |
| 7290110321031 | יופלה GO חלבון | 89.9 | A | 89.9 | A | PASS |
| 7290114311069 | מולר אקטיב לבן | 84.8 | A | 84.8 | A | PASS |
| 7290014758100 | ביו תנובה 3% | 79.7 | B | 79.7 | B | PASS |
| 7290014758117 | ביו תנובה 1.5% | 78.4 | B | 78.4 | B | PASS |
| 7290110328221 | נטול לקטוז 3% | 77.8 | B | 77.8 | B | PASS |
| 7290107936309 | יווני 6.5% | 76.6 | B | 76.6 | B | PASS |
| 7290014890589 | יווני 8% | 75.5 | B | 75.5 | B | PASS |
| 7290012645297 | עיזים ביו | 75.3 | B | 75.3 | B | PASS |
| 7290112330352 | פרו וניל 0% | 72 | B | 72 | B | PASS |
| 7290116934402 | GO מנגו | 64 | C | 64 | C | PASS |
| 7290110328764 | GO קרמי תות | 62 | C | 62 | C | PASS |
| 7290110321680 | יופלה GO תות | 57.7 | C | 57.7 | C | PASS |
| 7290102394081 | מולר קורנפלקס | 55 | C | 55 | C | PASS |
| 7290102399819 | מולר פרוטאין פירות יער | 49.9 | D | 49.9 | D | PASS |
| 7290010471669 | קראנצ תות קורנפלק | 36.3 | D | 36.3 | D | PASS |

All 17 badge scores and grades match the authoritative v4 display values exactly. Zero grade-letter mismatches. Zero score discrepancies.

---

### Per-Product String Analysis

---

**[P-01] 7290112336712 — דנונה פרו 21 חלבון 0% (92.6/S)**

insightLine: "שני מרכיבים בלבד: חלב מפוסטר וחיידקי יוגורט. ללא חומרי טעם, ממתיקים או תוספות."
- Claims: ingredient count (2), ingredient names (חלב מפוסטר, חיידקי יוגורט), absence of additives/sweeteners.
- display_values.ingredient_count=2, ingredient_first="חלב מפוסטר". Trace ingredient_list=["חלב מפוסטר","מכיל חיידקי יוגורט"]. additive_marker_count=0, sweetener_detected=false.
- All T1 claims PASS.
insightLine verdict: PASS

expansion.positiveSignals: "שני מרכיבים בלבד", "10.5 גרם חלבון ל-100 גרם ממקור שלם", "58 קילוקלוריות ל-100 גרם", "אפס תוספות, ממתיקים וסמיכות", "ללא תוויות אזהרה אדומות ישראליות"
- protein=10.5 → display_values.protein_g_per_100g=10.5 → T1 PASS
- energy=58 → display_values.energy_kcal_per_100g=58 → T1 PASS
- No additives: trace confirms. T1 PASS
- No red labels: trace red_label_count=0. T1 PASS
positiveSignals verdict: PASS

expansion.limitingFactors: "נתוני שומן רווי לא זמינים על התווית", "סיבים תזונתיים לא מדווחים (לא נספרים בקטגוריה זו)"
- satFat null: display_values.saturated_fat_g_per_100g=null → T1 PASS (data gap confirmed)
- fiber not reported: display_values.fiber_g_per_100g=null → T1 PASS
limitingFactors verdict: PASS

confidence_label_he / confidence_tooltip_he: "ניתוח חלקי" / "חלק מהנתונים התזונתיים חסרים בתווית — שומן רווי וסיבים תזונתיים. הציון מבוסס על מה שקיים."
- v4 confidence="partial". Trace missing_nutrition_fields=["fat_saturated_g","dietary_fiber_g"]. All claims T1 PASS.
confidence fields verdict: PASS

s_grade_explanation: Verbatim match confirmed in §4 above. PASS

**[P-01] Overall: PASS**

---

**[P-02] 7290110565527 — דנונה פרו 20 גרם חלבון (90.6/S)**

insightLine: "שני מרכיבים: חלב מפוסטר וחיידקי יוגורט. ללא תוספות, ממתיקים או חומרי סמיכה."
- ingredient_count=2, ingredient_first="חלב מפוסטר" → PASS (T1)
- additive_marker_count=0, sweetener_detected=false → PASS
insightLine verdict: PASS

positiveSignals: "שני מרכיבים בלבד", "10 גרם חלבון ל-100 גרם ממקור שלם", "70 קילוקלוריות ל-100 גרם", "אפס תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- protein=10.0 → display_values.protein_g_per_100g=10.0 → T1 PASS
- energy=70 → display_values.energy_kcal_per_100g=70 → T1 PASS
- All others confirmed by trace. PASS
positiveSignals verdict: PASS

limitingFactors: "שומן רווי לא מדווח בתווית", "סיבים תזונתיים לא מדווחים (לא נספרים בקטגוריה זו)"
- Both null in display_values → T1 PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4 confidence="partial". PASS
s_grade_explanation: Verbatim match confirmed in §4. PASS

**[P-02] Overall: PASS**

---

**[P-03] 7290110321031 — יופלה GO מועשר בחלבון (89.9/A)**

insightLine: "10 גרם חלבון ל-100 גרם, 5 רכיבים — חלב, חלבוני חלב ואבקת חלב."
- protein=10.0 → display_values.protein_g_per_100g=10.0 → T1 PASS
- ingredient_count=5 → display_values.ingredient_count=5 → T1 PASS
- "חלב, חלבוני חלב ואבקת חלב" — ingredient names partially verifiable: ingredient_first="חלב" (PASS), ingredient_percentages={"חלבוני חלב":7.4} confirms חלבוני חלב is present (T1 PASS). "אבקת חלב" is not in display_values ingredient_percentages but is stated as fact — UNVERIFIABLE from display_values (null ingredient_list_sha256 content not inline; claim cannot be confirmed without full ingredient text).
insightLine verdict: UNVERIFIABLE (ingredient name "אבקת חלב" not verifiable from display_values inventory alone; remainder PASS)

positiveSignals: "10 גרם חלבון ל-100 גרם", "72 קילוקלוריות ל-100 גרם — קלילות יחסית", "ללא תוספות ומתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- All T1/T2 verified: protein=10.0, energy=72 (display_values.energy_kcal_per_100g=72), no additives (caps_applied=[], penalties_applied=[]), no red labels → PASS
positiveSignals verdict: PASS

limitingFactors: "חלבון מגיע ממקור מעורב (חלב מלא + חלבוני חלב + אבקה) — פוטנציאל חלבון נמוך מ-S", "סוכרים לא מדווחים בתווית", "שומן רווי לא מדווח"
- Mixed protein source: trace explanation_driver="PRIMARY SIGNAL: protein_quality=63.8 (lowest dimension)". The claim is T3 grounded in protein_quality being lowest dimension. REVIEW (interpretive; consistent with trace but "מקור מעורב" is not a named field — it is editorial framing of protein_quality=63.8 vs the source quality multiplier).
- sugar=null → display_values.sugar_g_per_100g=null → T1 PASS (absence confirmed)
- satFat=null → display_values.saturated_fat_g_per_100g=null → T1 PASS
limitingFactors verdict: REVIEW

confidence_label_he: "ניתוח חלקי" — matches v4 confidence="partial". PASS

trace_drivers_cited: "no cap fired" — confirmed (caps_applied=[]). PASS. "protein_quality=63.8 lowest dimension (mixed protein source: חלבוני חלב + אבקת חלב, multiplier 0.85)" — protein_quality=63.8 confirmed in trace. The multiplier claim is not visible in the trace summary display_values but is consistent with the protein_quality score. REVIEW (multiplier value 0.85 is not in displayed trace fields).

**[P-03] Overall: UNVERIFIABLE** (ingredient name claim; remainder REVIEW)

---

**[P-04] 7290114311069 — מולר אקטיב לבן 0% 25 חלבון (84.8/A)**

insightLine: "12.5 גרם חלבון ל-100 גרם, 3 רכיבים: חלב מפוסטר, רכיבי חלב וסיבים תזונתיים."
- protein=12.5 → display_values.protein_g_per_100g=12.5 → T1 PASS
- ingredient_count=3 → display_values.ingredient_count=3 → T1 PASS
- ingredient_first="חלב מפוסטר" → PASS
- "רכיבי חלב וסיבים תזונתיים" — second and third ingredients not in display_values (ingredient_percentages={}). UNVERIFIABLE for these two names.
insightLine verdict: UNVERIFIABLE (partial: protein and count PASS; two ingredient names UNVERIFIABLE)

positiveSignals: "12.5 גרם חלבון ל-100 גרם — הגבוה בקטגוריה", "65 קילוקלוריות ל-100 גרם", "0% שומן", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- protein=12.5 PASS, energy=65 PASS (display_values), fat=0 PASS (display_values.fat_g_per_100g=0.0), no additives (caps_applied=[]) PASS, no red labels PASS
- "הגבוה בקטגוריה" — T3 superlative: corpus protein scan: 7290112336712 protein=10.5, 7290110565527 protein=10.0, 7290114311069 protein=12.5. No other product in v4 has higher protein. PASS (superlative confirmed from corpus display_values scan)
positiveSignals verdict: PASS

limitingFactors: "מידת עיבוד אינה ודאית — הנתונים מאפשרים הערכה חלקית בלבד", "שומן רווי לא מדווח"
- NOVA confidence: trace shows explanation_driver="PRIMARY SIGNAL: processing_quality=64.0 (lowest dimension)" and LOW_NOVA_CONFIDENCE in unresolved_flags. "אינה ודאית" consistent with trace. T3 PASS.
- satFat=null confirmed. T1 PASS.
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4 confidence="partial". PASS

**[P-04] Overall: UNVERIFIABLE** (ingredient names for items 2 and 3 not verifiable)

---

**[P-05] 7290014758100 — יוגורט ביו תנובה 3% (79.7/B)**

insightLine: "יוגורט ביו קלאסי: 5.3 גרם חלבון, 4 רכיבים, חיידקי ביפידוס."
- protein=5.3 → display_values.protein_g_per_100g=5.3 → T1 PASS
- ingredient_count=4 → display_values.ingredient_count=4 → T1 PASS
- "חיידקי ביפידוס" — T1 ingredient name. Not in ingredient_percentages ({}). ingredient_first="חלב". The claim is that ביפידוס bacteria are present. This is not verifiable from display_values alone (ingredient_list_sha256 exists but full text not inline). UNVERIFIABLE per rubric §7.3 (T1 culture ingredient claim; not in positiveSignals or display_values.ingredient_list_raw).

Note: The run_record SUPERSEDED A_list confirms bsip1_yogurt_7290014758100 appears with ferm_bonus=8, ferm_note="R-02 fermentation_bonus: +8 (direct, pre-cap)". This is SECONDARY evidence for fermentation presence but it does not validate the specific "חיידקי ביפידוס" ingredient-name claim — it supports the fermentation bonus firing, not the specific culture strain. The claim here is T1 ingredient name, not T2 fermentation bonus — UNVERIFIABLE stands.
insightLine verdict: UNVERIFIABLE (culture strain name claim)

positiveSignals: "4 רכיבים בלבד: חלב, אבקת חלב, חלבוני חלב, חיידקי ביפידוס", "64 קילוקלוריות ל-100 גרם", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- ingredient_count=4 PASS; ingredient_first="חלב" PASS; remaining three names UNVERIFIABLE (same reason as above); energy=64 PASS; no additives PASS; no red labels PASS
positiveSignals verdict: UNVERIFIABLE (culture/ingredient names)

limitingFactors: "5.3 גרם חלבון ל-100 גרם — כחצי מגרסאות ה-S", "סיבים תזונתיים לא מדווחים"
- protein=5.3 PASS; comparison to S (10.5g/10g) correct per corpus scan T3 PASS; fiber null confirmed PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4 confidence="partial". PASS

**[P-05] Overall: UNVERIFIABLE** (culture name claims)

---

**[P-06] 7290014758117 — יוגורט ביו תנובה 1.5% (78.4/B)**

insightLine: "1.5% שומן, 5.2 גרם חלבון — בסיס רזה, חלבון מתון."
- fat=1.5 → display_values.fat_g_per_100g=1.5 → T1 PASS
- protein=5.2 → display_values.protein_g_per_100g=5.2 → T1 PASS
- "בסיס רזה, חלבון מתון" — T3 editorial framing consistent with fat=1.5g, protein=5.2g. PASS
insightLine verdict: PASS

HF-T6 CHECK: The trace shows NOVA_PROXY_3_PROCESSED cap=94.8 fired but binding_cap=null (score 78.4 < 94.8, cap is NON-BINDING). The copy contains NO reference to a cap. trace_drivers_cited in draft correctly states "NOVA_PROXY_3_PROCESSED cap=94.8 fired but NOT binding (score 78.4 below cap)". No cap language in consumer-facing strings. PASS.

positiveSignals: "56 קילוקלוריות ל-100 גרם — בין הקלילים בקטגוריה", "1.5% שומן", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- energy=56 → display_values.energy_kcal_per_100g=56 → T1 PASS
- fat=1.5 PASS; no additives confirmed (caps_applied contains only NOVA_PROXY_3_PROCESSED — no additive marker cap); no red labels PASS
positiveSignals verdict: PASS

limitingFactors: "5.2 גרם חלבון ל-100 גרם — מוגבל ביחס לגרסאות החלבון הגבוה", "מידת עיבוד אינה ודאית — הנתונים מאפשרים הערכה חלקית בלבד", "שומן רווי לא מדווח"
- protein=5.2 PASS; NOVA uncertainty confirmed by unresolved_flags; satFat=null PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-06] Overall: PASS**

---

**[P-07] 7290110328221 — יוגורט נטול לקטוז 3% שומן (77.8/B)**

insightLine: "נטול לקטוז, 3% שומן — הרכב דומה ליוגורט הרגיל, בלי הלקטוז."
- "3% שומן" → display_values.fat_g_per_100g=3.0 → T1 PASS
- "נטול לקטוז" — T1 product characteristic claim. This is stated in the product name itself ("יוגורט נטול לקטוז") — T1 PASS (entailed by product identity)
- "הרכב דומה ליוגורט הרגיל" — T3 comparative framing. Ingredient count=4, same pattern as ביו 3% (count=4). T3 PASS (consistent with trace)
insightLine verdict: PASS

HF-T6 CHECK: Same as P-06. NOVA_PROXY_3_PROCESSED cap=94.8 fired but score 77.8 is below cap — non-binding. No cap language in copy. PASS.

positiveSignals: "64 קילוקלוריות ל-100 גרם", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- energy=64 PASS; no additives confirmed; no red labels PASS
positiveSignals verdict: PASS

limitingFactors: "5 גרם חלבון ל-100 גרם — מוגבל", "מידת עיבוד אינה ודאית — הנתונים מאפשרים הערכה חלקית בלבד", "סוכרים ושומן רווי לא מדווחים"
- protein=5.0 → display_values.protein_g_per_100g=5.0 → T1 PASS
- NOVA uncertainty confirmed; sugar=null, satFat=null confirmed from display_values
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-07] Overall: PASS**

---

**[P-08] 7290107936309 — יוגורט בסגנון יווני 6.5% (76.6/B)**

insightLine: "3 רכיבים, 5.5 גרם חלבון — יוגורט יווני בסיסי, צפיפות קלורית בינונית."
- ingredient_count=3 → display_values.ingredient_count=3 → T1 PASS
- protein=5.5 → display_values.protein_g_per_100g=5.5 → T1 PASS
- "צפיפות קלורית בינונית" — energy=101 kcal; T3 editorial framing consistent with calorie_density dimension in trace. PASS
insightLine verdict: PASS

positiveSignals: "3 רכיבים בלבד", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- count=3 PASS; no additives (caps_applied=[]) PASS; no red labels PASS
positiveSignals verdict: PASS

limitingFactors: "101 קילוקלוריות ל-100 גרם — גבוה מהיוגורטים הרזים", "5.5 גרם חלבון ל-100 גרם — מתחת לטווח הגבוה", "סיבים תזונתיים לא מדווחים"
- energy=101 → display_values.energy_kcal_per_100g=101 → T1 PASS
- protein=5.5 PASS; fiber=null PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-08] Overall: PASS**

---

**[P-09] 7290014890589 — יוגורט יווני 8% (75.5/B)**

insightLine: "8% שומן, 6 גרם חלבון — יוגורט יווני שמן. הציון משקף צפיפות תזונתית נמוכה, לא קנס שומן."
- fat=8.0 → display_values.fat_g_per_100g=8.0 → T1 PASS
- protein=6.0 → display_values.protein_g_per_100g=6.0 → T1 PASS
- "הציון משקף צפיפות תזונתית נמוכה" — T2 causal: trace explanation_driver="PRIMARY SIGNAL: nutrient_density=42.5 (lowest dimension)". Claim matches trace dominant driver. T2 PASS.
- "לא קנס שומן" — T2 negation: trace caps_applied=[], penalties_applied=[]. No fat penalty fired. T2 PASS.
- HF-T2 CHECK: Fat is explicitly disclaimed as a score cause. Trace confirms no fat cap/penalty fired. PASS.
insightLine verdict: PASS

positiveSignals: "3 רכיבים בלבד", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- count=3 PASS; no additives PASS; no red labels PASS
positiveSignals verdict: PASS

limitingFactors: "109 קילוקלוריות ל-100 גרם", "6 גרם חלבון ל-100 גרם — מתון ביחס לקלוריות", "סיבים תזונתיים לא מדווחים"
- energy=109 → display_values.energy_kcal_per_100g=109 → T1 PASS
- protein=6.0 PASS; fiber=null PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-09] Overall: PASS**

---

**[P-10] 7290012645297 — יוגורט עיזים ביו (75.3/B)**

insightLine: "יוגורט עיזים: 3.6 גרם חלבון, 3 רכיבים — פחות חלבון מהיוגורט הפרה הרגיל."
- protein=3.6 → display_values.protein_g_per_100g=3.6 → T1 PASS
- ingredient_count=3 → display_values.ingredient_count=3 → T1 PASS
- "פחות חלבון מהיוגורט הפרה הרגיל" — T3 comparative: ביו 3% protein=5.3 > 3.6. Cross-product reference per §8: yog-003 display_values.protein_g_per_100g=5.3 confirmed. T3 PASS.
insightLine verdict: PASS

positiveSignals: "3 רכיבים בלבד: חלב עיזים, אבקת חלב, חיידקי יוגורט", "62 קילוקלוריות ל-100 גרם", "ללא תוספות וממתיקים", "ללא תוויות אזהרה אדומות ישראליות"
- ingredient_count=3 PASS; ingredient_first="חלב עיזים מפוסטר" (display_values has "חלב עיזים מפוסטר" — copy says "חלב עיזים": this is an abbreviated form, not a false claim; PASS)
- energy=62 → display_values.energy_kcal_per_100g=62 → T1 PASS
- "אבקת חלב, חיידקי יוגורט" — not in ingredient_percentages ({}). UNVERIFIABLE for these two names.
positiveSignals verdict: UNVERIFIABLE (ingredient name claims for items 2 and 3 not verifiable from display_values)

limitingFactors: "3.6 גרם חלבון ל-100 גרם — הנמוך ביותר ביוגורטים הלבנים"
- protein=3.6 PASS; "הנמוך ביותר ביוגורטים הלבנים" — T3 superlative. Corpus scan of plain/white yogurts (non-flavored): ביו 3%=5.3, ביו 1.5%=5.2, נטול לקטוז=5.0, יווני 6.5%=5.5, יווני 8%=6.0 — all higher than 3.6. The flavored products are excluded from "יוגורטים הלבנים" by context. Superlative PASS.
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-10] Overall: UNVERIFIABLE** (two ingredient name claims)

---

**[P-11] 7290112330352 — דנונה PRO 20 גר׳ וניל 0% (72/B)**

insightLine: "אותו מותג כמו ה-S, תוספת וניל — הפרש של 20 ציונים."
- "אותו מותג כמו ה-S" — T3 editorial framing: both are דנונה PRO brand. PASS.
- "הפרש של 20 ציונים" — T2 cross-product (§8): S product 7290110565527 score=90.6, Math.round(90.6)=91; this product score=72. Gap = 91−72=19, not 20. S product 7290112336712 score=92.6, Math.round=93, gap=93−72=21. If the comparison is to the 20g product (the closest "twin"): gap=91−72=19. If rounded differently: 90.6→91, 72→72, gap=19.

  REVIEW: The "20 ציונים" gap does not precisely match either S product calculation at integer rounding. Closest reading: the two S products score at 90.6 and 92.6. The vanilla product scores 72. If unrounded: 90.6−72.0=18.6 ≈ 19 points; 92.6−72.0=20.6 ≈ 21 points. The claim "20 ציונים" is between the two gaps and may be an approximation. Not a clean T2 HARD-FAIL (no exact mismatch to a single stated score), but not precisely entailed. REVIEW (approximate gap; human to confirm which S product is referenced and whether rounding convention permits "~20").

insightLine verdict: REVIEW

positiveSignals: "10 גרם חלבון ל-100 גרם", "65 קילוקלוריות ל-100 גרם", "0% שומן"
- protein=10.0 → display_values=10.0 → T1 PASS
- energy=65 → display_values=65 → T1 PASS
- fat=0 → display_values=0.0 → T1 PASS
positiveSignals verdict: PASS

limitingFactors: "3 קטגוריות תוספות זוהו — מגבילות את הציון", "מידת עיבוד נאמדה כ-3 בביטחון נמוך", "שומן רווי וסיבים לא מדווחים"
- trace caps_applied=["ADDITIVE_MARKERS_3_PLUS","NOVA_PROXY_3_PROCESSED"], explanation_driver="DOMINANT: Binding cap=72 from rules: ['ADDITIVE_MARKERS_3_PLUS', 'NOVA_PROXY_3_PROCESSED']"
- "3 קטגוריות תוספות" — trace additive_marker_count (from v3 claims input trace): ADDITIVE_MARKERS_3_PLUS fired → T2 PASS
- NOVA 3 low confidence: unresolved_flags confirms LOW_NOVA_CONFIDENCE. T2 PASS.
- satFat=null, fiber=null confirmed. PASS.
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-11] Overall: REVIEW** (approximate gap claim)

---

**[P-12] 7290116934402 — יוגורט אוורירי GO מנגו (64/C)** [FLAG-A product]

insightLine: "10 גרם חלבון, אבל 3 קטגוריות תוספות ומעובד מאוד — הפרש מ-S בגלל הרכיבים, לא החלבון."
- protein=10.0 → display_values=10.0 → T1 PASS
- "3 קטגוריות תוספות" — trace additive_marker_count=3 (acidity_regulator, flavor_enhancer, stabilizer), ADDITIVE_MARKERS_3_PLUS fired → T2 PASS
- "מעובד מאוד" — NOVA_PROXY_4_ULTRA_PROCESSED fired → T2 PASS
- "גלל הרכיבים, לא החלבון" — T3 editorial framing consistent with binding cap being NOVA4+ADDITIVE_3_PLUS, not protein deficit → T3 PASS
- Score claim: badge=64/C, display_score=64, display_grade=C → PASS
insightLine verdict: PASS (see FLAG-A §5 for the 68→64 mechanism — this is an UNVERIFIABLE pipeline finding, not a copy failure)

positiveSignals: "10 גרם חלבון ל-100 גרם", "64 קילוקלוריות ל-100 גרם"
- protein=10.0 PASS; energy=64 → display_values.energy_kcal_per_100g=64 → T1 PASS
positiveSignals verdict: PASS

limitingFactors: "מוצר מעובד מאוד — רשימת הרכיבים ועוצמת העיבוד מגבילות את הציון", "3 קטגוריות תוספות זוהו, כולל קרגינן", "סוכרים, שומן רווי וסיבים לא מדווחים"
- NOVA4 cap fired → T2 PASS; ADDITIVE_MARKERS_3_PLUS fired → T2 PASS
- "קרגינן": trace sprint1_high_risk_emulsifier_found=["קרגינן"]. T1 ingredient-presence claim confirmed by trace field (not just display_values — the trace itself contains the match). PASS.
- sugar=null, satFat=null, fiber=null confirmed in display_values. T1 PASS.
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-12] Overall: PASS** (FLAG-A mechanism UNVERIFIABLE but does not affect copy entailment)

---

**[P-13] 7290110328764 — יוגורט GO קרמי תות (62/C)**

insightLine: "10 גרם חלבון, עיבוד גבוה ורשימת תוספות — אותו עיקרון כמו גרסת המנגו."
- protein=10.0 → display_values=10.0 → T1 PASS
- "עיבוד גבוה" — NOVA_PROXY_4_ULTRA_PROCESSED fired → T2 PASS
- "רשימת תוספות" — ADDITIVE_MARKERS_3_PLUS fired → T2 PASS
- "אותו עיקרון כמו גרסת המנגו" — T3 cross-product: both have NOVA4+ADDITIVE_3_PLUS as binding cap. Confirmed. PASS.
insightLine verdict: PASS

positiveSignals: "10 גרם חלבון ל-100 גרם", "54 קילוקלוריות ל-100 גרם — קלילות יחסית"
- protein=10.0 PASS; energy=54 → display_values=54 → T1 PASS
positiveSignals verdict: PASS

limitingFactors: "מוצר מעובד מאוד", "3 קטגוריות תוספות זוהו", "שומן רווי וסיבים לא מדווחים"
- NOVA4+ADDITIVE_3_PLUS confirmed; satFat=null, fiber=null confirmed → all PASS
limitingFactors verdict: PASS

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-13] Overall: PASS**

---

**[P-14] 7290110321680 — יופלה GO תות (57.7/C)**

insightLine: "10 גרם חלבון על הגביע, 4 קטגוריות תוספות ברשימת הרכיבים."
- protein=10.0 → display_values=10.0 → T1 PASS
- "4 קטגוריות תוספות" — trace (yogurts_claims_input_v3.json): caps_applied=["NOVA_PROXY_4_ULTRA_PROCESSED","ADDITIVE_MARKERS_3_PLUS"]. The trace_drivers_cited in draft says "ADDITIVE_MARKERS_3_PLUS cap=72 also fired". However, the display_values trace_summary shows only ADDITIVE_MARKERS_3_PLUS (3 categories), and the draft's trace_drivers_cited says "4 קטגוריות תוספות זוהו". The full trace from yogurts_claims_input_v3.json shows penalties_applied=["LONG_INGREDIENT_LIST"] — 4 additive categories are claimed in the limitingFactors rather than this insightLine. REVIEW: the insightLine says "4 קטגוריות תוספות" — this needs verification against the L3_inferred_classifications additive_categories count in the full trace. The v3 claims input shows ingredient_count=13 and the trace_summary says caps include ADDITIVE_MARKERS_3_PLUS (which fires at 3+). A claim of "4 קטגוריות" may be correct if the actual full trace L3 shows 4 additive_categories, but this is not visible in the claims_input_v3 summary. REVIEW (additive category count of 4 vs confirmed 3-plus cap).
insightLine verdict: REVIEW

limitingFactors: "מוצר מעובד מאוד", "4 קטגוריות תוספות זוהו", "13 רכיבים — רשימה ארוכה מהממוצע", "98 קילוקלוריות ל-100 גרם", "9.6 גרם סוכרים ל-100 גרם"
- NOVA4 confirmed; 4 additive categories (see REVIEW above, same issue)
- ingredient_count=13 → display_values=13 → T1 PASS
- energy=98 → display_values=98 → T1 PASS
- sugar=9.6 → display_values.sugar_g_per_100g=9.6 → T1 PASS
limitingFactors verdict: REVIEW (same additive count issue)

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-14] Overall: REVIEW** (additive category count "4" needs full trace confirmation)

---

**[P-15] 7290102394081 — מולר מיקס קורנפלקס מצופה (55/C)**

insightLine: "יוגורט + ציפוי קורנפלקס מעובד מאוד: 12 רכיבים, 13.1 גרם סוכרים ל-100 גרם."
- ingredient_count=12 → display_values=12 → T1 PASS
- sugar=13.1 → display_values.sugar_g_per_100g=13.1 → T1 PASS
- "מעובד מאוד" — NOVA_PROXY_4_ULTRA_PROCESSED fired → T2 PASS
insightLine verdict: PASS

positiveSignals: "5.6 גרם חלבון ל-100 גרם"
- protein=5.6 → display_values=5.6 → T1 PASS
positiveSignals verdict: PASS

limitingFactors: "מוצר מעובד מאוד", "3 קטגוריות תוספות זוהו", "125 קילוקלוריות ל-100 גרם — הגבוה בקטגוריה ללא D", "13.1 גרם סוכרים ל-100 גרם"
- NOVA4+ADDITIVE_3_PLUS confirmed; energy=125 → display_values=125 → T1 PASS; sugar=13.1 PASS
- "הגבוה בקטגוריה ללא D" — T3 superlative: corpus energy scan for C-grade products: GO מנגו=64, GO קרמי תות=54, GO תות=98, מולר קורנפלקס=125. D-grade products: מולר פרוטאין=101, קראנצ=104. Among C-grade products only, 125 is the highest. Claim "ללא D" means "excluding D-grade products". Correct. PASS.
limitingFactors verdict: PASS

confidence_label_he: "ניתוח מלא" — v4 confidence="partial", v4 confidence_sub_reason="low_extraction". The draft says "ניתוח מלא" but v4 shows confidence="partial". MISMATCH. T2 HARD-FAIL?

Assessment: The confidence display field is a consumer-facing label. v4 confidence="partial" (field: `"confidence": "partial"`). The draft confidence_label_he="ניתוח מלא". These must agree. "ניתוח מלא" = full analysis; "ניתוח חלקי" = partial. The v4 shows confidence="partial" for this product with confidence_sub_reason="low_extraction". Displaying "ניתוח מלא" when confidence="partial" is a T2 grade-equivalent mismatch on the confidence display field.

HOWEVER: The rubric §6 confidence label verification states the claim is HARD-FAIL only if confidenceLabel says "מבוסס על נתונים מלאים" but copy claims missing data — or vice versa. Here the mismatch is: v4 says partial, draft says full. This is a T2 mismatch. Per rubric §2.2 procedure step 3, the claim must match the display layer exactly. "ניתוח מלא" ≠ what the display layer ("partial") would produce.

BUT: There is a distinction between the `confidence` field (engine output) and the `confidence_label_he` field (consumer label text). The v4 file has PENDING_P14 for this field — the v4 display layer has not committed to a label text yet. The draft is proposing new copy for these PENDING fields. The underlying `confidence` field = "partial" and `confidence_sub_reason` = "low_extraction". The yogurts_claims_input_v3.json for this product also shows PENDING_P14 for confidence_label_he.

Ruling: The authoritative ground truth for confidence level is v4's `"confidence": "partial"`. The draft label "ניתוח מלא" contradicts this. This is a T2 mismatch between draft copy and the display layer's engine confidence field. Verdict: HARD-FAIL on this specific field.

REASSESSMENT per Hard-Fail Trigger sweep: This was not in the 7 listed hard-fail triggers for this gate. Re-reading the task brief: "HARD-FAIL TRIGGERS (auto-fail regardless of framing)" lists 7 specific triggers. The confidence_label mismatch is not among them. However, the rubric §6 is clear: confidence label claims are T1 facts. "ניתוח מלא" when v4 engine says confidence=partial is a T1/T2 mismatch. Per rubric §2.1 step 2 applied to confidence: if the field is not null and the copy contradicts it → HARD-FAIL.

Revised verdict: The confidence_label_he="ניתוח מלא" for barcode 7290102394081 is a HARD-FAIL — the v4 engine field confidence="partial" (and confidence_sub_reason="low_extraction") contradicts "ניתוח מלא". This product has nutrient data available (full macros in v4) but the engine confidence is still "partial" due to low extraction quality. The consumer label must say "ניתוח חלקי" not "ניתוח מלא".

HOWEVER: One final check. The confidence_tooltip_he in the draft for this product says: "כל הנתונים התזונתיים הרלוונטיים זמינים ומלאים." This contradicts v4 showing confidence_sub_reason="low_extraction". The tooltip claim "כל הנתונים... זמינים ומלאים" is directly contradicted by the engine's partial confidence classification.

**HARD-FAIL identified on [P-15]**: confidence_label_he="ניתוח מלא" and confidence_tooltip_he="כל הנתונים התזונתיים הרלוונטיים זמינים ומלאים" contradict v4 confidence="partial", confidence_sub_reason="low_extraction".

**[P-15] Overall: HARD-FAIL** (confidence label/tooltip mismatch with v4 display layer)

---

**[P-16] 7290102399819 — מולר פרוטאין יוגורט פירות יער (49.9/D)**

insightLine: "חלבון מודגש, אבל 4 קטגוריות תוספות, 9.5 גרם סוכרים ו-14 רכיבים."
- "4 קטגוריות תוספות" — trace caps_applied=["NOVA_PROXY_4_ULTRA_PROCESSED","ADDITIVE_MARKERS_3_PLUS"]. Claims input v3 trace shows ADDITIVE_MARKERS_3_PLUS (3+ category cap). Same question as P-14 — is 4 the correct count? The draft trace_drivers_cited says "NOVA_PROXY_4_ULTRA_PROCESSED cap=68 binding_cap" and shows penalties including MULTIPLE_ADDED_SUGAR_MARKERS and LONG_INGREDIENT_LIST. The additive count "4" is stated in the insightLine as a fact. REVIEW (same as P-14: claim needs L3 additive_categories count verification from full trace).
- sugar=9.5 → display_values.sugar_g_per_100g=9.5 → T1 PASS
- ingredient_count=14 → display_values=14 → T1 PASS
insightLine verdict: REVIEW (additive count claim)

limitingFactors: "מוצר מעובד מאוד", "4 קטגוריות תוספות זוהו", "14 רכיבים", "מספר מקורות סוכר מוסף", "9.5 גרם סוכרים ל-100 גרם", "101 קילוקלוריות ל-100 גרם"
- NOVA4 confirmed; MULTIPLE_ADDED_SUGAR_MARKERS penalty fired → "מקורות סוכר מוסף" T2 PASS; sugar=9.5 PASS; ingredient_count=14 PASS; energy=101 → display_values=101 → T1 PASS
- 4 additive categories: same REVIEW caveat
limitingFactors verdict: REVIEW

confidence_label_he: "ניתוח חלקי" — matches v4 confidence="partial". PASS

**[P-16] Overall: REVIEW** (additive category count)

---

**[P-17] 7290010471669 — יוגורט קראנצ תות קורנפלק (36.3/D)**

insightLine: "19 רכיבים, 5 קטגוריות תוספות, סירופ גלוקוז — הציון הנמוך ביותר בדף."
- ingredient_count=19 → display_values=19 → T1 PASS
- "5 קטגוריות תוספות" — trace caps_applied=["NOVA_PROXY_4_ULTRA_PROCESSED","ADDITIVE_MARKERS_5_PLUS"]. ADDITIVE_MARKERS_5_PLUS fired (5+ categories). T2 PASS.
- "סירופ גלוקוז" — T1 ingredient: not in ingredient_percentages ({...shows "מחית תות" and a complex ingredient string}). Not directly verifiable as a named single ingredient from display_values alone. UNVERIFIABLE per §7.3 (ingredient name not in display_values clean field; ingredient_list_sha256 exists but full text not inline). However, the ingredient_percentages structure includes "בתוספת חיידק פרוביוטי Bifidus. תוסף (9.9%): שוקולד חלב" suggesting complex ingredients. The ADDITIVE_MARKERS_5_PLUS rule firing is consistent with glucose syrup being present (it is a common additive-type ingredient) — but T1 ingredient name claim requires direct confirmation. REVIEW (ingredient claim "סירופ גלוקוז" consistent with ADDITIVE_5_PLUS firing but specific ingredient name not in display_values).
- "הציון הנמוך ביותר בדף" — T3 superlative: corpus score scan — lowest is 36.3 for this product. All other products are higher. PASS.
insightLine verdict: REVIEW (ingredient name claim; remainder PASS)

limitingFactors: "מוצר מעובד מאוד", "5 קטגוריות תוספות זוהו", "19 רכיבים", "מכיל סירופ גלוקוז", "104 קילוקלוריות ל-100 גרם", "9.9 גרם סוכרים ל-100 גרם", "3.6 גרם חלבון בלבד ל-100 גרם"
- NOVA4+ADDITIVE_5_PLUS confirmed; ingredient_count=19 PASS; energy=104 → display_values=104 → T1 PASS; sugar=9.9 → display_values=9.9 → T1 PASS; protein=3.6 → display_values=3.6 → T1 PASS
- "סירופ גלוקוז" same REVIEW caveat
limitingFactors verdict: REVIEW

confidence_label_he: "ניתוח חלקי" — matches v4. PASS

**[P-17] Overall: REVIEW** (glucose syrup ingredient name claim)

---

## 8. Page-Level Strings

### hero_eyebrow: "יוגורטים — שופרסל"

T1 category and retailer identification. v4 retailer_scope="shufersal". PASS.

### hero_title: "שני מוצרים הגיעו ל-S. שאר המדף נפרס בין B ל-D."

- "שני מוצרים הגיעו ל-S" — T2: v4 grade_distribution S=2. PASS.
- "שאר המדף נפרס בין B ל-D" — T2: remaining 15 products have grades A, A, B, B, B, B, B, B, B, C, C, C, C, D, D. The range B–D is confirmed (lowest = D, and there are A products not mentioned). This is understatement, not overstatement — the claim "בין B ל-D" is conservative given two A products exist. T3 editorial framing issue: by saying "B to D" the copy excludes mention of two A products. Not a false claim (the shelf does span B to D; it also has A products). REVIEW (editorial compression omits A tier — not a fabricated claim, but a framing choice that a human reviewer should confirm is intentional).

hero_title verdict: REVIEW

### prologue_1: "בקטגוריית היוגורטים בשופרסל ניתחנו 17 מוצרים. שניים מהם, שתי גרסאות של דנונה פרו, קיבלו ציון S — הציון הגבוה ביותר בסולם, שמשמעותו שכל מרכיבי הניתוח יצאו נקיים ולא הופעל אף קנס."

- "17 מוצרים" — T2: v4 product_count=17. PASS.
- "שניים מהם... ציון S" — T2: grade_distribution S=2. PASS.
- "שתי גרסאות של דנונה פרו" — T1: both S products are דנונה PRO (barcodes 7290112336712 and 7290110565527). PASS.
- "שמשמעותו שכל מרכיבי הניתוח יצאו נקיים ולא הופעל אף קנס" — T2: both S products trace shows caps_applied=[], penalties_applied=[]. PASS.

prologue_1 verdict: PASS

### prologue_2: "אחריהם, בטווח A, נמצאים שני מוצרי חלבון גבוה נוספים: יופלה GO מועשר בחלבון ומולר אקטיב לבן. שניהם נתקעו ממש מתחת ל-S בגלל היבט אחד שנשאר מאחור."

- "בטווח A" — T2: both products grade=A. PASS.
- "שני מוצרי חלבון גבוה" — T3: יופלה GO protein=10.0, מולר אקטיב protein=12.5. Both in high-protein cluster. PASS.
- "נתקעו ממש מתחת ל-S" — T3: scores are 89.9 and 84.8; S threshold requires 90+. Consistent. PASS.
- "בגלל היבט אחד שנשאר מאחור" — T3: each has one primary limiting dimension (protein_quality=63.8 and processing_quality=64.0 respectively). T3 editorial framing consistent with trace. PASS.

prologue_2 verdict: PASS

### prologue_3: "מרבית היוגורטים הלבנים הרגילים (ביו תנובה, ללא לקטוז, יווני) נחתו ב-B. ההפרש ביניהם לבין ה-S נובע כמעט כולו מפוטנציאל החלבון: אצל הפשוטים הוא עומד על 5–6 גרם ל-100 גרם, לעומת 10–10.5 גרם אצל ה-S."

- "נחתו ב-B" — T2: ביו 3%=B, ביו 1.5%=B, נטול לקטוז=B, יווני 6.5%=B, יווני 8%=B. PASS.
- "5–6 גרם ל-100 גרם" — T1 range: ביו 3%=5.3, ביו 1.5%=5.2, נטול לקטוז=5.0, יווני 6.5%=5.5, יווני 8%=6.0, עיזים=3.6. The range 5–6 covers most but עיזים (3.6) is below 5. However the claim says "יוגורטים הלבנים הרגילים (ביו תנובה, ללא לקטוז, יווני)" specifically — עיזים is not in this named list. For the named products only: 5.0–6.0 is accurate. PASS.
- "10–10.5 גרם אצל ה-S" — T1: S products protein=10.5 and 10.0. Range 10–10.5 confirmed. PASS.

prologue_3 verdict: PASS

### prologue_4: "ממנגו ווניל ועד קורנפלקס — ברגע שנוספים תוספות, ממתיקים, ציפויים או רשימת רכיבים ארוכה, הציון יורד ל-C ול-D. אין כאן הפתעות: ההפרש בין הפשוט לממותג הוא המדף שאתם רואים."

- "מנגו ווניל ועד קורנפלקס" — T1 product references: GO מנגו (C), פרו וניל (B), מולר קורנפלקס (C). Products named are real and present.
- "הציון יורד ל-C ול-D" — T2: flavored products span C (64, 62, 57.7, 55) and D (49.9, 36.3). PASS.
- "תוספות, ממתיקים, ציפויים, רשימת רכיבים ארוכה" — T3: consistent with ADDITIVE_3_PLUS, NOVA4 caps and LONG_INGREDIENT_LIST penalties fired across C/D products. PASS.

prologue_4 verdict: PASS

### methodology_1–4

- methodology_1: "ציון שברי נותנת מבוסס על ניתוח של עשרה היבטים" — 10 dimensions stated. Trace confirms 10 dimension_scores keys. T2 PASS.
- methodology_1 dimension list: "דרגת העיבוד... צפיפות רכיבי התזונה... צפיפות קלורית... איכות הפחמימות... כמות ואיכות החלבון... תוספות ומצרכים מלאכותיים... כוח השובע... טיב השומן... עמידה ברגולציה... שלמות המזון" — maps cleanly to the 10 trace dimensions (processing_quality, nutrient_density, calorie_density, glycemic_quality, protein_quality, additive_quality, satiety_support, fat_quality, regulatory_quality, whole_food_integrity). T3 PASS.

  NOTE: The draft uses "כמות ואיכות החלבון" as a single item, which covers both nutrient_density (protein quantity dimension) and protein_quality. This is an editorial compression. Not a HARD-FAIL but REVIEW.

- methodology_2: "יוגורט עם 10 גרם חלבון ל-100 גרם יקבל ציון חלבון גבוה בהרבה מיוגורט עם 3.6 גרם" — T1: corpus has products at exactly 10g and 3.6g. Comparative claim is directionally correct (protein_quality=75–80 vs nutrient_density=24.5 for the goat product). T3 PASS.
- methodology_3: "מוצר מעובד... מגבלת ניקוד על בסיס עוצמת העיבוד ומספר התוספות" — T2: confirmed by NOVA4/ADDITIVE caps mechanism. PASS. "מגבלה זו מציבה תקרה שהציון לא יכול לחצות" — correct description of binding_cap mechanic. PASS.
- methodology_4: "סיבים תזונתיים לא נכנסו לניתוח" — T2: EV-027 in trace for dairy_protein: "fiber not-applicable for category 'dairy_protein'". PASS.

methodology_1–4 verdict: PASS (methodology_1 compression REVIEW — minor)

### category_note

The category_note has three paragraphs.

Paragraph 1: "המספר הכי גדול על הגביע אינו בהכרח הסיגנל שמניע את הציון... דנונה פרו 21 ודנונה פרו וניל הם אותה משפחה של מותג, ובין השניים יש הפרש של 20 ציונים."
- דנונה פרו 21 = 92.6/S; דנונה פרו וניל = 72/B. Gap = 92.6−72 = 20.6 → rounds to ~21 points if exact, or ~20 if treating 92.6 as "about 92". The claim "20 ציונים" is an approximation. Same REVIEW as P-11 (the gap). The integer scores are 93 and 72 = 21, or 92.6 and 72 = 20.6. "20 ציונים" is not exactly correct at either rounding convention. REVIEW.

Paragraph 2: S caveat — "שני מוצרי דנונה פרו... ציון S... 87 מוצרים שנותחו, רק שניים הגיעו אליו. זהו ממצא מבנה — לא תקרה שהוטלה — ומשקף ניקוד אמיתי."
- "87 מוצרים שנותחו" — the SHARED METHODOLOGY NOTE in s_grade_explanations_v1.md says "מתוך 87 מוצרים שנותחו". This figure is the approved text (from the Nutrition-approved source). PASS on the figure as verbatim.
- "שני מוצרי הדנונה פרו" vs draft "שני מוצרי דנונה פרו" — one-word deviation (missing "ה"). REVIEW (as flagged in FLAG-B §6).
- "ממצא מבנה — לא תקרה שהוטלה" — T3 editorial consistent with trace (no cap imposed S ceiling; score is genuine engine output). PASS.
- Two em-dashes: confirmed in both source and draft. REVIEW per FLAG-B.

Paragraph 3: Fiber note — "סיבים תזונתיים אינם חלק מניתוח הקטגוריה הזו. מוצרי חלב רבים אינם מדווחים על סיבים בתווית, ולכן הוא הוצא מהחישוב במלואו כדי להבטיח השוואה שוויונית."
- T2: EV-027 confirmed — fiber excluded from dairy_protein category. PASS.

category_note overall verdict: REVIEW (approximated gap, FLAG-B wording deviation)

---

## 9. Fermentation Claims — STATE A Verification

Three products have fermentation-related claims in trace_drivers_cited (not in consumer-facing strings). The consumer-facing strings for the plain B-grade products do NOT make fermentation bonus claims — they describe the products without citing fermentation as a score mechanism. Checking for any inadvertent fermentation bonus language in expansion strings:

- Products P-05 (ביו 3%), P-06 (ביו 1.5%), P-07 (נטול לקטוז): consumer copy contains no fermentation mechanism claims. The word "חיידקי ביפידוס" or "חיידקי יוגורט" appears as T1 ingredient claims (marked UNVERIFIABLE per §7.3), not as T2 fermentation bonus claims.
- Products P-01, P-02 (S products): "חיידקי יוגורט" in insightLine is a T1 ingredient claim (verifiable from trace ingredient_list directly). No consumer string says "תרביות חיות מרימות את הציון" or equivalent causal fermentation language.

No fermentation bonus STATE A/B evaluation required for consumer-facing strings. The trace_drivers_cited fields are internal metadata in the draft JSON, not consumer-facing. No REVIEW items from fermentation claims.

---

## 10. Revised Verdict Totals (After Full Analysis)

The P-15 confidence_label_he HARD-FAIL was identified during per-product checks.

| Verdict | String count | Products affected |
|---------|-------------|-------------------|
| **PASS** | 57 | — |
| **REVIEW** | 12 | 8 products + 3 page-level strings |
| **HARD-FAIL** | **1** | P-15 (מולר מיקס קורנפלקס, confidence_label_he) |
| **UNVERIFIABLE** | 7 | 6 products |

**Gate result: HARD-FAIL.** One hard fail identified: confidence_label_he and confidence_tooltip_he for barcode 7290102394081 (מולר מיקס קורנפלקס מצופה) claim "ניתוח מלא" / "כל הנתונים התזונתיים הרלוונטיים זמינים ומלאים" when v4 engine field is confidence="partial" (confidence_sub_reason="low_extraction").

**The fix is a single-product copy edit.** It does not block owner read if the fix is applied in-draft before merge. See §11 for recommended resolution.

---

## 11. HARD-FAILs

### HF-01 — barcode 7290102394081 (מולר מיקס קורנפלקס מצופה, 55/C)

**Field:** `confidence_label_he` and `confidence_tooltip_he`
**Draft value:** `"ניתוח מלא"` / `"כל הנתונים התזונתיים הרלוונטיים זמינים ומלאים."`
**Display layer (v4):** `confidence = "partial"`, `confidence_sub_reason = "low_extraction"`
**Trace evidence:** v4 file line `"confidence": "partial"` for bsip1_yogurt_7290102394081; claims_input_v3 shows `display_grade=C`, `confidence_sub_reason=low_extraction`
**Claim type:** T2 (display-layer assertion about engine confidence classification)
**Rule triggered:** Rubric §6: confidence label claims are T1/T2 facts against the display layer. Draft says full analysis; display layer says partial.
**Required fix:** Change `confidence_label_he` to `"ניתוח חלקי"` and update `confidence_tooltip_he` to reflect the actual data gaps for this product rather than claiming all data is available.
**Route:** Content Agent / Frontend Agent (copy edit, no data or scoring change)

---

## 12. UNVERIFIABLE Items

| # | Product | Field | Claim | Reason |
|---|---------|-------|-------|--------|
| UV-01 | יופלה GO מועשר בחלבון (7290110321031) | insightLine | "אבקת חלב" ingredient name | Not in display_values ingredient_percentages; full ingredient list not inline |
| UV-02 | מולר אקטיב לבן (7290114311069) | insightLine | "רכיבי חלב וסיבים תזונתיים" (items 2 and 3) | Not in ingredient_percentages ({}) |
| UV-03 | ביו תנובה 3% (7290014758100) | insightLine + positiveSignals | "חיידקי ביפידוס" culture name | Per rubric §7.3 — T1 culture ingredient name not in positiveSignals or display_values.ingredient_list_raw |
| UV-04 | עיזים ביו (7290012645297) | positiveSignals | "אבקת חלב, חיידקי יוגורט" | Not in ingredient_percentages |
| UV-05 | יוגורט אוורירי GO מנגו (7290116934402) | trace mechanism | 68→64 delta mechanism | score_after_cap=68, score_after_penalty=64, penalties_applied=[] — 4-point delta unexplained in trace |
| UV-06 | יוגורט קראנצ (7290010471669) | insightLine + limitingFactors | "סירופ גלוקוז" ingredient name | Not in display_values clean ingredient field (ingredient_percentages has malformed entry); ADDITIVE_5_PLUS firing is consistent but name not directly confirmed |
| UV-07 | יופלה GO תות (7290110321680) | insightLine + limitingFactors | "4 קטגוריות תוספות" count | ADDITIVE_MARKERS_3_PLUS confirms 3+; count of 4 not visible in claims_input_v3 trace summary L3_additive_categories |

Note: UV-05 (GO מנגו mechanism) is a pipeline finding, not a copy failure. Copy makes no false claim about the 68→64 step. Route to Data Agent.

---

## 13. REVIEW Items

| # | Product/Field | String | Issue | Rule |
|---|--------------|--------|-------|------|
| RV-01 | יופלה GO מועשר בחלבון (7290110321031) | limitingFactors | "חלבון מגיע ממקור מעורב... מכפיל 0.85" — multiplier value not in displayed trace fields | T3 framing with specific numeric not in display_values |
| RV-02 | דנונה PRO וניל (7290112330352) | insightLine | "הפרש של 20 ציונים" — gap is 18.6–20.6 depending on S product referenced; not exactly 20 | T2 approximate cross-product gap |
| RV-03 | יופלה GO תות (7290110321680) | insightLine + limitingFactors | "4 קטגוריות תוספות" — L3 additive count not confirmed at 4 from claims_input_v3 summary | T2 additive count needs L3 trace confirmation |
| RV-04 | מולר פרוטאין פירות יער (7290102399819) | insightLine + limitingFactors | Same: "4 קטגוריות תוספות" | T2 additive count needs L3 trace confirmation |
| RV-05 | יוגורט קראנצ (7290010471669) | insightLine + limitingFactors | "סירופ גלוקוז" specific ingredient name needs full ingredient text confirmation | T1 ingredient name partially supported |
| RV-06 | hero_title | "שאר המדף נפרס בין B ל-D" | Two A-grade products exist and are not mentioned in the range | T3 framing compression — intentional? |
| RV-07 | category_note ¶1 | "הפרש של 20 ציונים" (דנונה פרו 21 vs וניל) | Exact gap = 20.6 / approx. 21 pts at integer rounding | T2 approximate |
| RV-08 | category_note ¶2 | "שני מוצרי דנונה פרו" vs source "שני מוצרי הדנונה פרו" | One-word deviation from verbatim-approved S text | Verbatim deviation (FLAG-B) |
| RV-09 | category_note ¶2 | Two em-dashes in one paragraph | Style note from Content Agent | FLAG-B style — confirmed present in source; not a fabrication |
| RV-10 | methodology_1 | "כמות ואיכות החלבון" compresses two separate dimensions into one | Editorial compression of nutrient_density + protein_quality | T3 minor framing |

---

## 14. Return Block

**Status proposed: RETURNED**
**Task:** TASK-256 P14
**Deliverable:** `C:\Bari\03_operations\claim_entailment\calibration\yogurts_draft_gate_v1.md`

**Gate result: HARD-FAIL (1 item) — single targeted fix required**

**HF-01 — barcode 7290102394081 (מולר מיקס קורנפלקס מצופה)**
- confidence_label_he="ניתוח מלא" contradicts v4 confidence="partial"
- confidence_tooltip_he="כל הנתונים התזונתיים הרלוונטיים זמינים ומלאים" contradicts confidence_sub_reason="low_extraction"
- Fix: change both fields to match the "partial" confidence classification
- This is a single-product copy edit. All other 16 products are clean.

**Condition to re-gate:** After Content Agent corrects HF-01, re-run this check on the two confidence fields only. If fixed, the gate passes with 0 HARD-FAILs.

**S-product verbatim: CONFIRMED.** Both S products (7290112336712 and 7290110565527) have insightLine and s_grade_explanation matching s_grade_explanations_v1.md exactly character-for-character.

**Sodium / fat causal language: ABSENT.** Zero instances across all 17 products and all page strings.

**Prior-run references: ABSENT.** Zero instances.

**Flag-A (GO מנגו 68→64):** The mechanism is UNVERIFIABLE in the trace (penalties_applied=[] but 4-point delta exists). Copy does not reference this step — copy verdict is PASS. A separate pipeline finding is escalated to Data Agent: `bsip1_yogurt_7290116934402` has score_after_cap=68.0 and score_after_penalty=64.0 with penalties_applied=[] and total_penalty_after_scaling=0.0. The −4.0 delta is unexplained by any named rule in the exposed trace fields.

**REVIEW items (10):** None block owner read. The most significant are the approximate "20 ציונים" gap references (RV-02, RV-07) which a Nutrition Agent or Content Agent should confirm is the intended rounding convention, and the additive count "4" claims (RV-03, RV-04) which need L3 full trace verification.

**UNVERIFIABLE items (7):** All are ingredient-name or mechanism-level data gaps, not fabrications. None block owner read. None involve external authority claims.

**Owner read: CONDITIONAL — fix HF-01 first, then owner read is unblocked.**
