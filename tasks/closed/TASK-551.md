---
id: TASK-551
title: Move 2 misclassified Actimel drinks spoonable->drinks (re-score under drinkable config + re-flow both pages, two-gate copy)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-09
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Moved 2 Actimel (7290119380916, 7290110578572) spoonable->drinks. Re-score under
  drinkable config VERIFIED via control-match (7290119380923 reproduced 55.7/C exactly)
  and returned IDENTICAL grades (49.3/D, 45.6/D) — dead-zone near both shelves' sugar
  medians, D driven by non-pool-relative NOVA-4/additive/long-list drivers; so no score
  change, no D8 co-sign trigger. Entries moved verbatim (signed copy intact), backed by
  drinkable-config traces placed in bsip2_task515_v3/drinkable/products/. Re-flow: spoon
  52->50, drinks 15->17 across _meta.product_count, hero counts, caveat/prologue prose
  (derived stats re-verified: sugar median still 4.50g, protein range still <3g..>13g),
  metadata, page-data comments, both FAQs regenerated. VERIFY: validate_comparison_page
  PASS both (score==trace 0 mismatch, counts consistent, copy-authored clean); DOM
  render-confirmed (spoon 0 Actimel/"50 היוגורטים"; drinks both present/"17 המשקאות").
  Guarded move asserted 0 mutation on the 65 untouched products.
summary: >
  Move 2 misclassified Actimel drinks spoonable->drinks + re-flow both pages
---

# TASK-551 — Move 2 misclassified Actimel drinks spoonable->drinks

Owner-directed (2026-07-09): 2 Actimel probiotic drinks were misclassified onto the
spoonable page (retailer category משקאות-יוגורט). Moved to /yogurt-drinks. Re-score under
drinkable config confirmed identical grades. Both pages re-flowed and re-verified. See
close_reason. Mirror files (02_products/.../frontend_out) NOT yet synced — flagged to owner.
