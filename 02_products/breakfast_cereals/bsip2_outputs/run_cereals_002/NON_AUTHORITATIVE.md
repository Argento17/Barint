# run_cereals_002 — NON-AUTHORITATIVE

This run is **evidence, not a shippable shelf.** Engine proto_v0 / 0.4.0 unmodified;
no manual score edits; provenance preserved (Shufersal source_url + barcode per item).

**Do NOT promote to the live frontend.** It fails the TASK-140 exit gate:
- Misroute **7.6% > 5%** (QA-CER-001): 7 real cereals route to bread / whole_food_fat /
  beverage — router has no cereal anchor (engine fix, out of scope; same class as run_yogurt_003).
- Nutrition approval pending for 4 NOVA-1 shaped baked-flake grade-A reads (possible under-call).

92 displayable · 0 insufficient · A7/B10/C48/D25/E2 · median 58.3.
Four cereals governance constructs applied at BSIP1 (granola subpool, children's, whole-grain
MDF, fortification). See `factory_run_002/` for the full stage artifacts and
`reports/run_cereals_002_run_summary.json`.

*data-agent · TASK-140 · 2026-06-01*
