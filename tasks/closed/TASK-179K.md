---
id: TASK-179K
title: Glass Box W1 go-live — Content finalizes Hebrew disclosure copy
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
depends_on: [TASK-179I]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
close_reason: >
  Hebrew disclosure copy finalized + verified (01_framework/glass_box/w1_disclosure_copy_v1.md): ניתוח חלקי
  label + tooltip, לא נוקד chip + canonical reason ("אין מספיק מידע בתווית כדי לדרג את המוצר"), "מה לא צוין
  בתווית" heading + one calm line per gap type. Caught + fixed a Q2 leak (replaced "רכיב לא זוהה בתווית" —
  reads as our failure — with "חלק מהתוספים צוינו לפי קבוצה בלבד"). No numbers, no jargon, no intent
  attribution. Flagged one Frontend unification: expansion-section.tsx L411 fallback differs from canonical
  reason (one-line edit) — carried into Data/Frontend wiring.
cc_comments:
  - flag: verify
    text: "Frontend: unify the withhold reason — expansion-section.tsx L411 fallback ('אין מספיק נתונים לאריזה זו כדי להציג פירוט.') must become the canonical 'אין מספיק מידע בתווית כדי לדרג את המוצר.' One-line edit, no logic change. Also: mobile tap-to-reveal for the ניתוח חלקי tooltip, or place that sentence as the first expansion line."
summary: >
  Go-live copy: Content finalizes/approves the consumer-facing plain-Hebrew wording for the D5/D6 states —
  each disclosure-gap note type (proportions not stated, ingredient unidentified, missing nutrition values,
  protein source unspecified, etc.), the לא נוקד withhold reason, and the ניתוח חלקי label. Frontend drafted
  strings; Content owns the final editorial. Calm register, plain everyday Hebrew, no accusation, no jargon.
  Output: a finalized wording dictionary (finding-type → Hebrew) for Data to wire.
---

# TASK-179K — Content finalizes Hebrew disclosure copy (Glass Box W1 go-live)

Part of TASK-179 (Glass Box), Wave 1 go-live. Drafts live in
`bari-web/src/lib/comparisons/glass-box-preview-data.ts` + the expansion component. Governance §9 register
(no "היצרן מסתיר"; use "לא צוין"/"לא ניתן לאמת"). Domain agent proposes RETURNED.
