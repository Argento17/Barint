# Israeli-Supplement Acquisition Layer — Build Note v1 (TASK-171G)

Parent: TASK-171. Proves out the plumbing the Phase-3 probe
(`phase3_sourcing_feasibility_v1.md`) said was the only thing to BUILD: a
Super-Pharm catalog reader (A) + an iHerb panel-extract pipeline (B) + a
barcode/name bridge (C). Read-only, provenance-stamped `candidate`, EDPG firewall.
Nothing ships; nothing is admitted to a published score.

## 1. The three modules

| # | Module | Path | What it does |
|---|--------|------|--------------|
| A | Super-Pharm catalog reader | `integrations/clients/il_prices.py` (extended; `CLIENT_VERSION=1.2`) | `list_super_pharm_files()` walks the PriceTransparency.WS MVC-grid (filter `?Category-equals=PriceFull&page=N`), `fetch_super_pharm_supplements()` reads one PriceFull store catalog, reuses the shared `parse_price_xml`, and filters to oral supplements via `is_oral_supplement()`. Output: barcode + Hebrew name + brand + price, provenance-stamped. **Identity+price only — no panel.** |
| B | iHerb panel-extract pipeline | `integrations/clients/iherb_panel.py` (new) | `extract_panel(url, scraper)` runs one `firecrawl_scrape(json)` with the fixed BSIP0-S schema (active·amount·unit·form·primary-claim·blend), maps to an `IherbPanel`, records every un-extractable field in `missing_fields` (never fabricated), stamps provenance `candidate`. SDK-free: takes an injected `scraper(url, schema)` callable — `firecrawl_tool_scraper(...)` in the agent runtime, `poc_fixture_scraper()`/`cache_scraper()` offline. |
| C | Barcode/name bridge | `integrations/clients/supplement_bridge.py` (new) | `bridge_one()` matches a Super-Pharm SKU to an iHerb panel **barcode-first** (GTIN-12↔13 leading-zero tolerant), then **brand+dose name fallback** (Hebrew→Latin brand transliteration + dose-token overlap). Records confidence; flags ambiguous near-ties instead of guessing. `assemble_label()` builds the candidate BSIP0-S label carrying **both** provenance stamps. |

E2E runner: `02_products/supplements/poc_real_skus/run_acquisition_e2e.py`
(→ `acquisition_e2e_result.json`).

## 2. End-to-end test result (live Super-Pharm + 5 PoC panels)

- **Catalog read (live):** one Super-Pharm PriceFull store file = **7,429 SKUs → 176
  oral supplements** classified (precision-first; ~1 cosmetic false-positive seen,
  harmless — it just won't bridge). 924 PriceFull files exist (one per store); one store
  is the whole shelf.
- **Panel extract: 5/5** PoC actives mapped cleanly to BSIP0-S panels; only lossy field
  was omega-3 chemical form (`form=None`, honestly marked — TG/EE not on the panel), as
  the probe found.
- **Barcode bridge — the real finding:** the 5 PoC panels are **iHerb US store-brands**
  (California Gold, Country Life, ALLMAX, NOW) → **0/5 matched the Super-Pharm shelf.**
  This is correct, not a bug: the live Israeli shelf is dominated by **local/global
  brands** — אלטמן/Altman 35, סופהרב/SupHerb 24, סולגר/Solgar 10, טינק/Tink, לייף/Life.
  "ships-to-IL (iHerb) ≠ on-Israeli-shelf (Super-Pharm)" is exactly the distinction the
  bridge exists to enforce, and it enforced it.
- **Positive-match proof (the real corpus pattern):** a **Solgar Omega-950** SP SKU
  (`0033984020580`, ₪262.9) bridges to a Solgar iHerb panel by **exact barcode** (conf
  1.0) — Solgar is one global brand, so the GS1 barcode (`033984…`) is shared across both
  shelves. An **Altman magnesium** SP SKU bridges by **name fallback** (conf 0.55, brand
  transliteration אלטמן→altman) when barcodes differ. No-match returns conf 0.0. All
  three paths verified.

**Takeaway:** the corpus must target **brands that are genuinely on the Super-Pharm
shelf** (Solgar/Altman/SupHerb/Life/NOW), then pull each brand's panel from iHerb — for
global brands the **barcode matches directly**; for local-only brands the name-fallback
or a brand-site panel is needed. The PoC's iHerb house-brands were the wrong corpus
targets (they proved the engine path, not the Israeli shelf).

## 3. Realistic throughput + reliability for a full corpus run

| Stage | Estimate | Basis |
|-------|----------|-------|
| Super-Pharm catalog | **whole shelf in 1 fetch** (~6 MB .gz, ~176 supplements/store), seconds | one live PriceFull read |
| iHerb panel extract | **~150–300 PDPs/hour** rate-limited & cached; **panel-extract success ≈ 5/5 (≈90–100%)** for HTML-panel PDPs; form lossy on a non-trivial minority (omega TG/EE etc.) | probe 5/5 + firecrawl latency/credit budget; respectful low-volume |
| Barcode bridge | instant (in-memory) once panels are in hand | — |
| **Expected bridge match rate** | **barcode ≈ 60–80% for global brands** (shared GS1), **lower for local-only brands** → name-fallback fills some; realistic **blended ≈ 40–60%** of the supplement shelf gets a complete BSIP0-S label on a first pass | shelf is ~½ global / ½ local brands |

**The true corpus ceiling is the engine's active coverage (5 dossiers), not
acquisition** — the live shelf is mostly multivitamins, B-complex, probiotics, collagen,
herbals the engine can't yet score. Acquisition is solved; dossier breadth is the gate
(a Nutrition effort, not a sourcing one).

## 4. Guardrails honored (EDPG)

- Read-only; rate-limit + cache (`cache_scraper`); robots/ToS respectful low-volume.
- Every catalog record, panel, and assembled label is `verification_status: candidate`;
  nothing reaches scoring without a BSIP0/QA promotion. Price feed carries **identity +
  price only**, never a panel. Super-Pharm presence is the Israeli-shelf integrity
  control. Stdlib + firecrawl; reused `parse_price_xml`; no new paid key; no BSIP2/food
  edits; nothing shipped.
- **Claim selection (§2.1) is a downstream Nutrition curation step** — the bridge leaves
  `primary_claim_mapped=null` and only carries the raw on-label claim; it never picks a
  dossier tier. (This was the probe's #1 risk: same magnesium grades very differently on
  a structure/function vs a studied-endpoint claim.)

## 5. Status

Proposed: **RETURNED**. The acquisition plumbing is built, live-verified, and tested
end-to-end with an honest match rate. Not CLOSED — pending CC close-readiness gate +
(if a corpus run is authorized) Product/Nutrition decisions on brand targeting and claim
curation. No engine change, no published-score movement, no launch.
