# Phase-3 Supplement Sourcing Feasibility — v1 (TASK-171D)

**Question for the owner:** *Do we have all the external APIs we need to acquire the real
Israeli supplement shelf and feed it to the SIE engine — and if not, what is the smallest
missing piece?*

**Verdict (headline):** **YES for a proof; ALMOST for the corpus.** The full path is
reachable today with the tools we already have. The **only thing that must be BUILT** is a
thin **iHerb (and/or Super-Pharm) firecrawl "panel-extract" pipeline** that turns a product
page into a BSIP0-S label — proven working in this probe on all 5 dossier actives. No new
API, no auth, no OCR is required for the structured (iHerb) path. The genuinely *missing*
piece is not an API but a **catalog↔panel bridge**: the Israeli price-transparency feed
gives the local **catalog + barcode** but no panel; iHerb gives the **panel** but is a
ships-to-IL catalog, not the Israeli shelf. Bridging them (by barcode/brand match) is the
build.

All data below is `verification_status: candidate` (EDPG). Nothing here moves a published
score. Engine unchanged.

---

## PART A — Per-source reach table

| # | Source | Reachable? | Structured? | Identity | Catalog | Label panel (active·dose·form) | Coverage of supplement shelf | Blockers / ToS |
|---|--------|-----------|-------------|----------|---------|-------------------------------|------------------------------|----------------|
| 1 | **`il_gov_data` — imported_foods (mazon)** | **YES** (LIVE) | YES (CKAN) | **YES** (Hebrew+English product name, importer, kosher cert, country, expiry, registration#) | partial (importer registry, not a shelf) | **NO** (description = kosher/label notes only; no dose) | High for *imported* supplements: 32,620 records; אלטמן 105, סולגאר 85, "ויטמין" 193 hits | None (public CKAN, no auth). `name7` is a registration/importer id, **NOT a barcode** |
| 1b | **`il_gov_data` — food_manufacturers** | **YES** | YES | **YES** (legitimacy: license #, GMP status+expiry, `ProductActivityFoodType="ייצור תוספי תזונה"`) | NO | NO | Supplement manufacturers/importers are explicitly typed | None |
| 2 | **Super-Pharm price-transparency** (`prices.super-pharm.co.il`) | **YES — open, NO login** | YES (standard IL PriceTransparency.WS .gz XML) | YES (Hebrew name, **13-digit EAN barcode**, price) | **YES** (full chain catalog, chain_id 7290172900007) | **NO** (price feed = identity+price only, by design/guardrail) | High — it is the whole Super-Pharm shelf incl. supplements | None for the feed. (Old Cerberus host `url.publishedprices.co.il` = **DEAD**, DNS gone — consistent with memory) |
| 3 | **`open_food_facts`** (by barcode) | YES (LIVE) | YES | — | — | thin | **0/4** test supplement barcodes found (`found:false`) | Crowd-sourced; supplements barely covered. Not viable as the panel source |
| 4 | **iHerb** (ships-to-IL catalog) | **YES** | **YES — richest** | YES (brand, barcode/UPC) | YES (huge) | **YES — firecrawl extracts active·amount·unit·claim·blend cleanly** (5/5 actives) | Very high for the 5 actives; deep global catalog | Storefront ToS (respectful, low-volume only). **Scoping caveat:** "ships-to-IL" ≠ "the Israeli shelf"; brands overlap but SKUs/IL barcodes differ |
| 5 | **Super-Pharm storefront / brand sites** (Altman, SupHerb) | YES (200) but **JS-rendered** | weak | partial | catalog behind JS/search | panel not directly in HTML on the category page tested | Local shelf, but fragile (matches the project's recurring "retailer storefront blocked/JS" memory) | JS rendering; deep category URLs redirect; would need stealth render or per-PDP firecrawl |

**Does Israel expose a supplement-specific registry?** Yes, two complementary layers:
`imported_foods` (per-SKU **identity/legitimacy** for imported supplements — importer, kosher,
country, expiry) and `food_manufacturers` (manufacturer **legitimacy** — license, GMP,
explicitly typed `ייצור תוספי תזונה`). **Neither carries the label panel** (active/dose/form).
They are an identity/legitimacy spine, not a composition source.

---

## PART B — End-to-end proof (the real test)

5 real SKUs (all dossier actives), panels extracted read-only from iHerb PDPs via
`firecrawl_scrape(json)` on 2026-06-03, mapped into `supplement_label.py`, run through the
**real** `score_engine.score_label`. Artifacts: `poc_real_skus/<sku>.json` (+ `_index.json`).

| SKU (real) | Active | Extracted panel | Score / Grade | Binding constraint | Read |
|---|---|---|---|---|---|
| California Gold Sport Pure Creatine Monohydrate 5 g | creatine | 5 g, monohydrate, strength claim, disclosed | **91.2 / S** | `blend_dominant_limit` | The ideal product: right dose, preferred form, Strong claim |
| Country Life Vitamin D3 5,000 IU | vitamin D3 | 5000 IU cholecalciferol, daily | **20.0 / E** | **`veto_safety`** | 5000 IU > 4000 IU UL → safety veto. A *common retail dose* trips the ceiling |
| California Gold Magnesium Bisglycinate 200 mg | magnesium | 200 mg elemental, bisglycinate, "bone/heart/nerve/muscle" claim | **34.0 / E** | **`cap_1_insufficient_evidence`** | Good product, **untethered** structure/function claim → §2.1 default. Dose short-circuits to N/A. Form scored 92 (preferred) |
| ALLMAX Essentials Caffeine 200 mg | caffeine | 200 mg anhydrous, alertness, disclosed | **80.0 / A** | `blend_dominant_limit` | Disclosed, in-range, preferred form |
| NOW Foods Omega-3 (EPA 360 + DHA 240 = 600 mg) | omega-3 | 600 mg EPA+DHA, CV claim, form not on panel | **42.1 / D** | `blend_dominant_limit` | Sub-therapeutic vs 2000 mg TG threshold + weaker CV-claim tier + form unknown (50) |

**Discipline checks that held on real data:**
- The **inverted-E pair survives on real SKUs**: D3 (E via `veto_safety`) and magnesium (E via
  `cap_1_insufficient_evidence`) are both E for *opposite, correctly-attributed* reasons.
- **Extraction lossiness was marked, never fabricated** (per `missing_or_lossy_fields`):
  - omega-3 chemical form (TG vs ethyl-ester) is **not on the panel** → `form=None` (unknown),
    not guessed. This drags Form to 50 (honest "unknown" handling).
  - creatine form "monohydrate" taken from the **product name** (not the Facts table) — unambiguous for a single-ingredient SKU, but flagged.
  - magnesium claim is **structure/function**, which has **no** matching dossier endpoint →
    resolved Insufficient. (See risk below — same SKU vs a "blood pressure" claim would grade very differently.)

---

## PART C — Recommended acquisition path

**Catalog + barcode (the Israeli shelf spine):** **Super-Pharm price-transparency feed**
(`prices.super-pharm.co.il`, open .gz XML, standard schema we already parse in `il_prices`).
Gives the real local SKU list, Hebrew names, EAN barcodes, prices across the chain. *This is
the only source that is genuinely "the Israeli shelf."*

**Identity / legitimacy / brand-importer bridge:** **`il_gov_data`** — `imported_foods` for
per-SKU importer/kosher/country/expiry, `food_manufacturers` for GMP/license legitimacy. Use
to validate that a brand is a registered IL supplement importer/manufacturer and to enrich
identity. Already a working client.

**Label panel (active · dose · form · claim · blend) — the scored surface:** **iHerb via a
firecrawl JSON-extract pipeline** (proven 5/5 here), **with `open_food_facts` by-barcode as a
cheap first try** (free when it hits; it mostly won't for supplements). Brand sites
(Altman/SupHerb/Solgar) as a secondary panel source where iHerb lacks the exact IL SKU.

### What needs BUILDING (concrete, with effort)

| Build | What | Effort | Notes |
|---|---|---|---|
| **A. `super_pharm` catalog client** | Add a Super-Pharm reader to `il_prices` (or a sibling). The grid is the standard PriceTransparency.WS schema; `parse_price_xml` is already shared. Mainly: enumerate the file grid (filter to `PriceFull`), gunzip, parse → `PriceItem` with provenance. | **Low** (~½ day). The parser exists; only listing/pagination differs from Shufersal/laibcatalog | Open, no login. Confirmed live 2026-06-03 |
| **B. `iherb` panel-extract pipeline** | A small module: given a product URL (or barcode/brand search), `firecrawl_scrape(json)` with the BSIP0-S schema used here → `SupplementLabel` dict + Provenance(`candidate`). Includes the lossiness rules (form-from-name flag, form=None when absent, EPA+DHA summation). | **Low–Med** (~1 day). Schema + mapping already written in `poc_real_skus/run_poc.py`; productionize + rate-limit + cache | Firecrawl credits are the cost; respectful low-volume |
| **C. Catalog↔panel BARCODE BRIDGE** | The real integration work: match a Super-Pharm IL SKU (barcode + Hebrew name + brand) to an iHerb/brand panel. Barcode-first; fall back to brand+active+dose fuzzy match on the Hebrew/English name. | **Med** (~1–2 days). This is where coverage is won or lost | iHerb IL-barcodes ≠ US-barcodes for some SKUs; bridge must be tolerant |
| **D. OCR for image-only panels** | Only if a panel is an image with no HTML text (some brand sites / Super-Pharm PDP photos). | **Med, and ONLY IF NEEDED** | **Not needed for the iHerb path** — iHerb panels are HTML text and extracted cleanly. Defer until a real image-only blocker appears |

**Smallest viable build to start the corpus:** **A + B + the barcode half of C.** OCR (D) is
**not** on the critical path. No new third-party API key is required.

---

## Biggest risks

1. **Claim→tier mapping is the dominant scoring lever, and on-label claims are vague.** The
   magnesium SKU graded **E** purely because its label claim is structure/function
   ("bone/heart/nerve/muscle"), not a studied endpoint — the *same* magnesium against a "blood
   pressure" or "sleep" claim would grade very differently. The corpus must decide, per SKU,
   **which on-label claim text is the PRIMARY claim** — that is a Nutrition/governance call,
   not a scrape. (This is by-design §2.1 behavior, but it means panel extraction alone is
   insufficient; claim selection is a curation step.)
2. **Panel non-standardization & form lossiness.** Chemical form is frequently absent from the
   panel (omega-3 TG/EE; creatine form was in the name). Form drives the Form dimension and
   the magnesium elemental conversion. Expect a non-trivial fraction of SKUs with `form=None`
   → honest 50, but it caps achievable grades.
3. **Scoping: ships-to-IL ≠ Israeli shelf.** iHerb is the richest panel source but is not the
   local shelf. Without the barcode bridge to the Super-Pharm feed, we'd be scoring a
   global catalog, not the Israeli one. The bridge is the integrity control.
4. **Image-only panels on local brand/storefront sites** (Super-Pharm PDP, some IL brands) —
   would force OCR. Mitigated by preferring iHerb HTML panels; only a risk if we must source a
   local-exclusive SKU whose panel is image-only.
5. **Coverage: our 5 actives vs the broader shelf.** The engine can only score creatine /
   magnesium / vitamin D3 / caffeine / omega-3 today. The real Israeli supplement shelf is
   mostly multivitamins, B-complex, probiotics, herbals, collagen, etc. — **dossier coverage,
   not data acquisition, is the real corpus ceiling.** Acquisition is solved; the engine's
   active coverage is the gate.
6. **ToS / volume.** Respectful low-volume only; firecrawl + cache, no bulk crawl. Not a
   blocker at corpus-build scale if rate-limited.

---

## Crisp answer to the owner

- **Do we have all the external APIs?** For the *price/catalog/identity* spine — **yes**
  (Super-Pharm transparency feed + `il_gov_data`, both live, no auth, already-shared parsers).
  For the *label panel* — **we have the tool (firecrawl + iHerb), but not yet a client**; it
  works (5/5 actives extracted and scored end-to-end here).
- **The smallest missing piece is not an API — it is a small build:** an **iHerb panel-extract
  pipeline (B)** plus a **Super-Pharm catalog reader (A)** and a **barcode bridge (C)** between
  them. ~2–3.5 days total. **No new API key, no OCR on the critical path.**
- **The true corpus ceiling is engine active-coverage (5 dossiers), not data.** Acquisition is
  feasible *now*; broadening beyond 5 actives is a Nutrition/dossier effort, not a sourcing
  one.

*All artifacts candidate / calibration-pending (EDPG). No engine change, no published-score
movement, no launch.*
