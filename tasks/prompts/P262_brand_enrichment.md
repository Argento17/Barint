# P262 / Brand enrichment via il_prices (bread + hard_cheeses + hummus) + hummus rank (route: C1-CURSOR)

Repo C:\Bari, site under bari-web. TASK-422. STAGING ONLY — no commit/push/deploy. Touch ONLY: `bread_frontend_v3.json`, `hard_cheeses_frontend_v4.json`, `hummus_frontend_v5.json` (bari-web/src/data/comparisons/). NO score/grade/copy changes — you add the `brand` field and (hummus only) fix `rank`. OFF-BAN ABSOLUTE. NEVER invent or infer a brand — real source only, else null.

## Why
These 3 categories render product rows WITHOUT the "· brand" suffix other categories show, because their products carry no `brand` field. bread 26/29, hard_cheeses 31/31, hummus 57/57 are missing brand. The authoritative source is the **il_prices** price-transparency feed (`ManufacturerName`), which is how other categories got their brands — NOT the Shufersal product scrape (which returns empty brand for these), and NEVER Open Food Facts.

## Do
1. Use the existing il_prices client under `integrations/clients/` (the read-only IL price-transparency client from TASK-170; find it, don't rebuild it). For each product in the 3 files that lacks a real `brand`, look up its `barcode` in il_prices and read the manufacturer/brand name (`ManufacturerName` or equivalent).
2. Populate `brand` with the REAL manufacturer name where il_prices returns a confident match for that barcode. Match on exact barcode only. Where il_prices has no match or an empty/ambiguous name, leave `brand` null/absent — DO NOT guess, DO NOT derive from the product name, DO NOT use OFF.
3. hummus only: after any changes, confirm the array stays score-sorted and reindex `rank` 1..N (hummus rank was flagged not-1..N).

## Verify + report (per file)
- N products, how many got a REAL brand from il_prices (with the barcode→ManufacturerName evidence for a sample of 5), how many remain legitimately null (no il_prices match).
- Confirm 0 `score`/`grade` values changed and no field other than `brand` (+ hummus `rank`) was touched.
- If the il_prices client is unavailable or returns nothing for these barcodes, STOP and report that (do not fabricate) — brand stays null and we accept it.

End with the return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED. Trace-derived counts + the lookup command/source.
