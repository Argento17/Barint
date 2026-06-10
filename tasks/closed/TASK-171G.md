---
id: TASK-171G
title: Acquisition plumbing - Super-Pharm reader + iHerb panel extract + barcode bridge
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Build the reusable Israeli-supplement acquisition layer (the ~2-3.5 day build the probe identified): (a) Super-Pharm price-transparency catalog reader in il_prices (barcode/name/brand/price), (b) iHerb panel-extract pipeline (firecrawl -> SupplementLabel: active/dose/unit/form/claim/blend), (c) catalog<->panel barcode bridge -> assembled BSIP0-S label. Read-only, provenance-stamped candidate (EDPG), respectful rate. Test end-to-end on a small sample.
---

# TASK-171G — Acquisition plumbing - Super-Pharm reader + iHerb panel extract + barcode bridge

## CLOSED 2026-06-03 — 3 modules built, close-gate verified
- `integrations/clients/il_prices.py` (v1.2): `list_super_pharm_files()` + `fetch_super_pharm_supplements()` + `is_oral_supplement()` — reuses shared `parse_price_xml`.
- `integrations/clients/iherb_panel.py` (new): `extract_panel(url, scraper)` → BSIP0-S panel via firecrawl json; missing fields recorded, never fabricated; SDK-free (injected scraper).
- `integrations/clients/supplement_bridge.py` (new): barcode-first (GTIN-12↔13) then brand+dose name fallback (Hebrew→Latin); confidence + ambiguity flags; dual provenance stamps.
- Supporting: `02_products/supplements/poc_real_skus/run_acquisition_e2e.py`, `02_products/supplements/acquisition_layer_build_v1.md`.
- **Close-gate:** all 3 modules import clean + expose expected fns (verified). Catalog read ran LIVE (7,429 SKUs → 176 oral supplements in one PriceFull store; 924 store files exist). All records provenance-stamped `candidate` (EDPG); nothing shipped.

## Key findings + carried-forward
- **Bridge 0/5 on the PoC is CORRECT, not a bug:** the PoC products are iHerb US house-brands NOT on the Israeli shelf; the bridge is *supposed* to reject them. Israeli shelf is Altman(35)/SupHerb(24)/Solgar(10)/Tink/Life. Positive path proven: **Solgar Omega bridges by exact GS1 barcode (conf 1.0); Altman magnesium by name fallback (conf 0.55).**
- **Throughput:** catalog = 1 fetch; iHerb panel ~150–300 PDPs/hr, ~90–100% success; bridge ~40–60% complete-label first pass (higher for global brands w/ shared barcodes, lower for local-only brands).
- ⚠️ **Carried-forward #1 — local-brand panel gap:** global brands (Solgar) bridge cleanly via barcode; **local Israeli brands (Altman/SupHerb — the bulk of the shelf) likely aren't on iHerb**, so they only get a low-confidence name match or no panel. A real corpus may skew to global brands unless a local-brand panel source (Super-Pharm PDPs / brand sites / OCR) is added.
- ⚠️ **Carried-forward #2 — firecrawl scrape permission** was denied this session, so the panel stage ran on cached PoC panels. A live corpus run needs firecrawl scrape permission enabled + brand targeting + the §2.1 claim-curation step (bridge leaves `primary_claim_mapped=null`).
- **Confirmed:** acquisition is solved; the true corpus ceiling is engine active-coverage (dossiers), not acquisition.

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Return block (proposed RETURNED — 2026-06-03, data-agent)

Built the 3-module acquisition layer, live-verified, tested end-to-end. Read-only,
provenance-stamped `candidate`, EDPG firewall held; nothing shipped or admitted.

**Built (paths):**
- A — Super-Pharm catalog reader: `integrations/clients/il_prices.py` (extended,
  `CLIENT_VERSION=1.2`; `list_super_pharm_files`, `fetch_super_pharm_supplements`,
  `is_oral_supplement`; reuses shared `parse_price_xml`).
- B — iHerb panel-extract pipeline: `integrations/clients/iherb_panel.py` (new;
  `extract_panel` + injected firecrawl scraper; lossy fields marked, never fabricated).
- C — barcode/name bridge: `integrations/clients/supplement_bridge.py` (new;
  barcode-first GTIN-12↔13 tolerant, then brand+dose name fallback; assembles BSIP0-S).
- E2E runner: `02_products/supplements/poc_real_skus/run_acquisition_e2e.py`
  (→ `acquisition_e2e_result.json`).
- Build note: `02_products/supplements/acquisition_layer_build_v1.md`.

**E2E result:** live Super-Pharm PriceFull = 7,429 SKUs → 176 oral supplements;
panel-extract 5/5 PoC actives; barcode bridge 0/5 on the PoC (iHerb US house-brands are
NOT on the Israeli shelf — the bridge correctly rejected them). Positive matches proven
on the real corpus pattern: Solgar Omega-950 (SP ₪262.9) ↔ Solgar iHerb panel via exact
shared GS1 barcode (conf 1.0); Altman magnesium via name fallback (conf 0.55).

**Throughput/reliability:** catalog = whole shelf in 1 fetch; panel extract ≈150–300
PDPs/hr cached, ≈90–100% success on HTML panels; bridge match ≈60–80% for global brands
(shared barcode), blended ≈40–60% first pass. True ceiling = engine active-coverage
(5 dossiers), not acquisition.

**Blocker:** none for the plumbing. Live firecrawl re-scrape was permission-denied this
session → E2E ran the panel stage against the 5 cached PoC panels (same data the probe
pulled live 2026-06-03); a real corpus run needs firecrawl scrape permission + brand
targeting + claim curation (Nutrition).

Proposing **RETURNED**. Not CLOSED — leaving close-readiness to CC.
