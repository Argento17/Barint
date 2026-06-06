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

### 5b. Red-Team Challenge

**Required for every category before advancing to BSIP2 Readiness. Do not skip.**

- Dispatch `red-team-agent` with the current corpus (scored JSON) and category methodology rationale
- Red-Team Agent produces a challenge report at `02_products/{category}/reports/red_team_{corpus_version}.md`
- Red-Team report must classify every finding as CRITICAL / HIGH / MEDIUM
- **Gate:** No CRITICAL findings may remain open before advancing. HIGH findings must be resolved or explicitly accepted (documented in the report)
- If CRITICAL findings are present: halt, return the report to Nutrition Agent for resolution, re-run Red-Team after fix
- Output: `red_team_{corpus_version}.md` — challenge report with all findings at CLOSED or explicitly accepted status

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

### 8. D4 Additive Wiring

**Required for every category. Do not skip.**

- Write a `wire_d4_<category>.py` script (modelled on `wire_d4_bread_vegspreads.py` and `wire_d4_snacks.py` in `03_operations/bsip2/proto_v0/reports/glass_box/w2/`)
- Ingredient source: BSIP1 `ingredients_text_he` field, keyed by barcode
- Explanation source: `01_framework/glass_box/w2_additive_copy_v1.md` (34 E-numbers, Hebrew copy)
- Run `detect_additives_d4(ingredient_text)` from the score engine on every product
- Enrich each detected additive with `explanation_he` from the copy doc; strip `match_source`
- Write `d4_additives` array into the frontend JSON; omit the key entirely for products with 0 additives
- **Coverage gate:** if fewer than 15% of products have ingredient text in BSIP1, halt and investigate the data gap before wiring
- **Invariant check (hard):** assert score, grade, and glassBox are byte-identical after writing
- Products with no BSIP1 ingredient text: log them; do not write an empty array; leave key absent
- Output: updated `*_frontend_vN.json` + console summary (products enriched / not found / invariant result)

---

## Forbidden Actions

- Do not skip the BSIP0 gate and jump to enrichment
- Do not proceed past any hard-fail gate
- Do not merge shelves across categories without explicit owner approval
- Do not modify corpus filter rules without recording the rationale
- Do not create a new category that duplicates an existing category's shelf scope
- Do not package for frontend before QA gate passes
- Do not advance past Stage 5 (QA Gate) until the Red-Team challenge report exists with no open CRITICAL findings (Stage 5b)
- Do not ship a category frontend JSON without running D4 additive wiring (Stage 8)

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
    "red_team_challenge": "pass | fail | skipped",
    "bsip2_readiness": "pass | fail | skipped",
    "frontend_packaging": "pass | fail | skipped",
    "d4_additive_wiring": "pass | fail | skipped"
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
| Red-Team Challenge | Red-Team Agent |
| BSIP2 Readiness | Scoring Governance Lead |
| Frontend Packaging | Frontend Architect |
| D4 Additive Wiring | Data Agent (script) + Content Agent (copy doc) |
