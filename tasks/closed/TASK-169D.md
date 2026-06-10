---
id: TASK-169D
title: "P2/P3 frozen wave — yogurt recal: R1-anchor top-trim decision + rescore"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
cc_reviewed: 2026-06-03
depends_on: []
blocks: []
category_id: null
close_reason: "Yogurt frozen wave SHIPPED LIVE. Owner decided option (b) cap-at-A (no S). Full chain executed + CC-verified: (1) corpus fixed — 190g protein SKU → 12.5 (OFF-sourced, cross-verified ×3), bio-naturel false +8 fixed via flag-gated marketing-prose filter (1-product radius). (2) Capped rescore run_yogurt_006_recal_p0_trim (config 6a01a8d83e2c325e): 15 A / 0 S, nothing ≥90, rollback OFF==OFF 86/86, golden/router clean OFF/ON/ON+TRIM. (3) Governance: Nutrition ENDORSED + authored EV-034 (yogurt +8 A-ceiling 89.9); Product D7 CO-SIGNED (covers option b only). (4) Reship: yogurts_frontend_v2.json rebuilt surgically from ship_capped (score/grade overwrite; macros preserved from run_004 because run_003 corpus carries EV-029 fat-overwrite — flagged, _meta.macros_note); 11 products = 6 A / 3 B / 1 C / 1 D, all match reship_before_after. (5) Content refreshed the inverted premise — prologue (4), 2 category notes, methodology comment, 10 insightLines (yog-008 fully inverted: was 'bottom of B' now tops shelf at A), 'נקי' prohibited token resolved. (6) QA caught + fixed a display bug: yog-008's capped 89.9 rounded to 90 (= the S threshold) → contradicted the cap; floored displayed score to 89/A (ScoreChip Math.round), copy reconciled 90→89. tsc 0 / corpus 0 err / next build clean (/hashvaot/yogurts). Deployed to master. NOTE: live yogurt page was stale (HEAD reproduced only 23/86 published run_004) so this is a deliberate stale→fresh re-baseline tied to TASK-178; macros still need the EV-029 corpus fix before a future full macro rebuild."
summary: >
  Frozen wave under TASK-169 — highest-judgment. P0 v1.1 produced a NEW yogurt distribution of 14 A / 3 S (35 yogurts legitimately +8 via gated live-cultures bonus). No prior numeric ceiling -> owner decision: accept the distribution or trim the top via the R1 yogurt anchor. Deliverable: present A/S distribution + before/after to owner, apply approved ceiling (R1 anchor trim if directed), rescore yogurt with BARI_RECAL_P0=on, reship yogurt frontend JSON + fix insight lines invalidated by new grades. Carries 169A router note (no top-level yogurt category; subtypes via name marker).
---

# TASK-169D — P2/P3 frozen wave — yogurt recal: R1-anchor top-trim decision + rescore

## Owner released the wave (2026-06-03)
Owner confirmed go on yogurt (3rd in order, after milk 169C + snack-bars 169E both closed). Unblocked → IN_PROGRESS. This authorizes the rescore + the decision package. Unlike milk/snacks, yogurt MOVES (P0 v1.1 predicted 14 A / 3 S), and there is NO prior numeric ceiling — so the deliverable is a verified rescore PLUS a clean accept-vs-trim decision for the owner. No ship until that decision.

## Scope / deliverable (Data Agent)
Rescore the frozen yogurt corpus with `BARI_RECAL_P0=on` into a NEW run id (published dirs + live `bari-web/src/data/comparisons/yogurts_frontend_v2.json` untouched). Produce:
1. **Verified before/after distribution** — live → recal grade counts; the full **A-list and S-list** (each product that reaches A/S, its score, and the driver — protein + the gated live-cultures +8).
2. **Culture-gate audit** — confirm the +8 fires ONLY on genuine cultured yogurts (not plain milk / non-cultured); list how many yogurts received it.
3. **R1-anchor top-trim model** — show the ALTERNATIVE distribution if the top is trimmed via the R1 yogurt anchor: which products drop from S→A or A→B, and the resulting counts. Give the owner a concrete A/B comparison: **(a) accept 14A/3S as-is** vs **(b) R1-anchor trim → [resulting counts]**.
4. **Drift separation (TASK-178 lens)** — does HEAD reproduce the published yogurt traces? Report the match count; separate recal effect from any HEAD-vs-published drift so we don't attribute drift to recal (milk found 13/20).
5. **Rollback** — flag-OFF rescore == published baseline byte-identical (N/N); golden + router clean OFF and ON.

