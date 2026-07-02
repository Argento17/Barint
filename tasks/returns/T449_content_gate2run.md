# TASK-449 — Content Agent, Gate 1 RE-PASS (rebuilt P461 candidate, worktree-live basis)

**Status proposed:** RETURNED (draft — gate 1 of 2; requires Adversarial QA / Red-Team sign-off before owner-facing use)
**Worktree:** `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`)
**Supersedes:** `tasks/returns/T449_content_gate1.md` (commit `cae16adb`) — that pass edited the OLD candidate, whose copy edits were overwritten by design when P461 rebuilt the artifact. The old log's baseline conclusion was **inverted**: the worktree copy of `brined_cheeses_frontend_v2.json` is the TRUE live baseline; the `C:\Bari` copy was stale pre-sweep. This re-pass uses only worktree artifacts.

## Basis verification (done before any edit)

- Baseline `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` sha256
  `532002574639cee09617883ecbc727d4f5b7959c4ee21c9ca2142b6035c65f72` — matches coordinator/P461.
- Rebuilt candidate `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` sha256
  `f17b572c006d13ed1707dc53fc22903d7a7e568dbf1a2ef4dfb1acd77650419c` — matches P461 contract.
- Pre-edit check: candidate copy was byte-identical to worktree-live copy for all 36 products
  (0 diverging insightLine/rowVerdict fields) — confirmed my previous 11 edits were gone.

## Derived movement (independent diff, candidate vs worktree-live)

- **24 score movers, 0 upward** — matches P461.
- **14 grade movers** — matches P461 and G7:
  A→B: `7290019635826, 7296073641940, 7290102397334, 7290011499303, 2133162`
  B→C: `7296073641902, 7290011499051, 7290019790808, 7290019790112, 7290114314015, 7290011499112, 7290019635222, 7290017065236`
  C→D: `7290114312707`
- 34 rank movers.
- Changes vs my first pass's list: `7296073641957` and `2107798` now stay B (edits DROPPED —
  `7296073641957`'s live "ה-B נובע מ-16% שומן" is true again and was left untouched);
  `7290108509106` is grade A in this basis (it is P461's 1/35 marker product that retains the
  fermentation bonus for an independent reason; `fermentation_bonus_applied=True` in its ON-ON trace).

## Lines changed: 9 products / 12 fields (4 insightLine + 8 rowVerdict)

Every superlative kept or written was rank-checked against ALL 36 products using a facts table
built from the candidate's own `expansion.nutrition` fields; every grade/score fact was checked
against the product's ON-ON `bsip2_trace.json`.

### A→B movers (framing: the composition was always this; no "product got worse" language, no engine meta-copy)

**1-2. `7290019635826` (קוביות פטה עיזים מעודנת 5%, 84.1/A→76.1/B, rank 1→4)**
- insightLine old: `שלושה רכיבים, חלב עיזים — הפשטות הזו מביאה את הציון הגבוה ביותר במדף.`
- insightLine new: `שלושה רכיבים, חלב עיזים — רשימה קצרה ופשוטה גם ביחס למדף הזה.`
- rowVerdict old: `פטה עיזים 5% מחלבות גד מגיעה לראש הקטגוריה בזכות הרשימה הקצרה ביותר האפשרית: ...`
- rowVerdict new: `פטה עיזים 5% מעודנת מחלבות גד עם הרשימה הקצרה ביותר האפשרית: ...` (rest unchanged)
- Grounding: ON-ON trace `final_score_estimate=76.1 grade_estimate=B fermentation_bonus_applied=False`; top score is now 82.7 (554457/554532) — "highest score on the shelf" and "reaches the top of the category" are both false at rank 4/36. Composition facts kept (3 ingredients, sodium 950mg ≈ median).

**3-4. `7290102397334` (גבינה בולגרית 5%, 82.2/A→74.2/B)**
- insightLine old: `שלושה רכיבים, חלבון מהגבוהים בקבוצת ה-A — אבל גם הנתרן הגבוה ביותר ב-A.`
- insightLine new: `שלושה רכיבים, חלבון מהגבוהים בקטגוריה — אבל גם הנתרן הגבוה ביותר בין הגבינות בשומן 5%.`
- rowVerdict old: `...נתרן של 1,550 מ"ג — הגבוה ביותר בין כל גבינות ה-A, וכ-550 מ"ג מעל חציון המדף...`
- rowVerdict new: `...נתרן של 1,550 מ"ג — הגבוה ביותר בין כל הגבינות בשומן 5% בקטגוריה, וכ-550 מ"ג מעל חציון המדף...`
- Grounding: product left the A group (trace 74.2/B). Rank-checks: protein 20.5 = 6th of 36 ("מהגבוהים בקטגוריה" holds); sodium 1550mg = max of the fat≤5.5 subset (next 1300).

