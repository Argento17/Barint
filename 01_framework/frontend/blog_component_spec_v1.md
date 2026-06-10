# Bari Blog Component Spec — v1
**Created:** 2026-06-07
**Authority:** Content Agent (TASK-199), to be ratified by Design Agent
**Status:** ACTIVE — canonical pattern for all blog article pages
**Reference implementation:** olive oil article (`/blog/shemen-zayit`)

---

## Purpose

Defines the component architecture for Bari blog articles. Every article page uses this set of components. Components are layout-stable — prose content lives in the content file, not in components. A content author changing `src/lib/blog/<slug>-content.ts` must not need to touch any component file.

---

## File Locations

All blog components live at `src/components/blog/`. No blog-specific logic is permitted in `src/app/blog/`.

Pages live at `src/app/blog/<slug>/page.tsx`. Each page exports `metadata` and renders exactly one root component.

---

## Component Registry

### Layout / Structural

| Component | File | Props | Notes |
|---|---|---|---|
| `<HomeContainer>` | `src/components/home/section-frame.tsx` | `className?` | Shared layout container; max-width padding; not blog-specific |

---

### Article-Level Components

| Component | File | Props | Purpose |
|---|---|---|---|
| `<OliveOilArticle>` | `blog/olive-oil-article.tsx` | none | Root component for olive oil article — composes all sub-components. Pattern for all articles. |

Future articles follow this pattern: one root `<CategoryArticle>` component per article.

---

### Section Components (reusable across articles with typed props)

| Component | File | Input prop | Purpose |
|---|---|---|---|
| `<InsightBlock>` | `blog/olive-oil-article.tsx` (inline) | `{ quote: string; index?: number }` | Bold pull-quote with left border. Used 3× per article at structural inflection points. Motion: fade+slide-right. |
| `<FindingCard>` | `blog/olive-oil-article.tsx` (inline) | `{ title, finding, whyItMatters, index }` | Rounded card — title + finding + "למה זה משנה" sub-label. Motion: fade+slide-up. |
| `<BuyingGuideCard>` | `blog/olive-oil-article.tsx` (inline) | `{ signal, what, availability }` | 2-col grid card. Signal in CAPS. What + availability in body. |
| `<RecentArticleCard>` | `blog/olive-oil-article.tsx` (inline) | `{ href, title, description, category, readTime, cta, comingSoon }` | Linked or "coming soon" article teaser card. |
| `<ScienceSection>` | `blog/olive-oil-article.tsx` (inline) | `{ science: typeof oliveOilArticle.science }` | Full science narrative + formal citations list with live links. |

**Migration note:** The inline components above should be extracted to dedicated files when reused across ≥2 articles. Until then, keeping them co-located with their article reduces import complexity.

---

### Article-Specific Sub-Components

| Component | File | Data source | Purpose |
|---|---|---|---|
| `<OliveOilArticleHero>` | `blog/olive-oil-article-hero.tsx` | `oliveOilArticle.hero` + `.disclaimer` | Article header: eyebrow, H1, subtitle, meta, key stats bar, disclaimer. |
| `<OliveOilOriginChart>` | `blog/olive-oil-origin-chart.tsx` | `oliveOilArticle.originData` | Horizontal bar chart — origin country distribution. CSS bars (no external chart lib). |
| `<OliveOilTransparencyMatrix>` | `blog/olive-oil-transparency-matrix.tsx` | `oliveOilArticle.transparencyMatrix` | Full-width table — 13 Shufersal products × 4 disclosure columns. `CheckCircle2` / `XCircle` cells. Corpus-only: every row must have a BSIP2 record. |
| `<OliveOilExternalResearch>` | `blog/olive-oil-external-research.tsx` | `oliveOilArticle.externalResearch` | UC Davis stat card + YouTube embed (lazy-loaded, privacy-safe). |

---

## Design Tokens (blog context)

Blog articles use the same token set as comparison pages, with the following article-specific values:

| Token | Value | Where used |
|---|---|---|
| Article prose max-width | `max-w-3xl` (768px) | Lead, science, conclusion |
| Data section max-width | `max-w-4xl` (896px) | Transparency matrix, buying guide |
| Body text size | `text-base` / `text-lg` on md | Lead paragraphs, science prose |
| Body line-height | `leading-[1.8]` / `leading-[1.85]` | Hebrew prose |
| Section background (alt) | `bg-[#FFFFFF]` | Findings, science sections |
| Page background | `bg-[#F7F7F2]` | Root |
| InsightBlock border | `border-r-4 border-[#7A9450]` | RTL-aware: right border = visual left indent |
| FindingCard border | `border border-black/[0.07]` | Subtle separation |
| Section eyebrow | `font-mono text-[0.65rem] tracking-[0.24em] text-[#7A9450]/85` | All section headers |
| Citation background | `bg-[#F7F7F2]` with `border-black/[0.06]` | Science citations box |

