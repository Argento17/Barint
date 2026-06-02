---
id: TASK-135A
title: Execute run_yogurt_002 full BSIP0->BSIP2->comparison cycle + reconcile DEC-005
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Execute run_yogurt_002 full BSIP0->BSIP2->comparison cycle + reconcile DEC-005.
  COMPLETE: real OFF run executed end-to-end (46 SKUs, engine 0.4.0 unmodified).
  Verdict NO-GO — corpus is ingredient-blind (OFF Israeli yogurt ingredient
  coverage 0%), cannot replace the manual-MVP shelf. DEC-005 stays; TASK-135
  cannot close. Proposing RETURNED; Controller to record CLOSED.
---

# TASK-135A — Execute run_yogurt_002 full BSIP0->BSIP2->comparison cycle + reconcile DEC-005

## Return block (2026-06-01, data-agent) — proposing RETURNED

**Outcome:** Full real BSIP0→BSIP2 cycle executed and reproducible. **GO/NO-GO = 🔴 NO-GO** for
retiring DEC-005. Live yogurts shelf untouched; no scores changed; engine 0.4.0 unmodified.

**Done:**
- BSIP0 — `03_operations/bsip0/scrape/off_yogurt/` (scraper + 50 raw OFF records + scrape_log + curation_report). 50→46 included / 4 excluded. Real 729… barcodes only.
- BSIP1 — `03_operations/bsip1/run_yogurt_002/output/` (46 records). Ingredients absent → in `missing_fields`; subtype inferred + flagged. No fabrication.
- BSIP2 — `02_products/yogurt_system/bsip2_outputs/run_yogurt_002/` (46 traces) + `reports/run_yogurt_002_run_summary.json`. 46 processed, 0 errors.
- Reports — `02_products/yogurt_system/reports/reconciliation_135a_findings.md`; `NON_AUTHORITATIVE.md` marker in run dir.

**Blocking finding:** OFF Israeli yogurt **ingredient coverage = 0/50**. Yogurt scoring is
ingredient-driven, so the run is 48% INSUFFICIENT, ceiling 75/B, **0 grade-A**, 70% routed
"default", no consumer explanations — and it **inverts** the displayed shelf's logic (protein
mass dominates when ingredients are blind). Best-effort overlap: every match drops 5–17.5 pts
(A→B) or goes INSUFFICIENT. Same wall as TASK-129B, now confirmed on real products.

**Recommendation:**
- DEC-005 **NOT retired** — stays as the disclosed manual-MVP provenance exception. Yogurts remains LIVE.
- **TASK-135 cannot close.** run_yogurt_002 preserved as non-authoritative evidence.
- Unblock for a real retire (run_yogurt_003): a retailer scrape with **ingredient panels + Hebrew names** (OFF cannot supply these; same data gap as run_bread_retail_004). Until that source exists, no machine run can reconcile this category.

**No frontend dataset shipped** (contract: produce frontend output only if validation passes;
a run_yogurt_002 dataset would fail `--handoff` on §5/§2.4/§2.5). Live shelf validate-corpus: 0 errors.

Only the Central Controller records CLOSED.
