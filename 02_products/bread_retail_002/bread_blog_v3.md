# Bari Bread Editorial — Implementation Handoff v3
**Date:** 2026-05-27
**Replaces:** blog_handoffs_v2.md
**Dataset:** real_bread_retail_002_v2_frontend_dataset.json — 108 products, Shufersal, 2026-05-25
**Reference architecture:** Milk Comparison page

---

## Why This Document Replaces v2

The v2 system failed at structural level. It produced fragments — themed comparison cards with no editorial spine, no analytical narrative, and no reason for specific products to appear together. This document resets from scratch around the milk comparison architecture: one coherent investigation per article, one analytical flow, products as evidence inside the narrative.

The bread articles are not product listing pages. They are shelf investigations.

---

## What Changed From v2

| v2 | v3 |
|----|----|
| 3 articles | 2 articles |
| Component-first design | Investigation-first design |
| Products as heroes | Products as evidence |
| Side-by-side comparison cards | Comparison matrix (table + explanation) |
| Repeated mini-duels | High-contrast pairs with causal explanation |
| No map | Category map with clustering logic |
| Vague "What's On The Shelf" | Decomposition system with observable dimensions |
| Defensive copy with repeated disclaimers | Assertive, finding-first copy |

---

## Architecture That Applies to Both Articles

Both articles follow this exact section sequence:

```
A. Intro
B. Key Findings (3–5 InsightCards)
C. Category Map
D. What's On The Shelf (Composition Breakdown)
E. Comparison Section
F. Glossary
G. Full Comparison CTA
H. Methodology Note
```

No section is skippable. The order is not flexible.

---

## Dataset Constants (Use These Exactly)

```
source: שופרסל
snapshot_date: מאי 2026
total_scraped: 108
not_analyzed: ~46% (no ingredient data available)
verified: 32 (ingredient list + nutrition panel)
partial: ~36 (ingredient list only)
score_range: 40–82
score_mean: 56.0
score_median: 62.0
highest_score: 82/A (קרקר כוסמין מלא ושומשום)
no_grade_A_bread: true (only cracker reached A)
```

---
---

# ARTICLE 1 — "הלחם שאתה קונה בכל שבוע"

**URL:** `/bread/everyday`
**Hebrew title:** הלחם שאתה קונה בכל שבוע

---

## 1. Page Purpose

This article investigates the everyday bread shelf — sliced breads, rolls, pitas, and basic whole-grain products that form the weekly shopping basket for most Israeli households. The investigation focuses on what separated similar-looking products in score and composition, with particular attention to the gap between the 46% of the shelf that could not be analyzed and the 54% that could. The central finding: products with whole grain flour in the first ingredient position separated clearly from those that didn't, regardless of packaging tone or price point.

---

## 2. Editorial Spine

> "Everyday breads ranged from 40 to 75 — and ingredient list position explained most of that gap, not the product name."

---

## 3. Full Page Structure

```
1.  Hero + ShelfStatBar
2.  Intro paragraph (130–160 words)
3.  Key Findings (4 InsightCards)
4.  Category Map — BreadEverydayMap
5.  What's On The Shelf — CompositionBreakdown
6.  Score Driver System explanation (prose + ScoreDriverTable)
7.  Main Comparisons — ProductComparisonMatrix
8.  Reader Takeaways (3 short bullets, no recommendation framing)
9.  Glossary — GlossaryAccordion
10. Full Comparison CTA
11. Methodology Note
```

---

## 4. Component Mapping

| Section | Component | Purpose |
|---------|-----------|---------|
| Hero + ShelfStatBar | ShelfStatBar | Shelf scope, data coverage, key numbers |
| Key Findings | InsightCardsGrid (4 cards) | Four findings that frame the investigation |
| Category Map | BreadEverydayMap | Visualize how grain structure and fiber source clustered products |
| What's On The Shelf | CompositionBreakdown | Five observable dimensions, how each affected score |
| Score Driver System | ScoreDriverTable | Plain-language mapping of signals to score impact |
| Main Comparisons | ProductComparisonMatrix | Two high-contrast pairs with causal explanation |
| Reader Takeaways | TakeawayList | Three factual synthesis bullets |
| Glossary | GlossaryAccordion | Six terms, short definitions |
| Full Comparison CTA | ComparisonCTA | Link to full table |
| Methodology | MethodologyNote | 5 sentences max |

---

## 5. Component Specifications

---

### ShelfStatBar
*(carry from v2 specification — same component)*

**Inputs:**
```json
{
  "scraped": 108,
  "scored": "~60",
  "not_analyzed_pct": 46,
  "retailer": "שופרסל",
  "date": "מאי 2026"
}
```

**Display:**
```
108 נסרקו  |  ~60 קיבלו ציון  |  46% ללא נתונים מספיקים  |  שופרסל · מאי 2026
```

Single line, no icons, no color coding, no badge. Plain text.

---

### InsightCardsGrid — Article 1

Four cards. Each card has: type tag (Finding / Gap / Pattern / Ambiguity), bold finding sentence, 1–2 sentence explanation, no CTA.

**Card 1 — Finding:**
> **קמח מלא ראשון ברשימה הבדיל בין המוצרים יותר מכל גורם אחר.**
> מוצרים שציינו קמח מלא כרכיב ראשון קיבלו ציון ממוצע גבוה ב-12 נקודות ממוצרים עם קמח לבן כרכיב ראשון.

**Card 2 — Gap:**
> **46% מהמוצרים לא קיבלו ציון — הנתונים לא היו זמינים.**
> לא מדובר בכישלון ניתוח. נתוני הרכיבים פשוט לא היו זמינים לציבור עבור חלק גדול מהמדף. זה עצמו ממצא.

**Card 3 — Finding:**
> **17.4 גרם סיבים לא הצדיקו ציון גבוה — כשהסיבים הגיעו מאינולין.**
> מוצר עם הסיבים הגבוהים ביותר בקטגוריה (17.4g) קיבל את הציון הנמוך ביותר האפשרי בגלל מקור הסיבים, לא כמותם.

**Card 4 — Pattern:**
> **רשימות רכיבים קצרות ופשוטות יחסו ציונים עקביים.**
> מוצרים עם פחות מ-7 רכיבים והרכיב הראשון קמח מלא הפגינו עקביות גבוהה יותר בציון מאשר מוצרים ארוכי-רשימה עם אותו בסיס דגנים.

