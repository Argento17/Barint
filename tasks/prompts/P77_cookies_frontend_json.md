# P77 — Cookies-near-coffee: generate frontend JSON data substrate (route: C1 / Frontend)

**Task:** TASK-275. **Lane:** C1 Frontend Agent (C1-CURSOR is DOWN — quota). Generate the frontend JSON
data substrate from the LOCKED scoring run `run_cookies_003`, mirroring the golden brined structure.
Authored copy is merged later (PENDING_COPY placeholders now).

## Deliverable
`bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json` — mirror the schema of the golden
`bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (milk-depth v3 schema).

## Source (read first)
- Scores: `02_products/cookies_coffee/bsip2_outputs/run_cookies_003/` (61 traces + run_record).
- Corpus (names/brands/barcodes/images/ingredients/nutrition): `02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json`
  + `02_products/cookies_coffee/factory_run_001/corpus_filter.json` (IN_SCORED bucket = the 61).
- Generator (if usable): `03_operations/page_generator/generate_page.py` with a cookies config mirroring how
  brined was generated; otherwise build the JSON directly mirroring brined_cheeses_frontend_v2.json field-for-field.
- Golden structural reference: `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json`.

## Requirements
1. **61 products**, each with: barcode, name (`<name> — <brand>`), score + grade + confidence (FROM the
   run_003 trace — do not recompute), per-100g nutrition (energy/protein/fat/satfat/sugar/sodium from BSIP0),
   `imageUrl` (from BSIP0 image_urls; wire it into the row VM so it RENDERS), `d4_additives` (parsed from
   ingredients; empty array `[]` if none, never undefined), and the milk-depth v3 authored fields
   (`consumerTakeaway`, `consumerExplanation`, `bariInterpretation[]` with real dimension scores from the
   trace, `bestUseCases[]`) as **`PENDING_COPY`** placeholders (Content fills them in the merge step).
2. **Sort the `products` array by score DESCENDING** (stable tiebreak) — Stage-7 hygiene; the page renders
   array order.
3. Page shell scaffold (`_meta`/page_copy) with PENDING_COPY for hero/prologue/methodology/caveat.
4. Carry the run provenance (`run_cookies_003`) in `_meta`.

## Guards (hard)
- **Scores/grades/confidence come straight from the run_003 traces** — do NOT recompute or alter. Verify the
  JSON grade dist == run_003 (A0 B0 C9 D22 E30).
- **OFF ban absolute** — only the direct scrape data; a missing field = null/"data could not be retrieved",
  never OFF-filled. off=0.
- Do NOT touch any other category's data file. New file only. No copy authored here (that's P76/merge).
- Confidence archetype: expected-null fields (e.g. fiber) must NOT trigger a "missing nutrition"
  partial-confidence flag when core nutrition (kcal/protein/fat/sugar) is present.

## Return
End with the return contract: task=P77, proposed_status=RETURNED, artifact (cookies_coffee_frontend_v1.json
+ sha256), counts (products=61, grade dist == run_003, sorted-desc verified, images present N/61,
d4_additives present 61/61, off=0, PENDING_COPY count for authored fields), not_done, self_check. Propose
RETURNED — do NOT close. The orchestrator verifies dist==run_003 + sort + OFF before the copy merge + render.
