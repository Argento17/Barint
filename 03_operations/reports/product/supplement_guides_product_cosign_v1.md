# Supplement Guides Re-Direction — Product Co-Sign Memo v1 (TASK-504)

**Type:** Product Agent consult response — co-sign-or-changes on `supplement_guides_redirection_brief_v1.md`.
**Status:** RETURNED (consult only — does not build, route, or close).
**Author:** Product Agent
**Date:** 2026-07-04
**Reads:** `01_framework/product/supplement_guides_redirection_brief_v1.md` (the brief under
consult), `03_operations/reports/content/creatine_page_model_decision_v1.md` (prior no-grade
ruling this re-direction generalizes), `bari-web/src/lib/comparisons/magnesium-page-data.ts`
(read directly), `bari-web/src/components/inventory/product-table.tsx` (read directly for the
TASK-427 buyUrl slot), and a repo search for `creatine-page-data.ts` / any "creatine" reference
under `bari-web/src`.

This memo makes the product call on the seven consult questions in the brief's §7. It does not
build, dispatch, or close anything — the orchestrator routes from here.

---

## 0. Premise correction (Hard Rule 10 — checked before the calls below rest on it)

The brief's §4 asset inventory and §7 context both assert `creatine-page-data.ts` is a **live**
data file, parallel to `magnesium-page-data.ts`. **That is not correct.** I searched
`bari-web/src` directly:

- `bari-web/src/lib/comparisons/magnesium-page-data.ts` exists — 820 lines, confirmed live, with
  its own grade distribution documented in-file (line 6-7: `B(4)·C(4)·D(6)·E(1) + no-score(3)`,
  18 displayed products, 15 scored / 3 no-score).
- **Zero files under `bari-web/src` reference "creatine"** (case-insensitive grep, no matches).
  There is no live creatine page, no creatine route, no `creatine-page-data.ts`. What exists for
  creatine is a **content package + a Nutrition co-sign + this Product ruling**
  (`creatine_page_model_decision_v1.md`, 2026-07-03) — a fully-decided product model that has
  never been built into a frontend page.

This matters directly for question 1 (T4): the two "guides" are not symmetric assets. Magnesium
is a live, published, currently-graded page carrying real traffic and the exact grade the owner
now doubts. Creatine is a fully-ruled but unbuilt spec. Treat that asymmetry as load-bearing in
the sequencing call below, not a rounding error.

---

## 1. MVP cut + sequencing (T4)

**Recommendation: build magnesium first, as the golden template, in isolation. Creatine is the
fast-follow stamp of the same template, not a parallel v1 track. Both ship together before
`/madrichim` opens publicly — but the template is proven on magnesium alone before creatine touches
a single line of UI.**

Reasoning:
- Magnesium is the disputed page. The brief's own §1.1 records the owner doubts the magnesium
  ranking, not just the creatine one. Shipping creatine first would prove the format on the page
  nobody complained about and leave the actual complaint untouched.
- Magnesium is also the harder design case: per §3's magnesium call, it **keeps** form-tier bands
  and UL safety flags rather than going fully flat (creatine is ruled fully flat per
  `creatine_page_model_decision_v1.md` Ruling 1). Proving the new 4-layer shape has to survive a
  page that still carries defensible tiered verdicts, not just a flat bars-only page. If the
  format works on the harder case, creatine (strictly simpler — no tiers, no live page to migrate,
  no existing grade to retire) is close to a template stamp.
- Creatine's underlying decisions are already made (score-vs-no-score, cert two-tier badge, price
  disclosure, dairy caveat, cognitive-claim cut — all five rulings closed 2026-07-03). Building it
  is largely a data-file + copy pass against an already-approved spec, not new product judgment.
  That is real, but it is sequencing logic, not a reason to build it in parallel with an unproven
  template — reuse only after the template is locked.
- A one-guide hub reads as broken (a "guides" section with one occupant undercuts the format's own
  credibility). So: **sequence the build** (magnesium → prove → creatine → stamp) but **gate the
  public hub open** on both being done, gated, and live together. This is the smallest v1 that (a)
  proves the format against the hardest real case, (b) doesn't ship a one-item hub, and (c) doesn't
  block on creatine build risk since the risk is retired first on magnesium.