---

### BreadEverydayMap

**Purpose:** Visualize where everyday products landed on two observable axes.

**X axis:** Grain structure — from "קמח לבן ראשון" (left) to "קמח מלא מאומת ראשון" (right)
**Y axis:** Fiber source — from "מקור לא ברור / מוסף" (bottom) to "סיבים ממטריצת הדגן" (top)

**Clusters (4):**

| Cluster | Label | Position | Products |
|---------|-------|----------|----------|
| A | קמח מלא + סיבים מטריצה | Top-right | לחם שיפון קל, לחם אקסקלוסיבי שיפון מלא, לחם שיפון גרעינים |
| B | קמח מלא + מקור סיבים לא ברור | Middle-right | לחם קמח מלא 100%, לחם שיפון מלא פרוס |
| C | קמח לבן / מעורב + סיבים מטריצה | Top-left | -- (rare in everyday) |
| D | לא זמין לניתוח | Gray, scatter | ~46% of shelf |

**Visual specs:**
- Dot = one product. Size = constant (no score encoding in size).
- Color = confidence tier: blue = verified, gray = partial, light gray = insufficient
- Cluster label appears as soft zone, not hard border
- Tooltip on hover: product name + score + one-line summary
- Outlier annotation: label the fiber laundering outlier (bottom-left, high fiber + added source)
- No animation. No gamification. Static or minimal-hover-only interaction.
- Mobile: collapse to cluster legend + top 3 products per cluster list

**Axis labels (consumer-facing):**
- X: קמח מלא מאומת ← → קמח לבן ראשון
- Y: סיבים ממקור הדגן ← → סיבים מוספים / לא מאומת

**Title:** מה מפריד בין המוצרים — שני ממדים

**Caption:** כל נקודה = מוצר אחד. מיקום מבוסס על רשימת הרכיבים בלבד — לא על הצגת המוצר.

**Do NOT:**
- Use rainbow color palette
- Encode score as bubble size (confusing)
- Show score numbers on the map itself
- Animate transitions
- Show recommendation badges in tooltip

---

### CompositionBreakdown

**Purpose:** Explain the five observable dimensions that determined scores. This is the article's most informative section — the one that answers "what actually moved the score."

**Structure:** Five rows, each row is one dimension.

**Row format:**
```
[Dimension name] — [One-sentence definition]
[What it looks like in the ingredient list]
[How it affected scores in this dataset]
[One specific product example]
```

**Five Dimensions for Article 1:**

---

**1. מיקום קמח ברשימה — Flour Position**

הרכיב הראשון ברשימת הרכיבים הוא הנפוח ביותר.

*מה זה אומר:* "קמח חיטה מלאה" כרכיב ראשון = הרוב הגדול של המוצר הוא קמח מלא. "קמח חיטה" (ללא "מלא") ראשון = בסיס לבן, גם אם קמח מלא מופיע מאוחר יותר.

*אפקט על ציון:* מוצרים עם קמח מלא ראשון קיבלו ציון ממוצע גבוה ב-12 נקודות.

*דוגמה:* לחם שיפון קל — "קמח שיפון מלא" ראשון ברשימה — 75/B

---

**2. מקור הסיבים — Fiber Source**

ערך הסיבים בלוח התזונה לא מספר את הסיפור המלא.

*מה זה אומר:* סיבים יכולים להגיע מהדגן עצמו (מטריצה), או להיות מוספים לאחר מכן (אינולין, שורש עולש, פסיליום). ציון הסיבים בלוח יכול להיות זהה — אבל ההרכב שונה.

*אפקט על ציון:* מוצרים עם סיבים מוספים קיבלו ציון נמוך יותר גם כאשר ערך הסיבים היה גבוה.

*דוגמה:* לחמניות לס קיטו — 17.4g סיבים מאינולין — 40/D. לחם שיפון קל — 12.4g סיבים ממטריצת הדגן — 75/B.

---

**3. אורך רשימת הרכיבים — Ingredient List Length**

*מה זה אומר:* רשימה ארוכה אינה בהכרח בעיה, אבל רשימה ארוכה עם תוספים לצד בסיס קמח לבן מצביעה על הנדסת מוצר בהיעדר מטריצה חזקה.

*אפקט על ציון:* מוצרים עם ≤6 רכיבים ובסיס קמח מלא הציגו עקביות גבוהה יותר בציון.

*דוגמה:* לחם שיפון קל — 4 רכיבים עיקריים — 75/B.

---

**4. שקיפות נתונים — Data Availability**

*מה זה אומר:* ~46% מהמוצרים לא קיבלו ציון מלא כי לא היו נתוני רכיבים מלאים זמינים לציבור. לא ניתן לנתח מוצר שרשימת רכיביו לא גלויה.

*אפקט על ציון:* מוצרים ללא נתונים מקבלים "לא נוקד" — לא ציון נמוך.

*דוגמה:* חלק גדול ממוצרי ברמן, וונדר, ואנג'ל לא היו זמינים לניתוח מלא.

---

**5. הכרזת תבואה מלאה — Whole Grain Claim Accuracy**

*מה זה אומר:* מוצרים שמציינים "100% מלא" או "מלא" בשמם אבל לא מאמתים זאת ברשימת הרכיבים (כלומר, קמח לבן מופיע ראשון) מקבלים ניתוח שמרני יותר.

*אפקט על ציון:* לחם קמח מלא 100% — הציון מבוסס על ניתוח רשימת הרכיבים בפועל, לא על שם המוצר.

*דוגמה:* לחם קמח מלא 100% — ציון 70/B. הרכיב הראשון ברשימה מבוסס על ניתוח.

---

**Visual specs for CompositionBreakdown:**
- Five rows, clearly labeled
- Row background: alternating white / very light gray
- Dimension name: bold, prominent
- No icons
- Product examples appear inline, with score and grade displayed inline next to product name
- Do NOT use cards for the product examples — inline text only
- Mobile: full single-column, rows stack

---

### ScoreDriverTable

**Purpose:** Compact reference table. What observable signal moved the score in which direction.

