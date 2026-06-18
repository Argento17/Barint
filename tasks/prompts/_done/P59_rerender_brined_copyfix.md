# P59 / Re-render brined: propagate 3 copy fixes to frontend (route: C1-CURSOR)
Spec-complete propagation. The brined copy source had 3 targeted edits (Stage-9 red-team fixes).
Propagate ONLY the changed strings into the rendered frontend. No score/structure changes.
Do NOT close — propose RETURNED.

## Source of truth (do not edit)
`C:\Bari\02_products\brined_cheeses\brined_cheeses_copy_v1.json`

## Targets
1. `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json` — update rowVerdict for
   barcodes 554457 and 7290017065236 to match copy_v1 exactly.
2. `C:\Bari\bari-web\src\lib\comparisons\brined-cheeses-page-data.ts` — update pageShell
   methodologyLines[0] to match copy_v1 exactly.
Match by barcode. Change NOTHING else (no scores, grades, other verdicts, confidence, images).

## Verify before return
- The two products' rowVerdict + methodologyLines[0] in the targets == copy_v1 (quote them).
- `npm run build` in bari-web → exit 0, route /hashvaot/brined-cheeses present.
- Confirm 0 score/grade/confidence changes. Return files+shas, build tail, return contract. Propose RETURNED.
