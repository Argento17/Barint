---
id: TASK-169B
title: P1 — promote recal behind BARI_RECAL_P0, rescore + reship CHEESE + HUMMUS only (frozen dairy deferred)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
summary: >
  P1 of TASK-169, owner green-lit (cheese+hummus first; frozen milk/yogurt/snack deferred to a later approved wave; yogurt top to be trimmed via R1 yogurt anchor in that wave). Author evidence-registry entries EV-029-032 (+EV-024/027 extensions); Product D7 co-sign; rescore cheese + hummus with BARI_RECAL_P0 ON (new run ids), rebuild ONLY their frontend JSON; do NOT regenerate milk/yogurt/snack/bread JSON (they stay on current scores until their wave). Then frontend integrate + Content fix stale insight lines + remove false 'מבנה רכיבים מעובד' labels (cottage now NOVA 2) + QA stale-data/build. Final owner confirm before live deploy. Flag OFF = byte-identical rollback.
---

# TASK-169B — P1 — promote recal behind BARI_RECAL_P0, rescore + reship CHEESE + HUMMUS only (frozen dairy deferred)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Progress note (Data Agent, 2026-06-02) — data half of P1 DONE; staged, not live; one blocker

**Done:**
1. **Evidence registry** — authored into the canonical store
   `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`:
   NEW **EV-030** (R1 category-relative protein), **EV-031** (R3 leanness),
   **EV-032** (R5 graded sat-fat), **EV-033** (R6 veg-spread fit); plus the
   **EV-027** (R2) and **EV-024/EV-026 lineage v1.1** (R4 NOVA flavored-variant +
   R7 culture gate) extensions. **ID-remap flagged:** design said EV-029..032 but
   EV-029 was already taken (BSIP0 fat-overwrite, TASK-142A) → shifted to EV-030..033.
2. **Rescored with `BARI_RECAL_P0=on`, new run ids** (published dirs untouched):
   - `run_cheese_004` (source = run_cheese_003 corpus) — A13/B17/C19/D4/E1, misroute 3.4%.
     Anchors match the v1.1 model exactly: cottage 1% **89.8/A**, cottage 9% **81.1/A**,
     white+garlic **84.3/A**, napoleon-16%-garlic-dill **74.5/B NOVA 3 (A-leak closed)**.
   - `run_hummus_003` (source = canonical_bsip1; run_hummus_002 is FROZEN → 003+) —
     display A7/B35/C16/D6; **R6 veg-spread fired on 17 items** (matbucha 60→71/B etc.).
   - Flag-OFF re-score == model OFF baseline 59/59 (rollback byte-identical); golden 0 FAIL,
     router 12/12, both OFF and ON.
3. **Staged frontend JSON (NOT live — page imports unchanged):**
   `bari-web/src/data/comparisons/cheese_frontend_v2.json` (52 disp) and
   `hummus_frontend_v4.json` (64 disp). v1/v3 (live) NOT repointed/rescored.
4. **Report artifacts:** `02_products/_recal_p0_model/TASK-169B_before_after_tables.json`
   (full cheese 51 + hummus 64 before/after) and `TASK-169B_run_records.json` (run ids,
   date, config hash 832fdb55e03cae06, artifact paths).

**Content/Frontend follow-up handed off (in the report):**
- 28 cheese + 28 hummus insight lines now STALE (explicit grade claims like cottage's
  "עוצר ב-B" now A; matbucha "נשאר ב-C" now B; position superlatives to re-verify).
- 5 live cottage products carry the false "מבנה רכיבים מעובד — תוספות מעבר לבסיס החלבי"
  limiting line and are now NOVA 2 → line must DROP.

**BLOCKER — escalate to Nutrition + Product + owner (governance conflict, not data):**
The run_003 cheese A-ceiling construct (EV-021 / RULING-DAIRY-A-01 C1–C6) sets
`a_eligible_pre_routing=False` for ALL cheese, so the package withholds all **13**
recalibrated grade-A products — including the flagship **cottage 1% (90/A)**. TASK-169
v1.1 (owner ruling) retires the hard grade cap and explicitly intends cottage to LAND at
90/A. These two owner-approved decisions conflict. `cheese_frontend_v2.json` STAGES the
recal A's (A-ceiling withhold NOT applied) for the owner look and records the conflict in
`_meta.recal_governance_conflict`. **Must reconcile EV-021 vs TASK-169 v1.1 before any
live repoint.**
