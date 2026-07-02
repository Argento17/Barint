# Red-Team Challenge Report — Magnesium Supplements (corpus_run_full_v8 / EDPG prototype)
Date: 2026-06-19   Scope: 19 products, /hashvaot/magnesium   Challenger: adversarial-qa-agent
Run source: C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v8.json (engine_active=='magnesium')

---

## TRACK V — VERIFICATION

### V-1: Build
`npm run build` in C:\bari\bari-web — EXIT CODE: **0**
Route `/hashvaot/magnesium` appears in the static build manifest. PASS.

### V-2: Route / Render
HTTP GET http://localhost:3000/hashvaot/magnesium — Status **200**. Content-Length: 92,073 bytes.
All 19 score numbers rendered as text nodes (>70<, >66<×3, >62<×2, >61<, >49<×9, >34<×3). PASS.
All 19 grade letters rendered in `<span>` elements (4×B, 3×C, 3×C counted by isolatedGrades pattern, full set confirmed). PASS.
All 7 product brands confirmed present in rendered HTML (אלטמן×23 appearances, נוטריקר×17, סופהרב×9, etc.). PASS.
Partial-page disclosure rendered: "חלק מהמוצרים בדף זה מבוססים על נתונים חלקיים מהתווית" — correctly triggered (13/19 = 68.4% partial, threshold ≥50%). PASS.
CategoryNote "הערת קטגוריה — מגנזיום יסודי" present in rendered HTML. PASS.
Page title: "תוספי מגנזיום | Bari — טיוטה" — EDPG/draft signal present. PASS.
Meta description includes "טיוטה בלבד". PASS.
No `next-error-h1` rendered (appears only in embedded CSS bundle, not in DOM). PASS.
`dir="rtl"` on `<html>` element. PASS.
Route NOT in sitemap.xml. PASS.
Route NOT linked from /hashvaot index page. PASS.

### V-3: Score Propagation Audit (all 19 products)

| Barcode | Product (short) | Corpus Score | Page Score | Delta | Corpus Grade | Page Grade | Grade Match | Confidence |
|---|---|---|---|---|---|---|---|---|
| 7290013142894 | Altman MagUp 60 | 69.5 | 70 | +0.5 | B | B | PASS | verified |
| 7290001065662 | Nutricare 520 100caps | 65.6 | 66 | +0.4 | B | B | PASS | partial |
| 7290015318426 | Tink Oxide 520 90 | 65.6 | 66 | +0.4 | B | B | PASS | partial |
| 7290017218564 | Altman 520 60caps | 65.6 | 66 | +0.4 | B | B | PASS | verified |
| 7290010207640 | NT LC Dead Sea | 62.0 | 62 | 0 | C | C | PASS | partial |
| 7290019444206 | Altman Balance 60 | 62.0 | 62 | 0 | C | C | PASS | verified |
| 7290017847122 | Magnox B6 60 | 61.4 | 61 | -0.4 | C | C | PASS | partial |
| 7290015429245 | Amorphicure PH 60 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 7290001066973 | Nutricare Malate 90 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 7290015318532 | Tink Malate 60 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 7290011899967 | Altman Citrate 120 | 49.0 | 49 | 0 | D | D | PASS | verified |
| 7290013464248 | Supherb Citrate+B6 60 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 7290019444480 | Altman Bisglycinate 60 | 49.0 | 49 | 0 | D | D | PASS | verified |
| 7290018439579 | Nutricare Taurate 90 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 7290118818205 | Supherb Max550 60 | 49.0 | 49 | 0 | D | D | PASS | partial |
| 0033984005181 | Solgar Ca+Mg+D 150 | 49.0 | 49 | 0 | D | D | PASS | verified |
| 7290118816065 | Supherb TRIOMAG 60 | 34.0 | 34 | 0 | E | E | PASS | partial |
| 7290001065594 | Nutricare Nano Lipo 60 | 34.0 | 34 | 0 | E | E | PASS | partial |
| 7290018439043 | Nutricare WELL 90 | 34.0 | 34 | 0 | E | E | PASS | partial |

