---
id: TASK-425
title: Brand enrichment: fresh il_prices PriceFull pull for bread/hard_cheeses/hummus (114 brand-less products)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
blocker: "il_prices client cannot fetch grocery-chain PriceFull catalogs (Shufersal delta-only ~15 SKUs/day; Super-Pharm=pharmacy no match; Victory/RamiLevy/Yochananof not wired). 0/114 matched, no fabrication (P265). Needs il_prices client EXTENSION (grocery PriceFull feed URLs/auth) or another real brand source — owner decision. Brands stay null per missing-data discard rule until then."
summary: >
  P262 found 0 il_prices matches because the Shufersal PriceFull catalog wasn't in the feed cache (only delta Price files). Owner (2026-07-01) chose to run a fresh PriceFull pull: download the current Shufersal (+Victory/RamiLevy as needed) PriceFull catalog via the il_prices client, match the 114 missing-brand barcodes (bread 26, hard_cheeses 31, hummus 57), populate real ManufacturerName, leave null where no match. Real data only, NEVER invent, OFF banned. Score-neutral (brand field only). Follow-up deploy after the 2026-07-01 conformity sweep went live.
---

# TASK-425 — Brand enrichment: fresh il_prices PriceFull pull for bread/hard_cheeses/hummus (114 brand-less products)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
