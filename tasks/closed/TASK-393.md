---
id: TASK-393
title: Cookies-coffee full rework (freshness re-score + de-recite + metric + intro + two-gate)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-24
closed_at: 2026-06-26
close_reason: >
  DEPLOYED origin/master d62331554 (2026-06-26, owner "finish everything"). Freshness
  re-score: BARI_D4_SCORE_V1=on (cookies brought to the live D4 state every other shelf had) —
  24 score updates, 2 grade moves D->E (313184, 7290018893845), both crossing the D/E line on
  the sulphite contested-additive penalty; verified vs traces (live untouched until deploy).
  De-recite: the board's "57 reciters" premise was STALE (verified 0 panel-reciters on live);
  delivered de-recite + grade-consistency (0/119 mismatches) + Tom's-Voice naturalness (0 HIGH)
  via the two-gate (content author + independent Adversarial-QA, PASS). Gate caught+fixed real
  data defects pre-ship: a FALSE "sugar at red-label threshold" claim on 313184 (trace 17.5g, no
  red label) and invented additive specificity (גופרית דו-חמצנית -> labels' generic סולפיט, per
  each label's class). Metric (sugar+sat-fat) + intro (hero/prologue) already present. d4_additives
  byte-identical, OFF=0, 119 products. Config records D4=on for reproducibility.
depends_on: [TASK-394]
blocks: []
category_id: null
summary: >
  Cookies-coffee full rework (freshness re-score + de-recite + metric + intro + two-gate)
---

# TASK-393 — Cookies-coffee full rework (freshness re-score + de-recite + metric + intro + two-gate)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
