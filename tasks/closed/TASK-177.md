---
id: TASK-177
title: "Cheese verdicts — surface the added-sugar / clean-label reason behind unintuitive cottage (and white-cheese) ordering (R1 from TASK-176, display-only copy)"
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
depends_on: [TASK-176]
blocks: []
category_id: cheese
work_type: content
roadmap_impact: false
resolution: "Close-readiness gate PASSED (independently verified). 9 insightLine verdicts rewritten in cheese_frontend_v2.json (3 cottage + 6 white-cheese) to name the added-sugar (סוכר) / clean-label reason behind the backwards-looking 9%-over-5% ordering. git diff = exactly 9 insertions / 9 deletions, ALL insightLine — no score/grade/_aCappedToB/engine field touched (verified). Every added-sugar claim re-checked against run_cheese_004 traces (added_sugar_sources_count/added_sugar_matches): cottage 77/75 = 1 ['סוכר'], 9%s = 0; white-cheese che-2824183/2824640/7290114311472 = 1, che-4127817/47942 = 0 — all match. Sugar cited as ingredient presence, never grams (display sugar null, grounding_v1 cheese rule). Upstream build script correctly left untouched (emits placeholders only; JSON is the authoritative authored layer). tsc exit 0."
summary: >
  R1 follow-up from TASK-176. The cheese page has an ordering that reads backwards to a shopper —
  a 9%-fat cottage (81/B) sits above two 5%-fat cottages (77/B, 75/B). TASK-176 proved this is
  food-science-correct, NOT a bug: the two low 5%s each declare added sugar (סוכר → NOVA-3 + HP
  penalty) while the 9%s have a clean label (no added sugar). The current verdicts don't tell the
  shopper that, so the ranking looks arbitrary. Fix is display-only copy: name the added sugar in
  the cheap-5% verdicts, and convey the 9%'s clean-label advantage (while keeping its existing
  saturated-fat B-cap reasoning). No score change, no D7 required.
---

# TASK-177 — Surface the added-sugar reason in cheese verdicts (R1)

## Why
TASK-176 (CLOSED, KEEP engine) confirmed the cottage ordering is correct but **opaque**: the
ranking is driven by added sugar in the cheap 5%s, which the verdicts never mention. Making the
real reason visible is the honest, zero-score-cost fix.

## Verified grounding (from run_cheese_004 traces — do not re-derive, but you may re-verify)
| product | id | score | added_sugar_sources | note |
|---|---|---|---|---|
| קוטג' 9% שומן | che-4127336 | 81/B | **0** (clean) | capped at B by sat-fat (existing copy) |
| קוטג' מהדרין 9% שומן | che-41452 | 81/B | **0** (clean) | same |
| קוטג' 5% (77) | che-7290114310918 | 77/B | **1 — "סוכר"** | sits below the 9% |
| קוטג' 5% שומן (75) | che-7290011194246 | 75/B | **1 — "סוכר"** | sits below the 9% |
| קוטג' 5% שומן | che-4127329 | 87/A | 0 (clean) | correctly above 9% |
| קוטג' 5% שומן | che-2868996 | 84/A | 0 (clean) | correctly above 9% — the proof |

## Scope
1. **Cheap 5% cottages (77, 75):** the verdict should name that they declare **added sugar (סוכר)** — that's why they sit below leaner-label cheeses. (Trace: `added_sugar_matches: ["סוכר"]`.)
2. **9% cottages (81/B):** convey that they out-rank the sugared 5%s on a **clean label / no added sugar**, while keeping the existing, correct saturated-fat reason for the B-cap. Don't drop the sat-fat catch.
3. **White-cheese / quark:** TASK-176 flagged the same pathology there (a 9% at 75 and 17% at 68 sitting above weaker 5%s). Check those rows; apply the same added-sugar / clean-label clarification wherever an ordering looks backwards AND the trace supports it.

## Guardrails
- **Display-only copy.** No score change, no JSON score/grade edits, no engine touch.
- Ground every claim in the trace's `added_sugar_sources_count` / `added_sugar_matches` — never assert sugar where the count is 0; never invent a value.
- Follow the editorial standards: insight-line spec, the 2-line row-verdict model, grounding_v1, and the row_description_standard (note: TASK-175 just made GO the canonical trace-anchored-catch example — same discipline applies).
- Apply the fix at the correct source layer (cheese_frontend_v2.json `insightLine`, and the upstream cheese build/authoring script if one drives it, so a re-run stays consistent).
- `npx tsc --noEmit` must stay green.
- No closing authority — end with a return block proposing status; orchestrator runs the close-readiness gate.

---

## Work log (Content Agent, 2026-06-03)

**Display-only copy. 9 `insightLine` verdicts rewritten in `bari-web/src/data/comparisons/cheese_frontend_v2.json`. No score/grade/engine touched (all 9 scores/grades re-verified unchanged). `npx tsc --noEmit` = EXIT 0.**

Every added-sugar claim re-verified against `run_cheese_004` traces (`added_sugar_sources_count` / `added_sugar_matches`). Sugar is cited as an **ingredient presence** ("סוכר ברשימת הרכיבים") — never as grams, because displayed `sugar` is `null` for all these rows (grounding_v1 cheese rule).

### Cottage (3 rows)
- **che-4127336 / che-41452 (9%, 81/B)** — added_sugar=0 (clean). New verdict adds the clean-label / no-added-sugar advantage AND keeps the existing sat-fat 5.4g B-cap catch.
- **che-7290114310918 (5%, 77/B)** & **che-7290011194246 (5%, 75/B)** — added_sugar=1 `["סוכר"]`. New verdict names that sugar appears in the ingredient list and that this is why they sit below leaner-label cottages.

### White-cheese / quark (6 rows)
- **che-4127817 / che-47942 (9%, 75/B)** — added_sugar=0 (clean). Old verdict implied 5%s are simply better; rewritten to keep the fat-ratio catch but state they out-rank the **sugared** 5%s on a clean label. (This is the genuine "9% above weaker 5%s" backwards case TASK-176 flagged.)
- **che-2824183 / che-2824640 (5%, 73/B)** — added_sugar=1 `["סוכר"]`. Old verdict blamed "protein slightly below" (wrong reason); rewritten to name the added sugar.
- **che-7290114311472 (5% מהדרין, 75/B)** — added_sugar=1 `["סוכר"]`. Old "protein solid but not standout" reason replaced with the added-sugar reason.

### Deliberately NOT changed
- **che-56272 (5% olives, 72/B)** — added_sugar=0 (clean). Its lower position is olives/flavoring, not sugar; ordering isn't sugar-driven. Left as-is.
- **che-3523230065467 (goat, 68/B)** — added_sugar=1 but its dominant, correctly-cited driver is fat (17g); not a clear backwards-ordering case. Left as-is to avoid over-reach.

### Source layer note
The cheese build script `02_products/cheese_spreads/factory_run_004/build_cheese_frontend_v2.py` only emits **deterministic placeholder** insightLines (its own docstring: "Content Agent WILL REWRITE these"). The rich authored verdicts live only in the JSON, which is the authoritative authored layer. Editing the script would NOT preserve any authored verdict (it would overwrite all of them with placeholders on re-run), so it was correctly left untouched.
