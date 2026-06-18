# Archived — bread_retail_001 (OFF-sourced, superseded)

**Archived 2026-06-10 under TASK-238 (Open Food Facts ban).**

This is the original `real_bread_retail_001` bread run. Its corpus was scraped from
Open Food Facts (`world.openfoodfacts.org`) — see the `bsip1/*` records carrying
`source_url: world.openfoodfacts.org`. OFF is now PROHIBITED as a Bari data source
(owner hard rule, 2026-06-10).

- It is **superseded** by `bread_retail_003` (the shipped, frozen-invariant bread run —
  Shufersal direct scrape, proven OFF-clean per the contamination audit).
- It is **NOT** to be rebuilt or re-scored. The scraper/batch scripts that produced it
  (`03_operations/bsip2/proto_v0/src/scrape_bread_retail.py`,
  `batch_run_bread_retail_001.py`) have been disabled (they hard-fail on run).

Do not move this back into `02_products/`.
