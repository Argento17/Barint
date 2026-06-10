# Bari Blog Template — Editorial Standard v1
**Created:** 2026-06-07
**Authority:** Content Agent (TASK-199)
**Status:** ACTIVE — applies to all Bari blog articles from this date forward
**Applies to:** TASK-200 through TASK-206 and all future articles

---

## Purpose

This document defines the editorial template for every Bari deep-dive article. It was extracted from the olive oil article (TASK-199), which is the canonical reference implementation. Future content agents follow this template. Deviations require a registry entry.

---

## 1. What a Bari Article Is

A Bari article is a shelf analysis — not a product review, not a health guide, not a listicle. It answers one editorial question: **what does the data actually say, and what does the label not say?**

Every article must be grounded in a real corpus scan. No article may be written without data artifacts to support its claims.

---

## 2. Required Sections (in order)

Each section maps to a named sub-component. The content file (`src/lib/blog/<slug>-content.ts`) contains the prose. The component is layout-stable.

| # | Section | Content key | Component | Required |
|---|---|---|---|---|
| 1 | Hero | `hero{}` | `<ArticleHero />` | Yes |
| 2 | Lead | `lead[]` | inline in `<Article />` | Yes |
| 3 | Science/Background | `science{}` | `<ScienceSection />` | Yes if citations exist |
| 4 | Grade guarantees | `extraVirginGuarantees{}` (or category equivalent) | inline section | Yes — what the grade standard does and does not guarantee |
| 5 | Insight block 1 | `editorialInsights[0]` | `<InsightBlock />` | Yes |
| 6 | Methodology | `methodology{}` | inline `<section id="methodology">` | Yes |
| 7 | Findings | `findings{items[]}` | `<FindingCard />` per item | Yes — min 3 items |
| 8 | Data chart / matrix | `originData{}` or `transparencyMatrix{}` | `<DataChart />` or `<TransparencyMatrix />` | Yes — min 1 |
| 9 | Insight block 2 | `editorialInsights[1]` | `<InsightBlock />` | Yes |
| 10 | External research | `externalResearch{}` | `<ExternalResearch />` | Recommended |
| 11 | Buying/action guide | `buyingGuide{}` | `<BuyingGuideCard />` per item | Yes |
| 12 | Insight block 3 | `editorialInsights[2]` | `<InsightBlock />` | Yes |
| 13 | Conclusion | `conclusion{}` | inline `<section id="conclusion">` | Yes |
| 14 | CTA block | `conclusion.cta` | inline `<aside>` | Yes |
| 15 | Recent articles | `recentAnalyses{}` | `<RecentArticleCard />` | Yes |
| 16 | Footer | — | inline `<footer>` | Yes |

---

## 3. Minimums

| Criterion | Minimum |
|---|---|
| Article word count (Hebrew prose) | ≥ 2,400 words |
| Cited scientific or regulatory sources | ≥ 4 |
| Data-driven charts or structured tables | ≥ 2 |
| Editorial insight blocks | ≥ 3 |
| Findings items | ≥ 3 |
| Buying guide signals | ≥ 3 |

---

## 4. Content File Structure

Every article has exactly one content file at:

```
src/lib/blog/<slug>-content.ts
```

The file exports a single `const` object with the slug as part of its name (e.g., `oliveOilArticle`, `milkAnalysisArticle`). The export shape:

```typescript
export const <categoryName>Article = {
  slug: string,
  hero: { eyebrow, title, subtitle, meta },
  disclaimer: string,
  lead: string[],            // 3–5 paragraphs
  editorialInsights: [string, string, string],  // exactly 3
  science: {                 // omit only if zero citations exist
    title, subtitle,
    paragraphs: string[],
    citations: Array<{ id, short, full, url, claim }>,
  },
  findings: {
    title, subtitle,
    items: Array<{ title, finding, whyItMatters }>,
  },
  // ...category-specific data sections (originData, transparencyMatrix, etc.)
  externalResearch: { ... },
  buyingGuide: {
    title,
    items: Array<{ signal, what, availability }>,
    caveat: string,
  },
  conclusion: {
    title,
    paragraphs: string[],
    cta: string,
  },
  methodology: {
    title,
    steps: Array<{ title, text }>,
    footnote: string,
  },
  recentAnalyses: {
    title,
    items: Array<{ slug, href, title, description, category, readTime, cta, comingSoon }>,
  },
} as const;
```

---

## 5. Editorial Standards

### Lede (hero title)
- Single stark sentence. Finding-first. No generic framing.
- Pattern: `[Quantity]. [Quantity]. [Stark negative finding].`
- Example: `"12 מותגים. 4 רשתות. אפס גילויים על תאריך הקציר."`

### Lead paragraphs
- 3–5 paragraphs. Each paragraph = one idea.
- First paragraph: why Bari can/cannot score this category + what the real story is.
- Second paragraph: the core finding stated plainly.
- Third paragraph: a surprising or counterintuitive observation from the data.
- Final paragraph: what this article does and does not do.

