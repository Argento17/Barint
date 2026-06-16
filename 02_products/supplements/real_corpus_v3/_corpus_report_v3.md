# Real Israeli Supplement Corpus — v3 re-measurement sprint (measured)

**Task:** TASK-171 (revival) · **Date:** 2026-06-13 · **Status:** candidate / EDPG — nothing ships, no published score.
**Owner ask:** "solve acquisition." This sprint re-measures the acquisition yield that the v2 MVP
run (TASK-171J) reported at **6.8%** — a number that closed the program as "scraping can't reach
the Israeli shelf." The hypothesis under test: that 6.8% was a *thin-pool execution artifact*
(the v2 run died on a session limit with only 8 panels ever scraped, and used a single acquisition
method), **not** the real ceiling.

## Headline — the hypothesis holds

| Metric | v2 (TASK-171J) | **v3 (this sprint)** |
|---|---|---|
| Scoreable yield | **6.8%** (8/118) | **64.0%** (16/25) |
| Acquisition methods used | 1 (resolver vs a tiny scraped pool) | 3 (brand panel · retailer/search panel · name-derived) |
| Tooling | firecrawl (session-cut) | WebFetch + WebSearch (this environment) |

Yield by acquisition method (of the 16 scored): **brand_panel 4 · search_panel 8 · name_derived 4.**
The two methods the v2 run lacked entirely (retailer/search panels + name-derived single-active doses)
account for **12 of the 16** scored SKUs. That is the whole story of the 6.8%→64% jump.

**Excluding non-acquisition failures** (1 false-positive that isn't a supplement + 2 out-of-ontology
omega-5 products), true acquisition yield = **16/22 = 73%** — squarely inside the feasibility probe's
original ~75–85%-addressable projection (TASK-171I). v2's 6.8% was an execution floor; ~73% is the
real signal.

## The sample (brand-stratified, 25 SKUs — NOT cherry-picked)

Drawn proportionally across the live Super-Pharm addressable shelf (118/200 SKUs map to the 15 engine
actives): altman 4 · other 7 · life 5 · supherb 4 · sequoia/tink/magnesia/solgar/floris 1 each.
Stratified deliberately so the measured yield reflects the real shelf mix (the v1 feasibility probe's
optimism bias came from hand-picking products known to be on the e-tailers).

## The 16 scored — the real Israeli shelf through Bari's engine (all candidate)

| Grade | Score | Active | Method | Product | Binding constraint |
|---|---|---|---|---|---|
| B | 77.5 | vitamin_c | brand | Altman Vitamin C500 Liposomal | blend dominant (immune) |
| B | 71.6 | caffeine | search | SupHerb Caffeine 200mg | blend dominant |
| B | 69.1 | vitamin_c | name | Vitamin C500 (generic) | blend dominant |
| B | 69.1 | vitamin_c | name | Life Vitamin C 500 | blend dominant |
| C | 59.2 | magnesium | search | Amorphicure pH Magnesium 160mg carbonate | blend dominant |
| D | 49.0 | vitamin_d3 | name | Life Vitamin D-400 (400 IU) | cap-2 fairy dust (under-dose) |
| D | 49.0 | iron | search | SupHerb Iron 9-months 30mg | cap-3 honesty |
| D | 49.0 | vitamin_b12 | search | SupHerb B12 + folic 1000mcg | cap-3 honesty |
| D | 49.0 | iron | search | Tink Iron Comfort 36mg | cap-3 honesty |
| D | 49.0 | vitamin_c | search | Floris Vitamin C Trio 50mg | cap-2 fairy dust (under-dose) |
| E | 34.0 | biotin | brand | Altman Biotin 1000mcg | cap-1 insufficient evidence (cosmetic) |
| E | 34.0 | biotin | search | Solgar Biotin 1000mcg | cap-1 insufficient evidence (cosmetic) |
| E | 34.0 | omega3 | brand | Altman Omega 3 – 9 months | cap-1 (pregnancy claim unmapped) |
| E | 34.0 | omega3 | search | SupHerb Omega 3 (EPA 180/DHA 120) | cap-1 (heart claim → contested) |
| E | 20.0 | magnesium | brand | Altman Magnesium Balance 450mg oxide | **veto-safety (>UL)** |
| E | 20.0 | magnesium | name | Hadas Full-Mag 600mg | **veto-safety (>UL)** |

The grades reproduce every prior validated behavior on fresh, independently-acquired real products:
oxide over-dose → safety veto (Altman 450, Hadas 600); cosmetic biotin → cap-1 (Altman + Solgar);
the "1000mg fish oil hides EPA 180/DHA 120" honesty/dose trap (SupHerb omega); under-dosed D-400 and
50mg vitamin C → fairy-dust cap. Grade spread B·C·D·E is healthy (no artificial clustering).

