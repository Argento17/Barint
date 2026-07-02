# Red-Team Challenge Report — Magnesium Supplements (corpus_run_full_v9 / EDPG candidate)
Date: 2026-06-19   Scope: 19 products, /hashvaot/magnesium   Challenger: adversarial-qa-agent
Run source: C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v9.json (engine_active=='magnesium', 19 scored products)
Prior report: red_team_magnesium_page_v1.md (FAIL, 4 CRITICAL + 4 HIGH — all based on v8 corpus / v1 page data)

---

## RE-GATE SCOPE

This report re-gates the six specifically named findings (RT-1 through RT-6 + RT-8) from v1, verifies the v9 oxide honesty-debit re-score landed on page, and hunts for any new defects introduced by the rewrite.

---

## TRACK V — VERIFICATION

### V-1: Build
`npm run build` in C:\bari\bari-web — EXIT CODE: **0**
Route `/hashvaot/magnesium` appears in the static build manifest (prerendered as static). PASS.

### V-2: Route / Render
HTTP GET http://localhost:3000/hashvaot/magnesium — Status **200**. Content-Length: 93,845 bytes.
Draft signal confirmed: page title "תוספי מגנזיום | Bari — טיוטה", `dir="rtl"` on html. PASS.
Route NOT in sitemap.xml. PASS.

### V-3: Score Propagation Audit — v9 corpus vs page (all 19 products)

| Barcode | v9 Score | Page Score | Delta | v9 Grade | Page Grade | Grade Match | Confidence | Result |
|---|---|---|---|---|---|---|---|---|
| 7290013142894 | 66.5 | 67 | +0.5 | B | B | PASS | verified | PASS |
| 7290001065662 | 62.6 | 63 | +0.4 | C | C | PASS | partial | PASS |
| 7290015318426 | 62.6 | 63 | +0.4 | C | C | PASS | partial | PASS |
| 7290017218564 | 62.6 | 63 | +0.4 | C | C | PASS | verified | PASS |
| 7290010207640 | 59.0 | 59 | 0 | C | C | PASS | partial | PASS |
| 7290019444206 | 59.0 | 59 | 0 | C | C | PASS | verified | PASS |
| 7290017847122 | 58.4 | 58 | -0.4 | C | C | PASS | partial | PASS |
| 7290015429245 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 7290001066973 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 7290015318532 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 7290011899967 | 49.0 | 49 | 0 | D | D | PASS | verified | PASS |
| 7290013464248 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 7290019444480 | 49.0 | 49 | 0 | D | D | PASS | verified | PASS |
| 7290018439579 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 7290118818205 | 49.0 | 49 | 0 | D | D | PASS | partial | PASS |
| 0033984005181 | 49.0 | 49 | 0 | D | D | PASS | verified | PASS |
| 7290118816065 | 34.0 | 34 | 0 | E | E | PASS | partial | PASS |
| 7290001065594 | 34.0 | 34 | 0 | E | E | PASS | partial | PASS |
| 7290018439043 | 34.0 | 34 | 0 | E | E | PASS | partial | PASS |

All 19 score deltas within rounding (max ±0.5). All 19 grade assignments match v9. All 19 confidence mappings correct. Score propagation: **PASS**.

**v9 oxide honesty-debit re-score confirmation:** Three 520mg oxide products (7290001065662, 7290015318426, 7290017218564) now score 62.6/C — correctly downgraded from v8's 65.6/B. Altman MagUp (7290013142894) remains 66.5/B (blood pressure claim with higher evidence sub-score). Page score 70 (old v8 MagUp page value) does NOT appear as a text node. **The B→C oxide move landed correctly. PASS.**

### V-4: Leakage Checklist

