---
id: TASK-139B
title: "Data: extend enricher FERMENTATION_TERMS to Israeli label vocab (credit cultures 0/88 -> detected) + regression-lock"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: [TASK-142, TASK-143]
category_id: null
summary: >
  run_yogurt_003 detected 0/88 fermentation markers because core/ingredient_enricher.py FERMENTATION_TERMS
  only match תרבויות/ביפידובקטריום/לקטובציל, while real Israeli labels write חיידק פרוביוטי/ביפידוס/BIFIDUS/תרבית.
  The yogurt-and-cheese-defining positive is never credited. Extend the term set, regression-lock against the
  golden corpus, and confirm zero movement on frozen milk/bread/snack scores. Governed scoring change.
---

# TASK-139B — Enricher culture-vocabulary fix

## Change
Extend `FERMENTATION_TERMS` in `ingredient_enricher.py` (verify current path/line before editing — memory
cites `core/ingredient_enricher.py`) to include the Israeli label vocabulary: `חיידק פרוביוטי`, `ביפידוס`,
`BIFIDUS`, `תרבית`, and common variants. Non-interpretive term matching only — no new scoring rule.

## Guards (hard)
- Golden regression corpus **12/12 PASS** after the change.
- **Frozen invariants unchanged**: milk run_004 (85/A top), bread retail_003, snacks (snk-001 70/B). The term
  set must not newly credit any non-dairy product in a way that moves a frozen score. QA verifies.
- Log to evidence registry with label-observability note + rollback (git revert).

## DoD
Re-run run_yogurt_003 enrichment: cultures now detected on live-culture SKUs (was 0/88); regression green;
frozen scores unmoved. Then propose RETURNED.

---

## Return block — proposed RETURNED (data-agent, 2026-06-01)

**Change (verified path):** `03_operations/bsip1/core/ingredient_enricher.py` → `FERMENTATION_TERMS`
(line ~354). Memory's `core/ingredient_enricher.py` resolves to this monorepo path. Extended with the
observed Israeli label vocabulary — non-interpretive, case-insensitive substring matching; **no new
scoring rule / weight / threshold**:

- generic live-culture phrasings → `live_cultures` (flag `has_live_cultures`):
  `חיידק פרוביוטי`, `חיידקי פרוביוטי`, `חיידקים פרוביוטי`, `חיידקי ביפידוס`, `חיידקי ביפדוס` (OCR variant),
  `חיידקי יוגורט`, `חיידקי אצידופילוס`, `חיידקי אצידופולוס` (variant), `חיידקי bio`
- `תרבית` → `cultures_generic` (singular of the existing `תרבויות`)
- `ביפידוס` / `ביפדוס` / `bifidus` → `bifidobacterium` (same organism category as existing `ביפידובקטריום`)

Also registered the existing `run_yogurt_003` run in `enrich_runner.py` `RUNS` so the fix is reproducible.

**DoD met — culture detection (run_yogurt_003, re-run via `enrich_runner.py --run run_yogurt_003`):**
- `has_live_cultures`: **0/88 → 49/88 (56%)**; any fermentation marker: **51/88 (58%)**.
- Marker categories produced: `live_cultures` 49, `bifidobacterium` 16, `cultures_generic` 1.
- Feeds the already-active **EV-015** fermentation bonus and satisfies **EV-021 RULING-DAIRY-A-01 C3**
  (the "Gap 2" precondition), previously blocked at 0% coverage.

**Hard guards — PASS:**
- Golden regression corpus: **11 PASS / 1 WARN / 0 FAIL** (`run_regression_check.py`). The lone WARN
  (`anchor_soy_drink` structural-class acceptable-secondary) is **pre-existing and change-independent** —
  the regression reads stored BSIP2 traces + `structural_classifier.py` and never invokes the BSIP1
  enricher edited here, so before == after by construction. No FAIL.
- Enricher unit tests: **64/64 PASS** (`test_enricher.py`), incl. `NV-bar = 0 markers` and `YOGURT_PLAIN`
  unchanged (new `תרבית`/`ביפידוס` are not substrings of `תרבויות`/`ביפידובקטריום`).
- **Frozen invariants unmoved** (QA-grade verification, 3 ways): (1) **collision audit** — 0 new markers
  on every frozen/non-dairy corpus (snacks run_001, bread_light_001, bread_retail_001/003, cereals_001,
  hummus_001, milk_001/002); the one bread match (`לחם הרים`, `מחמצת פרוביוטית`) credits only the
  pre-existing `מחמצת` term. (2) No re-score of any frozen category performed. (3) No frozen published
  score artifact modified by this task (milk run_004 / bread retail_003 / snk-001 untouched; the
  bread/snacks/maadanim frontend diffs in `git status` predate this session, not produced here).

**Evidence registry:** logged **EV-022** (label-observability + before/after coverage + collision audit +
guards + rollback) in both `bsip2_evidence_registry_v1.json` and `.md`.

**Rollback:** `git revert` the `FERMENTATION_TERMS` block in `ingredient_enricher.py` (+ the
`run_yogurt_003` entry in `enrich_runner.py`) → restores prior 0/88 behavior. `run_yogurt_003` BSIP1
output is non-authoritative evidence; re-enrichment is idempotent. Notify: Data Architecture + Nutrition.

**Heads-up (not a guard breach):** the term set is global, so a *future* re-score of **maadanim** (dairy,
live, but NOT one of the frozen-three) would newly credit cultures on ~30 SKUs via EV-015 — correct dairy
behavior, but the live `maadanim_frontend_v2` page would shift if/when re-run. Flagged for Nutrition/Product.

**Residual:** `חיידקי L.casei DN114-001` (1 DanActive-style SKU) unmatched — Latin strain code outside the
task-named vocab; left as a known minor gap, not blocking.

**Scope note:** this delivers culture *detection* only. BSIP2 re-scoring/grade publication for yogurt
remains gated on TASK-139C (A-threshold reconciliation) and is out of scope here. DEC-005 manual shelf
untouched. Only the Central Controller records CLOSED.

---

## CC bookkeeping note — 2026-06-01 (note-in-parent; no reopen)

TASK-139B was CLOSED on BSIP1-only culture *detection* (0/88 → 49/88). Its score-*crediting* DoD (making the
BSIP2 scorer actually credit those cultures) was a separate defect — the scorer reads an INDEPENDENT list
(`signal_extractor.FERMENTATION_MARKERS_HE`), not the enricher's `FERMENTATION_TERMS`. That gap was found and
fixed under the **TASK-139 parent closing re-score** and recorded as **EV-024** (Culture-Credit Propagation
Fix; run_yogurt_003 0/86 → 34/86 credited, 12 SKUs C→B). **Resolution: note-in-parent — TASK-139B stays CLOSED,
NOT reopened**; the crediting work is owned by the (CLOSED) parent and documented in EV-024. No engineering work
outstanding. Recorded per CC audit + operator authorization.
