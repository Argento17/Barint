---
id: TASK-146
title: Decide whether the TASK-144 dairy scoring fixes should apply to the frozen yogurt + cheese categories
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "No structural work gated."
depends_on: [TASK-144]
blocks: []
category_id: null
work_type: decision
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "TASK-154 (PO-confirmed) AFFIRMS this (B) keep-maadanim-scoped ruling as the STANDING state, after the same engine-baseline difference surfaced live as a cross-page grade gap on 2 dual-shelf יופלה GO SKUs (70/B yog vs 78/B maad). Cross-category convergence is NOT pursued and is NOT a flag flip — it would need a NEW governed re-run with C1–C6 A-ceiling enforcement + Nutrition co-sign (NOTE: TASK-143 is CLOSED, so it is not the vehicle). Interim mitigation = TASK-155 UI disclosure. No reopen of this task."
summary: >
  TASK-144's 3 dairy fixes (OCR-count sanitize, fiber absent!=zero for dairy, dairy-protein source typing) are currently scoped to the maadanim run only (BARI_TASK144_FIXES default OFF). Applied cross-category they would shift frozen categories: yogurt +8 incl 3 B->A, cheese 6 (none reach A), milk 1. Frozen isolation was proven (yogurt_003 = 0 diff). These B->A's are architecturally consistent with the milk 85/A precedent but were NOT deployed. Decide (Product + Nutrition) whether to adopt the fixes for yogurt/cheese under governance (numbers-versioning re-run + baseline re-freeze + DEC-005 reconciliation) or keep them maadanim-scoped. Deferred by Product Owner 2026-06-01.
---

# TASK-146 — Decide whether the TASK-144 dairy scoring fixes should apply to the frozen yogurt + cheese categories

## RULING (2026-06-02, Product + Nutrition) — **(B) KEEP maadanim-scoped**

`BARI_TASK144_FIXES` stays **OFF for the frozen yogurt + cheese categories.** The three fixes are
correct and stay live for maadanim (engine 0.4.1). Frozen categories will inherit the *corrected
logic* through their own governed per-category re-runs (TASK-143 for yogurt, TASK-142/142A for
cheese) — **not** through a cross-category flag flip. This is a "not via this mechanism / not yet,"
not a rejection of the fixes.

### Why not ADOPT-now (three independent disqualifiers, any one is sufficient)

1. **Governance breach — the raw blast-radius A's violate RULING-DAIRY-A-01.**
   The cross-category numbers are *raw engine output that does not enforce the C1–C6 A-condition.*
   Of the 3 yogurt B→A's, two are **דנונה פרו 20/21 חלבון** (80.9/A, 81.4/A) — *protein-enriched
   matrices*, the exact archetype TASK-144 **denied A** for GO under **C4 (intact dairy matrix /
   reconstituted-or-enriched base excluded)**. Flipping the flag would *publish two A's the
   governing ruling forbids.* Only the third, **יוגורט עזים טבעי 3%** (66.7→85/A), a plain natural
   goat yogurt, is architecturally legitimate (milk goat 85/A precedent) — and it should be **earned**
   through the governed re-run with C1–C6 enforced, not granted by a flag on unverified inputs.

2. **Data-integrity blocker — the inputs are under a confirmed CRITICAL defect (TASK-142A).**
   142A confirmed the Shufersal BSIP0 parser captures the trans-fat row as TOTAL fat
   (`fat_g=0.5` on 62/116 cheese) + nutrition-panel bleed, and **explicitly names the yogurt scraper**
   as sharing the same `nutritionList`/`NUTR_LABEL_MAP`. `fat_quality` feeds the score, so the
   yogurt/cheese blast-radius deltas (incl. these B→A's) are computed on **possibly-corrupted fat
   values.** Adopting now risks baking corrupted scores into frozen shelves. TASK-143 is already
   RE-BLOCKED on 142A for exactly this reason.

3. **Wrong mechanism — frozen categories have a governed adoption path that does this correctly.**
   A flag flip skips numbers-versioning, baseline re-freeze, content/insight re-authoring, the
   comprehension test, and Product go-live. TASK-143 (yogurt: re-run → reconcile → retire DEC-005 →
   PO go-live) and TASK-142→142A (cheese: parser fix → run_cheese_003 → re-validate) are the
   *purpose-built* vehicles where the fat-parse fix, the TASK-144 dairy logic, C1–C6 A-enforcement,
   and a fresh baseline re-freeze all land **together and verified.** That is where these categories
   should pick up the corrected behavior.

### Consequences / sequencing
- **No DEC-005 reconciliation, no frozen baseline re-freeze, no cross-category re-run** is triggered
  by this ruling. DEC-005 retirement remains owned by TASK-143.
- The TASK-144 dairy *logic* (EV-026/027/028) is **pre-approved in principle** for frozen adoption,
  but only re-derived inside TASK-143 (yogurt) and TASK-142/142A (cheese), **sequenced AFTER 142A's
  blast-radius verdict** — the corrected fat values may move these numbers again.
- Flag state unchanged: `BARI_TASK144_FIXES` default OFF; maadanim opts in. **Rollback is a no-op**
  (this ruling preserves the status quo for frozen categories).

### Disposition
Decision delivered; board cleanup unblocked. Status **RETURNED** — **Central Controller to record
CLOSED.** No structural work gated by this task.

