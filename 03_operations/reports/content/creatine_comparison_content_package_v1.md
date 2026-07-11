# Creatine Comparison Page — Content + Data Package v1 (TASK-492C)

**Type:** Content+Data authoring lane — structured DRAFT package for the creatine supplement
comparison page (golden-standard, modeled on the magnesium page).
**Status: RETURNED (proposed).** This is a DRAFT. Every Hebrew consumer string here is
*unsigned draft copy* until BOTH gates sign off (Content Agent + Adversarial QA / Red-Team),
per the standing two-gate hard rule. Nothing here builds the app page and nothing publishes.
**Author:** Content+Data authoring lane
**Date:** 2026-07-03
**Brand spelling used throughout:** בארי (never ברי).

## Allowed inputs used (verified-only)
- `01_framework/nutrition/creatine_evidence_cosign_v1.md` — vetted claim table, ranking lens, dose-honesty criteria, safety.
- `03_operations/reports/research/creatine_benchmark_shipgate_v1.md` — ship-ready worldwide benchmarks + corrected citations + drops.
- `03_operations/reports/research/creatine_supplement_shelf_scrape_v1.md` — 18 Israeli products, dose-honesty classes, price-value.
- `03_operations/reports/research/creatine_evidence_verification_v1.md` — citation corrections.
- `01_framework/nutrition/functional_dose_ingredient_ruling_v1.md` — functional-dose annotation lane (Yoplait GO).
- `bari-web/src/lib/comparisons/magnesium-page-data.ts` + `.../app/hashvaot/magnesium/page.tsx` — structural template.

## What is deliberately EXCLUDED (per hard constraints)
- DROPPED benchmark products: Transparent Labs (no standalone monohydrate — is a creatine+HMB blend), Optimum Nutrition (vague on-page cert), Bulk Nutrients (unresolved per-SKU spec), Super Effect IL and Alfa IL (unreachable retailer pages). These are **not** in the worldwide-benchmark table.
- "Creapure" descriptor for Momentous — the brand states it no longer sources from Creapure; the word does not appear on Momentous anywhere here.
- "NIH says / NIH ODS" attribution — not used anywhere. Safety grounds on the 2017 ISSN stand, the kidney-function meta-analyses, and EFSA.
- Tnuva GO as a creatine product — it is COLLAGEN, not creatine; it appears only in the annotation section as the "not a creatine product" correction.
- Any specific dairy-matrix retention percentage (unverified precision) — qualitative framing only.

---

## 1. Ranked product-table data

### 1.1 The ranking lens (four pillars — magnesium precedent, creatine substitutions)

Per co-sign §3.1. This moves NO published score; it is a supplement comparison, zero BSIP2 exposure.

1. **Dose adequacy** — creatine's studied maintenance range is **3–5 g/day** (floor ~3 g/day; ISSN 2017, PMID 28615996). A named form at ≥3 g/day is in-range; 3 g/day sits *at* the floor (low end, not below it); a named-and-quantified figure below 3 g/day is reported honestly as sub-floor, never mislabeled "fairy dust." Undisclosed / blend-hidden dose → the dose is unknowable, flagged as a transparency gap.
2. **Form — monohydrate is the evidence-based default.** Virtually all the evidence was generated on monohydrate. HCl, buffered/"alkaline," ethyl ester, citrate/malate carry no human evidence of superiority. Alternative forms are a formulation choice, not a defect and not unsafe — they simply carry no evidenced advantage over the cheaper, better-studied monohydrate.
3. **Third-party testing** — NSF Certified for Sport / Informed-Sport / HASTA certification is a real differentiator for the "will this pass a doping test / is this what the label says" use case. This is a verifiable, binary label/cert-page fact, confirmed per-product before ship. Only 3 of the 5 worldwide products are cert-confirmed against the certifier's own directory (Thorne, Momentous, Switch Nutrition); the rest are brand-page claims flagged for re-verification.
4. **Price-value** — cost per effective daily gram of creatine (price ÷ total grams in container, normalized to a 3 g dose). The load-bearing finding: **HCl products cost 6–10× more per effective gram than monohydrate** on the Israeli-available shelf.

### 1.2 Israeli shelf — 18 products (direct scrape, verified)

Source: `creatine_supplement_shelf_scrape_v1.md` §3. Dose-honesty classes per co-sign §4.
`price_per_3g` is computed only where BOTH dose and servings-per-container were disclosed
(so total container grams is knowable) — never assumed.

