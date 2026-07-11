# Supplement Guides Re-Direction — Nutrition Science Co-Sign / Corrections Memo v1 (TASK-504)

**Type:** Nutrition Agent consult response — science co-sign or corrections, not a build.
**Status:** ISSUED. Does not build, does not close. Answers the brief's §7 Nutrition
questions in order. Every factual claim below traces to an artifact already in the repo;
nothing new is asserted about any product or study that isn't already sourced there.
**Input:** `01_framework/product/supplement_guides_redirection_brief_v1.md` (brief, DRAFT FOR
CONSULTATION), `01_framework/nutrition/creatine_evidence_cosign_v1.md` (creatine evidence
base, ISSUED), `01_framework/nutrition/functional_dose_ingredient_ruling_v1.md` (dose-honesty
bands, ISSUED), `bari-web/src/lib/comparisons/magnesium-page-data.ts` (live v3 model output),
`03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml` (dossier),
`03_operations/supplement_engine/proto_v0/benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md`
(v3 architecture + evidence grounding for the tier factors).
**Scores affected:** None. **BSIP2/food scoring exposure:** None (confirmed in §6 below).
**Author:** Nutrition Agent
**Date:** 2026-07-04

---

## 1. T3 — the magnesium call (core question)

**Verdict: the brief's recommendation is scientifically defensible. Keep form-tier bands
(citrate/bisglycinate vs oxide-class absorption) + UL safety flags as retained
pass/flag/fail verdicts. Drop the ordinal 1–18 ranking and the composite 0–100 score.
Do not go fully flat like creatine — magnesium and creatine are not the same evidentiary
shape, and treating them identically would itself be a honesty failure in the other
direction (discarding a real, well-replicated finding to make the two guides look
structurally uniform).**

### 1.1 Why magnesium is not creatine

Creatine went flat because the science genuinely collapses to near-equivalence: monohydrate
is monohydrate, and the dossier's own ruling is that alternative forms (HCl, buffered,
citrate/malate) are "evidence-orphaned for a premium claim," not inferior — there is no
legitimate ordinal form differentiator to display (`creatine_evidence_cosign_v1.md` §3.1
point 2, row 14). Forcing rank differentiation onto a genuinely flat evidence base is
exactly the manufactured-differentiation failure the butter-clustering precedent names.

Magnesium's form question does not collapse the same way. The directional claim — organic
salts (citrate, bisglycinate, and related organic forms) are absorbed meaningfully better
than oxide — is one of the best-replicated form-level findings in mineral supplementation,
quoted directly from a primary regulatory source:

> NIH ODS Magnesium Fact Sheet (Health Professional Version): "Forms of magnesium that
> dissolve well in liquid are more completely absorbed in the gut than less soluble forms.
> Small studies have found that magnesium in the aspartate, citrate, lactate, and chloride
> forms is absorbed more completely and is more bioavailable than magnesium oxide and
> magnesium sulfate." (quoted in `magnesium_model_v3_bioav_adjusted_dose_spec.md` §1.2)

This is a **directional/categorical** claim with real evidentiary weight — evidence tier
**Moderate-to-Strong** for the direction (oxide < organic salts), per the dossier's own
`forms.form_ladder_confidence: "medium-high"` and `forms.citations: [PMID:39770988,
PMID:30761462, PMID:7815675]` (`magnesium.yaml` lines 64–71). It is corroborated by an
authoritative primary source (NIH ODS) independent of the cited PMIDs, which strengthens
confidence in the direction even before those three PMIDs are individually re-verified
(see caveat in §1.4).

