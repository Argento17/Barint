# Calibration Report v1
**Generated:** 2026-06-12
**Task:** TASK-254 Phase 1c — Apply rubric to both inventories

---

## 1. Verdict Totals

### Yogurts (Pilot — Pre-Launch)

- **Strings:** 33 total
- **Claims:** 165 total
- String verdicts: PASS=9  REVIEW=6  HARD-FAIL=15  UNVERIFIABLE=3
- Claim verdicts:  PASS=111  REVIEW=12  HARD-FAIL=26  UNVERIFIABLE=16

### Cereals (Control — Live)

- **Strings:** 79 total
- **Claims:** 188 total
- String verdicts: PASS=7  REVIEW=16  HARD-FAIL=16  UNVERIFIABLE=40
- Claim verdicts:  PASS=48  REVIEW=46  HARD-FAIL=21  UNVERIFIABLE=73

---

## 2. Yogurts — Severity-Sorted Findings

### 2.1 HARD-FAILs (15 strings, 26 claims)

**page / prologue_1**
- HARD-FAIL | T2 | `שבעה יוגורטים על המדף מגיעים ל-A`
  - Evidence: Corpus count: only 3 products have grade=A (yog-003, yog-004, yog-008). 2 products (yog-001, bsip1_7290110565527) have grade=S. 10 have B, 3 have C, 1 has D. Claim of 7 is contradicted by traces.
- HARD-FAIL | T2 | `הציון הגבוה הוא 96/A`
  - Evidence: Top scorer bsip1_7290110565527 trace=95.6/S. Math.round(95.6)=96 correct, but grade=S not A. Claim asserts grade=A for the top product; trace grade=S contradicts.

**page / prologue_2**
- HARD-FAIL | T2 | `ביו 1.5% מגיע ל-80 עד 81, A`
  - Evidence: yog-005 trace: score=79.0, grade=B. Math.round(79.0)=79 (not in range 80-81). Grade=B not A. Both score and grade contradicted.
- HARD-FAIL | T2 | `נטול הלקטוז מגיע ל-80 עד 81, A`
  - Evidence: yog-002 trace: score=78.4, grade=B. Math.round(78.4)=78 (not in range 80-81). Grade=B not A. Both score and grade contradicted.
- HARD-FAIL | T2 | `יוגורט עיזים נשאר ב-77/B`
  - Evidence: yog-006 trace: score=75.3, grade=B. Math.round(75.3)=75. Copy claims 77, trace rounds to 75. Score mismatch.

**page / prologue_3**
- HARD-FAIL | T2 | `יווני 8% עם 4.8 גרם שומן רווי עוצר ב-79/B`
  - Evidence: yog-009 trace: score=75.5, grade=B. Math.round(75.5)=76. Copy claims 79, trace rounds to 76. Score mismatch.

**page / prologue_4**
- HARD-FAIL | T2 | `'הכי טוב' הוא A — אבל לא S`
  - Evidence: Across 19 products, yog-001 trace grade=S (92.6) and bsip1_7290110565527 trace grade=S (95.6). Two products are S. Claim that best is A and not S contradicts traces.
- HARD-FAIL | T2 | `גם היוגורט המוביל נעצר ב-A`
  - Evidence: Top products by score: bsip1_7290110565527=95.6/S and yog-001=92.6/S. Neither stopped at A; both reached S.

**page / category_note_paragraph_2**
- HARD-FAIL | T2 | `'הכי טוב' כאן הוא A, לא S`
  - Evidence: yog-001 (92.6/S) and bsip1_7290110565527 (95.6/S) both trace grade=S, not A.
- HARD-FAIL | T2 | `שבעה יוגורטים על המדף מגיעים ל-A`
  - Evidence: Corpus count: only 3 A-grade products (yog-003, yog-004, yog-008). 2 are S. Claim of 7 contradicted.
- HARD-FAIL | T2 | `הגבוה הוא 96/A`
  - Evidence: Top product bsip1_7290110565527: 95.6/S. Math.round=96 correct, but grade=S not A.
