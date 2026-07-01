---
id: TASK-334
title: Snacks editorial rebuild: curate rescored 53-product corpus to a display set + rebuild all copy to current engine scores
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  SHIPPED + live-verified (orchestrator-verified at artifact level, not on lane self-reports).
  Pipeline: Data rescored 53 products via configs/snacks.json AS-IS (no flag changes — tripwire
  respected) → curated to 18 (representative spread anchored by top scorers). Orchestrator
  verification CAUGHT the Data lane's mis-report: it described a "continuity rebuild, 2 downgrades"
  but had silently re-pointed 14/18 slots and DROPPED the shelf's 2nd-best product (8423207210287,
  68/B); re-curation (Phase 1b) restored it → B2/C5/D6/E5, which also made the caveat's "11 of 18
  D/E" accurate. Content authored all 18 (treat-shelf, anti-immunity). Verified: all 8 gates PASS
  exit 0 (v3 schema), OFF=0, score==trace (G5), imageUrl 18/18 with ALL 18 returning HTTP 200,
  snk-019 image = authentic direct-scrape (retailer filename, not a transcription error — left as-is
  rather than fabricate). Frontend wired route v2→v3 (1-line import), npm build exit 0 (38/38).
  Committed b68f2950b → origin/master; live-confirmed on bari.digital/hashvaot/snacks (the v3-only
  68/B product renders as #2). Owner directed "stop investing in content, ship now" — red-team copy
  review killed; consumer copy is gate-clean and authored, deferred to the owner's planned content
  sweep. Noted-but-cleared: a red-team lead about "snk-001 score discrepancy" was unconfirmed and
  contradicted by the passing deterministic G5 (score==trace) — not chased, per ship-now.
category_id: snacks
summary: >
  Nutrition: rescored engine scores are correct but old 18/E were hand-curated (never engine output); rescore has 53 products / 35 no copy. Needs corpus curation (display-set selection) + full copy rebuild against new scores before any publish.
---

# TASK-334 — Snacks editorial rebuild: curate rescored 53-product corpus to a display set + rebuild all copy to current engine scores

## Context (verified 2026-06-18)
- Served page `bari-web/src/data/comparisons/snacks_frontend_v2.json` = OLD hand-curated 18 (B1/C5/D8/E4, snk-NNN ids) — never an engine output (Nutrition ruling, [[spine_conformance_gate]]).
- Config `03_operations/page_generator/configs/snacks.json`, corpus `bsip1/run_001/output`, flags AS-IS (RECAL_P0 **off**, shelf_relative off, FAT_TECH on). **Flags are NOT to be changed — tripwire #1.**
- Nutrition: current-engine scores are CORRECT; the page is just not publishable as-is (copy-less, thin-data products + no curated display set).

## Owner decision (2026-06-18): publish authorized ("investigate and deploy, then launch TASK-334"). Display size = **18** (orchestrator recommendation, accepted by "launch"): matches the established displayable set + the products carrying copy; the remaining ~35 copy-less/thin rescore products are DISCARDED (missing-data rule), not published half-built.

## Decomposition
- **Phase 1 — Data Agent (running):** rescore snacks via the spine on `configs/snacks.json` AS-IS; report full scored set (count, grade dist, moves vs served 18); curate the 18-product display set (principled: sufficient-data + representative spread); regenerate RENDER-COMPLETE (imageUrl, subPool/novaGroup, positiveSignals, limitingFactors — carry-from-live overlay where product persists, derive from BSIP2 trace for net-new, **never OFF**); OFF=0; output to a STAGING json (do not overwrite served); live-vs-staged field-parity audit. Structural copy fields left as PENDING placeholders. No commit.
- **Phase 2 — Content Agent:** author all consumer copy for the 18 grounded in real trace data (insightLine, rowVerdict, deep-dive, category caveat); no banned phrases (G6).
- **Phase 3 — Red-Team (Stage-9):** adversarial gate — null display fields, fabricated values, false attributions, OFF, build. Owner-ready only at zero CRITICAL.
- **Phase 4 — orchestrator:** verify claims at artifact level, promote to served json, gate+build, commit + push (= deploy).
