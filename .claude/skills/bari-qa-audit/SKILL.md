---
name: bari-qa-audit
description: Guide Claude through Bari QA validation — run QA runner, check traceability, identify hard fails and warnings, freeze baselines, and invalidate bad runs.
---

# Bari QA Audit Skill

**Owner:** QA Lead

## Use this skill when…

- You are running QA validation on a category corpus or enrichment output
- You are reviewing QA results and determining pass/fail
- You are freezing a QA baseline after a successful run
- You are investigating a failed QA run
- You are invalidating a QA run due to data contamination or pipeline error
- A user says "run QA", "check QA results", "validate category quality", "freeze baseline", "investigate QA failure", or "invalidate this run"

---

## QA Validation Protocol

### 1. Run QA Runner

- Trigger the QA runner against the enrichment output for the target category
- Confirm the runner is pointed at the correct pipeline run (by run ID or timestamp)
- Confirm the runner is using the current baseline (not a stale or invalidated one)
- Record: run ID, category slug, pipeline run reference, runner version

### 2. Check Traceability

Before evaluating results, verify traceability:

- Every product in the QA sample must be traceable to its source corpus entry
- Every label in the QA sample must be traceable to its enrichment step
- Every score in the QA sample must be traceable to its scoring rule
- If any product, label, or score is untraced: flag as a hard fail

### 3. Identify Hard Fails

Hard fails block promotion. Treat any of the following as a hard fail:

- Coverage below minimum threshold for any required label
- Label assigned to a product that is out of category scope
- Score produced by an unregistered or deprecated scoring rule
- Traceability gap (see above)
- Duplicate product entries in QA sample
- QA runner version mismatch with pipeline version

For each hard fail, record:
```json
{
  "fail_type": "<type>",
  "affected_product_ids": [],
  "affected_labels": [],
  "description": "<what went wrong>",
  "resolution_required": "<what must be fixed before re-run>"
}
```

### 4. Identify Warnings

Warnings do not automatically block promotion but must be explicitly accepted or resolved:

- Coverage between minimum and target threshold (acceptable but not ideal)
- Label distribution significantly skewed compared to baseline
- Enrichment confidence scores below target for a non-negligible portion of corpus
- New labels present that were not in the prior baseline (may indicate enrichment drift)

For each warning, record:
```json
{
  "warning_type": "<type>",
  "affected_scope": "<label, product set, or dimension>",
  "description": "<what was observed>",
  "owner_decision_required": "<accept | resolve>"
}
```

### 5. Freeze Baselines

After a clean run (zero hard fails, all warnings accepted or resolved):

- Freeze the QA baseline by recording the run ID and date
- Update the baseline reference for the category
- Record which warnings were accepted and by whom
- Forbidden: freezing a baseline over a run with unresolved hard fails

Baseline freeze record:
```json
{
  "category_slug": "<slug>",
  "baseline_run_id": "<run_id>",
  "freeze_date": "<ISO date>",
  "frozen_by": "<owner>",
  "accepted_warnings": [],
  "prior_baseline_archived": true
}
```

### 6. Invalidate Bad Runs

A run must be invalidated if:

- Pipeline ran against wrong corpus version
- QA runner had a known bug during the run
- Data contamination is detected post-run
- Run was not initiated from a clean pipeline state

To invalidate:
- Mark the run ID as invalid in the QA run registry
- Record the invalidation reason
- Do not freeze or reference an invalidated run
- Re-run from a clean state

Invalidation record:
```json
{
  "run_id": "<run_id>",
  "invalidated_date": "<ISO date>",
  "invalidated_by": "<owner>",
  "reason": "<description>",
  "replacement_run_id": "<new run id, if known>"
}
```

---

## Forbidden Actions

- Do not freeze a baseline over a run with hard fails
- Do not accept warnings without recording who accepted them and why
- Do not run QA against a stale or previously invalidated baseline
- Do not promote a category to BSIP2 with an unresolved hard fail
- Do not skip traceability checks even for small or low-stakes categories
- Do not invalidate a run without recording the reason and initiating a replacement run

---

## Expected Output Format

Final QA audit report:

```json
{
  "category_slug": "<slug>",
  "run_id": "<run_id>",
  "run_date": "<ISO date>",
  "auditor": "Claude (bari-qa-audit)",
  "traceability_check": "pass | fail",
  "hard_fails": [],
  "warnings": [],
  "verdict": "pass | fail | invalidated",
  "baseline_frozen": true,
  "baseline_run_id": "<run_id>",
  "promotion_blocked": false,
  "blocking_reason": ""
}
```

---

## Owner Mapping

| Responsibility | Owner |
|---|---|
| QA Runner | Data Architecture |
| Traceability Verification | Data Architecture |
| Hard Fail Review | QA Lead |
| Warning Acceptance | Category Team + QA Lead |
| Baseline Freeze Authorization | QA Lead |
| Run Invalidation | QA Lead + Engineering Lead |