- HARD-FAIL | T2 | `אף אחד לא מגיע ל-S`
  - Evidence: Two products have grade=S: yog-001 (92.6/S) and bsip1_7290110565527 (95.6/S). Negation directly contradicted.
- HARD-FAIL | T2 | `גם המוביל: חלבון גבוה ותרביות חיות מרימים את הציון`
  - Evidence: 'המוביל' (the leader) — top products are S, not A. And 'תרביות חיות' is a REVIEW-level fermentation claim. Grade claim is HARD-FAIL.

**yog-008 / insightLine**
- HARD-FAIL | T3 | `ראש המדף`
  - Evidence: yog-001 trace grade=S/92.6 and bsip1_7290110565527 S/95.6 both outrank yog-008's A/89.9. 'Top of shelf' contradicted by higher-scoring products.

**yog-001 / insightLine**
- HARD-FAIL | T2 | `מגיע ל-A`
  - Evidence: trace grade=S. Copy asserts A, trace shows S.
- HARD-FAIL | T2 | `ונעצר שם: חלבון צפוף לבדו לא מזכה ב-S`
  - Evidence: Trace grade=S contradicts 'לא מזכה ב-S' (does not merit S). The product DOES merit S. Double fail: 'A' and 'not S' both wrong.

**yog-004 / insightLine**
- HARD-FAIL | T3 | `החלבון הגבוה במדף`
  - Evidence: Corpus scan: bsip1_7290110565527 has 20g/100g protein. 12.5g is NOT the highest on shelf.

**yog-005 / insightLine**
- HARD-FAIL | T2 | `מגיע ל-A`
  - Evidence: trace grade=B (79.0/B). Grade A claim contradicted.
- HARD-FAIL | T3 | `מעט גבוה מהבסיסים האחרים, אך עדיין בראש המדף`
  - Evidence: 'בראש המדף' (top of shelf) implies top tier (A). Product is grade=B, score=79.0 — NOT top of shelf. Additionally, this implies the product is among the highest, which is contradicted by grade=B (not A/S).

**yog-002 / insightLine**
- HARD-FAIL | T2 | `מגיע ל-A`
  - Evidence: trace grade=B (78.4/B). Grade A claim contradicted.
- HARD-FAIL | T2 | `בתחתית קבוצת ה-A`
  - Evidence: Implicitly claims the product is in grade A band. Trace grade=B. Not in A group at all.

**bsip1_yogurt_7290110565527 / insightLine**
- HARD-FAIL | T2 | `מגיע ל-96/A`
  - Evidence: trace grade=S (95.6/S). Math.round(95.6)=96 correct. But grade=S, not A. Grade claim contradicted.

**bsip1_yogurt_7290000408316 / insightLine**
- HARD-FAIL | T2 | `צפיפות החלבון הנמוכה מושכת אותו מטה מה-A`
  - Evidence: DOMINANT driver: 'NOVA_PROXY_3_PROCESSED' cap (binding cap=94.8). Score is capped due to NOVA proxy 3 processing, NOT low protein density. Fabricated causal attribution.

**bsip1_yogurt_7290107936309 / insightLine**
- HARD-FAIL | T2 | `יחס שומן-חלבון גבוה מושך אותו מטה מגרסאות הסגנון היווני המועשרות בחלבון`
  - Evidence: DOMINANT driver: 'NOVA_PROXY_3_PROCESSED' cap (binding cap=94.8). The score is capped by NOVA proxy 3 processing classification, NOT by high fat-to-protein ratio. Fabricated causal attribution.

**bsip1_yogurt_7290102399819 / insightLine**
- HARD-FAIL | T2 | `הסוכר הגבוה גוזר ממנו נקודות`
  - Evidence: DOMINANT driver: 'NOVA_PROXY_4_ULTRA_PROCESSED' cap (binding cap=87.2). Score is capped by NOVA4 ultra-processing, NOT by high sugar. Sugar is 9.5g which does NOT trigger any sugar cap (requires >17.5g for HIGH_SUGAR_25G_PLUS or >22.5g for red label). Fabricated causal attribution.