Governance per `bari-bsip2-scoring-governance`. NO live score ships from this task — owner decides the ceiling on the verified numbers first, THEN a reship is scoped. Router note (from 169A): live router emits no top-level `yogurt` category — yogurt subtypes caught by name marker; verify the culture-gate keys on real router vocabulary. Do not invent data.

## Rescore verified + OWNER DECISION (2026-06-03)
Data rescore `run_yogurt_005_recal_p0` (config 38654862b46baaac, corpus run_yogurt_003 n=86) independently CC-verified: recal lifts yogurt 0A/0S → **11 A / 3 S** (OFF byte-clean 86/86; golden/router green). 10 of 11 A's + all 3 S's are driven by the gated live-cultures **+8** (35 yogurts, 0 leaks). Corrected the v1.1 "14A/3S" headline → **11A/3S** is authoritative (v1.1 doc was internally inconsistent).

**OWNER DECISION = option (b): cap yogurt at A, no S.** Implemented model = `BARI_RECAL_P0_YOGURT_TRIM` (+8 A-ceiling at 89.9) → **14 A / 0 S**, moves exactly the 3 S→A, 0 collateral, golden/router clean. Rationale: reserve the rare S grade rather than award it to engineered high-protein "GO/חלבון" yogurts lifted by the bonus, not nutrition ("best ≠ excellent").

**Ship is GATED (yogurt is NOT a same-day surgical ship like milk) — chain before live:**
1. **Corpus data fix (prereq):** `יוגורט גו נטול לקטוז` (bsip1_7290116932620) protein_g = 190.0/100g @ 86 kcal is CORRUPT (also wrong on the current live page @78.2/B) → source real value or mark insufficient (no invention). Plus the `יוגורט ביו נטורל 2.8%` false +8 exclusion (honey marketing-text bleed in ingredient field).
2. **Governance:** Nutrition authors an EV-registry entry for the yogurt +8 A-ceiling construct + soundness review; Product D7 co-sign (owner has set intent).
3. **Clean HEAD rescore** from the fixed corpus with `BARI_RECAL_P0` + `BARI_RECAL_P0_YOGURT_TRIM` ON (live page is STALE — HEAD reproduces only 24/86 published run_yogurt_004 → a clean rescore, NOT a patch; ties to TASK-178).
4. **Reship:** rebuild `yogurts_frontend_v2.json` (drift-safe), Content fixes insight lines invalidated by new grades, QA, owner final confirm, then deploy.

## Ship-prep DONE + owner approved reship (2026-06-03)
- Corpus fixed: 190g→**12.5** (OFF-sourced, cross-verified ×3); bio-naturel false +8 fixed via flag-gated marketing-prose filter (1-product blast radius).
- Capped rescore `run_yogurt_006_recal_p0_trim` (config 6a01a8d83e2c325e): **15 A / 0 S** (CC-verified, nothing ≥90); rollback OFF==OFF 86/86; golden/router clean. (15 not 14 = bio-naturel correctly regained its +8 → 85.5/A.)
- Governance: Nutrition ENDORSED the cap as-is + authored **EV-034**. **Product D7 CO-SIGNED 2026-06-03** — confirms (1) S reserved on yogurt shelf, +8 yogurt tops out at A/89.9, net 15A/0S; (2) yogurt-subtype-only, flag-gated, byte-identical rollback 86/86, exactly 3 former-S→A + 0 collateral (the +1 to 15A is the legitimate bio-naturel data-hygiene restore, not the cap); (3) ship-gating chain satisfied (corpus fixes + clean HEAD rescore run_yogurt_006_recal_p0_trim + Nutrition EV). CONDITION: EV-034 concept field reconciled 14→15 A. Standing approval covers option (b) cap only; reverting toward 11A/3S is a new D7+Nutrition gate. Reship + QA + deploy may proceed.
- Live-page impact (11 products): 8 grade moves, page goes 0→6 A (folds in recal + stale→fresh re-baseline; live was only 23/86 reproducible).
- **OWNER APPROVED the live reship (2026-06-03).** Executing: Product D7 co-sign → rebuild yogurts_frontend_v2.json from run_yogurt_006 (preserve the curated 11-product set) → Content refresh changed insight lines → QA → commit + deploy.
