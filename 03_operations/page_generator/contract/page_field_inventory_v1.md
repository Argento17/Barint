# Page Field Inventory v1 — Granola / Snacks / Milk

Source files:
| Category | File |
|----------|------|
| granola | `bari-web/src/data/comparisons/granola_frontend_v1.json` (42 products) |
| snacks  | `bari-web/src/data/comparisons/snacks_frontend_v2.json` (18 products) |
| milk    | `bari-web/src/data/milk-comparison.json` (18 products, legacy format) |

---

## Table 1: Product-object fields

| field path | type | in granola? | in snacks? | in milk? | example value (≤60 chars) | null allowed? |
|---|---|---|---|---|---|---|
| `id` | string | yes (42/42) | yes (18/18) | — | `bsip1_cereal_1164266` | no |
| `name` | string | yes (42/42) | yes (18/18) | — | `גרנולה ממותקת בסילאן` | no |
| `imageUrl` | string-null | yes (42/42) | yes (18/18) | — | `https://res.cloudinary.com/shufersal/image/upload/...` | yes (2 null) |
| `score` | number-null | yes (42/42) | yes (18/18) | — | `76` | no (all numeric) |
| `grade` | string-null | yes (42/42) | yes (18/18) | — | `B` | no (all present) |
| `insightLine` | string | yes (42/42) | yes (18/18) | — | `16 ג' חלבון, 12 ג' סיבים — ו-372 קק"ל, מהנמוכו` | no |
| `confidence` | string | yes (42/42) | yes (18/18) | — | `partial` | no |
| `retailer` | string | yes (42/42) | yes (18/18) | — | `shufersal` | no |
| `barcode` | string | yes (42/42) | yes (18/18) | — | `1164266` | no |
| `source_traceability_status` | string | yes (42/42) | yes (18/18) | — | `resolved` | no |
| `d4_additives` | array | yes (42/42) | yes (18/18) | — | `[]` | no (empty array) |
| `confidence_label_he` | string | yes (42/42) | yes (18/18) | — | `נתונים בבדיקה` | no |
| `confidence_tooltip_he` | string | yes (42/42) | yes (18/18) | — | `חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כ` | no |
| `confidence_sub_reason` | string-null | yes (42/42) | yes (18/18) | — | `low_extraction` | yes (all present) |
| `rowVerdict` | string | yes (42/42) | no | — | `הגרנולה החזקה במדף — כ-16 ג' חלבון, 12 ג' ס` | no |
| `_subpool` | string | yes (42/42) | no | — | `granola` | no |
| `_isChildrens` | boolean | yes (42/42) | no | — | `false` | no |
| `_wholeGrainClaim` | boolean | yes (42/42) | no | — | `false` | no |
| `confidence_level` | string | yes (33/42) | no | — | `sufficient` | yes (absent 9) |
| `_internal_cluster` | string | no | yes (18/18) | — | `date-simple` | no |
| `barcode` (milk) | string | — | — | yes (18/18) | `7290000051352` | no |
| `shortName` | string | — | — | yes (18/18) | `חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן` | no |
| `displayTitle` | string | — | — | yes (18/18) | `חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן` | no |
| `brandLine` | string | — | — | yes (18/18) | `תנובה` | no |
| `name_he` | string | — | — | yes (18/18) | `חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן` | no |
| `brand` | string | — | — | yes (18/18) | `חלב תנובה` | no |
| `productType` | string | — | — | yes (18/18) | `dairy` | no |
| `productTypeLabel` | string | — | — | yes (18/18) | `חלב פרה` | no |
| `image_url` | string | — | — | yes (18/18) | `https://api.yochananof.co.il/media/catalog/produ` | no |
| `score` (milk) | number | — | — | yes (18/18) | `85` | no |
| `grade` (milk) | string | — | — | yes (18/18) | `A` | no |
| `grade_label` | string | — | — | yes (18/18) | `מצוין` | no |
| `proteinPer100ml` | number-null | — | — | yes (18/18) | `3.3` | yes (null for some) |
| `sugarPer100ml` | number-null | — | — | yes (18/18) | `null` | yes (all null) |
| `additivesLabel` | string | — | — | yes (18/18) | `ללא תוספים מזוהים` | no |
| `mainIngredient` | string | — | — | yes (18/18) | `חלב` | no |
| `bestUseCases` | string[] | — | — | yes (18/18) | `["חלבון","רכיבים פשוטים","ילדים"]` | no |
| `consumerTakeaway` | string | — | — | yes (18/18) | `ציון גבוה ביחס למדף · ערך תזונתי נמוך יחסית` | no |
| `nova_proxy` | number | — | — | yes (18/18) | `1` | no |
| `red_labels` | string[] | — | — | yes (18/18) | `[]` | no |
| `ingredients_display` | string | — | — | yes (18/18) | `חלב` | no |
| `energy_kcal` | number | — | — | yes (18/18) | `67.0` | no |
| `filterTags` | string[] | — | — | yes (18/18) | `["type:dairy","no_additives","high_protein","high` | no |

