# Supplement Engine — Market Coverage & Maintenance-Economics Analysis (v1)

**Task:** TASK-171F · **Parent:** TASK-171 · **Date:** 2026-06-03 · **Author:** Research Agent
**Purpose:** decision-support for the owner's **build / widen / pause** call on the Supplement Intelligence Engine (SIE). Answers 5 coverage + maintenance questions by triangulating three measurable proxies; informs the roadmap, ships nothing, moves no score.

> **Hard framing (binding).** There is **no authoritative "Israeli supplement sales by active" dataset.** This report does **not** report a sales figure. It measures what is countable (shelf presence, search demand) and anchors it to published global category-share, labelling **every** number **MEASURED / ESTIMATED / BENCHMARK + confidence + method.** Ranges over points. Where the three lenses disagree, the disagreement is shown, not averaged away.

---

## The three lenses (what each can and cannot say)

| Lens | What it measures | Source (in-env) | Strength | Known bias |
|---|---|---|---|---|
| **L1 Shelf presence** | fraction of supplement SKUs naming each active | **Super-Pharm price-transparency feed** (chain 7290172900007, `PriceFull` branch catalog, 2026-06-03) — MEASURED | A real Israeli pharmacy shelf, the dominant supplement retail channel | Name-match **undercounts**: proprietary blends hide their actives (see §Q2). Single branch (one store's catalog). |
| **L2 Demand proxy** | Hebrew search interest (0–100, relative) | **`google_trends`** client, geo=IL, 12-mo, 19 actives — MEASURED (relative) | Israel-specific, real consumer-intent signal | Interest ≠ sales. Relative-not-absolute. One 429 (collagen) + two keyword-phrasing artifacts (see appendix). |
| **L3 Global benchmark** | category share of global/US supplement spend | published market research (firecrawl_search, 2026-06-03) — BENCHMARK | Sanity-anchor on which actives dominate spend | Not Israel; US/global mix differs (e.g. creatine is sports-niche, not mass-market). |

A secondary shelf source — `il_gov_data.imported_foods` (32,620 records) — was probed and **rejected as a coverage lens**: it is a *food-import* registry, not a supplement catalog. Supplement-as-medicine SKUs route through a different regulatory channel, so probiotics/melatonin/glucosamine returned **0** while caffeine returned 58 (energy drinks/coffee, not capsules). It is unfit for supplement shelf-share and is excluded from triangulation. (Reported here for transparency, not used.)

---

## Q1 — What share of the Israeli supplement market do the current 5 actives cover?

**Current 5:** creatine · magnesium · vitamin D3 · caffeine · omega-3 (EPA/DHA).

| Lens | Number | Method | Confidence |
|---|---|---|---|
| **L1 Shelf (Super-Pharm)** | **13.9%** of oral-supplement SKUs (51/366) name ≥1 of the 5 — MEASURED | classified 7,429-SKU branch catalog → 366 oral-supplement SKUs (oral dosage-form word, topical/cosmetic excluded) → counted active name-matches | Med |
| **L1 Shelf, blend-adjusted** | **~16–20%** — ESTIMATED | upward adjustment: ~15–20% of the 366 are name-opaque blends (e.g. "ריכוזית סילבר", "MYO BALANCE") that *contain* magnesium/D but don't surface it → name-match floor understates | Low–Med |
| **L2 Demand (Trends)** | **~28–32%** of summed search interest across the 19-active pool — MEASURED (relative) | the 5's avg-interest sum (creatine 60.5 + magnesium 84 + D 66.6 + omega-3 72.8 + caffeine 56.3 = 340) ÷ pool sum. Magnesium + omega-3 are top-tier demand; caffeine + creatine are mid | Low–Med |
| **L3 Benchmark** | D3 + omega-3 + magnesium sit inside the global **top 5–6** actives; creatine + caffeine are **sports-niche** (small mass-market share) — BENCHMARK | Grand View: vitamins = 28.1% of US ingredient share; minerals + omega-3 are next leaders; sports/energy actives are a distinct smaller segment | Med |

**Triangulated answer: ~15–25% shelf/demand-weighted coverage, Med confidence.**
The three lenses **agree in shape** (the 5 are a real but minority slice) and **disagree in level**, and the disagreement is informative:
- L1 shelf says **~14% (floor) → ~16–20% adjusted** — the 5 are present but not the bulk of the *shelf count*.
- L2 demand says **higher (~30%)** — because magnesium and omega-3 carry outsized *search* interest, so the 5 punch above their SKU count in consumer attention.
- L3 explains the split: **three of the five (D3, omega-3, magnesium) are genuine mass-market leaders; two (creatine, caffeine) are sports-niche** — strong as engine *stress-tests*, light as *coverage*.

> **Read honestly:** the current 5 were chosen to span the **evidence spectrum** (the stress matrix), **not** to maximize shelf coverage. So a low-teens-to-mid-20s coverage is expected and correct for an MVP. This is **coverage, not audited sales** — shelf-presence- and demand-weighted.

---

## Q2 — The next 10 actives to maximize shelf coverage

Ranked by combined L1 shelf SKU-count (Super-Pharm) + L2 demand (Trends avg). "Marginal coverage" = additional share of the 366 oral-supplement SKUs the active brings, by name-match (a floor — blends add more).

| Rank | Active | Shelf SKUs (L1, MEASURED) | Demand (L2, MEASURED rel.) | Marginal shelf coverage added* | Build difficulty |
|---|---|---|---|---|---|
| 1 | **Multivitamin** | 17 (4.6%) | 74.5 | **~+4–5%** | **STRUCTURALLY HARD** (per-active dose attribution; §Q4) |
| 2 | **Probiotics** | 17 (4.6%) | 74.7 | **~+4–5%** | **STRUCTURALLY HARD** (CFU viability, strain-specificity; §Q4) |
| 3 | **Vitamin C** | 11 (3.0%) | 52.0 | ~+3% | EASY (clean single-active, Strong/known) |
| 4 | **Zinc** | 8 (2.2%) | 66.4 | ~+2% | EASY (mineral, form ladder like Mg) |
| 5 | **Iron** | 6 (1.6%) | (artifact†) | ~+1.5% | EASY–MOD (form/absorption; necessity-context care) |
| 6 | **Collagen** | 6 (1.6%) | high (429‡) | ~+1.5% | MOD–HARD (claim contested; type/peptide spec) |
| 7 | **Calcium** | 5 (1.4%) | 63.0 | ~+1.5% | EASY (mineral, well-settled) |
| 8 | **Folic acid** | 5 (1.4%) | 72.7 | ~+1.5% | EASY (Strong, narrow claim; high demand) |
| 9 | **B12** | 4 (1.1%) | 58.6 | ~+1% | EASY (clean, settled) |
| 10 | **Vitamin B-complex** | 4 (1.1%) | (see B12) | ~+1% | EASY–MOD (multi-active = mini-blend attribution) |

*Marginal coverage is **net of overlap**: a multivitamin SKU already counted under "multivitamin" is not re-counted for the C/zinc/iron it contains, so per-row marginals are conservative and do **not** sum linearly to the cumulative in Q3.
†Iron Trends returned a phrasing artifact (avg 7) — the keyword "ברזל תוסף" is noisy; iron's *shelf* presence (6 SKUs) is the reliable signal. ‡Collagen Trends 429'd; its shelf presence + global benchmark both indicate **high** demand (collagen is one of the fastest-growing specialty actives).

**Tier-honest:** of the next 10, **6 are EASY** (C, zinc, iron, calcium, folic, B12 — clean single-actives, evidence-tractable like the existing minerals/vitamins), **2 are MOD** (B-complex, collagen), and the **2 highest-coverage rows — multivitamin and probiotics — are STRUCTURALLY HARD** (Q4). This is the central tension surfacing already at rank 1–2.

Deliberately **excluded** from the top-10 (lower IL shelf/demand or harder than their coverage justifies): **melatonin** (0 shelf SKUs — IL routes it pharmacist-counter/Rx-adjacent, not open shelf), **ashwagandha** (1 SKU; contested botanical), **turmeric/curcumin** (3 SKUs; contested + standardization), **CoQ10** (4 SKUs; niche), **glucosamine** (0 clean SKUs), **whey/protein** (a food-macro object, not an `(active,dose,form,evidence)` tuple — category-mismatched to the SIE).

---

## Q3 — Cumulative coverage at 15 actives (the 5 + next 10)

| Lens | Cumulative coverage at 15 | Method | Confidence |
|---|---|---|---|
| **L1 Shelf (Super-Pharm)** | **35.0%** of oral-supplement SKUs (128/366) name ≥1 of the 15 — MEASURED | union count (de-duplicated; a SKU naming two of the 15 counts once) | Med |
| **L1 Shelf, blend-adjusted** | **~40–48%** — ESTIMATED | +blends that contain a covered active but name it opaquely; +the many single-vitamin SKUs caught by C/D/B12 | Low–Med |
| **L3 Benchmark** | a 15-active set covering all major vitamins + core minerals + omega-3 + probiotics + multivit corresponds to **~55–70%** of global category spend — BENCHMARK | vitamins (28%) + minerals + omega-3 + probiotics are the bulk of published share; specialty/herbal/sports tail sits outside | Med |

**Triangulated answer: ~40–55% cumulative coverage at 15 actives, Med confidence** (shelf-count floor ~35% → blend-adjusted/spend-weighted ~45–55%).

**Diminishing-returns curve (shape):**
- The first **5** buy ~15–25%.
- The next **10** roughly **double** it to ~40–55% — but the *marginal SKUs per active are falling* (the 5 averaged ~3–4% each; ranks 6–10 add ~1–1.5% each).
- **15 does NOT reach 70%.** The curve flattens because the **long tail is real and fragmented**: the remaining ~45–60% is split across (a) **name-opaque proprietary blends** (the single biggest hidden bucket), (b) a **wide herbal/botanical tail** (ginkgo, ginseng, valerian, ashwagandha, spirulina, milk-thistle — each 1–3 SKUs), and (c) **specialty actives** (CoQ10, collagen variants, glucosamine, beauty-from-within). No single next-active moves the needle >1%.
- To get from ~50% to ~75% you do **not** add 10 more clean actives — you must score the **blend/multivitamin/probiotic machinery itself** (Q4). That is the wall.

---

## Q4 — Structurally-hard categories: how much shelf, and the headline tension

These are the categories the engine **deliberately defers** because each breaks the `(active, dose, form, evidence)` scoring unit. Shelf share measured among the 366 oral-supplement SKUs (Super-Pharm, MEASURED; name-match floor — true share higher).

| Hard category | Why it breaks the engine | Shelf share (L1, MEASURED floor) | Demand (L2) |
|---|---|---|---|
| **Multivitamin / multi-ingredient blends** | per-active **dose attribution** is impossible from the panel; can't score "is the dose adequate" when 20 actives share one serving | **≥4.6%** named "multivitamin" + an unmeasured slab of opaque blends → **realistically 10–20%** of the shelf once blends are included | 74.5 (high) |
| **Probiotics** | score depends on **CFU viability at end-of-shelf-life** + **strain-specificity** — neither is on the label nor in any client; evidence is strain-by-strain, not "probiotics" | **≥4.6%** | 74.7 (high) |
| **Herbals / botanicals** | **contested evidence** + **extract standardization** (KSM-66 vs generic ashwagandha aren't the same product); tiering a botanical is the hardest judgement | **~3%** named, +a fragmented tail → realistically **5–8%** | mixed (ashwagandha 55, turmeric 62.8) |
| **Collagen / beauty-from-within** | claim is **contested**; type/peptide/dose spec is non-standard | ~1.6% | high |

**Combined structurally-hard shelf share: ~12% by strict name-match → ~20–30% blend-adjusted, ESTIMATED (Low–Med).**

### THE HEADLINE TENSION (the business finding)

> **Yes — the biggest-selling categories are also the hardest to score.** In the Super-Pharm data, the **two single highest-coverage next actives (rank 1 = multivitamin, rank 2 = probiotics)** are *both* in the structurally-hard set, *and* they carry **top-tier demand** (Trends 74.5 / 74.7, neck-and-neck with magnesium). Multivitamins are the archetypal supplement purchase; probiotics are one of the fastest-growing segments. The engine's clean, tractable wins (vitamin C, zinc, B12, folic) are **real but individually small (~1–3% each)**; the **large blocks of shelf are exactly the blend/probiotic/herbal machinery the MVP set aside.**

This is the load-bearing fact for the build/widen/pause decision: **a clean-single-active engine has a coverage ceiling in the ~50–55% range. The top half of that ceiling is reachable; the next 20–30 points sit behind the deferred machinery, not behind "10 more dossiers."**

---

## Q5 — Estimated annual maintenance burden per dossier

Grounded in the **measured** TASK-171B build-cost report (`…/evidence_dossiers/_build_cost_report.md`) and methodology §5.1 lifecycle model (stable-vs-drift fields, detection-not-auto-update, authority re-sync, tiered sweep cadence).

**Cost model (from the measured data).** Per dossier the recurring cost lives in **4 drift fields** (`claim→evidence_tier`, `effective_dose`, `upper_limit_UL`, `form_ladder`); the **stable fields** (chemistry/identity) are compute-once and don't recur. Maintenance = a cheap **batched detection sweep** (re-run `literature` to flag new high-tier publications) + **human adjudication that fires only when a sweep actually flags something.** The authority-leverage offload: **UL/safety re-syncs to NIH ODS / EFSA** (store value + source + date, don't re-derive) — methodology §5.1 item 4.

| Dossier class | Example | Sweep cadence | Adjudication rate | **Est. hours/dossier/year** (ESTIMATED) | Confidence |
|---|---|---|---|---|---|
| **Settled** | creatine, D3, caffeine, most minerals/vitamins | **Annual** (1 detection sweep) | near-zero (settled tier rarely moves) | **~1–2 h** (detection + UL re-sync; adjudication rare) | Med |
| **Contested / active-literature** | omega-3 (CV/cognition), secondarily Mg-sleep | **Semi-annual** (2 sweeps) | moderate–high (live debate can shift consensus) | **~4–6 h** (2 sweeps + ≥1 real adjudication + golden-corpus re-validation) | Med |

> Hours are ESTIMATED. The 171B report deliberately measured **effort proxies** (queries run, papers screened, judgement vs lookup fields), **not** wall-clock — because the author was a model. The hour figures above apply a conservative human-analyst multiplier to those proxies (a settled annual sweep ≈ a batched literature re-run + read 0–1 new meta-analysis; a contested semi-annual cycle ≈ 2 sweeps + read several papers + adjudicate + re-run the 12-anchor golden corpus). Product should apply its own multiplier; the **ratio (~3–4× contested vs settled)** is the robust, measured-grounded part.

**Authority-leverage offload (measured, §2 of 171B):** of the 4 drift fields, **UL is fully delegable** (NIH/EFSA re-sync) and **dose is partially delegable** (DSLD market-prevalence check) → authority-leverage ratio ≈ **0.375**. The two highest-judgement fields — **claim-tier + form-ladder — are NOT delegable** (no external body publishes "Bari tier"). This is the **irreducible human floor** and it is correct: tiering is exactly the in-house judgement the EDPG firewall exists to protect.

**Extrapolated total annual burden (ESTIMATED, Low–Med):**

| Catalog size | Mix assumption | Annual maintenance | Method |
|---|---|---|---|
| **15 dossiers** | ~12 settled + ~3 contested | **~24–40 h/yr** (≈ 12×1.5 + 3×5) | per-class hours × count |
| **~50 dossiers** | ~42 settled + ~8 contested | **~80–115 h/yr** (≈ 42×1.5 + 8×5) + a **fixed batch-detection overhead** (one batched sweep covers the whole catalog cheaply) | per-class hours × count; detection batches, adjudication doesn't |

**What makes it unsustainable** (the named failure mode): **not** build cost — it is the **contested fraction growing and being treated like the settled majority.** Maintenance scales with the *number of contested/live-debate claims*, not the headcount of dossiers. If a category were added where most actives are contested (botanicals/herbals — exactly the Q4 hard set), the contested share inflates, adjudication stops being rare, and the cost curve bends from linear to punishing. The second failure mode is **silent staleness**: a contested dossier that misses its sweep misranks without erroring (omega-3 is the canary). The model is sustainable **iff** cadence is **tiered by evidence-settledness** (annual default, semi-annual for flagged contested claims) with a **hard staleness alarm** on any contested claim past `review_by` — i.e. the §5.1 model, applied. The 171B verdict ("GO for Phase-2, math works *and* scales, provided contested actives are the budgeted exception not the rule") holds and is corroborated here.

---

## Bottom line for the owner (build / widen / pause)

The coverage math **favors a bounded widen, not an open-ended one.** Widening from 5 → 15 clean actives roughly **doubles coverage to ~40–55%** at low, well-understood maintenance cost (~24–40 h/yr, dominated by 2–3 contested dossiers) — this is the **tractable, GO portion**. But the curve **flattens hard at ~50–55%**: the next 20–30 coverage points do **not** come from more single-active dossiers — they sit behind **multivitamins, probiotics, and herbals**, which are simultaneously the **biggest-selling, highest-demand** categories *and* the **structurally hardest to score** (the engine's deferred machinery). So the structurally-hard-category share **caps what a single-active engine can ever reach** without building the blend/CFU/standardization subsystems. **Recommendation framing for the decision:** widen to ~15 tractable actives now (high coverage-per-effort, sustainable maintenance), and treat the deferred-machinery categories as a **separate, explicitly-budgeted strategic decision** — because that is where both the remaining market *and* the remaining difficulty live. Do not pause; do not widen blindly into blends/probiotics expecting clean-active economics.

---

## Appendix — Methods, sources, confidence

**MEASURED.**
- **L1 Shelf:** Super-Pharm price-transparency feed, chain 7290172900007, `prices.super-pharm.co.il`, `Category-equals=PriceFull`, branch file `PriceFull7290172900007-101-202606030707.gz`, fetched 2026-06-03 via the `il_prices` plumbing (`parse_price_xml`). 7,429 SKUs → 366 oral-supplement SKUs (oral dosage-form word present, topical/cosmetic words excluded). Active counts by Hebrew/English name-match. **Caveats:** single branch; name-match is a **floor** (proprietary blends hide actives → undercount); residual noise (dishwasher tablets, coffee capsules) inflates the 366 denominator slightly → coverage % is conservative on both ends.
- **L2 Demand:** `google_trends` client, geo=IL, `today 12-m`, 19 Hebrew actives, run 2026-06-03. Values = relative search interest 0–100 (directional, not volume). Top demand: magnesium 84, probiotics 74.7, multivitamin 74.5, omega-3 72.8, folic 72.7. **Artifacts:** collagen 429'd (no value — benchmarked high instead); iron ("ברזל תוסף" avg 7) and CoQ10/vitamin-B phrasings returned noisy lows — for these, shelf presence is the trusted signal. Trends informs **sequencing**, never quality (Product fence, §google_trends docstring).

**BENCHMARK.**
- **L3:** firecrawl_search 2026-06-03. Grand View Research (US dietary supplements): **vitamins = 28.1% of ingredient share, 2025**; minerals + omega-3 are next leaders; probiotics + specialty/herbal are the growth tail. Nutrition Business Journal: US market ~$69.3B 2024. PMC global overview (PMC10421343). Used only to anchor *which actives dominate spend* and to sanity-check L1/L2 — **not** Israel-specific; adjust down for IL where creatine/caffeine are sports-niche.

**Rejected source (transparency).** `il_gov_data.imported_foods` (32,620 records) — a *food-import* registry, not a supplement catalog; supplement-as-medicine SKUs route elsewhere (probiotics/melatonin/glucosamine = 0; caffeine = 58 from energy drinks). Probed, found unfit for supplement shelf-share, **excluded** from triangulation.

**Maintenance (Q5).** Grounded in measured TASK-171B `_build_cost_report.md` (effort proxies: 21 lit queries, ~118 papers, 23 human-judgement fields, 29 mechanical-lookup fields across the 5; omega-3 ≈ 2× any other) + methodology_v1 §5.1 (stable/drift split, detection-not-auto-update, authority re-sync, tiered cadence, go/no-go gate). Hour figures are ESTIMATED (human-analyst multiplier on measured proxies); the **settled-vs-contested ratio (~3–4×)** and the **authority-leverage ratio (~0.375)** are the measured-robust parts.

**Confidence key:** High = directly measured, low bias · Med = measured with a known correction or a corroborated estimate · Low = single-lens estimate or benchmark-extrapolated. No point estimates are offered without a range.

**Scope.** Analysis only. No scoring change, no engine edit, no roadmap move. Read-only sources, a handful of calls each, robots/ToS honored. Status proposed: **RETURNED.**