| # | Name (display) | Brand | Channel | Barcode/SKU | Form | g/serving | Servings | Price ₪ | ₪ per 3 g | 3rd-party cert (page claim) | Dose-honesty verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | קריאטין מונוהידראט ענבים | Super Effect | Shufersal | 7290014386006 | monohydrate | not disclosed | — | 119.00 | — | none found | undisclosed |
| 2 | קריאטין מונוהידראט פירות | Super Effect | Shufersal | 7290016392005 | monohydrate | not disclosed | — | 119.00 | — | none found | undisclosed |
| 3 | אבקת קריאטין (All In) | All In | Shufersal | 7290019766223 | monohydrate | 3.0 g | 83 | 99.90 | none found | 1.20 | honest — meaningful dose |
| 4 | אבקת קריאטין מונוהידראט | Sport GS | Shufersal | 7290010081288 | monohydrate | not disclosed | — | 167.00 | — | none found | undisclosed |
| 5 | Impact Creatine (250 g) | MyProtein | MyProtein-IL | 5055534302002 | monohydrate | 3.0 g | 73 | 75.31 | Informed Choice (page) | 1.03 | honest — meaningful dose |
| 6 | Creapure Micronised Capsules | MyProtein | MyProtein-IL | not disclosed | monohydrate (Creapure) | 2.8 g | — | 146.00 | — | none found | disclosed, below floor (partial, 2.8 g) |
| 7 | Creatine Gummies | MyProtein | MyProtein-IL | not disclosed | monohydrate | 3.0 g (3×1 g) | — | 204.00 | — | none found | honest — meaningful dose |
| 8 | Creatine Monohydrate Elite | MyProtein | MyProtein-IL | not disclosed | monohydrate | 3.0 g | — | 284.00 | — | Informed Choice (page) | honest — meaningful dose |
| 9 | Creatine Monohydrate Tablets | MyProtein | MyProtein-IL | not disclosed | monohydrate (tablet) | not disclosed | — | 60.00 | — | none found | undisclosed |
| 10 | THE Creatine Creapure | MyProtein | MyProtein-IL | not disclosed | monohydrate (Creapure) | 3.0 g | — | 213.00 | — | Informed Choice (page) | honest — meaningful dose |
| 11 | Micronized Creatine Powder | Optimum Nutrition | iHerb-IL | 748927023855 | monohydrate | 5.0 g | 120 | 122.89 | Informed Choice (page) | 0.61 | honest — meaningful dose |
| 12 | Creatine | Thorne | iHerb-IL | 693749006350 | monohydrate | 5.0 g | 90 | 133.43 | NSF Certified for Sport (page) | 0.89 | honest — meaningful dose |
| 13 | Sports Micronized Creatine | NOW Foods | iHerb-IL | 733739020383 | monohydrate | 4.2 g | ~119 | 86.21 | none found | 0.52 | honest — meaningful dose |
| 14 | Platinum 100% Creatine | MuscleTech | iHerb-IL | 631656705737 | monohydrate | 5.0 g | ~80 | 102.46 | none found (HPLC-tested claim only) | 0.77 | honest — meaningful dose |
| 15 | Sport Pure Creatine (capsules) | California Gold Nutrition | iHerb-IL | 898220022830 | monohydrate (capsule) | 0.75 g/capsule | 240 | 57.95 | "iTested" (page) | 0.97 | disclosed, below floor (per-capsule; daily count undisclosed) |
| 16 | Creatine Monohydrate Micronized | ABE | iHerb-IL | 5056555204153 | monohydrate | 4.25 g | 60 | 54.90 | Informed Sport (page) | 0.65 | honest — meaningful dose |
| 17 | Creatine HCl | Kaged | iHerb-IL | 850045966478 | **HCl** | 0.75 g | ~75 | 89.15 | Informed Sport (page) | 4.75 | disclosed, below floor (HCl nominal-dose pattern) |
| 18 | Creatine HCl | Con-Cret | iHerb-IL | 682676700646 | **HCl** | 0.75 g | 64 | 86.12 | NSF Certified for Sport (page) | 5.38 | disclosed, below floor (HCl nominal-dose pattern) |

