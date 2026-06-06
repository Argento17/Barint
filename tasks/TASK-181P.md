---
id: TASK-181P
title: "Glass Box W5 Design: methodology page UX spec + consumer additive panel polish"
owner: design-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-05
completed_at: 2026-06-05
depends_on: []
blocks: [TASK-181Q]
category_id: null
roadmap_impact: true
work_type: design
cc_reviewed: 2026-06-05
close_reason: >
  CC close-readiness gate PASS (2026-06-05). Artifact independently verified:
  methodology_page_ux_spec_v1.md at 01_framework/glass_box/ — complete 5-section page
  spec with token values + full AdditivePanel polish. D-dimension presentation decision
  (inline paragraphs, framework invisibility rationale) is sound. Route /research/glass-box
  is appropriate with a documented deviation protocol for Frontend. Tooltip correctly rejected
  per EXCEPTION-001. All 3 polish items (TierChip 11→12px + height 24→26px; fontWeight
  600→500 on count+action string; word-boundary truncation) are targeted, achievable with
  existing tokens/Tailwind, and non-restructuring. No new tokens registered. Scope clean —
  no scores, flags, JSONs, or engine code touched. 181Q unblocked (both O + P now CLOSED).
cc_comments:
  - flag: fyi
    note: >
      Route /research/glass-box is a recommendation, not a hard constraint. The spec
      explicitly gives Frontend Agent authority to deviate if a different routing convention
      is identified — with documentation. CC confirms this is appropriate delegated design
      judgment, not an open question that needs resolution before 181Q ships.
---

## Return Block (design-agent, 2026-06-05)

**Deliverable:** `C:\Bari\01_framework\glass_box\methodology_page_ux_spec_v1.md`

**Claims:**
- Full 5-section page structure spec delivered with visual weight, spacing, and token references for each section.
- D-dimension presentation decision made: inline paragraphs with bold lead phrase (not icon rows, not card grid). Rationale: framework invisibility. Justified against Gen 1 editorial principles.
- Route recommendation: `/research/glass-box` — uses existing `research/` parent, avoids new top-level segment for a single page.
- Link surface from comparison pages: inline footnote within MethodologyFooter, not a button/row/tooltip. Second tooltip rejected (EXCEPTION-001 covers bread filter only).
- Date stamp spec: `11px / #AAAAAA / no heading / no border` — methodology register.
- AdditivePanel audit complete: 3 targeted polish items identified and specified.
- No new design tokens registered. All values from existing `bari-comparison-tokens.ts` or Tailwind utilities.
- Gen 1 compliance confirmed. No Gen 0 patterns introduced. No frozen constraints broken.

**AdditivePanel Polish Items (3):**
1. TierChip font size: `11px` → `12px`, height `24px` → `26px`. Improves Hebrew legibility on mobile.
2. Collapsed entry-point label: count+action string `fontWeight` `600` → `500`. Restores signal hierarchy (chip=signal, label=affordance).
3. `truncate()` helper: hard char-cut at 80 → word-boundary cut near 80. Prevents mid-word bisection of Hebrew text.

**Blocks:** TASK-181Q (Frontend build) — spec is complete and buildable.

**CC note:** The methodology page is a new route (`/research/glass-box`) — Frontend Agent must confirm the routing parent before building. No existing page is modified. No flag is flipped. Spec is draft-reversible until 181Q ships.

# TASK-181P — Glass Box W5: Design — methodology page UX + additive panel polish

Part of **TASK-181** (Glass Box program-of-record), Wave 5 — the consumer launch wave.

## Context

**181O (Content, parallel)** is authoring the Hebrew methodology page copy — 5 sections, ≤400 words, "non-silent flip" spine. The structure is already known (see 181O task spec), so Design can work from it without waiting for the final copy.

**The additive panel** (AdditivePanel component) is already live on hummus + maadanim behind `NEXT_PUBLIC_GLASSBOX_W2`. A polish pass is part of this wave to ensure the panel reads well in the full consumer-facing GlassBox launch context — not a rebuild, targeted improvements only.

The Gen 1 canonical reference is מעדנים (see `01_framework/frontend/canonical_reference_declaration_v1.md`). All design decisions must stay in the Gen 1 system. The component build sequence is frozen at `component_build_sequence_v1.md`.

## Deliverable 1 — Methodology page UX spec

A written spec (`methodology_page_ux_spec_v1.md`) delivered to `01_framework/glass_box/`, covering:

1. **Page structure** — section hierarchy mapping to 181O's 5 sections: lead / מה השתנה ולמה / מה ברי בודק עכשיו / על הציונים שזעו / תאריך. Propose a visual weight and spacing treatment for each.
2. **D-dimension cards** — how D3 / D4 / D5 / D6 appear in the "מה ברי בודק עכשיו" section. These are brief consumer-facing items (1–2 lines each), not technical tables. Propose whether they're inline paragraphs, icon+text rows, or a compact card grid — justify against the Bari editorial principle of "framework invisibility."
3. **Mobile layout** — this page will be read on mobile first. Define the mobile hierarchy and any desktop differences. Adhere to the mobile geometry checklist (`mobile_geometry_checklist_v1.md`).
4. **Link surface** — the per-page notes on hummus/maadanim (from 181N) will link to this page. Specify how the link renders on those comparison pages (inline footnote? a "learn more" row? tooltip?).
5. **Date / version stamp** — placement and typographic treatment for the page date.

Constraint: no new components. Use existing tokens + shared components only (`design_token_governance_v1.md`). If a new token is genuinely needed, register it in the governance doc, not inline.

## Deliverable 2 — Additive panel polish notes

A short section in the same spec (`additive_panel_polish_notes`) listing **targeted visual improvements only** to the existing AdditivePanel:

- Audit the current panel on hummus + maadanim (live at `/השוואה/חומוס` and `/השוואה/מעדנים` in dev). Identify friction points: legibility, tier chip sizing, explanation_he line truncation, panel header clarity.
- Propose ≤3 specific changes. Each must be: (a) achievable with existing tokens / Tailwind classes, (b) consistent with Gen 1 patterns, (c) not a restructuring of the panel's information architecture.
- No changes to the additive data model, scoring, or annotation logic — visual only.

## Out of scope

- Authoring the Hebrew copy — 181O.
- Frontend build — 181Q.
- Scoring, BSIP, or data model changes — not part of this task.

## Return format

- Path to `methodology_page_ux_spec_v1.md`
- Confirmation that the spec is buildable with existing Gen 1 tokens + components (or list any new tokens registered)
- Summary of the ≤3 additive panel polish items with before/after description
- Any design judgment calls made (e.g. card vs inline choice with rationale)
