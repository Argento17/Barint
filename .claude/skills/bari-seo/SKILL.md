---
name: bari-seo
description: Bari-specific SEO audit + growth loop — pull real data (GA4 MCP, Search Console, PageSpeed), run the Hebrew/RTL technical audit, mine near-page-one queries into two-gate content briefs, check GEO/AI-answer citability, and ship findings with a falsifiability check per recommendation. Use for any SEO audit, growth review, traffic diagnosis, or "why aren't we ranking" question about bari.digital.
---

# Bari SEO — audit + growth loop for bari.digital

**Owner:** Marketing Agent. Supersedes the generic `third_party/marketing/seo-audit`
skill (retired TASK-505, 2026-07-04). That skill was a generic English-market playbook;
this one is wired to Bari's actual site (bari.digital, Hebrew-only, RTL), Bari's actual
data clients, and Bari's governance (two-gate sign-off, no health claims, OFF ban).

Bari's SEO surface today: Next.js app at `bari-web/`, live comparison pages under
`/hashvaot/*`, catalog at `/catalog`, blog under `/blog`, plus deliberate GEO surface
(`/llms.txt`, `/ai-index`, `/data/products.json`, `/feed.xml`). Single locale: `he`.

---

## 1. Data pull — where the numbers come from (honest per-tool status)

Never audit from intuition when a number exists. Pull in this order.

| Source | How | Status (verified 2026-07-04) |
|---|---|---|
| **GA4 (traffic/behaviour)** | `analytics-mcp` MCP server tools: `run_report`, `run_realtime_report`, `run_funnel_report`, `run_conversions_report`, `get_account_summaries`, `get_property_details`, `get_custom_dimensions_and_metrics` | **LIVE.** Configured globally (service-account auth, GCP project `toms-budget`, key at `C:/Users/HP/.config/ga4-mcp/ga4-mcp-reader-key.json`). Use `get_account_summaries` to resolve the numeric property id at runtime. |
| **Search Console (acquisition)** | `C:\Bari\integrations\clients\search_console.py` — `query(dimensions=('query',), days, row_limit)` returns `SearchRow` (clicks, impressions, ctr, position); `SearchRow.near_page_one` flags position 11–20 with ≥50 impressions; `is_configured()` self-reports | **NEEDS-ENV-VERIFY.** Requires `GSC_ACCESS_TOKEN` (OAuth2, `webmasters.readonly`, ~1h expiry — refresh externally) + `GSC_SITE_URL`. Neither env var is set as of 2026-07-04. Code is complete; live run blocked on credentials. Until wired, pull GSC numbers manually from the Search Console UI and say so. |
| **PageSpeed / CWV (lab+field)** | `C:\Bari\integrations\clients\pagespeed.py` — `analyze(url, strategy='mobile')` returns performance score, LCP, CLS, TBT, FCP, Speed Index; `passes_mobile_budget` = perf ≥80 AND LCP ≤2.5s AND CLS ≤0.1 | **LIVE.** `PAGESPEED_API_KEY` is set. Without the key it 429s. |
| **Local perf gate** | `npm run test:perf` in `bari-web/` (Playwright `e2e/perf.spec.ts`, mobile project) | LIVE, local — run before/after any perf-affecting change. |
| **Google Trends (demand)** | `C:\Bari\integrations\clients\google_trends.py` — `interest_over_time(kw, geo='IL', hl='he')` → `DemandSeries` (`.momentum`, `.is_rising`, `.summary()`); `rising_queries(kw)` | DORMANT/fenced. No auth; unofficial endpoint, 429-prone; values are relative 0–100, directional only. Roadmap sequencing input only — NEVER a scoring or verdict input. |
| **Plausible (on-site)** | `C:\Bari\integrations\clients\analytics.py` | NEEDS-ENV-VERIFY (`PLAUSIBLE_API_KEY` + `PLAUSIBLE_SITE_ID` not set). GA4-via-MCP covers this need today. |

**GA4 CAVEAT (must appear in every GA4-based report):** GA4 on bari.digital is strictly
consent-gated (opt-in). Every GA4 number covers the *consenting subset only* and
systematically undercounts cold/bouncing traffic — exactly the segment SEO work targets.
Treat GA4 as behaviour-of-engaged-visitors, not total traffic. The complementary
cookieless signal is `@vercel/analytics` — built on branch `analytics/vercel-clean`
(exists on origin; NOT on master as of 2026-07-04, `@vercel/analytics` absent from
`bari-web/package.json`). For total-demand truth, prefer GSC impressions.

### GA4 playbook — which report answers which growth question

