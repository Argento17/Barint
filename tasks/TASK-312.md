---
id: TASK-312
title: Fix 10 grade-vs-copy self-contradictions (RT-1 expanded) before push — granola 4 rowVerdict + hummus 6 insightLine
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-310, TASK-311]
blocks: []
category_id: null
close_reason: >
  Content Agent (Sonnet), orchestrator-verified by reading all 10 rewrites + full re-scan. All 10 self-grade contradictions
  removed: granola 4 rowVerdict (7290017962047/962023/106771369 grade B, 7290013433107 grade D) + hummus 6 insightLine (all
  grade D: 7290111563492, 3989096, 7290105366023, 7296073725640, 7290119374885, 7290106520905). The stale "נשאר/יורדת ל/ב-C"
  clause was stripped and each line restarted with the substantive reason ("אבל…"/"מיוצב ב…"/"החלבה מביאה…"); milk-quality
  preserved, calorie-density kept, sodium fact-only, no numbers changed, no framework leakage. FULL self-grade scan across all
  7 pages = 0 contradictions remaining. Scores/grades on the 10 unchanged; no other product touched. Edits in granola+hummus
  live JSONs. Reversible, not pushed.
summary: >
  Red-team RT-1 caught 3 granola cards showing grade B with rowVerdict saying "stays/drops to C". Orchestrator full-scan
  widened it to 10 true self-grade contradictions (granola 4 rowVerdict: 7290017962047 B, 7290017962023 B, 7290106771369 B,
  7290013433107 D; hummus 6 insightLine all grade D: 7290111563492, 3989096, 7290105366023, 7296073725640, 7290119374885,
  7290106520905 — all say "נשאר ב-C"). Verified pre-existing LIVE inconsistencies (grade unchanged live→staging; stale copy
  from an earlier run where the grade differed, never regenerated). Fix = rewrite the offending clause to reflect the ACTUAL
  grade, milk-quality, grounded in the product's own facts; comparative neighbor refs OK, but no self-grade assertion that
  contradicts the grade. Edit the bari-web live JSONs directly. Verify 0 self-grade contradictions after. Hebrew=Content/Sonnet only.
---

# TASK-312 — Fix the 10 grade-vs-copy contradictions before push

Context dump: `_rescore_staging/_rt1_fix_context.txt`. These are consumer-visible and must be fixed before owner push.
