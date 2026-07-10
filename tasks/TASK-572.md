---
id: TASK-572
title: BSIP0 gap: capture statutory label warnings (polyol >10%, aspartame/phenylalanine) at acquisition
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found 2026-07-10 (TASK-557, owner question). The mandated Israeli label warning 'צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת' appears in ZERO scraped product records. BSIP0 captures ingredients_raw/nutrition/brand/name/image_urls but no label-warning field. Consequence: we know which products CONTAIN polyols, but not which cross the 10%-by-weight threshold that triggers the warning. That warning is the ONLY dose signal available to a consumer, since polyol grams are not otherwise declared per-serving. Capturing it would make a whole class of honest, label-derivable claims possible ('this product crosses the line') that are impossible today. Scope: add warning-text capture to the acquisition layer (product page text and/or label image OCR), for the polyol warning and the aspartame/phenylalanine warning. Label-derivable, no scoring change proposed. Reg: תקנות הגנה על בריאות הציבור (מזון) (סימון מזון המכיל ממתיק מסוגים מסוימים), תשעט-2018.
---

# TASK-572 — BSIP0 gap: capture statutory label warnings (polyol >10%, aspartame/phenylalanine) at acquisition

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
