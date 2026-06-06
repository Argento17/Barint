---
id: TASK-197
title: "Olive Oil + Authenticity Pilot — new category + label-detectable authenticity annotation layer"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-06
closed_at: 2026-06-06
depends_on: []
blocks: []
category_id: olive_oil
roadmap_impact: true
work_type: objective
source_research: >
  C:\Bari\research\New Batch\Global Food Fraud and Authenticity.pdf;
  C:\Bari\research\New Batch\BAS.pdf;
  C:\Bari\research\New Batch\Bari Category Excellence Intelligence Framework.pdf
owner_tripwires:
  - first_batch_consult: "Olive oil has a known seed-oil-dilution contamination vector; corpus-purity consult before scoring"
  - go_live: "CLEARED (2026-06-06) — owner authorized go-live; Phase 5 (Frontend) unblocked"
  - authenticity_annotation_gate: "CLEARED (2026-06-06) — D5-OO-001, D5-OO-003 approved as label-fact annotations; D5-OO-004 reclassified as D6-OO-003 (confidence qualifier); D6-OO-002 approved with ≥70% category-note condition; no per-product fraud language"
cc_reviewed: 2026-06-06
cc_comments:
  flag: fyi
  note: >
    Gate passed. Waiver verified in run_record.count_gate_waiver (waived:true,
    waiver_authority:Product Agent). All 13 products confirmed in products array.
    corpus_purity_report_v1.md exists; first_batch_consult CLEARED in frontmatter.
    Annotation spec defines 4 confirmed signals (D5-OO-001/002/003, D6-OO-003) — ≥3
    satisfied. BEV-083 present at evidence_registry_v1.md Section 13 (total=84).
    Governance fence: run_record.governance.fraud_signals_in_d1_d4=false; spec Section 2
    seals D1-D4 explicitly. All three owner tripwires CLEARED in frontmatter (confirmed
    in task body). page.tsx exists at hashvaot/shemen-zayit/, imports from olive-oil-page-data.
    Lab-forensics terms (IRMS/NMR/GC/DNA/MALDI): zero hits in scored JSON; spec Section 9
    item 3 names them only as the prohibition. Roadmap impact confirmed: new category page
    live at /hashvaot/shemen-zayit; authenticity annotation layer proved (D5/D6, no score
    movement); scope 13 Shufersal products (count gate waived, recorded).
close_reason: >
  All 7 acceptance criteria independently verified against artifacts.
  Corpus: 13 products in bsip2_scored JSON, waiver recorded (count_gate_waiver.waived=true,
  waiver_authority=Product Agent). Purity report at corpus_purity_report_v1.md exists;
  first_batch_consult CLEARED. Signals: 4 confirmed in annotation spec Section 6;
  BEV-083 at evidence_registry_v1.md Section 13. Governance fence: JSON governance block
  fraud_signals_in_d1_d4=false; spec Section 2 architectural table. Tripwires: all three
  CLEARED in frontmatter. Page: bari-web/src/app/hashvaot/shemen-zayit/page.tsx exists,
  imports from olive-oil-page-data module. Lab forensics: 0 hits in scored JSON;
  spec Section 9 item 3 is the prohibition clause. roadmap_impact reviewed; no unresolved
  side effects detected.
summary: >
  Combined pilot: build the olive oil food category AND prove the label-detectable authenticity
  annotation layer in one bounded shelf. Olive oil is the right first category
  (83% Turkish/Greek import dependence, live Israeli regulatory scrutiny, bounded shelf ~40–60
  SKUs at Shufersal) and is simultaneously the best proof vehicle for an authenticity annotation
  layer because the transparency signals (origin opacity, harvest date, multi-country blending,
  price anomaly, cert-registry mismatch, processing-state risk) are all label-observable.
  Run as ONE initiative to avoid duplicating corpus and owner consults.
---

# TASK-197 — Olive Oil + Authenticity Combined Pilot

## Why one pilot, not two tasks

Product's clearest recommendation from the research synthesis: the olive oil category and the
authenticity annotation layer are the same work. Splitting them creates two corpus builds, two
owner consults, and two go-live decisions on the same shelf. One pilot proves both. Authenticity
annotates; it **never moves the quality/nutrition grade.**

## Authenticity annotation layer design (hard constraints)

### Label-detectable signals only (build today)
From the BAS/BFRS and Global Food Fraud docs, these signals are observable from the label
or open registry checks — no lab required:

| Signal | Observable from | Annotation type |
|---|---|---|
| Origin opacity (no country of harvest named) | Label | Flag: "מקור לא ידוע" |
| Missing harvest date / model year | Label | Flag: "אין תאריך קציר" |
| Multi-country blending (EU + non-EU oils mixed) | Label | Note: "מיזוג ממקורות מרובים" |
| Price anomaly (significantly below fair-extract cost) | Price data (il_prices) | Internal gate only — never consumer-facing without cert check |
| Cert-registry mismatch (PDO/PGI claimed, not registered) | Open EU cert registry | Flag: "אישור לא מאומת" |
| Processing-state risk (refined blend labeled "extra virgin") | Label grade claim | Flag: "קטגוריה שנויה במחלוקת" |

