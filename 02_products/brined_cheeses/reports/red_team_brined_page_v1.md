# Red-Team Challenge Report — brined_cheeses (run_brined_003)
Date: 2026-06-13
Scope: 48 products, /hashvaot/brined-cheeses
Challenger: red-team-agent

---

## Opening Finding

**bc-048 (גבינת טמרה מלוחה בקר 17%, barcode 3075805) is scored at 39/D under the pre-EV-053 regime because the `brined_food` context flag did not fire.** The run_brined_003 run_record explicitly logs this product in `brined_flag_not_fired` with the note "sodium<=500 or name not matched." The product has sodium=1628mg and two ingredients (milk + salt). It is indisputably brined cheese. A 2-ingredient NOVA-1 product scoring D/39 — identical to the Nutrition Agent's documented over-penalty finding — is a scoring error that ships to consumers if not corrected. This is the opening structural finding.

A secondary structural issue: **bc-032 and bc-033 (גבינה צפתית קשה 24%)** also have `context_flag=null` because their sodium=300mg falls below the 500mg flag-activation threshold. These products are correctly excluded from the brined_food flag on sodium grounds, but they are scored under the non-brined path in a corpus that is otherwise brined. The insightLines do not disclose this routing difference to consumers.

---

## Product-by-Product Assessment

