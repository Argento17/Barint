# Bari Exception Registry — v1

**Status:** Active  
**Date:** 2026-05-28  
**Scope:** All deliberate deviations from frozen architecture rules across all Bari categories  
**Authority:** Any addition to this registry requires explicit approval. Undocumented exceptions are architecture violations.

---

## Purpose

The Bari comparison template architecture is frozen. Exceptions are not improvements — they are acknowledged risks that have been evaluated and approved on specific grounds. This registry documents every exception, its justification, and the constraints that prevent it from becoming a template for further drift.

A registered exception is not an invitation to repeat. It is a named deviation with defined boundaries.

---

## How to Use This Registry

**Before adding a UI element that violates a template rule:**

1. Identify which rule is being violated (cite section and item from `comparison-template-standard-v1.md` or `mobile_geometry_checklist_v1.md`)
2. State the consumer need that cannot be met without the exception
3. State why no in-template solution exists
4. Define the exact constraints that prevent the exception from multiplying
5. Submit for registry approval before shipping

If you cannot answer all four questions, the exception is not ready. Build the in-template solution instead.

---

## Active Exceptions

### EXCEPTION-001 — Bread Fermentation Filter Tooltip

**Status:** Approved  
**Category:** לחם (Bread)  
**Date approved:** 2026-05-28  
**Rule violated:** UI Stabilization Sprint 1 — "no tooltips on any UI element except EXCEPTION-001" (which this entry defines)

---

**What it is:**

A ⓘ info icon placed beside the filter option "ללא מחמצת מזוהה" in the bread category filter panel. When tapped, it displays a brief explanation (1–2 sentences maximum) of what "ללא מחמצת מזוהה" means in plain language.

It does not appear on any product row, any ingredient list, any score chip, or any other UI element. It appears only on one specific filter label.

---

**Why it is allowed:**

The filter label "ללא מחמצת מזוהה" uses the word "מחמצת," which is printed on bread packaging by manufacturers as a consumer-facing claim. It is not internal framework vocabulary. The tooltip clarifies a filter option whose words are already in use on product labels — the consumer who buys bread has already seen this word.

The need arises because a consumer may tap the filter and not understand why a bread with "שאור" in its name appears in the "ללא מחמצת מזוהה" filter. The tooltip explains that the filter reflects what was detectable in the ingredient list — not the packaging claim. This is a verification statement, not a framework disclosure.

---

**Why it does not violate the ontology-leakage policy:**

The ontology-leakage policy prohibits surfacing internal framework concepts in consumer language. The concepts at risk are: NOVA, BSIP, cap values, routing logic, structural classes, and analytical methodology.

This tooltip explains none of those. It explains the gap between a label claim and an ingredient-list signal, using words the consumer already knows: מחמצת (from packaging), שמרים (from packaging), רשימת הרכיבים (universally understood). No internal scoring variable, weight constant, or framework class is mentioned or implied.

Test: A consumer reading this tooltip learns that some breads say "שאור" on the front but use industrial yeast in the ingredients. That is a shelf observation, not a framework disclosure.

---

**Constraints preventing multiplication:**

1. **This is the only tooltip in the product.** No other filter option, score chip, ingredient item, product name, or UI element may carry a tooltip. A second tooltip anywhere in the product — regardless of category — constitutes a drift event requiring registry review and explicit re-approval.

2. **The tooltip text is fixed and reviewed.** It may not be updated without editorial review. It is not dynamically generated.

3. **Scope is bread only.** This exception was approved because מחמצת is a consumer-visible claim specific to the bread category. Other categories may not use this exception as a precedent. If מעדנים or חלב requires a tooltip, a new registry entry must be written and approved — it cannot inherit this approval.

4. **Filter context only.** The tooltip is permitted only on the filter label. If any developer or designer places a ⓘ icon on a product row, score chip, or ingredient text, it is an unauthorized exception regardless of content.

---

**Approved text (Hebrew):**

> "מחמצת לא זוהתה ברשימת הרכיבים. המוצר עשוי לציין שאור על האריזה."

Maximum 2 sentences. No additional explanation.

---

