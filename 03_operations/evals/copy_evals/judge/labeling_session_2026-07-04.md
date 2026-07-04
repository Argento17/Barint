# Naturalness Judge — Owner Labeling Session (2026-07-04)

Owner: Tom. Labeled via interactive page (artifact) → JSON ingested to `labels_template.jsonl` by id.

## Set
- **Batch 1** — 41 mixed: 5 translationese slots (tr-001…005) + 36 real shipped lines
  (ls-001…036, 3 from each of 12 live categories).
- **Batch 2** — 24 fresh `rowVerdict` lines (lb2-001…024, 2/category, deduped vs batch 1)
  to clear the ≥40 in-scope floor.
- Total 65 rows in `labels_template.jsonl`; provenance = `source` field per row.
- **In-scope calibration set (rowVerdict + tr_slot) = 41 → floor CLEARED.**
  In-scope verdicts: 10 approved · 24 partially · 7 not-approved. Natural exemplars:
  10 approved + 19 owner rewrites.

## Owner labels (3-level, lossless)
- **approved** 7 · **partially_approved** 22 · **not_approved** 12  (after the ls-013 fix below)
- 21 owner rewrites captured → the gold "natural" exemplar seed.

## Owner decisions this session
1. **ls-013 → not_approved** (was approved). Owner ruling: mis-click; the identical note
   on ls-013/ls-015 ("if this is a product description it is really not good") rejects both.
2. **Judge scope = full-description copy only.** `in_judge_scope: true` for `rowVerdict`
   + `tr_slot`; `insightLine` card-tags are labeled but **excluded from calibration** —
   many were rejected for being "too little / not a full description," which measures
   *completeness*, not *naturalness*. Feeding them in would teach the judge "short = bad"
   and blow the TNR ≥ 0.90 bar. → In-scope N = **17**.

## Reusable rubric signals for the judge prompt (kind-agnostic)
- **Don't restate the nutritional numbers in prose** (ls-014/016/025/026/027/034/036; lb2-006/009/010/011/012/017/018).
- **Minimize em-dashes** (lb2-003/004/005/007/008/011/020) — matches the owner phrasing rule.
- **Use נתרן, never 'סודיום'/'סודים'** (lb2-009/010; census: 30 shipped lines).
- **Brand name is 'בארי', not 'ברי'** in prose (lb2-004; census below).
- Odd similes / calques read as unnatural (lb2-014 'לא חד כמו פגיון'; tr-002 'X, not Y').

## Shipped-copy defects surfaced (flagging, NOT fixing — descriptions freeze active)
See `shipped_copy_defects_2026-07-04.md`. Route into the owner's own description-rewrite pass:
- **30 lines** use 'סודיום/סודים' for sodium → should be 'נתרן'.
- **7 lines** with a standalone 'ברי' token (2 clear brand-subject uses) → brand should be 'בארי'.

## Open (resolve before the judge is built — NOT this session)
- **Binary mapping of `partially_approved`.** Recommended: *flag* (unnatural) — the judge's
  value is catching copy that needs an editorial pass. Provisional labels set that way
  (`label_provisional: true` on every row); one-line flip if owner prefers ship.
- ~~**≥40 calibration floor.**~~ CLEARED via batch 2 — in-scope N = 41.

## Not yet done (deliberately)
- `dataset/cases.jsonl` and `baseline.json` **untouched** — tr-slot naturalness labels
  get promoted there only once mapping is locked and N ≥ 40, to avoid corrupting the
  regression baseline. `judge_stub.py` stays `NotImplementedError` until a committed
  calibration record exists (TPR ≥ 0.80, TNR ≥ 0.90).