### Editorial insight blocks
- Three per article, placed at structural inflection points (after lead, after origin chart, after transparency matrix).
- Each is a single declarative sentence — the sharpest version of a finding.
- No hedging, no "it seems," no em-dash as connector.
- Not the same content as a finding card. The insight block is the distilled take; the finding card has the supporting detail.

### Finding cards
- Title: 4–8 words, declarative.
- Finding: 2–3 sentences. The observation. Scoped to the dataset.
- "למה זה משנה": 1–2 sentences. Why the gap between what the label says and what it doesn't say matters to a consumer.
- No prescription language. No "you should buy" or "avoid."

### Science section
- Minimum 3 narrative paragraphs.
- Each cited claim inline-referenced via `[C#]` id — rendered in citations list below the prose.
- Citation format: short (display), full (archival), url (live link), claim (what it supports in the article).
- Claims must be traceable to the actual source. No paraphrase that overstates the finding.

### Buying guide
- Signal, not recommendation.
- "What it tells you" + "how available is it on the Israeli shelf."
- Always close with a caveat explaining what no signal can guarantee.

### Conclusion
- 3 paragraphs.
- First: what Bari can say about this category.
- Second: what Bari cannot say, and why (data boundary, not apology).
- Third: the single actionable truth a consumer should take away.

---

## 5b. Corpus Scope Integrity Rule (added 2026-06-07 after TASK-199 CC gap)

**An article may only make quantitative claims about products that appear in the scored BSIP2 corpus for that run.**

Specific prohibitions:
- The hero, subtitle, and meta line count must match the corpus count exactly.
- The transparency matrix may only include rows for products with a corpus record (`product_id` in the scored JSON).
- Origin/distribution chart slices may only include products from the corpus.
- If a finding uses a number ("X מוצרים", "Y רשתות"), that number must be traceable to the corpus.

Unscored retailers may appear in contextual narrative only (e.g., "other Israeli retailers carry primarily domestic brands") — never in data claims.

Violation of this rule is a **CC blocking gap** and prevents task closure.

---

## 6. Forbidden in All Articles

The following must never appear in consumer-facing article text:

| Term | Why forbidden |
|---|---|
| NOVA | Internal classification term |
| BSIP, BSIP2, D1–D6 | Framework internals |
| cap, floor, penalty, weight | Scoring vocabulary |
| structural_class, dimension | Architecture vocabulary |
| "בריא יותר" / "מומלץ" | Prescription language |
| raw score mechanics (e.g. "68.2 נקודות") | Scores appear as `72/B` only |
| "הכי טוב" without scope | Claim without bounds |
| Alarmist language (רעיל, מסוכן) | Not Bari's editorial register |

---

## 7. Tone

Bari sounds like a journalist who checked before publishing. Calm. Precise. Bounded.

The finding earns its place. If a paragraph cannot be traced to the data, it does not belong in the article.

---

## 8. Page-level requirements

Every article page (`src/app/blog/<slug>/page.tsx`) must include:

| Requirement | Format |
|---|---|
| `metadata.title` | ≤60 chars, Hebrew, ends with `\| Bari` |
| `metadata.description` | ≤155 chars, Hebrew, finding-led |
| `metadata.openGraph` | `{ title, description, type: "article" }` |
| SEO comment block | Inline comment with: primary keyword, secondary keywords, URL slug note |

---

## 9. Downstream Posts (TASK-200 to TASK-206)

| Task | Category | Slug | Corpus anchor |
|---|---|---|---|
| TASK-200 | לחם | /blog/lechem | real_bread_retail_003_v1 |
| TASK-201 | יוגורט | /blog/yogurt | bsip2_run_yogurt_003 |
| TASK-202 | חומוס | /blog/humus | TBD |
| TASK-203 | גבינות מרוחות | /blog/gevina-merucha | TBD |
| TASK-204 | מעדנים | /blog/maadanim | canonical reference |
| TASK-205 | חלב | /blog/chalav | run_005_headpin (frozen) |
| TASK-206 | חטיפי חלבון | /blog/chatif-chalvon | snacks corpus v2 |

Each downstream post follows this template. The slug, hero, and findings adapt to the category. The component structure is identical.

---

## 10. Acceptance Gate

Before a blog article can be handed off to Frontend Agent for publishing:

- [ ] Word count ≥ 2,400 Hebrew words
- [ ] ≥ 4 citations with live URLs verified
- [ ] ≥ 2 data sections (chart or table) grounded in a named corpus artifact
- [ ] ≥ 3 editorial insight blocks, each a single declarative sentence
- [ ] No forbidden terms (see section 6)
- [ ] Leakage check run via `hebrew_readability.analyze()` — `is_clean = True`
- [ ] DICTA nakdan check run on hero title, subtitle, and all insight block text
- [ ] Page metadata complete (title ≤60, description ≤155, openGraph)
- [ ] Content file follows the typed export shape in section 4
- [ ] Nutrition Agent sign-off on any claim involving a health mechanism
- [ ] Product Agent sign-off on any market-positioning statement

---

*Bari Blog Template v1 — Content Agent — 2026-06-07 — TASK-199*
