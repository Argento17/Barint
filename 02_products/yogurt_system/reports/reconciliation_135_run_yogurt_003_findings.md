# TASK-135 — run_yogurt_003 execution, reconciliation & GO/NO-GO

**Owner:** data-agent · **Date:** 2026-06-01 · **Parent:** TASK-135 (DEC-005 retirement)
**Engine:** proto_v0 / 0.4.0 (UNMODIFIED — no manual score edits; ingredient_enricher unmodified)
**Source:** Shufersal product pages (real Israeli yogurt SKUs, VPN-enabled scrape)
**Verdict:** 🟡 **NO-GO to retire DEC-005 in this run — but the blocker has fundamentally changed.**
The run_yogurt_002 *data* barrier is **resolved** (ingredients 0%→90%, insufficient 48%→0%). The
new, narrower blocker is **engine calibration for the yogurt category**, exposed for the first time
by a real ingredient-bearing corpus. Live DEC-005 manual shelf untouched; no scores changed.

---

## 1. What was executed (full real BSIP0→BSIP2 cycle, Shufersal)

| Stage | Artifact | Result |
|---|---|---|
| BSIP0 scrape | `03_operations/bsip0/scrape/shufersal_yogurt/01_scrape_yogurt.py` → `02_products/yogurt_system/bsip0/yogurt_bsip0_raw_*.json` | **97** real SKUs, gtin13 barcodes, Hebrew names, source_url per item. **0 failed fetches.** |
| BSIP0 gate | (in-scraper) | **PASS** — 90% nutrition, 90% ingredients, 100% images. |
| BSIP1 build+curate | `…/shufersal_yogurt/02_build_bsip1_yogurt.py` → `03_operations/bsip1/run_yogurt_003/output/` (88) + `curation_report.json` | 97 → **88 included / 9 excluded** (all `no_usable_nutrition`). Real ingredient enrichment via core `ingredient_enricher.py`. **Ingredient coverage among included = 88/88 (100%).** |
| BSIP2 score | `03_operations/bsip2/proto_v0/src/batch_run_yogurt_003.py` → `02_products/yogurt_system/bsip2_outputs/run_yogurt_003/` (88 traces) + `reports/run_yogurt_003_run_summary.json` | **88 processed, 0 errors, 0 INSUFFICIENT.** |

Provenance preserved: every record carries real barcode, Shufersal `source_url`, and acquisition query. `NON_AUTHORITATIVE.md` marker written to the run dir.

## 2. The headline: the run_yogurt_002 blocker is RESOLVED

The 135A NO-GO had exactly one cause — OFF was ingredient-blind (0/50), so 48% scored INSUFFICIENT
and NOVA was a flat, unreliable 2. Shufersal removes that wall completely:

| Signal | run_yogurt_002 (OFF) | run_yogurt_003 (Shufersal) |
|---|---|---|
| Ingredient coverage | **0%** | **90% scraped / 100% of scored** |
| Nutrition coverage | partial | 90% |
| Data sufficiency | **48% INSUFFICIENT** | **0% INSUFFICIENT** |
| NOVA | flat 2 (conf 0.2, unreliable) | differentiated **2 / 3 / 4** (4, 31, 53) |
| Hebrew names | empty / noisy ("Yoghort") | clean, native |
| Engine signals (router/additives/sweeteners) | empty | populated from real ingredients |

**Shufersal is a validated, reproducible yogurt source.** The source-assessment GO call holds.

## 3. Distribution: machine 003 vs OFF 002 vs DEC-005 manual

| Metric | DEC-005 manual (13) | run_yogurt_002 OFF (46) | run_yogurt_003 Shufersal (88) |
|---|---|---|---|
| INSUFFICIENT | 0% | 47% | **0%** |
| Score range (scored) | 51–88 | 60–75 | 34–78 |
| Score median | 72 | 70 | **57** |
| Grade A | **5** | 0 | **0** |
| Grade B / C / D / E | 5 / 3 / – / – | 21 / 3 / – / – | 17 / 46 / 24 / 1 |
| Ceiling | 88/A | 75/B (confidence-capped) | **78/B** |

**The machine run is data-complete but scores the category markedly LOWER** — median 57 vs 72, and
**no grade-A**. This is not a data defect: with real ingredients visible, the engine sees that
most Israeli mainstream yogurts contain added sugar (`סוכר`/`סוכר לבן`), modified starch
(`עמילן…מעובד E-1442`), and stabilizers (`פקטין`) → NOVA 3–4 (60% NOVA 4). run_yogurt_002 scored
*higher* only because, being ingredient-blind, it could not see any of this and over-credited.
**003's lower scores are more truthful, not worse.**

## 4. Three calibration gaps the real corpus exposed (the new blocker)

A real ingredient-bearing run revealed problems the curated manual shelf and the ingredient-blind
OFF run both hid. None is a data-acquisition problem; all are engine/pipeline calibration:

**(a) No grade-A ceiling — dairy scoring philosophy.** Top product is 78.2/B (יוגורט גו נטול לקטוז);
the manual shelf's #1 is plain תנובה 3% at **88/A**. The engine, reading ingredients, caps mainstream
Israeli yogurt at B. Genuine disagreement: *does Bari accept that real Israeli mainstream yogurt tops
out at B, or does the manual A-ceiling encode a scoring philosophy the engine should adopt?* This is a
**Nutrition/Product decision**, not a data decision.

**(b) Router yogurt-anchor gap — 17/88 (19%) misrouted.** Flavored "GO" yogurts → `dessert` (8);
crunch/cornflake yogurts → `cereal`/`snack_bar_granola` (4); and **2 false positives leaked curation**:
`זית ירוק יווני` (green olives — matched the "יווני/Greek" include token) routed `whole_food_fat`. The
router can't hold "yogurt" identity once a flavor/topping/`יווני` token dominates the name+ingredients.

**(c) Enricher culture-vocabulary gap — 0/88 fermentation markers detected.** Israeli labels write
`חיידק פרוביוטי` / `ביפידוס` / `BIFIDUS` / `תרבית`; the core enricher's `FERMENTATION_TERMS` only match
`תרבויות` / `ביפידובקטריום` / `לקטובציל`. So the live-culture **positive signal — the most
category-defining quality marker for yogurt — is never credited**, directly depressing the plain/bio
yogurts that should sit at the top. (Left unmodified per the no-tuning constraint; reported as a finding.)

## 5. Best-effort overlap vs DEC-005 manual shelf

| Manual shelf | Manual | Machine 003 (best match) | Δ |
|---|---:|---|---:|
| יוגורט מלא 3% תנובה | 88/A | plain full-fat ≈ 65–67/B (dairy_protein, NOVA 3) | −21 → A→B |
| יוגורט ביו 1.5% תנובה | 87/A | יוגורט ביו תנובה 1.5% = 66.7/B | −20 → A→B |
| יוגורט יווני 5% שטראוס | 85/A | Greek 5% band ≈ 62–67/C–B | ≈ −20 |
| אקטיביה טבעית דנונה | 78/B | bio/probiotic plain band 65.8–66.7/B | ≈ −12 |
| יופלה GO פירות יער | 69/B | יופלה GO פירות יער = 54.6/C (mis-routed dessert) | −14 → B→C |

Every identifiable match drops ~12–21 pts; the manual A-tier collapses to B, mid-tier flavored to C/D.
The two shelves encode **different definitions of a good yogurt** — the disagreement is now visible
because the engine can finally see ingredients.

## 6. validate-corpus / handoff

- **Live `yogurts_frontend_v1.json` (DEC-005):** untouched, remains contract-clean.
- **No run_yogurt_003 frontend dataset was built or shipped** (contract: produce frontend output only
  if validation passes). It would fail `--handoff`: §2.4 explanation completeness (no validated insight
  lines), router misroute rate 19%, and the unresolved A-ceiling/culture-credit calibration. Building it
  would create a failing orphan in the live data dir. Run preserved as non-authoritative evidence.

## 7. Recommendation — GO/NO-GO

- **Source: 🟢 GO / VALIDATED.** Shufersal supplies real ingredients + nutrition + Hebrew names +
  barcodes at 90%, 0% insufficient. **run_yogurt_002's blocker is permanently resolved.**
- **Retire DEC-005 now: 🟡 NO-GO.** Promoting run_yogurt_003 would ship a category regression — no A
  ceiling, 19% misrouting (incl. 2 non-yogurt false positives), and scores computed without the
  fermentation positive. Not an editorial/QA-validated shelf.
- **DEC-005 stays** as the disclosed manual-MVP exception; yogurts remains LIVE on the manual shelf.
- **TASK-135 stays BLOCKED — but reclassified.** Old blocker ("no ingredient-bearing source exists")
  is **CLOSED by this run**. New blocker is **yogurt-category engine calibration**, with three scoped,
  governed follow-ups before a machine shelf can replace DEC-005:
  1. **Router:** add a yogurt anchor so flavor/topping/`יווני` tokens don't override dairy identity
     (fixes 19% misroute + olive false positives). *(Frontend/router — Nutrition+Data)*
  2. **Enricher:** extend `FERMENTATION_TERMS` with Israeli culture vocabulary
     (`חיידק פרוביוטי`, `ביפידוס`, `BIFIDUS`, `תרבית`) — governed BSIP1 change, then re-run. *(Data)*
  3. **Scoring philosophy:** decide the dairy A-ceiling question — is a B-ceiling for mainstream Israeli
     yogurt the correct, defensible read, or should plain live-culture yogurt reach A? *(Nutrition/Product)*

Only the Central Controller records CLOSED. This run is reproducible end-to-end from the three scripts above.

*data-agent · TASK-135 / run_yogurt_003 · 2026-06-01 · engine 0.4.0 unmodified · no manual score edits · provenance preserved*