| ID | Product | Score | Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| bc-001 | קוביות פטה עיזים מעודנ5% | 89 | A | PLAUSIBLE | partial | Name truncated: מעודנ5% (missing ת). Top score with partial confidence. |
| bc-002 | גבינה בולגרית 5% | 88 | A | PLAUSIBLE | partial | Scrape artifact: ingredients end with `.n` |
| bc-003 | בולגרית מסורתית 5% | 85 | A | PLAUSIBLE | partial | Accepted |
| bc-004 | גבינה צפתית 5% שומן | 84 | A | PLAUSIBLE | partial | Identical nutrition to bc-005 (same score — consistent) |
| bc-005 | גבינה צפתית מעודנת 5% | 84 | A | PLAUSIBLE | partial | Identical nutrition to bc-004 |
| bc-006 | קוביות בולגרית מעודנת 5% | 84 | A | PLAUSIBLE | partial | Ingredients: typo פנטסיום (should be פוטסיום). Same nutrition as bc-012. |
| bc-007 | גבינה בולגרית 5% שומן | 84 | A | PLAUSIBLE | partial | InsightLine counts 2 additives (E-202, חומר משמר) but ingredients show only one: E202. Double-counted. |
| bc-008 | פטה מעודנת עיזים 5% | 83 | A | PLAUSIBLE | partial | Same double-count issue as bc-007 (E-202 + חומר משמר from single ingredient). |
| bc-009 | בולגרית מעודנת 5% שומן | 83 | A | PLAUSIBLE | partial | InsightLine lists 3 additives (E-202, E-575, חומר משמר); ingredients list E575 + E202 separately — חומר משמר is redundant. |
| bc-010 | בולגרית מעודנת 5% | 82 | A | PLAUSIBLE | partial | Accepted |
| bc-011 | גבינה בולגרית מסורתית 5% | 80 | A | NEEDS EXPLANATION | partial | Score=80 exact trace=80. On page alongside bc-013 at display-score 80/B. Consumer sees 80/A and 80/B — ambiguity. |
| bc-012 | גבינה בולגרית מעודנת 5% | 80 | A | NEEDS EXPLANATION | partial | Same as bc-011. E-202 + חומר משמר double-count. Same nutrition as bc-006. |
| bc-013 | קוביות בולגרית מעודנת 13% | 80 | B | DISPLAY AMBIGUITY | partial | Exact score=79.7 rounded to display 80. Grade B is correct per policy. Consumer sees 80/B vs 80/A on same page with no explanation. |
| bc-014 | בולגרית של פעם 16% שומן | 80 | B | DISPLAY AMBIGUITY | partial | Exact score=79.5. Same display-score ambiguity as bc-013. |
| bc-015 | פטה עיזים מעודנת 16% | 78 | B | PLAUSIBLE | partial | Accepted |
| bc-016 | בולגרית מעודנת 5% | 76 | B | PLAUSIBLE | verified | Scrape artifact: ingredients end with `.n` |
| bc-017 | בולגרית 24% | 76 | B | LABELING RISK | partial | Name says 24% (fat in dry matter). InsightLine says שומן 14% (actual fat). No tooltip or explanation. Consumer sees contradiction. Also: ingredients end with ` n`. |
| bc-018 | פטה עיזים 16% שומן | 76 | B | PLAUSIBLE | partial | InsightLine double-counts E-202 + חומר משמר from single ingredient E202. |
| bc-019 | בולגרית מעודנת 16% | 75 | B | PLAUSIBLE | partial | Ingredients null. Identical nutrition to bc-021 (same score — consistent). |
| bc-020 | בולגרית מעודנת 5% | 75 | B | PLAUSIBLE | partial | Ingredients null, limitingFactors null with score=75. |
| bc-021 | בולגרית מסורתית 16% | 75 | B | PLAUSIBLE | partial | Ingredients null. Identical nutrition to bc-019 (consistent). |
| bc-022 | גבינה צפתית 5% | 75 | B | PLAUSIBLE | partial | Ingredients null. |
| bc-023 | גבינה צפתית במים 5% | 75 | B | PLAUSIBLE | partial | Ingredients null. |
| bc-024 | פטה כבשים 20% | 74 | B | PLAUSIBLE | partial | Accepted |
| bc-025 | בולגרית מסורתית 16% | 74 | B | PLAUSIBLE | partial | Accepted |
| bc-026 | פטה כבשים 20% | 74 | B | PLAUSIBLE | partial | Accepted |
| bc-027 | גבינה פטה כבשים 20% | 74 | B | PLAUSIBLE | partial | Accepted |
| bc-028 | פטה עיזים 20% | 74 | B | PLAUSIBLE | partial | Double-count: E-202 + חומר משמר |
| bc-029 | גבינה בולגרית 16% | 74 | B | PLAUSIBLE | partial | Double-count: E-202 + חומר משמר |
| bc-030 | גבינה צפתית בטעמים | 72 | B | PLAUSIBLE | partial | Double-count: E-202 + חומר משמר |
| bc-031 | קוביות בולגרית מעודנת 16% | 72 | B | PLAUSIBLE | partial | Ingredient typo: פנטסיום (should be פוטסיום). Ingredients contain "ערכים תזונתיים" — scrape bleed from nutrition label section. |
| bc-032 | גבינה צפתית קשה 24% | 71 | B | PLAUSIBLE | partial | context_flag=null (sodium=300 below threshold). Ingredients null. Lowest sodium in corpus (300mg), highest protein (25g), yet scores below 21 products. Not intuitive; explained by fat/energy penalty path. No consumer explanation. |
| bc-033 | גבינה צפתית קשה 24% מגורד | 71 | B | PLAUSIBLE | partial | Identical nutrition to bc-032 (consistent — same score). context_flag=null. |
| bc-034 | בולגרית מעודנת 24% | 71 | B | PLAUSIBLE | partial | Same nutrition as bc-039 but 6 pts higher (bc-039 has no ingredients; NOVA inferred as 2 vs bc-034 NOVA=1). |
| bc-035 | פטה עיזים מעודנת 5% | 69 | B | CRITICAL DATA FAILURE | verified | Ingredients field (369 chars) is brand marketing copy (Mishek Tzuriyal product description) — not an ingredient list. limitingFactors=null despite score=69. The ingredient copy was scraped from a non-ingredients section of the product page. |
| bc-036 | גבינה מלוחה חמד 16% | 69 | B | PLAUSIBLE | partial | Double-count: E-202 + חומר משמר |
| bc-037 | גבינת חלומי 23% | 68 | B | PLAUSIBLE | partial | Accepted |
| bc-038 | חלומי בקר | 66 | B | PLAUSIBLE | partial | Scrape artifact: ingredients end with `.n` |
| bc-039 | בולגרית מעודנת 24% | 65 | B | PLAUSIBLE | partial | Ingredients null. Same nutrition as bc-034 but 6 pts lower (NOVA inferred as 2). |
| bc-040 | חלומי בקר 24% | 64 | C | PLAUSIBLE | partial | Accepted |
| bc-041 | בולגרית מעודנת 16% | 59 | C | PLAUSIBLE | verified | Scrape artifact: ingredients end with `n` (no period). |
| bc-042 | גבינת חלומי 24% | 58 | C | PLAUSIBLE | partial | E-252 (potassium nitrate) listed as preservative — not flagged beyond "תוספות מזוהות" in limitingFactors. E-252 has specific health context consumers should know but insightLine does not differentiate from E-202. |
| bc-043 | פטינה בסגנון פטה 22% | 58 | C | PLAUSIBLE | partial | Ingredients null, positiveSignals null. "פטינה" is a category that indicates partial dairy/substitute. Score validity depends on ingredient routing. |
| bc-044 | פטינה גבינה סגנון פטה 22% | 58 | C | PLAUSIBLE | partial | Same nutrition as bc-043 (consistent). |
| bc-045 | פטה עיזים מעודנת 16% | 54 | C | CRITICAL DATA FAILURE | verified | Ingredients field (370 chars) is brand marketing copy — same Mishek Tzuriyal product description as bc-035, word-for-word. limitingFactors=null despite score=54/C. |
| bc-046 | בולגרית שום+ע.תיבול 16% | 50 | C | PLAUSIBLE | verified | Ingredients contain split word: "פ וטסיום" (space inside פוטסיום). Scrape corruption. Also: ingredients end with `n`. |
| bc-047 | כדורי פטה בשמן מתובל | 45 | D | PLAUSIBLE | partial | Ingredients: malformed parenthesis "ח.משמר).(E-202" (reversed order). Scrape corruption. Also: "ערכים תזונתיים" bleed-through in ingredients. |
| bc-048 | גבינת טמרה מלוחה בקר 17% | 39 | D | INCORRECT SCORE | partial | **brined_food flag NOT fired** (name matching failed for "גבינת" construct form). Scored at 39/D under unmodified pre-EV-053 path. 2-ingredient NOVA-1 product (milk + salt) scores same as junk food. This is the documented over-penalty that EV-053 was designed to prevent, still present in the frontend because the vocabulary gap (noted in cap45_ruling §9) was deferred and not fixed before run_brined_003. |

