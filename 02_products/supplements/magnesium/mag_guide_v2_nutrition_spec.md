# Magnesium Guide v2 — Nutrition Evidence Spec

**Task:** TASK-575 subtask (Nutrition Agent)
**Governs:** `bari-web/src/lib/guides/magnesium-guide-data.ts` (current file, 630 lines, read in full for this spec) — the science/claims/grouping layer only. This document specifies claims, groupings, sources, and precedence rules for the Content Agent to author from. **It contains no final consumer Hebrew** — illustrative phrasing below is marked as such and is not cleared copy.
**Status:** Nutrition D6 proposal. Requires Product Agent co-sign (D7) before any of §2's group re-assignment, §3's dose-presentation change, or §5's absorption reclassification ships as live copy (these are scoring-*presentation* rule changes under `supplement_guides_bar_rubric_v1.yaml`'s governance, not pure copy edits — see §10).
**Input rubric:** `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml` (read in full, 1136 lines) — this spec amends and, in one place (§2), knowingly departs from its illustrative guidance. Departure is flagged, not silently taken (§9).
**Input dossier:** `03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml` (read in full).

---

## §0 — What this spec does and does not touch

This spec governs the **magnesium guide's presentation layer**: which descriptive group each of the 18 products belongs to, how dose is framed, what the absorption-evidence buckets say, how the cramps claim is scoped, and what sources back each claim. It does **not** touch:
- `score_engine.py`, `constants.py`, BSIP2, or any published food score (firewall unchanged, per rubric Hard Rule 2).
- The underlying bar-state computation logic in `supplement_guides_bar_rubric_v1.yaml` (PASS/FLAG/FAIL/CANNOT-VERIFY per bar) — those states are **inputs** to this spec's grouping logic, not something this document redefines. One exception is flagged explicitly in §9 (the bisglycinate badge-vs-copy tension).
- Any other supplement guide (creatine, etc.) — magnesium only.

---

## §1 — Model split: product assessment vs. market-information gaps

**Ruling.** Two categorically different things were being conflated in the live file and must never be merged again:

| | Product assessment (per-product, drives grouping) | Market-information gaps (guide-level, reported once) |
|---|---|---|
| Criteria | Dose adequacy, chemical form/absorption, safety (UL/GI-tolerance), label transparency | Price, third-party/independent testing |
| Why these four | All four are facts a consumer can read or derive from the product's own label. A product can be judged on them today. | Neither is observable from the label. Price was never collected by Bari (a Bari data-acquisition gap). Third-party testing: **no** magnesium brand in this 18-product corpus makes a certification claim at all (a fact about the market, not about Bari's collection) — this is not the same kind of gap as price, and copy must not conflate the two. |
| Renders | Per-product group membership (§2) | One guide-level statement, never a per-product badge, never a reason cited for why a specific product isn't in the top group |