---

## Motion Rules

| Component | Motion | Reduced-motion |
|---|---|---|
| `<InsightBlock>` | `opacity: 0→1, x: 12→0` | Skipped |
| `<FindingCard>` | `opacity: 0→1, y: 12→0` | Skipped |
| `<ScienceSection>` paragraphs | `opacity: 0→1, y: 8→0` staggered | Skipped |

Motion uses `whileInView` with `once: true` and a `-40px` margin. Delays stagger at `index * 0.04–0.05s`. All motion gates on `useReducedMotion()`.

---

## RTL Requirements

All blog components are RTL. Specific rules:

- `text-right` on all headers and body text blocks
- Border accent on `<InsightBlock>` is `border-r-4` (right side = visual left margin in RTL)
- Table column alignment: product name = `text-right`, data cells = `text-center`
- Navigation arrows use `ChevronLeft` / `ArrowLeft` (pointing right in RTL display)
- No `float` usage — use `flex` with `flex-row-reverse` or `dir="rtl"` as needed

---

## Layout Hierarchy (per section)

```
<main> (bg-[#F7F7F2], siteHeaderOffsetClass)
  <article>
    <ArticleHero />                     // white bg, border-b
    <HomeContainer>                     // Lead paragraphs
    <ScienceSection />                  // white bg, border-t, py-14/20
    <HomeContainer>                     // InsightBlock 1
    <HomeContainer>                     // Methodology box
    <section id="findings">             // white bg, border-y, py-14/20
    <div class="bg-[#F7F7F2]">         // Origin chart
    <HomeContainer>                     // InsightBlock 2
    <HomeContainer>                     // Transparency matrix
    <HomeContainer>                     // InsightBlock 3
    <div class="bg-[#F7F7F2]">         // External research
    <HomeContainer>                     // Buying guide + conclusion + CTA + recent
    <HomeContainer>                     // Footer
```

The alternating white / off-white backgrounds create visual rhythm without borders. Sections with data (charts, tables, research) sit in the off-white background; narrative and findings sit in white.

---

## Mobile Geometry

| Element | Mobile (375px) | Desktop (md+) |
|---|---|---|
| Transparency matrix | `overflow-x-auto` + `min-w-160` | full-width table |
| Origin chart bars | full-width | full-width |
| Buying guide cards | 1-col | 2-col `sm:grid-cols-2` |
| Recent articles | 1-col | 3-col `sm:grid-cols-3` |
| Key stats in hero | `flex gap-8` (may wrap) | `flex gap-8` |
| Science paragraphs | `text-base` | `text-lg` |

---

## Adding a New Article (checklist)

1. Create `src/lib/blog/<slug>-content.ts` — export `<categoryName>Article` following the typed shape in `blog_template_v1.md`.
2. Create `src/components/blog/<slug>-article.tsx` — compose `<InsightBlock>`, `<FindingCard>`, `<BuyingGuideCard>`, `<ScienceSection>`, and category-specific sub-components.
3. Create category-specific sub-components (hero, data chart/table, external research) under `src/components/blog/<slug>-*.tsx`.
4. Create `src/app/blog/<slug>/page.tsx` — export `metadata` + default component.
5. Add the article to `recentAnalyses.items` in the upstream article (or the blog index) to surface it.
6. Run leakage check and DICTA nakdan before handing to Frontend Agent.

---

## Corpus Scope Rule (component enforcement)

Components that render product data (`<TransparencyMatrix>`, `<OriginChart>`) must receive their data from the content file. The content file is the point of enforcement for corpus scope — components are display-only.

A component must never filter or augment the product list it receives. If the content file contains a row, the component renders it. If the row should not exist, it must be removed from the content file before publish. See `blog_template_v1.md §5b` for the corpus scope integrity rule.

---

## Extraction Backlog

These inline components should be extracted to standalone files when a second article needs them:

| Component | Trigger for extraction |
|---|---|
| `<InsightBlock>` | Any second article |
| `<FindingCard>` | Any second article |
| `<BuyingGuideCard>` | Any second article |
| `<RecentArticleCard>` | Any second article |
| `<ScienceSection>` | Any article with citations |

Extraction target: `src/components/blog/shared/`. Props stay identical — only the import path changes. Existing articles must be updated to import from `shared/`.

---

*Bari Blog Component Spec v1 — Content Agent — 2026-06-07 — TASK-199*