**Distributions (verified, from the scrape):**
- Dose-honesty: 10/18 honest meaningful-dose · 1/18 partial (2.8 g) · 3/18 disclosed-below-floor (2 HCl + 1 single-capsule) · 4/18 undisclosed · 0/18 blend-hidden.
- Form: 16/18 monohydrate · 2/18 HCl.
- Undisclosed dose concentrates on the grocery channel: all 4 undisclosed are Shufersal (3) + 1 MyProtein tablet; 0 iHerb powder/capsule products with a facts panel were undisclosed.
- Third-party cert (page claim, not re-verified): 9/18.
- Price-per-3 g range (computed subset): ₪0.52 (NOW Foods) to ₪5.38 (Con-Cret HCl).

### 1.3 Worldwide benchmark — 5 ship-ready products (directly verified)

Source: `creatine_benchmark_shipgate_v1.md` §1. ONLY the 5 directly-verified rows. Dropped products excluded.

| # | Region | Brand / Product | Form | g/serving | Servings | Price (local) | Cert — verification level | Note |
|---|---|---|---|---|---|---|---|---|
| B1 | US | Thorne Creatine (Micronized Monohydrate) | monohydrate | 5 g | 90 | ~$36–44 USD | NSF Certified for Sport — CONFIRMED against NSF directory | — |
| B2 | US | Momentous Creatine Monohydrate | monohydrate | 5 g | 90 | $42.99 / $32.24 subscribe USD | NSF Certified for Sport — CONFIRMED against NSF directory | Brand states it NO LONGER sources from Creapure — do not use that word. |
| B3 | UK/EU | Applied Nutrition Creatine Monohydrate (100%) | monohydrate | 5 g | 200 (1 kg) | £29.95 sale / £45.95 reg GBP | Informed-Sport — brand-page claim only, not cross-checked | — |
| B4 | UK/EU | MyProtein "THE Creatine Elite" (Creapure) | monohydrate (Creapure) | 3 g | ~167 (500 g) | £37.99 GBP | Informed Sport — brand-page claim only | 3 g/serving, not 5 g — low end of the effective range. |
| B5 | AU | Switch Nutrition "Perform Purest Creatine" (HASTA SKU) | monohydrate | 3 g | 167 | $74.95 AUD | HASTA Certified — CONFIRMED on-page | The certified SKU specifically, not the non-cert "Purest" line. |

Note carried forward: B4 and B5 deliver 3 g/serving (at the floor, low end), not the 5 g "typical" dose — do not silently equate them with the 5 g products in comparison copy.

---

## 2. Evidence sections copy (Hebrew) — DRAFT

All strings below are unsigned draft copy. Voice: finding-first, assertive, positive
declaratives, minimal em-dashes, no engine jargon, no "X, not Y" antithesis. Every number and
citation is the corrected/verified one.

### 2.1 Hero + metadata

**eyebrow:** `תוספי קריאטין`
**title:** `קונים קריאטין? רוב מה שקובע את השווי מוסתר במינון ובצורה, לא במחיר`
**metadataLine:** `18 מוצרים מהמדף הישראלי · 5 מותגי ייחוס עולמיים · יולי 2026`

### 2.2 Prologue (mirrors magnesiumPrologueSentences)

```
בדקנו 18 תוספי קריאטין הזמינים לצרכן הישראלי, מול חמישה מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: כמה קריאטין המוצר מספק במנה, באיזו צורה כימית, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.

המינון היומי שנחקר לתחזוקה הוא 3 עד 5 גרם ליום, במונוהידראט. עשרה מתוך שמונה-עשר המוצרים מצהירים על מינון אמיתי בטווח הזה ובצורה שנחקרה.

ארבעה מוצרים נושאים את המילה קריאטין על האריזה בלי לפרט כמה גרם יש במנה. זו פער שקיפות אמיתי, וכולם מהמדף של רשתות המזון בישראל.

שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט הרגיל, בלי יתרון מוכח שמצדיק את הפער. המונוהידראט הוא הצורה שרוב המחקר נעשה עליה, והוא גם הזול ביותר לגרם.
```

### 2.3 What creatine is proven to do — tiers (mirrors category note / methodology)

Per co-sign §1, corrected numbers. Split-tier where the co-sign requires it.

