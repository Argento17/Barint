# Bari Growth Foundation — Strategy v1

**Owner:** Marketing Agent  
**Scope:** Hebrew market only  
**Status:** Active — v1  
**Created:** 2026-05-31  
**Review date:** 2026-08-31

---

## North Star

Every Israeli consumer who stands in front of a supermarket shelf and wonders "which one is better?" should find Bari before they put anything in the cart. The growth system exists to make Bari the default answer to that question in Hebrew search.

Bari does not advertise. Bari earns attention by being more useful than anything else at that specific shelf moment.

---

## Market Framing

**Target user:** Hebrew-speaking Israeli adult, 25–55, shopping at Shufersal, Rami Levy, Carrefour, or Victory. Active on WhatsApp. Increasingly skeptical of marketing claims on packaging. Does not have time or expertise to decode ingredient lists.

**Category awareness:** Israeli food consciousness is high — "ללא שמן דקל", "ללא חומרים משמרים", "דיאטתי" are common shelf filters for consumers. Bari's differentiation is that it evaluates structural quality, not just surface claims.

**Search behavior:** Hebrew queries are shorter than English equivalents. Users often search the category name + "בריאות", "השוואה", or "הכי טוב". Brand-name queries are common because Israeli retail has dominant brands (תלמה, דנונה, טרה, שטראוס, ברמן, גד).

**Competitive gap:** No Hebrew-language product that provides cross-brand, cross-category comparison of food quality at scale. The closest alternatives are individual dietitian blog posts (personal opinion, not systematic) and the Yuka app (French, not Israeli-retail-optimized).

---

## 1. SEO Strategy

### 1.1 Core Positioning

Each comparison page at `/hashvaot/[category]` is a standalone SEO landing page. The site's SEO architecture is a hub-and-spoke model:

- **Hub:** `/hashvaot/` — category index (comparison directory)
- **Spokes:** `/hashvaot/[category]` — individual comparison pages (currently 5 live)
- **Future spokes:** sub-category pages, brand comparison pages, ingredient concern pages

The goal of the SEO layer is to intercept Hebrew search queries at the commercial investigation stage — when a user wants to compare options, not just learn about a category.

### 1.2 Technical SEO Requirements

| Item | Priority | Status |
|---|---|---|
| `hreflang="he"` + `lang="he"` on all pages | Critical | Verify implementation |
| `dir="rtl"` on `<html>` | Critical | Verify implementation |
| Structured data: `ItemList` schema per category page | High | Not yet implemented |
| Structured data: `Product` schema per product row | Medium | Future |
| Canonical tags on all category pages | High | Verify implementation |
| Open Graph tags with Hebrew `og:title` and `og:description` | High | Verify implementation |
| Core Web Vitals: LCP < 2.5s on mobile | High | Audit required |
| Sitemap includes all `/hashvaot/` routes | High | Verify generation |
| robots.txt allows all `/hashvaot/` routes | Critical | Verify |

**Priority action:** Run a technical SEO audit (`marketing/seo-audit`) against the live site before any content investment. Technical issues left unfixed negate content work.

### 1.3 On-Page SEO — Per Comparison Page

Each category page must satisfy these on-page requirements:

- `<title>`: `השוואת [category in Hebrew] — [year] | ברי` (e.g., "השוואת יוגורטים — 2026 | ברי")
- `<meta description>`: One sentence answering "מה הדף הזה עושה?" in consumer Hebrew. Max 155 chars. Example: "השוואנו 45 יוגורטים ישראליים לפי הרכב תזונתי. גלה איזה יוגורט עומד בפני הרכיבים שלו."
- `<h1>`: Category name in Hebrew — single, clear, above the fold
- CategoryHero text: consumer-facing, keyword-adjacent (e.g., naturally includes "יוגורט", "השוואה", "מוצרים")
- CategoryPrologue: 2–3 sentences with informational depth — provides context Google can use to classify the page
- MethodologyFooter: explains how the comparison works — builds E-E-A-T (expertise signals)

### 1.4 Link-Building Targets (Hebrew Market)

**Tier 1 — High-authority Israeli sites:**
- Walla! בריאות (health section) — product news, comparison coverage
- Ynet מגזין (lifestyle/food section) — consumer guides
- הארץ מדור צרכנות (Haaretz consumer section) — investigative food pieces

**Tier 2 — Authority blogs and communities:**
- Israeli dietitian blogs (דיאטנית, תזונאי) — offer data for their articles
- Facebook groups: "אמהות שאוהבות לאכול בריא", "ללא גלוטן ישראל"
- Parenting communities: Morim.co.il, Matnasim Facebook groups

**Tier 3 — Brand and product coverage:**
- Pitch comparison data to Israeli food/consumer journalists as a source, not as a product
- When a manufacturer launches a new product, Bari already has category context

