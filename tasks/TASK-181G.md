---
id: TASK-181G
title: Glass Box W4 Data implement D3 de-moralization behind BARI_GLASSBOX_W4 OFF byte-identical
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-04
blocker: "Waiting on TASK-181F (EV-042 must bind the confidence criteria + confidence_scale + population_correlation values, Product D7 co-signed, before Data builds the scoring rules)."
depends_on: [TASK-181F]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
summary: >
  Implement the D3 reframe per spec section 2 + EV-042: d3_processing_signal struct (2.2); confidence-scaled modifier_score = 50 + (base_score-50)*confidence_scale (2.5); confidence-scaled PROCESSING_LOAD caps (4.1); REMOVE NOVA_HP_WEIGHTS NOVA-class amplification (HP reverts to direct-observation magnitude); wire the 3 final note_he strings A/B/C + C-mobile (spec 463-480). All behind BARI_GLASSBOX_W4 (default OFF). OFF = byte-identical to the W2 baseline (0-diff golden/frozen runs). Does NOT flip the flag live - go-live is a separate owner gate.
---

# TASK-181G — Glass Box W4 Data implement D3 de-moralization behind BARI_GLASSBOX_W4 OFF byte-identical

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
