# Claim-Entailment Rubric v2

**Generated:** 2026-06-12
**Supersedes:** `claim_entailment_rubric_v1.md` (v1 retained as history at same path)
**Scope:** Consumer-facing claim verification for Bari comparison pages
**Pilot category:** Yogurts (pre-go-live; findings block launch)
**Control category:** Breakfast Cereals (live; findings are active incidents)
**Input files:**
- `03_operations/claim_entailment/inputs/yogurts_claims_input_v1.json`
- `03_operations/claim_entailment/inputs/cereals_claims_input_v2.json` (all 34 products, traces reconstructed)
**Governing incident:** "official food source" fabrication shipped live → zero tolerance on unsupported T4a

**v2 changes (calibration lessons from Phase 1c):**
1. **Two-Layer Verification** (§4): score/grade claims verify against live frontend values; mechanism claims verify against trace; drift between layers = PIPELINE finding, not copy HARD-FAIL.
2. **Fermentation Split** (§7): run-record bridge support → REVIEW; neither trace nor run record → UNVERIFIABLE. Closes calibration Ambiguity 5 (which misread OQ-03 as "all fermentation UNVERIFIABLE").
3. **T4b subtype** (§2.4): internal pipeline-history claims → REVIEW default. T4a zero tolerance unchanged.
4. **Cross-Product References** (§8): full §-procedure; verify claim about product Y against Y's trace; unresolvable → REVIEW.
5. **Display-Values Inventory Spec** (§9): field list for the inventory builder; enables T1 numeric claim verification; Data Agent implements, Nutrition Agent owns the spec.

---

## 1. Purpose and Ground Law

Every factual claim in consumer copy must be entailed by that product's BSIP2 trace JSON and Bari methodology docs. Ground truth = **trace + methodology docs only**. Never external sources, general nutrition knowledge, or off-system authority claims. If the trace doesn't show it, it is not entailed — even if true in reality.

Entailment is **per `product_id`**, never per barcode. When the same barcode appears under two product_ids (e.g., barcode 7290107936309 as both `yog-007` Shufersal and `bsip1_yogurt_7290107936309` Yohananof), each instance is checked against its own trace only. Cross-instance comparisons are not valid substitutes.