All 19 grade assignments match the corpus. All score deltas are within rounding (max ±0.5 for standard round()). The frontend does NOT re-derive grades via a food-score-threshold function; grades are passed directly from the VM. No silent re-grading detected. Score propagation: **PASS**.

Confidence mapping: all 19 products mapped correctly (brand_panel → verified, search_panel → partial). No name_derived products appear on page. **PASS**.

### V-4: Images
All 19 imageUrl values extracted from React hydration payload. Domain distribution: vitamins4all.co.il (10), altman.co.il (1), tinc.co.il (1), teva-call.co.il (2), biogaya.co.il (1), solgar.co.il (1). Zero openfoodfacts references. All domains registered in next.config.ts remotePatterns.

**Image identity:**
- 14/19: Barcode confirmed in filename (e.g. 7290001065662.webp) — CONFIRMED
- 3/19: Name or product text in URL, brand site — PLAUSIBLE
- 2/19: Cannot confirm from URL alone — UNVERIFIABLE

Unverifiable:
1. 7290013142894 (Altman MagUp): UUID filename `bd7e8878-3115-4e63-9646-d28e5d617979.webp` on altman.co.il — no barcode in URL.
2. 7290015318426 (Tink Oxide 520): `catalog_941469-l.jpg?637595154336530000` on tinc.co.il — catalog ID only, no barcode; timestamp query string suggests legacy CDN.

Plausible but not barcode-confirmed:
3. 7290017847122 (Magnox B6): `nagb6.jpg` on teva-call.co.il — name-derived filename.
4. 7290001065594 (Nutricare Nano Lipo): `nano-magnesium-Copy.webp` — generic name, could be any nano-magnesium SKU from that retailer.

OFF-sourced images: **ZERO**. OFF compliance: PASS.

### V-5: Leakage Checklist

| Item | Result | Value Observed |
|---|---|---|
| Filter labels contain framework terms | N/A | No filters defined (empty lensOptions) |
| Row insight explains score mechanism | **FAIL** | "חסום בגלל תת-מינון" in Amorphicure insightLine (visible on collapsed row) |
| Row verdicts expose scoring caps | **FAIL** | "חסום ב-34/E" in rowVerdict for 3 E-grade products (rendered in collapsed row) |
| Methodology names scoring dimensions | **FAIL** | "עדות (evidence), מינון יסודי (dose), צורת ספיגה (form) ויושרת תיוג (honesty)" — 4 dimension names rendered |
| Methodology exposes internal cap values | **FAIL** | "תקרה של 49/D" and "תקרה של 34/E" rendered as `<p>` text in methodology footer |
| Internal evidence sub-scores visible | **FAIL** | "92/100 בדירוג הצורה", "72/100", "17/100" — raw sub-scores in positiveSignals/limitingFactors |
| cap_1 / cap_2 mechanism strings visible | **PARTIAL** | "cap_1" appears in React hydration JSON payload (not rendered as visible DOM text); "cap_2_fairy_dust_hidden_dose" not rendered |
| Prologue predicts grade by form type | **FAIL** | "אוקסיד ייגמר ב-B, צורות טובות ייגמרו ב-D כשהמינון לא מוצדק" — prologue explicitly tells consumers what grade each form will receive |
| Hero/prologue contain prohibited framework vocabulary | PASS | No BSIP, NOVA, structural_class, matrix_integrity, pillar, routing terms in prologue/hero |
| No drift: no chart above first row | PASS | No chart or visualization above product rows |
| No drift: no user choice before products | PASS | No choice required (no filters) |
| Score has no verbal interpretation beside it | PASS | No "מצוין/טוב/בינוני" next to score chips |
| Highlighted pair ≤ 1 | PASS | Zero highlighted pairs |
| RTL: dir=rtl on html element | PASS | Confirmed |

**Leakage verdict: FAIL** — 6 checklist items fail (multiple CRITICAL-level).

---

## TRACK C — ADVERSARIAL CHALLENGE

### Opening Finding

**Three CRITICAL structural problems, all opening-level:**

