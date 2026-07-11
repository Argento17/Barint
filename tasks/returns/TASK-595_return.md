# TASK-595 return

RETURNED — read-only nutrition damage scan completed.

Changed files:

- `03_operations/reports/task595_nutrition_damage_scan.md` — evidence-replay method, per-shelf results, material and field-gap appendices; verify the cereal anchors and sodium replay behavior.
- `tasks/returns/TASK-595_return.md` — return record.

```json
{
  "task": "TASK-595",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/task595_nutrition_damage_scan.md",
      "action": "created",
      "sha256": "a655db708aeb35cfd3dc037ca75062a09f30ca83644033644e25471155b5a59f"
    }
  ],
  "counts": {
    "published_products": "757/757 (all versioned frontend shelf records)",
    "with_evidence": "359/757 (barcode matched selected raw panels)",
    "no_evidence": "398/757 (all versioned frontend shelf records)",
    "fully_match": "320/359 (evidence-backed products)",
    "rounding_only": "0/359 (evidence-backed products)",
    "material_products": "39/359 (evidence-backed products)",
    "material_fields": "39/39 (MATERIAL field-diff appendix)",
    "field_gaps": "5/44 (all appendix entries: 39 MATERIAL plus 5 FIELD_GAP)",
    "distribution_marker": "product disposition histogram: FULLY_MATCH=320, ROUNDING_ONLY=0, MATERIAL_PRODUCT=39; most_common=FULLY_MATCH(320) / 359 evidence-backed products",
    "cereal_fat_material_anchor": "15/20 (cereals_frontend_v2 products; required anchor signature)"
  },
  "commands_run": [
    {
      "cmd": "PYTHONDONTWRITEBYTECODE=1 python - (boundary-enforced TASK-595 scanner)",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Passed replay anchors 5010029000061 fat 0.5→2.0 and 7296073705574 fat 0.5→13.6; cereal fat MATERIAL=15; evidence-rich MATCH-majority assertion passed."
}
```