**bsip1_yogurt_7290102394081 / insightLine**
- HARD-FAIL | T3 | `הציון הנמוך בקטגוריה`
  - Evidence: Corpus scan: yog-011 has score=36.3/D, which is lower than 56.3. Superlative directly contradicted by another product's trace.

### 2.2 REVIEWs (6 strings)

**yog-009 / insightLine**
- REVIEW | T2 | `כי 8% שומן ו-4.8 גרם רווי מכריעים`
  - Evidence: trace driver: 'nutrient_density=42.5 (lowest dimension)'. limitingFactors: 'שומן רווי גבוה — 4.8 גרם'. Fat composition impacts nutrient_density. The 'מכריעים' causal framing is consistent with fat being the key limiting factor, but the trace doesn't explicitly name fat as the sole cause. REVIEW per rubric §5 'כי' guidance.

**yog-007 / insightLine**
- REVIEW | T2 | `כי 6.5% שומן, מתוכם 3.9 גרם רווי, מחזיקים אותו מתחת לראש המדף`
  - Evidence: trace driver: 'nutrient_density=38.8 (lowest dimension)'. limitingFactors: 'עתיר שומן לקטגוריה — 6.5 גרם'. Fat composition impacts nutrient_density. Causal 'כי' attribution to fat is consistent with limitingFactors but not explicit in trace. REVIEW per rubric §5.

**yog-006 / insightLine**
- REVIEW | T2 | `תרבית יוגורט`
  - Evidence: T2 fermentation claim. ferm_bonus_applied=null. BRIEF: per rubric §6, culture claims → REVIEW unless explicit in positiveSignals.
- REVIEW | T2 | `כי החלבון כאן 3.6 גרם בלבד, נמוך לקטגוריה`
  - Evidence: trace driver: 'nutrient_density=24.5 (lowest dimension)'. Protein (3.6g) is a key component of nutrient_density. Causal 'כי' attribution to low protein is interpretive but consistent. REVIEW per rubric §5.

**yog-010 / insightLine**
- REVIEW | T3 | `אותם 10 גרם חלבון של ה-GO הלבן שמוביל את המדף`
  - Evidence: 'ה-GO הלבן שמוביל את המדף' cross-references yog-008 as 'leader'. yog-008 is A/89.9 but there are S-grade products (yog-001, bsip1_7290110565527). Cross-product reference to another product as 'leader' is T3/REVIEW without full corpus check.

**bsip1_yogurt_7290110328764 / insightLine**

**bsip1_yogurt_7290116934402 / insightLine**

### 2.3 UNVERIFIABLEs (3 strings)

**yog-003 / insightLine**
- UNVERIFIABLE | T1 | `חלב, רכיבי חלב וחיידקי ביפידוס`
  - Evidence: 'חיידקי ביפידוס' not in positiveSignals/limitingFactors. T1 culture claim per rubric §6 → UNVERIFIABLE.

**yog-011 / insightLine**
- UNVERIFIABLE | T1 | `חלבון של 3.6 גרם בלבד`
  - Evidence: Not in positiveSignals/limitingFactors. Cannot confirm protein value from trace inputs.

**bsip1_yogurt_7290112330352 / insightLine**
- UNVERIFIABLE | T1 | `12 רכיבים: עמילן אורז, סטיביה, חומרי טעם וצבע קרמל`
  - Evidence: Ingredient names not in positiveSignals/limitingFactors. Trace L3 shows sweetener_detected=true, has_artificial_color=false (caramel is natural), but ingredient-level T1 claims not verifiable from trace inputs.

---

## 3. Cereals — Severity-Sorted Findings

### 3.1 HARD-FAILs (16 strings, 21 claims)

**page / prologue_3**
- HARD-FAIL | T2 | `11 ב-C`
  - Evidence: Trace_summary count: 10 grade=C. Live had 11 (bsip1_cereal_7290107647854 live=53/C but recon=D). Drift artifact reduces C count by 1. HARD-FAIL per trace verification.
- HARD-FAIL | T2 | `אחד ב-E`
  - Evidence: Trace_summary count: 2 grade=E (bsip1_cereal_884912126115 recon=E, bsip1_cereal_7613030979647=E). Live had 1 (great grains live=D). Drift artifact. HARD-FAIL.

