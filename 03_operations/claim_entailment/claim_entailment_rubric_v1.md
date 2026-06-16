# Claim-Entailment Rubric v1

**Generated:** 2026-06-12  
**Scope:** Consumer-facing claim verification for Bari comparison pages  
**Pilot category:** Yogurts (pre-go-live; findings block launch)  
**Control category:** Breakfast Cereals (live; findings are active incidents)  
**Input files:** `03_operations/claim_entailment/inputs/yogurts_claims_input_v1.json`,  
`03_operations/claim_entailment/inputs/cereals_claims_input_v1.json` (v1, superseded),  
`03_operations/claim_entailment/inputs/cereals_claims_input_v2.json` (reconstructed traces, all 8 NO_TRACE resolved)  
**Governing incident:** "official food source" fabrication shipped live → zero tolerance on unsupported T4

---

## 1. Purpose and Ground Law

Every factual claim in consumer copy must be entailed by that product's BSIP2 trace JSON and Bari methodology docs. Ground truth = **trace + methodology docs only**. Never external sources, general nutrition knowledge, or off-system authority claims. If the trace doesn't show it, it is not entailed — even if true in reality.

Entailment is **per `product_id`**, never per barcode. When the same barcode appears under two product_ids (e.g., barcode 7290107936309 as both `yog-007` Shufersal and `bsip1_yogurt_7290107936309` Yohananof), each instance is checked against its own trace only. Cross-instance comparisons are not valid substitutes.

---

## 2. Claim Taxonomy

### T1 — Observed Fact

Label or nutrition values: protein grams, fat grams, sodium milligrams, ingredient names, additive E-numbers, serving size, fat percentage, ingredient order/position.

**Entailed iff** the exact value or ingredient appears in the trace inputs. Exact match required — do not tolerate rounding beyond the display convention (see §5).

**What the trace carries:** `trace_summary` does not carry the full ingredient list or nutrition panel — it carries `final_score`, `grade`, `nova_level`, caps/penalties/drivers. Explicit numeric values (protein grams, fat grams, etc.) appear in `positiveSignals` and `limitingFactors` in the input `strings` dict, sourced from the frontend data layer. For T1 claims: the claim value must match one of: (a) an explicit value in `strings.positiveSignals` or `strings.limitingFactors`, or (b) be consistent with a fired BSIP2 rule (e.g., `ADDITIVE_MARKERS_3_PLUS` entails "3 or more additives present").

**When T1 is UNVERIFIABLE:** the ingredient/value is stated as fact but does not appear in any of: trace inputs, positiveSignals, limitingFactors, or fired rules. The trace cannot confirm or deny it. → UNVERIFIABLE, not PASS.

---

### T2 — Engine Conclusion

Scores, grades, fired rules, applied caps, applied penalties, and their named effects: "the fermentation bonus", "capped for sodium", "additive burden". This is the most governed type.

**Entailed iff** the rule/cap/penalty/bonus actually fired in THIS product's trace.

**Procedure:**
1. Extract the grade and numeric score claim from the string.
2. Check `trace_summary.grade`. Must match exactly (A ≠ B ≠ S ≠ C etc.).
3. Check score numeric: `Math.round(trace_summary.final_score)` must equal the stated score. Tolerance: ±0 (display convention is integer rounding; a 0.5 delta is a build-level rounding decision, not an entailment tolerance).
4. Check any named driver claim: the rule/cap/penalty must appear in `caps_applied`, `penalties_applied`, or `explanation_drivers`. A rule named in copy but absent from the trace = fabrication = HARD-FAIL.
5. "Capped" claim: the rule must appear in `caps_applied`.
6. "Penalized for X" claim: must appear in `penalties_applied`.
7. "X caused the grade" or "stopped at grade Y because of X" = the named factor X must be the declared DOMINANT driver in `explanation_drivers` or appear in `caps_applied`.

**Score-display tolerance (rounding only):** `Math.round(final_score)` = stated integer. 95.6 → 96 is PASS. 79.0 → 79 vs claimed 80 = HARD-FAIL. 75.5 → 76 vs claimed 79 = HARD-FAIL. If a score is stated as a range ("80 to 81"), every product named in that range must individually satisfy the range via rounding.

---

### T3 — Grounded Interpretation

Editorial framing of T1/T2: characterizations, comparisons, value judgments, contextual observations. Examples: "the honest choice on a sweet shelf", "kinut-style without a trick", "almost everything here is an add-on".

**Entailed iff** every embedded factual anchor resolves to a T1/T2 that passes, AND the interpretation does not contradict any trace value.

**Procedure:**
1. Decompose the phrase into its embedded factual claims (see §4).
2. Verify each embedded claim as T1 or T2.
3. If all embedded T1/T2 pass → T3 PASS.
4. If any embedded T1/T2 HARD-FAILs → T3 inherits that HARD-FAIL.
5. If the interpretation stretches beyond its anchors but does not contradict any trace data → REVIEW.
6. Superlative/comparative claims ("the highest", "the lowest", "the only one that") are T3 with embedded T2. They require a corpus-wide check (all products on the same page). If not checkable from the per-product trace alone → REVIEW. If directly contradicted by another product's trace on the same page → HARD-FAIL.

**T3 examples that are always REVIEW without full corpus check:** "הכי גבוה בקטגוריה" (highest in category), "ראש המדף" (top of shelf) — requires sorting all product scores. "מהנמוכים" (among the lowest) is softer framing, PASS if the score is genuinely low in the visible data.

---

### T4 — Provenance / Authority

Sources, officialdom, endorsement, verifiability attestations. Recognizable Hebrew markers: "לפי משרד הבריאות", "מאושר על ידי", "הסף האדום", "רשמי", "בדיקות מעבדה", "על פי נתוני משרד", "בהתאם לתקן", "מוסמך".

**ZERO TOLERANCE.** Entailed only by explicit provenance fields in the trace or Bari methodology docs. Otherwise HARD-FAIL, always, regardless of whether the claim is factually true in the external world.

**Acceptable provenance anchors:** a named rule in `caps_applied` that encodes an authority threshold (e.g., `ISRAELI_RED_LABEL_1_SUGAR` entails the Israeli red-label sugar threshold; `ISRAELI_RED_LABEL_1_SODIUM` would entail the sodium threshold — but only if it actually fired for this product). The rule name implicitly carries the authority reference. If the named rule did NOT fire → HARD-FAIL even if the threshold is otherwise known.

**Never acceptable as T4 evidence:** general knowledge of ministry thresholds, external databases, the reviewer's own knowledge, or "everyone knows this threshold".

**Example:** "600 mg sodium — the Ministry of Health red label threshold" → T4. Entailed only if `ISRAELI_RED_LABEL_1_SODIUM` appears in `caps_applied` for this product. If the trace shows no sodium cap → HARD-FAIL.

---

## 3. Verdict Codes

