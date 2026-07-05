---
id: TASK-515
title: Yogurt comparison category — full build (BSIP0 scrape → BSIP2 → page → two-gate → red-team)
owner: data-agent
status: IN_PROGRESS
decision_log: >
  OWNER OVERRIDE 2026-07-05: "ignore [the scraper fix] please. you go on to build the pages with the data you
  obtained." The ≥3-source hard requirement is WAIVED for this build — proceed on the 2 usable sources (Shufersal
  119 + Yohananof) / 126-survivor corpus. Reversible: the scraper-fix prompt is preserved at
  tasks/prompts/yogurt_bsip0_scraper_fix_PROMPT.md if a future ≥3 pass is wanted. Pipeline resumes at BSIP1.
  Reversible scope defaults (log, agents may flag): labneh (4) EXCLUDED from yogurt pages (Nutrition ruled it
  DAIRY_SOLID/cheese); kefir moot (0 products); cottage excluded if present (scored elsewhere). Two pages by
  subpool: TASK-515 spoonable (~103) / TASK-515A drinkable (~23).
priority: HIGH
created_at: 2026-07-05
depends_on: []
blocks: []
category_id: yogurt
summary: >
  New yogurt category, whole build-page cycle, conforms to the spine + standards. Brings high-protein dairy (skyr/Greek/protein yogurt) into a scored corpus. Enables TASK-504A GLP-1 guide (yogurt+cottage+fortified milk shortlist) afterward. New category go-live = tripwire 2 (owner merge). Owner directive 2026-07-05.
---

# TASK-515 — Yogurt comparison category — full build (BSIP0 scrape → BSIP2 → page → two-gate → red-team)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