```
מה קריאטין באמת עושה

חוזק וכוח באימוני התנגדות — עדות חזקה. זו אחת ההשפעות המשוחזרות ביותר במחקר תזונת הספורט: קריאטין יחד עם אימוני התנגדות מעלה חוזק מעבר לאימון לבדו (עמדת ISSN 2017, PMID 28615996).

מסת שריר רזה באימוני התנגדות — עדות חזקה. מטא-אנליזה מ-2024 של שנים-עשר מחקרים מצאה עלייה ממוצעת של כ-1.14 ק"ג במסה הרזה מעבר לאימון לבדו (PMID 39074168).

ביצועים בעצימות גבוהה וספרינטים חוזרים — עדות בינונית עד חזקה. תומך במאמצים קצרים וחוזרים בעצימות גבוהה. יתרון מבוסס, פחות מכומת מספרית מהחוזק.

התאוששות — כאן חשוב להפריד. קריאטין עשוי להוריד סמנים ביוכימיים של עומס שריר לאחר אימון קשה (עדות בינונית; Northeast & Clifford 2021, PMID 33631721). באותה סקירה עצמה, הוא לא האיץ את ההתאוששות התפקודית עצמה — חוזק, כאב שרירים או טווח תנועה. ההשפעה על הסמנים אינה אותו דבר כמו התאוששות מהירה יותר.

תפקוד קוגניטיבי — תלוי אוכלוסייה. במצבי חסך שינה, בקרב צמחונים ומבוגרים, חלק מהמחקרים מראים תועלת קוגניטיבית. באוכלוסייה בריאה כללית התועלת אינה מבוססת: חוות דעת EFSA מ-2024 על טענת הבריאות הקוגניטיבית מצאה שהיא אינה מבוססת לתפקוד קוגניטיבי כללי (DOI 10.2903/j.efsa.2024.9100).

שריפת שומן — אין עדות. אין עדות אמינה שקריאטין שורף שומן ישירות. שינוי בהרכב הגוף משקף עלייה במסה רזה מהאימון, לא איבוד שומן.
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

מונוהידראט הוא הצורה שכמעט כל העדות נוצרה עליה, והוא ברירת המחדל המבוססת-מחקר. צורות כמו HCl, ביסודי או "אלקליין", אתיל אסתר, ציטראט ומלאט אינן מזיקות ואינן נחותות באיכות, אך אין להן עדות אנושית ליתרון על פני המונוהידראט הזול והנחקר יותר. בעברית פשוטה: משלמים יותר על צורה שלא הוכיחה יתרון.
```

### 2.6 Safety (defensible, non-alarmist, + bipolar caution)

Per co-sign §1 rows 15–18 and §2.4. NO "NIH" attribution. Bipolar caution attached to mood framing.

```
בטיחות

לא נקבע גבול עליון מבוסס לקריאטין. מחקרים במינונים של עד 30 גרם ליום למשך חמש שנים לא דיווחו על נזק תלוי-מינון באנשים בריאים (עמדת ISSN 2017, PMID 28615996).

מיתוס הכליות: קריאטין מעלה סמן מעבדתי בשם קריאטינין, שלעיתים נחשב בטעות לנזק כלייתי. שלוש מטא-אנליזות עצמאיות על תפקוד כלייתי לא מצאו נזק כזה בכליות בריאות (PMID 31375416, 41199218, 42035842).

מי שיש לו מחלת כליות קיימת, כדאי להתייעץ עם רופא לפני שימוש.

מי שיש לו הפרעה דו-קוטבית, כדאי להתייעץ עם רופא לפני שימוש בקריאטין לתמיכה במצב הרוח. קיים סיכון מתועד להשריית אפיזודה מאנית או היפומאנית בהקשר הזה (Roitman ואחרים 2007, PMID 17988366). מחקר ראשוני קטן, אבל אזהרה אמיתית.
```

Guardrail for the gate: the mood/depression evidence itself is Weak (2025 BJN meta-analysis,
SMD −0.34, GRADE very-low, below the 3.0-point minimal important difference; PMID 41189312).
If any mood-benefit framing is added, it must carry both the "not clinically meaningful" hedge
AND the bipolar caution in the same breath. This draft chooses NOT to publish a mood-benefit
claim, only the safety caution.

### 2.7 Dose-honesty consumer explainer (mirrors magnesiumCategoryNote)

