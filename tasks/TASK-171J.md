---
id: TASK-171J
title: MVP acquisition build + real Israeli corpus run
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Build the ~8-10 day MVP acquisition adapter stack (third-party e-tailer generic adapter + Altman brand-site adapter + per-barcode source-priority resolver + claim-curation + QA/provenance/corpus-run harness) per the TASK-171I decision pack, then RUN it on the real addressable Super-Pharm shelf to MEASURE the actual corpus: real scoreable yield %, grade distribution, per-source contribution, residue. All candidate/EDPG; nothing ships; launch stays D10/D1. The MVP is a measurement instrument.
---

# TASK-171J — MVP acquisition build + real corpus run

## CLOSED 2026-06-03 — built + measured (agent hit a session limit before summarizing; orchestrator assembled the report from the run output + verified)
**Built:** `integrations/clients/il_supplement_panels.py` (3rd-party e-tailer + brand-site adapter), `il_panel_resolver.py` (source-priority resolver), corpus harness + caches under `02_products/supplements/real_corpus_v2/`. Report: `_corpus_report_v2.md`.

## ⚠️ THE MEASURED RESULT (decision-grade) — the MVP under-delivered
- **Scoreable yield = 6.8% (8 of 118 addressable SKUs)** vs the **~31–37% projection**. 110 SKUs = "no trustworthy panel." The feasibility probe's ~75–85% was hand-picked-optimistic; at scale the local-brand e-tailer/brand-site sources resolve almost nothing (per-source: altman 4, biogaya 2, vitamins4all 2).
- **Grade distribution: S:3 · E:5.** Engine scored every real product *correctly*: **Altman Vit D-1000 ×2 → S/91.2** (clean win); Altman Magnesium Balance 450mg oxide → **E/20** (safety veto, real over-dose); Altman Biotin → **E/34** (cosmetic Insufficient); TINC Mag Malate + SupHerb Mag Bisglycinate → **E/34** (claim didn't map — see calibration gap).
- Caveat: first run, cut short by session limit, no tuning → 6.8% is likely a **floor** (more sources + the claim-vocab fix would lift it), but far below projection.

## Two findings
1. **Acquisition yield is the binding constraint and is worse than projected (~7%).** A launch-credible corpus needs materially more sources + a thorough resolver, OR a manufacturer-feed (BD) path. **The "build the acquisition" case is weakened by the measurement.**
2. **Claim-umbrella vocab is incomplete for real Hebrew labels (Nutrition D6 calibration task).** Real products scored E because actual Hebrew claims ("עייפות/fatigue", "ספיגה/absorption") aren't in the dossier umbrellas — though **magnesium-for-fatigue is EFSA-authorized.** Umbrellas were built against expected/English claims, not the real Israeli shelf vocab. Fixable, depresses grades unfairly.

## Re-decision point (owner)
The MVP did its job as a measurement instrument. **Not launch-ready.** Options: (a) iterate acquisition (more sources + claim-vocab fix) + re-measure; (b) pursue a manufacturer-feed/BD path for local-brand panels; (c) pause — the engine is proven, the reachable corpus is currently ~7%. Launch stays a separate D10/D1; nothing shipped; all candidate.

# TASK-171J — MVP acquisition build + real Israeli corpus run

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
