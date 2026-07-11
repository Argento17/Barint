# Magnesium Guide v3 — Structure Spec (Owner Readability Restructure)

**Task:** TASK-577 (Nutrition Agent)
**Governs:** Facts + grouping-mapping layer feeding the v3 rebuild of
`bari-web/src/lib/guides/magnesium-guide-data.ts`. This document is a **FACTS/MAPPING
spec only** — no consumer Hebrew copy is authored here. Content Agent authors final
copy against this spec; both Content and Adversarial QA/Red-Team sign off before
anything ships (standing two-gate rule).
**Status:** Nutrition **D6** proposal — regroups displayed assessment (which of the 4
owner-dictated headings each product renders under). Requires Product Agent **D7**
co-sign before the group reassignment or gauge/section consolidation described here
ships as live copy, per the standing dual-key rule (`supplement_guides_bar_rubric_v1.yaml`,
carried forward from `mag_guide_v2_nutrition_spec.md` §10).
**Inputs read in full:**
`C:\Bari\02_products\supplements\magnesium\mag_guide_v2_nutrition_spec.md` (v2 spec — factual
source of truth for doses/forms/states/evidence tiers, unchanged by this document),
`C:\bari_wt_576\bari-web\src\lib\guides\magnesium-guide-data.ts` (live v2 data as shipped),
`C:\Bari\02_products\supplements\magnesium\mag_guide_v2_copy_package.md` (grepped for
serving-count language; referenced in §B).

**What this spec changes vs. v2:** PRESENTATION and GROUPING only. No new data, no
re-scoring, no new evidence tiers. Every dose, form, safety state, and label state below
is the same fact already in the v2 spec / live TS file — this document re-sorts those
facts into the owner's four dictated headings and specifies what must survive the prose
cuts.

---

## §A — Deterministic assignment rule

### A.1 — The four owner headings (dictated verbatim, this order)

1. **"ציטראט או ביסגליצינט עם תווית ברורה"** (citrate or bisglycinate with a clear label)
2. **"כמות נמוכה יחסית"** (relatively low amount)
3. **"מבוססי אוקסיד"** (oxide-based)
4. **"לא ניתן להבין מהתווית"** (cannot be understood from the label)

These are **form/label-based, not mutually exclusive** as literally written — several
products satisfy more than one heading's literal text at once (e.g. a citrate product at
a low dose satisfies both heading 1 and heading 2's text). Since the deliverable is a
**single group per product** (one section a product renders under), an explicit
precedence order is required to resolve every overlap deterministically. That order is
defined once here and applied uniformly — it is not re-derived per product.

### A.2 — Precedence order (first match wins, top to bottom)

Uses only each product's already-computed v2 bar states (`dose`, `form_absorption`,
`safety`, `label_transparency` — unchanged, this spec does not touch bar-state
computation) and `doseMg`/`formHe`.

**Tier 1 — Known poor-absorption form (Bucket 2: oxide, or carbonate by the
already-flagged chemical-class analogy).** `form_absorption` state = `fail` (oxide or
carbonate) → **Heading 3, "מבוססי אוקסיד."**
*Rationale:* mirrors v2 §2's already-established, already-co-signed precedence
principle — a known, determinate compound-level finding is checked before a dose or
label-clarity question, because it is a property of the compound the consumer cannot
fix by reading the label more carefully. Ranking oxide/carbonate above the "unclear
label" tier (Tier 2 below) for #16/#17 specifically preserves that same precedent (see
§A.4 deviation note — one of the two oxide-tier products is carbonate, not literally
oxide, which is the one heading-3 deviation).

**Tier 2 — Nothing determinate can be said about the product at all.** `form_absorption`
= `cannot_verify` because the **form itself** is an undisclosed multi-ingredient blend
(not merely an undisclosed ratio within a still-legible total dose — see the #9
distinction in §A.4) **and** dose is unresolved → **Heading 4, "לא ניתן להבין
מהתווית."**
*Rationale:* reserved for the one case where the label discloses literally nothing
usable — not even the total elemental figure. This is a narrower bar than "the label has
some gap" (most rows have at least one gap somewhere); it fires only when no single fact
in the four assessed criteria is knowable.

**Tier 3 — Form is citrate (Bucket 1, NIH-ODS-named as better absorbed) or bisglycinate
(a single, named, disclosed form — evidence_limited ranking per v2 §11, but not an
undisclosed blend) AND the label clearly discloses the elemental mg** (`label_transparency`
= `pass`) → **Heading 1, "ציטראט או ביסגליצינט עם תווית ברורה."**
*Rationale:* this is the heading the owner put first; treating "known, well-labeled form"
as taking precedence over "this product is also on the low end of the dose range" matches
the dictated ordering (heading 1 before heading 2) and does not conflict with Tier 1,
since no oxide product in this corpus is also low-dose (oxide products cluster at
450–520 mg, the top of the range) — the two tiers never compete for the same row in the
current 18-product corpus. Flagged as a forward-looking note, not a current conflict: if
a future low-dose oxide product enters the corpus, this ordering (good-form-first) would
need to be revisited against Tier 1 (known-problem-first), since the two principles point
in opposite directions and this corpus never tests that case.