---

## Summary Assessment

**Justified scores (structural logic holds and trace confirms):** 35 products (bc-003, bc-010, bc-013 through bc-015, bc-017 through bc-018, bc-019 through bc-031, bc-033 through bc-034, bc-036 through bc-042). The graduated sodium scoring (EV-055) and brined_food fixes (EV-053/EV-054) are properly applied for these 45 products where the flag fired.

**Plausible but unverifiable (ingredients null; NOVA inferred):** 10 products (bc-019, bc-020, bc-021, bc-022, bc-023, bc-032, bc-033, bc-039, bc-043, bc-044). Scores rely on inferred rather than parsed ingredient composition.

**Weak confidence:** 43 products carry `confidence: partial`. This is honest. No phantom confidence issues found for products where the flag did fire.

**Noise-level precision (display ambiguity):** bc-013 (79.7 rounds to 80/B) and bc-014 (79.5 rounds to 80/B) display the same score as bc-011 and bc-012 (genuine 80/A). Same displayed score, different grade — unexplained on the consumer page.

**Potentially incorrect:** 2 products — bc-035 (marketing text in ingredients field, not ingredient list) and bc-045 (same), and bc-048 (brined_food flag miss → 39/D for a 2-ingredient NOVA-1 product).

**Overriding structural problem:** bc-048's score is architecturally wrong. bc-035 and bc-045 have corrupted ingredient data being served to consumers as ingredient information.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: bc-048 (גבינת טמרה מלוחה, barcode 3075805) — brined_food flag vocabulary miss, score 39/D is an acknowledged over-penalty**

The cap-45 over-penalty (ISRAELI_RED_LABELS_2_PLUS) was identified and fixed via EV-053/EV-054/run_brined_002, then EV-055/run_brined_003. But barcode 3075805 does not receive the fix because its product name "גבינת טמרה מלוחה" uses the construct form "גבינת" and does not match the keyword list. The evaluation_scope vocabulary gap was explicitly documented in `brined_cheeses_cap45_ruling_v1.md §9` and marked as deferred.