| Growth question | GA4 pull |
|---|---|
| Which comparison pages earn traffic? | `run_report`, dimension `pagePath`, metrics `screenPageViews`,`activeUsers`, filter `pagePath` begins with `/hashvaot` |
| Where do visitors come from? | `run_report`, dimensions `sessionDefaultChannelGroup`,`sessionSource`, metric `sessions` |
| Do organic landers explore or bounce? | `run_report`, dimensions `landingPage`,`sessionDefaultChannelGroup`, metrics `engagementRate`,`averageSessionDuration` |
| Did a shipped change move behaviour? | `run_report` with date ranges before/after ship date, same dimension set; annotate via `list_property_annotations` |
| Is a just-shipped page receiving hits right now? | `run_realtime_report`, dimension `unifiedScreenName` |
| Does catalog → product → comparison flow hold? | `run_funnel_report` across the page steps |

Remember: GA4 answers *behaviour after arrival*. GSC answers *acquisition* (what Google
shows and what gets clicked, including queries that never convert to a visit). They are
complementary; a report using only one to answer the other's question is wrong.

---

## 2. Technical audit checklist (Hebrew/RTL specifics)

Work through in priority order. File paths are the ground truth — read them, don't assume.

**Crawl & index**
- [ ] `bari-web/src/app/robots.ts` — disallow set is exactly `/api/`, `/dev/`, `/admin`; AI/search bots (Googlebot, GPTBot, Google-Extended, ChatGPT-User, anthropic-ai, ClaudeBot) explicitly allowed incl. `/llms.txt`, `/ai-index`, `/data/`; sitemap declared.
- [ ] `bari-web/src/app/sitemap.ts` reads `ALL_INDEXABLE_PATHS` from `bari-web/src/lib/seo/sitemap-paths.ts`. **TASK-499 convention: every live, indexable, real-content route MUST be in `ALL_INDEXABLE_PATHS`** — when a page ships, sitemap membership is part of the ship. Known open follow-up (TASK-499 close note): several live blog routes are still absent.
- [ ] No false noindex *comments*: TASK-499 removed "(page stays noindexed)" comments from pages that never emit a robots override. A comment claiming noindex on an indexable page is a defect — code comments about robots state must match emitted metadata.
- [ ] All comparison pages reachable by real SSR anchors (home → `/hashvaot` → hub sections → page). Verified 17/17 in TASK-499; re-verify whenever a category ships.
- [ ] GSC coverage: discovered-not-indexed on important pages = the live symptom TASK-499 remediated; watch it per new page.

**Locale & canonicals**
- [ ] Root layout (`bari-web/src/app/layout.tsx`): `lang="he"`, default canonical `alternates: { canonical: "./" }` inherited by every page that doesn't set its own. Bari is single-locale (he) — there is no multi-language hreflang cluster to maintain; the check is that nothing *introduces* a bogus hreflang or an en alternate, and every page resolves a self-canonical.
- [ ] RTL rendering: `dir` correctness, no mirrored numerals/units, Hebrew text not corrupted in metadata (titles/descriptions render as Hebrew, not mojibake — check the built HTML, not just source).

