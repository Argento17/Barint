# DEPRECATED — Open Food Facts code path (removed by TASK-237)

Owner directive (2026-06-10): **Open Food Facts is NOT an acceptable nutrition source.**

These scripts sourced the salty-snacks nutrition panels + ingredients from Open Food Facts
(OFF) by EAN. OFF was the root cause of every salty-snacks data defect this session: trans
"<1g ÷ serving" artifacts that zeroed products, English ingredient text, impossible kcal,
fabricated fiber, missing sodium, garbled strings. TASK-237 re-sourced the entire salty
pipeline from REAL Yochananof retailer product-page panels and removed OFF entirely.

Do NOT run these. The live salty pipeline is, in order:
1. `../01_scrape_yoh_panels.py`        — BSIP0: real Yochananof product-modal panels + Hebrew ingredients (Playwright)
2. `../02_build_bsip1_retailer.py`     — BSIP1: retailer panels -> BSIP1 records; drops no-panel + per-serving-basis-error products; NO OFF
3. `batch_run_salty_snacks_002.py`     — BSIP2: unchanged engine (engine-baseline-2026-06-04 + TASK-216)
4. `../03_build_frontend_retailer.py`  — Frontend VM + is_clean + confidence<->ingredient gates
5. `wire_d4_salty_snacks_v4.py`        — D4 additive enrichment from REAL Hebrew ingredients

Deprecated here (OFF path + OFF-artifact patches that are now moot):
- `01_bsip0_off_panels.py`           — OFF panel BSIP0 (REMOVED)
- `02_build_bsip1.py`                — OFF-consuming BSIP1 builder
- `03_build_frontend_v4.py`          — OFF-era frontend builder (DROP_IDS/BASIS_ERROR/INGREDIENTS_OMIT/OFF-trans neutralization)
- `fix_*trans*.py`, `fix_nova_provenance_rt7.py` — manual OFF-artifact corrections (moot: real panels carry honest `<0.5` trans declarations handled by the engine's threshold_declaration convention)
- `probe_*.py`                       — one-off Yochananof DOM probes used to build the real scraper