| מה שנראה ברשימת הרכיבים | השפעה על הציון | תווית UX |
|---|---|---|
| קמח מלא ראשון ברשימה | מגביר | "קמח מלא מאומת" |
| קמח לבן ראשון ברשימה | מוריד | "בסיס קמח לבן" |
| פחות מ-7 רכיבים | מגביר | "הרכב פשוט" |
| סיבים ממקור מטריצה | מגביר | "סיבים מהדגן" |
| אינולין / שורש עולש / פסיליום כמקור סיבים | ניטרלי-מוריד | "סיבים מוספים" |
| נתוני תזונה ורכיבים שניהם זמינים | מגביר | "נתונים מלאים" |
| רשימת רכיבים לא זמינה | מוריד / לא נוקד | "נתונים לא זמינים" |
| ≥3 מקורות ממתיקים שונים | מוריד | "ריבוי ממתיקים" |

**Visual specs:**
- Simple 3-column table. No color coding. Monospace or tabular font.
- "מגביר" / "מוריד" / "ניטרלי" — no green/red. Text only.
- Mobile: scrollable table, not collapsed

**Do NOT:**
- Use up/down arrows that suggest recommendation
- Add emoji or gamification
- Color "מגביר" green and "מוריד" red — this encodes judgment visually

---

### ProductComparisonMatrix — Article 1

**Purpose:** Two high-contrast pairs. Each pair: two products, why they're paired, what the specific gap reveals. Cursor does NOT choose the pairings.

**Layout:** Two panels. Each panel = one pair. Panel has: title, comparison table, one-paragraph explanation.

---

**Pair 1: "כמות הסיבים לא מספרת את הסיפור"**

Comparison logic: Same category (everyday bread/rolls), both have high fiber values. But fiber sources are completely different.

| מוצר | ציון | דרגה | סיבים | מקור הסיבים |
|------|------|------|-------|-------------|
| לחם שיפון קל | 75 | B | 12.4g | קמח שיפון מלא |
| לחמניות לס קיטו | לא נוקד | — | 17.4g | אינולין, מקורות מוספים |

**Explanation text (write exactly):**
> "לחמניות לס קיטו מציגות את ערך הסיבים הגבוה ביותר בכל הנתונים שנסרקו — 17.4 גרם ל-100 גרם. לחם שיפון קל מציג 12.4 גרם. ההבדל: ב-שיפון קל, הסיבים מגיעים מקמח שיפון מלא כרכיב ראשון. בלחמניות לס קיטו, הסיבים מגיעים ממקורות מוספים. הציון משקף את המקור, לא את המספר."

**Tension:** The product with higher fiber has lower alignment. This is the core insight of this pair.

---

**Pair 2: "שיפון מלא — גם בלי מחמצת"**

Comparison logic: Two rye breads, both without fermentation claims, both claiming whole grain. Different score. What's different?

| מוצר | ציון | דרגה | סיבים | הרכב |
|------|------|------|-------|------|
| לחם שיפון קל | 75 | B | 12.4g | קמח שיפון מלא · מחמצת |
| לחם שיפון עגול | 67 | B | 5.8g | קמח שיפון מלא · שמרים |

**Explanation text (write exactly):**
> "שניהם לחמי שיפון מלא. שניהם ללא טענת 'מחמצת' גדולה על האריזה. הפרש הציון — 8 נקודות — נובע בעיקר מהפרש כמות הסיבים הנגזרת מהרכב הדגן: 12.4 גרם מול 5.8 גרם. לחם שיפון קל גם כולל מחמצת ברשימת הרכיבים — שיפון עגול לא. שני הציונים הם B, אך הפרש של 8 נקודות מייצג הבדל אמיתי ברמת הדגן."

---

**Visual specs for ProductComparisonMatrix:**
- Each pair: one colored separator above title
- Comparison table: 5 columns max, clean horizontal rules, no cell colors
- Explanation: prose paragraph below table. NOT a card. NOT a badge summary.
- Do NOT add recommendation language to either product in either pair
- Both products should feel neutral in display — no winner/loser visual treatment
- Mobile: table scrolls horizontally OR collapses to stacked rows

---

### TakeawayList — Article 1

Three bullets. These are synthesis, not advice. They describe what the data showed. They do not tell the reader what to do.

```
• מיקום הקמח ברשימת הרכיבים הוא האינדיקטור שהפריד בין המוצרים יותר מכל גורם אחר.
• ערך הסיבים הגבוה לא תמיד מייצג מקור סיבים מהדגן — כדאי לבדוק אם אינולין או שורש עולש מופיעים ברשימה.
• 46% מהמוצרים על המדף לא היו זמינים לניתוח מלא — הנתונים עצמם חסרים, לא הציון.
```

**Do NOT:**
- Start any bullet with "כדאי לך" / "עדיף לרכוש" / "המלצה"
- Add a fourth bullet that summarizes the summary
- Add score color to the bullets

---

### GlossaryAccordion — Article 1

Six terms. Each: term, 1-sentence definition. Accordion — collapsed by default.

| מונח | הגדרה |
|------|--------|
| ציון ברי | ציון 0–100 המשקף עד כמה הרכב המוצר תואם את שמו והצגתו |
| דרגה | A–D, מבוסס על טווח הציון |
| קמח מלא | קמח שבו שלושת חלקי גרגר הדגן נשמרים — ציין לפי הרשימה |
| מקור סיבים | מאין מגיעים הסיבים — מהדגן עצמו או ממקורות מוספים |
| סדר רכיבים | ברשימת הרכיבים, הרכיב הראשון הוא הנפוח ביותר |
| ניתוח חלקי | ניתוח מבוסס על רשימת רכיבים בלבד — ללא לוח תזונה |

---

### ComparisonCTA — Article 1

```
→ לטבלת ההשוואה המלאה: כל 108 המוצרים, סוננים לפי ציון
```

No marketing language. No "discover more." A direct functional link.

---

### MethodologyNote — Article 1

**Max 5 sentences. No ontology. No framework explanation.**

> "ניתחנו 108 מוצרי לחם, פיתה וקרקרים ממדף שופרסל, מאי 2026. 32 מוצרים קיבלו ציון מלא — הם כוללים גם לוח תזונה וגם רשימת רכיבים זמינים לציבור. ~46% מהמוצרים לא קיבלו ציון כי הנתונים הנדרשים לא היו זמינים. הניתוח מבוסס על נתוני מדף שופרסל בלבד — לא על סקר שוק ישראלי מלא. ציוני ברי אינם מהווים המלצה רפואית."

