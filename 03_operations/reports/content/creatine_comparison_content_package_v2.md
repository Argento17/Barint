# Creatine Comparison Page — Content + Data Package v2 (TASK-492C)

**Type:** Content+Data authoring lane — FINAL build-ready DRAFT package for the creatine
supplement comparison page. Folds the upgraded 13-product worldwide benchmark
(`creatine_benchmark_solid_v1.md`) and the five Product rulings
(`creatine_page_model_decision_v1.md`) into the stage-1 base
(`creatine_comparison_content_package_v1.md`).
**Status: RETURNED (proposed).** This is a DRAFT. Every Hebrew consumer string here is
*unsigned draft copy* until BOTH gates sign off (Content Agent + Adversarial QA / Red-Team),
per the standing two-gate hard rule. Nothing here builds the app page and nothing publishes.
**Author:** Content+Data authoring lane
**Date:** 2026-07-03
**Gate-revision (2026-07-03):** revised in place against the red-team report
(`creatine_comparison_redteam_v1.md`) and the voice gate. Applied: RT-1 (Sports Research B6
downgraded from directory-verified to manufacturer-stated; directory-verified count reconciled to
exactly 6 — Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel), RT-2 (grocery-channel
overclaim corrected to 3 Shufersal + 1 imported MyProtein tablet), the four "X, not Y" antithesis
rewrites, the three em-dash header separators, the MyProtein Elite 3.0 g / 3.4 g cross-reference
note, and the bipolar PMID 17988366 verification note. No new claims or data introduced. Still a
draft pending both gate sign-offs.
**Brand spelling used throughout:** בארי (never ברי).

## What changed from v1 (diff summary)

1. **Worldwide benchmark swapped: 5 products → 13 verified products** (US 7, Canada 1, UK/EU 4,
   AU 1). Each row now carries form, g/serving, price, servings, and a **two-tier certification
   label** per Product ruling 2.
2. **NO A–E grade (Product ruling 1).** `score`/`grade` are null on every product. The page
   headlines the **dose-honesty verdict** (honest / below-floor / undisclosed) and ranks on
   **price-per-effective-gram**. Headline + sort are now defined explicitly (§1.0).
3. **Two-tier cert labels applied everywhere (ruling 2).** "אומת מול מאגר" ONLY for the 6
   NSF-directory-confirmed worldwide rows (Thorne, Momentous, Klean Athlete, BPN, MegaFood,
   BioSteel). All other cert claims = "מוצהר על-ידי היצרן". ESN = honest uncertified comparator.
   Zero Israeli products qualify for "אומת מול מאגר".
4. **MyProtein Elite ≠ Creapure correction carried (ruling constraint).** The Israeli-shelf
   "Creatine Monohydrate Elite" and the worldwide "Elite" row are both labeled generic
   monohydrate (page states NOT Creapure). The Creapure SKU ("THE Creatine Creapure") is a
   separate row in both tables.
5. **Price disclosure = one page-level as-of-date + "may vary" line (ruling 3).** Added to the
   category-note block; removed any implication of per-row date stamping.
6. **Dairy ships now with a single-retailer caveat (ruling 4).** Yoplait GO = "amount not
   disclosed"; Tnuva GO = collagen. Inline Shufersal-only caveat added.
7. **Cognitive claim cut (ruling 5).** The uncited positive-population cognitive sentence is
   removed from §2.3. The cited EFSA null-general-cognition line stays.
8. **Israel = 0 ship-ready worldwide-grade products.** Super Effect and Alfa exist on the
   Israeli shelf but lack a verifiable per-serving dose, so neither enters the worldwide-grade
   benchmark. They remain in the 18-product Israeli shelf table only as scraped (dose
   undisclosed).
9. Product counts updated throughout: **18 Israeli shelf + 13 worldwide benchmark = 31 products**
   (v1 was 18 + 5 = 23).

## Allowed inputs used (verified-only)
- `03_operations/reports/content/creatine_comparison_content_package_v1.md` — stage-1 base.
- `03_operations/reports/research/creatine_benchmark_solid_v1.md` — upgraded 13-product worldwide benchmark (REPLACES the old 5-product table).
- `03_operations/reports/content/creatine_page_model_decision_v1.md` — Product rulings 1–5 (all applied).
- `03_operations/reports/research/creatine_supplement_shelf_scrape_v1.md` — 18 Israeli products, dose-honesty classes, price-value.
- `bari-web/src/lib/comparisons/magnesium-page-data.ts` + `.../app/hashvaot/magnesium/page.tsx` — structural template (score/grade fields left null here).

## What is deliberately EXCLUDED (per hard constraints + rulings)
- **A–E score/grade** — null on every product (ruling 1). No engine, so no grade.
- **The positive-population cognitive claim** — cut entirely (ruling 5). Only the cited EFSA null-general line remains.
- **"Creapure" descriptor for Momentous** — the brand's own current page states it no longer sources from Creapure. A stale Vitacost reseller title still reads "Creapure"; the brand page is the higher-authority source. The word is not applied to Momentous anywhere here.
- **"NIH / NIH ODS" attribution** — not used anywhere. Safety grounds on ISSN 2017, the kidney-function meta-analyses, and EFSA.
- **Informed-Sport "directory-verified" badges** — the Informed-Sport certifier site (sport.wetestyoutrust.com) returned HTTP 403 on all fetch attempts; no Informed-Sport claim is shown as directory-verified. All Informed-Sport/Informed-Choice claims carry "מוצהר על-ידי היצרן" only.
- **Israeli products in the worldwide-grade benchmark** — 0 qualify. Super Effect and Alfa lack a verifiable per-serving dose and are excluded from the benchmark (present only in the Israeli shelf table with dose undisclosed).
- **Any specific dairy-matrix retention percentage** — qualitative framing only; no computed Yoplait dose.
- **Dropped worldwide candidates** — Transparent Labs (creatine+HMB blend only, confirmed on NSF list), Optimum Nutrition (confirmed absent from NSF list), Bulk Nutrients (unresolved per-SKU spec) are NOT in the benchmark table.

