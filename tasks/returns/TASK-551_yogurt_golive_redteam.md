# TASK-551 — Yogurt go-live: two-gate sign-off record (2026-07-09)

Scope: `/hashvaot/yogurt` (spoonable, 50) + `/hashvaot/yogurt-drinks` (drinks, 17), plus the
hub cards on `/hashvaot/supermarket` and the `/madrichim/yogurt-glp1` guide that shares the
spoonable corpus. Owner authorized deploy 2026-07-09.

## Content gate — Content Agent

- Authored all 67 `insightLine` / `rowVerdict` + `positiveSignals` (full rewrite). Constraint:
  no nutrition values and no ingredient-count recitation in prose (the bars carry protein/sugar
  per 100g); no framework leakage, no grade letters, no "X, not Y", no cross-product references.
- Self-check: 0 digits in insight/row (excl. the literal brand name "פרו 21"), 0 count
  recitations, `hebrew_readability.is_clean` on all strings. Caught and fixed 21 of its own
  "X, not Y" antithesis constructions before returning.
- Second pass: corrected the drinks prologue overclaims after red-team MED-5 — `sentences[0]`
  "רבים" → "כרבע" (artificial sweeteners are 4/17), `sentences[2]` "חלק גדול" → "קצת פחות
  ממחצית" (real-fruit purees are 7/17) and quantified "כרבע מהם" so the 3/17 monk-fruit
  (natural) products are not implied to be artificial. `sentences[1]`/`[3]` byte-identical.

## Red-team gate — Adversarial QA Agent (3 passes)

Round 1 — **NOT CLEARED**, 2 CRITICAL:
- CRIT-1: `ציון S` leaked into live FAQ JSON-LD while the page chip beside it read `A`
  (copy law: copy never writes S).
- CRIT-2: `limitingFactors` claimed "סוכר גבוה יחסית למדף (1 גרם)" on barcode `7290110328221`,
  the shelf's LOWEST-sugar product. Trace: `SUGAR_SHELF_REL_V1 amount = -1` (a credit for being
  below the shelf median). The driver→label map ignored the sign.

Round 2 — CRITICALs verified fixed; **NEW-1 (HIGH)** found: the spoonable FAQ A-list claimed
"9 מוצרים" but named 8. Root cause was not a dedup — `generate_faq_schema.py` named
`a_products[:8]` while printing `len(a_products)`, so ANY category with >8 A-products emitted
self-contradicting structured data.

Round 3 — **GO-LIVE CLEARED**. 0 open CRITICAL, 0 open HIGH, no new findings.

## Fixes — made at the source, not patched into the JSON

| Finding | Fix |
|---|---|
| CRIT-1 + HIGH-3 | `03_operations/seo/generate_faq_schema.py`: new `frontend_grade()` folds the engine grade to the rendered chip grade (>=80 A) before emit, honoring `_aCappedToB`. Cannot recur on any category. |
| CRIT-2 | False limiter removed from `7290110328221`. Swept all 67: the 17 remaining "high sugar" labels all have `amount > 0`; 0 violations, 0 deserving products stripped. |
| NEW-1 | `A_LIST_CAP = 12`; count and enumeration can no longer disagree — names all A-products under the cap, else "ביניהם" (among them). Also replaced a U+060C Arabic comma with a normal comma inside Hebrew text. |
| MED-4 | Both FAQ `_bari_meta.product_count` regenerated → 50 / 17. |
| MED-5 | Drinks prologue proportions corrected (see Content gate above). |
| MED-6 | "פרו 21" accepted — the literal brand name, not a nutrition figure. |

Separately, a **gate bug** was fixed in `03_operations/page_generator/gates/run_gates.py`:
G2's v3 coverage counted an ABSENT `consumerExplanation.whyRated` / `bestUseCases` as
"still PENDING_COPY", contradicting its own comment and failing the already-shipped crackers
page. Now only a literal `PENDING_COPY` placeholder fails, matching the semantics
`consumerTakeaway` and `bariInterpretation` already used. Negative test: an injected
`PENDING_COPY` still fails 2/17.

## Final verification (all green)

- `run_gates.py` exit 0 on both pages (G3 SCOPE now documents all 33 culled/relocated barcodes
  in `_meta.exclusions`; G2 WARN, not FAIL).
- `validate_comparison_page.py` PASS on both (score==trace 0 mismatch, OFF=0, 0 PENDING,
  count consistency, ingredient sanity, imageUrl present, superlative rank-check).
- `tsc --noEmit` clean; `next build` exit 0; all four routes 200.
- Live-DOM: 0 `ציון S`, FAQ A-list 9 named == 9 claimed == 9 chips, 17 legitimate high-sugar
  labels, counts 50/17 everywhere, OFF=0, PENDING_COPY=0, deep-dive prose absent.
- Actimel relocation intact: 49.3/D and 45.6/D on drinks (backed by drinkable traces), absent
  from spoonable. Re-score under the drinkable config was control-proven (an existing drink
  reproduced its published 55.7/C exactly) and returned identical grades — no score movement.

**Verdict: GO-LIVE CLEARED.** Merge into `origin/master` remains the owner's call.
