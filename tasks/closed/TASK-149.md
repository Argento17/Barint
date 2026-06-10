---
id: TASK-149
title: "Re-scrape + re-score LIVE maadanim — EV-029 fat-parser bug collapsed fat on 88/200 products (latent grade impact)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
depends_on: [TASK-142A, TASK-151]
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "3 maadanim insight/comparison lines were neutralized inline (false point-gaps + 'lowest score' position from the old corrupted scores). Substance kept; Content should author proper replacements when convenient."
blocks: []
parent: TASK-142A
category_id: maadanim
summary: >
  The EV-029 / TASK-142A blast-radius audit confirmed LIVE maadanim is AFFECTED by the shared Shufersal
  BSIP0 nutrition-parse bug: the trans-fat row ("שומן טראנס פחות מ-0.5") was captured as TOTAL fat -> fat_g=0.5
  on 88/200 products, and saturated fat was never captured (0% across the corpus). Fat feeds the score engine
  (fat_quality uniformly neutralized to 50; also feeds fat_pct_of_kcal / hp_fat_*), so the LIVE maadanim grades
  carry latent error. The parser is already fixed (TASK-142A) and wired into shufersal_maadanim/01_scrape_maadanim.py.
  Re-scrape on the fixed parser -> re-build BSIP1 -> re-score -> QA -> diff vs live -> Product/Nutrition sign-off
  before any LIVE score swap.
---

# TASK-149 — Re-scrape + re-score LIVE maadanim (EV-029 fat collapse)

Spun off TASK-142A blast-radius (EV-029). **LIVE category — any score change is a published-score swap and
requires Product + Nutrition sign-off before promotion** (CLAUDE.md "do not change published scores unless
explicitly instructed"). This task executes the corrected re-score and produces the diff; it does NOT
unilaterally swap live grades.

## Defect (confirmed by EV-029 audit)
- 88/200 maadanim raw products had `fat_g = 0.5` (trans-row captured as total fat).
- Saturated fat 0% captured -> `fat_quality` dead (neutralized to 50) across the corpus.
- Parser fixed centrally in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`; the maadanim scraper
  (`shufersal_maadanim/01_scrape_maadanim.py`) is already wired to it.

## Required work
1. Re-scrape Shufersal maadanim with the fixed parser (replace the corrupt raw scrape).
2. Re-build BSIP1 on corrected fat/saturated values.
3. Re-score on the UNMODIFIED engine (no score tuning, no router changes) -> new run id.
4. QA gate incl. COV-006 plausibility; confirm fat sane across the corpus, no implausibility fails.
5. **Grade diff vs the LIVE maadanim grades** — quantify how many products change grade and by how much
   (esp. the documented anchors: מילקי=E, יופלה GO=69.6/B). Flag any A-ceiling / disclosure impacts.
6. Hand the diff to **Product Agent** (publication decision) + **Nutrition Agent** (grade sign-off).

## Exit / DoD
Clean re-scrape (fat sane, COV-006 pass); re-score complete on UNMODIFIED engine; grade-diff vs live delivered;
Product + Nutrition sign-off obtained. ONLY THEN swap the LIVE maadanim scores + frontend JSON. Then propose
RETURNED (CC records CLOSED). Do not promote any score before sign-off.

## Guards
Engine unmodified; no frozen invariants touched; LIVE scores swapped only after explicit Product/Nutrition
approval; rollback = current live run retained until swap is approved.

---

## RETURN BLOCK — proposed RETURNED (2026-06-02, data-agent)

**Data step complete; LIVE swap gated on Product + Nutrition sign-off (NOT done — human gate).**

**Pipeline executed on the UNMODIFIED engine (no score tuning, no router change):**
- **Re-scrape** (fixed shared parser): `02_products/maadanim/maadanim_bsip0_raw_20260602T055557.json`, 200 products,
  composition gate PASS. **fat=0.5 collapsed 87→2** (the 2 are genuinely 0.5g); **saturated fat 0→100 captured**;
  raw nutrition source persisted on 170 (TASK-151 hardening confirmed in a live run).
- **Rebuild BSIP1** → `run_maadanim_001/output` (removed 8 orphan barcodes not in the new scrape → clean 200).
- **Re-score** → `02_products/maadanim/bsip2_outputs/run_maadanim_001/` (200 traces, 0 errors; 8 orphan trace dirs removed).

**Grade diff vs LIVE baseline** (`reports/ev029_rescore/baseline_live_run001.json` ← captured from the pre-fix
run_001 traces before any overwrite): **191 matched barcodes, 33 grade changes, 126 score shifts (≥0.05)**,
predominantly DOWNWARD as EV-029 predicted (understated fat had inflated grades): D→E 15, C→D 12, D→C 3,
C→B 2, E→insufficient 1. **18 of the grade changes are on products whose fat was corrected from 0.5.**
Full detail: `reports/ev029_rescore/grade_diff.json`.

**LIVE page untouched:** frontend builder NOT run; `maadanim_frontend_v2.json` unchanged. Intermediates
(BSIP1 + bsip2 traces) now hold corrected data — the website still shows old grades until a Product/Nutrition-
approved rebuild + swap. Rollback = git (committed live run_001) + the baseline snapshot.

**Hand to Product (publication decision) + Nutrition (grade sign-off).** On approval: rebuild frontend JSON +
swap. **Proposed RETURNED** — Central Controller records CLOSED.

### LIVE SWAP SHIPPED (2026-06-02, owner-approved)
Owner approved publication. Rebuilt `maadanim_frontend_v1.json`→`v2.json` from corrected traces (87 editorial-
scope products) and copied to `bari-web/src/data/comparisons/maadanim_frontend_v2.json`. **3 stale insight/
bottom/comparison lines neutralized** (build_maadanim_v2 carried hardcoded prose keyed to the old scores):
מילקי שוקולד ("lowest score"/"30-pt gap" → composition framing), מילקי 26% פחות סוכר ("1.5-pt gap" → "profile
nearly identical"), פודינג אינסטנט שוקולד ("18 pts higher" → powder-vs-ready-cup composition fact). The 3
ingredient-count superlatives verified still true. Maadanim featured card is data-driven (no hardcoded scores).
`npx tsc --noEmit` exit 0. Editorial neutralizations flagged for Content polish. **Ready for CLOSED.**

---

## CLOSED (2026-06-02, cc-agent — close-readiness gate PASS; owner sign-off received)
Human Product/Nutrition sign-off (the gate this task explicitly held for) supplied by the owner on 2026-06-02
("close 149-151"). Verified against artifacts:
- LIVE swap present in working tree — `bari-web/src/data/comparisons/maadanim_frontend_v2.json` shows as
  modified (` M`), i.e. the corrected-trace rebuild landed on the published file.
- Grade-diff artifacts exist — `02_products/maadanim/reports/ev029_rescore/grade_diff.json` +
  `baseline_live_run001.json` (191 matched, 33 grade changes, predominantly downward as EV-029 predicted).
- Engine unmodified (re-score only); fat collapse 87→2, saturated 0→100 captured.
**Residual (non-blocking):** 3 stale insight/comparison lines were neutralized inline, not yet rewritten —
carried forward as the `cc fyi` flag for Content to author proper replacements. **CLOSED.**
