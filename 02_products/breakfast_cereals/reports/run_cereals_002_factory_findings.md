# TASK-140 — Cereals full-cycle BSIP0→BSIP2 (run_cereals_002) — findings & GO/NO-GO

**Owner:** data-agent · **Date:** 2026-06-01 · **Skill:** bari-category-factory (no stage skipped)
**Engine:** proto_v0 / 0.4.0 (UNMODIFIED — no score tuning, no manual edits)
**Source:** Shufersal real scrape (reused the run_yogurt_003 Shufersal path)
**Verdict:** 🟡 **NO-GO to launch live in this run — full cycle executed, one exit gate fails on a scoped router gap.**

---

## 1. What ran (all 7 factory stages)

| Stage | Artifact (`factory_run_002/`) | Result |
|---|---|---|
| 1 Shelf map | `shelf_map.json` | PASS — Shufersal `דגני בוקר` → breakfast-cereals; bars/pita/desserts out of scope |
| 2 Corpus filter | `corpus_filter.json` | PASS — include/exclude gates; granola kept (sub-pool, not excluded); no snack-bar overlap |
| 3 BSIP0 gate | `bsip0_gate_result.json` | PASS — 113 scraped, 0 fetch fails; **92 displayable @ 100% nutrition+ingredients** |
| 4 BSIP1 enrichment | `run_cereals_002/output/` (92) + `cereals_constructs_report.json` | PASS — core enricher + **4 governance constructs** |
| 5 QA gate | `qa_gate_result.json` | **HARD FAIL** — misroute 7.6% > 5% (QA-CER-001) |
| 6 BSIP2 readiness | `bsip2_readiness_checklist.json` | CONDITIONAL — engine registered, evidence-grounded; pending Nutrition + router fix |
| 7 Frontend package | `frontend_package.json` | PASS (artifact) — **NON-AUTHORITATIVE**, 81/92 display-approved, RTL, Hebrew 100% |

Full BSIP0→BSIP2 chain reproducible from `03_operations/bsip0/scrape/shufersal_cereals/`
(`01_scrape` → `02_build_bsip1` → `batch_run_cereals_002.py` → `03_package_frontend`).

## 2. Corpus & scores

- **113 scraped → 92 displayable** (excluded: 12 no-nutrition, 9 non-cereal contaminants).
- **0% INSUFFICIENT displayable; 100% nutrition + ingredient coverage; Hebrew 100%; gtin13 82.5% strict.**
- Grades **A7 · B10 · C48 · D25 · E2**, median **58.3** (engine thresholds S90/A80/B65/C50/D35).
- Subtypes: granola 25, oat 20, whole-grain flakes 16, cornflakes 9, muesli 8, kids 3, bran 2, puffed 2, other.

## 3. The four governance constructs (applied + documented)

1. **Granola sub-pool** (Rule 5 / Sec 2.9): **25/92** in granola pool via 2-of-3 proxy
   (added-sugar≥15g proxy / fat≥10g / processing). NOVA confirmation carried to BSIP2.
2. **Children's** (Sec 2.8): **4** classified — recognized child-mascot brands (Nesquik/Trix/Coco/
   nougat-pillows) satisfy D1+D2 jointly. ⚠️ D1 visual mascots on non-listed brands and D3 serving
   size are NOT text-observable → recall is conservative; single-indicator products flagged for CE review.
3. **Whole-grain threshold** (Sec 5.2.1): **43** whole-grain claims; **8 Marketing Divergence Findings**
   (claim present, ingredient ordering does not support ≥30% composition). First-grain-ingredient test.
4. **Endemic fortification** (Sec 6.4 / DISTORTION-004): **27.2% fortified → BELOW the 50% endemic
   threshold.** The Endemic Distortion Protocol does **NOT** trigger for this corpus. **This contradicts
   the pre-data governance assumption** that fortification is "the majority" in cereals — the real
   Shufersal shelf is granola/oat/muesli-heavy (largely unfortified). Product-level disclosure suffices.

## 4. Why NO-GO (the one failing exit gate)

**QA-CER-001 — misroute 7.6% (7/92 > 5% gate).** 7 *real* cereals route outside the cereal family:
- spelt flakes (`כוסמין מלא 100%`, `פתיתים אורגנים כוסמין`) → **bread** (whole-grain matrix reads as bread)
- nut-dense muesli/granola + honey Cheerios (×3) → **whole_food_fat** (nut tokens trigger WFF contamination)
- corn/rice rings → **beverage**; kids nougat pillows → **whole_food_fat**

Root cause: **Router v2 has no cereal anchor** (documented known gap in `scoring.md`). This is the same
*class* as run_yogurt_003's 19% misroute. **Fixing it is an engine/router change — out of scope for this
data-pipeline task and must not be hand-tuned here.** The 5 non-cereal contaminants (bread/pita/rolls/
dessert) that leaked grain tokens were already removed at curation (corpus-purity fix, like the yogurt
olive false-positives).

## 5. Secondary findings (for Nutrition / Product)

- **4 shaped baked-flake A's** (`פתיתים אפויים כוכבים/טבעות/אורז/קוסקוס`) read NOVA 1 → 85/A. Shaped
  baked/extruded flakes are plausibly NOVA 3 — **possible NOVA-proxy under-call**; withheld pending
  Nutrition review. The 2 plain whole-oat A's (`שיבולת שועל עבה`, `קוואקר`) ARE legitimate (single-
  ingredient whole grain, milk-precedent-consistent).
- **scoring.md grade table is stale** (A≥85) vs engine `constants.py` (A≥80) — **cross-ref TASK-139A**;
  affects A-count reporting across all categories, not just cereals.

## 6. Recommendation

- **GO / VALIDATED:** Shufersal source, full pipeline, 4 constructs, data quality (0 insufficient, 100% coverage).
- **NO-GO to launch live now.** Frontend package preserved **NON-AUTHORITATIVE**; not shipped.
- **Two scoped follow-ups before run_cereals_003 can replace this:**
  1. **Router:** add a cereal anchor that survives grain/nut tokens (category prior from the BSIP0
     cereal-shelf query, mirroring the yogurt router recommendation). *(Engine — Nutrition+Data)*
  2. **Nutrition:** review the NOVA-1 shaped-baked-flake reads; reconcile the scoring.md A-threshold (TASK-139A).
- Live cereals state unchanged (greenfield; nothing was shipped). Only the Central Controller records CLOSED.

*data-agent · TASK-140 / run_cereals_002 · 2026-06-01 · engine 0.4.0 unmodified · provenance preserved*