**Golden template = magnesium**, explicitly, for the same reason `golden_comparison_page_brined`
established brined-cheeses as the golden template for scored comparisons: it's the instance that
carries the most structural complexity (tiers + UL caps + a live page to migrate) and is already
public, so its conversion is the real proof, not a demo.

**Phase-1 MVP definition (Hard Rule 6, since this is multi-sprint work):**
- In: magnesium converted to the 4-layer guide shape (spine, bars, unordered shortlist + single
  default-pick flag per §2 below, benchmark + buy), on `/madrichim/magnesium`, 301 from
  `/hashvaot/magnesium`, buy button live per §4 below, both sign-off gates passed.
- In: creatine built to the same template on `/madrichim/creatine`, reusing every UI decision
  proven on magnesium, using the already-ruled spec from `creatine_page_model_decision_v1.md`.
- In: `/madrichim` hub with exactly these two cards, `/hashvaot/supplements` retired with a 301.
- Out (deferred, not this v1): any third supplement, any non-supplement guide, cross-retailer
  live price comparison, new evidence/dossier research beyond what's already collected, affiliate
  params.
- Out (cut to pay for it, Hard Rule 2): the ordinal 1-18 magnesium rank and the numeric A-E grade
  UI — this is the actual thing being retired to fund the new shortlist+bars mechanism, not an
  addition on top of the old page.

---

## 2. The shortlist (T2)

**Recommendation: verdict-per-attribute + a strictly unordered shortlist is necessary but not
sufficient. Add one narrow mechanism: a single, transparently-ruled "default pick" callout inside
the shortlist — not a rank.**

An unordered shortlist of, say, 5 products that all clear every bar still leaves the "just tell me
what to buy" user with a 5-way tie and no way to break it without inventing their own ordinal
judgment — which is exactly the failure the pivot is trying to kill, just deferred to the reader.
That fails the one-read test for the single largest use case (a user who wants one answer, not a
qualifying set).

