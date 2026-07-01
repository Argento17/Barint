---
id: TASK-365
title: Protein bars rework: combined shelf + protein_bar lens (de-weight protein, add sugar-mechanism/engineering/glycerol/source axes), corpus rebuild, display+copy fixes
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-21
closed_at: 2026-06-22
reclosed_r3_at: 2026-06-22
reclose_r3_reason: >
  Owner round-3 (4 items) resolved + LIVE on bari.digital/hashvaot/protein-bars
  (master 93f45165e, propagated — maltitol note present, stale rank gone, granola
  gone). Orchestrated via lanes per owner ("route to C1/C2/C3"): C2 = mechanical
  JSON (remove granola->32, re-rank, counts, strip "— C/D" grade tag from 29
  verdicts) [verified vs artifact]; C1-Frontend = expansion protein/sugar fill bars
  empty -> root cause var(--bari-green) undefined in imported CSS -> #1F8F6A
  [render-verified]; C1-content -> Red-Team gate = maltitol explainer (polyol,
  ~2kcal/g, GI~35 vs 65, carb-line-not-sugar-line, EU 10g, bridges to 69/B ceiling)
  + granola-removal fallout (ceiling 70->69/B, prologue reframe, pb-002 stale
  "second->first" verdict) [gate#1 BLOCK 2C/2H incl. "סוכר אמיתי" regression caught
  by orchestrator -> revised -> gate#2 PASS 0C/0H]; Nutrition = all 20 additive
  tiers DEFENSIBLE, none mis-tagged (no copy change; no evidence task needed).
  Build exit 0; 14/14 render checks PASS. Deploy owner-approved ("push").
  FOLLOW-UPS (non-blocking, logged): (1) 8 SKUs (pb-017–022,027,028) show truncated
  ingredient lists hiding maltitol though "24/32" is full-label-true -> Data
  display-completeness fix; (2) var(--bari-green) still used at expansion-section.tsx
  ~L45/L906 (likely same latent transparency bug) -> verify/fix; (3) RT-M-NEW-1
  maltitol GI cited at lower bound ~35 (range 35–52) -> Nutrition EV-citation check.
reopen_r3_reason: >
  Owner round-3 re-critique of live page (4 items): (1) explain what maltitol IS /
  why "sugar replaced by maltitol" is not a free pass (needs a consumer explainer);
  (2) review the additive set — owner asked to spawn Nutrition Agent (inventory has
  contested E330/E300/E202/E471/E224, disclosure-gap E150 ×18, unclassified E141);
  (3) STOP ending product descriptions with "— C"/"— D" grade tag (29/33 rowVerdicts
  do; grade already shown in badge — redundant); (4) remove תלמה גרנולה פרוטאין
  (pb-001, rank-1 70/B) — it's a granola/cereal, drifted onto the protein-bars
  shelf; move to cereals/granola. Removal drops ceiling to פנגיאה 68.6→69/B.
reclosed_at: 2026-06-22
reclose_reason: >
  Owner re-critique (4 defects) resolved + LIVE on bari.digital/hashvaot/protein-bars
  (master 4c5a3d896, propagated — new copy present, "WIN WIN" doubling gone).
  (1) BRANDS IN TITLES: row now renders displayTitle (was name_he/brandless);
  rebuilt 33 displayTitles via canonical brand map — de-doubled "חטיף חלב WIN WIN…"
  -> "WIN …", "נייטשר וואלי נייטשר…" -> "נייטשר וואלי …"; generic "פרוטאין"
  (no real brand) keeps its name, no fabricated prefix. (2) PROTEIN: verified
  genuinely per-100g (nutrition_basis=per_100g, conversion_factor=1.0, scraped) so
  34g is real (~17g per ~50g bar); render-verified non-zero for all 33 in prod
  build — the "shows 0" report was stale CDN cache pre-rebuild. Per-bar display NOT
  added (scrape has no pack weights; per-100g is the correct cross-size basis, kept
  + labeled). (3)+(4) WEAK D-TIER + POOR-HEBREW shelf-context: pb-031/032/033
  insightLine/rowVerdict/comparisonContext rewritten via content lane, PASSED
  Adversarial QA Red-Team gate (gate#1 BLOCK 2 HIGH+4 MED -> revised -> gate#2 PASS
  0 CRITICAL/0 HIGH). Removed owner-rejected "סוכר אמיתי"; pistachio/kataifi claim
  VERIFIED against direct product scrape (מחית פיסטוק 16%, שערות קדאיף 8%).
  Residual MED (non-blocking, documented): F-1 pb-032 insightLine "מקום הנכון"
  slightly indirect (gate PASS; line still leads with clear verdict).
reopen_reason: >
  Owner post-ship re-critique of the LIVE page (4 defects): (1) brand still
  missing from row titles (renders name_he, not displayTitle; All-in cookie eg) —
  also displayTitle data malformed (WIN/נייטשר doubling); (2) protein "shows 0"
  report + per-100g basis question — VERIFIED data is genuinely per_100g
  (conversion_factor=1.0, scraped) so 34g is real; render-bug + per-bar framing
  to chase (scrape has NO pack weights); (3) weak D-tier descriptions (#31 step
  back); (4) poor-Hebrew shelf-context line ("דוגמה לכך ש…") — owner wants the
  clearer "you get protein, but it's a candy bar with protein, just know that"
  reframe. Copy fixes route through content lane + Red-Team gate (HARD RULE).
reopen_reason: >
  Owner post-ship re-critique of the LIVE page (4 defects): (1) brand still
  missing from row titles (renders name_he, not displayTitle; All-in cookie eg) —
  also displayTitle data malformed (WIN/נייטשר doubling); (2) protein "shows 0"
  report + per-100g basis question — VERIFIED data is genuinely per_100g
  (conversion_factor=1.0, scraped) so 34g is real; render-bug + per-bar framing
  to chase (scrape has NO pack weights); (3) weak D-tier descriptions (#31 step
  back); (4) poor-Hebrew shelf-context line ("דוגמה לכך ש…") — owner wants the
  clearer "you get protein, but it's a candy bar with protein, just know that"
  reframe. Copy fixes route through content lane + Red-Team gate (HARD RULE).
depends_on: []
blocks: []
category_id: null
close_reason: >
  Shipped + LIVE on bari.digital/hashvaot/protein-bars (master 9918bd256, Vercel
  rebuild verified — new cluster-note text present). Combined 33-product shelf
  (16->33; bars+cookies; bites absent on Shufersal). New protein_bar lens
  (Nutrition D6 + Product D7 co-signed; flag BARI_PROTEIN_BAR_V1, flag-OFF proven
  byte-identical). Both content gates passed: Red-Team gate #2 PASS (0 CRITICAL,
  0 HIGH; 8/8 gate-#1 HIGHs resolved). Final shelf B=2/C=28/D=3, ceiling 70/B
  whole-food, no A, 45/D candy-with-protein. Orchestrator-verified each subagent
  claim against artifacts (caught 3 inaccurate self-reports: false A-grades from
  truncated scrapes, wrong tie-rank narrative, rowVerdict-not-rendering). Deploy
  was divergence-safe (dropped unrelated uncommitted bandNote; reconciled
  row-surface.ts + fields.ts against master). FAST-FOLLOWS (not blocking, logged):
  (1) per-bar protein display — scrape lacked pack weights, deferred not fabricated;
  (2) C-MEDIUM-1 trace transparency — log PROCESSING_FAMILY_BUDGET cap fields
  (scores correct, internal-audit only); (3) commit TASK-365 engine infra durably
  (constants.py/router_v2.py/score_engine.py/spec live in task-362 working tree;
  JSON output already durable on master).
summary: >
  Owner-approved 2026-06-21 off protein-bars page critique. Combined protein shelf (bars+cookies+bites, fold-in per owner). New protein_bar sub-lens per Nutrition D6: protein->~0 weight, axes=sugar-reduction mechanism (real-food vs polyol vs sweetener; maltitol>erythritol), engineering depth (NEW glycerol signal + isolate stacking + ingredient count), protein source (whole-food vs isolate, matrix-integrity not DIAAS). Corpus: brand-led+expanded scrape (WIN/all in/Max Protein/PRO20 variants), lift 'עוגיות' HARD_EXCLUDE. Display: fix slider scaleMax clip (protein/sugar 20->shelf range) + per-bar protein disclosure. Copy: re-author via Content+Red-Team (kill 'סוכר אמיתי'/'מייקר'/recitation; brand-in-title rule). Re-ranked shelf shown to owner BEFORE go-live (tripwire #1).
---

# TASK-365 — Protein bars rework: combined shelf + protein_bar lens (de-weight protein, add sugar-mechanism/engineering/glycerol/source axes), corpus rebuild, display+copy fixes

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
