# Supplement Guides — D7 Co-Sign + Empty-Shortlist Design Ruling v1 (TASK-504A/504B)

**Author:** Product Agent
**Status:** RETURNED — rulings below are in-model refinements within the owner-approved
concrete plan (`01_framework/product/supplement_guides_concrete_plan_v1.md`); none trips a
tripwire (see §6). D7 co-sign is granted on the bar rubric as authored, conditional on the
build folding in items 1, 2 and 5 below — no re-open of the YAML required.
**Inputs read:** `supplement_guides_concrete_plan_v1.md`, `supplement_guides_bar_rubric_v1.yaml`,
`supplement_guides_bar_rubric_companion_v1.md` (validation table + §7). All counts below cite
the companion doc's validation table sections — no number in this memo is re-derived or
eyeballed; Product interprets Nutrition's figures, it does not generate them.

---

## 1. The empty-shortlist fix — DECISION: promote & headline `passes_with_flag`, unchanged rubric

**Chosen option: (c), operationalized through existing bucket structure — no new mechanism, no
rubric change.**

When `clears_all_bars` is empty for a pool (true today for magnesium — 0/18 — and for the
creatine Israeli shelf — 0/18 — per companion doc §3 and §4.1), the page:

1. **Leads with the honest finding as a stated headline**, not a buried caveat: "אף מוצר במדף
   הישראלי עובר את כל ששת הספים" (no product on the Israeli shelf clears every bar) — placed at
   the top of the products section (plan §3 layer 2), before the bucket table.
2. **Then surfaces `passes_with_flag` as the practical shortlist**, exactly as already defined
   (no bar = FAIL, at least one FLAG/CANNOT-VERIFY), unordered, each row showing its own
   bar-states inline so the reader sees precisely what is unresolved per product — not a
   generic "close enough" label.

Why this option and not (a) or (b):

- **(a) rejected** — redefining "recommended" as "no FAIL bar" would silently loosen
  `clears_all_bars`'s own meaning (it already exists and is a stricter, correctly-named bucket).
  Two buckets both trying to mean "the answer" is confusing and edges toward the exact
  stealth-endorsement risk the plan's own red-team guard exists to block. `passes_with_flag`
  already IS "no FAIL bar" — it doesn't need renaming, it needs to be surfaced more
  prominently when the top bucket is empty. Nothing in the YAML changes.
- **(b) rejected as the primary fix** — shelf-splitting is already true for creatine (worldwide
  pool naturally has 3 clears-all-bars products) and I confirm it below in §2, but it does not
  solve the actual problem for the golden guide. Magnesium has no worldwide benchmark pool at
  all today (companion §3 headline finding), so a shelf-split default pick literally cannot
  exist for magnesium at v1 — it would ship the golden guide with the identical empty-shortlist
  problem it's supposed to solve. Shelf-splitting is the right call for the *default-pick*
  question (§2) but doesn't answer the *shortlist* question on its own.
