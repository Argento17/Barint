# Red-Team Challenge Report — Yogurts v4 (run_yogurt_005)
Date: 2026-06-11
Scope: 89 products, origin/rel/yogurts-v4 (HEAD d6fcc2eb), bari-web/src/data/comparisons/yogurts_frontend_v4.json
Challenger: red-team-agent

---

## Opening Finding

**CRITICAL — Published nutrition panel for bsip1_yogurt_7290116932620 ("יוגורט גו נטול לקטוז") displays protein=190.0 g per 100 g to consumers.** This value is physically impossible (190 g protein cannot fit in 100 g of product). It is a scrape/parse corruption: the Shufersal page for this product printed the per-serving protein claim ("190 gram per container" — a 190 g cup) as a per-100g macro value. The trace flags macros_plausible=false yet the pipeline allowed the record through at confidence="partial" and the product received 90/A. A consumer reading the expansion panel sees "חלבון: 190" next to a credible-looking score. This is factually false consumer information and constitutes the hardest single-product blocker.

---

## Score Reproduction Check

All 89 published scores reproduce exactly from trace final_score_estimate values by applying: cap to 89.9 if raw > 89.9, then round(). No unexplained deviations found.

---

## Product-by-Product Assessment

| ID | Name (truncated) | Published | Grade | Conf | RT Assessment | Critical Notes |
|----|-----------------|-----------|-------|------|---------------|---------------|
| bsip1_yogurt_7290110321031 | יופלה GO מועשר בחלבון | 90 | A | partial | PLAUSIBLE | Null sugar/satFat; NOVA 2; 0 fired caps; score driven by protein=10 + clean ingredients; 3 of 8 "ingredient" entries are nutrition-panel/disclaimer bleed |
| bsip1_yogurt_7290112336712 | דנונה פרו 21 חלבון 0% | 90 | A | partial | PLAUSIBLE | Engine produced 90.4/S; post-cap to 89.9/A is documented policy (TASK-246); NOVA3 binding cap fired at 94.8 — does not constrain 90.4; has_live_cultures=true, sweetener_count=1; null satFat |
| bsip1_yogurt_7290116932620 | יוגורט גו נטול לקטוז | 90 | A | partial | INCORRECT DATA | protein=190 g/100g — impossible, scrape corruption; macros_plausible=false flagged by engine; null sugar/satFat; score derived from implausible protein signal; CRITICAL |
| bsip1_yogurt_7290116935614 | יוגורט GO חלבון 25 גרם | 90 | A | partial | PLAUSIBLE BUT WEAK | Protein=12.5 is plausible; null sugar/satFat/fiber; NOVA 2, 0 caps; ingredient list has 3 of 6 entries as nutrition-label/disclaimer bleed; cannot verify sugar penalty absence |
| bsip1_yogurt_7290110565527 | דנונה פרו 20 גרם חלבון | 88 | A | partial | PLAUSIBLE | protein=10, sugar=3.4, NOVA3 cap fired; has_live_cultures=true; sweetener_count=1; null satFat |
| bsip1_yogurt_7290114311069 | מולר אקטיב לבן 0% 25חלבון | 83 | A | partial | PLAUSIBLE | protein=12.5, sugar=2.5; NOVA3 cap fired; has_live_cultures=true; sweetener_count=1; null satFat |
| bsip1_yogurt_7290119377480 | יוגורט פרו עם שוקולד | 82 | A | partial | CHALLENGING | Chocolate yogurt, 8.4g sugar, 120kcal, 2.3g satFat; NOVA3 cap fired (cap=94.8); contains E414 (acacia gum) + soy lecithin + hazelnut paste; enrich says additive_count=0 but E414 present in ingredients — additive detection miss; 82/A despite 8.4g sugar and a chocolate topping component |
| bsip1_yogurt_7290102395231 | יוגורט ביו נטורל 2.8% | 81 | A | partial | WEAK | NOVA2; only 3 ingredients; sweetener_count=1; protein=5.6 — the lowest protein A-grade; score mechanism unclear from trace; ingredient_count=3 raises "complete ingredient list?" question |
| bsip1_yogurt_2824466 | יוגורט ביו 0% שומן דנונה | 80 | A | partial | PLAUSIBLE | protein=5.3, sugar=4.6; NOVA3 cap fired; has_live_cultures=false but fermentation_marker_count=1; sweetener_count=1; null satFat |
| bsip1_yogurt_7290112346797 | אקטיביה שיבולת שועל שזיף | 60 | C | partial | MISROUTED | Engine classified as category="cereal" — this is a yogurt product; scored 59.9 under cereal cap logic (binding_cap=94.8, NOVA3); sweetener_count=2, sugar=8.9g; under dairy_protein routing would apply dairy caps and different base |
| bsip1_yogurt_7290114313070 | יוגורט מוקצף אפרסק | 35 | D | verified | GRADE DISAGREEMENT | Engine grade_estimate=E (raw=34.8); builder rounds 34.8→35 → grade D; consumer sees D not E; grade_from_score(35)=D by boundary design but engine computed E; 6 additives, NOVA4 |
| bsip1_yogurt_7290110328788 | יוגורט GO קרמי אפרסק | 65 | B | partial | NOTE | NOVA4 with binding_cap=68; null sugar/satFat; score=65 sits at cap boundary; sweetener_count=3 but additive_count=0 — sweeteners not counted as additives |
| (D-cluster: 23 products) | Various Froop/Mooked/Fruited | 35-47 | D | mixed | JUSTIFIED | NOVA4 with ADDITIVE + NOVA4 caps correctly limiting these heavily-processed dessert yogurts |
| (B-cluster: plain bio/greek 15 products) | Various Bio/Greek 3-8% | 72-79 | B | partial | PLAUSIBLE | Consistent cluster; null satFat across most; sugar absent in 0 of these; reasonable grouping |

