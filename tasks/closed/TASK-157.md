---
id: TASK-157
title: Standardize category caveat (cheese-style הערת קטגוריה box) across all 8 /hashvaot categories via the shared categoryNote slot
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — held judgement call (Product positioning sign-off on the cheese-vs-maadanim sodium/sat-fat caveat divergence) now resolved: Product verdict ACCEPTABLE WITH MINOR WORDING — keep both caveats, add one shared unifying lead clause to each. Clause APPLIED + independently verified against artifacts: (1) maadanim — src/lib/comparisons/maadanim-page-data.ts:125 ends with '...בדקו את התווית להשלמת התמונה.\\n\\nהציון מודד את מה שהתווית והנתונים מאפשרים בכל קטגוריה בנפרד; בקטגוריה זו ערכים אלה כן נכנסים לחישוב.'; (2) cheese — src/data/comparisons/cheese_frontend_v1.json _meta.disclosures.category_wide_sodium_satfat ends with '...בדקו זאת בתווית.\\n\\nהציון מודד את מה שהתווית והנתונים מאפשרים בכל קטגוריה בנפרד; בקטגוריה זו הנתרן והשומן הרווי אינם נכנסים עדיין לחישוב.'. Shared lead clause ('הציון מודד את מה שהתווית והנתונים מאפשרים בכל קטגוריה בנפרד') byte-identical on both pages; category-specific tail correctly diverges (maadanim: values DO score; cheese: not yet scored). Gates independently re-run: cheese JSON parses valid; npx tsc --noEmit exit 0; node scripts/validate-corpus.mjs 0 errors (260 pre-existing warnings, all yogurt/§2.x — none from these clauses; cheese 0 err, maadanim 0 err). roadmap_impact=true + cc_reviewed=2026-06-02 set, so PreToolUse guard permits close."
roadmap_impact: true
cc_reviewed: 2026-06-02
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "Implementation independently verified against artifacts: the caveat (Hebrew 'הערת קטגוריה') is threaded across all 8 categories — page-data + comparison-page components + routes. Nutrition's maadanim CORRECTION is real and well-grounded: maadanim-page-data.ts:115-122 documents that the cheese sodium/sat-fat 'not scored' framing does NOT carry to maadanim (run_maadanim_001, engine 0.4.1 actively scores both — fat_quality dim varies 17->100, 30 take ISRAELI_RED_LABEL_1_SAT_FAT cap, 24 take HIGH_SODIUM_700MG_PLUS, 12 take the fat-sodium HP penalty). Caveat copy at :125 now truthfully states sugar/sat-fat/sodium LOWER the score. tsc/lint/corpus-validate reported green."
  - date: 2026-06-02
    flag: verify
    text: "HELD at RETURNED — not closed. Open judgement call (NOT a pass/fail check, so it does not close here): Product positioning eyeball on the cheese-vs-maadanim caveat divergence (owner pre-approved 'keep both', but the final positioning sign-off on consumer-facing governed copy is Product's). roadmap_impact=true (consumer-facing governed copy); cc_reviewed set after this verification, so the PreToolUse guard will permit a close once Product signs off."
  - date: 2026-06-02
    flag: fyi
    text: "RESOLVED -> CLOSED. Product Agent signed off: verdict ACCEPTABLE WITH MINOR WORDING — keep both caveats, add one shared unifying lead clause to each so the divergence reads as intentional. Clause applied + verified on both artifacts (maadanim-page-data.ts:125 + cheese_frontend_v1.json _meta.disclosures.category_wide_sodium_satfat). Shared lead clause is byte-identical on both pages; the category-specific tail correctly diverges (maadanim: sodium/sat-fat DO enter the score; cheese: not yet). tsc exit 0, validate-corpus 0 errors. Close-gate PASS."
summary: >
  Added the cheese-style category-caveat box to all 8 categories via the shared categoryNote slot (page-data + components + routes). Build/tsc/lint/corpus-validate green. Nutrition VERIFIED milk + yogurt, and CORRECTED the maadanim caveat (it falsely implied sodium/sat-fat not scored; engine actually penalizes them). Consumer-facing governed copy; Product positioning eyeball on the cheese-vs-maadanim divergence in flight.
---

# TASK-157 — Standardize category caveat (cheese-style הערת קטגוריה box) across all 8 /hashvaot categories via the shared categoryNote slot

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
