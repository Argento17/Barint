# AI / data — Phase 1 (P1-12)

Theoretical only. No bari-web changes until implementation phase.

## Already on production

- /llms.txt, sitemap, /feed.xml
- JSON-LD: Organization, WebSite, FAQ (partial), ItemList, Article
- Public /data/comparisons/[slug] and product routes

## Phase 1 deliverables

| Task | Description |
|------|-------------|
| D1 | NutritionInformation in ItemList JSON-LD |
| D2 | FAQ schema for missing categories |
| D3 | /ai-index route |
| D4 | products.json flat index |
| D5 | schema_version + score_generated_at on VMs |

## Guardrails

Filter/sort only — never re-rank by user preferences. NOVA only where populated.
