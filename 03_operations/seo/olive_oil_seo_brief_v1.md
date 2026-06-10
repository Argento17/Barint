---
doc_id: olive_oil_seo_brief_v1
title: "SEO Brief — Olive Oil Blog Article (/blog/shemen-zayit)"
created_at: 2026-06-07
task_origin: TASK-199
authority: Marketing Agent
status: ACTIVE
---

# SEO Brief — Olive Oil Article

Article URL: `/blog/shemen-zayit`
Article title: "13 מוצרי שמן זית בשופרסל. אפס גילויים על תאריך הקציר."

---

## Primary Keyword

**שמן זית כתית מעולה**

Rationale: This is the highest-intent informational query for Israeli consumers researching olive oil. "כתית מעולה" is the grade designation appearing on every product — a consumer searching it is asking what it means and how to choose. The article directly answers this question. Search volume is consistent year-round (Israeli culinary staple). Competition is low for detailed, data-grounded Hebrew content — most results are either brand sites or superficial listicles.

---

## Secondary Keywords (3–5)

| Keyword | Rationale |
|---|---|
| **תאריך קציר שמן זית** | Core finding of the article; underserved query in Hebrew |
| **PDO שמן זית** | Informational — consumers who have seen the label claim and want to understand it |
| **שמן זית ישראלי לעומת מיובא** | Addresses the origin section; common consumer consideration |
| **מה לחפש בשמן זית** | Buying-guide intent; maps to the buying guide section |
| **פוליפנולים שמן זית** | Science-section anchor; emerging consumer awareness term in Hebrew |

---

## URL Slug

`/blog/shemen-zayit`

Justification: Hebrew romanised (not encoded Hebrew in URL) avoids URL encoding issues in sharing links. "shemen-zayit" is readable, unambiguous, and pronounceable. The `/blog/` prefix establishes article context distinct from the `/hashvaot/` comparison pages. Slug is stable — future rescans of the same category can update the article at this URL without a redirect.

---

## Meta Title

```
13 מוצרי שמן זית בשופרסל. אפס גילויים על תאריך הקציר. | Bari
```

Character count: 54 (within the 60-char limit including brand suffix).

Rationale: Leads with a stark quantitative finding. "אפס גילויים" is the negative surprise hook. Brand "Bari" appended per site convention.

---

## Meta Description

```
סרקנו את מלאי שמן הזית בשופרסל — 13 מוצרים. אף אחד לא מצהיר על תאריך קציר. מה "כתית מעולה" מבטיח — ומה הוא לא מחויב לגלות.
```

Character count: 130 (within 155-char limit).

Rationale: Mirrors the hero subtitle — finding first, scope second, question-hook last. Avoids generic phrasing. Includes the primary keyword ("כתית מעולה") naturally.

---

## Structured Data Recommendation

**Article schema (JSON-LD)** — implement in the article page layout or in a `<script type="application/ld+json">` block in `page.tsx`.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "13 מוצרי שמן זית בשופרסל. אפס גילויים על תאריך הקציר.",
  "description": "סרקנו את מלאי שמן הזית בשופרסל — 13 מוצרים. אף אחד לא מצהיר על תאריך קציר.",
  "datePublished": "2026-06-07",
  "dateModified": "2026-06-07",
  "author": { "@type": "Organization", "name": "Bari" },
  "publisher": { "@type": "Organization", "name": "Bari", "url": "https://bari.co.il" },
  "inLanguage": "he",
  "url": "https://bari.co.il/blog/shemen-zayit"
}
```

**FAQ schema** — applicable as a secondary schema if the buying guide section is structured as Q&A. The four buying guide signals (harvest date, PDO/PGI, variety declaration, organic certification) can each become an FAQ entry. This increases eligibility for rich snippet display.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "מה חשיבות תאריך הקציר בשמן זית?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "תאריך הקציר מספר כמה זמן עבר מהסחיטה. פוליפנולים — הרכיבים הפעילים ביותר בשמן זית — מתכלים תוך 12–18 חודשים. תאריך תפוגה אינו מחליף מידע זה."
      }
    },
    {
      "@type": "Question",
      "name": "מה מבטיח הסיווג כתית מעולה?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "כתית מעולה מבטיח עמידה בסף כימי (חומציות ≤0.8%) בעת הייצור. הוא אינו מבטיח רמת פוליפנולים, תאריך קציר, זן ספציפי, או מקור גיאוגרפי מאומת."
      }
    },
    {
      "@type": "Question",
      "name": "מה ההבדל בין PDO ל-PGI בשמן זית?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "PDO (Protected Designation of Origin) מבטיח שהזיתים גדלו ועובדו באזור גיאוגרפי מוסמך. PGI (Protected Geographical Indication) מבטיח שחלק ניכר מהייצור קשור לאותו אזור. אף מוצר ממדף שופרסל אינו מחזיק בסיווג כזה."
      }
    }
  ]
}
```

---

## Internal Link Targets

| Target page | Link direction | Anchor text recommendation |
|---|---|---|
| `/hashvaot` | Article → comparison hub | "לכל ניתוחי המדף" (already in CTA block) |
| `/blog/milk-analysis` | Article → recent article | Already in `recentAnalyses` |
| `/blog/bread-standouts` | Article → recent article | Already in `recentAnalyses` |
| `/hashvaot` → `/blog/shemen-zayit` | Comparison hub → article | "קרא את הניתוח המעמיק על שמן זית" — add this link from the comparison hub page when olive oil appears there |
| Home page | Home → article | Surface in "ניתוחים אחרונים" section if one exists |

Inbound links from existing Bari pages should be added by the Frontend Agent as part of the article go-live checklist.

---

## Distribution notes (for future Marketing Agent reference)

- Primary channel: organic search (Israeli audience, Hebrew query intent)
- Secondary: sharing via WhatsApp — the stark headline ("אפס גילויים על תאריך הקציר") is share-optimised
- Content hook for social: the transparency matrix visual — all-red (all-X) columns for harvest date and PDO/PGI across 13 products is a shareable image
- Re-surface trigger: any new Israeli regulatory news about olive oil labeling, or a new Yochananof/Victory scrape that can be appended to the article as a follow-up section

---

*Olive Oil SEO Brief v1 — Marketing Agent — 2026-06-07 — TASK-199*
