---
name: ""
metadata: 
  node_type: memory
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Built 2026-05-29. Amended 2026-05-29 (Section 5.2.1 added). Master document at `C:\Bari\01_framework\governance\consumer_usecase_guardrails_v2.md`.

**Why:** Purpose Framework v1 failed on category error (purpose is consumer property, not product property), taxonomy instability, detection circularity, and Indulgence immunity risk. This document is the controlled downgrade — smaller, safer, applied only where needed.

**How to apply:** Use-case reasoning is permitted in exactly four situations (comparison eligibility, explaining divergent decisions, marketing divergence findings, comparison caveats) and prohibited everywhere else. Apply at comparison construction time only — never upstream, never before scoring.

**Amendment (Cereals Gap Resolution v1):** Section 5.2.1 added — Claim Threshold Reference Table. Four claim types defined: whole grain composition (≥30%, first-ingredient test), whole grain dominant (≥51%, FDA/WGC standard), keto (≤5g net carbs/100g), high protein (≥20% calories or ≥15g/100g solid). Thresholds not in table cannot be used for Marketing Divergence Findings until documented at category launch (Constitution v1 criterion D6).

## Four-Point Conceptual Model

- **Product architecture** — observable nutritional reality (what is in it) — Bari's evidence base
- **Manufacturer claim** — commercial assertion to be evaluated against architecture, not authority
- **Consumer use-case** — relational, context-dependent, not fully inferable from product data
- **Comparison context** — the specific decision frame; where use-case reasoning is applied

None of the four is "ground truth." All four are inputs.

## Three Comparison Lenses (not product identities)

**Lens 1 — General Everyday Choice** (default)
Consumer making a routine purchase for normal consumption. No specific functional intent, no binding restriction. Products compared directly on nutritional architecture. Applies unless Lens 2 or 3 has positive architectural evidence.

**Lens 2 — Targeted Nutritional Function**
Consumer seeking a specific nutritional outcome (protein, fiber, probiotic). Both products must have architecturally supported functional positioning — claim alone insufficient. Products compared within the functional pool. Cross-lens comparison (Targeted vs General) requires use-case disclosure before score.

**Lens 3 — Dietary and Restriction-Driven Choice**
Consumer has a binding constraint (celiac, keto, vegan, developmental stage) that eliminates the general product from eligibility. Compared within restriction-compliant pool. Cross-lens disclosure required. Score is not reduced — architecture is stated with constraint context.

**Lens assignment rules:**
- Lenses assigned at comparison-time, never at product level
- Lens 1 is default; Lenses 2 and 3 require positive architectural evidence
- Ambiguous cases → Lens 1 (conservative interpretation)
- Lens assignment cannot improve a product's score

## Marketing Divergence Finding Standard

Triggered when all three conditions are met:
1. A specific purposive claim is present
2. The claim implies a specific nutritional standard in its ordinary meaning
3. The architecture falls materially short of the implied standard

**Standard format:**
```
MARKETING DIVERGENCE FINDING
Claim: [exact claim]
Observed: [measured value]
Expected: [threshold / category standard]
Gap: [quantified delta]
Finding: [claim] is [not supported / partially supported / unverifiable]
```

**Prohibited in findings:** intent attribution, product condemnation, findings without quantitative evidence, claims that the product should not exist.

## Anti-Immunity Rule (hard constraint)

> Purpose, use-case, and lens assignment can contextualize a score. They cannot excuse poor nutritional architecture. They cannot lower the bar. They cannot suppress or soften a score that reflects genuine nutritional limitations.

- Indulgence is not a protective category — never normalizes a low score
- Restriction products receive honest scoring — lens provides context, not score reduction
- Functional products still need dose evidence — claim-based score adjustment is prohibited
- "Different purpose" ≠ "nutritionally fine"

## Governance Answer

**C — Comparison-time guardrail.** Not a BSIP layer. Not a taxonomy. Not editorial-only (too weak). A comparison-time guardrail: three lenses + Marketing Divergence Finding + Anti-Immunity Rule.

[[bari-product-purpose-v1]]
[[bari-comparison-governance-v1]]
[[bari-governance-v1]]