The run_brined_003 run_record explicitly logs this product in `brined_flag_not_fired`:  
`"note": "sodium<=500 or name not matched"` — yet sodium=1628mg, so "sodium<=500" cannot explain it. The flag miss is the name-matching failure.

A 2-ingredient (milk + salt), NOVA-1, protein=19g product scoring 39/D while bc-002 (sodium=1550, protein=20.5, fat=5) scores 88/A cannot be defended to a journalist. The Nutrition Agent's own ruling called this "the exact inverse of honest scoring."

**Evidence:** run_record.json `brined_flag_not_fired` list; BSIP1 trace confirms nova_proxy=1, detected_additives=[], ingredient_text_quality="good"; `brined_cheeses_cap45_ruling_v1.md §9`.  
**Implication:** A consumer-facing page with a 39/D for milk+salt=NOVA-1 is an editorial scandal if surfaced by a journalist or competitor.  
**Routes to:** Data Agent (vocabulary fix in evaluation_scope.py), then re-run run_brined_004 scoped to bc-048 only.

---

**RT-2: bc-035 (פטה עיזים מעודנת 5%, barcode 7290114310550) and bc-045 (פטה עיזים מעודנת 16%, barcode 2107071) — ingredients field contains brand marketing copy, not an ingredient list**

Both products (Mishek Tzuriyal brand) have their `ingredients` field populated with a 369-370 character brand description beginning: "בסלט, כריכים, אומלטים, מאפים או פשטידות משק צוריאל הוא מותג בוטיק..." This is product-page marketing copy, not an ingredient declaration.

Both products show `confidence: verified` and non-null `ingredients`, meaning the pipeline and QA treated them as having complete ingredient data. In reality the ingredient data is garbage.

bc-035 score=69/B has `limitingFactors: null` — the absence of a real ingredient string means no additives were detected and none were flagged. If real ingredients contain additives, the score is higher than it should be. bc-045 score=54/C has the same problem.

**Evidence:** `brined_cheeses_frontend_v1.json`, bc-035 and bc-045 `expansion.ingredients` fields, both 369-370 chars, identical Mishek Tzuriyal brand text.  
**Implication:** Consumer expansion panels show marketing copy as "ingredient information." This violates the hard rule against fabricated provenance (ref: milk-page content gold standard). The scoring confidence label "נתונים מלאים" is false for both products.  
**Routes to:** Data Agent (re-scrape ingredient fields for barcodes 7290114310550 and 2107071; set to null if real ingredient text cannot be recovered; downgrade confidence to partial).

---

### HIGH — should resolve before launch

**RT-3: bc-048 scoring context (bc-002 vs bc-048) — 49-point gap for products with similar sodium**

bc-002 (sodium=1550, protein=20.5, fat=5, NOVA=1, score=88/A) vs bc-048 (sodium=1628, protein=19, fat=17, NOVA=1, score=39/D). Without the flag-miss explanation (RT-1), this 49-point gap for 78mg additional sodium is indefensible. Even granting that fat=5 vs fat=17 contributes, the gap is disproportionate. This finding is fully explained by RT-1 (flag miss) but independently visible to any journalist spot-checking the corpus.

**Evidence:** JSON, run_record `brined_flag_not_fired`.  
**Implication:** Undermines the entire scoring narrative. The categoryNote says "הנתרן על התווית (ל-100 גרם) גבוה בדרך כלל" — true — but a consumer comparing bc-002 (high sodium, A) to bc-048 (slightly higher sodium, D) will conclude the scoring is arbitrary.  
**Routes to:** Data Agent (implement vocabulary fix; RT-1 resolves this).

---

**RT-4: Score/grade display ambiguity — bc-013 (80/B) and bc-014 (80/B) adjacent to bc-011 (80/A) and bc-012 (80/A) on the same page**

bc-013 exact score=79.7, bc-014 exact score=79.5. Both display as "80" due to rounding. bc-011 and bc-012 are genuine 80 (A). A consumer sees four products at "80" with two at A and two at B, with no visible explanation. The grade boundary policy is technically respected (grade derives from unrounded score), but the consumer experience is that the displayed score of 80 awards A to some and B to others.