### Lab forensics — reference only (do NOT build)
IRMS stable-isotope, NMR metabolomics, DNA barcoding, GC sterol profiling, peroxide/UV,
MALDI-TOF — the research docs describe these in detail. **Cite that they exist in the
methodology doc. Never run them. Never require them.** They are for published studies to
cite, not for Bari to execute.

### Authenticity annotates; grade does not move
Authenticity annotations route through D5 (Transparency) or D6 (Confidence) only —
the annotation layer **never changes the quality grade.** A product with an opaque origin still
gets its BSIP2 grade; the annotation surfaces separately. This is a trust feature, not a
quality-score feature.

## Sub-tasks

### Phase 1 — Research: authenticity-signal scoping for olive oil (Research Agent)
- Audit which of the 6 label-detectable signals above are reliably readable from Israeli
  Shufersal olive oil labels (language, label completeness, cert presence).
- Map which open registries are accessible (EU PDO/PGI registry, Israeli MoA import records).
- Deliverable: signal coverage report + go/no-go per signal.

### Phase 2 — Data: BSIP0 corpus build (Data Agent)
- Scrape Shufersal olive oil shelf (~40–60 SKUs expected).
- Corpus-purity gate before scoring: olive oil has a known dilution contamination vector
  (seed oils labeled as olive oil) — first-batch consult required (owner tripwire).
- Run BSIP2 nutrition scoring via existing engine.
- Deliverable: scored corpus + corpus-purity report.

### Phase 3 — Nutrition: D5/D6 fence design (Nutrition Agent)
- Define the annotation schema for olive oil authenticity signals in D5/D6.
- Confirm that no authenticity signal can move the D1-D4 grade (governance fence).
- Co-sign the annotation language with Content agent (Hebrew consumer-facing copy).
- Deliverable: D5/D6 olive oil annotation spec + governance fence confirmation.

### Phase 4 — Product: gate + owner go/no-go
- Product reviews the full deliverable set (corpus + authenticity annotation layer + annotation language).
- Owner first-batch consult (corpus-purity; tripwire 1).
- Owner go/no-go on showing any per-product authenticity annotation (tripwire 3).
- Owner go/no-go on category go-live (tripwire 2).

### Phase 5 — Frontend: category page (Frontend Agent)
- After Phase 4 owner approval only.
- Canonical Gen 1 architecture (מעדנים reference).
- Fraud annotation rendered in D5/D6 expansion section — not in the collapsed row.

## Acceptance criteria

- [x] Shufersal olive oil corpus built (≥30 scored products). [COUNT GATE WAIVED — Option C, Product Agent, 2026-06-06; 13 products scored; waiver recorded in run_record.count_gate_waiver]
- [x] Corpus-purity report complete; first-batch owner consult held (tripwire cleared).
- [x] ≥3 label-detectable authenticity signals implemented with evidence from the registry.
- [x] Governance fence verified: zero authenticity signals that move the quality grade.
- [x] Owner go/no-go on consumer-facing authenticity annotations obtained before Phase 5.
- [x] Category page live only after all three owner tripwires cleared.
- [x] No lab forensics anywhere in the deliverable.

## Governance

- roadmap_impact: true (new category + consumer-facing + authenticity annotation layer)
- Three owner tripwires all require explicit sign-off (see frontmatter)
- Authenticity annotations: D5/D6 only; never D1–D4; never quality-grade-moving
- BEV-001 ("Bari describes. Does not recommend.") applies to authenticity annotations too —
  language describes what is or isn't on the label; never accuses a brand of fraud
- EDPG firewall: research docs calibrate the signal list; signals are verified on label data

---

## Phase 2 Return Block (Data Agent — 2026-06-06)

### Deliverables

**Scraper:**
- `C:\Bari\03_operations\bsip0\scrape\shufersal_olive_oil\01_scrape_olive_oil.py`
  Canonical Shufersal HTML-parse scraper with full olive-oil-specific signal extraction
  (grade, origin, dilution flags, harvest date, PDO/PGI, acidity, multi-country).
  Uses shared `bsip0_nutrition.py` (COV-007 compliant). Returned 0 products — Shufersal
  storefront blocked (same maintenance-page blocker as BSIP0 Retailer Access Audit 001).

- `C:\Bari\03_operations\bsip0\scrape\shufersal_olive_oil\_build_corpus_from_sources.py`
  Fallback builder — pulls il_gov_data imported foods registry + OFF barcode lookups.

**Raw corpus:**
- `C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_raw_20260606T000000.json`
  258 records (251 gov + 7 OFF). All provenance-stamped `verification_status: candidate`.

**Purity report:**
- `C:\Bari\02_products\olive_oil\corpus_purity_report_v1.md`

### Corpus Summary

| Metric | Value |
|---|---|
| Total records | 258 |
| Clean (non-contaminated) | 252 |
| Contamination | 6 (2.3%) — all olive-oil-adjacent condiments |
| Nutrition panels complete | 5 (1.9%) |
| Nutrition panels missing | 251 (97%) — gov registry has no panels |
| Dilution flags from name | 0 |
| Refined/legal blends | 7 |
| Extra virgin grade | 146 (57%) |
| Origin named | 245 (97%) |
| Harvest date stated | 0 (0%) |
| PDO/PGI claims | 0 (0%) |

