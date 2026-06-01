# Bari Snack Bar Editorial — Implementation Handoff v1
**Date:** 2026-05-27
**Architecture reference:** milk comparison + stabilized bread (bread_blog_v3.md + bread_blog_refinement_v1.md)
**Dataset:** run_snack_bars_synthesis_001 — 53 products, Yohananof, May 2026
**Governance reference:** bari_governance_v1.md + assertive_writing_v1.md + editorial_intelligence_v1.md

---

## IMPORTANT — DATA STATUS BEFORE IMPLEMENTATION

Before Cursor begins implementation, confirm the following:

**Current data status (run_snack_bars_001 + synthesis_001):**
- ✓ 53 products scored
- ✓ NOVA proxy, cap/floor system, synthesis layer applied
- ✓ Two routing bugs fixed (beverage misroute, dairy_protein misroute)
- ✗ `ingredients_raw` field is EMPTY in BSIP1 source — fiber laundering and full additive detection are blocked
- ✗ `granola_bar` archetype not yet defined — Nature Valley Crunchy routing is borderline (cereal vs. snack_bar_granola)
- ✗ `whole_food_fat + NOVA4` contradiction not yet flagged at routing level

**What the re-run should do before Cursor implementation:**
1. Run updated BSIP2 on snack_bars corpus once BSIP1 `ingredients_raw` is populated
2. Stabilize granola routing (add `granola_bar` archetype or strengthen snack form signals)
3. Apply NOVA-awareness gate to `whole_food_fat` classification (NOVA4 products should not route here)

**Editorial architecture in this document is final and ready.** Cursor implementation should wait for re-run data.

---

## What This System Replaces

The previous snack-bar work predates:
- The updated editorial governance system
- The new score explainability standards
- The stabilized milk/bread investigation format
- The consumer translation layer
- The assertive-but-restrained writing standard

Do not reference the prior snack-bar editorial work. This document is the starting point.

---

## What Changed From Bread Architecture

| Bread | Snack Bars |
|-------|-----------|
| CompositionBreakdown (5 dimensions: flour, fiber, list length, transparency, whole-grain claim) | BarCompositionBreakdown (5 dimensions: base, sweetener architecture, processing depth, additive load, name alignment) |
| ThreeGapBreakdown (fermentation / spelt / fiber) | ThreeMisalignmentBreakdown (protein / "natural" / fitness positioning) |
| BreadEverydayMap + BreadWellnessMap | SnackBarShelfMap + SnackBarWellnessMap |
| Fermentation as key tension | Processing depth + additive architecture as key tension |
| No A grade for bread, only cracker | No A grade at all. Only B: a date bar (70/B) |

---

## Dataset Constants (Use These Exactly)

```
source: יוחננוף
snapshot_date: מאי 2026
total_scraped: 53
scored: 48
insufficient_data: 5
score_range: 13–70
score_mean: ~35
highest_score: 70/B (חטיף תמרים במילוי חמאת שקדים)
no_grade_A: true
grade_B_count: 1
nova4_pct: 58.5% (31 of 53 products)
nova3_pct: 28.3% (15 of 53 products)
nova2_pct: 13.2% (7 of 53 products)
capped_products: 79% (42 of 53)
```

---

## Grade Distribution

| Grade | Count | % |
|-------|-------|---|
| B | 1 | 1.9% |
| C | 16 | 30.2% |
| D | 12 | 22.6% |
| E | 24 | 45.3% |
| Insufficient | 5 | 9.4% |

---

## Shelf Segments (Both Articles)

Six real shelf types Cursor should recognize throughout both articles:

1. **חטיפי תמרים** — date bars, nut-date bars (4–6 ingredients, NOVA2)
2. **חטיפי גרנולה ושיבולת שועל** — oat/granola bars (Nature Valley Crunchy, Fitness oat)
3. **חטיפי דגנים מצופי שוקולד** — chocolate-coated cereal bars (Corny, Shogi, Energy, Fitness grain)
4. **חטיפי פרוטאין** — protein-positioned bars (Nature Valley Protein, Fitness variants)
5. **חטיפי "סלים" / רב-דגן** — slim/multi-grain positioned bars (Slim Delice variants)
6. **חטיפי אגוזים** — nut bars (Rafaels, Free)

---

## Bar-Native Decomposition — 5 Dimensions

This is the analytical backbone of both articles. These five dimensions separated the products in the data. They apply category-wide.

---

### Dimension 1 — מקור הבסיס (Structural Base)

**What it is:** What the bar is actually made of at its core — before coatings, flavors, or additives.

**Three structural types:**
- **בסיס שלם:** תמרים, אגוזים, שיבולת שועל שלמה — recognizable whole foods as the first ingredient. NOVA2 territory.
- **בסיס מעובד:** סירופ גלוקוז, קמח חיטה, דגנים מנופחים — refined cereal base, syrups as first ingredients. NOVA3–4 territory.
- **בסיס מהונדס:** emulsifiers + protein isolates + refined grains + coating systems — multiple layers of industrial reconstruction. NOVA4 + additive load.

**Score effect in this dataset:**
- Whole food base (NOVA2): clustered at 55–70/B–C
- Processed cereal base (NOVA3): clustered at 50–60/C
- Engineered base (NOVA4): clustered at 13–48/D–E

**Specific example:**
- חטיף תמרים במילוי חמאת שקדים: תמרים, חמאת שקדים, שקדים, קקאו — 4 ingredients, whole food base — 70/B
- חטיפי דגנים פיטנס קלאסי: קמח חיטה, סירופ גלוקוז, שמן, חלבון חלב, מייצבים, משחזים — NOVA4 — 46/D

---

### Dimension 2 — ארכיטקטורת הסוכר (Sweetener Architecture)

**What it is:** How sweetness is built in the product — one transparent source or multiple engineered sweetener sources.

**Three patterns:**
- **מקור אחד:** תמרים בלבד, דבש בלבד — transparent, single-source sweetness.
- **סוכר מוסף בינוני:** סוכר + מולסות, or honey + sugar — moderate.
- **ריבוי מקורות:** glucose syrup + cane sugar + invert sugar + flavor enhancers — multiple added sweeteners stacked.

**Score effect:**
- Multi-source sweetener architecture → sugar red label → cap to 55 maximum.
- Single-source natural sweetener: no cap from sweetener axis.

**Specific example:**
- חטיפי דגנים Energy אגוזים ושוקולד (18/E): contains סירופ גלוקוז, סוכר, סירופ סוכר מולסות — three sweetener sources.
- חטיף תמרים במילוי חמאת שקדים (70/B): sweetness from תמרים only — no added sweeteners.

**Consumer translation:** "תמרים ראשונים ברשימה" is not the same as "ממותק בתמרים" — the position in the list tells you how much.

---

### Dimension 3 — עומק העיבוד (Processing Depth)

**What it is:** How far the product has been reconstructed from its original ingredients. Approximated by NOVA proxy.

**Four levels:**
- **NOVA2 — מינימלי:** whole food ingredients, simple combination, few steps. 7 products in dataset.
- **NOVA3 — מעובד:** identifiable ingredients, some additives, industrial but not reconstructed. 15 products.
- **NOVA4 — אולטרה-מעובד:** synthetic additives, emulsifiers, flavor systems, engineered texture. 31 products (58.5% of shelf).

