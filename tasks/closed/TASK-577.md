---
id: TASK-577
title: Magnesium guide v3 - owner readability restructure (findings box top, products first, 4-line cards + disclosure, owner group headings, delete duplicate prose, -40-50% text)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Owner-dictated v3 restructure shipped through the full loop and LIVE on
  bari.digital/madrichim/magnesium (master 9ba9dcf2 -> 55847d7b, branch deploy/mag-guide-v3,
  final commit 71ecb1cf rebased; live confirmed ~90s post-push, 7/7 live markers pass,
  noindex preserved). Chain verified at each hop: Nutrition D6 v3 structure spec
  (mag_guide_v3_structure_spec.md, final sha256 cc0cc76f...) with 18/18 owner-heading mapping
  6/5/6/1; Product D7 co-sign independently re-derived 18/18 (2 amendments: mandatory #17
  carbonate on-card disambiguation; servings row omitted entirely, never a placeholder);
  Content gate-1 package (mag_guide_v3_copy_package.md, sha256 668fdaee...) with owner text
  verbatim + 18 authored one-liners, self-gates clean; wiring script-extracted byte-exact
  (28/28 scripted checks); orchestrator personal read caught 3 defects the scripts missed
  (wrong H1, "מחיר לא זמין" x18 data-state narration, disclaimer rendered twice) - fixed;
  gate-2 Adversarial QA verdict GO conditional (0 CRITICAL; RT-2 form-name/absorption-rating
  conflation on #9/#18 fixed from spec §B pre-deploy; RT-1 HIGH = owner-heading vs member-row
  tension -> owner digest, gates only the index flip which was already owner-gated).
depends_on: []
blocks: []
category_id: null
summary: >
  Owner 2026-07-10 ("You overcorrected... The page is not readable now"): full v3 restructure of /madrichim/magnesium per dictated page order and copy. Facts unchanged from v2 spec; presentation + grouping rebuilt.
---

# TASK-577 — Magnesium guide v3 — owner readability restructure

## Delivered (LIVE on bari.digital/madrichim/magnesium, noindex, master @ 55847d7b)
1. **Owner page order end-to-end**: H1 "איך לבחור תוסף מגנזיום" + one-sentence intro → compact
   "מה גילינו" box (4 owner bullets) → products IMMEDIATELY (no methodology first, no prose
   product summaries) → "איך לקרוא תווית מגנזיום" (3 owner bullets) → single collapsed
   "לפרטים ומקורות" accordion.
2. **Four owner-dictated group headings**, membership per D6+D7-signed deterministic
   first-match-wins rule: ציטראט או ביסגליצינט עם תווית ברורה (6) · כמות נמוכה יחסית (5) ·
   מבוססי אוקסיד (6) · לא ניתן להבין מהתווית (1).
3. **4-line cards**: elemental mg, chemical form, "מה חשוב לדעת:" signed one-liner (servings/day
   omitted — data gap, see follow-ups); everything else (gauges, badges, evidence_limited state)
   under collapsed לפרטים. Per-card price placeholder removed (omit-when-null; the market-gaps
   box is the single sanctioned price/third-party statement).
4. **Owner deletions executed**: "אף מוצר…" prose block + per-product summaries, repeated
   forms explainer, duplicate dose-safety/price/third-party occurrences, duplicate disclaimer.
   Survival list intact inside collapsed content: UL-350 (IOM) + EFSA-250 framing ("זו לא רעילות"),
   evidence_limited meaning, RDA 310-420 "מכל המקורות יחד", corpus 76-520/median-190 gauge,
   Cochrane cramps scoping, 3 clickable primary sources.
5. **v2 path preserved** behind `useV3Layout` flag for rollback; v2 data/components untouched.

## Artifacts
- `02_products/supplements/magnesium/mag_guide_v3_structure_spec.md` (D6+D7, final sha256 cc0cc76fc147955b802befbad64ab3a479d152a76d1915d38dfcfb3ea5ab6a84)
- `02_products/supplements/magnesium/mag_guide_v3_copy_package.md` (gate-1, sha256 668fdaee57449e8514c12d2fded3ed653a391a7cc0f5a49fd7919b622160f2dd)
- Code on master @ 55847d7b (commits f08f71e5 structure, 303f509c wire, ac9cc77e fix, 71ecb1cf RT-2 fix).

## Open follow-ups (registered here; none block)
- **RT-1 HIGH → OWNER (gates index flip, not this noindex deploy):** owner heading
  "כמות נמוכה יחסית" contains #5 (hydroxide, 190 mg = corpus median, higher than two heading-1
  members) whose own one-liner honestly says "בדיוק בחציון הקטגוריה" — heading text vs member
  row tension. Recommended fix: owner amends heading 2 to a form/label-based label (the group's
  real classifier), e.g. "צורות אחרות עם תווית ברורה"; alternatively accept as-is knowingly.
- **Owner-text fact flags (informational, owner's own words shipped verbatim):**
  (a) intro "מהמדף הישראלי" — v2 spec §8 killed shelf-universal phrasing; scoped-claims rule
  says "בקרב 18 המוצרים שנבדקו". (b) findings bullet "מוצרים רבים מבוססים על אוקסיד" — precise
  count is 6/18 (7/18 counting carbonate).
- **Servings-per-day data gap:** NULL for all 18 (never parsed from labels). Card line renders
  only when data exists. Follow-up: Data Agent label-text re-parse to populate; then the owner's
  dictated third card line appears automatically.
- **RT-3 MEDIUM (monitor):** v2 market-structure headline finding (no product combines top-half
  dose + citrate + clean safety/label) dropped entirely per owner cut; not on §D must-survive
  list; revisit only if owner asks where it went.
- **DEVIATION log (D6 flagged, D7 adjudicated, all shipped):** heading-2 form-agnostic reading;
  #9 blend in heading 2 with ratio-gap disclosed on card; #17 carbonate under "מבוססי אוקסיד"
  via chemical-class analogy with MANDATORY on-card disambiguation (rendered); #16 in heading 3
  on known-problem-before-data-gap precedence.
- **Index-flip checklist unchanged from TASK-575:** owner robots approval + human-browser check
  of the NIH ODS URL + RT-1 acknowledgment.
