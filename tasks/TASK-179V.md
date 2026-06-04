---
id: TASK-179V
title: "Glass Box W2 — QA: OFF byte-identity + additive panel integration + mobile QA"
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179S, TASK-179T, TASK-179U]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
---

# TASK-179V — Glass Box W2: QA gate

Part of TASK-179 (Glass Box), Wave 2. Runs after TASK-179S (engine), TASK-179T (frontend),
and TASK-179U (Hebrew copy). This is the final gate before W2 ships to the pilot pages.

**QA is the closing authority witness here.** CC closes this task only after QA's
independent verification confirms all 4 checks below pass.

## Checks

### Check 1 — Engine OFF byte-identity
Run `verify_glassbox_w2_off_identical.py` (TASK-179S deliverable) independently.
- Command: `BARI_GLASSBOX_W2=off python verify_glassbox_w2_off_identical.py`
- Expected: `PASS — 0 diffs` across the pilot corpus (hummus + maadanim).
- Failure = TASK-179S must return with a fix; QA reopens that task before proceeding.

### Check 2 — Engine ON output sample
Run the engine with `BARI_GLASSBOX_W2=on` on the pilot corpus.
Verify:
1. `d4_additives` is present in the output for products with ingredient text.
2. Every entry has: `e_number`, `name_he`, `tier`, `function_he`, `match_source`.
3. Tier values are all from the allowed set (functional / likely-neutral / dose-dependent /
   contested / disclosure-gap / unclassified / confirmed-negative).
4. No `score`, `grade`, or `gate` field is changed vs the OFF output.
5. Sample at least 10 products (5 hummus + 5 maadanim) with non-empty `d4_additives`.
   Record findings summary in the return block.

### Check 3 — Frontend visual QA
On the comparison pages for hummus and maadanim (local dev server):
1. **Collapsed state:** Additive panel entry point renders — `X תוספים — הצג פירוט`.
   For products with 0 additives, empty state renders — `לא זוהו תוספי מזון בפרטי המוצר`.
2. **Expanded state:** Tapping/clicking expands inline. Tier chips render with correct
   colors (see TASK-179T tier color spec). Hebrew explanation lines visible.
3. **No Gen 0 patterns:** No alarm icons, no color-coded score bars, no dimension bars.
4. **Mobile:** Verify at 375px viewport width. No horizontal scroll. Tier chip + name
   legible. Min tap target satisfied (44px).
5. **Flag OFF:** With `NEXT_PUBLIC_GLASSBOX_D5D6=off`, the additive panel does not render
   (it is gated by the same flag as W1).

### Check 4 — Instrumentation events
Confirm the 6 engagement events from TASK-179T fire correctly:
1. `glassbox_panel_open` fires on expand.
2. `glassbox_panel_close` fires on collapse.
3. `glassbox_tier_expand` fires with `tier` property on "עוד" click.
4. `glassbox_panel_scroll_depth` fires at 50% and 100% of panel scroll.
5. `glassbox_panel_time_30s` fires at 30 seconds.
6. `glassbox_panel_time_60s` fires at 60 seconds.
Verify via browser devtools / analytics console. No PII in event properties.

## Guardrails
- Do NOT close this task if any check fails. Return to the owning sub-task with exact
  failure description.
- Frozen invariants: confirm milk/snack/bread scores are not in scope of W2 JSONs
  (pilot = hummus + maadanim only).

## Deliverables
1. Check 1 PASS confirmation (paste output of verify script)
2. Check 2 summary (10-product sample, d4_additives present, tier distribution found)
3. Check 3 visual QA (screenshot of collapsed + expanded states at 375px)
4. Check 4 instrumentation confirmation

## Return block
QA returns with all 4 checks PASS and evidence for each. States explicitly:
"Checks 1–4 all PASS. W2 is clear to close." or lists which checks failed and why.
CC closes this task (and TASK-179T, TASK-179S, TASK-179U) only after QA PASS return.