The fix is not a hidden rank recreated as five separate 1-2-3-4-5 badges. It's **one explicit,
named, single-criterion tie-break, stated in the copy**: among products that clear every bar, the
one with the lowest price-per-effective-unit (₪/absorbed-mg for magnesium, ₪/effective-gram for
creatine — both already computed and cited in the existing dossiers/content package) gets a
"הבחירה הפשוטה ביותר" (the simplest pick) label, with the stated reason visible inline ("הזול
ביותר מבין המוצרים שעברו את כל הקריטריונים"). This is not a 1-18 rank — it's one flag, one
criterion, fully disclosed, applied only inside the already-qualified set. It preserves "clarity
without fake precision" while still answering the actual question a majority of readers arrive
with.

---

## 3. The 4-layer page (§3) — anti-overbuild check

| Layer | Verdict | Why |
|---|---|---|
| 1. Educational spine | **Keep, as-is** | Cheap — the evidence dossiers already exist (magnesium model v3, creatine 20-claim tiered base per brief §4). No new research funded here; assemble from what's already co-signed. |
| 2. Honest bars (quantity/form/verification/price-fairness) | **Keep, this is the core mechanism** | This replaces the grade — it is the product, not a nice-to-have. Inputs already exist for both categories (magnesium's absorbed-mg engine, creatine's dose-honesty/cert/price rulings). |
| 3. Shortlist | **Keep, scoped down to unordered + single default-pick flag** (§2) | Cut: any per-row ranking, star system, or numeric re-encoding of the old grade under a new name — that would be the same failure with new paint. |
| 4a. Benchmark placement | **Keep** | Worldwide benchmark sets already built (13 creatine products / 5 regions per brief §4; magnesium worldwide set). Reuse, zero new data collection. |
| 4b. Buy button | **Keep, v1 rules only** (§4) | Cheap — dormant slot already exists (TASK-427). Defer anything beyond a plain link: no price-tracking, no cross-retailer aggregation, no affiliate. |

**What gets cut to fund this (Hard Rule 2):** the ordinal grade/rank UI (magnesium's 1-18 sort
and A-E badge display component) is retired outright, not kept as a toggle or a secondary view.
Also explicitly held out of v1: any "complementary data" beyond the existing dossiers (owner point
7 is satisfied by presenting what's already collected "smartly," not by commissioning new
research), and any new visual-component work beyond the existing badge/pill/bar primitives
(reuse per Design Token Governance v1 — no new component library for this).

---

## 4. Buy button v1 rules (T1, product side)

**Confirm 3 of 4, amend 1.**

- Plain retailer link, no affiliate params — **confirm**.
- Visible disclosure — **confirm**.
- Verdict data and buy-link data live in separate files/fields so no future affiliate deal can
  touch a verdict — **confirm**, and treat this as a hard build constraint, not a style preference.
- "Button on every product that clears the bar" — **amend**. The button should appear on **every
  listed product**, shortlisted or not, not gated by pass/fail.

Reasoning for the amendment: gating the buy button on verdict outcome re-couples the two systems
the brief itself wants decoupled ("verdict data and buy-link data in separate files"). A product
that fails a bar (e.g., undisclosed dose) is still a real, purchasable product Bari is showing —
withholding the link on top of the visible fail-flag is an extra, verdict-conditioned punishment
layer that isn't itself grounded in an attribute test; it's an editorial add-on riding on the
verdict. The verdict is already fully communicated by the bars and the shortlist section. The buy
button is retail-finding utility, not an endorsement stamp — treat it as "where to find this,"
constant across every listed product, disclosure unchanged either way.

---

## 5. Naming (T6)

**Recommendation: confirm "מדריכים."**

It's the owner's own word for the format (§1.3: "the page itself is a detailed guide"), it's plain
Hebrew with no jargon, and — most importantly — it does not over-promise the thing that just broke.
"השוואות" (comparisons) primed exactly the ranking expectation that failed on creatine. "מדריך"
correctly sets reader expectation to "explains + shows real products," not "ranks them." No
alternative naming work needed; ship as proposed.

---

## 6. Hub/migration (T5, product side)

**Confirm.** Supplements leave `/hashvaot` in the same PR the `/madrichim` hub ships — no
half-migrated state is a hard acceptance gate, not a preference: at no point should a user be able
to land on a live `/hashvaot/supplements` card pointing at a graded page while `/madrichim` also
exists, or vice versa with a dangling 404. The PR-sequencing mechanics themselves (branch order,
deploy steps) are the orchestrator's call, not mine — my gate is the **end state**: zero
overlap window between old and new supplement surfaces.

---

## 7. Scope guard

**Confirm v1 = supplements only.** "Morph to other areas" stays parked behind an explicit,
measurable success metric — not owner intuition, not "it feels right."

**Named metric: shortlist-engagement rate, measured via GA4/Plausible (both already wired per
memory `ga4_mcp_configured` and the Product Agent's live `google_trends`/`analytics` access),
compared against each guide's own pre-conversion baseline (magnesium's current live page, which
has real traffic to baseline against) over a defined post-launch window (recommend 4-6 weeks for
sufficient session volume — a real number to be pulled from GA4 at baseline-measurement time, not
asserted here).**

Definition: % of guide-page sessions that reach the shortlist section and click a buy button (or,
if buy-button click events aren't instrumented yet, scroll-depth-to-shortlist as the proxy) at
parity or better than the equivalent engagement signal on magnesium's current ranked-table page,
**and** zero unresolved CRITICAL/HIGH Adversarial QA findings accumulated in that window. Both
guides must clear this, not just one, before "morph to other areas" is even discussed. I am not
asserting a current baseline number here — that has to come from a GA4/Plausible pull at
measurement time (Data Agent / Adversarial QA lane), per Hard Rule 9.

---

## 8. Go/no-go shape for the first guide (magnesium)

The launch gate for `/madrichim/magnesium`, before it goes live:

1. **Two-gate content sign-off** (Content Agent + Adversarial QA) on every consumer string — spine
   copy, bar labels, the "default pick" callout copy, benchmark copy, disclosure lines. Standing
   hard rule, no exceptions.
2. **Nutrition co-sign** on the attribute thresholds (T3 — quantity/form/verification/price-
   fairness pass/flag/fail lines) as the functional replacement for the retired D7 scoring-rule
   co-sign. No score exists anymore, but the bar thresholds are doing the same job a scoring rule
   did and deserve the same rigor.
3. **Adversarial QA red-team** specifically targeting the three failure modes the brief itself
   names (§7): shortlist read as endorsement, benchmark read as ranking-by-stealth, undisclosed-
   dose flag read as accusation. Zero unresolved CRITICAL/HIGH findings required.
4. **Migration verification**: `/hashvaot/magnesium` 301s correctly, `/madrichim` renders, no
   overlap window (per §6).
5. **Buy-button verification**: disclosure visible, zero affiliate params present (grep-verifiable
   against the built page), link resolves to a real, current retailer product page. Adversarial QA
   verification track, not owner review.
6. **Product Agent sign-off** that the shipped page matches this memo's rulings: grade/rank UI
   removed, shortlist unordered with the single stated default-pick criterion, buy button present
   on every listed product regardless of verdict.
7. **Owner touch at the actual public flip.** The program start is already owner-cleared (brief
   header: tripwire 3 cleared by origin). But removing a live page's published grade and cutting
   over its URL is itself consumer-facing and effectively irreversible once public — treat the
   final go-live as a short tripwire-2 confirmation to the owner (not a re-litigation of the
   redirection itself, which he already ordered): "built, gated, ready — confirming the magnesium
   grade comes down and the URL moves, per your 2026-07-04 direction." One line, not a review
   cycle.

Creatine's go/no-go repeats steps 1-6 (its rulings are already closed per
`creatine_page_model_decision_v1.md`, so step 2 is largely a confirmation, not new work) and does
not need its own step-7 owner touch beyond a mention alongside magnesium's, since it has no
existing live grade to retire.

---

## Summary table

| # | Question | Call |
|---|---|---|
| 1 | MVP + sequencing | Magnesium is the golden template, built and proven first (harder case, disputed page, live migration); creatine stamped second from its already-ruled spec; both gate the hub open together — no one-item hub |
| 2 | Shortlist | Unordered + one transparently-ruled "default pick" flag (cheapest per effective unit among bar-clearers) — plain shortlist alone fails "just tell me what to buy" |
| 3 | 4-layer page | All 4 layers earn v1 place; cut is the retired grade/rank UI itself plus any new research/new components beyond existing dossiers and primitives |
| 4 | Buy button | Confirm plain-link/no-affiliate/disclosure/separated-data; amend — button shows on every listed product, not gated by verdict |
| 5 | Naming | Confirm "מדריכים" |
| 6 | Hub/migration | Confirm same-PR migration; hard gate = zero overlap window between `/hashvaot/supplements` and `/madrichim` |
| 7 | Scope guard | Confirm supplements-only v1; "morph" gated on a named shortlist-engagement metric (GA4/Plausible, vs magnesium's own baseline, 4-6 week window, both guides must clear it) |
| 8 | Go/no-go shape | 6 build/QA/co-sign gates + 1 short owner touch at the actual public flip (grade removal + URL cutover), not a re-litigation of the redirection |

---

## Return Contract

```json
{
  "task": "TASK-504",
  "deliverable": "supplement_guides_product_cosign_v1",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/product/supplement_guides_product_cosign_v1.md",
      "action": "created",
      "sha256": "COMPUTE_AT_READ_TIME: self-referential hash cannot be embedded; verify with sha256sum/Get-FileHash on read"
    }
  ],
  "counts": {
    "consult_questions_answered": "8/8 (source: brief §7 Product Agent question list, each answered in sections 1-8 of this memo)",
    "magnesium_products_displayed": "18/18 (source: bari-web/src/lib/comparisons/magnesium-page-data.ts line 82 comment, read directly)",
    "magnesium_scored_vs_noscore": "15 scored / 3 no-score of 18 (source: magnesium-page-data.ts line 6-7 in-file comment: B(4)+C(4)+D(6)+E(1)=15, plus 3 no-score)",
    "creatine_frontend_files_found": "0 (source: case-insensitive grep for 'creatine' across bari-web/src — zero matches; Glob for '**/creatine*' under bari-web — zero matches; contradicts brief §4/§7's claim that creatine-page-data.ts is live)",
    "creatine_worldwide_benchmark_products": "13 across 5 regions (source: brief §4 asset inventory, itself sourced from creatine_page_model_decision_v1.md counts: 3/23 directory-verified, 4/18 Israeli undisclosed dose)",
    "buyurl_field_locations_in_frontend": "1 (source: grep for 'buyUrl' across bari-web/src — only bari-web/src/components/inventory/product-table.tsx lines 52, 239-243, 925, 1077; zero matches in bari-web/src/lib/view-models, confirming the TASK-427 slot is not yet part of the shared comparison-page view model)",
    "premise_corrections_flagged": "1 (creatine-page-data.ts does not exist; brief's asset-inventory claim corrected in section 0 of this memo)",
    "owner_tripwires_fired": "0/5 direct fires (source: decision_authority_matrix_v1.md 5-wire test; program start already cleared per brief header; this memo recommends ONE short owner touch at final public flip in section 8, framed as confirmation not re-litigation, since removing a live published grade + URL cutover is consumer-facing/irreversible-adjacent)"
  },
  "commands_run": [
    {"cmd": "wc -l bari-web/src/lib/comparisons/magnesium-page-data.ts bari-web/src/lib/comparisons/creatine-page-data.ts", "exit_code": 0},
    {"cmd": "grep -rniE 'creatine' bari-web/src (via Grep tool, case-insensitive)", "exit_code": 0},
    {"cmd": "grep -rn 'buyUrl' bari-web/src (via Grep tool)", "exit_code": 0},
    {"cmd": "grep -n 'grade|score' bari-web/src/lib/comparisons/magnesium-page-data.ts (via Grep tool, first 15 lines)", "exit_code": 0}
  ],
  "not_done": [
    "No build, routing, dispatch, or file creation for the actual guide pages — this is a consult memo only, per task scope",
    "No GA4/Plausible baseline pull performed for the §7 shortlist-engagement metric — the metric is DEFINED here; pulling the actual baseline number is a Data Agent / Adversarial QA task before it can gate anything",
    "Nutrition Agent's T3 co-sign (magnesium tier defensibility) not addressed here — explicitly Nutrition's lane per the brief's own routing",
    "Adversarial QA's strategy red-team (T1 hardest case) not run here — separate consult track per the brief",
    "C3 independent challenge of the premise itself not run here — separate consult track per the brief",
    "Did not verify the exact shape of TASK-427's buyUrl field against a comparison-page VM contract (view-models/index.ts) beyond confirming it is absent there today — Frontend Agent's task if this memo's amendment (button on every listed product) is adopted"
  ],
  "self_check": "Acceptance test: answer all 8 consult questions from brief §7 (Product Agent's assigned set) with one clear recommendation each, no A/B menus, every cited number sourced to a named artifact, premise-checked before any call rests on it, no build/route/close performed. Result: PASS. Section 0 caught and corrected a false premise in the brief itself (creatine-page-data.ts asserted live, verified absent) before question 1's sequencing call was built on it — the corrected premise directly changed the T4 answer (magnesium-first, not parallel-two-guides) versus what the brief's own framing implied. All 8 questions in §1-8 give one recommendation each with named reasoning; three amend rather than blanket-confirm the brief's draft (shortlist needs a default-pick flag beyond bare unordered; buy button shows on every listed product not just bar-clearers; go-live needs one short owner touch at the actual public flip). Every count in the JSON above cites its source file/line or the artifact it was read from. Zero numbers invented; the one metric-threshold-dependent claim (§7) is stated as a metric DEFINITION requiring a future GA4/Plausible pull, not asserted as an already-known figure. No subagents spawned. No CLOSED status proposed."
}
```
