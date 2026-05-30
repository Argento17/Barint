# Bread — Comparison Template Application v1

**Template version:** comparison_template_v1.md  
**Source data:** bread_retail_003 (258 scraped, 81 coherent scored products)  
**Date:** 2026-05-28  
**Status:** Ready for implementation — hero product to be confirmed from data lookup (see note)

---

## Page Structure

No changes to the frozen template:

```
[1] HERO
[2] PROLOGUE
[3] PRODUCT TABLE
[4] METHODOLOGY
```

---

## 1. Hero

**Hero product:** "לחם שאור" from a mainstream brand — scoring in D range despite sourdough positioning.

*Data note: Select the highest-volume commercial "שאור" or "מחמצת" bread that scores below 55. Candidates are among the D-grade wellness-segment products in bread_retail_003. The editorial team should pick the most recognizable brand name among these. The structural finding — fermentation label without fermentation signal — is confirmed across the category (58% of wellness-positioned breads lack a detectable fermentation signal).*

**Hero sentence form:**

> "[שם לחם מסחרי] — שאור בשם, שמרים תעשייתיים ברשימת הרכיבים."

If no single strongly-branded commercial sourdough with a D score is available, the alternative hero uses the highest-lowest contrast:

> "לחם מחמצת קמח מלא עם 77 נקודות. לחם כוסמין מסחרי עם [X] נקודות. שניהם קוראים לעצמם 'שאור'."

**Hero image:** Packaging photograph of the selected product. Clean background. Label and sourdough/שאור claim visible.

**Hero height:** Compact. The table headline must be visible without scrolling on a standard mobile screen (812px height).

**Score:** Visible immediately on load. No animation.

---

## 2. Prologue

> "מדף הלחם של שופרסל כולל מעל 80 מוצרים — מלחם אחיד לבן ועד לחם מחמצת מקמח כוסמין מלא. המילה 'שאור' מופיעה על מוצרים עם הרכבים שונים מאוד זה מזה. סיבים תזונתיים — שנחשבים לסימן לעיבוד נמוך יותר — נעים בין פחות מ-2 גרם ל-18.5 גרם ל-100 גרם. הבדל שקשה לראות מהאריזה."

Three sentences. Shelf observation only. No framework language. No value claims. Ends on the consumer's inability to see — which is the page's entire reason for existing.

**What the prologue does not say:**
- Which bread is better
- What the reader should buy
- What sourdough means nutritionally
- How we score

---

## 3. Product Table

### Default sort

Score descending. Highest-scoring product appears first.

Confirmed top products for editorial scope:
1. לחם טחינה פרוס — 82/A
2. קרקר כוסמין מלא ושומשום — 82/A
3. לחם ירוק מקמח מלא — 80/B
4. קרקר כוסמין אורגני — 78/B
5. לחם מחמצת קמח מלא — 77/B

*These five are the "best of shelf" cluster and will appear at the top of the table.*

### Editorial scope filter

Include in table: products where `data_sufficiency != "insufficient"` and `final_score_estimate is not null`.

From bread_retail_003: 81 coherent products.

### Optional highlighted pair

**Selected pair:** לחם שאור מסחרי [score D] vs. לחם מחמצת קמח מלא 77/B

**Driver line:** "שניהם נקראים 'שאור'. רשימת הרכיבים מספרת סיפור שונה."

This is one of the strongest editorial pairs in the Bari dataset across categories — the same label on products with structurally different fermentation. It should be used.

Visual treatment: two adjacent rows, thin bracket, driver line between them. Not a separate scene.

---

## 4. Filters

Three dimensions:

| Dimension | Hebrew label | Values |
|---|---|---|
| סוג לחם | סוג | לחם פרוס, לחם שלם, פיתה, קרקר, חלה |
| ציון | ציון | A, B, C, D |
| תסיסה | תסיסה | עם מחמצת, ללא מחמצת מזוהה |

**Note on "תסיסה" filter:** This exposes the fermentation signal as a filter dimension. This is acceptable because "מחמצת" is already a consumer-facing concept — it is printed on packaging. The filter makes it possible to see which products actually have a detected fermentation signal vs. which have the label without it. This is the single most useful filter for the bread category.

**The filter does not say "fermentation_detected = true."** It says "עם מחמצת" / "ללא מחמצת מזוהה."