---

## 1. Ranked product-table data

### 1.0 Headline + ranking model (Product ruling 1 — no A–E grade)

**There is no A–E grade and no numeric Bari score on this page.** Creatine has no scored BSIP2
engine, and monohydrate at an honest dose is evidence-equivalent across brands. Forcing a graded
spread would manufacture differentiation the science does not support. Instead:

- **Primary headline = dose-honesty verdict**, one of three bands per product:
  `honest — meaningful dose` / `disclosed, below floor` / `undisclosed`. This is the real
  differentiator on the Israeli shelf (4/18 undisclosed, all in the grocery channel).
- **Primary sort / ranking signal = price-per-effective-gram** (₪ per 3 g effective dose),
  computed only where BOTH a per-serving dose AND servings-per-container were disclosed. Within
  the honest-dose tier this is the load-bearing finding: HCl products cost 6–10× more per
  effective gram than monohydrate for no evidenced benefit.
- **Cert status = a two-tier badge, not a ranking input** (§1.1 / ruling 2).
- **Form = a badge** (monohydrate vs HCl), not a ranking input.

Product-model term for Frontend/Data: reuse `BariProductVM`, but `score` and `grade` are `null`
for every creatine product (Israeli and worldwide). `insightLine`/`rowVerdict` carry the
dose-honesty + price-value verdict as the headline, exactly the role those fields already play on
the magnesium page's no-score rows.

### 1.1 The ranking lens (four pillars — magnesium precedent, creatine substitutions)

Per co-sign §3.1. This moves NO published score; it is a supplement comparison, zero BSIP2 exposure.

1. **Dose adequacy** — creatine's studied maintenance range is **3–5 g/day** (floor ~3 g/day;
   ISSN 2017, PMID 28615996). A named form at ≥3 g/day is in-range; 3 g/day sits *at* the floor
   (low end, not below it); a named-and-quantified figure below 3 g/day is reported honestly as
   sub-floor, never mislabeled "fairy dust." Undisclosed / blend-hidden dose → the dose is
   unknowable, flagged as a transparency gap.
2. **Form — monohydrate is the evidence-based default.** Virtually all the evidence was generated
   on monohydrate. HCl, buffered/"alkaline," ethyl ester, citrate/malate carry no human evidence
   of superiority. Alternative forms are a formulation choice, not a defect and not unsafe — they
   simply carry no evidenced advantage over the cheaper, better-studied monohydrate.
3. **Third-party testing** — NSF Certified for Sport / HASTA / Informed-Sport certification is a
   real differentiator for the "will this pass a doping test / is this what the label says" use
   case. Presented via the **two-tier badge** (ruling 2): "אומת מול מאגר" only where the
   certifier's own directory was directly confirmed; "מוצהר על-ידי היצרן" for every brand-page
   claim not directory-confirmed.
4. **Price-value** — cost per effective daily gram of creatine (price ÷ total grams in container,
   normalized to a 3 g dose). The load-bearing finding: **HCl products cost 6–10× more per
   effective gram than monohydrate** on the Israeli-available shelf.

### 1.2 Israeli shelf — 18 products (direct scrape, verified)

Source: `creatine_supplement_shelf_scrape_v1.md` §3. Dose-honesty classes per co-sign §4.
`price_per_3g` is computed only where BOTH dose and servings-per-container were disclosed
(so total container grams is knowable) — never assumed. **All cert claims below are
"מוצהר על-ידי היצרן" (manufacturer-stated); zero Israeli products are directory-confirmed.**

