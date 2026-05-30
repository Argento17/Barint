# Bread Comparison Page — Cursor Build Handoff
## real_bread_retail_003_v1 | Shufersal Representative Shelf

**UX reference:** Use the existing milk comparison page as the direct UX template. Adapt layout, card patterns, column structure, and interaction patterns from that page — do not invent new structure.

**Data source:** `real_bread_retail_003_v1_curated_comparison_dataset.json` (31 products, 6 clusters)

**Page URL slug suggestion:** `/bread-comparison` or `/לחם-מושווה`

---

## 1. Hero Section

**Headline (Hebrew):** `מה באמת יש בלחם שלכם?`

**Sub-headline:** `ניתחנו 256 מוצרי לחם ממדף שופרסל. רק 81 קיבלו מספיק נתונים לניתוח מהימן. בחרנו 31 מוצרים שמייצגים את המגוון הקיים.`

**Scope disclaimer (prominent, not buried):**
> הניתוח מבוסס על מדף שופרסל בלבד — לא סקר שוק ישראלי. חלק מהמוצרים לא קיבלו ציון מפני שהנתונים הציבוריים לא הספיקו לניתוח.

**Stats strip (3 numbers):**
- 256 — מוצרים שנסרקו
- 81 — מוצרים עם נתונים מספיקים לניתוח
- 31 — נבחרים לדף זה

---

## 2. Cluster Navigation / Filter

Display 6 cluster tabs or filter pills. Use `website_cluster` + `website_cluster_label_he` from JSON:

| cluster_id | label_he |
|:-----------|:---------|
| `everyday` | לחם יומיומי — עוגן צרכני |
| `strong` | מוצרים עם מבנה גרעיני חזק |
| `fermentation` | ספקטרום התסיסה — מחמצת בפועל |
| `wellness_ambig` | לחמי בריאות — שאלות המבנה |
| `crackers` | קרקרים — מגוון המבנים |
| `transparency` | שקיפות הנתונים — מה לא ניתן לנתח |

Default view: all clusters visible. Filter = show selected cluster only.

---

## 3. Main Comparison Table

**Show all products where `display_score_boolean = true`.** For transparency cluster (`display_score_boolean = false`), show a separate panel (see Section 6 below).

### Table columns

| Column label (Hebrew) | JSON field | Notes |
|:----------------------|:-----------|:------|
| מוצר | `name_he` + `image_url` + `source_url` | Image + name, link to Shufersal |
| קטגוריה | `category_display_he` | לחם / קרקר / פיתה / מוצר אפייה |
| ציון | `score` (integer) + `grade` | Show score/grade only if `display_score_boolean=true`. Never show score for null. |
| רמת ודאות | `confidence_label_he` | Display as badge/chip |
| סיבים תזונתיים | `fiber_g` | Per 100g, in grams |
| תסיסה | `fermentation_status_he` | See signal glossary below |
| מבנה קצר | `structural_summary_he` | Short descriptor |
| הערה עיקרית | `why_featured_he` | Why this product appears |

### Score display rules
- `display_score_boolean = true` → show score + grade badge (color by grade: A=green, B=blue, C=yellow, D=red)
- `display_score_boolean = false` → show "אין ציון — נתונים לא מספיקים" (grey, no number)
- **Never** show score=null as 0 or as any number

### Confidence badge colors
- `נתונים מלאים יחסית` → green badge
- `נתונים חלקיים` → yellow badge
- `חסרים נתונים מהותיים` → orange badge
- `לא מספיק לניתוח ודאי` → grey badge

### Fermentation signal display
Map `fermentation_status_he` values to icons + short labels:

| Raw value | Display icon | Short label |
|:----------|:-------------|:------------|
| מחמצת אמיתית (מזוהה ברכיבים) | ✅ | מחמצת ברכיבים |
| מחמצת אמיתית (עם שמרים עזר) | ✅~ | מחמצת + שמרים עזר |
| מחמצת בשם, שמרים ברכיבים | ⚠️ | שמרים ברכיבים |
| שמרים תעשייתיים בלבד | ○ | שמרים תעשייתיים |
| לא ידוע — חסרים נתוני רכיבים | — | לא ידוע |
| לא זוהה תוהל | — | לא רלוונטי (קרקרים) |