**C1. Factually wrong elemental fraction amounts in consumer-facing copy.** The copy states elemental magnesium quantities that are chemically incorrect for malate, bisglycinate, and citrate compounds. These numbers appear in limitingFactors (rendered in expansion) and explain why products were downgraded — but the explanation is wrong. A food scientist, journalist, or regulator reading these numbers will catch the errors immediately.

**C2. Solgar Ca+Mg+D: page states Mg dose as 200mg; corpus panel shows actual Mg = 100mg.** The corpus bsip0s_label misrouted all three actives (Ca, Mg, D3) under `active_slug=vitamin_d3`; the engine scored on 200mg of CALCIUM citrate as if it were magnesium citrate. The page copy reflects this error: "מגנזיום ציטראט 200 מ\"ג" is factually wrong — the actual magnesium content is 100mg. The grade (D/49) likely survives the correction (100mg Mg-citrate = ~16mg elemental, even further below fairy_floor), but a consumer reading the page sees the wrong number for a real product.

**C3. Rendered leakage of scoring mechanism in consumer-visible text.** The methodology footer renders "תקרה של 49/D" and "תקרה של 34/E" as visible HTML text. Three E-grade rowVerdicts render "חסום ב-34/E" and "חסום ב-E" in the collapsed row. The Amorphicure insightLine renders "חסום בגלל תת-מינון" in the collapsed row. These expose the scoring cap/block architecture to consumers in violation of the leakage standard.

---

## Product-by-Product Assessment

