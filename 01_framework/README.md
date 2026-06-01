# 01_framework — Bari Intelligence Framework

This directory contains the reusable, stage-independent intelligence layer of the Bari system: design documents, architectural decisions, scoring theory, and concept definitions.

**No operational code lives here. No run artifacts live here.**

## Structure

```
01_framework\
├── bsip0_framework\    Extraction layer design (field standards, handoff schema, retailer spec format)
├── bsip1_framework\    Consolidation layer design (canonical schema, trust layer, conflict resolution)
├── bsip2_framework\    Scoring layer design — primary and most developed (30 documents)
│   ├── docs\
│   │   ├── scoring\               Core scoring design documents
│   │   └── positive_structure_v1\ Positive structure architecture (6 documents)
│   └── validation\                Validation documents
├── shared\             Cross-cutting concepts (signal taxonomy, category taxonomy, glossary)
└── freezes\            Immutable point-in-time snapshots of framework states
    ├── bsip0_v0_2\                        BSIP0 scraper v0.2 milestone
    ├── bsip2_concept_v1_complete\         Full framework snapshot (pre-migration 2026-05-17)
    └── bsip2_concept_v1_partial_early\    Superseded early partial snapshot
```

## Maturity by stage

| Framework | Maturity | Documents |
|---|---|---|
| `bsip0_framework` | Early | 1 (README placeholder) |
| `bsip1_framework` | Early | 1 (README placeholder) |
| `bsip2_framework` | Developed | 30 (full scoring architecture) |
| `shared` | Not started | 1 (README placeholder) |

## Relationship to operations

Framework documents describe *what the system does and why*. Operational code in `03_operations\` describes *how it actually does it right now*. These can diverge during development — the framework is aspirational and normative; the operational code is the ground truth of current behavior.
