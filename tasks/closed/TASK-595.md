---
id: TASK-595
title: Corpus-wide damage scan: ALL published nutrition fields vs in-repo raw panels (extends TASK-591)
owner: nutrition-agent
status: CLOSED
close_reason: >
  BUILD-LIGHT (Codex gpt-5.6-terra) scan delivered, C0 PASS, both sanity anchors held (15 cereals
  reproduce; MATCH-majority on evidence-rich shelves: hummus 57/57, granola 22/22, cookies 95/95).
  Raw scan verdict: 39 MATERIAL rows / 359 evidence-backed products. ORCHESTRATOR ADJUDICATION
  (independent replays, appended to the report): 24 brined sodium rows + snk-018 are REPLAY-SIDE
  ARTIFACTS - published values CORRECT; root cause = _to_float comma-as-decimal at
  bsip0_nutrition.py:555 misreads thousands-comma ('1,628' mg -> 1.628, verified live on bc-036)
  plus an implausible small-value unit token on snk-018. Parser bugs registered as TASK-597 (HIGH,
  urgent: Shelf Watch weekly run 07-12 will make its first real nutrition comparisons post-590).
  ADJUDICATED DAMAGE: 15 products, ALL cereals (fat, EV-026) - fix scope unchanged from TASK-591.
  Also surfaced: ~95 FIELD_GAP rows (cookies carbs / ricecakes satFat+carbs displayed as None while
  evidence exists) = completeness backlog; 398/757 products have NO in-repo panel (bread, cheese,
  chocolates, juices, milk, yogurt-drinks unprovable either way). Report:
  03_operations/reports/task595_nutrition_damage_scan.md (adjudication section at end, read FIRST).
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner directive 2026-07-11 ('let's see what the damage is - scan for other shelves'). TASK-591 scanned one signature (fat==0.5, EV-026): 15/20 cereals CONFIRMED wrong. Extend to the full question: for EVERY product in EVERY served *_frontend_v*.json, replay every persisted in-repo raw panel (nutrition_raw_source.rows under 02_products/** and 03_operations/bsip0/**) through the correct *_raw mapping and diff EVERY nutrition field against the published expansion.nutrition values. Bucket deltas by magnitude (rounding-level vs material) so damage is measured honestly. READ-ONLY; no corrections; any score-movement implication = tripwire-1 movement table only. BUILD-LIGHT Codex terra, worktree.
---

# TASK-595 — Corpus-wide damage scan: ALL published nutrition fields vs in-repo raw panels (extends TASK-591)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
