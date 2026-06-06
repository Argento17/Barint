# DATA SIGN-OFF — run_cereals_multiretailer_001 (TASK-184)

**Agent:** data-agent
**Date:** 2026-06-05
**Run:** `run_cereals_multiretailer_001`
**Scope of this sign-off:** the 42 genuinely-new products (post-dedup vs the 66-product Shufersal
baseline `run_cereals_005`) proposed for GATE-3 live promotion.
**Owner status:** GATE-3 promotion APPROVED conditional on a clear Data + Nutrition sign-off; EV-045c ADOPTED.

**VERDICT: GO with carve-outs — 35 of 42 fit to promote; 7 held NO-GO (do not promote).**

This is a Data sign-off only. It does **not** promote anything to live and does **not** touch
`bari-web`. Promotion (frontend merge + Content authoring) proceeds only after BOTH the Data and
Nutrition sign-offs are in. No published scores and no engine were changed in this work.

---

## 1. Real-data provenance — PASS (no fabrication)

- **Identity layer:** Israeli price-transparency feeds (law-mandated catalogs). Carrefour
  self-hosted `prices.carrefour.co.il` (chain 7290055700007); Yochananof via `laibcatalog.co.il`
  (chain 7290455000004). Barcode + Hebrew name + brand only — **never** nutrition (price-feed guardrail).
- **Nutrition/ingredient layer:** Open Food Facts (OFF) **candidate** panels, paired by barcode.
  A barcode miss in OFF = "no panel", never an invented panel.
- **EDPG envelope present on all 42 records** (top-level `provenance`):
  `identity_source: il_prices:<chain>`, `identity_source_url`, `panel_source: open_food_facts`,
  `panel_found`, `panel_has_macros`, `off_completeness`, `verification_status: candidate`, `fetched_at`.
  All 42 also carry the `off_candidate_panel` risk flag. **Every panel remains `candidate`** — no
  external value has been promoted to `verified`; GATE-3 + Nutrition sign-off are the promotion gate.
- **Honest gaps recorded, not papered over:** OFF ingredient **text** was thin for these SKUs
  (`ingredients_raw_provenance.source = "missing"` on the records that had macros but no ingredient
  list). This is a real coverage limit of the free OFF endpoint, documented in the run record
  (an IP throttle mid-Yochananof batch), not a data invention.

**Conclusion:** all 42 trace to authoritative identity + a clearly-marked OFF candidate panel.
No fabricated data. ✔

## 2. Dedup correctness vs the 66 Shufersal baseline — PASS

- Dedup key = barcode (transparency-feed EAN = authoritative cross-retailer identity).
- Result (re-verified this session): **42 new unique · 16 duplicate-vs-baseline · 2 cross-retailer
  duplicate** — byte-identical to the prior run.
- Spot-checked: cross-retailer EAN matches are genuine same-product matches (same barcode, different
  chain — widens availability, not the corpus); the 42 new barcodes are absent from `run_cereals_005`.
  Split: 23 standard cereal + 19 granola/muesli.

**Conclusion:** dedup is correct; the 42-new set is genuinely new vs the baseline. ✔

## 3. EV-045 / 045b / 045c validation — PASS (and EV-045c now implemented)

### EV-045 / 045b (imported UNCHANGED, run on unseen data) — HELD
Per the run record: every contaminant-class exclusion inspected was a genuine non-cereal (bars,
breads, oat drinks, crackers/rice cakes, capsules, dairy desserts, chocolate confections, sub-floor
energy). **No false drop of a real cereal.** Curation counts re-run this session are unchanged
(Carrefour 54 IN / 163 OUT; Yochananof 6 IN / 88 OUT). The שמרים≠משמרים yeast word-boundary guard
could not be re-exercised (thin OFF ingredient panels) — flagged for the next storefront-sourced run.

### EV-045c — IMPLEMENTED this session (owner-adopted), flag-not-drop
- **Where:** `shufersal_cereals/02_build_bsip1_cereals.py` → `fitness_noncereal_flag()` (canonical),
  imported UNCHANGED by `multiretailer_cereals/02_build_bsip1_multiretailer.py` (same ruling, not a fork).
