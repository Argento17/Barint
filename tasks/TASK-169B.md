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

**BLOCKER RESOLVED (2026-06-02) — EV-021 AMENDMENT A1 applied to staged cheese JSON:**
The governance conflict (blanket cheese A-ceiling vs TASK-169 v1.1's intended cottage
1% @ ~90/A) is RESOLVED via owner-approved **EV-021 AMENDMENT A1**. The blanket
`a_eligible_pre_routing=False` cheese cap is retired and replaced by a **conditional
A-eligibility gate** (cheese-scoped, gated by `BARI_RECAL_P0`):
`a_eligible = sodium_mg <= 400 AND fat_saturated_g <= 4.0` (both required; missing data
fails closed). Fields = `L1_observed_signals.sodium_mg` / `.fat_saturated_g` (carried as
`nutrition.*`, verified identical to traces).

Mechanism is a **CAP, not a withhold**: a product that earns an A/S-band score but fails
the gate keeps its numeric score and stays visible on the shelf, displaying grade **B**.
Misroute + insufficient + transparency withholds unchanged. Flag OFF → unchanged.

`build_cheese_frontend_v2.py` updated and re-run with `BARI_RECAL_P0=on`. Verdict
reproduces Nutrition's exactly:
- **52 displayed products** — grade distribution **A 11 / B 19 / C 18 / D 3 / E 1**
  (B rose 17→19 by absorbing the 2 caps).
- **11 keep A**, led by **cottage 1% `che-7290014758681` = 90/A** (Na 350, sat-fat 0.6).
- **Exactly 2 capped A→B:** `che-4127336` קוטג' 9% שומן and `che-41452` קוטג' מהדרין 9% שומן —
  both **81/B**, sat-fat **5.4 > 4.0** (over the line). No A candidate fails on sodium.
- Builder flag-gated: OFF rebuild reproduces the prior staged 13-A behavior (gate
  inert); ON applies the cap. Full-pipeline flag-OFF re-score == model-OFF baseline
  59/59 unchanged (score layer; this change is display-only).
- `_meta.recal_governance_conflict` replaced with `_meta.recal_governance_note`
  (status RESOLVED, references EV-021 Amendment A1). Capped products also enumerated in
  `_meta.provenance.a_eligibility_gate.capped_products`.

**Content handoff:** the 2 capped rows must be phrased as "B because saturated fat over
the line" (9% milkfat cottage tier, sat-fat 5.4 g vs the 4.0 g cleanliness cut). All
other A's are earned A's.

Still **STAGED** — page imports unchanged (still `cheese_frontend_v1.json`). Product
Agent D7 co-sign required before live repoint.
