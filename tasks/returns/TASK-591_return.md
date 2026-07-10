# TASK-591 return

Proposed status: RETURNED.

Created `03_operations/reports/task591_fat_ev026_audit.md`. The audit scanned all
20 served comparison files (757 product records), found 22 total-fat hit records,
and replayed 15 persisted captured panels. The required barcode `5010029000061`
is `CONFIRMED_DISCREPANCY` at published 0.5 versus replayed 2.0.

Verify: `03_operations/reports/task591_fat_ev026_audit.md` — coverage table,
results table, and tripwire-1 scope note.

```json
{
  "task": "TASK-591",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/reports/task591_fat_ev026_audit.md", "action": "created", "sha256": "bddec4959882a362f0f0cb8804d3274b8232e83331bceae0b2b3ee3e2f72ee0e"}
  ],
  "counts": {
    "comparison_files_scanned": "20/20 matched bari-web/src/data/comparisons/*_frontend_v*.json",
    "product_records_scanned": "757/757 records in the 20 matched served comparison files",
    "published_total_fat_0_5_records": "22/757 product records; duplicate publication versions retained",
    "unique_barcodes_with_published_total_fat_0_5": "20/22 hit records; denominator = published-hit records",
    "classification_histogram": "CONFIRMED_DISCREPANCY=15, CONSISTENT=0, NO_EVIDENCE=7; denominator=22 published-hit records; most_common=CONFIRMED_DISCREPANCY(15)",
    "replayable_raw_panels": "15/22 published-hit records; denominator=published-hit records"
  },
  "commands_run": [
    {"cmd": "python recursive JSON traversal over bari-web/src/data/comparisons/*_frontend_v*.json", "exit_code": 0},
    {"cmd": "git grep -l -- <each hit barcode> -- 02_products 03_operations/bsip0", "exit_code": 0},
    {"cmd": "python replay of nutrition_raw_source.rows through parse_nutrition_rows plus parse_nutrition_numeric with canonical *_raw mapping", "exit_code": 0},
    {"cmd": "Get-FileHash -Algorithm SHA256 03_operations/reports/task591_fat_ev026_audit.md", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "PASS: barcode 5010029000061 appears as CONFIRMED_DISCREPANCY; published fat=0.5 and local captured-panel replay fat=2.0."
}
```
