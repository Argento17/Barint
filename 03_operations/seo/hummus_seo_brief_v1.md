---
doc_id: hummus_seo_brief_v1
title: "SEO Brief — Hummus Blog Article (/blog/hummus)"
created_at: 2026-06-07
task_origin: TASK-202
authority: Content Agent
status: ACTIVE
---

# SEO Brief — Hummus Article

Article URL: `/blog/hummus`
Article title: "64 מוצרי חומוס בשופרסל. פער של 46 נקודות בין הראש לזנב."

---

## Primary Keyword

**חומוס השוואה**

Rationale: High-intent informational query for Israeli consumers comparing hummus products at the shelf. Consumers searching this term are in an active decision context — they want to know what makes one hummus different from another before buying. The article directly answers this with data from 64 products. Hebrew-language competition for data-grounded, ingredient-level hummus analysis is low.

---

## Secondary Keywords (5)

| Keyword | Rationale |
|---|---|
| **אחוז טחינה בחומוס** | Core finding; underserved query in Hebrew — consumers don't know this matters |
| **נתרן בחומוס** | High practical relevance; sodium variance is the most surprising finding |
| **חומוס שופרסל** | Branded informational query with local intent |
| **מה לחפש בחומוס** | Buying-guide intent; maps to the buying guide section |
| **חומוס גרגרים לעומת ממרח** | Category boundary topic that no other Hebrew content addresses well |

---

## URL Slug

`/blog/hummus`

Justification: The word "חומוס" in romanised form is universally understood. Short, memorable, unambiguous. No encoding issues. Stable — future rescans at this URL do not require a redirect. The `/blog/` prefix distinguishes the article context from `/hashvaot/hummus` (the comparison tool page).

---

## Meta Title

```
64 מוצרי חומוס בשופרסל. פער של 46 נקודות. | Bari
```

Character count: 44 (well within 60-char limit including brand suffix).

Rationale: Two quantitative findings in two sentences. The number 46 is specific and surprising — it signals genuine data behind the claim. Brand "Bari" appended per site convention.

---

## Meta Description

```
סרקנו את מדף החומוס בשופרסל — 64 מוצרים. אחוז הטחינה הוא הגורם שמסביר הכי הרבה את הפערים. הנתרן משתנה פי-50 על אותו מדף.
```

Character count: 125 (within 155-char limit).

Rationale: Three findings stated bluntly — scope, tahini angle, sodium surprise. No hedging. Includes the primary keyword context ("מדף החומוס") and both core findings that drive click intent.

---

## Structured Data Recommendation

**Article schema (JSON-LD)** — implement in the article page layout or `<script type="application/ld+json">` in `page.tsx`.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "64 מוצרי חומוס בשופרסל. פער של 46 נקודות בין הראש לזנב.",
  "description": "סרקנו את מדף החומוס בשופרסל — 64 מוצרים. אחוז הטחינה הוא הגורם שמסביר הכי הרבה את הפערים.",
  "datePublished": "2026-06-07",
  "dateModified": "2026-06-07",
  "author": { "@type": "Organization", "name": "Bari" },
  "publisher": { "@type": "Organization", "name": "Bari", "url": "https://bari.co.il" },
  "inLanguage": "he",
  "url": "https://bari.co.il/blog/hummus"
}
```

**FAQ schema** — applicable as a secondary schema mapped to the buying guide section:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "איך יודעים כמה טחינה יש בחומוס?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "רשימת הרכיבים בגב האריזה. אם מצוין 'טחינה גולמית 31%' — יש אחוז. אם כתוב רק 'טחינה' — אין מידע על הכמות. ניתן להסיק בעקיפין: ממרח עם 10 גרם חלבון ל-100 גרם כנראה מכיל יותר טחינה מממרח עם 7 גרם."
      }
    },
    {
      "@type": "Question",
      "name": "כמה נתרן יש בחומוס?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "תלוי מאוד במוצר. גרגרי חומוס לבישול — 17 עד 24 מ\"ג ל-100 גרם. ממרחים מוכנים — 230 עד 480 מ\"ג. ממרחי ירקות כמו מטבוחה — עד 850 מ\"ג. הנתרן תמיד מצוין בטבלת הערכים התזונתיים בגב האריזה."
      }
    },
    {
      "@type": "Question",
      "name": "מה ההבדל בין גרגרי חומוס לממרח חומוס?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "גרגרי חומוס לבישול: רכיב יחיד, נתרן נמוך מאוד, חלבון 17–22 גרם ל-100 גרם ביבש. ממרח מוכן: חומוס מבושל + טחינה + מלח + תוספים, נתרן 200–500 מ\"ג. שניהם יכולים להיות קרויים 'חומוס' בחזית האריזה."
      }
    }
  ]
}
```

---

## Internal Link Targets

| Target page | Link direction | Anchor text recommendation |
|---|---|---|
| `/hashvaot/hummus` | Article → comparison tool | "לניתוח המלא של מדף החומוס" (in CTA block) |
| `/hashvaot` | Article → comparison hub | "כל ניתוחי המדף" (in footer) |
| `/blog/shemen-zayit` | Article → recent article | Already in `recentAnalyses` |
| `/hashvaot/hummus` → `/blog/hummus` | Comparison tool → article | "קרא את הניתוח המעמיק" — add link from comparison page |
| Home page | Home → article | Surface in "ניתוחים אחרונים" section |

---

## Corpus Scope Note

Corpus: `run_hummus_003` (v5-glassbox_w4) — single retailer: Shufersal. Scrape date: 2026-05-30.

All quantitative claims in the article (product counts, score range, sodium range, grade distribution) are anchored to this corpus. No multi-retailer claims appear. Future rescans of additional retailers (Rami Levy, Victory, Yochananof) will require a versioned article update or a separate article.

---

## Distribution Notes (for future Marketing Agent reference)

- Primary channel: organic search (Israeli audience, Hebrew query intent)
- Secondary: WhatsApp sharing — "פי-50 בנתרן על אותו מדף" is a high-surprise share hook
- Content hook for social: the sodium variance table — 17 mg vs. 852 mg is a visually stark contrast
- Re-surface trigger: any new Israeli labeling regulation for hummus, or a new retailer scrape that can extend the corpus

---

*Hummus SEO Brief v1 — Content Agent — 2026-06-07 — TASK-202*
