# TASK-449 — Content Agent, Gate-2 fix pass (RT-1 / RT-2 / RT-3, single atomic pass)

**Status proposed:** RETURNED (for targeted Adversarial-QA re-verify per gate-2 GO_WITH_FIXES routing)
**Worktree:** `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`)
**Input:** `tasks/returns/T449_redteam_gate2.md` (commit `48c04507`) — verdict GO_WITH_FIXES; RT-1 CRITICAL, RT-2 CRITICAL, RT-3 HIGH assigned here.
**Appends to:** `tasks/returns/T449_content_gate2run.md` (commit `1c0f0223`).

## RT-1 (CRITICAL) — `_meta.grade_distribution` regenerated from final products

File: `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` (gitignored; this log is the record).

- Old: `{A:8, B:21, C:6, D:1}` (carried from live, stale after 14 grade drops)
- New: `{A:3, B:18, C:13, D:2}` — **derived programmatically**: `Counter(p["grade"] for p in products)` over the final 36-product array (matches gate 2's independent count exactly).
- Audit trail added: `_meta.p461_construction.grade_distribution_regenerated = "2026-07-02 (RT-1: derived from final products array)"`.
- Rest of `_meta` audited against the products array: `product_count=36` ✓ (== len(products)), `scored_count=36` ✓; `reflow` block is historical de-anchor provenance (accurate for worktree-live, left as history); no other product-derived field found stale.

Deriving command (script `fix_rt1_rt3.py`, run from worktree root, exit 0):
```python
from collections import Counter
actual = dict(Counter(p['grade'] for p in d['products']))   # -> {'A':3,'B':18,'C':13,'D':2}
d['_meta']['grade_distribution'] = {g: actual[g] for g in ('A','B','C','D','E') if g in actual}
```

## RT-2 (CRITICAL) — FAQ JSON-LD rebuilt from the candidate

File: `bari-web/src/data/seo/brined_cheeses_faq_schema.json` (tracked — committed with this log). Wired into the live route via `bari-web/src/app/hashvaot/brined-cheeses/page.tsx` → `faqKey="brined_cheeses"`.

**Method (systematic, not artisanal):** regenerated with the real deterministic generator, then a logged re-author pass:
1. `python 03_operations/seo/generate_faq_schema.py --input _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --category-he "גבינות מלוחות" --url https://bari.digital/hashvaot/brined-cheeses --out bari-web/src/data/seo/brined_cheeses_faq_schema.json` (invoked via a Python runner to keep the Hebrew arg uncorrupted by the Windows shell; ran AFTER RT-1 so the generator read the corrected candidate).
2. Re-author pass (below), then programmatic claim verification.

**Every factual claim, old → new (derived from candidate):**

| Claim | Old (live schema) | New | Derivation |
|---|---|---|---|
| A-count (Q2) | "9 מוצרים קיבלו ציון A" (and listed only 8 — self-inconsistent) | "3 מוצרים קיבלו ציון A" | `len([p for p in products if grade=='A'])` = 3 |
| A-list names (Q2) | 8 named products, incl. now-B `7290019635826`, `7290102397334`, `2133162`, `7296073641940`, `7290011499303`, `7290011499112(!)` | exactly `גבינה צפתית 5% שומן`, `גבינה צפתית מעודנת 5%`, `קוביות בולגרית מעודנת 13%` | the 3 A-grade products (554457, 554532, 7290108509106); verified 0 non-A names present |
| Top score (Q1, Q3, Q4) | "85/100" | "83/100" | top candidate score 82.7 (554457/554532 tie) at display precision — page renders `Math.round(score)` (`bari-grade-badge.tsx:41`); `hebrew_readability` flags raw decimals as score-mechanic leakage (its run on the generator's "82.7" output is what forced the rounding) |
| Min score (Q3) | "46/100" | "47/100" | min candidate score 47.1 (7290114312486), display-rounded |
| Product count (Q3, `_bari_meta`) | Q3 said 36 but `_bari_meta.product_count` said 48 | 36 in both | `len(products)` = 36 |
| Top-product insight quotes (Q1, Q4) | old insightLines | current candidate insightLines (unchanged lines, re-verified true: 554457's "הנתרן הנמוך ביותר בין כל גבינות ה-A" holds — A set sodium 600/600/720) | quoted from candidate fields |
| `_bari_meta.source_version` | `brined_cheeses_frontend_v2.json` | `brined_cheeses_candidate_brinedfix.json` | honest provenance: this schema was built from the candidate; regenerate at promotion if the filename changes |

**Re-author pass (Hebrew, on generator output — full old→new in the JSON block below):**
- Q1 + Q4: gender agreement — `גבינה ... קיבל` → `קיבלה` (3 occurrences; hard grammar-gate item).
- Q1: added tied-top honesty clause `, בציון זהה לגרסה המעודנת שלה` — 554532 holds the identical 82.7/A; an unqualified single-product "highest score" claim would be incomplete one-read.
- Score display rounding (as in the table above).
- `hebrew_readability` on all 4 answers + the RT-3 line after edits: **5/5 `is_clean=True`** (pre-rounding it failed 3/5 on decimal leakage — caught and fixed).

**Programmatic claim verification (verify_faq script, exit 0):** 24 checks + 10 re-checks after rounding, **0 failures** — no `85/100` / `46/100` / `9 מוצרים` / raw decimals anywhere in the file; A-count, A-names (and absence of any non-A name), top/min display scores, both insight quotes, meta counts all match the candidate.

**Standing item routed onward (not fixed here):** the generator emits raw decimal scores (`{top_score}/100`) — any category with non-integer scores would leak decimals again. Routes to data-agent as a generator fix (`generate_faq_schema.py:54,91,103`); this pass corrected the brined output.

## RT-3 (HIGH) — `7290019635826` false "shortest list possible" superlative

- Old: `פטה עיזים 5% מעודנת מחלבות גד עם הרשימה הקצרה ביותר האפשרית: חלב עיזים מפוסטר, מלח, חומר משמר אחד. ...`
- New: `פטה עיזים 5% מעודנת מחלבות גד עם רשימה קצרה: חלב עיזים מפוסטר, מלח, חומר משמר אחד. ...` (rest unchanged)
- Ruling applied: displayed `3075805` has 2 ingredients (חלב, מלח) vs this product's 3, and both are brined cheeses — the superlative is indefensible. **Dropped rather than rescoped**: rank-check across all 36 shows 3-ingredient lists are common on this shelf (near-mode), so no honest superlative exists here; plain `רשימה קצרה` (3 items vs shelf max 10) is unimpeachable and keeps the insight.

## Gate results after the pass (baseline = worktree-live)

```
python 03_operations/page_generator/gates/run_gates.py _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
```
G1 FAIL / G3 FAIL (pre-existing live debt, per gate 2's own ruling — fails on live too) · G2 PASS · G4 PASS · **G5 PASS · G6 PASS · G7 PASS with exactly 14 grade changes** · G8 PASS. Run AFTER RT-1+RT-3 (the FAQ file is not a gates input).

## Self-check: scope discipline

- **0/36** products show score/grade/rank drift vs the pre-edit snapshot (programmatic).
- Copy-divergence set vs worktree-live is **unchanged at the same 12 (barcode, field) pairs** — RT-3 re-edited an already-diverging field; set-equality vs the edit log re-verified `True`. `_meta.grade_distribution` is the only additional diff, explicitly ordered by RT-1.
- No engine/score/rank change; no push/PR/deploy; `C:\Bari` read-only (gates `--corpus` reads the shared BSIP1 input store per the established contract invocation).
- Correction to my gate-2 log's informational self-count (flagged by QA): the 12 copy fields split **3 insightLine + 9 rowVerdict**, not "4+8" as mislabeled there; the enumerated field list was and remains correct.

```json
{
  "task": "TASK-449 content gate-2 fix pass (RT-1/RT-2/RT-3)",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json", "action": "modified (RT-1 _meta.grade_distribution + audit note; RT-3 one rowVerdict)", "note": "gitignored — this log is the record"},
    {"path": "bari-web/src/data/seo/brined_cheeses_faq_schema.json", "action": "regenerated from candidate + re-authored (RT-2)", "note": "tracked; committed with this log"},
    {"path": "tasks/returns/T449_content_gate3run.md", "action": "created"}
  ],
  "counts": {
    "rt1_grade_distribution": "A:3 B:18 C:13 D:2 (Counter over final 36 products; == gate-2 independent count; old A:8 B:21 C:6 D:1)",
    "rt2_claims_rebuilt": "7 claim groups (A-count 9->3, A-list 8-named->3-named with 0 non-A names, top 85->83/100, min 46->47/100, meta product_count 48->36, source_version -> candidate, insight quotes -> current)",
    "rt2_verification": "24+10 programmatic claim checks, 0 failures; hebrew_readability 5/5 is_clean after rounding fix (3/5 before — decimal leakage caught)",
    "rt3_superlative": "dropped (3075805 displays 2 ingredients vs 3; no honest shortest-superlative exists — 3-ingredient lists are near-mode on shelf)",
    "gates": "G5/G6/G7/G8 PASS, G7 = exactly 14 grade changes; G1/G3 pre-existing (fail on live too)",
    "drift": "0/36 score/grade/rank; copy-divergence set unchanged (12 fields, set == log)"
  },
  "commands_run": [
    {"cmd": "python scratchpad/fix_rt1_rt3.py (RT-1 Counter derivation + RT-3 edit, exact-old-text asserted)", "exit_code": 0},
    {"cmd": "python 03_operations/seo/generate_faq_schema.py --input _rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json --category-he \"גבינות מלוחות\" --url https://bari.digital/hashvaot/brined-cheeses --out bari-web/src/data/seo/brined_cheeses_faq_schema.json (via Python runner for Hebrew arg)", "exit_code": 0},
    {"cmd": "python scratchpad/reauthor_faq.py + round_faq.py (logged re-author: gender agreement, tied-top clause, display rounding)", "exit_code": 0},
    {"cmd": "python scratchpad/check_readability.py (hebrew_readability on 4 FAQ answers + RT-3 line)", "exit_code": 0},
    {"cmd": "python scratchpad/verify_faq.py + inline re-verify (34 claim checks vs candidate)", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py <candidate> --corpus C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output --run _rescore_staging/brined_cheeses/products --baseline bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json", "exit_code": 1},
    {"cmd": "python scratchpad/verify_scope_v3.py (0/36 drift; divergence set == log)", "exit_code": 0}
  ],
  "not_done": [
    "generate_faq_schema.py decimal-leakage generator fix (routed to data-agent; brined output corrected here)",
    "RT-4/RT-5 MEDIUM pre-existing loose claims (routed to content-agent as standing items by gate 2, not in this fix scope)",
    "targeted Adversarial-QA re-verify (next step per GO_WITH_FIXES); owner sign-off, PR, deploy (out of scope)"
  ],
  "self_check": "RT-1 distribution == Counter over products == gate-2 count; RT-2 FAQ passes 34 programmatic claim checks + readability 5/5; RT-3 superlative dropped and rank-checked; G5/G6/G7 PASS with G7=14; 0/36 drift"
}
```

## Full old → new record (all 8 field changes this pass)

**RT-1 — `_meta.grade_distribution`:** `{A:8,B:21,C:6,D:1}` → `{A:3,B:18,C:13,D:2}`; plus audit field `p461_construction.grade_distribution_regenerated = "2026-07-02 (RT-1: derived from final products array)"`.

**RT-3 — rowVerdict 7290019635826:**
- Old: `...עם הרשימה הקצרה ביותר האפשרית: חלב עיזים מפוסטר, מלח, חומר משמר אחד...`
- New: `...עם רשימה קצרה: חלב עיזים מפוסטר, מלח, חומר משמר אחד...`

**RT-2 — FAQ (after generator regeneration; re-author deltas):**
- Q1 old (generator): `גבינה צפתית 5% שומן קיבל את הציון הגבוה ביותר — 82.7/100 (ציון A). הנתרן הנמוך ביותר בין כל גבינות ה-A — ורק שלושה רכיבים.`
- Q1 new: `גבינה צפתית 5% שומן קיבלה את הציון הגבוה ביותר — 83/100 (ציון A), בציון זהה לגרסה המעודנת שלה. הנתרן הנמוך ביותר בין כל גבינות ה-A — ורק שלושה רכיבים.`
- Q2 (generator, unchanged by re-author): `3 מוצרים קיבלו ציון A: גבינה צפתית 5% שומן، גבינה צפתית מעודנת 5% ו-קוביות בולגרית מעודנת 13%.` (old live: `9 מוצרים קיבלו ציון A: [8 names incl. now-B products]`)
- Q3 old (generator): `...הציון הגבוה ביותר הוא 82.7/100 והציון הנמוך ביותר הוא 47.1/100.` → Q3 new: `...הציון הגבוה ביותר הוא 83/100 והציון הנמוך ביותר הוא 47/100.` (old live: `85/100` / `46/100`)
- Q4 old (generator): `גבינה צפתית 5% שומן קיבל 82.7/100, גבינה צפתית מעודנת 5% קיבל 82.7/100. ...` → Q4 new: `גבינה צפתית 5% שומן קיבלה 83/100, גבינה צפתית מעודנת 5% קיבלה 83/100. ...` (insight quotes unchanged, verified current)
