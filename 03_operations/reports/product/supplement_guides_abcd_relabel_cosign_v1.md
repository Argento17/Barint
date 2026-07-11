# Supplement Guides — A/B/C/D Band Relabel: Product Agent Co-Sign (TASK-504)

**Task:** Owner ruling co-sign, dual-key with Nutrition per `recommendation_tier_mapping`
in `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`.
**Reviewer:** Product Agent. **Date:** 2026-07-04.
**Nature of this review:** confirms an OWNER decision is implementable cleanly and
anti-drift-safe; does not relitigate it. Recommends the exact mapping/labels and flags
the one load-bearing production consequence the owner's decision creates.

**Bonus closure in this return:** Nutrition's `dose_adequacy_sole_caveat` split predicate
(`supplement_guides_tier_mapping_cosign_v1.md`) has been sitting on an outstanding Product
D7 co-sign since 2026-07-04 earlier this session. Reviewed here (§0) and **co-signed** —
this was a blocking gap on the very system this task now relabels, so closing it here
rather than leaving two open co-signs on the same mechanism.

---

## §0. Outstanding Nutrition D7 co-sign — CO-SIGNED

Reviewed `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`
`recommendation_tier_mapping.passes_with_flag_split_rule` (`dose_adequacy_sole_caveat`) and
Nutrition's ruling that Product's original count-threshold split (1 vs ≥2 non-PASS bars)
computes a prohibited implicit numeric aggregate under Hard Rule 1.

