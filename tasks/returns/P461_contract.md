# P461 Contract — TASK-449 brined candidate rebuild (joint-flag protocol, live-baseline)

**Worktree:** `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`)
**Status proposed:** RETURNED
**Scope:** Rebuild `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` under joint-flag protocol vs **worktree-live** baseline (`bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`). No engine/code changes.

## Step A — reproduction gate (PASS)

With `BARI_REDLABEL_CONTINUOUS_V1=on` + `BARI_FERMENT_MARKER_BRINED_FIX_V1=off`, rescore + swap-candidate from worktree-live reproduces published page exactly: **36/36 identical scores and grades, 0 diffs**.

## Step B — ON-ON candidate (PASS)

With both flags ON, candidate built via established method (live JSON + score/grade swap from ON-ON traces + competition rerank with stable live-order tiebreak). Movement vs **worktree-live** is ferment-fix-only, **downward-only** (24/24 score movers), and **3/3 sweep flips preserved** (7290108509106, 7290108509755, 369617 unchanged vs live).

## Movement table vs worktree-live (ON-ON candidate)

| barcode | old score/grade | new score/grade | direction |
|---------|-----------------|-----------------|-----------|
| 7290019635826 | 84.1/A | 76.1/B | down |
| 7296073641940 | 82.8/A | 74.8/B | down |
| 7290102397334 | 82.2/A | 74.2/B | down |
| 7290011499303 | 81.2/A | 73.2/B | down |
| 2133162 | 81.0/A | 73.0/B | down |
| 2133889 | 79.6/B | 71.6/B | down |
| 7296073641964 | 79.4/B | 71.4/B | down |
| 7290011499129 | 78.7/B | 70.7/B | down |
| 7290011499327 | 76.9/B | 68.9/B | down |
| 7290011499358 | 76.8/B | 68.8/B | down |
| 7290011499105 | 76.1/B | 68.1/B | down |
| 7290019790402 | 75.4/B | 67.4/B | down |
| 7290017065663 | 74.6/B | 66.6/B | down |
| 2107798 | 73.2/B | 65.2/B | down |
| 7296073641957 | 73.1/B | 65.1/B | down |
| 7296073641902 | 72.8/B | 64.8/C | down |
| 7290011499051 | 72.7/B | 64.7/C | down |
| 7290019790808 | 72.7/B | 64.7/C | down |
| 7290019790112 | 71.5/B | 63.5/C | down |
| 7290114314015 | 71.4/B | 63.4/C | down |
| 7290011499112 | 71.3/B | 63.3/C | down |
| 7290019635222 | 68.1/B | 60.1/C | down |
| 7290017065236 | 67.4/B | 59.4/C | down |
| 7290114312707 | 55.9/C | 47.9/D | down |

Non-movers (incl. sweep flips preserved): 7290108509106 A/80.3, 7290108509755 B/65.7, 369617 C/50.9, plus 9 unchanged products.

## Grade/score distributions (Rule 5, worktree-live vs ON-ON candidate)

| state | n | min | max | median | stdev | most_common | grade histogram |
|-------|---|-----|-----|--------|-------|-------------|-----------------|
| BEFORE (worktree-live) | 36 | 47.10 | 84.10 | 73.15 | 9.00 | 73 (×5) | A:8 B:21 C:6 D:1 |
| AFTER (ON-ON candidate) | 36 | 47.10 | 82.70 | 66.15 | 8.11 | 65 (×5) | A:3 B:18 C:13 D:2 |

AFTER score histogram (rounded int): `{47:1,48:1,51:1,58:1,59:1,60:1,63:2,64:4,65:5,66:1,67:3,68:1,69:2,71:2,72:1,73:2,74:2,75:1,76:1,80:1,83:2}`

## Marker census (ON-ON traces)

34/35 brined_food products with `CULTURED_CHEESE_NAME_MARKERS_HE` lose the +8 (`fermentation_bonus_applied=False`); 1 retains bonus for independent reason.

## run_gates.py on candidate (`--baseline` = worktree-live)

| Gate | Result | Notes |
|------|--------|-------|
| G1 SCHEMA | FAIL | Pre-existing live debt (comparisonContext, satFat, limitingFactors) |
| G2 COVERAGE | PASS | 36/36 fields |
| G3 SCOPE | FAIL | Pre-existing: 12 scored barcodes not in displayed 36, no _meta exclusions |
| G4 OFF | PASS | 0 |
| G5 GRADE-INTEGRITY | PASS | floor policy |
| G6 COPY-SAFETY | PASS | 0 violations |
| G7 PARITY | PASS | 36/36 count; 14 grade changes vs worktree-live |
| G8 DATA-SANITY | PASS | 0 violations |
| **Overall** | **FAIL** | Pre-existing G1/G3 debt carried from live baseline |