| # | Name (display) | Brand | Channel | Barcode/SKU | Form | g/serving | Servings | Price ₪ | ₪ per 3 g | 3rd-party cert (page claim → tier) | Dose-honesty verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | קריאטין מונוהידראט ענבים | Super Effect | Shufersal | 7290014386006 | monohydrate | not disclosed | — | 119.00 | — | none found | undisclosed |
| 2 | קריאטין מונוהידראט פירות | Super Effect | Shufersal | 7290016392005 | monohydrate | not disclosed | — | 119.00 | — | none found | undisclosed |
| 3 | אבקת קריאטין (All In) | All In | Shufersal | 7290019766223 | monohydrate | 3.0 g | 83 | 99.90 | none found | 1.20 | honest — meaningful dose |
| 4 | אבקת קריאטין מונוהידראט | Sport GS | Shufersal | 7290010081288 | monohydrate | not disclosed | — | 167.00 | — | none found | undisclosed |
| 5 | Impact Creatine (250 g) | MyProtein | MyProtein-IL | 5055534302002 | monohydrate | 3.0 g | 73 | 75.31 | Informed Choice → מוצהר על-ידי היצרן | 1.03 | honest — meaningful dose |
| 6 | Creapure Micronised Capsules | MyProtein | MyProtein-IL | not disclosed | monohydrate (Creapure) | 2.8 g | — | 146.00 | — | none found | disclosed, below floor (partial, 2.8 g) |
| 7 | Creatine Gummies | MyProtein | MyProtein-IL | not disclosed | monohydrate | 3.0 g (3×1 g) | — | 204.00 | — | none found | honest — meaningful dose |
| 8 | Creatine Monohydrate Elite | MyProtein | MyProtein-IL | not disclosed | monohydrate (generic, NOT Creapure) | 3.0 g | — | 284.00 | — | Informed Choice → מוצהר על-ידי היצרן | honest — meaningful dose |
| 9 | Creatine Monohydrate Tablets | MyProtein | MyProtein-IL | not disclosed | monohydrate (tablet) | not disclosed | — | 60.00 | — | none found | undisclosed |
| 10 | THE Creatine Creapure | MyProtein | MyProtein-IL | not disclosed | monohydrate (Creapure) | 3.0 g | — | 213.00 | — | Informed Choice → מוצהר על-ידי היצרן | honest — meaningful dose |
| 11 | Micronized Creatine Powder | Optimum Nutrition | iHerb-IL | 748927023855 | monohydrate | 5.0 g | 120 | 122.89 | Informed Choice → מוצהר על-ידי היצרן | 0.61 | honest — meaningful dose |
| 12 | Creatine | Thorne | iHerb-IL | 693749006350 | monohydrate | 5.0 g | 90 | 133.43 | NSF Certified for Sport → מוצהר על-ידי היצרן* | 0.89 | honest — meaningful dose |
| 13 | Sports Micronized Creatine | NOW Foods | iHerb-IL | 733739020383 | monohydrate | 4.2 g | ~119 | 86.21 | none found | 0.52 | honest — meaningful dose |
| 14 | Platinum 100% Creatine | MuscleTech | iHerb-IL | 631656705737 | monohydrate | 5.0 g | ~80 | 102.46 | none found (HPLC-tested claim only) | 0.77 | honest — meaningful dose |
| 15 | Sport Pure Creatine (capsules) | California Gold Nutrition | iHerb-IL | 898220022830 | monohydrate (capsule) | 0.75 g/capsule | 240 | 57.95 | "iTested" → מוצהר על-ידי היצרן | 0.97 | disclosed, below floor (per-capsule; daily count undisclosed) |
| 16 | Creatine Monohydrate Micronized | ABE | iHerb-IL | 5056555204153 | monohydrate | 4.25 g | 60 | 54.90 | Informed Sport → מוצהר על-ידי היצרן | 0.65 | honest — meaningful dose |
| 17 | Creatine HCl | Kaged | iHerb-IL | 850045966478 | **HCl** | 0.75 g | ~75 | 89.15 | Informed Sport → מוצהר על-ידי היצרן | 4.75 | disclosed, below floor (HCl nominal-dose pattern) |
| 18 | Creatine HCl | Con-Cret | iHerb-IL | 682676700646 | **HCl** | 0.75 g | 64 | 86.12 | NSF Certified for Sport → מוצהר על-ידי היצרן* | 5.38 | disclosed, below floor (HCl nominal-dose pattern) |

\* Thorne and Con-Cret state "NSF Certified for Sport" on their iHerb page. This is the Israeli
*retail-page* claim, **not** directory-confirmed for the specific Israeli-sold SKU, so it carries
"מוצהר על-ידי היצרן" here. (Thorne's US SKU IS NSF-directory-confirmed in the worldwide table
below; the Israeli iHerb listing was not separately directory-matched, so it stays
manufacturer-stated on this shelf per ruling 2's discipline.)

**Distributions (verified, from the scrape):**
- Dose-honesty: 10/18 honest meaningful-dose · 1/18 partial (2.8 g) · 3/18 disclosed-below-floor (2 HCl + 1 single-capsule) · 4/18 undisclosed · 0/18 blend-hidden.
- Form: 16/18 monohydrate · 2/18 HCl.
- Undisclosed dose concentrates on the grocery channel: all 4 undisclosed are Shufersal (3) + 1 MyProtein tablet; 0 iHerb powder/capsule products with a facts panel were undisclosed.
- Third-party cert (page claim, all "מוצהר על-ידי היצרן"): 9/18. Directory-confirmed: 0/18.
- Price-per-3 g range (computed subset): ₪0.52 (NOW Foods) to ₪5.38 (Con-Cret HCl).

### 1.3 Worldwide benchmark — 13 directly-verified products (6 regions)

Source: `creatine_benchmark_solid_v1.md` §1 (REPLACES the old 5-product table). Cert tier per
ruling 2: **"אומת מול מאגר" only for the 6 NSF-directory-confirmed rows** (Thorne, Momentous,
Klean Athlete, BPN, MegaFood, BioSteel); everything else "מוצהר על-ידי היצרן"; ESN is the honest
uncertified comparator. Prices are point-in-time and re-verified at build (§5).

| # | Region | Brand / Product | Form | g/serving | Servings | Price (local) | ₪/3 g (USD est.) | Cert — tier |
|---|---|---|---|---|---|---|---|---|
| B1 | US | Thorne Creatine (Micronized) | monohydrate | 5 g | 90 | ~$36–44 | ~$0.27 | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com id 1204244) |
| B2 | US | Momentous Creatine Monohydrate | monohydrate (brand states NOT Creapure) | 5 g | 90 | $42.99 / $32.24 sub | ~$0.19–0.26 | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com id 1285010). Stale Vitacost reseller title reads "Creapure"; brand page overrides — do not use that word. |
| B3 | US | Klean Athlete — Klean Creatine | monohydrate | 5 g | 63 | not captured | not computed | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com id 1121640) |
| B4 | US | Bare Performance Nutrition (BPN) — Creatine Monohydrate | monohydrate | 5 g | 30 / 60 | $34.99 / $26.24 sub | ~$0.16–0.21 | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com id 1635096) |
| B5 | US | MegaFood — Micronized Creatine Monohydrate | monohydrate | 5 g | 100 | not captured | not computed | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com, active) |
| B6 | US | Sports Research — Creatine Monohydrate Unflavored | monohydrate | 5 g | ~90 | not captured | not computed | NSF Certified for Sport (brand page) → **מוצהר על-ידי היצרן** (specific SKU not directory-confirmed this pass). Separate Sports Research Creapure SKU is brand-page claim only; do not conflate the two. |
| B7 | US | Naked Nutrition — Naked Creatine | monohydrate | 5 g | 100 / 200 | $35.99 / $28.79 sub | ~$0.17–0.22 | "NSF-certified" (brand page) → **מוצהר על-ידי היצרן** (no matching directory listing located) |
| B8 | Canada | BioSteel — Creatine (72 servings) | monohydrate | **2.5 g — below the 3 g/day floor at one scoop** | 72 | $19.99 / $13.99 sale | ~$0.17–0.24 (at 1 scoop) | NSF Certified for Sport → **אומת מול מאגר** (nsfsport.com id 1292599) |
| B9 | UK/EU | Applied Nutrition — Creatine Monohydrate (100%) | monohydrate | 5 g | 200 (1 kg) | £18.95–£24.95 | ~$0.14–0.19 | Informed-Sport (brand page) → **מוצהר על-ידי היצרן** (certifier site 403; not directory-confirmed) |
| B10 | UK/EU | MyProtein — Creatine Monohydrate Elite | monohydrate (generic, page states NOT Creapure) | 3.4 g | 294 (1 kg) | £30.99 | ~$0.37 | Informed-Sport (brand page) → **מוצהר על-ידי היצרן** |
| B11 | UK/EU | MyProtein — THE Creatine (Creapure) | monohydrate (Creapure, on-page) | 3.4 g | ~147 (500 g) | £36.49 | ~$0.44 | Informed Choice (brand page) → **מוצהר על-ידי היצרן** |
| B12 | AU | Switch Nutrition — Perform Purest Creatine | monohydrate | 3 g | 167 | $74.95 AUD | ~$0.49 | HASTA (brand page) → **מוצהר על-ידי היצרן** (HASTA directory not cross-checked this pass) |
| B13 | Germany/EU | ESN — Ultrapure Creatine Monohydrate | monohydrate, microfine | 3.5 g | 142 (500 g) | €29.90 | ~$0.34 | **none — honest uncertified comparator** (Kölner Liste footer mention only, not a confirmed listing) |