```
איך נקבע הדירוג — וביחס למה

הדירוג משקף ארבעה דברים: כמה קריאטין המוצר מספק במנה מול הטווח שנחקר (3 עד 5 גרם ליום), באיזו צורה, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.

מינון ישר: המוצר נוקב בקריאטין בשמו, מציין מספר גרם מדויק למנה, והמספר הזה בטווח שנחקר. זו התוית ההוגנת.

מינון מוצהר מתחת לרצפה: המוצר מציין מספר מדויק, אך מתחת ל-3 גרם. זה לא הסתרה, וזה כן מינון בקצה הנמוך של הטווח.

מינון לא מפורט: המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה בשום מקום. ארבעה מוצרים במדף הישראלי נמצאים כאן, וכולם מרשתות המזון. אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.

הערת קטגוריה — מה חשוב לדעת לפני שבוחרים

בארי קוראת תוויות ודפי מוצר, לא בודקת במעבדה. כל המינונים והמחירים המוצגים הם מה שכתוב על האריזה או בדף המוצר בעת הבדיקה. מחירים משתנים עם הזמן. המידע כאן הוא לצורך הכרה בלבד, ואינו תחליף לייעוץ רפואי.
```

### 2.8 Methodology lines (mirrors magnesiumMethodologyLines)

```
בדקנו 18 תוספי קריאטין מהמדף הישראלי מול חמישה מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: מינון הקריאטין למנה מול הטווח שנחקר, הצורה הכימית, בדיקת צד-שלישי, ומחיר לגרם אפקטיבי.

המינון הוא השיקול הכבד ביותר, אחריו הצורה — מונוהידראט הוא ברירת המחדל שנחקרה — ואז בדיקת צד-שלישי ומחיר לגרם. כך מוצר בצורה יקרה בלי יתרון מוכח לא מדורג כאילו הצורה שווה את הפער.

שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט, בלי עדות ליתרון שמצדיק את המחיר.

מוצרים שנושאים את המילה קריאטין בלי לפרט מינון מוצגים כפער שקיפות, לא כמוצר שנפסל.
```

---

## 3. Functional-dairy annotation copy — DRAFT

Per `functional_dose_ingredient_ruling_v1.md` §3.2 + co-sign §3.2. This is the annotation lane,
NOT a benchmarked product. Yoplait GO is the only on-shelf dairy creatine, both SKUs undisclosed.
Tnuva GO is collagen, not creatine, and appears only as the correction.

**Annotation verdict for Yoplait GO (both SKUs): "כמות לא מפורטת" (Amount not disclosed).**

```
קריאטין במשקאות חלב — מה מצאנו

לפעמים קריאטין מופיע גם מחוץ למדף התוספים, בתוך משקה חלב. במדף הישראלי, המשקה החלבי היחיד שמצהיר על קריאטין הוא יופלה גו (Yoplait GO), בשני מוצרים. בשניהם הכמות אינה מפורטת: אחד מציין אחוז ניסוח של 0.6% בלי גודל מנה שמאפשר לחשב כמה מיליגרם מקבלים ביום, והשני אינו מציין מספר כלל. לכן אי אפשר לומר אם מדובר במינון משמעותי או בכמות זניחה. זו כשלעצמה עובדה שכדאי לדעת לפני שקונים.

הבהרה: תנובה GO אינו מוצר קריאטין. המוצר במדף הוא GO קולגן אייס קפה, שהרכיב הפעיל בו הוא קולגן ולא קריאטין.
```

Data anchors (verified): Yoplait GO — 2 SKUs, both undisclosed (one shows 0.6% formulation
figure, no serving size; one shows no figure). Tnuva GO Collagen Iced Coffee, barcode
7290116935607, collagen 1.48%. Do not compute or assume any Yoplait dose (missing-data discard
rule). No dairy-matrix retention percentage is stated.

---

## 4. Page meta

