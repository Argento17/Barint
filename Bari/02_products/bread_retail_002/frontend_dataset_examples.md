# Frontend Dataset Examples — real_bread_retail_002_v2

Usage examples for Cursor to implement UI components.

---

## Example 1 — Product Card (verified, high score)

```json
{
  "id": "shufersal_96086000966",
  "name_he": "קרקר כוסמין מלא ושומשום",
  "category": "cracker",
  "category_label_he": "קרקר",
  "score": 82,
  "grade": "A",
  "displayable": true,
  "confidence_label_he": "נתונים חלקיים",
  "confidence_level": "verified",
  "fiber_g": 10.0,
  "fermentation_real": false,
  "whole_grain": true,
  "seed_halo": false,
  "key_flags": ["גרעינים מלאים", "כוסמין", "שומשום", "סיבים גבוהים במיוחד"],
  "short_summary_he": "עשוי מקמח כוסמין מלא. תכולת סיבים גבוהה במיוחד — 10.0g ל-100g.",
  "ingredient_architecture_summary": "קמח כוסמין מלא · שמרים · שומשום"
}
```

**Cursor implementation note:**
- Show score badge (82 / A)
- Show `confidence_label_he` as a small pill below the name
- Show `key_flags` as color-coded tags
- Use `image_url` for the product photo
- Link `source_url` to Shufersal product page

---

## Example 2 — Product Card (insufficient data)

```json
{
  "id": "shufersal_2759522",
  "name_he": "מארז לחמניות חלה מתוקה",
  "displayable": false,
  "confidence_label_he": "לא מספיק לניתוח ודאי",
  "confidence_level": "insufficient",
  "score": null,
  "grade": null
}
```

**Cursor implementation note:**
- Do NOT show a score or grade
- Show only the `confidence_label_he` label
- Gray out the card or show a "??" placeholder
- Do not include in rankings or top lists

---

## Example 3 — Comparison Card

```json
{
  "id": "comp_fermentation_rye",
  "title": "מחמצת אמיתית לעומת שמרים תעשייתיים — לחם שיפון",
  "narrative": "שני לחמי שיפון עם ציוני תזונה דומים — אך אחד מכיל מחמצת אמיתית ברשימת הרכיבים והשני מסתמך על שמרים תעשייתיים.",
  "left_product_id": "shufersal_574370",
  "right_product_id": "shufersal_3719259",
  "key_difference": "מחמצת אמיתית לעומת שמרים תעשייתיים",
  "visual_direction": "left_wins"
}
```

**Cursor implementation note:**
- Render as side-by-side card
- Left = "better" product by `visual_direction`
- Show `key_difference` as the central callout
- Pull full product data from `products[]` by ID

---

## Example 4 — Insight Widget (fermentation)

```json
{
  "headline_he": "מתוך 32 מוצרים מאומתים, 18 כוללים מחמצת אמיתית ברשימת הרכיבים.",
  "genuine_count": 18,
  "mismatch_count": 13,
  "industrial_only_count": 8,
  "note_he": "13 מוצרים נושאים את השם 'מחמצת' אך כוללים שמרים תעשייתיים ברשימת הרכיבים."
}
```

**Cursor implementation note:**
- Render as a stat card with donut chart
- `headline_he` is the primary text
- `note_he` is a secondary callout / warning

---

## Example 5 — Homepage Section (strongest_verified)

```json
[
  {
    "id": "shufersal_96086000966",
    "name_he": "קרקר כוסמין מלא ושומשום",
    "score": 82,
    "grade": "A",
    "category_label_he": "קרקר",
    "image_url": "https://res.cloudinary.com/shufersal/...",
    "short_summary_he": "עשוי מקמח כוסמין מלא. תכולת סיבים גבוהה במיוחד — 10.0g ל-100g."
  }
]
```

**Cursor implementation note:**
- Render as horizontal scroll or grid of product cards
- Use `score` for the badge, `grade` for the letter
- Use `image_url` for the product photo
- Only products in this list are guaranteed displayable

---

## Example 6 — Mandatory Transparency Text

Always show before any score rankings:

```
ניתחנו 108 מוצרי לחם, פיתה וקרקרים ממדף שופרסל.
32 מוצרים עמדו בסף הנתונים הנדרש לניתוח מלא.
זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא.
```

Source: `homepage_sections.mandatory_framing_he`

---

## Confidence Label Color Guide

| Label | Color | When |
|:------|:------|:-----|
| נתונים חלקיים | Green / teal | `confidence_level = "verified"` |
| חסרים נתונים מהותיים | Orange / amber | `confidence_level = "partial"` |
| לא מספיק לניתוח ודאי | Gray | `confidence_level = "insufficient"` |

---

## Do NOT

- Do not read raw BSIP2 report markdown files for UI data
- Do not show score for `displayable = false` products
- Do not use the word "Israeli market" — this is Shufersal only
- Do not rank products across `confidence_level` tiers
