---
id: TASK-240
title: "BSIP0 follow-ups from TASK-239 — frozen-veg re-run (owner-deferred) + parser/gate debt"
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-10
depends_on: [TASK-239]
relates_to: [TASK-235, TASK-239]
roadmap_impact: false
work_type: pipeline-followup
blocked_reason: >
  Item 1 (frozen-veg re-run) owner-deferred 2026-06-10 ("Not yet"). It regenerates PUBLISHED
  frozen-veg data (relates_to TASK-235 Phase 1) → consumer-facing, needs owner green light.
  Remaining items are MEDIUM debt, do-when-convenient.
---

# TASK-240 — BSIP0 follow-ups carried over from TASK-239

The structural parser + gate fix (TASK-239) is done, verified, and landed. These are the
deferred / lower-severity items split out so they aren't lost.

## Items
1. **Frozen-veg re-run (HIGH, owner-deferred / gated).** Shipped frozen-veg v3 nutrition is still
   the MANUAL PATCH from the earlier correction. Re-run the category through the now-fixed
   scrapers (`01/02` → shared parser) so published data is structurally regenerated. The TASK-239
   fixture proof shows the parser reproduces the patched values (77 kcal / 12 mg) — so a re-run
   should clear the legacy G2/G3 basis WARN with no score surprise. **Owner said "Not yet"
   (2026-06-10).** Unblock only on owner go-ahead (moves published data, TASK-235 Phase 1).
2. **`ingredients_raw_source` capture (MEDIUM).** Nutrition has replay capture; ingredients don't.
   Add `capture_ingredients_raw` mirroring `extract_nutrition_raw` so ingredient parsing is
   repairable offline without re-scraping. Gate G8 currently WARNs in the meantime.
3. **Scope consolidation (MEDIUM).** Four drifted frozen-veg scope layers documented in the
   TASK-239 audit. Recommendation: single `FROZEN_VEG_SCOPE_RULES` source (in `_shared/` or
   `evaluation_scope.py`); retire the parallel `scope_clean_*` track.
4. **Other-retailer scraper migration (MEDIUM).** carrefour / victory / yohananof scrapers still
   use inline nutrition extraction. The shared path is fixed (won't drift), but migrating these to
   `bn.extract_nutrition_raw` removes the remaining inline copies. Do before their next run.

## Notes
- No scoring-methodology change in any item. No OFF. No manual JSON patch as a fix.
- Item 1 is the only consumer-facing one; 2-4 are internal pipeline hardening.