### EXCEPTION-002 — "Algorithm / Scoring Engine" Vocabulary in Social Marketing Collateral

**Status:** Approved
**Category:** Off-page social/marketing collateral (Instagram carousel and equivalent), NOT comparison pages
**Date approved:** 2026-07-02
**Authority:** Owner ruling (explicit override, 2026-07-02)
**Rule violated:** Framework-invisibility / ontology-leakage policy (`bari_editorial_intelligence_v1`) and the leakage gate `integrations/clients/hebrew_readability.py` `_LEAK_TERMS`, which ban "אלגוריתם" and "מנוע הניקוד" in consumer-facing copy.

---

**What it is:**

Social marketing collateral may name the scoring mechanism explicitly — e.g. "מנוע ניקוד אלגוריתמי" (algorithmic scoring engine) and "אלגוריתמי" — to convey the rigor/objectivity of Bari's scoring as an acquisition message.

---

**Why it is allowed:**

Owner ruling: the algorithmic, systematic, science-based nature of the scoring IS the differentiator for marketing acquisition ("it is not someone guessing the scores"), and the owner explicitly wants it named in ad copy. On-page framework invisibility exists to keep the *comparison experience* clean; a top-of-funnel social ad has a different job (explain why Bari is credible) and a different audience (people who have not yet seen the product). The owner, as the highest editorial authority, weighed this and chose to expose the mechanism in marketing only.

---

**Constraints preventing multiplication:**

1. **Marketing collateral only.** This exception NEVER extends to comparison pages, product rows, score chips, ingredient lists, filters, or any on-site consumer copy. Framework invisibility holds in full on the site.
2. **This term only.** It does not license other framework vocabulary. NOVA, BSIP, cap values, routing logic, structural classes, weight constants remain banned everywhere, marketing included.
3. **Claims stay defensible.** Naming the engine does not permit overclaim: no "every product / same way" universality (categories carve-out / mid-rollout), no per-score citation claim, no health/medical claim.
4. **Two-gate still applies.** Every such asset still passes Content + Adversarial QA. This exception resolves the leakage finding only; all other findings stand.
5. **Gate bug is separate.** The leakage gate currently false-passes "אלגוריתמי" because Hebrew final-letter inflection (מ vs ם) breaks its substring match. That is a defect to fix in `hebrew_readability.py` regardless of this exception; the exception does not depend on or excuse the bug.

---

### EXCEPTION-003 — Recommendation-Tier Vocabulary for the מדריכים (Guides) Product

**Status:** Approved — dual-keyed Product Agent (author) + Nutrition Agent (co-sign landed
2026-07-04). Owner directive already given; this entry LOGS it per exception-registry
discipline, triggered by QA gate-2 red-team finding RT-4
(`03_operations/reports/qa/magnesium_guide_tier_copy_redteam_v1.md`).
**Category:** מדריכים (Supplement Guides) tier-label UI only — the magnesium guide
(TASK-504) and any future guide built on the same bar rubric (e.g. creatine). Does **not**
extend to comparison pages, BSIP/food-score presentation, or marketing collateral
(marketing has its own separate EXCEPTION-002).
**Date approved:** 2026-07-04. Nutrition co-sign delivered this session — see
`01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md`.
**Authority:** Owner ruling (explicit, 2026-07-04). Co-signers: Product Agent (this entry)
+ Nutrition Agent (owns `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`,
the source of the tier logic this vocabulary names).
**Rule violated:** The recommendation-language HARD-leak gate,
`integrations/clients/hebrew_readability.py` `_RECOMMENDATION_TERMS` (contains the
literal term "מומלץ"), one of the `_HARD_LEAK_KINDS` that fails `is_clean` — a
score-presentation-era rule enforcing "Bari describes, never prescribes."

---

**What it is:**

The 4 owner-final Guides recommendation-tier labels — **מומלץ מאוד**, **מומלץ**, **טוב**,
**לא מומלץ** — used as the tier-header vocabulary on the מדריכים (Guides) product (e.g.
the magnesium buying guide). Three of the four literally contain the banned substring
"מומלץ" and HARD-fail the mechanical leak gate as currently wired.

---

**Why it is allowed:**