**Score effect:** NOVA4 triggers a hard cap. In this dataset, no NOVA4 product exceeded 48/D. All E-grade products are NOVA4.

**Specific pattern:** Nature Valley Protein (47/D) is NOVA4. The date bar (70/B) is NOVA2. The processing tier is the single strongest predictor of score tier.

---

### Dimension 4 — עומס התוספות (Additive Load)

**What it is:** How many functional additives (emulsifiers, stabilizers, flavor enhancers, coating agents) appear in the ingredient list.

**Three levels:**
- **0–2 תוספות:** minimal (date bars, simple nut bars)
- **3–4 תוספות:** moderate (Nature Valley Crunchy, Slim Delice)
- **5+ תוספות:** high (Fitness grain bars, Corny, Shogi) → triggers additional cap

**Score effect:** 5+ additives triggered `ADDITIVE_MARKERS_5_PLUS` cap (−10 from max). 3–5 triggered `ADDITIVE_MARKERS_3_PLUS`. Products with highest additive counts also received "hyper-palatable reconstruction" flag from synthesis layer (−3 additional).

**Specific examples (hyper-palatable synthesis flag applied):**
- חטיפי דגנים פיטנס קרם ועוגיות (22/E): sweetener + ≥3 additives + non-isolate protein → −3
- חטיף דגנים שוקו וניל נסטלה (25/E): same pattern → −3

---

### Dimension 5 — יחסיות ההצגה (Name-Composition Alignment)

**What it is:** Whether the product name and primary positioning matches what's in the ingredient list.

**Four alignment states:**
- **מאוזן:** "חטיף תמרים" + dates-first ingredient list. Aligned.
- **ניטרלי:** "קראנצ'י שיבולת שועל" + oats-first. Reasonably aligned.
- **פער:** "פיטנס" / "אנרג'י" on NOVA4 product. The name implies composition performance that the ingredient list doesn't deliver.
- **פער גדול:** "פרוטאין" on NOVA4 product with engineered protein system. Protein positioning doesn't reward score when processing depth is NOVA4.

**Score effect:** Bari's score reflects the ingredient list, not the product name. Products with the largest name-composition gaps show the widest divergence between consumer expectation and score.

**Specific examples:**
- פיטנס קלאסי (46/D): "Fitness" brand — 15 ingredients, NOVA4, multiple additives
- חטיף אנרג'י אגוזים ושוקולד (18/E): "Energy" brand — one of the lowest scores in the dataset

---
---

# ARTICLE 1 — "החטיפים שרוב ישראל קונה"

**URL:** `/snack-bars/everyday`
**Hebrew title:** החטיפים שרוב ישראל קונה

---

## 1. Page Purpose

This article investigates the mainstream snack bar shelf — cereal bars, granola bars, chocolate-coated grain bars, and "fitness"-branded products that form the daily snack basket for most Israeli households. The investigation focuses on why products with similar packaging, similar prices, and similar shelf positioning diverged dramatically in score. The central finding: processing depth was the dominant separator — not the product name. Nearly 60% of the shelf is NOVA4. The only products to escape D–E territory did so through structural base and sweetener architecture, not through branding.

---

## 2. Editorial Spine

> "מרבית החטיפים שנסרקו קיבלו ציון E. הגורם המרכזי שהפריד — לא השם על האריזה, אלא עומק העיבוד ואיך הסוכר מגיע."

---

## 3. Full Page Structure

```
1.  Hero + ShelfStatBar
2.  Intro paragraph (130–160 words)
3.  Key Findings (4 InsightCards)
4.  Shelf Map — SnackBarShelfMap
5.  What's On The Shelf — BarCompositionBreakdown (5 dimensions)
6.  Main Comparisons — ProductComparisonMatrix (2 pairs)
7.  Reader Takeaways (3 bullets)
8.  Glossary — GlossaryAccordion
9.  Full Comparison CTA
10. Methodology Note
```

---

## 4. Component Mapping

| Section | Component | Purpose |
|---------|-----------|---------|
| Hero + ShelfStatBar | ShelfStatBar | Shelf scope, grade distribution, key numbers |
| Key Findings | InsightCardsGrid (4 cards) | Four shelf findings that frame the investigation |
| Shelf Map | SnackBarShelfMap | Visualize where products landed on two observable axes |
| What's On The Shelf | BarCompositionBreakdown | Five bar-native dimensions, how each affected score |
| Main Comparisons | ProductComparisonMatrix | Two high-contrast pairs with causal explanation |
| Takeaways | TakeawayList | Three factual synthesis bullets, no advice |
| Glossary | GlossaryAccordion | Seven terms |
| CTA | ComparisonCTA | Link to full table |
| Methodology | MethodologyNote | 5 sentences max |

---

## 5. Component Specifications

---

### ShelfStatBar — Article 1

**Inputs:**
```json
{
  "scraped": 53,
  "scored": 48,
  "not_scored_pct": 9,
  "nova4_pct": 59,
  "grade_e_count": 24,
  "retailer": "יוחננוף",
  "date": "מאי 2026"
}
```

**Display:**
```
53 נסרקו  |  48 קיבלו ציון  |  59% מהמוצרים — NOVA4  |  24 מוצרים בדרגה E  |  יוחננוף · מאי 2026
```

Single line. No color. No icons. Plain text.

---

### InsightCardsGrid — Article 1

Four cards. Each: type tag (Finding / Gap / Pattern / Ambiguity), bold finding sentence, 1–2 sentence explanation.

**Card 1 — Finding:**
> **רק מוצר אחד מכל 53 הגיע לדרגה B — חטיף תמרים עם 4 רכיבים.**
> כל יתר המוצרים קיבלו C, D, או E. הדרגה הגבוהה ביותר הלכה למוצר הפשוט ביותר על המדף.

**Card 2 — Pattern:**
> **58% מהמוצרים הם NOVA4 — מה שאומר שפחות מ-60 הנקודות הם תקרה.**
> כל מוצר NOVA4 בנתונים אלה קיבל D או E. לא נמצא מוצר NOVA4 שהגיע ל-C.

**Card 3 — Finding:**
> **"פיטנס" על האריזה לא ניבה ציון — גם לא "אנרג'י".**
> מוצרים עם "פיטנס" בשם קיבלו בין 17 ל-46. מוצרים עם "אנרג'י" בשם — בין 18 ל-31. שניהם בטווח D–E.

**Card 4 — Gap:**
> **45% מהציונים הם E — הקצה התחתון של הקטגוריה.**
> הנתח הגדול ביותר של חטיפי הדגנים המצופים נמצא בטווח הנמוך ביותר. שוגי, קורני, ורוב חטיפי פיטנס דגנים — כולם E.

---

### SnackBarShelfMap

**Purpose:** Show where everyday snack bar products positioned on two observable axes.

**X axis:** עומק עיבוד — from "עיבוד מינימלי / שלם" (left) to "NOVA4 — אולטרה-מעובד" (right)
**Y axis:** ארכיטקטורת סוכר — from "מקור טבעי יחיד" (top) to "מרובה סוכרים מוספים" (bottom)

**Clusters (4):**

