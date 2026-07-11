---
id: TASK-596
title: Correct published fat values baked from EV-026 parser bug (cereals confirmed set)
owner: orchestrator
status: RETURNED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: cereals
summary: >
  Phase 1: correct 15 CONFIRMED_DISCREPANCY expansion.nutrition.fat values in cereals_frontend_v2.json to in-repo raw-panel replay (TASK-591). Phase 2: diagnose score impact, STOP (tripwire-1). Remaining shelves follow when TASK-595 damage scan lands.
---

# TASK-596 — Correct published fat values baked from EV-026 parser bug (cereals confirmed set)

## Context
Pre-TASK-142A EV-026 fat parser bug (trans-fat sub-row overwrote total fat → 0.5)
baked into `bari-web/src/data/comparisons/cereals_frontend_v2.json`. TASK-591
confirmed 15 CONFIRMED_DISCREPANCY cereals products (see
`03_operations/reports/task591_fat_ev026_audit.md`). Owner-approved 2026-07-11:
fix displayed values from in-repo raw-panel replay only; diagnose score impact and STOP.

## Phase 1 — DONE (proposed RETURNED; consumer-facing → owner merge)
Worktree `C:/bari_wt_596`, branch `task596-cereals-fat-fix`, commit `f872fd88`.
- Corrected 15 `expansion.nutrition.fat` values (0.5 → 2.0–13.6 g) in
  cereals_frontend_v2.json. **Only** that field touched (15 insertions, 15 deletions).
- Values from independent replay (`parse_nutrition_rows` + `parse_value_bound` on
  `nutrition_raw_source.rows`) = TASK-591 report exactly (0/15 mismatch). No OFF, no estimates.
- satFat left unchanged: published satFat already == replayed satFat for all 15.
- No copy on affected rows cites fat ("lean"/דל שומן) — verified, no contradiction.
- Both gates identical to baseline (only pre-existing TASK-563 G3/G5 fails; G8 still PASS).
- `npx tsc` clean; `next build` clean; render-verified served DOM: 0 fat==0.5, all 15 present.
- Note: cereals surfaces do NOT render nutrition.fat (grid = protein/sugar/energy/sodium;
  only brined-cheeses viz reads fat). This corrects the published DATA record.

**PR:** https://github.com/Argento17/Barint/pull/new/task596-cereals-fat-fix

## Phase 2 — DIAGNOSIS ONLY (no score moved; NOT a tripwire-1 escalation)
Did scoring inputs use the bugged fat? **NO.** Every bsip2 trace
(`run_cereals_008/products/*/bsip2_trace.json`) already scored on the CORRECT fat:
`L1_observed_signals.fat_g` = the replay value (e.g. 72968 → 9.4, fat_quality dim 93.0,
final 55.0), never 0.5. The EV-026 residue lived ONLY in the frontend-build JSON.
**Movement table: Δ = 0 for all 15** — re-scoring on corrected fat changes nothing,
because scoring never saw 0.5. No re-score needed; no published score moves.

## TASK-595 handoff note
TASK-591's CONFIRMED set is cereals-only (15). The other 7 fat==0.5 hits (bread ×2 in two
versions, yogurt-drinkable ×2, yogurt-spoonable ×1) are NO_EVIDENCE (no persisted raw panel)
→ untouched per the rule. Corpus-wide field-by-field corrections on OTHER shelves await
TASK-595's damage-scan report (`03_operations/reports/task595_nutrition_damage_scan.md`,
not yet landed; owned by another session in `C:/bari_wt_592`). Do NOT re-run that scan here.
