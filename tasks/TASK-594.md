---
id: TASK-594
title: board_check.py parser fixes: anchor status regex to frontmatter (indented return-block status false-positives) + scope-log header false stale_active
owner: data-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Found 2026-07-11 unattended run. (1) MISFILED false positives: TASK-200/201/202 frontmatter says CLOSED but board_check matches the indented 'status: RETURNED' inside the return_block YAML - the status regex must anchor to column-0 within the frontmatter block only. (2) STALE_ACTIVE false positives: closed tasks with deliberate '(history)/scope log' board sections (575/577/580/583/587) are flagged as active headers - exempt headers containing 'scope log'/'history', or match only non-history section titles. Both are checker precision bugs; the registry data is correct.
---

# TASK-594 — board_check.py parser fixes: anchor status regex to frontmatter (indented return-block status false-positives) + scope-log header false stale_active

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