**5-6. `2133162` (גבינה בולגרית 5% שומן, 81.0/A→73.0/B)**
- insightLine old: `חלבון מהגבוהים בקבוצת ה-A (21 גרם) — עם נתרן גבוה שמאזן.`
- insightLine new: `חלבון של 21 גרם, הגבוה ביותר בין גבינות ה-5% שומן במדף — עם נתרן גבוה שמאזן.`
- rowVerdict old: `בולגרית 5%. חלבון של 21 גרם — הגבוה ביותר בין כל גבינות ה-A. ...`
- rowVerdict new: `בולגרית 5%. חלבון של 21 גרם — הגבוה ביותר בין גבינות ה-5% שומן בקטגוריה. ...`
- Grounding: trace 73.0/B. Rank-check: protein 21.0 = max of the fat≤5.5 subset; overall max is halloumi 24.0, so the superlative MUST stay scoped to the 5%-fat group.

Non-edits among A→B movers: `7296073641940` and `7290011499303` — their live copy cites no
grade letter, rank, or now-false superlative ("מה שמבדיל אותה מהמובילות" remains coherent at
rank 5). Verified line by line; left unchanged.

### B→C movers (only 3 of the 8 cite their grade; the other 5 verified clean)

**7. `7296073641902`** — rowVerdict `ה-B נובע בעיקר מאחוז השומן` → `ה-C נובע בעיקר מאחוז השומן` (trace 64.8/C).
**8. `7290017065236`** — rowVerdict `ה-B נובע מהשומן הגבוה יחסית` → `ה-C נובע מהשומן הגבוה יחסית` (trace 59.4/C).
**9. `7290019790112`** — rowVerdict `...ביחד הם מציבים את הגבינה בתחתית ה-B.` → `...ביחד הם מה שמוריד את הגבינה ל-C.`
   NOTE: a literal swap to "בתחתית ה-C" would be a NEW false claim — 63.5 is 7th of 13 C products
   (mid-C), not the bottom. Reframed to the two drivers pushing it into C (trace 63.5/C).

Verified clean (no grade/rank/superlative in copy): `7290011499051`, `7290019790808`,
`7290114314015`, `7290011499112`, `7290019635222`.

### C→D mover

`7290114312707` — copy cites no grade letter or position ("הם מה שמסביר את הציון"); verified clean, unchanged.

### Score-only / rank-only movers with position claims made stale

**10. `7296073641964` (79.4/B→71.4/B)** — rowVerdict `...ומוריד את הציון לגבול ה-B.` → `...ומוריד את הציון.`
   "לגבול ה-B" described 79.4 sitting at the upper B edge next to the A cutoff; 71.4 is mid-B
   (candidate B range 65.1–76.1) — the boundary claim is stale in both directions. Kept the causal driver.
**11. `7290108509106` (A, 80.3 unchanged, rank 8→3)** — rowVerdict `בולגרית 13% שמגיעה לראש המדף בזכות...` → `בולגרית 13% שמתבלטת בזכות...`
   Rank-check vs new ranks: rank 3/36 with 554457/554532 above at 82.7 — "reaches the top of the
   shelf" fails (it also failed in live at rank 8; noting the pre-existing origin). Kept the verified
   sodium superlative: 720mg = min of the fat≥13 subset (next 770).
**12. `7290102393718` (חלומי בקר, 63.6/C unchanged, rank 31→25)** — rowVerdict `...הצפיפות הקלורית היא מה שמוריד לתחתית ה-C.` → `...הצפיפות הקלורית היא מה שמוריד אותה ל-C.`
   Position check vs the NEW C group (13 products, 64.8–50.9): 63.6 is 4th–6th of 13, upper third —
   "לתחתית ה-C" fails. Calorie-density driver kept (356 kcal = max of all 36, verified).

### Claims re-verified and deliberately kept

- `554457`/`554532` (A, now tied rank 1): `הנתרן הנמוך ביותר בין כל גבינות ה-A` — A set is now
  {554457, 554532, 7290108509106} at 600/600/720mg; the claim is still true (tied lowest).
- `7290108509106` insightLine sodium superlative (720mg lowest among full-fat) — verified true, kept.
- `7290114312486` (D, rank 36): `הציון הנמוך ביותר בין הבולגריות` — 47.1 < 47.9 (7290114312707); still true.
- `7290017065663`: `מה שמוריד אותה מה-A` — evergreen gap-to-A explanation for a B product; not a stale self-citation.
- `4861360`: `החלבון עוזר לשמור על B` — stays B (74.5); true.
- `7290108509755`: `מה שמחזיק אותה ב-B` — stays B (65.7); true.
- `3075805`: `הנתרן הגבוה ביותר במדף` (1,628mg) — verified max of all 36; true.

