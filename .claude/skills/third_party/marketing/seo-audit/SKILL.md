---
name: seo-audit
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "SEO health check," "my traffic dropped," "lost rankings," "not showing up in Google," "site isn't ranking," "Google update hit me," "page speed," "core web vitals," "crawl errors," or "indexing issues." Use this even if the user just says something vague like "my SEO is bad" or "help with SEO" — start with an audit. For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema. For AI search optimization, see ai-seo.
metadata:
  version: 2.0.0
---

<!-- source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/seo-audit -->
<!-- installed: 2026-05-31 -->
<!-- bari-agent: Head of Product, Research Analyst -->

# SEO Audit

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`), read it before asking questions.

Before auditing, understand:

1. **Site Context** — Type of site, primary business goal for SEO, priority keywords/topics
2. **Current State** — Known issues, current organic traffic, recent changes or migrations
3. **Scope** — Full site audit or specific pages? Technical + on-page or one focus area? Access to Search Console / analytics?

---

## Audit Framework

### Schema Markup Detection Limitation

`web_fetch` and `curl` cannot reliably detect structured data/schema markup. Many CMS plugins inject JSON-LD via client-side JavaScript — it won't appear in static HTML.

**To accurately check schema markup:**
1. Browser tool — `document.querySelectorAll('script[type="application/ld+json"]')`
2. Google Rich Results Test — https://search.google.com/test/rich-results
3. Screaming Frog export (SF renders JavaScript)

### Priority Order
1. **Crawlability & Indexation** — Can Google find and index it?
2. **Technical Foundations** — Is the site fast and functional?
3. **On-Page Optimization** — Is content optimized?
4. **Content Quality** — Does it deserve to rank?
5. **Authority & Links** — Does it have credibility?

---

## Technical SEO Audit

### Crawlability
- Robots.txt: check for unintentional blocks, verify important pages allowed, check sitemap reference
- XML Sitemap: exists and accessible, submitted to Search Console, contains only canonical/indexable URLs
- Site Architecture: important pages within 3 clicks of homepage, logical hierarchy, no orphan pages

### Indexation
- Index status: `site:domain.com` check, Search Console coverage report
- Issues: noindex tags on important pages, canonicals pointing wrong direction, redirect chains/loops, soft 404s, duplicate content without canonicals
- Canonicalization: all pages have canonical tags, HTTP→HTTPS canonicals, www vs. non-www consistency, trailing slash consistency

### Site Speed & Core Web Vitals
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1
- Tools: PageSpeed Insights, WebPageTest, Chrome DevTools

### Mobile-Friendliness
- Responsive design, tap target sizes, viewport configured, no horizontal scroll, same content as desktop

### Security & HTTPS
- HTTPS across entire site, valid SSL certificate, no mixed content, HTTP→HTTPS redirects

---

## International SEO & Localization

Check when the site serves multiple languages or regions.

### Hreflang
- Self-referencing entry on every page (page must include itself)
- Reciprocal links (if A points to B, B must point back to A)
- Valid codes: ISO 639-1 language + optional ISO 3166-1 Alpha 2 region (e.g., `en`, `en-GB` — never `en-UK`)
- `x-default` present, pointing to fallback page
- All target URLs return 200, are indexable, and match their canonical URL

**Common errors:** Missing self-referencing entry. No return tag. Invalid codes like `en-UK`. Hreflang target is non-canonical or 404.

### Canonicalization for Multilingual Sites
- Each locale page must self-canonical (`/ar/page` canonicals to `/ar/page`)
- Never cross-locale canonical (French to English — suppresses that locale entirely)
- Canonical URL must appear in the hreflang set

### Locale URL Structure
**Recommended:** Subdirectories (`/en/`, `/ar/`, `/he/`). **Not recommended:** URL parameters (`?lang=en`).

---

## On-Page SEO Audit

### Title Tags
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters
- Compelling and click-worthy

### Meta Descriptions
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition and call to action

### Heading Structure
- One H1 per page containing primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Not used just for styling

### Content Optimization
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth for topic
- Answers search intent

### Image Optimization
- Descriptive file names and alt text
- Compressed file sizes, modern formats (WebP)
- Lazy loading, responsive images

### Internal Linking
- Important pages well-linked
- Descriptive anchor text
- No broken internal links

---

## Content Quality Assessment

### E-E-A-T Signals
- **Experience**: First-hand experience demonstrated, original insights, real examples
- **Expertise**: Author credentials visible, accurate and detailed information
- **Authoritativeness**: Recognized in the space, cited by others
- **Trustworthiness**: Accurate information, transparent about business, contact info, HTTPS

---

## Common Issues by Site Type

### Multilingual / Multi-Regional Sites
- Hreflang errors (missing return tags, invalid codes, no self-reference)
- Canonical conflicting with hreflang (cross-locale canonical suppresses indexing)
- Thin locale pages dragging down site-wide quality signal
- Only boilerplate translated, main content identical across locales
- No x-default fallback declared
- IP-based redirects hiding content from Googlebot

---

## Output Format

### Audit Report Structure

**Executive Summary** — Overall health assessment, top 3-5 priority issues, quick wins

**Technical SEO Findings** — For each issue: Issue | Impact (H/M/L) | Evidence | Fix | Priority

**On-Page SEO Findings** — Same format

**Prioritized Action Plan:**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Rich Results Test (https://search.google.com/test/rich-results) — **use for schema, not web_fetch**
- Mobile-Friendly Test

**Paid Tools** (if available)
- Screaming Frog, Ahrefs/Semrush, Sitebulb, ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?

---

## Bari-Specific Notes

- Bari serves Hebrew-speaking Israeli consumers — hreflang configuration for `he` locale is critical
- Check hreflang self-reference and reciprocal links carefully on comparison pages
- Category pages are the primary SEO surface — audit these before blog or supporting pages
- Canonical consistency between category pages and their comparison drawer URLs must be verified
- For content strategy around SEO improvements, use `content-strategy` skill
- For AI search optimization (AEO, GEO), check if `ai-seo` skill is available in the repo
