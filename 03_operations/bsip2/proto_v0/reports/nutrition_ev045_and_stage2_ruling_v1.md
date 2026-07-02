# Nutrition Rulings — EV-045 Juice Emulsifier Penalty + Stage-2 (BARI_PROC_CONTINUOUS_V1) Activation Brief

**Author:** Nutrition Agent
**Date:** 2026-07-01
**Status:** ANALYSIS + RECOMMENDATION ONLY. No published score changed. No engine file edited. Nothing deployed.
**Both items owner-gated at activation (tripwire #1 — frozen invariant / published scores).**

---

## Deliverable 1 — EV-045 emulsifier-complexity penalty ruling (juices)

### 0. Correction to the brief's premise

The brief characterizes the mechanism as "a flat −4 penalty for 3+ trace stabilizers/emulsifiers." That is
**not what the code does.** `_emulsifier_complexity()` (`score_engine.py:1845`) is genuinely tiered — it
computes `highest_individual_penalty` (high=−5 / medium=−3 / low=−1, per `EMULSIFIER_COMPLEXITY_CONSTANTS`,
`constants.py:356`) **plus** a separate count-based `complexity_adjustment` (0 / 0 / −1 / −3 for 0/1/2/3+
distinct agents). A high-risk product (CMC/P80 present) could in principle land on −5 or more; a
low-tier-only product lands far lower. So the *architecture* honors the differentiated scale. The problem
identified below is narrower and more specific than "flat −4": **the count-based complexity adjustment
fires identically regardless of which risk tier the agents belong to**, and in the juice corpus, every
single firing case is low-tier-only. −4 is what that combination happens to produce for one juice, not a
uniform constant.

### 1. What actually fires in juices — traced against the live engine, not stale trace files

**Method.** The frontend-published `juices_frontend_v3.json` (`run_id: run_juices_task410_d4on`) is built
from BSIP2 trace files in `02_products/juices/bsip2_outputs/run_juices_yohananof_002/`, generated
**2026-06-07T17:37:45Z** — three days *before* ECS-v1/EV-045 landed (commit `117e7021`, 2026-06-10). Those
trace files have no `emulsifier_complexity_penalty` field at all and empty `tax_emulsifier_*` signal lists.
**The currently-published juice scores predate ECS-v1 entirely; EV-045 is not the mechanism behind any
currently-live juice score.** I re-ran the current engine (worktree `C:/bari_nutr_p282` @ `78d61c18`, canonical
juices pipeline `batch_run_juices_yohananof_002.py`: `input_loader → extract_signals → classify_category →
infer_nova → assign_evaluation_scope → score_product`, flags `BARI_RECAL_P0=on`, `BARI_TASK144_FIXES=off`) on
all 29 juice BSIP1 records live, to see what ECS-v1 *would* do if this run were regenerated today.

**Separately confirmed:** the TASK-410 D4 sulphite-activation script that produced the *actual* published
D→E moves (`02_products/juices/staging/task410_d4_activate/build_juices_d4.py:77`) explicitly stubs
`l3_stub = {"emulsifier_complexity_penalty": 0}` when computing its delta — i.e., the one juice D4 rescore
that did ship deliberately excluded ECS-v1's contribution. This corroborates: **EV-045 has never moved a
published juice score.** The brief's framing ("the ACTUAL mechanism dropping several juice scores") does
not hold against the artifacts; the actual live mechanism was D4 (E220 sulphite family), confirmed
score-neutral on grade (0 grade changes) per that run's own record.

### 2. Trace — 3 real juice records (live engine run, this session)

Of 29 scored juice records, **5 fire the ECS-v1 penalty; only 1 crosses a grade boundary.**

| Product | Agents detected | Tier | Penalty | Score w/o ECS → grade | Score w/ ECS → grade |
|---|---|---|---|---|---|
| `7290019056737` קריסטל מיץ אשכולית 2 ליטר (grapefruit) | pectin, gum_arabic, guar_gum (3 distinct) | **all low** | **−4** (−1 base + −3 complexity_high) | 36.33 → **D** | 32.33 → **E** |
| `7290006822192` מיץ חמוציות דיאט (cranberry diet) | pectin (1) | low | −1 | 40.9 → D | 39.9 → D (no move) |
| `7290019056355` תפוזינה לימונענע (orange-mint) | gum_arabic (1) | low | −1 | 34.37 → E | 33.37 → E (no move) |
| `7290013153418` / `7290110114916` סחוט לימונענע (lemon-mint, 2 SKUs) | pectin (1) each | low | −1 | 29.48 → E | 28.48 → E (no move) |

**Zero juice records in the current corpus contain a high-tier (CMC, P80) or medium-tier (carrageenan,
mono/diglycerides, DATEM, SSL, PGPR) agent.** Every firing agent across all 5 products is pectin, gum arabic,
or guar gum — thickeners with a food-technology role in juice pulp suspension, not the synthetic emulsifiers
EV-003/EV-019 built the tiered scale to flag. Direct trace of the grapefruit product's ingredient text:
`מייצבים (פקטין, E445, E414, E412)` — pectin, E445 (glycerol ester of wood rosin — genuinely a distinct
emulsifying agent, but classed here under `tax_emulsifier_low` alongside gum arabic/guar gum, not surfaced
separately), gum arabic, guar gum. The `highest_individual_penalty` component correctly caps this product's
identity-based penalty at −1 (low tier). **The entire −4 is the count-based `complexity_high` adjustment
(−3) stacked on top of that −1** — i.e., the grade-moving portion is not risk-graded at all; it's a bare
"3-or-more-of-anything" trigger.

### 3. Ruling on defensibility

**Verdict: the D→E move on the grapefruit juice is an over-penalty artifact of the complexity-count term,
not a defensible application of Bari's own differentiated emulsifier science. REFINE.**

Reasoning:
- Bari's public-facing scoring identity (`emulsifier_differentiation_live` memory; EV-003/EV-019) is
  explicitly built to distinguish CMC/P80 (−5, high concern) from lecithin/gums (−1, near-neutral,
  prebiotic-adjacent). The count-based complexity tier in EV-045 **erases that distinction at the moment it
  matters most** — it applies the same −3 "high complexity" surcharge whether the 3 agents are three
  synthetic high-risk emulsifiers or three plant-derived thickeners with a functional, declared purpose
  (juice pulp stability). A product that used 3 low-tier agents is being penalized as if agent-diversity
  itself were the concern, independent of what the agents are.
- This is precisely the failure mode the standing **red-label de-anchor directive** warns against: a binary/
  count-style trigger overriding continuous, risk-graded assessment. EV-045's own evidence-registry entry
  (`bsip2_evidence_registry_v1.md:1587`, risk_of_misuse #3) explicitly flags this exact risk in advance:
  *"Lecithin and prebiotic gums must not trigger the same penalty weight as CMC/P80."* In the live corpus,
  the complexity term does exactly that — the per-agent identity component stays correctly capped at −1, but
  the flat count surcharge (−3 for 3+, regardless of tier) is agent-identity-blind and produces the same
  grade-moving effect a 3-high-risk-agent product would get.
- **Publicly indefensible in this specific configuration.** If asked "why does a juice thickened with pectin,
  gum arabic, and guar gum — three food-technology-standard, GRAS, non-synthetic stabilizers — score a full
  grade band lower than the identical juice with two of them," Bari's own methodology doc (differentiated
  severity, not binary/count penalty) cannot answer "because count of distinct low-tier agents ≥ 3" without
  contradicting its own EV-003 doctrine.
- EV-051 (the NutriNet-Santé mixture-effect evidence upgrade) does **not** rescue this: EV-051's human-cohort
  anchor is specifically for the **modified-starch ∧ gum ∧ emulsifier co-occurrence cluster** — a named
  interaction pattern, not "any 3 distinct low-tier agents." Applying EV-051's outcome-anchor language to a
  pectin/gum-arabic/guar-gum-only product would be evidence misuse; EV-051 itself is still Nutrition-proposed
  and D7-pending, not activated.

**This is not a case for KEEP AS-IS.** It is also not severe enough to warrant "this move is illegitimate,
revert immediately" language on its own — the current corpus impact is exactly 1 product, 1 grade band
(D→E, both already low grades; not an S↔A-tier distortion) — but the *mechanism* generalizes badly the moment
any category has more than one low-tier-agent-heavy product, and it will misfire the same way again wherever
food-technology-standard thickeners cluster (juices, jams, dressings). Left as-is, it's a latent defect
waiting to recur, not an isolated one-off.

### 4. Specified refinement (NOT implemented — spec only; score-moving → D6/D7 + owner-gated)

**Behind a new flag, default OFF, byte-identical off:** `BARI_ECS_TIER_GATED_COMPLEXITY_V1`

Change: gate the `complexity_adj` (moderate/high count surcharge) so it only applies when the agent set
includes at least one **medium-or-higher** tier agent. Low-tier-only agent sets (pectin, gum arabic, guar
gum, agar, alginate, gellan, lecithins) are exempted from the count surcharge entirely — they still take
their per-agent −1 `highest_individual_penalty`, but never the −1/−3 complexity stack.

Pseudocode delta to `_emulsifier_complexity()` (`score_engine.py:1845`):

```
# current (unconditional):
if distinct_count == 0: complexity_adj = 0
elif distinct_count == 1: complexity_adj = 0
elif distinct_count == 2: complexity_adj = C["complexity_moderate"]
else: complexity_adj = C["complexity_high"]

# proposed (tier-gated), flag BARI_ECS_TIER_GATED_COMPLEXITY_V1=on:
has_medium_or_high = bool(high_agents) or bool(medium_agents)
if not has_medium_or_high:
    complexity_adj = 0   # low-tier-only agent sets never pay the count surcharge
else:
    # existing count logic, unchanged, applies only when >=1 medium/high agent present
    if distinct_count == 0: complexity_adj = 0
    elif distinct_count == 1: complexity_adj = 0
    elif distinct_count == 2: complexity_adj = C["complexity_moderate"]
    else: complexity_adj = C["complexity_high"]
```

Effect on the traced grapefruit product: penalty drops from −4 to −1 (per-agent low-tier penalty only,
complexity surcharge exempted) → score 32.33 → 35.33 → **grade reverts D** (crosses back over the 35.0
D-boundary). The other 4 firing products are already single-agent (`distinct_count==1`), so
`complexity_adj` was already 0 for them — no change.

**Rollback:** unset the env var; default-off preserves current (unrefined) behavior exactly.
**Scope:** applies to the shared `_emulsifier_complexity()` function — a live-corpus rescore under this flag
would need to check all categories (snack_bars, dairy_protein, sauce_spread, cereal, bread, cracker,
dessert — the EV-045 `affected_categories` list), not just juices, before any activation decision. This
report scopes the trace to juices only, per the brief; a full-corpus shadow run is required before D6/D7,
not included here.
**Requires:** Product Agent co-sign (D7) before any flag flips to `on` in any run — this is a score-moving
change per the standard rule, independent of the owner-gate on juices specifically.

---

## Deliverable 2 — Stage-2 (BARI_PROC_CONTINUOUS_V1) activation brief

### Status recap (verified against artifacts this session)
Branch `p277/stage2-continuous-proc` (commit `f449d8cb`, worktree `C:/bari_p277`), NOT on master. Flag
defaults `off` in both `score_engine.py:333` and `signal_extractor.py:58`; `score_processing_quality()`
(`score_engine.py:1677`) only routes to the continuous path `if BARI_PROC_CONTINUOUS_V1 and l3 is not None
and "has_refined_substrate" in l3` — confirmed as a genuine flag-gated branch, not a default-path change.
TASK-419 (CLOSED) already ruled the specific motivating case (Petit-Beurre vs. Chokita "inversion") is **not
a defect** — the chocolate cookie's macro panel is decisively worse (11.9g vs 4.0g sat-fat, 2 red labels vs
1), so the current ranking is correct on that pair. That closure is not revisited here; this brief is scoped
strictly to the separate, standalone question TASK-419 explicitly deferred: **should Design 1 activate on
its own philosophical merits, independent of the inversion case that originally motivated building it.**

