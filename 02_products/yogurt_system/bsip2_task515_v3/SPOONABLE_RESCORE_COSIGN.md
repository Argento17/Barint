# Spoonable ingredient-cleanup rescore — Nutrition co-sign record (TASK-515)

Durable provenance for the 8 spoonable score moves caused by the 2026-07-05 ingredient-text
scrape-artifact cleanup. Not an engine change: score_engine.py + constants.py byte-identical to
committed baseline 2474b04a (verified). The moves are 100% attributable to fixing whitespace that had
been HIDING real, on-label ingredient signals from signal_extractor.py (space-split words like
"גלוק וזה"→"גלוקוזה"). Nutrition Agent (dispatch a9db636e1f9ebe11f, 2026-07-05) read each product's
corrected ingredients_text_he + trace and CO-SIGNED all 8 as genuine true detections (0 spurious
rejoins). ingredients_raw_he (audit field) preserves the original artifacted scrape — correction is
reversible + auditable.

| barcode | before | after | unmasked (real, on-label) signal |
|---|---|---|---|
| 408354 | 63.1/C | 46.4/D | סירופ גלוקוזה (glucose syrup) → NOVA 3→4 (GRADE CROSSED — ruled honest) |
| 7290110578572 | 54.8/C | 50.0/C | חומרי טעם וריח (flavor agent) |
| 7290119380916 | 58.5/C | 53.7/C | חומרי טעם וריח |
| 7290102390465 | 38.7/D | 36.9/D | חומרי טעם וריח |
| 7290102390489 | 40.4/D | 38.6/D | חומרי טעם וריח |
| 7290102393176 | 43.6/D | 41.8/D | flavor-agent cluster / acidity regulator |
| 7290102393947 | 43.5/D | 41.7/D | מווסת חומציות (acidity regulator) |
| 7290102393169 | 42.4/D | 42.8/D | פקטין (pectin/fiber) → small glycemic/satiety bonus (score UP) |
| 7290102393060 | 62.0/C | 41.9/D | (9th, same class) BSIP1 trim-bug truncation restored from raw scrape → caramel E150 + soy lecithin E322 + mono/di-glycerides E392 now visible → NOVA 3→4 (GRADE CROSSED — same honest-data principle; blast-radius audit found this was the ONLY trim-bug-truncated product in the 122-corpus) |

- **Shelf-relative validity:** SUGAR_SHELF_REL_V1 guard unchanged (n=80, median 4.65, IQR scale 4.6,
  guard_pass=true) — sugars_g / nutrition values were NOT touched by the text cleanup, so the guard is
  unchanged by construction.
- **408354 C→D:** ruled honest and shippable (label genuinely carries more processing signal than the
  corrupted text showed); consistent with the honest-data-over-grade-continuity doctrine.
- **Systemic follow-up (Nutrition rec, separate task):** signal_extractor.py is whitespace-fragile;
  harden with internal-whitespace normalization in the matcher (not per-term literal variants), across
  all categories, with Nutrition+Product co-sign on the fix design. NOT done in this build.
- **Process note:** constants.py carries an uncommitted TASK-515A drinkable sweetener match-pattern
  addition (display-only, drinkable scores 0-diff, 0 overlap with the 94 spoonable products) — commit
  with the yogurt build, its own EV review.

Copy for the affected products (esp. 408354's grade + any d4-count-changed products) is re-authored
against these corrected scores before the spoonable page's Adversarial QA gate 2.