### Flagged for gate 2 (pre-existing live-copy items, NOT touched — truth unchanged by this rescore)

- `369617` rowVerdict: `8 גרם חלבון בלבד, הנמוך בין גבינות השמן` — "גבינות השמן" appears to be a
  one-member group (itself). Pre-existing live phrasing.
- `7290102393718` rowVerdict: `28 גרם שומן ו-356 קק"ל ... הגבוהים בקטגוריה` — 356 kcal is the max
  but 28g fat is 2nd (369617 has 31g). Pair-claim looseness is pre-existing live copy.
- `7290019635826` rowVerdict keeps live's `הרשימה הקצרה ביותר האפשרית` (3 items) while `3075805`
  has 2 ingredients; defensible as "shortest possible [for a preserved brined cheese]" but gate 2 should rule.

## Gate results (after edits; `--baseline` = WORKTREE live file)

```
python 03_operations/page_generator/gates/run_gates.py _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
```

| Gate | Status | Note |
|---|---|---|
| G1 SCHEMA | FAIL | Pre-existing live debt (comparisonContext / satFat / limitingFactors) — unchanged from P461 |
| G2 COVERAGE | PASS | |
| G3 SCOPE | FAIL | Pre-existing (12 scored-not-displayed barcodes) — unchanged from P461 |
| G4 OFF | PASS | |
| G5 GRADE-INTEGRITY | PASS | unchanged |
| **G6 COPY-SAFETY** | **PASS** | 0 violations after edits |
| **G7 PARITY** | **PASS** | **14 grade changes** vs worktree-live — the required count, unchanged by copy edits; avg chars/product 354 vs 353 (+0 rounded) |
| G8 DATA-SANITY | PASS | |

## Self-check: scope discipline

- 0/36 products show score/grade/rank drift vs the pre-edit rebuilt-candidate snapshot.
- Enumerated ALL copy fields diverging from worktree-live: exactly the 12 fields in this log —
  set-equality verified programmatically (`divergence == edit log: True`).
- No `C:\Bari` data file was read for any diff or fact in this re-pass (corpus path for run_gates
  `--corpus` is the shared BSIP1 input store, per the P459/P461 contract invocation; all
  score/grade/copy baselines came from the worktree).

```json
{
  "task": "TASK-449 content gate 1 re-pass",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json", "action": "modified (copy fields only: 9 products / 12 fields)", "note": "gitignored — this log is the record of the diff"},
    {"path": "tasks/returns/T449_content_gate2run.md", "action": "created"}
  ],
  "counts": {
    "grade_movers_derived": "14/36 (independent diff, candidate vs worktree-live sha 5320025746...; A:8/B:21/C:6/D:1 -> A:3/B:18/C:13/D:2; matches P461 and G7)",
    "score_movers_derived": "24/36 (0 upward)",
    "rank_movers_derived": "34/36",
    "products_edited": "9/36 (regex stale-token + superlative/position scan, every hit adjudicated vs facts table + ON-ON traces)",
    "fields_edited": "12 (4 insightLine + 8 rowVerdict)",
    "edits_dropped_vs_first_pass": "2 products (7296073641957, 2107798 — stay B in the corrected basis; their live grade citations are true again)",
    "copy_divergence_equality": "12/12 (fields diverging from worktree-live == edit log, set-verified)"
  },
  "commands_run": [
    {"cmd": "sha256 checks on baseline + candidate (match coordinator/P461)", "exit_code": 0},
    {"cmd": "python scratchpad/analyze3.py (independent movement diff vs worktree-live)", "exit_code": 0},
    {"cmd": "python scratchpad/edits_v3.py + edit12.py (12 field edits, exact-old-text asserted)", "exit_code": 0},
    {"cmd": "python scratchpad/verify_scope_v3.py (0 data drift; divergence==log)", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json", "exit_code": 1}
  ],
  "not_done": [
    "G1/G3 pre-existing schema/scope debt (not a content fix)",
    "3 pre-existing live-copy claims flagged above for gate 2 ruling (369617 oil-cheese group; 7290102393718 fat pair-claim; 7290019635826 shortest-list phrasing)",
    "Adversarial QA / Red-Team gate 2 review; owner sign-off; PR/deploy (out of scope)"
  ],
  "self_check": "run_gates exit 1 driven only by pre-existing G1/G3; G5/G6/G7/G8 PASS; G7 reports exactly 14 grade changes; 0/36 data-field drift; copy divergence set == edit log"
}
```
