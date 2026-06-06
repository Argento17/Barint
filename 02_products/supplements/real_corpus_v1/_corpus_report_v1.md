# Real Corpus v1 — Thin Live Proof (global-brand Israeli supplement SKUs)

**Task:** TASK-171 thin-live-proof (completes TASK-171D's "thin live proof", owner-approved)
**Date:** 2026-06-03 · **Owner:** Data Agent · **Engine:** `03_operations/supplement_engine/proto_v0` (UNCHANGED)
**Pipeline:** TASK-171G plumbing — `il_prices` (live Super-Pharm) → `firecrawl_search`+`firecrawl_scrape` (live iHerb) → `iherb_panel._coerce` → `supplement_bridge` (barcode-first) → `supplement_label` → `score_engine`
**EDPG:** every record `verification_status=candidate` / `should_affect_score_now=false`. Nothing ships. No engine/dossier/methodology edit. Missing fields recorded, never fabricated.

---

## 0. Re-derivation (the input was NOT enumerated)

`addressable_corpus_mapping_v1.md` gives only AGGREGATE counts (23 "global-brand", 115 addressable) and does **not** enumerate SKUs, so step 0 re-derived from the **live** Super-Pharm catalog (`derive_global_brand_skus.py`).

**A correction surfaced here that matters.** The doc's "global-brand = 23" counted by the Super-Pharm **importer** field, which reads `אמברוזיה/סולגר` (Ambrosia/Solgar) for BOTH the genuine global **Solgar** line AND the **local house brand SupHerb** (`סופהרב`) — they share one Israeli distributor. The doc itself lists SupHerb as **local-only / not iHerb-gettable**. Matching the importer therefore over-counts. Re-deriving by the **product-NAME brand** (and hard-excluding SupHerb) and requiring **single-active** (excluding multivitamins / combos, which the engine doesn't score) gives the honest set for this live snapshot:

| Stage | Count |
|---|---|
| Live Super-Pharm oral-supplement SKUs (this snapshot) | 176 |
| Addressable (≥1 of the 15 engine actives) | 81 |
| **Global-brand (genuine Solgar name) AND single-active** | **4** |

All 4 are Solgar (the only global single-active brand present in this snapshot; Now/Centrum/etc. did not appear as single-active SKUs here).

---

## 1. The corpus table

| SKU (Israeli shelf) | barcode | brand | active | iHerb resolve | grade | binding constraint |
|---|---|---|---|---|---|---|
| סולגאר אומגה 950 100 כמוסות | 0033984020580 | Solgar | omega-3 (EPA/DHA) | **barcode match** /26738 | **60.5 / C** | blend_dominant (contested CV evidence) |
| סולגר אבץ פיקולינט 100 טבליות | 0033984037250 | Solgar | zinc | **barcode match** /10035 | **68.4 / B** | blend_dominant |
| סולגר ביוטין 1000 מק"ג 50 כמוסות | 0033984003101 | Solgar | biotin | no exact pack on iHerb | — | not scored (honest miss) |
| סולגר אבץ מציצה 22מ"ג 50 טבליות | 0033984010642 | Solgar | zinc | no exact pack on iHerb | — | not scored (honest miss) |

**Grade distribution (scored):** B ×1, C ×1. (No A — consistent with the contested/deferred evidence tiers that bound these actives.)

---

## 2. Measured real rates (this is the proof number)

| Stage | Rate | Read |
|---|---|---|
| iHerb URL resolved (live `firecrawl_search`, barcode-verified) | **2 / 4** | the 2 misses are real "not on iHerb US", not search failures |
| Panel extracted (live `firecrawl_scrape` json) | **2 / 4** | 100% of *resolved* URLs extracted a full panel cleanly |
| Barcode bridge matched | **2 / 4** | both resolved panels matched the SP barcode exactly (GTIN-12/13) |
| **Scored end-to-end** | **2 / 4 (50%)** | 2 lost to "exact pack not on iHerb", 0 lost to a panel/claim/form failure |