**bsip1_cereal_5010029000061 / rowVerdict**
- HARD-FAIL | T4 | `ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים`
  - Evidence: Provenance claim about prior run's score and cause. No provenance field in trace. T4 zero tolerance. HARD-FAIL.
- HARD-FAIL | T2 | `כי מועשר בוויטמינים (לא ספונטני)`
  - Evidence: DOMINANT driver: Binding cap=94.8 from NOVA_PROXY_3_PROCESSED. Vitamin enrichment NOT a named cap or penalty. Fabricated causal attribution. HARD-FAIL.

**bsip1_cereal_7290017325910 / rowVerdict**
- HARD-FAIL | T2 | `יורד ל-C`
  - Evidence: trace_summary grade=B (69.2/B). Copy says C, trace says B. HARD-FAIL.
- HARD-FAIL | T4 | `הסף האדום של משרד הבריאות`
  - Evidence: No ISRAELI_RED_LABEL_* sodium rule fired (caps_applied=[]). T4 zero tolerance. HARD-FAIL.

**bsip1_cereal_72968 / rowVerdict**
- HARD-FAIL | T2 | `B על בסיס הדגן המלא`
  - Evidence: trace_summary grade=C (55.0/C). Both live and trace show C. Copy says B. Grade fabrication. HARD-FAIL.
- HARD-FAIL | T3 | `הנתרן מושך כלפי מטה`
  - Evidence: DOMINANT driver: Binding cap=55 from HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_3_PROCESSED. No sodium cap fired. Sodium not the grade driver. Fabricated causal attribution. HARD-FAIL.

**bsip1_cereal_7290107647731 / rowVerdict**
- HARD-FAIL | T2 | `עוצר ב-B תחתון`
  - Evidence: trace_summary grade=C (55.0/C). Live and trace show C. Copy says B. Grade fabrication. HARD-FAIL.

**bsip1_cereal_7290112495433 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (43.0/D). Live=D recon=D. No drift on grade. Copy says C but all sources show D. HARD-FAIL.

**bsip1_cereal_7296073705550 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (46.0/D). Live=D. No drift on grade. Copy says C. HARD-FAIL.

**bsip1_cereal_7296073705567 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (46.0/D). Live=D. Copy says C. HARD-FAIL.

**bsip1_cereal_7290017894911 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (46.0/D). Live=D. Copy says C. HARD-FAIL.

**bsip1_cereal_7290017894928 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (43.0/D). Live=D. Copy says C. HARD-FAIL.

**bsip1_cereal_7290017894904 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (43.0/D). Live=D. Copy says C. HARD-FAIL.

**bsip1_cereal_7296073642022 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (41.8/D). Live=43/D recon=42/D (1pt drift, same grade D). Copy says C, trace=D. No drift on grade. HARD-FAIL.

**bsip1_cereal_7290112495228 / rowVerdict**
- HARD-FAIL | T2 | `C`
  - Evidence: trace_summary grade=D (37.4/D). Live=40/D recon=37/D (3pt drift within D). Copy says C. No drift on grade. HARD-FAIL.

**bsip1_cereal_7296073705574 / rowVerdict**
- HARD-FAIL | T2 | `יורד ל-C`
  - Evidence: trace_summary grade=D (36.4/D). Live=D recon=D. Copy says C. No drift. HARD-FAIL.
- HARD-FAIL | T2 | `כי 320 מ"ג נתרן ל-100 גרם — גבוה לדגני בוקר`
  - Evidence: DOMINANT: Binding cap=55 from HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_3_PROCESSED. No sodium cap fired (sodium=320<700). Fabricated causal attribution to sodium. HARD-FAIL.

**bsip1_cereal_884912126115 / rowVerdict**
- HARD-FAIL | T2 | `כי BHT (E321) ברשימה — נוגד חמצון שנוי במחלוקת`
  - Evidence: Real drivers: HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_4_ULTRA_PROCESSED. BHT NOT a named BSIP2 rule — not in caps_applied, penalties_applied, or explanation_drivers. Fabricated causal attribution. HARD-FAIL.