| Cluster | Label | Position | Key Products |
|---------|-------|----------|--------------|
| A | בסיס שלם, סוכר מינימלי | Top-left | חטיף תמרים במילוי חמאת שקדים (70/B), חטיף תמרים בציפוי שוקולד (56/C) |
| B | עיבוד בינוני, סוכר מתון | Middle | סלים דליס (51–62/C), Nature Valley Crunchy (51–53/C) |
| C | NOVA4, ריבוי סוכר | Bottom-right | קורני, שוגי, פיטנס דגנים (13–46/D–E) |
| D | NOVA4, ציון D | Middle-right | פיטנס קלאסי (46/D), פיטנס שקדים ודבש (45/D) |

**Outlier to annotate:**
- חטיף תמרים במילוי חמאת שקדים — top-left, highest score (70/B), 4 ingredients. Label on map: "4 רכיבים — 70/B"
- שחור ולבן קורני שוקולד — bottom-right, lowest score (13/E). Label: "13/E — הציון הנמוך ביותר"

**Map title:** "עומק עיבוד וסוכר — איפה עומד כל חטיף"

**Caption:** "כל נקודה = מוצר אחד. המיקום מבוסס על מבנה הרכיבים — לא על הצגת המוצר."

**Visual specs:**
- Same dot system as bread maps: one dot = one product
- Color: blue = NOVA2, gray-blue = NOVA3, gray = NOVA4, light gray = insufficient data
- Tooltip on hover: name + score + one-line reason
- No animation. No score encoding in dot size.
- Mobile: cluster legend + top 3 per cluster as list

**Do NOT:**
- Use rainbow colors
- Show grade labels as victory badges
- Encode NOVA level as dot size
- Add arrows suggesting which direction is "better"

---

### BarCompositionBreakdown — Article 1

**Purpose:** Explain the five bar-native dimensions that separated products in this dataset. This is the investigation's analytical core — the section that answers "what actually moved the score."

**Structure:** Five rows. Same format as CompositionBreakdown in bread: dimension name + definition + what it looks like + score effect + specific example.

---

**1. מקור הבסיס — Structural Base**

מה שמרכיב את הבסיס הוא הגורם הראשון שצריך לבדוק.

*מה זה אומר:* הרכיב הראשון ברשימה הוא הכי נפוח. תמרים ראשון — הבסיס הוא תמרים. קמח חיטה ראשון — הבסיס הוא קמח מעובד. סירופ גלוקוז ראשון — הבסיס הוא סוכר מתועש.

*אפקט על הציון:* בנתונים אלה — מוצרי NOVA2 עם בסיס שלם: 55–70. מוצרי NOVA3 עם בסיס מעובד: 50–60. מוצרי NOVA4 עם בסיס מהונדס: 13–48.

*דוגמה:* חטיף תמרים במילוי חמאת שקדים — תמרים ראשון — 70/B. חטיפי דגנים פיטנס קלאסי — קמח חיטה + סירופ ראשונים — 46/D.

---

**2. ארכיטקטורת הסוכר — Sweetener Architecture**

ערך הסוכר בלוח התזונה לא מספר את הסיפור. מה שמספר — כמה מקורות סוכר מוספים מופיעים ברשימת הרכיבים.

*מה זה אומר:* "סוכר" (אחד) שונה מ"סוכר + סירופ גלוקוז + מולסות" (שלושה מקורות). כשמרובה מקורות סוכר מוסף מופיעים, זה גם משפיע על הציון מבחינת עצמת העיבוד.

*אפקט על הציון:* מוצרים עם סוכר אדום ישראלי (>25g/100g) קיבלו cap=55. מוצרים עם מרובה מקורות סוכר קיבלו cap נוסף. שילוב של NOVA4 + מרובה סוכרים = מגיע ל-E בעקביות.

*דוגמה:* חטיף אנרג'י אגוזים ושוקולד (18/E): סירופ גלוקוז + סוכר + מולסות — שלושה מקורות. חטיף תמרים (70/B): אין סוכר מוסף — תמרים הוא המקור.

---

**3. עומק העיבוד — Processing Depth**

NOVA4 הוא לא רק תווית — הוא כיסוי של סוג עיבוד שמתורגם ישירות לתקרת ציון.

*מה זה אומר:* NOVA4 הופיע ב-31 מתוך 53 מוצרים. כל מוצר NOVA4 קיבל cap של 68 לכל היותר — ובשילוב עם גורמים נוספים, רוב הגיעו ל-D או E.

*אפקט על הציון:* NOVA2 (7 מוצרים): 42–70. NOVA3 (15 מוצרים): 28–62. NOVA4 (31 מוצרים): 13–48.

*דוגמה:* Nature Valley Protein בוטנים קרמל (47/D) — NOVA4. חטיף תמרים (70/B) — NOVA2. הפרש: 23 נקודות. השינוי העיקרי: עומק העיבוד.

---

**4. עומס התוספות — Additive Load**

מספר התוספות הפונקציונליות ברשימה הוא אינדיקטור לרמת ההנדסה של המוצר.

*מה זה אומר:* מייצב, מחמיר, חומר ציפוי, משפר טעם — כל אחד מאלה הוא תוספת פונקציונלית. מוצרים עם 5+ מסוג זה ברשימה קיבלו cap נוסף.

*אפקט על הציון:* 5+ תוספות → cap של 60. מוצרים עם 5+ תוספות שגם הפגינו "הנדסת היפר-פאלטביליות" קיבלו −3 נוספות מ-synthesis layer.

*דוגמה:* פיטנס קרם ועוגיות (22/E) + נסטלה שוקו וניל (25/E): שניהם קיבלו "hyper-palatable reconstruction" flag. שניהם קיבלו −3 מהסינתזה.

---

**5. יחסיות ההצגה — Name-Composition Alignment**

השם על האריזה לא קובע את הציון.

*מה זה אומר:* ברי מבסס את הציון על מה שמופיע ברשימת הרכיבים — לא על מה שמוצג על האריזה. "פיטנס" ו"אנרג'י" ו"פרוטאין" על מוצרי NOVA4 לא תרמו לציון.

*אפקט על הציון:* המוצרים עם הפער הגדול ביותר בין שם לרשימה הם בדיוק אלה שציפית להם לציון גבוה יותר. פיטנס קלאסי (46/D). אנרג'י (18/E). נייצ'ר וואלי (38–47/D).

*דוגמה:* חטיף תמרים — "תמרים" מוצג כרכיב ראשון. חטיף אנרג'י — "אנרג'י" הוא שם. הציון שיקף את הרשימה, לא את השם.

---

**Visual specs for BarCompositionBreakdown:**
- Five rows, alternating background
- Dimension name: bold and prominent
- No icons
- Product examples inline with score
- Do NOT use cards — inline text only
- Mobile: single column, rows stack

---

### ProductComparisonMatrix — Article 1

Two pairs. Each pair: title, comparison table, one-paragraph explanation.

---

**Pair 1: "הפיטנס על האריזה לא אמר מה יש בפנים"**

Comparison logic: Both are chocolate-adjacent snack bars. Both carry health-adjacent framing. Different structural base, different NOVA tier.

| מוצר | ציון | דרגה | NOVA | בסיס | רכיבים (משוער) |
|------|------|------|------|------|----------------|
| חטיף תמרים בציפוי שוקולד 100% קקאו | 56 | C | 2 | תמרים | ~4 |
| חטיפי דגנים פיטנס קלאסי | 46 | D | 4 | קמח חיטה + סירופ | ~15 |