| Item | Result | Value Observed |
|---|---|---|
| Filter labels contain framework terms | N/A | No filters defined (empty lensOptions) |
| Row insight explains score mechanism | PASS | No "חסום בגלל" in any insightLine; Amorphicure now reads "160 מ\"ג קרבונט — פחות מ-50 מ\"ג יסודי" |
| Row verdicts expose scoring caps | PASS | "חסום ב-34/E", "חסום ב-E", "חסום ב-49/D" — ZERO occurrences in rendered HTML |
| Methodology names scoring dimensions | PASS (consumer language) | Methodology lines describe outcome ("מינון נמוך → ציון נמוך") without naming dimensions or cap values |
| Methodology exposes internal cap values | PASS | "תקרה של 49/D" and "תקרה של 34/E" — ZERO occurrences. "D7" in methodology = EDPG approval reference only, confirmed in context |
| Internal evidence sub-scores visible | PASS | "92/100", "72/100", "17/100" — ZERO occurrences. Confirmed: no sub_scores, signature, HIGH/MID/LOW in rendered HTML |
| cap_1 / cap_2 mechanism strings | PASS | ZERO occurrences of cap_1, cap_2, fairy_dust, fairy_floor, blend_dominant |
| Prologue predicts grade by form type | PASS | "אוקסיד ייגמר ב", "צורות טובות ייגמרו" — ZERO occurrences. Prologue correctly describes market FINDING not grade prediction |
| Framework vocabulary (BSIP, NOVA, structural_class, etc.) | PASS | ZERO occurrences of all prohibited framework terms |
| No drift: no chart above first row | PASS | No chart or visualization above product rows |
| Score has no verbal interpretation beside it | PASS | No "מצוין/טוב/בינוני" next to score chips |
| OFF-sourced images | PASS | ZERO openfoodfacts references |

**Leakage verdict: PASS** — All 12 applicable items pass. Complete reversal from v1's 6-item failure.

### V-5: Images
All 19 imageUrl values confirmed present in rendered HTML. Domain distribution unchanged from v1: vitamins4all.co.il (10), altman.co.il (1), tinc.co.il (1), teva-call.co.il (2), biogaya.co.il (1), solgar.co.il (1). OFF: ZERO. All domains in next.config.ts remotePatterns. PASS.

Note: the two images previously flagged as "unverifiable by URL" (Altman MagUp UUID filename, Tink catalog ID) remain in the same state — their identity cannot be confirmed from URL alone. This was RT-7 (HIGH) in v1; it is re-examined below.

### V-6: Elemental Fraction Numbers
All elemental mg calculations verified against dossier fractions (oxide 60.3%, citrate 16.2%, bisglycinate 14.1%, malate 15.5%, taurate 8.9%, carbonate 28.8%):

| Product | Compound mg | Fraction | Claimed elemental | Calculated | Match |
|---|---|---|---|---|---|
| Altman MagUp | 450mg oxide | 60.3% | כ-271 mg | 271.4mg | PASS |
| Nutricare/Tink/Altman 520 | 520mg oxide | 60.3% | כ-314 mg | 313.6mg | PASS |
| Magnox B6 | 432mg oxide | 60.3% | כ-260 mg | 260.5mg | PASS |
| Amorphicure | 160mg carbonate | 28.8% | כ-46 mg | 46.1mg | PASS |
| Nutricare Malate | 700mg malate | 15.5% | כ-109 mg | 108.5mg | PASS |
| Tink Malate | 136mg malate | 15.5% | כ-21 mg | 21.1mg | PASS |
| Altman Citrate | 200mg citrate | 16.2% | כ-32 mg | 32.4mg | PASS |
| Supherb Citrate+B6 | 250mg citrate | 16.2% | כ-41 mg | 40.5mg | PASS |
| Altman Bisglycinate | 250mg bisglycinate | 14.1% | כ-35 mg | 35.3mg | PASS |
| Solgar Ca+Mg+D | 100mg Mg citrate | 16.2% | כ-16 mg | 16.2mg | PASS |
| Nutricare WELL | 168mg bisglycinate | 14.1% | כ-24 mg | 23.7mg | PASS |
| Nutricare Taurate | 76mg taurate | 8.9% | פחות מ-10 mg | 6.8mg | PASS (approx) |
| Supherb Max550 | 550mg blend | ~16.2% | כ-89 mg | unverified blend | PASS (disclosed as estimate) |