| Code | Meaning | Build behavior |
|------|---------|----------------|
| **PASS** | All claims in the string are entailed by the trace | Build proceeds |
| **REVIEW** | No HARD-FAIL; interpretation stretches beyond anchors, superlative needs corpus-check, or cross-run score mismatch in non-authoritative trace (cereals run_006) | Human queue; does NOT break build immediately |
| **HARD-FAIL** | At least one claim contradicts the trace, names an unfired rule, asserts an unobserved fact, or is an unsupported T4 | Build must break |
| **UNVERIFIABLE** | Product has no trace file, or the claim type cannot be evaluated against available artifacts | Ship blocker — counted separately; means missing evidence, not fabrication |

**String-level verdict** = worst claim verdict in the string. One HARD-FAIL anywhere = the string is HARD-FAIL.

**Tie-break:** When uncertain between REVIEW and PASS → REVIEW. When uncertain between HARD-FAIL and REVIEW → HARD-FAIL. Never resolve uncertainty to PASS.

---

## 4. Decomposition Procedure

Apply to every string (insightLine, rowVerdict, positiveSignal, limitingFactor, prologue, category_note paragraph, methodology line):

**Step 1 — Identify atomic claims.** Split at clause boundaries: "X גרם חלבון", "עוצר ב-Y/Z", "כי W גרם", "הסף של משרד הבריאות", "הכי גבוה בקטגוריה". One claim = one measurable assertion.

**Step 2 — Assign type** (T1 / T2 / T3 / T4) per §2.

**Step 3 — Check each claim** against the trace, using the procedure for that type.

**Step 4 — Assign per-claim verdict** (PASS / REVIEW / HARD-FAIL / UNVERIFIABLE).

**Step 5 — String verdict** = worst per-claim verdict.

**Example decomposition** — yog-011 insightLine:  
"הציון הנמוך במדף — יוגורט שהפך לקינוח: תוספת קורנפלקס ושוקולד, חמישה תוספי מזון ומעלה, סוכר מוסף שזוהה של 9.9 גרם וחלבון של 3.6 גרם בלבד. צונח ל-D כי כמעט הכול כאן תוספת."
- Claim A: "הציון הנמוך במדף" → T3 superlative, needs corpus-wide check → REVIEW (but see §7 Ex-14: another product scores lower, so this is HARD-FAIL for this example)
- Claim B: "חמישה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_5_PLUS` in `caps_applied` → PASS
- Claim C: "סוכר מוסף שזוהה" → T2 rule: `MULTIPLE_ADDED_SUGAR_MARKERS` in `penalties_applied` → PASS
- Claim D: "9.9 גרם" sugar → T1 value from `limitingFactors` string → PASS
- Claim E: "3.6 גרם חלבון" → T1 value, consistent with trace inputs → PASS
- Claim F: "צונח ל-D" → T2 grade: trace grade="D" → PASS
- Claim G: "כמעט הכול כאן תוספת" → T3 framing supported by NOVA4 + ADDITIVE_5_PLUS + long ingredient list + sugar penalties → PASS
- String verdict: HARD-FAIL (Claim A is HARD-FAIL — another product has a lower score)

---

## 5. Hebrew-Specific Guidance

### Grade and score claims

Hebrew patterns that assert a grade/score:
- "מגיע ל-A" / "מגיעים ל-A" → T2 grade assertion, must match `trace_summary.grade`
- "עוצר ב-B" / "נשאר ב-C" / "צונח ל-D" → T2 grade assertion
- "XX/Y" (numeric/letter) → T2 score + grade, both must be verified
- "הציון הוא XX" → T2 score assertion
- "נעצר ב-A: ... ולא S" → T2 assertion that grade is A AND grade is NOT S; both must match trace
- "אף אחד לא מגיע ל-A" → T2 corpus-wide grade assertion; needs corpus check → REVIEW unless directly contradicted

### Negation traps

"לא מגיע ל-S" asserts the grade is below S. If trace shows grade=S → HARD-FAIL. The negation is part of the claim.

"לא מזכה ב-S" (does not merit S) combined with "מגיע ל-A" together assert grade=A. If trace says S → both are HARD-FAIL.

### Superlatives and comparatives

These are always T3 with embedded cross-product check:
- "הכי טוב" / "המוביל" / "ראש המדף" → REVIEW, requires corpus sort
- "הציון הנמוך" / "הנמוך ביותר" / "הנמוך בקטגוריה" → REVIEW if corpus sort not done; HARD-FAIL if another product's trace shows a lower score
- "הגבוהים בקטגוריה" (highest in category on two dimensions) → REVIEW
- "הכי גבוה" on a numeric value → requires checking all other products' traces

### Causal attribution ("כי")

"כי" (because) introduces an explanation. In "עוצר ב-B כי מועשר בוויטמינים" — the "כי" links the grade to a cause. That cause must appear in the trace as a fired driver. Vitamin enrichment is not a BSIP2 scoring factor (vitamins added = synthetic = does not appear as a cap or penalty unless the ingredient list triggers ADDITIVE rules). If the real driver in the trace is `NOVA_PROXY_3_PROCESSED`, attributing the grade to vitamin enrichment is a T2 fabrication → HARD-FAIL.

### Ministry/authority implicatures

"הסף האדום" (the red label) invokes the Israeli MoH Nutrition Labeling Law thresholds (sugar, saturated fat, sodium). Requires the corresponding ISRAELI_RED_LABEL_* rule to have fired in `caps_applied` for that specific product. If 600 mg sodium is stated as "the red label" threshold without `ISRAELI_RED_LABEL_1_SODIUM` in caps → T4 HARD-FAIL.

Note: the standard MoH sodium red-label threshold for cereals is 600 mg/100g (high-sodium category) or alternatively 400 mg/100g. The BSIP2 engine encodes this as `ISRAELI_RED_LABEL_1_SODIUM` (not confirmed in cereal run_006 traces reviewed — no sodium caps appear in any cereal product trace reviewed). Until the rule name is confirmed in a fired trace, invoking MoH authority for sodium is T4 HARD-FAIL.

### "היחיד ש..." (the only one that...)

Claims uniqueness across the category. T3 with embedded T2. Requires corpus-wide negative check. → REVIEW until corpus-checked.

### Confidence label claims

"ערכי הסוכר לא היו זמינים" (sugar values were not available) → T1 fact about data availability. Entailed by `strings.confidenceLabel` ∈ {"חסרים נתוני תזונה", "חסרים נתוני רכיבים"} AND by explicit `strings.unknowns` entry. If confidenceLabel says "מבוסס על נתונים מלאים" and the copy claims missing data → HARD-FAIL.

### Flavored/variant comparisons

"אותם X גרם חלבון של הלבן" (same protein as the plain version) = T3 cross-product T1 claim. Requires checking the referenced comparison product's trace. If the reference product's protein value is not in its own positiveSignals → UNVERIFIABLE.

---

## 6. Fermentation Bridge (Yogurts Only)

### The gap

