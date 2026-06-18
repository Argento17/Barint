# P107 — TASK-278 Phase-4: Cereals × Sugar D7 Co-Sign (route: C1)
# Product Agent — Ratify the shelf-relative sugar enrollment for breakfast cereals

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS, Phase 4 D7 co-sign)
**D6 ruling deliverable:** `01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md`
**D7 co-sign template:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Prior D7 example (biscuits):** `01_framework/bsip2_framework/project_rescore/biscuits_d7_cosign_v1.md` (if exists), or `tasks/returns/P101_return.md`
**EV registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`

---

## Context

TASK-278 is the Bari-wide program replacing binary red-label caps with shelf-relative continuous
scoring. The mechanism is fully implemented (`BARI_SHELF_RELATIVE_V1`, default-off behind a flag).
Biscuits pilot CONFIRMED the mechanism is sound; the cookies-coffee shelf is degenerate (floor-saturated)
so biscuits stays with absolute-only scoring. Yogurt diagnostic proved the mechanism LANDS on spread-y
shelves (8 grade changes, 0% absorption).

**Cereals×sugar is Phase 4's first PRODUCTION enrollment.**

**D6 ruling (P106) was ACCEPTED by the orchestrator 2026-06-14.** Verified:
- Stats: n=45, median=14.0g, IQR=11.0, robust_scale=8.896 (confirmed from traces, exact match)
- Router category: `"cereal"`, bleed risk NONE
- Surcharge bands (P_max=6): [0,0.5)→0, [0.5,1.0)→1, [1.0,1.5)→2, [1.5,2.5)→4, [2.5,∞)→6
- Relief bands (B_max=3): [0,0.5)→0, [0.5,1.5)→1, [1.5,3.0)→2, [3.0,∞)→3
- formulation_absolute_floor=62, trigger≥25g sugar
- Anti-Immunity proof: 62+3=65 < 70 (HOLDS)
- Two named inversions verified at file:line (traces confirmed exact)
- EV-087 confirmed free in registry
- NO engine files modified

**One open question from D6 (flagged by Nutrition Agent):**
> "No family budget raise is proposed for cereals (unlike biscuits: `SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6`).
> Rationale: the base `SUGAR_FAMILY_BUDGET` should accommodate a 6pt relative surcharge without
> double-counting since absolute backbone sugar penalties already fired before the relative layer.
> Product Agent should confirm or override."

---

## Your tasks

### 1. Validate the D6 enrollment spec

Read `cereals_sugar_enrollment_v1.md`. For each of the following, confirm or flag:

- **Scope:** "cereal" is the right router category key (no bleed to dairy, no granola confusion)
- **Bands:** P6/B3 asymmetry appropriate for a scale of 8.896 (considerably wider than biscuits 5.115)?
  - Does P_max=6 produce meaningful differentiation without over-penalising borderline products?
  - Does B_max=3 adequately reward genuinely low-sugar cereals (bran/muesli at 0.5g)?
- **Floor:** 62 with trigger ≥25g — is this the right precautionary threshold?
  - High-sugar cereals in corpus max at 39g/100g. Floor=62 means even the most generous relief (+3)
    keeps them at 65 — below B (70). Anti-Immunity holds.
- **Anti-Immunity rule:** High-sugar cereals MUST NOT reach A/B. Confirm the floor+relief math is airtight.

### 2. Resolve the open question: family budget raise

The biscuits enrollment added `SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6` to prevent the 6pt surcharge
from double-counting against the `SUGAR_FAMILY_BUDGET` cap. For cereals:

- Option A: **No budget raise** (Nutrition Agent's recommendation) — the SUGAR_FAMILY_BUDGET is not
  binding on cereals because absolute backbone sugar penalties for cereals are lower (unlike biscuits
  where heavy HP_SUGAR penalties already consumed the budget).
- Option B: **Add SUGAR_CEREAL_BUDGET_RAISE=6** — same as biscuits to avoid any risk of double-counting.

**Make the call.** Recommend one option and state why. This is a binding Product decision.

### 3. Lock the pilot gate criteria

The pilot rescore (Phase 5, measured not published) must pass a gate before any go-live. Define
the criteria that the pilot must satisfy — minimum to accept, maximum that triggers rejection.
Base on the biscuit pilot gate (from D7 co-sign P101) and adapt for cereals. At minimum:
- Min n_movers (how many products should show score movement?)
- Min n_grade_changes
- Max absorption rate (floor-saturation threshold)
- Inversion A corrected (7290100000029 should rank above 5054568100011 after SR)
- Inversion B gap widened (delta ≥ 5.5pts)
- No non-cereal bleed (dairy products score unchanged)
- brined 48/48 byte-identical (invariant)

### 4. Register EV-087

Append to `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`:

```
### EV-087 — Cereals × Sugar Shelf-Relative Enrollment (D7 Co-Sign)
- **Date:** 2026-06-14
- **Task:** TASK-278 Phase 4
- **Decision:** [YOUR RATIONALE]
- **Scope key:** cereal
- **Bands:** Surcharge [0/1/2/4/6] at r=[0,0.5,1.0,1.5,2.5,∞); Relief [0/1/2/3] at r=[0,0.5,1.5,3.0,∞)
- **Floor:** 62 at sugar≥25g
- **Budget raise:** [NONE / SUGAR_CEREAL_BUDGET_RAISE=6]
- **Anti-Immunity:** floor(62) + max_relief(3) = 65 < 70 ✓
- **Pilot gate:** [CRITERIA]
- **File:** `01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md`
```

### 5. Write the D7 co-sign document

Write to: `01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md`

Follow the structure of `shelf_relative_d7_cosign_v1.md` (the design-level D7). Include:
- Scope ratification
- Band ratification (or override)
- Floor ratification (or override)
- Budget raise decision (Option A or B)
- Pilot gate criteria
- Conditions (if any) before pilot launch
- Reference to EV-087

---

## Definition of Done

- [ ] D6 spec validated (scope/bands/floor/anti-immunity each confirmed or flagged)
- [ ] Family budget raise decision made (Option A or B, with rationale)
- [ ] Pilot gate criteria locked (min_movers, min_grade_changes, max_absorption, 2 inversion checks, brined byte-id)
- [ ] EV-087 registered in evidence registry (append only — no edits to prior entries)
- [ ] `cereals_d7_cosign_v1.md` written
- [ ] NO engine files modified
- [ ] NO scores moved
- [ ] OFF ban absolute

---

## Constraints

- **DO NOT modify engine source files** — D7 is governance + ratification only
- **DO NOT run any scoring**
- **OFF ban absolute**
- **No published score changes**

---

## Return format

Write return to `C:\Bari\tasks\returns\P107_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-4 D7 cereals sugar co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "d6_validated": true,
  "d6_issues": [],
  "budget_raise_decision": "none|SUGAR_CEREAL_BUDGET_RAISE=6",
  "budget_raise_rationale": "...",
  "pilot_gate_criteria": {
    "min_movers": <n>,
    "min_grade_changes": <n>,
    "max_absorption_rate": <fraction>,
    "inversion_a_corrected": true,
    "inversion_b_gap_min_pts": <n>,
    "no_dairy_bleed": true,
    "brined_byte_identical": true
  },
  "ev_087_registered": true,
  "ev_087_registry_line": <line_number>,
  "deliverable": "01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md",
  "engine_files_modified": false,
  "off_ban_satisfied": true,
  "not_done": [],
  "artifacts": [
    {"path": "01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md", "action": "created"},
    {"path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md", "action": "modified", "line_appended": <n>}
  ]
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
