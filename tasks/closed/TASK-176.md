---
id: TASK-176
title: "Cottage fat-vs-protein weighting — a 9% cottage outranks 5% cottages on the live cheese page (whole-food rubric over-weights small protein deltas, under-weights fat %)"
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
cc_reviewed: 2026-06-03
depends_on: [TASK-169]
blocks: []
category_id: cheese
work_type: investigation
roadmap_impact: true
resolution: "Investigation complete — verdict KEEP engine (no recalibration, no live change). Close-readiness gate PASSED: cheese_frontend_v2.json confirmed UNCHANGED (no published score touched, guardrail honored); NOT-LIVE model artifacts present at 02_products/cheese_spreads/_model_task176/. Task premise (9% beats 5% on a protein edge) DISPROVEN against real traces: protein contributes only +0.4 wtd pt; the real driver is a NOVA-2 vs NOVA-3 split from an added-sugar marker (סוכר) in the cheap 5%s + the HP penalty — fat IS already penalizing the 9% (~-4.55) plus the sat-fat A→B cap. Proof independently verified in live data: a 5% with NO added sugar (che-2868996) scores 84/A while sugared 5%s score 77/B & 75/B — same fat band. Ordering is food-science-correct; no fat-monotonic rule fixes it without misranking a clean product below a sugared one. Friction is PRESENTATIONAL. Follow-ups are OWNER decisions, NOT auto-executed: R1 (Content/editorial — cheese verdicts should surface added-sugar; recommended, no D7) and R2 (optional, governed display-only number-clamp + bounded tie-break; needs Product+Nutrition D7 + owner sign-off)."
summary: >
  On the live cheese page, קוטג' 9% שומן scores 81/B while two קוטג' 5% שומן score 77/B and
  75/B — i.e. a higher-fat cottage outranks lower-fat ones, which reads backwards to a shopper.
  Driver appears to be the TASK-169 category-relative whole-food rubric: score tracks protein
  density almost linearly while fat % is a weak secondary signal, so a 0.4g protein edge (9% =
  10.5g vs the low 5%s = 10.1/10.2g) beats a 4-point fat difference. Same name "קוטג' 5% שומן"
  also spans 75–87 by brand (protein 10.1–11g). Investigate whether the rubric's protein/fat
  balance produces a defensible ordering for same-family products that differ mainly in fat,
  and whether a fat-aware tie-break or cap is warranted. Governed scoring change → roadmap_impact.
---

# TASK-176 — Cottage 9% outranks 5% (fat-vs-protein weighting)

## What a shopper sees (live cheese page)
Within the cottage family (`cheese_frontend_v2.json`):

| Product | id | score | protein/100g | fat |
|---|---|---|---|---|
| קוטג' 1% | che-7290014758681 | 90/A | 11.5 | 1% |
| קוטג' 3% | che-4127077 | 89/A | 11.0 | 3% |
| קוטג' 5% | che-4127329 | 87/A | 11.0 | 5% |
| קוטג' 5% | che-2868996 | 84/A | 10.0 | 5% |
| **קוטג' 9%** | **che-4127336** | **81/B** | **10.5** | **9% (sat 5.4g)** |
| קוטג' 5% | che-7290114310918 | 77/B | 10.1 | 5% |
| קוטג' 12% | che-7290116931241 | 76/B | 10.0 | 12% |
| קוטג' 5% | che-7290011194246 | 75/B | 10.2 | 5% |

The **9% cottage (81/B) outranks two 5% cottages (77/B, 75/B)**. To a shopper choosing on fat, that is backwards.

## Likely mechanism (to confirm against traces)
The TASK-169 whole-food rubric is **category-relative and protein-density-driven**; fat % is a weak secondary signal. So:
- The 9% has slightly more protein (10.5g) than the low 5%s (10.1/10.2g) — a 0.4g edge.
- That 0.4g protein edge outweighs the 4-percentage-point fat difference, lifting 9% above 5%.
- Note also the 9% is *already* held at B by the `_aCappedToB` saturated-fat A-ceiling — so without the cap it would score even higher (A-range) than the 5%s.

Secondary symptom: "קוטג' 5% שומן" as a name spans **75–87** purely on protein (10.1–11g), a 12-point swing under one label.