**Explanation text:**
> "שני חטיפים בציפוי שוקולד. שניהם על אותו מדף. הפרש ציון: 10 נקודות. חטיף התמרים: בסיס תמרים, NOVA2, ציפוי שוקולד 100% קקאו. פיטנס קלאסי: בסיס קמח חיטה ו-סירופ גלוקוז, NOVA4, מרובה תוספות. 'פיטנס' על האריזה — הציון שיקף את רשימת הרכיבים."

**Tension:** "Fitness" branding on lower-scoring product vs. unnamed date bar on higher-scoring product.

---

**Pair 2: "שיבולת שועל בשני קצות המדף"**

Comparison logic: Both contain oats. Both appear in the "healthy snack" zone of the shelf. Score gap: 36 points.

| מוצר | ציון | דרגה | NOVA | בסיס | הסיבה לפרש |
|------|------|------|------|------|------------|
| קראנצ'י שיבולת שועל עם דבש | 53 | C | 3 | שיבולת שועל שלמה | עיבוד בינוני |
| פיטנס בר גרנולה שוקולד מריר | 17 | E | 4 | קמח + סירופ | NOVA4 + מרובה תוספות |

**Explanation text:**
> "שניהם עם שיבולת שועל. שניהם קראנצ'י/גרנולה. הפרש ציון: 36 נקודות. קראנצ'י של Nature Valley: שיבולת שועל שלמה כרכיב ראשון, NOVA3, מעט תוספות. פיטנס בר גרנולה שוקולד מריר: בסיס קמח ו-סירופ, NOVA4, תוספות מרובות. אותה מילה — 'גרנולה' — על שני מוצרים שונים לחלוטין בהרכב."

---

### TakeawayList — Article 1

Three bullets. Synthesis, not advice.

```
• הגורם המרכזי שהפריד בין המוצרים — עומק העיבוד (NOVA), לא השם על האריזה.
• כל מוצר NOVA4 בנתונים אלה קיבל D או E. אף NOVA4 לא הגיע ל-C.
• "פיטנס", "אנרג'י", ו"גרנולה" הופיעו על מוצרים בטווח 17–53 — פרש של 36 נקודות בין מוצרים עם אותו מיצוב.
```

**Do NOT:**
- Start bullets with "כדאי לבחור" or "מומלץ"
- Add a fourth bullet that summarizes the others
- Add color encoding to the bullets

---

### GlossaryAccordion — Article 1

Seven terms. Collapsed by default.

| מונח | הגדרה |
|------|--------|
| ציון ברי | ציון 0–100 המשקף עד כמה הרכב המוצר תואם את שמו והצגתו |
| דרגה | A–E, מבוסס על טווח הציון |
| NOVA | מערכת סיווג שמקרבת את מידת העיבוד התעשייתי של מוצר — 1 (מינימלי) עד 4 (אולטרה-מעובד) |
| NOVA4 | מוצר אולטרה-מעובד — מכיל חומרי ציפוי, מייצבים, משפרי טעם, וחומרים שלא ניתן להכין בבית |
| בסיס שלם | כשהרכיב הראשון הוא מזון שלם (תמרים, שיבולת שועל שלמה, אגוזים) |
| ארכיטקטורת סוכר | כיצד מגיע הסוכר — ממקור יחיד (תמרים) או ממרובה מקורות מוספים (סירופ, סוכר, מולסות) |
| לא נוקד | מוצר שנתוני הרכיבים שלו לא היו מלאים — ברי לא חישבה ציון |

---

### ComparisonCTA — Article 1

```
→ לטבלת ההשוואה המלאה: כל 53 המוצרים, סוננים לפי ציון
```

---

### MethodologyNote — Article 1

> "ניתחנו 53 חטיפי דגנים, גרנולה, ותמרים ממדף יוחננוף, מאי 2026. 48 מוצרים קיבלו ציון — 5 לא קיבלו בגלל נתונים חלקיים. הניתוח מבוסס על מבנה הרכיבים, פרוקסי NOVA, ומנגנוני cap/floor מתועדים. הניתוח מבוסס על נתוני מדף יוחננוף בלבד — לא על סקר שוק ישראלי מלא. ציוני ברי אינם מהווים המלצה תזונאית."

---

## 6. Product Clustering Logic — Article 1

| Cluster | Label | Logic | Products |
|---------|-------|-------|---------|
| A | בסיס שלם, סוכר מינימלי | nova_proxy ≤ 2 AND no added sugar red label | תמרים + אגוזים + קקאו bars (NOVA2) |
| B | עיבוד בינוני, ציון C | nova_proxy = 3 AND grade = C | Slim Delice variants, Nature Valley Crunchy |
| C | NOVA4, ציון D | nova_proxy = 4 AND grade = D | Fitness grain bars, Nature Valley Protein, Chewy |
| D | NOVA4, ציון E | nova_proxy = 4 AND grade = E | Corny, Shogi, Energy, Fitness grain chocolate |

---

## 7. Score Driver System — Article 1

| מה שנראה בנתוני המוצר | השפעה על הציון | תווית UX |
|---|---|---|
| NOVA2 — עיבוד מינימלי | מגביר | "עיבוד מינימלי" |
| NOVA4 — אולטרה-מעובד | מגביל חזק — cap 68 | "אולטרה-מעובד" |
| בסיס שלם (תמרים / אגוזים / שיבולת שועל שלמה) | מגביר | "בסיס שלם" |
| בסיס קמח לבן + סירופ גלוקוז | מוריד | "בסיס מעובד" |
| סוכר אדום (>25g/100g) | cap 55 | "סוכר גבוה" |
| מרובה מקורות סוכר | מוריד | "ריבוי ממתיקים" |
| 5+ תוספות פונקציונליות | cap 60 | "הנדסת חטיף" |
| היפר-פאלטביליות (synthesis) | −3 | "הנדסת טעם מרוכב" |
| נתונים חלקיים | לא נוקד | "נתונים לא מלאים" |

No green/red color in this table. Text labels only.

---

## 8. Comparison Logic — Article 1

**Pair 1: חטיף תמרים בציפוי שוקולד קקאו vs. פיטנס קלאסי**
- Why paired: both chocolate-adjacent, both snack format, similar price range
- Tension: "Fitness" brand = lower score than unnamed date bar
- Score spread: 56 vs. 46 (10-point gap)
- Driver: NOVA tier (2 vs. 4), base structure (dates vs. refined flour + syrup)
- Never imply: Fitness brand is fraudulent or misleading — document the composition gap

**Pair 2: קראנצ'י שיבולת שועל ודבש vs. פיטנס בר גרנולה שוקולד מריר**
- Why paired: both oat-based, both "granola" adjacent
- Tension: same grain type signal, 36-point score gap
- Score spread: 53 vs. 17
- Driver: NOVA tier (3 vs. 4), additive count, processing depth
- Never imply: Nature Valley Crunchy is healthy — it scored C, not B or A

---

## 9. Visual Hierarchy Rules — Article 1

**Dominant:** SnackBarShelfMap and BarCompositionBreakdown — the two visual anchors
**Secondary:** InsightCardsGrid and ProductComparisonMatrix
**Minimal:** ShelfStatBar, TakeawayList, Glossary

