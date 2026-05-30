# Shared Framework

**Maturity:** Not yet written  
**Status:** Placeholder — cross-cutting concepts to be documented here

This directory holds framework elements that apply across multiple BSIP pipeline stages — concepts that are not specific to BSIP0, BSIP1, or BSIP2.

## What belongs here

- **Signal taxonomy** — the L1→L6 signal layer architecture that spans the whole pipeline
- **Product category taxonomy** — what categories exist, how they are defined, how classification works
- **Retailer registry** — canonical list of retailers, their codes, capabilities, and status
- **Evaluation philosophy** — what Bari is optimizing for; what it is not; anti-goals
- **Explainability budget** — how much explanation is allocated to each system layer
- **Glossary** — canonical definitions for terms used across BSIP0/1/2 documentation

## What does NOT belong here

Stage-specific design documents — those live in `bsip0_framework\`, `bsip1_framework\`, or `bsip2_framework\`.

## Cross-cutting documents already in bsip2_framework to consider promoting

The following documents in `bsip2_framework\` are broad enough that they arguably belong here:
- `signal_taxonomy.md` — the L1→L6 framework applies to all stages
- `evaluation_scope.md` — scoping philosophy applies to all stages
- `explainability_budget.md` — cross-cutting design constraint

These will be moved here when the framework matures. For now they are referenced from `bsip2_framework\`.