| Barcode | Product | Score | Grade | RT Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| 7290013142894 | Altman MagUp 60 | 70 | B | Plausible | verified | Image unverifiable (UUID filename). Dose sub_therapeutic not in_range — leads category by evidence (blood pressure, Moderate tier EV). |
| 7290001065662 | Nutricare 520 100 | 66 | B | Plausible | partial | Claimed "highest dose in category" matches 520mg; no evidence for specific claim stated on label. |
| 7290015318426 | Tink Oxide 520 90 | 66 | B | Plausible | partial | Image unverifiable (catalog ID). Score identical to Nutricare 520 — tie mechanically justified (same formula). |
| 7290017218564 | Altman 520 60 | 66 | B | Plausible | verified | Third identical 66/B oxide product; consistent. |
| 7290010207640 | NT LC Dead Sea | 62 | C | Plausible-but-incomplete | partial | Hydroxide mapped to oxide form score (45) — honest, copy discloses. Missing context: B6+E not disclosed as potentially irrelevant cofactors. |
| 7290019444206 | Altman Balance 60 | 62 | C | WEAK — contains insightLine factual error | verified | insightLine says "ציון זהה לגרסה הבסיסית" (same score as basic version). No other Altman oxide scores 62; UP=70, 520s=66. Claim is wrong. Separately: ashwagandha KSM-66 50mg + valerian 50mg + B6 30mg omitted from expansion.ingredients — incomplete supplement disclosure. |
| 7290017847122 | Magnox B6 60 | 61 | C | Plausible | partial | 432mg oxide = 260mg elemental, sub_therapeutic. Image name-derived (nagb6.jpg). |
| 7290015429245 | Amorphicure PH 60 | 49 | D | Plausible verdict, leakage in insightLine | partial | 160mg carbonate × 28.8% = 46.1mg elemental — copy claim is CORRECT here. InsightLine says "חסום בגלל תת-מינון" — leakage (explains block mechanism). |
| 7290001066973 | Nutricare Malate 90 | 49 | D | WRONG chemistry in copy | partial | Copy says "מלאט מכיל כ-9% יסודי — כ-63 מ\"ג בלבד". Actual: Mg malate = 15.5% elemental. 700mg × 15.5% = 108.5mg (page says 63mg — wrong by 72%). Engine still fires fairy_dust because 108.5mg < fairy_floor. Verdict defensible; explanation is chemically wrong. |
| 7290015318532 | Tink Malate 60 | 49 | D | WRONG chemistry in copy | partial | Same error: 136mg malate × 15.5% = 21.1mg elemental (page says ~12mg, implying 9% fraction — wrong). |
| 7290011899967 | Altman Citrate 120 | 49 | D | WRONG chemistry in copy | verified | 200mg citrate × 16.2% = 32.4mg elemental (page says ~42mg, implying 21% — wrong by 30%). |
| 7290013464248 | Supherb Citrate+B6 60 | 49 | D | WRONG chemistry in copy | partial | 250mg citrate × 16.2% = 40.5mg elemental (page says ~53mg, implying 21% — wrong by 31%). |
| 7290019444480 | Altman Bisglycinate 60 | 49 | D | WRONG chemistry in copy | verified | 250mg bisglycinate × 14.1% = 35.3mg elemental (page says ~50mg, implying 20% — wrong by 42%). |
| 7290018439579 | Nutricare Taurate 90 | 49 | D | Plausible — chemistry within margin | partial | 76mg taurate × 8.9% = 6.8mg elemental (page says ~8mg — within rounding margin, acceptable). |
| 7290118818205 | Supherb Max550 60 | 49 | D | Partial — compound identity conflict | partial | Panel records form=citrate (550mg), form_raw=oxide+citrate blend. Page correctly calls it "תערובת ציטראט ואוקסיד". Elemental claim: 89mg; 550mg × 16.2% (citrate) = 89.1mg — internally consistent. But the exact ratio of oxide:citrate is unverified (partial confidence), making the elemental estimate unverifiable. Copy notes "הרכב המדויק לא מאומת" — honest. |
| 0033984005181 | Solgar Ca+Mg+D 150 | 49 | D | DATA ERROR — wrong Mg dose stated | verified | bsip0s_label maps all actives to vitamin_d3 slug; engine scored on 200mg Ca-citrate as Mg. Page states "מגנזיום ציטראט 200 מ\"ג" — WRONG. Actual Mg = 100mg per panel. Grade (D) survives correction (100mg citrate → ~16mg elemental → fairy_dust), but the stated dose is factually wrong for a real product on a verified (brand_panel) source. Routes to: data-agent, nutrition-agent. |
| 7290118816065 | Supherb TRIOMAG 60 | 34 | E | Plausible | partial | Evidence cap (cap_1) for unverified blend claim. rowVerdict "חסום ב-34/E" = leakage. |
| 7290001065594 | Nutricare Nano Lipo 60 | 34 | E | Plausible | partial | Evidence cap for liposomal nano claim. Image unverifiable (generic "nano-magnesium-Copy.webp"). rowVerdict "חסום ב-E" = leakage. |
| 7290018439043 | Nutricare WELL 90 | 34 | E | Plausible | partial | Evidence cap for undefined "WELL" claim. 168mg bisglycinate = 23.7mg elemental — not separately stated in copy. rowVerdict "חסום ב-E" = leakage. |

---

## Summary Assessment

**Plausible-but-unverifiable (overall)** with several specific weak and incorrect elements.

The high-level narrative (oxide paradox, dose beats form when form is under-dosed, evidence caps for marketing claims) is coherent and grounded. The scoring architecture produces defensible relative rankings. However, the copy layer introducing factual numbers to consumers (elemental fractions, mg doses) contains systematic errors for four compound types, plus one verified product with a misrouted active in the pipeline that propagates a wrong dose into consumer-facing text.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: Elemental fraction percentages in consumer-facing copy are chemically wrong for four compound types.**
- Malate: copy says "כ-9% יסודי", chemistry = 15.5% (Mg malate, MW=156.4). 700mg malate → page claims 63mg, actual = 108.5mg.
- Bisglycinate: copy says "כ-50 מ\"ג יסודי" from 250mg, implying 20%; chemistry = 14.1% (Mg bisglycinate, MW=172.4), actual = 35.3mg.
- Citrate: copy says "כ-42 מ\"ג" from 200mg (21%) and "כ-53 מ\"ג" from 250mg (21%); chemistry = 16.2% (trimagnesium dicitrate), actual = 32.4mg and 40.5mg respectively.
- Taurate (~8mg from 76mg): chemistry = 8.9%, gives 6.8mg — within acceptable rounding, not flagged as error.
- Carbonate (46mg from 160mg): chemistry = 28.8%, gives 46.1mg — CORRECT (matches SUPP-EV-028).
- Evidence: positiveSignals and limitingFactors in expansion panel for barcodes 7290001066973, 7290015318532, 7290011899967, 7290013464248, 7290019444480.
- Implication: A food scientist or journalist will immediately spot these errors. The explanation given to consumers for why a product scored low (the stated elemental amount) is factually wrong. The verdict (underdosed) may still be correct, but the stated numbers are not. An adversarial regulator could use these errors to challenge the entire methodology's credibility.
- Routes to: nutrition-agent (verify correct elemental fractions and update copy), data-agent (verify whether the engine itself uses wrong fractions or only the copy is wrong).