**Notes carried forward:**
- **Cert tier honesty:** 6/13 directory-confirmed (all NSF: Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel), 6/13 manufacturer-stated (Naked, Applied Nutrition, both MyProtein SKUs, Switch Nutrition, and Sports Research — brand-page NSF claim, specific SKU not directory-confirmed this pass), 1/13 explicitly uncertified (ESN). Sports Research's brand page states NSF Certified for Sport, but the specific SKU was not matched in the NSF directory this pass, so it carries "מוצהר על-ידי היצרן" per ruling 2's discipline.
- **BioSteel (B8) delivers 2.5 g at one labeled scoop — genuinely below the 3 g floor**, the clearest "sub-therapeutic at labeled serving" case in the set. Do not equate it with the 5 g rows.
- **MyProtein Elite (B10) is NOT Creapure** — corrects the prior 5-product table. The Creapure SKU (B11) is a separate product. Both serve 3.4 g (not 3 g), above the floor, low end.
- **MyProtein "Creatine Monohydrate Elite" appears in both tables at two doses** — Israeli row #8 lists 3.0 g (myprotein.co.il, Israeli scrape pass) and worldwide row B10 lists 3.4 g (myprotein.com UK/EU listing, later benchmark pass). This is the same branded SKU captured on two regional listings in two passes, not a data conflict; both figures are above the 3 g floor. A one-line on-row footnote should carry this cross-reference so a reader who notices the name match has the explanation on-page.
- **Switch Nutrition (B12) and the two MyProtein rows deliver 3–3.4 g** (at/just above the floor), not the 5 g typical dose — do not silently equate them with the 5 g products in copy.
- **Informed-Sport is never shown as directory-verified** (certifier site 403 on all attempts).

---

## 2. Evidence sections copy (Hebrew) — DRAFT

All strings below are unsigned draft copy. Voice: finding-first, assertive, positive
declaratives, minimal em-dashes, no engine jargon, no "X, not Y" antithesis. Every number and
citation is the corrected/verified one.

### 2.1 Hero + metadata

**eyebrow:** `תוספי קריאטין`
**title:** `קונים קריאטין? המינון והצורה קובעים את השווי. המחיר מספר סיפור נפרד.`
**metadataLine:** `18 מוצרים מהמדף הישראלי · 13 מותגי ייחוס עולמיים · יולי 2026`

### 2.2 Prologue (mirrors magnesiumPrologueSentences)

```
בדקנו 18 תוספי קריאטין הזמינים לצרכן הישראלי, מול שלושה-עשר מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: כמה קריאטין המוצר מספק במנה, באיזו צורה כימית, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.

המינון היומי שנחקר לתחזוקה הוא 3 עד 5 גרם ליום, במונוהידראט. עשרה מתוך שמונה-עשר המוצרים מצהירים על מינון אמיתי בטווח הזה ובצורה שנחקרה.

ארבעה מוצרים נושאים את המילה קריאטין על האריזה בלי לפרט כמה גרם יש במנה. זו פער שקיפות אמיתי. שלושה מהם נמכרים ברשת המזון שופרסל, והרביעי הוא מוצר טבליות מיובא של MyProtein.

שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט הרגיל, בלי יתרון מוכח שמצדיק את הפער. המונוהידראט הוא הצורה שרוב המחקר נעשה עליה, והוא גם הזול ביותר לגרם.
```

### 2.3 What creatine is proven to do — tiers (mirrors category note / methodology)

Per co-sign §1, corrected numbers. Split-tier where the co-sign requires it. **The uncited
positive-population cognitive sentence is cut (ruling 5); only the cited EFSA null-general line
remains.**

