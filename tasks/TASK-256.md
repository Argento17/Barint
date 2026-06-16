---
id: TASK-256
title: "Yogurts S-tier relaunch from clean run (shipcfg2): OFF purge, S=2 honest, page rebuild + full copy regeneration + claim gate → go-live"
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-12
depends_on: [TASK-254]
blocks: []
category_id: null
summary: >
  Registry-drift fix: the post-close yogurt chain (P10/P13/P16/P18/P19/P14) was
  riding the CLOSED TASK-249 id. This task is the relaunch's home. State at
  creation: authoritative clean run = run_yogurt_006_shipcfg2 (87 products,
  S=2 A=10 B=32 C=19 D=23 E=1; all 8 OFF-contaminated Yohananof records
  excluded with evidence per TASK-238; RT-1 exclusion; dedup machinery; Shadow
  CLEAN, engine e31614b89004b3d0). Owner S-grade ruling 2026-06-12: honest
  engine-recognized S ships, gated on Nutrition trace audit + very good
  consumer explanation — never capped to enforce framing.
---

# TASK-256 — Yogurts S-tier relaunch (shipcfg2)

## Chain & state
1. P13 (Nutrition audit, first S blessed) — ACCEPTED.
2. P16 (clean re-run shipcfg2, OFF purge, S=2) — ACCEPTED (orchestrator-verified
   run record, exclusion evidence, clean Shufersal source records).
3. **P18 (second-S confirmation + Hebrew explanations) — ACCEPTED 2026-06-12
   (orchestrator-verified).** Nutrition audited bsip1_yogurt_7290110565527
   dimension-by-dimension: weighted pre-bonus 82.62 reproduces, +8 Path A
   (declared "חיידקי יוגורט" → has_fermentation, r7_culture_credit NOT set, so
   YOGURT_TRIM correctly does not apply — trim contains Path B only), no caps/
   penalties fired, confidence 80/high. 90.6/S honest. **S_count=2 CONFIRMED —
   provisional status lifted.** Deliverable verified:
   02_products/yogurt_system/s_grade_explanations_v1.md — both Hebrew
   S-explanations (92.6 + 90.6, twins' 2-pt gap explained: fat 0 vs 1.5g,
   protein 10.5 vs 10.0g) + shared category-caveat line ("structural finding,
   not an applied ceiling — 2 of 87"). Rubric-compliant (no framework terms,
   every claim trace-entailed).
4. P19 (frontend rebuild, yogurts_frontend_v4.json, 18 products Shufersal-only,
   S-badge display check, strings PENDING_P14) — ACCEPTED.
5. **P22 (S-badge visual treatment) — ACCEPTED 2026-06-12 (orchestrator-verified).**
   Added S to `gradePalette` in `bari-comparison-tokens.ts` (deeper green, same
   hue family as A — no new color axis). All 3 chip components auto-inherit via
   `gradePalette[grade] ?? C`. `corpus.ts` stale comment fixed. Go-live = flip
   `v3`→`v4` in `yogurts-comparison-page-data.ts:3` + `yogurts-shelf-filters.ts:1`.
6. P14 (full copy regeneration vs shipcfg2 incl. both S explanations) —
   orchestrator drafts after P22 accepted.
6. Claim-gate pass on P14 copy (rubric v2, same as P17 rehearsal).
7. Owner read (read-every-string hard gate) → **go-live = owner call
   (tripwire 2)**.

## Notes
- One product (7290000408316, Yohananof-only) drops from the page until P6
  re-scrape delivers clean storefront data.
- First time the live site renders grade S — P19 must report display findings
  before any route change.
