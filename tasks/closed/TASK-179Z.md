---
id: TASK-179Z
title: "Glass Box W4 prep — D3 de-moralization spec (methodology doc)"
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: governance
close_reason: >
  CC close-readiness gate PASS (2026-06-04). Spec verified at
  01_framework/glass_box/d3_demoralization_spec_v1.md. All 6 sections confirmed against
  artifact: Section 1 quotes score_engine.py:697-699/1247-1251/1321-1350 + 3 overstatements
  O1/O2/O3; Section 2 defines d3_processing_signal struct + confidence-scaling formula +
  D3→D6 deferral; Section 3 Product co-sign verified in spec (§3.3 "Product co-sign —
  decisions recorded 2026-06-04") + task return block; Section 4 scope boundary + frozen
  invariants explicit; Section 5 6-item build checklist + blocker table; Section 6 draft
  EV-042 (Product D7 still pending — EV-042 filing deferred to W4 task open, after
  TASK-179X engagement gate). Note_he wording finalized: Candidates A/B (ברמה אוכלוסייתית
  → במחקרים גדולים), C full + C mobile approved.
cc_comments:
  - flag: fyi
    note: >
      EV-042 (draft in §6 of spec) requires Product D7 co-sign before it can be appended to
      bsip2_evidence_registry_v1.md. Nutrition brings EV-042 back to CC when W4 tasks open
      (after TASK-179X). Not a blocker for this task's close.
summary: >
  W4 architecture spec: reframe D3 (processing signal) from NOVA-penalty-equals-bad to a
  probabilistic population-level signal with explicit uncertainty. Methodology document only
  — no code. Written in parallel with the W2 gate wait (2–3 week window). If gate passes,
  W4 opens immediately with spec ready. If gate fails, D3 reframe still ships as methodology.
  Nutrition owns reframe; Product co-signs consumer-surface framing.
---

# TASK-179Z — Glass Box W4 prep: D3 de-moralization spec

Part of TASK-179 (Glass Box), Wave 4 pre-work. **Runs in parallel with TASK-179X (engagement
gate) — the 2–3 week wait window is the write window.**

## Why D3 needs a reframe

The current D3 implementation uses NOVA classification as a proxy for processing quality:
higher NOVA score → score penalty. This is a governance problem:
- NOVA is a population-level epidemiological signal, not a product-level quality verdict.
- "Processing is bad" is not the claim — "ultra-processed patterns correlate with poorer
  diet quality at population scale" is the claim. They are different.
- Applying it as a deterministic penalty moralizes a probabilistic signal.
- The Glass Box philosophy (born from the clinician stress-test) requires the engine NOT to
  pretend certainty where there is none (D6 = confidence dimension).

## Scope — methodology document only, no code

Nutrition writes `01_framework/glass_box/d3_demoralization_spec_v1.md`. The spec must cover:

### 1. Current D3 model — what it claims and what it actually knows
- Quote the current penalty logic (file:line from `score_engine.py`).
- State the actual evidence claim: population-level correlation, not individual product
  determinism.
- Identify where the current model overstates certainty.

### 2. Reframed D3 model
- D3 becomes a **probabilistic signal**: a score modifier within a defined confidence
  interval, not a deterministic penalty.
- Signal form: `d3_processing_signal: { nova_class: int, confidence: "low"|"medium"|"high",
  population_correlation: float, note_he: str }`.
- The `note_he` field carries the honest consumer-facing framing: what the signal means and
  what it does NOT mean.
- Uncertainty: when ingredient data is insufficient for NOVA classification, D3 defers to
  D6 (confidence dimension) to lower the overall grade ceiling — it does NOT invent a class.

### 3. Consumer-surface framing (Product co-sign required)
- How does D3's reframed signal appear to the user?
- Forbidden framing: "מזון מעובד = גרוע" (ultra-processed = bad).
- Required framing: probabilistic / population-level language, explicitly hedged.
- Nutrition drafts; Product co-signs this section before the spec is filed as CLOSED.

### 4. Score impact boundary
- Specify exactly which score cases are affected by the D3 reframe.
- State explicitly: this spec is not a rescore. Frozen invariants (milk/snack/bread) are
  not affected unless an explicit rescore is authorized separately.
- D3 reframe ships in W4 behind a new flag (`BARI_GLASSBOX_W4` or similar); OFF = current
  behavior.

### 5. W4 build readiness checklist
- What does Data need from this spec to start the W4 engine implementation?
- Enumerate the 3–5 concrete inputs (signal shape, confidence thresholds, flag name,
  score formula delta, consumer copy templates).

## Co-sign requirement

Product must co-sign **section 3 (consumer-surface framing)** before Nutrition files the
return block. Nutrition delivers a draft; Product reviews and signs off inline in the doc
or via a return annotation.

## Guardrails

- This is a methodology document only — no engine code changes.
- Do NOT rescore any live product as part of this task.
- Do NOT open W4 tasks without CC confirmation (and only after TASK-179X gate verdict).
- Frozen invariants (milk run_005_headpin / snack 70/B / bread provenance) are unaffected
  unless explicitly authorized.

## Deliverable

`01_framework/glass_box/d3_demoralization_spec_v1.md` — complete and Product co-signed on
section 3.

## Return block

Nutrition returns with: (a) spec file path, (b) confirmation that section 3 is Product
co-signed, (c) the W4 build readiness checklist (section 5) listed explicitly so Data can
confirm it has everything needed to start W4.
CC closes after verifying the spec exists, section 3 co-sign is present, and build
checklist is complete.

---

## Return block — Nutrition Agent (2026-06-04)

**Spec written:** `01_framework/glass_box/d3_demoralization_spec_v1.md`

Confirms:
- Section 1 (current model critique): DONE — quotes `score_engine.py:697–699` (`score_processing_quality`), `score_engine.py:1247–1251` (PROCESSING_LOAD caps), `score_engine.py:1321–1350` (NOVA_HP_WEIGHTS scaling), and `constants.py:50–52` (NOVA_PROCESSING_SCORES / NOVA_WFI_SCORES / NOVA_HP_WEIGHTS). Three overstatements of certainty identified and labelled O1/O2/O3.
- Section 2 (reframed model + signal shape): DONE — full signal struct (`d3_processing_signal`) defined; confidence-scaling formula specified; D3-defers-to-D6 rule for insufficient data stated explicitly.
- Section 3 (consumer framing): DRAFTED — three candidate `note_he` phrases authored (Candidate A: NOVA 1 positive; Candidate B: NOVA 3–4 negative with individual-product hedge; Candidate C: low-confidence provisional). **Awaiting Product co-sign.**
- Section 4 (score impact boundary + frozen invariants stated): DONE — affected cases enumerated; milk/snack/bread invariants explicitly preserved; flag `BARI_GLASSBOX_W4` confirmed consistent with existing naming convention.
- Section 5 (W4 build checklist): DONE — 6 items listed with source, status, and resolution path. Summary blocker table included.
- Section 6 (draft EV-042): DONE — draft evidence-registry entry authored, pending Product D7 co-sign.

**Product co-sign required on Section 3 before CC closes this task.**

**Status proposal: RETURNED** — pending Product co-sign on Section 3 (consumer framing) and EV-042 registration.

---

## Product co-sign annotation — 2026-06-04

Section 3 reviewed and co-signed. Decisions:
- Q1: Candidate B's explicit disavowal ("לא אמירה על מוצר זה בפני עצמו") approved on ALL surfaces — consumer drilldown and professional. Removing the hedge in any context recreates the governance problem the reframe was written to fix.
- Q2: Mobile variants approved for Candidate C only (one-sentence compression: "הרכב המוצר לא פורט במלואו — האומדן לדפוס העיבוד הוא זמני."). Candidates A and B are each one sentence; no separate mobile variant needed.
- Q3: Candidate A (positive NOVA 1 framing) approved and required. Suppressing the positive signal is a distortion; surfacing both directions signals that D3 is a factual formulation-pattern observation, not a health-warning system.
- Q4: "ברמה אוכלוסייתית" replaced with "במחקרים גדולים על אוכלוסיות רבות" in Candidates A and B. The original phrase is jargon for the target consumer; the replacement carries the same epistemic content in plain language.

Approved note_he phrases: Candidate A (wording updated), Candidate B (wording updated), Candidate C full form (unchanged), Candidate C mobile variant (new, approved). All three candidates ship.

**Product D7 co-sign complete. TASK-179Z is ready for CC final close.**
