# P53 / Re-render brined-cheeses v2 from corrected copy (route: C1-CURSOR)

You are a spec-complete implementer with repo access. The brined-cheeses consumer copy was
corrected at its SOURCE after an independent review caught a fabricated methodology line plus
grammar/factual fixes. Propagate the corrected copy into the two rendered frontend artifacts so
the local page matches the source. Mechanical propagation only — no new copy, no score changes.

## Source of truth (corrected — DO NOT edit)
`C:\Bari\02_products\brined_cheeses\brined_cheeses_copy_v1.json`
  - keyed by barcode under `.products.<barcode>` with fields like `insightLine`, `rowVerdict`, etc.
  - page-level strings under `.pageShell` (incl. `methodologyLines`, `heroTitle`, `categoryNote`).
  - `.products.<barcode>.score` / `.grade` are the authoritative display values (run_brined_004).

## Targets to regenerate (edit these)
1. `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
2. `C:\Bari\bari-web\src\lib\comparisons\brined-cheeses-page-data.ts`

## Contract
- For every barcode, copy the corrected Hebrew strings from copy_v1.json into the matching VM
  fields in both targets. Match by barcode (stable key) — NOT by array position, NOT by bc-NN label.
- Page-level strings (methodologyLines, heroTitle, categoryNote, any pageShell text) must match
  copy_v1.json pageShell exactly.
- DO NOT change any score, grade, barcode, image URL, confidence flag, ordering, or JSON/TS
  structure. Only the human-readable Hebrew copy strings change.
- The single most important change to confirm present: the methodology line must now read the
  structural-fairness framing ("מלח הכבישה ... חלק בלתי נפרד משיטת הייצור ...") and the old
  "חלק מהמלח נשאר בתמיסה ולא נאכל" must be ABSENT from both targets.

## Guards
- OFF ban (absolute): introduce no Open Food Facts / external data. Unknown stays unknown.
- No score/grade/nutrition value changes — copy strings only.

## Gate + return
- Run `npm run build` in `C:\Bari\bari-web`. It MUST exit 0 with the `/hashvaot/brined-cheeses`
  route present. Paste the build tail.
- Return: list of files changed; confirm old fabricated phrase absent in BOTH targets (show your
  grep), new framing present; confirm zero score/grade/structure changes; build exit code.
- Do NOT close — propose RETURNED. End with the machine-readable return contract
  (`C:\Bari\01_framework\operations\return_contract_v1.md`).