This is not a claim that "מומלץ" isn't really recommendation language — it is, plainly,
and the exception says so honestly rather than arguing around it. The owner directed
these exact 4 labels (2026-07-04, this session) because the Guides product's entire
consumer promise is structurally different from a comparison page's: a comparison page's
job is to lay out facts and let the reader compare (the ban exists precisely so the page
never tips its hand); a buying guide's entire job is to tell the reader what to do next.
Recommending is the product, not a leak into it. The recommendation ban was written for
and belongs to the comparison-page/score-presentation surface; it was never designed with
a "how to choose X" guide in mind, and applying it there blocks the product from doing
its stated job.

**Separately, and independently**, this exception does NOT reopen the owner's earlier
rejection of a composite/numeric ranking. The 4 tiers are a purely CATEGORICAL grouping
computed from the 6 already-visible PASS/FLAG/FAIL/CANNOT-VERIFY bar states (see
`01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
`recommendation_tier_mapping`) — no composite score, no percentage, no numeric field
anywhere.

**Correction made at Nutrition co-sign (2026-07-04):** the citation above originally read
"dual-keyed Nutrition + Product D7" — that overstated the mapping's approval state and is
corrected here. Product's original `recommendation_tier_mapping` proposal computed the
מומלץ/טוב split by **counting** non-PASS bars and thresholding at 1-vs-≥2. Nutrition ruled
that this DID compute a prohibited implicit numeric aggregate under Hard Rule 1 (a count is
a sum, even when only used for a binary gate) and replaced it with `dose_adequacy_sole_caveat`,
a set-membership predicate that performs no counting and reaches the identical tier
assignment on the current 18-product corpus. That replacement carries Nutrition's D7;
**Product's D7 co-sign on the amended predicate specifically is still outstanding** (tracked
in the mapping's own `status` field and in
`01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md`). This does not block
THIS exception: no tier-split logic has shipped to any live surface yet (Frontend has not
built against the mapping), and the vocabulary question this exception resolves is
independent of exactly which compliant split predicate ultimately governs מומלץ vs טוב —
both candidate mechanisms produce the same 4 categorical tier names with nothing numeric
shown to the consumer. The recommendation-LANGUAGE question (is the word "מומלץ" allowed)
and the recommendation-MECHANISM question (is there a hidden score behind it) remain two
different gates; this exception resolves only the first. The anti-drift invariant continues
to govern the second, via the dual-keyed mapping review once Product's co-sign on
`dose_adequacy_sole_caveat` lands, and is otherwise unaffected by this vocabulary exception.

---

**Constraints preventing multiplication:**

1. **Guides tier-label token only — never prose.** The exemption applies ONLY to the 4
   exact strings above when they are the literal, standalone value of the tier-label
   field (a tier header/badge). It does NOT license "מומלץ," "כדאי לקנות," "עדיף לקנות,"
   or any other recommendation phrasing inside Guides body copy, captions, one-liners, or
   any full sentence — even one that happens to contain the word "מומלץ." A caption like
   "מומלץ לבדוק את התווית" is NOT covered by this exception and must still be rewritten
   or separately excepted. See the gate carve-out spec below for how this is enforced
   mechanically (exact-string match, not substring/contains).
2. **Guides product only.** Never comparison pages, never BSIP/score-presentation copy,
   never marketing collateral. If a comparison page or any BSIP-adjacent surface is found
   using "מומלץ," that is a real leak, not a use of this exception.
3. **Bound to the current categorical tier logic.** This exception is granted for the
   4-tier system AS COMPUTED TODAY — a pure lookup over visible bar states with zero
   numeric aggregation. If any future revision of the Guides tier logic introduces a
   composite score, weighting, or numeric aggregate of any kind, this exception is void
   automatically and requires a fresh Product + Nutrition review; it does not carry over
   by inertia.
4. **Two-gate still applies in full.** Every Guides string — tier labels included — still
   requires Content + Adversarial QA sign-off (`content_signoff_hard_rule`). This
   exception waives only the mechanical leak-gate's HARD block on these 4 exact strings;
   it waives no editorial, red-team, or accuracy review.
5. **Reusable only for the same mechanism.** A future guide (e.g. creatine) built on the
   SAME bar rubric and SAME 4-tier categorical structure may reuse this exception without
   a new registry entry. A DIFFERENT Guides product using a DIFFERENT recommendation
   mechanism (not a pure bar-state lookup) requires its own fresh entry — it cannot
   inherit this one.

---

**Approved text (Hebrew, exact strings only):**

> מומלץ מאוד · מומלץ · טוב · לא מומלץ

No other recommendation phrasing is authorized by this entry.

---

**Gate carve-out implementation:** see
`03_operations/reports/product/madrichim_tier_vocabulary_gate_carveout_spec_v1.md` for
the implementable spec (scope-gated, exact-string-match exemption in
`hebrew_readability.py`) — Product does not implement; routed to the gate/copy-rules code
owner and Frontend for wiring.

---

### EXCEPTION-004 — BSIP1 Reversed-Bracket-Nesting Repair (barcode 4267230, crackers/ricecakes)

**Status:** Approved — Nutrition Agent finding + recommendation, Data Agent implementation
(TASK-517, 2026-07-05).
**Category:** קרקרים/פריכיות (Crackers, ricecakes expansion) — BSIP1 enrichment stage,
one product record only.
**Date approved:** 2026-07-05.
**Authority:** Nutrition Agent (source-defect diagnosis + approved fix design). Not a
scoring-rule change — no D6/D7 co-sign required (confirmed: score/grade unaffected,
41.2/D before and after re-run).
**Rule violated:** The "never rewrite BSIP1 text, missing-data-discard rather than
correct" default posture (`missing_data_discard_rule`; also the general never-invent/
never-clean-structural-data norm this Data Agent operates under). This entry documents
why a narrow, signature-gated repair is the correct exception to that default here,
rather than discarding the product.

---

**What it is:**

A stack-based reverse-nesting detector plus a position-preserving character-swap repair
(`detect_reversed_brackets()` / `normalize_reversed_brackets()` /
`repair_reversed_brackets()` in
`03_operations/bsip1/run_ricecakes_conform_001/build_ricecakes_bsip1.py`), applied to
`ingredients_text_he` during BSIP1 enrichment. It fires ONLY when the detector proves the
bracket nesting is inverted (a `)`/`}` appears before its matching opener is on the
stack) — never as a blanket transform on every product's ingredient text.

---

**Why it is allowed (repair, not fabrication):**

Barcode 4267230's `ingredients_text_he` carries a bracket-reversal bug present in
Shufersal's OWN raw HTML source
(`03_operations/bsip0/raw_store/shufersal/ricecakes/P_4267230/20260705T055346868812.html`,
line 2790: `<div class="componentsText">...</div>`) — parentheses and curly braces are
systematically mirrored/swapped at fixed positions (`(`<->`)`, `{`<->`}`), while every
other character (letters, digits, punctuation, whitespace) is untouched and in its
original order. Unscrambling with the inverse of that exact swap (itself a swap, since
swapping twice is the identity) produces text with provably correct, balanced bracket
nesting — confirmed by re-running the same detector against the repair's own output and
finding zero remaining reverse-nesting flags. No character was invented, deleted, or
reordered; only the open/close role of 4 bracket glyphs was corrected in place. This is
the textbook difference between "fixing a known encoding/scrape artifact whose inverse
transform is provable" (a repair) and "guessing what a missing value should be" (which
the missing-data-discard rule correctly forbids and this repair does not do).

**Scope confirmed non-systemic:** An independent stack-based scan was run against ALL 54
BSIP1 records feeding the crackers comparison page (20 files in
`run_crackers_conform_001/output` — 19 displayed + 1 pre-existing nutrition-nulled
exclusion — plus 34 files in `run_ricecakes_conform_001/output`). The signature fired
on exactly ONE record: barcode 4267230. Every other product's ingredient text has
normal, correctly-ordered brackets (or none). This is a single-product scrape-side
defect, not a scraper-template or corpus-wide issue — a blanket transform would have
been wrong and unnecessary; the signature-gated design guarantees it never fires
elsewhere unless the exact same fault pattern recurs.

---

**Effect on scoring (verified, not assumed):** BSIP2 was re-run for the full 34-product
ricecakes batch before and after the fix. Barcode 4267230's `final_score_estimate` and
`grade_estimate` are byte-identical before and after (41.2 / D) — the additive/marker
extraction that drives scoring (e.g. E-322 lecithin detection) matches on substrings
that don't depend on bracket direction, so the repair changes only the displayed
ingredient text and the `ingredient_order` diagnostic breakdown (which went from an
incorrectly depth-tracked count of 2 to the correct 5, matching BSIP2's own independent
parse), not any scored signal. The other 33 ricecakes products' BSIP2 traces are
byte-identical except the non-semantic `trace_generated_at` timestamp (verified by diff
across all 34).

---

**Constraints preventing multiplication:**

1. **Signature-gated, not barcode-gated.** The trigger is `detect_reversed_brackets()`,
   a general stack-based proof of inverted nesting — not a hardcoded barcode check. It
   will correctly no-op on every product that does not exhibit this exact fault, now or
   in future corpus expansions of this script. It must never be replaced with a blanket
   `.translate()` call unconditioned on the detector.
2. **Position-preserving swap only.** The repair function may only swap `(`<->`)` and
   `{`<->`}` in place. It must never reorder characters, insert/delete text, or "tidy up"
   the result beyond what the pure swap produces (even where the swap yields a
   cosmetically odd but faithful artifact, e.g. an adjacent empty `()` pair — see the
   pinned unit test in `test_bracket_repair.py`, which documents this explicitly).
3. **Full corpus scan required before reuse.** Before applying this same repair function
   to any other category's BSIP1 script, a fresh stack-based scan of that category's
   corpus must confirm the signature is genuinely present (not assumed by analogy) and
   the fix must be logged as its own exception-registry entry — this entry does not
   pre-authorize silent reuse.
4. **Fully audited.** Every application logs before/after text into the BSIP1
   `data_fixes_applied` array and the run record's `bracket_repairs_applied` list
   (`run_ricecakes_conform_001/run_record.json`). A repair with no before/after log is a
   process violation of this exception, not a valid use of it.
5. **Not a precedent for skipping missing-data-discard.** This exception applies only
   when the corruption's inverse transform is provable and mechanically checkable (as
   here). It does not license repairing corruption whose original form cannot be proven
   (e.g. the unrelated per-serving/per-100g corruption on barcode 7290112968807, which
   remains correctly nulled per the missing-data-discard rule — that corruption has no
   provable inverse, only a plausible scaling-factor guess, which is exactly what the
   discard rule exists to forbid).

---

**Verification artifacts:**
`03_operations/bsip1/run_ricecakes_conform_001/build_ricecakes_bsip1.py` (FIX 3),
`03_operations/bsip1/run_ricecakes_conform_001/test_bracket_repair.py` (10/10 pinned
tests incl. the exact barcode-4267230 string), `run_record.json` →
`bracket_repairs_applied` (1 entry, barcode 4267230).

---

## Rejected Exception Requests

*None yet. This section will log exception requests that were reviewed and denied, with rationale, so future contributors understand the boundaries.*

---

## Governance

### Approval process

1. Write a proposed entry following the format above
2. Answer all four required questions (rule violated, consumer need, no in-template solution, multiplication constraints)
3. Present for editorial review — approved additions are merged into this registry and the relevant UI spec is updated to reference EXCEPTION-[N]
4. Unapproved exceptions shipped to production are architecture violations, not judgment calls

### Registry maintenance

- Exceptions are reviewed at each major category launch
- If an exception's consumer need disappears (e.g., bread changes its filter label), the exception is retired and the tooltip removed
- Retired exceptions remain in this document under a "Retired" section for historical reference

### The drift test

Before adding an exception, ask: if ten other teams in ten other categories saw this exception, would it spread into something that mutates the architecture? If yes, the exception is not narrow enough. Tighten the constraints or abandon the exception.

---

*This registry is governed by the same editorial authority as `comparison-template-standard-v1.md` (the canonical comparison template). Architecture rules in the template take precedence over any exception not documented here.*
