# run_yogurt_003 — NON-AUTHORITATIVE evidence run

**Status:** evidence only — **NOT a shippable shelf, NOT promoted to frontend.**
**Engine:** proto_v0 / 0.4.0 (UNMODIFIED — no manual score edits, enricher unmodified).
**Source:** Shufersal product pages (real Israeli yogurt SKUs, ingredient-bearing).

This run executed the full real BSIP0→BSIP1→BSIP2 cycle for yogurt from Shufersal and
**resolved the run_yogurt_002 data blocker** (ingredient coverage 0% → 90%; insufficient
48% → 0%). However it is preserved as **non-authoritative evidence**, not a live shelf,
because it surfaced three engine/pipeline calibration gaps (router yogurt-anchor,
enricher culture vocabulary, dairy A-ceiling philosophy) that must be resolved before a
machine yogurt shelf can replace the DEC-005 manual-MVP shelf.

The live `yogurts_frontend_v1.json` (DEC-005 manual shelf) is **untouched**. No scores changed.

See: `02_products/yogurt_system/reports/reconciliation_135_run_yogurt_003_findings.md`.
