# P55 / Investigate missing brined-cheese data: genuine scrape gap vs parser miss (route: C1-GEMINI)

You are a careful investigator with repo read access. For the brined-cheeses shelf, determine for
each product with a missing field whether the value is GENUINELY ABSENT from the source scrape
(honest null — correct to show "could not be retrieved") or a PARSER MISS (the data is present in
the raw scraped HTML/JSON but our parser failed — a fixable bug). Read-only investigation + a report.
Do NOT edit data, scores, or copy. Do NOT close — propose RETURNED.

## HARD GUARD — OFF ban (absolute)
NEVER consult Open Food Facts or any non-scrape source. The ONLY source is the direct product scrape.
Your job is to compare our PARSED output against the RAW SCRAPE of the SAME product — nothing else.
If a field is absent from the raw scrape, it is an honest null. Never suggest filling from elsewhere.

## Targets (read these)
- Parsed page: `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
  — products with `confidence_sub_reason == "missing_ingredients"` (12) or `"missing_nutrition"` (3),
  plus specifically barcode **4861070** (#33, גבינה צפתית קשה 24% — missing ingredients).
- Raw scrape: `C:\Bari\02_products\brined_cheeses\bsip0_outputs\brined_cheese_bsip0_raw_*.json`
  (and any banked HTML under `C:\Bari\03_operations\bsip0\`). Match by barcode.
- BSIP1 parsed output: `C:\Bari\03_operations\bsip1\run_brined_cheeses_002\output`.

## Method (per affected product)
1. Pull the product's RAW scrape record (the original Shufersal HTML/JSON we banked).
2. Look in the raw text for the missing field (ingredient list / sugar / whichever is null in our output).
3. Classify: HONEST-NULL (not in raw scrape) | PARSER-MISS (present in raw, absent in parsed) |
   AMBIGUOUS (present but malformed). Quote the raw evidence for each.
4. For #33 (4861070) specifically: explain exactly why ingredients are null.

## Return (machine-readable contract required)
- A table: barcode · name · missing field · raw-scrape evidence (quote) · verdict (honest-null /
  parser-miss / ambiguous).
- A count: how many of the 15 are honest-null vs parser-miss.
- If parser-miss found: name the parser file/pattern likely responsible (do NOT fix it — just point).
- Confirm OFF=0 (no external source consulted).
- End with the JSON return contract (`C:\Bari\01_framework\operations\return_contract_v1.md`).
  Do NOT close — propose RETURNED.
