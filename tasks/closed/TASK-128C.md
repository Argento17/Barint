---
id: TASK-128C
title: Maadanim corpus confidence finalization + freeze (v2 activation gate)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "The platform-level blocker is cleared"
depends_on: [TASK-129]
blocks: [TASK-128B]
category_id: null
summary: >
  Finalize and freeze the maadanim displayed corpus so its v2 confidence labels are
  launch-defensible. Gates TASK-128B activation (flip MAADANIM_V2_SLICE → true).
---

# TASK-128C — Maadanim corpus confidence finalization + freeze (v2 activation gate)

## Why this exists
B1 (comparison_ui_reference_v2 §14 + §12) was CLEARED 2026-06-01. The same TASK-129
hummus confidence re-audit (`03_operations/bsip2/confidence_reaudit_launch_v1.md`)
rates **maadanim 🟡 CONDITIONAL GO**. TASK-128B promotes confidence from a 10px
footnote to a headline row label — which *amplifies* maadanim's confidence-label
defect. Controller decision (2026-06-01): **hold maadanim v2 activation until the
corpus is confidence-clean and frozen.**

## Scope (per re-audit §2.1, §2.2, §3 P0 #1/#3)
Operates on `bari-web/src/data/comparisons/maadanim_frontend_v2.json` (displayed 90).
Current state: **87/90 labelled `verified`, 3 `partial`.**
1. **Exclusion list (§2.1).** Formalize a maadanim `excluded_products` list (mirror
   hummus pattern); re-confirm the 7 non-maadanim items + probiotic-supplement cluster
   are absent from the displayed 90.
2. **Instability survivors (§2.2)** — re-route or exclude; do not publish `verified`:
   - `סופר גמדים תות בננה מארז` (53/C, cat_conf 0.30)
   - `גמדים לשתיה תות בננה` (46/D, cat_conf 0.30)
   - `דנונה מולטי קולגן` (45/D, cat_conf 0.55)
3. **Confidence-gate hardening (§3 P0 #1).** Relabel marketing-prose `verified` rows
   → `partial` (~63 candidates) and suppress ingredient-derived positive signals on
   those rows. Display-label change only — **no score changes** (CLAUDE.md invariant).
4. **Freeze** the corrected displayed corpus and document it.

## Exit / hand-off
When the corpus is frozen and confidence labels are defensible, hand to frontend-agent
to flip `MAADANIM_V2_SLICE = true` (one line) + QA re-baseline at mobile + `lg`. Only
the Central Controller records CLOSED.
