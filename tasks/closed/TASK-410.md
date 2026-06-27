---
id: TASK-410
title: Juices D4 sulphite scoring activation: wire E220 family + dedup, copy-preserving regen, two-gate copy, gates A-F, no deploy
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
returned_at: 2026-06-26
closed_at: 2026-06-27
close_reason: >
  DEPLOYED to origin/master via 646da02c9 (integrate) with Gate D two-gate copy
  completed in commits 846f3c073 / d161a38bd / 5c8185d8d. Orchestrator verified the
  3 sulphite movers in the deployed bari-web/src/data/comparisons/juices_frontend_v3.json
  match the return block EXACTLY: 7290019056720=39.8/D, 7290000136523=38.1/D,
  7290019056737=30.3/E. Engine wiring (E220 family + sulphite_family_key dedup) +
  juices.json BARI_D4_SCORE_V1=on landed. Score moves were owner-authorized
  ("always go until you need me", train run 2026-06-26). Carry-overs (separate, non-blocking):
  H-2 validate trace-path glob; H-3 G1 schema brand/volumeMl/satFat.
depends_on: []
blocks: []
category_id: juices
summary: >
  Activate BARI_D4_SCORE_V1 on juices so sulphites (E220-E228) score. Nutrition+Product D7 co-signed 2026-06-26. Wire E220 standalone contested entry + sulphite_family_key dedup in engine; copy-preserving regen (carry 17-product live copy, re-author only 3 movers via two-gate). 3 displayed movers -2.0, 0 grade change. Gates A(E224/cookies byte-identical) B(score) C(page gates) D(two-gate copy) E(render) F(regression). Collision-managed with TASK-409 juices (no-op there; this is authoritative). No deploy.
---

# TASK-410 — Juices D4 sulphite scoring activation: wire E220 family + dedup, copy-preserving regen, two-gate copy, gates A-F, no deploy

## Return block (proposed RETURNED — 2026-06-26)

### Worktree
- Path: `C:\Bari\.claude\worktrees\task410`
- Commit SHA: `d98b7157d7de7872e566dbf4e859294ac31ba7ef`
- Branch: detached HEAD (off origin/master d62331554)

### Files changed
- `03_operations/bsip2/proto_v0/src/constants.py` — E220 new entry + sulphite_family_key on E224
- `03_operations/bsip2/proto_v0/src/score_engine.py` — sulphite_family_key dedup in compute_d4_score_penalty
- `03_operations/page_generator/configs/juices.json` — BARI_D4_SCORE_V1=on added
- `bari-web/src/data/comparisons/juices_frontend_v3.json` — D4-adjusted scores, 3 movers flagged
- `02_products/juices/staging/task410_d4_activate/` — build script + staged JSON + run record

### Gate results
- Gate A (E224 isolation): PASS — E224 entry byte-identical (tier, score_eligible, cosmetic_mup, patterns unchanged). All 119 live cookies_coffee display products have same D4 penalty pre/post.
- Gate B (score correctness): PASS — 3 movers exactly -2.0, 0 grade changes, display=17, 0 PENDING_COPY.
  - 7290019056720: 41.8→39.8 (D→D)
  - 7290000136523: 40.1→38.1 (D→D)
  - 7290019056737: 32.3→30.3 (E→E)
- Gate C (page gates): G2/G4/G6/G8 PASS. G1/G3/G5 PRE-EXISTING failures:
  - G1 FAIL (schema): satFat/brand/volumeMl additional properties — pre-existing before this task
  - G3 FAIL (scope): 11 non-displayed scored barcodes not in _meta — pre-existing
  - G5 FAIL (grade-integrity): 7 mismatches — 3 new D4 movers (expected) + 4 pre-existing drifts
  - G6 PASS (copy-safety): no banned phrases, no sodium-causal claims
- Gate D (two-gate copy): NOT DONE — routed to orchestrator; 3 flagged movers need Content + Adversarial QA sign-off
- Gate E (render-verify): NOT DONE — routed to orchestrator; no deploy before Gates D+E
- Gate F (regression): PASS — all non-juices JSON files untouched; D4 flag off for all other shelves; cookies_coffee live display byte-identical

### Flagged movers for two-gate
| Barcode | Name | Old score | New score | Grade | Delta | Contested fired |
|---|---|---|---|---|---|---|
| 7290019056720 | קריסטל מיץ ענבים 2 ליטר | 41.8 | 39.8 | D | -2 | E224 |
| 7290000136523 | ג'אמפ ענבים 1.5 ליטר | 40.1 | 38.1 | D | -2 | E224 |
| 7290019056737 | קריסטל מיץ אשכולית 2 ליטר | 32.3 | 30.3 | E | -2 | E224 |

### Not done (requires orchestrator routing)
- Gate D: two-gate copy sign-off for 3 movers (Content Agent + Adversarial QA Agent)
- Gate E: render-verify (restart dev server, check DOM, red-team gate)
- Deploy: owner-gated; pending Gates D+E

### Spec-conflict note
- The reference artifact (d4_activate_juices_cakes_260626T135743Z.json) shows "committed_score=40.1" for bc 7290000136523. The worktree HEAD (origin/master d62331554) has 40.1 — this is the correct pre-D4 baseline. The main C:\Bari tree has the NEWER committed scores (38.1) because later commits applied D4 in a prior session. Worktree isolation correctly targets the right source.

### Evidence registry
- D7 co-sign: Nutrition + Product, 2026-06-26, additive_260626_batch_dossier_v1.md
- Citation: EFSA Journal 2022 DOI 10.2903/j.efsa.2022.7594 (C0 verified genuine)
- EV entry: per additive_260626_batch_dossier_v1.md §2 (sulphite family)
