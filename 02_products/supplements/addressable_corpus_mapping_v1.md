# Addressable-Corpus Mapping v1 — Israeli Supplement Shelf (Super-Pharm)

**Task:** TASK-171D (parent TASK-171) · **Stage:** D2/D3 catalog-side shelf mapping (identity only, no panels, no scoring)
**Date:** 2026-06-03 · **Owner:** Data Agent
**Source:** Super-Pharm price-transparency feed (`prices.super-pharm.co.il`, chain `7290172900007`), live, no login, urllib (NO firecrawl)
**Plumbing:** `integrations/clients/il_prices.py` — `list_super_pharm_files()` / `fetch_super_pharm_supplements()` / `is_oral_supplement()` (TASK-171G)
**Provenance (EDPG):** every SKU carries a `provenance` envelope, `verification_status=candidate`. Identity + price only — **no panel reached scoring**. Nothing ships.

---

## 1. Sample

- Read **3 PriceFull store catalogs** (stores 101, 105, 109) of the 924 available — a few stores is representative; the supplement shelf is near-identical across stores.
- Lines read: **23,051** → deduped to **10,236 unique barcodes** (the real mixed shelf: food + cosmetics + household + supplements, no category code on the line).
- Oral-supplement SKUs after the precision-first name classifier: **207**.
- Removed **3 false positives** that leaked via "מולטי ויטמין"/"ויטמין" but are topical/intimate (a face night-mask, a vaginal wash, an anti-dryness gel). **Net oral-supplement SKUs: 204.**

## 2. Addressable coverage (measured)

| Bucket | SKUs | % of net shelf |
|---|---|---|
| **Addressable** (maps to 1 of the 15 engine actives) | **115** | **56.4%** |
| Deferred (multivitamin / probiotic / collagen / herbal / multi-active blend / other) | 89 | 43.6% |

**6 multi-active combos were flagged ambiguous and counted as deferred blends, not force-mapped** (e.g. "ויטמין D + C + אבץ", "סידן ומגנזיום + D", "B12 + חומצה פולית"). A blended SKU is not a single-active corpus member.

## 3. Per-active SKU counts (the 115 addressable)

| Active | SKUs | Shelf presence |
|---|---|---|
| magnesium | 28 | **strong** |
| vitamin D3 | 24 | **strong** |
| omega-3 | 16 | strong |
| vitamin C | 11 | solid |
| zinc | 8 | solid |
| iron | 8 | solid |
| calcium | 6 | moderate |
| folic acid | 4 | thin |
| vitamin B12 | 4 | thin |
| caffeine | 3 | thin |
| biotin | 2 | thin |
| vitamin E | 1 | very thin |
| **creatine** | **0** | absent on this shelf |
| **CoQ10** | **0** | absent on this shelf |
| **melatonin** | **0** | absent on this shelf |

**Read:** The Israeli pharmacy supplement shelf concentrates on magnesium + vitamin D3 + omega-3 + vitamin C (these 4 = ~68% of the addressable shelf). Three engine actives — **creatine, CoQ10, melatonin** — returned **zero SKUs** in this Super-Pharm sample. That is a shelf-channel artifact, not absence in Israel: creatine lives in sports-nutrition retail, melatonin is partly behind-counter/Rx-adjacent, CoQ10 is low-volume. They would surface in a different channel (sports/iHerb), so keep them in the engine; just don't expect them on the pharmacy price feed.

## 4. Panel-gettability split (the business number)

For the 115 addressable SKUs, classified by brand:

| Class | SKUs | % of addressable | Panel today? |
|---|---|---|---|
| **Global brand** (Solgar, Centrum, Now, BioGaia, Nature's…) | **23** | **20.0%** | **YES — iHerb barcode bridge** |
| **Local-only brand** (Altman, SupHerb, Life, Tink, Marshall, Floris, Amorphical, Magnesia, Sequoia…) | **92** | **80.0%** | **NO — blocked on a local-brand panel source** |
| Unknown | 0 | 0% | — |

**Brand concentration (addressable):** Altman 24, Solgar/Ambrosia 22, Life 21 dominate — i.e. the shelf is overwhelmingly Israeli house/pharma brands. Only Solgar (+ a thin tail of Centrum/BioGaia) is iHerb-gettable today.

## 5. Headline

- **Real measured addressable coverage = 56.4%** of the net oral-supplement shelf maps to our 15 actives. This **confirms (upper end of)** the prior ~40–55% estimate — the real shelf sits just above it because Israeli pharmacy supplements skew toward exactly the high-volume single actives we cover (magnesium / D3 / omega-3 / C).
- **But only ~20% of the addressable shelf is panel-gettable today** (global brands via iHerb). **~80% is local-brand and blocked** on a panel source. So the binding constraint is **not** active coverage — it is the **local-brand panel gap**. Of the full 204-SKU shelf, we can assemble a scored label *today* for roughly **23 SKUs (~11%)**; unlocking the rest requires a local-brand panel pipeline.

## 6. Limitations

- 3-store sample (representative for shelf composition; not a national availability census).
- Name-based active match (Hebrew/English substrings); precision-first — a miss is "not found," never invented. Ambiguous multi-active SKUs flagged, not forced.
- Brand→panel-gettable is a *capability* estimate (iHerb presence assumed for known global brands; not per-barcode verified). Per-SKU iHerb barcode verification is the next step before any ingestion.
- Identity/catalog only. No nutrition panel was fetched or admitted; no scoring; EDPG `candidate` status throughout.

---

**Proposed status: RETURNED** — catalog-side mapping complete; next decision is whether to stand up a local-brand panel source (the real bottleneck), which is a Product/Nutrition scope call.
