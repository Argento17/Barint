---
id: TASK-279
title: GEO Stage: AI-crawler robots.txt + FAQ JSON-LD on all comparison pages
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-14
closed_at: 2026-06-14
depends_on: []
blocks: []
category_id: null
close_reason: >
  All artifacts verified by orchestrator. robots.ts: rules array with 6 AI-crawler entries
  (GPTBot/PerplexityBot/ClaudeBot/anthropic-ai/YouBot/Applebot-Extended), tsc clean.
  Pipeline: 03_operations/seo/generate_faq_schema.py + run_all_faq_schemas.py present and
  executed — 13 OK 0 FAIL. 14 FAQ schema files in bari-web/src/data/seo/ (13 categories +
  snacks). lib/seo/faq-schema.ts buildFaqScript() strips _bari_meta before JSON.stringify.
  14 comparison route pages updated with <script type="application/ld+json">. TypeScript
  compiles with 0 errors. Category factory SKILL.md updated: Stage 9 + stage summary JSON +
  owner table. Milk deferred (old format, legacy isolation). No score movement, no OFF, no
  consumer-facing copy fabrication — content derived verbatim from corpus insightLine/name/score.
summary: >
  Add Generative Engine Optimization layer to bari.digital: (1) Update robots.ts to explicitly
  allow GPTBot/PerplexityBot/ClaudeBot/YouBot/Applebot-Extended. (2) Build pipeline Stage 9
  that generates JSON-LD FAQPage schema from each category frontend JSON — deterministic
  slot-fill, no LLM calls. (3) Inject schema into 14 live hashvaot comparison routes as a
  server-side script tag. Milk deferred (legacy format/isolation policy).
---

# TASK-279 — GEO Stage: AI-crawler robots.txt + FAQ JSON-LD on all comparison pages

## Context
Owner identified GEO (Generative Engine Optimization) as an extremely strategic initiative:
when Israeli consumers ask ChatGPT/Perplexity/Claude "מה בריא יותר — X או Y?", Bari's
comparison pages need to be (a) crawlable by AI bots and (b) structured so LLMs can extract
and cite the answers. Hebrew food comparison space has near-zero competition for this.

## Scope
Three discrete deliverables:

### 1. robots.ts — AI crawler entries
**File:** `bari-web/src/app/robots.ts`
Changed `rules` from single object to array; added 6 AI-crawler bot entries (all `allow: "/"`).
No disallow changes to existing rules.

### 2. Pipeline Stage 9 — FAQ schema generator
**Files:**
- `03_operations/seo/generate_faq_schema.py` — single-category generator (argparse CLI)
- `03_operations/seo/run_all_faq_schemas.py` — runs all categories in one pass

**Logic:** fully deterministic slot-fill from `*_frontend_vN.json`:
- Q1: best product (name + score + grade + insightLine)
- Q2: A-grade product list (skipped if none)
- Q3: total products examined + score range
- Q4: top-2 comparison (names + scores + insight lines)

Coverage gates (exit 1 if violated): `product_count >= 5`, non-empty products array.
No LLM calls. No OFF. No fabricated content — all answers derived verbatim from corpus fields.

### 3. Next.js injection — 14 comparison routes
**New utility:** `bari-web/src/lib/seo/faq-schema.ts` — `buildFaqScript()` strips `_bari_meta`
and returns `JSON.stringify(schema)` for safe inline injection.

**Updated routes** (14 pages, all under `bari-web/src/app/hashvaot/`):
cheese, yogurts, bread, butter, hummus, breakfast-cereals, granola, salty-snacks,
juices, hard-cheeses, brined-cheeses, cookies-coffee, vegetable-spreads, snacks.

Pattern: `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />`
added as first child of a `<>` fragment wrapping the existing page component.

### 4. Category factory skill update
`SKILL.md` updated: Stage 9 added between D4 Additive Wiring and render_local_page; stage
summary JSON has `"faq_schema_generation"` entry; owner table updated.

## Definition of Done (verified by orchestrator)
- [x] robots.ts rules array with 6 AI-crawler entries — tsc clean
- [x] `generate_faq_schema.py` + `run_all_faq_schemas.py` present; 13 OK 0 FAIL on execution
- [x] 14 FAQ schema JSON files in `bari-web/src/data/seo/`
- [x] `buildFaqScript()` in `lib/seo/faq-schema.ts`
- [x] 14 comparison route pages inject JSON-LD via `<script>` tag
- [x] `npx tsc --noEmit` exits 0 (no TypeScript errors)
- [x] Category factory SKILL.md Stage 9 entry present
- [x] No fabricated content: every FAQ answer derived verbatim from `name`/`score`/`grade`/`insightLine` in the corpus JSON
- [x] `_bari_meta` block absent from rendered output (stripped by `buildFaqScript`)
- [x] OFF=0: no OFF dependency anywhere in this stage

## Deferred
- Milk comparison page (`/hashvaot/milk-comparison`): uses old `milk-comparison.json` format
  (pre-canonical BariProductVM schema, no `insightLine` field). Blocked on legacy-to-canonical
  migration. Track separately when milk is migrated to the factory pipeline.

## Orchestrator verification (2026-06-14)
- **robots.ts:** read file — rules is an array of 7 objects; first entry is the wildcard rule,
  entries 2-7 are AI crawlers (GPTBot/PerplexityBot/ClaudeBot/anthropic-ai/YouBot/Applebot-Extended).
- **Scripts:** both files present in `03_operations/seo/`. Runner output: "13 OK, 0 FAIL/SKIP".
  WARN entries (no A-grade for butter/cereals/granola/hard_cheeses/cookies_coffee/snacks) are
  correct — Q2 is correctly omitted for those categories.
- **Schema files:** 14 JSON files confirmed in `bari-web/src/data/seo/`.
  Spot-check `brined_cheeses_faq_schema.json`: correct product name/score/insightLine in Q1,
  9 A-grade products listed in Q2, product count 36 (actual displayed corpus, correct over meta's 48).
- **Route pages:** all 14 checked — each imports `buildFaqScript` + `rawFaqSchema` and wraps
  return in `<><script .../><PageComponent /></>`.
- **TypeScript:** `npx tsc --noEmit` = 0 errors.
- **Factory skill:** SKILL.md Stage 9 entry present at correct position.

```json
{
  "task_id": "TASK-279",
  "status": "CLOSED",
  "closed_date": "2026-06-14",
  "close_reason": "All artifacts verified by orchestrator. robots.ts AI-crawler entries present. 14 FAQ schemas generated + injected. TypeScript clean. Factory skill updated. No score movement, no OFF, no fabrication.",
  "artifacts_verified": [
    "bari-web/src/app/robots.ts",
    "03_operations/seo/generate_faq_schema.py",
    "03_operations/seo/run_all_faq_schemas.py",
    "bari-web/src/data/seo/[14 faq_schema.json files]",
    "bari-web/src/lib/seo/faq-schema.ts",
    "bari-web/src/app/hashvaot/[14 page.tsx files]",
    ".claude/skills/bari-category-factory/SKILL.md"
  ]
}
```
