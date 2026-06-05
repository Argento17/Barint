---
name: bsip2-run-cereals-002
description: run_cereals_002 — greenfield real Shufersal cereals full cycle (TASK-140); 4 governance constructs applied; NO-GO live on a router cereal-anchor gap (misroute 7.6%); fortification NOT endemic
metadata: 
  node_type: memory
  type: project
  originSessionId: d77b0840-b538-4903-8ea1-ff744d5b876d
---

run_cereals_002 executed 2026-06-01 (data-agent, TASK-140) via bari-category-factory, all 7 stages,
engine proto_v0/0.4.0 UNMODIFIED, real Shufersal scrape (reused run_yogurt_003 pattern). Supersedes the
stale synthetic run_cereals_001 (Yohananof, 2026-05-18, no BSIP0).

**Result:** 113 scraped → **92 displayable** (0 insufficient, 100% nutrition+ingredient coverage,
Hebrew 100%). Grades **A7/B10/C48/D25/E2**, median 58.3 (engine thresholds S90/A80/B65/C50/D35).

**The 4 cereals governance constructs (from [[cereals_gap_resolution_v1]]) were applied at BSIP1 as
label-observable CLASSIFICATION/DISCLOSURE layers — NOT score changes:**
1. Granola sub-pool (Rule 5 / Sec 2.9): 25/92 via 2-of-3 proxy (sugar≥15 / fat≥10 / processing).
2. Children's (Sec 2.8): 4 via recognized child-mascot brands (D1+D2 jointly); D1 visual + D3 serving
   NOT text-observable → conservative recall + single-indicator candidate flagging for CE review.
3. Whole-grain (Sec 5.2.1): 43 claims, **8 Marketing Divergence Findings** (first-grain-ingredient test).
4. Fortification (Sec 6.4 / DISTORTION-004): **27.2% — BELOW 50% endemic threshold. Endemic Distortion
   Protocol does NOT trigger. This CONTRADICTS the pre-data governance assumption that fortification is
   "the majority" in cereals** — the real Shufersal shelf is granola/oat/muesli-heavy, largely unfortified.

**Why NO-GO to launch (1 failing exit gate):** misroute **7.6% > 5%** (QA-CER-001). 7 real cereals route
to bread (spelt/`כוסמין` whole-grain matrix), whole_food_fat (nut-dense muesli/granola + honey Cheerios),
beverage (corn/rice rings). Router v2 has **no cereal anchor** — same CLASS as the run_yogurt_003 19%
misroute. **Fix is an engine/router change (out of scope for the data task);** recommended: carry a category
prior from the BSIP0 cereal-shelf query (mirrors yogurt router recommendation). Re-run = run_cereals_003.

**Secondary findings for Nutrition/Product:** (a) 4 NOVA-1 shaped baked-flake A's (`פתיתים אפויים …`)
look like a NOVA-proxy under-call — withheld pending review; the 2 plain-oat A's are legit (milk-precedent).
(b) **scoring.md grade table (A≥85) is stale vs engine constants.py (A≥80)** — cross-ref [[bsip2-run-yogurt-003]]
TASK-139A A-threshold flag; affects A-count reporting across ALL categories.

**Frontend package = NON-AUTHORITATIVE, NOT promoted** (81/92 display-approved; 7 misrouted + 4 NOVA-review
withheld). Artifacts: `02_products/breakfast_cereals/factory_run_002/` (7 stage JSONs) + findings
`reports/run_cereals_002_factory_findings.md`. Reproduce: `03_operations/bsip0/scrape/shufersal_cereals/`
(01_scrape → 02_build_bsip1 → `bsip2/proto_v0/src/batch_run_cereals_002.py` → 03_package_frontend).
TASK-140 = RETURNED (proposed). [[category_audit_cereals_v1]]
