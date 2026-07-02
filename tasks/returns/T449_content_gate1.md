# TASK-449 — Content Agent, Gate 1 of 2 (Hebrew copy flip for brined-cheeses candidate)

**Status proposed:** RETURNED (draft — gate 1 of 2; requires Adversarial QA / Red-Team sign-off, gate 2, before this reaches the owner)
**Worktree:** `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`)
**Scope:** Consumer-facing copy only, in `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json`. No score/grade/rank/barcode/name/schema field touched (verified — see Self-check).

## Context

P459's engine fix (`BARI_FERMENT_MARKER_BRINED_FIX_V1`) removed an unearned +8
"fermentation name marker" bonus from brined cheeses. The candidate artifact was
rebuilt from the exact live page (score/grade swapped from new traces, rank
recomputed, copy carried over unchanged). Because copy was carried over
unchanged, several products' `insightLine`/`rowVerdict` cited numbers, grade
letters, or rank/superlative claims made stale by the rescore.

## Derivation of the mover count (built independently, not trusted from the contract)

The contract states 16 grade movers; an earlier count said 19. I built my own
diff of the candidate JSON against the TRUE production-live baseline
(`C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json` — the
main tree, not the worktree's own copy of that file).

**First pass used the worktree's local copy** of `brined_cheeses_frontend_v2.json`
as the baseline and got **19** grade movers — 3 more than the contract's 16
(barcodes `369617`, `7290108509106`, `7290108509755`). Investigation found the
worktree's local copy is **stale relative to `C:\Bari`**: the worktree branch
carries an extra commit (`7723c5c4`, "De-anchor sweep go-live:
BARI_REDLABEL_CONTINUOUS_V1 across 10 categories") on top of the same base as
`C:\Bari`'s live file, which already moved those 3 products' grades for an
unrelated reason (the red-label de-anchor sweep, not this fermentation fix).
Re-running the diff against `C:\Bari`'s live file (the true production
baseline, and what `run_gates.py --baseline` in the contract's own
`commands_run` actually points at) gives **16 grade movers, exactly matching
the contract**. The 19-count and the 16-count are both "real" outputs of
different (correct vs stale) baselines — 16 is the one that matters because it
is diffed against what is actually live.

**Derived grade-mover list (16, matches contract and G7 PARITY gate exactly):**
`2107798, 2133162, 7290011499051, 7290011499112, 7290011499303, 7290017065236,
7290019635222, 7290019635826, 7290019790112, 7290019790808, 7290102397334,
7290114312707, 7290114314015, 7296073641902, 7296073641940, 7296073641957`

24 score movers, 34 rank movers (rank is highly volatile because more than a
third of the shelf moved).

## Copy audit method

1. Dumped every product's `insightLine` + `rowVerdict` + `expansion.limitingFactors`
   alongside score/grade/rank deltas (candidate vs `C:\Bari` live).
2. Regex-scanned all 36 products for stale grade-letter tokens (`ה-A`, `ה-B`,
   `קבוצת ה-X`, `גבינות ה-X`) and stale rank/superlative phrases ("הציון הגבוה
   ביותר במדף", "לראש הקטגוריה", "לראש המדף").
3. For each hit, checked whether the citation still matches the product's
   *own current* grade/rank/score, or referenced a fact that changed.
4. For every superlative kept or rewritten, verified it against a fresh
   facts table built from all 36 products' `expansion.nutrition` fields
   (sodium/protein/fat), not assumed.

## Lines changed: 8 products, 11 fields

| # | Barcode | Product | Field | Grounding |
|---|---|---|---|---|
| 1 | 2133162 | גבינה בולגרית 5% שומן | insightLine | trace: score 72.3/B (was 80.3/A); facts table: 21g protein still highest among the fat≤5.5% subset (8 products) |
| 2 | 2133162 | גבינה בולגרית 5% שומן | rowVerdict | same |
| 3 | 7290102397334 | גבינה בולגרית 5% | insightLine | trace: score 73.5/B (was 81.5/A); facts table: 1550mg sodium still highest among the fat≤5.5% subset |
| 4 | 7290102397334 | גבינה בולגרית 5% | rowVerdict | same |
| 5 | 7290017065236 | בולגרית מעודנת 24% | rowVerdict | trace: score 58.3/C (was 66.3/B); grade token `ה-B` → `ה-C` |
| 6 | 7290019635826 | קוביות פטה עיזים מעודנת 5% | insightLine | trace: score 75.3/B rank 4 (was 83.3/A rank 1); no longer highest score on shelf (554457/554532 now score 82.7) |
| 7 | 7290019635826 | קוביות פטה עיזים מעודנת 5% | rowVerdict | same; removed "reaches the top of the category" |
| 8 | 7296073641902 | פטה כבשים 20% | rowVerdict | trace: score 63.7/C (was 71.7/B); grade token `ה-B` → `ה-C` |
| 9 | 7296073641957 | בולגרית מסורתית 16% | rowVerdict | trace: score 64.0/C (was 72.0/B); grade token `ה-B` → `ה-C` |
| 10 | 7290019790112 | פטה כבשים 20% שומן | rowVerdict | trace: score 62.5/C (was 70.5/B); grade token `ה-B` → `ה-C` |
| 11 | 7290108509106 | קוביות בולגרית מעודנת 13% | rowVerdict | facts table: rank now 3/36 (was 10/36) — two A-grade products occupy rank 1; "reaches the top of the shelf" no longer accurate (score/grade themselves unchanged, 78.6/B, per trace — fermentation_bonus_applied=True for this product independently, per P459 contract's "1 marker product retained bonus for independent reason") |

**Framing discipline applied throughout:** every A→B rewrite reframes the
product's real, unchanged composition (protein/sodium/ingredient facts that
never moved) rather than narrating that "the engine changed" or that the
product "got worse." No meta-commentary about scoring methodology was
introduced into any line.

### Full old → new text (all 11 edits)

**2133162 — insightLine**
- Old: `חלבון מהגבוהים בקבוצת ה-A (21 גרם) — עם נתרן גבוה שמאזן.`
- New: `חלבון של 21 גרם — הגבוה ביותר בין גבינות ה-5% שומן במדף — לצד נתרן גבוה שמאזן.`

**2133162 — rowVerdict**
- Old: `בולגרית 5%. חלבון של 21 גרם — הגבוה ביותר בין כל גבינות ה-A. הנתרן עומד על 1,300 מ"ג, כ-300 מ"ג מעל חציון המדף, ומוסיף חיסרון קל.`
- New: `בולגרית 5%. חלבון של 21 גרם — הגבוה ביותר בין גבינות ה-5% שומן בקטגוריה. הנתרן עומד על 1,300 מ"ג, כ-300 מ"ג מעל חציון המדף, ומוסיף חיסרון קל.`

**7290102397334 — insightLine**
- Old: `שלושה רכיבים, חלבון מהגבוהים בקבוצת ה-A — אבל גם הנתרן הגבוה ביותר ב-A.`
- New: `שלושה רכיבים, חלבון מהגבוהים בקטגוריה — אבל גם הנתרן הגבוה ביותר בין הגבינות בשומן 5%.`

**7290102397334 — rowVerdict**
- Old: `בולגרית 5% של משק צוריאל. החוזק ברשימה הנקייה ועוצמת החלבון. החיסרון: נתרן של 1,550 מ"ג — הגבוה ביותר בין כל גבינות ה-A, וכ-550 מ"ג מעל חציון המדף. הפער הזה מוריד מהציון אבל לא מסחרר את הדירוג.`
- New: `בולגרית 5% של משק צוריאל. החוזק ברשימה הנקייה ועוצמת החלבון. החיסרון: נתרן של 1,550 מ"ג — הגבוה ביותר בין כל הגבינות בשומן 5% בקטגוריה, וכ-550 מ"ג מעל חציון המדף. הפער הזה מוריד מהציון אבל לא מסחרר את הדירוג.`

**7290017065236 — rowVerdict**
- Old: `...הנתרן המדוד על התווית: 1,010 מ"ג, על החציון, ואינו מוסיף חיסרון מעבר לבסיס. ה-B נובע מהשומן הגבוה יחסית.`
- New: `...הנתרן המדוד על התווית: 1,010 מ"ג, על החציון, ואינו מוסיף חיסרון מעבר לבסיס. ה-C נובע מהשומן הגבוה יחסית.`

**7290019635826 — insightLine**
- Old: `שלושה רכיבים, חלב עיזים — הפשטות הזו מביאה את הציון הגבוה ביותר במדף.`
- New: `שלושה רכיבים, חלב עיזים — רשימה קצרה ופשוטה גם ביחס למדף הזה.`

**7290019635826 — rowVerdict**
- Old: `פטה עיזים 5% מחלבות גד מגיעה לראש הקטגוריה בזכות הרשימה הקצרה ביותר האפשרית: חלב עיזים מפוסטר, מלח, חומר משמר אחד. אין מייצבים, אין רכיבי חלב נוספים. הנתרן נמצא ליד חציון המדף — ולכן אינו מוסיף חיסרון מעבר לבסיס.`
- New: `פטה עיזים 5% מעודנת מחלבות גד עם הרשימה הקצרה ביותר האפשרית: חלב עיזים מפוסטר, מלח, חומר משמר אחד. אין מייצבים, אין רכיבי חלב נוספים. הנתרן נמצא ליד חציון המדף — ולכן אינו מוסיף חיסרון מעבר לבסיס.`

**7296073641902 — rowVerdict**
- Old: `...הנתרן (1,100 מ"ג) גבוה מהחציון ב-100 מ"ג — חיסרון קטן. ה-B נובע בעיקר מאחוז השומן.`
- New: `...הנתרן (1,100 מ"ג) גבוה מהחציון ב-100 מ"ג — חיסרון קטן. ה-C נובע בעיקר מאחוז השומן.`

**7296073641957 — rowVerdict**
- Old: `...הנתרן (1,000 מ"ג) בדיוק על החציון ולא מוסיף חיסרון מעבר לבסיס. ה-B נובע מ-16% שומן.`
- New: `...הנתרן (1,000 מ"ג) בדיוק על החציון ולא מוסיף חיסרון מעבר לבסיס. ה-C נובע מ-16% שומן.`

**7290019790112 — rowVerdict**
- Old: `...כל אחד מהם גורם לחיסרון; ביחד הם מציבים את הגבינה בתחתית ה-B.`
- New: `...כל אחד מהם גורם לחיסרון; ביחד הם מציבים את הגבינה בתחתית ה-C.`

**7290108509106 — rowVerdict**
- Old: `בולגרית 13% שמגיעה לראש המדף בזכות שני דברים שנדיר למצוא יחד בגבינה בכבישה: ...`
- New: `בולגרית 13% שמתבלטת בזכות שני דברים שנדיר למצוא יחד בגבינה בכבישה: ...`

## Lines checked and deliberately left unchanged (still factually true)

- `554457` / `554532` (rank 1, grade A, unmoved): `הנתרן הנמוך ביותר בין כל גבינות ה-A` —
  still literally true; there are now exactly 2 A-grade products in the set (both
  these SKUs), both tied at 600mg sodium, the lowest in the whole 36-product
  set. Not stale.
- `7290017065663` (grade B, unmoved): `מה שמוריד אותה מה-A` — evergreen
  explanatory framing (explains its own gap to A), not a stale citation of its
  own grade.
- `7296073641964`, `7290102393718` and other non-grade-movers whose text cites
  their own current grade letter — all verified self-consistent (grade token
  matches `product.grade` in the candidate JSON).

## Gate results (after edits)

Ran the exact contract invocation:
```
python 03_operations/page_generator/gates/run_gates.py _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline C:/Bari/bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
```

| Gate | Status | Note |
|---|---|---|
| G1 SCHEMA | FAIL | Pre-existing (missing `comparisonContext`, extra `satFat`, `limitingFactors` typing) — identical failure set to the pre-edit gate report, unrelated to copy |
| G2 COVERAGE | PASS | |
| G3 SCOPE | FAIL | Pre-existing — same 12 scored-but-undisplayed barcodes as before my edits, unrelated to copy |
| G4 OFF | PASS | |
| G5 GRADE-INTEGRITY | PASS | |
| **G6 COPY-SAFETY** | **PASS** | No copy-safety violations detected |
| G7 PARITY | PASS | 16 grade changes (unchanged by copy edits — proves no data was moved); avg consumer-text chars/product 354 vs pre-edit 353 (+1), confirming edits were surgical |
| G8 DATA-SANITY | PASS | |

Overall: FAIL — driven entirely by the pre-existing G1/G3 debt already present
in the candidate before I touched it (same failure counts/barcodes as the
gate report generated at candidate-build time, `brined_cheeses_candidate_brinedfix_gates_report.md`,
timestamped before my edits). **G5, G6, G7, G8 all PASS**, confirming the copy
pass did not touch scores/grades/ranks and introduced no copy-safety
violation.

## Self-check: scope discipline

Verified programmatically that every one of the 36 products' `score`, `grade`,
and `rank` in the post-edit JSON is byte-identical to the pre-edit JSON
(0 mismatches). Only `insightLine`/`rowVerdict` on the 8 listed barcodes
changed. No barcode, name, schema, `_meta`, or non-copy field was touched.

## Not done / handed to gate 2

- G1/G3 schema/scope debt is pre-existing engine/generator output, not a
  content-agent fix — flagged for Data/Frontend, not resolved here.
- This return is a DRAFT. It has not been reviewed by Adversarial QA /
  Red-Team (gate 2). No owner-facing sign-off has occurred.

```json
{
  "task": "TASK-449 content gate 1",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json", "action": "modified (copy fields only, 8 products, 11 fields)", "note": "gitignored — not committed; this log is the record of the diff"},
    {"path": "tasks/returns/T449_content_gate1.md", "action": "created"}
  ],
  "counts": {
    "products_edited": "8/36 (derived from stale grade-token + stale superlative regex scan cross-checked against facts table built from candidate expansion.nutrition fields)",
    "fields_edited": "11 (7 rowVerdict + 4 insightLine, derived from edit_log entries written by the edit script)",
    "grade_movers_derived": "16/36 (diff vs C:\\Bari TRUE production-live brined_cheeses_frontend_v2.json; matches contract's 16, NOT the 19 first obtained from the worktree's own stale local copy of that file, which carries an extra unrelated commit 7723c5c4)",
    "score_movers_derived": "24/36",
    "rank_movers_derived": "34/36"
  },
  "commands_run": [
    {"cmd": "python C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e6653b0d-675a-4d0b-90c7-36976c2e5fba/scratchpad/analyze2.py (custom diff script, candidate vs C:/Bari live)", "exit_code": 0},
    {"cmd": "python C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e6653b0d-675a-4d0b-90c7-36976c2e5fba/scratchpad/scan_stale.py (regex scan for stale grade/superlative tokens, pre and post edit)", "exit_code": 0},
    {"cmd": "python C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e6653b0d-675a-4d0b-90c7-36976c2e5fba/scratchpad/edits.py (applies the 11 field edits, writes edit_log.json)", "exit_code": 0},
    {"cmd": "python C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e6653b0d-675a-4d0b-90c7-36976c2e5fba/scratchpad/verify_scope.py (confirms 0 score/grade/rank mismatches vs pre-edit state)", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline C:/Bari/bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json", "exit_code": 1}
  ],
  "not_done": [
    "G1/G3 schema/scope debt (pre-existing, not a content-agent fix)",
    "Adversarial QA / Red-Team gate 2 review (required before any owner-facing use)",
    "Owner sign-off, PR, deploy (out of scope for this worktree per task boundaries)"
  ],
  "self_check": "verify_scope.py: 0/36 products show score/grade/rank drift vs pre-edit snapshot; run_gates.py G5/G6/G7/G8 all PASS; G1/G3 FAIL counts identical to pre-edit gate report"
}
```