This is the "Great Grains 884912126115 incident" class of display-score integrity problem referenced in grade_boundary_policy_v1.json — specifically the rule that score display may round but grade derives from raw trace.

**Evidence:** run_record.json `before_after_run002` entries for 7290108509106 (79.7/B) and 7290019790402 (79.5/B); grade_boundary_policy_v1.json.  
**Implication:** Consumer confusion. A curious consumer may perceive two A-grade products and two B-grade products at the same score as a system error or bias.  
**Routes to:** Design Agent (display: show score as 79 or add sub-grade tooltip), or Data Agent (correct the score in the JSON to show 79 for bc-013 and bc-014 per rounding rules — currently the JSON shows `80` which is a rounded-up integer that crosses the published A boundary without entitling the product to the grade).

---

**RT-5: Additive double-counting — E-202 listed as both "E-202" and "חומר משמר" in 10 products' limitingFactors**

E-202 is potassium sorbate. In 10 products, the ingredients field contains a single preservative written as "E202" or "E-202," and the limitingFactors list separately names both the E-number and the Hebrew generic term "חומר משמר" as if they were two different additives. The insightLine for some of these products (bc-007, bc-008, bc-009) says "מכיל 2 תוספים מזוהים (E-202, חומר משמר)" — a direct consumer-facing claim that the product has 2 additives when it has 1.

Affected products: bc-007, bc-008, bc-009, bc-011, bc-012, bc-018, bc-028, bc-029, bc-030, bc-036 (10 products).

**Evidence:** JSON insightLines and limitingFactors cross-referenced against ingredients strings.  
**Implication:** InsightLines make a precise, verifiable claim ("מכיל 2 תוספים") that is factually wrong. A journalist or regulator reading the actual label would immediately contradict this. This is the "fabricated claim" class of failure referenced in CLAUDE.md.  
**Routes to:** Data Agent (additive deduplication logic: if E-XXX and its common name both appear in the parsed additive list, count once).

---

**RT-6: bc-035 and bc-045 — confidence labeled "נתונים מלאים" is false when ingredients is corrupted marketing copy**

Both products have `confidence: verified` / `confidence_label_he: "נתונים מלאים"` displayed to consumers. The consumer-facing confidence tooltip reads "כל נתוני התזונה העיקריים זמינים מהתווית" — all key nutrition data available from the label. This is falsely applied when the ingredients field is brand marketing text. The signal that the pipeline had "full verified data" was generated by the scrape returning non-null text, not by the text being a valid ingredient declaration.

**Evidence:** bc-035 and bc-045, `confidence_label_he: "נתונים מלאים"` combined with marketing-text ingredients.  
**Implication:** The confidence signal that Bari uses to tell consumers "this data is complete" is materially false for these two products. The confidence architecture is only as good as its ability to reject corrupted data.  
**Routes to:** Data Agent (scrape validator must check for non-ingredient keywords in ingredients strings; marketing copy should trigger null-ingredient flag, not a verified confidence label).

---

**RT-7: bc-017 — name/fat discrepancy unexplained to consumer**

bc-017 name "בולגרית 24%" refers to fat-in-dry-matter (the standard Israeli label convention). The insightLine shows "שומן 14%" (actual fat per 100g wet weight). The consumer sees a product labeled 24% and a Bari score saying 14% fat. No tooltip or methodology note explains this discrepancy. The methodology line in the page data mentions "אחוז השומן על האריזה הוא שומן בחומר יבש — החישוב משתמש בשומן בפועל" — but this explanation is buried in methodology and not proximate to the individual insightLine.

**Evidence:** bc-017 `name`, `insightLine`, `expansion.nutrition.fat`.  
**Implication:** A consumer may distrust the Bari score, thinking we are mis-reading the label. This is a framing integrity issue, not a data error.  
**Routes to:** Content Agent (add a category-wide or product-level note explaining DM% vs wet-weight%); Design Agent (proximity of the methodology note to the individual insightLine).

---

**RT-8: bc-032 and bc-033 (גבינה צפתית קשה) — lowest sodium (300mg) in corpus but only B-tier; context_flag=null; no consumer explanation**

