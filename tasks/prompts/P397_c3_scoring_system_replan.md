(route: C3)

# P397 — C3 INDEPENDENT REVIEW: re-plan the Bari scoring-system overhaul

You are C3, the independent outside reviewer. The Bari product owner has concluded that
a series of surgical fixes to one scoring signal (the "NOVA proxy") is the wrong frame —
the engine needs a whole scoring-system review, run as a real program. You are one of four
participants (the others: in-house Nutrition, Data, and Red-Team agents) asked to RE-PLAN it.
Evidence-grounded independent opinion only — no code, no data production, you never close work.

## How Bari scores
Bari rates packaged foods 0–100 / A–E on "nutritional architecture." A continuous weighted
sum of ~10 dimensions (processing, nutrient density, glycemic, protein, additives, satiety,
fat quality, etc.) is then clamped by a thick layer of HARD OVERRIDES the owner calls "chains":
~40 of them — score CAPS (sugar→55/60, 2-red-labels→45, NOVA-4→68, 3+ additives→72…), rigid
NOVA-class step LOOKUPS ({1:95,2:85,3:65,4:35}), binary red-label caps, and floors.

## What just happened (the trigger + what we learned)
- A verified INVERSION: a worse cream cookie (29g sugar, 8.6g sat-fat, palm oil, 2 red labels)
  scored 26/E, ABOVE a plain biscuit (22g sugar, 4g sat-fat, 1 red label) at 21/E.
- Root cause was diagnosed and surgically fixed (NOVA misclass + a half-wired confidence-
  discount + a brittle additive parser). The cookie now ranks correctly (cream 18.2 < plain 21.4).
- BUT measurement revealed the surgical frame is insufficient:
  1. The cookies category alone still has **~200 worse-beats-better inversion pairs** — the fix
     corrected one; the rest are produced by the chains themselves.
  2. **8 of 12 live categories' committed/published baselines CANNOT be reproduced by today's
     engine** (provenance drift) — so before/after drift cannot be trusted on those.
  3. Every fix so far moves scores only DOWNWARD; the owner's stated goal ("give the algorithm
     freedom, remove the chains") — letting good products RISE as caps come off — is untouched.
- Owner directive stands: move OFF the rigid NOVA lookup + the caps, toward continuous/graduated
  assessment; keep only genuine safety vetoes (trans-fat=0) + an outcome guardrail (a within-
  category "a worse product must not outrank a better one" invariant, now built).
- Hard constraints: ~847 products across 12 LIVE consumer-facing categories; any change re-flows
  PUBLISHED scores; deploy is owner-gated; firewall = engine reads only in-house scraped labels
  (no external nutrition DBs); "we never cut corners."

## Re-plan it — answer ALL, concretely (≤1000 words)
1. **Is a whole-system overhaul the right call, or continued patching?** Make the strongest case
   each way, then pick. If overhaul: incremental-refactor-behind-flags vs. a parallel rebuild-and-
   cutover — which, and why, for a system whose outputs are already public?
2. **The reproducibility crisis first.** 8/12 baselines can't be regenerated. Argue whether
   establishing a clean, version-pinned, reproducible baseline for all 12 categories must be
   PHASE 0 (no scoring change is trustworthy until drift is measurable) — or whether that's
   over-caution. What is the minimum bar for a "trustworthy baseline"?
3. **Target architecture.** What should replace the ~40 chains? How much should be pure continuous
   dimensions vs. a small set of retained guards? Name the failure modes a de-chained engine MUST
   still prevent (clean-label-but-poor products winning; engineered low-sugar UPFs winning;
   reformulation gaming) and how a continuous engine prevents them WITHOUT the caps.
4. **How do we KNOW it works?** Define the acceptance bar for the whole program — the invariants /
   gates / evidence that would let the owner trust a system-wide rescore (beyond "the one cookie
   is fixed"). What would you, as a skeptic, demand to see before believing it?
5. **Phased sequence + decision gates.** Give the phase plan (Phase 0…N), each phase's exit
   criterion, where the owner must look, and what could go catastrophically wrong at each step.
6. **The one warning** you'd give this team about big scoring-system rewrites.

Be specific and adversarial toward both "keep patching" and "rewrite it all." Cite your reasoning.