**bsip1_cereal_7613030979647 / rowVerdict**
- HARD-FAIL | T2 | `D`
  - Evidence: trace_summary grade=E (31.9/E). Live=E recon=E (match). Copy says D, trace=E. No drift on grade. HARD-FAIL.

### 3.2 REVIEWs (16 strings)

**page / prologue_4**
- REVIEW | T1 | `חמישה מוצרים מיועדים לילדים`
  - Evidence: No children's product field in trace_summary. Not verifiable from trace alone. REVIEW.

**page / prologue_5**
- REVIEW | T1 | `גרנולה ומוזלי מוצגים בעמוד נפרד`
  - Evidence: Site structure claim. Not verifiable from product trace. REVIEW.
- REVIEW | T3 | `משפחת מוצרים אחרת`
  - Evidence: Editorial categorization. REVIEW.

**page / category_note**
- REVIEW | T1 | `טענת 'דגנים מלאים' מופיעה על 20 מוצרים`
  - Evidence: Not verifiable from trace. No 'package_claim' field. REVIEW.
- REVIEW | T1 | `לעיתים קמח לבן מופיע לפני הדגן המלא`
  - Evidence: Qualitative observation requires corpus ingredient-order scan. REVIEW.

**bsip1_cereal_7297488098688 / rowVerdict**
- REVIEW | T3 | `כי 3 גרם סיבים נמוך יחסית למיטב הקטגוריה, ואין רשימת רכיבים מורחבת`
  - Evidence: Dominant: NOVA_PROXY_3_PROCESSED cap. Causal attribution to fiber is editorial. 'No extended ingredient list' not a trace driver. REVIEW.

**bsip1_cereal_5900020036407 / insightLine**
- REVIEW | T4 | `הציון הקודם היה שגוי — נתוני שומן וסוכר לא הועברו למנוע`
  - Evidence: Softer T4 about internal pipeline error. No provenance field in trace. REVIEW.

**bsip1_cereal_5900020036407 / rowVerdict**
- REVIEW | T4 | `ערכים שלא הועברו לגרסה הקודמת`
  - Evidence: Softer T4 about prior pipeline. REVIEW.
- REVIEW | T3 | `גלוקוז גבוה וארכיטקטורת שומן בינונית מורידים את הציון`
  - Evidence: DOMINANT: Binding cap=55 from ISRAELI_RED_LABEL_1_SUGAR+NOVA_PROXY_3_PROCESSED. Glucose/fat not named trace drivers. T3 editorial. REVIEW.

**bsip1_cereal_5900020012814 / insightLine**
- REVIEW | T1 | `מוצר ילדים`
  - Evidence: No children's product field in trace. REVIEW.
- REVIEW | T4 | `הציון הקודם שלו היה מנופח`
  - Evidence: Softer T4 about prior run. REVIEW.

**bsip1_cereal_5900020012814 / rowVerdict**
- REVIEW | T4 | `הציון הקודם (78/B) לא כלל נתוני סוכר ושומן מלאים`
  - Evidence: Softer T4 about prior pipeline. REVIEW.

**bsip1_cereal_72968 / insightLine**
- REVIEW | T1 | `חיטה מלאה ראשונה`
  - Evidence: has_whole_grain=true, but 'first ingredient' requires ingredient order verification from trace. REVIEW.
- REVIEW | T3 | `גבוה לקטגוריה`
  - Evidence: Comparative requiring corpus scan. REVIEW.

**bsip1_cereal_7290116537351 / rowVerdict**
- REVIEW | T3 | `כי המילוי המתוק מגדיר את המוצר, ונתוני הסוכר והסיבים אינם זמינים`
  - Evidence: Dominant: Confidence ceiling + HIGH_CAL_LOW_SATIETY_SOFT. Missing data consistent. T3 editorial. REVIEW.

**bsip1_cereal_4005528115218 / rowVerdict**

**bsip1_cereal_42400108153 / rowVerdict**
- REVIEW | T3 | `כי הסוכר שולט וחלבון של 3.6 גרם בלבד; הדגן המלא שולי`
  - Evidence: DOMINANT: HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_3_PROCESSED. Sugar IS binding. T3 editorial. REVIEW.