**Product Agent D7: CO-SIGNED.** Nutrition's existential-quantifier vs. cardinality-comparison
distinction is correct and the replacement predicate reaches the identical result on the
current corpus (verified: `supplement_guides_tier_mapping_cosign_v1.md` §2 table, 2×מומלץ /
3×טוב, matches Product's original count-rule output exactly). No objection. This mechanism
now carries full dual-key authority and Frontend may build against it.

---

## 1. Label mapping — CONFIRMED, one clarification

| Bucket (unchanged mechanism) | Current Hebrew tier | Letter |
|---|---|---|
| `clears_all_bars` | מומלץ מאוד | **A** |
| `passes_with_flag`, caveat set = `{dose_adequacy}` | מומלץ | **B** |
| `passes_with_flag`, caveat set ≠ `{dose_adequacy}` | טוב | **C** |
| `fails` | לא מומלץ | **D** |
| `cannot_assess` | לא ניתן להעריך | **stays unlettered** |

I would not order or name this differently. A→D is the mechanical, already-approved
`recommendation_tier_mapping` order (`tier_ordering_no_within_tier_sort`) with nothing
recomputed — this is a pure label swap on an existing categorical grouping, not a new
mechanism, and not something to second-guess for its own sake.

**One clarification, not a change:** `cannot_assess` must NOT become a 5th letter ("E" or
"N/A" styled as part of the sequence). TRIOMAG's undisclosed 3-way blend is a data gap, not
a worse verdict than D — giving it a letter invites exactly the ordinal reading ("E is worse
than D") that `bucket_logic`'s own `worked_distinction` (Tink Oxide-520 = known-bad form →
fails/D; TRIOMAG = genuinely unknowable → cannot_assess) was written to prevent. It keeps its
existing out-of-sequence, separately-labeled section per `display_position`
(already co-signed, unchanged here).

---

## 2. Anti-drift check — where's the line, and does A/B/C/D stay on the right side of it

**Mechanically: yes, cleanly.** Hard Rule 1 (the rubric's anti-drift invariant) bans a
*computation* — summing, weighting, or thresholding a cardinality into a numeric aggregate.
Swapping the display string on an already-computed categorical bucket (מומלץ מאוד → "A")
introduces no computation at all. The bucket membership rule (`bucket_logic` + the co-signed
`dose_adequacy_sole_caveat` set-membership test, §0 above) is completely unchanged; only the
label rendered next to the result changes. This is architecturally identical to
`display_suppression_rule` — a presentation-layer change layered on top of an unchanged
computation — which Nutrition already ruled compliant on the same grounds.

**Semiotically: no, not for free — and this is the real question, not the mechanical one.**
The task's own framing is right: a bare letter reads more like a *score* than a Hebrew word
does, independent of what's computed underneath, because Bari's own site already trains
users to read a letter grade as a score. Live food comparison pages show grades in exactly
the format `72/B` (`bari_score_presentation_v1` — numeric/grade, no strength labels). A bare
"B" badge on a supplement product sitting next to a badge system a shopper has *already
learned means "computed score"* elsewhere on the same site is a real cross-contamination
risk, not a hypothetical one — and it already fired once: the magnesium guide's gate-2
red-team (`RT-6`, TASK-504 log) caught the bar-state badge literally importing
`gradePalette.A/C/E` byte-for-byte, and Design's vision-critic independently flagged the same
thing as CRITICAL before it shipped. That was a component reusing grade *colors*; a bare
letter reuses the grade *symbol* itself, which is the harder case, not the same one already
fixed.

**The line, stated plainly:** the invariant governs computation; the *live BSIP0/BSIP2
firewall this rubric is built on* (`firewall.bsip2_exposure: none`) governs mental-model
separation from scored food. A→D crosses the second concern even while it fully respects the
first. Both must hold for this to ship clean.

**What closes the gap — required, not optional:**
1. **Never render a bare letter alone.** Every band badge carries the word "קבוצה" (band/group)
   or equivalent, e.g. "קבוצה A", never a solo circled "A" — the same discipline already
   applied to keep `bar-state-badge` a 4-state primitive distinct from a grade chip.
2. **Distinct visual system from `ScoreChip`/`gradePalette`.** No shared hex values, no shared
   shape/typography with the food-grade component — same rule Design already enforced on the
   bar badges, extended explicitly to the new tier-level letter.
3. **A one-line, static definition caption travels with the badge wherever it appears** (not
   just in a scrolled-past intro paragraph — same "visible, not buried" discipline as the
   safety bar's `rendering_rule`): *"קבוצה = קיבוץ קטגורי לפי אילו ספים המוצר עומד בהם, לא ציון
   מחושב"* (a band = a categorical grouping by which thresholds a product clears, not a
   computed score). This is the honest-framing caption the task asked about — it is required,
   not a nice-to-have, precisely because the letter alone under-discloses relative to the
   Hebrew-word version it replaces.

With all three, this stays on the right side of the line. Without item 2 specifically, it
does not — and it is the one Frontend is most likely to skip by default, since reaching for
the existing grade component is the path of least resistance.

---

## 3. The D-band framing — does relabeling achieve the owner's actual goal

**Honest answer: no, not by itself — and I'd say so plainly rather than let this ship on the
assumption that it does.** The owner's stated reason for moving off "לא מומלץ" was that it
felt like too blunt a negative verdict on a named brand. A bare "D" does not fix that; if
anything it risks reading as blunter to a consumer raised on school grading, where D is
"barely passing / nearly failing" — a harsher personal judgment than the plain factual
Hebrew phrase it replaces. Renaming the wrapper without changing what's inside it is not the
fix the owner is asking for; it's the same verdict in different packaging, and worth saying
so directly rather than quietly shipping it as if the letter alone solved the problem.

**What actually achieves "grouping, not a stamp":** the same discipline already used
correctly elsewhere in this build. The FAILS bucket's own products already carry a factual,
specific `oneLinerHe` naming exactly which bar failed and why (verified in
`creatine-guide-data.ts`, e.g. line ~511, MyProtein Creatine Tablets: *"לא מפורט — התווית
לא מציינת מספר גרם קריאטין למנה. מוצר טבליות מיובא."* — a fact, not a condemnation). That
pattern is the honest framing, and it must be **mandatory, not incidental**, for every D-band
product: the band badge is never shown without the specific blocking-bar reason immediately
adjacent (which threshold, what the actual number is, sourced from the bar's own `measures`
definition) — never a bare "D" with the reason left to a separate row a reader might not
reach. This is a direct extension of the safety bar's own `rendering_rule` ("a FAIL... is a
bar-level, always-visible block — never a tooltip, never collapsed") to the tier level: the
same discipline that already governs one bar must govern the tier label built from it.

**Recommendation:** ship the letter (it's the owner's explicit call, and B/C/D read less
loaded than a red "לא מומלץ" chip in aggregate table view, which is a real and legitimate UI
win), but do not present the relabel as having solved the "too blunt" problem. It reduces the
list-view starkness; it does not, by itself, reduce the per-product verdict weight — that
requires the mandatory causal caption above.

---

## 4. Benchmark split + provenance tags — CONFIRMED, with one production consequence flagged

**Confirms the buying-guide model cleanly.** Pulling `wb-*` products out of the four ranked
bands into a separate BENCHMARK section is exactly right for "don't lead an Israeli shopper
with products they can't buy here" — and it doesn't distort the NSF-gap finding, because nothing
about bar-state *computation* changes: the rubric's `price_fairness.boundary_method.currency_rule`
already keeps ₪-priced and $-priced products on separate, never-mixed medians (Israeli-shelf
bars were never computed against worldwide $-prices to begin with). This is a display/grouping
change layered on unchanged computation — the same category of change as
`display_suppression_rule`, and it needs no new D6/D7 pass beyond this co-sign.

**Two distinct axes — do not conflate them, and name both clearly in the shipped copy:**
1. **Ranked vs. Benchmark** (decision #2): is this product part of the Israeli shopper's
   actual buying-decision set at all. `wb-*` items move to BENCHMARK.
2. **Domestic-shelf vs. import-via-iHerb/MyProtein** (decision #3): *within* the ranked set,
   how does a shopper actually acquire it. This tag already has a real, sourced answer for
   every ranked item today — it is not new research. The existing creatine data already
   distinguishes these per-product in comments and in shipped copy (e.g. `creatine-guide-data.ts`
   line 339 "Thorne (IL/iHerb) Creatine," and its own `oneLinerHe` already states *"הרישום
   ה-iHerb הישראלי לא נבדק בנפרד"*). Formalizing this into a structured provenance field is
   populating a fact that already exists in the data model, not fabricating one.

**Load-bearing consequence to flag before this ships (verified, not eyeballed):** grepping
`creatine-guide-data.ts` for `bucket: CLEARS` shows all three of creatine's current
`clears_all_bars` (→ A band) members are `wb-*` benchmark products — `wb-thorne-creatine`
(line 517), `wb-momentous-creatine` (line 531), `wb-bpn-creatine` (line 560). Zero
Israeli-shelf/import-buyable creatine products clear all 6 bars today. Once `wb-*` moves out
of the ranked bands per decision #2, **creatine's A band goes from 3 members to empty** —
the identical "0/N clears every bar" finding magnesium already shipped and got a co-signed
empty-tier treatment for (`empty_state_handling`, rendered unconditionally with an honest
headline). This is not a new mechanism to build — reuse the existing empty-tier rule as-is —
but it IS new copy: creatine's gate-1 tier copy (`creatine_guide_tier_copy_v1.md`) was
authored under the old assumption that the A band had 3 members, and that pack, plus the
`headlineFinding` text on the creatine guide, needs a rewrite to state the honest empty
result once wb items move out. Flagging this now so it doesn't surface as a surprise gate-2
finding the way the magnesium empty-shortlist issue did in Wave 0 — route the copy rewrite to
Content, two-gate as usual.

**Scope discipline on the provenance tag (Hard Rule 2 — naming the cut):** ship this as a
static two-value tag ("במדף בישראל" / "מיובא — iHerb / MyProtein") plus one factual caption
line, sourced from the scrape's own retailer identity — nothing computed. Explicitly OUT for
v1: any shipping-cost estimate, customs/import-tax math, or delivery-time claim. Those numbers
are not reliably sourceable and estimating them would violate Hard Rule 9 (no invented
figures) for a guide whose entire premise is honesty over the SIE's own composite-scoring
history. If landed-cost information becomes a real product need later, it is a separate,
explicitly-sourced data acquisition task, not an extension of this tag.

**Before ship:** route a cheap check to the Data Agent — confirm each of the 18 IL-shelf
items' domestic/import classification against the actual scrape source record, not against
the existing free-text comments/copy (which are a reasonable signal but not the system of
record). Premise pre-check per Hard Rule 10, cheap and mechanical.

---

## 5. Apply the same relabel to magnesium — CONFIRMED, no divergence

Yes, unconditionally. `EXCEPTION-003` already governs both guides under one vocabulary rule
("the magnesium guide (TASK-504) and any future guide built on the same bar rubric (e.g.
creatine)") precisely so the two never drift apart on this axis — this repo's own standing
discipline (uniform baseline doctrine, zero-different-category mandate) applies here even
though this is a supplements product, not a food category: one relabel, applied identically,
same day, not "magnesium now / creatine later."

Two things carry over cleanly, one thing does not apply today:
- A/B/C/D + mandatory band caption + mandatory D-band causal caption: identical on both guides.
- `cannot_assess` (TRIOMAG, magnesium-only today) stays unlettered, same rule.
- The BENCHMARK-split consequence in §4 is a no-op for magnesium **today** — magnesium has no
  `wb-*` items yet (rubric: "magnesium has no worldwide benchmark set today"), so its A band
  stays empty for the same reason it already is (0/18, unchanged). But the BENCHMARK section
  as a template element should still exist in the shared guide component so it activates the
  moment a magnesium worldwide product is added — not rebuilt bespoke per guide later, per the
  same "no rubric rewrite required" principle the price-fairness pooling logic already uses.

---

## Return Contract

```json
{
  "task": "TASK-504-supplement-guides-abcd-relabel-product-cosign",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\supplement_guides_abcd_relabel_cosign_v1.md",
      "sha256": "pending — compute post-write"
    }
  ],
  "counts": {
    "creatine_clears_all_bars_members_verified": 3,
    "creatine_clears_all_bars_denominator": "31 total creatine products (18 Israeli-shelf/import + 13 worldwide benchmark), per creatine-guide-data.ts headers",
    "creatine_clears_all_bars_wb_prefixed": 3,
    "source_for_clears_all_count": "C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\creatine-guide-data.ts — grep 'bucket: CLEARS' -> lines 518 (wb-thorne-creatine), 532 (wb-momentous-creatine), 561 (wb-bpn-creatine); no non-wb match found",
    "magnesium_clears_all_bars_members": 0,
    "magnesium_clears_all_bars_denominator": 18,
    "source_for_magnesium_count": "01_framework/nutrition/supplement_guides_tier_mapping_cosign_v1.md §5 empty_state_handling (0/18, dated 2026-07-04)",
    "tier_mapping_elements_reviewed_this_return": 5,
    "outstanding_d7_items_closed_this_return": 1
  },
  "commands_run": [
    {"cmd": "Grep pattern 'bucket: CLEARS' path creatine-guide-data.ts", "exit_code": 0},
    {"cmd": "Grep pattern 'wb-' path creatine-guide-data.ts", "exit_code": 0},
    {"cmd": "Grep pattern 'EXCEPTION-003' path exception_registry_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "Rubric YAML edit (recommendation_tier_mapping letter field) — Nutrition-owned file (supplement_guides_bar_rubric_v1.yaml), not edited here; this report specifies the exact mapping for Nutrition/Frontend to apply",
    "EXCEPTION-003 registry addendum for the letter vocabulary — governance file, dual-keyed; recommend Product+Nutrition add a short addendum rather than a new exception (same category, same authority, just a symbol change)",
    "Creatine tier copy rewrite for the now-empty A band — routed to Content, two-gate as usual, not authored here",
    "Data Agent premise-check of the 18 IL-shelf items' domestic/import provenance against scrape source-of-record — recommended, not run here",
    "Frontend implementation of the band badge (letter + mandatory caption + distinct-from-ScoreChip visual system) — not built here, this is the scope spec for that build",
    "This does not close TASK-504 — proposal-and-ruling only"
  ],
  "acceptance_test": {
    "spec": "Confirm the A/B/C/D label mapping and order; rule on whether the letters stay on the right side of the anti-drift/firewall line and what's needed to keep them there; give an honest read on whether relabeling D achieves the owner's stated 'less blunt' goal and recommend a fix if not; confirm the benchmark split and provenance tag serve the buying-guide model without distorting the honest finding, citing real data for any consequence claimed; confirm the same relabel applies to magnesium.",
    "result": "PASS — mapping confirmed with rationale; anti-drift ruled compliant mechanically with three named, required implementation conditions to hold the firewall line; D-band relabel ruled insufficient alone with a concrete required fix (mandatory causal caption); benchmark/provenance split confirmed with the two-axis distinction named and one verified, cited production consequence flagged (creatine's A band goes to empty, sourced via direct grep of the live data file, not asserted from memory); magnesium relabel confirmed with no divergence. Bonus: closed the outstanding Product D7 co-sign on dose_adequacy_sole_caveat that was blocking full dual-key authority on the underlying tier mechanism this relabel sits on."
  }
}
```
