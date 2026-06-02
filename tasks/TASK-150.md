---
id: TASK-150
title: "Re-scrape + re-score LIVE hummus — EV-029 fat-parser bug collapsed fat on 59/69 products (max fat 5.9g)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
depends_on: [TASK-142A, TASK-151]
blocks: []
parent: TASK-142A
category_id: hummus
roadmap_impact: true
cc_reviewed: 2026-06-02
cc_comments:
  - date: 2026-06-02
    flag: verify
    text: "Before CLOSE: the TASK-039 fat register is now stale (report-only, did NOT affect scores) — regenerate or retire it so the batch summary stops emitting the false 'fat_quality from incorrect fat_g' warning."
  - date: 2026-06-02
    flag: fyi
    text: "Featured-hummus card had 3 hardcoded lines hand-fixed (A-count 1→5, gap 37→47, 'fat not shown'→now shown). Frontend/Content should confirm the new copy reads well."
summary: >
  The EV-029 / TASK-142A blast-radius audit confirmed LIVE hummus is AFFECTED by the shared Shufersal BSIP0
  nutrition-parse bug (same defect first seen in the TASK-039 hummus audit, which patched downstream but not the
  shared parser): the trans-fat row was captured as TOTAL fat -> fat_g=0.5 on 59/69 products, with the whole
  corpus capping at max fat 5.9g (implausible for tahini-based spreads) and 0% saturated captured. Fat feeds the
  score engine, so the LIVE hummus grades carry latent error. The parser is fixed (TASK-142A) and wired into
  shufersal_hummus/02_scrape_hummus_shufersal.py. Re-scrape -> re-build BSIP1 -> re-score -> QA -> diff vs live
  -> Product/Nutrition sign-off before any LIVE score swap.
---

# TASK-150 — Re-scrape + re-score LIVE hummus (EV-029 fat collapse)