## Questions for Nutrition
1. Is protein density correctly the dominant driver, with fat near-zero weight, for *within-family* products that differ mainly in fat? Or is fat under-weighted?
2. Should a same-family ordering guarantee (lower fat ≥ higher fat, all else near-equal) or a fat-aware tie-break exist, so a 9% can't sit above a 5%?
3. Does the A-ceiling logic interact badly here — capping the 9% at B but still above lower-fat 5%s?
4. Blast radius: any weighting change re-scores cottage/white-cheese and likely propagates to milk/yogurt (shared rubric). Needs before/after table + Product/Nutrition D7 before any live change.

## Guardrails
- No live score change until owner sign-off (recal-went-live lesson, see [[task169_scoring_recal_sprint]]).
- Depends on TASK-169 (the rubric this stems from). Investigation + before/after model first; ship separately.

---

## Findings (Nutrition, 2026-06-03) — INVESTIGATION + MODEL ONLY, nothing shipped

**Model artifacts (NOT LIVE):** `02_products/cheese_spreads/_model_task176/`
- `TASK-176_model_v1.md` (full diagnosis + before/after + recommendation)
- `model_task176.py`, `model_task176_v2.py` (read-only, re-runnable)
- `cottage_before_after.csv`, `cottage_white_before_after.csv`

### Mechanism — the task's hypothesis is largely WRONG
The "9% beats 5% on a 0.4g protein edge" story is incorrect. Decomposing the 9% (81.1) vs the low 5%
טרה (76.9) gap against real traces: protein contributes only **+0.4 weighted pt**. The real driver is
a **NOVA-2 vs NOVA-3 processing split** caused by an **added-sugar ingredient marker** (סוכר) in the
cheap 5%s:
- 9% cottage (4127336): NOVA 2 (חלב/מלח/סידן, no added sugar) → processing 85, WFI 85, no HP penalty.
- 5% טרה / 5% (7290114310918 / 7290011194246): NOVA 3 (declares סוכר) → processing 65, WFI 60,
  glycemic −7.5, **−3.0 HP_fat_sodium penalty** (NOVA-3 gives the HP penalty weight 0.5; NOVA-2 zeros it).
- Fat IS already penalizing the 9% (~−4.55 wtd: fat_quality 41 vs 76, regulatory 60 vs 95) **and** the
  sat-fat A→B grade cap fires (`_aCappedToB`). It loses ~4.55 pts to fat yet still wins by being a
  cleaner-label product (~+4.6 from NOVA 2) while the 5%s eat the sugar/HP hit.
- Proof: a 5% with NO added-sugar marker (2868996) scores **84/A** — same fat, same protein band,
  different ingredient text. The 75–87 spread under the "5%" label tracks NOVA/sugar, not protein.

### A-ceiling interaction (Q3)
The sat-fat cap correctly caps the **grade** A→B but leaves the **number** (81) intact; the shelf
sorts within-family on the number, so the 9% still sorts above the 5%s. Cap interacts badly only in
that it's a letter cap, not a number cap.

### Blast radius (Q4)
Same pathology in **white-cheese-quark** (9% at 75 and 17% at 68 sit above weaker 5%s). Any fix is
**display-only** and scoped to fat-ladder `_cluster`s → **zero engine change, zero milk/yogurt
numeric propagation** (milk = legacy page, no recal JSON; yogurt recal unshipped).

### Recommendation: **KEEP the engine** (no recalibration, no fat re-weight)
The ordering is food-science-correct: the 9% outranks the cheap 5%s because those 5%s are genuinely
worse (added sugar → NOVA 3 + HP penalty), not because fat is under-weighted. No mechanical
fat-monotonic rule both fixes the headline and avoids misranking a clean product below a sugared one
(M1 over-corrects −17 B→C on white cheese; M3 changes nothing; M4 bounded tie-break only fixes the
genuine near-ties and leaves the defensible 9%>5% gap, correctly).

The friction is **presentational**, fixable display-only:
- **R1 (recommended, Content/D13 — no D7):** editorial — the 9% insight line should say it out-scores
  the cheap 5%s because of its clean label/no added sugar; the 75/77 5% lines should surface their
  added sugar. Honest, zero score-integrity cost.
- **R2 (optional, display-only, governed):** make the sat-fat cap also clamp the displayed *number*,
  combined with M4 bounded near-equal tie-break (Δ≤2). Touches 3 cottage + 3 white-cheese display
  values; **requires Product + Nutrition D7 co-sign + owner sign-off**; still no engine change.

**Proposed status: CLOSED** (investigation+model complete; KEEP verdict means no engine work to
schedule). If owner wants R2, spin a separate display-change task with D7 + owner gate. R1 can be a
Content task. **Closure needs CC roadmap review (cc_reviewed) per the guard — orchestrator runs the gate.**
