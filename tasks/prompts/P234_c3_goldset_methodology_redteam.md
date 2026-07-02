(route: C3)

# P234 — Gold Set Phase 0: red-team the expert-rubric accuracy-gate METHODOLOGY (TASK-349)

Independent reviewer, no repo write access. Reasoning only — you do not implement, build, or close.
For each question give ONE clear recommendation, the single strongest reason, and the main risk if
wrong. Be adversarial: your job is to find where this design quietly fails or becomes dangerous.

## Context (facts, verified this session)
Bari scores packaged foods 0–100 → grade S/A/B/C/D/E across 10 dimensions (processing_quality,
nutrient_density, calorie_density, glycemic_quality, protein_quality, additive_quality,
satiety_support, fat_quality, regulatory_quality, whole_food_integrity), then caps/penalties/floors.
There is already a regression harness, **Shadow1** (`shadow_backtest.py`): it snapshots the engine's
OWN output as a baseline and flags when ENGINE CODE moves a score, with attribution. Shadow answers
"did it CHANGE?" — it has NO concept of whether a score is RIGHT. Its only correctness checks are
crude invariants (e.g. "no snack bar at grade A").

We propose a sibling, the **Gold Set**: a curated set of ~30 products, each with an expert-reviewed
EXPECTED grade band + score range + per-dimension direction (e.g. fat_quality: low), with a written
rubric rationale + source citation per criterion. A harness (`gold_check.py`) scores them at HEAD and
reports agreement vs the reviewed expectation. Exit 0 = all within band, 1 = advisory/borderline,
2 = engine output outside a reviewed band → a FINDING routed to the Nutrition lane (NEVER an
auto-change to scores or engine).

**Hard constraints already fixed:** changing published scores or scoring philosophy is a tripwire
that requires the owner; the gold gate must NOT auto-modify the engine. There is no human dietitian
on the team — the owner is a non-programmer/non-nutritionist. The proposed "two expert reviewers" are
two independent AGENT lanes: the Nutrition Agent proposes the expected band + rationale, the Red-Team
Agent independently reviews, agreement is recorded (target ≥90%, modeled on LifeSciBench).

## Questions
1. **Circularity risk.** The expected bands are authored by the same kind of model that could later
   justify the engine. Does an agent-authored "ground truth" reviewed by another agent give any real
   independent signal, or is it just the engine grading its own homework with extra steps? How do we
   make the gold labels genuinely independent of the engine's logic? (e.g. derive expected band from
   first-principles nutrition + the physical label, never from a Bari score.)
2. **Backdoor risk.** Could this gate become a covert path to change scores — i.e. someone "fixes" a
   gold disagreement by quietly tuning the engine to match the label, bypassing the tripwire/EV
   governance? What guardrail prevents the accuracy gate from becoming a score-change lever?
3. **Anchor selection.** Is "pick uncontroversial best/worst + a few ambiguous mid-tier" the right
   seed strategy, or does it bias the set toward cases the engine already handles? What kinds of
   products MUST be in a 30-item seed to actually stress the engine (adversarial/edge cases)?
4. **Band vs point.** We use expected RANGES (grade band, score range, dimension direction) not exact
   numbers. Is that the right granularity, or does it make the gate too loose to catch real errors?
5. **30 vs 200.** We propose seeding 30 reviewed products and scaling later, vs the ~200 the source
   benchmark implies. Right call, or a false economy that lets accuracy regressions hide?

End with the single biggest risk you'd flag to the owner before any build.
