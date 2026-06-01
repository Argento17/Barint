---
name: bari-bsip2-scoring-governance
description: Guide Claude when proposing or modifying Bari scoring logic — enforces evidence registry, label observability, activation scope, rollback plans, and prevents rule accumulation.
---

# Bari BSIP2 Scoring Governance Skill

**Owner:** Scoring Governance Lead

## Use this skill when…

- You are proposing a new scoring rule for any category
- You are modifying an existing scoring rule
- You are reviewing a scoring PR or scoring config change
- You are adding weights, thresholds, penalties, or boosting logic
- A user says "add a scoring rule", "change the score for", "update scoring weights", "tune the algorithm", or "modify BSIP2 logic"

---

## Governance Checklist

Every scoring proposal or modification must satisfy all five requirements before it is accepted.

### 1. Evidence Registry Reference

- Every scoring rule must cite at least one entry in the Bari evidence registry
- The registry entry must show:
  - The business signal that justifies the rule
  - The data source that supports the signal
  - The date the evidence was recorded
- If no registry entry exists: create one first, then reference it
- Forbidden: adding a scoring rule based on intuition alone without evidence

### 2. Label Observability

- Every scoring rule that reads a label must confirm that label is observable:
  - The label exists in the label registry
  - The label has a defined coverage threshold
  - Coverage metrics are being tracked (not just assumed)
- If the label is not observable: block the rule and require observability setup first
- Forbidden: referencing a label in scoring that has no coverage tracking

### 3. Category Activation Scope

- Clearly define which categories this scoring rule applies to
- Forbidden: writing a global scoring rule that applies to all categories without explicit multi-category approval
- If the rule is category-specific: scope it explicitly in the rule definition
- If the rule is intended to be cross-category: require written approval from all affected category owners

### 4. Rollback Plan

- Every scoring change must include a documented rollback plan:
  - What the previous state was
  - How to restore it (config reference or version tag)
  - Who to notify if rollback is triggered
- Forbidden: merging a scoring change without a rollback reference

### 5. Rule Accumulation Prevention

- Before adding a new rule: check if an existing rule already addresses the same signal
- If an existing rule covers it: modify the existing rule rather than adding a new one
- If rules have overlapping scope: flag for consolidation review before proceeding
- Forbidden: adding a new scoring rule that creates a shadow of an existing rule

---

## Review Protocol

When reviewing a scoring proposal, produce a governance verdict in this format:

```json
{
  "proposal_id": "<id or description>",
  "review_date": "<ISO date>",
  "reviewer": "Claude (bari-bsip2-scoring-governance)",
  "governance_checks": {
    "evidence_registry_reference": "pass | fail | missing",
    "label_observability": "pass | fail | missing",
    "category_activation_scope": "pass | fail | missing",
    "rollback_plan": "pass | fail | missing",
    "rule_accumulation_check": "pass | fail | flagged"
  },
  "verdict": "approved | blocked | needs_revision",
  "blocking_reasons": [],
  "revision_requests": []
}
```

A verdict of `approved` requires all five checks to pass. Any `fail` or `missing` blocks approval.

---

## Forbidden Actions

- Do not approve scoring rules without evidence registry references
- Do not allow global scoring rules without explicit multi-category sign-off
- Do not proceed without a rollback plan documented
- Do not add a new rule that duplicates the signal of an existing rule
- Do not modify scoring weights without checking label observability first
- Do not accept "it feels right" as evidence for a scoring change

---

## Expected Output Format

Produce the governance verdict JSON above. For approved proposals, also produce:

```json
{
  "approved_rule": {
    "rule_id": "<assigned id>",
    "category_scope": ["<slug>"],
    "evidence_registry_ref": "<ref>",
    "label_refs": ["<label>"],
    "rollback_ref": "<version or config path>",
    "effective_date": "<ISO date>"
  }
}
```

---

## Owner Mapping

| Responsibility | Owner |
|---|---|
| Evidence Registry | Data Architecture |
| Label Observability | Data Architecture |
| Category Activation Scope | Category Team |
| Rollback Plan | Engineering Lead |
| Rule Accumulation Review | Scoring Governance Lead |
| Final Approval | Scoring Governance Lead |