The 700/1119-scores-move / 51/1119-grade-move shadow figures are **carried forward from the prior agent's
P277 report, not independently re-run by me this session** (no shadow-run artifact was committed to the
branch for me to re-verify byte-for-byte). Treat those two numbers as reported, not re-confirmed.

### 1. The philosophy question, in one sentence

Should Bari replace the rigid four-bucket NOVA-class lookup (`NOVA_PROCESSING_SCORES`, a flat score per
NOVA-1/2/3/4 tier) with a continuous, label-observable processing-burden signal — refined-substrate
penalties + bounded additive-category increment, offset by whole-food-complexity credit, clamped to a band
around the legacy NOVA anchor — demoting NOVA from sole authority to a non-authoritative corroborating
proxy?

### 2. Case for / against

**FOR — the defect it fixes.** The rigid NOVA lookup gives every product within a NOVA class the *same*
processing_quality score regardless of how refined its base actually is. A plain, additive-light,
white-flour biscuit and a whole-grain biscuit with one gum can both proxy to the same NOVA tier and get
identical processing credit — "plain + additive-light" reads as a free processing-quality pass even when the
substrate itself (refined flour/sugar/fat) is heavily processed. Design 1 closes that gap: it separately
scores refined-substrate presence, so a plain-but-refined product no longer coasts on the *absence* of
additives as if that made it minimally processed. This is a real, identifiable class of false-clean scoring,
and it's the kind of continuous-signal upgrade consistent with the standing de-chain-the-engine directive
(remove hard chains, let continuous assessment drive).