Spun off TASK-142A blast-radius (EV-029). **LIVE category — any score change is a published-score swap and
requires Product + Nutrition sign-off before promotion** (CLAUDE.md "do not change published scores unless
explicitly instructed"). Note: TASK-039 previously caught this in hummus but only patched downstream; the shared
parser fix (TASK-142A) is what finally closes re-propagation — so this re-score is on genuinely corrected data.

## Defect (confirmed by EV-029 audit)
- 59/69 hummus raw products had `fat_g = 0.5`; whole corpus max fat 5.9g (implausible — tahini is fat-dense).
- Saturated fat 0% captured -> `fat_quality` neutralized.
- Parser fixed centrally in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`; the hummus scraper
  (`shufersal_hummus/02_scrape_hummus_shufersal.py`) is already wired to it.

## Required work
1. Re-scrape Shufersal hummus with the fixed parser (replace the corrupt raw scrape).
2. Re-build BSIP1 on corrected fat/saturated values; confirm fat now reflects real tahini-based composition.
3. Re-score on the UNMODIFIED engine (no score tuning) -> new run id.
4. QA gate incl. COV-006 plausibility; confirm fat sane (no longer capped ~5.9g), no implausibility fails.
   Cross-check the raw-vs-prepared boundary still holds (tahini+sodium+energy, never protein) per TASK-137A.
5. **Grade diff vs the LIVE hummus grades** (`02_products/hummus/frontend/hummus_frontend_v3.json`) — quantify
   grade changes and magnitude.
6. Hand the diff to **Product Agent** (publication decision) + **Nutrition Agent** (grade sign-off).

## Exit / DoD
Clean re-scrape (fat sane, COV-006 pass); re-score on UNMODIFIED engine; grade-diff vs live delivered;
Product + Nutrition sign-off obtained. ONLY THEN swap the LIVE hummus scores + frontend JSON. Then propose
RETURNED (CC records CLOSED). Do not promote any score before sign-off.

## Guards
Engine unmodified; no frozen invariants touched; LIVE scores swapped only after explicit Product/Nutrition
approval; rollback = current live hummus_frontend_v3.json retained until swap is approved.

---

## RETURN BLOCK — proposed RETURNED (2026-06-02, data-agent)

**Data step complete; LIVE swap gated on Product + Nutrition sign-off (NOT done — human gate).**

**Pipeline executed on the UNMODIFIED engine:**
- **Re-scrape** (fixed shared parser) → `observations_bsip0/shufersal/` (82 products, 0 failed).
  **fat=0.5 collapsed 59→0**; real tahini-range fat now present (e.g. 24/32.3/55.3g); raw nutrition source
  persisted on 78 (TASK-151 hardening confirmed live).
- **Convert** BSIP0→BSIP1 (82) → `run_hummus_001/output`.
- **Surgical canonical update:** injected ONLY the corrected `normalized_nutrition_per_100g` into the existing
  69 `canonical_bsip1` records (preserving enrichment fields the fresh convert lacks). 67 updated, **64 fat
  corrections** (`reports/ev029_rescore/canonical_fat_injection.json`).
- **Re-score** → `intelligence_bsip2/run_hummus_001/` (69 traces, 0 errors).

**Grade diff vs LIVE baseline** (`reports/ev029_rescore/baseline_live_frontend_v3.json` ← from published
`hummus_frontend_v3.json`): **66 matched, 24 grade changes**, predominantly DOWNWARD as predicted (capped fat
≤5.9g had inflated grades): B→C 14, C→D 5, D→C 2, None→B 2, A→B 1. Detail: `reports/ev029_rescore/grade_diff.json`.

**Note on the TASK-039 fat register** (`audit/fat_anomaly_TASK039.json`): it is **report-only** in
`batch_run_hummus_001.py` (never overrides fat or score), so the corrected fat flowed through cleanly. The
register is now STALE (its 69 entries describe a bug fixed at source) and should be regenerated/retired so the
batch summary stops emitting the "fat_quality derived from incorrect fat_g" warning — recommended follow-up,
not score-affecting. (Saturated fat is still not captured in the hummus record schema — pre-existing; total-fat
correction is the material fix.)

**LIVE page untouched:** frontend builder NOT run; `hummus_frontend_v3.json` unchanged. Rollback = git +
`hummus_frontend_v3.PRE-TASK129A.json` + baseline snapshot.

**Hand to Product (publication decision) + Nutrition (grade sign-off).** On approval: rebuild frontend JSON +
swap. **Proposed RETURNED** — Central Controller records CLOSED.

### LIVE SWAP SHIPPED (2026-06-02, owner-approved)
Owner approved publication. Surgically updated `hummus_frontend_v3.json` from corrected traces (66 products:
59 score / 24 grade / 66 fat-panel corrections — preserving all editorial) and copied to
`bari-web/src/data/comparisons/hummus_frontend_v3.json`. Per-product insight lines verified editorially clean
(0 score-dependent claims). **Featured-hummus card had 3 stale hardcoded lines fixed:** A-count (was already
wrong: claimed 1, real now 5), top-bottom gap 37→47, and "fat values not shown — source limitation" → now FALSE
(all 66 fat panels populated 0–55g) replaced with the real fat-range fact. `npx tsc --noEmit` exit 0. **Ready
for CLOSED.**

---

## CLOSED (2026-06-02, cc-agent — close-readiness gate PASS; owner sign-off received)
`roadmap_impact:true` + `cc_reviewed:2026-06-02` already set → PreToolUse close-guard satisfied. Human
Product/Nutrition sign-off supplied by owner on 2026-06-02 ("close 149-151"). Verified against artifacts:
- LIVE swap present in working tree — `bari-web/src/data/comparisons/hummus_frontend_v3.json` modified (` M`).
- Independently re-checked the two headline data claims in the swapped file: **A-grade count = 5** (matches the
  corrected featured-card line, was wrongly 1) and **66 products / 66 fat panels populated** (matches the diff).
- Grade-diff artifact exists — `02_products/hummus/reports/ev029_rescore/grade_diff.json` (66 matched, 24 grade
  changes, predominantly downward as the capped-fat ≤5.9g inflation predicted). Engine unmodified.
**Residual (non-blocking, the `cc verify` flag):** the TASK-039 fat register (`audit/fat_anomaly_TASK039.json`)
is now stale — it is **report-only** (never overrode fat or score, so it did NOT affect this re-score), but it
still makes `batch_run_hummus_001.py` emit a false "fat_quality from incorrect fat_g" warning. Regenerate/retire
it as a clean-up follow-up; not score-affecting and not a close blocker. **CLOSED.**