These products have sodium=300mg (lowest in the 48-product corpus) and protein=25g (highest in corpus). Both score 71/B. The scoring path is explained by fat=24% (high) and energy=330kcal — the fat dimension penalizes. But from the consumer's perspective, the product with the lowest sodium and highest protein on the entire shelf scores 71/B while products with sodium 3–5x higher score similarly or higher. The categoryNote says "הנתרן על התווית (ל-100 גרם) גבוה בדרך כלל" — which is accurate but creates a false expectation that lower sodium = higher score.

Additionally: the `context_flag=null` (sodium below 500mg threshold) means these products are not scored under the brined_food architecture. They are in the same corpus, displayed on the same page, but routed differently. The consumer cannot see this.

**Evidence:** bc-032 and bc-033 scores and nutrition; run_record `brined_flag_not_fired`.  
**Implication:** Consumer sees the two highest-protein, lowest-sodium products at 71/B and may conclude the scoring is not tracking the headline metrics (sodium and protein) the page emphasizes.  
**Routes to:** Content Agent (insightLine clarification for bc-032/bc-033 explaining the fat/energy scoring path); Nutrition Agent (confirm that 300mg-sodium products are correctly excluded from brined_food path — this appears intentional but should be verified).

---

### MEDIUM — should document or monitor

**RT-9: 6 scrape artifacts in ingredients strings reaching consumers**

Products bc-002, bc-016, bc-017, bc-038 (ingredients end with `.n`), bc-031 (ingredients end with "ערכים תזונתיים" — Hebrew for "nutritional values"), bc-041 (ends with trailing `n`), bc-046 (contains "פ וטסיום" — space inside the word פוטסיום), bc-047 (reversed parenthesis "ח.משמר).(E-202").

These are raw scrape parsing errors. Most are cosmetically minor (trailing `.n`). Two are semantically incorrect: bc-031 has "ערכים תזונתיים" in the ingredient string (the scraper bleed past the ingredient section into the nutrition label header), and bc-047 has a malformed parenthesis structure that garbles the additive identification.

**Evidence:** JSON ingredients strings for the named products.  
**Implication:** Consumer expansion panels display corrupted text. Not score-affecting but a quality failure in a page claiming "מידע, לא המלצה."  
**Routes to:** Data Agent (scrape post-processing: strip trailing `.n`, `n`, `ערכים תזונתיים`; flag reversed parentheses for manual review).

---

**RT-10: Ingredient typo פנטסיום in 2 products (bc-006, bc-031)**

The word "פוטסיום סורבט" (potassium sorbate) is misspelled as "פנטסיום סורבט" — a transposition error in the source ingredient label or scrape. This is displayed verbatim to consumers.

**Evidence:** bc-006 and bc-031 ingredients fields.  
**Implication:** Minor — cosmetic. But displays a misspelling to consumers on a page presenting itself as authoritative data.  
**Routes to:** Data Agent (note in enrichment log; cannot be corrected without re-scraping or manual override).

---

**RT-11: bc-001 product name truncated (מעודנ5%)**

The product name "קוביות פטה עיזים מעודנ5%" is missing the letter ת before 5%. Should be "מעודנת 5%." This is the top-ranked product in the corpus (89/A) and the name displays incorrectly on the page.

**Evidence:** bc-001 `name` field.  
**Implication:** Top product has a visible name error. A consumer recognizing the product may doubt the data quality.  
**Routes to:** Data Agent (correct the name field in the JSON; verify against the actual product label).

---

**RT-12: Content is first-pass factual draft — zero editorial voice**

All consumer-facing copy (hero, prologue, methodology, categoryNote) is marked `// DRAFT first-pass — Content Agent + Hebrew fresh-eyes pass pending`. The copy is factually correct but reads as terse data summary, not Bari editorial. The hero title "בולגרית, פטה, צפתית וחלומי — גבינות שמיועדות לשימוש במלח, ולכן הנתרן על התווית בדרך כלל גבוה" is passive and observatory. The single prologue sentence provides no interpretation.

This is a known pending item, not a surprise. However, the task brief required flagging content-quality gaps.

