---
id: TASK-199
title: "Olive Oil Blog Post — first full-depth article + blog template for all future posts"
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-06
depends_on: []
blocks: []
roadmap_impact: true
cc_reviewed: false
work_type: editorial-product
drift_ack: false
---

# TASK-199 — Olive Oil Blog: First Deep-Dive Article + Blog Template

## Context

The olive oil comparison page was removed (2026-06-06) because uniform 60/C scores across all 13 products produce no meaningful ranking. The real story is richer: Israeli labeling law, harvest date opacity, authenticity gaps, origin mapping, and why nutritional purity alone cannot differentiate a category where processing level is structurally capped.

This task builds the **first full-depth blog article** on olive oil — and simultaneously defines the **template, component architecture, and editorial standard** that all future Bari blog posts inherit from.

---

## Owner mapping

| Layer | Owner |
|---|---|
| Overall coordination | Content Agent |
| Nutritional science + findings | Nutrition Agent |
| Data / charts / corpus analysis | Data Agent |
| Visual layout + component spec | Design Agent |
| SEO + distribution strategy | Marketing Agent |

All five agents must deliver. Content Agent integrates, reconciles, and signs off on the final article.

---

## Acceptance criteria

- [ ] Article length: ≥ 2,400 Hebrew words (≈ 2 printed pages at standard density)
- [ ] At least 4 scientific/regulatory sources cited (with inline references)
- [ ] At least 2 data-driven charts or visual data tables built from the Bari corpus
- [ ] At least 2 editorial insight cards (styled, not just callout text)
- [ ] A working article template extracted and documented so future posts can inherit it
- [ ] SEO brief delivered: target keyword cluster, meta title, meta description, URL slug
- [ ] Design spec delivered: section hierarchy, component list, spacing rules
- [ ] All corpus claims cross-verified against `02_products/olive_oil/bsip2_scored/olive_oil_bsip2_20260606.json`

---

## Phase 1 — Research + Findings (Nutrition Agent + Data Agent)

### Nutrition Agent deliverables

Answer each question with evidence (peer-reviewed sources or regulatory documents):

1. **Why does harvest date matter?** What does the science say about polyphenol degradation over time post-harvest? What is the typical degradation timeline?
2. **What does "כתית מעולה" (extra virgin) actually guarantee?** What are the Israeli vs EU/IOC standards? What do they test, what do they not test?
3. **What is the origin opacity problem?** Why does "blend of EU olives" on an Israeli label provide near-zero traceability?
4. **Polyphenols, oleocanthal, and oleacein** — what does the evidence actually say about health relevance vs marketing claims?
5. **What are the real consumer-relevant differentiation signals** that a label can and cannot tell you?

Sources to draw from: PubMed, EFSA, Israeli Standards Institute (SII), IOC (International Olive Council), EU regulation 29/2012.

### Data Agent deliverables

Using `02_products/olive_oil/bsip2_scored/olive_oil_bsip2_20260606.json` and `bari-web/src/data/comparisons/olive_oil_frontend_v1.json`:

1. **Origin distribution chart**: Israel / Italy / Spain / Unknown — counts and % of shelf
2. **Label transparency matrix**: For each of the 13 products, which of {harvest_date, PDO/PGI claim, origin_country_back, olive_grade_back} are present vs absent — render as a table
3. **Score distribution note**: confirm all 11 sufficient products at 60/C; 2 insufficient — explain why uniform score is itself a finding
4. **Price-per-liter vs transparency gap** (if price data is available from integrations/shufersal): is premium pricing correlated with any additional label disclosure?

---

## Phase 2 — Article Architecture (Design Agent + Content Agent)

### Design Agent deliverables

Deliver a **section hierarchy spec** for the article page, covering:

1. Article hero — what it contains, max height, whether a pull quote belongs here
2. Section types and their visual treatment:
   - Narrative section (standard prose)
   - Data section (chart or table with caption)
   - Insight card (key finding, styled box — NOT a comparison row)
   - Source citation section (footnote or inline?)
   - Pull quote (when to use, styling rules)
3. Mobile-first layout rules: how charts collapse at 375px
4. Typography rules for the article context (different from the comparison page spec)
5. Navigation within long articles: section anchors? floating TOC?
6. **Reusable component list**: name each component, where it lives (`src/components/blog/`), what props it accepts
7. Define the **blog template** — the NextJS page structure every future article inherits

