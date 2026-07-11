# Adversarial QA / Red-Team v2 — Magnesium Guide 4-Tier Copy (TASK-504, gate-2 re-check)

**Date:** 2026-07-04 · **Verdict: NO-GO** (single blocker) · Instrument: live `hebrew_readability.analyze().is_clean`
**Persisted by:** Orchestrator (QA harness returns in-message).

## Re-check result
- **מומלץ caption** — PASS (scoped to displayed bars, no "meets all bars", names dose shortfall; is_clean True). RT-1 resolved.
- **טוב caption** — PASS (scoped to displayed bars, includes dose caveat + product-side caveat; is_clean True). RT-1/RT-2 resolved.
- **body[2]** — **FAIL (RT-8)**: antithesis fixed, but the rewrite uses the literal "מומלץ" in prose ("…תחת הכותרת מומלץ…") → HARD recommendation-leak, is_clean False. EXCEPTION-003 covers the 4 labels ONLY as tier-label field values, NOT prose.

## RT-4 — CONFIRMED CLOSED
EXCEPTION-003 Approved, dual-keyed (Product + Nutrition); scope = 4 exact labels as tier-label field values, not prose; legitimately sanctions the vocabulary. The 4 labels are defensible-to-ship as tier headings.

## Blocker
- **RT-8 (blocks):** body[2] recommendation-leak in prose. Fix = Content rewrites body[2] to reference the tiers positionally/descriptively (no literal tier-label word in prose). Scope-preserving alternative to widening EXCEPTION-003 into prose.

## Non-blocking monitors
- **RT-5:** EXCEPTION-003's gate carve-out is UNWIRED in `hebrew_readability.py` (raw gate still fails the standalone label). Governance-approved, but mechanical CI enforcement pending → pre-public-flip code task (frontend/gate owner). Does NOT block local review / governance GO.
- **RT-6:** the PROPOSED (unapplied) body[8] companion carries the same "מומלץ"-in-prose leak — fix in the same pass before it's applied.
- **RT-7:** the מומלץ "only reservation is dose" framing is honest only if `suppressedBarsDisclosureHe` renders in the same view → Frontend must guarantee disclosure adjacency. (Also notes Product D7 co-sign on the amended predicate — that co-sign IS on record from Product; Nutrition hadn't seen it.)

## Disposition
Content rewrites body[2] + the proposed body[8] to drop literal tier-label words from prose (full is_clean must pass, not just the narrow antithesis scan). Orchestrator re-verifies is_clean mechanically. RT-5 tracked as pre-flip code task; RT-7 disclosure-adjacency folded into the Frontend build spec.