### Nested: `expansion`

| field path | type | in granola? | in snacks? | in milk? | example value (≤60 chars) | null allowed? |
|---|---|---|---|---|---|---|
| `expansion.nutrition` | object-null | yes (42/42) | yes (18/18) | — | `{"energyKcal":372,...}` | no (always obj) |
| `expansion.nutrition.energyKcal` | number-null | yes (42/42) | yes (18/18) | — | `372.0` | yes (snacks all null) |
| `expansion.nutrition.protein` | number-null | yes (42/42) | yes (18/18) | — | `15.9` | yes (snacks all null) |
| `expansion.nutrition.sugar` | number-null | yes (42/42) | yes (18/18) | — | `null` | yes |
| `expansion.nutrition.fat` | number-null | yes (42/42) | yes (18/18) | — | `0.5` | yes (snacks all null) |
| `expansion.nutrition.fiber` | number-null | yes (42/42) | yes (18/18) | — | `11.8` | yes (snacks all null) |
| `expansion.nutrition.sodium` | number-null | yes (42/42) | yes (18/18) | — | `38.0` | yes (snacks all null) |
| `expansion.ingredients` | string-null | yes (42/42) | yes (18/18) | — | `שיבולת שועל (מכיל גלוטן), סובין שיבולת שועל (מכ` | yes (snacks all null) |
| `expansion.confidenceLabel` | string | yes (42/42) | yes (18/18) | — | `נתונים בבדיקה` | no |
| `expansion.servingNote` | string | yes (42/42) | yes (18/18) | — | `ל-100 גרם` | no |
| `expansion.positiveSignals` | string[] | yes (42/42) | yes (18/18) | — | `["קלוריות נמוכות יחסית (372 קק\"ל)","עשיר בחלבו` | no |
| `expansion.limitingFactors` | string[] | yes (30/42) | yes (18/18) | — | `["קלורית גבוהה (491 קק\"ל ל-100 גרם)"]` | yes (absent 12 granola) |
| `expansion.comparisonContext` | string | yes (42/42) | yes (18/18) | — | `מהטובות במדף — חלבון וסיבים גבוהים יחד. נדיר ` | no |
| `expansion.bottomLine` | string | no | yes (18/18) | — | `70/B: הניקוד הגבוה ביותר בקטגוריה — הבסיס הנקי` | no |
| `expansion.unknowns` | string[] | no | yes (18/18) | — | `["ערכי אנרגיה, חלבון, סוכר, שומן, סיבים תזונתיים ` | no |
| `expansion.caveats` | string[] | no | no | — | absent in all 3 JSONs | n/a |

### Nested: milk-only product objects (`consumerExplanation`, `bariInterpretation`, `dimensions`, `matrix_integrity`, `explanation_drivers`)