---

## Summary Assessment

**Justified scores (structural logic holds):** 68 of 89 — plain bio, greek, and high-protein products where protein + NOVA + additive caps produce internally consistent differentiation.

**Plausible but unverifiable:** 12 products — scores driven partly by null fields (sugar, satFat absent; penalty cannot fire; benefit of doubt falls to the product). This inflates scores for products where those nutrients might in reality be high.

**Weak confidence:** 3 products — bsip1_yogurt_7290102395231 (only 3 ingredients parsed; sweetener present; protein 5.6g yet A), bsip1_yogurt_7290116935614 (ingredient list contaminated; null sugar), bsip1_yogurt_7290119377480 (chocolate yogurt A-grade; additive detection miss).

**Noise-level precision (indistinguishable):** 8 products score 37-38 in the D-band with raw differences of 0.2-1.2 points. Published as distinct integers but mechanically identical profiles.

**Potentially incorrect:** 1 product with corrupted data (protein=190), 1 misrouted product, 1 grade boundary disagreement.

**Overriding structural problems:**
1. Null sugar across 15 products (16.9%) silently prevents sugar penalty from firing. Three A-grades carry null sugar.
2. 67/89 products have ingredient list entries that contain nutrition-panel text bleed. The TASK-144 sanitizer marks these "clean" but they inflate ingredient_count and feed erroneous NOVA inference.
3. All 89 products carry confidence="partial" or "verified"; zero products are "insufficient" — yet 40/89 have null satFat, 15/89 have null sugar. The partial/verified distinction does not accurately signal to the consumer which critical fields are missing.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: Phantom protein=190 g/100g published to consumers (barcode 7290116932620)**
Evidence: bsip2_trace.json L1_observed_signals.protein_g=190.0, macros_plausible=false, energy_kcal=86. Physical maximum protein per 100g for any yogurt product is approximately 25g. The 190 value comes from Shufersal page HTML where the per-container protein claim ("25 gram protein per 190g cup" expressed as "190 gram") was parsed as the per-100g macro. This product is published at 90/A with a consumer-facing expansion panel showing protein=190. Any user who reads the expansion sees a fabricated nutrition value under an A grade. macros_plausible=false was flagged by the engine but no gate blocked the record.
Implication: Consumer decision harm (the product appears to have 15x a realistic protein density), regulatory exposure (publishing false nutrition data), and direct brand credibility risk if a journalist reads the panel. The score itself may also be corrupted: if the engine used protein_g=190 in any calculation pathway, the 90/A score is wrong.
Routes to: data-agent (pipeline gate: reject or quarantine records with macros_plausible=false before frontend emission), nutrition-agent (score validity review for this product if protein signal influenced scoring), content-agent (do not publish this product until data corrected).

