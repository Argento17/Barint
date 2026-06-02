---
id: TASK-129D
title: Hummus confidence label hardening
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: [TASK-129]
blocks: [TASK-128D]
category_id: null
summary: >
  Implement P0 #1 (confidence-gate hardening) for Hummus per confidence_reaudit_launch_v1.md.
  Finding: 0 displayed hummus rows are over-verified — the TASK-087 exclusion list already
  removed every ingredient-quality-gate failure. 5 genuine failures (all excluded NOVA-1 rows)
  relabeled verified->partial for corpus consistency; displayed distribution unchanged. No score
  movement. Recommendation: GO for HUMMUS_V2_SLICE activation (confidence-label dimension).
---

# TASK-129D — Hummus confidence label hardening

## Scope (as assigned, nutrition-agent)
Implement the re-audit §3 **P0 #1** confidence-gate correction for Hummus. Constraints honored:
**no score/grade change · confidence labels only · `run_hummus_002` frozen.**

## Method
Added a deterministic, idempotent ingredient-quality detector as the final confidence pass over
the displayed corpus: a row stays `verified` only if its ingredients read as a genuine list
(named additive class or structured comma/parenthetical/percentage markers); nutrition-panel OCR
dumps and bare allergen lines fail → `partial`. Display-label only.

## Key finding
The re-audit's "~15 marketing-prose verified" was counted against its 66-row **file** view, which
predates the hummus route's page-level exclusions (TASK-087) and was inflated by substring false
positives (`טרי` in `ציטרית`; `עשיר ב` echoing product names). On the **displayed** shelf
(37 rows; 35 `verified`): **0 fail** the ingredient-quality gate and **0 fail** the ≥3/6 nutrition
half — every displayed `verified` row is legitimately verified. The 5 genuine gate-failures are
**all already excluded from display** (NOVA-1 single-ingredient chickpeas).

## Deliverable results
- **Products relabeled:** 5 (`verified → partial`) — bsip1_7296073733324, _7296073733331,
  _7296073005889, _7296073006015, _3643820. All in the excluded set → **0 consumer-facing change.**
- **Before/after confidence (file):** verified 58→53 · partial 6→11 · insufficient 2→2.
- **Before/after confidence (displayed 37):** verified 35→35 · partial 2→2 (unchanged).
- **Score impact:** none — asserted `before_scores == after_scores`; git diff shows only
  `"confidence"` keys moved (10 lines); `_meta.score_statistics` unchanged; `run_hummus_002` frozen.
- **GO / NO-GO for HUMMUS_V2_SLICE:** **GO** (confidence-label dimension). The TASK-128D activation
  blocker (confidence promotion amplifying over-verified rows) does not materialize — 0 displayed
  rows are over-verified. Remaining non-blocking items are QA mobile+`lg` re-baseline (QA-owned)
  and P1 #5 fat re-run (post-launch, internal-confidence not display-label).

## Files
- NEW `02_products/hummus/frontend/harden_hummus_confidence_v1.py` — detector + idempotent pass;
  must run AFTER `build_hummus_explanation_v1.py` (authoritative final confidence pass).
- `bari-web/src/data/comparisons/hummus_frontend_v3.json` (+ workspace mirror) — 5 confidence
  relabels + refreshed `_meta.confidence_distribution` + `_meta.confidence_hardening` provenance.
- NEW `03_operations/bsip2/hummus_confidence_hardening_129d.md` — full report.

## Proposed next state
**RETURNED** — P0 #1 implemented + verified for Hummus; activation recommendation GO. Only the
Central Controller records CLOSED and decides the `HUMMUS_V2_SLICE` flip (with QA re-baseline).
