# P265 / Brand enrichment — fresh il_prices PriceFull pull (route: C1-CURSOR)

Repo C:\Bari, site under bari-web (local == origin/master). TASK-425. STAGING ONLY — no commit/push/deploy. Touch ONLY `bread_frontend_v3.json`, `hard_cheeses_frontend_v4.json`, `hummus_frontend_v5.json` (bari-web/src/data/comparisons/). NO score/grade/copy changes — only add the `brand` field. OFF-BAN ABSOLUTE. NEVER invent/infer a brand — real source only, else leave null.

## Context
An earlier run (P262) found 0 brand matches because the il_prices feed cache held only Shufersal *delta* `Price` files, not the full `PriceFull` catalog. Owner authorized a FRESH PriceFull pull.

## Do
1. Using the il_prices client under `integrations/clients/` (the read-only IL price-transparency client, TASK-170), trigger/download the current **`PriceFull`** catalog for Shufersal (and, if it improves coverage, Victory / Rami-Levy / Yochananof — these are grocery chains that carry bread/cheese/hummus, unlike Super-Pharm). If the client caches feeds, force a fresh fetch of PriceFull.
2. For each of the 114 products lacking a real `brand` (bread 26, hard_cheeses 31, hummus 57), look up its `barcode` in the PriceFull data and read `ManufacturerName` (or the manufacturer/brand field). Populate `brand` with the REAL name on an exact barcode match. Where no match/empty, leave null — no guessing, no name-derivation, no OFF.
3. Report coverage: per file, how many barcodes matched → real brand (with 5 sample barcode→ManufacturerName pairs as evidence), how many remain null, and which retailer feed provided the matches.

## Guards
- If PriceFull still can't be fetched (feed unavailable / client limitation), STOP and report exactly what blocked it — do NOT fabricate. Brands stay null and we accept it for now.
- Confirm 0 score/grade/copy changes; only `brand` added.

End with the return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED. Trace-derived coverage counts + the feed source.
