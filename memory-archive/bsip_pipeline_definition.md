---
name: bsip-pipeline-definition
description: Canonical definition of BSIP0 / BSIP1 / BSIP2 pipeline stages and responsibilities
metadata: 
  node_type: memory
  type: project
  originSessionId: 41dec126-e15e-427c-a7d2-e5e93bc10a54
---

## Pipeline stages

**BSIP0** — Raw retailer-specific capture
- Captures retailer reality as-is
- No normalization, no scoring, no cross-retailer logic
- Output: retailer-specific product.json with raw observations + provenance

**BSIP1** — Cross-retailer product consolidation and normalization
- Creates canonical deployable food records
- Consolidates multiple retailer observations into a unified product identity
- Responsibilities:
  1. Cross-retailer product identity resolution
  2. Canonical product object creation
  3. Provenance-preserving normalization
  4. Nutrition normalization into comparable units
  5. Ingredient normalization (non-interpretive)
  6. Conflict detection across retailers
  7. Confidence scoring for identity matching (NOT health scoring)
  8. Preservation of retailer observations (traceable back to BSIP0)
- Every normalized field must remain traceable to its BSIP0 source observation
- Must NOT: invent health scores, classify UPF/NOVA, rank products, interpret nutrition quality, make recommendations

**BSIP2** — Scoring / intelligence / interpretation
- Health scores, UPF/NOVA classification, product ranking, nutrition quality interpretation, recommendations

## Common mistakes to avoid
- Do NOT call BSIP1 a "scoring layer" — scoring is BSIP2
- Do NOT call BSIP1 a "parser cleanup layer" — it is cross-retailer consolidation
- "Confidence scoring" in BSIP1 refers to identity-matching confidence (is this the same product across retailers?), not health or quality scoring
- BSIP1 normalizes for comparability, not for interpretation

**Why:** User correction, May 2026. Previous docs incorrectly described BSIP1 as a scoring/cleanup layer.