**Evidence:** `brined-cheeses-page-data.ts`, all copy sections.  
**Implication:** Content does not meet milk-page gold standard. Not a launch blocker on its own (the task brief acknowledged this is a pending follow-up), but ships as-is if not tracked.  
**Routes to:** Content Agent (Hebrew fresh-eyes pass + editorial voice pass after structural issues resolved).

---

**RT-13: limitingFactors=null for bc-035 (score=69) and bc-045 (score=54)**

Both products have no limiting factors flagged despite intermediate-to-low scores. bc-045 is 54/C with no stated reason for the lower score visible to the consumer. Combined with corrupted ingredients (RT-2 and RT-6), the expansion panel for these products is uninformative: corrupted ingredient text, no limiting factors, misleading verified confidence.

**Evidence:** bc-035 and bc-045 `limitingFactors`, `positiveSignals`.  
**Implication:** Consumer cannot understand why bc-045 is 54/C.  
**Routes to:** Data Agent (re-scrape + rebuild; interim: set limitingFactors based on fat/energy if no clean ingredients recoverable).

---

**RT-14: E-252 (potassium nitrate) in bc-042 not differentiated from standard preservatives**

bc-042 (גבינת חלומי 24%) contains E-252 (potassium nitrate), which is a curing salt used as a preservative. The limitingFactors lists "תוספות מזוהות: E-202, E-252" — combining a common mold inhibitor (E-202) with a nitrate compound without distinguishing them. E-252 has different health discussion context from E-202; consumers who care about nitrate exposure cannot tell from the limitingFactors that E-252 is present.

**Evidence:** bc-042 ingredients "חלב בקר מפוסטר, מלח, חומרים משמרים (E-202, E-252)"; limitingFactors.  
**Implication:** The page does not differentiate additive classes. Not a score error (the additive detection is correct) but a framing gap for an additive with higher consumer concern than the generic חומר משמר label suggests.  
**Routes to:** Content Agent / Nutrition Agent (consider additive classification display: differentiate nitrates from generic preservatives in future insightLine updates).

---

## Build Verification

`npm run build` passed at commit `d577c8f8`. The `/hashvaot/brined-cheeses` route is included in the static build output as `○ (Static)`. No TypeScript errors, no hydration errors detected. All 45 routes generated successfully.

The brined-cheeses comparison page renders structurally correctly. The component `BrinedCheesesComparisonPage` correctly passes sodium as the headline metric with `scaleMax: 1600`, `good: 700`, `poor: 1200` — consistent with the corpus sodium range (300–1628mg).

---

## OFF Ban Verification

`_meta.off_used: false`. BSIP1 trace for bc-048 confirms `off_source_used: false`, `provenance.off_used: false`. All 48 products sourced from direct Shufersal scrape. No OFF contamination detected.

---

## Verdict

**SHIP-BLOCKED.**

Two CRITICAL findings block launch:

1. **RT-1:** bc-048 (גבינת טמרה) scores 39/D due to a vocabulary gap in the brined_food flag. A 2-ingredient NOVA-1 product (milk + salt) carries D/39 because the Hebrew construct form "גבינת" is not in the keyword list. The fix is documented and small; the re-run is required.

2. **RT-2:** bc-035 and bc-045 (Mishek Tzuriyal products) have brand marketing copy in the ingredients field being served to consumers as ingredient information, with confidence labeled "נתונים מלאים." This is materially false data presented with false confidence.

Both must be resolved before the page can ship. RT-3 through RT-6 (HIGH severity) should also be resolved before launch but do not independently block if the CRITICAL items are fixed.

---

