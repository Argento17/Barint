# run_yogurt_002 — NON-AUTHORITATIVE (evidence only)

**Status:** NON-AUTHORITATIVE. Do NOT use for the frontend or to rescore the live yogurts shelf.
**Run by:** TASK-135A (data-agent), 2026-06-01 · engine proto_v0 / 0.4.0 (unmodified).
**Source:** Open Food Facts — 46 real Israeli yogurt SKUs (real barcodes/brands/provenance).

## Why non-authoritative
The OFF Israeli yogurt corpus is **ingredient-blind (0/50 SKUs carry ingredient lists)**.
Yogurt scoring is ingredient-structure-driven, so this run is:
- 48% INSUFFICIENT (22/46), ceiling 75/B, **0 grade-A**;
- 70% routed to "default" (router cannot identify yogurt without ingredients);
- NOVA confidence 0.2 (unreliable); **no consumer-facing explanations producible**.

It **inverts** the displayed shelf's editorial logic (protein mass dominates when ingredients
are blind) and cannot reconcile 1:1 with the 13 displayed manual-MVP products.

## What it IS good for
Measured evidence that DEC-005 cannot be retired with OFF data, and a precise spec for the
real unblock: a retailer scrape carrying **ingredient panels + Hebrew names** (run_yogurt_003).

Full analysis: `02_products/yogurt_system/reports/reconciliation_135a_findings.md`.
The live shelf (`bari-web/src/data/comparisons/yogurts_frontend_v1.json`) is unchanged.