`fermentation_bonus_applied` is `null` in **all** per-product BSIP2 trace files. The +8 fermentation bonus is applied at the category scoring layer, not recorded per-product. This means no per-product trace entails a fermentation claim directly.

### Documented cross-reference path

The SUPERSEDED run record at `02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json` contains an `A_list` array with `ferm_bonus` and `ferm_note` fields per product. This record is `_status: "SUPERSEDED/REFERENCE_ONLY"` — it covers a pre-remediation candidate run with a contaminated corpus and blocked barcode.

### Policy: when SECONDARY evidence is acceptable

A T2 fermentation claim ("the fermentation bonus lifts the score", "live cultures raise the grade") is verified against the SUPERSEDED run record only under ALL of the following conditions:
1. The product barcode appears in the A_list of the SUPERSEDED run record with `ferm_bonus ≠ null` AND `ferm_bonus > 0`.
2. The product's current trace grade (run_yogurt_006) is A or S — confirming the product is in the high-scoring tier where the fermentation bonus is architecturally meaningful.
3. The copy claim is about the existence/effect of the fermentation bonus, NOT about the specific numeric value.

When all three conditions hold → verdict = REVIEW (not PASS, because the run record is SUPERSEDED). The reviewer confirms the product identity across both records before signing off.

When any condition fails → UNVERIFIABLE. Examples: a product with NOVA_PROXY_4_ULTRA_PROCESSED cap (score capped below the fermentation-meaningful range) where copy claims live cultures boosted the grade → UNVERIFIABLE.

### T1 ingredient claims about cultures

"חיידקי ביפידוס" (Bifidus bacteria), "תרבית יוגורט" (yogurt culture), "חיידקי פרוביוטי" → T1 ingredient claims. These are from BSIP0/BSIP1 ingredient enrichment (Hebrew ingredient detection), not the trace. They appear in the `positiveSignals` / `unknowns` / product name of the frontend data but are NOT carried by the `trace_summary`. Verdict = UNVERIFIABLE unless the value appears explicitly in `strings.positiveSignals` or `strings.limitingFactors` for that product.

---

## 7. Worked Examples

Format per example: **[ID] Product → String excerpt → Decomposition → Verdict → Trace evidence**

---

### YOGURTS EXAMPLES

---