- **Rule (scoped to the Fitness/פיטנס brand line only):** flag when **(a)** a savory descriptor is in
  the name (מלח/פלפל/רוזמרין/שום/סלק/בטטה/זית/צ'ילי/כפרי/מתובל/תיבול/veggie/cracker/קרקר/thin/פרכי…)
  **OR (b)** fat ≥ 13 g/100g **AND** no sweet/granola signal (no granola/muesli/חמוצי/honey/chocolate
  token and sugars < 12 g). Reuses the EV-045b pattern + Hebrew word-boundary discipline (e.g. `מלח`
  guarded so it does not fire on `מלא`; `זית` as construct head of `זיתים`).
- **Policy:** **flag-not-drop** — attaches `cereals_governance.ev_045c_fitness_noncereal_flag` +
  a `fitness_savory_cracker_suspect` risk flag. It does NOT exclude, so it cannot change corpus
  membership (curation = contamination handling, not calibration). No score/engine change.
- **Result:** 7 SKUs flagged (6 Carrefour + 1 Yochananof); **6 are in the 42-new set**, the 7th
  (`7290118420811 Fitness Thins`) is a duplicate-vs-baseline (already in the Shufersal 66, not in 42).
- **False-positive check — PASS:** the genuine Fitness GRANOLA `פיטנס גרנולה חמוציות`
  (7613035758834, 14.8 g fat, sugars 18.7 g, granola token) is **NOT** flagged — the sweet-signal
  carve-out worked, avoiding the `חומוס גרגרים`-style false positive the owner directive warned of.
  Genuine Fitness cereals (קורנפלקס פיטנס, almond honey, Chocolate&Rice, Dark Chocolate) not flagged.
- **Net value:** 5 of the 6 in-set flags were already caught by the router as misroutes (→ default),
  but **`Fitness Thin` (7290112968807) routed to `cereal` and scored C** — i.e. without EV-045c it
  would have entered the live cereal corpus as a scored cereal. EV-045c catches it at curation,
  exactly as the run record predicted ("router luck" → explicit, auditable evidence).

### Does EV-045c change the 42-product promotion set?
**NO — the 42-set is unchanged.** EV-045c is flag-not-drop by design and adds no exclusion. Dedup
re-run confirms 42 / 16 / 2, identical to the prior run. What EV-045c changes is **which of the 42
are fit to promote as cereals** (see §5): it converts a corpus-membership question into a per-product
GO/NO-GO, removing the 6 flagged savory crackers from the promotable cereal set.

## 4. Scores — byte-identical engine, no change — PASS

- Engine: `proto_v0`, `algorithm_version 0.4.1`, `BARI_RECAL_P0=on` — byte-identical to
  `run_cereals_005` (the frozen baseline). Verified on the BSIP2 traces.
- No scoring rule was proposed, modified, or implemented in this work. EV-045c is a **curation**
  flag (no score path). Frozen invariants (milk run_005_headpin, snack 70/B, bread provenance) untouched.
- Outcome (40 of 42 scored; 2 insufficient): 1 A · 14 B · 17 C · 7 D · 1 E, median 60.2.
- **Hard Rule 7 surfaced (not a halt):** the single A — `גרנולה בתוספת חלבון` (Carrefour, 81.2/A) —
  is a new category-high above the run_005 ceiling (79.9/B), **earned on real OFF macros**
  (24.8 g protein / 15.4 g fiber / 7.2 g sugar / 46 mg sodium per 100g) by the unchanged engine, i.e.
  a better product than Shufersal stocked, not a scoring drift. **Routed to Nutrition Agent as the FYI
  to confirm in their sign-off** before it goes live as a category-topping A.

## 5. Per-set GO / NO-GO

**GO — fit to promote: 35 of 42.**
The 23 standard cereals + 19 granola/muesli, minus the 7 held below. These have a real OFF candidate
panel, scored cleanly on the byte-identical engine, deduped correctly, and carry no contamination flag.

**NO-GO — held, do NOT promote (7 products):**

| Barcode | Name | Reason | Route / grade |
|---|---|---|---|
| 7290112965660 | פיטנס מלח פלפל | EV-045c savory cracker (salt/pepper, fat 22.4g) | default / C |
| 7290118420323 | Fitness Veggie Mix | EV-045c savory cracker + insufficient_data | default / insufficient |
| 7290112968807 | Fitness Thin | EV-045c savory cracker (Thin, fat 15.8g) — *router missed it; would have scored AS cereal* | cereal / C |
| 7290115205176 | Fitness | EV-045c (fat 17.0g, no sweet signal) | default / B |
| 7290115205312 | Fitness | EV-045c (fat 17.2g, no sweet signal) | default / C |
| 7290109352916 | Fitness | EV-045c (fat 22.0g, no sweet signal) | default / C |
| 5900020034021 | Fitness | insufficient_data (no clean category signal; bare "Fitness", thin panel) | default / insufficient |

- The 6 EV-045c-flagged SKUs are savory-cracker suspects — **not breakfast cereals**, so they must
  not promote into the cereal comparison regardless of grade.
- The 2 `insufficient_data` products (one overlaps the flagged set) lack the signal to be scored as a
  cereal; promoting an insufficient panel as a graded cereal would misrepresent confidence.

## 6. Flagged products / caveats for the record
- **EV-045c savory-cracker suspects (6 in-set):** held NO-GO above. If Nestlé/Carrefour later
  publish these as a separate savory-cracker shelf, they belong to a different category, not cereals.
- **OFF ingredient-text coverage was thin** (macros present, ingredient list often missing) — does
  not block the 35 GO products (they scored on macros), but the שמרים≠משמרים yeast guard remains
  un-re-exercised; re-confirm on the next storefront-sourced run with richer panels.
- **Rami-Levy** remains BLOCKED (owner dropped the Playwright/login path) — no impact on the 42.
- **Category-code anchoring** (TASK-183 #2) is unavailable on the price-feed path (transparency XML
  has no category code); EV-045b + EV-045c are the only door-gates there. Documented, not a defect.

---

## Sign-off

**Data Agent: GO on 35 of 42 new products; 7 held NO-GO (6 EV-045c savory crackers + 1 insufficient-only).**
Provenance real (EDPG candidate), dedup correct, EV-045/045b/045c validated, scores produced by the
byte-identical engine with no score/engine change. **EV-045c did NOT change the 42-set** (flag-not-drop),
only the promotable-as-cereal subset.

**Conditions before promotion:**
1. Nutrition Agent sign-off required (per owner directive) — including confirmation of the 81.2/A
   category-high (Hard Rule 7 FYI).
2. Content authoring of insightLine/rowVerdict for the promoted products (Content Agent).
3. Promotion is the orchestrator's to execute after both sign-offs; this agent does not touch bari-web.

**Proposes:** task stays **RETURNED** pending the Nutrition sign-off + promotion.
