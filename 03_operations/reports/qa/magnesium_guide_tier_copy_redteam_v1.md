# Adversarial QA / Red-Team — Magnesium Guide 4-Tier Copy (TASK-504, gate 2)

**Date:** 2026-07-04 · **Scope:** 9 tier-copy strings (+2 companions) · **Verdict: NO-GO (conditional)**
**Persisted by:** Orchestrator (QA harness returns findings in-message; this is the durable gate record).
Ground-truth rubric hash `d8ae4089…` matches Nutrition's co-signed version.

## Result: 6/9 GO, 3/9 re-author. 0 CRITICAL · 4 HIGH · 3 MEDIUM.

**GO (6):** מומלץ מאוד caption · לא מומלץ caption · empty-state line · cannot_assess line (RT-5 monitor) · expander show · expander hide.
**NO-GO — re-author (3):** מומלץ caption · טוב caption · body[2] rewrite.
**Companions:** body[0] GO; body[8] carries RT-4 only.

## HIGH findings
- **RT-1 (over-claim / self-contradiction).** מומלץ ("בכל הספים חוץ מאחד") + טוב ("עומדים בכל הספים") claim a standing the bars don't support: a מומלץ product is dose=FLAG + third_party/price=CANNOT-VERIFY (3 of 6 non-PASS); טוב adds a form/safety FLAG (4 of 6). Contradicts headlineFinding.body[8] ("two suppressed bars are why none reaches מומלץ מאוד"). Fix: re-scope captions to the DISPLAYED/checkable bars; never assert "meet all bars." → content-agent.
- **RT-2 (understatement).** טוב caption omits the dose caveat every current טוב product carries (body[2] says otherwise → same package disagrees). → content-agent.
- **RT-3 (HARD-gate antithesis).** body[2] fails hebrew_readability at "…, לא רק לכמות". Likely a gate over-match (inclusive "לא רק"), but a HARD-failing string ships only after trivial re-author or a logged exception. → content-agent.
- **RT-4 (systemic governance conflict).** Owner-mandated tier vocabulary (מומלץ מאוד/מומלץ/טוב/לא מומלץ) fires the standing recommendation-language HARD-leak gate. Needs an Exception-Registry entry sanctioning the guides tier vocabulary (owner override) + a gate scope carve-out, else mechanical copy CI red-flags most tier copy. → product-agent + nutrition-agent (governance) + gate/copy_rules owner (wiring).

## MEDIUM
- **RT-5.** cannot_assess caption bakes a blend-specific cause (fine for TRIOMAG; a future non-blend cannot_assess product would be misdescribed). Monitor.
- **RT-6.** Retired "הרשימה המעשית" persists at `magnesium-guide-data.ts:478` (`promotedShortlistLabel`), obsoleted by the 4-tier model. → frontend/content on integration.
- **RT-7.** מומלץ "take more" advice has no safety-ceiling reminder (safe for actual members; generic phrasing). Low priority.

## Dose-honesty trap: NOT triggered
The מומלץ caption states the dose is below threshold and to top it up; actual members (Altman Citrate 120 = 200mg, Nutricare WELL = 168mg) reach 300mg well under the 350mg UL. C3 (P508) independently affirmed with the same "keep the under-dose caveat visible" guardrail.

## Disposition (orchestrator)
- RT-1/RT-2/RT-3 → Content re-authors the 3 strings; QA re-gates.
- RT-4 → Product+Nutrition author an Exception-Registry entry (owner-directed tier vocabulary) + gate carve-out spec.
- RT-6 → Frontend drops `promotedShortlistLabel` in the tier-model integration.
