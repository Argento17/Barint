---
id: TASK-151
title: "Harden _shared BSIP0 scrape path: persist raw nutritionList source (rows + HTML) for offline replay of future parser fixes"
owner: data-agent
status: RETURNED
priority: MEDIUM
created_at: 2026-06-02
completed_at: 2026-06-02
depends_on: [TASK-142A]
blocks: [TASK-149, TASK-150]
parent: TASK-142A
category_id: infra
summary: >
  EV-029 (TASK-142A) showed the Shufersal BSIP0 scrapers persisted only the parser's reduced *_raw fields,
  not the source div.nutritionList — so when the trans-as-total-fat parser bug was fixed, the true fat/
  saturated values were unrecoverable from disk (saturated 0% captured; fat collapsed to 0.5) and a fresh
  NETWORK re-scrape was the only way to recover them. This hardens the shared scrape path so every scrape
  persists the raw nutrition source, making any FUTURE parser fix a free OFFLINE re-parse. Landed BEFORE the
  TASK-149/150 live re-scrapes so those runs capture the raw source going forward.
---

# TASK-151 — Persist raw nutrition source for offline replay

Spun off EV-029 / TASK-142A. Sequenced before TASK-149/150 (user ruling 2026-06-02: "harden first, then 149+150").

## Change (data-ingestion only; no scoring, no published scores)
- `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`:
  - Split the parse into `extract_nutrition_rows(soup)` (raw `(value,label)` pairs, pre-classification) and
    `parse_nutrition_rows(rows)` (the classification half). `parse_nutrition_list(soup)` is now a thin wrapper
    over both — **behaviour identical** (verified: total fat from the genuine total row, saturated captured,
    first-per-field).
  - Added `extract_nutrition_raw(soup) -> {"rows":[…], "html":"<outer div.nutritionList>"}` for capture.
- All 5 nutritionList scrapers (cheese, hummus, maadanim, yogurt, cereals) import `extract_nutrition_raw` and
  persist `nutrition_raw_source` in each BSIP0 product record.

## Verification
- Unit test: total fat = 9 (not 0.5) on a panel with trans/saturated sub-rows; saturated = 5.4 captured;
  7 raw rows + 507-char HTML persisted; **offline replay (`parse_nutrition_rows(raw.rows)`) == live parse**.
- All 5 scrapers `ast.parse` clean after wiring.

## Exit / DoD
Raw nutrition source persisted by all nutritionList scrapers; offline-replay round-trip proven; behaviour of the
existing parse unchanged. A future EV-029-class label-mapping fix replays from `nutrition_raw_source.rows`
without re-scraping. **Proposed RETURNED** — CC records CLOSED.

## Guards
Additive only; no scoring logic, no published/frozen scores, no router touched. Existing `parse_nutrition_list`
call sites and outputs unchanged (the new field is additive to the record).