**Two-layer principle (v2):** Score/grade claims have two authoritative reference points — the live display (what the consumer sees) and the BSIP2 trace (the engine's internal state). These can diverge when ship-flag trim or reconstruction drift occurs. Copy must match the display layer. The display layer must match the trace layer. When the two layers disagree, that is a pipeline finding, not a copy HARD-FAIL on its own. See §4 for the full procedure.

---

## 2. Claim Taxonomy

### T1 — Observed Fact

Label or nutrition values: protein grams, fat grams, sodium milligrams, ingredient names, additive E-numbers, serving size, fat percentage, ingredient order/position.

**Entailed iff** the exact value or ingredient appears in the trace inputs or the `display_values` spec (§9). Exact match required — do not tolerate rounding beyond the display convention.

**Verification path (v2):**
1. Check `display_values` in the inventory entry (§9) for numeric fields (protein, fat, sugar, fiber, sodium, energy, ingredient count). Match required within display rounding convention (1dp displayed = ±0.05 tolerance; integers = ±0).
2. If the `display_values` field is `null` → UNVERIFIABLE. Absence of data ≠ fabrication; null is not a HARD-FAIL.
3. For ingredient-name or position claims: check `display_values.ingredient_first`, `ingredient_percentages`, or the raw ingredient hash. If not in the inventory → UNVERIFIABLE.
4. For claims consistent with a fired BSIP2 rule (e.g., "contains additives" when ADDITIVE_3_PLUS is in `caps_applied`) → PASS without a `display_values` match.

**What the trace summary carries:** `trace_summary` does not carry the full ingredient list or nutrition panel — it carries `final_score_estimate`, `grade_estimate`, `nova_level`, caps/penalties/drivers. Explicit numeric values (protein grams, fat grams, etc.) appear in `positiveSignals` and `limitingFactors` in the input `strings` dict, sourced from the frontend data layer. For T1 claims: the claim value must match one of: (a) an explicit value in `strings.positiveSignals` or `strings.limitingFactors`, (b) be consistent with a fired BSIP2 rule, or (c) match a field in `display_values` (§9).

**When T1 is UNVERIFIABLE:** the ingredient/value is stated as fact but does not appear in any of: trace inputs, positiveSignals, limitingFactors, fired rules, or display_values. The trace cannot confirm or deny it. → UNVERIFIABLE, not PASS.

---

### T2 — Engine Conclusion

Scores, grades, fired rules, applied caps, applied penalties, and their named effects: "the fermentation bonus", "capped for sodium", "additive burden". This is the most governed type.

**Entailed iff** the rule/cap/penalty/bonus actually fired in THIS product's trace.

**Grade and score verification (v2 two-layer — see §4 for full procedure):**
- **Layer 1 (display):** `Math.round(display_score)` = stated integer; `display_grade` = stated grade. If copy matches display → Layer 1 PASS on grade/score.
- **Layer 2 (trace):** Named driver, cap, penalty, bonus claims verified against trace only.
- Score drift ≤3pts (same grade band) between display and trace → PIPELINE finding; string verdict = Layer 1 result.
- Grade-band change between display and trace → PIPELINE finding; route to Data Agent; string verdict = Layer 1 result for copy purposes.

**Procedure:**
1. Extract the grade and numeric score claim from the string.
2. Check `display_values.display_grade`. Must match exactly (A ≠ B ≠ S ≠ C etc.).
3. Check score numeric: `display_values.display_score` must equal the stated score. Tolerance: ±0.
4. Check any named driver claim: the rule/cap/penalty must appear in `caps_applied`, `penalties_applied`, or `explanation_drivers`. A rule named in copy but absent from the trace = fabrication = HARD-FAIL.
5. "Capped" claim: the rule must appear in `caps_applied`.
6. "Penalized for X" claim: must appear in `penalties_applied`.
7. "X caused the grade" or "stopped at grade Y because of X" = the named factor X must be the declared DOMINANT driver in `explanation_drivers` or appear in `caps_applied`.

**Score-display tolerance (rounding only):** `Math.round(final_score)` = stated integer. 95.6 → 96 is PASS. 79.0 → 79 vs claimed 80 = HARD-FAIL. 75.5 → 76 vs claimed 79 = HARD-FAIL. If a score is stated as a range ("80 to 81"), every product named in that range must individually satisfy the range.

---

### T3 — Grounded Interpretation

Editorial framing of T1/T2: characterizations, comparisons, value judgments, contextual observations. Examples: "the honest choice on a sweet shelf", "kinut-style without a trick", "almost everything here is an add-on".

**Entailed iff** every embedded factual anchor resolves to a T1/T2 that passes, AND the interpretation does not contradict any trace value.

**Procedure:**
1. Decompose the phrase into its embedded factual claims.
2. Verify each embedded claim as T1 or T2.
3. If all embedded T1/T2 pass → T3 PASS.
4. If any embedded T1/T2 HARD-FAILs → T3 inherits that HARD-FAIL.
5. If the interpretation stretches beyond its anchors but does not contradict any trace data → REVIEW.
6. Superlative/comparative claims ("the highest", "the lowest", "the only one that") are T3 with embedded T2. They require a corpus-wide check (all products on the same page). If not checkable from the per-product trace alone → REVIEW. If directly contradicted by another product's trace on the same page → HARD-FAIL.

**T3 examples that are always REVIEW without full corpus check:** "הכי גבוה בקטגוריה" (highest in category), "ראש המדף" (top of shelf). "מהנמוכים" (among the lowest) is softer framing — PASS if the score is genuinely low in the visible data.

---

### T4a — External Provenance / Authority

Sources, officialdom, endorsement, verifiability attestations. Recognizable Hebrew markers: "לפי משרד הבריאות", "מאושר על ידי", "הסף האדום", "רשמי", "בדיקות מעבדה", "על פי נתוני משרד", "בהתאם לתקן", "מוסמך".

**ZERO TOLERANCE.** Entailed only by explicit provenance fields in the trace or Bari methodology docs. Otherwise HARD-FAIL, always, regardless of whether the claim is factually true in the external world.

**Acceptable provenance anchors:** a named rule in `caps_applied` that encodes an authority threshold (e.g., `ISRAELI_RED_LABEL_1_SUGAR` entails the Israeli red-label sugar threshold). The rule name implicitly carries the authority reference. If the named rule did NOT fire → HARD-FAIL even if the threshold is otherwise known.

**Never acceptable as T4a evidence:** general knowledge of ministry thresholds, external databases, the reviewer's own knowledge, or "everyone knows this threshold".

**Example:** "600 mg sodium — the Ministry of Health red label threshold" → T4a. Entailed only if `ISRAELI_RED_LABEL_1_SODIUM` appears in `caps_applied` for this product. If the trace shows no sodium cap → HARD-FAIL. (No ISRAELI_RED_LABEL_1_SODIUM rule exists in the cereals BSIP2 category as of 2026-06-12, TASK-189 open — all sodium T4a claims in cereals are HARD-FAIL.)

---

### T4b — Internal Pipeline History (new in v2)

Claims about the pipeline's own prior state: prior version scores, prior run errors, data corrections, reasons for historical score changes.

**Recognized markers:** "בגרסה הקודמת", "הציון הקודם", "עקב תקלת נתונים", "נתונים שלא הועברו", "הציון המתוקן", "שגיאה בנתונים", "הציון הישן".

**Default verdict: REVIEW.** These claims describe internal system history that a human reviewer can verify through pipeline logs. They do not invoke external authority. REVIEW is appropriate: non-blocking for build intent, requiring human confirmation before final sign-off.

**HARD-FAIL escalation condition:** If the T4b claim embeds a T4a marker (e.g., "the previous version cited Ministry of Health authority for a threshold that doesn't exist") → HARD-FAIL. The T4a zero tolerance applies to the embedded external-authority claim regardless of T4b framing.

**Never PASS on its own:** A T4b claim cannot self-entail. The copy reviewer must verify the historical claim through pipeline logs or run records. If verified → PASS. If not verifiable → REVIEW persists.

**Scope boundary:** T4b applies only to claims about Bari's own pipeline history. Claims referencing another product's history on a different platform, or citing an external authority's historical position, remain T4a.

---

## 3. Verdict Codes

| Code | Meaning | Build behavior |
|------|---------|----------------|
| **PASS** | All claims in the string are entailed by trace/display | Build proceeds |
| **REVIEW** | No HARD-FAIL; interpretation stretches beyond anchors, superlative needs corpus-check, cross-run score mismatch in non-authoritative trace, T4b pipeline history claim, or cross-product unresolvable reference | Human queue; does NOT break build immediately |
| **HARD-FAIL** | At least one claim contradicts the trace or display, names an unfired rule, asserts an unobserved fact, or is an unsupported T4a | Build must break |
| **UNVERIFIABLE** | Product has no trace file, display_values field is null, or the claim type cannot be evaluated against available artifacts | Ship blocker — counted separately; means missing evidence, not fabrication |

**String-level verdict** = worst claim verdict in the string. One HARD-FAIL anywhere = the string is HARD-FAIL.

**Tie-break:** When uncertain between REVIEW and PASS → REVIEW. When uncertain between HARD-FAIL and REVIEW → HARD-FAIL. Never resolve uncertainty to PASS.

**DISPLAY-DRIFT (informational tag, not a verdict code):** When Layer 1 (display) and Layer 2 (trace) disagree on a score or grade, the string verdict is assessed against Layer 1. The drift is flagged as a DISPLAY-DRIFT annotation and routed to the Data Agent as a pipeline finding, separate from the claim verdict. DISPLAY-DRIFT does not block ship on its own — it is evidence of a rebuild requirement. A string may carry a PASS verdict and a DISPLAY-DRIFT annotation simultaneously.

---

## 4. Two-Layer Verification (new in v2)

### 4.1 The Two Layers

**Layer 1 — Display:** The value visible to the consumer on the live page.
Source: `display_values.display_score` and `display_values.display_grade` in the inventory entry (§9). If absent, fall back to the live frontend JSON grade/score fields.

**Layer 2 — Trace:** The BSIP2 engine's internal record.
Source: `trace_summary.final_score_estimate`, `trace_summary.grade_estimate`, `caps_applied`, `penalties_applied`, `explanation_drivers`.

### 4.2 Verification Order

**For T2 score/grade claims:**
1. Check copy claim against Layer 1 (display values).
2. If Layer 1 matches copy → Layer 1 PASS. Log any Layer 1/Layer 2 divergence as DISPLAY-DRIFT.
3. If Layer 1 contradicts copy → HARD-FAIL (copy tells the consumer the wrong thing, regardless of trace state).

**For T2 mechanism/driver claims (causal "כי"):**
Verify against Layer 2 (trace) only. The display layer does not carry mechanism information.
- Named unfired rule → HARD-FAIL.
- Interpretation consistent with trace drivers → REVIEW.

**For T1 numeric claims:**
Verify against `display_values` in inventory (§9).
- Null field → UNVERIFIABLE.
- Mismatch → HARD-FAIL.

### 4.3 Drift Policy

**Score drift ≤3pts, same grade band:**
Layer 1 vs Layer 2 drift ≤3 points, product remains in the same grade band (both B, or both C, etc.) → DISPLAY-DRIFT (informational). String verdict = Layer 1 result. No copy HARD-FAIL.

**Grade-band drift:**
Layer 1 grade ≠ Layer 2 grade (e.g., display=C, trace=D) → DISPLAY-DRIFT (pipeline finding). Route to Data Agent for trace re-check and possible re-ship. String verdict still = Layer 1 result for copy purposes; the drift is escalated separately.

**Ship-flag trim (yogurts 169D):**
yog-001 earns S (92.6) in the TASK-249 trace but displays as A under the zero-S ship flag. Display grade = A. Copy claiming A → Layer 1 PASS. Copy claiming S → HARD-FAIL.
"לא מגיע ל-S" when display=A: this is a Nutrition Agent judgment call (per OQ-02 ruling); the claim may correctly describe the trimmed display state even though the pre-trim trace = S. Nutrition Agent decides before launch whether this framing is appropriate.

### 4.4 When Layer 1 Source Is Unknown

If the inventory entry lacks `display_values.display_score` or `display_values.display_grade`, the verifier falls back to `trace_summary` values for the grade/score check. In this fallback case, any display-vs-trace drift remains undetected — annotate as DISPLAY-DRIFT-UNKNOWN and flag for Data Agent to populate the `display_values` fields.

---

## 5. Decomposition Procedure

Apply to every string (insightLine, rowVerdict, positiveSignal, limitingFactor, prologue, category_note paragraph, methodology line):

**Step 1 — Identify atomic claims.** Split at clause boundaries: "X גרם חלבון", "עוצר ב-Y/Z", "כי W גרם", "הסף של משרד הבריאות", "הכי גבוה בקטגוריה". One claim = one measurable assertion.

**Step 2 — Assign type** (T1 / T2 / T3 / T4a / T4b) per §2. Note: pipeline-history markers ("בגרסה הקודמת", etc.) → T4b, not T4a.

**Step 3 — Check each claim** against the appropriate source:
- T1 numeric: check `display_values` (§9); fall back to `positiveSignals`/`limitingFactors`.
- T2 grade/score: apply two-layer verification (§4.2, Layer 1 first).
- T2 causal/driver: check Layer 2 (trace) only.
- T3: decompose into embedded T1/T2 claims, verify each, apply T3 procedure.
- T4a: zero-tolerance check against trace provenance fields.
- T4b: default REVIEW; check for embedded T4a before accepting REVIEW.
- Cross-product references: apply §8 procedure.

**Step 4 — Assign per-claim verdict** (PASS / REVIEW / HARD-FAIL / UNVERIFIABLE).

**Step 5 — String verdict** = worst per-claim verdict.

**Example decomposition** — yog-011 insightLine:
"הציון הנמוך במדף — יוגורט שהפך לקינוח: תוספת קורנפלקס ושוקולד, חמישה תוספי מזון ומעלה, סוכר מוסף שזוהה של 9.9 גרם וחלבון של 3.6 גרם בלבד. צונח ל-D כי כמעט הכול כאן תוספת."
- Claim A: "הציון הנמוך במדף" → T3 superlative → corpus-wide check → PASS (yog-011 at 36.3/D is confirmed lowest in corpus)
- Claim B: "חמישה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_5_PLUS` in `caps_applied` → PASS
- Claim C: "סוכר מוסף שזוהה" → T2 rule: `MULTIPLE_ADDED_SUGAR_MARKERS` in `penalties_applied` → PASS
- Claim D: "9.9 גרם" sugar → T1: check `display_values.sugar_g_per_100g` or `limitingFactors` → PASS
- Claim E: "3.6 גרם חלבון" → T1: check `display_values.protein_g_per_100g` → UNVERIFIABLE if null
- Claim F: "צונח ל-D" → T2 grade: display grade="D" → PASS
- Claim G: "כמעט הכול כאן תוספת" → T3 framing supported by NOVA4 + ADDITIVE_5_PLUS + long ingredient list + sugar penalties → PASS
- String verdict: UNVERIFIABLE (Claim E unverifiable; no HARD-FAIL present)

---

## 6. Hebrew-Specific Guidance

### Grade and score claims

Hebrew patterns that assert a grade/score:
- "מגיע ל-A" / "מגיעים ל-A" → T2 grade assertion, must match `display_values.display_grade`
- "עוצר ב-B" / "נשאר ב-C" / "צונח ל-D" → T2 grade assertion
- "XX/Y" (numeric/letter) → T2 score + grade, both must be verified
- "הציון הוא XX" → T2 score assertion
- "נעצר ב-A: ... ולא S" → T2 assertion that grade is A AND grade is NOT S; both must match display

### S-grade and ship-flag trim

Under the zero-S ship policy (169D trim, option b), a product earning S in the trace may display as A on the page. When this applies:
- Copy claiming A → Layer 1 PASS (display=A matches).
- "ולא S" / "לא מגיע ל-S" when display=A: Nutrition Agent judgment call per OQ-02. The claim correctly describes the display state. Whether it appropriately discloses or misrepresents the trimmed score is a product decision, not a rubric verdict. Rubric verdict = REVIEW (consistent with display; interpretation open to Nutrition).
- "אף אחד לא מגיע ל-S" (page-level claim): If any product's display shows S, → HARD-FAIL. If all displays show ≤A due to trim → PASS at Layer 1; DISPLAY-DRIFT where traces show S.

### Negation traps

"לא מגיע ל-S" asserts the grade is below S. If display grade = S → HARD-FAIL. The negation is part of the claim.

"לא מזכה ב-S" (does not merit S) combined with "מגיע ל-A" assert grade=A. If display says S → both are HARD-FAIL.

### Superlatives and comparatives

Always T3 with embedded cross-product check — apply §8 for the referenced product(s):
- "הכי טוב" / "המוביל" / "ראש המדף" → REVIEW, requires corpus sort
- "הציון הנמוך" / "הנמוך ביותר" → REVIEW if corpus sort not done; HARD-FAIL if another product's trace shows a lower score
- "הכי גבוה" on a numeric value → requires checking all other products' traces

### Causal attribution ("כי")

"כי" introduces an explanation. In "עוצר ב-B כי מועשר בוויטמינים" — the cause must appear in the trace as a fired dominant driver. Vitamin enrichment is not a BSIP2 scoring factor; if the real driver is `NOVA_PROXY_3_PROCESSED`, attributing the grade to vitamin enrichment is a T2 fabrication → HARD-FAIL.

### Ministry/authority implicatures

"הסף האדום" (the red label) invokes the Israeli MoH thresholds. Requires the corresponding `ISRAELI_RED_LABEL_*` rule to have fired in `caps_applied` for this product. If the rule did not fire → T4a HARD-FAIL.

Note: `ISRAELI_RED_LABEL_1_SODIUM` is not wired in the BSIP2 cereals category as of 2026-06-12 (TASK-189 open). All sodium T4a claims in cereals are therefore HARD-FAIL until TASK-189 closes and the rule is wired and confirmed fired.

### "היחיד ש..." (the only one that...)

Claims uniqueness across the category. T3 with embedded T2. Requires corpus-wide negative check → REVIEW until corpus-checked.

### Confidence label claims

"ערכי הסוכר לא היו זמינים" → T1 fact about data availability. Entailed by `strings.confidenceLabel` ∈ {"חסרים נתוני תזונה", "חסרים נתוני רכיבים"} AND by explicit `strings.unknowns` entry. If confidenceLabel says "מבוסס על נתונים מלאים" but copy claims missing data → HARD-FAIL.

---

## 7. Fermentation Bridge (Yogurts Only)

### 7.1 The Gap

`fermentation_bonus_applied` is `null` in **all** per-product BSIP2 trace files. The +8 fermentation bonus is applied at the category scoring layer, not recorded per-product. This means no per-product trace entails a fermentation claim directly.

### 7.2 Split Policy (v2 — supersedes v1 unified REVIEW policy)

The v1 rubric treated all fermentation claims as REVIEW via the run-record bridge. The Phase 1c calibration report §5.5 incorrectly generalized this to "all fermentation claims UNVERIFIABLE." The correct policy — confirmed by orchestrator OQ-03 ruling — is a two-state split:

**STATE A — Run-record bridge available → REVIEW:**

Conditions (ALL must hold):
1. The product barcode appears in the SUPERSEDED run record (`run_yogurt_006_recal_p0_trim/run_record.json`) A_list with `ferm_bonus ≠ null` AND `ferm_bonus > 0`.
2. The product's current display grade is A or S.
3. The copy claim is about the existence or effect of the fermentation bonus — NOT a specific numeric value.

All three conditions met → REVIEW. The run record is SECONDARY evidence only (it is `_status: "SUPERSEDED/REFERENCE_ONLY"`). The reviewer confirms product identity across both records before signing off.

**STATE B — No run-record bridge support → UNVERIFIABLE:**

Any of these conditions:
- Product does NOT appear in the SUPERSEDED run record A_list, OR
- `ferm_bonus` is null or 0 in the A_list entry, OR
- The SUPERSEDED run record is not accessible

→ UNVERIFIABLE. Ship blocker. Do not pass as REVIEW.

Example of STATE B: a product with `NOVA_PROXY_4_ULTRA_PROCESSED` cap where copy claims live cultures boosted the grade → UNVERIFIABLE (the product is unlikely to be in the A_list at all; even if it were, the ultra-processing cap would make the fermentation bonus claim architecturally inconsistent).

**Both states block ship** until the trace schema carries `fermentation_bonus_applied` with a non-null value in a current, non-SUPERSEDED run record. Resolution: trace-schema fix queued separately.

### 7.3 T1 Culture Ingredient Claims

"חיידקי ביפידוס" (Bifidus bacteria), "תרבית יוגורט" (yogurt culture), "חיידקי פרוביוטי" → T1 ingredient claims. These appear in the frontend data layer's ingredient enrichment (Hebrew ingredient detection) but are NOT carried by `trace_summary`. Verdict = UNVERIFIABLE unless the value appears explicitly in `strings.positiveSignals` or `strings.limitingFactors`, OR in `display_values.ingredient_list_raw` (once the display-values spec is implemented per §9).

---

## 8. Cross-Product References (new in v2)

### 8.1 Definition

A cross-product reference is any claim in product card X that makes a factual assertion about a different product Y. Examples:
- "אותם 10 גרם חלבון של ה-GO הלבן שמוביל את המדף" (yog-010 referencing yog-008's protein)
- "הפער האמיתי מ-ויטביקס הוא 20 נקודות" (ליון rowVerdict referencing ויטביקס's score)
- "ראש המדף" (implies no product ranks higher — requires checking all other traces)
- "ליון עמד על 78/B בגרסה הקודמת" (ויטביקס rowVerdict making a history claim about ליון)

Cross-product references are handled AFTER the per-product decomposition in §5. They require a second pass.

### 8.2 Verification Procedure

**Step 1 — Identify the referenced product Y.** Y may be named explicitly, described by position ("the white one", "the previous version"), or implied by a superlative ("the only one that", "the highest in the category").

**Step 2 — Determine Y's product_id.** Look up Y in the page's product list. If Y's product_id cannot be determined from available inventory → REVIEW (human can identify Y from the page). Do not escalate to HARD-FAIL on identification failure alone.

**Step 3 — Look up Y's trace.** Retrieve Y's inventory entry (`trace_summary`, `display_values`, `caps_applied`, `penalties_applied`).

**Step 4 — Verify the claim about Y:**
- Claim about Y's score/grade → two-layer verification (§4) against Y's display and trace.
- Claim about Y's mechanism/driver → Layer 2 check against Y's trace.
- Claim about Y's T1 numeric value → check Y's `display_values`.
- Claim directly contradicted by Y's trace → HARD-FAIL.
- Claim unverifiable from Y's trace (e.g., Y's trace has no record of the claimed attribute) → UNVERIFIABLE.

**Step 5 — If Y's trace is inaccessible or Y cannot be identified → REVIEW.** The human reviewer locates Y and completes verification.

**Step 6 — Pipeline-history claims about Y (T4b cross-product):** "Y scored 78/B in the previous version" → T4b → REVIEW. Apply §2.4 T4b rules against Y's pipeline history.

### 8.3 Superlative Claims (Corpus-Wide)

"הכי גבוה בקטגוריה", "ראש המדף", "הנמוך ביותר", "היחיד ש..." — these are cross-product claims against ALL products on the page.

**Procedure:**
1. Collect all product scores/grades from the inventory.
2. For "highest score" superlative: sort by `display_values.display_score` descending. The claimed product must rank first.
3. If the superlative is confirmed by corpus scan → PASS.
4. If another product's trace or display value directly contradicts the superlative → HARD-FAIL.
5. If corpus scan cannot be completed from available inventory → REVIEW.

Note: Grade-tier superlatives ("ראש המדף") are HARD-FAIL if any product has a higher NUMERIC score, regardless of grade labels. A product with score=92.6/S outranks score=89.9/A.

### 8.4 Composite Verdicts for Cross-Product Strings

A string with both per-product claims and cross-product claims receives:
- Per-product verdict: per §5 decomposition.
- Cross-product verdict: per this §8 procedure.
- **String verdict = worst of the two verdicts.**

---

## 9. Display-Values Inventory Spec (new in v2)

### 9.1 Purpose

Phase 1c calibration found 73 of 188 cereal claims (39%) UNVERIFIABLE because the inventory carried trace scores/grades but not the frontend display values. Copy states protein grams, fiber grams, sodium mg, etc. as facts, but these values appeared nowhere checkable in the claims inventory.

This section defines the required fields. The **Data Agent implements** these in the inventory builder (`_build_claims_v2.py`). The **Nutrition Agent owns the field spec only** — not the implementation.

### 9.2 Required Fields Per Inventory Entry

```json
"display_values": {
  "display_score":               null,  // integer: Math.round(final_score_estimate) from live frontend JSON
  "display_grade":               null,  // string: grade shown to consumer ("A", "B", "C", "D", "E", "S")
  "energy_kcal_per_100g":        null,  // integer or null
  "protein_g_per_100g":          null,  // float (1dp) or null — e.g. 10.5
  "fat_g_per_100g":              null,  // float (1dp) or null
  "saturated_fat_g_per_100g":    null,  // float (1dp) or null
  "carbohydrate_g_per_100g":     null,  // float (1dp) or null
  "sugar_g_per_100g":            null,  // float (1dp) or null
  "fiber_g_per_100g":            null,  // float (1dp) or null
  "sodium_mg_per_100g":          null,  // integer or null — e.g. 600
  "ingredient_count":            null,  // integer or null
  "ingredient_first":            null,  // string: name of first ingredient (Hebrew) or null
  "ingredient_percentages":      {},    // dict: {"קמח_תירס_אורגני": 94.0} or {}
  "ingredient_list_sha256":      null   // SHA-256 of full raw ingredient text (Hebrew); full text not inline
}
```

### 9.3 Source Rules

**All values from the direct product scrape (BSIP0/BSIP1 pipeline) only.**
- Never from Open Food Facts (OFF banned project-wide — banned for all Bari data, every field, every category)
- Never from external databases, USDA FDC, Tzameret, or general knowledge
- `null` is acceptable; OFF-filled is a launch blocker

**`display_score` and `display_grade`:** from the live frontend JSON for that product. Must represent what the consumer sees at time of entailment check — not the raw trace value. Under ship-flag trim (169D), `display_grade` = "A" even if `trace_summary.grade_estimate` = "S".

**`ingredient_list_sha256`:** SHA-256 of the full raw ingredient text. The full text is NOT stored inline — it would bloat inventory files significantly (some products have 300+ character ingredient strings). The hash enables audit. If the full text is needed for a T1 ingredient-name verification, the reviewer fetches it from the product's BSIP0 scrape output.

### 9.4 Null Semantics

- `null` → UNVERIFIABLE (data gap; not a fabrication finding)
- `{}` for `ingredient_percentages` → UNVERIFIABLE for any percentage claim
- A field present with a non-null value → T1 claims about that value are checkable from the inventory

### 9.5 Implementation Priority

Data Agent should populate in this order:
1. **`display_score`, `display_grade`** — unblocks two-layer verification immediately
2. **`protein_g_per_100g`, `sugar_g_per_100g`, `sodium_mg_per_100g`** — covers highest-frequency UNVERIFIABLE claim types (identified in Phase 1c: ~40 of 73 cereal UNVERIFIABLEs are these three fields)
3. Remaining macro fields (`fat`, `saturated_fat`, `fiber`, `energy`, `carbohydrate`)
4. Ingredient structure fields (`ingredient_count`, `ingredient_first`, `ingredient_percentages`, `ingredient_list_sha256`)

### 9.6 Verification Rounding Convention

T1 numeric match tolerance:
- Float fields displayed to 1dp: ±0.05 tolerance (e.g., trace=10.3g, copy "10.3g" → PASS; copy "10.2g" → HARD-FAIL)
- Integer fields (energy, sodium): ±0 tolerance
- Percentages: ±0.5% tolerance

---

## 10. Worked Examples

Format per example: **[ID] Product → String excerpt → Decomposition → Verdict → Trace evidence**

Verdicts changed from v1 are annotated **[V2 CHANGE: reason]**. All other verdicts are unchanged.

---

### YOGURTS EXAMPLES

---

**[YEX-01]** `yog-008` (יופלה GO מועשר בחלבון)
**String:** insightLine — "ראש המדף — 10 גרם חלבון, בלי סוכר מוסף שזוהה ועם תרביות חיות שמרימות את הציון. מגיע ל-A אך נעצר שם, לא S."
**Decomposition:**
- "10 גרם חלבון" → T1: `display_values.protein_g_per_100g` or `positiveSignals` ("חלבון גבוה לקטגוריה — 10 גרם ל-100 גרם") → PASS
- "בלי סוכר מוסף שזוהה" → T1: no `MULTIPLE_ADDED_SUGAR_MARKERS` in penalties, no sugar cap → PASS
- "תרביות חיות שמרימות את הציון" → T2 fermentation. `fermentation_bonus_applied=null`. SUPERSEDED A_list: `bsip1_yogurt_7290110321031` ferm_bonus=8. Current display grade=A (STATE A condition 2 met). → **REVIEW** (STATE A, SECONDARY evidence)
- "מגיע ל-A" → T2 grade: display grade="A" → PASS
- "נעצר שם, לא S" → T2 negation: display grade="A" ≠ S, so "not S" is confirmed → PASS
- "ראש המדף" → T3 superlative via §8 corpus-wide check: yog-001 display=A/92.6 (or S post-trim), bsip1_yogurt_7290110565527 display=S/95.6 — a product with a higher score exists → **HARD-FAIL**

**String verdict: HARD-FAIL** (ראש המדף contradicted by products with higher score)

---

**[YEX-02]** `yog-001` (דנונה פרו 21 חלבון 0%)
**String:** insightLine — "מגיע ל-A על שילוב נדיר של חלבון גבוה וסוכר נמוך, ונעצר שם: חלבון צפוף לבדו לא מזכה ב-S."
**Decomposition:**
- "מגיע ל-A" → T2 grade: trace grade="S", display grade under zero-S trim = "A". Under two-layer verification: if display="A" → Layer 1 PASS. **Note:** this HF resolves after ship-flag run regeneration confirms display grade. Currently YHF-01 remains HARD-FAIL pending that regeneration — the TASK-249 run has not been regenerated under ship flags yet.
- "ונעצר שם: ... לא מזכה ב-S" → T2 negation: if display=A, "not S" describes display state correctly. Nutrition Agent decision on whether this framing is appropriate (OQ-02). → REVIEW (pending regeneration; currently HARD-FAIL at trace level)
- "10.5 גרם חלבון" → T1: `positiveSignals` "10.5 גרם ל-100 גרם" → PASS
- "3.3 גרם סוכר, ללא סוכר מוסף שזוהה" → T1: `positiveSignals` "סוכר נמוך — 3.3 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS

**String verdict: HARD-FAIL** — pending ship-flag run regeneration. YHF-01 and YHF-02 remain HARD-FAIL until display grade is confirmed. **PRE-LAUNCH BLOCKER.**

---

**[YEX-03]** `yog-005` (יוגורט ביו תנובה 1.5%)
**String:** insightLine — "אותו ביו פשוט של תנובה בגרסת 1.5% שומן — אותם חיידקי ביפידוס, 5.2 גרם חלבון. מגיע ל-A על אותו בסיס פשוט."
**Decomposition:**
- "מגיע ל-A" → T2 grade: trace grade="B", display grade="B" (NOVA_PROXY_3_PROCESSED cap; no trim applied). Layer 1 = B ≠ A → **HARD-FAIL**
- "5.2 גרם חלבון" → T1: check `display_values.protein_g_per_100g` → UNVERIFIABLE if null
- "חיידקי ביפידוס" → T1 ingredient: not in positiveSignals or display_values → UNVERIFIABLE
- "1.5% שומן" → T1: positiveSignals "שומן נמוך — 1.5 גרם ל-100 גרם" → PASS

**String verdict: HARD-FAIL** (grade A contradicts display B). **PRE-LAUNCH BLOCKER.**

---

**[YEX-04]** `yog-002` (יוגורט נטול לקטוז 3% שומן)
**String:** insightLine — "מגיע ל-A על בסיס פשוט ותרביות חיות, בתחתית קבוצת ה-A: ערכי הסוכר לא היו זמינים."
**Decomposition:**
- "מגיע ל-A" → T2 grade: trace grade="B", display grade="B". Layer 1 = B ≠ A → **HARD-FAIL**
- "בתחתית קבוצת ה-A" → T2: implies product is in grade A band, display=B → **HARD-FAIL** (same violation)
- "ערכי הסוכר לא היו זמינים" → T1 confidence fact: confidenceLabel="חסרים נתוני תזונה" + unknowns lists sugar → PASS
- "תרביות חיות" → T2 fermentation: ferm_bonus_applied=null. SUPERSEDED A_list: `bsip1_yogurt_7290110328221` — not in A_list (product didn't reach A in the superseded run). → **UNVERIFIABLE** (STATE B)

**String verdict: HARD-FAIL** (grade A contradicts display B). **PRE-LAUNCH BLOCKER.**

---

**[YEX-05]** `yog-003` (יוגורט ביו תנובה 3%)
**String:** insightLine — "מהפשוטים במדף — חלב, רכיבי חלב וחיידקי ביפידוס, 5.3 גרם חלבון וסוכר נמוך של 4 גרם ללא סוכר מוסף שזוהה. מגיע ל-A בלי שום טריק חלבון."
**Decomposition:**
- "מגיע ל-A" → T2 grade: display grade="A" → PASS
- "ללא סוכר מוסף שזוהה" → T1: positiveSignals "סוכר נמוך — 4 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS
- "4 גרם סוכר" → T1: positiveSignals → PASS
- "5.3 גרם חלבון" → T1: check `display_values.protein_g_per_100g` → UNVERIFIABLE if null
- "חיידקי ביפידוס" → T1 ingredient: not in trace inputs → UNVERIFIABLE
- "בלי שום טריק חלבון" → T3 framing: no ADDITIVE_* caps, no protein-enrichment signals, consistent with NOVA=2 → PASS

**String verdict: UNVERIFIABLE** (protein value and culture presence unverifiable from trace)

---

**[YEX-06]** `yog-009` (יוגורט יווני 8%)
**String:** insightLine — "רק שלושה רכיבים — חלב, שמנת וחלבון חלב — וסוכר נמוך של 3 גרם ללא סוכר מוסף שזוהה. עוצר ב-B, מתחת לבסיסים הרזים, כי 8% שומן ו-4.8 גרם רווי מכריעים."
**Decomposition:**
- "עוצר ב-B" → T2 grade: display grade="B" → PASS
- "3 גרם סוכר" → T1: positiveSignals "סוכר נמוך — 3 גרם ל-100 גרם, ללא סוכר מוסף שזוהה" → PASS
- "4.8 גרם רווי" → T1: limitingFactors "שומן רווי גבוה — 4.8 גרם ל-100 גרם" → PASS
- "8% שומן" → T1: product name says "8%" → PASS
- "שלושה רכיבים" → T1 ingredient count: check `display_values.ingredient_count` → UNVERIFIABLE if null
- "4.8 גרם רווי מכריעים" → T2 causal: trace explanation_driver = "nutrient_density=42.5 (lowest dimension)". limitingFactors lists saturated fat. Saturated fat impacts nutrient_density. "מכריעים" is an interpretive causal consistent with limitingFactors but not literally named as the sole driver → REVIEW

**String verdict: REVIEW** (ingredient count unverifiable; interpretive causal framing)

---

**[YEX-07]** `yog-010` (יופלה GO תות)
**String:** insightLine — "אותם 10 גרם חלבון של ה-GO הלבן שמוביל את המדף — אבל הוספת התות הביאה 9.6 גרם סוכר, צבע מאכל ושלושה תוספי מזון ומעלה. צונח ל-C כי אותו בסיס חלבון הפך לקינוח מתוק."
**Decomposition:**
- "צונח ל-C" → T2 grade: display grade="C" → PASS
- "שלושה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_3_PLUS` in `caps_applied` → PASS
- "9.6 גרם סוכר" → T1: limitingFactors "סוכר גבוה — 9.6 גרם ל-100 גרם" → PASS
- "10 גרם חלבון" → T1: positiveSignals "חלבון גבוה לקטגוריה — 10 גרם ל-100 גרם" → PASS
- "ה-GO הלבן שמוביל את המדף" → T3 cross-product reference to yog-008 as "leader". Via §8: yog-008 grade=A, but corpus has S-grade products (yog-001, bsip1_7290110565527). The "leader" claim for yog-008 is contextual/informal rather than a direct grade assertion → REVIEW (cross-product superlative cannot be confirmed without full corpus sort)
- "הפך לקינוח מתוק" → T3 framing: NOVA4 + ADDITIVE_3_PLUS + sugar cap → PASS

**String verdict: REVIEW** (cross-product reference to yog-008 as leader requires corpus verification)

---

**[YEX-08]** `yog-011` (יוגורט קראנצ תות קורנפלק)
**String:** insightLine — "הציון הנמוך במדף — ... חמישה תוספי מזון ומעלה, סוכר מוסף שזוהה של 9.9 גרם וחלבון של 3.6 גרם בלבד. צונח ל-D כי כמעט הכול כאן תוספת."
**Decomposition:**
- "הציון הנמוך במדף" → T3 superlative via §8 corpus scan: trace score=36.3/D. Corpus scan confirms no product lower than 36.3 → **PASS** (superlative confirmed)
- "צונח ל-D" → T2 grade: display grade="D" → PASS
- "חמישה תוספי מזון ומעלה" → T2 rule: `ADDITIVE_MARKERS_5_PLUS` in `caps_applied` → PASS
- "סוכר מוסף שזוהה" → T2 rule: `MULTIPLE_ADDED_SUGAR_MARKERS` in `penalties_applied` → PASS
- "9.9 גרם" sugar → T1: limitingFactors "סוכר מוסף זוהה — 9.9 גרם סוכר ל-100 גרם" → PASS
- "3.6 גרם חלבון" → T1: check `display_values.protein_g_per_100g` → UNVERIFIABLE if null
- "כמעט הכול כאן תוספת" → T3 framing: NOVA4 + ADDITIVE_5_PLUS + LONG_INGREDIENT_LIST → PASS

**String verdict: UNVERIFIABLE** (protein value unverifiable; remainder passes)

---

**[YEX-09]** `bsip1_yogurt_7290110565527` (דנונה PRO יוגורט 20 גר׳ חלבון, Yohananof)
**String:** insightLine — "המוביל הבלתי מעורר ספק — 20 גרם חלבון ל-100 גרם על רכיב יחיד: חלב מפוסטר. מגיע ל-96/A: צפיפות חלבון שלא נמצאת במדף, בלי תוספות."

**Note (v2):** This product has trace grade="S" (95.6). Under the zero-S ship policy, display grade = "A". If display="A", then "96/A" is Layer 1 PASS. The grade claim in copy would be consistent with the trimmed display. However, this is contingent on ship-flag run regeneration — the same dependency as YHF-01/02. Currently HARD-FAIL pending confirmation.

**Decomposition:**
- "מגיע ל-96/A" → T2: if display="A" and display_score=96 → PASS (Layer 1). Currently HARD-FAIL at trace level (trace=S). Resolves after ship-flag regeneration.
- "20 גרם חלבון ל-100 גרם" → T1: product name contains "20 גרם חלבון" → PASS
- "רכיב יחיד: חלב מפוסטר" → T1 ingredient count/identity: check `display_values.ingredient_count` → UNVERIFIABLE if null
- "המוביל הבלתי מעורר ספק" → T3 superlative via §8 corpus scan: display score=96 (if trimmed) vs yog-001=96 (also 95.6→96). Tied. "Undisputed leader" — REVIEW if tied.
- "צפיפות חלבון שלא נמצאת במדף" → T3 superlative on protein density: 20g/100g strongly supported → PASS
- "בלי תוספות" → T1: no ADDITIVE_* rules, NOVA=2 → PASS

**String verdict: HARD-FAIL** (pending ship-flag regeneration; grade/score claim resolves to REVIEW after regeneration confirms display)

---

**[YEX-10]** `bsip1_yogurt_7290102394081` (מולר Mix קורנפלקס, Yohananof)
**String:** insightLine — "פתיתי שוקולד ויוגורט — 13 גרם סוכר ל-100 גרם, ורכיב שני הוא שוקולד חלב. 56/C: הציון הנמוך בקטגוריה; קינוח, לא יוגורט בסיסי."
**Decomposition:**
- "56/C" → T2: display score=56, display grade="C" → PASS
- "הציון הנמוך בקטגוריה" → T3 superlative via §8 corpus scan: yog-011 trace=36.3/D, which is lower → **HARD-FAIL** (superlative contradicted by another product)
- "13 גרם סוכר" → T1: check `display_values.sugar_g_per_100g` → UNVERIFIABLE if null
- "רכיב שני הוא שוקולד חלב" → T1 ingredient order: check `display_values.ingredient_first`/ingredient structure → UNVERIFIABLE if null
- "קינוח, לא יוגורט בסיסי" → T3 framing: NOVA4 + ADDITIVE_3_PLUS → PASS

**String verdict: HARD-FAIL** (lowest-in-category superlative false per corpus scan)

---

**[YEX-11]** page-level `prologue_2`
**String:** "היוגורטים הפשוטים של תנובה — ביו 3% וביו 1.5% — וגם נטול הלקטוז מגיעים ל-80 עד 81, כולם A: בסיס חלבי, חיידקי ביפידוס, מעט מרכיבים."
**Decomposition:**
- "ביו 3% מגיע ל-80 עד 81, A" → T2: yog-003 trace=80.2/A. Math.round(80.2)=80. Display grade=A → PASS
- "ביו 1.5% מגיע ל-80 עד 81, A" → T2: yog-005 trace=79.0/B. Display grade=B. Score rounds to 79 (not in range 80-81). → **HARD-FAIL** (both score and grade contradict display)
- "נטול הלקטוז מגיע ל-80 עד 81, A" → T2: yog-002 trace=78.4/B. Display grade=B. Score rounds to 78 (not in range 80-81). → **HARD-FAIL**
- "חיידקי ביפידוס" → T1 ingredient: UNVERIFIABLE

**String verdict: HARD-FAIL** (two products falsely claimed as A). **PRE-LAUNCH BLOCKER.**

---

**[YEX-12]** page-level `category_note` paragraph 2
**String:** "שבעה יוגורטים על המדף מגיעים ל-A, והגבוה הוא 96/A. אבל אף אחד לא מגיע ל-S, גם המוביל."
**Decomposition:**
- "שבעה יוגורטים מגיעים ל-A" → T2 corpus count: corpus shows yog-003(A), yog-004(A), yog-008(A) = 3 A-grade displays; yog-001 and bsip1_7290110565527 = S (or A post-trim, depending on regeneration state). Count "7" is not entailed → **HARD-FAIL**
- "אף אחד לא מגיע ל-S" → T2 negation: at trace level, two products are S. Under ship-flag trim, both would display as A. This claim resolves to PASS after regeneration if trim is applied; currently HARD-FAIL at trace level.
- "הגבוה הוא 96/A" → T2: top display score=96, grade=S or A depending on trim. Grade claim "A" depends on trim → pending regeneration.

**String verdict: HARD-FAIL** (A-count wrong; S-negation contradicted at trace level pending regeneration). **PRE-LAUNCH BLOCKER.**

---

### CEREALS EXAMPLES

---

**[CEX-01]** `bsip1_cereal_5010029000061` (ויטביקס)
**String:** insightLine — "95% חיטה, 12 גרם חלבון, 10 גרם סיבים — הכי גבוה בקטגוריה על שני הממדים."
**Decomposition:**
- "95% חיטה" → T1: check `display_values.ingredient_percentages` → UNVERIFIABLE if null
- "12 גרם חלבון" → T1: check `display_values.protein_g_per_100g` → UNVERIFIABLE if null
- "10 גרם סיבים" → T1: check `display_values.fiber_g_per_100g` → UNVERIFIABLE if null
- "הכי גבוה בקטגוריה על שני הממדים" → T3 superlative via §8 corpus-wide check on protein AND fiber. Not checkable from available inventory → REVIEW

**String verdict: UNVERIFIABLE** (numeric values not in trace inputs or display_values; superlative needs corpus check)

---

**[CEX-02]** `bsip1_cereal_5010029000061` (ויטביקס)
**String:** rowVerdict — "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים; הציון המתוקן הוא 55/C. הפער האמיתי מ-ויטביקס הוא 20 נקודות. עוצר ב-B כי מועשר בוויטמינים (לא ספונטני) ו-342 קלוריות ל-100 גרם."
**Decomposition:**
- "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים" → **T4b** (pipeline history claim about ליון). No provenance field in either ויטביקס's or ליון's trace. → **REVIEW** **[V2 CHANGE: v1 classified as T4 HARD-FAIL; v2 reclassifies as T4b internal pipeline history → REVIEW]**
- "הציון המתוקן הוא 55/C" → T2 cross-product (§8): ליון (`bsip1_cereal_5900020036407`) display score=55, grade=C. Layer 1 matches → PASS for the corrected-score claim
- "הפער האמיתי מ-ויטביקס הוא 20 נקודות" → T2 cross-product arithmetic: ויטביקס display=75, ליון display=55. Gap=20 → PASS
- "עוצר ב-B" → T2 grade: ויטביקס display grade="B" → PASS
- "כי מועשר בוויטמינים (לא ספונטני)" → T2 causal (Layer 2): ויטביקס trace caps_applied=["NOVA_PROXY_3_PROCESSED"]. DOMINANT driver = "Binding cap from NOVA_PROXY_3_PROCESSED". Vitamin enrichment is NOT a named cap or driver → **HARD-FAIL** (fabricated causal attribution; real driver is NOVA processing cap)
- "342 קלוריות ל-100 גרם" → T1: check `display_values.energy_kcal_per_100g` → UNVERIFIABLE if null

**String verdict: HARD-FAIL** (fabricated causal for grade). T4b pipeline-history claim now REVIEW rather than HARD-FAIL, but the T2 fabricated causal remains HARD-FAIL. **LIVE INCIDENT.**

---

**[CEX-03]** `bsip1_cereal_7290017325910` (קורנפלקס אורגני הרדוף)
**String:** rowVerdict — "קורנפלקס אורגני עם שתי שורות רכיבים — 94% קמח תירס אורגני, בלי תוספים. יורד ל-C כי 600 מ\"ג נתרן ל-100 גרם — הסף האדום של משרד הבריאות — גבוה לקטגוריה שבה רוב המוצרים מתחת ל-200 מ\"ג."
**Decomposition:**
- "יורד ל-C" → T2 grade: display grade="B" (trace=66.3/B, no grade-band change between display and trace). Layer 1 = B ≠ C → **HARD-FAIL**
- "600 מ\"ג נתרן" → T1: check `display_values.sodium_mg_per_100g` → UNVERIFIABLE if null
- "הסף האדום של משרד הבריאות" → T4a: `caps_applied=[]`. No `ISRAELI_RED_LABEL_*` sodium rule fired. Zero tolerance → **HARD-FAIL**
- "כי 600 מ\"ג נתרן" → T2 causal (Layer 2): no sodium cap fired. OQ-04 confirmed: no `ISRAELI_RED_LABEL_1_SODIUM` exists in cereals. Sodium is not a grade driver here → **HARD-FAIL**
- "רוב המוצרים מתחת ל-200 מ\"ג" → T3 corpus sodium claim: requires corpus scan → REVIEW
- "94% קמח תירס אורגני" → T1: check `display_values.ingredient_percentages` → UNVERIFIABLE if null

**String verdict: HARD-FAIL** (grade contradicts display; T4a MoH authority unsupported; no sodium cap fired). **LIVE INCIDENT.**

---

**[CEX-04]** `bsip1_cereal_5900020036407` (ליון דגני שוקולד וקרמל)
**String:** rowVerdict — "ליון: דגני שוקולד וקרמל עם 24.7 גרם סוכר ו-6.2 גרם שומן ל-100 גרם ... הציון הנכון הוא 55/C."
**Decomposition:**
- "הציון הנכון הוא 55/C" → T2: display score=55, grade="C" → PASS
- "24.7 גרם סוכר" → T1: check `display_values.sugar_g_per_100g` → UNVERIFIABLE if null
- "ערכים שלא הועברו לגרסה הקודמת" → **T4b** (internal pipeline history). No provenance field in trace. Default → REVIEW (consistent with §2.4 T4b; confirmed in v1 as REVIEW, now explicitly T4b)
- ISRAELI_RED_LABEL_1_SUGAR confirmed in `caps_applied` → supports the high-sugar framing

**String verdict: REVIEW** (T4b pipeline-history claim; numeric values unverifiable)

---

**[CEX-05]** `bsip1_cereal_7296073705574` (ריבועי דגנים עם קינמון)
**String:** rowVerdict — "יורד ל-C כי 320 מ\"ג נתרן ל-100 גרם — גבוה לדגני בוקר, שרוב מוצריו מתחת ל-100 מ\"ג."
**Decomposition:**
- "יורד ל-C" → T2 grade: display grade="D" (trace=36.4/D; no drift — live=D, recon=D). Layer 1 = D ≠ C → **HARD-FAIL**
- "320 מ\"ג נתרן" → T1: display_values or insightLine confirms 320 mg → PASS
- "כי 320 מ\"ג נתרן" → T2 causal (Layer 2): trace DOMINANT driver = "Binding cap=55 from HIGH_SUGAR_25G_PLUS + ISRAELI_RED_LABEL_1_SUGAR + NOVA_PROXY_3_PROCESSED". No sodium cap fired → **HARD-FAIL** (fabricated causal)
- "רוב מוצריו מתחת ל-100 מ\"ג" → T3 corpus claim: requires corpus scan → REVIEW

**String verdict: HARD-FAIL** (grade contradicts display; causal attribution fabricated). **LIVE INCIDENT.**

---

**[CEX-06]** `bsip1_cereal_884912126115` (דגני גרייט גריינס דייטס)
**String:** rowVerdict — "D כי BHT (E321) ברשימה — נוגד חמצון שנוי במחלוקת; הציון מגביל בקטגוריה הישראלית."
**Decomposition:**
- "D כי BHT" → T2 grade: display grade="E" (trace=34.7/E; no drift — recon=E). Layer 1 = E ≠ D → **HARD-FAIL**
- BHT as causal → T2 causal (Layer 2): BHT (E321) is NOT a BSIP2 rule. Not in caps_applied, penalties_applied, or explanation_drivers. OQ-05 confirmed: BHT is not scored. → **HARD-FAIL** (fabricated driver)
- "BHT (E321) ברשימה" → T1 ingredient: check `display_values.ingredient_list_sha256` / ingredient raw → UNVERIFIABLE if not in display_values
- "הציון מגביל בקטגוריה הישראלית" → T4a-adjacent: "הקטגוריה הישראלית" invokes a context without a named threshold. → REVIEW

**String verdict: HARD-FAIL** (grade E vs copy D; fabricated causal attribution to BHT). **LIVE INCIDENT.**

---

**[CEX-07]** `bsip1_cereal_7297488098688` (פצפוצי אורז ללת"ס)
**String:** insightLine — "100% אורז מלא, אפס סוכר ואפס מלח — 71 מ\"ג נתרן."
**Decomposition:**
- "100% אורז מלא" → T1: check `display_values.ingredient_percentages` → UNVERIFIABLE if null
- "אפס סוכר" → T1: no sugar penalties/caps in trace, consistent but not explicit → check `display_values.sugar_g_per_100g` → UNVERIFIABLE if null
- "71 מ\"ג נתרן" → T1: check `display_values.sodium_mg_per_100g` → UNVERIFIABLE if null

**String verdict: UNVERIFIABLE** (all numeric/ingredient claims unverifiable without display_values population)

---

**[CEX-08]** `bsip1_cereal_7613037686906` (Fitness almond honey)
**String:** rowVerdict — "עוצר ב-B כי הפרופיל סביר, אך הסוכר המוסף בולט לצד שם ה'פיטנס'."
**Note (v2):** Reconstructed trace now available. Was UNVERIFIABLE in v1 (NO_TRACE). Now verifiable via `cereals_claims_input_v2.json`.
**Decomposition:**
- "עוצר ב-B" → T2 grade: reconstructed trace grade="B" (70/B). Display grade="B". Layer 1 → PASS
- "הסוכר המוסף בולט" → T2: if MULTIPLE_ADDED_SUGAR_MARKERS or similar rule fires in trace → check caps/penalties. Review reconstruction trace for sugar signal. → REVIEW (pending per-claim T1/T2 re-evaluation from reconstructed trace)

**String verdict: REVIEW** (grade claim now verifiable as PASS; sugar claim requires per-claim T1/T2 re-evaluation from reconstructed trace per §9 display_values population)

---

## 11. Summary of Current Findings

### YOGURTS — Pre-Launch Blockers

**HARD-FAILs (launch must not proceed without resolution):**

| # | Product ID | String field | Claim | Display evidence | Type |
|---|-----------|-------------|-------|----------------|------|
| YHF-01 | yog-001 | insightLine | "מגיע ל-A" | trace grade=S; display grade pending ship-flag regeneration | T2 |
| YHF-02 | yog-001 | insightLine | "לא מזכה ב-S" | trace grade=S; Nutrition judgment call post-regeneration | T2 negation |
| YHF-03 | yog-005 | insightLine | "מגיע ל-A" | display grade=B | T2 |
| YHF-04 | yog-002 | insightLine | "מגיע ל-A ... בתחתית קבוצת ה-A" | display grade=B | T2 |
| YHF-05 | prologue_1 | page string | "שבעה יוגורטים מגיעים ל-A" | 3 A-grade displays; 2 are S or A-post-trim | T2 count |
| YHF-06 | prologue_2 | page string | "ביו 1.5% מגיעים ל-80 עד 81, כולם A" | yog-005 display=79/B | T2 score + grade |
| YHF-07 | prologue_2 | page string | "נטול הלקטוז מגיעים ל-80 עד 81, כולם A" | yog-002 display=78/B | T2 score + grade |
| YHF-08 | category_note ¶2 | page string | "שבעה יוגורטים מגיעים ל-A" | same as YHF-05 | T2 count |
| YHF-09 | category_note ¶2 | page string | "אף אחד לא מגיע ל-S" | trace: two products are S; display depends on trim | T2 negation |
| YHF-10 | yog-008 | insightLine | "ראש המדף" | yog-001 and bsip1_7290110565527 have higher scores | T3 superlative |
| YHF-11 | bsip1_yogurt_7290102394081 | insightLine | "הציון הנמוך בקטגוריה" | yog-011 trace=36.3/D < 56.3 | T3 superlative |

**Additional HARD-FAILs from Phase 1c calibration (not in v1 §11):**

| # | Product ID | String field | Claim | Evidence | Type |
|---|-----------|-------------|-------|----------|------|
| YHF-12 | prologue_4 | page string | "'הכי טוב' הוא A — אבל לא S" | yog-001 and bsip1_7290110565527 trace=S | T2 |
| YHF-13 | category_note ¶2 | page string | "הגבוה הוא 96/A" | bsip1_7290110565527 trace=S/95.6 | T2 grade |
| YHF-14 | yog-004 | insightLine | "החלבון הגבוה במדף" | bsip1_7290110565527 has 20g/100g > 12.5g | T3 superlative |
| YHF-15 | yog-005 | insightLine | "בראש המדף" | product is grade=B, score=79 — not top of shelf | T3 |
| YHF-16 | bsip1_yogurt_7290110565527 | insightLine | "מגיע ל-96/A" | trace grade=S; display grade pending ship-flag regeneration | T2 |
| YHF-17 | bsip1_yogurt_7290000408316 | insightLine | "צפיפות החלבון הנמוכה מושכת אותו מטה" | DOMINANT driver=NOVA_PROXY_3_PROCESSED cap, not protein density | T2 fabricated driver |
| YHF-18 | bsip1_yogurt_7290107936309 | insightLine | "יחס שומן-חלבון גבוה מושך אותו מטה" | DOMINANT driver=NOVA_PROXY_3_PROCESSED cap, not fat-to-protein ratio | T2 fabricated driver |
| YHF-19 | bsip1_yogurt_7290102399819 | insightLine | "הסוכר הגבוה גוזר ממנו נקודות" | DOMINANT driver=NOVA_PROXY_4_ULTRA_PROCESSED cap (87.2); sugar 9.5g below any cap threshold | T2 fabricated driver |

**Root cause of YHF-01 through YHF-19:** Copy authored against pre-TASK-249 run state. TASK-249 remediated NOVA classifications — several A-grade products became B (NOVA_PROXY_3_PROCESSED cap fired); yog-001 gained S; bsip1_7290110565527 gained S. Copy never updated.

**REVIEWs (human queue before launch):**
- All "תרביות חיות" (live cultures) T2 fermentation claims — STATE A (SUPERSEDED run record evidence) or STATE B (UNVERIFIABLE)
- Prologue_2 "יוגורט עיזים נשאר ב-77/B" — trace=75.3/B, score 77 ≠ 75 (score mismatch; grade correct)
- Prologue_3 "יווני 8% עוצר ב-79/B" — trace=75.5/B, score 79 ≠ 76 (score mismatch; grade correct)

---

### CEREALS — Live Incidents

**HARD-FAILs (active on live site):**

| # | Product ID | String field | Claim | Display evidence | Type | v2 change |
|---|-----------|-------------|-------|----------------|------|-----------|
| CHF-01 | bsip1_cereal_7290017325910 | rowVerdict | "יורד ל-C" | display grade=B | T2 | — |
| CHF-02 | bsip1_cereal_7290017325910 | rowVerdict | "הסף האדום של משרד הבריאות" | no sodium cap fired; rule absent in cereals | T4a | — |
| CHF-03 | bsip1_cereal_7296073705574 | rowVerdict | "יורד ל-C" | display grade=D | T2 | — |
| CHF-04 | bsip1_cereal_7296073705574 | rowVerdict | "כי 320 מ\"ג נתרן" (causal) | dominant driver = sugar caps, not sodium | T2 fabricated | — |
| CHF-05 | bsip1_cereal_884912126115 | rowVerdict | "D כי BHT" | display grade=E; BHT not in BSIP2 | T2 grade + T2 fabricated | — |
| CHF-06 | bsip1_cereal_5010029000061 | rowVerdict | "כי מועשר בוויטמינים (לא ספונטני)" | dominant driver = NOVA_PROXY_3_PROCESSED | T2 fabricated | — |
| CHF-07 | bsip1_cereal_5010029000061 | rowVerdict | "ליון עמד על 78/B בגרסה הקודמת עקב תקלת נתונים" | no provenance field in trace | **T4b → REVIEW** | **[V2 CHANGE: was HARD-FAIL (T4); reclassified as T4b internal pipeline history → REVIEW]** |

**Additional HARD-FAILs from Phase 1c calibration:**

| # | Product ID | String field | Claim | Evidence | Type |
|---|-----------|-------------|-------|----------|------|
| CHF-08 | prologue_3 | page string | "11 ב-C" | trace count: 10 C-grade; 1 C→D drift | T2 count |
| CHF-09 | prologue_3 | page string | "אחד ב-E" | trace count: 2 E-grade (recon); copy says 1 | T2 count |
| CHF-10 | bsip1_cereal_72968 | rowVerdict | "B על בסיס הדגן המלא" | display grade=C | T2 |
| CHF-11 | bsip1_cereal_7290107647731 | rowVerdict | "עוצר ב-B תחתון" | display grade=C | T2 |
| CHF-12 | bsip1_cereal_7290112495433 | rowVerdict | "C" | display grade=D | T2 |
| CHF-13 | bsip1_cereal_7296073705550 | rowVerdict | "C" | display grade=D | T2 |
| CHF-14 | bsip1_cereal_7296073705567 | rowVerdict | "C" | display grade=D | T2 |
| CHF-15 | bsip1_cereal_7290017894911 | rowVerdict | "C" | display grade=D | T2 |
| CHF-16 | bsip1_cereal_7290017894928 | rowVerdict | "C" | display grade=D | T2 |
| CHF-17 | bsip1_cereal_7290017894904 | rowVerdict | "C" | display grade=D | T2 |
| CHF-18 | bsip1_cereal_7296073642022 | rowVerdict | "C" | display grade=D | T2 |
| CHF-19 | bsip1_cereal_7290112495228 | rowVerdict | "C" | display grade=D | T2 |
| CHF-20 | bsip1_cereal_7613030979647 | rowVerdict | "D" | display grade=E | T2 |
| CHF-21 | bsip1_cereal_72968 | rowVerdict | "הנתרן מושך כלפי מטה" | dominant driver = sugar caps (HIGH_SUGAR + NOVA); no sodium driver | T2 fabricated |

**REVIEWs for cereals (all 16 strings from Phase 1c calibration — see `calibration_v1.md` §3.2 for full list):**
- Softer T4b pipeline-history claims (CEX-04, and ליון insightLine/rowVerdict about prior run)
- T3 editorial framing claims about whole grain, sugar composition, processing level
- Children's product classification claims (no children's product field in trace)
- Page structural claims ("granola is on a separate page")

---

## 12. Worked Example Counts by Verdict

| Verdict | Yogurts examples | Cereals examples | Total |
|---------|-----------------|-----------------|-------|
| HARD-FAIL | YEX-01, 02, 03, 04, 10, 11, 12 | CEX-02, 03, 05, 06 | 11 |
| UNVERIFIABLE | YEX-05, 08, 09 | CEX-01, 07 | 5 |
| REVIEW | YEX-06, 07 | CEX-04, 08 | 4 |
| PASS (all claims) | — | — | 0 |

**v2 verdict changes from v1:**
- CEX-02 first claim ("ליון בגרסה הקודמת"): HARD-FAIL → REVIEW (T4b reclassification). String verdict remains HARD-FAIL (fabricated T2 causal).
- CHF-07 in §11: HARD-FAIL → REVIEW (T4b reclassification).
- CEX-08: UNVERIFIABLE → REVIEW (reconstructed trace now available).

---

## 13. Changelog

**v2 vs v1 (2026-06-12)**

| Change | Section | Description |
|--------|---------|-------------|
| Two-Layer Verification | §4 (new) | Score/grade claims verify against live display values; mechanism claims verify against trace; display-vs-trace drift = PIPELINE finding, not copy HARD-FAIL |
| T4b subtype | §2.4 (new) | Internal pipeline-history claims → REVIEW default; T4a zero tolerance unchanged |
| T4 → T4a rename | §2.3 (rename) | Original T4 renamed T4a for clarity; zero tolerance policy unchanged |
| Fermentation split | §7.2 (updated) | Explicit STATE A (run-record bridge → REVIEW) / STATE B (no bridge → UNVERIFIABLE). Closes calibration Ambiguity 5 which misread OQ-03 |
| Cross-Product References | §8 (new) | Full §-procedure for claims in card X about product Y; unresolvable → REVIEW |
| Display-Values Spec | §9 (new) | 14-field inventory spec enabling T1 numeric claim verification; OFF banned; Data Agent implements |
| Two-layer in T2 | §2.2 (updated) | Layer 1/Layer 2 verification path formalized in T2 procedure |
| Two-layer in T1 | §2.1 (updated) | display_values as primary T1 verification source; fallback to positiveSignals/limitingFactors |
| Decomposition Step 3 | §5 (updated) | Step 3 now routes to two-layer, T4a/T4b, cross-product procedures |
| S-grade/ship-trim guidance | §6 (updated) | Explicit Layer 1 treatment for trimmed grades; "לא מגיע ל-S" under display=A = Nutrition judgment, not HARD-FAIL |
| Additional HARD-FAILs | §11 (updated) | YHF-12 through YHF-19 (yogurts) and CHF-08 through CHF-21 (cereals) from Phase 1c calibration |
| CHF-07 verdict | §11 (updated) | HARD-FAIL → REVIEW per T4b reclassification |
| CEX-08 verdict | §10 (updated) | UNVERIFIABLE → REVIEW (reconstructed trace available) |
| CEX-02 first claim | §10 (updated) | T4 HARD-FAIL → T4b REVIEW (string verdict unchanged: still HARD-FAIL on T2 fabricated causal) |

**v1 features retained without change:**
- T1/T2/T3/T4a definitions (core procedures)
- Verdict codes (PASS/REVIEW/HARD-FAIL/UNVERIFIABLE)
- Decomposition procedure (Steps 1–5)
- Hebrew-specific guidance (§6) — extended but not overridden
- All 20 worked examples — retained with v2 annotations
- §11 Orchestrator Rulings from v1 — absorbed into v2 as standing policy; OQ answers now codified in the relevant sections

---

*Rubric authors: Nutrition Agent (Phase 1b, OQ closure, v2 calibration codification). v1 executing-agent edits ratified 2026-06-12. v2 authored 2026-06-12. No copy, traces, or engine modified.*

---

## Return Block — TASK-254 Phase 1c / P12

**Status proposed: RETURNED**

**Deliverable:** `C:\Bari\03_operations\claim_entailment\claim_entailment_rubric_v2.md`
v1 retained as history at `claim_entailment_rubric_v1.md`.

**Changelog summary (5 calibration lessons codified):**
1. §4 Two-Layer Verification — display = copy reference; trace = mechanism reference; drift = PIPELINE finding
2. §7.2 Fermentation Split — STATE A (run-record → REVIEW) / STATE B (no support → UNVERIFIABLE); closes calibration Ambiguity 5
3. §2.4 T4b — internal pipeline history claims → REVIEW; T4a zero tolerance intact
4. §8 Cross-Product References — full §-procedure; unresolvable → REVIEW; superlatives require corpus scan
5. §9 Display-Values Inventory Spec — 14 fields defined; Data Agent implements; addresses 73/188 cereal UNVERIFIABLEs

**Display-values field spec (for Data Agent):**
Priority 1: `display_score`, `display_grade` (unblocks Layer 1 verification)
Priority 2: `protein_g_per_100g`, `sugar_g_per_100g`, `sodium_mg_per_100g` (covers ~40 of 73 cereal UNVERIFIABLEs)
Priority 3: remaining macros (`fat`, `saturated_fat`, `fiber`, `energy`, `carbohydrate`)
Priority 4: ingredient fields (`ingredient_count`, `ingredient_first`, `ingredient_percentages`, `ingredient_list_sha256`)
Source rule: BSIP0/BSIP1 scrape only. OFF banned.

**Verdict changes from v1:**
- CHF-07: HARD-FAIL → REVIEW (T4b reclassification; pipeline-history claim, not external authority)
- CEX-02 first claim: HARD-FAIL → REVIEW (T4b); string verdict unchanged (T2 fabricated causal still HARD-FAIL)
- CEX-08: UNVERIFIABLE → REVIEW (reconstructed trace available; per-claim T1/T2 re-evaluation pending display_values population)

**Nothing pushed back on from the 5 orchestrator points.** One note on Point 5: `ingredient_list_raw` (full ingredient text inline) would bloat inventory files significantly; replaced with `ingredient_list_sha256` (hash for audit; full text fetched from BSIP0 scrape on demand). Functionally equivalent for verification purposes.

**Remaining open dependencies (not resolved in this rubric version):**
- Ship-flag run regeneration (OQ-02): YHF-01/02/16 cannot close until display grades confirmed post-trim
- TASK-189: cereal sodium scoring rule absent; all sodium T4a claims in cereals remain HARD-FAIL
- Trace schema fix: `fermentation_bonus_applied` field with non-null value; fermentation claims remain at best REVIEW until this lands
- Rubric v3 scope: if cereal live incidents (CHF-08 through CHF-21) require a systematic copy-remediation pass, a v3 addendum may be needed to cover the full 34-product re-evaluation once display_values fields are populated