**Structured data (what exists — verify presence per page, not in the abstract)**
- [ ] Sitewide Organization + WebSite JSON-LD: `bari-web/src/components/seo/site-structured-data.tsx` (`inLanguage: "he-IL"`; deliberately NO SearchAction — the site has no search endpoint; never add schema pointing at a non-existent URL).
- [ ] Product snippets: `bari-web/src/lib/seo/item-list-schema.ts` — ItemList of schema.org Product, each carrying the Bari score as an editorial `review`/`reviewRating` (satisfies Google's offers/review/aggregateRating requirement; independent editorial review, not self-serving).
- [ ] FAQPage: generated deterministically by `03_operations/seo/generate_faq_schema.py` (slot-fill from `*_frontend_vN.json`, no LLM) via `03_operations/seo/run_all_faq_schemas.py` → `bari-web/src/data/seo/*_faq_schema.json`, wired per category in `bari-web/src/lib/seo/faq-registry.ts` (8 categories as of 2026-07-04). **New live category ⇒ add to `run_all_faq_schemas.py` CATEGORIES + faq-registry.ts.** Regenerate after any rescore (answers embed scores/grades — stale schema = published wrong number).
- [ ] JSON-LD is server-rendered (via `json-ld-script.tsx`) — verify in built HTML with Rich Results Test, not curl-vibes.

**Performance**
- [ ] `pagespeed.analyze(url, 'mobile')` per live comparison page; budget = `passes_mobile_budget` (perf ≥80, LCP ≤2.5s, CLS ≤0.1).
- [ ] `npm run test:perf` green locally before shipping perf-relevant changes.
- [ ] Hebrew webfont loading doesn't gate LCP; images same-origin under `bari-web/public/products/` (TASK-478 — never hotlink retailers).

---

## 3. Content opportunity loop (near-page-one → brief → two-gate)

The growth engine. One cycle:

1. **Pull**: `search_console.query(('query','page'), days=28, row_limit=100)`; filter
   `near_page_one` (position 11–20, impressions ≥50). Until GSC env is wired, export the
   same view from the Search Console UI (Performance → position 11–20 filter) and label
   the pull "manual".
2. **Rank the hit list** by `impressions × plausible CTR gain` (moving 15→8 on a
   500-impression Hebrew query beats moving 11→9 on a 60-impression one).
3. **Diagnose per query**: does the ranking page actually answer that Hebrew query in a
   heading + first paragraph? Is the query intent (comparison / "מה הכי בריא" / brand)
   matched by the page type? Is FAQ schema present for it?
4. **Write a content brief** — target query (exact Hebrew), the page, current position,
   what to add/change, the falsifiability check (§5). The brief is the Marketing
   deliverable; the *copy* is not.
5. **Route through the two-gate**: any consumer-facing string the brief provokes goes
   Content Agent → Adversarial QA. Marketing never ships copy directly, never edits
   `bari-web/src/` directly (Frontend Agent implements).
6. **Measure**: same GSC query 3–6 weeks later; record moved/didn't in the brief.

Demand-side input: `google_trends.rising_queries()` for rising Hebrew queries feeds new
brief candidates (directional only).

---

## 4. GEO / AI-answer citability checklist

How Bari pages read to AI Overviews, ChatGPT, Claude, Perplexity. Bari already invests
here deliberately (robots.ts allows GPTBot/ClaudeBot/Google-Extended; `/llms.txt`,
`/ai-index`, `/data/products.json` exist). Per page, check:

- [ ] **Quotable verdict line**: the page's core finding exists as one standalone,
  liftable Hebrew sentence carrying the number ("X קיבל 85/100 — הציון הגבוה בקטגוריה").
  A verdict spread across three paragraphs never gets cited.
- [ ] **Question-shaped headings**: at least the top questions users actually ask appear
  as headings matching FAQ-schema questions ("מה ה___ הבריא ביותר?"). LLM answerers
  align answers to question headings.
- [ ] **FAQ schema present and current** for the category (faq-registry.ts) — the same
  Q/A pairs the FAQPage declares should be visible on-page.
- [ ] **Answer-first structure**: finding before methodology; the first screen of content
  answers the query, framework mechanics stay invisible (editorial law anyway).
- [ ] **Attribution surface**: brand name + date near the verdict so a citation carries
  "לפי בארי"; Organization schema resolves the entity.
- [ ] **Machine surface fresh**: `/llms.txt`, `/ai-index`, `/data/products.json` include
  the category and current scores after every rescore/go-live.
- [ ] **No framework vocabulary** in any liftable line (see §6) — an AI quoting Bari must
  quote consumer language, never internals.

---

## 5. Output format — findings table + falsifiability

Every audit/growth deliverable ends with this table. **A recommendation without a
falsifiability check is not a recommendation — it's a vibe.**

| # | Finding | Severity | Evidence (file/URL/number) | Recommendation | Falsifiability check (how we know within N weeks) | Leading indicator |
|---|---|---|---|---|---|---|

- Severity: CRITICAL (indexation/crawl blocked, wrong published number) · HIGH (ranking
  or citability materially impaired) · MEDIUM (opportunity) · LOW (hygiene).
- Falsifiability check = a concrete number, source, and horizon: "GSC avg position for
  'לחם בריא' moves from 14 → ≤10 within 4 weeks, else the change didn't work and we say
  so." Leading indicator = the earlier tell (impressions up in week 1–2 before position
  moves; GA4 engagement rate on the lander, with the consent caveat attached).
- Findings must cite evidence you actually pulled (file:line, GSC row, PageSpeed number).
  Numbers not pulled = labeled "unverified".

---

## 6. Never rules (hard)

1. **No health claims.** Bari describes products and scores; it never advises on diet,
   health outcomes, or conditions. No "helps with", no "good for your ___" — in meta
   descriptions, FAQ answers, briefs, everything.
2. **No pre-go-live campaigns or SEO work for unlaunched categories.** Marketing
   activates only after Adversarial QA PASS + go-live. No demand pages, no briefs, no
   "coming soon" for unverified categories.
3. **OFF is banned project-wide** — Open Food Facts is never a source for any field,
   including SEO copy, FAQ answers, or schema. Unknown is acceptable; OFF is not.
4. **No framework vocabulary in anything public-facing or liftable**: NOVA, BSIP, cap,
   floor, structural_class, gate names — banned from meta tags, schema text, headings,
   briefs' proposed copy.
5. **Two-gate always**: any consumer-facing string this skill provokes ships only via
   Content Agent + Adversarial QA sign-off. This skill produces briefs and findings,
   never live copy.
6. **Demand signals never touch scoring** — Trends/GSC/GA4 inform sequencing and content
   priority only; a popularity number never reaches a BSIP score or a product verdict.
7. **Schema must match reality** — never declare schema for content/endpoints that don't
   exist on the page (the no-SearchAction precedent), and regenerate score-bearing
   schema after every rescore.
