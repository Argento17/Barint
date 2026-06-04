**Task:** TASK-179C

# Glass Box Wave 0 — Product Co-Sign Memo (v1)

**Status:** CO-SIGN / RECOMMENDATION ONLY. No engine code, no scoring change, no published score movement, no rule binding. This memo ratifies postures and routes the owner-level calls; it does not implement. Every posture that later binds a number still requires its EV-### + the D7 (Nutrition+Product) gate per the contract's own discipline.

**Author:** Product Agent · **Date:** 2026-06-03 · **Wave:** TASK-179, Wave 0
**Co-signs against:** `C:\Bari\01_framework\glass_box\six_dimension_contract_v1.md` (TASK-179B) §5 Q1–Q4, §4 invariants, §1.3 delta D-SCO-1.
**Grounded in:** `C:\Bari\research\glass_box\engine_enrichment_frameworks_scoping_v1.md` (TASK-179A) — esp. the empirical finding that the real shelf additive load is overwhelmingly functional/neutral; only carrageenan/CMC/aspartame/NNS are contested.

---

## 0. The frame I am ruling inside

Bari's consumer value proposition is **decisiveness** — one grade a shopper can act on in ~15 seconds — sold honestly because the box is glass underneath. There are two symmetric failure modes and my job on all four questions is to refuse both:

- **Failure A (Yuka-clone / crude oracle):** "processing = bad," name-fear, a confident grade on thin data.
- **Failure B (epistemic paralysis):** six numbers, endless "we can't be sure," `לא נוקד` on half the shelf — a glass box no one can act on.

The contract is built correctly against Failure A. My pressure on every question below is to make sure Wave 0 does not over-correct into Failure B. **Decisiveness is the product; honesty is the license to be decisive. Neither wins alone.**

One governance fence I am holding throughout, because it decides three of the four answers: **the headline grade is a within-shelf ranking over *disclosed* data (contract §1.1). It is not a health verdict and not an opacity-punishment instrument.** When a question asks "may X move the grade," the test is: *does X change where this product ranks on the observable data, or does it merely change how much we trust that ranking?* The first moves the grade; the second gates it. That single distinction resolves Q2, bounds Q3, and shapes Q1.

---

## 1. The four judgment calls

### Q1 — How aggressively should D6 demote / withhold? Where is the null-vs-cap boundary?

**Recommended posture: Conservative-to-demote, reluctant-to-withhold. Default to a *demoted, graded* answer; reserve `לא נוקד` (null) for a genuine floor-of-observability failure, not for ordinary partial disclosure. Concretely: keep three live states — unconstrained / demote / withhold — but set the withhold trigger HIGH so the common case (partial disclosure) lands in *demote*, and null is rare.**

Rationale. The whole product is decisiveness. A grade withheld is a grade the shopper cannot use — that is Failure B, and at scale it is fatal: the bread shelf's ~40% `לא נוקד` under a strict posture is not a badge of rigor, it is 40% of a category where Bari had nothing to say. A shopper standing in the aisle with "we decline to rank this" learns nothing and leaves. So withhold must be the *exception*, earned only when the data is genuinely below the floor where any ranking would be a guess — e.g. no usable nutrition panel at all, or a disclosure gap so total that D1 (the spine) cannot be computed. Ordinary partial disclosure — the *normal* case the contract itself names — must resolve to a **demoted but real grade plus a visible confidence flag** (`ניתוח חלקי`), not to silence. That is exactly the glass-box bargain: we still rank, and we tell you our hands are partly tied.

The tradeoff I am accepting: **coverage over maximal earned-certainty.** I am explicitly buying coverage, paid for by leaning on D6's *flag* (`ניתוח חלקי`) and the demote-cap to carry the honesty, rather than on withholding. This is safe because demote can only lower a grade and the confidence flag is always visible — we are never *over*-claiming, we are declining to *go silent*. The credibility risk of a demoted-with-flag grade is far smaller than the product risk of a half-empty shelf.