**Tactic:** When Bari publishes a new category, email 3–5 Israeli dietitians offering the full dataset for their use, with attribution to bari.co.il. This converts research work into backlinks without paid placement.

### 1.5 Keyword Strategy by Stage

**Stage 1 (Now) — Capture existing demand for live categories:**
Focus exclusively on the 5 live categories. Optimize each page for the primary category query cluster. See `keyword_universe_v1.md` for full term lists.

**Stage 2 (Q3 2026) — Expand into brand and product queries:**
When category pages have established rankings, add structured data for individual products so brand-name queries ("תלמה 0% שומן") can surface Bari's comparison context in SERPs.

**Stage 3 (Q4 2026) — Concern-based acquisition:**
Create dedicated pages for high-frequency concern queries: "מוצרים ללא שמן דקל", "מזון מעובד רשימה ישראל". These pages link back to relevant category comparisons.

---

## 2. Newsletter Strategy

### 2.1 Purpose

The newsletter serves one function: convert first-time visitors into recurring users. Bari's comparison pages are updated as new products are added — the newsletter tells people when to come back.

The newsletter is NOT a marketing channel in the promotional sense. It is a product extension — it delivers a weekly dose of the Bari experience to people who already trust it.

### 2.2 Format — "מה שנמצא השבוע"

**Name:** מה שנמצא (What we found)  
**Cadence:** Weekly, sent Sunday evening (Israeli family prep time before the week)  
**Length:** Short — 3 sections, readable in 90 seconds  
**Language:** Hebrew, RTL

**Standard issue structure:**

```
[1] ממצא השבוע (The finding of the week)
    One specific, surprising finding from the current category data.
    Example: "מתוך 45 יוגורטים שבחנו, 31 מכילים עמילן מוסף — כולל חלק מהאחיות שמתיימרות להיות 'טבעיות'."
    Link to the relevant comparison page.

[2] שאלה מהמדף (Question from the shelf)
    One question Bari can answer that users might not think to ask.
    Example: "מה ההבדל בין יוגורט 0% לבין יוגורט 3% מבחינת הרכב הרכיבים — לא קלוריות?"
    Answer in 2–3 sentences. Link to category if relevant.

[3] מה בא אחר כך (What's coming)
    One-line preview of the next category Bari is working on.
    Keeps subscribers curious without making promises.
```

### 2.3 Sign-Up Placement

| Placement | Trigger | Priority |
|---|---|---|
| Inline in CategoryPrologue area | After 60% scroll depth on category page | 1 |
| Fixed bottom banner | After 3 minutes on page OR on exit intent | 2 |
| Homepage (when exists) | Above the fold | 3 |

**Copy for sign-up CTA:** "אחת לשבוע — ממצא אחד מהמדף הישראלי. ללא שיווק, ללא ספאם."

**Constraint:** Do not gate comparison data behind an email wall. The comparison pages must remain fully accessible. Sign-up is opt-in only, never required.

### 2.4 Growth Targets

| Milestone | Target | Method |
|---|---|---|
| Months 1–3 | 250 subscribers | In-page sign-up, organic |
| Months 4–6 | 750 subscribers | + dietitian referrals, WhatsApp group seeding |
| Month 12 | 2,000 subscribers | + newsletter mentions in food media |

**Platform requirement:** Must support RTL Hebrew email rendering. Evaluated options: Mailchimp (RTL support via custom template), Loops.so, or Brevo. Confirm before implementation.

### 2.5 Content Calendar — Newsletter

Issues are tied to category data cycles. When a category is re-run (new products added, scores updated), that produces 2–3 newsletter issues worth of material.

| Month | Category focus | Issue theme |
|---|---|---|
| June 2026 | מעדנים | Summer desserts — what's actually in them |
| July 2026 | יוגורטים | Back-to-school: family yogurt guide |
| August 2026 | חטיפים | Summer snack bars: which ones earned their "health" label |
| September 2026 | לחם | Rosh Hashana preparation: bread and baked goods edition |
| October 2026 | New category TBD | Based on pipeline |

---

## 3. Content Strategy

### 3.1 Content Pillars

Bari produces two types of content: **core content** (the comparison pages — product of the pipeline) and **editorial content** (articles, social posts, newsletter issues — built on top of the pipeline data).

Editorial content is organized into four pillars:

**Pillar 1 — Category comparisons (Core SEO traffic)**
The comparison pages themselves. Each page is an authoritative, data-driven comparison of all major products in a category. This is Bari's primary content asset.

**Pillar 2 — Ingredient education (Authority building)**
Short articles explaining what specific ingredients are, why they matter in specific product categories, and what Bari's data shows about their prevalence. Written in consumer Hebrew, no framework vocabulary.

