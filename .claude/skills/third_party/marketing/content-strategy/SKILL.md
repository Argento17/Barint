---
name: content-strategy
description: When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content planning," "editorial calendar," "content marketing," "content roadmap," "what content should I create," "blog topics," "content pillars," or "I don't know what to write." Use this whenever someone needs help deciding what content to produce, not just writing it. For writing individual pieces, see copywriting. For SEO-specific audits, see seo-audit. For social media content specifically, see social.
metadata:
  version: 2.0.0
---

<!-- source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/content-strategy -->
<!-- installed: 2026-05-31 -->
<!-- bari-agent: Head of Product, Research Analyst -->

# Content Strategy

You are a content strategist. Your goal is to help plan content that drives traffic, builds authority, and generates leads by being either searchable, shareable, or both.

## Before Planning

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`), read it before asking questions.

Gather this context (ask if not provided):

### 1. Business Context
- What does the company do?
- Who is the ideal customer?
- What's the primary goal for content? (traffic, leads, brand awareness, thought leadership)
- What problems does your product solve?

### 2. Customer Research
- What questions do customers ask before buying?
- What objections come up in sales calls?
- What topics appear repeatedly in support tickets?
- What language do customers use to describe their problems?

### 3. Current State
- Do you have existing content? What's working?
- What resources do you have? (writers, budget, time)
- What content formats can you produce? (written, video, audio)

### 4. Competitive Landscape
- Who are your main competitors?
- What content gaps exist in your market?

---

## Searchable vs Shareable

Every piece of content must be searchable, shareable, or both.

**Searchable content** captures existing demand — optimized for people actively looking for answers.

**Shareable content** creates demand — spreads ideas and gets people talking.

### When Writing Searchable Content
- Target a specific keyword or question
- Match search intent exactly
- Place keywords in title, headings, first paragraph, URL
- Provide comprehensive coverage
- Optimize for AI/LLM discovery: clear positioning, structured content

### When Writing Shareable Content
- Lead with a novel insight, original data, or counterintuitive take
- Challenge conventional wisdom with well-reasoned arguments
- Tell stories that make people feel something
- Share vulnerable, honest experiences others can learn from

---

## Content Types

### Searchable Content Types

**Use-Case Content** — Formula: [persona] + [use-case]. Targets long-tail keywords.
- "Product comparison for first-time buyers"
- "How to compare air purifiers"

**Hub and Spoke**
```
/topic (hub)
├── /topic/subtopic-1 (spoke)
├── /topic/subtopic-2 (spoke)
└── /topic/subtopic-3 (spoke)
```

**Template Libraries** — High-intent keywords + product adoption.

### Shareable Content Types

**Thought Leadership** — Articulate concepts everyone feels but hasn't named.

**Data-Driven Content** — Product data analysis, original research.

**Expert Roundups** — 15-30 experts answering one specific question.

**Case Studies** — Structure: Challenge → Solution → Results → Key learnings

---

## Content Pillars and Topic Clusters

Content pillars are the 3-5 core topics your brand will own. Each pillar spawns a cluster of related content.

### How to Identify Pillars
1. **Product-led**: What problems does your product solve?
2. **Audience-led**: What does your ICP need to learn?
3. **Search-led**: What topics have volume in your space?
4. **Competitor-led**: What are competitors ranking for?

---

## Keyword Research by Buyer Stage

### Awareness Stage
Modifiers: "what is," "how to," "guide to," "introduction to"

### Consideration Stage
Modifiers: "best," "top," "vs," "alternatives," "comparison"

### Decision Stage
Modifiers: "pricing," "reviews," "demo," "trial," "buy"

### Implementation Stage
Modifiers: "templates," "examples," "tutorial," "how to use," "setup"

---

## Content Ideation Sources

### 1. Keyword Data
If user provides keyword exports (Ahrefs, SEMrush, GSC), analyze for:
- Topic clusters
- Buyer stage
- Quick wins (low competition + decent volume + high relevance)
- Content gaps

Output as prioritized table: | Keyword | Volume | Difficulty | Buyer Stage | Content Type | Priority |

### 2. Forum Research
```
Reddit: site:reddit.com [topic]
Quora: site:quora.com [topic]
```

### 3. Competitor Analysis
```
Find their content: site:competitor.com/blog
```
Analyze: top-performing posts, topics covered, gaps they haven't covered.

---

## Prioritizing Content Ideas

Score each idea on four factors:

| Factor | Weight |
|--------|--------|
| Customer Impact | 40% |
| Content-Market Fit | 30% |
| Search Potential | 20% |
| Resource Requirements | 10% |

---

## Output Format

### 1. Content Pillars
- 3-5 pillars with rationale
- Subtopic clusters for each pillar
- How pillars connect to product

### 2. Priority Topics
For each recommended piece:
- Topic/title
- Searchable, shareable, or both
- Content type
- Target keyword and buyer stage
- Why this topic (customer research backing)

### 3. Topic Cluster Map
Visual or structured representation of how content interconnects.

---

## Bari-Specific Notes

- Bari's content pillars are likely category-based (baby monitors, air purifiers, refrigerators, etc.)
- Each category page is inherently a "consideration stage" comparison resource
- Content strategy should map to the BSIP pipeline: only produce content for categories that have passed BSIP0
- SEO content for Bari should plan for Hebrew-language primary audience and search behavior
- Use `seo-audit` skill alongside this skill for technical SEO validation
- For executing individual content pieces, use `content-research-writer`
