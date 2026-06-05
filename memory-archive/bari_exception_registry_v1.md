---
name: bari_exception_registry_v1
description: "Deliberate architecture exceptions approved for production; each entry defines the exception, justification, and multiplication constraints"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Registry file: `C:\Bari\01_framework\governance\exception_registry_v1.md`

**Why:** The Bari template architecture is frozen. Exceptions must be explicitly documented and approved to prevent drift. Undocumented exceptions are violations.

**EXCEPTION-001 — Bread fermentation filter tooltip**
- What: ⓘ icon on the filter label "ללא מחמצת מזוהה" only; shows 1–2 sentences explaining signal vs. packaging claim
- Approved text: "מחמצת לא זוהתה ברשימת הרכיבים. המוצר עשוי לציין שאור על האריזה."
- Why allowed: מחמצת is consumer-facing packaging language, not internal framework; the tooltip explains a label gap the consumer can independently verify
- Why not leakage: No NOVA, BSIP, cap, routing, or structural class is mentioned; only words already on bread packaging
- Constraints: **Only tooltip in entire product**; bread category only; filter label only; cannot inherit to other categories without new registry entry; text is fixed, not dynamic

**Governance:** New exceptions require answering 4 questions (rule violated / consumer need / no in-template solution / multiplication constraints) before approval. See registry file for full governance procedure.

**Related:** [[bari_comparison_template_v1]] [[bari_insight_line_spec_v1]]
