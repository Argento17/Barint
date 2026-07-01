---
id: TASK-392
title: Brand names in comparison-card titles (cross-shelf render + data plumbing)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-24
closed_at: 2026-06-24
depends_on: []
blocks: []
category_id: null
close_reason: >
  Owner recurring complaint: brand names missing from comparison-card titles across
  shelves. Root cause (orchestrator-diagnosed): shared card rendered only product.name;
  the VM never carried brand; and the generator dropped brand on its way to the page.
  SHIPPED + LIVE-VERIFIED across all shelves where brand data exists:
  - Frontend (a64b156be): brand added to BariProductVM + inline "· brand" render with
    case-insensitive dedup, geometry 0-delta (121px), build 43/43. Commit cbe4de5fd.
  - Data backfill (a3050e2028 + sweep a1e0522c): brand populated from the DIRECT scrape
    by barcode on 4 reworked shelves (juices/cereals/granola + chocolate already had it)
    AND swept across brined-cheeses 36/36, cakes 65/65, cheese 53/53, cookies-coffee
    73/119, milk 18/18. 0 score / 0 grade / 0 non-brand-field changes vs origin/master.
    generate_page.py fixed to map brand -> no recurrence on regen. Commits cbe4de5fd,
    09e0f39b7.
  - Orchestrator-CAUGHT on live-verify: cakes brand didn't render (cakes is the SOLE
    shelf reconstructing the VM field-by-field vs ...p spread -> dropped brand). Fixed
    (2 lines, scanned all page-data = only cakes). Commit f61d25418.
  - LIVE-VERIFIED on bari.digital: all 9 brand-bearing shelves render brand (chocolate
    ARENSTO, juices אושן ספריי, cereals תלמה, granola דני וגלית, brined משק צוריאל,
    cheese כפרייה, cookies לה פזואלוס, milk אלפרו, cakes עדן קינוחים). dedup verified
    (35 chocolate suppressions all legitimate, 0 false hides). 3 juice over-captures +
    1 milk trim cleaned to source-true.
  - Bonus: ct-030 Toblerone spelled-out "שישים גרם סוכר" recitation removed.
  HONESTLY BLANK (no brand at source scrape -> not invented): hard-cheeses 23, hummus 57,
  bread 31, + 46 cookies-coffee with no source record. Re-scrape would be a separate job
  if owner wants brands there.
summary: >
  Brand names in comparison-card titles (cross-shelf render + data plumbing) — SHIPPED.
---

# TASK-392 — Brand names in comparison-card titles (cross-shelf render + data plumbing)

CLOSED 2026-06-24 — see close_reason. Brand live across 9 shelves; render + data + generator fixed.
