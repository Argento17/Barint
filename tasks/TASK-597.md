---
id: TASK-597
title: bsip0_nutrition parser: comma-thousands misread + unreliable small-value unit token (sodium)
owner: data-agent
status: IN_PROGRESS
depends_note: folded into TASK-598 (owner re-route 2026-07-11)
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Found by TASK-595 adjudication (2026-07-11). Bug 1: _to_float (03_operations/bsip0/scrape/_shared/bsip0_nutrition.py:555) does replace(',','.') assuming decimal comma, so Shufersal thousands-comma values ('1,628' mg sodium) parse as 1.628 - a x1000 under-read. Verified live on brined-cheese raw capture bc-036/3075805. Bug 2: captured unit token is unreliable on small sodium values (snacks 7290019297208 raw {value:'0.2', unit:'mem-gimel'} - 0.2mg implausible, true value 0.2g=200mg; conflicts with the TASK-190 heuristic that TRUSTS the token). Fix _to_float comma disambiguation (comma followed by exactly 3 digits then end/unit = thousands separator) + add a sodium plausibility cross-check; extend test_bsip0_nutrition.py with both real cases. IMPACT: Shelf Watch weekly comparisons (nutrition live since TASK-590) would false-drift or under-read on these labels; any future rebuild replaying sodium hits it. Published site values are NOT affected (builders shipped correct values). Do not change any published JSON.
---

## Routing record (owner override, 2026-07-11)
First dispatch: Data Agent (sonnet, warm from TASK-590) — **STOOD DOWN minutes later on owner
instruction "Use Sol 5.6 to solve the BSIP0 malfunction"** (agent confirmed zero diff on both target
files before standing down). Re-routed: the fix is Part A of TASK-598 Round 1 (Codex gpt-5.6-sol,
BUILD-HEAVY, worktree C:/bari_wt_597), inside the owner-ordered full BSIP0 audit + Sol↔Claude
debate. This task closes when 598's Part A is verified.

# TASK-597 — bsip0_nutrition parser: comma-thousands misread + unreliable small-value unit token (sodium)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
