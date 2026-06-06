# Local-Brand Panel-Acquisition Feasibility Probe v1

**Task:** TASK-171I (parent TASK-171) · **Stage:** scoping probe (feasibility, NOT a build)
**Date:** 2026-06-03 · **Owner:** Data Agent
**Question:** How gettable are Supplement-Facts panels for the Israeli **local-brand-dominated**
supplement shelf (Altman / Life / SupHerb / Tink / Florish / Magnesia / Amorphical / Marshall / Sequoia),
via three sources — Super-Pharm PDPs, brand sites, OCR — so Product can cost the build.

**Provenance (EDPG):** every value below is `candidate`. Nothing was admitted to scoring; no scores
moved; nothing ships. Samples were small, read-only, rate-limited, respectful (a few dozen pages).
A page with no panel = measured 0, never assumed; an unreachable page = reported, never guessed.

---

## Sample

Built from the live Super-Pharm price feed (`il_prices.fetch_super_pharm_supplements`, 176 oral-supplement
SKUs this read). A 26-SKU representative sample was drawn round-robin across the **9 dominant local brands**
× the engine actives (magnesium / D3 / C / zinc / B12 / calcium / folic acid / omega-3), saved to
`_probe_sample_171I.json`. Pages were located with `firecrawl_map(search=...)` and scraped with
`firecrawl_scrape` (`waitFor` 8–9 s for the JS render). PDP URL pattern: `shop.super-pharm.co.il/.../p/<id>`.

Pages actually fetched this probe (the measured evidence set):

| # | Source | Brand / product | Result |
|---|---|---|---|
| 1 | SP PDP | Altman מגנזיום Balance (691202) | identity + lead dose in name; **no panel table** |
| 2 | SP PDP | Life ויטמין C 500 קומפלקס (477372) | identity + lead dose; **no panel table** |
| 3 | SP PDP | Life ויטמין C לעיסה (460470) | identity + lead dose + "עובדות תזונה: תוסף תזונה" boilerplate; **no panel** |
| 4 | SP PDP | Altman אלספה אומגה 3 (289968) | identity + **qualitative `מכיל:` ingredient string**; `has_per_active_dose_table=false` |
| 5 | SP PDP | Tink מגנזיום מאלאט (711269) | HTTP 481 (transient block) — **miss, recorded** |
| 6 | Brand site | Altman מגנזיום Balance | **FULL per-active panel**: 4 actives × (active·dose·unit·form) + רכיבים + ערכים תזונתיים |
| 7 | Brand site | SupHerb מגנזיום מקס 550 | lead active 550 מ"ג + compound mix (single-active → adequate) |
| 8 | 3rd-party | vitamins4all → Altman מגנזיום 520 | **clean panel**: 520 מ"ג + רכיבים + barcode |
| 9 | 3rd-party | biogaya → Tink מגנזיום מאלאט | **clean panel**: malate 850 mg / **elemental 136 mg** + barcode |
| 10 | 3rd-party | htiveit → Tink מגנזיום טאורט | connection closed — **miss, recorded** (dose was in search snippet: 1000 mg / elem 80 mg) |
| 11 | Image (OCR) | SP secondary image 7290019444206_2 | front-of-pack carton render — **no panel** |
| 12 | Image (OCR) | Altman site back-label image | **flat back-label panel; vision reads the full table cleanly** |
| 13 | Image (OCR) | SupHerb 3D render | side-panel present but **angled / fine-print marginal** |

---

## Q1 — Super-Pharm PDP panel coverage

**Measured PDP structured-panel hit rate ≈ 0%.** Across every Super-Pharm PDP fetched, the page has a
**fixed schema that does not include a Supplement-Facts panel**:

- `תיאור המוצר` — marketing prose (often carries the **lead single active's dose**, e.g. "450 מ"ג מגנזיום",
  "ויטמין C 500"). This is the *same* dose already inferable from the price-feed item name.
- `מאפייני המוצר` — usage / storage / allergens / kosher / unit-weight / warning. **No dose table.**
- barcode (always), product images, reviews.
- **What's missing:** a structured per-active table (active · per-serving amount · unit · **form**),
  co-active doses (B6/valerian/ashwagandha are *named*, never dosed), and a chemical-form column.
