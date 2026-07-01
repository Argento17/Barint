---
id: TASK-388
title: Adopt ZOE-style additive-quality scoring (activate tier + cosmetic-MUP density; refound count caps) — EXPLORE
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-24
closed_at: 2026-06-24
close_reason: >
  EXPLORE concluded — owner decision 2026-06-24. Finding (verified vs file:line + git):
  ZOE's "grade additives by quality, not presence" is ALREADY adopted via the live
  contested-tier D4 penalty (TASK-371, deployed 4e02bba06, 6 grade moves). The only
  remaining evidence-graded increment is phosphate (E450), but Product D7 co-sign
  (APPROVE-WITH-REVISION) established that broad phosphate penalty = penalizing
  baking-powder leavening in 2/3 of cakes — the 2026-06-21 "functional additive in
  native context" failure mode. The defensible, leavening-excluded version moves just
  ~1 product (oat-milk C→D) and would require a bespoke leavening-vs-emulsifying
  context classifier + full governance pipeline = over-build for 1 grade move
  (anti-overbuild, owner_systematic_not_artisanal). DECISION: declare ZOE adopted via
  contested-tier; do NOT build phosphate penalty. Emulsifying-phosphate logged as a
  known low-value gap to revisit only if processed-cheese / plant-milk scoring is
  deepened. NO published score changed (flags default-OFF). Side-deliverables shipped:
  EV-106 (Tufts/AJPH processing-harm evidence, verified DOI) + GLP-1 blog backlog BL-001.
depends_on: []
blocks: []
category_id: null
summary: >
  Explore activating the already-built D4 tier library + cosmetic_mup quality model into the headline grade (replacing/refounding the count-based ADDITIVE_MARKERS_3_PLUS/5_PLUS caps). Deliverable: D6 activation design + Tufts/AJPH EV entry as supporting evidence + live-corpus grade-move impact estimate. Owner sign-off required before any published-score change (tripwire #1).
---

# TASK-388 — Adopt ZOE-style additive-quality scoring (activate tier + cosmetic-MUP density; refound count caps) — EXPLORE

## Origin
Owner directive 2026-06-24: "I would adopt the ZOE approach to additives… let's explore this."
Triggered by the Hebrew Health Scan radar item "ZOE Processed Food Risk Scale — 4-factor
NOVA alternative." Research Agent evidence brief (2026-06-24) found ZOE's scale is not
peer-reviewed and carries a commercial conflict — but its core idea (grade additives by
**type/risk**, not mere presence) is sound and, critically, **Bari already implements a more
granular version of it.**

## Diagnosis (what already exists — verified at file:line)
- **Live scoring is count-based:** `PROCESSING_CAPS` in
  `03_operations/bsip2/proto_v0/src/constants.py:114-119` applies `ADDITIVE_MARKERS_5_PLUS`
  (additives≥5 → cap 60) and `ADDITIVE_MARKERS_3_PLUS` (≥3 → cap 72). Presence-counting —
  the NOVA-style "all additives equal" logic ZOE criticizes.
- **A graded library already exists (annotate-only):** `additive_tiered_library_v1.md`
  (EV-043) — 51 additives, 7 evidence tiers + a `cosmetic_mup` (Marker-of-Ultra-Processing)
  flag. Drives display copy only; no headline-grade weight.
- **A tier-weighted penalty exists but is mostly inert:** `compute_d4_score_penalty`
  (`score_engine.py:~1050`) behind flag `BARI_GLASSBOX_W2`. It weights only `contested`
  + `score_eligible` additives; **`D4_SCORE_COSMETIC_MUP_WEIGHT` is set to 0** — the quality
  term was built and then zeroed.

So this is an **activation + calibration**, not a build. The machinery is ~80% there.

## Scope (EXPLORE phase — produce a decision packet, do NOT change published scores)
1. **D6 activation design** (Nutrition, via `bari-bsip2-scoring-governance` skill):
   how tier severity + cosmetic-MUP density translate into the score; how this interacts
   with / replaces / refounds `ADDITIVE_MARKERS_3_PLUS/5_PLUS`; the cosmetic_mup weight to
   un-zero; activation scope; rollback (flag); label observability; rule-accumulation check
   (don't double-count vs ECS-v1 emulsifier penalty or sweetener caps).
2. **Adopt Tufts/AJPH as supporting evidence:** author the EV registry entry in
   `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` for
   Hatta-Langedyk et al., AJPH 2026, DOI 10.2105/AJPH.2026.308499 (processing as an
   independent harm pathway beyond sat-fat/sugar/sodium). Evidence tier = MODERATE
   (observational, no causation). Quote the authors' hedged line; flag over-reaches.
   This is the published-evidence backbone for *why* additive quality should move the grade.
3. **Impact measurement (self-verifying):** re-score the live corpus under the proposed
   activation (the trace data + `BARI_GLASSBOX_W2` flag already exist) and produce the
   grade-move distribution — per [[feedback_return_self_verifying]]: full distribution,
   most-common-count, a stable barcode/score/grade/caps table, trace-derived counts with
   the command used, and a baseline diff vs the committed scores.

## Definition of Done
- D6 design doc committed (proposal status; not activated).
- Tufts EV entry committed with verified DOI (citation gate: no fabricated identifiers).
- Impact table showing how many products / which categories move grade if activated.
- Clear recommendation: activate as-designed / revise / don't. NO published score changed.

## Governance / gates (do NOT skip)
- Changing published scores = tripwire #1 → **owner sign-off required** before activation.
- Requires **Product D7 co-sign** on the rule (scoring-rule co-sign is Nutrition+Product).
- Before any "done" on an actual activation: full re-audit of affected verdicts + C3
  review ([[rescore_full_reaudit_and_c3]]), conformance, render, red-team. This task's
  EXPLORE phase stops at the decision packet.

## ⚠️ Orchestrator correction (2026-06-24) — supersedes Nutrition's measurement
Nutrition's calibrated-MUP impact (RETURNED 2026-06-24: "35 products / 2 grade moves")
is WRONG — its script matched phosphate by Hebrew words only (`match_patterns_he`),
but the real engine `detect_additives_d4()` (score_engine.py:935) matches BOTH the
E-number form (`e450`/`e-450`/`ה-450`) AND the Hebrew words. It silently missed 72
products that list phosphate as "E450"/"450" (cakes collapsed 72→3 — baking powder).
**Engine-faithful re-measurement (orchestrator, `run_task388_groundtruth.py`, calls the
real detector):**
- Phosphate-carrying products: **107 / 480 (22%)** [not 35]. (16 products have no
  ingredient text on file → 107 is a floor.)
- Grade moves under −1: **6** [not 2] — 5× D→E (cakes/VOILA cookies/הדר biscuit),
  1× C→D (oat-milk 7394376620904).
- By category: cakes 43/65, cookies_coffee 46/119, cheese-spreads 11/53, milk 7/18;
  other 8 categories = 0.
- Ground-truth JSON: `C:\Bari\_task388_groundtruth.json`.
**Open judgment for D7:** most phosphate here is baking-powder LEAVENING (functional
raising agent), not a sensory-restoring "cosmetic MUP". Whether to penalize it as the
"ZOE adoption" is a Nutrition+Product call — flagged for Product D7 co-sign.