```
מה קריאטין באמת עושה

חוזק וכוח באימוני התנגדות — עדות חזקה. זו אחת ההשפעות המשוחזרות ביותר במחקר תזונת הספורט: קריאטין יחד עם אימוני התנגדות מעלה חוזק מעבר לאימון לבדו (עמדת ISSN 2017, PMID 28615996).

מסת שריר רזה באימוני התנגדות — עדות חזקה. מטא-אנליזה מ-2024 של שנים-עשר מחקרים מצאה עלייה ממוצעת של כ-1.14 ק"ג במסה הרזה מעבר לאימון לבדו (PMID 39074168).

ביצועים בעצימות גבוהה וספרינטים חוזרים — עדות בינונית עד חזקה. תומך במאמצים קצרים וחוזרים בעצימות גבוהה. יתרון מבוסס, פחות מכומת מספרית מהחוזק.

התאוששות — כאן חשוב להפריד. קריאטין עשוי להוריד סמנים ביוכימיים של עומס שריר לאחר אימון קשה (עדות בינונית; Northeast & Clifford 2021, PMID 33631721). באותה סקירה עצמה, הוא לא האיץ את ההתאוששות התפקודית עצמה: חוזק, כאב שרירים או טווח תנועה. ירידה בסמנים ביוכימיים מעידה על פחות עומס נמדד, אך אינה מבטיחה חזרה מהירה יותר לתפקוד.

תפקוד קוגניטיבי — לא מבוסס לאוכלוסייה הכללית. חוות דעת EFSA מ-2024 על טענת הבריאות הקוגניטיבית מצאה שהיא אינה מבוססת לתפקוד קוגניטיבי כללי (DOI 10.2903/j.efsa.2024.9100).

שריפת שומן — אין עדות. אין עדות אמינה שקריאטין שורף שומן ישירות. שינוי בהרכב הגוף משקף עלייה במסה רזה שמגיעה מהאימון עצמו.
```

### 2.4 Effective dose

```
המינון האפקטיבי

הטווח שנחקר לתחזוקה הוא 3 עד 5 גרם ליום, בנטילה עקבית. שלושה גרם ליום נמצאים ברצפת הטווח האפקטיבי.

שלב העמסה של כ-20 גרם ליום (4 מנות של 5 גרם) למשך 5 עד 7 ימים מזרז את הרוויה, ואינו הכרחי. נטילה קבועה של 3 עד 5 גרם ליום מגיעה לאותו מקום, לאט יותר.
```

### 2.5 Forms

```
צורות

מונוהידראט הוא הצורה שכמעט כל העדות נוצרה עליה, והוא ברירת המחדל המבוססת-מחקר. צורות כמו HCl, ביסודי או "אלקליין", אתיל אסתר, ציטראט ומלאט אינן מזיקות ואינן נחותות באיכות, אך אין להן עדות אנושית ליתרון על פני המונוהידראט הזול והנחקר יותר. המשמעות המעשית: משלמים יותר על צורה שלא הוכיחה יתרון.
```

### 2.6 Safety (defensible, non-alarmist, + bipolar caution)

Per co-sign §1 rows 15–18 and §2.4. NO "NIH" attribution. Bipolar caution attached to mood framing.

```
בטיחות

לא נקבע גבול עליון מבוסס לקריאטין. מחקרים במינונים של עד 30 גרם ליום למשך חמש שנים לא דיווחו על נזק תלוי-מינון באנשים בריאים (עמדת ISSN 2017, PMID 28615996).

מיתוס הכליות: קריאטין מעלה סמן מעבדתי בשם קריאטינין, שלעיתים נחשב בטעות לנזק כלייתי. שלוש מטא-אנליזות עצמאיות על תפקוד כלייתי לא מצאו נזק כזה בכליות בריאות (PMID 31375416, 41199218, 42035842).

מי שיש לו מחלת כליות קיימת, כדאי להתייעץ עם רופא לפני שימוש.

מי שיש לו הפרעה דו-קוטבית, כדאי להתייעץ עם רופא לפני שימוש בקריאטין לתמיכה במצב הרוח. קיים סיכון מתועד להשריית אפיזודה מאנית או היפומאנית בהקשר הזה (Roitman ואחרים 2007, PMID 17988366). זהו מחקר ראשוני קטן, אך האזהרה שהוא מעלה אמיתית וראויה לתשומת לב.
```

Guardrail for the gate: the mood/depression evidence itself is Weak (2025 BJN meta-analysis,
SMD −0.34, GRADE very-low, below the 3.0-point minimal important difference; PMID 41189312).
If any mood-benefit framing is added, it must carry both the "not clinically meaningful" hedge
AND the bipolar caution in the same breath. This draft chooses NOT to publish a mood-benefit
claim, only the safety caution.

**Citation verification note (bipolar caution):** PMID 17988366 is verified — Roitman et al.
2007, "Creatine monohydrate in resistant depression: a preliminary study," *Bipolar Disorders*,
an n=10 open-label study in which two bipolar patients developed hypomania/mania. Real, on-topic,
and correctly attributed; independently re-pulled against PubMed at the red-team gate. The
citation trail for this claim is therefore documented, not a candidate.

### 2.7 Dose-honesty consumer explainer (mirrors magnesiumCategoryNote)

Price disclosure line updated per ruling 3 (page-level as-of-date + "may vary"). Category caveat
retained per standard.