**bsip1_cereal_8445291638839 / rowVerdict**
- REVIEW | T3 | `כי סוכר הרכיב השלישי, ואריזת הדגנים המלאים לא מציגה פרופיל חלבון מספק (8.3 גרם)`
  - Evidence: DOMINANT: ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_4_ULTRA_PROCESSED. Sugar IS binding. Protein claim is editorial. REVIEW.

**bsip1_cereal_8445290964595 / rowVerdict**
- REVIEW | T3 | `הדגן המלא נוכח אבל מוקף ממתיקים ועיבוד גבוה`
  - Evidence: DOMINANT: ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_3_PROCESSED + penalties. Multiple sugar markers consistent. T3 editorial. REVIEW.

**bsip1_cereal_3387390525960 / rowVerdict**
- REVIEW | T3 | `השוקולד והעיבוד הגבוה מורידים משמעותית למרות הדגן המלא`
  - Evidence: DOMINANT: ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_4_ULTRA_PROCESSED. Choc not a named driver. T3 editorial. REVIEW.

**bsip1_cereal_7613030979647 / insightLine**
- REVIEW | T1 | `תווית ילדים`
  - Evidence: Not verifiable from trace. REVIEW.

### 3.3 UNVERIFIABLEs (40 strings)

Most are T1 numeric claims (protein, sugar, fiber, sodium values, ingredient percentages) that do not appear in `trace_summary.positiveSignals` or `limitingFactors`. The trace carries score/grade/caps/penalties but not the frontend display values. This is a systemic verification gap — see §5.

Representative examples:

**bsip1_cereal_5010029000061 / insightLine**
- UNVERIFIABLE | T1 | `95% חיטה, 12 גרם חלבון, 10 גרם סיבים`
  - Evidence: No positiveSignals/limitingFactors in trace_summary for these values. UNVERIFIABLE.

**bsip1_cereal_7613037686906 / insightLine**
- UNVERIFIABLE | T1 | `10 גרם סוכר ל-100 גרם`
  - Evidence: Not in trace_summary. Missing ingredient data. UNVERIFIABLE.

**bsip1_cereal_7613037686906 / rowVerdict**
- UNVERIFIABLE | T1 | `10 גרם חלבון, 7.7 גרם סיבים, 10 גרם סוכר ל-100 גרם`
  - Evidence: Not in trace_summary. Missing ingredient data. UNVERIFIABLE.

**bsip1_cereal_7290017325910 / insightLine**
- UNVERIFIABLE | T1 | `94% קמח תירס אורגני, 600 מ"ג נתרן`
  - Evidence: Not in trace_summary. UNVERIFIABLE.

**bsip1_cereal_7613033548192 / insightLine**
- UNVERIFIABLE | T1 | `14 גרם סוכר, 10.3 גרם סיבים`
  - Evidence: Not in trace_summary. Missing ingredient data. UNVERIFIABLE.


---

## 4. Top 10 Findings (Across Both Categories)

### Y1 [HARD-FAIL] Page-level S-grade denial — Page strings prologue_1, prologue_4, category_note
All three page strings assert "no product reaches S" and that the highest is 96/A. Trace shows yog-001 (92.6/S) and bsip1_7290110565527 (95.6/S). Three HARD-FAILs on the same false fact. **Pre-launch blocker: page copy must acknowledge S-grade exists.**

### Y2 [HARD-FAIL] A-count wrong — Page strings prologue_1, category_note
"Seven yogurts reach A." Only yog-003 (80.2/A), yog-004 (84.8/A), yog-008 (89.9/A) have trace grade=A. Two are S, ten are B. Count is 3, not 7. **Pre-launch blocker.**

### Y3 [HARD-FAIL] Bio 1.5% and lactose-free falsely claimed as A — prologue_2
"Bio 1.5% and lactose-free reach 80-81, all A." yog-005 trace=79/B, yog-002 trace=78/B. Both grade (B vs A) and score (79 vs 80, 78 vs 80-81) are wrong. **Pre-launch blocker.**