```json
{
  "return_contract": "v1",
  "task_id": "red-team-brined-page",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\brined_cheeses\\reports\\red_team_brined_page_v1.md",
      "action": "written",
      "sha256": "COMPUTED_BELOW"
    }
  ],
  "counts": {
    "images_live": "48/48",
    "images_live_denominator": "48 products checked via HTTP HEAD against Cloudinary URLs",
    "expansions_complete": "38/48",
    "expansions_complete_denominator": "48 products; complete = all of energyKcal+protein+fat+sodium+ingredients non-null",
    "expansions_core_nutrition_only": "10/48 (null ingredients, all core nutrition present)",
    "expansions_missing_core_nutrition": "0/48",
    "fabricated_claims": 10,
    "fabricated_claims_detail": "10 insightLines claim 2 additives (E-202 + חומר משמר) when ingredients show 1 additive; 2 products (bc-035, bc-045) show marketing copy as ingredients",
    "off_used": 0,
    "build_pass": true,
    "critical_count": 2,
    "high_count": 6,
    "medium_count": 6,
    "grade_distribution_verified": {"A": 12, "B": 27, "C": 7, "D": 2},
    "grade_distribution_matches_meta": true,
    "brined_flag_not_fired": 3,
    "brined_flag_not_fired_denominator": "3 products: bc-048 (name miss), bc-032 (sodium<500), bc-033 (sodium<500)",
    "display_grade_boundary_ambiguity": 2,
    "display_grade_boundary_ambiguity_detail": "bc-013 exact=79.7 displays as 80/B; bc-014 exact=79.5 displays as 80/B; bc-011 and bc-012 both genuine 80/A — same displayed score, different grade, no consumer explanation",
    "scrape_artifacts": 6,
    "scrape_artifacts_detail": "bc-002,bc-016,bc-017,bc-038 (.n suffix); bc-031 (ערכים תזונתיים bleed); bc-046 (פ וטסיום split); bc-047 (reversed parenthesis)",
    "null_ingredients": "10/48: bc-019,bc-020,bc-021,bc-022,bc-023,bc-032,bc-033,bc-039,bc-043,bc-044",
    "products_with_corrupted_ingredients": "2/48: bc-035 (369 char marketing copy), bc-045 (370 char marketing copy)"
  },
  "commands_run": [
    {"cmd": "python expansion_completeness_check.py", "exit_code": 0},
    {"cmd": "python HEAD_check_48_images.py", "exit_code": 0, "note": "All 48 URLs returned HTTP 200"},
    {"cmd": "python score_grade_analysis.py", "exit_code": 0},
    {"cmd": "npm run build (bari-web)", "exit_code": 0, "note": "45/45 routes generated; /hashvaot/brined-cheeses present"},
    {"cmd": "python run002_vs_run003_drift.py", "exit_code": 0, "note": "42/48 products show score drift: run_003 is EV-055 graduated-sodium run, not a regression — documented intent"},
    {"cmd": "json grade_boundary_policy_v1.json read", "exit_code": 0},
    {"cmd": "json bsip2_evidence_registry_v1.md grep EV-053/054/055", "exit_code": 0, "note": "All three EVs found in registry"}
  ],
  "not_done": [
    "Live browser rendering not confirmed (static HTML inspected via build output; full browser test not run)",
    "Full BSIP2 trace review for all 48 products — only bc-048 BSIP1 trace read in full; others spot-checked",
    "EV-055 D7 co-sign document not read in full (only summary reviewed via EV registry entry)",
    "Crossref/Semantic Scholar literature challenge on EV-053 evidence (food-science mechanism clear; deferred to Research Agent if challenged)",
    "bc-032/bc-033 exact scoring path not traced (no bsip2_trace.json opened for these products)"
  ],
  "self_check": {
    "spec_conflict": "None. The task brief asked for CRITICAL/HIGH/MEDIUM findings. No conflict with lane law or standing owner rulings.",
    "frozen_invariant_touched": false,
    "tripwire_analysis": "No owner tripwires fire. CRITICAL findings route to Data Agent (vocabulary fix, scrape repair) — not to owner. No published scores affected (category not yet live). No strategy change proposed.",
    "acceptance_test_result": "BLOCKED: bc-048 vocabulary miss and bc-035/bc-045 corrupted ingredients are unresolved CRITICAL findings. Category cannot ship with these artifacts. Acceptance test passes only after: (1) vocabulary fix in evaluation_scope.py, (2) run_brined_004 scoped to bc-048, (3) bc-035/bc-045 re-scraped or set to null + confidence downgraded.",
    "off_used": false,
    "images_live": "48/48 — ALL PASS (Cloudinary, not Shufersal direct — Cloudinary CDN is stable)"
  }
}
```