```
איך נקבע הדירוג, וביחס למה

הדף הזה אינו נותן ציון מספרי או דירוג אותיות. קריאטין מונוהידראט במינון הוגן עובד באותה מידה בין המותגים, ולכן הדירוג נשען על מה שבאמת משתנה בין המוצרים: שקיפות המינון והשווי לגרם. ארבעה דברים נמדדים: כמה קריאטין המוצר מספק במנה מול הטווח שנחקר (3 עד 5 גרם ליום), באיזו צורה, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.

מינון ישר: המוצר נוקב בקריאטין בשמו, מציין מספר גרם מדויק למנה, והמספר הזה בטווח שנחקר. זו התוית ההוגנת.

מינון מוצהר מתחת לרצפה: המוצר מציין מספר מדויק, אך מתחת ל-3 גרם. זה לא הסתרה, וזה כן מינון בקצה הנמוך של הטווח.

מינון לא מפורט: המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה בשום מקום. ארבעה מוצרים במדף הישראלי נמצאים כאן: שלושה מרשת המזון שופרסל ואחד מוצר טבליות מיובא של MyProtein. אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.

בדיקת צד-שלישי מוצגת בשתי רמות: "אומת מול מאגר" כשבדקנו את רישום המוצר ישירות במאגר של גוף ההסמכה, ו"מוצהר על-ידי היצרן" כשהטענה מופיעה רק בדף המוצר של המותג ולא אומתה מול המאגר. שש מנות ייחוס עולמיות אומתו מול מאגר NSF. אף מוצר מהמדף הישראלי לא אומת מול מאגר בשלב זה.

הערת קטגוריה: מה חשוב לדעת לפני שבוחרים

בארי מבססת את ההשוואה על קריאת תוויות ודפי מוצר. כל המינונים והמחירים המוצגים הם מה שכתוב על האריזה או בדף המוצר בעת הבדיקה. המחירים המוצגים נכונים לתאריך הבדיקה (יולי 2026) ועשויים להשתנות. המידע כאן הוא לצורך הכרה בלבד, ואינו תחליף לייעוץ רפואי.
```

### 2.8 Methodology lines (mirrors magnesiumMethodologyLines)

```
בדקנו 18 תוספי קריאטין מהמדף הישראלי מול שלושה-עשר מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: מינון הקריאטין למנה מול הטווח שנחקר, הצורה הכימית, בדיקת צד-שלישי, ומחיר לגרם אפקטיבי.

הדף אינו מציג ציון מספרי או דירוג אותיות. המינון הוא השיקול הכבד ביותר, אחריו הצורה — מונוהידראט הוא ברירת המחדל שנחקרה — ואז בדיקת צד-שלישי ומחיר לגרם. כך מוצר בצורה יקרה בלי יתרון מוכח אינו מוצג כאילו הצורה שווה את הפער.

שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט, בלי עדות ליתרון שמצדיק את המחיר.

מוצרים שנושאים את המילה קריאטין בלי לפרט מינון מוצגים כפער שקיפות; המוצר נשאר על המדף.
```

---

## 3. Functional-dairy annotation copy — DRAFT

Per `functional_dose_ingredient_ruling_v1.md` §3.2 + co-sign §3.2. This is the annotation lane,
NOT a benchmarked product. Yoplait GO is the only on-shelf dairy creatine, both SKUs undisclosed.
Tnuva GO is collagen, not creatine, and appears only as the correction. **Single-retailer caveat
added inline per ruling 4 — ship now, do not hold for a second-retailer pass.**

**Annotation verdict for Yoplait GO (both SKUs): "כמות לא מפורטת" (Amount not disclosed).**

```
קריאטין במשקאות חלב: מה מצאנו

לפעמים קריאטין מופיע גם מחוץ למדף התוספים, בתוך משקה חלב. במדף הישראלי, המשקה החלבי היחיד שמצהיר על קריאטין הוא יופלה גו (Yoplait GO), בשני מוצרים. בשניהם הכמות אינה מפורטת: אחד מציין אחוז ניסוח של 0.6% בלי גודל מנה שמאפשר לחשב כמה מיליגרם מקבלים ביום, והשני אינו מציין מספר כלל. לכן אי אפשר לומר אם מדובר במינון משמעותי או בכמות זניחה. זו כשלעצמה עובדה שכדאי לדעת לפני שקונים. (בדיקה ברשת שופרסל; לא נבדק ברשתות נוספות.)

הבהרה: תנובה GO אינו מוצר קריאטין. המוצר במדף הוא GO קולגן אייס קפה, שהרכיב הפעיל בו הוא קולגן ולא קריאטין.
```

Data anchors (verified): Yoplait GO — 2 SKUs, both undisclosed (one shows 0.6% formulation
figure, no serving size; one shows no figure). Tnuva GO Collagen Iced Coffee, barcode
7290116935607, collagen 1.48%. Do not compute or assume any Yoplait dose (missing-data discard
rule). No dairy-matrix retention percentage is stated. Finding is Shufersal-scoped until a second
clean retailer confirms it.

---

## 4. Page meta

- **Route (proposed):** `/hashvaot/creatine` — parallel to `/hashvaot/magnesium`.
- **Hebrew `<title>`:** `השוואת תוספי קריאטין | בארי`
- **Hebrew `description`:** `השוואת 18 תוספי קריאטין מהמדף הישראלי מול 13 מותגי ייחוס עולמיים — דירוג בארי לפי שקיפות מינון, צורה, בדיקת צד-שלישי ומחיר לגרם אפקטיבי. כלי הכרה לפני קנייה.`
- **Data file (proposed for Frontend):** `bari-web/src/lib/comparisons/creatine-page-data.ts`, exporting `creatineHero`, `creatineMetadataLine`, `creatinePrologueSentences`, `creatineMethodologyLines`, `creatineCategoryNote`, `creatineProducts`, and `creatineWorldwideBenchmark` — mirroring the magnesium exports so the same page shell renders it.
- **Product VM contract (ruling 1):** Products carry the standard `BariProductVM` fields (name, brand, imageUrl same-origin, insightLine, rowVerdict, confidence, expansion with positiveSignals/limitingFactors/caveats). **`score` and `grade` are `null` for every product** — Israeli and worldwide. `insightLine`/`rowVerdict` carry the dose-honesty + price-value verdict as the headline. Cert fields carry the two-tier label (`certTier: "directory_verified" | "manufacturer_stated" | null`).
- **Owner FYI (not a gate, per ruling summary):** this page structurally differs from magnesium by design — verdict-ranked, no A–E grade. The "golden template" now has two shapes (scored: magnesium; verdict-ranked: creatine). This is a heads-up so it does not read as an inconsistency later.

