# Hummus Confidence-Label Hardening — TASK-129D

**Task:** TASK-129D (child of TASK-129) · **Owner:** nutrition-agent · **Date:** 2026-06-01
**Implements:** `confidence_reaudit_launch_v1.md` §3 **P0 #1** (confidence-gate hardening), Hummus slice.
**Constraints honored:** no score/grade change · confidence labels only · `run_hummus_002` frozen.
**Artifact:** `02_products/hummus/frontend/harden_hummus_confidence_v1.py` (deterministic, idempotent).
**Operates on:** `bari-web/src/data/comparisons/hummus_frontend_v3.json` (+ workspace mirror).

---

## 1. The gate defect (recap)
Launch-Definition §5: `verified` iff (≥3/6 nutrition fields present **AND** ingredients present).
It is **presence-based** — it never checks that the ingredients field is a *real ingredient
list*, so an OCR'd nutrition-panel dump or a bare allergen line can pass as `verified`.

**Fix:** a deterministic ingredient-quality detector. A row stays `verified` only if its
ingredients read as a genuine list (named additive class — `חומר משמר`/`מווסת חומציות`/`מייצב`…,
or structured comma/parenthetical/percentage markers). Nutrition-panel dumps and bare
allergen lines **fail → `partial`**. Display-label only; no signal/score change.

## 2. What the re-audit's "~15 marketing-prose verified" actually were
The re-audit counted against its **66-row file view**, which predates the **page-level
exclusions** the hummus route applies (TASK-087: NOVA-1 whole-chickpea + non-spread removed;
vegetable spreads routed to their own page). Re-running a *proper* detector (not a coarse
substring sweep) over the file finds **5** genuine gate-failures — and **all 5 are already
excluded from the displayed hummus shelf**:

| id | name | score/grade | ingredients field | on hummus page? |
|---|---|---|---|---|
| bsip1_7296073733324 | חומוס | 86/A | `100% חומוס עלול להכיל גלוטן חיטה` (allergen line) | ❌ excluded (NOVA-1) |
| bsip1_7296073733331 | חומוס ענק | 86/A | `100% חומוס עלול להכיל גלוטן חיטה` (allergen line) | ❌ excluded (NOVA-1) |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 85/A | nutrition-panel OCR dump | ❌ excluded (NOVA-1) |
| bsip1_7296073006015 | חומוס גדול שופרסל | 85/A | nutrition-panel OCR dump | ❌ excluded (NOVA-1) |
| bsip1_3643820 | חומוס ענק | 85/A | `חומוס ענק עלול להכיל גלוטן חיטה` (name+allergen) | ❌ excluded (NOVA-1) |

The audit's larger "~15" tally was inflated by (a) these excluded NOVA-1/non-spread rows and
(b) substring false positives (`טרי` inside `ציטרית`; `עשיר ב` echoing product names) on rows
that are, in fact, fully structured ingredient lists.

## 3. Displayed-shelf audit (the rows consumers see: 37; 35 verified)
- **Ingredient quality:** every one of the 35 displayed `verified` rows carries a genuine,
  structured ingredient list (e.g. `חומוס מבושל 61% (מים, חומוס, מווסת חומציות…), טחינה גולמית,
  חומר משמר (פוטסיום סורבט)`). **0 fail** the hardened ingredient-quality gate.
- **Nutrition half:** all 35 meet ≥3/6 (28 rows = 3/6 → energy+protein+sodium; 7 rows = 4/6
  → +fiber). fat suppressed (HUM-001), sugar absent (HUM-002). **0 fail.**
- **Net: 0 displayed hummus rows are over-verified.** The TASK-087 exclusion list already
  removed every quality-gate failure before display.

## 4. Relabeling applied (before / after)

| confidence | file before | file after | displayed before | displayed after |
|---|---:|---:|---:|---:|
| verified | 58 | **53** | 35 | 35 |
| partial | 6 | **11** | 2 | 2 |
| insufficient | 2 | 2 | 0 | 0 |

- **5 rows relabeled `verified → partial`** — all in the excluded set (§2). Done for corpus
  consistency / defense-in-depth: if the exclusion list ever changes, these can no longer
  re-enter as false-`verified`. **Consumer-facing distribution is unchanged (before == after).**

## 5. Score impact
**None.** Script asserts `before_scores == after_scores` (id → (score, grade)) and aborts on any
movement. Git diff of the shipped JSON: only `"confidence"` keys moved (10 lines = 5×2); zero
`"score"`/`"grade"` lines changed. `run_hummus_002` untouched. `_meta.score_statistics` unchanged.

## 6. Activation recommendation — `HUMMUS_V2_SLICE`

**GO** (confidence-label dimension).

TASK-128D held activation because *"promoting confidence to the row header amplifies P0 #1
(~15 over-verified marketing-prose rows)."* That risk **does not materialize on the displayed
hummus shelf**: 0 of 35 displayed `verified` rows fail the hardened gate; the genuine failures
were already excluded. With the 5 excluded rows relabeled, the corpus is internally consistent
with the hardened §5 gate. Hummus confidence labels are defensible at row-header prominence.

**Remaining (non-blocking, not this task):** QA mobile + `lg` re-baseline (QA-owned, independent
of confidence); P1 #5 `fat_quality` re-run (post-launch; internal scoring-confidence, not the
display label). Final flag flip is the Central Controller's call.

## 7. Reproducibility / build order
`harden_hummus_confidence_v1.py` is the **authoritative final confidence pass** for the hummus
corpus and must run **after** `build_hummus_explanation_v1.py` (which regenerates v3 and copies
`confidence` verbatim from v2). It is idempotent — re-running on its own output relabels 0.
