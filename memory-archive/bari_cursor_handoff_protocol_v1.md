---
name: bari_cursor_handoff_protocol_v1
description: "Cursor session handoff protocol — 8 required context docs, frozen pixel values, 6 prohibited improvisation zones, 5 approval checkpoints (hard gate at checkpoint 3), visual QA + mobile QA checklists, 9 drift escalation rules, session handoff format"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

File: `C:\Bari\01_framework\frontend\cursor_handoff_protocol_v1.md`

**Why:** Multiple Cursor sessions implementing the same component set will diverge without explicit handoff rules. This doc is read at the start of every session.

**8 required context docs (in priority order):** this protocol → component_build_sequence_v1 → comparison_template_v1 → ui_stabilization_sprint_1 → design_token_governance_v1 → legacy_isolation_policy_v1 → architecture_generations_registry_v1 → exception_registry_v1

**Frozen pixel values (14 values, non-negotiable):** row=72px, image=56px, chip=28px, insight-line=13px/#444444, hero-max=280px, pre-table-max=480px, methodology=12px/#AAAAAA, rows=#FFF/#F9F9F9, filter-margin=16px

**6 prohibited improvisation zones:**
1. Score chip appearance (no color by grade, no label text, no animation)
2. Expansion content (no headings, no score attribution, no framework terms)
3. Filter (no NOVA, no grade filter, no count badge, max 3 dims)
4. Hero (no stats, no multi-product animation, no English eyebrow, single sentence)
5. Methodology (no card, no heading, no collapsible, ≤12px)
6. Legacy imports (no BariGradeBadge, SnackScoreChip, DimensionBars, InterpretationPanel, MatrixIntegrityBadge)

**5 checkpoints:** ScoreChip → ProductRow (hard gate) → ExpansionSection (hard gate) → ProductTable → Full page assembly. Each requires explicit visual approval before proceeding.

**9 drift escalation rules:** Gen 0 pattern proposed; legacy import; second tooltip; framework term in JSX; score chip color by grade; page sections > 4; component added to legacy directory; hardcoded value duplicates token; checkpoint skipped → all require stop + fix before continuing.

**Session handoff format:** date, component in progress, last checkpoint, files modified/created, tokens added, open issues, next action. Goes in comment at top of in-progress file or CE_DIRECTION_V1.md.

**Related:** [[bari_component_build_sequence_v1]] [[bari_legacy_isolation_v1]] [[bari_architecture_generations_v1]] [[bari_design_token_governance_v1]]
