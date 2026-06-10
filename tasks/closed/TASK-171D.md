---
id: TASK-171D
title: Phase 3 - Israeli supplement corpus (BSIP0-S) + QA freeze
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Acquire the real Israeli supplement shelf for the engine. Step 1 = acquisition feasibility probe + end-to-end proof-of-concept: what's reachable (il_gov_data supplement importers, Super-Pharm price feed, OFF IL barcodes, iHerb-IL structured pages, brand sites) and can we reliably extract the (active,dose,form,claim) label tuple. Output a sourcing report + recommended acquisition path + 3-5 real SKUs scored end-to-end through the engine. Then build the corpus + QA freeze. Reference brain (dossiers) already live; the Israeli shelf is the known data gap.
---

# TASK-171D — Phase 3 - Israeli supplement corpus (BSIP0-S) + QA freeze

## Step 1 — acquisition feasibility probe + PoC (2026-06-03, data-agent) — DONE
**Answer to "do we have the APIs?":** catalog/barcode (Super-Pharm price-transparency feed — LIVE, no login),
identity/legitimacy (`il_gov_data` imported_foods: Altman 105 / Solgar 85 SKUs), and panel extraction
(iHerb via firecrawl — 5/5 actives clean) are all reachable. **The missing piece is NOT an API — it's a
small build** (~2–3.5 days, no new key, no OCR on critical path): a Super-Pharm catalog reader in `il_prices`,
an iHerb panel→`SupplementLabel` extract pipeline, and the catalog↔panel **barcode bridge** (the real work).
OFF supplement coverage = 0/4 (not viable). Report: `02_products/supplements/phase3_sourcing_feasibility_v1.md`.

**End-to-end PoC — 5 REAL Israeli-market SKUs scored through the live engine** (`02_products/supplements/poc_real_skus/`):
| SKU | active | grade | binding constraint |
|---|---|---|---|
| California Gold Creatine 5g | creatine | S (91.2) | blend_dominant |
| ALLMAX Caffeine 200mg | caffeine | A (80.0) | blend_dominant |
| NOW Omega-3 600mg | omega-3 | D (42.1) | sub-therapeutic + weak claim + form unknown |
| CGN Magnesium Bisglycinate 200mg | magnesium | E (34.0) | **cap_1_insufficient_evidence** (vague structure/function claim) |
| Country Life Vit D3 5000 IU | vitamin D3 | E (20.0) | **veto_safety** (5000 > 4000 IU UL) |
Inverted-E discipline held on real data (Mg-E vs D3-E, opposite correctly-attributed reasons). All
`verification_status: candidate`, EDPG firewall, no engine change, golden corpus still 14/14, nothing shipped.

## TWO STRATEGIC FINDINGS the real data exposed (corpus build PAUSED pending owner decision)
1. **The real ceiling is dossier/active coverage, not acquisition.** The Israeli shelf is dominated by
   multivitamins / probiotics / herbals the engine cannot yet score (only 5 actives have dossiers). A corpus
   built today would cover a sliver of the real shelf.
2. **"As-sold / claim-specific" applied to real labels grades many well-made products E** because their labels
   use vague untethered structure/function claims (the magnesium case: good form, honest, safe → E on claim).
   Defensible (punishes vague marketing) but a deliberate positioning choice with editorial implications +
   a per-SKU claim-curation workload. **This is the business-thesis crux, not a scoring bug.**