**RT-2: Ingredient list contamination inflates NOVA inference for 67/89 products**
Evidence: 67 of 89 products have at least one ingredient_list entry longer than 80 characters containing embedded nutrition panel data and legal disclaimers (e.g. "מכיל חלב ערכים תזונתיים 100 גרם 86 קל אנרגיה 12.5 גרם חלבונים 4.4 גרם פחמימות 2 גרם שומנים 72 מג נתרן הנתונים המדויקים מופיעים על גבי המוצר, אין להסתמך על הפירוט המופיע באתר, יתכנו טעויות או אי התאמות"). The TASK-144 sanitizer marks these records as ingredient_text_quality="clean" despite the contamination. This inflates raw ingredient_count (the nutrition panel entries are being counted as ingredients) and feeds the NOVA inference logic with non-ingredient text. Two specific consequences: (a) the NOVA-2 assignments for 7290110321031 and 7290116932620 (both 90/A) depend on ingredient lists where 3-4 of 8 "ingredients" are disclaimer/marketing/nutrition text; the true ingredient count may be 4-5 which could alter NOVA proxy; (b) additive detection may miss real additives because the contaminated entries fragment the ingredient text.
Implication: NOVA proxy assignments for a majority of the corpus are unverified. The three 90/A NOVA-2 products could be NOVA-3 if a correct ingredient count were used, which would fire the NOVA3_PROCESSED cap at 94.8 — no scoring change at that level, but the NOVA field displayed to consumers would be wrong.
Routes to: data-agent (BSIP0/BSIP1 scrape: ingredient parser must separate the ingredient declaration from the nutrition panel and disclaimer text before handing to BSIP2; the "clean" flag from the sanitizer is incorrect), nutrition-agent (NOVA proxy methodology: ingredient_count threshold needs review given this contamination rate).

**RT-3: Category misroute — Activia Oat Plum (barcode 7290112346797) scored as "cereal"**
Evidence: bsip2_trace.json category="cereal", grade_estimate="C", raw=59.9. This is a drinkable probiotic yogurt with oat (אקטיביה שיבולת שועל שזיף). It is sold in the Shufersal yogurt aisle. The cereal category uses a different cap floor and baseline than dairy_protein. It has sugar=8.9g, sweetener_count=2, has_live_cultures=false (despite being Activia — fermentation detection missed). Published to consumers in the yogurts category at 60/C. Its score under dairy_protein rules would differ — possibly higher or lower depending on the category base score. Publishing a product in a category using a different scoring universe than intended is a structural error.
Implication: The score may not be the correct signal for this product's comparative standing against the other 88 yogurts. A consumer comparing Activia Oat to plain yogurt sees a score computed under incompatible rules.
Routes to: data-agent (re-route to dairy_protein category and rescore), nutrition-agent (confirm correct category for probiotic + oat yogurt hybrids).

---

### HIGH — should resolve before launch

**RT-4: Grade boundary suppression — יוגורט מוקצף אפרסק (barcode 7290114313070) published D, engine says E**
Evidence: run_summary.json grade="E" at raw=34.8. builder applies round(34.8)=35, grade_from_score(35)=D. Published grade: D. The engine judged this product below the D threshold (it has 6 additives, NOVA4, sweetener_count=3, high sugar 9.8g). grade_from_score uses >= 35 as D threshold. A raw score of 34.8 is below this threshold at full precision. The rounding step that promotes it to D is a builder artifact that overrides the engine's E verdict. A consumer sees D (acceptable-but-poor) for what the engine computed as E (poor).
Implication: One product promoted one grade band by a builder arithmetic artifact. This is the kind of finding a hostile nutritionist would use to argue the grade system is gamed.
Routes to: nutrition-agent (confirm whether round-then-grade vs grade-then-round is the intended architecture), data-agent (if round-then-grade is wrong, fix builder logic and round_score function).

**RT-5: Chocolate yogurt with E414 additive scores 82/A — additive detection miss**
Evidence: bsip1_yogurt_7290119377480 ("יוגורט פרו עם שוקולד"), ingredients_raw contains: "חומר הזגה (E414), מחית אגוזים (לוז)". E414 is acacia gum (a permitted additive). enrichment_summary.additive_count=0. The additive count parser failed to identify E414. Had it been detected: additive_count=1, which would not by itself trigger any cap (caps fire at >= 3 additives). However, the product also contains soy lecithin (implied by "פתיתי סויה") and a complex chocolate component. The additive detection miss means the insight line says "ללא תוספים מזוהים" (no identified additives) — a false claim about a product that contains at least one E-number.
Additionally: 8.4g sugar, 120kcal/100g, 2.3g satFat. For context, a plain bio yogurt with 5g protein scores 78-80/B. This chocolate yogurt scores 82/A on the strength of 11.2g protein — the protein bonus overrides what is nutritionally a significantly less clean product. The 82/A grade will be the most screenshot-worthy result in the corpus by a hostile nutritionist.
Implication: (a) "ללא תוספים מזוהים" is published as a positive signal for a product with E414; (b) 82/A for a flavored chocolate product with added sugar and an animal-nut composite inclusion contradicts the category's implicit framing of A as a clean, minimally processed product.
Routes to: data-agent (fix E414 and similar parenthetical E-number detection in BSIP1 enrichment), nutrition-agent (review whether high-protein flavored yogurts with added chocolate components should be scored against a flavored sub-baseline or have a sugar/fat composite gate for A eligibility).