---

## 5. Ship-gate carry-forward (must re-verify before go-live)

Everything below is a datum this package carries at less-than-fully-verified confidence, or a
consumer string still needing the two-gate sign-off.

1. **All third-party certification claims on the 18 Israeli products (9/18)** — page claims only, all labeled "מוצהר על-ידי היצרן", NOT cross-checked against the certifier's own registry. 0/18 directory-confirmed.
2. **Informed-Sport directory cross-check remains OPEN** — the certifier site (sport.wetestyoutrust.com) returned HTTP 403 on all 5 fetch attempts. No Informed-Sport claim is shown as directory-verified anywhere (Applied Nutrition B9, both MyProtein SKUs B10/B11). HASTA's directory (Switch Nutrition B12) also not cross-checked. Naked Nutrition's NSF claim (B7) has no located directory listing. All carry "מוצהר על-ידי היצרן".
3. **Every price** — point-in-time e-commerce fact; re-verify all Israeli (₪) and worldwide (USD/GBP/AUD/EUR) prices at go-live. Applied Nutrition's price already moved between benchmark passes (£29.95→£18.95–£24.95), which is why the page carries one page-level as-of-date (יולי 2026) + "may vary" (ruling 3), not blind-reused numbers.
4. **Product images** — must be self-hosted same-origin under `bari-web/public/products/` (per product-images-self-hosted rule); no retailer/Cloudinary hotlinks. Image sourcing/migration is a Frontend/Data step; this package does not assign imageUrls.
5. **Ingredient / full label panels** — not captured per-product; if the expansion shows an ingredients list, verify from the Israeli label before go-live.
6. **Second-retailer cross-check on the Yoplait/Tnuva GO dairy finding** — single-retailer (Shufersal) only; Victory/Yochananof/Rami-Levy were blocked. Ruling 4 ships the annotation now with the inline single-retailer caveat; a second clean retailer would upgrade it from a Shufersal-shelf finding to a market finding.
7. **Sleep-deprivation cognitive RCTs** — the positive-population cognitive claim is CUT (ruling 5), so no citation is owed. The EFSA null-general line (DOI 10.2903/j.efsa.2024.9100) is verified and stays.
8. **Worldwide price-per-3g not computed for 4 rows** (Klean Athlete B3, MegaFood B5, Sports Research B6, Switch Nutrition B12) where a clean price figure was not captured this pass — left blank, not estimated. Capture at build if these rows are shown with a price.
9. **All Hebrew consumer copy in §2 and §3** — DRAFT. Requires Content Agent authorship sign-off AND Adversarial QA / Red-Team sign-off before it reaches the owner. This is gate-1 input.

---

## 6. Constraints compliance

