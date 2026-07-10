---
id: TASK-486
title: Crackers page parity — remove extra description layer (golden-standard parity) + backfill missing brands (17/19) from scrape
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #67 (merged, origin/master 32198372 ancestor-verified). Crackers deep-dive layer removed → golden parity (live-verified: 0/19 consumerTakeaway). Barcode-keyed 0 protected-field change; Adversarial QA render gate GO. Brand 17/19 = honest source-empty (scrape brand field empty for all 19; only 2 אסם tokens), no OFF/fabrication — confirmed by TASK-489 audit."
depends_on: []
blocks: []
category_id: crackers
summary: >
  Owner-flagged (2026-07-03): the crackers comparison page shows a long product description no other
  comparison has, and it is "too much / not in par with the golden standard." Confirmed: crackers is the
  ONLY comparison JSON with consumerTakeaway (19/19) AND expansion.consumerExplanation (19/19) populated;
  the golden brined-cheeses page has ZERO of both. Also 17/19 crackers products have brand=None (golden =
  36/36). FIX: (1) bring crackers structure to golden parity — stop rendering / remove the extra
  description layer; (2) backfill brand from the crackers BSIP0 scrape only (OFF BANNED; if brand not in
  the scrape → leave null, do NOT fabricate, per missing_data_discard_rule).
---

# TASK-486 — Crackers parity + brand backfill (owner-flagged 2026-07-03)

## Owner instruction (verbatim intent)
"for crackers I see the long product description which is not something we have in other comparisons.. and
if we do that's a bit too much and not in par with our golden standard, also check why there are no brand
names in most products in crackers."

## Verified facts (orchestrator scouted origin/live JSON)
- `bari-web/src/data/comparisons/crackers_frontend_v1.json`, 19 products, LIVE (shipped PR #58).
- `consumerTakeaway` populated 19/19 (avg 188 chars, max 265). NO other live page uses it except cookies
  (61/117 partial). Golden brined-cheeses = 0.
- `expansion.consumerExplanation` populated 19/19 (avg 600 chars). Only granola (7/22) else. Golden = 0.
- `brand` present only 2/19 (both אסם / barcodes 74252, 74375). Golden brined-cheeses = 36/36.

## Deliverable (Frontend owns; INVESTIGATE → RECOMMEND → APPLY; do NOT close — propose RETURNED)
1. **Render parity.** Open the crackers comparison page component AND the golden brined-cheeses page
   component. Determine EXACTLY which field(s) render as the long description the owner sees
   (`consumerTakeaway`? `expansion.consumerExplanation`? both?). Confirm the golden page does not render
   them. Recommend the parity fix (remove the extra layer vs trim) with the rendered evidence, and apply
   it so crackers matches the golden structure. rowVerdict + insightLine + expansion positiveSignals/
   limitingFactors already carry the verdict — the extra description layer is the redundancy to resolve.
   Any consumer copy that STAYS goes through the content two-gate; wholesale REMOVAL of a redundant field
   is structural (still consumer-facing → owner PR) and does not need re-authoring, but Adversarial QA
   must confirm nothing else on the page depended on it.
2. **Brand backfill.** For the 17 brand=None crackers, source `brand` from the crackers BSIP0 scrape /
   corpus ONLY (product name, retailer product page, manufacturer field in the scrape). **OFF is BANNED —
   any field, any fallback.** If the brand is genuinely not in the scrape for a product → leave it null;
   do NOT fabricate or infer, do NOT over-invest re-sourcing (missing_data_discard_rule). Report how many
   you could fill and how many stay null with the reason.
3. Isolation: touch only `crackers_frontend_v1.json` (+ the page component if a render change is needed).
   Zero score/grade/rank change. tsc + build must pass.

## Guards
- OFF ban absolute. Consumer-facing → owner merges the PR (tripwire-2); you build + return, never merge.
- No score/grade/rank/scoring change (that would be tripwire-1).
- Preserve rowVerdict/insightLine/positiveSignals/limitingFactors byte-for-byte unless the parity fix
  explicitly removes a field; report any copy delta for the two-gate.

## Return: 5-part + machine-readable Return Contract (01_framework/operations/return_contract_v1.md).
Propose RETURNED. Do not write CLOSED.

## RETURNED (Frontend, branch fix/task486-crackers-parity) + orchestrator-VERIFIED
- **Render parity APPLIED = wholesale removal** of 4 crackers-only fields (consumerTakeaway, bestUseCases, bariInterpretation top-level, expansion.consumerExplanation) that fed the DeepDiveSection block (gated by hasDeepDiveContent, deep-dive-section.tsx:251-262). NOT editorial — pure subtraction; golden brined-cheeses + 12 live pages already render 0/N on all 4 via the same graceful-null path → crackers now matches golden structure exactly.
- **Orchestrator cross-page audit CONFIRMS agent did not over-remove:** all 4 fields are 0 on golden + 12+ pages; only crackers had all four (cookies has 3 of them partial, granola has expl partial → their parity queued TASK-488). Removing all 4 from crackers is correct parity, not a new inconsistency.
- **Barcode-keyed verify (origin/master vs branch):** 1 file changed; 19/19 barcodes preserved; **0 protected-field mismatches** (score/grade/rank/categoryTotal/rowVerdict/insightLine/brand/name/nameHe/confidence + expansion comparisonContext/positiveSignals/limitingFactors/nutrition/ingredients all byte-identical); 4 target fields fully removed (0 residual). tsc/lint/build 0, /hashvaot/crackers in route manifest.
- **Brand backfill = 0/17, HONEST unknown (not a bug):** agent traced source — raw Shufersal scrape `brand` field is `""` for all 19 crackers records at BSIP0→BSIP1→frontend; nothing dropped. Only 2 (74252/74375=אסם) carry a recognizable brand token. Per missing_data_discard_rule: leave null, no OFF, no fabrication. Stray legacy "KRIT" on a bread page for 8434165658523 correctly still excluded.
- **Adversarial QA render gate = GO** (a0f94ba3): 0 CRITICAL / 0 HIGH. Independently drove real Chromium (Playwright) on /hashvaot/crackers + golden brined-cheeses, mobile+desktop: deep-dive block absent (0 markers across 3 rows × 4 combos), structure matches golden, 0 console errors, 0 h-scroll, 0 null/undefined DOM leak on 17/19 null-brand rows, re-diffed protected fields 0-mismatch itself, tsc/lint/build 0. 1 MEDIUM = pre-existing .font-mono contrast IDENTICAL on golden → not a regression, routes Design.
- **🚀 PR #67 OPENED** https://github.com/Argento17/Barint/pull/67 (consumer-facing removal = owner merge, tripwire-2). Two-gate satisfied (no new copy → content-author N/A; Adversarial QA GO). CLOSE on merge; prune C:\bari_wt_t486 + t486qa.
