---
name: bsip0-fat-overwrite-ev029
description: TASK-142A/EV-029 — Shufersal nutritionList parser overwrote total fat with trans sub-row (fat=0.5) across ALL nutritionList categories; fixed centrally; cheese_003+live maadanim(149)+hummus(150) all re-scored & RETURNED awaiting sign-off; scrape now persists raw source (TASK-151); TASK-143 still blocked on run_yogurt_004
metadata: 
  node_type: memory
  type: project
  originSessionId: b72ec54f-f116-4de3-8ae0-8b352e4b38fd
---

**TASK-142A (RETURNED 2026-06-02) — EV-029, EV-026 data-hygiene family.**

The shared Shufersal `div.nutritionList` parser (`NUTR_LABEL_MAP`, substring + break-on-first)
mapped both `שומנים` (total fat) and `שומן` (substring of every `מתוכו…` sub-row) → `fat`. Panel
lists total fat first then "of which" sub-rows, so the trans row (`פחות מ 0.5`) **overwrote** total
fat → `fat_g=0.5`; saturated fat **never captured** (0% in every corpus — the signature). Hebrew
**final-letter trap**: `שומן` (final-ן) ⊄ `שומנים` (regular-נ), so naive stem fixes fail.

**Fix:** single-source parser `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`
(`classify_nutr_label` normalizes final-forms, most-specific-first, sub-rows never overwrite totals;
`parse_nutrition_list`). All 5 nutritionList scrapers (cheese/cereals/yogurt/maadanim/hummus) import it.
Data-ingestion only — NO scoring logic touched. Live re-scrape verified (גבינת עזים 32% 0.5→32 etc.).

**Blast radius:** affected = cheese_001/002, cereals_002, yogurt_003 (all NON-AUTHORITATIVE/NO-GO) +
**LIVE maadanim (88/200)** + **LIVE hummus (59/69, max fat 5.9g)**. `fat_quality` dimension uniformly
neutralized to 50 across affected runs. NOT affected (different paths, frozen): milk (Playwright tab
capture), bread (proto_v0), snacks, yohananof (textblock regex). TASK-039 had already found this in
hummus but never centralized the fix → it re-propagated to 4 categories.

**TASK-143 verdict:** run_yogurt_003 is **AFFECTED, not clean** → yogurt LIVE swap blocked until a clean
re-scrape (run_yogurt_004) + re-score. The parser itself is now fixed.

**QA guard:** `COV-006` in [[bsip_pipeline_definition]] QA runner (`03_operations/qa/run_qa.py`) hard-fails
≥5% implausible; scraper `main()` gate prints Plausibility line. Catches `sat>fat` and `fat≤0.5` with
energy ≥50 kcal above macro-implied energy (cereal flakes pass).

**run_cheese_003 DONE (TASK-142, RETURNED 2026-06-02)** — full cycle re-run on corrected fat, engine 0.4.0
UNMODIFIED. Re-scrape replaced the corrupt raw; BSIP1 at `run_cheese_003/output`, BSIP2 at
`bsip2_outputs/run_cheese_003`, artifacts in `factory_run_003/`. Gates GREEN: COV-006 0.0% implausible
(was 31.9%), fat sane all 4 sub-pools (cream-cheese now real 25–32% not 0.5g), misroute 1.7%, INSUFFICIENT
0% displayable. **Two truths the fix exposed:** (1) scores dropped truthfully — overall median 65→55,
cream-cheese 60.7→52 (real high fat now penalized); (2) 5 transparency-tier withholds on GENUINE partial
Shufersal panels (no total fat/protein/carbs at source) — run_002's "0 insufficient" was itself the bug
fabricating fat. A-ceiling holds on real fat: lone macro-A (טבורוג 5%/82) withheld, 0 A-eligible. NON-AUTHORITATIVE
pending Nutrition sign-off (`factory_run_003/NUTRITION_SIGNOFF_REQUEST.md`). **Nutrition signed
APPROVED-FOR-PUBLICATION 2026-06-02** (all 5 items; verdict in `factory_run_003/NUTRITION_SIGNOFF_VERDICT.md`) →
TASK-142 ready for Controller CLOSED; package stays NON-AUTHORITATIVE until Product promotes. **Engine is
0.4.1 NOT 0.4.0** (algorithm_version per `trace_writer.py:15`; TASK-144 EV-026/027/028) — Nutrition caught the
mislabel; both run_002+003 ran 0.4.1 so "unchanged between runs" holds; label corrected across all artifacts.

