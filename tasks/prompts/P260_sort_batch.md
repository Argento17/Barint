# P260 / Sort-conformity batch — reorder 7 out-of-order comparison JSONs by score (route: C2)

Repo C:\Bari. TASK-421. DETERMINISTIC, ZERO-INFERENCE task. STAGING ONLY — no commit/push/deploy. Touch ONLY the 7 files listed. No score/grade/copy/field changes — ONLY array order + the `rank` integer.

## Why
The comparison table (`bari-web/src/components/shared/comparison-table.tsx`) has NO sort logic — it renders `products[]` in array order and inserts band dividers on score-band change. 7 live category JSONs have their `products` array out of score order, so rows and band dividers render wrong. Fix = sort each array by `score` DESCENDING and re-number `rank` 1..N. (cereals already fixed; cookies_coffee handled by a separate lane — do NOT touch it.)

## Do exactly this
Write a script `bari-web/_sort_frontend.py` that, for each target file: loads JSON, sorts `products` by `score` descending (stable; ties keep existing relative order), rewrites the `rank` field of each product to its new 1-based position, writes the file back with the SAME formatting/encoding (UTF-8, indent=2, ensure_ascii=false) and ALL other fields byte-identical. Then run it over exactly these 7 files:
- bari-web/src/data/comparisons/bread_frontend_v3.json
- bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
- bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json
- bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json
- bari-web/src/data/comparisons/granola_frontend_v2.json
- bari-web/src/data/comparisons/juices_frontend_v3.json
- bari-web/src/data/comparisons/snacks_frontend_v5.json

## Verify + report (per file)
For each file print: N products, and confirm the score sequence is monotonically non-increasing after sorting, and that the set of products (by id/barcode) is UNCHANGED (same members, only reordered) and no field other than `rank` changed value. Report the before/after position of any product that moved.

End with the machine-readable return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED.