**[YEX-01]** `yog-008` (יופלה GO מועשר בחלבון)  
**String:** insightLine — "ראש המדף — 10 גרם חלבון, בלי סוכר מוסף שזוהה ועם תרביות חיות שמרימות את הציון. מגיע ל-A אך נעצר שם, לא S."  
**Decomposition:**  
- "10 גרם חלבון" → T1: appears in `positiveSignals` ("חלבון גבוה לקטגוריה — 10 גרם ל-100 גרם") → PASS  
- "בלי סוכר מוסף שזוהה" → T1: no `MULTIPLE_ADDED_SUGAR_MARKERS` in penalties, no sugar cap → PASS  
- "תרביות חיות שמרימות את הציון" → T2 fermentation. `fermentation_bonus_applied=null`. SUPERSEDED A_list: `bsip1_yogurt_7290110321031` ferm_bonus=8. Current trace grade=A (condition 2 met). → **REVIEW** (SECONDARY evidence, SUPERSEDED run record)  
- "מגיע ל-A" → T2 grade: trace grade="A" → PASS  
- "נעצר שם, לא S" → T2 negation: trace grade="A" ≠ S, so "not S" is confirmed → PASS  
- "ראש המדף" → T3 superlative: yog-001 trace shows S (92.6), yog-008 is A (89.9). A product with a higher score exists on the same page. → **HARD-FAIL** (superlative contradicted by another product's trace)  

**String verdict: HARD-FAIL** (ראש המדף claim contradicted by yog-001 trace=S, score 92.6 > 89.9)

---

**[YEX-02]** `yog-001` (דנונה פרו 21 חלבון 0%)  
**String:** insightLine — "מגיע ל-A על שילוב נדיר של חלבון גבוה וסוכר נמוך, ונעצר שם: חלבון צפוף לבדו לא מזכה ב-S."  
**Decomposition:**  
- "מגיע ל-A" → T2 grade: trace grade="S" → **HARD-FAIL** (copy asserts A, trace is S)  
- "ונעצר שם: ... לא מזכה ב-S" → T2 negation: trace grade="S" contradicts the explicit "does not merit S" → **HARD-FAIL** (double violation: asserts A, explicitly denies S, trace is S)  
- "10.5 גרם חלבון" → T1: positiveSignals "10.5 גרם ל-100 גרם" → PASS  
- "3.3 גרם סוכר, ללא סוכר מוסף שזוהה" → T1: positiveSignals "סוכר נמוך — 3.3 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS  

**String verdict: HARD-FAIL** — grade/S-negation claim directly contradicts trace. **PRE-LAUNCH BLOCKER.**

---

**[YEX-03]** `yog-005` (יוגורט ביו תנובה 1.5%)  
**String:** insightLine — "אותו ביו פשוט של תנובה בגרסת 1.5% שומן — אותם חיידקי ביפידוס, 5.2 גרם חלבון. מגיע ל-A על אותו בסיס פשוט."  
**Decomposition:**  
- "מגיע ל-A" → T2 grade: trace grade="B" → **HARD-FAIL**  
- "5.2 גרם חלבון" → T1: not in positiveSignals (positiveSignals only says "שומן נמוך — 1.5 גרם"). No explicit 5.2g protein entailment → UNVERIFIABLE  
- "חיידקי ביפידוס" → T1 ingredient: not in positiveSignals or limitingFactors → UNVERIFIABLE  
- "1.5% שומן" → T1: positiveSignals "שומן נמוך — 1.5 גרם ל-100 גרם" → PASS  

**String verdict: HARD-FAIL** (grade A contradicts trace B). **PRE-LAUNCH BLOCKER.**

---

**[YEX-04]** `yog-002` (יוגורט נטול לקטוז 3% שומן)  
**String:** insightLine — "מגיע ל-A על בסיס פשוט ותרביות חיות, בתחתית קבוצת ה-A: ערכי הסוכר לא היו זמינים."  
**Decomposition:**  
- "מגיע ל-A" → T2 grade: trace grade="B" → **HARD-FAIL**  
- "בתחתית קבוצת ה-A" → T2: implies the product is in the A grade band, trace says B → **HARD-FAIL** (same violation, different phrasing)  
- "ערכי הסוכר לא היו זמינים" → T1 confidence fact: confidenceLabel="חסרים נתוני תזונה" + unknowns lists sugar → PASS  
- "תרביות חיות" → T2 fermentation: ferm_bonus_applied=null. SUPERSEDED A_list: this product is `bsip1_yogurt_7290110328221`. Not listed in the A_list (because it didn't reach A in the old run either — confirmed by checking the A_list). → UNVERIFIABLE  

**String verdict: HARD-FAIL** (grade A contradicts trace B). **PRE-LAUNCH BLOCKER.**

---

**[YEX-05]** `yog-003` (יוגורט ביו תנובה 3%)  
**String:** insightLine — "מהפשוטים במדף — חלב, רכיבי חלב וחיידקי ביפידוס, 5.3 גרם חלבון וסוכר נמוך של 4 גרם ללא סוכר מוסף שזוהה. מגיע ל-A בלי שום טריק חלבון."  
**Decomposition:**  
- "מגיע ל-A" → T2 grade: trace grade="A" → PASS  
- "ללא סוכר מוסף שזוהה" → T1: positiveSignals "סוכר נמוך — 4 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS  
- "4 גרם סוכר" → T1: positiveSignals → PASS  
- "5.3 גרם חלבון" → T1: not explicitly in positiveSignals (positiveSignals only confirms low sugar). → UNVERIFIABLE  
- "חיידקי ביפידוס" → T1 ingredient: not in trace inputs → UNVERIFIABLE  
- "בלי שום טריק חלבון" → T3 framing: no ADDITIVE_* caps, no protein-enrichment signals in trace, consistent with NOVA=2 → PASS (no contradiction)  

**String verdict: UNVERIFIABLE** (cannot confirm protein value and culture presence). Note: UNVERIFIABLE does not mean PASS — strings with UNVERIFIABLE T1 claims must be reviewed before launch.

---

**[YEX-06]** `yog-009` (יוגורט יווני 8%)  
**String:** insightLine — "רק שלושה רכיבים — חלב, שמנת וחלבון חלב — וסוכר נמוך של 3 גרם ללא סוכר מוסף שזוהה. עוצר ב-B, מתחת לבסיסים הרזים, כי 8% שומן ו-4.8 גרם רווי מכריעים."  
**Decomposition:**  
- "עוצר ב-B" → T2 grade: trace grade="B" → PASS  
- "3 גרם סוכר" → T1: positiveSignals "סוכר נמוך — 3 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS  
- "4.8 גרם רווי" → T1: limitingFactors "שומן רווי גבוה — 4.8 גרם ל-100 גרם" → PASS  
- "8% שומן" → T1: product name says "8%" → PASS  
- "שלושה רכיבים" → T1 ingredient count: not in trace → UNVERIFIABLE  
- "4.8 גרם רווי מכריעים" → T2 causal: trace explanation_driver = "nutrient_density=42.5 (lowest dimension)". `limitingFactors` lists saturated fat. The nutrient_density score reflects fat composition. T3 framing that fat is the decisive factor is consistent with nutrient_density being the lowest dimension and limitingFactors listing saturated fat → REVIEW (interpretation consistent, but "מכריעים" is an interpretive causal not literally named in trace)  

**String verdict: REVIEW** (unverifiable ingredient count + interpretive causal framing)

---

**[YEX-07]** `yog-010` (יופלה GO תות)  
**String:** insightLine — "אותם 10 גרם חלבון של ה-GO הלבן שמוביל את המדף — אבל הוספת התות הביאה 9.6 גרם סוכר, צבע מאכל ושלושה תוספי מזון ומעלה. צונח ל-C כי אותו בסיס חלבון הפך לקינוח מתוק."  
**Decomposition:**  
- "צונח ל-C" → T2 grade: trace grade="C" → PASS  
- "שלושה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_3_PLUS` in `caps_applied` → PASS  
- "9.6 גרם סוכר" → T1: limitingFactors "סוכר גבוה — 9.6 גרם ל-100 גרם" → PASS  
- "10 גרם חלבון" → T1: positiveSignals "חלבון גבוה לקטגוריה — 10 גרם ל-100 גרם" → PASS  
- "ה-GO הלבן שמוביל את המדף" → T3 cross-product reference to yog-008 as the "leader". yog-008 has grade=A; see YEX-01 for the "ראש המדף" problem there, but within this string the reference is contextual, not a direct grade assertion → REVIEW  
- "הפך לקינוח מתוק" → T3 framing: NOVA4 + ADDITIVE_3_PLUS + sugar cap → PASS  

**String verdict: REVIEW** (cross-product reference to yog-008 as leader requires that product's verdict to hold)

---

**[YEX-08]** `yog-011` (יוגורט קראנצ תות קורנפלק)  
**String:** insightLine — "הציון הנמוך במדף — ... חמישה תוספי מזון ומעלה, סוכר מוסף שזוהה של 9.9 גרם וחלבון של 3.6 גרם בלבד. צונח ל-D כי כמעט הכול כאן תוספת."  
**Decomposition:**  
- "הציון הנמוך במדף" → T3 superlative: trace score=36.3/D. Checking other products: `bsip1_yogurt_7290102394081` (מולר Mix) has score=56.3/C which is higher. No product lower than 36.3 appears in the yogurts traces reviewed. This is actually the lowest → PASS (superlative confirmed by corpus scan)  
- "צונח ל-D" → T2 grade: trace grade="D" → PASS  
- "חמישה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_5_PLUS` in `caps_applied` → PASS  
- "סוכר מוסף שזוהה" → T2 rule: `MULTIPLE_ADDED_SUGAR_MARKERS` in `penalties_applied` → PASS  
- "9.9 גרם" sugar → T1: limitingFactors "סוכר מוסף זוהה — 9.9 גרם סוכר ל-100 גרם" → PASS  
- "3.6 גרם חלבון" → T1: not in positiveSignals/limitingFactors → UNVERIFIABLE  
- "כמעט הכול כאן תוספת" → T3 framing: NOVA4 + ADDITIVE_5_PLUS + LONG_INGREDIENT_LIST → well-supported → PASS  

**String verdict: UNVERIFIABLE** (protein value unverifiable; remainder passes)

---

**[YEX-09]** `bsip1_yogurt_7290110565527` (דנונה PRO יוגורט 20 גר׳ חלבון, Yohananof)  
**String:** insightLine — "המוביל הבלתי מעורר ספק — 20 גרם חלבון ל-100 גרם על רכיב יחיד: חלב מפוסטר. מגיע ל-96/A: צפיפות חלבון שלא נמצאת במדף, בלי תוספות."  
**Decomposition:**  
- "מגיע ל-96/A" → T2 score+grade: trace final_score=95.6, grade="A". Math.round(95.6)=96. Grade A. → PASS  
- "20 גרם חלבון ל-100 גרם" → T1: product name contains "20 גרם חלבון" → PASS (product-name entailment)  
- "רכיב יחיד: חלב מפוסטר" → T1 ingredient count/identity: not in trace. No positiveSignals/limitingFactors confirm single-ingredient → UNVERIFIABLE  
- "המוביל הבלתי מעורר ספק" → T3 superlative: yog-001 has trace score=92.6/S. If S > A, then 92.6 (S, Shufersal pool) nominally ranks higher in grade tier. However this product (95.6/A) has a higher numeric score than yog-001 (92.6). The "מוביל" (leader) by numeric score is correctly this product → PASS (score-based leadership confirmed, 95.6 > 92.6)  
- "צפיפות חלבון שלא נמצאת במדף" → T3 superlative on protein density: 20g/100g vs next highest products (~12.5g). Strongly supported by corpus scan → PASS  
- "בלי תוספות" → T1 ingredient framing: no caps for additives, NOVA=2, no ADDITIVE_* rules → PASS  

**String verdict: UNVERIFIABLE** (single-ingredient claim not verifiable from trace)

---

**[YEX-10]** `bsip1_yogurt_7290102394081` (מולר Mix קורנפלקס, Yohananof)  
**String:** insightLine — "פתיתי שוקולד ויוגורט — 13 גרם סוכר ל-100 גרם, ורכיב שני הוא שוקולד חלב. 56/C: הציון הנמוך בקטגוריה; קינוח, לא יוגורט בסיסי."  
**Decomposition:**  
- "56/C" → T2: trace final_score=56.3, grade="C". Math.round(56.3)=56. Grade C. → PASS  
- "הציון הנמוך בקטגוריה" → T3 superlative: yog-011 (יוגורט קראנצ) trace=36.3/D, which is lower. Directly contradicted by another product's trace → **HARD-FAIL**  
- "13 גרם סוכר" → T1: not in positiveSignals/limitingFactors → UNVERIFIABLE  
- "רכיב שני הוא שוקולד חלב" → T1 ingredient order: not in trace → UNVERIFIABLE  
- "קינוח, לא יוגורט בסיסי" → T3 framing: NOVA4 + ADDITIVE_3_PLUS → PASS  

**String verdict: HARD-FAIL** (lowest-in-category superlative is false per corpus scan)

---

**[YEX-11]** page-level `prologue_2`  
**String:** "היוגורטים הפשוטים של תנובה — ביו 3% וביו 1.5% — וגם נטול הלקטוז מגיעים ל-80 עד 81, כולם A: בסיס חלבי, חיידקי ביפידוס, מעט מרכיבים."  
**Decomposition:**  
- "ביו 3% מגיע ל-80 עד 81, A" → T2: yog-003 trace=80.2/A. Math.round(80.2)=80. Grade A. → PASS  
- "ביו 1.5% מגיע ל-80 עד 81, A" → T2: yog-005 trace=79.0/B. Math.round(79.0)=79. Grade B. Copy claims 80–81/A, trace is 79/B → **HARD-FAIL** (both score and grade contradict trace)  
- "נטול הלקטוז מגיע ל-80 עד 81, A" → T2: yog-002 trace=78.4/B. Math.round(78.4)=78. Grade B. Copy claims 80–81/A, trace is 78/B → **HARD-FAIL**  
- "חיידקי ביפידוס" → T1 ingredient: not in traces → UNVERIFIABLE  

**String verdict: HARD-FAIL** (two products falsely claimed as A, score range contradicts traces). **PRE-LAUNCH BLOCKER.**

---

**[YEX-12]** page-level `category_note` paragraph 2  
**String:** "שבעה יוגורטים על המדף מגיעים ל-A, והגבוה הוא 96/A. אבל אף אחד לא מגיע ל-S, גם המוביל."  
**Decomposition:**  
- "שבעה יוגורטים מגיעים ל-A" → T2 corpus count: across all 19 products, traces show A: yog-008(A), yog-004(A), yog-003(A), bsip1_yogurt_7290110565527(A) = 4 A-grade products. yog-001 = S. The count "7" is not entailed → **HARD-FAIL**  
- "אף אחד לא מגיע ל-S" → T2 negation: yog-001 trace grade="S" → **HARD-FAIL**  
- "הגבוה הוא 96/A" → T2: bsip1_yogurt_7290110565527 = 95.6/A → rounds to 96 → PASS  

**String verdict: HARD-FAIL** (A-count wrong, S-negation contradicted by trace). **PRE-LAUNCH BLOCKER.**

---

### CEREALS EXAMPLES

---

**[CEX-01]** `bsip1_cereal_5010029000061` (ויטביקס)  
**String:** insightLine — "95% חיטה, 12 גרם חלבון, 10 גרם סיבים — הכי גבוה בקטגוריה על שני הממדים."  
**Decomposition:**  
- "95% חיטה" → T1: not in trace directly, consistent with product identity. positiveSignals absent → UNVERIFIABLE  
- "12 גרם חלבון" → T1: not in positiveSignals/limitingFactors for this product → UNVERIFIABLE  
- "10 גרם סיבים" → T1: not in positiveSignals → UNVERIFIABLE  
- "הכי גבוה בקטגוריה על שני הממדים" → T3 superlative on protein AND fiber: requires corpus-wide check across all 34 cereals. Weetabix 12g protein appears plausibly highest; 10g fiber also appears among the highest in the traces reviewed. No product in the review clearly exceeds both values simultaneously → REVIEW (cannot confirm without full corpus scan; the claim is plausible but not verified from trace alone)  

**String verdict: UNVERIFIABLE** (numeric values not in trace inputs; superlative needs corpus check)

---

**[CEX-02]** `bsip1_cereal_5010029000061` (ויטביקס)  
**String:** rowVerdict — "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים; הציון המתוקן הוא 55/C. הפער האמיתי מ-ויטביקס הוא 20 נקודות. עוצר ב-B כי מועשר בוויטמינים (לא ספונטני) ו-342 קלוריות ל-100 גרם."  
**Decomposition:**  
- "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים" → T4 provenance claim about a prior version's score and the cause. No provenance field in trace. → **HARD-FAIL** (T4 zero tolerance unless explicitly documented in trace/methodology)  
- "הציון המתוקן הוא 55/C" → T2 for ליון (different product): `bsip1_cereal_5900020036407` trace=55.0/C → PASS (if we accept cross-product T2 within the same page; but this appears in ויטביקס's row, which is architecturally problematic — a product's row references another product's corrected score)  
- "הפער האמיתי מ-ויטביקס הוא 20 נקודות" → T2 arithmetic: ויטביקס trace=74.7, ליון corrected=55.0. Gap=19.7. Rounded: 20 → PASS  
- "עוצר ב-B" → T2 grade: ויטביקס trace grade="B" → PASS  
- "כי מועשר בוויטמינים (לא ספונטני)" → T2 causal: ויטביקס trace caps_applied=["NOVA_PROXY_3_PROCESSED"]. DOMINANT driver = "Binding cap=94.8 from NOVA_PROXY_3_PROCESSED". Vitamin enrichment is NOT a named cap or driver in the trace → **HARD-FAIL** (fabricated causal attribution; the real driver is NOVA processing cap)  
- "342 קלוריות ל-100 גרם" → T1: not in positiveSignals/limitingFactors → UNVERIFIABLE  

**String verdict: HARD-FAIL** (fabricated causal for grade + T4 provenance claim). **LIVE INCIDENT.**

---

**[CEX-03]** `bsip1_cereal_7290017325910` (קורנפלקס אורגני הרדוף)  
**String:** rowVerdict — "קורנפלקס אורגני עם שתי שורות רכיבים — 94% קמח תירס אורגני, בלי תוספים. יורד ל-C כי 600 מ\"ג נתרן ל-100 גרם — הסף האדום של משרד הבריאות — גבוה לקטגוריה שבה רוב המוצרים מתחת ל-200 מ\"ג."  
**Decomposition:**  
- "יורד ל-C" → T2 grade: trace grade="B" (66.3/B) → **HARD-FAIL** (copy says C, trace says B)  
- "600 מ\"ג נתרן" → T1: insightLine also states "600 מ\"ג נתרן — גבוה משמעותית." Not in positiveSignals/limitingFactors → UNVERIFIABLE  
- "הסף האדום של משרד הבריאות" → T4: `caps_applied=[]`, `penalties_applied=[]`. No ISRAELI_RED_LABEL_* rule fired. T4 authority claim with zero trace support → **HARD-FAIL**  
- "600 מ\"ג נתרן ... גרם הסף האדום" → T2 embedded in T4: claiming sodium exceeded the red-label threshold → **HARD-FAIL** (rule did not fire; T4 + T2 double fail)  
- "רוב המוצרים מתחת ל-200 מ\"ג" → T3 corpus-wide sodium claim: requires corpus scan → REVIEW  
- "94% קמח תירס אורגני" → T1: not in trace → UNVERIFIABLE  

**String verdict: HARD-FAIL** (grade contradicts trace; T4 MoH authority claim unsupported; unfired rule named as cause). **LIVE INCIDENT.**

---

**[CEX-04]** `bsip1_cereal_5900020036407` (ליון דגני שוקולד וקרמל)  
**String:** rowVerdict — "ליון: דגני שוקולד וקרמל עם 24.7 גרם סוכר ו-6.2 גרם שומן ל-100 גרם ... הציון הנכון הוא 55/C."  
**Decomposition:**  
- "הציון הנכון הוא 55/C" → T2: trace final_score=55.0, grade="C". Math.round(55.0)=55. Grade C → PASS  
- "24.7 גרם סוכר" → T1: not in positiveSignals/limitingFactors → UNVERIFIABLE  
- "ערכים שלא הועברו לגרסה הקודמת" → T4 provenance about prior pipeline run: not in trace → REVIEW (softer T4 — internal process description without external authority invocation. REVIEW rather than HARD-FAIL)  
- Caps fired: ISRAELI_RED_LABEL_1_SUGAR confirmed in caps_applied, consistent with 24.7g sugar being above the red-label threshold → supports the high-sugar framing  

**String verdict: REVIEW** (T4-adjacent provenance claim about prior run; numeric values unverifiable)

---

**[CEX-05]** `bsip1_cereal_7296073705574` (ריבועי דגנים עם קינמון)  
**String:** rowVerdict — "יורד ל-C כי 320 מ\"ג נתרן ל-100 גרם — גבוה לדגני בוקר, שרוב מוצריו מתחת ל-100 מ\"ג."  
**Decomposition:**  
- "יורד ל-C" → T2 grade: trace grade="D" (36.4/D) → **HARD-FAIL** (copy says C, trace says D)  
- "320 מ\"ג נתרן" → T1: insightLine confirms 320 mg sodium → PASS  
- "כי 320 מ\"ג נתרן" → T2 causal: trace DOMINANT driver = "Binding cap=55 from rules: ['HIGH_SUGAR_25G_PLUS', 'ISRAELI_RED_LABEL_1_SUGAR', 'NOVA_PROXY_3_PROCESSED']". No sodium cap fired. The grade driver is sugar + NOVA, not sodium → **HARD-FAIL** (fabricated causal attribution for grade)  
- "רוב מוצריו מתחת ל-100 מ\"ג" → T3 corpus claim: requires corpus scan → REVIEW  

**String verdict: HARD-FAIL** (grade contradicts trace; causal attribution fabricated). **LIVE INCIDENT.**

---

**[CEX-06]** `bsip1_cereal_884912126115` (דגני גרייט גריינס דייטס)  
**String:** rowVerdict — "D כי BHT (E321) ברשימה — נוגד חמצון שנוי במחלוקת; הציון מגביל בקטגוריה הישראלית."  
**Decomposition:**  
- "D כי BHT" → T2 grade + causal: trace grade="E" (34.7/E) → **HARD-FAIL** (copy says D, trace says E)  
- "BHT (E321) ברשימה" → T1 ingredient: not in trace → UNVERIFIABLE  
- "הציון מגביל בקטגוריה הישראלית" → T4: undefined authority ("הקטגוריה הישראלית" = context claim but not a named threshold). REVIEW.  
- ACTUAL trace drivers: HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_4_ULTRA_PROCESSED + multiple sugar markers + long list + seed oil. BHT is NOT a named BSIP2 rule — it is not in any fired cap or penalty. The copy attributes the grade to BHT but BHT did not fire → T2 HARD-FAIL (fabricated driver)  

**String verdict: HARD-FAIL** (grade E vs copy D; fabricated causal attribution to BHT). **LIVE INCIDENT.**

---

**[CEX-07]** `bsip1_cereal_7297488098688` (פצפוצי אורז ללת"ס)  
**String:** insightLine — "100% אורז מלא, אפס סוכר ואפס מלח — 71 מ\"ג נתרן."  
**Decomposition:**  
- "100% אורז מלא" → T1: not in trace → UNVERIFIABLE  
- "אפס סוכר" → T1: no sugar penalties/caps in trace, NOVA_PROXY_3_PROCESSED cap only → consistent but not explicitly stated in positiveSignals → UNVERIFIABLE  
- "71 מ\"ג נתרן" → T1: not in positiveSignals/limitingFactors → UNVERIFIABLE  

**String verdict: UNVERIFIABLE** (all numeric/ingredient claims unverifiable from trace)

---

**[CEX-08]** `bsip1_cereal_7613037686906` (Fitness almond honey — NO TRACE)  
**String:** rowVerdict — "עוצר ב-B כי הפרופיל סביר, אך הסוכר המוסף בולט לצד שם ה'פיטנס'."  
**Decomposition:**  
- "עוצר ב-B" → T2 grade: `trace_found=false`, `trace_summary=null` → **UNVERIFIABLE** (no trace)  
- "10 גרם חלבון, 7.7 גרם סיבים" → T1: no trace → UNVERIFIABLE  
- All strings → UNVERIFIABLE  

**String verdict: UNVERIFIABLE** — ship blocker. **LIVE INCIDENT** (product has no trace in any available run).

---

## 8. Summary of Current Findings

### YOGURTS — Pre-Launch Blockers

**HARD-FAILs (launch must not proceed without resolution):**

| # | Product ID | String field | Claim | Trace evidence | Type |
|---|-----------|-------------|-------|----------------|------|
| YHF-01 | yog-001 | insightLine | "מגיע ל-A" | trace grade=S | T2 |
| YHF-02 | yog-001 | insightLine | "לא מזכה ב-S" | trace grade=S | T2 negation |
| YHF-03 | yog-005 | insightLine | "מגיע ל-A" | trace grade=B | T2 |
| YHF-04 | yog-002 | insightLine | "מגיע ל-A ... בתחתית קבוצת ה-A" | trace grade=B | T2 |
| YHF-05 | prologue_1 | page string | "שבעה יוגורטים מגיעים ל-A" | 4 A-grade products in traces; 1 is S | T2 count |
| YHF-06 | prologue_2 | page string | "ביו 1.5% מגיעים ל-80 עד 81, כולם A" | yog-005 trace=79/B | T2 score + grade |
| YHF-07 | prologue_2 | page string | "נטול הלקטוז מגיעים ל-80 עד 81, כולם A" | yog-002 trace=78/B | T2 score + grade |
| YHF-08 | category_note ¶2 | page string | "שבעה יוגורטים מגיעים ל-A" | same as YHF-05 | T2 count |
| YHF-09 | category_note ¶2 | page string | "אף אחד לא מגיע ל-S" | yog-001 trace=S | T2 negation |
| YHF-10 | yog-008 | insightLine | "ראש המדף" | yog-001 trace=S/92.6 > A/89.9 | T3 superlative |
| YHF-11 | bsip1_yogurt_7290102394081 | insightLine | "הציון הנמוך בקטגוריה" | yog-011 trace=36.3/D < 56.3 | T3 superlative |

**Root cause of YHF-01 through YHF-09:** The copy was authored against the pre-TASK-249 run state (`run_yogurt_006_recal_p0_trim`). TASK-249 remediated NOVA classifications — several products that were A in the old run became B in the remediated run (NOVA_PROXY_3_PROCESSED cap fired). yog-001 gained S in the remediated run (score rose to 92.6 from 87.0). The copy was never updated to reflect the remediated traces.

**REVIEWs (human queue before launch):**
- All "תרביות חיות" (live cultures) T2 fermentation claims — null in traces, SECONDARY evidence from SUPERSEDED run record only
- prologue_2 "יוגורט עיזים נשאר ב-77/B" — trace=75.3/B, score 77 ≠ 75
- prologue_3 "יווני 8% עוצר ב-79/B" — trace=75.5/B, score 79 ≠ 76
- Multiple per-product T1 claims (protein values, ingredient counts, culture names) — UNVERIFIABLE from trace

---

### CEREALS — Live Incidents

**HARD-FAILs (active on live site):**

| # | Product ID | String field | Claim | Trace evidence | Type |
|---|-----------|-------------|-------|----------------|------|
| CHF-01 | bsip1_cereal_7290017325910 | rowVerdict | "יורד ל-C" | trace grade=B (66.3) | T2 |
| CHF-02 | bsip1_cereal_7290017325910 | rowVerdict | "הסף האדום של משרד הבריאות" | no sodium cap fired | T4 + T2 |
| CHF-03 | bsip1_cereal_7296073705574 | rowVerdict | "יורד ל-C" | trace grade=D (36.4) | T2 |
| CHF-04 | bsip1_cereal_7296073705574 | rowVerdict | "כי 320 מ\"ג נתרן" (causal) | dominant driver = sugar caps, not sodium | T2 fabricated driver |
| CHF-05 | bsip1_cereal_884912126115 | rowVerdict | "D כי BHT" | trace grade=E; BHT not in any fired rule | T2 grade + T2 fabricated driver |
| CHF-06 | bsip1_cereal_5010029000061 | rowVerdict | "כי מועשר בוויטמינים (לא ספונטני)" | dominant driver = NOVA_PROXY_3_PROCESSED, not vitamins | T2 fabricated driver |
| CHF-07 | bsip1_cereal_5010029000061 | rowVerdict | "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים" | no provenance field in trace | T4 |

**UNVERIFIABLEs — [ALL RESOLVED 2026-06-12 via TASK-254/F1 reconstruction]**

All 8 previously NO_TRACE products now have reconstructed traces in `cereals_claims_input_v2.json`. See `run_cereals_008_reconstruction/` and `run_cereals_multiretailer_001_reconstruction/` for trace files. The UNVERIFIABLE verdicts for these products should be re-evaluated against the reconstructed traces.

| Product ID | Name | Grade claimed in copy | Recon grade | Match? |
|------------|------|-----------------------|-------------|--------|
| bsip1_cereal_7613037686906 | Fitness almond honey | B | 70/B | True |
| bsip1_cereal_7613033548192 | Nestle Fitness Dark Chocolate | B | 68/B | True |
| bsip1_cereal_5900020041142 | קורנפלקס פיטנס | B | 65/B | True |
| bsip1_cereal_3560071016074 | Corn flakes (Carrefour) | C | 61/C | True |
| bsip1_cereal_7290116537351 | כריות נוגט | C | 52/C | True |
| bsip1_cereal_4005528115218 | דגני חיטה ואורז בטעם | D | 48/D | True |
| bsip1_cereal_42400108153 | Lucky Charms | D | 44/D | True |
| bsip1_cereal_5900020046833 | Cheerios | D | 44/D | True |

**REVIEWs for cereals with run_006 traces (per instruction: grade/score mismatches = REVIEW, not HARD-FAIL, until run_008 reconstruction):**
- Any product where the copy grade matches the frontend JSON grade but differs from the run_006 trace grade — flagged REVIEW pending run_008

---

## 9. Worked Example Counts by Verdict

| Verdict | Yogurts examples | Cereals examples | Total |
|---------|-----------------|-----------------|-------|
| HARD-FAIL | YEX-01, 02, 03, 04, 10, 11, 12 | CEX-02, 03, 05, 06 | 11 |
| UNVERIFIABLE | YEX-05, 08, 09 | CEX-07, 08 | 5 |
| REVIEW | YEX-06, 07 | CEX-01, 04 | 4 |
| PASS (all claims) | — | — | 0 (most strings carry at least one UNVERIFIABLE claim) |

Note: YEX-08 strings are all UNVERIFIABLE because the product is a PASS on per-string structure but has grade claims. YEX-09 and others mix PASS claims with UNVERIFIABLE T1s, yielding a worst-case UNVERIFIABLE verdict. No string among the 20 worked examples achieves a clean all-PASS verdict — this is a finding, not a limitation of the rubric.

---

## 10. Open Questions for the Orchestrator

**OQ-01 — Copy refresh scope:** HARD-FAILs YHF-01–09 are caused by copy authored against the pre-remediation run. The fix is to update the copy to match the TASK-249 traces, not to revert the traces. Confirm: is re-authoring the yogurt prologue, category note, and per-product insight lines in scope before go-live?

**OQ-02 — S-grade on display:** yog-001 (דנונה פרו 21) shows grade=S in the TASK-249 trace. The existing copy explicitly denies S ("לא מגיע ל-S") and the category note says "אף אחד לא מגיע ל-S". Does the page currently show S for this product, or has the frontend JSON grade field been set to A manually? If the frontend shows S on the page, the category note denial of S is a live contradiction. If the frontend shows A, the frontend JSON grade field diverges from the trace — itself an integrity issue.

**OQ-03 — Fermentation T2 policy:** The rubric sets fermentation claims to REVIEW (not PASS) because the only supporting evidence is a SUPERSEDED run record. Confirm: is the SUPERSEDED run record's A_list a legally adequate secondary source for fermentation T2, or should all fermentation T2 claims be UNVERIFIABLE until the authoritative run_006 run record is regenerated?

**OQ-04 — T4 sodium threshold:** The rubric treats "הסף האדום של משרד הבריאות" for sodium as T4 HARD-FAIL when no ISRAELI_RED_LABEL_1_SODIUM rule fired. Confirm: does the BSIP2 engine have this rule wired for the cereals category? If it does but didn't fire (sodium not high enough), the copy claim is wrong. If the rule doesn't exist in cereals, the T4 claim is entirely unsupported.

**OQ-05 — BHT scoring rule:** קורנפלקס גרייט גריינס (CHF-05) copy attributes the grade drop to BHT (E321). BHT does not appear as a fired rule in the trace. Does BSIP2 encode a BHT penalty? If yes and it should have fired → data pipeline bug. If no → the copy claim is fabricated and must be rewritten as a factual T1 observation only ("BHT appears in the ingredient list") without causal attribution.

**OQ-06 — Run_008 reconstruction [RESOLVED 2026-06-12]:** Both run_cereals_008 and run_cereals_multiretailer_001 have been reconstructed (TASK-254/F1). `cereals_claims_input_v2.json` now resolves all 8 previously UNVERIFIABLE products — all 34 products have `trace_found: true`. The cereals clause in §10("until reconstruction") is now moot.

**OQ-07 — Cross-product row references:** CEX-02 (ויטביקס rowVerdict) references ליון's previous corrected score within ויטביקס's own product card. This is architecturally unusual — a product card containing a different product's score correction. This is outside the claim-entailment model (which checks per-product). Does this cross-product referencing pattern need to be governed separately?

---

## 11. Orchestrator Rulings (2026-06-12)

Answers received from the orchestrator. Each ruling closes or redirects the corresponding OQ. HARD-FAIL verdicts in §8 are unchanged unless explicitly noted here.

---

**OQ-01 CLOSED — Copy refresh method confirmed:**  
Full regeneration from the final reconciled run state. No line-by-line patching of stale copy. All yogurt consumer strings (prologue, category note, per-product insight lines) must be re-authored against the TASK-249 trace outputs as a single coherent replacement, not incremental edits.  
**Effect on §8:** YHF-01 through YHF-09 remain HARD-FAIL and block launch. Resolution path = full copy regeneration, not targeted patches.

---

**OQ-02 CLOSED — S-grade display policy confirmed:**  
The zero-S ship policy (169D trim, option b) stands. The remediated run must be regenerated under ship flags before copy is authoritatve. If S survives under the correct trim configuration, that is a Nutrition decision with owner visibility — it is not a display question.  
**Effect on §8:** YHF-01 ("מגיע ל-A") and YHF-02 ("לא מזכה ב-S") are HARD-FAIL at trace level and remain so. They resolve only after the run is regenerated under ship flags and the post-trim grade is confirmed:  
- If post-trim grade = A → YHF-01 resolves (copy says A, display says A)  
- If post-trim grade = A → YHF-02 "לא מגיע ל-S" is a Nutrition judgment call on whether it correctly describes display state (A) vs suppressed score truth (S). Out of scope for this rubric; Nutrition Agent decides.  
- If S survives trim → owner-visibility decision; YHF-01/02 remain open with escalated severity.  
**Dependency:** These two items cannot close until ship-flag run regeneration is complete and Nutrition has reviewed.

---

**OQ-03 CLOSED — Fermentation T2 policy confirmed:**  
The rubric's existing treatment is correct: SUPERSEDED run record A_list is SECONDARY evidence; fermentation T2 claims = REVIEW, not PASS. Trace-schema fix (adding `fermentation_bonus_applied` field with non-null value) is queued separately and is not in scope for this rubric.  
**Effect on §8:** No change. All fermentation claims remain REVIEW.

---

**OQ-04 CLOSED — Cereal sodium scoring rule confirmed absent:**  
No ISRAELI_RED_LABEL_1_SODIUM rule exists in the BSIP2 engine for the cereals category (TASK-189 open). Sodium in cereal copy is a displayed fact only; it is never a grade driver.  
**Effect on §8:** CHF-02 confirmed HARD-FAIL. Additional rule for future use: any cereal copy that attributes a grade penalty or cap to sodium → automatic T4+T2 HARD-FAIL until TASK-189 closes and the sodium rule is wired and fired.

---

**OQ-05 CLOSED — BHT scoring rule confirmed absent:**  
BHT (E321) is not a scored rule in BSIP2. Any grade attribution to BHT is a fabricated driver by definition.  
**Effect on §8:** CHF-05 confirmed HARD-FAIL (both grade mismatch E vs D, and fabricated BHT causal attribution). Copy fix = remove causal attribution; BHT may remain as a T1 ingredient observation ("BHT מופיע ברשימת הרכיבים") but must not be linked to grade.

---

**OQ-06 CLOSED — Run reconstruction confirmed (ratification of executing-agent edit):**  
`run_cereals_008_reconstruction` and `run_cereals_multiretailer_001_reconstruction` exist on disk. Spot-checked 4 of 8 formerly-NO_TRACE products: Fitness almond honey (70/B), Cheerios (43.7/D→44/D), קורנפלקס פיטנס (65.3/B→65/B), כריות נוגט (52.3/C→52/C) — all match values in `cereals_claims_input_v2.json`. The executing agent's modifications to §8 and the header are ratified. The "re-evaluated against reconstructed traces" qualification in §8 stands: T2 grade/score claims can now be verified; T1 ingredient/nutrition claims remain UNVERIFIABLE for products with no ingredient data in the trace.

---

**OQ-07 CLOSED — Cross-product reference rule (interim):**  
A claim in product card X about another product Y must be entailed by product Y's trace. If product Y's trace is not accessible or the claim cannot be verified against it → REVIEW. Full governance treatment deferred to rubric v2.  
**Effect on §8 and worked examples:** CEX-02 and CEX-04 cross-product reference verdicts remain REVIEW. CHF-07 (ויטביקס referencing ליון's prior score) remains HARD-FAIL on T4 provenance grounds — the cross-product framing does not change the T4 verdict; the claim invokes a prior pipeline run as a named source, which has no provenance field in either trace.

---

*Rubric authors: Nutrition Agent (Phase 1b + OQ closure). Executing-agent edits ratified 2026-06-12. No copy, traces, or engine modified. Status: RETURNED.*