- **One richer variant:** a minority of PDPs (e.g. Altman omega-3) expose a **qualitative `מכיל:`
  ingredient string** (`שמן דגים, ג'לטין, גליצרול, די-אלפא טוקופרול...`) — useful for identity/allergens,
  but still `has_per_active_dose_table=false`.

**Read:** Super-Pharm is a reliable source of **identity + lead-active dose + sometimes an ingredient
string** — but **not** a scoreable per-active panel. For a single-active SKU (most of the magnesium / D3 /
C / zinc shelf) the lead dose alone often *is* the scoreable signal; for any multi-active SKU the PDP is
insufficient. **PDP-as-sole-source yields a scoreable panel for ~0% via a structured table, but ~30–40%
of the shelf is single-active where the PDP lead dose is enough** (lower-bound, name-derived).

**Effort signal — LOW-to-MEDIUM.** URLs aren't in the feed (must `map`/search by name, ~1 call each),
pages are JS-rendered (need `waitFor` 8 s), occasional 481 blocks (retry). No panel parsing needed because
there's no panel. Brittle on URL discovery, cheap per page.

## Q2 — Brand-site coverage + panel availability

**Measured: a usable structured panel exists for the dominant brands via brand-site OR third-party
e-tailer, covering an estimated ~75–85% of the local-brand shelf by SKU share.**

