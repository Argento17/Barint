---
doc_id: bread_seo_brief_v1
title: "SEO Brief — Bread Blog Article (/blog/lechem)"
created_at: 2026-06-07
task_origin: TASK-200
authority: Content Agent (SEO sections per brief template)
status: ACTIVE
---

# SEO Brief — Bread Article

Article URL: `/blog/lechem`
Article title: "24 מוצרי לחם בשופרסל. מה מפריד בין A ל-B."

---

## Primary Keyword

**לחם מלא ישראל**

Rationale: The category's central consumer question is "what is actually in whole wheat bread?" — a question the article answers with data. "לחם מלא" is the most common consumer-facing term for this query segment. Adding "ישראל" scopes to the Israeli market and matches the article's Shufersal-only corpus. Volume is consistent year-round (staple product category). Competition is low for data-grounded Hebrew content with named products and actual scores.

---

## Secondary Keywords (4–5)

| Keyword | Rationale |
|---|---|
| **לחם מחמצת ישראל** | Core finding: sourdough name ≠ sourdough ingredients. High consumer interest post-pandemic. |
| **לחם שיפון ישראל** | Two rye products scored highest in the corpus — the article directly establishes this finding. |
| **מה ההבדל בין לחמים** | Informational buying-intent query; maps to the findings and product matrix sections. |
| **קמח מלא לחם אחוז** | Addresses the label gap finding (no minimum % requirement). Underserved query in Hebrew. |
| **לחם שופרסל השוואה** | Branded + category query; corpus is Shufersal-specific, so this is an honest exact-match. |

---

## URL Slug

`/blog/lechem`

Justification: Hebrew romanised slug (not URL-encoded Hebrew). "lechem" is unambiguous and pronounceable. The `/blog/` prefix distinguishes editorial content from `/hashvaot/lechem` (comparison page). Slug is stable — a future re-scan of the bread shelf can update the article in place without a redirect.

---

## Meta Title

```
24 מוצרי לחם בשופרסל. מה מפריד בין A ל-B. | Bari
```

Character count: 50 (within the 60-char limit including brand suffix).

Rationale: Quantitative hook ("24 מוצרים") establishes data authority. "מה מפריד בין A ל-B" signals comparison intent without vague language. "Bari" appended per site convention.

---

## Meta Description

```
סרקנו את מדף הלחם של שופרסל — 24 מוצרים עם ציון. מחמצת בשם ≠ מחמצת ברכיבים. מה שמסביר את פער 16 הנקודות בין הלחם הכי גבוה לכי נמוך.
```

Character count: 138 (within 155-char limit).

Rationale: Finding-first structure. The "מחמצת בשם ≠ מחמצת ברכיבים" line is the article's sharpest claim and is share-optimised. Includes the numeric spread (16 נקודות) to establish that this is a category with real variance — unlike some categories where all products cluster.

---

## Structured Data Recommendation

**Article schema (JSON-LD)** — implement in the article page layout.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "24 מוצרי לחם בשופרסל. מה מפריד בין A ל-B.",
  "description": "סרקנו את מדף הלחם של שופרסל — 24 מוצרים עם ציון. מחמצת בשם ≠ מחמצת ברכיבים.",
  "datePublished": "2026-06-07",
  "dateModified": "2026-06-07",
  "author": { "@type": "Organization", "name": "Bari" },
  "publisher": { "@type": "Organization", "name": "Bari", "url": "https://bari.co.il" },
  "inLanguage": "he",
  "url": "https://bari.co.il/blog/lechem"
}
```

**FAQ schema** — applicable if the buying guide section is structured as Q&A:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "מה ההבדל בין לחם מחמצת ללחם שמרים?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "תסיסת מחמצת אמיתית מתבצעת עם חיידקי חומצה לקטית ושמרים טבעיים, ומשפיעה על זמינות המינרלים ועל מבנה הפחמימות. תסיסת שמרים תעשייתיים שונה בתהליך ובהשפעה. כדי לדעת איזה מהשניים יש בלחם — בדקו את רשימת הרכיבים, לא את שם המוצר."
      }
    },
    {
      "@type": "Question",
      "name": "איך יודעים אם לחם הוא 'מלא' באמת?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "בדקו שני דברים: (1) האם 'קמח חיטה מלא' (או שיפון/כוסמין מלא) מופיע ראשון ברשימת הרכיבים. (2) כמה גרמי סיבים ל-100 גרם — 6 גרם ומעלה מצביעים על בסיס דגן שלם אמיתי. הכיתוב 'מלא' בחזית האריזה אינו מחויב לאחוז מינימלי בתקן הישראלי."
      }
    },
    {
      "@type": "Question",
      "name": "מה הלחם עם הציון הגבוה ביותר בשופרסל?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "מספר מוצרים קיבלו ציון 82/A בניתוח מדף שופרסל מיוני 2026 — ביניהם לחם שיפון קל ולחם אחיד פרוס קל. הציון מבוסס על נתוני תווית — סיבים, דגן מלא ונוכחות מחמצת."
      }
    }
  ]
}
```

---

## Internal Link Targets

| Target page | Link direction | Anchor text recommendation |
|---|---|---|
| `/hashvaot/lechem` | Article → comparison page | "לניתוח הלחם המלא" (already in CTA block) |
| `/blog/shemen-zayit` | Article → recent article | Already in `recentAnalyses` |
| Home page | Home → article | Surface in "ניתוחים אחרונים" if section exists |
| `/hashvaot/lechem` → `/blog/lechem` | Comparison page → article | "קרא את הניתוח המעמיק על לחם" — add when Frontend Agent integrates |

---

## Distribution Notes

- Primary channel: organic search (Israeli audience, Hebrew query intent)
- Secondary: WhatsApp sharing — "מחמצת בשם ≠ מחמצת ברכיבים" is a shareable single-finding hook
- Content hook for social: the product matrix showing sourdough-named products with yeast in the ingredients list
- Re-surface trigger: any new Israeli labeling regulation on "לחם מלא" minimum percentages, or a new Shufersal scan round

---

*Bread SEO Brief v1 — Content Agent — 2026-06-07 — TASK-200*