**RT-6: All 9 A-grade products carry confidence="partial" — no A grade is "verified"**
Evidence: conf distribution = 70 partial / 19 verified; 9/9 A-grades are partial. The "verified" products are all D-grade (verified = "both nutrition and ingredients fully parsed and cross-checked"). The A-grades are partial because they lack sugar and/or satFat. Three A-grades at 90 carry null sugar (no sugar penalty could fire), null satFat (no sat-fat penalty could fire).
Implication: The consumer UI (per Bari Score Presentation v1) shows a confidence indicator. Showing partial/A simultaneously tells the consumer the product scored best in the category on incomplete data. For the three 90/A products with null sugar, the honest statement is "we don't know the sugar content — if it is >= 5g, the score would be lower." This is not surfaced. The unknowns field in the expansion does note missing sugar, but the top-line 90/A grade does not carry a visible caveat.
Routes to: nutrition-agent + content-agent (methodology: should a product with null sugar receive an A grade, or should null sugar invoke a confidence downgrade that prevents A?), design-agent (UI: partial confidence on A-grade needs a visible caveat pattern, not just in the expansion unknowns field).

**RT-7: "No serving size" for all 89 products — serving_size_g=null across corpus**
Evidence: every BSIP1 record has serving_size_g=null. The frontend displays all nutrition "ל-100 גרם" (per 100g). For yogurts sold in fixed-size cups (common sizes: 100g, 150g, 175g, 190g, 200g, 500g), the per-100g values are interpretable but the consumer cannot verify whether the panel data is per-cup or per-100g without the serving size anchor. The Shufersal scrape does capture nutrition_basis_detected="per_100g" correctly — confirmed for the 5 sampled BSIP1 files. This is lower severity than initially feared: the basis is per-100g and verified. However, no serving size means:
(a) A consumer sees "חלבון: 10 גרם" on a 190g product and cannot immediately compute "I get 19g of protein from this cup" — the comparison page shows per-100g which undersells high-protein products and can mislead on actual consumption impact.
(b) Products sold as multi-packs (e.g. 4x175g) may have the portion be a single 175g cup, making per-100g arithmetic unintuitive.
Routes to: data-agent (capture serving_size_g from Shufersal structured data during re-scrape; it is present in the JSON-LD on many pages), content-agent (serving note copy "ל-100 גרם" is accurate but a contextual serving note would strengthen consumer utility).

---

### MEDIUM — should document or monitor

**RT-8: TASK-246 Path A gap still live — fermentation keyword bonus uncapped at engine level**
Evidence: TASK-246 is IN_PROGRESS. The builder-level 89.9 post-cap suppresses the symptom for 1 product (barcode 7290112336712, 90.4→90). The underlying engine gap (fermentation keyword bonus not subject to the BARI_RECAL_P0_YOGURT_TRIM cap) means any future product with strong fermentation keyword presence that also passes NOVA3 could exceed the cap again. Current run: 1 product affected. The stopgap is documented and mechanically correct. But the gap itself means the engine is not self-consistent with its own trim policy.
Routes to: nutrition-agent + data-agent (TASK-246 already tracking; confirm no second product in current corpus is within 2 points of triggering).

**RT-9: Null satFat for 40/89 products (44.9%) — sat-fat penalty cannot fire for nearly half the corpus**
Evidence: fat_saturated_g=null for 40 products. The ISRAELI_RED_LABEL_1_SAT_FAT cap is listed in every trace but fires based on null condition (condition evaluated as false when satFat is null). Products with naturally high saturated fat (e.g. full-fat Greek yogurts at 6-8% total fat) could carry elevated satFat that is never penalized. Greek yogurt products 7290017065588 (10% fat, score=70/B), 7290014890589 (8% fat, score=73/B) — neither has satFat data. Their scores may be 3-5 points too high if satFat >=4g.
Routes to: data-agent (Shufersal panels for Greek yogurt products do typically include satFat — rescrape or re-parse these specific products), nutrition-agent (sat-fat null handling policy: should null satFat invoke conservative penalty or not?).