**AGAINST — is it better-calibrated or just different.** Two concerns, both load-bearing:
- **Scale of movement vs. verification depth.** 700/1119 scores moving and 51/1119 grade moves (per the
  carried-forward, not-independently-verified figures) is not a minor recalibration — it is a broad
  re-weighting of a dimension that's 15% of every score in the corpus. "Direction-sane on spot check" is a
  substantially lower bar than the re-audit standard this shop holds itself to for any full re-flow (see
  memory `rescore_full_reaudit_and_c3` — spot-checks have shipped fabrications before). Before activation,
  every one of the 51 grade moves needs individual verification, not a spot check.
  - **The NOVA-band clamp is a tell, not just a safety feature.** Design 1 deliberately clamps its
  continuous score to `NOVA_anchor ± band`, i.e., it cannot actually diverge far from the rigid lookup it's
  meant to replace. That's a sound engineering safety choice for a first activation, but it also means the
  "continuous" signal is really "NOVA plus a small, bounded wobble" — it has not been demonstrated to be a
  *better-calibrated* processing signal in the sense of tracking real-world processing burden more
  accurately; it's been demonstrated to *move* scores in a bounded, plausible-looking way. Those are
  different claims, and only the second one is proven so far.
- **The dimension weight ceiling already limits its own upside.** TASK-419's own finding: even a full,
  uncapped activation on a maximally-motivating pair (Petit-Beurre/Chokita) only moved processing_quality
  35→32 — not enough to flip the pair, because processing_quality is 15% weight against a 40% combined
  macro-panel weight. If the signal can't flip even its best-case motivating example, the "what does
  activation actually buy us" case rests entirely on the diffuse 700-score movement, which has not yet been
  shown to correct real errors rather than just redistribute noise.

