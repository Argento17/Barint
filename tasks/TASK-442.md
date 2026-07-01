---
id: TASK-442
title: IL red-label thresholds stale vs current MoH (2021 Phase-2) — align + fix copy provenance
owner: nutrition-agent
status: BLOCKED
blocker: owner go/no-go on de-anchor direction — resume TASK-395 (BARI_REDLABEL_V1) staged activation + hold TASK-442 tighter-thresholds + ship Track B copy fix (tripwire #1)
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  FOPL verify (2026-07-01) found RED_LABEL_THRESHOLDS (sugar17.5/sat5.0/sodium600) mislabeled as MoH and stale vs current Phase-2 (10/4/400 solid; 5/3/300 per-100ml beverage). Track A: co-sign corrected values behind dormant flag + quantify score movement (regulatory_quality dimension) -> owner tripwire-1 go/no-go. Track B: fix consumer copy that attributes stale numbers to MoH. No scores/copy changed yet.
---

# TASK-442 — IL red-label thresholds stale vs current MoH (2021 Phase-2) — align + fix copy provenance

## HANDOFF STATE (2026-07-01) — for a fresh chat continuing this

### One-paragraph what-this-is
Bari's `RED_LABEL_THRESHOLDS` (sugar 17.5 / sat_fat 5.0 / sodium 600, per-100g, flat, no beverage set) are labeled in code as "Israeli red label thresholds (Ministry of Health, solids)" but are **stale + mislabeled** — they match no MoH phase. Current MoH Phase-2 (Jan 2021) = solid **10/4/400** per-100g, beverage **5/3/300** per-100ml. These feed the `regulatory_quality` scoring dimension (5% weight), so correcting them **moves published scores = owner tripwire-1**. Two tracks: **A** = align thresholds (quantify + co-sign → owner go/no-go); **B** = fix consumer copy that attributes the stale numbers to MoH.

### DONE (all verified by orchestrator)
- **FOPL verify** (nutrition-agent): found the drift; confirmed at `constants.py:68-72` + consumer copy at `bari-web/src/components/shared/comparison-metric-column.tsx:214,237,241,260`.
- **Track A-1 (Nutrition, co-sign + build):** corrected MoH values co-signed vs 2 gov.il/efsharibari primary fetches (confidence Moderate-Strong; no post-2021 red-label revision found — green-label committee rounds only). **Provenance ruling: 17.5/5/600 was NEVER a legit MoH mirror — a Bari anchor mislabeled as an MoH citation.** Beverage scope = `category=="beverage"` OR (`dairy_protein` AND fluid-milk name-marker). **EV-108** authored. Corrected thresholds built behind **dormant flag `BARI_MOH_REDLABEL_2021_V1`** (env var, default OFF, `>=` comparator). Score-neutral proven byte-identical off: **0/96 mismatches** (juices 28 + hard_cheeses 68).
- **Track A-2 (Data, quantify what-if):** isolated worktree `C:\bari_task442` off the branch. Valid method = **flag ON vs OFF on identical corpus** (NOT vs committed baseline — it's separately stale). **644 products / 14 live cats: 97 move, 27 grade flips, ALL downward.** Flips: cheese 4 (→D, one −29pts), granola 4 (→D, mean −11.7), juices 4 (3× natural 100% juice **A→C** + 1 D→E), snacks 9, cookies_coffee 3, cakes 1, chocolate_tablets 1 (Lindt78 C→D), hummus 1; **milk 0** (beverage scope fires, 2 new sugar labels, 5% weight insufficient to cross grade); bread/brined/hard_cheeses/choc_bars 0.
- **Track A-3 (Product, co-sign):** **CO-SIGNED activation.** All flips defensible (correction only tightens; old anchor too loose = a mislabeled-citation bug, not a philosophy change). **Natural-juice A→C ships as-is** (Bari runs no intrinsic-vs-added sugar carve-out anywhere; MoH really red-labels 100% juice >5g/100ml). Sequencing: **per-category rollout, zero-flip cats first** (fiber-gate/TASK-432 precedent), isolate cheese −29 + juice each in own two-gate. Non-blocking follow-up: Nutrition to consider a juice category-caveat box.

### ARTIFACTS / WHERE THINGS LIVE
- **Branch `task442/moh-redlabel-2021` (commit d79c01c8), NOT on master** — carries the 5 dormant-flag files: `constants.py`, `score_engine.py`, `signal_extractor.py` (comment-only), `method_counterfactual.py` (comment-only), `bsip2_evidence_registry_v1.md` (EV-108).
- **Worktree `C:\bari_task442`** — what-if report at `_task442_report/FINAL_MOVEMENT_TABLE.json` (+ grade_flips_readable.txt). Remove with `git worktree remove C:\bari_task442 --force` when done.
- Main tree `C:\Bari` on master is UNTOUCHED by the flag (verified 0 tracked changes).

### THE PENDING DECISION (owner, tripwire-1)
Orchestrator recommendation presented to owner: **ACTIVATE, per-category rollout, zero-flip categories first**; each grade-moving category through the normal two-gate + owner go-live. **Awaiting owner go/no-go.** On "go": begin zero-change batch to prove the flag mechanically, then bring each grade-moving category one at a time.

### NEXT STEPS (once owner says go)
1. Per-category activation: register the flag in the affected-set / rollout path; start zero-flip batch (milk, bread, cereals, brined_cheeses, hard_cheeses, chocolate_bars).
2. Each grade-moving category (cheese incl. the −29 product, granola, juices, snacks, cookies_coffee, cakes, chocolate_tablets, hummus): re-score → **Track B copy fix** (correct the MoH-attribution in `comparison-metric-column.tsx`) → two-gate copy → Adversarial QA → owner go-live.
3. **Activation coordination note (EV-108 ↔ EV-049):** BARI_SODIUM_CEREAL independently appends sodium red labels at `>=600`; never validated jointly with EV-108 — re-verify the interaction before activating both (relevant to cereal/granola).

### SEPARATE DISCOVERY (log, do not conflate with TASK-442)
Flag-OFF full run does NOT reproduce the committed published baseline on **8/15 shelves** — pre-existing corpus-identity drift (hard_cheeses 12/27 barcode overlap; snacks baseline 21 vs corpus 51; chocolate_tablets 35 vs 94). Verified flag-independent (reproduces on master tip). Ties to corpus_traceability_program / local_origin_brain_divergence. Owner told; plan owed separately. protein_bars is harness-incompatible (bsip1_dir=null).

<!-- Live orchestrator view: tasks/DISPATCH_BOARD.md → TASK-442 block. -->

<!-- opened with new_task.py -->



## NUTRITION STRATEGIC RULING (2026-07-01, orchestrator-VERIFIED) — owner directive "drift away from red-label"
Consulted Nutrition per owner. **Key finding: the de-anchor mechanism the owner wants ALREADY EXISTS + is built + flag-gated + Product-co-signed** — `BARI_REDLABEL_V1` (score_engine.py:245, default off; continuous per-label severity deduction replaces the 95/60/25 step + binary caps) + **TASK-395 de-chain program**, which is ALREADY at the owner tripwire (activation_eval: SPLIT GO-10/NO-GO-2, verified). This is activation-sequencing, not new design.

**Ruling on TASK-442 (this task): (b) DO NOT activate the tighter MoH thresholds now.** They feed the very binary mechanism about to be de-anchored → 27 downward flips would be churn that de-anchoring partly reverses. `BARI_MOH_REDLABEL_2021_V1` is orthogonal/additive to the caps (verified). Re-measure the 27-flip number AFTER de-anchor (Stage 5); the legacy binary measurement won't reproduce. TASK-442 Track A -> PARKED behind TASK-395.
**Track B (copy honesty fix): SHIP NOW, independent** — stop attributing 17.5/5/600 to MoH (they never were MoH). comparison-metric-column.tsx:214/237/241/260. Two-gate copy.
**Prerequisites flagged:** (1) BARI-INVERSION-TEST-001 not canonically landed (I have a reframed panel-dominance version on branch p277) — the real blocker on further de-chain staging; (2) EV-108↔EV-049 joint check before cereal/granola.
**Caveat:** red-label de-anchor does NOT fix the Chokita/Petit-Beurre NOVA inversion (separate chain = Stage 2 NOVA-replacement).
**Status -> BLOCKED on owner go/no-go: (i) resume TASK-395 staged de-anchor activation? (ii) hold TASK-442 Track A + ship Track B?** Tripwire #1.
