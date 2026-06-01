---
name: bari-category-factory
description: Guide Claude through Bari category factory tasks including shelf mapping, corpus filtering, BSIP gates, enrichment, QA, and frontend packaging.
---

# Bari Category Factory Skill

**Owner:** Data Architecture / Category Team

## Use this skill when…

- You are creating, modifying, or auditing a Bari product category
- You are mapping shelves to category definitions
- You are filtering the corpus for a category
- You are running or reviewing a BSIP0 gate, BSIP1 enrichment, BSIP2 readiness check
- You are packaging a category for frontend consumption
- A user says "build a category", "add a shelf", "run category pipeline", or "prepare category for frontend"

---

## Pipeline Stages

Work through these stages in order. Do not skip stages or reorder them.

### 1. Shelf Mapping

- Identify the canonical shelf slug(s) that belong to this category
- Verify each shelf exists in the shelf registry
- Confirm there are no duplicate shelf-to-category assignments
- Output: `shelf_map.json` — list of `{ shelf_slug, category_slug, mapping_rationale }`

### 2. Corpus Filter

- Apply corpus filter rules to restrict product corpus to this category's scope
- Validate that filter rules do not overlap with other active categories
- Confirm minimum corpus size threshold is met (do not proceed if corpus is too sparse)
- Output: `corpus_filter.json` — filter spec with product count estimate

### 3. BSIP0 Gate

- Validate that the category definition meets BSIP0 entry criteria:
  - Shelf map is confirmed
  - Corpus filter is non-empty
  - No blocking conflicts with existing categories
- If BSIP0 fails: halt and report blocking reason. Do not proceed to BSIP1.
- Output: `bsip0_gate_result.json` — pass/fail with evidence

### 4. BSIP1 Enrichment

- Run enrichment pipeline on corpus:
  - Attribute extraction
  - Label assignment
  - Comparison dimension selection
- Validate enrichment coverage meets threshold
- Output: `bsip1_enrichment_report.json` — coverage stats, label distribution, flagged products

### 5. QA Gate

- Run QA validation on enriched corpus (see also: `bari-qa-audit` skill)
- Hard fails block promotion to BSIP2
- Warnings must be reviewed and explicitly accepted or resolved
- Output: `qa_gate_result.json` — pass/fail, hard fails list, warnings list

### 6. BSIP2 Readiness

- Validate scoring logic is registered and approved (see also: `bari-bsip2-scoring-governance` skill)
- Confirm label observability is in place
- Confirm rollback plan exists
- Output: `bsip2_readiness_checklist.json`

### 7. Frontend Packaging

- Package the category for frontend consumption:
  - Export comparison page data structure
  - Export RTL-safe labels
  - Validate Hebrew label coverage
- Output: `frontend_package.json` — structured for Bari website consumption

---

## Forbidden Actions

- Do not skip the BSIP0 gate and jump to enrichment
- Do not proceed past any hard-fail gate
- Do not merge shelves across categories without explicit owner approval
- Do not modify corpus filter rules without recording the rationale
- Do not create a new category that duplicates an existing category's shelf scope
- Do not package for frontend before QA gate passes

---

## Expected Output Format

At each stage, produce a structured JSON artifact named as specified above. After all stages complete, produce a summary:

```json
{
  "category_slug": "<slug>",
  "pipeline_run_date": "<ISO date>",
  "stages": {
    "shelf_mapping": "pass | fail | skipped",
    "corpus_filter": "pass | fail | skipped",
    "bsip0_gate": "pass | fail | skipped",
    "bsip1_enrichment": "pass | fail | skipped",
    "qa_gate": "pass | fail | skipped",
    "bsip2_readiness": "pass | fail | skipped",
    "frontend_packaging": "pass | fail | skipped"
  },
  "blocking_issues": [],
  "warnings": [],
  "promoted_to_frontend": true
}
```

---

## Owner Mapping

| Stage | Owner |
|---|---|
| Shelf Mapping | Category Team |
| Corpus Filter | Data Architecture |
| BSIP0 Gate | Category Team + Data Architecture |
| BSIP1 Enrichment | Data Architecture |
| QA Gate | QA Lead |
| BSIP2 Readiness | Scoring Governance Lead |
| Frontend Packaging | Frontend Architect |
