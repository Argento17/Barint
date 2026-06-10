---
id: TASK-195
title: "SIE methodology Phase-2 amendments — speciation, EFSA TUL ceiling, strain-resolved probiotics (banked; apply on revival)"
owner: nutrition-agent
status: CLOSED
priority: LOW
created_at: 2026-06-06
closed_at: 2026-06-06
cc_reviewed: 2026-06-06
depends_on: []
blocks: []
category_id: null
roadmap_impact: false
work_type: objective
source_research: "C:\\Bari\\research\\New Batch\\Clinical and Pharmacological Assessment of Dietary Supplementation.pdf"
revival_dependency: "TASK-171 banked_asset revival_gate (manufacturer/importer data feed)"
summary: >
  Three methodology amendments to the SIE engine, sourced from the Clinical and
  Pharmacological Assessment research doc. The SIE engine (TASK-171) is banked;
  these amendments update methodology_v1.md while banked so they are ready to apply
  the moment the revival gate opens. No engine code changes; no corpus changes.
  Pre-launch, reversible, no score movements.
---

# TASK-195 — SIE Methodology Phase-2 Amendments

## Context

Source: `Clinical and Pharmacological Assessment of Dietary Supplementation.pdf`
(New Batch research, 2026-06-06). The SIE engine (TASK-171) is CLOSED and banked
(proven asset; acquisition blocked at ~6.8% reachable Israeli shelf). These amendments
should be incorporated into the banked methodology so they are ready on revival —
not lost in a future context window.

## Three amendments

### Amendment A — Form dimension: speciation-aware and graded
Current Form dimension distinguishes absorbable vs poor form at a binary level. The research
doc documents clear absorption differentials that support a graded score within the Form tier:
- **Magnesium:** oxide ~4% absorption vs citrate 25–30% vs glycinate ~31% — the gap is large
  enough to differentiate product grades within the same "active present" bucket.
- **Folate:** folic acid (synthetic, requires MTHFR conversion) vs 5-MTHF (active, bypasses
  MTHFR) — clinically significant for the ~10–15% of population with MTHFR polymorphism.
  Label-observable (ingredient name).
- **B12:** cyanocobalamin vs methylcobalamin vs adenosylcobalamin — tier-able from the label.

**Change to methodology_v1.md:** Add a "speciation tier" sub-table to Form & Bioavailability
(§3 or §4) with at least Mg, folate, and B12 covered. Graded within-form scoring (not
binary) where absorption differential is ≥2× and label-observable.

### Amendment B — Safety dimension: EFSA Tolerable Upper Limit as a hard ceiling
Current Safety uses "exceeds tolerable upper limit, risky/banned active, unjustified
mega-dosing" but does not name the reference table. The research doc cites EFSA TULs as
the most defensible European reference. Israel has no equivalent standalone table.

**Change to methodology_v1.md:** Name EFSA TUL as the primary Safety ceiling reference
(already partially captured in individual dossiers; now formalized as the engine's reference
table). Add a tiered Safety penalty:
- Dose > EFSA TUL → Safety VETO (grade cap = E), existing behavior, now explicitly cited
- Dose 80–100% TUL → Safety FLAG (annotate only; note in explanation, no grade cap)
- Dose < 80% TUL → no Safety action on dose grounds

### Amendment C — Probiotic scoring: strain-resolved
Current methodology pools probiotic strains (CFU counts) without strain-level resolution.
The research doc documents that efficacy evidence is entirely strain-specific: pooling
*Lactobacillus acidophilus* + *Bifidobacterium longum* strains under a single CFU count
misrepresents the evidence base.

**Change to methodology_v1.md:** Add a probiotics sub-section to the Advanced (Phase 3+)
scope. Probiotics require strain-resolved Evidence Dossiers (not active-level). Each named
strain gets its own dossier entry. Un-named strains ("probiotic blend") → Insufficient tier
regardless of CFU count. This does NOT affect the MVP or Phase 2 scope (probiotics were
already in "Advanced / deferred").

## Deliverables

1. **methodology_v1.md** amended with all three changes (versioned as v1.4).
2. **SUPP-EV registry** updated with the three new Evidence entries (speciation differentials,
   EFSA TUL table reference, strain-specificity rule).
3. **SIE_ASSET_AND_CLOSURE.md** updated with a "pending amendments on revival" section
   listing all three changes + this TASK-ID.

## Acceptance criteria

- [ ] methodology_v1.md at v1.4 with all three amendments clearly marked and cited.
- [ ] EFSA TUL table is named and referenced (not just "consult EFSA") in Safety §.
- [ ] Speciation tier sub-table covers Mg, folate, B12 with absorption values and sources.
- [ ] Probiotics sub-section explicitly defers to Phase 3+ and requires named strains.
- [ ] SIE_ASSET_AND_CLOSURE.md reflects the pending amendments so a future revivor picks them up.
- [ ] No engine code touched. No corpus touched. No score changed.

## Governance

- roadmap_impact: false (methodology docs only; engine banked, pre-launch)
- Nutrition owns; no D7 required (pre-launch methodology within the lane)
- Revival gated by TASK-171 revival_gate: manufacturer/importer data feed (BD, not engineering)