---

## 6. Product Clustering Logic — Article 1

Cursor uses these clusters to position products on the BreadEverydayMap.

| Cluster | Label | Logic |
|---------|-------|-------|
| A — קמח מלא + סיבים מטריצה | Whole grain, native fiber | whole_grain=true AND fiber_laundering=false AND fiber_g ≥ 6 |
| B — קמח מלא + מקור לא ברור | Whole grain, unclear fiber | whole_grain=true AND fiber source unclear |
| C — בסיס לבן + תוספי סיבים | Refined base, added fiber | whole_grain=false AND fiber_laundering=true |
| D — לא זמין לניתוח | Insufficient data | confidence_level = "insufficient" |

**Outlier to annotate explicitly:**
- לחמניות לס קיטו — highest fiber (17.4g) + lowest score (40) + Cluster C → annotate with label on map

---

## 7. Score Driver System — Article 1

| Driver | Direction | Evidence | UX Label |
|--------|-----------|----------|----------|
| קמח מלא ראשון | ↑ strong | whole_grain=true + position 1 in list | "קמח מלא מאומת" |
| קמח לבן ראשון | ↓ | ingredient_architecture_summary contains "לבן" | "בסיס קמח לבן" |
| סיבים ממטריצה | ↑ | fiber_laundering=false AND whole_grain=true | "סיבים מהדגן" |
| סיבים מוספים | ↓ | fiber_laundering=true | "סיבים מוספים" |
| רשימה קצרה | ↑ weak | ingredient count ≤6 (not directly in dataset — use ingredient_architecture_summary) |  "הרכב פשוט" |
| נתונים מלאים | ↑ | confidence_level = "verified" | "נתונים מלאים" |
| ניתוח חלקי | neutral | confidence_level = "partial" | "ניתוח חלקי" |
| לא נוקד | block | confidence_level = "insufficient" | "נתונים לא זמינים" |

---

## 8. Comparison Logic — Article 1

**Pair 1: לחם שיפון קל vs. לחמניות לס קיטו**
- Why paired: both have high fiber values; completely different fiber sources
- Tension: more fiber ≠ better composition alignment
- Score spread: 75 vs. 40 (35-point gap)
- Driver of gap: fiber source (matrix grain vs. added inulin/psyllium)
- Never imply: לחמניות לס קיטו is bad / dangerous / not worth buying

**Pair 2: לחם שיפון קל vs. לחם שיפון עגול**
- Why paired: both rye whole grain, no fermentation claims, same basic category
- Tension: same grain type, different score
- Score spread: 75 vs. 67 (8-point gap)
- Driver of gap: fiber density (12.4g vs. 5.8g) + fermentation signal
- Never imply: לחם שיפון עגול is inferior. The 8-point gap is real; the framing is neutral.

---

## 9. Visual Hierarchy Rules — Article 1

**Dominant:** The Category Map and the CompositionBreakdown are the two visual anchors of the article. They carry the most weight visually.

**Secondary:** InsightCards and ProductComparisonMatrix

**Minimal:** ShelfStatBar (informational header), TakeawayList, Glossary

**Score display:** Always `[number] / [grade]` — no colored backgrounds.

**No dominant visual should be a product card.** Products appear in tables and prose, never as isolated hero cards.

**Spacing:** Follow milk comparison density. Dense but readable. Not airy. This is a reference document, not a landing page.

**Badge rules:** No badges on products in comparison tables. Scores and grades only.

---

## 10. Copywriting Rules — Article 1

**Approved examples:**
```
קמח שיפון מלא מצוין ראשון ברשימת הרכיבים.
הסיבים מגיעים ממקורות מוספים, לא ממטריצת הדגן.
46% מהמוצרים שנסרקו לא קיבלו ציון — נתונים לא זמינים.
הציון משקף קמח מלא כרכיב ראשון, בלי תוספי סיבים.
```

**Forbidden examples:**
```
זהו לחם מצוין לארוחת הבוקר שלך.
הסיבים המוספים מטעים את הצרכן.
קנה את זה, לא את זה.
לחם "בריא" לא תמיד בריא.
```

**One footer disclaimer only. Zero body disclaimers.**

---

## 11. Data Requirements — Article 1

**Dataset fields required per product:**
```
name_he, score, grade, confidence_level, confidence_label_he,
fiber_g, fermentation_real, fiber_laundering, whole_grain,
ingredient_architecture_summary, short_summary_he, displayable
```

**Products that must appear in this article:**
- לחם שיפון קל (75/B) — in both comparisons and map
- לחמניות לס קיטו (40/D, fiber=17.4g) — in Pair 1 and as map outlier
- לחם שיפון עגול (67/B) — in Pair 2
- לחם קמח מלא 100% (70/B) — in CompositionBreakdown example
- Representative unscored products from everyday segment — for map Cluster D

**Transparency handling:**
- Products with confidence_level="insufficient": show as gray dots on map, "לא נוקד" label
- Never show score=40 as if it were a real score for insufficient products
- In comparison tables: show "לא נוקד" for unscored products, not "40"

**Missing data handling:**
- If a product field is null: do not infer. Show "—" or "לא זמין"
- Do not rank insufficient products alongside verified products

---

## 12. Cursor Build Notes — Article 1

**Priorities:**
1. BreadEverydayMap must be built before articles go live — it is the visual anchor
2. CompositionBreakdown must be implemented as a distinct component, not repurposed from any card system
3. ProductComparisonMatrix must be a table component — not the old comparison card duel

**Likely failure modes:**
- Defaulting to product card layout for comparisons — explicitly prevented above
- Adding green/red color to score drivers — explicitly prevented above
- Treating insufficient products as low-scorers — they are unscored, not low-scored
- Removing the methodology note — it is mandatory
- Adding recommendation language to TakeawayList bullets

**Must remain consistent with milk comparison:**
- ShelfStatBar format
- GlossaryAccordion structure
- MethodologyNote position and length
- InsightCard format and 4-variant system
- Overall article density and readability register