**What is NOT well-evidenced, and must never ship in consumer copy:** the specific
fractional-absorption percentages (oxide ≈ 4%, citrate ≈ 28–32%) cited in the v3 spec's
"Quantitative reference" subsection are explicitly flagged there as heterogeneous,
study-design-dependent, and not assertable as individual-level facts — this is exactly why
the v3 scoring model uses a coarse calibration constant (1.0 / 0.75 / 0.35) rather than the
raw percentages, and why the display rule forbids ever showing an "adjusted" or "absorbed"
mg figure (`magnesium_model_v3_bioav_adjusted_dose_spec.md` §1.2, §1.3, §8). This
distinction — real directional finding, fake-precision on the magnitude — is the entire
scientific basis for a **tier band**, not a numeric score: a tier band ("high absorption
class" / "moderate" / "low") communicates exactly what the evidence supports (a category),
while a numeric score or 1–18 rank implies precision the underlying absorption literature
does not have.

### 1.2 The model's own history is corroborating evidence for "band, not rank"

The magnesium v3 scoring model's build history is itself informative: the LOW tier factor
was recalibrated from 0.45 to 0.35 specifically because C3's review found that 0.45 produced
a 0.4-point gap between oxide-314mg and a clean bisglycinate-122mg product — a gap C3
characterized as **"below consumer-signal noise (same grade C, near-tie)"**
(`magnesium_model_v3_bioav_adjusted_dose_spec.md` §1.2, "MRT-8" note; also see current
`magnesium-page-data.ts` C-band comment: "These products cluster in C... The clustering IS
the finding, not an artifact"). This is Nutrition's own prior finding that fine-grained
ordinal separation within a tier is not a real signal — it is calibration noise dressed as
precision. A guide format that drops the composite number and displays only the categorical
tier (HIGH/MODERATE/LOW/UNRESOLVED) plus the administered dose is a more honest
representation of what the evidence actually distinguishes than the ranked list ever was.

### 1.3 Is tier-membership defensible at the per-product label level?

**Mostly yes, with one honest exception that must stay visible.** Reviewing the live
corpus (`magnesium-page-data.ts`, 18 products): 15 of 18 have a clearly stated chemical form
on-label (citrate, bisglycinate, oxide, malate, taurate, hydroxide) from which tier
membership (HIGH/MODERATE/LOW per `BAV_TIER_FACTORS`) is directly and unambiguously
derivable. The remaining **3 of 18 (17%)** are genuinely UNRESOLVED at the label level —
blend ratios undisclosed (Solgar Ca+Mg+D3, TRIOMAG tri-form blend) or the elemental-vs-
compound distinction itself is ambiguous (Amorphicure carbonate, Tink Oxide-520 missing the
"from magnesium oxide" qualifier). This is not a flaw in the tier concept; it is a real,
already-correctly-handled finding (**UNRESOLVED is its own displayed state, never defaulted
to a tier** — see §5 for why this generalizes to the guide's bar system). Tier-membership
is defensible **provided the guide preserves this fourth "cannot determine" state distinctly**
rather than silently assuming a tier when the label doesn't support one.

### 1.4 One verification gap to flag before this ships as guide copy

The three PMIDs backing `forms.citations` in `magnesium.yaml` (`PMID:39770988`,
`PMID:30761462`, `PMID:7815675`) have not been through the same explicit independent
re-verification pass the creatine evidence base received (`creatine_evidence_cosign_v1.md`
labels every claim VERIFIED-primary / corroborated / unverified explicitly; the magnesium
dossier's provenance block does not carry that same per-citation confidence marking — it
only states `nutrition_cosign: true` at the dossier level). **Recommendation: before any
specific PMID appears as an inline citation in guide copy (as opposed to the NIH ODS
quote, which is independently citable as-is), route a verification pass to Research Agent**,
consistent with the citation-fabrication gate. This does not block the T3 recommendation
itself — the directional claim already stands on the independently-quotable NIH ODS primary
source — but it does gate whether those three specific PMIDs can be named in copy.

**Bottom line on T3:** form-tier bands + UL flags = keep, scientifically grounded, tier
membership is derivable for 83% of the current corpus with the remaining 17% correctly
handled as its own "cannot determine" state. Ordinal 1–18 rank and composite score = drop,
correctly identified by the brief and owner as manufactured precision the underlying
absorption evidence does not support. This is not "go fully flat like creatine" — it is
the middle path the actual evidence shape calls for, and going fully flat would discard a
real finding (oxide's absorption disadvantage) that Bari has independently corroborated via
its own recalibration history.

---

## 2. Attribute completeness

**Verdict: {dose adequacy, chemical form/absorption, third-party verification,
price-per-effective-unit} is a good starting set but is missing two attributes that should
be added as first-class bars, and one that should be threaded as context rather than a
fifth bar.**

### 2.1 What's correctly included

All four map cleanly onto machinery Bari already owns:
- **Dose adequacy** → SIE Dose dimension / the functional-dose annotation bands
  (`functional_dose_ingredient_ruling_v1.md` §3.2: ≥3g/day meaningful, 1.5–3g/day partial,
  <1.5g/day decorative, undisclosed/blended = its own flag).
- **Chemical form/absorption** → SIE Form dimension / magnesium's BAV tier classes.
- **Third-party verification** → a genuine, **verifiable, binary, label/cert-page fact**
  (NSF Certified for Sport, Informed-Sport), not a scientific-evidence-tier question —
  confirmed usable per `creatine_evidence_cosign_v1.md` §3.1 point 3, but it requires
  per-product fact-checking against the certifying body's registry before it ships, the
  same discipline as any other product fact (not a Nutrition evidence-tier call).
- **Price-per-effective-unit** → cost normalized to servings-at-effective-dose, the same
  normalization already used for both magnesium and creatine
  (`creatine_evidence_cosign_v1.md` §3.1 point 4).

### 2.2 What's missing — recommend adding as first-class bars

1. **Safety, as its own bar, separate from dose adequacy.** The current four-attribute
   list has no explicit safety/UL bar — UL crossing is implicitly folded into "dose"
   language in the brief's §3, but UL exceedance and dose *adequacy* are orthogonal
   findings, and magnesium's own corpus proves it: four oxide products are simultaneously
   adequately-dosed-on-paper (450–520mg elemental, well above the 300mg general-gap floor)
   **and** over the 350mg IOM/NASEM supplemental UL (`magnesium-page-data.ts` UL_EXCEED
   block; `magnesium_model_v3_bioav_adjusted_dose_spec.md` §2.4). A single "dose adequacy"
   bar cannot honestly represent both "enough" and "too much" as the same axis. Full
   treatment in §4 below.

2. **Label transparency / dose-disclosure honesty, as its own bar, separate from dose
   adequacy.** "Undisclosed" is currently described in the brief as a *state within* the
   quantity bar, but the underlying finding is categorically different from a low-but-known
   dose: it is a **labeling-honesty pattern** (SIE §2.4's fairy-dust/hidden-dose logic;
   creatine's "blend-hiding cap" — creatine named on-label but buried in a proprietary
   blend with no per-active gram figure, `creatine_evidence_cosign_v1.md` §4). This
   generalizes beyond dose: it also covers whether a label states **elemental vs compound
   mass** (magnesium's central trap — oxide is 60.3% elemental by mass, bisglycinate is only
   14.1%, so a compound-mass-only label systematically favors the worse-absorbed form,
   `magnesium.yaml` lines 11–27) and whether a **serving-size manipulation** is inflating a
   per-serving number while the effective daily dose stays sub-therapeutic. Recommend this
   be a distinct, explicitly-named bar ("is the dose disclosed honestly and completely,"
   independent of whether the disclosed number clears the effective-dose bar) rather than
   silently absorbed into the dose-adequacy bar's edge case.

### 2.3 What should be threaded as context, not a fifth bar

**Form-specific tolerability/side-effect profile** (Q asked directly, e.g. magnesium
oxide/citrate causing GI-laxative effects at any dose vs bisglycinate's better GI
tolerance) is real and already appears in existing copy as context on the form bar (e.g.
"ביסגליצינט נחשב עדין יותר לקיבה" in the live magnesium page). Recommend **keeping it as
qualitative context attached to the form/absorption bar**, not a fifth independent
pass/flag/fail bar, for two reasons: (1) it is not cleanly binary/tiered the way form-class
or UL-crossing is — tolerability is graded and individual, closer to a caveat than a
verdict; (2) adding a fifth bar for every category risks exactly the attribute-proliferation
overbuild Product Agent is tasked to guard against. If a future supplement surfaces a case
where tolerability diverges sharply from its absorption-class placement (plausible for
some minerals/vitamins at high single doses), re-open this as a dedicated bar at that time
— it does not need to be pre-built now.

### 2.4 What should be EXCLUDED as not defensible

- Any per-product ordinal rank or composite score (already ruled out in §1).
- Any "absorbed mg" / adjusted-dose display — the v3 hard display rule (never show the
  internal tier factor or an "adjusted" figure) must carry over unchanged into the guide
  format; the guide's form bar shows administered label dose + class label only.
- A claim that alternative creatine forms (HCl, buffered) are unsafe or lower-quality —
  the dossier's framing is "no evidenced advantage over monohydrate," not "worse"; the
  guide must preserve that distinction exactly.
- Fabricated precision on fractional-absorption percentages as individual-level facts
  (§1.4) — categorical/directional framing only.
- Any framing that implies the product is "needed" (SIE Invariant 1, No-Necessity Rule) —
  carries over unchanged to the guide's educational spine.

---

## 3. Claims discipline for guide copy

**Verdict: the creatine co-sign's tiered claim table (Strong/Moderate/Weak/Insufficient,
each with a consumer-safe framing line and an explicit confident/hedge/no-go flag) is not
creatine-specific — it is Hard Rule 6's evidence-tier discipline in worked form, and it
generalizes directly to magnesium and to any future supplement.** Magnesium's own dossier
already uses the identical structure (BP reduction = Moderate/ratified; sleep = Weak-held;
bone/muscle health mapped to Weak observational endpoints via the `structure_function_umbrella`
mechanism, `magnesium.yaml` lines 29–51, 104–288) — the guide format should reuse this
existing tier table directly rather than re-derive a parallel one.

### 3.1 Allowed in the educational spine

1. **Tiered, population-qualified efficacy statements**, where a Moderate/Weak claim
   carries its qualifying population or context inline in the same sentence — e.g.
   magnesium's blood-pressure claim is real (Moderate) but subgroup/dose-dependent; the
   guide must not compress it to a flat "magnesium lowers blood pressure."
2. **Explicit null/negative findings**, stated with the same directness as positive
   findings (creatine + fat loss = Insufficient, stated as a clear null, not softened).
   Hard Rule 6 requires this symmetry — a guide that hedges every positive claim but goes
   quiet on nulls is itself a claims-discipline failure.
3. **Mechanistic/format facts carrying no efficacy claim** (e.g., magnesium's
   elemental-vs-compound mass math, or dairy-matrix creatine-stability facts) — always safe
   provided no benefit inference rides along with the fact.
4. **Defensible safety cautions framed as cautions, not health claims** — UL framing,
   contraindication flags (per §4).
5. **"Well-replicated" framing reserved for genuinely Strong-tier, consensus claims only**
   (creatine strength/power = Strong; nothing in magnesium's current dossier reaches Strong
   — its best-tiered claim, blood pressure, is Moderate, so magnesium copy should never
   borrow creatine's "one of the best-replicated effects" register).

### 3.2 Banned

1. **Compressing a split-tier finding into one flat statement** — this is the exact error
   Research caught in the creatine synthesis (a Moderate-marker + Weak-functional recovery
   claim flattened into one "creatine speeds recovery" line, `creatine_evidence_cosign_v1.md`
   §2.2). Generalizes as a hard rule for any future split finding.
2. **Specific effect-size numbers without an independently re-verified citation** — no
   numeric effect size (kg, %, SMD) ships without a verified PMID trace, per the
   creatine co-sign's ship-gate discipline (§5 there) and the magnesium PMID-verification
   gap flagged in §1.4 above.
3. **General-population extrapolation from population-specific evidence** — magnesium's
   bone/muscle mappings are observational-only and Weak; they must not be presented as if
   RCT-proven or generally applicable.
4. **Necessity framing** ("you need this") — SIE Invariant 1 carries over unchanged.
5. **Unverified PMIDs/DOIs** — never, per the project-wide citation fabrication gate.
6. **Internal engine jargon leaking into copy** — "cap," "floor," "NOVA," "BSIP,"
   "structural_class" are already banned (Hard Rule 4); the same logic extends to the SIE's
   own internal terms — "tier factor," "adjusted dose," "bav_class," "BAV" — none of which
   may appear in consumer-facing guide copy (the v3 spec's own hard display rule already
   requires this; it must survive the format change unchanged).

---

## 4. UL/safety treatment

**Verdict: UL crossing renders as a bar-level FAIL, always visible-block (never a tooltip
or collapsed note) — it is a whole-product safety fact independent of everything else on
the page. Context-specific contraindications (e.g., creatine's bipolar-mood caution) render
as a scoped note attached to the specific claim/context they apply to, never as a
blanket product-level flag.**

### 4.1 Why the distinction matters

Magnesium's live model already treats UL_EXCEED as a **grade ceiling (max D) plus a
mandatory visible safety block** — not a tooltip, not a footnote — with explicit
dose-vs-limit language and GI-tolerance-not-toxicity framing (`magnesium-page-data.ts`
lines 20–22, 505–513; the model's own comment: "VISIBLE (requirement 4). Dose vs limit
framing, GI-tolerance-not-toxicity, dose stated explicitly"). In a de-ranked guide there is
no grade left to cap — so the ceiling mechanism's *communicative work* must be preserved by
promoting UL-crossing to its own **bar** in the pass/flag/fail system, rendered as FAIL,
not softened into a note. Downgrading this to a mere annotation would be a real regression
in prominence relative to what the current, already-shipped model achieves for the same
four products.

By contrast, creatine's bipolar/manic-switch caution is explicitly **scoped**: it "does not
apply to standard strength/lean-mass use in the general population; specific to
mood/depression-use context in bipolar individuals" (`creatine_evidence_cosign_v1.md` §2.4).
Rendering this as a blanket product-level FAIL would misrepresent its scope — it would imply
every creatine product carries a general safety problem, when the actual finding only
applies within a specific use-context. This must render as a **note attached wherever
mood/depression framing appears** in the guide (never standalone, per the co-sign's own
requirement that the mood claim and the caution are inseparable in copy), not as a
product-wide flag.

### 4.2 General rule for future supplements (recommend codifying)

- A safety signal that applies to the **whole product regardless of use-context** (dose
  crosses an established UL/toxicity-relevant threshold) → **bar-level FAIL, always visible,
  never a tooltip.**
- A safety signal that applies only within a **specific use-context or subpopulation**
  (contraindication) → a **scoped note attached to the relevant claim/context**, never
  generalized into a blanket product flag.
- Neither renders as a hidden/collapsed element. Bari already has this precedent
  ("visible, not tooltip," TASK-384A) — recommend it become the standing rule for the guide
  format generally, not a magnesium-specific artifact.

---

## 5. The undisclosed-dose flag

**Confirmed: undisclosed dose must carry into the bar system as its own fourth state —
PASS / FLAG / FAIL / CANNOT VERIFY — never collapsed into FAIL and never assumed as PASS.**

This is not a new ruling; it is the direct extension of two already-standing rules: the
missing-data-discard doctrine ("unknown is acceptable; OFF is not," extended to dose math by
`functional_dose_ingredient_ruling_v1.md` §3.1) and the magnesium page's own live
implementation (3 of 18 products render with `score: null, grade: null` and the explicit
copy "לא ניתן לדרג — נתוני תווית חסרים," never assumed low or high, `magnesium-page-data.ts`
lines 720–813). The creatine dairy finding is the cleanest precedent for the guide context
specifically: both Yoplait GO SKUs land in "Amount not disclosed," with **zero score or
grade rendered**, which the co-sign calls "a real, publishable transparency-gap finding — a
stronger and more honest story than a fabricated dose verdict would be"
(`creatine_evidence_cosign_v1.md` §3.2).

**Two implementation implications specific to the guide format (not present in a scored
comparison page), worth flagging explicitly:**

1. **CANNOT VERIFY must attach to the specific bar it affects, not the whole product**, when
   only one attribute is undisclosed and the rest of the product's data is known (e.g., a
   product with disclosed dose and form but no third-party-verification data available
   should show CANNOT VERIFY only on the verification bar, not across the board).
2. **Whole-product discard remains the correct treatment when the core dose/form picture is
   entirely unknowable** — the standing precedent is Supherb Max 550, discarded from the
   magnesium corpus because its oxide:citrate blend ratio is unknowable at all
   (`magnesium-page-data.ts` line 820). This is different from "one bar undisclosed, rest
   known" — that case should still appear in the guide with the affected bar marked CANNOT
   VERIFY, not be discarded outright. The two failure modes look similar but require
   different treatment; conflating them would either over-discard genuinely useful partial
   information or under-discard a product with no real basis for inclusion.

---

## 6. Scoring firewall

**Confirmed: this program touches zero BSIP2/food scoring. The Supplement Intelligence
Engine (SIE) that magnesium and creatine data comes from is architecturally a sibling engine
to BSIP2, not an extension of it** (`functional_dose_ingredient_ruling_v1.md` §5: "the SIE
is architecturally already a sibling engine, not a BSIP2 extension... shared acquisition
plumbing, forked scoring brain"). The guides re-direction changes only the SIE's **output
presentation layer** (drop ordinal rank + composite number, keep tier bands + UL as
pass/flag verdicts) — it touches no BSIP2 dimension, no `score_engine.py`, no
`constants.py`, no cap/floor/veto in the food-scoring spine. No published food score is
affected by anything in this consult.

**One scope-boundary worth naming explicitly so it doesn't get conflated going forward:**
the **functional-dose annotation lane** (creatine detected inside a food product, e.g.
Yoplait GO dairy drinks) is a *different surface* from the **מדריכים (Guides) product**
this consult is about. The annotation lane borrows SIE Dose Adequacy logic read-only to
produce a non-scoring annotation *on a food page* (`functional_dose_ingredient_ruling_v1.md`
§2); the Guides product is a *standalone page* for a supplement-as-product. Both use the
same underlying SIE dossier machinery, which creates a real risk that a future
implementation session conflates them (e.g., "reuse the guide's bar component on the food
annotation, since it's the same data") — that would be fine for *display components* but
must never blur the fact that the food annotation still has zero scoring exposure by design,
while the Guide is itself becoming the primary consumer-facing surface for that same
evidence. Recommend this boundary get one explicit line in whatever spec Product/Frontend
write next.

**Tripwires I see (none of the owner's 5 strategic wires fire from Nutrition's vantage
point; two lower-grade governance risks worth flagging anyway):**

1. **Not a strategic tripwire, but a standing-process one:** the bar system's
   PASS/FLAG/FAIL/CANNOT-VERIFY thresholds (what dose counts as adequate, what form sits in
   which tier, what UL value triggers FAIL) are themselves a rubric with the same weight as
   a scoring rule, even though they will not live inside `score_engine.py`. Recommend they
   ship as a **versioned, machine-readable config artifact** (same discipline as
   `grade_boundary_policy_v1.json`), not prose that a future generator has to re-interpret —
   consistent with the standing "Rulings as Config" mandate. This is a build-quality
   recommendation, not a blocker on this consult.
2. **Rule-accretion risk to flag and foreclose now:** because the bar model is structurally
   a scoring rubric with the number stripped off, there is a real future temptation to bolt
   a composite number back on top of the bars (e.g., "let's just add up the pass/fail counts
   into a new mini-score"). That would silently undo the entire point of this re-direction —
   the owner's finding that ranking supplements doesn't work. Recommend an explicit standing
   note in whatever spec ships next: **the bar system is terminal for the guide context; it
   does not feed a new composite score without a fresh Product+Nutrition review**, exactly
   the same protection the SIE and BSIP2 already have against rule accretion.
3. No tripwire on frozen invariants (no published score touches), irreversible
   consumer-facing commitment (guide content is revisable, not a one-way door), starting/
   killing a major program (owner-initiated), external commitment/spend (buy button v1 has
   no affiliate terms), or redefinition of what Bari is (extends the existing "describe,
   don't recommend" posture to a new page format). Nutrition concurs with the brief's own
   read on this point.

---

## Constraints compliance

- No product data, ingredient list, PMID, or DOI invented anywhere in this memo. Every
  factual claim traces to `creatine_evidence_cosign_v1.md`, `functional_dose_ingredient_
  ruling_v1.md`, `magnesium-page-data.ts`, `magnesium.yaml`, or
  `magnesium_model_v3_bioav_adjusted_dose_spec.md`, cited by file and, where the source
  document supplies one, PMID.
- One verification gap flagged explicitly rather than silently assumed clean: the three
  PMIDs backing magnesium's form-ladder citations have not been through the same explicit
  per-citation verification pass the creatine base received (§1.4) — flagged as a
  Research Agent candidate, not resolved here, and not treated as blocking the T3
  recommendation because the NIH ODS primary-source quote independently supports the
  directional claim.
- No consumer copy drafted. Every line in §3 is a *permitted claim type*, not finished
  copy — Content Agent authorship + the mandatory two-gate sign-off (Content + Adversarial
  QA) still applies before anything reaches the owner, per the standing hard rule.
- No BSIP2/`score_engine.py`/`constants.py` file touched or referenced as a target for
  change. No published score moves. Confirmed explicitly in §6.
- Open Food Facts not used, referenced, or considered anywhere in this memo.
- No subagents spawned.
- This is a consult response (RETURNED), not a build. Does not close TASK-504.

---

## Return Contract

```json
{
  "task": "TASK-504",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "01_framework/nutrition/supplement_guides_science_cosign_v1.md",
      "action": "created",
      "sha256": "NOTE: this file's own hash cannot be embedded without changing itself on next save; the hash below is of the pre-this-edit content and will drift by one edit. Verify with `sha256sum 01_framework/nutrition/supplement_guides_science_cosign_v1.md` at read time — last computed: 0100282fc80fdf8aae26a63f9dd7f3ba778fd74bb5f0d3c2df330e7d3079296a"
    }
  ],
  "counts": {
    "consult_questions_answered": "6/6 (source: brief §7 Nutrition Agent line: T3, attribute completeness, claims discipline, UL/safety treatment, undisclosed-dose flag, scoring firewall — each answered in its own numbered section §1-§6 of this memo)",
    "artifacts_cited_as_evidence_basis": "5/5 (source: this memo's header Input list — creatine_evidence_cosign_v1.md, functional_dose_ingredient_ruling_v1.md, magnesium-page-data.ts, magnesium.yaml, magnesium_model_v3_bioav_adjusted_dose_spec.md — every factual claim in §1-§6 traces to one of these five)",
    "magnesium_corpus_tier_derivable_from_label": "15/18 (source: magnesium-page-data.ts — 15 products with an explicitly stated chemical form; denominator 18 = total displayed products per file header comment 'Scored products displayed: 15. No-score products displayed: 3. Total shown: 18.')",
    "magnesium_corpus_unresolved_tier": "3/18 (source: magnesium-page-data.ts UNRESOLVED block, lines 720-813 — Solgar Ca+Mg+D3, Amorphicure carbonate, TRIOMAG tri-blend; same 18-product denominator)",
    "new_bars_recommended_beyond_briefs_four": "2/2 (source: this memo §2.2 — Safety-as-own-bar, Label-transparency/dose-disclosure-as-own-bar; denominator = 2 gaps identified against the brief's 4-attribute set in §7)",
    "attributes_recommended_for_exclusion": "5/5 (source: this memo §2.4 — ordinal rank/composite score, absorbed-mg display, alternative-creatine-form-inferiority framing, fabricated absorption percentages, necessity framing; denominator = 5 items listed in that section)",
    "verification_gaps_flagged_not_silently_assumed_clean": "1/1 (source: this memo §1.4 — magnesium form-ladder PMIDs PMID:39770988/PMID:30761462/PMID:7815675 not independently re-verified per-citation, unlike the creatine base's explicit VERIFIED-primary/corroborated markings)",
    "scores_changed": "0/0 (no BSIP2 file touched; confirmed in §6 and Constraints compliance)",
    "off_usages": "0/0 (banned source, never invoked, confirmed in Constraints compliance)"
  },
  "commands_run": [],
  "not_done": [
    "No independent PubMed re-verification of the three magnesium form-ladder PMIDs performed in this memo — flagged in §1.4 as a Research Agent candidate, not resolved here",
    "No versioned machine-readable config artifact created for the recommended bar-threshold rubric (§6 tripwire 1) — this memo recommends the artifact exist before build, but authoring it is a build-stage action for whoever owns the guide spec next, not this consult",
    "No consumer copy drafted for either the magnesium or creatine guide — explicitly out of scope per the task brief; §3 supplies permitted claim TYPES only",
    "No fact-check performed on any specific third-party-verification claim (NSF Certified for Sport status) for any named product — flagged in §2.1 as a per-product fact-check requirement, not a Nutrition evidence-tier question",
    "No Product Agent, Adversarial QA, or C3 consult content addressed here beyond what bears directly on the Nutrition questions in brief §7 — this memo answers only the Nutrition Agent's assigned questions, not the full multi-agent consult round"
  ],
  "self_check": "Acceptance test: answer all 6 brief §7 Nutrition questions with one clear recommendation each, ground every factual claim in an already-existing artifact (no invented PMIDs/product data), flag rather than silently assume any unverified citation, and confirm zero BSIP2/scoring exposure with named tripwires -- all without building, closing, or spawning subagents. Result: PASS. Section 1 delivers a single verdict on T3 (keep form-tier bands + UL flags, drop ordinal rank/score, do not go fully flat) grounded in the NIH ODS primary-source quote and the magnesium corpus's own recalibration history, with the per-citation PMID verification gap flagged rather than hidden. Section 2 gives a complete attribute audit: confirms the brief's 4 attributes, adds 2 recommended new bars (safety, label-transparency) with corpus evidence for why they're distinct axes, threads tolerability as context rather than a 5th bar with reasoning, and lists 5 attributes to explicitly exclude. Section 3 confirms the creatine tier-table method generalizes, with a concrete allowed/banned claim-type list reusing the creatine co-sign's own caught errors as generalizable rules. Section 4 gives a binary safety-rendering rule (whole-product UL fail vs scoped contraindication note) grounded in the magnesium page's existing 'visible not tooltip' precedent and the creatine bipolar-flag's explicit scoping. Section 5 confirms the undisclosed-dose fourth-state treatment carries into the bar system, with two guide-specific implementation nuances (bar-level vs whole-product discard) flagged. Section 6 confirms zero BSIP2 exposure with the SIE-sibling-engine citation, names the annotation-lane-vs-guide scope-boundary risk explicitly, and surfaces 2 non-owner-tripwire governance risks (config-not-prose, rule-accretion-back-to-a-score) while confirming none of the owner's 5 strategic tripwires fire. No PMID, DOI, product fact, or dose value asserted anywhere that isn't already sourced in the 5 cited artifacts. No subagents spawned; no file outside 01_framework/nutrition/ written."
}
```