Examples:
- "שמן דקל: כמה מוצרי יוגורט בישראל מכילים אותו?"
- "מה זה עמילן מוסף ולמה הוא מופיע בכל כך הרבה מעדנים?"
- "ממתיקים מלאכותיים בחטיפי בריאות — מה הנתונים אומרים?"

**Pillar 3 — Surprising findings (Virality and sharing)**
Short, specific, counter-intuitive findings from the data. Designed for social sharing in WhatsApp groups and Facebook.

Format: one surprising finding per post, with a link to the full comparison.

Examples:
- "חטיף שמוכר כ'ללא סוכר' מכיל 5 סוגי ממתיקים שונים"
- "3 מתוך 10 יוגורטים טבעיים מכילים חלבון מי גבינה מוסף — לא כתוב על האריזה"
- "הלחם הכי מתוק שבחנו הוא לחם לחם לבן רגיל — לא הלחם 'עם קינמון'"

**Pillar 4 — Seasonal and event-driven content (Timely spikes)**
Israeli calendar creates predictable demand spikes:
- ראש השנה: "מה לקנות לשולחן החג בלי להצטער" — מעדנים, לחם
- פסח: "מה מסתתר בתחליפי החמץ?" — potential new category
- חזרה ללימודים: "ארוחת הביניים הכי טובה — נתונים"
- Summer: "חטיפים לפיקניק — מה שווה"

### 3.2 Content Production Cadence

| Content type | Frequency | Owner |
|---|---|---|
| Comparison page update (new products) | Per category cycle | Data Agent → Content Agent |
| Newsletter issue | Weekly | Content Agent + Marketing Agent |
| Pillar 2 ingredient article | 1 per month | Content Agent |
| Pillar 3 social finding | 2–3 per week | Marketing Agent |
| Pillar 4 seasonal piece | Per Israeli calendar | Content Agent + Marketing Agent |

### 3.3 Content Voice Constraints

These apply to all editorial content (not just comparison pages):

- No health claims. "מוצר X מכיל פחות מרכיבים מעובדים מ-Y" is allowed. "מוצר X בריא יותר" is not.
- No moralizing. Bari describes what's in the product, not what the consumer should do.
- No framework vocabulary in any consumer-facing content: NOVA, BSIP, cap, floor, structural_class, matrix_integrity.
- Hebrew-first. All consumer content originates in Hebrew, not translated from English.
- Specific over generic. "31 מתוך 45 יוגורטים" is better than "רוב היוגורטים".

### 3.4 Distribution Channels

| Channel | Content type | Goal |
|---|---|---|
| Google organic | Comparison pages, ingredient articles | Primary acquisition |
| WhatsApp (shared links) | Pillar 3 findings, seasonal pieces | Viral distribution |
| Instagram | Pillar 3 findings (visual format) | Awareness |
| Facebook groups | Pillar 3 findings, comparison links | Community distribution |
| Email newsletter | Weekly digest | Retention |
| Dietitian referrals | Category datasets, Pillar 2 articles | Authority + backlinks |

---

## 4. Comparison-Page Acquisition Strategy

### 4.1 Current Asset Inventory

Bari currently has 5 live comparison pages serving as SEO landing pages:

| Page | Route | Products | SEO status |
|---|---|---|---|
| מעדנים | `/hashvaot/maadanim` | ~90 | Live |
| לחם | `/hashvaot/bread` | ~80 | Live |
| חטיפים | `/hashvaot/snack-bars` | 53 | Live |
| יוגורטים | `/hashvaot/yogurts` | 45 | Live |
| חלב | `/hashvaot/milk-comparison` | 20 | Live (legacy) |

Each page already functions as a comparison landing page. The acquisition strategy is to expand this inventory systematically.

### 4.2 Expansion Tiers

**Tier A — New full categories (Highest value, pipeline required)**
New `/hashvaot/[category]` pages. Each requires full BSIP0–BSIP2 pipeline execution. Priority candidates based on search demand and Israeli retail density:

| Category | Hebrew | Rationale |
|---|---|---|
| Breakfast cereals | דגני בוקר | High search volume, parent decision point |
| Baby food | מזון לתינוקות | Extreme purchase anxiety, zero tolerance for error |
| Plant-based alternatives | תחליפי בשר | Growing Israeli market, heavy marketing claims |
| Cottage and soft cheeses | גבינות רכות | High daily consumption, complex ingredient landscape |
| Granola and muesli | גרנולה | Adjacent to snack bars, high "health" claim density |

**Tier B — Sub-category filter pages (Medium value, frontend work required)**
Dedicated pages for sub-segments within existing categories. These capture specific intent queries that the full comparison page doesn't rank for.

