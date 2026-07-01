---
id: TASK-276
title: Scale Israeli supplement corpus to full addressable shelf (SIE revival, acquisition)
owner: data-agent
status: CLOSED
priority: HIGH
close_reason: >
  ACQUISITION OBJECTIVE MET + ORCHESTRATOR-VERIFIED 2026-06-13. Full 118/118 addressable shelf
  covered; 85 scored, 33 unscoreable (18 premarket + 15 incomplete); measured yield 72.0%
  (recomputed from _corpus_run_full.json, not self-reported). Honesty: OFF=0, engine dir git-clean
  (unchanged), 0 scored SKUs with null/fabricated dose, all 118 cache files acquisition_method-tagged.
  Per-method scored: brand_panel 22 / search_panel 43 / name_derived 20. The Life house-brand wall
  held as predicted (mostly incomplete/name_derived). ONE DEFECT caught in verification: 3 Life
  omega-3 SKUs (7290118206118, 7290118206101, 7290119911011) were name_derived with a total-fish-oil
  dose (900/600/300mg) in violation of the never-name-derive-omega3 guard; numeric impact nil (all
  E/34 via cap_1 regardless) but classification is wrong → routed to the Nutrition re-score (TASK-277).
  GRADES ARE NON-AUTHORITATIVE: 38/49 E-grades fire cap_1 (claim-mapping artifact, incl. strong
  products like Solgar Omega 950) — the corpus MUST be re-scored after Nutrition calibration before any
  grade is shown. EDPG candidate throughout; nothing shipped; no published score moved.
created_at: 2026-06-13
depends_on: []
blocks: []
category_id: null
summary: >
  Revival of SIE/TASK-171 after v3 re-measurement overturned the 6.8% wall (now 64%/73%). Acquire candidate panels for the ~105 needs-fetch addressable Super-Pharm SKUs (brand sites + targeted search, checkpointed/resumable), assemble + score the full real corpus through the proven engine; target ~55-65% scoreable; Life house-brand residue = BD discard. EDPG candidate; engine untouched; nothing ships.
---

# TASK-276 — Scale Israeli supplement corpus to full addressable shelf (SIE revival, acquisition)

## Context
The SIE supplement engine (TASK-171, closed) was banked as proven but parked on a measured
**6.8% acquisition yield** (v2 / TASK-171J) — concluded "the Israeli shelf can't be scraped."
On 2026-06-13 the owner reopened it ("solve acquisition"). A re-measurement sprint
(`02_products/supplements/real_corpus_v3/`) showed 6.8% was a **thin-pool execution artifact**:
re-run on a brand-stratified 25-SKU sample with 3 acquisition methods → **64% yield (16/25),
73% excluding non-acquisition failures**. Owner directive: **scale to the full addressable shelf.**
Full diagnosis: `02_products/supplements/real_corpus_v3/_corpus_report_v3.md`.

## Scope
Acquire candidate panels for the **105 needs-fetch addressable SKUs** (the 13 name-derived are
already done; full worklist in `real_corpus_v3/_name_derived.json` → `needs_fetch`). Assemble +
score the full real corpus through the **proven engine (unchanged; golden 17/17)**.

**Method (cost order, checkpointed/resumable via the persistent `cache/` dir):**
1. **Altman bulk** (~17 SKUs) — brand site `altman.co.il`, WebFetch works cleanly, prints barcode. Highest leverage.
2. **SupHerb** (~17) — brand site/e-tailer + WebSearch.
3. **Targeted search** for the mid-tail (other/tink/magnesia/solgar/floris ~50) — one WebSearch each; many resolve from snippet.
4. **STOP at the residue** — Life house-brand (~21, the wall), bot-walled e-tailers (vitamins4all = Cloudflare), and out-of-ontology actives (omega-5/punicic). Mark `unscoreable` with a reason. **Do NOT over-source** (missing-data discard rule).

**Honesty guards (hard):** dose+unit must be **explicitly stated in a source tied to the exact
barcode/product**, or the SKU is `unscoreable`. No inference, no "typical value." Prefer sources
showing the matching barcode. Tag every panel with `acquisition_method`. Reuse the existing
pipeline: `build_cache.py` (cache schema), `run_v3.py` (resolve→score→trace), extend to all 118.

## Definition of Done
- [ ] Candidate panels acquired + cached for the reachable subset of the 105 (method-tagged, barcode-confirmed where possible).
- [ ] Full corpus run over all 118 addressable SKUs → `_corpus_run_full.json` + per-SKU `skus/*.json` + traces.
- [ ] Coverage report `_corpus_report_full.md`: measured yield %, per-method + per-brand breakdown, full grade distribution, and the **unscoreable residue table with a reason per SKU** (Life-wall vs walled-source vs out-of-ontology vs no-data).
- [ ] Honesty audit: zero fabricated doses; every scored dose traces to a cited source URL + barcode.
- [ ] Return-block with trace-derived counts (not self-reported) + the stable barcode/score/grade/binding-constraint table per the self-verifying-returns rule.

## Out of scope / parallel
- **Scoring calibration is NOT in this task** — the 3 grade bugs (cap-3 "hidden-in-blend" misfire on single-active iron/B12; omega pregnancy/"heart" claim→cap-1; detector noise נטול-caffeine + omega-5≠omega-3) go to **Nutrition D6** in parallel. Panels are independent of grades; grades recompute after calibration.
- **No launch.** Category go-live (D10/D1) is a separate owner decision after the corpus + a QA freeze. EDPG candidate throughout; engine untouched; no published score moves; nothing ships.