**No dominant visual should be a product card.**
Products appear in tables and prose. Never isolated hero cards.

**Tone:** calm, investigative, matter-of-fact. Dense but readable. Reference document, not landing page.

---

## 10. Copywriting Rules — Article 1

**Approved:**
```
NOVA4 — 31 מתוך 53 מוצרים.
חטיף תמרים: 4 רכיבים, 70/B.
פיטנס קלאסי: NOVA4, קמח ו-סירופ ראשונים, 46/D.
כל מוצר NOVA4 בנתונים אלה קיבל D או E.
```

**Forbidden:**
```
הפיטנס מרמה.
קנה תמרים, לא פיטנס.
שוגי / קורני הם גרועים.
חטיפי הדגנים מסוכנים.
הציון הנמוך מוכיח שהמוצר לא בריא.
```

**One footer disclaimer only. Zero body disclaimers.**

---

## 11. Data Requirements — Article 1

**Dataset fields required per product:**
```
name_he, score, grade, displayable, confidence_level,
nova_proxy, structural_class, caps_applied,
short_summary_he, ingredient_architecture_summary
```

**Products that must appear in this article:**
- חטיף תמרים במילוי חמאת שקדים (70/B) — InsightCard 1, map anchor (Cluster A)
- חטיף תמרים בציפוי שוקולד 100% קקאו (56/C) — Pair 1
- חטיפי דגנים פיטנס קלאסי (46/D) — Pair 1
- קראנצ'י שיבולת שועל עם דבש (53/C) — Pair 2
- פיטנס בר גרנולה שוקולד מריר (17/E) — Pair 2
- שחור ולבן קורני שוקולד (13/E) — map annotated outlier (lowest score)
- Representative E-grade cluster products — for map Cluster D

**Insufficient data handling:**
- Products with confidence_level="insufficient": gray dots on map, "לא נוקד"
- Never show score from insufficient products
- Rafaels nut bars (insufficient data) appear as gray dots only

---

## 12. Cursor Build Notes — Article 1

**Priorities:**
1. SnackBarShelfMap — must be built before article goes live. Primary visual anchor.
2. BarCompositionBreakdown — new component, distinct from any card system
3. ProductComparisonMatrix — table + prose, NOT card duels

**Likely failure modes:**
- Using "better/worse" product card treatment — forbidden
- Showing score=50 for insufficient data products — show "לא נוקד"
- Color-coding "מגביר/מוריד" as green/red — text only
- Labeling NOVA4 as "dangerous" or "unhealthy" — describe, never moralize
- Treating the 59% NOVA4 stat as a system failure — it's a shelf finding, not an apology

**Must remain consistent with bread/milk:**
- ShelfStatBar format
- GlossaryAccordion structure
- MethodologyNote position and length
- InsightCard 4-variant system (Finding/Gap/Pattern/Ambiguity)
- Article density

**Must differ from bread:**
- Map axes are snack-bar-specific (processing depth × sweetener architecture)
- BarCompositionBreakdown dimensions are bar-native (base / sweetener / NOVA / additives / alignment)
- No fermentation or flour-position language
- No whole-grain position analysis — replaced with structural base analysis

---
---

# ARTICLE 2 — "פרוטאין, 'טבעי', פיטנס: מה הרכיבים הראו"

**URL:** `/snack-bars/wellness`
**Hebrew title:** פרוטאין, "טבעי", פיטנס: מה הרכיבים הראו

---

## 1. Page Purpose

This article investigates the protein, wellness, and "natural" snack bar segment — products positioned around protein content, natural ingredients, whole food claims, and functional benefits. The investigation focuses on three specific positioning gaps found in the data: protein positioning versus actual structural quality, "natural" date-based branding versus processing depth, and "fitness" naming versus composition. The article's central finding: the only B-grade product in the entire snack bar dataset is a 4-ingredient date bar — simpler than all protein-positioned products, and 23 points above the best protein bar scored.

---

## 2. Editorial Spine

> "הציון הגבוה ביותר בכל הנתונים שנסרקו — 70/B — הוא של חטיף תמרים עם 4 רכיבים. כל חטיפי הפרוטאין קיבלו D. הפרש הציון: 23 נקודות."

---

## 3. Full Page Structure

```
1.  Hero + ShelfStatBar
2.  Intro paragraph (150–180 words)
3.  Key Findings (5 InsightCards)
4.  Shelf Map — SnackBarWellnessMap
5.  What's On The Shelf — ThreeMisalignmentBreakdown
6.  Main Comparisons — ProductComparisonMatrix (3 pairs)
7.  Synthesis paragraph (150–200 words)
8.  Glossary — GlossaryAccordion
9.  Full Comparison CTA
10. Methodology Note
```

---

## 4. Component Mapping

| Section | Component | Purpose |
|---------|-----------|---------|
| Hero + ShelfStatBar | ShelfStatBar | Shelf numbers emphasizing the key contrast |
| Key Findings | InsightCardsGrid (5 cards) | Five findings that frame the wellness segment |
| Shelf Map | SnackBarWellnessMap | Two axes: ingredient simplicity vs. positioning claim |
| What's On The Shelf | ThreeMisalignmentBreakdown | Three positioning gaps found in the data |
| Comparisons | ProductComparisonMatrix (3 pairs) | Three high-contrast pairs |
| Synthesis | SynthesisParagraph | One editorial paragraph |
| Glossary | GlossaryAccordion | Eight terms |
| CTA | ComparisonCTA | Full table link |
| Methodology | MethodologyNote | 5 sentences max |

---

## 5. Component Specifications

---

### ShelfStatBar — Article 2

```
53 נסרקו  |  70/B — הציון הגבוה ביותר (חטיף תמרים, 4 רכיבים)  |  חטיפי פרוטאין: 45–47/D  |  יוחננוף · מאי 2026
```

The key contrast ("70/B date bar vs. 45–47/D protein bars") belongs in the ShelfStatBar — it is the article's opening frame.

---

### InsightCardsGrid — Article 2

Five cards.

**Card 1 — Finding:**
> **הציון הגבוה ביותר בכל הנתונים הוא של חטיף עם 4 רכיבים — 70/B.**
> חטיף תמרים במילוי חמאת שקדים: תמרים, חמאת שקדים, שקדים, קקאו. לא עוד. הפשוט ביותר — הציון הגבוה ביותר.

**Card 2 — Finding:**
> **חטיפי הפרוטאין קיבלו D — 23 נקודות מתחת לחטיף התמרים.**
> Nature Valley Protein: 45–47/D. הסיבה: NOVA4, מרובה רכיבים מהונדסים. הפרש הציון לא בא מהפרוטאין — בא מעומק העיבוד.

**Card 3 — Ambiguity:**
> **"תמרים" על האריזה לא אומר בהכרח תמרים-ראשון ברשימת הרכיבים.**
> פרי מארז תמרים ואגוזי לוז (43/D): NOVA4, סוכרים מוספים, cap מ-NOVA4. חטיף תמרים במילוי חמאת שקדים (70/B): תמרים ראשון, NOVA2, בלי סוכר מוסף. שני מוצרים "תמרים" — 27 נקודות הפרש.