**Tooltip on ⚠️ icon:** "שם המוצר מכיל 'מחמצת', אך רשימת הרכיבים מציגה שמרים תעשייתיים — לא מחמצת אמיתית."

---

## 4. Structural Map (Scatter Plot)

A 2-axis positioning chart for all displayable products.

**X axis:** בסיס הדגן (מזוקק ↔ שלם יותר)
- Derive from `fiber_source_status_he`:
  - "סיבים מדגן שלם" → X position right (whole grain side)
  - "חלק מהסיבים מתוספים" → X position center-left
  - "מקור הסיבים לא ברור" → X position center

**Y axis:** מורכבות ומנגנון (פשוט ↔ מהונדס/מורכב)
- Use `score` as proxy (higher score = more coherent structure = higher Y)
- Products with `display_score_boolean=false` are excluded from this map

**Dot color:** by `grade` (A=green, B=blue, C=yellow)
**Dot size:** uniform
**Dot label:** `name_he` (abbreviated, show on hover)
**Clusters:** color-shade background regions loosely grouping everyday / strong / crackers

**Callouts (3–4 annotation labels on the map):**
1. "מחמצת אמיתית — נדיר" pointing to cluster with genuine fermentation products
2. "מיינסטרים מפתיע — ברמן אקטיב" pointing to score=72 everyday product
3. "ציון גבוה, מנגנון שונה — לחם טחינה" pointing to score=82 whole_food_fat product
4. "קרקרים — לא לחם, אבל מנותח" pointing to cracker cluster

**Note below chart:**
> המפה מבוססת על מוצרים עם נתונים מספיקים בלבד (81 מתוך 256). מיקום משוער — לא ייצוג מדויק של כל ממד.

---

## 5. Look-Alike Comparison Pairs

Display as side-by-side card pairs with a connecting arrow or VS label. For each pair, show both products' key stats.

**Pair 1: מיינסטרים מפתיע מול תווית מחמצת**
- Left: לחם ברמן אקטיב (everyday, score=72, fiber=11.4g, מחמצת אמיתית)
- Right: לחם מחמצת מכוסמין (wellness, score=66, fiber=6.7g, מחמצת בשם+שמרים ברכיבים)
- Caption: "ברמן אקטיב — מותג יומיומי עם מחמצת אמיתית ברכיבים. מול מוצר שמציג 'מחמצת' בשם אבל שמרים תעשייתיים בפועל."

**Pair 2: דגן שלם בפועל מול שם שמרמז על כך**
- Left: לחם ירוק מקמח מלא (strong, score=80, fiber=6.4g, קמח מלא ברכיבים)
- Right: לחם כוסמין לבן (wellness, score=68, fiber=3.3g, כוסמין לבן)
- Caption: "כוסמין הוא סוג דגן, לא מידת מלאות. 'כוסמין לבן' הוא קמח מזוקק מכוסמין — לא כוסמין מלא."

**Pair 3: לחם פשוט מול לחם פרימיום**
- Left: לחם אחיד פרוס קל (everyday, score=73, fiber=10.4g, שמרים תעשייתיים)
- Right: לחם מחמצת אגוזים צימוקים (wellness, score=60, fiber=3.7g, מחמצת בשם+שמרים)
- Caption: "לחם אחיד פרוס קל קיבל ציון גבוה יותר — עם סיבים גבוהים יותר. מנגד: לחם הפרימיום עם האגוזים קיבל ציון נמוך יותר עם סיבים נמוכים יותר."

