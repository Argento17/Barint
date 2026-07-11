---
id: TASK-622
title: PD-3.1 refinements: English internal chrome, human list columns, status line, bar values, human actions, evidence-status fix
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-620
lesson_trigger: none
close_reason: "VERIFIED (render) + merged 88a2cdda. Built by Codex gpt-5.6-terra (BUILD primary, probed live), Opus-verified via real-DOM screenshots (localhost:3000, HTTP 200). All 6 owner points confirmed rendered: (1) clean English internal chrome 'Bari — Product Dossier (internal)' — consumer Hebrew header/footer/cookie-banner removed via internal-route-frame.tsx; Hebrew VerdictRow KEPT with 'Consumer-facing verdict' label; (2) list = human columns Product/Category/Score/Data quality (Good 80% / Partial 70%)/Main issue/Action needed/Last updated, pid hidden, filter chips; (3) status line 'Status: Barcode appears malformed. Score is not fully verified.' above the cards; (4) profile bars show values + 'higher is better'; (5) actions human-phrased ('Review barcode identity' + explanation), PID_SPLIT out of Overview; (6) Evidence not-retrieved cells now Status='Missing'/Confidence='Not available' (was contradictory 'Retrieved'). tsc clean on merged main. 14 files, net -239 lines."
summary: >
  Owner PD-3.1 round-2: (1) English UI chrome + 'Consumer-facing verdict' label on Hebrew VerdictRow; (2) human list columns (Product/Category/Score/Data quality/Main issue/Action needed/Last updated), hide pid; (3) strong status line above cards; (4) values on profile bars + 'higher is better'; (5) human-readable recommended actions (PID_SPLIT only in tech audit); (6) fix evidence status showing 'Retrieved' for not-retrieved cells.
---

# TASK-622 — PD-3.1 refinements: English internal chrome, human list columns, status line, bar values, human actions, evidence-status fix

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