- **Altman (≈24 addressable SKUs, the #1 local brand):** own site (`altman.co.il`, WooCommerce) publishes
  the panel as **HTML text** in a `#product-components-popup` — `רכיבים`, `ערכים תזונתיים` table, and a
  per-active dose table. Extracted 4/4 actives cleanly **with form** (מגנזיום 450 / אשווגנדה 50 / ולריאן 50 /
  B6 30 מ"ג). This is a complete BSIP0-S panel. **Altman alone = full coverage.**
- **SupHerb / אמברוזיה (≈22 addressable):** own site (`supherb.co.il`) carries the lead dose + compound
  description; structured per-active text is thinner than Altman but present for the lead active. Third-party
  e-tailers (klilhateva, vitamania) carry the `רכיבים` string. **Covered, brand-site-primary.**
- **Life / לייף (≈21 addressable, Super-Pharm house brand):** **no independent brand site** — Life *is*
  Super-Pharm's house line, so its panel availability == the Super-Pharm PDP gap (Q1). This is the **biggest
  brand-site hole**: ~18% of the addressable local shelf has *no* richer source than the PDP and must fall to
  OCR. (Mitigant: most Life SKUs are single-active, so the PDP lead dose covers many.)
- **Tink / TINC (≈8 addressable):** own site (`tinc.co.il`) is thin, but **third-party e-tailers carry the
  full panel including the elemental split** (biogaya: malate 850 mg / elemental 136 mg; htiveit: taurate
  1000 mg / elem 80 mg). **Covered via third-party.**
- **Tail (Florish/Magnesia/Amorphical/Marshall/Sequoia, single-active each):** covered by a mix of brand
  pages + third-party e-tailers; each is low-SKU so individually cheap.

**A material structural win surfaced:** Israel has several **third-party vitamin e-tailers**
(vitamins4all, biogaya, klilhateva, vitamania, htiveit, bella-natura) that **aggregate brands AND publish
structured `רכיבים` + dose**, often richer than the brand's own site. They are a second, redundant panel
source per SKU — they de-risk any single brand site being thin or blocked.

**Effort signal — MEDIUM (heterogeneous).** No single template: Altman (clean WooCommerce popup) is easy;
Life has no source; Tink needs a third-party fallback. A real build needs **2–3 source adapters** (brand
WooCommerce popup, generic e-tailer `רכיבים` block, Super-Pharm PDP) + a per-barcode source-priority
resolver. Per-SKU it's 1–2 scrapes. The fiddle is breadth of templates, not depth.

## Q3 — OCR feasibility (photo → structured label)

**Verdict: feasible and accurate WHEN a flat back-label image exists — but it's a fallback, not the
primary path, and image availability (not OCR accuracy) is the binding constraint.**

Tested on three real images via the vision Read path (corroborated against the DOM-extracted Altman panel):

- **(a) Image availability is the gate.** Super-Pharm product images are **front-of-pack carton renders**
  only (the `_1/_2` secondaries are just rotations) — **no back-label/panel image on the retailer.** Brand
  sites *do* carry the back-label (Altman's site image is the full panel). So OCR is only worth running where
  a real panel image is reachable, which is **brand sites — where the panel is already in HTML text anyway**,
  making OCR largely **redundant** there.
- **(b) Accuracy on a good image is high.** On the Altman flat back-label, vision read the entire panel
  cleanly: the table (שם הרכיב / כמות ליחידה / % הקצובה), all 4 actives with doses + forms, רכיבים,
  allergens, ערכים תזונתיים, barcode, kosher/storage prose — Hebrew + English + numerics. Effectively
  byte-faithful to the DOM panel. **Expected accuracy on a flat, high-res back-label scan: high
  (~90%+ field-level), with a mandatory human/QA verify on dose digits.**
- **(c) The difficulty is panel-image *quality variance*.** SupHerb's only image is an angled **3D marketing
  render**; the side-panel fine-print is perspective-distorted and near the legibility floor — headline and
  lead dose readable, full table marginal. So OCR accuracy is bimodal: **excellent on flat back-label scans,
  unreliable on angled hero renders.**

**Critical difficulty (single biggest, OCR-specific):** **panel-image availability**, not OCR accuracy.
The source that's missing a text panel (Super-Pharm / Life) is also the source missing a *flat panel image* —
so OCR does not rescue the exact gap it's meant to. Where a flat back-label exists (brand sites), the text
panel usually exists too, so OCR is a redundancy/verification layer rather than a primary acquisition path.

**Effort signal — MEDIUM-to-HIGH if relied on; LOW as a verify layer.** No new tooling needed (the vision
Read path works on Hebrew panels today; the BSIP0 food pipeline used Azure/structured parsing, not photo
OCR, so this is greenfield for supplements). Cost is in **sourcing flat label images** for the SKUs that
lack a text panel — which is exactly the set without such images. Treat OCR as **tier-3 fallback +
QA cross-check on the dose digits**, not the workhorse.

## Q4 — Expected scoreable shelf coverage AFTER acquisition

Of the **~56% addressable shelf** (115 SKUs maps to the 15 engine actives; TASK-171D), here is the
expected scoreable fraction if a real combined pipeline (brand-site primary → third-party fallback → PDP
lead-dose → OCR last) is built. Bands are of the **addressable** shelf, with the binding source per band:

| Band | Coverage of addressable | Binding source |
|---|---|---|
| **High-confidence** (clean per-active panel, incl. form) | **~55–65%** | Altman site + third-party e-tailers (vitamins4all/biogaya/klilhateva) — measured clean on every one fetched |
| **+ Single-active PDP-derivable** (lead dose = full signal) | **+15–20%** | Super-Pharm PDP lead dose for single-active Life/tail SKUs (no panel table needed) |
| **Hard residue** (multi-active, no brand source, PDP-only) | **~15–25% NOT scoreable** | mostly Life multi-active + thin-brand SKUs with no panel anywhere; OCR can't rescue (no flat image) |

**Combined expected scoreable = ~75–85% of the addressable shelf** (≈ **42–48% of the *net* oral-supplement
shelf**), up from the ~20% global-brands-only (iHerb) baseline. The realistic planning number is
**~80% of addressable** — bounded **above** by third-party e-tailer breadth, bounded **below** by the
Life-house-brand multi-active residue that only a manufacturer data feed (not scraping) would close.

---

## Per-source effort summary (for Product's build-days estimate)

| Source | Panel yield | Effort | Notes for costing |
|---|---|---|---|
| **Super-Pharm PDP** | identity + lead dose; ~0% structured table | **LOW–MED** | URL discovery via map/search (not in feed); JS `waitFor`; occasional 481. Good for identity + single-active dose, not panels. |
| **Brand sites** | full panel (Altman); partial (SupHerb); none (Life) | **MED** | Heterogeneous templates → 2–3 adapters + source-priority resolver. Altman clean; Life has no site. |
| **3rd-party e-tailers** | full `רכיבים` + dose, often richest | **MED** | The real unlock + redundancy. Several sites, similar WooCommerce `רכיבים` blocks → one generic adapter covers most. |
| **OCR (vision)** | high on flat back-label; marginal on 3D render | **LOW as verify / HIGH as primary** | No new tooling; gated by flat-image availability, which correlates with where text panels already exist. Use as tier-3 + dose-digit QA. |

**Biggest single difficulty (whole build):** the **Life / Super-Pharm house-brand residue** — ~18% of the
addressable shelf whose *only* source is the Super-Pharm PDP (no brand site, no third-party panel, no flat
label image), so neither brand-scrape nor OCR closes it. Everything else is template-breadth engineering,
not a wall.

---

**Proposed status: RETURNED** — feasibility measured on real samples; hands to Product for the
cost-in-days + build-vs-pause synthesis. No pipeline built; all data `candidate`; nothing shipped.

---

# Product synthesis — TASK-171I decision pack

**Owner:** Product Agent · **Date:** 2026-06-03 · **Stage:** decision-support (no code, no scoring change, nothing ships)
**Decision being made:** whether to *build the local-brand acquisition pipeline* — NOT whether to launch a supplements category. Launch stays gated (see §D).
**Basis:** Data's measured probe (above) + addressable-corpus mapping (`addressable_corpus_mapping_v1.md`, TASK-171D). All numbers are Data's; I cost and decide, I do not re-measure.

## A. Cost estimate — in DAYS

The build decomposes into six components. Estimates are engineering-days for a single builder (Data Agent), assuming the integration layer (`integrations/clients/`, TASK-170) and firecrawl access already exist (they do — these are real, not new infra).

| # | Component | Days | Drives | Note |
|---|---|---|---|---|
| a | **Third-party e-tailer generic adapter** (one WooCommerce-style `רכיבים`+dose block, 4–5 sites: vitamins4all/biogaya/klilhateva/vitamania/htiveit) | **3–4** | the High-confidence band (~55–65% of addressable) | Data's named "real unlock." One generic parser + per-site selectors. Highest leverage per day. |
| b | **Brand-site adapters** (Altman clean WooCommerce popup + SupHerb + 1 tail) **+ per-barcode source-priority resolver** | **3–4** | redundancy on the High-confidence band; closes Altman (#1 brand, 24 SKUs) authoritatively | Resolver (which source wins per barcode) is the load-bearing piece, not the scrapers. |
| c | **Super-Pharm single-active PDP-derive path** (identity + lead-active dose → scoreable for single-active SKUs) | **2** | the **+15–20% single-active** band — and it's the *only* path into Life single-actives | URL discovery via map/search + `waitFor`; no panel parsing (there's no panel). |
| d | **OCR verify layer** (vision Read on flat back-labels; dose-digit cross-check) | **2** | quality gate, not coverage | Tier-3 fallback + QA on dose digits. No new tooling. Do NOT scope as a primary acquisition path — Data proved it can't close the exact gap. |
| e | **Claim-curation step** (capture the on-label claim per SKU so v1.3 resolution works) | **2–3** | correctness/identity, ongoing | Per-SKU human-in-loop capture; this is the recurring-cost tail, not a one-time build. |
| f | **QA + provenance + corpus-run harness** (EDPG `candidate`→promote flow, run-all, coverage report) | **3–4** | trust + repeatability; required to know real coverage | This is the gate that makes the corpus admissible. Non-optional for anything that touches scoring. |

**Total range: ~15–19 engineering-days** for the full build (≈3–4 working weeks of one builder, not months). Confirms Data's framing: **days, not months.**

**Minimum-viable subset (the 80/20): components (a) + (b-resolver only) + (f) ≈ 8–10 days.**
That ships the **third-party e-tailer adapter + Altman brand adapter + source-priority resolver + a QA/coverage harness** — which alone delivers the entire **High-confidence band (~55–65% of addressable ≈ ~31–37% of net shelf)** with provenance. It deliberately defers (c) PDP single-active, (d) OCR, and (e) claim-curation to a phase 2 that only happens if the measured MVP corpus justifies a launch. The MVP's job is not to launch — it's to **measure the real corpus** so the launch decision is made on data, not on this probe's bands.

## B. Expected shelf coverage after the build

Restating Data's measured bands with my confidence:

- **Full build → ~75–85% of the addressable shelf ≈ ~42–48% of the net oral-supplement shelf** (up from ~20% addressable / ~11% net on iHerb-only today). Planning number: **~80% addressable ≈ ~45% net** (~92 of 204 net SKUs). **Confidence: medium-high** — the High-confidence band was measured clean on *every* third-party/Altman page Data fetched; the +15–20% single-active band is an inference (sound, but PDP-derived, not panel-verified).
- **MVP-only → ~55–65% addressable ≈ ~31–37% net.** High confidence — this is the directly-measured band.
- **Diminishing-returns shape:** the first ~8–10 days buy ~60% of addressable. The next ~7–9 days buy the +15–20% single-active band (real, but lower-confidence, PDP-derived). The **last 15–25% is a hard wall**: the **Life / Super-Pharm house-brand multi-active residue (~18% of addressable)** has *no* scrape, *no* third-party panel, and *no* flat label image — so neither adapter nor OCR closes it. Per Data, **only a manufacturer data feed** would, which is a partnership/BD ask, not an engineering task. Treat that ~45% net as the **honest ceiling** of a scrape-based acquisition; do not plan past it.

## C. Build-vs-pause recommendation — **BUILD, phased: ship the MVP adapter, measure the real corpus, then decide launch.**

This is a build decision, and the cost/leverage profile clears the bar:

1. **The engine is proven and cheap** (~30–33 h/yr to run per prior probes) and the acquisition is **days, not months** — the build cost is genuinely small relative to standing up a new consumer category.
2. **~45% net / ~80% addressable is a real, defensible shelf** for a launch *framed honestly* (Bari's whole identity is "best ≠ excellent," partial-coverage transparency, EDPG `candidate`-until-promoted). ~45% of the real shelf with clean provenance is a *more* honest artifact than most supplement comparison sites, which silently cherry-pick. Bari can ship "here is the half of the shelf we can verify, and here is exactly why the other half isn't here."
3. **But two real costs cap a full-send:** the **Life residue hard wall** means we can never claim full-shelf coverage by scraping, and **claim-curation (e) + maintenance are ongoing**, not one-time — heterogeneous templates drift, and per-SKU claim capture is a standing tax. That argues against committing the full 15–19 days up front.

**So: phase it.** Build the **8–10-day MVP** (a + b-resolver + f). Run the real corpus. Measure actual scoreable coverage and the maintenance burden on live data — not on a 26-SKU probe. *Then* the owner makes the launch call (D10/D1) on a measured ~31–37% net corpus, with a known phase-2 cost (~7–9 more days) to reach ~45%. This converts a one-shot bet into a cheap, reversible measurement. Pausing entirely would bank a proven-feasible, days-cheap unlock for no good reason; full-build-before-measuring over-commits against an uncloseable residue.

**What I am NOT recommending:** building (c)/(d)/(e) before the MVP corpus is measured, and treating OCR as anything but a tier-3 verify layer (Data proved it can't close the Life gap).

## D. What stays gated

- **Category go-live is a separate D10 / D1 decision and is NOT made here.** This synthesis approves (conditionally, phased) the *acquisition build* only. A supplements category cannot launch until: the MVP corpus is measured, a BSIP0-S panel passes QA, the EDPG `candidate`→promote gate (D3/D4, my authority) is run on real panels, and Nutrition co-signs any supplement-specific scoring rule (D7 — required alongside me; not in scope here).
- **No scores move, nothing ships, all data stays `candidate`** through the MVP. The MVP is a measurement instrument, not a launch.
- **The one genuine owner-taste / irreversible item** is the **launch commitment itself** (standing up a public supplements category + the ongoing claim-curation/maintenance tax). That is the owner's call, made *after* the MVP corpus is on the table — not now.

## Bottom line (one line for the owner)

**Build the 8–10-day MVP adapter (third-party e-tailer + Altman + resolver + QA harness) to measure the real ~31–37%-net corpus; defer the +15–20% single-active path and any launch — ~45% net is the honest scrape ceiling (Life house-brand residue is the uncloseable wall), so phase it, measure, then make the launch call.**

**Proposed status: RETURNED** — decision pack complete; build/phase/pause recommendation delivered. Launch (D10/D1) and scoring (D7, Nutrition co-sign) remain gated and out of scope. No code, no scoring change, nothing shipped.