**LIVE maadanim (TASK-149) + hummus (TASK-150) DONE — re-scored AND SHIPPED LIVE 2026-06-02 (owner-approved),
engine UNMODIFIED.** Corrected frontends copied to `bari-web/src/data/comparisons/{maadanim_frontend_v2.json,
hummus_frontend_v3.json}` (tsc clean). Editorial drift fixed at swap time: 3 maadanim insight/comparison lines
neutralized (false point-gaps + "lowest score" from old scores) + 3 hummus featured-card lines fixed (A-count
1→5, gap 37→47, "fat not shown"→now shown). Both RETURNED, ready for Controller CLOSED.
- maadanim: re-scrape 200, fat=0.5 87→2, sat 0→100; rebuild (8 orphans dropped)+re-score run_maadanim_001;
  **33 grade changes / 126 score shifts**, mostly DOWN (D→E 15, C→D 12). Diff+baseline in
  `02_products/maadanim/reports/ev029_rescore/`.
- hummus: re-scrape 82, fat=0.5 59→0 (real tahini fat 24/32/55g); surgical inject of corrected
  `normalized_nutrition_per_100g` into the 69 `canonical_bsip1` (preserve enrichment), re-score
  `intelligence_bsip2/run_hummus_001`; **24 grade changes**, mostly DOWN (B→C 14, A→B 1). Diff in
  `02_products/hummus/reports/ev029_rescore/`. TASK-039 fat register is report-only (didn't override scores)
  but now STALE → regenerate/retire (recommended, not score-affecting).

**TASK-151 (hardening, RETURNED 2026-06-02):** `_shared/bsip0_nutrition.py` now also persists the raw
nutrition source — `extract_nutrition_raw(soup)→{rows, html}` written as `nutrition_raw_source` by all 5
scrapers. `parse_nutrition_list` split into `extract_nutrition_rows`+`parse_nutrition_rows` (behaviour
identical); offline replay (`parse_nutrition_rows(rows)`) == live parse. **Future EV-029-class label-map
fixes replay OFFLINE — no network re-scrape needed.** Root cause of this whole episode: scrapers persisted
only the parser's reduced `*_raw` output, so the true fat was unrecoverable from disk once corrupted.

**run_yogurt_004 DONE (TASK-143, RETURNED 2026-06-02)** — clean re-scrape (93→86 BSIP1) replaced corrupt raw;
BSIP1 `run_yogurt_004/output`, BSIP2 `bsip2_outputs/run_yogurt_004`, engine 0.4.1 UNMODIFIED. COV-006 0.0%,
fat=0.5 47/97→1. **EV-029 impact MILD on yogurt** — only 5/84 grade changes, median score delta 0.0 (yogurt fat
is genuinely low 0–3%, so fake-0.5 barely moves the score, unlike cream-cheese). Reconciled vs run_003 + LIVE
DEC-005 manual shelf (`reconciliation_143_run_yogurt_004_findings.md` + `run_yogurt_004_qa_gate.json`):
**downward correction confirmed** — live A-heavy (5 A's, top 88) vs machine B-capped (max 78.7, 0 A's); A-ceiling
139A does NOT restore A. DATA CYCLE CLEAN; **live swap HELD on 2 human gates** = PO go-live (retire DEC-005,
accept A→B) + Content/Design re-author (incl. plant-pool decision for soy/coconut live rows). No live frontend
touched.

**Still open:** TASK-142 + TASK-143 RETURNED, awaiting Controller CLOSED + (for 143) PO go-live before the live
yogurt swap. Related: [[bsip2-run-cheese-001]], [[bsip2_run_yogurt_003]], [[bsip2_task133_and_maadanim_drift]],
[[bsip2_evidence_registry_v1]].