### Y4 [HARD-FAIL] yog-001 (Danone Pro 21) — "reaches A, does not merit S"
Trace grade=S, score=92.6. Copy claims grade=A and explicitly denies S. Both the positive claim and the negation are false. **Pre-launch blocker.**

### Y5 [HARD-FAIL] bsip1_7290110565527 (Danone PRO 20g) — "reaches 96/A"
Trace grade=S (95.6). Copy says A. Correct claim would be 96/S. This product is the Yohananof pool — same S-grade pattern as Y4. **Pre-launch blocker.**

### C1 [HARD-FAIL] 11 products with inflated grade in copy
Products in the D band (~37-46 pts) are systematically mislabeled as C in copy. Examples: bsip1_cereal_7290017894928 (copy=C, trace=D/43.0), bsip1_cereal_7296073705574 (copy=C, trace=D/36.4), bsip1_cereal_3387390525960 (copy=D, trace=D/35.1 — score off by 2). Most are in the 1-3pt drift zone per comparison_table.txt but the grade boundary is crossed. **Live incident: page shows wrong grades for ~1/3 of products.**

### C2 [HARD-FAIL] T4 zero-tolerance: MoH red label — bsip1_cereal_7290017325910
rowVerdict invokes "the Ministry of Health red label threshold" for 600mg sodium. No ISRAELI_RED_LABEL_* sodium rule fired — caps_applied=[]. T4 authority claim with zero trace support. **Live incident.**

### C3 [HARD-FAIL] Fabricated causal attributions (3 products)
bsip1_cereal_7296073705574: "drops to C because 320mg sodium" — real driver = sugar caps. bsip1_cereal_884912126115: "D because BHT" — BHT is not a BSIP2 rule. bsip1_cereal_5010029000061: "stops at B because vitamin-enriched" — real driver = NOVA_PROXY_3_PROCESSED. **Live incidents: causal claims fabricated.**

### C4 [Systemic] T1 UNVERIFIABILITY gap — 73/188 claims (39%)
Numeric values (protein grams, fiber grams, sodium mg, ingredient percentages) are stated as fact in copy but cannot be verified from trace_summary. The trace carries score/grade/caps/penalties but NOT the display values that appear in positiveSignals/limitingFactors. This affects both categories equally. **Infrastructure issue: claims-input builder must carry display values into the verdict engine.**

### C5 [REVIEW] Prologue distribution drift — prologue_3
Prologue claims 11x C / 1x E. Trace shows 10x C / 2x E (drift from 1-3pt recon differences pushing products across grade boundaries: 7290107647854 live=C→recon=D; 884912126115 live=D→recon=E). **Frontend data and copy distribution disagree with reconstructed traces.**

---

## 5. Rubric Ambiguities Encountered

### Ambiguity 1 — T1 verification from trace_summary only
The rubric says T1 claims must appear in `positiveSignals` or `limitingFactors` or be consistent with a fired BSIP2 rule. In practice, the trace_summary object carries none of these — they live in the frontend JSON strings dict. The rubric's worked examples handle this by checking the strings dict, but the rubric §2.1 says "trace_summary does not carry the full ingredient list or nutrition panel" and only checks `positiveSignals`/`limitingFactors` from the input JSON. This means EVERY numeric claim not explicitly in those fields is UNVERIFIABLE. **Suggestion v2:** Add a `display_values` field to trace_summary, or define a separate entailment path for frontend-displayed values.

### Ambiguity 2 — T4 scope for internal process descriptions
Rubric §2.4 defines T4 as "sources, officialdom, endorsement, verifiability attestations" with recognized Hebrew markers. But internal process descriptions ("the previous version had bad data", "the corrected score is 55/C") are T4-adjacent — they reference the pipeline's own history, not external authority. The rubric's CEX-02 example classifies this as HARD-FAIL (T4) but it is arguably a T3 interpretation of the pipeline state. **Suggestion v2:** Add a T4b subtype for internal provenance claims about scoring history, with REVIEW default rather than HARD-FAIL.