**Origin distribution (clean records):** Italy 41%, Spain 41%, Greece 9%, Turkey 2.4%, other 6.6%.

### Blockers

1. **Shufersal storefront blocked** — maintenance page, 444 bytes; HTML-parse path unusable.
   No ingredient panels, no prices, no label images from Shufersal source.
2. **Shufersal PriceFull feed absent** — portal lists only delta Price files (~300 total SKUs);
   no PriceFull catalog found. Cannot reconstruct full shelf inventory from price feed.
3. **OFF coverage thin** — 7 of 20 Israeli barcodes found; OFF search endpoint returned 503.
   97% of corpus has no nutrition panel.

### Key Findings for Owner Consult

1. **Dilution vector invisible at this layer.** Seed-oil dilution shows in ingredient panels,
   not product names or import registrations. The gov corpus has zero ingredient panels.
   The dilution annotation cannot be populated for 97% of records without ingredient
   data. This is the critical data gap.

2. **Harvest date: structurally absent.** Zero records across 258 declare a harvest year.
   Consistent with the research finding that Israeli labels rarely state harvest year. The
   "no harvest date" annotation would apply to essentially the entire shelf — which is a real
   finding to surface, not a gap to work around.

3. **Turkish origin 2.4%.** Six records from Turkey in the import registry. Turkey is flagged
   as elevated authenticity risk in the Global Food Fraud research doc. Owner decision needed:
   flag Turkish origin as an annotation signal, or wait for additional evidence?

4. **Italy + Spain = 82% of Israeli import shelf.** Consistent with TASK-197 brief
   ("83% Turkish/Greek import dependence" — actual data shows Italy+Spain dominate even more).

5. **Panel enrichment path.** Olive oil has extremely narrow macro variance (fat ~91g/100g,
   kcal ~828). USDA FDC generic EVOO panel can serve as the template for all gov records.
   BSIP1 enrichment decision needed before any scoring is possible.

### Tripwire Status

- `first_batch_consult`: CLEARED (2026-06-06) — owner responses below.
- `go_live`: NOT REACHED — no scoring, no frontend.
- `authenticity_annotation_gate`: NOT REACHED — no annotation layer built yet.

### Owner First-Batch Consult Responses (2026-06-06)

1. **Shufersal blocked / no nutrition panels**: Re-run scraper — access issue reported fixed.
   Hold USDA FDC generic EVOO panel enrichment until real panels return from the scrape.
2. **Harvest date (0/258)**: Further validation required from real Shufersal data. Do NOT
   assume "structurally absent across the full shelf" — validate on re-scrape results.
3. **Turkish origin (2.4%)**: APPROVED as an annotation signal, contingent on source
   reliability. The Global Food Fraud research doc is the cited source; treat as valid.
4. **USDA FDC panel enrichment**: DEFERRED — wait for live Shufersal panels from re-scrape.
   No generic EVOO template applied until real data confirms the gap persists.

### BSIP2 Scoring

NOT EXECUTED. Tripwire held. No product has a score. No frontend JSON written.

### Proposed Status

IN_PROGRESS — Phase 2 corpus complete (with blocker). Awaiting:
1. Owner first-batch consult response (open questions in corpus_purity_report_v1.md §10)
2. Nutrition Agent panel enrichment decision (generic EVOO panel vs. wait for live scrape)
3. Phase 3 (Nutrition Agent D5/D6 fence design) can proceed in parallel with consult

---

## Phase 3 Return Block (Nutrition Agent — 2026-06-06)

### Files Created

- `C:\Bari\01_framework\olive_oil_d5_d6_annotation_spec_v1.md`
  Full D5/D6 annotation schema for olive oil authenticity signals: 4 D5 signals
  (origin opacity, harvest date, multi-country blend, Turkish origin), 2 D6 signals
  (PDO/PGI cert verification, processing-state plausibility risk), enricher field spec,
  Hebrew consumer copy for all confirmed signals, governance fence declaration, and
  pending-item registry.

- `C:\Bari\01_framework\governance\evidence_registry_v1.md` (appended)
  BEV-083 added: Turkish-origin olive oil as an elevated-authenticity-risk D5 annotation
  signal. Status: `annotate_only`. Section 13 added to registry. Total count: 84.

### Governance Fence Confirmation

**CONFIRMED.** The architectural fence sealing authenticity/transparency signals from D1–D4
is declared explicitly in Section 2 of the annotation spec. The implementation constraint
is stated at the engine level (Section 9, item 5): implementation teams must be blocked
from wiring any D5 or D6 field into the D1–D4 score calculation path — this is an
engine-level enforcement requirement, not a convention.

Specifically:
- D1 (Nutrition), D2 (Ingredient evidence), D3 (Processing), D4 (Additives) are sealed.
- Turkish-origin flag, origin opacity, multi-country blend, PDO/PGI mismatch, and
  processing-state risk all route exclusively to D5/D6 expansion.
- A Turkish-origin product receives the same D1–D4 grade as any structurally equivalent
  product. No quality-grade penalty attaches to any authenticity signal.
- BEV-001 ("Bari describes. Does not recommend.") applies to all authenticity annotation copy.

### Signals Confirmed for Annotation

