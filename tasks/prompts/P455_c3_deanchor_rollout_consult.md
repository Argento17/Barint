# P455 / Continuous red-label de-anchor — independent rollout review (route: C3)

You are the outside-the-family independent challenger (C3). Bari is about to begin activating a NEW scoring behavior across live categories (a tripwire-1 scoring-philosophy change, owner-approved in principle). Your job is to REFUTE its readiness and surface what has NOT been thought through — risks, blind spots, and anything that couldn't be publicly defended. You do not fix, approve, or close; you raise findings (CRITICAL / HIGH / MEDIUM) with specifics. This is additive advice (no veto); the orchestrator folds it.

## What is being activated (facts, not for re-litigation)
- Bari's engine currently punishes red-label products with hard "cliff caps": crossing a sugar / 2+-labels / saturated-fat threshold slams the final score to a fixed ceiling (55 / 45 / 55) regardless of everything else.
- New flag `BARI_REDLABEL_CONTINUOUS_V1` (DORMANT on master, default off) REMOVES those three cliff caps and replaces them with a continuous per-label penalty that scales with how far over the threshold a product is (via the `regulatory_quality` dimension, 5% weight). Verified properties:
  - OFF = byte-identical to today's published scores (confirmed independently: cakes 149/149 zero diff + full-run git-stash A/B).
  - ON genuinely moves scores (e.g. cakes 117 products move).
  - Inversion-invariant (a worse-panel product must never outrank its dominator) never regresses on any of 15 shelves; monotonic; trans-fat safety veto untouched.
  - Corpus-wide: ~700 small score-moves, ~20 grade-flips (orchestrator re-measured — the design agent's flip counts were slightly overstated; e.g. cheese=0 flips not 1, cakes=1 not 2). Every flip is a single-band boundary-straddle.
- KNOWN TRADEOFF (disclosed): "continuous" cuts BOTH ways. It is NOT pure relief for red-label products — a CLEAN product sitting just under a threshold (e.g. 16.5g sugar, no red label) loses ~2 points of the "clean bonus" it used to get from the cliff not reaching it. Net across the corpus is slightly more downward than upward moves.
- Prerequisites already cleared: (a) sodium double-count check on cereals/granola = GO (the cereal sodium rule and this flag are mutually exclusive by construction; 0 cereal products even carry a sodium label); (b) cocoa/chocolate = deferred behind a Product ruling that relief must be a per-product cocoa-solids gate (~≥70% dark qualifies; milk/white/filled bars get none), pending a Nutrition evidence entry.

## Planned rollout
Safe batch first (zero-move shelves bread/juices/milk/hard_cheeses = literally no change + cheese = 0 grade flips, only small number shifts) → then grade-movers one at a time (cereals, granola, cookies, cakes, snacks) each through content re-authoring + two content gates + Adversarial QA before owner go-live → chocolate last (after the cocoa evidence entry).

## Challenge these axes (raise a finding wherever the answer is "no / not defensible / not checked")
1. **Is "continuous instead of binary" the right answer to the owner's actual goal** ("drift away almost completely from the red-label thing")? The owner may have wanted red labels to matter LESS overall; this makes them matter *proportionately* (and adds a small tax to clean near-threshold products). Is that a mismatch worth surfacing, or the correct interpretation?
2. **The clean-product tax.** Is it defensible to LOWER the score of a clean product that has NO red label, purely because it's near a threshold? Could a consumer or competitor reasonably call that arbitrary? Where does it bite hardest?
3. **Removing the cliff caps** — do the caps protect against anything real (a genuinely bad product that the continuous 5%-weight dimension can't hold down)? Name a product archetype where losing the hard cap lets something indefensible score too high.
4. **Measurement trust** — the flip counts came from re-scoring the existing corpus, which has known baseline-reproduction drift on several shelves (published baselines don't reproduce). Does measuring ON-vs-OFF on a drifted corpus hide anything? Is the ~20-flip number trustworthy for an owner decision?
5. **Rollout sequencing risk** — activating category-by-category means the SAME red-label rule scores differently across live categories during the rollout window (cheese de-anchored while snacks still on cliffs). Is that a cross-category consistency problem a user could notice?
6. **Cocoa gate** — is a ≥70%-cocoa per-product relief line defensible, or does it create a cliff of its own (a 69% bar penalized, a 70% bar relieved)?
7. **Anything missing** — a category, an interaction, a safety property, or a copy/consumer-facing implication not on this list.

## Output
Ranked findings, most severe first: `severity | area | the problem | why it can't be defended / what's unverified | suggested direction (not final words)`. State explicitly which axes are clean. End with the machine-readable return-contract JSON block: finding counts by severity + an overall GO / GO-WITH-CONDITIONS / NO-GO recommendation on beginning the staged rollout, with the single decisive reason.
