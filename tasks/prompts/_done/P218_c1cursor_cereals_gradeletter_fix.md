# P218 — TASK-330 cereals grade-letter copy error (route: C1-CURSOR)
# Data Agent build — single precise copy correction, no score move

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-330.md`
**ONLY file you may edit:** `bari-web/src/data/comparisons/cereals_frontend_v2.json`

## Problem (genuine copy error, verified)
Product barcode **7290107647854** carries a **standalone Hebrew grade letter `ג` (= grade C)** in its `rowVerdict`,
but the product's actual badge grade is **D** (score 49.7). G6 flags:
`standalone Hebrew grade letter 'ג' (maps to C) ≠ badge grade D near: ...'רם חלבון. ג; מוצר מעובד ב'...`

## Fix
In `cereals_frontend_v2.json`, product 7290107647854 `rowVerdict`, change the **standalone grade-letter token
`ג`** (the one asserting the grade, in the fragment `...חלבון. ג; מוצר מעובד...`) to **`ד`** so it matches the
badge grade D. Change ONLY that standalone grade-letter token. Do NOT alter any `ג` that is part of a real word
(e.g. גרם, גבוה, דגנים), and do NOT touch any other product, field, score, or grade.

## Hard guards
- No score/grade movement (you are correcting copy text to match the existing badge grade, not changing the grade).
- OFF-ban absolute. Do not commit or push. Do not close.

## Acceptance test (run it, put result in self_check)
Re-run the spine drill and confirm this specific G6 failure is gone:
`python 03_operations/page_generator/spine_flip.py --set BARI_PALM_HYDRO_V1=on --note "TASK-330 gradeletter verify"`
- Show the cereals G6 report no longer lists barcode 7290107647854 (grep it → 0).
- Confirm score_moves=0 for cereals and `git diff --stat` touches ONLY cereals_frontend_v2.json.
Note: the 2 sodium-causal cereals "fails" (7296073642046/7296073642022) are a separate GATE-regex fix, not yours.

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.**
