# P136 Return — Hummus Sodium Stats n=60 Re-run
## TASK-278 Phase-12 | Data Agent | 2026-06-14

### Summary

Re-ran sodium distribution statistics on n=60 in-scope hummus products after excluding
9 out-of-scope items (4 eggplant_spread + 5 matbucha_pepper_spread) from the n=69 corpus.

All 60 in-scope products have valid sodium_mg from direct BSIP1 scrape panels.
OFF not used.

### Key Finding

Q3 (395mg), P80 (395mg), and P85 (395mg) all resolve to the same value.
|Q3 - median| = 5.00mg — exactly at the escalation boundary.

The distribution has a dense spike at 375-400mg (34 of 60 products = 57%).
Escalation to Nutrition Agent is required before finalizing the floor constant.

### Artifacts

- Stats methodology file: `C:\Bari\02_products\hummus\methodology\hummus_sodium_stats_n60_v1.md`
- Computation script: `C:\Bari\02_products\hummus\methodology\compute_sodium_stats.py`

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-12 hummus n=60 sodium stat re-run",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "n_total_corpus": 69,
  "n_excluded": 9,
  "n_excluded_breakdown": {"eggplant_spread": 4, "matbucha_pepper_spread": 5},
  "n_in_scope": 60,
  "n_with_sodium": 60,
  "n_missing_sodium": 0,
  "mean_mg": 342.85,
  "stdev_mg": 187.93,
  "min_mg": 6.0,
  "q1_mg": 352.00,
  "median_mg": 390.00,
  "q3_mg": 395.00,
  "iqr_mg": 43.00,
  "mad_mg": 10.00,
  "robust_scale_mg": 31.88,
  "p80_mg": 395.00,
  "p85_mg": 395.00,
  "max_mg": 864.0,
  "q3_minus_median_abs": 5.00,
  "escalation_flag": true,
  "escalation_reason": "Q3 within 5mg of median AND Q3=P80=P85=395mg (distribution spike collapses all upper percentiles to same value)",
  "floor_threshold_recommendation": "ESCALATE: Q3=P80=P85=395mg — Nutrition Agent must confirm 395mg as floor or select alternative signal. Q3 within 5mg of median triggers D7 escalation rule.",
  "off_used": false,
  "source": "BSIP1 canonical files, normalized_nutrition_per_100g.sodium_mg, direct scrape only",
  "script": "C:\\Bari\\02_products\\hummus\\methodology\\compute_sodium_stats.py",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\hummus\\methodology\\hummus_sodium_stats_n60_v1.md",
      "type": "distribution_stats_report"
    },
    {
      "path": "C:\\Bari\\02_products\\hummus\\methodology\\compute_sodium_stats.py",
      "type": "computation_script"
    },
    {
      "path": "C:\\Bari\\tasks\\returns\\P136_return.md",
      "type": "return_block"
    }
  ],
  "counts": {
    "total_corpus_denominator": 69,
    "excluded_denominator": "n_excluded=9 (4 eggplant_spread + 5 matbucha_pepper_spread)",
    "in_scope_denominator": "n_in_scope=60 (30 hummus_spread + 30 hummus_and_savory_dips)",
    "with_valid_sodium_denominator": "60/60 in-scope products have sodium_mg",
    "histogram_bucket_375_400": "34/60 products in 375-400mg bucket (57%)"
  },
  "commands_run": [
    {
      "cmd": "python C:\\Bari\\02_products\\hummus\\methodology\\compute_sodium_stats.py",
      "exit_code": 0,
      "note": "Minor UnicodeEncodeError on first run due to PowerShell console encoding; re-run with PYTHONIOENCODING=utf-8 succeeded, exit_code=0"
    }
  ],
  "not_done": [
    "Floor constant not set — awaiting Nutrition Agent confirmation of 395mg or alternative",
    "Score engine not touched (read-only stat run only)",
    "No published scores modified"
  ],
  "acceptance_test": "PASS: n_in_scope=60 confirmed (30+30); n_with_sodium=60/60; all stats derived from artifact; Q3=P80=P85=395mg verified from sorted value list; escalation flag correctly triggered (|Q3-median|=5mg); OFF=false",
  "propose": "RETURNED"
}
```