| field path | type | in granola? | in snacks? | in milk? | example value (≤60 chars) | null allowed? |
|---|---|---|---|---|---|---|
| `consumerExplanation` | object | — | — | yes (18/18) | `{"whyRated":"ציון Bari 85...`, | no |
| `consumerExplanation.whyRated` | string | — | — | yes (18/18) | `ציון Bari 85 (מצוין) — בין השאר בזכות רשימת ר` | no |
| `consumerExplanation.good` | string[] | — | — | yes (18/18) | `["רשימת רכיבים יחסית פשוטה","הרכב המוצר קרוב י` | no |
| `consumerExplanation.watchOut` | string[] | — | — | yes (18/18) | `["ערך תזונתי ביחס למוצר נמוך"]` | no |
| `consumerExplanation.context` | string | — | — | yes (18/18) | `פשוט ברכיבים, אך ערך תזונתי ביחס למוצר לא בהכר` | no |
| `consumerExplanation.takeaway` | string | — | — | yes (18/18) | `ציון גבוה ביחס למדף · ערך תזונתי נמוך יחסית` | no |
| `bariInterpretation` | array | — | — | yes (18/18) | `[{"key":"ingredients","label":"איכות רכיבים",...` | no |
| `bariInterpretation[].key` | string | — | — | yes (18/18) | `ingredients` | no |
| `bariInterpretation[].label` | string | — | — | yes (18/18) | `איכות רכיבים` | no |
| `bariInterpretation[].score` | number | — | — | yes (18/18) | `100` | no |
| `bariInterpretation[].strength` | string | — | — | yes (18/18) | `חזק` | no |
| `bariInterpretation[].interpretation` | string | — | — | yes (18/18) | `רשימת רכיבים קצרה — מרכיב בסיס מוכר` | no |
| `dimensions` | object | — | — | yes (18/18) | `{"processing_quality":{...}, "nutrient_density":` | no |
| `dimensions.*.score` | number | — | — | yes (18/18) | `95` | no |
| `dimensions.*.display_name` | string | — | — | yes (18/18) | `processing_quality` | no |
| `matrix_integrity` | object | — | — | yes (18/18) | `{"matrix_integrity_score":100,...}` | no |
| `matrix_integrity.matrix_integrity_score` | number | — | — | yes (18/18) | `100.0` | no |
| `matrix_integrity.reconstruction_depth` | number | — | — | yes (18/18) | `0` | no |
| `matrix_integrity.structural_degradation_level` | string | — | — | yes (18/18) | `minimal` | no |
| `matrix_integrity.engineering_intensity` | number | — | — | yes (18/18) | `0.0` | no |
| `matrix_integrity.dominant_matrix_signals` | string[] | — | — | yes (18/18) | `[]` | no |
| `matrix_integrity.integrity_summary` | string | — | — | yes (18/18) | `Matrix integrity 100/100 — minimal degradation` | no |
| `explanation_drivers` | string[] | — | — | yes (18/18) | `["PRIMARY SIGNAL: nutrient_density=10.7",...]` | no |

---

## Table 2: Page-level / `_meta` fields

| field | type | in granola? | in snacks? | in milk? | example value (≤60 chars) |
|---|---|---|---|---|---|
| `_meta.generated` | string | yes | yes | — | `2026-06-07T05:23:06.033439+00:00` |
| `_meta.category` | string | yes | yes | — | `granola` |
| `_meta.product_count` | number | yes | yes | — | `42` |
| `_meta.scored_count` | number | yes | yes | — | `53` |
| `_meta.schema` | string | yes | yes | — | `BariProductVM[]` |
| `_meta.version` | string | yes | yes | — | `v1` |
| `_meta.provenance` | string | yes | no | — | `run_cereals_005 granola sub-pool...` |
| `_meta.expansion` | string | no | yes | — | `interpretive_expansion_system_v2` |
| `_meta.source_run_id` | string | no | yes | — | `yochananof_snack_retail_v1` |
| `_meta.scope_note` | string | no | yes | — | `ניתוח מדף יוחננוף בלבד — לא סקר שוק ישראלי` |
| `_meta.editorial_note` | string | no | yes | — | `18 מוצרים נבחרו מתוך 48 שקיבלו ציון על בסיס מ` |
| `_meta.production_pass` | string | no | yes | — | `CE-approved corpus v2; NOVA terminology...` |
| `generated_at` (milk) | string | — | — | yes | `2026-05-20` |
| `data_source` (milk) | string | — | — | yes | `מדגם מדף (תוויות) · נכון ל־2026 · כל המוצרים ` |
| `comparison_title` (milk) | string | — | — | yes | `השוואת חלב ותחליפי חלב` |
| `story_headline` (milk) | string | — | — | yes | `השווינו 18 מוצרי חלב ומשקאות חלב פופולריים ביש` |
| `story_teaser` (milk) | string | — | — | yes | `ההשוואה מתבססת על רכיבים, ערכים תזונתיים, רכיבי` |
| `philosophy_note` (milk) | string | — | — | yes | `המידע נועד לספק הקשר והשוואה בין מוצרים, ולא מהו` |