What I am NOT doing: I am not setting the actual null-vs-cap number. The contract correctly marks it conceptual (needs EV-### + D7). My posture *constrains* that future number — withhold floor set high, demote band doing the heavy lifting — but the threshold itself binds later.

**Classification: (a) Product co-sign I ratify — as a posture.** The *direction* (reluctant-to-withhold, demote-carries-the-load, coverage-over-silence) is a product-strategy call squarely in my D7 lane and I sign it now. **BUT the specific null-vs-cap threshold number is (b) — it co-binds with Nutrition at D7 + EV-### when D6 ships,** because where the floor sits is partly a scoring-validity judgment Nutrition owns. So: posture ratified now, number gated later.

---

### Q2 — May D5 non-disclosure MOVE the grade, or only annotate + act via D6?

**Recommended posture: D5 may NOT move the headline grade on its own axis. D5 annotates (surfaces the named gap) and acts only through D6 (confidence). Bari declines to over-credit the undisclosed; Bari does not directly *penalize* opacity in the grade.**

Rationale. This is the cleanest of the four because the §1.1 fence decides it. The grade is *"on the disclosed data, where does this rank."* Non-disclosure is, by definition, the *absence* of data — it cannot change where the product ranks on data that isn't there. The honest engine response to a gap is "I trust this ranking less" (D6) and "here is exactly what's missing" (D5's named gap list), **not** "I will dock points for the gap." The moment D5 subtracts from the headline on its own axis, the grade stops being a ranking-over-disclosed-data and becomes a *behavioral verdict on the manufacturer* — which crosses straight into the intent-attribution line governance forbids ("היצרן מסתיר"). Carrageenan-grade science is contested; *opacity* is not even a quality signal — it's a data condition. Letting a data condition move a quality grade is a category error.

There is a real-sounding counter — "a product that hides its composition deserves to rank below one that discloses fully, all else equal" — and I am rejecting it deliberately. It feels just, but it is punitive, not descriptive, and Bari is descriptive ("ברי מתארת, לא ממליצה"). The disclosing product *already* ranks differently in practice, because the opaque product's grade is demoted-and-flagged by D6 and visibly annotated by D5. The shopper sees the opaque product carrying a `ניתוח חלקי` flag and a "מקור החלבון לא צוין" note sitting next to a clean, full-confidence grade. **That asymmetry does the work honestly** — the disclosed product wins on *trust*, which is visible, rather than on a hidden opacity penalty baked into the number. We get the same consumer outcome (transparency is rewarded) without corrupting what the grade means.

Tradeoff named: we forgo a sharper, more "punchy" anti-opacity stance (some users would *want* Bari to hammer secretive labels). We accept a quieter mechanism (demote + flag + annotate) in exchange for keeping the grade's meaning pure and staying clear of intent attribution. Worth it — the grade's integrity is the trust asset; a punchier opacity penalty is not.

**Classification: (b) owner-ratification call — but with my firm recommendation to ratify "annotate-only."** This question *defines what the headline grade fundamentally claims* (a data-ranking vs an opacity-verdict). That is exactly the class of decision the frame reserves for the human owner. I am not hedging — my recommendation is unambiguous: **annotate + act via D6, no standalone D5 grade move.** But because it sets the meaning of the grade, it needs the owner's name on it, not just mine. The contract's default-conservative holding already matches this; I am converting the default into a recommended permanent posture and routing it up for ratification.

---

### Q3 — What ceiling weight may a single scientifically-contested additive carry?

**Recommended posture: a contested-tier additive (carrageenan E407, CMC E466, aspartame E951) may carry a SMALL, BOUNDED, single-grade-band-maximum signal — and only ever in the demoting direction. Concretely: the entire contested-additive contribution should be capped so it can, at most, move a product by less than one grade band on its own, and the *aggregate* of all contested additives on a single product cannot exceed roughly one grade band. It must never, alone, be decisive between two grades a shopper would treat as far apart (e.g. cannot drag a B to a D).**

Rationale. 179A's empirical finding is the anchor and it is the whole point: the real shelf is overwhelmingly functional/neutral additives that move *nothing*. The contested tier is a *handful* of molecules where regulators (EFSA/JECFA) say "safe at permitted levels" while live research (Chassaing 2022 on CMC; the microbiome work on carrageenan; IARC's 2B on aspartame) is genuinely unsettled. The governance hazard is precise: if a *contested-but-regulator-cleared* additive carries a heavy penalty, Bari is asserting an unsettled science *as if settled* — that is the fear-based register (governance §9) and it is indistinguishable from Yuka. The honest weight of "scientists disagree and regulators say fine" is **a nudge, not a verdict.** A small bounded demote says truthfully "there's an open question here, it costs this product a little"; a large penalty lies by overstating the certainty of harm.