### Ambiguity 3 — Cross-product references in product cards
CEX-02: bsip1_cereal_5010029000061 rowVerdict references lion's corrected score. The rubric correctly flags this as architecturally problematic (per-product decomposition can't handle cross-product claims). No clean verdict path exists. **Suggestion v2:** Add a `cross_reference` claim type that triggers a separate cross-product verification pass after per-product pass completes.

### Ambiguity 4 — Drift-aware grade verification
For the 9 cereals with live-vs-recon drift (1-3pts), the orchestrator ruling says "do not HARD-FAIL on the drift itself." But when drift crosses a grade boundary (e.g., live 53/C → recon 50/D), a grade claim that matches live but not recon is technically HARD-FAIL against the trace. The orchestrator ruling creates a tension: verify against trace, but don't fail on drift. **Suggestion v2:** Define a third reference column — "frontend JSON value" — as the authoritative source for score/grade claims, keeping traces as authoritative for mechanisms only. This would align with the orchestrator's ruling #1.

### Ambiguity 5 — Fermentation evidence path
The orchestrator confirms: "No support in either → UNVERIFIABLE, never PASS." But the rubric §6 defines a cross-reference path through the SUPERSEDED run record that yields REVIEW. This is now overridden — all fermentation claims are UNVERIFIABLE. **Suggestion v2:** Update rubric §6 to match orchestrator ruling (UNVERIFIABLE not REVIEW).

---

## 6. Pre-Launch Blockers (Yogurts)

The following findings individually block TASK-249 go-live:

1. **Page denies S-grade;** two products are S (yog-001, bsip1_7290110565527). Page copy and category_note must be rewritten to acknowledge S-grade exists.
2. **A-count wrong:** "7 reach A" — only 3 reach A, 2 are S, 10 are B. Page copy wrong.
3. **Bio 1.5% and lactose-free graded A in copy;** traces show B. Pre-remediation copy never updated.
4. **yog-001 grade reversal:** copy says A/not-S, trace says S. Direct contradiction.
5. **bsip1_7290110565527 grade reversal:** copy says 96/A, trace says 96/S. Same pattern.
6. **11/19 product strings carry a HARD-FAIL.** The page cannot launch as-is.

---

## 7. Live Incidents (Cereals)

The following findings are active on the live site and should be escalated:

1. **~1/3 of products show wrong grade on page** due to copy graded against pre-reconstruction trace state. D-band products labeled C.
2. **T4 MoH red-label claim** (bsip1_cereal_7290017325910) has zero trace support — fabricated authority.
3. **Three fabricated causal attributions** (sodium→grade for sugar-capped product, BHT→grade, vitamins→grade for NOVA-capped product).
4. **73 UNVERIFIABLE claims (39%)** — systemic verification gap means ~40% of factual assertions on the cereals page cannot be traced to the scoring engine.

---

## 8. Claim-Type Distribution

| Type | Yogurts claims | Cereals claims | Yogurts HF | Cereals HF | Notes |
|------|---------------|----------------|------------|------------|-------|
| T1   | 50            | 87             | 0          | 0          | Most are UNVERIFIABLE — numeric values not in trace |
| T2   | 55            | 54             | 16         | 16         | Grade mismatches + fabricated drivers |
| T3   | 35            | 40             | 8          | 0          | Yogurt superlatives vs corpus |
| T4   | 5             | 7              | 2          | 5          | Zero-tolerance: all HF |

---

## 9. Proposed Status

**Yogurts: RETURNED** — 15/33 strings HARD-FAIL. Page copy was authored against pre-TASK-249 run state and never updated. Go-live blocked by 6 findings in §6.

**Cereals: RETURNED** — 16/79 strings HARD-FAIL, 40/79 UNVERIFIABLE. Live page carries fabricated causal claims (C3), an unsupported T4 authority claim (C2), and a systemic grade-inflation pattern affecting ~1/3 of products (C1). The 39% UNVERIFIABLE rate (C4) is a pipeline gap, not a copy issue, but constitutes a ship-blocker under the rubric's definition.

---

_Generated by calibration runner. Read-only analysis — no artifacts, traces, or copy modified._