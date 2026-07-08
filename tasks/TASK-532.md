---
id: TASK-532
title: yogurt-glp1-guide-data.ts:5 comment cites stale sha256 hash (pre S-vs-A fix)
owner: frontend-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Terminal red-team (TASK-504A) found a code comment citing sha256 43a988fd... (the copy hash BEFORE this session's S-vs-A prose fix); actual current hash is 4da1beef... Code-comment only, non-consumer-facing, does not affect the verified byte-match between source and built copy files. Cosmetic fix: update the comment to the current hash.
---

# TASK-532 — yogurt-glp1-guide-data.ts:5 comment cites stale sha256 hash (pre S-vs-A fix)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