Two hard fences inside the posture:
- **Asymmetric and demote-only.** Contested additives can only lower, never raise — consistent with §4 (no new dimension can promote, which is what keeps the snk-001 70/B ceiling structurally safe). A "clean of contested additives" product is not *bonused*; it simply isn't nudged down.
- **Confirmed-negative is a different tier and not bound by this ceiling.** Industrial trans fat is already an engine veto and stays one — Q3 governs *contested*, not *confirmed-negative*. I am bounding the unsettled tier, not declawing the settled-bad one.

Tradeoff: a small ceiling means a carrageenan-heavy product will *not* be visibly punished the way a fear-driven app would punish it, and some users will read that as Bari being "soft" on additives. I accept that. Bari's differentiator is being *right and inspectable*, not *alarming*. The additive feature was scoped (owner frame) as "a nice visual that attracts crowds — explain each additive plainly," explicitly NOT a clinical indictment. A small ceiling + a plain-language "קיים דיון מדעי" note delivers exactly that: it draws the crowd and tells the truth, without letting one contested molecule hijack a grade.

**Classification: (a) Product co-sign I ratify as a *bound*, co-binding with Nutrition on the number.** The *ceiling principle* — small, bounded, demote-only, sub-one-grade-band, never decisive alone — is a scope/governance call in my lane and I sign it. The *exact weight* each contested additive carries is a scoring-rule value that requires **Nutrition's D7 co-sign + the controlling EV-### (D-EV-1)** before it binds — and per Hard Rule 8, if Nutrition lodges a science objection to a specific weight, I do not override it. So: ceiling ratified now; per-additive number is a joint D7 + EV-### action later. Not an owner call — it doesn't redefine the grade, it bounds one input.

---

### Q4 — Does the consumer drilldown expose dimension-level findings, or only headline + confidence flag?

**Recommended posture: YES, expose dimension-level *findings* in the opt-in drilldown — but as plain-language, translated findings, NEVER as the six raw numbers and never with internal terms. The six numbers and the per-additive EV-cited graph live only on the professional surface. The consumer drilldown is a lossy, plain-language projection of that graph, gated behind an explicit opt-in.**

Rationale. The glass box is the entire differentiator. A consumer surface that shows *only* a grade + a flag is not a glass box — it is Yuka with a Hebrew accent and a confidence dot. The thing that makes Bari trustworthy is that a curious shopper can *open the box* and see "בסיס קמח לבן," "מקור החלבון לא צוין," "מרכיב טכנולוגי מוכר," "קיים דיון מדעי על המעי" — real findings in their own language, on demand. That is the product. Withholding all findings to the professional tier would amputate the consumer value proposition to protect against leakage — solving the wrong risk.

But the contract's §3 seam and the Sophistication Gradient are exactly right and I am holding them as the guardrail: **findings yes, numbers no.** The shopper never sees six 0–100 sub-scores (that is the paralysis failure mode — six numbers no one acts on), never sees "NOVA / structural_class / cap / floor / BSIP," never sees raw EV citations. They see a decisive grade up top, and *if they opt in*, a short stack of plain-language findings that explain it. Sophistication rises only as the reader chooses. The full six-dimension graph + EV trace is the professional face's job.

