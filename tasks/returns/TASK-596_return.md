# TASK-596 Return — cereals published-fat correction (EV-026 residue)

## Summary
Phase 1 complete (proposed RETURNED, consumer-facing → owner merge). Corrected the 15
CONFIRMED_DISCREPANCY `expansion.nutrition.fat` values in `cereals_frontend_v2.json` from the
in-repo raw-panel replay (TASK-591), independently re-verified (0/15 mismatch). Only that field
changed. satFat, scores, grades, ranks, and all copy untouched.

Phase 2 diagnosis (STOP, no score moved): bsip2 traces already scored on the CORRECT fat
(`L1_observed_signals.fat_g` = replay value, not 0.5), so re-scoring on corrected fat = Δ0 for
all 15. Not a tripwire-1 escalation — nothing to re-score.

## Corrected fat distribution (15 products, g/100g)
- values (sorted): 2.0, 2.3, 2.9, 3.5, 3.7, 4.0, 4.7, 5.4, 6.0, 6.0, 6.2, 7.4, 9.4, 10.8, 13.6
- min 2.0 · max 13.6 · median 5.4 · mean 5.86 · stdev 3.11 · most-common 6.0 (count 2)
- all 15 previously published as 0.5; 0 remain at 0.5 post-fix (served DOM + JSON)

## Verification
- Independent replay (`parse_nutrition_rows` + `parse_value_bound` on `nutrition_raw_source.rows`)
  == TASK-591 report: 0/15 mismatch.
- Published satFat == replayed satFat for all 15 (no satFat change needed); new fat ≥ satFat for all 15.
- No fat-claim copy (שומן/"lean") on any affected row → no contradiction to flag.
- Both page gates: byte-identical output vs pristine baseline (only pre-existing TASK-563 G3/G5
  fails; G8 DATA-SANITY still PASS → no sat>fat introduced).
- `npx tsc --noEmit` exit 0; `npm run build` exit 0.
- Render-verify (real DOM, prod server): 20 fat fields, 0 == 0.5, all 15 corrected values present.
- Display surface note: cereals pages do not render nutrition.fat (grid shows
  protein/sugar/energy/sodium; only brined-cheeses viz reads fat) — this corrects the DATA record.

## C0 sha note (merge-pending)
The artifact lives on pushed branch `task596-cereals-fat-fix` (commit `f872fd88`), built off
`origin/master` (LIVE baseline `b943d18…`). The declared sha `0855d6…` is the branch/PR file state
(verified `sha256sum` in `C:/bari_wt_596`). `validate_return.py` run from `C:/Bari` re-hashes the
LOCAL main copy (`67045db…`, itself divergent from LIVE per the known local↔origin split) and will
report C2 sha MISMATCH until the PR is merged — expected for a consumer-facing owner-merge return, not
a defect. C0 sha will match once merged to origin/master. All other C0 checks (C1/C3/C4/C5/C6/C7) PASS.

```json
{
  "task": "TASK-596",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/data/comparisons/cereals_frontend_v2.json", "action": "modified",
     "sha256": "0855d62670fac73058edf7345ddb73f4346006141da900cd683db11b88d3832b"}
  ],
  "counts": {
    "fat_values_corrected: 15/15 (TASK-591 CONFIRMED_DISCREPANCY set, cereals_frontend_v2.json)": "15/15",
    "replay_vs_report_mismatch: 0/15 (independent parse_nutrition_rows replay vs task591 report)": "0/15",
    "fat_eq_0.5_remaining: 0/20 (expansion.nutrition.fat in served cereals_frontend_v2.json)": "0/20",
    "satFat_unchanged_matches_replay: 15/15 (published satFat == replayed satFat)": "15/15",
    "scoring_inputs_using_bugged_fat: 0/15 (bsip2_trace L1_observed_signals.fat_g == replay, run_cereals_008)": "0/15",
    "expected_score_movement: 0/15 (Delta=0; scores already computed on correct fat)": "0/15",
    "corrected_fat_dist_gper100g: min2.0 max13.6 median5.4 mean5.86 stdev3.11 mostcommon6.0(count2)": "15/15",
    "page_gate_diff_vs_baseline: 0 new failures (run_gates + validate_comparison_page output identical, TASK-563 G3/G5 pre-existing)": "0/0"
  },
  "commands_run": [
    {"cmd": "python scratchpad/replay_fat.py (parse_nutrition_rows/parse_value_bound replay vs TASK-591)", "exit_code": 0},
    {"cmd": "python scratchpad/check_copy_satfat.py (satFat + fat-claim copy scan)", "exit_code": 0},
    {"cmd": "python scratchpad/patch_fat.py (surgical 15-line fat patch)", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py cereals_frontend_v2.json --run <run_cereals_008/products> --corpus <run_cereals_008/output> --config configs/cereals.json (baseline vs patched: identical)", "exit_code": 1},
    {"cmd": "python 03_operations/spine/validate_comparison_page.py --json cereals_frontend_v2.json --traces <run_cereals_008/products> (baseline vs patched: identical)", "exit_code": 1},
    {"cmd": "npx tsc --noEmit", "exit_code": 0},
    {"cmd": "npm run build", "exit_code": 0},
    {"cmd": "python scratchpad/render_verify.py (served DOM fat-value read on localhost:3411)", "exit_code": 0},
    {"cmd": "python scratchpad/phase2_score_impact.py (bsip2 trace fat-input diagnosis)", "exit_code": 0}
  ],
  "not_done": [
    "Owner merge of PR https://github.com/Argento17/Barint/pull/new/task596-cereals-fat-fix (consumer-facing → owner-gated by policy)",
    "Non-cereal shelves: 7 NO_EVIDENCE fat==0.5 hits (bread/yogurt) left untouched per missing-panel rule; corpus-wide other-field corrections await TASK-595 damage-scan report (not yet landed, owned by another session)"
  ],
  "self_check": "Acceptance: re-run TASK-591 detection post-fix expects 0 remaining CONFIRMED_DISCREPANCY. Observed: fat==0.5 count in served cereals_frontend_v2.json = 0/20; all 15 corrected values render in the prod DOM payload; both page gates byte-identical to baseline (no new failures). PASS."
}
```