### 3. Recommendation

**KEEP DORMANT for now — needs-more-shadow before an owner go/no-go, not ready to present as an activation
decision yet.** Not "no A/B menu" hedging — this is the single strongest-reasoned call available given what
exists today:

The case FOR (the plain+additive-light free-pass defect) is real and worth eventually fixing. But the
evidence bar for a 15%-weight, ~700-score-moving re-flow of live published grades is a full-corpus
re-audit of every grade-crossing case (the way TASK-418/419's own sibling work insists on for any re-score),
not a spot check. That audit does not exist yet — it is the concrete, scoped next step, not an open-ended
deferral: **run the 16-shelf shadow fresh (byte-identical-off already verified; flip on in a worktree), pull
the full list of the ~51 grade-crossing products, and Nutrition individually verifies each one the way EV-045
was just verified above** (real ingredient text, real macro panel, does the new grade make sense on its own
terms — not just "direction-sane"). Only after that audit exists is this a fair go/no-go to bring to the
owner. Activating on today's evidence would be presenting a bounded-plausible-looking re-flow as a verified
improvement when only the mechanism (not the outcome set) has been checked.

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:/Bari/03_operations/bsip2/proto_v0/reports/nutrition_ev045_and_stage2_ruling_v1.md",
      "sha256": "e7fe03e89aabbf718f45a7a0ecd076dc09bf9b6ed2aec79daddb7e1bd0ef5d1a"
    }
  ],
  "counts": {
    "juice_bsip1_records_loaded": 29,
    "juice_records_with_ecs_penalty_gt_0": 5,
    "juice_records_with_ecs_grade_move": 1,
    "juice_ecs_high_or_medium_tier_agents_detected": 0,
    "juice_ecs_low_tier_agents_detected_across_corpus": 5,
    "stage2_flag_files_touched": 2,
    "stage2_shadow_scores_moved_of_total": "700/1119 (carried forward from prior P277 report, NOT independently re-run this session)",
    "stage2_shadow_grade_moves": "51/1119 (carried forward, NOT independently re-run this session)"
  },
  "commands_run": [
    {"cmd": "git worktree add C:/bari_nutr_p282 78d61c18", "exit_code": 0},
    {"cmd": "python batch_run_juices_yohananof_002.py pipeline reproduced inline (29 BSIP1 records, live engine, score_product() direct call)", "exit_code": 0},
    {"cmd": "python inline: _emulsifier_complexity(l3) direct call on grapefruit record 7290019056737", "exit_code": 0},
    {"cmd": "git show 117e7021 --stat", "exit_code": 0},
    {"cmd": "git log --oneline --all | grep -i 418|419|EV-045|juice", "exit_code": 0},
    {"cmd": "git worktree remove C:/bari_nutr_p282 --force", "exit_code": 0}
  ],
  "not_done": [
    "SHA256 of this report not computed post-write (compute before archival if required)",
    "Full-corpus (non-juice) ECS-v1 shadow trace not run — EV-045 affected_categories list includes snack_bars/dairy_protein/sauce_spread/cereal/bread/cracker/dessert; this report is juices-scoped only per the brief",
    "Stage-2 700/1119 and 51/1119 shadow figures not independently re-run this session — carried forward from prior P277 orchestrator-verified report, flagged as such, not re-verified byte-for-byte",
    "No D6/D7 filed for either the EV-045 refinement spec or Stage-2 activation — both remain recommendations pending owner/Product routing per the brief's instruction not to close or route"
  ],
  "acceptance_test": "Both deliverables produced with real-record tracing (not simulated): EV-045 traced against the LIVE engine on all 29 juice BSIP1 records (published trace files found stale/pre-ECS-v1, disclosed), 1 exact grade-moving case identified and quantified; Stage-2 brief grounded in verified flag-gate code inspection + TASK-419's closed ruling, with unverified figures explicitly labeled as carried-forward. PASS on 'analysis only, no score/engine/deploy changes' constraint — worktree used for Deliverable 1 traces was created, read from, and removed; zero files in C:\\Bari main tree modified.",
  "decision_routing": {
    "EV-045 refinement (BARI_ECS_TIER_GATED_COMPLEXITY_V1)": "Recommend Product Agent co-sign review (D7) — score-moving spec, not yet implemented",
    "Stage-2 activation (BARI_PROC_CONTINUOUS_V1)": "Recommend KEEP DORMANT; next concrete step is a fresh full-corpus shadow + per-product grade-move audit, THEN owner go/no-go — not ready for tripwire escalation yet"
  }
}
```