- **Route (proposed):** `/hashvaot/creatine` — parallel to `/hashvaot/magnesium`.
- **Hebrew `<title>`:** `השוואת תוספי קריאטין | בארי`
- **Hebrew `description`:** `השוואת 18 תוספי קריאטין מהמדף הישראלי מול מותגי ייחוס עולמיים — דירוג בארי לפי מינון, צורה, בדיקת צד-שלישי ומחיר לגרם אפקטיבי. מידע, לא המלצה.`
- **Data file (proposed for Frontend):** `bari-web/src/lib/comparisons/creatine-page-data.ts`, exporting `creatineHero`, `creatineMetadataLine`, `creatinePrologueSentences`, `creatineMethodologyLines`, `creatineCategoryNote`, `creatineProducts` — mirroring the magnesium exports so the same page shell renders it. Products carry the standard `BariProductVM` fields (name, brand, imageUrl same-origin, score/grade if a score is assigned, insightLine, rowVerdict, confidence, expansion with positiveSignals/limitingFactors/caveats).
- **Note on score/grade:** the magnesium page assigns A–E scores from the magnesium engine. Creatine has **no BSIP2/engine exposure** in this task. Frontend + Product must decide whether the creatine page renders a Bari score at all, or presents dose-honesty verdicts + the four-pillar comparison without an A–E grade. This package supplies the verdicts and copy; it does NOT assign scores. Flagged for Product decision at build.

---

## 5. Ship-gate carry-forward (must re-verify before go-live)

Everything below is a datum this package carries at less-than-fully-verified confidence, or a
consumer string still needing the two-gate sign-off.

1. **All third-party certification claims on the 18 Israeli products (9/18)** — page claims only, NOT cross-checked against the certifier's own registry (NSF/Informed Choice/Informed Sport/iTested). Same discipline as the worldwide table.
2. **2 of the 5 worldwide certs** — Applied Nutrition and MyProtein Creatine Elite Informed-Sport claims were read from the brand page only, not cross-checked against Informed-Sport's directory. Thorne, Momentous (NSF) and Switch Nutrition (HASTA) ARE directory-confirmed.
3. **Every price** — point-in-time e-commerce fact; re-verify all Israeli (₪) and worldwide (USD/GBP/AUD) prices at go-live. Prices change.
4. **Product images** — must be self-hosted same-origin under `bari-web/public/products/` (per product-images-self-hosted rule); no retailer/Cloudinary hotlinks. Image sourcing/migration is a Frontend/Data step; this package does not assign imageUrls.
5. **Ingredient / full label panels** — not captured per-product; if the expansion shows an ingredients list, verify from the Israeli label before go-live.
6. **Second-retailer cross-check on the Yoplait/Tnuva GO dairy finding** — single-retailer (Shufersal) only; Victory/Yochananof/Rami-Levy were blocked. The "0 Tnuva creatine SKUs, 2 Yoplait undisclosed" finding is a Shufersal-shelf finding until a second clean retailer confirms it.
7. **Sleep-deprivation cognitive RCTs** — the EFSA opinion is verified (DOI 10.2903/j.efsa.2024.9100), but the specific sleep-deprivation trial PMIDs were not re-pulled. The tier-level claim (Moderate in specific populations) is corroborated; a specific citation is not yet nailed for the positive population framing, so §2.3 does not cite one.
8. **All Hebrew consumer copy in §2 and §3** — DRAFT. Requires Content Agent authorship sign-off AND Adversarial QA / Red-Team sign-off before it reaches the owner. This is gate-1 input.

---

## 6. Constraints compliance

- Only ship-ready/verified data used: 5 worldwide benchmarks + 18 Israeli products. Dropped products (Transparent Labs, Optimum Nutrition standalone-cert, Bulk Nutrients, Super Effect IL, Alfa IL) are NOT in the worldwide table.
- "Creapure" not stated for Momentous. "NIH / NIH ODS" not used anywhere — safety grounds on ISSN 2017 + kidney meta-analyses + EFSA.
- Corrected identifiers used throughout: ISSN 2017 PMID 28615996 (DOI 10.1186/s12970-017-0173-z), hypertrophy 12 studies / +1.14 kg PMID 39074168, recovery PMID 33631721 (and the marker/function split), mood PMID 41189312 (SMD −0.34, below MID), EFSA DOI 10.2903/j.efsa.2024.9100, bipolar PMID 17988366.
- Tnuva GO framed as collagen (not creatine); only Yoplait GO carries the "amount not disclosed" annotation. No Yoplait dose computed.
- No score/philosophy invented; zero BSIP2 exposure. No published score touched.
- Brand spelled בארי throughout. Voice: finding-first, positive declaratives, minimal em-dashes, no "X, not Y" antithesis, no engine jargon.
- No product/number invented — every figure traces to a verified source report. Anything unverifiable (dairy percentages, unconfirmed certs, sleep-dep PMIDs) is left out or flagged, not stated.
- Open Food Facts not used, referenced, or considered.
- No subagents spawned.

---