## Step 2 — addressable-corpus mapping (2026-06-03, data-agent) — DONE (no firecrawl; live catalog)
Sampled 3 of 924 Super-Pharm PriceFull stores → **204 oral-supplement SKUs**. Report: `02_products/supplements/addressable_corpus_mapping_v1.md`.
- **56.4% addressable** by the 15 actives (115/204) — confirms the upper end of the ~40–55% estimate. Rest = multivit/probiotic/collagen/herbal/blends (deferred set).
- Real per-active depth: magnesium 28, D3 24, omega-3 16, vit C 11 strong; zinc/iron/calcium solid; folic/B12/biotin/vit E thin; **creatine/CoQ10/melatonin = 0 on the pharmacy shelf** (channel artifact — sports/iHerb, not Israeli absence; keep them).
- **⚠️ THE BINDING CONSTRAINT (newly quantified): the local-brand panel gap.** Of the 115 addressable SKUs, only **20% (23) are global brands** (Solgar-led, iHerb-panel-gettable today); **80% (92) are local-only** (Altman/Life/SupHerb/Tink…) whose Supplement Facts panels are **NOT on iHerb** → need a non-iHerb panel source. **Of the full shelf, only ~11% (~23 SKUs) is scoreable TODAY.**
- **Reframe:** the constraint is NOT active coverage (fine at ~56%) and NOT the engine (excellent) — it's **panel acquisition for the local-brand-dominated shelf.** Reaching the other ~45% needs a Super-Pharm-PDP / brand-site / OCR panel source (a real, more-brittle build). Product/Nutrition scope call.

## Step 3 — thin live proof corpus (2026-06-03, data-agent) — DONE (firecrawl LIVE, no fallback)
Owner chose "thin live proof, then decide." Ran the global-brand SKUs end-to-end through the 15-active engine. Artifacts: `02_products/supplements/real_corpus_v1/`.
- **Real yield: 4 global-brand SKUs derived live → 2 scored end-to-end** (the other 2 = honest catalog misses: those exact Israeli packs aren't on iHerb-US; verified, not pipeline failures).
- **Solgar Omega 950 → C/60.5** — real barcode-matched iHerb panel (EPA 504 + DHA 378 mg ethyl ester, "Heart Healthy"); bound because "Heart Healthy" resolved to the **CONTESTED/deferred CV-events endpoint** (evidence 17) — engine refuses a contested claim on a real SKU. *(Calibration Q surfaced: should vague "heart healthy" pin to contested-CV or resolve to omega-3's Strong triglyceride endpoint? → Nutrition D6 review.)*
- **Solgar Zinc Picolinate → B/68.4** — preferred form, immune claim resolves to a real tier, blend-bound.
- Firecrawl live all session (no denial, no cache fallback); URL-rot confirmed (must resolve current URLs by barcode).
- **Two sharpening corrections (honest):** (1) the "~23 global-brand" was an **importer-field over-count** (אמברוזיה/סולגר distributes BOTH global Solgar AND local SupHerb house-brand); genuine-global count is far smaller. (2) **"ships-to-IL on iHerb" ≠ "this exact Israeli pack is on iHerb"** — Israeli-pack barcodes differ from iHerb-US, halving even the genuine-Solgar set.

## ⚠️ The sharpened conclusion (decision-grade)
The pipeline is **proven end-to-end on real Israeli SKUs** — but **iHerb is NOT a viable breadth source for an Israeli corpus**: it yields only a *handful* of SKUs (global brand + matching Israeli-pack barcode is a tiny intersection). A real corpus REQUIRES a dedicated **local-brand / local-pack panel source** (Super-Pharm PDPs / brand sites / OCR). The engine + maintenance economics are proven; **the make-or-break for the category is the panel-acquisition build.**

## CLOSED 2026-06-03 — acquisition experiment concluded (owner directive)
The full local-brand corpus was scoped (171I), built as an MVP, and measured (171J → 6.8% scoreable yield, far below the ~31–37% projection — panel acquisition by scraping is the wall). Owner directive: stop engineering, bank the engine as a proven asset, close the acquisition experiment. **No launch; D10/D1 not made.** Engine + dossiers + plumbing all remain as candidate artifacts; the only path to the local-brand shelf is a manufacturer/importer data feed (BD, not engineering). Asset record: `03_operations/supplement_engine/SIE_ASSET_AND_CLOSURE.md`.