- Only ship-ready/verified data used: **13 worldwide benchmarks + 18 Israeli products**. Dropped worldwide candidates (Transparent Labs = HMB blend, Optimum Nutrition = absent from NSF list, Bulk Nutrients = unresolved spec) are NOT in the benchmark table. Israel = 0 ship-ready worldwide-grade products; Super Effect + Alfa lack a verifiable per-serving dose and are excluded from the benchmark (present only in the 18-row Israeli shelf with dose undisclosed).
- **No A–E grade** — `score`/`grade` null on all 31 products (ruling 1). Headline = dose-honesty verdict; ranking = price-per-effective-gram.
- **Two-tier cert labels** — "אומת מול מאגר" only for the 6 NSF-directory-confirmed (Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel); "מוצהר על-ידי היצרן" for all other claims; ESN = honest uncertified. 0 Israeli directory-confirmed. Informed-Sport never shown as directory-verified (site 403). (Ruling 2.)
- **MyProtein Elite ≠ Creapure** correction carried in both tables; Creapure SKU is a separate row (Israeli #10, worldwide B11). (Constraint.)
- **Price disclosure** — one page-level as-of-date (יולי 2026) + "עשויים להשתנות" line in the category-note block, not per-row. (Ruling 3.)
- **Dairy** — Yoplait GO "amount not disclosed" ships now with inline Shufersal-only caveat; Tnuva GO = collagen. No Yoplait dose computed. (Ruling 4.)
- **Cognitive claim cut** — uncited positive-population sentence removed; cited EFSA null-general line kept. (Ruling 5.)
- "Creapure" not stated for Momentous. "NIH / NIH ODS" not used anywhere — safety grounds on ISSN 2017 + kidney meta-analyses + EFSA.
- Corrected identifiers used throughout: ISSN 2017 PMID 28615996 (DOI 10.1186/s12970-017-0173-z), hypertrophy 12 studies / +1.14 kg PMID 39074168, recovery PMID 33631721 (marker/function split), mood PMID 41189312 (SMD −0.34, below MID), EFSA DOI 10.2903/j.efsa.2024.9100, bipolar PMID 17988366 (verified: Roitman et al. 2007, *Bipolar Disorders*, n=10 open-label; two bipolar patients developed hypomania/mania — re-pulled at the red-team gate), kidney metas PMID 31375416 / 41199218 / 42035842.
- No score/philosophy invented; zero BSIP2 exposure. No published score touched.
- Brand spelled בארי throughout. Voice: finding-first, positive declaratives, minimal em-dashes, no "X, not Y" antithesis, no engine jargon.
- **Gate-revision applied (2026-07-03):** RT-1 (Sports Research B6 → manufacturer-stated; directory-verified reconciled to exactly 6 everywhere), RT-2 (grocery-channel claim corrected to 3 Shufersal + 1 imported MyProtein tablet in prologue §2.2 and explainer §2.7), all "X, not Y" antithesis removed from consumer copy (0 remaining, including the two beyond the flagged four found on re-scan at §2.7), three em-dash header separators replaced with colon/comma, MyProtein Elite 3.0/3.4 g cross-reference note added, bipolar PMID verification documented. No new claim, product, price, or citation introduced.
- No product/number invented — every figure traces to a verified source report. Anything unverifiable (dairy percentages, unconfirmed certs, uncomputed worldwide prices) is left out or flagged, not stated.
- Open Food Facts not used, referenced, or considered.
- No subagents spawned.

---

## Return Contract

```json
{
  "task": "TASK-492C",
  "deliverable": "creatine_comparison_content_package_v2",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/content/creatine_comparison_content_package_v2.md",
      "action": "created",
      "sha256": "COMPUTE_AT_READ_TIME: self-referential hash cannot be embedded; verify with `sha256sum` on read"
    }
  ],
  "counts": {
    "israeli_products_included": "18/18 (all verified in creatine_supplement_shelf_scrape_v1.md §3)",
    "worldwide_benchmarks_included": "13/13 (US 7, Canada 1, UK/EU 4, AU 1; source creatine_benchmark_solid_v1.md §1 — REPLACES the v1 5-product table)",
    "total_products_in_package": "31 (18 Israeli + 13 worldwide)",
    "certs_directory_verified": "6/31 (all NSF: Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel — worldwide rows only; 0/18 Israeli)",
    "certs_manufacturer_stated": "manufacturer-stated label applied to every non-directory-confirmed claim (9/18 Israeli + Naked/Applied/2x MyProtein/Switch Nutrition/Sports Research worldwide; Sports Research downgraded from directory-verified per red-team RT-1, specific SKU not directory-confirmed this pass)",
    "certs_none_or_uncertified": "ESN worldwide = honest uncertified comparator; Israeli rows with no claim carry no badge",
    "informed_sport_directory_status": "OPEN (certifier site 403 on all 5 attempts) — no Informed-Sport claim shown as directory-verified anywhere",
    "score_grade": "null on all 31 products (ruling 1 — no A-E grade; headline = dose-honesty verdict, sort = price-per-effective-gram)",
    "dairy_annotation_products": "1 (Yoplait GO, 2 SKUs, both 'amount not disclosed', inline Shufersal-only caveat); Tnuva GO excluded as collagen-not-creatine",
    "cognitive_claims_cut": "1 (uncited positive-population sentence removed from §2.3; cited EFSA null-general line kept)",
    "evidence_sections_drafted": "8 (hero, prologue, proven-effects tiers, dose, forms, safety, dose-honesty explainer + two-tier cert + price-as-of-date, methodology)",
    "corrected_citations_used": "7 (ISSN 2017 28615996, hypertrophy 39074168, recovery 33631721, mood 41189312, EFSA DOI 10.2903/j.efsa.2024.9100, bipolar 17988366, kidney metas 31375416/41199218/42035842)",
    "ship_gate_carryforward_items": "9",
    "scores_invented": "0/0 (zero BSIP2 exposure; ruling 1 sets score/grade null)",
    "off_usages": "0/0 (banned source, never invoked)",
    "subagents_spawned": "0/0"
  },
  "commands_run": [],
  "not_done": [
    "No app page built and nothing committed/deployed — DRAFT content package only",
    "Two-gate content sign-off (Content Agent + Adversarial QA) not run — required before this reaches the owner",
    "Informed-Sport / HASTA directory cross-checks remain OPEN (certifier sites 403/not-attempted) — all such claims carry 'מוצהר על-ידי היצרן', none shown as directory-verified (ship-gate item 2)",
    "9/18 Israeli cert claims not registry-checked — all 'מוצהר על-ידי היצרן', 0 directory-confirmed (ship-gate item 1)",
    "All prices carried at scrape-time value — require live re-check at go-live; page uses one as-of-date + 'may vary' line (ship-gate item 3)",
    "Worldwide price-per-3g not computed for 4 rows (Klean Athlete, MegaFood, Sports Research, Switch Nutrition) — blank, not estimated (ship-gate item 8)",
    "Second-retailer cross-check on the Yoplait/Tnuva dairy finding not performed — shipped with inline single-retailer caveat per ruling 4 (ship-gate item 6)",
    "No imageUrls assigned — same-origin image sourcing/migration is a Frontend/Data step (ship-gate item 4)"
  ],
  "self_check": "Acceptance test: produce the FINAL build-ready v2 content+data package by folding the upgraded 13-product benchmark and all 5 Product rulings into the stage-1 base. Result: PASS. §1.3 now carries the 13 verified worldwide products (US 7, CA 1, UK/EU 4, AU 1) with form/dose/price/servings and the two-tier cert label — 'אומת מול מאגר' on exactly the 6 NSF-directory-confirmed rows (Thorne, Momentous, Klean Athlete, BPN, MegaFood, BioSteel), 'מוצהר על-ידי היצרן' on all others, ESN as the honest uncertified comparator; the MyProtein Elite-vs-Creapure correction is carried (Elite = generic, Creapure = separate B11 row) in both tables. Ruling 1 applied: score/grade null on all 31 products, headline = dose-honesty verdict, ranking = price-per-effective-gram, both defined in §1.0. Ruling 2 (two-tier certs), Ruling 3 (page-level as-of-date + may-vary in §2.7), Ruling 4 (Yoplait ships now with inline Shufersal-only caveat; Tnuva = collagen), Ruling 5 (uncited cognitive claim cut from §2.3, cited EFSA line kept) all applied. Israel = 0 ship-ready worldwide-grade products (Super Effect/Alfa lack a verifiable per-serving dose, excluded from the benchmark, present only in the 18-row Israeli shelf). All prior constraints held: no NIH attribution, corrected PMIDs/DOI throughout, no Creapure for Momentous, dairy stability qualitative only, brand בארי, positive-declarative voice, no OFF, no subagents. Final counts: 18 Israeli + 13 worldwide = 31 products. 9 ship-gate items carried. Every consumer string marked DRAFT pending the two-gate sign-off."
}
```