## The 9 unscoreable — and what each one actually means

| SKU | Reason | Category of failure |
|---|---|---|
| Aroma decaf coffee capsules | name matched "קפאין" inside "נטול **קפאין**" (caffeine-**free**) | **false positive — not a supplement** (inflates addressable count) |
| Granagard nano-omega 5 ×2 | pomegranate-seed **punicic acid (omega-5)**, not EPA/DHA | **out of engine ontology** (coverage gap, not acquisition) |
| Life calcium citrate | no per-serving dose retrievable anywhere | **house-brand wall (BD)** |
| Life magnesium citrate | no dose retrievable | **house-brand wall (BD)** |
| Life omega "elite zero" 600 | no EPA/DHA split retrievable | **house-brand wall (BD)** |
| Nutricare iron Lipofer | dose behind a bot-walled e-tailer (vitamins4all) | acquisition miss (tooling) |
| Sequoia Lipo folate+B12 syrup | no dose retrievable | acquisition miss (niche) |
| Magnesia FOCUS | no dose retrievable | acquisition miss (niche) |

**The residue is exactly the predicted shape:** the 3 genuine structural misses are all **Life
(Super-Pharm house brand)** — no brand site, no e-tailer panel — the one slice only a manufacturer/
importer **data feed (BD, not engineering)** closes. The 2 omega-5 products are an engine-coverage
gap, not an acquisition failure. The decaf is a detector false-positive worth fixing in the active
mapper.

## Tooling reality in THIS environment (matters for any scale-up)

- **Brand sites (Altman) — WebFetch works**, full panel incl. barcode. Clean.
- **WebSearch snippets reliably surface per-active dose+form** for single-active mineral/vitamin SKUs
  (Amorphicure 160mg carbonate, SupHerb caffeine 200, Tink iron 36 bisglycinate, etc.).
- **Name-derived** path scores single-active SKUs whose name encodes active+dose (Life D-400, C500)
  with zero fetches — the "PDP single-active" band the decision pack costed but v2 never built.
- **vitamins4all (the breadth e-tailer the v1 probe relied on) is bot-walled here** (Cloudflare
  "verifying your request"). gov.il and some e-tailers (epharma) also block/503. So the *firecrawl*
  the original program assumed is not available — yet yield is still 64%/73% via brand sites + search.
  A real scale-up should budget a JS-capable scraper for the walled e-tailers to recover the niche
  misses (Nutricare/Sequoia/Magnesia class).

## Calibration items surfaced (for Nutrition D6 — none block the yield finding)

1. **cap-3 "core_active_dose_hidden_in_blend" fires on simple single-active iron/B12 SKUs** (SupHerb
   iron, SupHerb B12, Tink iron) that are NOT proprietary blends. Looks like a curation/label-shape
   artifact, not real honesty failure — needs an engine/curation check before any grade is authoritative.
2. **Omega-3 pregnancy & "heart" claims → cap-1.** Altman prenatal omega (DHA-for-pregnancy) and SupHerb
   "cardiovascular" omega both fall to E because the claim doesn't map to a Strong omega endpoint. Same
   open question the v2 run raised: should vague "heart" pin to the contested-CV or the Strong-triglyceride
   tier, and is there a DHA-pregnancy studied endpoint to author? (Nutrition D6.)
3. **Detector false-positive** ("נטול קפאין" → caffeine) + **omega-5 vs omega-3 conflation** in
   `detect_active_slug` — tighten the active mapper (negative-lookahead on נטול; punicic/רימונים ≠ omega3).

## Bottom line
The supplement category was parked on a **measurement that was wrong by ~10×.** Acquisition is not a
6.8% dead end — it is **~64% measured / ~73% of genuinely-addressable SKUs**, reachable with ordinary
WebFetch + WebSearch, no firecrawl. The honest residue is the **Life house-brand slice (a BD/data-feed
ask)** plus an engine-coverage gap (omega-5) and detector noise — exactly what the v1 feasibility probe
predicted before v2's execution buried it. **The engineering wall the program closed on does not exist
at the scale claimed.** Re-decision for the owner: this is now a credible-corpus, real-launch question,
not a "can we even acquire" question.

## Artifacts
- `_corpus_run_v3.json` — full per-SKU results (25 attempted, 16 scored, traces)
- `skus/*.json` — scored SKU records · `cache/*.json` — acquired candidate panels (method-tagged)
- `build_addressable.py` · `select_sample.py` · `build_cache.py` · `run_v3.py` — the pipeline
- Engine: `03_operations/supplement_engine/proto_v0/` (unchanged; golden 17/17) · methodology v1.4