**Why the 2 misses are honest, not pipeline failures.** Both are a *catalog-mismatch*, verified by scraping the candidate barcodes rather than assumed:
- **Biotin 1000mcg/50ct (`…003101`)** — iHerb carries Solgar Biotin 1000mcg only as **100ct (`…003118`)** and **250ct (`…003125`)**, and 50ct only at **5000mcg (`…003132`)**. The exact IL pack (1000mcg × 50) is not on iHerb US. Forcing a 100ct or a 5000mcg panel would have been a fabricated bridge — refused.
- **Zinc lozenge 22mg/50 (`…010642`)** — iHerb's Solgar 22mg zinc is **Picolinate (`…037250`)** and **Chelated (`…008007`)** *tablets × 100*; there is no 50ct *lozenge*. Different form + pack, no barcode match — refused.

This is the central real-world lesson: **"ships-to-IL on iHerb" ≠ "this exact Israeli-shelf pack is on iHerb"**, even within one global brand. The barcode bridge correctly refuses the near-miss.

---

## 3. Did a missing field change a grade? (asked explicitly)

No grade was changed by a missing field on the two scored SKUs — checked counterfactually:

| SKU | live field | with field | with field=unknown | grade moved? |
|---|---|---|---|---|
| Omega 950 | form = **ethyl ester** (disclosed live) | form_sub 72 → score 60.5 | form_sub 50 → score 56.1 | **No** — C either way (contested CV evidence is the ceiling) |
| Zinc Picolinate | form = **picolinate** (disclosed live) | form_sub 92 → score 68.4 | form_sub 50 → score 69.1 | **No** — B either way |

Notable real result worth flagging: the **live Omega panel disclosed the chemical form (ethyl ester)** — a field the earlier TASK-171D PoC omega SKU had as `null`. So the live corpus *improved* panel completeness over the PoC fixture, while the engine correctly held the grade at C on evidence, not form.

---

## 4. Notable results (real, with binding constraints)

- **Solgar Omega 950 → 60.5 / C.** A strong-dose (882 mg combined EPA+DHA/day), honest, ethyl-ester product capped at C because its on-label "Heart Healthy" claim maps to the dossier's **CONTESTED / deferred CV endpoint** (evidence sub-score 17). The engine rewards the dose/form but refuses to let a contested cardiovascular claim earn a B/A. This is the engine behaving exactly as designed on a real, common retail SKU.
- **Solgar Zinc Picolinate → 68.4 / B.** Preferred form (picolinate), disclosed 22 mg, immune claim resolving to a real tier; bound by the blend, no cap fired. The single highest real grade in this thin corpus.

---

## 5. Honest read — is this a credible live proof?

**Yes for the pipeline; no for the corpus breadth.** The run is a genuine end-to-end LIVE exercise of every stage — live Super-Pharm catalog → live `firecrawl_search` URL resolution → live `firecrawl_scrape` panel → barcode-verified bridge → BSIP0-S label (with the real on-label claim) → real 15-active engine, producing real scores + binding constraints + full traces. **No firecrawl call was denied**; the 2 unscored SKUs are honest catalog misses the bridge correctly refused, not failures. But the **breadth is thin (4 derived, 2 scored)** — the doc's "~23" was an importer-field over-count, and the iHerb-US ↔ Israeli-pack mismatch halves even that. The real bottleneck remains the **local-brand panel gap** (SupHerb/Altman/Life dominate the shelf and are not on iHerb), exactly as TASK-171D concluded. This proof validates the *machinery* on real Israeli SKUs; it does not (and was not meant to) widen the scorable corpus.

---

## 6. Files

- `derive_global_brand_skus.py` → `global_brand_skus.json` (step-0 live derivation)
- `run_real_corpus_v1.py` → per-SKU JSON (`REAL-IL-*.json`) + `_index.json` (with `measured_rates`)
- `REAL-IL-OMEGA3-SOLGAR-0033984020580.json`, `REAL-IL-ZINC-SOLGAR-0033984037250.json` — scored (label + engine_output + trace + provenance)
- `REAL-IL-BIOTIN-SOLGAR-0033984003101.json`, `REAL-IL-ZINC-SOLGAR-0033984010642.json` — honest misses (panel=null, bridge unmatched, no fabrication)
