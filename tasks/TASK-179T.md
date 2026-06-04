---
id: TASK-179T
title: "Glass Box W2 — additive panel component: Frontend + Design build"
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179Q, TASK-179R, TASK-179U]
blocks: [TASK-179V]
category_id: null
roadmap_impact: true
work_type: execution
---

# TASK-179T — Glass Box W2: additive panel component

Part of TASK-179 (Glass Box), Wave 2. Runs in parallel with TASK-179S (engine D4 wire)
and TASK-179U (Hebrew content). Formally depends on 179U for final Hebrew strings
(coordinate — design work can start in parallel; Hebrew strings are merged before ship).
Gates TASK-179V (QA).

**No score movement.** The additive panel is a *disclosure / transparency* surface.
It renders D4 tier data from the pilot frontend JSONs (already on-shelf after TASK-179S
phases). The engagement gate (TASK-179R) measures whether consumers interact with it;
passing the gate is what unlocks W3 (full library + score movement consideration).

## Design brief (from `w2_engagement_gate_spec_v1.md §5`)

Read `01_framework/glass_box/w2_engagement_gate_spec_v1.md` in full before starting.
Key constraints:

- **Entry point — collapsed on load:** A single row below the score section and above
  the nutrition table: `X תוספים — הצג פירוט` (X = count of detected additives).
  Products with 0 additives show the empty state (§5.6 of the spec).
- **Expanded state — tier chips:** Each detected additive renders as a row:
  `[TIER CHIP] | additive name (Hebrew) | one-line Hebrew explanation | ▾ "עוד"`.
- **Tier chip encoding (5 active tiers):**
  - `functional` → chip background `#E8F5E9` (light green), text `#1B5E20` — "פונקציונלי"
  - `likely-neutral` → chip background `#F5F5F5`, text `#424242` — "ניטרלי"
  - `dose-dependent` → chip background `#FFF3E0`, text `#E65100` — "תלוי-מינון"
  - `contested` → chip background `#FFF8E1`, text `#F57F17` — "שנוי במחלוקת"
  - `disclosure-gap` → chip background `#F3E5F5`, text `#4A148C` — "לא מוגדר"
  - `unclassified` (fallback) → chip background `#FAFAFA`, text `#9E9E9E` — "לא מסווג"
- **Forbidden patterns (DEC-006 + Gen 0 rules):**
  - No alarm icons (⚠️ ☠ 🔴) for any tier — including contested and dose-dependent.
  - No raw E-numbers as the primary visible label (E-number may appear as sub-label only).
  - No attribution of manufacturer intent ("deliberately added", "hidden", etc.).
  - No Gen 0 patterns (color-coded score bars, dimension breakdown bars, card grids).
  - No "dangerous", "harmful", "toxic" phrasing in any label or tooltip.

## Component architecture

### `AdditivePanel` (new shared component)
Location: `bari-web/src/components/shared/AdditivePanel.tsx`

Props:
```typescript
interface AdditivePanelProps {
  additives: AdditiveEntry[];   // from product.d4_additives (TASK-179S output)
  locale?: "he";                // Hebrew only for now
}
interface AdditiveEntry {
  e_number: string;
  name_he: string;
  tier: AdditiveTier;
  function_he: string;
  explanation_he: string;       // from TASK-179U final Hebrew copy
}
type AdditiveTier =
  | "functional" | "likely-neutral" | "dose-dependent"
  | "contested" | "disclosure-gap" | "unclassified";
```

Behavior:
- Collapsed on initial render. Single `<button>` entry point: `{count} תוספים — הצג פירוט`.
- `onClick` → expands inline (no modal, no route change). Button label flips to `סגור`.
- Each row: `[TierChip] {name_he}` on the first line; `{explanation_he}` on the second
  line (one line, truncated at 80 chars with `…` if needed); `{function_he}` as a
  `<details>`/`<summary>` "עוד" sub-row (optional expand).
- Empty state (0 additives): `"לא זוהו תוספי מזון בפרטי המוצר"` — one calm line, no icon.
- Mobile-first. The tier chip + name must be legible at 375px width without horizontal
  scroll. Explanation text wraps. Min tap target 44px.

### `TierChip` (sub-component or inline)
Renders the tier label with the color encoding above. Props: `tier: AdditiveTier`.
If defined inline in AdditivePanel.tsx, that is fine — no need for a separate file
unless it becomes reused elsewhere.

### Wire into comparison page
In the product expansion section (the `<ExpansionSection>` component — the section that
currently shows nutrition + ingredients), render `<AdditivePanel>` immediately before
the nutrition table, gated on `GLASSBOX_D5D6_ON` (same flag as W1 — the W2 panel is
part of the same Glass Box go-live gate).

If `product.d4_additives` is undefined or empty, render the empty state, not null
(the panel entry point should always be present for pilot categories so the engagement
gate can measure its interaction rate even for clean products).

## Instrumentation

Wire the 6 engagement events from `w2_engagement_gate_spec_v1.md §3` (Instrumentation plan):
1. `glassbox_panel_open` — fired when user expands the additive panel
2. `glassbox_panel_close` — fired when user collapses it
3. `glassbox_tier_expand` — fired when user opens the "עוד" sub-row (with `tier` property)
4. `glassbox_panel_scroll_depth` — fired at 50% + 100% scroll depth inside the expanded panel
5. `glassbox_panel_time_30s` — fired if panel stays open ≥ 30 seconds
6. `glassbox_panel_time_60s` — fired if panel stays open ≥ 60 seconds

Privacy boundary (from spec): No user identifiers in event properties. Session-level
aggregation only. Use whatever analytics client is already wired in `bari-web`
(check existing event patterns before wiring a new one).

## Guardrails
- Gen 1 patterns only. Read `01_framework/frontend/architecture_generations_registry_v1.md`.
- All new components in `src/components/shared/`.
- No score/grade fields touched.
- Hebrew strings come from TASK-179U (Content sign-off); do NOT author new Hebrew from scratch —
  use the draft from `additive_prototype_set_v1.md` as a starting point, coordinate with
  Content before shipping.
- Tier color values are frozen (spec above); do not adjust without Design co-sign.
- Mobile first: verify at 375px and 390px before marking complete.
- Instrumentation privacy boundary: session-only, no PII.

## Deliverables
1. `bari-web/src/components/shared/AdditivePanel.tsx` — component
2. Wired into `ExpansionSection` (or equivalent expansion component) for pilot categories
3. 6 engagement events instrumented per spec
4. Mobile QA verified at 375px + 390px
5. Visual screenshot of collapsed + expanded state (for QA record)

## Return block
Frontend returns with: (a) component built, (b) wired into pilot pages, (c) events
instrumented, (d) mobile QA pass at 375px/390px, (e) screenshot of both states.
QA (TASK-179V) runs visual regression + mobile checklist independently.

## Dependency note
TASK-179U (Hebrew copy) must complete before final ship. Coordinate: Frontend can build
with the draft Hebrew from `additive_prototype_set_v1.md`; Content sign-off (179U)
is required before the task ships. If 179U is not yet complete when Frontend finishes
building, return with "awaiting Content sign-off" and block on 179U.
