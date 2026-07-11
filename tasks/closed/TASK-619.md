---
id: TASK-619
title: BSIP0 nutrition parser: comma-thousands _to_float corruption fix + replay regression
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: [TASK-614]
category_id: null
lesson_trigger: failure
lesson_outcome: regression_test
lesson_artifact: 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py
lesson_validator: python 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py --selftest
lesson_evidence: "Root cause: blind `.replace(',','.')` in `_to_float` treated every comma as a decimal, corrupting thousands-separated Israeli-retail values 1000x (`1,200 מג` sodium -> 1.2 mg). Fix: `_normalize_decimal_comma` (strip `\\d,\\d{3}` thousands, convert `\\d,\\d{1,2}` decimal), wired into all 3 blind-replace sites. Regression codified IN the module: `--selftest` (13 cases incl. `1,200->1200`, `16,5->16.5`, `1,234.5->1234.5`, `פחות מ 0.5->0.5`), cp1252-console-safe. Verified by controlled HEAD-vs-fixed replay over 14,840 manifest rows: exactly 46 changed, all sodium, all thousands-comma, all <=1895 mg (ceiling 2000), rest byte-identical (task619_comma_replay_diff.json). Commit 6057f920."
close_reason: "VERIFIED + committed 6057f920. Checked: (1) diff artifact task619_comma_replay_diff.json = 46/14840 changed, fields=={sodium}, max_new=1895<=2000, all increased; (2) selftest exit 0 on a bare cp1252 console (the reported crash mode) after stdout.reconfigure hardening; (3) git status = only bsip0_nutrition.py + artifact touched, no collateral. Scope respected: no re-enrich/re-score/frontend. Unblocks TASK-614."
summary: >
  _to_float replace(',','.') corrupts thousands-separated values (1,200 mg -> 1.2). Israeli retailers use period-decimal, comma=thousands. Fix disambiguation + replay-harness byte-diff proving only thousands-comma values change. Unblocks TASK-614 re-score.
---

# TASK-619 — BSIP0 nutrition parser: comma-thousands _to_float corruption fix + replay regression

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