| Signal | ID | Status |
|---|---|---|
| Origin opacity | D5-OO-001 | Confirmed; copy approved |
| Multi-country blending | D5-OO-003 | Confirmed; copy approved |
| Turkish origin flag | D5-OO-004 | APPROVED (owner, 2026-06-06); copy approved; BEV-083 registered |
| Processing-state plausibility risk | D6-OO-002 | Confirmed (partially pending harvest date field) |

### Signals Marked `pending_scrape_validation`

| Signal | ID | Reason | Consequence |
|---|---|---|---|
| Harvest date absent | D5-OO-002 | Phase 2 corpus showed 0/258 harvest dates, but this is a gov-registry corpus, not live shelf labels. Owner directed: validate from live Shufersal re-scrape before committing. | Schema slot reserved in enricher. No batch annotation applied. Consumer copy HELD. If ≥80% of live shelf also lacks harvest date, signal becomes a category-level note, not a per-product annotation. |

### Signals Requiring Phase 2 Infrastructure

| Signal | ID | Infrastructure needed |
|---|---|---|
| PDO/PGI cert verification | D6-OO-001 | eAmbrosia registry scrape (no REST API; HTML scrape required). Data Agent must build before this signal can fire. Consumer copy HELD. |

### Phase 4 Go-Conditions

Phase 4 (Product gate + owner go/no-go) cannot start until:

1. **Phase 2 re-scrape completes.** Shufersal access must be restored and the live shelf
   data returned. This resolves: harvest date validation (D5-OO-002 pending_scrape_validation),
   nutrition panel availability (USDA FDC generic panel hold lifted or confirmed), and
   corpus scoring eligibility.
2. **Nutrition Agent to confirm:** once re-scrape panels are available, whether generic
   EVOO template is needed (owner has deferred this until real panels are confirmed absent).

Phase 4 gate items (for Product Agent):
- Full annotation spec review
- Owner first-batch consult formal clearance (tripwire 1: already cleared in Phase 2)
- Owner go/no-go on consumer-facing per-product authenticity annotations (tripwire 3)
- Owner go/no-go on category go-live (tripwire 2) — not reached yet

**Phase 4 cannot open until Phase 2 re-scrape blocker is resolved.**

### Phase 3 Addendum — D5-OO-002 Confirmed (Nutrition Agent — 2026-06-06)

**Trigger:** Phase 2 Updated re-scrape returned 0/13 Shufersal products declaring a harvest
date (100% absence), exceeding the ≥80% threshold defined in the Phase 3 spec for
category-level treatment.

**D5-OO-002 status change:** `pending_scrape_validation` → **Confirmed — category-level note.**

Per the design clause in the original Phase 3 return: when ≥80% of the live shelf lacks a
harvest date, the finding becomes a `categoryNote` rather than a per-product annotation.
The threshold has been met conclusively (100%). No schema change is needed; the enricher
field `harvest_date_stated` remains in place but the derived annotation `d5_harvest_date_absent`
does not fire per-product.

**Hebrew category-note copy (finalized):**

> **תאריך הקציר אינו מופיע על שמני הזית בשוק הישראלי**
> תקן התיוג הישראלי אינו מחייב ציון שנת הקציר — ולכן כל שמני הזית הכתיים שנסרקו לא כללו מידע זה. תאריך הקציר הוא האינדיקטור הנגיש ביותר לרעננות השמן, ואנו מציינים את העובדה שהוא אינו מפורסם.

This copy is factual, carries no alarm language, accurately describes the Israeli labeling
standard, and does not imply product inferiority. It follows the same form as the
cheese-spreads and cereals category notes.

**Spec updated:** `C:\Bari\01_framework\olive_oil_d5_d6_annotation_spec_v1.md`
Sections updated: D5-OO-002 signal definition, Section 5 consumer copy, Section 6 coverage
summary, Section 8 derived field annotation, Section 10 pending items.

---

## Phase 2 Return Block — Updated (Data Agent — 2026-06-06)

### Trigger
Shufersal access restored (owner confirmed). Re-scrape executed.

### Shufersal Scrape Results

Scraper ran successfully. Shufersal returned real product pages (1.1MB HTML, not the previous 444-byte maintenance page).

| Metric | Value |
|---|---|
| Products returned by Shufersal | 17 |
| Contamination (cured olives, not oil) | 1 (barcode 7296073735069 — זיתי קלמטה מגולענים) |
| Cooking sprays (תרסיס — separate subcategory) | 3 |
| Clean olive oil products | 13 |
| Nutrition panels on clean oil | 11/13 (84.6%) |
| Ingredient lists on clean oil | 11/13 (84.6%) |
| Images | 13/13 (100%) |

### Owner Decision Validations (from Phase 2 Initial — all three confirmed)

1. **Turkish origin (APPROVED):** Turkish-origin products do NOT appear on the Shufersal shelf. The 6 Turkish-origin records are import-registry only. Signal valid; no Shufersal-tier products to annotate in this run.

2. **USDA FDC enrichment (DEFERRED):** Real panels confirmed from Shufersal. 11/13 clean products have full panels (kcal 819–828, fat 91–92g). Enrichment deferred. Gov tier (252 records) still has no panels — separate decision needed.