**"ללא מחמצת מזוהה"** is not "without sourdough." It is: the BSIP1 ingredient analysis did not detect markers consistent with sourdough fermentation. This note should appear as a hover tooltip or single explanatory line if the filter is selected — not as permanent UI text.

---

## 5. Methodology

> "בדקנו מעל 80 מוצרי לחם ממדף שופרסל. הציון מבוסס על רכיבים, ערכי תזונה ורמת עיבוד — לא רק על קלוריות. הציונים יחסיים לקטגוריית הלחם. [המתודולוגיה המלאה →]"

Footer position. Low visual weight. No subheading.

---

## 6. Insight Lines — Examples

The following examples illustrate the insight-line approach for bread. Full production requires applying insight_line_spec_v1.md to all 81 coherent products.

| Product | Score | Grade | Insight Line | Type |
|---|---|---|---|---|
| לחם טחינה פרוס | 82 | A | מחמצת, קמח מלא, 18.5 גרם סיבים — הציון הגבוה ביותר | T1 |
| קרקר כוסמין מלא ושומשום | 82 | A | הציון הגבוה ביותר — קרקר, לא לחם | T3 |
| לחם ירוק מקמח מלא | 80 | B | קמח מלא, 6.4 גרם סיבים ל-100 גרם | T1 |
| קרקר כוסמין אורגני | 78 | B | אורגני, 9.3 גרם סיבים — ציון גבוה מרוב הלחמים | T1+T3 |
| לחם מחמצת קמח מלא | 77 | B | מחמצת עם תסיסה מזוהה — נדיר בין לחמי השאור | T3 |
| [לחם שאור מסחרי, score ~D] | ~50 | D | שאור בשם, שמרים תעשייתיים ברשימת הרכיבים | T2 |
| לחם אחיד [brand] | ~50 | D | לחם לבן קלאסי — הרכב צפוי, ציון צפוי | T3 |
| לחם כוסמין [brand] | ~55 | C | כוסמין — גרגיר עתיק, עיבוד תעשייתי | T2 |
| חלה [brand] | ~45 | D | חלה שבת — שמרים, סוכר, שמן — ציון נמוך בקטגוריה | T1 |
| פיתה [brand] | ~50 | D | פיתה ללא תוספים מיוחדים — ציון קרוב לממוצע | T3 |
| לחם מלא [brand] עם סיבים | ~60 | C | "מלא" בשם — קמח לבן ברשימת הרכיבים הראשונה | T2 |
| לחם פשתן ושיפון | ~65 | B | פשתן, שיפון, מחמצת — שלושת הסיבות לציון הגבוה | T1 |

### The essential "fiber laundering" line

One of the bread category's strongest editorial findings is "fiber laundering" — products where the label implies high fiber but the fiber source is isolated/added rather than whole grain.

Line for products with this pattern:
> "'עשיר בסיבים' — מקור הסיבים: אינולין מוסף, לא קמח מלא"

This is a Type 2 line. It names the specific mechanism without calling the product misleading.

---

## 7. Applying the Template: What Stays the Same

These elements are identical to מעדנים and all future categories:

- Page structure (hero → prologue → table → methodology)
- Row anatomy (image, name, score chip, insight line, expand toggle)
- Expanded row (nutrition 5-field, ingredients, data note, confidence)
- Filter behavior (collapsed by default, single-select)
- Methodology format (2–4 sentences, footer weight)
- All public language rules from comparison_template_v1.md
- All drift-prevention rules

---

## 8. What Is Different from מעדנים

| Element | מעדנים | לחם |
|---|---|---|
| Hero finding | Icon paradox (most famous = lowest score) | Label gap (sourdough = not always fermented) |
| Grade ceiling | Max B (4 products) | A grades exist (2 products) |
| Score range | 26–70 | 40–82 |
| Primary tension | Processing depth | Fermentation authenticity |
| Filter dim 3 | — | תסיסה (fermentation signal) |
| Cluster names | מילקי / חלבון / הגולן / פירות / פודינג / סויה | פרוס / שלם / פיתה / קרקר / חלה |
| Highlighted pair | מילקי vs. יופלה GO | מחמצת מסחרי vs. מחמצת אמיתי |

The template is the same. The data is different.