**Card 4 — Pattern:**
> **NOVA4 = תקרת ציון D. אף מוצר פרוטאין/פיטנס לא פרץ את הגבול הזה.**
> כל מוצר NOVA4 בנתונים הוגבל ל-68 מקסימום, ובשילוב עם גורמים נוספים — ל-D לכל היותר. מיצוב "פרוטאין" לא מבטל את cap ה-NOVA.

**Card 5 — Gap:**
> **פרי מארז — "טבעי" ועם תמרים — קיבל 43/D. למה?**
> NOVA4, סוכרים מוספים, cap משולב. המיצוב הטבעי לא הגן עליו מה-cap. הרכב הרשימה הוא שקבע.

---

### SnackBarWellnessMap

**Purpose:** Show the wellness/protein/natural segment across two axes: ingredient simplicity vs. positioning strength.

**X axis:** פשטות הרכיבים — from "פשוט / בסיס שלם" (left) to "מורכב / מהונדס" (right)
**Y axis:** חוזק מיצוב ה"בריאות" — from "מיצוב נמוך" (bottom) to "מיצוב גבוה (פרוטאין / טבעי / פיטנס)" (top)

**Clusters (4):**

| Cluster | Label | Position | Key Products |
|---------|-------|----------|--------------|
| A | פשוט + ללא מיצוב | Top-left / left | חטיף תמרים במילוי חמאת שקדים (70/B) |
| B | פשוט-בינוני + מיצוב בינוני | Middle-left | חטיף תמרים קקאו (56/C), חמאת בוטנים (55/C) |
| C | מורכב + מיצוב גבוה | Top-right | Nature Valley Protein (45–47/D), Chewy (38–39/D) |
| D | בינוני + "טבעי" מוצהר | Middle | פרי מארז (42–43/D) |

**Key annotation:**
- Cluster A (70/B) is top-left — simple, lower positioning claim, highest score
- Cluster C (D range) is top-right — high positioning claim, NOVA4, lower score
- Annotate the distance between A and C with: "23 נקודות הפרש — אותה קטגוריה, עיבוד שונה"

**Visual specs:**
- Same dot system as Article 1 map
- Annotate the 70/B date bar explicitly — it is the article's key reference point
- Cluster C products (protein bars) should have a visible label showing score range (45–47/D)
- No color-coding to imply "good cluster" vs "bad cluster"

**Map title:** "מיצוב מול פשטות הרכיבים: איפה עומד כל חטיף"

**Caption:** "כל נקודה = מוצר אחד. מיקום מבוסס על רשימת הרכיבים ומיצוב המוצר — לא על הצגת האריזה."

---

### ThreeMisalignmentBreakdown — Article 2

**Purpose:** This replaces generic "What's On The Shelf." Three named positioning gaps explain most of the wellness segment's score variance.

**Structure:** Three panels. Each: gap name, what the gap looks like in the data, how many products, score effect, product evidence inline.

---

**Gap 1: פער הפרוטאין (The Protein Gap)**

```
מה זה: מוצר שמציג "protein" בשמו או בתאור, אבל הציון לא שיקף יתרון מקמח-פרוטאין מבחינת עיבוד.
כמה מוצרים: שני מוצרי Nature Valley Protein מותגיים, + מוצרי פיטנס פרוטאין.
מה אפשר לדעת: הציון מבוסס על מבנה הרכיבים ועומק העיבוד — NOVA4 cap גובר על תביעת הפרוטאין.
מה לא ניתן לדעת: האם כמות הפרוטאין עצמה גבוהה — אין נתוני תזונה מלאים לכל המוצרים.
```

*Product evidence (inline):*
- נייצ'ר וואלי פרוטאין בוטנים קרמל מלוח — 45/D — NOVA4 — "protein" בשם, D בציון
- נייצ'ר וואלי פרוטאין בוטנים ושוקולד — 47/D — NOVA4 — אותו דפוס
- חטיף תמרים במילוי חמאת שקדים — 70/B — NOVA2 — אין "protein" בשם, הציון הגבוה ביותר

---

**Gap 2: פער ה"טבעי" (The Natural Gap)**

```
מה זה: מוצרים המוצגים כ"טבעי" או "תמרים" שעדיין קיבלו D — בגלל NOVA4 ו-cap מסוכר.
כמה מוצרים: שני מוצרי פרי מארז + מוצרי Free (מארז תמרים).
מה אפשר לדעת: גם מוצרים עם תמרים בשם קיבלו cap מ-NOVA4 כשסוכרים מוספים הופיעו ברשימה.
מה לא ניתן לדעת: מהו האחוז המדויק של תמרים לעומת סוכרים מוספים — אין נתוני הרכב מפורטים.
```

*Product evidence (inline):*
- פרי מארז תמרים ואגוזי לוז — 43/D — NOVA4 — תמרים בשם, cap מ-NOVA4 + סוכר
- פרי מארז תמרים ושברי קקאו — 42/D — NOVA4 — אותו דפוס
- חטיף תמרים במילוי חמאת שקדים — 70/B — NOVA2 — "תמרים" ראשון ברשימה, ללא סוכר מוסף

**The key insight:** "תמרים" בשם המוצר לא מספיק — מה שנבדק הוא האם תמרים ראשון ברשימת הרכיבים ומה מגיע אחריו.

---

**Gap 3: פער ה"פיטנס" (The Fitness Gap)**

```
מה זה: מוצרים עם "פיטנס" בשמם שקיבלו ציון ממוצע של 25–45/D–E.
כמה מוצרים: לפחות 6 מוצרי פיטנס ממותגים בנתונים.
מה אפשר לדעת: "פיטנס" על האריזה לא תרם לציון — הציון מבוסס על מבנה הרכיבים בלבד.
מה לא ניתן לדעת: האם יש שוני תזונאי בין מוצרי פיטנס לאחרים — נדרשים נתוני תזונה מלאים.
```

*Product evidence (inline):*
- חטיפי דגנים פיטנס קלאסי — 46/D — NOVA4
- חטיפי דגנים פיטנס שקדים ודבש — 45/D — NOVA4
- פיטנס בר גרנולה שוקולד מריר — 17/E — NOVA4
- חטיפי דגנים פיטנס שוקולד מריר — 29/E — NOVA4
- חטיפי דגנים פיטנס שוקולד בננה — 22/E — NOVA4

ממוצע ציון מוצרי "פיטנס" ממותגים: ~32. ממוצע NOVA2 date bars: ~57.

---

**Visual specs for ThreeMisalignmentBreakdown:**
- Three panels in sequence, not tabs
- Each panel: gap name, stats, two-column inline product evidence (misalignment example vs. aligned example)
- Evidence: text + score only — no product photography
- Do NOT title this section "איפה פיטנס נכשל" or any failure framing
- Do NOT call any product misleading or deceptive — document the composition pattern

---

### ProductComparisonMatrix — Article 2

Three pairs.

---

**Pair 1: "בר פרוטאין מול חטיף תמרים"**

| מוצר | ציון | דרגה | NOVA | רכיבים (משוער) | גורם עיקרי |
|------|------|------|------|----------------|------------|
| חטיף תמרים במילוי חמאת שקדים | 70 | B | 2 | ~4 | בסיס שלם + עיבוד מינימלי |
| נייצ'ר וואלי פרוטאין בוטנים ושוקולד | 47 | D | 4 | ~15+ | NOVA4 + cap מסוכר |

