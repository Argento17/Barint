---
id: TASK-538
title: bariInterpretation dimension-panel text recites UI-duplicate numbers + satiety boilerplate (owner complaint #2, deeper layer)
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-08
closed_at: 2026-07-08
close_reason: >
  Core defect (bariInterpretation reciting UI-duplicate per-100g numbers, 735/980 rows) FIXED and
  ORCHESTRATOR-VERIFIED: 0/980 digit-bearing interpretation rows on both yogurt pages. Executed via the
  systematic path Product ruled (not hand-rewrite): the round-2 Content Agent hardened the canonical
  generator `_author_bari_interpretation()` in author_copy.py (qualitative category-relative phrase bank,
  dropped raw grams + the (score_int) parenthetical, satiety kept a non-absolute "פוטנציאל" hedge) and
  regenerated all 980 rows deterministically against the BSIP2 traces — retiring build_final_v3.py's
  hand-authored path for this field. Folded into TASK-533's 3-round two-gate cycle (GATE-2 PASS).
  Remaining minor note (NOT this task's number-recitation defect): QA observed the panel still shows the
  scoring-dimension LABELS (רמת עיבוד/חלבון/צפיפות קלורית etc.) — but a per-dimension breakdown panel showing
  dimension names is its intended function, not a framework-leak; if the owner wants those relabeled to
  pure consumer language that's a separate design call, logged as a design consideration, not a blocker.
  Also separate/pre-existing: cookies_coffee has 117 malformed legacy bariInterpretation rows (route to Data
  when surfaced). Generator hardening means the NEXT category inherits the clean behavior.
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-533 re-authored insightLine/rowVerdict/expansion but the bariInterpretation dimension panel (rendered via bari-interpretation-panel.tsx in product expansion) still carries engine-templated interpretation strings that reproduce the owner's exact complaint #2: e.g. satiety_support row = '10.5 גרם חלבון ל-100 גרם — מרכיב שבדרך כלל תורם לתחושת שובע' — recites the protein number (already shown), the strength (חזק, already a field), the score (100, already a field). ~980 interpretation strings across 98 products, all generator-templated. SYSTEMATIC fix required (fix the generator, not hand-rewrite): Product scopes whether dimension interpretation should carry prose numbers AT ALL vs trim to label+strength+score; then engine/Content fix. Not artisanal. Blocks clean owner re-review of yogurt pages.
---

# TASK-538 — bariInterpretation dimension-panel text recites UI-duplicate numbers + satiety boilerplate (owner complaint #2, deeper layer)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