This spec becomes the `blog_template_v1.md` governing document for all future Bari articles.

### Content Agent

- Deliver a **Hebrew article outline** (section titles + 2–3 sentence summary of each section's argument) before writing full prose
- Outline must be reviewed and confirmed before prose begins
- Article must follow the Bari editorial principles: insight-first, finding-led, consumer-lens, assertive but not accusatory

---

## Phase 3 — Full Article Draft (Content Agent)

Write the complete Hebrew article integrating:
- Nutrition Agent's scientific findings and citations
- Data Agent's corpus charts and tables
- Design Agent's section structure and component spec

Article structure (suggested — Content Agent may adjust if the outline review changes it):

1. **Hook / lede** — the key finding in one stark sentence. e.g. "בדקנו 13 שמני זית ישראלים. כולם ציון זהה. הסיבה לא מחמיאה לאף אחד."
2. **Why uniform scores are a finding, not a failure** — NOVA-1, cooking oil structural cap, what this reveals about the category
3. **What the label doesn't tell you** — harvest date law gap, IOC standard, Israeli standard delta
4. **Origin opacity** — "blend of EU olives" as near-zero information; data chart of origin distribution from the Bari shelf scan
5. **The science of freshness** — polyphenol degradation, what harvest date actually predicts, what a consumer can realistically infer
6. **Extra virgin: what it guarantees and what it doesn't** — chemical tests vs sensory tests vs provenance
7. **Insight card: What to actually look for when buying** — concrete, actionable, honest about limitations
8. **Label transparency matrix** — the table from Phase 1 Data: which products disclose what
9. **Closing** — what Bari can and can't tell you; the framing consistent with BEV-001

---

## Phase 4 — SEO Brief (Marketing Agent)

Deliver:
1. Primary keyword: Hebrew search intent for "שמן זית" content (volume, competition)
2. Secondary keywords: related Hebrew queries the article should address
3. URL slug recommendation (Hebrew or English?)
4. Meta title (≤60 chars) + meta description (≤155 chars)
5. Structured data recommendation: Article schema, FAQ schema if applicable
6. Distribution plan: which channels, what timing, what hook per channel
7. Internal link targets: which existing Bari pages should link TO this article, and from where

---

## Phase 5 — Blog Template Documentation (Design Agent + Content Agent)

After the article is drafted and approved, extract the template:

1. `01_framework/editorial/blog_template_v1.md` — editorial standard: section types, word count minimums, source requirements, insight card rules, lede standard
2. `01_framework/frontend/blog_component_spec_v1.md` — component list, file paths, props, design tokens for blog context
3. Update `component_build_sequence_v1.md` to reference the blog template as the authority for article pages (distinct from comparison pages)

---

## Data assets available (do not re-scrape)

| Asset | Path |
|---|---|
| BSIP2 scored corpus | `02_products/olive_oil/bsip2_scored/olive_oil_bsip2_20260606.json` |
| Frontend JSON (BariProductVM[]) | `bari-web/src/data/comparisons/olive_oil_frontend_v1.json` |
| D5/D6 annotation spec | `01_framework/olive_oil_d5_d6_annotation_spec_v1.md` |
| Corpus purity report | `02_products/olive_oil/bsip2_scored/corpus_purity_report_v1.md` |
| External integrations | `integrations/` — literature client (PubMed, EuropePMC), pubchem, il_gov_data |

---

## Tripwires

This task trips **no owner tripwires** — it is editorial content (not a score change, not an irreversible consumer-facing launch, not a new program start). The blog post goes live as a draft/PR; the owner reviews before publish.

---

## Return block (to be filled by Content Agent at completion)

```
return_block:
  claims:
    - article_word_count: <actual count>
    - sources_cited: <count>
    - charts_delivered: <count>
    - insight_cards: <count>
    - template_doc_created: true/false
    - seo_brief_delivered: true/false
    - design_spec_delivered: true/false
  artifacts:
    - path: bari-web/src/app/blog/shemen-zayit/page.tsx
    - path: bari-web/src/lib/blog/olive-oil-content.ts
    - path: 01_framework/editorial/blog_template_v1.md
    - path: 01_framework/frontend/blog_component_spec_v1.md
  status: RETURNED
```