**Explanation:**
> "שניהם חטיפי "ממתק" — אחד עם תמרים ואחד עם שוקולד ובוטנים. הפרש: 23 נקודות. חטיף התמרים: תמרים, חמאת שקדים, שקדים, קקאו — NOVA2. בר הפרוטאין: קמח, סירופ, חלבון ממקור מבודד, ציפוי, תוספות — NOVA4. הציון שיקף את עומק העיבוד, לא את כמות הפרוטאין."

**Tension:** The simpler product outscored the protein-positioned product by 23 points.

---

**Pair 2: "שלושה מוצרים מצופי שוקולד — שלושה ציונים"**

| מוצר | ציון | דרגה | NOVA | בסיס |
|------|------|------|------|------|
| חטיף תמרים בציפוי שוקולד 100% קקאו | 56 | C | 2 | תמרים |
| מרבה סלים דליס שוקולד מריר | 58 | C | 3 | רב-דגן מעובד |
| פיטנס בר גרנולה שוקולד מריר | 17 | E | 4 | קמח + סירופ |

**Explanation:**
> "שלושה חטיפים בציפוי שוקולד מריר. שלושה ציונים: 56, 58, ו-17. הפרש בין הגבוה לנמוך: 41 נקודות. הגורם: הבסיס ועומק העיבוד. חטיף התמרים (NOVA2) ומרבה סלים (NOVA3) — בטווח C. פיטנס גרנולה (NOVA4) — 17/E. על אותו מדף, בגובה עיניים."

**Tension:** Three visually similar products, 41-point score span.

---

**Pair 3: "תמרים — אבל לא אותו דבר"**

| מוצר | ציון | דרגה | NOVA | הסיבה לפרש |
|------|------|------|------|------------|
| חטיף תמרים במילוי חמאת שקדים | 70 | B | 2 | תמרים ראשון, ללא סוכר מוסף |
| פרי מארז תמרים ואגוזי לוז | 43 | D | 4 | NOVA4, cap מסוכר + עיבוד |

**Explanation:**
> "שני מוצרים 'תמרים'. שניהם מוצגים כ-snack טבעי. הפרש: 27 נקודות. פרי מארז: תמרים בשם, אבל NOVA4, cap מסוכר מוסף. חטיף תמרים: תמרים ראשון ברשימה, NOVA2, אין סוכר מוסף. 'תמרים' על האריזה לא ניבא ציון — רשימת הרכיבים כן."

**Tension:** Same product category signal, same natural framing — 27-point divergence.

---

### SynthesisParagraph — Article 2

**One paragraph. 150–200 words. Finding-first. No recommendation.**

> "מה שמפריד את המוצרים בקטגוריה הזו הוא לא השם ולא המיצוב — זה מבנה הרכיבים ועומק העיבוד. חטיפי פרוטאין (D), חטיפי פיטנס (D–E), ומוצרי תמרים עם NOVA4 (D) — כולם נחסמו על ידי אותה תקרה: NOVA4 cap שמגביל ל-68 לכל היותר, ובשילוב עם סוכרים מוספים — ל-45–55. מיצוב 'פרוטאין' לא ביטל את ה-cap. מיצוב 'טבעי' לא ביטל את ה-cap. מה שביטל אותו — הרכב פשוט, עיבוד מינימלי, ומקור שלם כרכיב ראשון."
>
> "הציון הגבוה ביותר בכל הנתונים שנסרקו — 70/B — הלך לחטיף עם 4 רכיבים: תמרים, חמאת שקדים, שקדים, קקאו. NOVA2. ללא סוכר מוסף. הוא לא נקרא 'פרוטאין' ולא נקרא 'פיטנס'. הוא פשוט מה שרשימת הרכיבים שלו אמרה שהוא."

---

### GlossaryAccordion — Article 2

Eight terms.

| מונח | הגדרה |
|------|--------|
| ציון ברי | ציון 0–100 המשקף עד כמה הרכב המוצר תואם את שמו והצגתו |
| דרגה | A–E, מבוסס על טווח הציון |
| NOVA | מערכת סיווג לעומק עיבוד תעשייתי — 1 (מינימלי) עד 4 (אולטרה-מעובד) |
| NOVA4 | מוצר אולטרה-מעובד — מכיל חומרים שלא ניתן להכין בבית |
| cap | תקרת ציון שברי מפעיל עקב סיכון מתועד (NOVA4, סוכר גבוה, תוספות מרובות) |
| בסיס שלם | כשהרכיב הראשון הוא מזון שלם (תמרים, שקדים, שיבולת שועל שלמה) — לפני עיבוד |
| מיצוב מול הרכב | הפרש בין מה שמוצג על האריזה לבין מה שמצוין ברשימת הרכיבים |
| ניתוח חלקי | ניתוח מבוסס על נתוני מבנה רכיבים בלבד — ללא לוח תזונה מלא |

---

## 6. Product Clustering Logic — Article 2

| Cluster | Label | Logic | Products |
|---------|-------|-------|---------|
| A | פשוט + בסיס שלם | nova_proxy ≤ 2 AND base = whole food (dates/nuts) | חטיף תמרים במילוי חמאת שקדים (70/B) |
| B | בינוני + בסיס שלם-מעובד | nova_proxy = 2–3 AND grade = C | חטיף תמרים קקאו (56/C), חמאת בוטנים (55/C), Slim Delice (52–62/C) |
| C | מורכב + מיצוב גבוה | nova_proxy = 4 AND high wellness claim | Nature Valley Protein (45–47/D), Chewy (38–39/D) |
| D | "טבעי" + NOVA4 | nova_proxy = 4 AND natural/date positioning | פרי מארז (42–43/D) |

**Cluster A special annotation:** The single B-grade product is isolated in Cluster A. Annotate it explicitly: "70/B — הפשוט ביותר, הציון הגבוה ביותר."

---

## 7. Score Driver System — Article 2

Same component as Article 1, with these additional drivers:

| Driver | Direction | Evidence | UX Label |
|--------|-----------|----------|----------|
| תמרים ראשון ברשימה + NOVA2 | ↑ strong | whole_food base = dates + nova_proxy = 2 | "בסיס שלם" |
| "פרוטאין" בשם + NOVA4 | ↔ neutral (cap applies) | protein claim + nova_proxy = 4 | "פרוטאין מהונדס — NOVA4 מגביל" |
| סוכרים מוספים + NOVA4 | ↓ | multiple sweetener sources + nova_proxy = 4 | "NOVA4 + סוכר — cap" |
| NOVA2 without added sugar | ↑ | nova_proxy = 2 + no sugar red label | "עיבוד מינימלי" |
| synthesis: hyper-palatable | ↓ −3 | sweetener + ≥3 additives + non-isolate | "הנדסת טעם" |

---

## 8. Comparison Logic — Article 2

**Pair 1: חטיף תמרים במילוי חמאת שקדים vs. נייצ'ר וואלי פרוטאין**
- Why paired: both premium snack positioning, both available same shelf
- Tension: protein-positioned product scores 23 points below a date bar
- Score spread: 70 vs. 47
- Driver: NOVA tier (2 vs. 4), ingredient list length (~4 vs. ~15+)
- Never imply: protein bars are bad for health — document the composition gap

