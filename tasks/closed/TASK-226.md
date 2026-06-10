---
id: TASK-226
title: Shared comparison-page cleanup — strip dashboard furniture + align confidence layer to D12 spec
status: CLOSED
owner: Frontend Agent
renumber_note: >
  Originally drafted as TASK-223; renumbered to TASK-226 on 2026-06-10 to resolve an id
  collision. TASK-223/224/225 were already allocated by a parallel BSIP/ECS session and lived
  in tasks/closed/ (the live tasks/ dir only showed up to 222 when this id was picked). TASK-223
  = "ECS-v1 design + QA" (restored). All in-code "TASK-223" comments authored by THIS task were
  updated to TASK-226.
contributors: [Design Agent, Content Agent, QA Agent]
created: 2026-06-10
closed: 2026-06-10
close_reason: >
  All four scope items verified at the artifact level by the orchestrator (not taken from the
  return block on trust). Scope 1: confidence-marker.tsx renders nothing for `verified` and an
  identical achromatic marker (6px #5E6560 dot + 1px dotted --hairline ring via outline, 0 width)
  for partial/insufficient; confidence-indicator.tsx gutted to a label-free alias (hued
  #1F8F6A/#B5882F dots + "נתונים מלאים" text removed); comparison-row.tsx wires the marker + ring +
  NullScorePill, Glass Box DEMOTE / withhold paths preserved; expansion-section.tsx untouched.
  Scope 2: rail <aside>, showRail prop, railBandsFor, averageScore + "· ממוצע" removed from
  comparison-table.tsx; in-list band dividers kept. Scope 3: second yellow METHODOLOGY_NOTE box
  removed; locked sentence relocated into MethodologyFooter. Scope 4: prologue + methodology
  strings match COPY-LOCK verbatim. Build + lint pass (lint delta vs base = 0; pre-existing errors
  in untracked files only). Governance conflict #1 (FG3 token) resolved owner-approved: --fg3 set
  to #5E6560 (darker, contrast-aligned), spec score_confidence_indicators_spec_v1.md amended to
  match. State 7 null pill present in code but not activated (threshold owned by Nutrition/Product).
close_notes: >
  COMMIT HYGIENE: the working tree commingles TASK-223 with a concurrent contrast-token task
  (TASK-224/225 — score-chip.tsx accent→text, view-models.ts +3 optional confidence fields,
  colors_and_type.css, contrast_token_decision_v1.md). TASK-223 itself made NO grade-chip/VM
  changes (DoD satisfied); whoever commits must stage TASK-223's files separately from the
  contrast-token files so the two ship as distinct commits. Mobile 0px-scroll ≥3 rows holds for
  salty-snacks/bread/yogurt/cereals/butter/maadanim; cheese/milk/granola/hummus show 1 (pre-existing
  taller heros, not caused by this task). Pre-launch: salty-snacks copy string B carries a
  positioning disclaimer → Nutrition (accuracy) + Product (positioning) sign-off before go-live.
commit_topology: >
  Committed across two commits, NOT one, because a background process landed part of this work
  first. (1) Commit 30258a64 "Add score confidence / data-completeness indicators (TASK-226)" — a
  background bundle that captured the confidence-marker.tsx / confidence-indicator.tsx /
  comparison-row.tsx / score_confidence_indicators_spec_v1.md (incl. the 223→226 renames + FG3
  #5E6560 reconciliation) BUT mixed them with unrelated parallel work (contrast-token files,
  BSIP confidence-annotation, data-JSON regen). Not unpicked — history rewrite would revert
  legitimate parallel work. (2) Follow-up commit — the genuine TASK-226 remainder that 30258a64
  missed: rail/average removal (comparison-table.tsx, globals.css, butter-comparison-page.tsx),
  pre-table methodology relocation (comparison-page.tsx), and this close file. Net: all TASK-226
  scope is committed; the salty-snacks prologue (scope 4) remains uncommitted, deferred to a
  dedicated TASK-222 commit per owner decision.
source: Combined Review — Salty-Snacks Comparison Page (verdict: FAIL before launch)
blocks_launch: salty-snacks
depends_on: TASK-222
governance:
  - 01_framework/frontend/score_confidence_indicators_spec_v1.md   # D12 authority — supersedes comparison_ui_reference_v2
  - CLAUDE.md Hard Rules (Hard Rule 1 — chip is the only color axis)
---

## Why

The combined review of `/hashvaot/salty-snacks` returned **FAIL before launch**. The page
renders as an analytics/report dashboard rather than a consumer shelf, and the shipped
confidence layer implements a **superseded** model (`comparison_ui_reference_v2`) that the
newer D12 spec `score_confidence_indicators_spec_v1.md` (2026-06-10) explicitly overrides.

All fixes are **removals or reverts** toward existing governance — no new components, no new
concept, no new sections. Changes land in **shared** comparison components, so they propagate
to every live category (intended) and require site-wide regression.

## Scope / Deliverables

### 1. Align confidence-indicator to D12 spec — `confidence-indicator.tsx` + `comparison-row.tsx`
- [ ] `verified` / complete data → renders **nothing** on the collapsed row
- [ ] `partial` / `insufficient` → **quiet achromatic marker only** (dotted ring + `--fg3` grey dot)
- [ ] **No hued dot** (remove `#1F8F6A` / `#B5882F` row-path colors — Hard Rule 1)
- [ ] **No row-level "נתונים מלאים"** text label
- [ ] Hebrew label appears **only inside the expansion confidence row** (per spec §4)
- [ ] Update call site `comparison-row.tsx:193`; preserve existing Glass Box DEMOTE/withhold paths

### 2. Remove dashboard/report furniture — `comparison-table.tsx`
- [ ] Remove left score-distribution rail (`bari-cmp-rail` block + `showRail` prop + `railBandsFor` usage + dead CSS)
- [ ] Remove average score from column header (`averageScore` calc + "ציון · ממוצע" render)
- [ ] **Keep in-list band dividers untouched**

### 3. Reduce pre-table clutter — `comparison-page.tsx`
- [ ] Keep **maximum one** category caveat box (`categoryNote`)
- [ ] Remove the `METHODOLOGY_NOTE` block from above the table
- [ ] Move the (Content-revised) methodology sentence into `MethodologyFooter`

### 4. Salty-snacks copy cleanup — `salty-snacks-page-data.ts` (+ shared `METHODOLOGY_NOTE` if kept global)
- [ ] Replace stats-heavy prologue with **one shelf-investigator line** (no gram/count dumps)
- [ ] Remove framework leakage — no naming of scoring axes (e.g. "ערכים תזונתיים, רכיבים ורמת עיבוד")
- [ ] No health claims

### 5. Regression-check all live comparison categories
- [ ] milk · bread · cheese · yogurt · hummus · granola · cereals · butter · maadanim · salty-snacks

## Quality gates (DoD)
- [ ] Build passes
- [ ] Lint passes
- [ ] **No score changes**
- [ ] **No grade-chip changes**
- [ ] No VM contract changes unless explicitly required (justify if so)
- [ ] No new components
- [ ] No new sections / headings (Gen 1 expansion rule preserved)
- [ ] 3+ rows visible at 0px scroll on 375px where feasible
- [ ] No CLS regression
- [ ] Shared-component impact documented in return block

## Files in scope (shared — render every category)
- `bari-web/src/components/shared/confidence-indicator.tsx`
- `bari-web/src/components/shared/comparison-row.tsx`
- `bari-web/src/components/shared/comparison-table.tsx`
- `bari-web/src/components/comparisons/comparison-page.tsx`
- `bari-web/src/lib/comparisons/salty-snacks-page-data.ts`
- `bari-web/src/components/shared/methodology-footer.tsx` (target for relocated sentence)

## Return block (Frontend Agent fills on completion — propose RETURNED, do not self-close)
- TASK id: TASK-223
- Files changed: …
- Before/after summary (per scope item): …
- Viewport evidence: salty-snacks + ≥3 other live categories (screenshots / 375px capture): …
- Regression checklist (10 categories, build, lint, CLS, 0px-scroll row count): …
- Unresolved governance conflicts, if any: …

## LOCKED INPUTS (Design + Content, 2026-06-10) — Frontend builds to these verbatim

### DESIGN-LOCK — collapsed-row confidence marker (authority: score_confidence_indicators_spec_v1.md §2–§4)
- `verified` / complete → render **nothing** (no ring, no dot, no label, no wrapper). Chip stays solid.
- `partial` AND `insufficient` (non-suppressed rows) → **identical** achromatic marker; do NOT branch the dot by state (gap type is differentiated only in the expansion):
  - Dot: `6px × 6px` filled circle, color `var(--fg3)` (`#7A817C`), inline-start gutter; **RTL = right of chip, before name**; `4px` gap to chip.
  - Ring: on the chip — `outline: 1px dotted var(--hairline); outline-offset: 1px;` radius `var(--radius-lg)` (12px). MUST add 0 layout width — use `outline`/pseudo-element, NOT `border`.
  - No text on row. No fill. No grade hue anywhere. Desktop hover `title` = badge label only.
- Expansion confidence row in `expansion-section.tsx` is **already conformant — do not edit.** Hebrew label (`.bari-meta`/`--fg3`) + tooltip (`.bari-footnote`/`--fg4`) verbatim from backend. This is the ONLY place the Hebrew label appears (mobile + desktop).
- Remove the `pill` desktop variant's text + hued dot too — desktop row gets the same dotted-ring + `--fg3` dot, no `נתונים מלאים`, no bordered white pill.
- Unaffected (carry own signal, do NOT touch): Glass Box DEMOTE pill, `לא נוקד` withhold path, legacy expansion label fallback.
- **State 7 (null pill) = DEFERRED, out of scope** — chip-suppression threshold owned by Nutrition/Product (potential tripwire #1). Track separately.
- Post-fix: re-run `npm run test:a11y` on /hashvaot/salty-snacks (achromatic marker should clear the WCAG 1.4.3 finding the hued dots produced).

### COPY-LOCK — final Hebrew strings (paste verbatim)
- **Salty-snacks prologue** (replace `prologueSentences` in `salty-snacks-page-data.ts`, single-element array):
  `"עברנו על מדף החטיפים המלוחים בסופר, מקצה לקצה, ומיינו אותו בשבילכם."`
- **Methodology footer sentence** (replace `METHODOLOGY_NOTE` in `comparison-page.tsx`):
  `"הציון מסכם את מה שכתוב על תווית המוצר. הוא אינו המלצה ואינו קובע אם המוצר טוב או רע לאכילה."`
- Removed: stat-dump prologue (counts/grams/grades) and the leaked dimension names ("ערכים תזונתיים, רכיבים ורמת עיבוד").
- Note (carried from Content): string B carries a positioning-relevant disclaimer — Nutrition (accuracy) + Product (positioning) sign-off required before public launch, not before merge.

## Known governance note (carried from the review)
The shipped confidence indicator cites `comparison_ui_reference_v2`. This task treats
`score_confidence_indicators_spec_v1.md` (D12, 2026-06-10) as authoritative and removes the
older row-label/hued-dot model. If Design later wants ANY row-level confidence text retained,
that is a spec change to `score_confidence_indicators_spec_v1.md` first — not drift left in code.
