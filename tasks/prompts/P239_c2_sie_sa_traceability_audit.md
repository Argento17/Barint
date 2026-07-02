# P239 / SIE S+A traceability audit (route: C2)

META (read first): Zero-inference extraction only. Do NOT judge grades or reason about correctness. Read the file, filter by the stated rule, output the table. Do not edit any file. End with the JSON block.

## Input
`C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v3.json` → top-level key `results` (a list). Each item has: `barcode`, `name_he`, `acquisition_method`, and `engine_output` (which contains `grade` and `score`).

## Task (pure filter — no interpretation)
1. Select every item where `engine_output.grade` is `"S"` or `"A"`.
2. For each selected item output a row: `barcode | grade | score | acquisition_method | name_he`.
3. Then a SEPARATE list: every selected item whose `acquisition_method == "name_derived"` (these are the audit flags — a top-grade product whose dose came from the product name, not a panel).
4. Report counts: total S+A, and how many are name_derived.

## Return (machine block at end)
```json
{"task_id":"P239","status":"RETURNED","agent":"c2-deepseek",
 "sa_total":<int>,"name_derived_in_sa":<int>,
 "name_derived_barcodes":["..."]}
```