**Must differ from milk comparison:**
- Map axes are bread-specific (grain structure × fiber source)
- Clustering logic is bread-specific
- CompositionBreakdown is new (milk didn't have this section)
- No "processing depth" section from milk — replaced with "What's On The Shelf" for bread

---
---

# ARTICLE 2 — "מה שכתוב לא תמיד מה שיש"

**URL:** `/bread/wellness`
**Hebrew title:** מה שכתוב לא תמיד מה שיש

---

## 1. Page Purpose

This article investigates the wellness and premium bread segment — products positioned around sourdough, spelt, seeds, and whole-grain claims. The investigation focuses on three specific alignment gaps found in the data: fermentation name vs. actual primary leavener, כוסמין vs. כוסמין מלא, and fiber value vs. fiber source. It also surfaces the finding that the highest score in the entire bread category (82/A) went to a cracker, and that no bread product reached Grade A. The article is sharper and more contrast-driven than Article 1.

---

## 2. Editorial Spine

> "The widest score divergence in the category was in the wellness segment — driven by three gaps: fermentation name vs. ingredient list, whole spelt vs. refined spelt, and fiber value vs. fiber source."

---

## 3. Full Page Structure

```
1.  Hero + ShelfStatBar
2.  Intro paragraph (150–180 words)
3.  Key Findings (5 InsightCards)
4.  Category Map — BreadWellnessMap
5.  What's On The Shelf — ThreeGapBreakdown
6.  Score Driver System explanation
7.  Main Comparisons — ProductComparisonMatrix (3 pairs)
8.  Synthesis paragraph (150–200 words)
9.  Glossary — GlossaryAccordion
10. Full Comparison CTA
11. Methodology Note
```

---

## 4. Component Mapping

| Section | Component | Purpose |
|---------|-----------|---------|
| Hero + ShelfStatBar | ShelfStatBar | Shelf numbers framing |
| Key Findings | InsightCardsGrid (5 cards) | Five major findings |
| Category Map | BreadWellnessMap | Two axes: fermentation vs. grain structure |
| What's On The Shelf | ThreeGapBreakdown | Sourdough gap / Spelt gap / Fiber gap |
| Score Drivers | ScoreDriverTable | Same component as Article 1 |
| Comparisons | ProductComparisonMatrix (3 pairs) | Three high-contrast pairs |
| Synthesis | SynthesisParagraph | Editorial conclusion |
| Glossary | GlossaryAccordion | Eight terms for this article |
| CTA | ComparisonCTA | Full table link |
| Methodology | MethodologyNote | 5 sentences max |

---

## 5. Component Specifications

---

### ShelfStatBar — Article 2

```
108 נסרקו  |  32 ניתוח מלא  |  13 מוצרי "מחמצת" עם שמרים עיקריים  |  שופרסל · מאי 2026
```

The "13 מוצרי מחמצת" stat belongs here, not buried in the article. It is the opening frame.

---

### InsightCardsGrid — Article 2

Five cards.

**Card 1 — Finding:**
> **13 מוצרים שמו "מחמצת" בשמם — בכולם, שמרים תעשייתיים הם המחמיץ הראשי ברשימה.**
> מחמצת מופיעה ברשימת הרכיבים שלהם, אך שמרים תעשייתיים מופיעים לפניה. לא ניתן לאמת שמחמצת היא מנגנון ההתפחה הדומיננטי.

**Card 2 — Ambiguity:**
> **"כוסמין" ו-"כוסמין מלא" — לא אותו דבר.**
> כשהמילה "מלא" לא מופיעה לידי שם הדגן ברשימת הרכיבים, ברי אינה יכולה לאמת שמדובר בכוסמין מלא. זה לא שלילה — זה גבול הנתונים.

**Card 3 — Finding:**
> **הציון הגבוה ביותר בכל הקטגוריה הוא של קרקר, לא לחם — 82/A.**
> אף לחם לא הגיע לדרגה A. הציון הגבוה ביותר של לחם הוא 75/B. הפרש של 7 נקודות בין הקרקר הטוב ביותר ללחם הטוב ביותר — שניהם כוסמין מלא.

**Card 4 — Finding:**
> **17.4 גרם סיבים קיבלו ציון נמוך מ-12.4 גרם סיבים — כשהמקור שונה.**
> כמות הסיבים לבדה לא מספיקה לאמת הרכב. מוצר עם סיבים ממקור מטריצת הדגן קיבל ציון גבוה יותר ממוצר עם סיבים גבוהים יותר אך ממקורות מוספים.

**Card 5 — Gap:**
> **זרעים על גבי בסיס מזוקק — לא אותו דבר כמו זרעים בתוך בסיס דגן מלא.**
> מוצרים עם זרעים כרכיב שניה עד שלישי ברשימה לאחר קמח מלא — שונים ממוצרים שבהם הזרעים מופיעים על גבי קמח לבן כרכיב ראשון.

---

### BreadWellnessMap

**Purpose:** Map the wellness/premium segment across fermentation authenticity and grain verification.

**X axis:** אימות דגן מלא — מ"לא אומת" (שמאל) ל"קמח מלא מאומת ראשון" (ימין)
**Y axis:** אות תסיסה — מ"שמרים תעשייתיים בלבד / שם ללא אימות" (תחתית) ל"מחמצת מאומתת לפני שמרים" (עליון)

**Clusters (4):**

| Cluster | Label | Position | Key Products |
|---------|-------|----------|--------------|
| A | תסיסה אמיתית + דגן מלא | Top-right | לחם שיפון קל 75B, לחם אקסקלוסיבי שיפון מלא 74B, לחם הארץ שיפון אגוזים 71B |
| B | דגן מלא, ללא תסיסה | Top-left | קרקר כוסמין מלא ושומשום 82A, קרקר כוסמין אורגני 78B, לחם שיפון 100% 70B |
| C | שם מחמצת / שמרים עיקריים | Bottom-right / middle | לחם מחמצת שיפון 74B (mismatch), 12 additional mismatch products |
| D | לא זמין לניתוח | Gray scatter | ~46% of shelf |

**Important annotation:**
- Cluster C sits close to Cluster A in score — annotate this explicitly on the map: "ציון גבוה לא תמיד אומר תסיסה מאומתת"
- The paradox: לחם מחמצת שיפון (74/B, mismatch) appears close to לחם שיפון קל (75/B, verified) on score, but far apart on the fermentation axis
- This is the article's key tension point — the map should make this visible

**Visual specs:**
- Same structure as BreadEverydayMap (dot per product, cluster zones, tooltip on hover)
- Add one annotation line: from Cluster A (verified) to Cluster C (mismatch), showing score proximity despite axis distance
- No animation
- Mobile: cluster legend + top 3 per cluster

---

### ThreeGapBreakdown

**Purpose:** This replaces the generic "What's On The Shelf" section for Article 2. Instead of five dimensions, this article has three named gaps that explain most of the wellness segment's score variance.

**Structure:** Three panels. Each panel = one gap. Panel has: gap name, what the gap looks like in the data, how many products, what it means for score.

---

**Gap 1: פער המחמצת (The Fermentation Gap)**

```
מה זה: מוצר שמציג "מחמצת" בשמו, אך שמרים תעשייתיים מופיעים לפני המחמצת ברשימת הרכיבים.
כמה מוצרים: 13 מתוך 29 שטענו לתסיסה.
מה אפשר לדעת: לא ניתן לאמת שמחמצת היא המתפיח הדומיננטי.
מה לא ניתן לדעת: האם תהליך התסיסה בפועל שונה. רשימת הרכיבים לא מפרטת את משך התסיסה.
```

*Product evidence (inline, not cards):*
- לחם מחמצת שיפון — score 74/B — fermentation_real=false — "שמרים תעשייתיים לפני מחמצת"
- לחם מחמצת צרפתי פרוס — mismatch — "שמרים תעשייתיים עיקריים"
- לחם מחמצת מכוסמין — mismatch + refined flour claim — "שמרים עיקריים + בסיס לא מאומת כמלא"

---

**Gap 2: פער הכוסמין (The Spelt Gap)**

```
מה זה: ההבדל בין "כוסמין" (ללא קוואלפייר "מלא") ל-"כוסמין מלא" ברשימת הרכיבים.
כמה מוצרים: כמה מוצרים מציינים כוסמין ללא "מלא" — לא ניתן לאמת אם הגרעין מלא.
מה אפשר לדעת: קרקר כוסמין מלא ושומשום (82/A) — "כוסמין מלא" מצוין מפורשות ברשימה.
מה לא ניתן לדעת: מוצרים עם "כוסמין" בלבד — לא ניתן לאמת את רמת הדגן.
```

*Product evidence (inline):*
- קרקר כוסמין מלא ושומשום — 82/A — "כוסמין מלא" ברשימה — ציון גבוה ביותר בקטגוריה
- קרקר כוסמין אורגני — 78/B — "כוסמין מלא" ברשימה
- מוצר עם "כוסמין" ללא "מלא" — ברי אינה מאמתת — ציון מוגבל

---

**Gap 3: פער הסיבים (The Fiber Gap)**

```
מה זה: מוצר שמציג ערך סיבים גבוה בלוח התזונה, אך הסיבים מגיעים ממקורות מוספים (אינולין, שורש עולש, פסיליום), לא ממטריצת הדגן.
כמה מוצרים: 4 מוצרים עם אימות סיבים מוספים. מוצרים נוספים עם מקור לא ברור.
מה אפשר לדעת: לחמניות לס קיטו — 17.4g סיבים, מקור מוסף. לחמניות פשתן טרי — 15.7g סיבים, מקור מוסף.
מה לא ניתן לדעת: ההשפעה הפיזיולוגית של הבדל המקורות — זה מחוץ לתחום הניתוח.
```

*Product evidence (inline):*
- לחמניות לס קיטו — 17.4g — מוסף — "לא נוקד"
- לחמניות פשתן טרי — 15.7g — מוסף — "לא נוקד"  
- כוסמין מלא 100% — 11.0g — מוסף — ציון מוגבל
- לחם שיפון קל — 12.4g — מטריצת הדגן — 75/B

---

**Visual specs for ThreeGapBreakdown:**
- Three panels in sequence, not tabs, not accordion
- Each panel: large gap name, stats, two-column evidence section (left: mismatch example, right: aligned example)
- Evidence is text + score badge only — no product photography
- Do NOT title this section "Where Premium Brands Fail" or any activist framing

---

### ProductComparisonMatrix — Article 2

Three pairs. More than Article 1 because this segment has more meaningful tension.

---

**Pair 1: "תסיסה אמיתית לא תמיד על האריזה"**

| מוצר | ציון | דרגה | מחמצת בשם? | תסיסה ברשימה? |
|------|------|------|------------|----------------|
| לחם שיפון קל | 75 | B | לא | כן — מחמצת לפני שמרים |
| לחם מחמצת שיפון | 74 | B | כן | לא ניתן לאמת — שמרים לפני מחמצת |

**Explanation:**
> "שני לחמי שיפון, ציון כמעט זהה. אבל: לחם שיפון קל לא כולל 'מחמצת' בשמו — ומחמצת מצוינת ברשימת הרכיבים לפני השמרים. לחם מחמצת שיפון כולל 'מחמצת' בשמו — אך שמרים תעשייתיים מופיעים ראשון ברשימה. הציון הוא B בשני המקרים. ההבדל הוא ביחס בין שם המוצר לרשימת הרכיבים."

**Tension:** Same score tier, opposite fermentation alignment.

---

**Pair 2: "זרעים בתוך הבסיס ומחוצה לו"**

| מוצר | ציון | דרגה | בסיס | זרעים |
|------|------|------|------|-------|
| קרקר כוסמין מלא ושומשום | 82 | A | קמח כוסמין מלא | שומשום בתוך מטריצת הדגן המלא |
| קרקר פריך בסגנון שוודי | 72 | B | קמח חיטה לבן | זרעים על גבי בסיס מזוקק |

**Explanation:**
> "שני קרקרים עם זרעים. שניהם מציגים ערכי סיבים גבוהים: 10.0g ו-8.3g בהתאמה. הפרש הציון — 10 נקודות — נובע מהבסיס, לא מהזרעים. קרקר כוסמין מלא: בסיס כוסמין מלא, זרעי השומשום הם תוספת לבסיס שלם. קרקר שוודי: בסיס קמח לבן, הזרעים מופיעים אחריו. הבסיס הוא שמפריד."

---

**Pair 3: "מלא ב-100% — מה אפשר לאמת"**

| מוצר | ציון | דרגה | סיבים | מקור | שם מול רשימה |
|------|------|------|-------|------|--------------|
| קרקר כוסמין מלא ושומשום | 82 | A | 10.0g | מטריצת הדגן | "מלא" מצוין ברשימה |
| כוסמין מלא 100% | — | — | 11.0g | מוסף (⚠) | "מלא 100%" בשם — סיבים מאינולין |

**Explanation:**
> "שני מוצרים עם 'כוסמין מלא' בשמם. ערכי הסיבים דומים. אבל: בקרקר כוסמין מלא, הסיבים מגיעים מקמח כוסמין מלא כרכיב ראשון. ב-כוסמין מלא 100%, הניתוח מצביע על סיבים ממקורות מוספים. הציון משקף את ההבדל הזה."

**Note:** כוסמין מלא 100% may not have a displayable score — show "—" if displayable=false, not a number.

---

### SynthesisParagraph — Article 2

**One editorial paragraph (150–200 words). Finding-first. No recommendation.**

> "מה שמפריד את המוצרים בקטגוריה הזו הוא לא הצגת המוצר — זה מה שמופיע ראשון ברשימת הרכיבים. מוצרים שמציינים 'מחמצת' בשמם ומופיעים עם שמרים תעשייתיים ראשונים — קיבלו ציון B. מוצרים שלא מזכירים מחמצת בשמם אך כוללים אותה לפני השמרים — גם קיבלו ציון B. ההבדל ביניהם הוא ביחס בין שם המוצר להרכבו, לא בציון."
>
> "הציון הגבוה ביותר בכל הנתונים שנסרקו הגיע לקרקר — 82/A. אף לחם לא הגיע לדרגה A. שני הקרקרים המובילים (82/A ו-78/B) עשויים מקמח כוסמין מלא ומציינים 'מלא' ברשימת הרכיבים. המסקנה מהנתונים: מה שמצוין ברשימת הרכיבים — ולא מה שמצוין על האריזה — הוא מה שניתן לאמת."

---

### GlossaryAccordion — Article 2

Eight terms.

| מונח | הגדרה |
|------|--------|
| ציון ברי | ציון 0–100 המשקף עד כמה הרכב המוצר תואם את שמו והצגתו |
| דרגה | A–D, מבוסס על טווח הציון |
| תסיסה מאומתת | מחמצת מצוינת ברשימת הרכיבים לפני שמרים תעשייתיים |
| שמרים תעשייתיים עיקריים | שמרים מופיעים לפני מחמצת ברשימת הרכיבים |
| כוסמין מלא | כוסמין עם ציון "מלא" ברשימת הרכיבים — ברי מאמתת כשמצוין במפורש |
| סיבים מוספים | סיבים מאינולין, שורש עולש, או פסיליום — לא ממטריצת הדגן |
| סיבים מהדגן | סיבים המגיעים מהדגן המלא עצמו |
| ניתוח חלקי | ניתוח מבוסס על רשימת רכיבים בלבד — ללא לוח תזונה |

---

## 6. Product Clustering Logic — Article 2

| Cluster | Label | Logic |
|---------|-------|-------|
| A | תסיסה אמיתית + דגן מלא | fermentation_real=true AND whole_grain=true |
| B | דגן מלא, ללא תסיסה / ללא תביעת תסיסה | whole_grain=true AND fermentation_real=false AND fermentation_mismatch=false |
| C | שם מחמצת / שמרים עיקריים | fermentation_mismatch=true |
| D | לא זמין לניתוח | confidence_level = "insufficient" |

**Cluster C special annotation:**
Products in Cluster C that score 70+ (like לחם מחמצת שיפון 74/B) should be annotated: "ציון גבוה — תסיסה לא מאומתת." This is the article's main finding made visible on the map.

---

## 7. Score Driver System — Article 2

Same ScoreDriverTable component as Article 1, with these additional drivers:

| Driver | Direction | Evidence | UX Label |
|--------|-----------|----------|----------|
| מחמצת לפני שמרים ברשימה | ↑ | fermentation_real=true | "תסיסה מאומתת" |
| שמרים לפני מחמצת ברשימה | ↔ (neutral) | fermentation_mismatch=true | "שמרים עיקריים — מחמצת משנית" |
| "מלא" מצוין ליד שם הדגן | ↑ | whole_grain=true + explicit "מלא" qualifier | "כוסמין/שיפון מלא מאומת" |
| "מלא" לא מצוין | ↓ weak | no "מלא" qualifier in ingredient_architecture_summary | "לא ניתן לאמת דגן מלא" |
| זרעים בתוך מטריצת דגן מלא | ↑ | seed_halo=false AND whole_grain=true | "זרעים בבסיס מלא" |
| זרעים על גבי בסיס לבן | ↔ | seed_halo=true | "זרעים על בסיס מזוקק" |

---

## 8. Comparison Logic — Article 2

**Pair 1: לחם שיפון קל vs. לחם מחמצת שיפון**
- Why paired: same grain type (rye, whole grain), nearly same score (75 vs. 74), opposite fermentation signal
- Tension: the product claiming sourdough has industrial yeast first; the one not claiming it has real fermentation
- Score spread: 1 point — the irony is in the labeling, not the score

**Pair 2: קרקר כוסמין מלא ושומשום vs. קרקר פריך בסגנון שוודי**
- Why paired: both crackers, both with seeds, both high fiber
- Tension: grain base (whole grain vs. refined) drives the 10-point gap
- Score spread: 82 vs. 72

**Pair 3: קרקר כוסמין מלא ושומשום vs. כוסמין מלא 100%**
- Why paired: both claim "כוסמין מלא 100%", similar fiber values, different fiber source
- Tension: the name "מלא 100%" appears on both but the ingredient composition differs
- Note: show כוסמין מלא 100% without a score if not displayable — show "—"

---

## 9. Visual Hierarchy Rules — Article 2

**Dominant:** BreadWellnessMap (with the Cluster C annotation) and ThreeGapBreakdown panels
**Secondary:** InsightCardsGrid (5 cards) and SynthesisParagraph
**Minimal:** ScoreDriverTable, Glossary, Methodology

**The key visual innovation for Article 2:** The map annotation showing score proximity between Cluster A and Cluster C. This annotation should be a visible element — a line or bracket with label — not a tooltip. It carries the article's main tension.

**Tone distinction from Article 1:** Article 2 is sharper and more contrast-driven. The visual density should feel slightly higher than Article 1. More data, more nuance, same restraint.

---

## 10. Copywriting Rules — Article 2

**Approved:**
```
שמרים תעשייתיים מופיעים לפני מחמצת ברשימת הרכיבים.
לא ניתן לאמת שמחמצת היא המתפיח הדומיננטי.
הציון גבוה — אך מחמצת לא מאומתת כמנגנון ההתפחה העיקרי.
"כוסמין" ו-"כוסמין מלא" — ברי מאמתת רק כש-"מלא" מצוין במפורש.
```

**Forbidden:**
```
מחמצת מזויפת / שיווקית.
המוצר מטעה.
לחם מחמצת האמיתי הוא X.
הסיבים המוספים הם טריק.
כדאי לבחור את X במקום Y.
```

**Critical for this article:** The 13 fermentation mismatch products are documented as a pattern, not accused as fraudulent. The language is: "שמרים תעשייתיים מופיעים לפני מחמצת" — not "מחמצת מזויפת."

---

## 11. Data Requirements — Article 2

**Dataset fields required per product:**
```
name_he, score, grade, displayable, confidence_level, confidence_label_he,
fiber_g, fermentation_real, fermentation_mismatch, fiber_laundering,
seed_halo, whole_grain, ingredient_architecture_summary, short_summary_he
```

**Products that must appear in this article:**
- קרקר כוסמין מלא ושומשום (82/A) — in Pair 2, Pair 3, map Cluster B
- קרקר כוסמין אורגני (78/B) — in map Cluster B
- לחם שיפון קל (75/B) — in Pair 1, ThreeGapBreakdown
- לחם מחמצת שיפון (74/B, mismatch) — in Pair 1, map Cluster C
- קרקר פריך בסגנון שוודי (72/B, seed_halo) — in Pair 2
- לחמניות לס קיטו (17.4g fiber, matrix-added) — in ThreeGapBreakdown
- כוסמין מלא 100% (11.0g, matrix-added) — in Pair 3 and ThreeGapBreakdown
- All 13 fermentation mismatch products — named in ThreeGapBreakdown, displayed inline as a list

**13 fermentation mismatch products (for ThreeGapBreakdown inline list):**
```
לחם מחמצת צרפתי פרוס
לחם מחמצת צרפתי
לחם מחמצת אגוזים צימוקים
לחם מחמצת דגנים
לחם מחמצת זיתי קלמטה
לחם מחמצת אגוזים
לחם מחמצת שיפון+אגוזים
10 פיתות מחמצת
לחם מחמצת שיפון
לחם מחמצת מכוסמין
לחמניות מחמצת טבעית
+ 2 additional (לחם מחמצת צרפתי dup / לחם מחמצת שיפון dup)
```

Display inline as a compact list, not cards. One line per product. No scores displayed for products with insufficient/undisplayable data.

---

## 12. Cursor Build Notes — Article 2

**Priorities:**
1. BreadWellnessMap Cluster C annotation is the most critical visual element — it carries the article's main insight
2. ThreeGapBreakdown must be implemented as three distinct panels with inline product evidence — not as InsightCards
3. SynthesisParagraph is prose-only — no component wrapper needed, but must appear above Glossary

**Likely failure modes:**
- Labeling the fermentation mismatch products as "deceptive" or "fraudulent" — they are documented, not accused
- Showing score for undisplayable products (כוסמין מלא 100% etc.) — show "—" instead
- Treating the 13-product mismatch list as a leaderboard or "worst" list — it is a pattern, not a ranking
- Merging ThreeGapBreakdown with InsightCards — they are structurally different
- Removing the Cluster C annotation from the map — this is mandatory

**Must remain consistent with milk comparison:**
- ShelfStatBar format
- GlossaryAccordion structure  
- MethodologyNote position
- InsightCard format
- Article density

**Must differ from milk comparison:**
- Map has four clusters, not a spectrum gradient
- ThreeGapBreakdown is unique to this article (named gaps, not processing depth)
- The Cluster C annotation on the map is unique to this article
- Five InsightCards instead of three (more complex segment)
- Three comparison pairs instead of two

---
---

# SHARED COMPONENT LIBRARY

## Components used in both articles

### ScoreDriverTable
*(Specification above in Article 1. Use same component in Article 2 with Article 2's additional drivers.)*

### GlossaryAccordion
Six terms for Article 1. Eight terms for Article 2. Same component, different content arrays.

### ComparisonCTA
Same in both articles. Text differs. Link target differs.

### MethodologyNote
Same component. Same 5-sentence max. Different final framing sentence per article.

---

## Display Rules That Apply to Both Articles

**Score display rule:** Only show score when `displayable=true`. When `displayable=false`, show `—`.

**Confidence label:** Always display `confidence_label_he` on every product that appears in any component.

**Score format:** Always `[number] / [grade]` — e.g., `75 / B`. Never just the number. Never the grade alone.

**Insufficient products:** If `confidence_level = "insufficient"`, display `לא נוקד`, not `40/D`. The score=40 in the dataset is a technical floor, not a real score.

**No ranked lists:** Never present products in a "best to worst" ordered list format. The Comparison Matrix is not a ranking.

---

# GLOBAL CURSOR BUILD NOTES

1. **Build the two maps before the articles go live.** The maps are the anchor of each article. Articles without maps are structurally incomplete.

2. **The CompositionBreakdown and ThreeGapBreakdown are new components.** They do not exist in the existing system. They must be built fresh. They are not repurposed InsightCards or ProductCard wrappers.

3. **The ProductComparisonMatrix must be a table with prose.** Not a card duel. Not a side-by-side hero comparison. A clean data table with an explanation paragraph below it.

4. **Copy must follow the assertive writing framework.** Every finding sentence should name a product, a score, or an ingredient position. No generic observations. No apologetic framing. One footer disclaimer per article.

5. **The articles are reference documents, not landing pages.** Dense, readable, investigative. Not airy. Not promotional. No hero animations.

6. **The 46% unscored finding is editorial context, not a failure disclosure.** Surface it prominently (ShelfStatBar, Card 2 in Article 1) and treat it as a shelf finding, not a system apology.