**Kill instruction (verbatim finding).** Lines 486-490 of the current file state that the reason **zero products** reach the (retired) top tier is *not* product quality but the price/third-party gaps ("הסיבה המרכזית לכך אינה איכות ירודה של המוצרים עצמם... יש כאן שני דברים נפרדים..."). This is factually backwards under the corrected model and must not survive into v2. Under §2's four-criterion grouping, price and third-party testing are **excluded from the assessed set entirely** — they cannot explain why a product misses the top group, because they are never evaluated per-product in the first place. The real, product-level reason the top group is empty is stated at the end of §2: **no product in this corpus simultaneously has (a) a disclosed dose at or above the reviewed range's upper half, (b) a form with directional evidence of decent absorption, and (c) no safety-note dose crossing** — every product tested here that reaches a higher dose does so with magnesium oxide (directionally poor absorption, per §5), and every product with a well-regarded form tops out at 250 mg. That is a genuine, product-level finding (the guide's actual headline), not a byproduct of unrelated data gaps. Price/third-party gaps get their own, separate, one-line market statement (unchanged in spirit from the existing `suppressedBarsDisclosureHe` at line 511-512, which already correctly separates the two reasons — that line is fine as-is and should be kept, just decoupled from the tier-ladder framing that surrounded it).

---

## §2 — Product grouping: 18-row mapping table + precedence rule

### Precedence rule (defined here, applied uniformly)

Three tiers, evaluated top to bottom, first match wins, using **only** each product's already-computed per-product facts (bar states from `states: [dose, form, thirdParty, price, safety, label]`, `doseMg`, `formHe`):

1. **Tier 1 — known, determinate concern about the compound or its safety profile.** `form_absorption` state ∈ {FLAG, FAIL} **or** `safety` state ∈ {FLAG, FAIL} → **Group (c) Form or tolerance concern.**
   Rationale for ranking this above a dose-only concern: this mirrors the rubric's own already-co-signed `nutritional_grounding` principle (rubric lines 776-790) — a form or safety finding is a property of the compound the consumer cannot fix by taking more of it, categorically different from a quantity shortfall.
2. **Tier 2 — known, determinate dose concern, nothing else wrong.** `dose_adequacy` state ∈ {FLAG, FAIL} (a real, disclosed number, just outside the reviewed range) **and** Tier 1 did not fire → **Group (b) Lower elemental amount.**
3. **Tier 3 — the label itself does not disclose enough to know what's being delivered, and nothing above already resolved the product.** `label_transparency` state ∈ {FLAG, FAIL, CANNOT-VERIFY} **or** `form_absorption` = CANNOT-VERIFY (undisclosed multi-form blend) **or** `dose_adequacy` = CANNOT-VERIFY, **and neither Tier 1 nor Tier 2 fired** → **Group (d) Insufficient label information.**
4. **Default — nothing above fired.** All four assessed bars clean → **Group (a) Meets all assessed criteria.**

**Why "known problem" is checked before "data gap," not the reverse.** The task brief's illustrative ordering was "insufficient-label trumps all, then form/tolerance, then lower-amount." I did not use that literal order — see §9 for the full reasoning; in short, applying it verbatim would reclassify two products with a **known bad form** (oxide, directionally poor absorption per NIH ODS) as merely "insufficient label information" whenever their dose reading also happens to be ambiguous, which erases a real, actionable, already-established finding behind a data-gap label. The rubric's own `bucket_logic` (lines 450-455) already enacts the opposite principle — a known problem is never hidden behind an "insufficient data" framing — and I applied that same, already-house-standard principle here for consistency rather than introduce a new, conflicting one.

### 18-row mapping table

| # | Product (brand) | Disclosed elemental Mg | Form | Group | One-line factual reason |
|---|---|---|---|---|---|
| 1 | מגנזיום ציטראט+B6, סופהרב | 250 mg | Citrate | **(c) Form/tolerance concern** | Form and label are clean; the disclosed dose (250 mg) sits in the 250–350 mg soft GI-tolerance note band (`safety` = FLAG) — a real, determinate tolerance note, not a data gap. |
| 2 | מגנזיום ביסגליצינט, אלטמן | 250 mg | Bisglycinate | **(c) Form/tolerance concern** | Same profile as #1: 250 mg sits in the same soft GI-tolerance note band (`safety` = FLAG). |
| 3 | מגנזיום ציטראט 120, אלטמן | 200 mg | Citrate | **(b) Lower elemental amount** | Form, safety, and label all clean; 200 mg sits just above the corpus median (190 mg) but still below the upper-range doses (250 mg+). No other concern. |
| 4 | מגנזיום WELL, נוטריקר | 168 mg | Bisglycinate | **(b) Lower elemental amount** | Form, safety, and label all clean; 168 mg sits below the corpus median (190 mg), in the lower-middle of the reviewed range — a genuinely modest dose, no other concern. |
| 5 | אנטי לג קרמפס, NT L.C. | 190 mg | Hydroxide | **(b) Lower elemental amount** [REVISED, §11] | `form_absorption` moves off the FLAG/"בינונית" tier under the §11 ruling (Bucket-3 "evidence too limited" is no longer treated as a determinate Tier-1 concern) — no Tier-1 trigger remains. `dose_adequacy` = FLAG (190 mg, modest) fires Tier 2 instead. |
| 6 | ביסגליצינט 600 כמוסות, פול-מג הדס | 122 mg | Bisglycinate | **(b) Lower elemental amount** | Form, safety, and label all clean (label transparency is in fact a strong point here — see §9's bisglycinate-600 correction); 122 mg is in the bottom quartile of the reviewed range. No form or safety concern. |
| 7 | מגנזיום מלאט, טינק | 136 mg | Malate | **(b) Lower elemental amount** [REVISED, §11] | Same off-ladder move as #5: `form_absorption` no longer fires Tier 1. `dose_adequacy` = FAIL (136 mg, well below range) fires Tier 2. |
| 8 | מגנזיום מלאט, נוטריקר | ~135 mg | Malate | **(b) Lower elemental amount** [REVISED, §11] | `form_absorption` no longer fires Tier 1. `dose_adequacy` = FAIL fires Tier 2. Label also only states compound mass (700 mg malate) without an elemental conversion on-pack (`label_transparency` = FLAG) — a real, secondary fact that should still be named in copy, but the dominant, first-firing concern is now the low dose. |
| 9 | סידן ומגנזיום +D3, סולגר | 100 mg | Blend (oxide + citrate, ratio undisclosed) | **(b) Lower elemental amount** | The 100 mg elemental figure IS clearly disclosed on-label (`label_transparency` = PASS) — this is a known, determinate low dose. Separately, and not the dominant reason: the oxide/citrate split within that 100 mg is not disclosed, so the blend's own absorption profile cannot be separately assessed (`form_absorption` = CANNOT-VERIFY). Both facts belong in copy; the group reflects the dominant, determinate one. |
| 10 | מגנזיום טאוראט, נוטריקר | 76 mg | Taurate | **(b) Lower elemental amount** [REVISED, §11] | `form_absorption` no longer fires Tier 1. `dose_adequacy` = FAIL (76 mg, lowest disclosed dose in the corpus) fires Tier 2. |
| 11 | מגנזיום אוקסיד 520, נוטריקר | 520 mg | Oxide | **(c) Form/tolerance concern** | Two determinate concerns fire simultaneously: `form_absorption` = FAIL (oxide, §5 directionally-poor bucket) and `safety` = FAIL (520 mg exceeds the 350 mg supplemental UL). Both should be named in copy — this is the corpus's clearest multi-issue case. |
| 12 | מגנזיום 520, אלטמן | 520 mg | Oxide | **(c) Form/tolerance concern** | Identical profile to #11. |
| 13 | מגנזיום UP, אלטמן | 450 mg | Oxide | **(c) Form/tolerance concern** | Same two determinate concerns as #11 (form FAIL + safety FAIL), at 450 mg. |
| 14 | מגנזיום באלאנס, אלטמן | 450 mg | Oxide | **(c) Form/tolerance concern** | Same as #13. Co-ingredients (ashwagandha, valerian) on the label are irrelevant to the magnesium-specific finding. |
| 15 | נאנו מגנזיום ליפוזומלי, נוטריקר | 88 mg | Bisglycinate (stated base form) | **(b) Lower elemental amount** | Form (bisglycinate base), safety, and label all clean; 88 mg is the second-lowest disclosed dose in the corpus. The "nano liposomal" delivery claim is a separate, unresolved marketing claim (no evidence in-file to confirm or deny an absorption benefit beyond the base form) — does not change the group, should be named as a distinct, unverified claim in copy, not folded into "form." |
| 16 | מגנזיום אוקסיד 520, טינק (90 כמוסות) | Ambiguous (520, unit unresolved) | Oxide | **(c) Form/tolerance concern** | `form_absorption` = FAIL fires (oxide is a known, determinate poor-absorption form — this is knowable even though the exact elemental-vs-compound reading of "520 mg" is not, per the rubric's `blend_rule.distinguished_from` clause). The dose-reading ambiguity is a real, additional, and separate finding that must also be named in copy — but it does not soften or reclassify the known-bad-form finding into a mere data gap. |
| 17 | pH מגנזיום, אמורפיקיור | Ambiguous (unresolved) | Carbonate | **(c) Form/tolerance concern** | Same logic as #16: `form_absorption` = FAIL fires because carbonate is a known, determinate poor-absorption form (§5), independent of the unresolved dose reading. |
| 18 | TRIOMAG, סופהרב | Unresolved | Undisclosed 3-form blend (citrate/bisglycinate/taurate) | **(d) Insufficient label information** | The **only** product in the corpus where nothing is determinately known: the form itself is an undisclosed-ratio blend (`form_absorption` = CANNOT-VERIFY), so no dose, safety, or absorption statement is possible at all. This is a genuinely different finding from #16/#17 — there the *form* is known and bad; here the *form itself* is unknowable. Keep these visibly distinct in copy (the rubric's own `bucket_logic.worked_distinction`, lines 459-466, makes exactly this point and should not be re-collapsed). |

*Median correction (Product Agent D7 catch, applied here): the 15 determinate `doseMg` values sorted are {76, 88, 100, 122, 135, 136, 168, 190, 200, 250, 250, 450, 450, 520, 520}; the 8th of 15 is the median, i.e. **190 mg** (product #5, NT L.C.) — not 168 mg (product #4). This corrects an arithmetic slip in an earlier draft of this spec and is now the value used consistently throughout §2 and §3 (body text, table rows #3/#4, and the gauge-geometry median reference tick).

### Group distribution

**REVISED by the §11 QA gate-2 ruling** (2026-07-10) — the original distribution below is superseded; see §11 for the full derivation. Original (pre-§11) counts, kept for the audit trail: (a) 0/18, (b) 5/18 (#3,#4,#6,#9,#15), (c) 12/18 (#1,#2,#5,#7,#8,#10,#11,#12,#13,#14,#16,#17), (d) 1/18 (#18).

**Current (post-§11):**
- **(a) Meets all assessed criteria: 0/18**
- **(b) Lower elemental amount: 9/18** (#3, #4, #5, #6, #7, #8, #9, #10, #15)
- **(c) Form or tolerance concern: 8/18** (#1, #2, #11, #12, #13, #14, #16, #17)
- **(d) Insufficient label information: 1/18** (#18)

Sum check: 0 + 9 + 8 + 1 = 18. ✓

### Why (a) is genuinely empty (the real headline, replacing the retired ladder's empty-top-tier framing)

**Corrected under §11** (the pre-§11 version of this paragraph mis-stated #2, Altman Bisglycinate, as a citrate product — a drafting error, caught during the §11 revision, not present in the group table itself). Every product that reaches a disclosed dose at or above the reviewed range's upper half (450–520 mg: #11–14, #16) does so in magnesium oxide — a form with directional evidence of poor absorption (Bucket 2, §5). The two citrate products (#1, #3 — the only Bucket-1, NIH-confidently-better-absorbed form present in this corpus) top out at 250 mg. Every Bucket-3 "evidence too limited to rank" product (bisglycinate #2/#4/#6/#15, hydroxide #5, malate #7/#8, taurate #10) also discloses a dose below the range's upper portion (`dose_adequacy` = FLAG or FAIL for every one of them — none reaches PASS). So the finding holds for an updated, more precise reason: no product in this corpus combines a dose at the top of the reviewed range with a form that is either confidently well-absorbed (Bucket 1) or not confidently poorly-absorbed (i.e., not Bucket 2) — the only products reaching the top of the range are all Bucket 2 (oxide), a determinate concern. That is a real market-structure finding about this corpus, not an artifact of the price/third-party gaps (§1) and not a manufactured differentiation.

---

## §3 — Dose presentation spec: no universal effective-dose floor

### What must be deleted

- Line 570 (`educationSpine`, "התאמת המינון" heading): *"הספרות המדעית מצביעה על סביבות 300 מ"ג יסודי ליום כדי לקבל ערך משמעותי מתוסף"* — presents 300 mg as a general "meaningful value" floor. **Kill.**
- Same paragraph, line 570: *"מוצר שנותן פחות ממחצית הסף (מתחת ל-150 מ"ג) הוא בעיקר מחווה סמלית: הכמות קטנה מכדי לעשות הבדל אמיתי בתזונה"* — "mainly symbolic" framing tied to the same invented universal floor. **Kill.**
- Every product `oneLinerHe` and `headlineFinding.body` sentence that frames a dose as "עומד/לא עומד בסף" (meets/fails **the** threshold) as if 300 mg were a single validated effectiveness line for magnesium supplementation in general — lines 220, 231, 242, 253, 264, 275, 286, 297, 308, 319, 491–495. These need re-authoring under the comparative framing below, not a threshold-pass/fail framing.

### Why: the evidence behind "300 mg" is real but scoped, not general

Verified directly (WebFetch, PMID:27402922 → Zhang et al., *Hypertension*, Aug 2016, "Effects of Magnesium Supplementation on Blood Pressure: A Meta-Analysis..."): the review's own stated finding is *"Mg supplementation with a dose of 300 mg/d or duration of 1 month is sufficient to elevate serum Mg and reduce BP"* — median dose studied was 368 mg/day. **This is a blood-pressure-specific finding.** The paper makes no claim about 300 mg being an effectiveness floor for any other outcome (sleep, general deficiency correction, muscle function). This is also the exact citation the Bari supplement engine's `effective_dose.dose_citations` field uses for its internal `min_effective: 300` value (`magnesium.yaml` line 55, 61) — meaning the engine's own 300 mg number is, at the source, a BP-trial dose, not a validated general "you need this much magnesium to get value from a supplement" threshold. The owner's skepticism is correct and sourced, not just a stylistic preference.

Separately: NIH ODS' RDA for magnesium (verified via WebFetch, NIH ODS Magnesium Health Professional Fact Sheet, `ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/`) is **310–420 mg/day depending on age and sex**, and explicitly **"includes magnesium from all sources — food, beverages, dietary supplements, and medications."** It is a whole-diet reference intake, not a supplement-only target, and it is not derived from an effectiveness trial at all — it is a population nutrient-adequacy estimate. Presenting 310-420 as if it told a reader "how much your supplement should give you" would repeat the same category error the owner flagged for the 300 mg figure, just with a different, more official-sounding number. **This spec explicitly rules that against** — the RDA range must always be labeled "all sources combined," never rendered as a supplement-dose target.

### Replacement principle for copy

No single number is presented as *the* line between "meaningful" and "symbolic." Instead, each product's disclosed elemental dose is placed in **two honest, clearly-labeled comparative contexts**, neither implying a validated floor:

1. **Relative to the 18 reviewed products' own disclosed range.** Determinate doses (15 of 18 products; #16–18 are unresolved) run 76–520 mg, median 190 mg. State each product's dose as "X mg — [above/at/below] the middle of the range Bari found on this shelf (76–520 mg across 18 products)." This is a factual, corpus-derived comparison, not an invented standard.
2. **Relative to the RDA-all-sources context band, explicitly labeled as such.** "NIH's general daily reference intake for magnesium from every source combined — food and supplements together — is roughly 310–420 mg/day depending on age and sex. A supplement is normally only part of that total; how much of it a reader still needs from a supplement depends on their diet, which Bari cannot know." This band must never be rendered as "your supplement should give you 310-420 mg."

Both statements are descriptive, not evaluative — no "passes/fails the bar" language rides on top of them. The evaluative content (safety-note crossing, form-tier, label-clarity) lives entirely in §2's grouping, not in the dose number itself.

### Gauge geometry — replacing the "300 (הסף)" tick

The current `MAGNESIUM_DOSE_GAUGE` (lines 96–106 of the file) encodes the killed universal floor directly into its zone geometry (`{ upTo: 300, tone: "flag", tickLabel: '300 (הסף)' }`, `{ upTo: 150, tone: "fail", tickLabel: '150 (חצי סף)' }`). This geometry must not ship as-is. Recommended reference points for the redesigned dose gauge (a Frontend/Design implementation task, out of this spec's authorship, but the *reference values and their honest labels* are specified here since that is a Nutrition call):

- **Corpus range shading**, not pass/fail zones: mark the reviewed-corpus min (76 mg) and max (520 mg, already clamped-plus per the existing `domainMax` overflow convention) as neutral range boundaries, with the median (190 mg) marked as a plain reference tick (label: "חציון בין 18 המוצרים שנבדקו" / "median among reviewed products" — no tone color).
- **RDA-all-sources context band**, 310–420 mg, rendered as a distinctly-labeled band (not a pass/fail line) with an explicit "מכל המקורות יחד — לא רק תוסף" ("from all sources combined — not supplement-only") qualifier attached wherever it renders, per the replacement principle above.
- **Do not reuse the safety gauge's 250/350 mg pass/flag/fail coloring on the dose gauge.** Those two numbers stay on `MAGNESIUM_SAFETY_GAUGE` (lines 108–119) **unchanged** — 250 mg (EFSA soft GI-tolerance note) and 350 mg (NIH/IOM hard UL) are real, sourced, safety-relevant thresholds and are not what this fix targets. The two gauges already read the same `doseMg` value into two separate `GuideGaugeGeometry` objects (`buildProduct`, lines 181–190) specifically so this decoupling is architecturally already possible — implementation should not need to restructure that split, only redefine `MAGNESIUM_DOSE_GAUGE`'s own zones.

---

## §4 — Serving/UL safety language spec: remove the multi-capsule suggestion

### What must be deleted

- Line 490 (`headlineFinding.body[2]`): *"אצל חלקם ההסתייגות היחידה היא מינון חלקי, שאפשר להשלים פשוט על ידי לקיחת כמות גדולה יותר"* — "for some, the only caveat is partial dose, which can simply be made up by taking a larger amount." **Kill.**
- Line 526 (`recommendationTierCaptions.recommended`): *"אפשר להגיע לטווח הזה על ידי לקיחת כמות יומית גדולה יותר"* — "you can reach this range by taking a larger daily amount." **Kill.** (This entire field is retired anyway under §2's group model, but flagging the specific sentence in case any fragment of it is reused in the new group-(b) description.)

### Why

1. **Co-ingredients scale, and several of these products are not magnesium-only.** Supherb Citrate+B6 (#1) carries a B6 dose alongside the magnesium; Altman Magnesium Balance (#14) carries ashwagandha and valerian. Doubling or tripling the daily capsule count to reach a target elemental-mg number scales those co-ingredients proportionally — an outcome the guide has no evidence base to evaluate and should not casually recommend.
2. **It is off-label use.** The manufacturer's stated daily serving is what the product was formulated, labeled, and (presumably) tested for. Instructing a reader to exceed it is Bari recommending a use the label itself does not authorize.
3. **The math can approach or cross the supplemental UL.** US NIH/IOM UL for supplemental magnesium is 350 mg/day (verified, §7). A reader "topping up" a 168 mg product (#4) by taking roughly double the labeled serving to approach 300+ mg is arithmetically fine against the UL in isolation, but the guide has no way to know what other magnesium sources (other supplements, fortified foods, other UL-relevant medications) that reader is already combining it with — recommending capsule-stacking invites a UL-adjacent decision Bari cannot see the full picture for.

### Replacement principle

Describe the **labelled serving only**. State what the label discloses (elemental mg per stated daily serving, as directed) and stop there. If a reader's dose sits below the comparative range (§3) and they want more, the guide should point to **either** a different product **or** a conversation with a pharmacist/physician — never to "take more capsules than directed." This applies uniformly to every Group (b) product in §2's table; none of their one-line reasons above suggest self-titration, and none should acquire that suggestion in the final copy either.

---

## §5 — Absorption bucket reclassification (3 buckets)

### The three buckets

**Bucket 1 — Better absorbed (NIH ODS names these directly).** Verified (WebFetch, NIH ODS Magnesium Health Professional Fact Sheet): *"magnesium in the aspartate, citrate, lactate, and chloride forms is absorbed more completely and is more bioavailable than magnesium oxide and magnesium sulfate."* Forms: **citrate, aspartate, lactate, chloride.**
Present in the 18-product corpus: **citrate only** (#1, #3 — corrected; #2 is bisglycinate, Bucket 3, see below, not citrate — a typo in an earlier draft of this spec, caught during the §11 revision).

**Bucket 2 — Worse absorbed (NIH ODS names these directly, as the low comparator in the same sentence).** Forms: **oxide, sulfate.**
Present in the corpus: **oxide** (#9 partial/blend, #11, #12, #13, #14, #16). Sulfate does not appear in the current corpus.
**Weaker-sourced addition, flagged not asserted with the same confidence:** the current file also groups **carbonate** into this "cheap, poorly absorbed" bucket (line 615, #17 in this corpus). NIH ODS does not name carbonate in the sentence above. Carbonate's inclusion rests on chemical-class analogy (poorly water-soluble mineral salt, similar to oxide) rather than a direct citation. This spec keeps carbonate in Bucket 2 on that analogy but requires copy to disclose the weaker basis wherever carbonate is discussed at more than a badge-label level (i.e., in the "הצורות הכימיות, מוסבר שוב בקצרה" education-spine section, not necessarily in a one-line product badge).

**Bucket 3 — Evidence too limited for confident ranking.** Everything not named in Bucket 1 or 2. Forms present in the corpus: **bisglycinate/glycinate** (#2, #4, #6, #15), **hydroxide** (#5), **malate** (#7, #8), **taurate** (#10).
Basis: NIH ODS does not name any of these four forms anywhere in the fact sheet (verified directly via WebFetch — "these forms are not mentioned by name in the fact sheet" for bisglycinate specifically; malate/taurate/hydroxide are likewise absent from the cited sentence). The three PMIDs previously used in the live copy to support a bisglycinate-specific absorption claim do not hold up on inspection (already independently verified by Research, `03_operations/reports/research/magnesium_form_ladder_verification_v1.md`, and baked into the rubric's own `evidence_confidence_split`, lines 188-220): one shows no significant plasma response for bisglycinate and carries an undisclosed conflict of interest (2 of 5 authors affiliated with the maker of the study's comparator ingredient); one is a mouse study; one shows a benefit only in 4 of 12 severely malabsorption-impaired patients, not a general population. None of these three PMIDs may be cited to support a bisglycinate-superiority claim (this restriction was already in force in the rubric; this spec does not loosen it).

**Rendering requirement (added by §11 ruling, 2026-07-10):** Bucket 3's `form_absorption` state may not render on the fail/flag/pass ordinal ladder at all — not at "בינונית"/flag (that tier itself asserts a confident middle-of-the-ladder ranking, a claim Bucket 3's own evidence basis does not support) and not at "גבוהה"/pass. See §11 for the full ruling, exact field-level changes, and the confirmed knock-on impact on §2's grouping.

### Kill instruction: the oxide-cost-causation claim

Two instances of an unestablished causal claim must be deleted, not softened:
- Line 615 (`educationSpine`, "הצורות הכימיות, מוסבר שוב בקצרה"): *"הצורה הזו זולה לייצור בדיוק בגלל שהגוף סופג ממנה פחות"* — "this form is cheap to produce precisely because the body absorbs less of it." **Kill** the causal "precisely because" framing.
- Line 627 (`educationSpine`, "הממצא שכדאי לזכור"): *"בדיוק בגלל שהגוף סופג ממנה הכי פחות"* — same causal claim, restated. **Kill.**

Both oxide's low cost and its low fractional absorption are independently true and independently sourced (dossier `forms.rationale`, `elemental_mg_fraction` chemistry). No source in this spec's research pass establishes that manufacturers price oxide low *because* it absorbs poorly, as opposed to the two facts simply co-occurring (oxide is cheap to manufacture as an industrial compound for reasons unrelated to human bioavailability — it is a bulk commodity chemical used far beyond supplements). Replace with a **correlation-only** framing: "אוקסיד הוא גם הזול ביותר לייצור וגם נספג הכי פחות — שני ממצאים נפרדים, לא אחד גורם לשני" (illustrative only — final phrasing is Content's).

---

## §6 — Cramps claim: narrowed scope

### What must change

Four locations currently state or imply an unscoped "magnesium does not help muscle cramps" finding: line 264 (#5's `oneLinerHe`), line 495 (`headlineFinding.body[7]`), line 606 (`educationSpine`, "מה מגנזיום עושה בפועל"), line 636 (`educationSpine`, "מקורות"). All four must be re-scoped to name the population the finding actually applies to.

### Verified finding (WebFetch, PMID:32956536 directly)

Garrison, S.R. et al., *Cochrane Database of Systematic Reviews*, 2020 ("Magnesium for skeletal muscle cramps"):
- **Older adults with ordinary (idiopathic/nocturnal) skeletal muscle cramps:** no statistically significant benefit found versus placebo; the review's own stated conclusion is *"It is unlikely that magnesium supplementation provides clinically meaningful cramp prophylaxis to older adults experiencing skeletal muscle cramps."* Mean participant age 61.6–69.3 years.
- **Pregnancy-associated cramps:** evidence is **conflicting**, not negative — three trials reviewed, one no benefit, one benefit for frequency/intensity, one inconsistent on frequency. The review calls for further research; it does not conclude magnesium doesn't help pregnancy cramps.
- **Exercise-associated or disease-state-associated cramps (e.g. ALS):** **no trials exist at all.** The review states this explicitly as a gap, not a null finding. Absence of evidence here must not be presented as evidence of absence.

### Replacement principle

Every instance of the claim must name **older adults** and **ordinary/idiopathic cramps** as the scope, and must not extend the "no meaningful benefit" conclusion to pregnancy (conflicting, not negative) or exercise/disease-state cramps (no evidence either way, not tested). Illustrative scoping (final Hebrew is Content's): "אצל מבוגרים עם התכווצויות שרירים רגילות (לא בהריון ולא הקשורות לפעילות גופנית), סקירת קוקריין משנת 2020 (Garrison et al., PMID 32956536) לא מצאה תמיכה קלינית משמעותית למגנזיום כתוסף מונע. הראיות לגבי הריון סותרות ולא שליליות; לגבי עוויתות הקשורות לפעילות גופנית, לא בוצעו בכלל מחקרים מבוקרים."

---

## §7 — Verified source list

| Source | URL | What it supports | Verification method |
|---|---|---|---|
| NIH Office of Dietary Supplements, Magnesium — Health Professional Fact Sheet | `https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/` | (1) Citrate/aspartate/lactate/chloride absorbed more completely than oxide/sulfate — §5 Bucket 1/2. (2) Bisglycinate/glycinate not named anywhere in the fact sheet — §5 Bucket 3 basis. (3) UL for supplemental magnesium = 350 mg/day, adults 19+ — §3, §4 (unchanged safety gauge). (4) RDA 310–420 mg/day (age/sex-dependent), explicitly "from all sources — food, beverages, dietary supplements, and medications" — §3 comparative-context band. | **Direct fetch returned HTTP 403** (also independently observed by Research in the standing rubric, line 200-203: "the live ODS page itself returned HTTP 403 to direct fetch"). Content retrieved and quoted via a text-extraction proxy (`r.jina.ai` mirror of the same URL) this task, 2026-07-10. The canonical URL is the one above; the 403-on-direct-fetch limitation is disclosed here rather than silently worked around. A follow-up direct re-fetch (e.g. from a different network context) is recommended before any sentence here ships as a verbatim quote in consumer copy — this is the same caution the rubric already carries for this exact source. |
| Garrison, S.R. et al. — "Magnesium for skeletal muscle cramps," *Cochrane Database of Systematic Reviews* 2020, PMID 32956536 | `https://pubmed.ncbi.nlm.nih.gov/32956536/` | §6 narrowed cramps claim: older-adults/idiopathic-cramps null finding; pregnancy evidence conflicting; exercise/disease-state cramps untested (zero trials). | **Direct WebFetch succeeded** on the PubMed abstract page this task, 2026-07-10. Title, authors, journal, and PMID all confirmed to match. Full-text Cochrane Library page (`cochranelibrary.com`, DOI 10.1002/14651858.CD009402.pub3) was not independently re-fetched this task (PubMed's own abstract carried sufficient detail for every claim used here); recommend the Cochrane DOI as the canonical citation in published copy, with PubMed as the accessible mirror. |
| Zhang, X. et al. — "Effects of Magnesium Supplementation on Blood Pressure: A Meta-Analysis of Randomized Double-Blind Placebo-Controlled Trials," *Hypertension*, Aug 2016, PMID 27402922 | `https://pubmed.ncbi.nlm.nih.gov/27402922/` | §3: the 300 mg/day figure is a blood-pressure-trial finding ("300 mg/d or duration of 1 month is sufficient to elevate serum Mg and reduce BP"), median dose studied 368 mg/day — not a general supplement-effectiveness threshold. This is also the exact citation the SIE dossier's own `min_effective: 300` field already uses (`magnesium.yaml` line 61), confirming the 300 mg number was never sourced as a general-effectiveness floor even internally. | **Direct WebFetch succeeded** on the PubMed abstract page this task, 2026-07-10. |
| EFSA/SCF — "Overview on Tolerable Upper Intake Levels as derived by the Scientific Committee on Food (SCF) and the EFSA Panel on Dietetic Products, Nutrition and Allergies (NDA)," Version 11 (August 2025) | `https://www.efsa.europa.eu/sites/default/files/2024-05/ul-summary-report.pdf` | §3 (safety gauge, unchanged), §4: magnesium UL = 250 mg/day for ages 4+ through adults, pregnancy, and lactation, sourced to SCF (2001b); footnote (g) confirms the 250 mg/day figure applies to "readily dissociable Mg salts... and compounds like MgO in food supplements, water or added to foods" and explicitly **excludes** magnesium naturally present in food. | **Direct WebFetch succeeded** and the file was read in full via the Read tool (PDF, all 8 pages) this task, 2026-07-10. This is an EFSA-published, currently-maintained (Aug 2025) summary document, not the original 2001 SCF opinion PDF itself — the original SCF (2001b) opinion PDF and the 2015 EFSA NDA Panel DRV opinion (`doi.org/10.2903/j.efsa.2015.4186`) were both attempted and blocked (`efsa.europa.eu/sites/default/files/consultation/150511.pdf` not attempted directly; the Wiley-hosted 2015 opinion returned HTTP 402/a CAPTCHA wall on two fetch attempts). This EFSA summary document is treated as sufficiently primary (it is EFSA's own current, citable restatement of the SCF opinion's numeric output, with the source opinion cited) — flagged rather than silently treated as equivalent to the original opinion text. |

**Explicitly not verified / not used:** the phrase "verified through reliable secondary quotations" appears nowhere in this document by design — every numeric or scoped claim above traces to a source this task directly fetched and quoted, with the one disclosed exception (NIH ODS direct-fetch blocked, proxy-fetched instead, flagged) and one partial exception (EFSA original 2001/2015 opinions blocked, EFSA's own current summary substituted, flagged). No claim in this spec rests on an un-fetched, un-quoted secondary paraphrase.

---

## §8 — Scope phrasing rules

1. **Certification claims** (third-party verification) must read as a **search result**, not a market fact: "no publicly verifiable certification found among the 18 products reviewed, as of July 2026" — never "no certified magnesium product exists in Israel" or similar unscoped market claims. The existing copy at line 512 and 582 already mostly follows this pattern ("אף מותג מגנזיום במדף לא פרסם טענת בדיקה כזו כלל") — keep that scoping, extend the "as of July 2026" temporal qualifier explicitly wherever this claim renders, since a market fact stated without a date silently ages into a false claim.
2. **Market claims generally** must be scoped "among the 18 products reviewed" (or "in this corpus"), never "on the Israeli shelf" or "in Israel" — Bari reviewed 18 specific SKUs, not an exhaustive market census. This applies to every instance of the price-gap and third-party-gap statements, and to the "אף מוצר מגנזיום במדף הישראלי" framing at line 486 and 927 (rubric) — "המדף הישראלי" ("the Israeli shelf") over-claims a market census this guide did not perform. Replace with "מתוך 18 המוצרים שנבדקו" ("of the 18 products reviewed") consistently.

---

## §9 — Concerns (honest-broker notes, not softened into the spec above)

1. **My precedence rule in §2 deliberately departs from the task brief's illustrative ordering.** The brief's example was "insufficient-label trumps all, then form/tolerance, then lower-amount." Applied literally, that ordering would place Tink Oxide-520 (#16) and Amorphicure (#17) — both a **known, determinate bad form** (oxide/carbonate) with only an *ambiguous dose reading* — into "insufficient label information," which reads to a consumer as "we don't know enough to say anything," when in fact Bari does know something important and negative about these two products (the form). This would have quietly reversed the rubric's own already-co-signed `bucket_logic.worked_distinction` (lines 459-466), which exists specifically to keep a known-bad-form product ("fails") visibly distinct from a genuinely-unknowable one ("cannot_assess"). I used a precedence rule that preserves that existing distinction instead. Flagging this because the task said "e.g." for its ordering (illustrative, not literal), but a domain reviewer should confirm this substitution rather than have it pass silently.
2. **RESOLVED by §11 (2026-07-10), was open at first draft.** §5's 3-bucket absorption framing was stricter for bisglycinate than the live bar-STATE badge (which showed bisglycinate at the same PASS/HIGH-tier badge as citrate) — flagged here as an open, unresolved internal-inconsistency risk in the first draft of this spec. Adversarial QA gate-2 caught the shipped form of exactly this risk (HIGH-1) before go-live. §11 rules the fix: all four Bucket-3 forms (bisglycinate, hydroxide, malate, taurate) move off the fail/flag/pass ladder into a distinct, non-ordinal "evidence too limited" rendering. This is exactly the D6/D7 badge-level review this note originally said was needed — it is no longer deferred.
3. **Carbonate's placement in Bucket 2 rests on weaker evidence than oxide/sulfate's.** NIH ODS names oxide and sulfate directly; carbonate is grouped in by chemical-class analogy in the pre-existing copy, not by direct citation. I kept it there (§5) because the analogy is scientifically reasonable and no source contradicts it, but this is a Weak-tier inference sitting inside a claim otherwise built on a Moderate-tier, directly-quoted source, and the two should not be presented with identical confidence.
4. **The SIE dossier's entire `effective_dose` block (magnesium.yaml lines 53-62) is blood-pressure-outcome-derived**, not derived from a general magnesium-supplementation-effectiveness review. This spec fixes how that number is *presented* to consumers (§3), but the underlying dossier field itself being BP-specific while feeding a generic "dose adequacy" bar used regardless of why a given reader is taking magnesium (sleep, general deficiency, muscle) is a modeling question larger than this guide's copy — worth a future dossier-level NEEDS-ENV-VERIFY review, not something I am resolving here.
5. **I did not find a documented owner-facing science problem with fixes #1, #4, #6, #7, or #8** — these are all corrections toward more accurate, better-scoped claims with no countervailing scientific concern I could find. Fix #3 (kill the universal floor) is, if anything, under-stated by the owner's framing — the 300 mg number isn't just "lacking solid support," it is actively sourced (by Bari's own dossier) to a BP-specific trial, which is a stronger indictment than "no solid support for a universal threshold" alone would suggest, and I've made that the lead argument in §3 rather than a footnote.

---

## §10 — Governance note

Per the standing rubric (`supplement_guides_bar_rubric_v1.yaml`), any rule that changes what governs bucket/tier assignment or bar-state semantics needs Product Agent D7 co-sign alongside Nutrition (D6/D7 dual-key, Hard Rule 8 project-wide). §2 (grouping precedence), §3 (dose-presentation change), and §5 (absorption bucket reclassification) are exactly that kind of rule and are proposed here as **Nutrition D6**, pending Product D7 co-sign, before Content authors final copy from them. §1, §4, §6, §7, §8 are claim-accuracy and sourcing corrections that do not change scoring-presentation logic and can be treated as standing Nutrition guidance without a separate D7 gate — though nothing here ships to consumers without the standard two-gate (Content + Adversarial QA) sign-off regardless.

---

## §11 — QA Gate-2 Ruling (HIGH-1 / MEDIUM-1), 2026-07-10

**Trigger.** Adversarial QA (gate-2) returned NO-GO on the drafted magnesium guide v2. HIGH-1: bisglycinate rows (#2, #4, #6, #15) render `formAbsorption` = PASS ("גבוהה") while the drafted prose next to them (from §5) says bisglycinate's absorption evidence is too limited to rank confidently against citrate — the same row asserts both. This is the shipped form of the risk already flagged, unresolved, in §9 concern 2 of the first draft of this spec.

### Ruling (Nutrition D6): option (b)

**Chosen: (b) — introduce a distinct, off-ladder rendering for ALL Bucket-3 forms** (bisglycinate, hydroxide, malate, taurate), not just bisglycinate.

**Why not (a).** Moving bisglycinate alone down to match hydroxide/malate/taurate's *current* FLAG/"בינונית" state only fixes the four-forms-split-across-two-tiers inconsistency QA named explicitly. It does not fix the deeper, same-shape error one inference-step behind it: FLAG/"בינונית" itself is defined by the standing rubric as **"MODERATE tier"** — a confident, ranked, middle-of-the-ladder absorption claim — for exactly the four forms §5 says the evidence is "too limited to rank with confidence" at all. "Too limited to rank" and "confidently ranked in the middle" are different claims. Shipping (a) resolves today's QA finding by creating tomorrow's — the single best option available fixes both at once rather than trading one contradiction for a smaller one.

**Why not (c).** Agreed with QA: a visible, same-row contradiction between a badge and its own adjacent prose is not resolvable by adding more prose next to it. Not viable.

### Exact field-level changes (for Product D7 to rule on mechanically)

File: `bari-web/src/lib/guides/magnesium-guide-data.ts`. The `formAbsorption` element (2nd position) of the `states` tuple changes from its current value to a **new, non-ordinal state** — call it `evidence_limited` for this ruling; the literal `GuideBarState` enum name and its rendering path are a Frontend/Product implementation decision, not a Nutrition one, but the **behavioral requirement is exact**: it must render off the fail/flag/pass tone ladder entirely (the same non-ordinal treatment `cannot_verify` already receives elsewhere in this file for `thirdPartyVerification`/`priceFairness`), and its label text must **not** be the generic "לא ניתן לאימות" ("cannot be verified") — that phrase asserts missing data, and the form itself is not missing here (it is disclosed and known); only the ranking confidence is limited. Recommend a distinct label along the lines of "[form name] — ראיות מוגבלות לדירוג מול ציטראט" (illustrative; final Hebrew is Content's), reusing the existing `formHe` field to carry the form name as it already does today.

Rows requiring the change (8 of 18 — every Bucket-3-form row):

| Row | Product | Barcode | Current `formAbsorption` | New `formAbsorption` |
|---|---|---|---|---|
| #2 | Altman Bisglycinate | 7290019444480 | `pass` | `evidence_limited` |
| #4 | Nutricare WELL | 7290018439043 | `pass` | `evidence_limited` |
| #5 | NT L.C. Anti Leg Cramps | 7290010207640 | `flag` | `evidence_limited` |
| #6 | Full-Mag Hadas | 7290001943700 | `pass` | `evidence_limited` |
| #7 | Tink Malate | 7290015318532 | `flag` | `evidence_limited` |
| #8 | Nutricare Malate | 7290001066973 | `flag` | `evidence_limited` |
| #10 | Nutricare Taurate | 7290018439579 | `flag` | `evidence_limited` |
| #15 | Nutricare Nano Liposomal | 7290001065594 | `pass` | `evidence_limited` |

**Unchanged:** #1, #3 (citrate, Bucket 1, stay `pass`) — the badge now honestly means "confidently well-absorbed," a claim only citrate in this corpus can support. #9, #18 (undisclosed blends) stay `cannot_verify` — a genuinely different reason (form itself unknown) from `evidence_limited` (form known, ranking-confidence limited); these two states must not be merged into one code path or label, or QA will have grounds to raise the same class of finding again for a different pair of rows. #11–14, #16, #17 (oxide/carbonate, Bucket 2) stay `fail` — a determinate, NIH-sourced concern, unaffected by this ruling.

### Knock-on impact on §2 grouping — CONFIRMED IMPACT, not "no impact"

The coordinator's working assumption ("bisglycinate leaving the top tier doesn't change §2 grouping") is **correct for #2/#4/#6/#15 only** and **incorrect for #5/#7/#8/#10**. Verified by re-running the §2 precedence rule with `evidence_limited` treated as scientifically neutral for grouping purposes (it asserts no determinate negative finding about the product, so it cannot fire Tier 1 — see rationale below):

- **#2, #4, #6, #15 (bisglycinate): no group change.** #2 stays Group (c) — driven by its independent `safety` = FLAG (250 mg GI-tolerance note), not by form. #4, #6, #15 stay Group (b) — they were already there via `dose_adequacy` alone; form was never their trigger (it was PASS, which never fired Tier 1 either).
- **#5, #7, #8, #10 (hydroxide/malate/taurate): MOVE from Group (c) to Group (b).** These four were in Group (c) **solely** because `form_absorption` = FLAG fired Tier 1. Once FLAG is retired in favor of the neutral `evidence_limited` state, Tier 1 no longer fires for any of them, and each falls through to Tier 2 on its own independently-determinate `dose_adequacy` state (FLAG for #5, FAIL for #7/#8/#10) → **Group (b) Lower elemental amount.**

**Why `evidence_limited` is treated as neutral, not as a Tier-1 trigger, for §2 purposes:** §2's Tier 1 is defined for "known, determinate concern[s] about the compound" (§2 rationale, unchanged) — a FLAG/FAIL form or safety state that makes an affirmative claim about the product. "Evidence too limited to rank with confidence" makes no affirmative claim about the product at all; it is a statement about the state of the literature, symmetric with — not more negative than — a citrate/Bucket-1 "confidently good" claim's absence. Treating it as a Tier-1 concern would smuggle back in exactly the confident-middle-ranking claim this ruling just removed from the badge. It is also not routed to Tier 3 (data gap) group (d), since the label and the form ARE both fully known here — only the scientific ranking is unresolved, a different kind of gap than an undisclosed blend or an ambiguous label reading.

**Updated group distribution:** (a) 0/18, **(b) 9/18** (#3, #4, #5, #6, #7, #8, #9, #10, #15), **(c) 8/18** (#1, #2, #11, #12, #13, #14, #16, #17), (d) 1/18 (#18). Full table and "why (a) is empty" rationale updated in §2 above to match.

### MEDIUM-1: headline formulation guidance

The drafted line *"כל מוצר בצורה כימית מומלצת יותר, כמו ציטראט או ביסגליצינט, נשאר מתחת ל-250 מ"ג"* (paraphrased: "every product in a more-recommended chemical form, like citrate or bisglycinate, stays under 250 mg") incorrectly attributes "more-recommended" to bisglycinate, which is exactly the Bucket-1/Bucket-3 line this entire ruling exists to hold. **Factually-exact replacement guidance:**

- The market-structure claim survives **stated on citrate alone**: "שני המוצרים היחידים בצורה עם עדות מבוססת לספיגה טובה יותר (ציטראט) לא עוברים 250 מ"ג" ("the only two products in a form with an established evidence basis for better absorption — citrate — don't exceed 250 mg") — illustrative Hebrew, Content's to finalize, but the **factual content is exact**: 2 products, citrate, both ≤250 mg (#1 at 250 mg, #3 at 200 mg), Bucket-1 basis per §5.
- Bisglycinate may still be mentioned in the same breath **descriptively, without the "recommended" attribution**: e.g., as a separate clause noting the four bisglycinate products in this corpus also range 88–250 mg, with no evaluative word attached to "bisglycinate" itself. It must not share a "מומלצת" (recommended) or equivalent adjective with citrate in the same clause.
- This same correction applies anywhere else in drafted copy that pairs citrate and bisglycinate under one evaluative label (Content should grep the current draft for "ציטראט או ביסגליצינט" and similar constructions and check each instance against this rule, not just the one line QA cited).

### Status

This ruling is **Nutrition D6**, submitted for **Product D7 co-sign** per the standing rubric dual-key requirement (§10). Field-level changes above are stated precisely enough for Product to rule mechanically without a further Nutrition round-trip, pending confirmation that the `evidence_limited` enum addition (or equivalent) is an acceptable Frontend implementation cost.
