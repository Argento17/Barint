---
id: TASK-443
title: cookies_coffee corpus integrity: repair truncated ingredient record 7290119043149 + completeness sweep (truncation caused false D->C: dropped E450/E500 + hydrogenated fat)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-440]
blocks: []
category_id: null
summary: >
  Re-scrape/repair the truncated BSIP1 record (ingredients cut at white-wheat-flour open-paren) that falsely scored the butter cookie NOVA-2/C. Sweep whole cookies_coffee corpus for other truncated records before any re-flow. Data-only.
---

# TASK-443 — cookies_coffee corpus integrity: repair truncated ingredient record 7290119043149 + completeness sweep (truncation caused false D->C: dropped E450/E500 + hydrogenated fat)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->


## SWEEP RESULTS (2026-07-01, orchestrator)
Scanned 61 cookies_coffee corpus records (run_cookies_001/output). **4 flagged:**
- **7290119043149** (butter cookie): TRUNCATED, ingredients="קמח חיטה לבן (" (14 chars). Complete list (8 ingredients incl. hydrogenated fats + E450/E500) exists in the cakes-corpus twin, BUT its provenance = `bsip1_text_fallback` / `bsip0_file_not_found` (NOT a clean direct scrape) — per OFF-ban/source policy + missing_data_discard_rule, DO NOT hand-substitute. Needs proper BSIP0 re-scrape.
- **80083764**: TRUNCATED, ends "...קמח חיטה מלאה (" (32 chars).
- **7290013740694**: nutrition-panel BLEED into ingredients ("...ללא צבעי מאכל ערכים תזונתיים...") — the same pollution pattern as HC/TASK-418.
- **7290119043798**: likely FALSE POSITIVE (ends with a clean allergen statement "מכיל גלוטן חיטה"); verify.

**LIVE page is CORRECT** — 7290119043149 shows D (47.7) on the live cookies page (built from a complete parse); the truncation only corrupts a FUTURE re-flow (which is why TASK-440 is held). No live bug.
**FIX (data pipeline, not hand-patchable under source policy):** BSIP0 direct re-scrape of 7290119043149 + 80083764; strip the nutrition bleed from 7290013740694; then cookies re-flow is safe. Until then TASK-440 stays blocked.