- **(c) accepted** — costs zero rubric rewrite (verified against both validation tables:
  `passes_with_flag` already has real candidates — 5/18 magnesium, 11/18 creatine-Israeli, per
  companion §3/§4.1), requires no new sortable field (so it cannot violate the anti-drift
  invariant's ban on a "closest to clearing" count), and turns the data gap itself into the
  editorial finding — which is the Bari brand posture (clarity over comfort; memory:
  `bari_brand_anchor_clarity`), not a bug to paper over.

**This is a page-shape/presentation ruling under Product's own plan §3 authority** ("Page
shape... all earn v1 per Product"), not a change to the bar rubric's bucket *definitions* —
Nutrition's YAML ships as authored. Route to Content/Frontend as a build instruction, not a
rubric amendment.

**One consequence to hold precisely in copy:** `default_pick_rule`'s empty-bucket handling
(`If clears_all_bars is empty ... NO default pick is shown`) stays exactly as Nutrition wrote
it. Headlining `passes_with_flag` answers "what should I look at," it does NOT manufacture a
default pick from a lower bucket — those are two different questions and the rubric is right to
keep them separate.

## 2. Default-pick rule under currency-pool separation — DECISION: one pick per currency pool, never one global pick

**Confirmed, no amendment needed.** One default pick per same-currency pool where
`clears_all_bars` is non-empty for that pool — never a single cross-shelf pick. Reasoning:

- The rubric already forbids FX-mixing for price_fairness itself (no invented exchange rate —
  Hard Rule 1). A single global default pick spanning ₪ and $ would either require exactly that
  invented rate, or compare raw nominal numbers across currencies, which is not a meaningful
  "cheapest" claim even without doing arithmetic on it. Both are dishonest; reject both.
- Applied to today's data (companion §4.3): creatine worldwide pool has a legitimate default
  pick (BPN, cheapest of 3 clears-all-bars worldwide products, ~$0.185/3g); creatine Israeli
  pool has none (0/18); magnesium has none (no pool clears, no benchmark pool exists).
- **Mandatory copy constraint, not a new rule — restating what the companion doc already
  flags (§4.3):** if a worldwide default pick is shown at all, it must be labeled inline as a
  *worldwide reference pick*, never phrased as an Israeli buy recommendation, since Israeli
  purchasability through this corpus's retail channels is unconfirmed for those 3 products. This
  is a copy-precision requirement for whoever builds the creatine guide, not a rubric change.

Single criterion unchanged: cheapest by price-per-effective-unit within `clears_all_bars`,
computed inside that pool only.

## 3. Bucket priority (FAIL before cannot_assess) — DECISION: confirmed correct, no change

Ratified as the right product call. A known, demonstrated problem (decorative dose, a form with
directional evidence of poor absorption, a certification claim checked and refuted) is more
actionable and more protective of a buying decision than deferring to "insufficient data" — a
known-bad product must never get to hide behind an unknown-data framing. The worked example in
the rubric (Tink Oxide-520 → `fails`, form is a known FAIL even though dose is unresolved, vs.
TRIOMAG → `cannot_assess`, nothing at all is concretely known) is the correct distinction and
matches Bari's clarity-over-comfort posture. No change requested.

## 4. D7 co-sign — GRANTED, conditional on §1/§2/§5 folding into the build (no YAML re-open)

The six bars, thresholds, blend rule, verification sub-states, and anti-drift invariant match
Bari product governance. Specifically checked against standing rules:

- **Anti-drift / no composite:** the YAML's own invariant block explicitly bans any "N/6 passed"
  number, and I independently verified no bucket or field in the config computes one — buckets
  are unordered categorical sets throughout both validation tables. **Approved.**
- **Missing-data discard doctrine** (`missing_data_discard_rule` memory — unknown is
  acceptable, never punish/cap): CANNOT-VERIFY carries zero negative inference throughout the
  config (explicit in `third_party_verification.states.CANNOT-VERIFY` and
  `label_transparency.states.CANNOT-VERIFY`). **Approved.**
- **Third-party verification 3-way split** (FAIL = checked-and-refuted vs. FLAG =
  not-yet-checked vs. CANNOT-VERIFY = never claimed): this is a refinement beyond the plan's
  literal two-tier wording, but it adds precision without adding a bar or a number — a real
  label-integrity finding (Naked Nutrition, checked, not found) is a materially different fact
  from "haven't checked yet," and collapsing them would have hidden a real finding the live data
  already surfaces. **Approved as a legitimate refinement, not scope drift.**
- **SCF-1 price-fairness resolution** (Nutrition's own spec-conflict flag against the plan's
  "per absorbed-mg" wording): correctly caught and correctly resolved. Building Price Fairness
  off the tier-adjusted absorbed-mg figure would have silently violated the standing display
  hard rule (no `adjusted_dose_mg`/`tier_factor` in consumer output) and collapsed Price
  Fairness into a restatement of Form/Absorption. Resolving to price-per-disclosed-dose (the
  same convention creatine's live data already uses) is the right call. **Confirmed correct —
  Product co-signs this resolution specifically, per the flag's own request.**
- **Blend rule:** uniform, deterministic, closes a real live inconsistency (Solgar vs. TRIOMAG
  both currently render as identical null/null). **Approved.**

**Co-sign is granted with two build-time conditions, both already named above and in §5 below —
neither requires touching the YAML:**
1. The guide build adopts the §1 presentation ruling (headline + `passes_with_flag` promotion)
   when `clears_all_bars` is empty.
2. The three flagged data/copy corrections (§5) ship with the guide, not after it.

## 5. Scope items

**Unproven delivery-tech claims ("nano liposomal", magnesium row 15 in companion §3) — OUT of
v1.** This is a real gap (no bar captures an unsubstantiated technology claim riding on an
otherwise-honest base form), and Nutrition was right to flag it rather than resolve it
unilaterally — adding a 7th bar or extending Label Transparency's scope is a genuine rubric
change requiring its own D6/D7 pass. My call: don't take that pass now. This program has already
gone through two full rounds of scope negotiation (redirection brief → concrete plan → rubric)
and the plan explicitly names the frozen-veg precedent as the risk to avoid ("that band-based
redesign stalled post-spec... mitigation: ships in ONE build wave" — plan §7). Re-opening bar
scope mid-build, on the golden guide, for one product's marketing claim, is exactly that risk.
**Handling for v1:** this is a copy-claims-discipline problem, not a scoring problem — it is
already governed by `creatine_evidence_cosign_v1.md` §3 / the science co-sign §3, which the
open_gaps note itself says "still govern what may be SAID in copy about it, independent of this
rubric." The guide's copy simply does not repeat or endorse the "nano liposomal" superiority
framing; the product's honest base-form bar-state (bisglycinate = PASS) ships as-is. **What gets
cut to pay for this deferral:** nothing new gets cut — this is a decision not to add scope, not
an addition requiring a compensating cut. If unsubstantiated technology claims turn out to be a
pattern across more products post-launch (not just this one row), that becomes a v2 rubric
proposal with real volume behind it, not a v1 speculative bar.

**The 3 flagged corrections — IN, mandatory pre-ship, not optional cleanup:**
1. California Gold Nutrition creatine capsules: reclassify from the live `below_floor` tag to
   the rubric-driven `dose_adequacy = CANNOT-VERIFY` (daily capsule count undisclosed, so the
   true daily dose is unknown, not merely low) — companion §4.1 note ‡.
2. Naked Nutrition's NSF claim: ship the `FAIL` (checked-against-registry, not found) sub-state,
   not a generic FLAG — companion §1.3.
3. `magnesium-page-data.ts`'s "EFSA (2021)" citation date (4 occurrences, lines 152/156/193/197)
   is confirmed wrong (no such EFSA opinion exists) — fix to "EFSA (2001/2015)" or no year,
   never "2021," anywhere the guide or the live page cites this figure.

These are accuracy corrections surfaced by the validation exercise, not scope additions — they
fall under the standing citation-fabrication and read-copy-before-shipping gates and should be
routed to Content/Data as pre-ship fixes for the magnesium golden guide, independent of the
guide-template build itself.

## 6. Owner escalation check — NONE OF THIS RISES TO THE OWNER

Checked against the 5 tripwires (`decision_authority_matrix_v1.md`):

1. **Frozen invariant / published scores** — no. Firewall confirmed in the YAML (0 BSIP2 file
   touches); nothing here computes or displays a composite number.
2. **Irreversible + consumer-facing** — no. Nothing ships to consumers from this memo; the
   plan's own tripwire-2 owner gate at the public flip (§6 of the concrete plan) is unaffected
   and still applies at deploy time, not now.
3. **Starts or kills a major program** — no. The program itself was already owner-approved
   (concrete plan). Every ruling above is a refinement inside that approved shape.
4. **External commitment, spend, legal exposure** — no.
5. **Redefines strategy, target user, or what Bari is** — no.

All four items (§1 empty-shortlist presentation, §2 pool-scoped default pick, §3 bucket
priority, §5 scope cut) are in-model product judgment calls, resolved here per the Autonomy
Mandate. Routing to the orchestrator for build dispatch (Content for copy/corrections, Frontend
for the guide template, per the existing plan's build order) — not to the owner.

---

## Return Contract

```json
{
  "task": "TASK-504A",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/product/supplement_guides_d7_cosign_v1.md",
      "action": "created",
      "sha256": "54bb8b1c7a9c90b6ef8df0c9f81c31d67cf26e22db2e4664c94d282f2ae2f4f4 (of the file content prior to this hash-field edit — self-referential hash of the final state cannot be embedded in itself; re-run `sha256sum` at verification time)"
    }
  ],
  "counts": {
    "magnesium_clears_all_bars": "0/18 (source: supplement_guides_bar_rubric_companion_v1.md §3 validation table + totals line)",
    "magnesium_passes_with_flag": "5/18 (source: companion doc §3 totals line — this is the promoted shortlist per §1 of this memo)",
    "creatine_israeli_clears_all_bars": "0/18 (source: companion doc §4.1 table + §4.3 totals table, Israeli row)",
    "creatine_israeli_passes_with_flag": "11/18 (source: companion doc §4.3 totals table, Israeli row)",
    "creatine_worldwide_clears_all_bars": "3/13 (source: companion doc §4.2 table + §4.3 totals table, Worldwide row — Thorne, Momentous, BPN)",
    "creatine_combined_clears_all_bars": "3/31 (source: companion doc §4.3 Combined totals row)",
    "d7_cosign_conditions_attached": "2/2 (source: this memo §4 — (1) fold in §1 presentation ruling, (2) fold in §5's 3 corrections; both required before the rubric governs published guide copy, neither requires re-opening the YAML)",
    "scope_items_ruled": "2/2 (source: this memo §5 — unproven-delivery-tech-claims ruled OUT of v1 with reasoning; the 3 flagged corrections ruled IN as mandatory pre-ship fixes)",
    "owner_tripwires_triggered": "0/5 (source: this memo §6, checked against 01_framework/governance/decision_authority_matrix_v1.md's 5-tripwire list)",
    "rubric_yaml_changes_required": "0 (source: this memo §1/§4 — all rulings operate through existing bucket structure or page-copy instructions; the YAML ships as authored by Nutrition)"
  },
  "commands_run": [],
  "not_done": [
    "No page copy drafted — this memo is a product ruling + D7 co-sign, not a build deliverable; routes to Content/Frontend per the existing concrete plan's build order",
    "No fix applied to magnesium-page-data.ts's 'EFSA (2021)' defect, the California Gold dose-tag reclassification, or the Naked Nutrition cert-severity tag — all 3 are named as mandatory pre-ship items for whoever builds the magnesium/creatine guides, not made in this memo",
    "No 7th-bar or Label Transparency scope extension for unproven delivery-tech claims — explicitly ruled OUT of v1 in §5, to be revisited only if a real pattern (not one product) emerges post-launch",
    "Nutrition Agent's own sign-off on this memo's D7 conditions (§4) not yet separately confirmed in writing — D7 requires both signatures; this memo constitutes Product's half, routes back to Nutrition/orchestrator to close the loop"
  ],
  "self_check": {
    "acceptance_test": "Co-sign (or reject with required changes) the bar rubric on D7 grounds, and resolve — with one clear recommendation each, no A/B menus — the empty-shortlist design problem, the default-pick rule under currency separation, and bucket-priority correctness; rule on the two named scope items; state plainly whether any of it needs the owner.",
    "result": "PASS",
    "evidence": "D7 co-sign granted (§4) with two named, already-actionable build conditions, zero YAML re-open required. Empty-shortlist problem resolved with a single chosen option (§1: headline the honest finding, then promote the existing passes_with_flag bucket — no new bucket, no new numeric field, verified against real data that passes_with_flag has usable candidates in every pool: 5/18 magnesium, 11/18 creatine-Israeli). Default-pick rule confirmed as one-per-currency-pool with a stated single criterion and a mandatory worldwide-vs-Israeli labeling constraint (§2). Bucket priority (FAIL before cannot_assess) ratified as correct with reasoning (§3). Both scope items ruled decisively — delivery-tech claims OUT of v1 with a stated reason and no compensating cut needed since nothing is being added, the 3 data/copy corrections IN as mandatory pre-ship fixes (§5). Owner escalation checked against all 5 tripwires and explicitly found not to apply (§6). No number in this memo was generated by Product — every count cites the companion doc's validation table by section. No subagents spawned, no pages built, no BSIP2/scoring file touched."
  }
}
```