**Pair 4: שיפון עם ובלי תווית מחמצת**
- Left: לחם שיפון מלא מסטמכר (strong, score=76, fiber=10.6g, שמרים תעשייתיים)
- Right: לחם מחמצת שיפון+אגוזים (fermentation mismatch, score=61, fiber=6.1g, מחמצת בשם+שמרים)
- Caption: "שיפון מלא — ציון 76 גם בלי מחמצת. לחם שיפון עם תווית מחמצת ואגוזים קיבל ציון נמוך יותר."

**Pair 5: קרקר אמיתי מול קרקר מהונדס**
- Left: קרקר כוסמין מלא ושומשום (crackers, score=82, fiber=10.0g)
- Right: קרקר קרם קרקר (crackers, score=59, fiber=3.0g)
- Caption: "שני קרקרים — מבנה שונה לחלוטין. כוסמין מלא עם שומשום: ציון 82. קרם קרקר עם שלושה מקורות סוכר: ציון 59."

---

## 6. Transparency Panel

Display at the bottom of the page as a distinct section (different background color, grey or muted).

**Section heading:** `מוצרים שלא קיבלו ציון — ולמה`

**Intro text:**
> חלק מהמוצרים הנפוצים ביותר לא מציגים נתוני תזונה ורכיבים מלאים באתר שופרסל. לא ניתן לנתח מה שאין — לכן לא נציג להם ציון. זו לא שיפוט על המוצר, אלא על זמינות הנתון.

**Display the 4 transparency cluster products as cards:**
For each: show `name_he`, `image_url`, `suggested_card_blurb_he`
Do NOT show score (it is null / INSUFFICIENT).
Show: "אין ציון — אין נתוני רכיבים מספיקים"

**Transparency cluster products:**
1. מארז פיתות אסליות — "פיתות אסליות — נפוצות מאוד, אבל אין לנו מספיק נתונים לציון."
2. לחם מחמצת אגוזים פרוס — "מחמצת ואגוזים — נשמע מצוין. אך הנתונים לא מספיקים לציון."
3. לחם אחיד — "לחם אחיד ללא תזונה מלאה. אנחנו לא מציגים ציון בלי מידע מספיק."
4. חלה קלועה — "חלה קלועה — ייצגת, אבל חסרים הנתונים. לא נציג ציון."

**Footer note for the section:**
> 46% מהמוצרים שסרקנו לא הציגו נתוני רכיבים מלאים. זה מגבלה של זמינות הנתונים הציבוריים — לא של הניתוח שלנו.

---

## 7. Footnotes / Methodology Note

Below the page, collapsible or linked:

> **על הניתוח:** כל המוצרים נסרקו ממדף שופרסל בין התאריכים 25–26 במאי 2026. הנתונים — רכיבים, ערכים תזונתיים, תמונה — מקורם בדפי המוצר הציבוריים. הציון מבוסס על מבנה הדגן, מקור הסיבים, מנגנון התסיסה, ורמת העיבוד. ציון לא מוצג כאשר הנתונים לא מספיקים לניתוח מהימן. לא נותחו מוצרים ממדפים אחרים.

---

## 8. Implementation Notes for Cursor

- **Field mapping is explicit** — every JSON field name above maps directly to the data file
- **`display_score_boolean`** is the gate for all score display — check this field first, every time
- **`safe_for_ranking_boolean`** = same as `display_score_boolean` for this dataset — use it for any rank or sort
- **`safe_for_blog_boolean`** = true for displayable products — use this to flag linkable products
- **Cluster F products** always have `display_score_boolean = false` — they are editorial examples only
- **`לחם טחינה פרוס`** has `score=82` but `_category_internal = "whole_food_fat"` — show it normally on the wellness_ambig cluster, but the tooltip/card should include the `why_featured_he` field which explains the tahini-fiber mechanism
- **Do not auto-sort by score across all clusters** — each cluster has its own editorial curation logic
- **Hebrew text direction:** all Hebrew fields are RTL — ensure proper `dir="rtl"` or tailwind RTL class on containers
- **Image URLs:** from Shufersal CDN — may be subject to hotlink policy; test before deploying