**Exit-code semantics:** `rescore_all.py` exits **0** when pipeline succeeds (score moves vs live expected in re-baseline mode; C10 milk delta diagnostic only, not hard-fail). `run_gates.py` exits **1** on candidate (pre-existing G1/G3 FAIL).

```json
{
  "task": "P461",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json", "action": "created", "sha256": "f17b572c006d13ed1707dc53fc22903d7a7e568dbf1a2ef4dfb1acd77650419c"},
    {"path": "_rescore_staging/brined_cheeses/verification_table.csv", "action": "created", "sha256": "8ad232deac17d02235bb68d697ec4a25e25deb04e4d7c9d8c5546cef9c4d344c"}
  ],
  "counts": {
    "reproduction_gate": "36/36 (Step A swap-candidate vs worktree-live brined_cheeses_frontend_v2.json; 0 score/grade diffs; median 73.15 stdev 9.00 most_common 73(x5))",
    "brined_score_moves_ON_ON": "24/36 (trace-derived vs worktree-live; BEFORE median 73.15 stdev 9.00 most_common 73(x5) → AFTER median 66.15 stdev 8.11 most_common 65(x5); all 24/24 downward)",
    "brined_grade_moves_ON_ON": "14/36 (trace-derived vs worktree-live; grade hist A:8/B:21/C:6/D:1 → A:3/B:18/C:13/D:2; stdev 9.00→8.11)",
    "sweep_flips_preserved": "3/3 (worktree-live barcodes 7290108509106, 7290108509755, 369617 unchanged in candidate vs live)",
    "pinned_corpus_barcode_parity": "36/36 (worktree-live brined_cheeses_frontend_v2.json barcodes == candidate; 0 added 0 dropped)",
    "brined_products_with_marker_losing_plus8": "34/35 (ON-ON staging traces + CULTURED_CHEESE_NAME_MARKERS_HE; 1 marker product retained bonus for independent reason)",
    "grade_flips_listed_in_G7": "14/36 (run_gates.py G7 parity candidate vs worktree-live baseline; overlaps brined_grade_moves 14/36; AFTER dist median 66.15 stdev 8.11 most_common 65(x5))"
  },
  "commands_run": [
    {"cmd": "powershell -File _p461_step_a.ps1", "exit_code": 0},
    {"cmd": "python -c \"import json;from pathlib import Path;R=Path('.');live={str(p['barcode']):p for p in json.loads((R/'bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json').read_text(encoding='utf-8'))['products']};cand={str(p['barcode']):p for p in json.loads((R/'_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json').read_text(encoding='utf-8'))['products']};diffs=[bc for bc in live if live[bc]['score']!=cand[bc]['score'] or live[bc]['grade']!=cand[bc]['grade']];assert len(diffs)==0 and len(live)==36\"", "exit_code": 0},
    {"cmd": "powershell -File _p461_step_b.ps1", "exit_code": 0},
    {"cmd": "python _p461_build_and_verify.py step_b", "exit_code": 0},
    {"cmd": "powershell -File _p461_census.ps1", "exit_code": 0},
    {"cmd": "powershell -File _p461_derive_counts.ps1", "exit_code": 0},
    {"cmd": "powershell -File _p461_gates.ps1", "exit_code": 1},
    {"cmd": "python 03_operations/validators/validate_return.py --md tasks/returns/P461_contract.md --root C:\\bari_wt_t449", "exit_code": 0},
    {"cmd": "git commit -m \"P461: brined candidate rebuilt under joint-flag protocol vs live baseline\"", "exit_code": 0}
  ],
  "not_done": [
    "owner/Content/Adversarial-QA two-gate sign-off + PR/deploy (out of P461 boundaries)",
    "G1/G3 schema/scope debt fix (pre-existing live baseline; not in P461 scope)"
  ],
  "self_check": "Step A reproduction gate 36/36 identical (0 diffs) AND Step B candidate preserves 3/3 sweep flips vs worktree-live; validate_return.py --md tasks/returns/P461_contract.md exits 0"
}
```

**Proposed RETURNED.** Orchestrator: verify sha256 at each artifact path, rerun deriving commands in `commands_run`, confirm sweep-flip preservation and worktree-live baseline usage.