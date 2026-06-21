---
id: TASK-350
title: Admin blog editor — extend /admin to edit blog article prose (all blog pages), prose-only
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-19
depends_on: [TASK-340]
blocks: []
category_id: null
summary: >
  Migrate blog article prose from src/lib/blog/*-content.ts into JSON data files (page-config code stays), then add a Blog section to /admin reusing the auth/github/save infra with a generic Hebrew-prose recursive extractor (links/slugs/ids/citation-urls excluded). Done in verified waves: clean article pages (hummus/milk/yogurt/olive-oil/bread) first, then snack-editorial + blog-index. Built on feature/admin-blog-editor; owner-gated go-live.
---

# TASK-343 — Admin blog editor — extend /admin to edit blog article prose (all blog pages), prose-only

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