**Pair 2: חטיף תמרים קקאו vs. סלים דליס שוקולד מריר vs. פיטנס גרנולה שוקולד**
- Why paired: all three chocolate-coated, all three on same shelf
- Tension: 41-point span between highest and lowest in this chocolate-coated group
- Score spread: 56 / 58 / 17
- Driver: NOVA tier (2 / 3 / 4), base structure

**Pair 3: חטיף תמרים במילוי חמאת שקדים vs. פרי מארז תמרים ואגוזי לוז**
- Why paired: both "date" positioned, both natural-adjacent claim
- Tension: 27-point gap between two products with same stated identity
- Score spread: 70 vs. 43
- Driver: NOVA tier difference (2 vs. 4), added sugars in פרי מארז

---

## 9. Visual Hierarchy Rules — Article 2

**Dominant:** SnackBarWellnessMap (with Cluster A annotation) and ThreeMisalignmentBreakdown
**Secondary:** InsightCardsGrid (5 cards) and SynthesisParagraph
**Minimal:** ShelfStatBar, Glossary, Methodology

**Key visual innovation for Article 2:** The map annotation showing Cluster A (70/B date bar) as an isolated outlier — simple, low positioning, highest score — while Cluster C (protein bars) clusters at D despite high positioning claims. This paradox should be visible on the map.

**Tone distinction from Article 1:** Article 2 is sharper — the protein/fitness positioning gap is the core finding and the article leans into it. Same restraint, higher contrast.

---

## 10. Copywriting Rules — Article 2

**Approved:**
```
חטיף תמרים: 4 רכיבים, NOVA2, 70/B.
Nature Valley Protein: NOVA4, ~15 רכיבים, 47/D.
NOVA4 cap גובר על מיצוב הפרוטאין.
"פרוטאין" על האריזה לא שינה את ה-cap.
```

**Forbidden:**
```
חטיפי פרוטאין מרמים.
פרוטאין מהונדס הוא לא פרוטאין אמיתי.
קנה תמרים, לא פרוטאין.
הפיטנס מסוכן.
```

**Tone:** The 70/B date bar is documented, not celebrated. The protein bars at D are documented, not condemned.

**One footer disclaimer only. Zero body disclaimers.**

---

## 11. Data Requirements — Article 2

**Dataset fields required per product:**
```
name_he, score, grade, displayable, confidence_level,
nova_proxy, structural_class, caps_applied, synth_score,
short_summary_he, ingredient_architecture_summary
```

**Products that must appear in this article:**
- חטיף תמרים במילוי חמאת שקדים (70/B) — in Pairs 1 and 3, map anchor (Cluster A)
- נייצ'ר וואלי פרוטאין בוטנים ושוקולד (47/D) — in Pair 1, ThreeMisalignmentBreakdown Gap 1
- נייצ'ר וואלי פרוטאין קרמל מלוח (45/D) — in ThreeMisalignmentBreakdown Gap 1
- חטיף תמרים בציפוי שוקולד 100% קקאו (56/C) — in Pair 2
- מרבה סלים דליס שוקולד מריר (58/C) — in Pair 2
- פיטנס בר גרנולה שוקולד מריר (17/E) — in Pair 2
- פרי מארז תמרים ואגוזי לוז (43/D) — in Pair 3, ThreeMisalignmentBreakdown Gap 2
- All fitness-branded products — named inline in ThreeMisalignmentBreakdown Gap 3

---

## 12. Cursor Build Notes — Article 2

**Priorities:**
1. SnackBarWellnessMap with Cluster A annotation — most critical visual. Carries the article's main tension.
2. ThreeMisalignmentBreakdown — three panels, inline product evidence, not cards
3. SynthesisParagraph — prose only, appears above Glossary, no component wrapper needed

**Likely failure modes:**
- Labeling protein bars as "deceptive" — they are documented, not accused
- Showing the 70/B date bar as a "recommended product" — it is documented evidence, not a recommendation
- Treating the three-way chocolate comparison (Pair 2) as a ranked "best-to-worst" list — it is a structural contrast
- Removing the Cluster A annotation from the map — mandatory
- Conflating "simple" with "healthy" in copy — Bari describes composition, not health outcomes

---
---

# SHARED COMPONENT LIBRARY

---

## Components Used in Both Articles

### SnackBarShelfMap / SnackBarWellnessMap
Different axes per article. Same technical component with different configuration objects.

### GlossaryAccordion
Seven terms for Article 1. Eight terms for Article 2. Same component, different content arrays.

### ProductComparisonMatrix
Two pairs in Article 1. Three pairs in Article 2. Same table + prose structure.

### ComparisonCTA
Same component. Different text per article. Link targets differ.

### MethodologyNote
Same component. 5 sentences max. Same position in both articles.

---

## Display Rules — Both Articles

**Score display:** `[number] / [grade]` — e.g., `70 / B`. Never number alone. Never grade alone.

**Insufficient data:** If `confidence_level = "insufficient"`, show `לא נוקד`. Not a score.

**NOVA label:** Display as "NOVA2", "NOVA3", "NOVA4" — never "level 2", "ultra-processed level", etc.

**Cap display:** When showing caps, show the cap reason, not just the number. "NOVA4 — cap 68" not just "68".

**No ranked lists:** Never present products in a "best to worst" ordered format. Comparisons are structural contrasts.

**Synthesis scores:** Use synthesized scores (from run_snack_bars_synthesis_001), not base scores, for displayed values.

---

# GLOBAL CURSOR BUILD NOTES

1. **Both maps must be built before articles go live.** The maps are the primary visual anchor. Articles without maps are structurally incomplete.

2. **BarCompositionBreakdown and ThreeMisalignmentBreakdown are new components.** They do not exist in the current system. They must be built fresh. They are not repurposed InsightCards or ProductCard wrappers.

3. **ProductComparisonMatrix must be table + prose.** Not card duels. Not side-by-side hero comparisons.

4. **The 70/B date bar is evidence, not a recommendation.** Never display it with "מומלץ" or any endorsement badge.

5. **NOVA4 is factual, not moral.** Never write "NOVA4 is bad." Write: "NOVA4 — all products in this tier received D or E."

6. **The ShelfStatBar for Article 2 carries the key contrast** (70/B date bar vs. 45–47/D protein bars). It appears at the top — before InsightCards — and sets the article's frame.

7. **Data re-run required before Cursor implementation.** See Data Status section at the top of this document.

8. **Synthesis scores are the canonical scores.** All displayed scores come from `run_snack_bars_synthesis_001`. Base scores appear only in methodology/audit contexts.

---

# PRE-IMPLEMENTATION CHECKLIST

Before Cursor begins building:

- [ ] BSIP2 re-run completed with updated BSIP1 ingredients_raw
- [ ] Granola routing stabilized (granola_bar archetype or disambiguation)
- [ ] NOVA-awareness gate applied to whole_food_fat classification
- [ ] Frontend dataset JSON generated (matching bread_retail_002_v2_frontend_dataset.json format)
- [ ] All 53 products have `displayable`, `confidence_level`, `confidence_label_he` populated
- [ ] Synthesis scores confirmed as canonical in frontend dataset
- [ ] Score=50 default for insufficient data products NOT displayed as real scores

---