**RT-2: Solgar Ca+Mg+D (barcode 0033984005181): page states magnesium dose as 200mg; actual magnesium per panel = 100mg.**
- The corpus bsip0s_label misrouted all three actives (Ca, Mg, D3) to active_slug=vitamin_d3; the engine scored on 200mg Ca-citrate as if it were the magnesium dose. The page copy ("מגנזיום ציטראט 200 מ\"ג" in insightLine, rowVerdict, and expansion.ingredients) states the wrong dose for a verified brand-panel product.
- The grade (D/49) very likely survives: correct Mg = 100mg × 16.2% = 16.2mg elemental, even more deeply fairy_dust than the miscalculated 200mg path. But a consumer reading the label will see 100mg Mg, not 200mg as the page says.
- Evidence: corpus bsip0s_label[0] shows quantity=200, display_name=calcium (calcium citrate), active_slug=vitamin_d3. Panel actives[1] shows magnesium at 100mg.
- Implication: Factually wrong consumer-facing number for a real product from a verified source. A product brand (Solgar) could dispute this claim publicly.
- Routes to: data-agent (fix the bsip0s_label routing for Solgar), nutrition-agent (re-verify score after correction), content-agent (update page copy for insightLine, rowVerdict, ingredients).

**RT-3: Systematic leakage of scoring mechanism in consumer-visible rendered text.**
- Methodology footer (rendered `<p>` tags): "מוצרים שנחסמו בגלל מינון לא מוצדק ('אבק פיות') מקבלים תקרה של 49/D" and "מוצרים שנחסמו בגלל עדות בלתי מספקת לטענה המרכזית מקבלים תקרה של 34/E" — both render as visible text, exposing the cap architecture and specific score floor values.
- Three E-grade rowVerdicts (TRIOMAG, Nano Lipo, WELL) render "חסום ב-34/E" or "חסום ב-E" in the collapsed row — visible without any user interaction.
- Amorphicure insightLine: "חסום בגלל תת-מינון" — visible on collapsed row, explains the blocking mechanism.
- Internal sub-scores in positiveSignals/limitingFactors: "92/100 בדירוג הצורה", "72/100", "17/100" — rendered in expansion.
- Evidence: HTML text nodes confirmed by entity-encoded text search (&#x27;אבק פיות&#x27; rendered in <p>).
- Implication: This is a Hard Rule 1 violation (Never PASS if any leakage checklist item fails). A consumer or journalist reads "תקרה של 49/D" and infers the scoring uses hard cap floors — the mechanism is fully visible. The page cannot pass the leakage gate.
- Routes to: content-agent (rewrite methodology lines to describe in consumer language without cap values), content-agent (rewrite E-grade rowVerdicts to remove "חסום ב-E"), content-agent (rewrite Amorphicure insightLine to remove "חסום בגלל"), content-agent (remove raw sub-scores from positiveSignals).

**RT-4: Prologue explicitly predicts what grade each form type will receive, exposing scoring architecture.**
- Rendered text: "אוקסיד ייגמר ב-B, צורות טובות ייגמרו ב-D כשהמינון לא מוצדק" — this tells the consumer the scoring assigns B to oxide and D to good-form products with low dose, which is an explanation of the scoring algorithm's grade-band assignments.
- This is structurally different from describing the market finding (oxide products happen to have higher dose on this shelf). It pre-announces grade outcomes by form type, which is framework leakage at the hero/prologue level.
- Evidence: C:\bari\bari-web\src\lib\comparisons\magnesium-page-data.ts line 21 (magnesiumPrologueSentences[3]).
- Routes to: content-agent (reframe as an observed market finding without predicting grades by form type).

### HIGH — should resolve before launch

**RT-5: Altman Balance insightLine claims "ציון זהה לגרסה הבסיסית" (same score as basic version) — factually wrong.**
- Altman Balance scores 62/C. No other Altman oxide product scores 62: Altman UP = 70/B, Altman 520 = 66/B. The "basic version" the copy appears to reference does not exist at score 62.
- Evidence: score comparison from corpus; insightLine at magnesium-page-data.ts (product 7290019444206).
- Routes to: content-agent.

**RT-6: Altman Balance expansion.ingredients omits ashwagandha KSM-66 (50mg), valerian (50mg), and vitamin B6 (30mg).**
- The corpus panel records four actives for this product. The page shows only "מגנזיום (from oxide), 450 מ\"ג לכמוסה". For a supplement where consumers need to see the full active ingredient list to assess interactions and tolerability, omitting three named actives (including a herbal sedative, valerian) is a material disclosure gap.
- Evidence: corpus panel actives for barcode 7290019444206 show all four actives. Page expansion.ingredients in magnesium-page-data.ts shows only the oxide.
- Routes to: content-agent (add full active ingredients to expansion.ingredients).

**RT-7: Two images with unverifiable identity.**
- 7290013142894 (Altman MagUp): UUID filename on brand site — product identity cannot be confirmed from the URL alone. If the image is wrong, consumers see an incorrect product photo for the category leader.
- 7290015318426 (Tink Oxide 520): catalog_941469-l.jpg with timestamp query — no barcode anchoring. Tink has multiple magnesium products; this could be any of them.
- Routes to: data-agent (verify both images link to the correct product by checking the brand/retailer page where each was sourced).

**RT-8: Oxide paradox framing does not disclose absorption-adjusted outcome.**
- The prologue correctly warns that oxide's dose advantage does not mean it is the "better" product. The categoryNote explains bioavailability. However, the scoring still ranks oxide HIGHER, and no product row explicitly states the absorption-adjusted net magnesium. A consumer who scans only the collapsed row sees oxide scored higher than bisglycinate and may reasonably conclude oxide is the better supplement — the opposite of what clinical absorption data suggests.
- Specific numbers: Altman UP oxide 450mg = ~271mg elemental at ~4% absorption (Schuette/Lindberg) → ~11mg net absorbed. Altman bisglycinate 250mg = ~35mg elemental at ~46% absorption (Coudray 2005) → ~16mg net absorbed. The lower-scoring bisglycinate product delivers ~46% more absorbed magnesium than the category leader by score. The page does not disclose this.
- Assessment: the framing is HONEST about the paradox's existence but INCOMPLETE about its magnitude. The page says the oxide "wins" on dose and warns about absorption — it does not quantify that the bisglycinate may actually deliver more usable magnesium. For a prototype/EDPG candidate, this is defensible if acknowledged. For consumer launch it is HIGH risk.
- Routes to: nutrition-agent (decision: should absorption-adjusted net Mg be disclosed? Is the scoring philosophy choosing dose-only intentionally or as a simplification?).

### MEDIUM — should document or monitor

**RT-9: Magnolia / Magnesia brand (5 premarket products) and Life brand (3-4 name_derived products) have zero page coverage with no disclosure.**
- The page scores 19 of 29 magnesium products; 10 are omitted. The corpus shows 5 Magnesia-brand premarket products and 3-4 Life-brand name_derived products with zero scored representation. The page does not mention these brands are absent.
- Magnesia is a distinct Israeli brand present on shelf. A consumer looking for Magnesia products on this page will find nothing, with no explanation. For the category note to be complete, brand omissions of this scale should be disclosed.
- Routes to: content-agent (add disclosure of omitted brands to categoryNote or methodology), product-agent (decision on disclosure standard for prototype pages).

**RT-10: TRIOMAG insightLine says "ספיגה מיטבית" but page then challenges the claim — framing inconsistency.**
- The insightLine for TRIOMAG: "שלושה סוגי מגנזיום — טענת 'ספיגה מיטבית' לא מגובה בעדות מספקת." This quotes a marketing claim the product itself makes, but a consumer might not understand whether Bari endorses or challenges it. The "לא מגובה" clarification follows, but in a fast scan the claim appears endorsed.
- Routes to: content-agent (restructure insightLine to lead with the Bari finding, not the marketing claim).

**RT-11: Tink Oxide and Nutricare 520 tie-break order within the 66/B band is arbitrary.**
- Three products score 66/B (Nutricare 520, Tink 520, Altman 520). The corpus does not provide a tie-breaking signal; page order appears to be corpus order. The page makes no disclosure that within-band ordering is arbitrary.
- For an EDPG prototype this is acceptable, but for consumer launch the tie-breaking rule must be defined and documented.
- Routes to: product-agent, data-agent.

**RT-12: Score metadata date mismatch.**
- Page metadataLine: "19 מוצרים • נובמבר 2026". The corpus was generated 2026-06-19. The November 2026 date is a prospective / future date — it is not the actual run date. For a prototype this is a placeholder but it must not ship with a future date as if it were a publication date.
- Routes to: content-agent.

---

## Oxide Paradox Framing Verdict

The oxide paradox framing — that cheap high-dose oxide outranks premium under-dosed citrate/bisglycinate — is **honest about its existence** but **incomplete about its consequence**. The prologue (sentence 2) and the categoryNote correctly explain the mechanism. The key problem is not the framing itself but that:

1. The scoring ranks oxide HIGHER in the table, and consumers reading the collapsed row see oxide at rank 1 with a higher score than bisglycinate at rank 12+. The copy warns about bioavailability but the score chip contradicts it.
2. The copy does not disclose that on an absorption-adjusted basis, the highest-scoring oxide product may deliver less usable magnesium than several of the D-grade bisglycinate products it outranks.
3. A regulator or journalist asking "does your scoring guide consumers toward the product that actually works less well?" would have a valid point. The honest answer requires disclosing absorption-adjusted comparisons, which the page does not do.

The framing is not fraudulent, but it is not complete enough for consumer-facing use. For the EDPG prototype stage this is HIGH, not CRITICAL, because the page clearly marks itself as candidate/draft.

---

## Image Identity Verdict

14/19 images are confirmed by barcode in filename — strong identity evidence. 2/19 are unverifiable from the URL (Altman MagUp UUID, Tink catalog ID). 3/19 are plausible but not confirmed. No OFF-sourced images. No obviously wrong products were detected from URL analysis, but the two UUID/catalog-ID cases cannot be cleared without checking the source page directly. Rated HIGH, not CRITICAL, because these are brand-site or trusted Israeli retailer images — the risk of a wrong image is real but not certain.

---

## Verdict

**FAIL — launch blocked.**

Track V: FAIL (leakage checklist — 6 items fail; scores/grades themselves propagate correctly).
Track C: FAIL — 4 open CRITICAL findings. The D10 gate requires zero open CRITICALs.

**Named blockers (must resolve before any consumer-facing deployment):**
- RT-1: Chemically wrong elemental fraction numbers in copy for malate, bisglycinate, citrate — routes to nutrition-agent + content-agent.
- RT-2: Solgar Ca+Mg+D magnesium dose stated as 200mg when corpus panel shows 100mg Mg — routes to data-agent + content-agent.
- RT-3: Scoring cap mechanism (תקרה של 49/D, חסום ב-34/E, חסום בגלל תת-מינון) rendered in consumer-visible HTML — routes to content-agent.
- RT-4: Prologue predicts grade outcomes by form type (oxide→B, good forms→D) — routes to content-agent.

**HIGH findings (should resolve before launch, acknowledged before CONDITIONAL PASS):**
RT-5 (Balance insightLine wrong), RT-6 (Balance ingredients incomplete), RT-7 (2 unverifiable images), RT-8 (absorption-adjusted outcome not disclosed).

---

## Return Contract JSON

```json
{
  "agent": "adversarial-qa-agent",
  "task_ref": "EDPG-magnesium-prototype-gate",
  "run_date": "2026-06-19",
  "artifacts_read": [
    {
      "path": "C:\\bari\\bari-web\\src\\lib\\comparisons\\magnesium-page-data.ts",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v8.json",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\bari\\bari-web\\src\\app\\hashvaot\\magnesium\\page.tsx",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\bari\\bari-web\\src\\components\\comparisons\\magnesium-comparison-page.tsx",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\bari\\bari-web\\src\\components\\comparisons\\comparison-page.tsx",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\bari\\bari-web\\src\\lib\\view-models\\index.ts",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "C:\\bari\\bari-web\\next.config.ts",
      "sha256": "not_computed_read_only"
    },
    {
      "path": "http://localhost:3000/hashvaot/magnesium",
      "sha256": "live_fetch_92073_bytes"
    }
  ],
  "counts": {
    "products_in_corpus_magnesium_engine": "29 (denominator: all engine_active==magnesium records)",
    "products_scored": "19 of 29",
    "products_on_page": "19 of 19 scored (100%)",
    "products_omitted_premarket": "6 (Magnesia brand x5, Tink Taurate x1)",
    "products_omitted_incomplete": "4 (Life brand x3, Hadas x1)",
    "score_propagation_pass": "19 of 19",
    "grade_propagation_pass": "19 of 19",
    "confidence_mapping_pass": "19 of 19",
    "images_confirmed": "14 of 19",
    "images_plausible": "3 of 19",
    "images_unverifiable": "2 of 19",
    "images_off_sourced": "0 of 19",
    "leakage_checklist_pass": "7 of 13 applicable items",
    "leakage_checklist_fail": "6 of 13 applicable items",
    "critical_findings": 4,
    "high_findings": 4,
    "medium_findings": 4
  },
  "commands_run": [
    {"cmd": "npm run build (C:\\bari\\bari-web)", "exit_code": 0},
    {"cmd": "Invoke-WebRequest http://localhost:3000/hashvaot/magnesium", "exit_code": 0, "status_code": 200},
    {"cmd": "Invoke-WebRequest http://localhost:3000/sitemap.xml (magnesium not found)", "exit_code": 0},
    {"cmd": "Invoke-WebRequest http://localhost:3000/hashvaot (magnesium not linked)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit.py (corpus extraction)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit2.py (form scores)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit3.py (Solgar audit)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit4.py (Solgar full trace)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit5.py (dose threshold analysis)", "exit_code": 0},
    {"cmd": "python3 _tmp_mg_audit6.py (Balance ingredients check)", "exit_code": 0}
  ],
  "not_done": [
    "E2E / Playwright test run not performed (npm run test:e2e not executed — live server confirmed by HTTP 200 fetch)",
    "Hebrew readability tool (C:\\Bari\\integrations\\clients\\hebrew_readability.py) not invoked — leakage confirmed by direct HTML text search",
    "run_gates.py not invoked — no gates.py configured for supplement category (food categories only); leakage audit performed manually",
    "Visual screenshot / mobile geometry not measured — geometry checklist requires browser rendering at 375px; not performed in this pass",
    "Crossref / SemanticScholar adversarial evidence client not invoked — evidence weight challenge deferred to nutrition-agent",
    "Image HTTP 200 check not performed for individual imageUrls — proxy domains confirmed in next.config.ts; direct URL resolution not tested"
  ],
  "spec_acceptance_test": {
    "result": "FAIL",
    "reason": "4 open CRITICAL findings block the D10 go-live gate. Track V fails leakage checklist (6 items). Track C: RT-1 chemistry errors, RT-2 Solgar dose error, RT-3 scoring mechanism leakage, RT-4 prologue grade prediction are all CRITICAL and unresolved."
  }
}
```
