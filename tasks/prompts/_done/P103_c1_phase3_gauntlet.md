# P103 — TASK-278 Phase-3: No-Regression Gauntlet (route: C1)
# Data Agent — Combined shelf-relative flag-off + PHVO no-regression

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS)
**Engine:** `03_operations/bsip2/proto_v0/src/score_engine.py` (uncommitted — shelf-relative mechanism)

---

## Context

The engine has TWO classes of uncommitted/committed changes to verify:

### A. Shelf-relative mechanism (UNCOMMITTED, BARI_SHELF_RELATIVE_V1)
- Added by P99 to `score_engine.py` and `constants.py`
- `BARI_SHELF_RELATIVE_V1=off` by default (env var)
- When off, must be structurally byte-identical to the current committed engine
- Scope: `SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit"})` (only biscuit category, only when flag on)

### B. PHVO changes (COMMITTED, Fix-B + Fix-C, attributed to TASK-275)
- Fix-B: `signal_extractor.py` — added PHVO markers (מרגרינה, שומנים מוקשים, מחמאה, מוקשה variants)
- Fix-C: `score_engine.py` — `fat_quality` dimension ceilinged at 40 when `has_phvo=True`
- These fire on ANY product containing hardened/hydrogenated fats or margarine
- **Governance gap**: committed without D7 co-sign or EV registration

---

## Your task

### Gate 1: Shelf-relative flag-off byte-identical

For each of the 11 live published categories, run the CURRENT engine (committed PHVO + uncommitted shelf-relative with flag OFF) and compare to the reference run:

| Category | Reference run | Reference run path |
|---|---|---|
| Milk (frozen invariant) | run_005_headpin | `02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/` |
| Brined cheeses | run_brined_004 | `02_products/brined_cheeses/bsip2_outputs/run_brined_004/` |
| Hard cheeses | last scored run | `02_products/hard_cheeses/bsip2_outputs/` (most recent) |
| Cheese spreads | last scored run | `02_products/cheese_spreads/bsip2_outputs/` |
| Bread | last scored run | `02_products/bread/bsip2_outputs/` |
| Yogurts | last scored run | `02_products/yogurt_system/bsip2_outputs/` |
| Cereals | last scored run | `02_products/breakfast_cereals/bsip2_outputs/` |
| Granola | last scored run | `02_products/granola/bsip2_outputs/` |
| Salty snacks | last scored run | `02_products/salty_snacks/bsip2_outputs/` |
| Hummus | last scored run | `02_products/hummus/bsip2_outputs/` |
| Butter | last scored run | `02_products/butter/bsip2_outputs/` |

**Test**: For each category, run scoring with `BARI_SHELF_RELATIVE_V1=off` (or not set) and compare scores to the reference run. A PASS is: every product's `final_score_estimate` matches the reference run within floating-point rounding (≤0.01 pts tolerance). A FAIL is: any product with score delta > 0.01 or grade change.

**BUT**: The reference runs were scored by an older engine (before Fix-B/Fix-C PHVO commit). If the current engine gives different scores even with flag-off, that's a PHVO REGRESSION (not a shelf-relative issue) → report separately (see Gate 2).

**If any score difference is found with flag-off:**
- Is it consistent with PHVO firing? (product contains margarine/hydrogenated fat in ingredients?) → PHVO regression, not shelf-relative (report in Gate 2)
- Is it unexplained? → STOP, report as CRITICAL regression, do not proceed

### Gate 2: PHVO no-regression audit

For the categories AT RISK of PHVO firing (products may contain margarine/hydrogenated oils):
- **Bread** (industrial breads often contain margarine)
- **Cereals / Granola** (some granola bars use hydrogenated oils)
- **Salty snacks** (some crackers use shortening)
- **Vegetable spreads / Hummus** (some non-pure hummus has margarine)
- **Butter** (check: some "butter blends" have margarine component)

For each at-risk category:
1. Look through the published frontend JSON (`bari-web/src/data/comparisons/`) for any product whose ingredient string contains: מרגרינה, שומנים מוקשים, שומן מוקשה, שומן צמחי מוקשה, partially hydrogenated
2. If any such products exist in the live corpus → compare their scores under current engine vs reference run
3. If grade changes occur → flag as PHVO GOVERNANCE REGRESSION (committed engine is live but its effect on published products hasn't been authorized)

**Safe categories (no hardened fats expected):**
- Milk, Yogurts, Brined cheeses, Hard cheeses, Juices → skip Gate 2 for these

### Gate 3: engine_invariants 342 PASS

Run:
```
python 03_operations\bsip2\proto_v0\shadow\engine_invariants.py
```
Must pass all 342 invariants. This confirms the PHVO + shelf-relative additions don't break any invariant.

---

## Definition of Done

- [ ] Gate 1: shelf-relative flag-off tested on all 11 live categories; PASS = byte-identical (≤0.01 pts); any delta reported
- [ ] Gate 2: PHVO at-risk categories audited; list of any products with PHVO markers in live corpus + whether scores changed; any grade regressions flagged as GOVERNANCE REGRESSION
- [ ] Gate 3: engine_invariants 342 PASS
- [ ] Summary table: category | gate1_result | phvo_products_found | grade_regressions | notes

---

## Constraints

- **OFF ban absolute** — no Open Food Facts anywhere
- **DO NOT rescore anything** — this is read-only verification, not a scoring run
- **DO NOT commit anything** — report only, no git writes
- **DO NOT modify any published frontend JSON** — read only
- **STOP on any unexplained regression** — unexplained = score changes that aren't attributable to PHVO and aren't in scope for shelf-relative
- Agent does NOT decide go/no-go — orchestrator evaluates the gate

---

## Return format

End with machine-readable contract:
```json
{
  "task_id": "TASK-278",
  "phase": "Phase-3 gauntlet",
  "status": "RETURNED",
  "return_date": "...",
  "agent": "data-agent",
  "gate1_shelf_relative": {
    "categories_tested": [...],
    "pass": true/false,
    "regressions": []
  },
  "gate2_phvo_audit": {
    "at_risk_categories_checked": [...],
    "phvo_products_in_live_corpus": [],
    "grade_regressions": [],
    "governance_gap": true/false
  },
  "gate3_invariants": {
    "pass": true/false,
    "count": 342
  },
  "overall_verdict": "PASS|FAIL|CONDITIONAL",
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
