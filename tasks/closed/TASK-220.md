---
id: TASK-220
title: "Bari Hebrew Content Golden Eval Framework — structured quality gate for AI-generated Hebrew content"
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: []
blocks: []
roadmap_impact: false
cc_reviewed: false
work_type: governance
---

# TASK-220 — Bari Hebrew Content Golden Eval Framework

## Context

Bari repeatedly suffers from weak AI-generated Hebrew content: inaccurate,
generic, non-consumer-friendly, or misaligned with Bari standards. Better
prompting alone is not enough. The BSIP2 scoring pipeline has a golden-corpus
regression gate; Hebrew content has none.

The existing editorial framework (`assertive_writing_v1.md`,
`score_presentation_v1.md`, `ui_language.md`, 12+ additional docs) defines
the *standards* but provides no structured *evaluation gate* to check whether
generated content actually meets them.

## Required deliverables

### 1. Evaluation schema (4 dimensions × 4-point scale)

| Dimension | Min. pass score | Description |
|-----------|-----------------|-------------|
| factual_accuracy | 3 (excellent) | Every claim verifiable against BSIP2 trace and product data |
| bari_standard_compliance | 2 (acceptable) | Tone, forbidden terms, recommendation language, findings-first structure |
| consumer_usefulness | 2 (acceptable) | Actionable shopping insight vs. generic boilerplate |
| hebrew_rtl_quality | 2 (acceptable) | Native-quality Hebrew, correct RTL formatting |

### 2. Automatic fail conditions

- Any unsupported health claim
- Any contradiction of Bari scoring logic
- Any forbidden term from `ui_language.md`

### 3. Golden dataset structure

- 8 content types: comparison page intro, yellow caveat box, product score explanation,
  ingredient concern explanation, additive explanation, category insight, blog paragraph,
  social comparison card copy
- Target 30–50 records across all 8 types
- Each record has: id, hebrew_text, expected_scores (4 dims), auto_fail_conditions,
  expected_result, reviewer_notes

### 4. Five worked examples (Hebrew)

| ID | Category | Type | Status | Content |
|----|----------|------|--------|---------|
| GOLDEN-MK-001 | Milk | product_score_explanation | approved | Whole 3.4% — 1 ingredient, pasteurized, not fortified. Baseline standard: short, factual, restrained |
| GOLDEN-SN-001 | Snacks | comparison_page_intro | approved | Divides snack bars into 2 real archetypes (date-almond vs. processed grain) without value judgment |
| GOLDEN-MK-002 | Milk | comparison_page_intro | failed | Overclaim: "אחד המזונות הטבעיים והמזינים ביותר", "בריא יותר", recommendation language |
| GOLDEN-SN-002 | Snacks | ingredient_concern_explanation | failed | Moralizing: "על חשבון הבריאות של הצרכנים", manufacturer intent attribution |
| GOLDEN-MK-003 | Milk | comparison_page_intro | borderline | Factually correct but slightly informal tone — PASS WITH NOTES |

### 5. Reviewer instructions

- Step-by-step review process (read → score → check auto-fail → determine outcome → write notes)
- Dimension-specific checklists
- Calibration guide: common score patterns mapped to review outcomes

## Acceptance criteria

- [x] 4 eval dimensions defined with 0–3 scale and per-level descriptions
- [x] Pass/fail thresholds: factual_accuracy must be 3, others min 2
- [x] Automatic fail conditions: health claims, scoring contradictions, forbidden terms
- [x] 8 content types defined with target record counts (30–50 total)
- [x] Record ID scheme: GOLDEN-{CAT}-{NNN}
- [x] 5 fully written example records (2 approved, 2 failed, 1 borderline)
- [x] All 5 examples use real Hebrew content patterns from Bari comparison/editorial data
- [x] Reviewer instructions document the review process step-by-step
- [x] Anti-patterns documented: no medical claims, no moralizing, no generic wellness, no unsupported certainty
- [x] Expansion plan: 5 phases from starter set to full 30–50 records
- [x] Framework placed in `01_framework/editorial/` alongside existing editorial docs
- [ ] Record status workflow: draft → reviewed → approved/failed/borderline

## Out of scope

- Writing the 30–50 golden set records — this task defines the framework and provides 5 starters
- Building automated eval tooling or CI gates — this task defines the human-eval schema
- Creating Hebrew style guide — the existing editorial docs (`assertive_writing_v1.md`,
  `score_presentation_v1.md`, `ui_language.md`) already define standards; this task defines
  the eval gate that checks compliance
- Rewriting existing Hebrew content on the site — eval applies to new content only

---

## Return block (orchestrator, 2026-06-09)

**Proposed status:** RETURNED

### What was built

| Deliverable | Path | Notes |
|---|---|---|
| Eval framework + schema | `01_framework/editorial/hebrew_content_golden_eval_v1.md` | 4 dimensions, 4-point scale, pass/fail rules, auto-fail conditions, precedence rule |
| Record structure | Same file §5 | 8 content types, ID scheme (MK/SN primary), status workflow, JSON/JSONL export plan |
| 5 worked examples | Same file §6 | Calibrated on Milk (baseline) + Snacks (stress test), not hard cheese |
| Reviewer instructions | Same file §8 | Step-by-step process, per-dimension checklist, auto-fail checklist, calibration guide |

### Implementation summary

**Eval schema** — 4 dimensions (factual_accuracy, bari_standard_compliance, consumer_usefulness, hebrew_rtl_quality) each scored 0–3. Hard thresholds: factual_accuracy must be 3, others min 2. Three automatic-fail conditions (health claim, scoring contradiction, forbidden term) that override dimension scores.

**Record format** — Each golden eval record is a 9-field tuple: id, content_type, status, hebrew_text, expected_scores (4 dims), auto_fail_conditions, expected_result, reviewer_notes.

**Example records** — 5 fully worked examples anchored on Milk (clean baseline) and Snacks (stress test), not hard cheese. Approved examples: GOLDEN-MK-001 (whole 3.4% — 1 ingredient, restrained) and GOLDEN-SN-001 (snack bar archetype split without value judgment). Failed examples: GOLDEN-MK-002 (overclaim/generic wellness) and GOLDEN-SN-002 (moralizing manufacturer intent). Borderline: GOLDEN-MK-003 (factually correct, slightly informal tone). All examples are shorter and more consumer-facing than the prior hard cheese versions.

**Reviewer instructions** — Step-by-step process from reading through outcome determination. Per-dimension checklists with specific things to look for. Auto-fail checklist formatted for quick scanning. Calibration guide mapping common content patterns to expected outcomes.

### Open items (not blocking RETURNED)

1. **25–45 additional records needed** — current 5 records are starters. Phases 2–5 must fill to 30–50.
2. **No automated tooling** — eval is human-only. No CI integration, no script that runs the eval.
3. **No reviewed/draft record status workflow** — the status field (`approved`/`failed`/`borderline`/`draft`) is defined but no process for moving records through the pipeline.
4. **Incomplete cross-category coverage** — anchor categories (MK, SN) have started; BR, CE, YG, HM, J, SS remain.
5. **No JSON/JSONL export** — records are in-doc only; `01_framework/editorial/golden_eval/` directory structure and manifest are specified but not created.
6. **No social card examples** — the social_comparison_card content type has no examples yet.