Examples:
- `/hashvaot/yogurts?type=natural` → standalone page: "יוגורט טבעי — השוואה"
- `/hashvaot/snack-bars?type=protein` → standalone page: "חטיפי חלבון — השוואה"
- `/hashvaot/maadanim?brand=danone` → standalone page: "מוצרי דנונה — השוואה"

**Implementation note:** These require Product Agent approval and Frontend Agent implementation. They are not marketing pages — they are product pages that extend the comparison feature.

**Tier C — Concern-based landing pages (Medium value, content-only)**
Pages targeting ingredient-concern queries. These pages surface relevant products from existing categories, filtered by a specific concern signal.

| Page concept | Target query | Source category |
|---|---|---|
| מוצרים ללא שמן דקל | "מוצרים ללא שמן דקל ישראל" | All categories |
| מוצרים ללא ממתיקים מלאכותיים | "ממתיקים מלאכותיים מזיקים" | יוגורט, חטיפים |
| מזון מינימלי מעובד | "מזון לא מעובד" | All categories |
| מוצרים עם הכי פחות רכיבים | "מרכיבים פשוטים" | All categories |

**Tier D — Brand comparison pages (Lower priority, long-tail)**
Head-to-head pages for the most-searched brand pairs within a category.

Examples:
- "תלמה מול דנונה — יוגורטים"
- "אחלה מול גד — חלב"
- "שי עוגיות מול ערד — חטיפים"

These are long-tail but high commercial intent. Build only after Tier A and B are established.

### 4.3 Priority Sequencing

| Quarter | Focus | Deliverable |
|---|---|---|
| Q2 2026 | Optimize existing 5 pages for SEO (on-page, structured data) | Technical audit → implementation |
| Q3 2026 | Launch 1 new full category (recommended: דגני בוקר) | New comparison page + newsletter campaign |
| Q3 2026 | Build 3–5 sub-category filter pages for highest-traffic categories | Frontend implementation |
| Q4 2026 | Launch 2 concern-based landing pages | Content-only, no pipeline required |
| Q4 2026 | Launch 2nd new full category | Based on pipeline readiness |

### 4.4 Page Quality Standards for SEO

Every comparison page — existing and new — must meet this standard before it is treated as an SEO asset:

- At minimum 20 products in the comparison (thin comparison pages do not rank)
- Hebrew meta title and description (not auto-generated)
- CategoryPrologue text is substantive — at least 80 words of consumer-relevant context
- MethodologyFooter explains the comparison logic in consumer terms
- Structured data (`ItemList`) implemented
- Mobile load time under 3 seconds
- No broken product images

---

## 5. 90-Day Execution Priorities

| Week | Action | Owner |
|---|---|---|
| 1–2 | Technical SEO audit of all 5 live pages | Marketing Agent + Frontend Agent |
| 1–2 | Set up newsletter platform (Hebrew RTL) | Marketing Agent |
| 3–4 | Fix critical technical SEO issues | Frontend Agent |
| 3–4 | Write Hebrew meta titles/descriptions for all 5 pages | Content Agent |
| 5–6 | Implement sign-up CTA on comparison pages | Frontend Agent |
| 5–6 | Send first newsletter issue | Marketing Agent |
| 7–8 | Implement `ItemList` structured data | Frontend Agent |
| 7–12 | Publish 2 Pillar 2 ingredient articles | Content Agent |
| 7–12 | Begin outreach to 5 Israeli dietitians | Marketing Agent |

---

## 6. Metrics

| Metric | Baseline | 90-day target | 12-month target |
|---|---|---|---|
| Organic sessions (Hebrew) | TBD after audit | +40% | 10,000/month |
| Average position for category keywords | TBD | Top 10 for 3+ categories | Top 5 for all live categories |
| Newsletter subscribers | 0 | 250 | 2,000 |
| Backlinks from Israeli domains | TBD | +10 referring domains | +50 referring domains |
| Comparison pages (live) | 5 | 5 (optimized) | 8–10 |
| Newsletter open rate | — | >40% (Hebrew consumer norm) | >45% |

---

## Hard Rules (Marketing Agent)

1. No campaign for any category before Product Agent go-live approval.
2. No health claims in any marketing copy or article.
3. No framework vocabulary (NOVA, BSIP, cap, floor, structural_class) in any consumer-facing output.
4. Newsletter sign-up is always opt-in. No gating of comparison data.
5. Hebrew-first. All consumer content originates in Hebrew.
6. Do not publish Pillar 2 or Pillar 4 articles without Nutrition Agent accuracy review.
7. SEO technical fixes require Frontend Agent implementation — Marketing Agent does not edit `C:\Users\HP\bari\src\` directly.
