# Adversarial QA / Red-Team — Creatine Guide Tier Copy (TASK-504 Wave 2, gate 2)

**Date:** 2026-07-04 · **Verdict: GO** (11/11 shipped strings) · Instrument: live `hebrew_readability.analyze().is_clean` (independently re-run)
**Persisted by:** Orchestrator (QA harness returns in-message).

## Result: GO — 0 CRITICAL, 1 HIGH (non-shipping rationale), 3 MEDIUM, 1 LOW.

- **is_clean:** 11/11 True (independent run). EXCEPTION-003 compliance mechanically proven (0 recommendation-kind leaks → no tier word in any prose string). Only leaks = 4 advisory `english` tokens (NSF/Certified/for/Sport) on headline_body0, which never affect is_clean.
- **Data accuracy (re-derived from `origin/master:creatine-page-data.ts@9546878`):** Israeli directory-verified 0/18, worldwide 7/13 — CONFIRMED exact. Tier counts 3/1/19/7/1 = 31 — CONFIRMED. No טוב product carries a form caveat (HCl form-FLAG only on the 2 dose-FAIL products) — tier_good caption correct.
- **NSF-gap headline — challenged hardest, HONEST:** scopes third-party as 1 of 6 bars, disclaims it's a quality finding, gives a constructive path, never says "buy imported." Not misrepresentation.
- **CGN cannot-assess line:** correctly reflects price = CANNOT-VERIFY (Nutrition's correction), no price number, no negative verdict.

## Findings
- **RT-1 (HIGH, non-shipping):** Content's tier_good provenance tally is 11+7+3=21 for a 19-row tier; correct split (re-derived) = third-party-alone 7 / third-party+price 8 / price-alone 3 / dose+tp+price 1 = 19. The "11" is the Israeli-טוב subtotal mis-imported. **Shipped caption is count-free and substantively correct — no consumer string affected.** Per gate law a HIGH requires acknowledgment + rationale correction so a future builder doesn't inherit the bad tally. → content-agent (fix the rationale note only).
- **RT-2 (MEDIUM):** cannot_assess_intro hard-codes "למעלה" (assumes it renders below the 4 tiers) → Frontend must place the cannot-assess section after the four tiers (as magnesium does).
- **RT-3 (MEDIUM):** headline_body0 ~24.5 words/sentence (advisory readability). Optional tightening.
- **RT-4 (MEDIUM):** tier_recommended plural voice on an N=1 tier (defensible house style) + "take more" dose arithmetic (clears no-health-claim; awareness).
- **RT-5 (LOW):** hero_alt describes a TBD asset → re-verify against the final image at asset delivery.

## Disposition
Copy GO for the build. RT-1 → Content corrects the rationale tally (non-blocking, acknowledged here). RT-2/RT-5 → build constraints for Frontend/C1 lane. RT-3/RT-4 → optional/awareness. Go-live still requires the built page to pass render + geometry gates (creatine-guide-data.ts not yet built).
