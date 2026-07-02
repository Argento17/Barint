# Magnesium Worldwide Benchmark — v1 (LOCKED spec)

> **Status: EDPG / candidate. NO published score movement.** This is the reference-perfect
> target a commercial product is rated *against* (distance-from-anchor), pending Nutrition
> D6/D7 co-sign before it drives any consumer-facing score. TASK-361.
>
> **Provenance:** triangulated from THREE independent research passes (2026-06-20):
> ChatGPT Deep Research PDF (`research/Magnesium Oral Supplements Worldwide Benchmark.pdf`,
> the load-bearing source — it alone delivered prices + per-product metrics), plus two
> earlier pasted passes. Where they diverged, the resolution + reason is recorded below.
> All values carry an authority; OFF is not a source anywhere.

## 1. The standing caveats (read first — they bound everything)
1. **Label-truthful, not lab-verified.** Bari rates the *declared* label. A Polish AAS assay
   of 116 EU supplements found **58.7% outside legal tolerance** (actual content 98% below to
   304% above the label), and the discrepancy was **independent of price**. Bari cannot detect
   content fraud without lab assay — the score is "best case, assuming the label is honest."
2. **Banded targets, never one universal number.** US RDA (310–420) ≠ EFSA AI (300–350) ≠
   WHO/FAO RNI (220–260). Store authority-specific values + a pragmatic supplemental band;
   surface divergence, do not average it away.
3. **Label-declared elemental governs.** Compound-mass → elemental conversion is ambiguous when
   hydration state / assay is undisclosed. When the label states elemental mg, that number wins.
4. **Price snapshots are stale fast** — every price carries a capture date.
5. **Price is WITHIN-region only.** A product's price-value is ranked against *its own national
   shelf* — never across countries. Cross-border price comparison is confounded by VAT, currency,
   purchasing power, and import/shipping (owner ruling 2026-06-20). The *quality/dose* benchmark is
   worldwide (science is universal); *price positioning* is local.

## 2. Reference-perfect anchor (the "perfect product"), by claim
| Use / claim | Defensible elemental dose band | Evidence tier | Reference form | UL (supplemental) | Authority |
|---|---|---|---|---|---|
| **General RDA-gap / low-status repletion** | **100–200 mg/day** (gap-closing; US food intake ~234–268 mg leaves a ~50–150 mg gap) | **Strong** (repletion/adequacy) | **Citrate** (glycinate = gentle alt) | US/AU 350 · EU/SCF 250 | NIH ODS; IOM DRI; EFSA AI; WHO/FAO RNI |
| **Constipation / laxative** | ~1,000–2,000 mg/day (hydroxide, pharmacologic — not nutrition) | Strong (pharmacologic) | Hydroxide | exceeds routine UL by design | DailyMed (milk-of-magnesia) |
| **Migraine prophylaxis** | 400–600 mg/day | **Moderate** | Citrate/oxide (trial-guided) | exceeds EU UL; near/over US UL | American Headache Society; 2015 review |
| **Blood pressure** | 300–400 mg/day (≥1–3 mo) | **Moderate** | Citrate | within US UL; over EU UL | 2016 meta-analysis, 34 RCTs, 368 mg median |
| **Sleep** | 200–400 mg/day (no firm target) | **Weak** | Bisglycinate (tolerance) | — | systematic reviews (contradictory) |
| **Muscle cramps** | no reliable benchmark | **Insufficient** | none | — | Cochrane CD009402 (no benefit) |
| **Stress / energy** | 100–200 mg (repletion only) | **Weak** | Citrate | — | EFSA: fatigue/energy claims OK; "mental stress resistance" NOT authorized |

## 3. Form ranking (RESOLVED — citrate-first, the key correction)
> Direct *human comparative* bioavailability evidence is strongest for **citrate** (and
> chloride/lactate/aspartate) over oxide. **Glycinate/bisglycinate is a tolerability-forward
> alternative, NOT the proven bioavailability winner** — its comparative evidence is thinner
> than its marketing. This overrides the earlier glycinate-first drafts.

**Hierarchy:** citrate > chloride / lactate / aspartate > bisglycinate/glycinate (high tolerance,
weaker comparative data) > malate / taurate (sparse human data) > carbonate / hydroxide (GI-active)
> **oxide** (cheap, dense, poorly absorbed ~4%).

## 4. Elemental fractions (hydration-aware — label species matters)
oxide 60.3% · trimagnesium dicitrate anhydrous 16.2% / citrate nonahydrate 11.9% ·
bisglycinate 14.1% / bisglycinate dihydrate 11.7% · malate 15.5% · taurate 8.9% ·
carbonate 28.8% · chloride anhydrous 25.5% / hexahydrate 12.0% · lactate 12.0% / dihydrate 10.2% ·
hydroxide 41.7%. A label naming only "citrate"/"chloride" without the species is *less transparent
than it looks* — flag it.

## 5. The two consumer metrics (the deliverable)
1. **Promise-Delivery Ratio** = delivered elemental daily dose ÷ **lower bound of the benchmark
   band for the product's OWN main claim**. `<1` = misses even the lowest defensible bar for its
   own promise. (Generic support threshold = 100 mg/day; sleep = 200 mg/day; migraine = 400.)