---

## Table 3: Page-level string constants consumed by page-data `.ts` files

| exported constant name | file | example value (≤80 chars) |
|---|---|---|
| `granolaMetadataLine` | `granola-page-data.ts:42` | `42 מוצרים • עודכן ביוני 2026` |
| `granolaHero` | `granola-page-data.ts:47` | `{eyebrow:"גרנולה ומוזלי", title:"גרנולה ומוזלי: 53 מוצרים, פער של 47 נקודות"}` |
| `granolaPrologueSentences` | `granola-page-data.ts:52` | `["בדקנו 53 מוצרי גרנולה ומוזלי מהמדף הישראלי..."]` |
| `granolaCategoryNote` | `granola-page-data.ts:59` | `גרנולה ומוזלי הם דגן אפוי עם שמן וממתיק...` |
| `granolaMethodologyLines` | `granola-page-data.ts:62` | `["בדקנו 53 מוצרי גרנולה ומוזלי משלוש רשתות..."]` |
| `granolaComparisonMetadata` | `granola-page-data.ts:68` | `{title:"השוואת גרנולה ומוזלי | Bari", description:"השוואת 53..."}` |
| `snacksMetadataLine` | `snacks-comparison-page-data.ts:56` | `18 מוצרים בדף · 53 נסרקו · 48 קיבלו ציון ...` |
| `snacksHero` | `snacks-comparison-page-data.ts:61` | `{eyebrow:"חטיפים", title:"השוואת חטיפים"}` |
| `snacksPrologueSentences` | `snacks-comparison-page-data.ts:67` | `["חטיפי תמרים, גרנולה, פיטנס ופרוטאין על אותו מדף..."]` |
| `snacksCategoryNote` | `snacks-comparison-page-data.ts:77` | `"הערת קטגוריה — 'הכי טוב' כאן הוא B, לא A` |
| `snacksMethodologyLines` | `snacks-comparison-page-data.ts:83` | `(imported from snack-analysis-content.ts)` |
| `snacksComparisonMetadata` | `snacks-comparison-page-data.ts:85` | `{title, description}` |
| `milkMetadataLine` | `milk-comparison-page-data.ts:90` | `18 מוצרים בדירוג · מדגם מדף (תוויות), 2026 · ממוין ` |
| `milkHero` | `milk-comparison-page-data.ts:92` | `{eyebrow:"חלב ותחליפים", title:"השוואת חלב ותחליפי חלב"}` |
| `milkPrologueSentences` | `milk-comparison-page-data.ts:98` | `["חלב נראה כמו קטגוריה פשוטה, אבל המדף מספר סיפור..."]` |
| `milkMethodologyLines` | `milk-comparison-page-data.ts:106` | `["ההשוואה מבוססת על מוצרי חלב שנאספו ונבדקו..."]` |
| `milkCategoryNote` | `milk-comparison-page-data.ts:118` | `הערת קטגוריה — 'דל שומן' אינו אוטומטית ציון גבוה יותר` |
| `milkComparisonMetadata` | `milk-comparison-page-data.ts:129` | `{title:"השוואת חלב ואלטרנטיבות | Bari", description:"השוואת מוצרים..."}` |
| `milkBlogLink` | `milk-comparison-page-data.ts:124` | `{href:"/blog/milk-analysis", label:"קראו את הניתוח העיתונאי בבלוג ←"}` |

---

## Required vs nullable summary

**Required in ALL products across ALL 3 categories** (non-null in every product):
- `id` / `barcode` (naming differs by format)
- `score` (numeric in every product)
- `grade` (string in every product)
- `name` / `name_he` / `displayTitle`

**Null allowed in at least one product**:
- `imageUrl` (granola has 2 products with null)
- `expansion.nutrition.*` (snacks: all 6 nutrition fields null in all products; granola: sugar/sodium occasional null)
- `expansion.ingredients` (snacks: all null)
- `expansion.limitingFactors` (granola: absent in 12/42)
- `confidence_level` (granola: absent in 9/42)
- `proteinPer100ml` (milk: some null)
- `sugarPer100ml` (milk: all null)