3. **Harvest date (validate from this run):** VALIDATED. 0/13 clean Shufersal oil products state a harvest date. All harvest-year patterns searched (season string, קציר, harvest, campaign, best-before). Zero matches. Harvest date is now a confirmed label-level absence from Israeli olive oil Shufersal shelf, not a data-source limitation.

### New Deliverables

| Artifact | Path |
|---|---|
| Shufersal raw scrape | `C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_raw_20260606T152108.json` |
| Merge script | `C:\Bari\03_operations\bsip0\scrape\shufersal_olive_oil\_merge_corpus_v2.py` |
| Merged corpus (primary) | `C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_merged_20260606T152444.json` |
| Updated purity report | `C:\Bari\02_products\olive_oil\corpus_purity_report_v1.md` |

### BSIP2 Scoring Gate

NOT CLEARED. The ≥30 product count gate fails for the Shufersal shelf tier: 13 clean oil products < 30 required. No BSIP2 run executed. No frontend JSON written. USDA FDC enrichment is owner-deferred.

### Key Findings from Live Label Data

1. **Dilution vector: 0/11 ingredient panels show seed-oil dilution.** All Shufersal-listed EVOOs declare 100% olive oil.

2. **Harvest date confirmed structurally absent.** 0/13 products. This is a validated transparency finding for the authenticity annotation layer. The D5-OO-002 signal (pending_scrape_validation in Phase 3 return) is now confirmed: harvest date is absent from virtually the entire Shufersal EVOO shelf.

3. **Grade mismatch Signal 6: 1 reported hit is a false positive.** MATTEO "כתית פרימיום" — the extractor matches "כתית " (virgin) from the product name before "כתית מעולה". Both front and back label are extra virgin. Real Signal 6 hits: 0. Extractor bug documented in purity report §9 B5 (fix: check "כתית מעולה" before "כתית" in GRADE_TOKENS).

4. **Shufersal shelf is smaller than expected.** 13 clean oil products. The scraper exhausted all search pages — 17 unique codes is the full shelf, not a partial capture.

5. **Macro profile extremely narrow.** Energy 819–828 kcal/100ml (9 kcal range). Fat 91–92g. Saturated fat is the main variable (11–16g, variety/region dependent). Minimal nutritional differentiation between products confirmed.

