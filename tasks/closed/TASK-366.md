---
id: TASK-366
title: Fix E476 (PGPR) consumer copy clause + Wave-6 two-gate sign-off
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-21
closed_at: 2026-06-21
depends_on: []
blocks: [TASK-370]
category_id: null
close_reason: >
  E476 (PGPR) consumer copy fixed and unified repo-wide, double-gated (Content Agent +
  Adversarial QA/Red-Team), zero CRITICAL/HIGH within scope. Verified against artifacts by
  the independent gate via grep: the false tail "אינו מוכר בשאר שימושי המזון" is gone from all
  live explanation_he (0 hits); the separate false claim "EFSA ו-JECFA מסווגים כ'לא מוגדר'"
  (cookies_coffee + cakes_hard_cookies) is gone (0 hits); the new canonical E476 line
  "PGPR הוא חומר תחליב סינתטי להפחתת צמיגות בשוקולד; מאושר ברמות הנוכחיות, מותר גם ברטבים מתחלבים ותחליבי שומן."
  (108 chars, Reg (EC) 1333/2008 Cat 12.6+02.2.2, DEC-006 clean) is byte-identical across 19
  live occurrences in 5 comparison files + the w2 content record. Folded-in no-corners cleanups
  that ALSO passed the gate: cakes_hard_cookies E322 aligned to canonical (0 legacy / 31 canonical),
  sorbitol(E420) "נחשב בטוח לחלוטין" overclaim removed repo-wide (0 hits) and replaced with a
  dose-qualified, source-cited line; new E420 record added to w2_additive_copy_v1.md. All edited
  JSONs parse. Residual cookies_coffee legacy E322 debris (45 soya-only + 5 sunflower-only) and the
  E422-glycerol GI-claim are pre-existing carryovers on a legacy page, NOT in this task's scope →
  routed to TASK-370 (launch blocker for cookies_coffee only; does not affect the bars/chocolate pages).
summary: >
  E476 explanation_he ends with the factually-wrong clause 'אינו מוכר בשאר שימושי המזון' (PGPR IS used in low-fat spreads/dressings). Re-author the clause (Content gate), propagate the corrected explanation_he to all occurrences across w2_additive_copy_v1.md + chocolate_tablets/chocolate_bars/protein_bars frontend JSONs, then pass Adversarial QA/Red-Team. Wave-6 additives (E476/E322/E414) currently lack the two-gate sign-off the content hard rule requires.
---

# TASK-366 — Fix E476 (PGPR) consumer copy clause + Wave-6 two-gate sign-off

## Origin
Owner spotted that the rendered E476 (PGPR) additive line ended with the factually-wrong clause
"אינו מוכר בשאר שימושי המזון" ("not known in other food uses") — PGPR is in fact permitted outside
chocolate (emulsified sauces / fat emulsions). Wave-6 additives had reached the page without the
two-gate sign-off the content hard rule requires.

## Delivered (double-gated: Content Agent + Adversarial QA/Red-Team)
- **E476 line re-authored & unified** across all 5 comparison files (chocolate_tablets, chocolate_bars,
  protein_bars, cookies_coffee, cakes_hard_cookies) + the w2 content record — 19 live occurrences,
  byte-identical, 108 chars, regulation-cited, DEC-006 clean.
- **RT-H1:** removed the separate false regulatory claim "EFSA ו-JECFA מסווגים כ'לא מוגדר'" (E476 has
  ADIs 25 / 7.5 mg/kg) from cookies_coffee (6) + cakes_hard_cookies (3).
- **RT-M1:** tightened "ממרחים דלי-שומן" → "רטבים מתחלבים ותחליבי שומן" (precise Annex II categories).
- **RT2-H1:** cakes_hard_cookies E322 (3 legacy variants, 31 occurrences) aligned to Wave-6 canonical.
- **RT2-M2:** sorbitol(E420) "נחשב בטוח לחלוטין" overclaim removed repo-wide; dose-qualified line added;
  new E420 record added to w2_additive_copy_v1.md.

## Out of scope → TASK-370
cookies_coffee legacy E322 debris (45 soya-only + 5 sunflower-only variants) and the E422-glycerol
GI-claim accuracy (RT3-H1, RT3-M2). Launch blocker for the cookies_coffee page only.

## Gate trail
- Content gate: Nutrition Agent APPROVED (3 rounds).
- Red-Team gate: Adversarial QA Agent — final verdict PASS for in-scope deltas, zero CRITICAL, zero
  in-scope HIGH. Open HIGH (RT3-H1) is a pre-existing cookies_coffee carryover → TASK-370.