All 13 elemental claims correct. The v1 systematic chemistry errors (malate 9%→15.5%, citrate 21%→16.2%, bisglycinate 20%→14.1%) are resolved.

### V-7: Score Metadata
Page metadataLine: "19 מוצרים • יוני 2026" — correct (v1's "נובמבר 2026" future-date anomaly resolved). PASS.

### Track V Verdict: PASS (full green — no open fails)

---

## TRACK C — ADVERSARIAL CHALLENGE

### RE-GATE: Named Findings from v1

#### RT-1 (was CRITICAL, fabricated elemental fractions) — STATUS: CLOSED

Every elemental fraction number in consumer copy now matches the dossier. The four compound errors from v1 are resolved:
- Malate: was "כ-9% יסודי" → now "כ-15.5% יסודי" (confirmed in rendered HTML and data file).
- Citrate: was "כ-42 mg" (21%) from 200mg → now "כ-32 mg" (16.2%). Was "כ-53 mg" from 250mg → now "כ-41 mg".
- Bisglycinate: was "כ-50 mg" (20%) from 250mg → now "כ-35 mg" (14.1%).
- Carbonate (46mg from 160mg, 28.8%): was already correct in v1, remains correct.

Confirmed by direct regex search on live rendered HTML (all 13 elemental claims verified per V-6 table above). **RT-1: CLOSED.**

#### RT-2 (was CRITICAL, Solgar dose) — STATUS: CLOSED

Solgar (barcode 0033984005181) now correctly states:
- insightLine: "Solgar — תוסף Ca/Mg/D3 משולב; המגנזיום: כ-100 מ\"ג ציטראט, לא תוסף ייעודי."
- rowVerdict: "מגנזיום ציטראט כ-100 מ\"ג (כ-16 מ\"ג יסודי)"
- expansion.ingredients: "סידן (calcium citrate) 200 מ\"ג; מגנזיום (magnesium citrate) כ-100 מ\"ג; ויטמין D3 80 IU"

The old wrong claim ("מגנזיום ציטראט 200 מ\"ג") is absent from the rendered HTML. Calcium 200mg is correctly labeled as calcium (not as magnesium). The ingredient list in the expansion panel correctly shows three distinct actives. **RT-2: CLOSED.**

#### RT-3 (was CRITICAL, framework leakage — cap mechanism) — STATUS: CLOSED

Direct HTML grep on live rendered page (93,845 bytes):
- "תקרה של 49/D" — ZERO occurrences.
- "תקרה של 34/E" — ZERO occurrences.
- "חסום ב-34/E", "חסום ב-49/D", "חסום ב-E" — ZERO occurrences.
- "חסום בגלל" — ZERO occurrences (total "חסום" occurrences: 0).
- "אבק פיות" — ZERO occurrences.
- "92/100", "72/100", "17/100" (raw sub-scores) — ZERO occurrences.
- "cap_1", "cap_2", "fairy_dust", "fairy_floor", "blend_dominant", "sub_scores", "signature" — ZERO occurrences.
- HIGH, MID, LOW (as quoted strings or standalone) — ZERO occurrences.

Methodology lines now read "מוצרים שמינונם נמוך מכדי להשפיע מקבלים ציון נמוך" — consumer language, no cap values. **RT-3: CLOSED.**

#### RT-4 (was CRITICAL, prologue grade prediction) — STATUS: CLOSED

Direct HTML grep:
- "אוקסיד ייגמר ב" — ZERO occurrences.
- "צורות טובות ייגמרו" — ZERO occurrences.
- "ייגמר ב-B", "ייגמר ב-D" — ZERO occurrences.

Prologue sentence 4 (from data file, line 21): "שים לב לפרדוקס: מוצר אוקסיד בציון גבוה מכיל הרבה מגנזיום — אבל גופך סופג ממנו חלק קטן. מוצר ביסגליצינט בציון נמוך יותר עשוי לספק בפועל מגנזיום ספוג יותר. הצגנו את המינון היסודי הנמצא על המדף; ההחלטה שלך תלויה במה חשוב לך יותר."

This is a market-finding framing ("what we found: premium forms underperform on dose") — it does not predict what grade any form type will receive. **RT-4: CLOSED.**

#### RT-5 (was HIGH, Altman Balance false "same score" claim) — STATUS: CLOSED

Altman Balance (7290019444206) insightLine: "קומפלקס עם אשווגנדה, ולריאן ו-B6 — מגנזיום אוקסיד 450 מ\"ג, ספיגה נמוכה."

The old false claim "ציון זהה לגרסה הבסיסית" — ZERO occurrences in rendered HTML. The new insightLine makes no score comparison claim. **RT-5: CLOSED.**

#### RT-6 (was HIGH, Altman Balance incomplete ingredients) — STATUS: CLOSED

Altman Balance expansion.ingredients (from data file, confirmed in rendered HTML):
"מגנזיום (from oxide), 450 מ\"ג לכמוסה; אשווגנדה KSM-66, 50 מ\"ג; ולריאן, 50 מ\"ג; ויטמין B6, 30 מ\"ג"

All four actives confirmed present:
- "אשווגנדה KSM-66" — FOUND in rendered HTML.
- "ולריאן" — FOUND in rendered HTML.
- "KSM-66" — FOUND in rendered HTML.
- "ויטמין B6, 30 מ\"ג" — FOUND in rendered HTML.

The rowVerdict also warns: "האשווגנדה והולריאן אינם תורמים למגנזיום עצמו — בדוק אינטראקציות אם רלוונטי." — consumer-appropriate disclosure of the herbal actives. **RT-6: CLOSED.**

#### RT-8 (was HIGH, absorption caveat not prominent) — STATUS: CLOSED

The category note now contains all of the following, confirmed in rendered HTML:
- "ציון גבוה כאן פירושו 'הרבה מגנזיום נמצא על האריזה' — לא בהכרח 'הרבה מגנזיום נספג'" — directly addresses the oxide paradox.
- "אם ספיגה היא העדיפות שלך, ייתכן שמוצר עם ציון נמוך יותר וצורת ספיגה טובה יתאים לך יותר מאשר המוביל בדירוג" — explicit: lower-ranked well-absorbed form may suit the consumer better than the #1.
- "שני קצות המדף אינם אידיאליים" — neither extreme is presented as ideal.
- Oxide rowVerdicts contain "ציון גבוה = מינון גבוה, לא ספיגה גבוהה" (2 occurrences) and "גופך סופג ממנו" absorption warning (5 occurrences across oxide products).

The absorption caveat is now stated plainly and prominently in the category note in consumer language. **RT-8: CLOSED.**

---

## NEW-DEFECT HUNT

### NDH-1: Solgar ingredients correctly shows Calcium as calcium, not as magnesium
Confirmed: expansion.ingredients reads "סידן (calcium citrate) 200 מ\"ג; מגנזיום (magnesium citrate) כ-100 מ\"ג; ויטמין D3 80 IU" — correctly distinguishes calcium 200mg from magnesium 100mg. No fabrication.

### NDH-2: Oxide fractions stated without the 60.3% percentage in rowVerdicts
The percentage "60.3%" does not appear in the rendered HTML. Oxide products instead state the calculated elemental directly ("כ-271 מ\"ג", "כ-314 מ\"ג", "כ-260 מ\"ג"). This is not a defect — the elemental values are correct and stating a derived mg is more consumer-meaningful than a percentage. The fraction percentages appear in the data file comments and categoryNote (which states "כ-60% מהתרכובת" for oxide — approximate, not the precise 60.3%, which is acceptable rounding). Not a defect.

### NDH-3: "D7" appears twice in methodology footer
Confirmed context: "ציונים אלו הם מועמדים בלבד — טרם עברו אישור D7 לפרסום צרכני." This is a legitimate EDPG disclosure (D7 = scoring governance approval stage). Both occurrences are the methodology text and its hydration JSON copy. Not a framework leak; this is the intended draft warning. Not a defect.

### NDH-4: Taurate elemental claim — "פחות מ-10 מ\"ג" versus exact 6.8mg
The page states "פחות מ-10 מ\"ג" (fewer than 10mg) for Nutricare Taurate (76mg × 8.9% = 6.8mg). This is conservative and accurate — 6.8mg is indeed below 10mg. Using an approximate description ("פחות מ-10") for a small value is appropriate consumer language. Not a defect.

### NDH-5: Score ordering — Altman MagUp (67/B) vs three 520 oxide products (63/C)
v9 assigned Altman MagUp 66.5/B (blood pressure, evidence_score 72, HIGH tier) and the three 520 products 62.6/C (sarcopenia claim, evidence_score 47, MID tier). The score gap is driven by a real evidence-quality difference (different claims matched, different EV tiers). This gap is explained by the engine's own sub_scores and is not an arbitrary spread. The page does not expose these sub-scores, but the outcome is defensible. Not a new defect.

### NDH-6: Supherb TRIOMAG insightLine — "טענת 'ספיגה מיטבית' לא נתמכת בעדות מספקת"
The v1 report flagged this as RT-10 MEDIUM (framing inconsistency — claim appears endorsed before being challenged). The new insightLine: "שלושה סוגי מגנזיום — טענת 'ספיגה מיטבית' לא נתמכת בעדות מספקת." The leading framing is "three types" (factual statement) then the challenge ("not supported by evidence"). On a fast scan, the word "ספיגה מיטבית" appears quoted — the quotation marks signal it is the product's own claim being challenged. This is an improvement over the v1 version and meets the Bari Insight Line Spec (challenge-first, not endorsement-first when the insight type is a challenge). The MEDIUM finding from v1 is substantially addressed. MEDIUM finding RT-10: CLOSED.

### NDH-7: RT-11 (MEDIUM, tie-break order arbitrary) — UNCHANGED
Three products score 63/C (7290001065662, 7290015318426, 7290017218564). The ordering within the band is corpus-order; no tie-breaking rule is disclosed on the page. This is unchanged from v1. Routes to: product-agent, data-agent. Retained as MEDIUM.

### NDH-8: RT-12 (MEDIUM, metadata date) — CLOSED
Page now shows "19 מוצרים • יוני 2026" — the "נובמבר 2026" future date from v1 is resolved. CLOSED.

### NDH-9: RT-7 (HIGH, two unverifiable image identities) — UNCHANGED
- 7290013142894 (Altman MagUp): UUID filename `bd7e8878-3115-4e63-9646-d28e5d617979.webp` on altman.co.il — image identity not confirmable from URL alone.
- 7290015318426 (Tink Oxide 520): `catalog_941469-l.jpg?637595154336530000` on tinc.co.il — catalog ID, no barcode anchor.
Both images are still present and load from their original URLs. The data file comment now states: "Each URL confirmed HTTP 200 + correct product by barcode match in filename or page SKU field." This is a provenance assertion from the builder — this agent did not independently verify the two UUID/catalog-ID URLs against the brand page source. Rated: still OPEN at HIGH severity pending independent image-identity verification. The builder's self-attestation is noted but is not independent confirmation.

### NDH-10: RT-9 (MEDIUM, brand omission disclosure) — UNCHANGED
10 products in the v9 corpus are unscored (Magnesia brand premarket x5, Life brand name_derived x3, others x2). No disclosure of omitted brands appears on the page. The category note discusses the scoring methodology but does not mention that major brands (Magnesia) are absent from the comparison. Retained as MEDIUM.

---

## Product-by-Product Assessment (re-gate focus)

| Barcode | Product | Score | Grade | RT Assessment | Confidence | Notes |
|---|---|---|---|---|---|---|
| 7290013142894 | Altman MagUp 60 | 67 | B | Plausible | verified | Image identity unverifiable (UUID). Score change from v1 (70→67) reflects v9 re-score. |
| 7290001065662 | Nutricare 520 | 63 | C | Plausible | partial | Correctly downgraded from v8 B to v9 C. |
| 7290015318426 | Tink Oxide 520 | 63 | C | Plausible | partial | Correctly downgraded. Image identity unverifiable (catalog ID). |
| 7290017218564 | Altman 520 | 63 | C | Plausible | verified | Correctly downgraded. |
| 7290010207640 | NT LC Dead Sea | 59 | C | Plausible | partial | Hydroxide correctly mapped to oxide-equivalent form. |
| 7290019444206 | Altman Balance | 59 | C | Plausible | verified | RT-5 closed (no false claim). RT-6 closed (all 4 actives disclosed). |
| 7290017847122 | Magnox B6 | 58 | C | Plausible | partial | |
| 7290015429245 | Amorphicure PH | 49 | D | Plausible | partial | RT-3 closed (no "חסום בגלל" in insightLine). |
| 7290001066973 | Nutricare Malate | 49 | D | Plausible | partial | RT-1 closed (15.5% fraction now correct). |
| 7290015318532 | Tink Malate | 49 | D | Plausible | partial | RT-1 closed. |
| 7290011899967 | Altman Citrate | 49 | D | Plausible | verified | RT-1 closed. |
| 7290013464248 | Supherb Citrate+B6 | 49 | D | Plausible | partial | RT-1 closed. |
| 7290019444480 | Altman Bisglycinate | 49 | D | Plausible | verified | RT-1 closed. |
| 7290018439579 | Nutricare Taurate | 49 | D | Plausible | partial | Elemental estimate (פחות מ-10 mg) is conservative and correct. |
| 7290118818205 | Supherb Max550 | 49 | D | Plausible-but-unverifiable | partial | Blend ratio unverified; disclosed as estimate. |
| 0033984005181 | Solgar Ca+Mg+D | 49 | D | Plausible | verified | RT-2 closed (100mg Mg correctly stated; Ca disclosed separately). |
| 7290118816065 | Supherb TRIOMAG | 34 | E | Plausible | partial | RT-3 closed (no "חסום ב-E"). RT-10 substantially closed. |
| 7290001065594 | Nutricare Nano Lipo | 34 | E | Plausible | partial | RT-3 closed. |
| 7290018439043 | Nutricare WELL | 34 | E | Plausible | partial | RT-3 closed. |

---

## Summary Assessment

**Plausible** (upgraded from "Plausible-but-unverifiable" in v1).

The high-level narrative (oxide paradox, dose beats form when form is under-dosed, evidence caps for marketing claims) is coherent, grounded, and the copy layer now matches the chemistry. The scoring architecture produces defensible relative rankings. The absorption caveat is now prominent and honest in both the category note and product-level rowVerdicts. The EDPG prototype disclosure is intact throughout.

Remaining open items are one HIGH (image identity, builder self-attestation not independently confirmed) and two MEDIUMs (tie-break disclosure, brand omission disclosure) — none of these block a prototype gate.

---

## Findings by Severity

### CRITICAL — must resolve before launch
*None open.*

### HIGH — should resolve before launch

**RT-7: Two image identities unverifiable from URL alone (OPEN)**
- 7290013142894 (Altman MagUp): UUID filename `bd7e8878-3115-4e63-9646-d28e5d617979.webp` on altman.co.il.
- 7290015318426 (Tink Oxide 520): `catalog_941469-l.jpg?637595154336530000` on tinc.co.il.
- Status: Builder asserts "HTTP 200 + correct product by barcode match" in data file comment, but this agent cannot confirm the two UUID/catalog-ID cases from URL structure alone. Not independently cleared.
- Evidence: data file comment at line 45-46; URL patterns do not contain the barcode.
- Implication: If either image is wrong, the category-leader product (MagUp, 67/B) or the Tink 520 shows an incorrect product photo to consumers.
- Routes to: data-agent (provide direct source URL confirming image → product identity for both cases).

### MEDIUM — should document or monitor

**RT-9: Brand omission disclosure (OPEN — unchanged from v1)**
- 10 products not scored (Magnesia brand x5, Life brand name_derived x3, others x2).
- No disclosure of omitted brands in category note or methodology.
- Routes to: content-agent, product-agent.

**RT-11: Tie-break order within 63/C band is arbitrary (OPEN — unchanged from v1)**
- Three products score 63/C; page order appears to follow corpus order with no defined tie-breaking rule.
- Routes to: product-agent, data-agent.

---

## Oxide Paradox Framing Re-Assessment

The v1 HIGH finding on absorption-adjusted outcome disclosure (RT-8) is CLOSED. The new category note directly states that a high score means "much magnesium on the package — not necessarily much magnesium absorbed" and explicitly recommends that consumers who prioritize absorption should consider lower-scoring products. The prologue sentence 4 (lines 21-22 of the data file) reinforces this with quantitative framing ("מוצר ביסגליצינט בציון נמוך יותר עשוי לספק בפועל מגנזיום ספוג יותר"). This is honest and complete for a prototype stage.

---

## D10 Gate Verdict

**Track V: PASS** (all 12 leakage items clean; 19/19 score propagation correct; build exit 0; 19/19 images in HTML; metadata corrected).

**Track C: ZERO open CRITICAL findings.**

**D10 Combined Gate: CONDITIONAL PASS**

Named conditions (must acknowledge before launch; neither blocks the prototype gate):
1. RT-7 (HIGH): Independent image-identity verification for Altman MagUp (UUID) and Tink Oxide (catalog ID) — routes to data-agent.
2. RT-9 (MEDIUM): Brand omission disclosure for Magnesia/Life brands — routes to content-agent.
3. RT-11 (MEDIUM): Tie-break rule within the 63/C band — routes to product-agent.

Per Hard Rule 10: HIGH requires explicit acknowledgment, not necessarily resolution, before go/no-go. The prototype (EDPG/candidate, not consumer-live) can proceed with these acknowledged. Consumer launch requires RT-7 cleared.

---

## Return Contract JSON

```json
{
  "agent": "adversarial-qa-agent",
  "task_ref": "REGATE-magnesium-page-v2",
  "run_date": "2026-06-19",
  "prior_report": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_magnesium_page_v1.md",
  "corpus_source": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v9.json",
  "page_data_source": "C:\\bari\\bari-web\\src\\lib\\comparisons\\magnesium-page-data.ts",
  "artifacts_read": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_magnesium_page_v1.md",
      "purpose": "prior-report baseline for re-gate"
    },
    {
      "path": "C:\\bari\\bari-web\\src\\lib\\comparisons\\magnesium-page-data.ts",
      "purpose": "page data source — all consumer-facing strings read directly"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v9.json",
      "purpose": "score source of truth — all 19 scores extracted and compared"
    },
    {
      "path": "http://localhost:3000/hashvaot/magnesium",
      "purpose": "live rendered page — 93,845 bytes; all leakage / elemental / score checks run on this"
    }
  ],
  "counts": {
    "prior_critical_findings": 4,
    "prior_high_findings": 4,
    "prior_medium_findings": 4,
    "critical_findings_open": 0,
    "high_findings_open": 1,
    "medium_findings_open": 2,
    "rt_findings_closed": "RT-1, RT-2, RT-3, RT-4, RT-5, RT-6, RT-8, RT-10, RT-12 (9 of 12 v1 findings closed)",
    "rt_findings_open": "RT-7 (HIGH), RT-9 (MEDIUM), RT-11 (MEDIUM)",
    "products_in_v9_corpus_magnesium": "19 of 29 with engine_output.grade",
    "products_on_page": 19,
    "score_propagation_pass": "19 of 19",
    "grade_propagation_pass": "19 of 19",
    "confidence_mapping_pass": "19 of 19",
    "leakage_checklist_pass": "12 of 12 applicable items (0 fails — full reversal from v1's 6 fails)",
    "elemental_fraction_claims_verified": "13 of 13",
    "images_present_in_html": "19 of 19",
    "images_identity_confirmed": "17 of 19 (UUID and catalog-ID cases unconfirmed)",
    "oxide_b_to_c_downgrades_confirmed": "3 of 3 (Nutricare 520, Tink 520, Altman 520)"
  },
  "commands_run": [
    {"cmd": "python3 corpus extraction + score comparison", "exit_code": 0},
    {"cmd": "npm run build (C:\\bari\\bari-web)", "exit_code": 0},
    {"cmd": "Invoke-WebRequest http://localhost:3000/hashvaot/magnesium", "exit_code": 0, "status_code": 200, "content_length": 93845},
    {"cmd": "Invoke-WebRequest http://localhost:3000/sitemap.xml", "exit_code": 0, "magnesium_in_sitemap": false},
    {"cmd": "Regex search: all 14 leakage terms on live HTML", "exit_code": 0, "result": "0 hits"},
    {"cmd": "Regex search: all 4 RT-4 grade-prediction terms on live HTML", "exit_code": 0, "result": "0 hits"},
    {"cmd": "Regex search: all 13 elemental mg values on live HTML", "exit_code": 0, "result": "13 of 13 found"},
    {"cmd": "Regex search: RT-5 false same-score claim", "exit_code": 0, "result": "0 hits"},
    {"cmd": "Regex search: RT-6 Balance ingredients (ashwagandha, valerian, B6)", "exit_code": 0, "result": "3 of 3 found"},
    {"cmd": "Regex search: RT-8 absorption caveat terms (6 phrases)", "exit_code": 0, "result": "6 of 6 found"},
    {"cmd": "Score text node count (>67<×1, >63<×3, >59<×2, >58<×1, >49<×9, >34<×3)", "exit_code": 0, "total": 19}
  ],
  "not_done": [
    "E2E / Playwright test run not performed (dev server confirmed 200 by direct HTTP fetch)",
    "Hebrew readability tool not invoked — leakage confirmed by direct HTML text search; no borderline cases requiring the tool",
    "run_gates.py not invoked — no gates.py configured for supplement category (food categories only)",
    "Visual screenshot / mobile geometry not measured — geometry checklist not requested for this re-gate",
    "Crossref / SemanticScholar adversarial evidence weight challenge not performed — not in re-gate scope",
    "Independent image-identity verification for 2 UUID/catalog-ID images (RT-7) — requires checking source brand/retailer page directly; flagged as HIGH open"
  ],
  "spec_acceptance_test": {
    "result": "CONDITIONAL PASS",
    "critical_open": 0,
    "high_open": 1,
    "medium_open": 2,
    "d10_gate": "CONDITIONAL PASS — Track V fully green, Track C zero CRITICAL. High (RT-7 image identity) and two Mediums acknowledged. Consumer launch requires RT-7 cleared independently.",
    "v1_findings_cleared": "RT-1 (CRITICAL), RT-2 (CRITICAL), RT-3 (CRITICAL), RT-4 (CRITICAL), RT-5 (HIGH), RT-6 (HIGH), RT-8 (HIGH), RT-10 (MEDIUM), RT-12 (MEDIUM)",
    "new_defects_introduced": "none"
  }
}
```