2. **Price per effective daily dose** = price ÷ (total elemental mg in pack ÷ effective dose),
   currency + capture-date stamped. **Ranked by percentile WITHIN the same national shelf only**
   (see caveat 5) — never compared across countries.

**Value matrix (the "luxury but crap" flag):**
| | Delivers (ratio ≥ ~1) | Under-delivers (ratio < ~1) |
|---|---|---|
| **Premium-priced (top quartile of the SAME national shelf)** | premium, earned | ⚠️ **premium price, weak delivery** |
| **Low-priced** | best value | cheap & weak |

**Israeli pilot result (2026-06-20, n=19, price within-IL):** worst-value = boutique forms —
נוטריקר טאוראט (PDR 0.07, 100th price %ile), נוטריקר נאנו-ליפוזומלי (0.12, 94th), טינק מאלאט
(0.21, 88th), TRIOMAG (0.32, 82nd), אמורפיקיור carbonate (0.46, 71st). Best-value = oxide-520
trio + MagUp (PDR 2.7–3.1, 6th–24th %ile). The metrics differentiate the nine engine-"49" products
across PDR 0.07→1.08 with **no score change** — candidate overlay, D7 decides any score feed.

Validated exemplar (real shelf): **CanPrev Bis-Glycinate 80 "Ultra Gentle"** — most expensive
per effective day in the Canada sample, delivers **0.80×** its own minimum benchmark. Broader
pattern across all three sources: **price does not buy delivery; the shelf prices chelation more
aggressively than the evidence justifies** — best value was the plain citrate product in every region.

## 6. Real shelf data status (per-region scrapes)
- **US — DONE:** 64 magnesium-primary products via DSLD (`benchmark/shelf_us_dsld.json`,
  2026-06-20). Real distribution: median **212 mg/serving**, p90 **400**, range 100–500;
  form mix citrate-dominant (38/64) — confirms §3.
- **Canada — DONE:** 60 magnesium-primary NHP licences via Health Canada LNHPD (`benchmark/shelf_ca_lnhpd.json`,
  2026-06-20). Corpus: 1,570 unique active Mg-primary licences; sample every-26th by lnhpd_id.
  Distribution (46/60 with elemental_mg populated): median **178 mg/serving**, p90 **350 mg**, range 5–3000 mg
  (3000 mg = 12-form blend product, 250 mg × 12 forms; bisglycinate-dominant (23/60), not citrate-dominant
  as in the US — reflects the Canadian market favouring chelated forms). Client: `integrations/clients/lnhpd.py`.
  SSL fix: certifi CA bundle (`certifi.where()`), per the task spec — no verification disabled.
- **Australia — TGA ARTG:** BLOCKED. www.tga.gov.au DNS resolves but all HTTP traffic times out
  from this environment (geo/firewall block). EBS portal (ebs.tga.gov.au) reachable but has no
  public ARTG data endpoints. Client stub + unblock instructions at `integrations/clients/tga.py`;
  blocked output at `benchmark/shelf_au_tga.json`. Unblock path: download TGA quarterly ARTG extract
  (Excel) from https://www.tga.gov.au/resources/artg from a reachable environment.
- **EU — PARTIAL (done, indicative):** no central DB (Directive 2002/46/EC). C3 hunt (P244) gathered
  8 magnesium-primary products across France / Italy / Spain (Nutri&Co B6, Arkopharma ARKOMAG, Novoma,
  Magnesio Supremo + Stick + Notte Relax, Solgar Citrato ES). Indicative distribution: median ~300 mg/day,
  ~p90 430 mg; citrate-leaning. Recovered detail: `benchmark/shelf_eu_c3_recovered.md` (the clean C3 file
  was clobbered by the router capture — known quirk). Statistically weak (small n); national registries
  are PDF-only / partial as expected.
- **Price (all regions incl. Israel):** retailer leg, not in any official DB — separate scrape.

## 6b. Cross-region shelf picture (elemental mg/day at labeled dose)
| Region | Source | n | Median elemental | Dominant form |
|---|---|---|---|---|
| 🇺🇸 US | DSLD | 64 | **212 mg** | citrate |
| 🇨🇦 Canada | LNHPD | 60 | **178 mg** | bisglycinate |
| 🇪🇺 EU | C3 partial | 8 | **~300 mg** | citrate |
| 🇮🇱 Israel | corpus | 18 | **~90 mg** | oxide |
| 🇦🇺 Australia | TGA | — | BLOCKED (geo) | — |
**Headline:** the Israeli shelf delivers roughly **half (or less)** the elemental magnesium of the
US/Canada/EU shelves at the labeled daily dose. Price is NOT compared across regions (caveat 5).

## 7. Key sources
NIH ODS Magnesium (HealthProfessional) · IOM/NAM DRI · EFSA DRV 2015 (10.2903/j.efsa.2015.4186) +
Art.13.1 claims (10.2903/j.efsa.2010.1807) · WHO/FAO RNI · SCF/EC UL (out105_en.pdf) ·
Cochrane CD009402 · American Headache Society migraine guidance · 2016 BP meta-analysis
(hypertensionaha.116.07664) · FDA supplement labeling guide · Directive 2002/46/EC ·
Polish AAS assay (label-vs-actual) · NIH DSLD · Health Canada LNHPD. Full inline URLs in the
three research artifacts under `research/`.