**Tier 4 — Default/catch-all.** Everything not caught above: a single, named,
non-oxide/non-carbonate form (malate, taurate, hydroxide) with a clear label, or an
undisclosed-ratio blend whose **total** elemental dose is still clearly disclosed on-label
(#9) — in every case landing in the lower part of the reviewed dose range → **Heading 2,
"כמות נמוכה יחסית."**

### A.3 — Full 18/18 table

| # | Product | Elemental Mg (disclosed) | Form | `dose` | `form_absorption` | `safety` | `label_transparency` | → Heading |
|---|---|---|---|---|---|---|---|---|
| 1 | Supherb Citrate+B6 | 250 mg | Citrate | flag | pass (Bucket 1) | flag | pass | **1** |
| 2 | Altman Bisglycinate | 250 mg | Bisglycinate | flag | evidence_limited | flag | pass | **1** |
| 3 | Altman Citrate 120 | 200 mg | Citrate | flag | pass (Bucket 1) | pass | pass | **1** |
| 4 | Nutricare WELL | 168 mg | Bisglycinate | flag | evidence_limited | pass | pass | **1** |
| 5 | NT L.C. Anti Leg Cramps | 190 mg | Hydroxide | flag | evidence_limited | pass | pass | **2** |
| 6 | Full-Mag Hadas | 122 mg | Bisglycinate | fail | evidence_limited | pass | pass | **1** |
| 7 | Tink Malate | 136 mg | Malate | fail | evidence_limited | pass | pass | **2** |
| 8 | Nutricare Malate | ~135 mg | Malate | fail | evidence_limited | pass | flag | **2** |
| 9 | Solgar Ca+Mg+D3 | 100 mg | Blend (oxide+citrate, ratio undisclosed) | fail | cannot_verify | pass | pass | **2** (DEVIATION, §A.4) |
| 10 | Nutricare Taurate | 76 mg | Taurate | fail | evidence_limited | pass | pass | **2** |
| 11 | Nutricare Oxide-520 | 520 mg | Oxide | pass | fail (Bucket 2) | fail | pass | **3** |
| 12 | Altman Oxide-520 | 520 mg | Oxide | pass | fail (Bucket 2) | fail | pass | **3** |
| 13 | Altman Magnesium UP | 450 mg | Oxide | pass | fail (Bucket 2) | fail | pass | **3** |
| 14 | Altman Magnesium Balance | 450 mg | Oxide | pass | fail (Bucket 2) | fail | pass | **3** |
| 15 | Nutricare Nano Liposomal | 88 mg | Bisglycinate (base) | fail | evidence_limited | pass | pass | **1** |
| 16 | Tink Oxide-520 (90 caps) | Ambiguous | Oxide | cannot_verify | fail (Bucket 2) | cannot_verify | cannot_verify | **3** |
| 17 | Amorphicure pH Magnesium | Ambiguous | Carbonate | cannot_verify | fail (Bucket 2, weaker basis) | cannot_verify | cannot_verify | **3** (DEVIATION, §A.4) |
| 18 | TRIOMAG | Unresolved | Undisclosed 3-form blend | cannot_verify | cannot_verify | cannot_verify | cannot_verify | **4** |

**Distribution: Heading 1 = 6/18 (#1,2,3,4,6,15); Heading 2 = 5/18 (#5,7,8,9,10); Heading
3 = 6/18 (#11,12,13,14,16,17); Heading 4 = 1/18 (#18). Sum check: 6+5+6+1 = 18. ✓**

### A.4 — DEVIATION-FROM-OWNER-TEXT flags (each on its own line, for orchestrator surfacing)

**DEVIATION 1 — Heading 2's literal text is form-agnostic; malate/taurate/hydroxide
products only fit it if that is read as intentional.** Heading 2's dictated text
("כמות נמוכה יחסית" / relatively low amount) never mentions chemical form — unlike
headings 1 and 3, which do. Read literally in isolation, heading 2 already covers
malate/taurate/hydroxide products (#5, #7, #8, #10) with no adjustment needed. The
deviation is flagging that this reading must be **confirmed as the owner's intent**
rather than assumed: an alternate reading, where heading 2 was meant (by parallel
construction with heading 1) to apply only to citrate/bisglycinate products at a low
dose, would leave #5/#7/#8/#10 fitting no heading at all. This spec adopts the
form-agnostic reading (smallest possible adjustment — none, in fact, since it matches
the heading's own literal text) and flags it for confirmation rather than silently
assuming it.

**DEVIATION 2 — Product #9 (Solgar Ca+Mg+D3) placed in Heading 2 despite an undisclosed
form.** #9's total elemental dose (100 mg) IS clearly disclosed on-label
(`label_transparency` = pass on the total) — only the internal oxide/citrate *ratio*
is undisclosed. This does not cleanly match Heading 2 (a single, named form, which #9
lacks) nor Heading 4 (a fully-unknowable product, which #9 is not — the dose that
matters most to a consumer, the elemental total, IS known). Smallest honest adjustment:
place #9 in Heading 2 on the dominant, most consumer-relevant determinate fact (a
disclosed, low elemental dose), carrying the blend-ratio gap as a **mandatory secondary
card fact** (§B), not folded into or hidden by the heading. This mirrors v2's own
established treatment of this exact row (v2 spec §2, row #9: "the group reflects the
dominant, determinate reason").

**DEVIATION 3 — Product #17 (Amorphicure, carbonate) placed under "מבוססי אוקסיד"
(oxide-based) despite not literally being oxide.** Carbonate is grouped with oxide in
v2 §5 (Bucket 2) by chemical-class analogy only — NIH ODS names oxide and sulfate
directly; it does not name carbonate. v2 §5/§9-3 already flag this as a **weaker
evidence basis** than oxide's direct citation. Heading 3's dictated Hebrew text says only
"אוקסיד" (oxide), not "oxide-like forms" or "oxide and carbonate." Smallest honest
adjustment: keep #17 under Heading 3 for display (its poor-absorption finding is real
and belongs with the other Bucket-2 products, not scattered into Heading 2's
"low-amount" framing, since #17's dose is unresolved, not low), but the **heading's
underlying membership definition** — not the owner's displayed Hebrew text, which this
spec does not alter — must be understood internally as "oxide-based (including one
carbonate product grouped by chemical-class analogy, weaker evidence basis)." Content
should decide whether that nuance needs a one-clause card note for #17 (recommended:
yes, since it is a real, already-flagged evidence-strength gap) or stays in a collapsed
disclosure; either is acceptable, but it must not be silently dropped.

**DEVIATION 4 — Product #16 (Tink Oxide-520) has an unresolved dose reading but is
placed under Heading 3, not Heading 4.** #16's `dose_adequacy` and `label_transparency`
are both `cannot_verify` (the on-pack "520" doesn't distinguish elemental vs. compound
weight) — the same ambiguity that sends #18 to Heading 4. #16 is placed in Heading 3
instead because its **form** (oxide) is known and determinate, per the Tier-1-before-Tier-2
precedence (§A.2, mirroring v2 §9 note 1's "known problem checked before data gap, not
the reverse"). This is a precedence-resolution call, not a literal-text mismatch (#16
does say "oxide," so it fits Heading 3's text) — flagged here for visibility since the
dose-ambiguity fact must still surface on #16's card (§B) even though it isn't the
grouping driver.

**No other deviations.** #1–#4, #6, #15 fit Heading 1's literal text exactly (confirmed
citrate/bisglycinate form + confirmed clear label). #11–#14 fit Heading 3's literal text
exactly (confirmed oxide). #18 fits Heading 4's literal text exactly (nothing knowable).

### A.5 — What Heading-1 membership does and does not claim (owner directive, task item 2)

The owner knowingly placed citrate and bisglycinate together under one heading — that
grouping decision is not relitigated here. What this spec requires Content to hold onto
so the copy doesn't overclaim:

**Does claim:**
- The product's chemical form is citrate or bisglycinate — a single, named, disclosed
  form (not an undisclosed blend).
- The label clearly discloses the elemental magnesium amount per stated daily serving —
  no ambiguity about what's being delivered.

**Does NOT claim:**
- That citrate and bisglycinate have equal absorption evidence. Citrate has a direct NIH
  ODS citation (Bucket 1, "absorbed more completely... than magnesium oxide"). Bisglycinate
  does not — NIH ODS never names it, and it carries the `evidence_limited` state (v2 §11,
  a standing D6/D7-ruled fix, not reopened here). Heading-1 copy must never pair citrate
  and bisglycinate under one evaluative adjective (the exact error the §11 MEDIUM-1
  ruling already corrected once in v2; do not reintroduce it in v3's shorter copy).
- That the product is free of the GI-tolerance note. #1 and #2 (both 250 mg) independently
  carry `safety` = FLAG (sitting exactly at EFSA's 250 mg soft-tolerance advisory) — a
  separate fact from form/label that must still appear on those two cards even though it
  isn't why they're grouped here.
- Any claim about dose adequacy in general, or any health outcome / recommendation
  ("best," "most effective," "recommended") — banned under Hard Rule 5 (no health
  claims) regardless of heading.

---

## §B — Per-card visible-4 facts (all 18 products)

**Servings-per-day note (applies to every row below):** neither of this task's two input
files, nor the raw product-identity file
(`bari-web/src/lib/comparisons/magnesium-page-data.ts`), carries a per-product
"X capsules/day" field distinct from the elemental-mg figure. The one serving-related
field present (`servingNote: "לנטילה היומית המומלצת"`) is an identical boilerplate string
repeated on all 18 products ("for the recommended daily intake") — not a parsed capsule
count. Per the missing-data discard rule, this field is **NULL for all 18 products** in
this spec. If the owner's card format requires an actual capsule count (e.g., "2 capsules
daily"), that would need a fresh scrape/parse pass on the raw label text — flagging for
Data Agent, not inventing a number here.

| # | Product | Elemental Mg/serving | Form (He) | Servings/day | Factual basis for "מה חשוב לדעת" |
|---|---|---|---|---|---|
| 1 | Supherb Citrate+B6 | 250 mg | ציטראט | NULL | Citrate — only form in corpus with direct NIH ODS support for more complete absorption vs. oxide. Label clearly discloses 250 mg elemental. Carries a GI-tolerance note: 250 mg sits exactly at EFSA's 250 mg soft-tolerance advisory threshold (not a UL breach — a comfort note). |
| 2 | Altman Bisglycinate | 250 mg | ביסגליצינט | NULL | Bisglycinate — a known, disclosed form, but NIH ODS never names it; ranking its absorption confidently against citrate is evidence-limited (§11 state). Label clean, 250 mg elemental. Same GI-tolerance note as #1 (250 mg = EFSA's 250 mg threshold). |
| 3 | Altman Citrate 120 | 200 mg | ציטראט | NULL | Citrate, same Bucket-1 NIH ODS support as #1. Label and safety both clean at 200 mg — no tolerance note. Sits just above the reviewed-corpus median (190 mg among 15 products with a clear elemental reading). |
| 4 | Nutricare WELL | 168 mg | ביסגליצינט | NULL | Bisglycinate, evidence-limited absorption ranking (known form, not NIH-ODS-named). Label and safety clean. 168 mg sits below the corpus median (190 mg), lower-middle of the reviewed range. |
| 5 | NT L.C. Anti Leg Cramps | 190 mg | הידרוקסיד | NULL | Hydroxide, evidence-limited absorption ranking. Label and safety clean. Dose sits exactly at the corpus median (190 mg). Product name references leg cramps: the directly relevant evidence (Cochrane 2020, PMID 32956536) found no significant benefit specifically for **older adults** with **ordinary (non-pregnancy, non-exercise)** cramps — a narrowly scoped finding, not a general verdict on magnesium and cramps generally. |
| 6 | Full-Mag Hadas | 122 mg | ביסגליצינט | NULL | Bisglycinate, evidence-limited absorption ranking. Label is in fact a strong point here: correctly does not conflate the "600" in the product name (capsule count in the package) with a magnesium-mg figure. Dose is 122 mg, bottom quartile of the reviewed range (76–520 mg). |
| 7 | Tink Malate | 136 mg | מלאט | NULL | Malate, evidence-limited absorption ranking (not NIH-ODS-named). Label and safety clean. 136 mg is in the lower part of the reviewed range. |
| 8 | Nutricare Malate | ~135 mg | מלאט | NULL | Malate, evidence-limited absorption ranking. Label carries a real, separate gap: the package states only the 700 mg malate compound weight, not an elemental conversion — Bari derived the ~135 mg elemental figure; it is not printed on-pack. Dose is in the lower part of the reviewed range. |
| 9 | Solgar Ca+Mg+D3 | 100 mg | תערובת (אוקסיד + ציטראט, יחס לא מפורסם) | NULL | 100 mg elemental IS clearly disclosed on-label. Form is a blend of oxide and citrate in an undisclosed ratio, so this specific blend's absorption cannot be ranked separately (mandatory secondary fact — see DEVIATION 2, §A.4). 100 mg is in the lower part of the reviewed range. Product also carries calcium and vitamin D3, not evaluated here. |
| 10 | Nutricare Taurate | 76 mg | טאוראט | NULL | Taurate, evidence-limited absorption ranking. Label and safety clean. 76 mg is the lowest disclosed elemental dose among the 18 products reviewed. |
| 11 | Nutricare Oxide-520 | 520 mg | אוקסיד | NULL | Oxide — NIH ODS names this form directly as less completely absorbed than citrate/aspartate/lactate/chloride. At 520 mg, also crosses the 350 mg/day supplemental UL (NIH/IOM) — a separate, additive safety fact, not caused by the form itself. Both figures are clearly disclosed on-label. |
| 12 | Altman Oxide-520 | 520 mg | אוקסיד | NULL | Identical profile to #11 (same form, same dose, same two findings). |
| 13 | Altman Magnesium UP | 450 mg | אוקסיד | NULL | Oxide, same NIH ODS lower-absorption finding as #11/#12. At 450 mg, still crosses the 350 mg/day UL, by a smaller margin than the 520 mg products. |
| 14 | Altman Magnesium Balance | 450 mg | אוקסיד | NULL | Oxide, same profile as #13 (450 mg, crosses 350 mg UL). Also lists ashwagandha and valerian on-label — not part of the magnesium-specific facts here. |
| 15 | Nutricare Nano Liposomal | 88 mg | ביסגליצינט (צורת בסיס) | NULL | Bisglycinate (stated base form), evidence-limited absorption ranking. Label and safety clean. 88 mg is the second-lowest disclosed dose among 15 products with a clear elemental reading. "Nano liposomal" is a separate marketing claim — no evidence found in sources reviewed to confirm or deny an absorption benefit beyond the base bisglycinate form. |
| 16 | Tink Oxide-520 (90 caps) | Ambiguous / not verifiable | אוקסיד | NULL | Oxide — NIH ODS names this form as less completely absorbed, a fact independent of the dose reading. Separately, and must be named too: the label states "520" without clarifying whether that's the elemental figure or the compound weight, so the actual elemental dose cannot be verified from the label. |
| 17 | Amorphicure pH Magnesium | Ambiguous / not verifiable | קרבונט | NULL | Carbonate — grouped with oxide as a poorly-absorbed mineral salt by chemical-class analogy only (weaker evidence basis than oxide's direct NIH ODS citation — no direct NIH ODS statement names carbonate; see DEVIATION 3, §A.4). Separately: the label states no daily elemental magnesium figure at all, an independent gap on top of the form finding. |
| 18 | TRIOMAG | Unresolved | תערובת בלתי מפורשת (ציטראט/ביסגליצינט/טאוראט) | NULL | The only product among the 18 where nothing determinate can be stated: the label names three forms in an undisclosed ratio, so neither the elemental dose per serving nor a form-specific absorption ranking can be determined from the label. |

---

## §C — Findings-box facts ("מה גילינו," 4 findings)

| # | Owner's finding | Supported? | Supporting numbers | Wording hazard |
|---|---|---|---|---|
| 1 | Big printed number ≠ actual elemental amount | Yes, but **scoped to specific instances**, not a corpus-wide pattern | 2/18 products carry an explicit, on-pack numeral that is not the elemental mg figure: #6 (Full-Mag Hadas — "600" is the capsule count in the package) and #8 (Nutricare Malate — "700 mg" is the malate compound weight, elemental ~135 mg derived by Bari, not printed). A third case is a milder version of the same pattern: #9's headline "100 mg" IS the elemental figure (correctly labeled), but the product also states a combined-blend weight elsewhere on-pack. | Must not generalize to "products mislead" or "many products hide the real number" — only 2/18 have a genuinely different large number on the front; phrase as a reading tip ("look for the elemental mg figure specifically"), not an accusation against the category. |
| 2 | Citrate = clearest support among reviewed | Yes | Citrate is the only Bucket-1 form (NIH ODS-named as more completely absorbed than oxide/sulfate) present in this 18-product corpus — 2/18 products (#1, #3). No other form in the corpus (bisglycinate, malate, taurate, hydroxide, oxide, carbonate) has a comparably direct citation. | Must not say "best magnesium" or "recommended" — no health claims, no product recommendation (Hard Rule 5). Phrase as "the form with the most direct sourced evidence among those reviewed," not a superlative. Must also not re-pair this finding with bisglycinate under one adjective (the exact error the standing §11 MEDIUM-1 ruling already corrected — do not reopen it in v3 copy). |
| 3 | Many products are oxide-based | Yes, with a **precise, not vague, count needed** | 6/18 are Bucket-2 form-`fail` products (#11, #12, #13, #14, #16 — literally oxide; #17 — carbonate, grouped by chemical-class analogy, weaker basis per DEVIATION 3). Of those, 4/18 (#11–#14) also disclose a dose that crosses the 350 mg/day UL — a separate, additive finding. | The findings box gives exact numbers elsewhere (76 mg, 520 mg, 190 mg) — "many" here should likewise be "6 of the 18" or "a third," not left vague. Must scope "among the 18 products reviewed" (v2 §8 rule), never "on the Israeli shelf." Must not imply oxide itself is unsafe outside the disclosed UL-crossing cases — describe as "a form NIH ODS identifies as less completely absorbed," not "harmful" or "dangerous." |
| 4 | Some labels are unclear | Yes, with a **precise count** | 4/18 have a `label_transparency` state other than `pass`: #8 (flag — compound mass only, no elemental conversion on-pack), #16, #17, #18 (all `cannot_verify`). | Give the exact count (4/18), not "some." Must not imply intentional deception — these are disclosure gaps, not accusations of motive. Scope to "among the 18 products reviewed." |

---

## §D — Deletion audit

Owner-dictated deletions, mapped against the current live TS source
(`magnesium-guide-data.ts`, read in full for this task):

| Dictated deletion | Best-matching live field(s) | Mapping confidence | Load-bearing facts inside it | Where they must land |
|---|---|---|---|---|
| "'אף מוצר...' prose block + five product summaries" | `headlineFinding` (title + 3-paragraph body — contains "אף אחד מ-18 המוצרים... לא משלב...") | **PARTIAL / FLAGGED.** No 5-paragraph per-product summary block exists in the current source — v2 already removed that structure (TS header comment: "product detail now lives only in each product's own oneLinerHe, never duplicated" in headlineFinding). The 3-paragraph `headlineFinding` is the closest match to the "אף מוצר" prose the owner is describing. The "five product summaries" phrase does not map to anything in this source as read. **Recommend the orchestrator confirm against the rendered page** (not just source) before deletion — possible the owner is describing content that already differs from what shipped, or conflating this page with another guide. | The market-structure finding itself (no product combines top-of-range dose + citrate/aspartate-tier form + clean safety/label) — this is the guide's actual headline finding, not filler. Also: the §11 MEDIUM-1 citrate-vs-bisglycinate non-pairing correction currently lives in this same block (`body[0]`: "שני המוצרים היחידים בצורה עם עדות מבוססת... נשארים מתחת ל-250 מ"ג" / bisglycinate named separately without a shared adjective). | The market-structure finding: shortened to 1-2 sentences in the new intro/hero area. The citrate-vs-bisglycinate non-pairing correction: must survive verbatim in spirit wherever citrate and bisglycinate are next discussed together (most likely inside Heading 1's group caption, since that's the section where the two forms now sit side by side — see §A.5). |
| "the repeated chemical-forms explainer" | `educationSpine[2]` ("צורה כימית וספיגה: שלוש קבוצות ראיות במקום סולם אחד") vs. the per-row `EVIDENCE_LIMITED_FORM_NOTE_HE` (8 rows) vs. each product's own `oneLinerHe` re-deriving the same bucket logic | **HIGH** — this is a real, 3-way repetition (standalone explainer + identical per-row note + per-product re-derivation in prose). v2's own header comment already claims one round of consolidation ("11 sections → 5") but the redundancy persists across these three surfaces. | The 3-bucket framework itself (citrate/aspartate/lactate/chloride better-absorbed; oxide/sulfate worse-absorbed; bisglycinate/hydroxide/malate/taurate evidence-limited), the NIH ODS citation, and the carbonate weaker-basis flag. | Recommend ONE canonical location for the full derivation — either the collapsed/secondary evidence section or a "לפרטים" disclosure — with per-card facts (§B) staying terse (form name + evidence-tier fact only, no re-derivation of *why*). Content's call on which single location; the requirement here is exactly one, not zero. |
| "the second dose-safety section" | `educationSpine[1]` ("המינון בהקשר...") and `educationSpine[3]` ("בטיחות: מתי מינון גבוה עלול להפריע...") | **HIGH** — these are the only two dose/safety-adjacent sections in the current source; TS comments confirm a *prior* round of de-duplication already happened once ("removes the live duplication between 'בטיחות' and 'מינון ובטיחות'") — the owner is asking for a second pass. | Corpus dose range (76–520 mg, median 190 mg among 15 determinate readings), the RDA-all-sources band (310–420 mg, mandatory "מכל המקורות יחד" qualifier), the 350 mg NIH/IOM UL, the 250 mg EFSA soft-tolerance note, and the no-capsule-stacking instruction (v2 §4 — never suggest exceeding the labeled serving). | Merge into one "dose & safety" section carrying every fact above. None may be dropped in the merge — this section is where the guide's only safety-relevant content lives. |
| "one of two third-party-testing explainers" | `buyingRuleIntro` (mentions price + third-party once, briefly) and `suppressedBarsDisclosureHe` (restates both in full, with the "as of July 2026" date qualifier) | **MODERATE** — likely refers to this same pair of facts (price, third-party) being stated in full twice across these two fields, not two literally distinct third-party-only sections (the standalone third-party education-spine section was already removed in v2, per TS header comment). | Zero publicly-verifiable third-party certification found among the 18 products, **dated** "as of July 2026" (v2 §8 phrasing rule — a market fact stated without a date silently ages into a false claim). | Keep the full, dated statement in exactly one place — recommend `suppressedBarsDisclosureHe` (the guide-level market-gaps box), since it already carries the required date qualifier and the correct price-vs-third-party distinction (v2 §1: these are two different *kinds* of gap, must not be conflated). Trim `buyingRuleIntro` to a bare one-clause pointer, not a restatement. |
| "one of two price explainers" | Same two fields as above | **MODERATE**, same reasoning | Price = a Bari data-collection gap (zero price data collected for magnesium), explicitly **not** a product-quality fact — this distinction is the entire point of v2 §1's kill instruction (the old copy wrongly implied price/third-party gaps explained why no product reached a top tier). | Same as above — one location, keep the price-is-a-Bari-gap-not-a-product-fact distinction intact wherever it lands. |
| "'הממצא שכדאי לזכור'" | *Not found in current source.* | **ALREADY SATISFIED / STALE REFERENCE.** This exact heading does not appear anywhere in the live TS file — v2's own §5 (kill instruction, line 627 of the pre-v2 file) already removed content under this heading name, and v2's education-spine consolidation ("11 sections → 5 content + 1 sources") does not include a section by this title. No action needed unless the owner is looking at a cached/stale render — flagging for the orchestrator to confirm, not treating as a live deletion target. | N/A (nothing found to preserve) | N/A |

### Minimal set of facts that MUST survive somewhere (cross-reference, all sourced above)

1. **350 mg/day supplemental UL** (NIH/IOM) — safety-critical; survives in the merged dose &
   safety section and in the (unchanged) safety-gauge geometry.
2. **250 mg/day EFSA soft GI-tolerance note** — survives alongside #1.
3. **No-capsule-stacking instruction** (v2 §4) — must survive as the closing instruction of
   the merged dose & safety section; never re-derive a "take more" suggestion anywhere else.
4. **RDA-all-sources framing** (310–420 mg, mandatory "מכל המקורות יחד — לא רק תוסף"
   qualifier) — survives in gauge geometry (unchanged) and merged-section prose; never
   rendered as a supplement-only target (v2 §3).
5. **`evidence_limited` meaning** (known form, ranking-confidence limited — not a data gap,
   not equal to citrate) — survives per-product (§B basis column) and in Heading 1's group
   caption (§A.5).
6. **Market-gaps disclosure** (price = Bari collection gap; third-party = zero certification
   found among 18, dated July 2026) — survives in exactly one place, recommended
   `suppressedBarsDisclosureHe`.
7. **Cramps claim scoping** (older adults, non-pregnancy, non-exercise; PMID 32956536) —
   survives wherever cramps are mentioned (#5's card, and the education-spine section on
   what magnesium does) — this is a previously-corrected claim (v2 §6) and must not be
   re-generalized during the prose trim.
8. **Sources list** (NIH ODS, Cochrane PMID 32956536, EFSA UL summary, with URLs) — survives
   unchanged in a sources section/disclosure.
9. **Compound-mass-vs-elemental-mg corrections for #6 and #8 specifically** — survive at
   minimum in those two products' own card facts even if the general explainer is trimmed
   (§C finding 1).
10. **Citrate-vs-bisglycinate non-pairing rule** (§11 MEDIUM-1 ruling — never share an
    evaluative adjective) — survives wherever citrate and bisglycinate are discussed
    together, now most likely Heading 1's group caption (§A.5).

---

## Nutrition D6 sign-off

This spec is submitted as **Nutrition D6** — regrouping of displayed assessment (which
heading each of the 18 products renders under) and consolidation guidance for the
education/disclosure sections. No underlying dose, form, safety, or label fact changes;
no bar-state computation changes; no new evidence tier. Four deviation flags (§A.4) and
one stale-reference note (§D, "הממצא שכדאי לזכור") require orchestrator attention before
Content authors from this spec. Pending **Product Agent D7 co-sign**, dispatched
separately by the orchestrator, per the standing dual-key rule.

---

## Product D7 co-sign — TASK-577 (2026-07-10)

**Method.** Independently re-derived all 18 group assignments from the §A.2 precedence
rule applied to the v2-spec bar states (not trusted from the §A.3 table) — see working
verification below. Recomputed §C's four support counts directly from the §A.3 state
columns. Read `mag_guide_v2_nutrition_spec.md` in full as the underlying-facts source of
truth. File hash confirmed before review: `mag_guide_v3_structure_spec.md` =
`3ca10b70244f5d2c0bfca77c53b0401efd39f5ea817a3930dd49367d2da05ae7` (matches the spec's own
citation and the task dispatch's citation — premise check passes, Hard Rule 10).

### 1 — Group re-derivation: 18/18 AGREE

Walked the precedence rule top to bottom for every row using each product's `form_absorption`,
`label_transparency`, and `doseMg`/elemental-disclosure state as carried in v2 §2/§5/§11 and
restated in §A.3:

- **Tier 1 fires** (form_absorption = fail) for exactly #11, #12, #13, #14, #16, #17 → Heading 3.
  Confirms 6/18, matches claim.
- **Tier 2 fires** (cannot_verify AND form itself an undisclosed blend AND dose unresolved) for
  exactly #18. #9 is cannot_verify but its elemental total (100 mg) IS disclosed, so Tier 2
  correctly does not catch it — it falls through. Confirms 1/18, matches claim.
- **Tier 3 fires** (single named citrate/bisglycinate form AND label_transparency = pass) for
  exactly #1, #2, #3, #4, #6, #15. #9 is excluded correctly (blend, not a single named form,
  even though label_transparency = pass on the total). #5/#7/#8/#10 are excluded correctly
  (hydroxide/malate/taurate, not citrate/bisglycinate). Confirms 6/18, matches claim.
- **Tier 4 default** catches the remainder: #5, #7, #8, #9, #10 → 5/18, matches claim.

**Sum check re-verified: 6+5+6+1 = 18.** No product's underlying dose/form/safety/label fact
changed in this re-derivation — every reassignment vs. v2's 3-group model traces to the new
Tier-1 definition being narrower than v2's (form-fail only, not form-fail-or-safety-fail),
which is what moves #1/#2 into Heading 1 and #3/#4/#6/#15 out of v2's dose-only Group (b).
That narrowing is the correct, deliberate consequence of the owner's headings being
form/label-based rather than safety-based — **co-signed, no correction needed.**

### 2 — Deviation adjudications

**DEVIATION 1 (heading 2 form-agnostic reading) — CO-SIGNED, no amendment.** The
form-agnostic reading requires zero adjustment to fit the dictated text and is the more
conservative interpretation (adds no unstated constraint the owner didn't write). Adopting
without a blocking owner round-trip: this is an interpretation call inside Product's D7
business-and-scope lane, not a strategic tripwire (no frozen invariant, no irreversible
consumer-facing ship yet, no program start/kill, no spend, no strategy redefinition) — decide
and log per the autonomy mandate, surface in the next digest for after-the-fact owner visibility.

**DEVIATION 2 (#9 in Heading 2, blend-ratio gap as mandatory secondary card fact) —
CO-SIGNED, no amendment.** Correct application of "dominant, determinate fact" precedent
already established and D7-ruled in v2 §2 row 9. The secondary-fact requirement in §B is
already stated directly (not folded into silence) — verified by re-reading the §B row 9 cell.

**DEVIATION 3 (#17 carbonate under "מבוססי אוקסיד") — CO-SIGNED WITH AMENDMENT.**
Reassignment is rejected: moving #17 out of Heading 3 would misrepresent the actual finding
(#17's problem is poor-absorption-by-chemical-class-analogy, not low dose — Heading 2 would be
a *false* home too, just a differently false one). Rewriting the heading's dictated Hebrew text
is also rejected: the four headings were dictated verbatim by the owner, this order, this text;
unilaterally editing owner-dictated consumer copy is out of Product's D7 remit even under the
autonomy mandate (this is copy the owner personally wrote, not a Nutrition/Product default) —
flagging the literal-text gap for the owner digest is the right move, not silently patching
their words. **Amendment: §A.4's "recommended: yes... either is acceptable" is upgraded from
discretionary to MANDATORY.** Content must render a one-clause disambiguation on #17's card
(e.g., along the lines of "קרבונט, מסווג יחד עם אוקסיד לפי דמיון כימי — לא בציטוט ישיר של NIH
ODS," final Hebrew Content's) — non-negotiable, not a collapsed-disclosure option. Rationale:
leaving this to case-by-case Content discretion is the exact same undisciplined path that
produced the v2 "group caption denying a member's row" failure class this task was written to
guard against; a mandatory card-level fact closes the gap without touching the owner's
dictated heading text.

**DEVIATION 4 (#16 in Heading 3 despite dose ambiguity) — CO-SIGNED, no amendment.**
Precedence-resolution call, correctly distinguished from a literal-text mismatch (§A.4 already
notes #16's own on-pack text says "oxide," so Heading 3 is textually accurate for #16, unlike
#17). Mirrors the already-established v2 §9 note-1 principle (known problem checked before data
gap). Dose ambiguity already required to surface on-card per §B — sufficient, no upgrade needed.

### 3 — §B / §C sanity re-computation

Re-derived §C's four counts directly from the §A.3 state columns rather than trusting the
prose:
- Finding 1 (misleading on-pack numeral): 2/18 (#6, #8) — confirmed. #9 correctly excluded as
  "milder version," not counted (its headline figure IS the elemental one).
- Finding 2 (citrate = clearest support): 2/18 (#1, #3) — confirmed, matches v2 §5 Bucket 1
  membership exactly.
- Finding 3 (oxide-based): 6/18 (#11–14, #16, #17) — confirmed against `form_absorption = fail`
  rows exactly; #9 correctly excluded (blend, `cannot_verify`, not a determinate oxide finding —
  more precise than v2's looser "#9 partial/blend" phrasing, no error). Sub-finding "4/18 cross
  the 350 mg UL" (#11–14) re-verified against disclosed doses (520/520/450/450, all > 350).
- Finding 4 (unclear labels): 4/18 (#8, #16, #17, #18) — confirmed against
  `label_transparency ≠ pass` rows exactly.

§B per-card facts spot-checked against v2 doses/forms/safety states for #1, #6, #9, #11, #16,
#17, #18 — no discrepancies found.

### 4 — Servings-per-day: CO-SIGNED WITH AMENDMENT

Agree the field is genuinely NULL for all 18 (never parsed, not a data-collection oversight
this spec can fix) and that inventing a capsule count is barred by the missing-data discard
rule. **Amendment, upgrading the default from "omitted" to explicit:** the servings-per-day
line must be **fully absent from the rendered card** — no row, no dash, no "not available"
placeholder — never a data-state narration line. This follows the standing owner ruling that
consumer copy never narrates data-state (no confidence/provenance prose on a consumer-facing
card); showing "not available" on 18/18 cards for the same field would be exactly that
narration, just spelled differently. Recommend the orchestrator open a Data Agent follow-up to
attempt a fresh scrape/parse of the labelled serving count from raw product-label text —
Product does not generate that number here, only names the gap and the correct default
rendering.

### 5 — Anti-drift check: PASSES

Confirmed the regroup stays a categorical first-match-wins lookup over existing discrete
bar states — no composite score introduced, no numeric weighting, no ordinal ranking
resurrected. §A.5's Heading-1 membership language is verified to state form + label clarity
only, with an explicit, still-standing bar against pairing citrate and bisglycinate under one
evaluative adjective (the §11 MEDIUM-1 correction is preserved, not reopened, by this spec).

### Verdict

**D7 CO-SIGNED**, with one mandatory amendment (DEVIATION 3 disambiguation clause becomes
required, not optional) and one clarified default (servings-per-day row fully omitted, not
shown as a placeholder). Both amendments are additive discipline, not disagreement with
Nutrition's D6 analysis — the underlying facts, precedence rule, and 18/18 group assignments
are independently re-verified and accepted as submitted. Content may author from this spec
(with the two amendments folded in) subject to the standing two-gate (Content + Adversarial
QA/Red-Team) sign-off before anything ships.

— Product Agent, D7, 2026-07-10