Tradeoff: every exposed finding is surface area for framework leakage (an internal term slipping into consumer copy) and for the "wall of caveats" effect. I accept it and contain it two ways — (1) findings are capped in number and curated (the contract's "≤3 findings" editorial instinct applies; a drilldown is a short verdict, not a report), and (2) every consumer-facing finding string passes the existing content/governance gate (D13) before it ships. The risk is real but it is a *copy-discipline* problem we already know how to manage, not a reason to hide the glass.

**Classification: mostly (a) Product co-sign, with a (b) Design/Content seam.** The *principle* — drilldown exposes plain findings, not numbers; opt-in gated; professional surface holds the full graph — is a product/scope call I ratify now (D11 scope + D12/D13 governance edge are mine). The *exact rendering* (how many findings, disclosure interaction, mobile progressive-disclosure pattern) is **Design's call (D11 implementation), executed against this principle and run back through D12/D13.** No owner ratification needed — this does not redefine what the grade claims; it defines how much of the (already-decided) box is visible. Routed to Design Agent for the rendering spec when Frontend Wave opens.

---

## 2. D-SCO-1 verdict — roll-up vs replacement

**I CO-SIGN D-SCO-1. The ten internal scoring dimensions ROLL UP into the six public dimensions as a grouping/relabeling layer. They are not replaced.**

This is the single most important risk-control decision in the wave and I sign it without reservation, for three reasons:

1. **It is what makes the invariants safe by construction.** Milk = run_004 (top 85/A), snk = 70/B ceiling, bread provenance — all of these are properties of the *existing internals* and the existing `GRADE_THRESHOLDS`. A roll-up/relabel preserves them because the numbers underneath don't move; only their *presentation* regroups. A *replacement* would rebuild the scoring substrate and put every frozen invariant back in play — a re-derivation I would not approve in a transparency wave. The contract's §4 invariant-preservation statement only holds *because* D-SCO-1 is a relabel, not a rebuild.

2. **It matches the strategic posture.** The glass box is "same engine, two faces" (§3). Roll-up *is* the two-faces architecture — one computation, regrouped for inspection. Replacement would be a new engine wearing a transparency label, which is precisely the thing the "same engine, two faces" principle forbids.

3. **It keeps Wave 0 a documentation/contract wave, not a scoring rewrite.** My job is to prevent scope creep. "Replace the ten dimensions with six" is a scoring-engine project; "relabel the ten into six and document the rollup map" is a contract deliverable. D-SCO-1 keeps us in the second, which is what TASK-179 is chartered to be.

One condition on my co-sign (a deferral, not an objection): **the rollup map itself must be documented and verified when D5/D6 ship** — i.e. an explicit table showing which of the ten internals feeds each of D1–D6, confirmed against the engine, with the golden runs re-verified 0-diff under the flag (same discipline as `BARI_RECAL_P0`). D-SCO-1 asserts the rollup is *clean*; that assertion must be *shown*, not assumed, at ship time. With that condition, co-signed.

---

## 3. Co-sign ledger — what I ratify now vs what goes to the owner

| Item | My recommendation (one line) | Classification | Who ratifies / next gate |
|---|---|---|---|
| **Q1** D6 aggressiveness | Conservative-to-demote, reluctant-to-withhold; demote carries the load, null is rare; buy coverage over silence | (a) posture I ratify; (b) the null-vs-cap **number** co-binds at D7+EV-### | Posture: **me, now.** Number: Nutrition+Product D7 when D6 ships |
| **Q2** D5 moving the grade | NO standalone move — annotate + act via D6 only; reward disclosure through visible trust, not a hidden opacity penalty | (b) owner call — it defines what the grade claims | **Owner ratification** (my firm rec: annotate-only) |
| **Q3** contested-additive ceiling | Small, bounded, demote-only, sub-one-grade-band, never decisive alone; trans-fat veto unaffected | (a) ceiling I ratify; per-additive **weight** co-binds at D7+EV-### | Ceiling: **me, now.** Weight: Nutrition+Product D7 + EV-### |
| **Q4** drilldown exposure | YES — plain-language findings on opt-in; never the six numbers, never internal terms; full graph stays professional | (a) principle I ratify; rendering is a Design seam | Principle: **me, now.** Rendering: Design (D11) → D12/D13 |
| **D-SCO-1** rollup vs replace | CO-SIGN roll-up/relabel, not replacement — condition: rollup map documented + 0-diff-verified at ship | (a) I co-sign | **Me, now**, condition gated to D5/D6 ship |

**Two items require the human owner before any binding work:** Q2 (defines the grade's meaning) and the *numeric* halves of Q1/Q3 (bind via the normal D7+EV path, not owner — but listed so they aren't mistaken for ratified-and-done). Everything else — Q1 posture, Q3 ceiling principle, Q4 principle, D-SCO-1 — I co-sign outright as Product.

**Discipline reminder carried forward (not a new rule):** nothing in this memo binds a number. Every numeric threshold (Q1 floor, Q3 per-additive weights) still ships behind a flag, OFF = byte-identical, golden runs 0-diff-verified, with its EV-### and D7 co-sign, exactly as §4 and §6 require. This memo authorizes *postures and direction*, not deployment.

---

*End of Wave 0 Product Co-Sign memo v1. Co-sign/recommendation only — no engine, scoring, frontend, or governance file was modified. Proposed task status: RETURNED (Product does not write CLOSED).*
