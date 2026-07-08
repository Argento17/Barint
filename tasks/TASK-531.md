---
id: TASK-531
title: GLP-1 guide (yogurt-glp1): pass a 4-field VM projection to the client component instead of the full BariProductVM (over-serialization into hydration payload)
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Terminal red-team (TASK-504A) found yogurt-glp1-guide-page.tsx receives the FULL BariProductVM per shortlist item but only renders score/grade/imageUrl/name -- the full expansion (ingredient text incl 10x fiber mentions, dimension-mechanic vocabulary like processing_quality/additive_quality, raw sub-scores) gets serialized into the page's self.__next_f hydration payload even though never rendered in visible DOM. Not a guardrail violation (consumer-invisible, page is noindex, fiber only appears as factual ingredient text never framed as remedy) but avoidable data-minimization gap on a framework-invisibility-sensitive page. Fix: pass {score,grade,imageUrl,name} projection from the loader, not the whole VM.
---

# TASK-531 — GLP-1 guide (yogurt-glp1): pass a 4-field VM projection to the client component instead of the full BariProductVM (over-serialization into hydration payload)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
