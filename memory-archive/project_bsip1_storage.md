---
name: project_bsip1_storage
description: Storage rule for BSIP1 concept and design artifacts — where they live and why
metadata: 
  node_type: memory
  type: project
  originSessionId: 41dec126-e15e-427c-a7d2-e5e93bc10a54
---

All BSIP1 concept, design, and schema artifacts live under `C:\Bari\bsip1_concept\`, NOT under `bsip0_scrape\` or any retailer folder.

Structure:
```
C:\Bari\bsip1_concept\
├── schemas\          JSON Schema definitions (bsip1_product_schema_v0_1.json, ...)
├── examples\         Example canonical products (example_bsip1_product.json)
├── docs\             README and architecture docs (README_BSIP1_SCHEMA.md)
├── merge_strategy\   Merge strategy documents (merge_strategy.md)
└── validation_notes\ Notes from schema validation passes
```

**Why:** BSIP1 is a cross-retailer stage, not a carrefour or yohananof artifact. Placing it under a retailer folder or under bsip0_scrape/schemas/ would imply it belongs to a single retailer or is part of BSIP0, both of which are incorrect.

**How to apply:** Any time a new BSIP1 file is created (updated schema, new example, design doc), it goes in this directory tree. Never under `bsip0_scrape/schemas/` or any retailer subfolder.

See also: [[project_bsip0_structure]] for BSIP0 layout and freeze locations.
[[bsip_pipeline_definition]] for BSIP0/1/2 definitions.