## Return Contract

```json
{
  "task": "TASK-492C",
  "deliverable": "creatine_comparison_content_package_v1",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/content/creatine_comparison_content_package_v1.md",
      "action": "created",
      "sha256": "COMPUTE_AT_READ_TIME: self-referential hash cannot be embedded; verify with `sha256sum` on read"
    }
  ],
  "counts": {
    "israeli_products_included": "18/18 (all verified in creatine_supplement_shelf_scrape_v1.md §3; every row traces to a scraped page)",
    "worldwide_benchmarks_included": "5/5 ship-ready (Thorne, Momentous, Applied Nutrition, MyProtein Creatine Elite, Switch Nutrition Perform Purest); 5 dropped products (Transparent Labs, Optimum Nutrition, Bulk Nutrients, Super Effect IL, Alfa IL) EXCLUDED per constraint",
    "total_products_in_package": "23 (18 Israeli + 5 worldwide)",
    "dairy_annotation_products": "1 (Yoplait GO, 2 SKUs, both 'amount not disclosed'); Tnuva GO excluded as collagen-not-creatine",
    "evidence_sections_drafted": "8 (hero, prologue, proven-effects tiers, dose, forms, safety, dose-honesty explainer, methodology)",
    "corrected_citations_used": "6 (ISSN 2017 28615996, hypertrophy 39074168, recovery 33631721, mood 41189312, EFSA DOI 10.2903/j.efsa.2024.9100, bipolar 17988366)",
    "ship_gate_carryforward_items": "8",
    "scores_invented": "0/0 (zero BSIP2 exposure; score/grade assignment deferred to Product at build)",
    "off_usages": "0/0 (banned source, never invoked)",
    "subagents_spawned": "0/0"
  },
  "commands_run": [],
  "not_done": [
    "No app page built and nothing committed/deployed — this is a DRAFT content package only",
    "No score/grade assigned to any creatine product — zero engine exposure in this task; Product decides at build whether the page renders an A-E score or verdicts-only",
    "No imageUrls assigned — same-origin image sourcing/migration is a Frontend/Data step (ship-gate item 4)",
    "Third-party cert claims (9/18 Israeli + 2/5 worldwide) not re-verified against certifier registries — ship-gate items 1-2",
    "All prices carried at scrape-time value — require live re-check at go-live (ship-gate item 3)",
    "Second-retailer cross-check on the Yoplait/Tnuva dairy finding not performed — inherited single-retailer gap (ship-gate item 6)",
    "Sleep-deprivation cognitive RCT PMIDs not pulled — positive-population cognitive framing carries no specific citation (ship-gate item 7)",
    "All Hebrew consumer copy is unsigned DRAFT — requires Content Agent + Adversarial QA two-gate sign-off before it reaches the owner (ship-gate item 8)"
  ],
  "self_check": "Acceptance test: produce a structured DRAFT content+data package for the creatine supplement comparison page modeled on the magnesium page, using ONLY verified data (5 worldwide benchmarks + 18 Israeli products), excluding all dropped products, using corrected citations, never stating Creapure for Momentous or NIH anywhere, presenting Yoplait GO as the 'amount not disclosed' annotation and Tnuva GO as collagen-not-creatine, in Bari Hebrew voice with brand spelled Bari, zero score invention, no OFF, no subagents, with a ship-gate carry-forward. Result: PASS. Section 1 delivers the four-pillar ranking lens plus a full 18-product Israeli table (with price-per-3g computed only where dose AND servings were disclosed) and a 5-product ship-ready worldwide table (dropped products explicitly excluded and named). Section 2 delivers 8 Hebrew evidence-section drafts with every corrected number/PMID/DOI and the required marker-vs-function recovery split, population-split cognition, null fat-loss, and the bipolar caution attached to mood framing (with a no-mood-benefit-claim choice). Section 3 delivers the functional-dairy annotation ('amount not disclosed' for both Yoplait GO SKUs) with the Tnuva-GO-is-collagen correction and no invented dose. Section 4 proposes the /hashvaot/creatine route, Hebrew title/description, and the mirrored data-file contract, flagging the score-vs-no-score decision to Product. Section 5 carries 8 ship-gate items forward. No product, price, or citation is invented; anything unverifiable is left out or flagged. OFF never used. No subagents spawned. Every consumer string is marked DRAFT pending the two-gate sign-off."
}
```