**RT-10: Sweetener-bearing products score A without sweetener penalty**
Evidence: 7290102395231 (81/A) has sweetener_count=1, only 3 parsed ingredients. 7290114311069 (83/A) has sweetener_count=1. 7290112336712 (90/A) has sweetener_count=1. None of these trigger a sweetener-specific cap — no such cap exists in the engine. The sweetener count is visible in enrichment_summary but not a scoring signal. For the Bio Natural 2.8% (81/A, 3 ingredients, sweetener present), a hostile nutritionist would ask: why is a 3-ingredient yogurt containing a sweetener graded the same as a plain yogurt with 5g protein and no sweetener?
Routes to: nutrition-agent (policy question: should a yogurt with a non-sugar sweetener receive any scoring signal? Currently invisible to scoring).

**RT-11: NOVA2 high-protein yogurts score identically despite different protein levels**
Evidence: Three NOVA2 products all score 90/A (after cap): barcodes 7290110321031 (protein=10g), 7290116932620 (protein=190g — corrupted), 7290116935614 (protein=12.5g). The score compression at the top of the range means real protein differences between products at 10g, 12.5g, 20g etc. produce the same published score. Consumers see three products all at 90/A and cannot differentiate. This is a ceiling artifact, not a scoring error, but it is worth disclosing. Note: this is partly by design (BARI_RECAL_P0_YOGURT_TRIM trim policy), but may surprise consumers who compare these products.
Routes to: nutrition-agent (methodology note: confirm the ceiling compression is intentional and document in category caveat copy), content-agent (category caveat should note that high-protein products at the top band are nutritionally differentiated beyond what the score communicates).

**RT-12: Activia Bio Oat has_live_cultures=false despite being an Activia probiotic product**
Evidence: bsip1_yogurt_7290112346797 enrichment_summary.has_live_cultures=false, fermentation_marker_count=1. The product is sold as a probiotic yogurt (Activia brand, contains live cultures by product definition). The BSIP1 enrichment did not detect live cultures. This is likely a keyword detection failure (the probiotic culture marker was present in the ingredient text but not in the has_live_cultures detection pattern). This is secondary to the category misroute (RT-3) but means the insight line and positive signals for this product are incorrect (would not surface "תרביות חיות" as a positive signal).
Routes to: data-agent (review BSIP1 live_cultures detection logic; Activia/Danone probiotic products reliably contain live cultures and should be detectable from ingredient text).

**RT-13: Muller Protein Fruity (barcode 7290102399819) published 50/C, run_summary says 49.6/D**
Evidence: run_summary.json for this barcode: score=49.6, grade="D". Frontend: score=50, grade=C. The rounding of 49.6 → 50 crosses the C/D boundary (C threshold = 50). Engine produced D; builder produces C. Same architectural issue as RT-4 but in the opposite direction (a D promoted to C at the boundary by rounding). grade_from_score(50)=C.
Routes to: nutrition-agent (confirm round-then-grade vs grade-first policy), data-agent (second boundary crossing identified — same fix needed as RT-4).

---

## Verdict

**FAIL — launch blocked on CRITICAL findings RT-1, RT-2, RT-3.**

RT-1 (protein=190 published to consumers) is an outright data error on a 90/A product. It cannot ship.
RT-2 (67/89 ingredient lists contaminated, NOVA inference corrupted) means the published NOVA fields and additive signals are unverified for most of the corpus.
RT-3 (one product scored and published under wrong category rules) means the comparison is internally inconsistent.

HIGH findings RT-4 and RT-13 (two grade boundary crossings by rounding) require a confirmed policy decision before launch — if round-then-grade is intentional, document it; if it is not, fix it. These affect one D→C and one E→D promotion.

HIGH finding RT-5 (chocolate yogurt 82/A with E414 miss and false "no additives" signal) is a specific consumer-facing accuracy problem that should be resolved.

HIGH finding RT-6 (all A-grades partial confidence, three with null sugar) requires a UI/methodology decision about whether null-sugar products are eligible for A.

**Summary counts:**
- CRITICAL: 3 (RT-1, RT-2, RT-3)
- HIGH: 4 (RT-4, RT-5, RT-6, RT-7) — RT-7 is lower-end HIGH (serving size)
- MEDIUM: 6 (RT-8 through RT-13)
- Total: 13 findings
