---
id: TASK-575
title: Magnesium guide v2 - owner review fixes (assessed-criteria vs market-gaps split, descriptive groups replace tier ladder, drop 300mg universal threshold, remove multi-capsule advice, 3-bucket absorption evidence, narrow Cochrane cramps claim, clickable primary sources, scope phrasing to 18 reviewed products, fix bisglycinate-600 copy error)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  All 6 owner fixes + smaller items shipped through the full two-gate pipeline and
  deployed to origin/master (380f1020 -> 84e15e2e, commits 71b94296 + 12cd0850 + 84e15e2e
  on deploy/mag-guide-v2). Evidence verified by orchestrator at each hop: nutrition
  evidence spec (mag_guide_v2_nutrition_spec.md, final sha256 f1730513...) with 18/18
  group mapping mechanically re-derived by Product D7; gate-1 copy package
  (mag_guide_v2_copy_package.md, final sha256 cf157080...) 61/61 strings clean on the
  hard gates; gate-2 Adversarial QA first pass NO-GO (CRITICAL meta + HIGH bisglycinate
  badge) -> fixes ruled (Nutrition D6 spec-11 evidence_limited state + regroup 0/9/8/1,
  Product D7 co-sign with independent re-derivation) -> targeted re-verify GO (0 CRITICAL,
  0 HIGH, 4/4 fixes verified on rendered DOM). Final group(b) caption precision fix
  (SLOT 11.2-rev) wired verbatim and render-verified before push. Live marker string
  confirmed on bari.digital/madrichim/magnesium post-deploy. Page remains noindex.
depends_on: []
blocks: []
category_id: null
summary: >
  Owner 2026-07-10 full review of /madrichim/magnesium. Six fixes + smaller items. Two-gate + Nutrition evidence spec required. Deploy to origin/master after gate-2.
---

# TASK-575 — Magnesium guide v2 — owner review fixes

## Delivered (live on bari.digital/madrichim/magnesium, noindex)
1. **Assessed-criteria vs market-gaps split** — 4 assessed criteria (dose, form, safety, label);
   price + third-party testing render ONCE as a guide-level market-information-gaps box, removed
   from every product's bar set; empty group (a) reframed as the discovered market-structure
   finding (all 450-520mg products are oxide; recommended forms top out at 250mg).
2. **Ladder removed** — 4 descriptive groups replace מומלץ מאוד/מומלץ/טוב/לא מומלץ + A-D letters.
   Final distribution a:0 / b:9 / c:8 / d:1 (post spec-§11 regroup; #5/#7/#8/#10 moved c→b).
3. **300mg universal threshold dead** — neutral corpus-range gauge (76-520, median 190 — a real
   arithmetic error in the spec caught by Product D7 and fixed pre-authoring), RDA 310-420
   labeled "מכל המקורות יחד", UL 350 safety context only. The old 300mg figure traced to a
   BP-specific trial (Zhang 2016), not a general threshold.
4. **Multi-capsule advice deleted**; labelled-serving-only language everywhere.
5. **Absorption = 3 evidence buckets**; NEW `evidence_limited` bar state (off-ladder, label
   "ראיות מוגבלות לדירוג") for all 8 bucket-3-form rows — bisglycinate no longer renders
   top-tier while prose says evidence is limited; oxide-cheap causal claim removed.
6. **Cramps narrowed** to older adults/idiopathic (Cochrane PMID 32956536); pregnancy conflicting.
7. Clickable primary sources (NIH ODS, Cochrane/PubMed, EFSA); certification phrased as a
   search result among the 18 reviewed as of 2026-07; "המדף הישראלי" universal phrasing purged;
   ביסגליצינט 600 clarified as capsule count.

## Artifacts
- `02_products/supplements/magnesium/mag_guide_v2_nutrition_spec.md` (final sha256 f17305132482d2e7b68fb988d6b682c5275dd62badafd7f6b6e80819353a29fc)
- `02_products/supplements/magnesium/mag_guide_v2_copy_package.md` (final sha256 cf15708060c284f88eb53b2c0387d098f5bb2846f08f6a67dcebad482291ffef)
- Code: bari-web guide VM/components/data on master @ 84e15e2e.

## Open follow-ups (registered here, none block)
- **MEDIUM (design monitor):** evidence_limited off-ladder marker sits mid-track (50%),
  geometrically near the בינונית label — disambiguated by shape/icon/label; Design Agent to monitor.
- **Index-flip checklist:** confirm NIH ODS URL human-browser reachability (403 to bots);
  owner robots approval still required (page is noindex).
- **Follow-on D7 (non-blocking, opened by Product):** whether a sub-label mechanism belongs in
  the GuideBucket schema rather than prose alone, if future regroupings recreate mixed captions.
- Hub-card classifier pass for the 5 original group-(b) rows (Content flagged, deliberately out of scope).