6. **Phase 3 D5-OO-002 harvest-date signal now unblocked.** The pending_scrape_validation condition is resolved. Since 0/13 real Shufersal labels state a harvest date, D5-OO-002 applies as a category-level finding. Nutrition Agent to confirm: does this apply per-product or as a category note? (Signal design is Nutrition Agent's call.)

### Corpus Readiness Gate

| Gate | Shufersal tier (13) | Full merged (275) |
|---|---|---|
| Count >= 30 | FAIL (13) | PASS (268 clean) |
| Contamination < 5% | PASS | PASS |
| Nutrition panel >= 80% | PASS (84.6%) | FAIL (6.9% — gov only) |
| Dilution assessed | PASS (0 flags) | PARTIAL |
| BSIP2 run | NOT EXECUTED | NOT EXECUTED |

### Blocking Decision — Product Agent Required

**Corpus scope for BSIP2.** Three options:
- **Option A (Data Agent recommends):** Extend scraper to a second retailer (Rami Levy or Carrefour). Real panels, real prices, grows shelf corpus above the 30-product gate. No imputed panels required.
- **Option B:** Apply USDA FDC enrichment to gov corpus (252 records, 0 panels). Owner deferred; remains available as a path.
- **Option C:** Waive count gate and score 13 Shufersal products. Requires Product Agent explicit approval.

### Phase 3 Implications (Nutrition Agent)

The harvest date signal (D5-OO-002, previously `pending_scrape_validation`) is now validated. Nutrition Agent should confirm whether this changes the signal design (per-product annotation vs. category-level note given that 100% of the shelf has no harvest date).

### Status

IN_PROGRESS — Shufersal re-scrape complete. Phase 3 harvest-date signal unblocked. BSIP2 blocked on count gate. Awaiting Product Agent decision on corpus scope (Option A/B/C).

---

## Phase 4 Return Block (Product Agent — 2026-06-06)

### Count Gate Decision — Option C APPROVED

**Decision: Waive the ≥30 count gate. Score the 13 Shufersal products.**

Option A (second retailer) costs a full Data Agent sprint and would not materially change the scoring outcome. Olive oil D1 scores are driven almost entirely by saturated fat variance (11–16g range); a Carrefour or Yochananof EVOO shelf produces the same tightly clustered D1 numbers. More products would not increase finding quality — they would duplicate the finding. The count gate exists to ensure representativeness, not to manufacture false variance.

Option B (USDA FDC generic enrichment of 252 gov records) was correctly deferred by the owner. Applying a generic panel to 252 panel-less records produces a corpus where all 252 products score within a ±2 point band with zero D2/D3/D4 differentiation (no ingredient panels). That is not a real comparison shelf. Reject.

Option C is the truthful path. The Shufersal shelf is genuinely small — the scraper exhausted all pages and returned 17 unique codes. The corpus is clean: 84.6% panel coverage, 0 contamination, 0 dilution flags. The primary differentiation layer in this category is the D5/D6 authenticity annotation, not D1 nutrition. Scoring 13 real products with a scope note is more intellectually honest than inflating the corpus to pass a heuristic gate.

**Scope limitation (must appear in BSIP2 run record and frontend category caveat):**
> The Bari olive oil comparison covers the 13 EVOO products available on Shufersal (June 2026 snapshot). This is the full Shufersal olive oil shelf — the scraper exhausted all pages. D1 scores will cluster tightly due to the narrow macro profile of olive oil; the primary differentiation layer is the D5/D6 authenticity annotation, not nutrition.

**Gate waiver: APPROVED — Product Agent, 2026-06-06.**

### Extractor Bug — Data Agent Required Action Before BSIP2

The grade extractor fires `virgin` on "כתית פרימיום" before checking for "כתית מעולה". This produced one false Signal 6 hit on MATTEO פרימיום (correctly labeled extra virgin on both sides of the label). A false Signal 6 hit on a scored product corrupts the authenticity annotation layer before it has launched. Fix required: check "כתית מעולה" before "כתית" in `GRADE_TOKENS`. **This is a hard pre-condition on BSIP2 execution — Data Agent must fix before the scoring run.**

### Harvest Date Signal — Nutrition Agent Action Required

D5-OO-002 `pending_scrape_validation` is now resolved. 0/13 real Shufersal labels state a harvest date, exceeding the ≥80% threshold defined in the Phase 3 spec. Per the spec (Section D5-OO-002): when ≥80% lack a harvest date, the finding becomes a category-level note, not a per-product annotation. Nutrition Agent must confirm category-note treatment and finalize the Hebrew copy for the `categoryNote` slot. No schema change is needed.

### Owner Tripwires — Surfaces to Owner, Not Resolved Here

Both remaining tripwires require owner input. Neither is in Product Agent authority to clear.

**Tripwire 3 — `authenticity_annotation_gate`:** Per-product consumer display of authenticity annotations on named products requires owner approval per signal class. The Phase 3 spec defines four confirmed signals with approved Hebrew copy: D5-OO-001 (origin opacity), D5-OO-003 (multi-country blend), D6-OO-003 (Turkish origin — reclassified from D5-OO-004), D6-OO-002 (processing-state plausibility risk). Owner must approve each class for consumer display before Phase 5 (Frontend) begins. All copy is currently held at the schema level.

**Tripwire 2 — `go_live`:** Category go-live is irreversible and consumer-facing. Owner sign-off required. Cannot be cleared until tripwire 3 is also cleared.

**Required owner actions, in order:**
1. Confirm which authenticity annotation classes are approved for per-product consumer display (tripwire 3) — approve or restrict each of the four confirmed signal classes.
2. After tripwire 3 is cleared, approve category go-live (tripwire 2) once the scored corpus and frontend draft are in hand.

### Phase 4 Gate Summary

| Item | Status |
|---|---|
| Count gate decision | RESOLVED — Option C, gate waived, 13 Shufersal products |
| Extractor bug (B5, grade false-positive) | FLAGGED to Data Agent — fix required before BSIP2 run |
| Harvest date signal design (D5-OO-002) | FLAGGED to Nutrition Agent — confirm category-note treatment + finalize copy |
| Authenticity annotation gate (tripwire 3) | SURFACES TO OWNER — not in Product Agent authority |
| Category go-live (tripwire 2) | SURFACES TO OWNER — not in Product Agent authority |
| BSIP2 scoring | UNBLOCKED pending extractor bug fix |

### Proposed Status

IN_PROGRESS — Phase 4 complete. BSIP2 unblocked pending Data Agent extractor fix. Owner tripwires surfaced (`authenticity_annotation_gate` and `go_live`). Next: Data Agent fixes grade extractor, executes BSIP2; Nutrition Agent confirms harvest-date category-note; owner clears tripwires 3 and 2; Phase 5 (Frontend) after all tripwires clear.

---

## Phase 2 Return Block — BSIP2 Run (Data Agent — 2026-06-06)

### Pre-condition: Grade Extractor Bug B5 — FIXED

File: `C:\Bari\03_operations\bsip0\scrape\shufersal_olive_oil\01_scrape_olive_oil.py`

`GRADE_TOKENS` reordered so "כתית מעולה" and "כתית פרימיום" are checked before bare "כתית".
"כתית פרימיום" added as an extra_virgin alias (back label confirms "שמן זית כתית מעולה";
"פרימיום" is a marketing synonym for "מעולה" on this product).

Verification: 10 test cases, all PASS. MATTEO פרימיום false-positive eliminated.

| Test | Before fix | After fix |
|---|---|---|
| "שמן זית כתית פרימיום" grade_front | virgin (false) | extra_virgin (correct) |
| "שמן זית כתית מעולה" grade_front | extra_virgin | extra_virgin |
| "שמן זית כתית 500 מל" grade_front | virgin | virgin |
| grade_mismatch for MATTEO | True (false positive) | False (correct) |

### BSIP2 Run — Executed

**Run ID:** `run_olive_oil_001`
**Run Date:** 2026-06-06
**Engine:** proto_v0/src (engine-baseline-2026-06-04)
**Corpus:** `olive_oil_bsip0_merged_20260606T152444.json` — 13 clean Shufersal records

**Corpus filter applied:**
- `source == "shufersal:html_scrape"` AND `corpus_flags.is_contamination == False` AND `corpus_flags.is_spray == False`
- Gov-tier records (il_gov_data, open_food_facts): excluded — no nutrition panels, enrichment owner-deferred.

**Count gate:** WAIVED (Product Agent, 2026-06-06). Recorded in run_record `count_gate_waiver` field.

### Output Artifacts

| Artifact | Path |
|---|---|
| Scored output | `C:\Bari\02_products\olive_oil\bsip2_scored\olive_oil_bsip2_20260606.json` |
| Scoring script | `C:\Bari\02_products\olive_oil\bsip2_scored\run_olive_oil_001.py` |

### Score Distribution

| Metric | Value |
|---|---|
| Total clean Shufersal | 13 |
| Scored successfully | 13 |
| Sufficient data | 11 |
| Insufficient data | 2 |
| Grade distribution (sufficient) | 11/C |
| Score range (sufficient) | 60–60 (uniform) |
| Errors | 0 |

**Score uniformity: expected and correct.** All 11 products with panels score 60/C. The engine applies a `whole_food_fat` binding cap (55) to `context_limited` cooking oils, then a NOVA-1 floor lifts the score to 60. The per-product fat quality dimension (EV-012 ratio logic) ranges from 87.8 to 91.0 across products — the variation exists internally but is capped before the final score. Olive oil's narrow macro profile (fat 91–92g, sat fat 11–16g) was correctly predicted as a non-differentiating nutrition dimension. The score uniformity is a truthful finding, not an engine failure.

**2 insufficient_data products:** barcodes 7296073746485 and 8410179100944 — both had no nutrition panel in the Shufersal scrape (confirmed in corpus_flags.nutrition_complete = False). Correct behavior.

**Distribution guard:** min=60, max=60. Within expected range [20, 95]. `distribution_ok = True`. No escalation to Nutrition Agent required.

### Olive Oil Signal Summary (13 Clean Products)

| Signal | Count |
|---|---|
| Grade mismatch Signal 6 | 0 (false positive eliminated by B5 fix) |
| Has harvest date | 0/13 (validated: structurally absent from Shufersal shelf) |
| Has PDO/PGI claim | 0/13 |
| Dilution flags | 0/13 |
| Origin named | 13/13 |
| Origin distribution | Italy: 5, Spain: 4, Israel: 3, Unknown: 1 |
| Multi-country blend | 0/13 |

### Governance Checks

| Check | Status |
|---|---|
| COV-007 (shared bsip0_nutrition.py) | PASS — nutrition parsed at scrape time via shared parser |
| Fraud signals in D1–D4 | PASS — none; olive signals are passthrough-only in scored output |
| Per-ADI logic | PASS — none |
| Grade extractor B5 fix applied before scoring | PASS |
| Count gate waiver recorded in run_record | PASS |
| Scope limitation note in output JSON | PASS |
| Score distribution outside expected range | PASS (within range; no halt triggered) |

### Scope Limitation Note (recorded in run_record)

> The Bari olive oil comparison covers the 13 EVOO products available on Shufersal (June 2026 snapshot). This is the full Shufersal olive oil shelf — the scraper exhausted all pages. D1 scores will cluster tightly due to the narrow macro profile of olive oil; the primary differentiation layer is the D5/D6 authenticity annotation, not nutrition.

### Next Steps

Frontend JSON is NOT generated — Phase 5 requires owner tripwires 3 (`authenticity_annotation_gate`) and 2 (`go_live`) to be cleared first.

Open items for other agents:
- **Nutrition Agent:** confirm D5-OO-002 harvest-date signal as category-level note (per Phase 4 Return Block request); finalize Hebrew copy for `categoryNote` slot.
- **Owner:** tripwire 3 (`authenticity_annotation_gate`) → tripwire 2 (`go_live`).
- **Frontend Agent:** holds until both owner tripwires cleared.

### Proposed Status

IN_PROGRESS — Phase 2 BSIP2 complete. Extractor bug fixed, 13 products scored, output at `olive_oil_bsip2_20260606.json`. Awaiting: Nutrition Agent harvest-date category-note confirmation, owner `authenticity_annotation_gate` + `go_live` clearances. Phase 5 (Frontend) cannot start until tripwires cleared.

---

## Tripwire 3 Clearance Record — `authenticity_annotation_gate` (Owner — 2026-06-06)

### Signal Classification Decisions

| Signal | Final ID | Disposition | Evidence type | Severity |
|---|---|---|---|---|
| Origin opacity | D5-OO-001 | APPROVED — copy unchanged | Label fact | Transparency note |
| Multi-country blend | D5-OO-003 | APPROVED — copy unchanged | Label fact | Informational |
| Turkish origin | D6-OO-003 | APPROVED WITH CHANGES — reclassified D5→D6; "ודאות אותנטיות מוגבלת" framing; "זיוף"/"סיכון" language removed; confidence-qualifier framing only | Research-backed confidence qualifier | D6 confidence qualifier |
| Processing-state | D6-OO-002 | APPROVED WITH CONDITION — elevate to category note if fires on ≥70% of shelf; copy revised to name what WOULD satisfy each gap | Derived label composite | Confidence qualifier |

### Namespace Ruling

`consumer_fraud_flag` → **`authenticity_annotation_gate`** effective 2026-06-06.

Removed from: TASK-197 frontmatter, spec header, Section 9, Section 10, all schema annotation classes, all body governance language.

Retained "fraud" only in: BEV-083 evidence body (scientific term of the cited research peer-reviewed literature).

### Copy Changes Mandated

**D6-OO-003 (formerly D5-OO-004) — Hebrew copy revised:**
> Old: מקור: טורקיה — סיכון אותנטיות מוגבר / מחקרי זיוף מזון...
> New: מקור הזיתים: טורקיה — ודאות אותנטיות מוגבלת / מחקרי ציות במסחר הבינלאומי מצביעים על שונות רבה יחסית בעמידה בתקנים בשמן זית ממקור טורקי. ברי מציינת זאת כהסתייגות אמינות — לא כממצא על המוצר הספציפי.

**D6-OO-002 — Hebrew copy revised (second sentence now names what would satisfy the gap):**
> Old: המוצר מסומן כ"כתית מעולה" אך אינו מציין מקור קציר, תאריך קציר, או תעודת הגנה. אין ביכולתנו לאמת את הסיווג מהמידע הזמין.
> New: המוצר מסומן "כתית מעולה" אך אינו כולל מקור קציר, תאריך קציר, או תעודת הגנה מוכרת. אלה הם הנתונים שמאפשרים אימות עצמאי של הסיווג.

### UI Separation Requirements (Frontend Agent mandate)

Consumer UI must visually distinguish three annotation types:
- **Label fact** (D5-OO-001, D5-OO-003): neutral chip, no warning color
- **Missing transparency** (D5-OO-002, category note): muted note, gray — not orange/red
- **Research-backed confidence qualifier** (D6-OO-003, D6-OO-002): explicitly labeled as confidence qualifier; visually distinct from label facts; mandatory second sentence naming the evidence scope

### Tripwire Status — Updated

- `first_batch_consult`: CLEARED (2026-06-06)
- `authenticity_annotation_gate`: **CLEARED (2026-06-06)** — all four signal classes approved
- `go_live`: **CLEARED (2026-06-06)** — owner authorized go-live; Phase 5 unblocked

---

## D6-OO-002 Firing Rate Determination — categoryNote (2026-06-06)

**Signal:** D6-OO-002 — Processing-state plausibility risk (EVOO verification gap)

**Threshold:** ≥70% of the extra virgin labeled shelf → elevate to categoryNote

**Corpus check (13 clean Shufersal products):**

| Metric | Count |
|---|---|
| Products with extra virgin grade detected | 11/13 |
| Of those: missing harvest date | 11/11 (100%) |
| Of those: missing PDO/PGI cert | 11/11 (100%) |
| D6-OO-002 fire rate (% of EVOOs) | 100% |

**Determination: categoryNote** — 100% exceeds the 70% threshold. D6-OO-002 does NOT fire per-product on any of the 13 products. It is elevated to a category-level note alongside D5-OO-002.

**Final per-product annotation roster (all 13 products):**

| Signal | Per-product fires | Count |
|---|---|---|
| D5-OO-001 (origin opacity) | origin_country_primary = "Unknown" | 1 product |
| D5-OO-003 (multi-country blend) | origin_multi_country = true | 0 products |
| D6-OO-003 (Turkish origin) | origin_country_primary = "TR" | 0 products |
| D6-OO-002 (EVOO verification gap) | → categoryNote | 0 per-product |

**Category notes (applies to whole page):**
- D5-OO-002: harvest date absent from Israeli EVOO shelf (Hebrew copy confirmed, Phase 3 Addendum)
- D6-OO-002: EVOO grade cannot be independently verified from label alone (Hebrew copy confirmed in tripwire 3 clearance record)

---

## Go-Live Clearance Record — `go_live` (Owner — 2026-06-06)

All three tripwires cleared. Phase 5 (Frontend Agent) authorized to proceed.

**Corpus state at go-live:**
- 13 clean Shufersal products, 11 sufficient (60/C), 2 insufficient_data
- Score uniformity (all 60/C) is a truthful finding — cooking oil category cap + NOVA-1 floor. Not an engine failure.
- Primary differentiation layer: D5/D6 authenticity annotations, not D1 nutrition

**Frontend Agent instructions (recorded here as mandate):**
1. Generate frontend JSON from `C:\Bari\02_products\olive_oil\bsip2_scored\olive_oil_bsip2_20260606.json`
2. Output to `C:\Bari\bari-web\src\data\comparisons\olive_oil.json`
3. Gen 1 architecture — מעדנים is the canonical reference
4. Authenticity annotations rendered in D5/D6 expansion section ONLY — never in the collapsed row
5. Two category notes in the `categoryNote` slot (D5-OO-002 + D6-OO-002 Hebrew copy from clearance record)
6. Three visual tiers (from tripwire 3 clearance): label facts (neutral chip) / missing transparency (gray/muted) / research-backed confidence qualifiers (explicitly labeled, mandatory evidence scope sentence)
7. D1 score uniformity disclosed via the scope limitation note in the category caveat
8. Route: `/hashvaot/shemen-zayit`
