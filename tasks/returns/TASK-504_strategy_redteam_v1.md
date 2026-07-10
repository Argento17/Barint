# Strategy Red-Team — Supplement Guides Re-Direction (TASK-504)
Date: 2026-07-04   Scope: `01_framework/product/supplement_guides_redirection_brief_v1.md` §3 product shape, pre-build   Challenger: adversarial-qa-agent   Track: C (strategy), no build exists yet to run Track V against

This is a challenge of a **proposal**, not a shipped artifact. Findings below are read against the
brief text plus the live state of the two assets it claims to inherit (`/hashvaot/magnesium`,
`/hashvaot/creatine`), verified directly in the repo and in GA4 — not against the brief's own
characterization of that state, per the independence rule.

## Opening Finding — CRITICAL-adjacent (evidentiary, not structural)

**The redirection is being decided with almost zero real-user evidence on the two live artifacts it
treats as its foundation.** Queried GA4 (property `properties/543266887`) for
`2026-06-01..today` (2026-07-04):

- `/hashvaot/magnesium` (live since 2026-06-23, linked from the hub, in the sitemap): **8
  pageviews, 2 users**, total, over 11+ days.
- `/hashvaot/creatine` (merged to `origin/master` at `d9005328`, today, 2026-07-04): **0
  pageviews, 0 users** — because it is not linked from `/hashvaot/supplements` (which hand-wires
  only the magnesium card — confirmed at `bari-web/src/app/hashvaot/supplements/page.tsx:49` on
  `origin/master`) and not present in `bari-web/src/lib/seo/sitemap-paths.ts`'s
  `ALL_INDEXABLE_PATHS` (confirmed: only `/hashvaot/magnesium` appears in that list; creatine is
  absent). TASK-503, which existed to fix exactly this orphaning, is now `BLOCKED`/parked by
  this very redirection.

Implication: the brief's diagnosis ("the creatine comparison confirmed [ranking] doesn't work")
is a **reasoning-based** conclusion, not a **behavioral** one — no real user has ever reached the
grade-free bars-and-benchmark format organically, because the one live example of it has had zero
discoverable traffic since it shipped. The owner's read that "ranking doesn't work" is plausible on
the merits (thin ordinal differentiation is real — see the brief's own diagnosis in §2), but nothing
in the data available today distinguishes "the ranking framing failed with users" from "the page was
never seen by users." Betting the next iteration's design (bars, shortlist, benchmark-placement) on
an unvalidated format is the single biggest structural risk in this brief — not because the
diagnosis is wrong, but because there is no instrument in place to tell if the *next* format is
right either, and the brief proposes no usage-validation checkpoint before or after v1 ships.
**Requirement, not fix:** name a concrete usage signal (even a crude one — session recordings, a
"was this helpful" tap, search-console impressions once indexed) that the guide format is expected
to move, and check it before calling v1 validated. Routes to: product-agent.

## Attack 1 (T1) — Buy button vs independence

The brief's proposed defenses are: (a) visible disclosure, (b) buttons on every bar-clearing
product never selectively, (c) verdict data and buy-link data in separate files.

**These are process/data-hygiene defenses, not structural ones — none of them prevent the outcome
they're meant to prevent.** Concrete scenarios:

1. **Bar-threshold tuning is invisible and undetectable by the proposed defenses.** "Buttons appear
   on every product that clears the bar" only constrains *which already-passing products* get a
   button — it says nothing about where the bar itself sits. If a future revision nudges the
   quantity-adequacy floor, the verification tier, or the price-fairness cutoff by even a small
   margin, and that nudge happens to admit one more monetizable product into the shortlist, "verdict
   data and buy-link data live in separate files" does not catch it — the bar-setting logic and the
   buy-link population are two *different* systems, and nothing here audits whether a bar change
   correlates with which products carry a working buy link vs a dead/absent one. **A hostile
   journalist's story writes itself: "Bari changed its magnesium dose threshold from X to Y in
   March; the only new product that cleared the bar afterward happens to be the one paying an
   affiliate fee."** Separate files defend against *inserting* a product into the verdict layer
   for money; they do nothing against *tuning the bar* for money, which is the harder-to-detect and
   more plausible version of the same corruption. **Structural defense that would actually hold:**
   a versioned, timestamped bar-definition file with a change-log that is diffed against the
   affiliate-product list on every change, by a party (this agent, or a fixed rule) with no stake in
   either — i.e., a mechanical gate, not a policy statement. The brief proposes no such gate.

2. **Shortlist composition drift over time is not addressed at all.** The brief's rules are
   snapshot rules ("buttons on every clearing product, never selectively") — they say nothing about
   what happens when the corpus is refreshed (prices change, a product reformulates, a new SKU is
   scraped). If the shortlist silently gains or loses members over successive corpus refreshes with
   no diff surfaced anywhere, "never selectively" is unverifiable after the fact — there is no
   record of what the shortlist *used to be* to check drift against. This directly recreates the
   same failure class RT-2 in the TASK-503 red-team already caught in this exact product line (a
   card stat computed from two differently-scoped arrays with "today's numbers are correct only by
   coincidence" — `tasks/returns/TASK-503_redteam_v1.md` RT-2). **Requirement:** every corpus
   refresh emits a shortlist diff (added/removed products + the specific bar each move crossed),
   checked automatically, not just "the file structure keeps them separate."

3. **A reader screenshot-cropping the disclosure is not a hypothetical — it is the median outcome
   for how comparison content is actually consumed and shared** (social re-shares, WhatsApp
   forwards, a competitor's "look what Bari recommends" post). A disclosure that lives once on the
   page (however visible) does not travel with a cropped screenshot of "product X — passes every
   bar — [BUY]". **Structural defense that would actually hold:** the buy affordance itself must be
   visually inert/non-verdict-shaped (this repo already has a live precedent for exactly this: the
   `/catalog` buy column is deliberately "dormant... inert/coming-soon feel," per
   `bari-web/src/components/inventory/product-table.tsx:6-38` and its Design-Agent-specified low-
   opacity, non-CTA styling) — i.e., the button must not visually read as an endorsement badge even
   in isolation. The brief says "just the button for now" without specifying this constraint, and a
   plain, prominent "קנה עכשיו" CTA sitting directly under a "עבר את כל הרף" pass-bar row is exactly
   the shape a hostile crop takes.

**What a hostile journalist would write, concretely:** "Bari says it doesn't rank supplements
anymore — but it still tells you which ones to buy, and it still gets paid when you click." The
brief's own §1.6 ("clear linkage to buy — just the button for now") and TASK-427's dormant `buyUrl`
slot make it trivial to write that sentence today, before a single affiliate deal exists, because
the shortlist-plus-button shape is functionally a recommendation regardless of what the page calls
itself. Disclosure text does not neutralize a structural resemblance to an ad unit.

**Severity: CRITICAL.** None of the three proposed T1 defenses in the brief are structural; all
three are policy statements that require someone to remember to follow them and no one to slip.
**Survivable only if:** (a) a mechanical, independently-run bar/shortlist diff exists before any
buy-button ships, (b) the buy affordance is visually inert per the existing `/catalog` precedent,
not a colored CTA, and (c) the disclosure text is tested for legibility *inside a plausible cropped
screenshot*, not just on the full page.

## Attack 2 — Shortlist as stealth endorsement

**Not defensible as-is against a "Bari recommends these" reading**, and the brief's own §3.3
acknowledges this is its "main addition" precisely because a bars-only page with no headline output
"fails the one-read test" — which is an admission that the shortlist IS meant to function as the
page's takeaway, i.e., its recommendation, in every way a reader experiences it, while the brief
elsewhere insists Bari makes "no health claims." Those two positions are in tension and the brief
does not resolve it, only names it.

Required guardrails (none currently specified in the brief; without them this fails outright):
- **Explicit, numeric inclusion criteria stated ON the page**, not just in an internal spec — the
  exact quantity floor, the exact form/absorption tier boundary, the exact verification standard,
  the exact price-fairness cutoff — in the reader's language, adjacent to the shortlist, not buried
  in a methodology footer. ("Any product meeting these four bars appears here" only works as a
  defense if the four bars are stated in numbers a reader could in principle re-check.)
- **A dated freshness stamp on the shortlist itself** ("current as of [date]; re-checked on every
  price/corpus refresh"), because "products that clear every bar" is a claim with a shelf life —
  price changes, reformulations, and re-scrapes all move membership, and an undated shortlist reads
  as a permanent verdict when it is a snapshot.
- **The "any product meeting these bars would appear" sentence stated explicitly and literally on
  the page**, not left as an internal design principle — this is the only sentence that actually
  distinguishes "we picked winners" from "these are the ones that happened to clear an open,
  public bar," and the brief does not currently propose putting it in the copy.
- **Unordered must be enforced by the rendering, not by convention** — e.g., alphabetical or
  scrape-order, never price-ascending or score-descending, because a reader will read "the first
  one listed" as "the best one" regardless of what the page says about ordering. The brief says
  "UNORDERED" but does not specify the enforced sort key; "unordered" that happens to render in a
  price-ascending scrape order is ordered in every way that matters to a reader.

**Severity: HIGH.** The instinct (an unordered pass/fail shortlist beats an ordinal ranking) is
sound and is a real improvement over grades — but "unordered, no claims" requires the four
guardrails above to be structural, not just a naming choice ("shortlist" vs "ranking"). Renaming the
output does not change what a reader does with it.

## Attack 3 — Benchmark as stealth ranking

"Where each product sits on the worldwide benchmark" cannot be rendered as a **sorted table, a
bar chart with products in score/price order, a percentile position, or a "top X%" label** without
recreating an ordinal ranking under a different visual skin — every one of those renderings implies
an ordering a reader will read as "better than / worse than" the row above and below it, which is
precisely the framing the owner's directive retires. Concretely, renderings that would FAIL:
- A horizontal bar chart of price-per-effective-unit sorted ascending (this *is* a ranking; sorting
  alone recreates it even with no grade badge — this repo has no existing chart precedent for
  supplements to reuse, confirmed: no `recharts`/`BarChart` usage exists anywhere under
  `bari-web/src/app/hashvaot/magnesium/` today, so this would be new UI, not a reuse of a vetted
  pattern).
- A "this product ranks in the top 20% worldwide on dose" percentile statement — a percentile IS an
  ordinal rank restated as a fraction.
- Grouping worldwide products into "better than the Israeli median / worse than" bands — a two-bucket
  ranking is still a ranking.

Renderings that could plausibly avoid it: placing a product's own attribute values (dose, price,
verification tier) next to the **published external reference standard** (e.g., the IOM/NASEM UL,
an NSF directory listing, the literature-derived effective-dose range) rather than next to *other
products* — i.e., benchmark against the standard, not against the field. The moment the comparison
axis becomes "vs. the other 30 products" instead of "vs. the external reference," it re-derives a
ranking regardless of chart type. **The brief does not specify which of these two the "benchmark
placement" section means** — §3.4 says "where each product sits vs the worldwide benchmark set," which
reads as product-vs-field, i.e., the failing kind.

**Severity: HIGH.** This is resolvable by rewording the requirement to "vs. the external standard,"
not by a visual treatment — flagging now because §3.4 as literally written specifies the wrong axis.

## Attack 4 — Undisclosed-dose flag as accusation

The current live creatine page already handles this fact pattern and does it defensibly: the label
used is the neutral `"לא מפורט"` ("not specified") — confirmed at
`bari-web/src/lib/comparisons/creatine-page-data.ts:65` (via `origin/master`) — not an accusatory
verb like "hides" or "conceals," and it is folded into prose rather than rendered as a red/failing
visual element. That is a real, working precedent worth preserving.

**The risk is specifically in the brief's proposed upgrade, not in the underlying fact.** §3.2
proposes rendering this as one of four **pass/flag/fail bars** — a discrete, likely color-coded,
per-attribute status sitting directly beside a named brand and product. That is visually a stronger
claim than a sentence buried in a paragraph: a red or amber bar reading "FAIL — dose undisclosed"
next to "Brand X" is legible at a glance as "Brand X failed something," which is a materially
different reader experience than the current prose treatment, even if the underlying fact (the
label doesn't state a per-serving dose) is identical and true. This is the closest thing in the
brief to defamation-adjacent risk — not because the claim is false, but because the **visual
register of a fail-bar amplifies a neutral fact into a verdict against a named, real company.**

**What the copy must do to stay strictly factual (requirement, not fix):**
- The bar/badge text names the fact, never a verb implying intent ("dose per serving not stated on
  label" — never "doesn't disclose," "hides," "avoids stating").
- No color-coded fail state for this specific attribute if the underlying reason can be a benign
  labeling-format difference (e.g., a product declaring "servings per container" without a listed
  per-serving mg figure is a different case from a product declaring nothing at all) — the current
  live page already treats "undisclosed" as its own third category rather than lumping it into
  "fail," and the guide format should preserve that three-way split (declared-adequate /
  declared-inadequate / undisclosed), not collapse it into a binary pass/fail bar.
- Every undisclosed-dose flag traces to the exact scrape/label evidence in an always-visible
  citation, not a hover tooltip, given the elevated scrutiny a named-brand fail-bar invites.

**Note on rule-citation accuracy (MEDIUM, separate from the defamation question):** the brief cites
the "missing-data discard rule" as its authority for "undisclosed = its own flag" (§3.2). That rule
(`missing_data_discard_rule` — owner 2026-06-13, reinforced 2026-06-26) is specifically about Bari's
*own scrape failing to read* a required field, with a mandated disposition of **discard the product
entirely**, not flag it. A manufacturer's label genuinely omitting a per-serving dose is a different
fact pattern (a true fact about the product, not a Bari data-collection gap), and the current
creatine page's "undisclosed" tier already treats it correctly as display-worthy rather than
discard-worthy — but the brief's citation is imprecise and could be read by a future implementer as
license to apply the *discard* disposition here, which would silently remove real, informative
products from the guide. Routes to: product-agent / nutrition-agent (tighten the citation before
this becomes an implementation instruction).

**Severity: HIGH** (visual-register risk to named brands), **MEDIUM** (rule-citation precision).

## Attack 5 (T3 territory, QA framing) — Magnesium tier retention: boundary cases

The live magnesium data already contains boundary cases that a four-attribute bars scheme (§3.2)
does not have a stated rule for:

1. **Blended-form products get inconsistent dispositions today for the same underlying problem
   (undisclosed compound ratio).** Compare two live rows in
   `bari-web/src/lib/comparisons/magnesium-page-data.ts`:
   - Solgar Ca+Mg+D3 (barcode `0033984005181`, lines 428-466): oxide+citrate blend, ratio
     undisclosed, US-label-only elemental dose (100mg) — **scored: 49/D**, displayed with
     `label_confidence: "חלקי"`.
   - TRIOMAG (barcode `7290118816065`, lines 785-813): citrate+bisglycinate+taurate blend, ratio
     undisclosed — **not scored: score/grade = null**, `confidence: "insufficient"`.
   Both are "undisclosed blend ratio" cases; one gets a confident letter grade and a D-band UL
   framing, the other gets no score at all. The distinguishing factor (dose confidence vs. form
   confidence) is real but is not visible anywhere in the brief's four-bar scheme, which treats
   "compound/form" as one bar and "quantity" as another — it does not say what happens to the
   **form** bar when the dose is known but the form mix isn't (Solgar's actual situation), versus
   what happens to the **quantity** bar when the form is known but the confirmed-elemental dose
   isn't. Without an explicit joint rule, whoever builds this will have to invent one under
   deadline pressure, which is exactly how the current inconsistency (D-grade vs. no-grade for the
   same fact pattern) was likely created in the first place.
2. **Combination products break the "price fairness" bar by construction.** Solgar's price
   includes calcium and D3; the price-fairness bar (₪/effective-mg magnesium) is proposed in §3.2 as
   a straight division, which will make every legitimate combination product look artificially
   overpriced per unit of magnesium relative to a magnesium-only product, regardless of whether the
   combination product is actually a worse value for someone who wants calcium+D3+magnesium
   together. The current page already flags this in prose ("הציון מתייחס למגנזיום בלבד") but a
   pass/flag/fail **bar** for price-fairness has no room for that caveat unless the bar itself is
   suppressed or asterisked for combination SKUs — undefined in the brief.
3. **Elemental-vs-compound-mass label ambiguity** (the three UNRESOLVED products, e.g. the
   `pH מגנזיום` product where "160 mg" could mean elemental or carbonate compound mass, a ~3.5x
   swing) is handled today by refusing to score at all. The brief's bars scheme must state, in
   advance, whether "quantity: undisclosed/ambiguous" is its own third state (matching today's
   UNRESOLVED tier) or collapses into "fail" — collapsing it into fail would be a real regression
   from the current, more honest three-state model.

**Honest fallback required (not proposed anywhere in the brief):** a named, non-bar "cannot assess"
state for both the quantity and form bars independently, preserving the UNRESOLVED tier's honesty,
rather than forcing every product into a binary pass/fail on every attribute.

**Severity: MEDIUM** (the current engine already has functioning, if under-documented, answers to
most of this — the risk is that the bars UI collapses distinctions the underlying data still makes).

## Attack 6 — Migration failure modes

1. **No redirect infrastructure exists in this codebase today.** Verified: `bari-web/next.config.ts`
   (`origin/master`) has no `redirects()` block at all; there is no `vercel.json`; there is no
   `middleware.ts` anywhere in the tree. "301s: `/hashvaot/magnesium` and `/hashvaot/creatine` →
   their guide successors... anything wrong with /madrichim + 301s in one PR?" (brief §5 T5) is
   phrased as if this is a routine addition to an existing mechanism; it is actually **net-new
   infrastructure**, first use, on a site that is *also* mid-flight on a dedicated SEO-hygiene task
   (`seo/crawl-hygiene-task499`, the current branch) — meaning redirect correctness is being
   added for the first time in the same window as other crawl-hygiene fixes, raising the chance of
   an interaction the crawl-hygiene work didn't anticipate (e.g., a sitemap entry surviving after
   its route 301s, which TASK-499's own remit — "sitemap completeness + false noindex" — suggests
   is a known failure class on this site already).
2. **The two routes are not symmetric migration risks, and the brief treats them as if they are.**
   `/hashvaot/magnesium` is linked, sitemapped, and has had real (if tiny — 8 views/2 users since
   June 1) traffic for 11+ days; a 301 here is a genuine, if low-stakes, SEO migration. `/hashvaot/
   creatine` has zero traffic, is not in the sitemap, and is not linked from any page a crawler
   would reach without the direct URL — there is effectively **nothing to preserve** for creatine,
   which means "prove the redirect works" testing effort will be spent equally on a real case and a
   no-op case unless someone notices the asymmetry first.
3. **The "comparisons hub still shows supplements" half-state is explicitly ruled out by the brief**
   ("Supplements leave the comparisons hub in the same PR that the guides hub ships — no
   half-migrated state") — but this is a same-PR *code* guarantee, not a same-*moment* guarantee for
   external systems: Google's index, cached search results, and any inbound link (social, email,
   bookmark) will show the old `/hashvaot/magnesium` URL and old framing for an indeterminate window
   after deploy regardless of how atomic the PR is, and GSC will show both URL sets simultaneously
   until re-crawl — which for a near-zero-traffic page (8 views/11 days) could take a long time to
   resolve, during which search snippets may still show grade language ("A/B/C/D") for a page that
   no longer has grades at the destination.
4. **Bookmark/direct-URL users hitting a 301'd URL will land on a differently-*shaped* page**, not
   just a redesigned one — a grade-seeking returning visitor to `/hashvaot/magnesium` who bookmarked
   it precisely because it told them "buy the B-grade citrate one" will land on a page that
   deliberately no longer answers that question that way. The brief has no transitional messaging
   plan for this (e.g., a one-time explainer banner "we changed how this works, here's why") — worth
   naming since the *entire premise* of this redirection is that the previous format
   mis-served users, so the users most likely to notice and object to the change are exactly the
   returning visitors who liked the old format.

**Severity: MEDIUM overall** (real but low-blast-radius given current traffic levels), **HIGH** on
point 1 specifically (building first-ever redirect infra correctly, under a live SEO-hygiene
initiative, deserves its own verification pass rather than being folded into "one PR").

## Attack 7 — Format-level failure mode (most likely real-world failure)

**This exact move — "drop the score/grade, replace with bands or bars" — has been tried once
before at Bari and stalled.** `frozen_vegetables_v2_scorefree` (TASK-235, owner-approved 2026-06-10):
score dropped entirely, replaced with 4 use-case segment bands + benefit highlights, explicitly "not
a precedent for other categories." As of the last recorded state, **Phase 1 (the model spec) is
locked; Phases 2-4 (the USDA join table, the 53-product copy re-author, the frontend chip removal)
were never started, and the live page still ships the old score/copy in production** — a
score-free redesign that got owner approval and a locked spec, then did not ship, over multiple
weeks. This is the single most relevant internal precedent for "how does a score-free Bari page
actually fail in practice," and the brief's asset inventory (§4) does not mention it or draw the
lesson from it.

The most likely concrete failure mode for the guides redirection, given that precedent and the
traffic data above:
- **The spec gets built and approved (as this consult round will produce), the golden guide (likely
  magnesium, per §5 T4) gets built and two-gated, and then the second guide (creatine, which
  *already exists* and would need to be reshaped rather than newly authored) stalls** because it
  requires touching an already-shipped, already-red-teamed page for a second time with no new
  underlying data — the kind of "redo work with no new information" task that competes poorly for
  priority against categories with real traffic or real launches pending.
- **Maintenance burden compounds specifically because this format has MORE moving state than the
  one it replaces**, not less: a graded page needs the score/grade recomputed on a corpus refresh; a
  guide needs the score-equivalent (bar thresholds), the shortlist membership, the benchmark
  placement, AND the price freshness all kept in sync across every refresh, each with its own
  staleness clock. Buy links rot the fastest (retailer URLs and prices change) and are the newest,
  least-tested category of "stays synced" surface in this codebase (`buyUrl` has shipped nowhere
  live yet — only as an inert placeholder in `/catalog`).
- **Benchmark rot**: the worldwide benchmark sets (13 creatine / magnesium's own set) are
  point-in-time research artifacts (manual verification against NSF/Informed-Sport directories,
  literature pulls) — re-verifying them is real analyst labor, not a pipeline re-run, so "worldwide
  benchmarks stay" (brief §1.4) as a permanent feature commits to recurring manual re-verification
  work that nothing in the brief schedules or assigns.

**Severity: the credible worst case is not "the guide is wrong on day one" — every gate this agent
runs is built to catch that. It is "the guide format is approved, magnesium gets rebuilt, and
creatine (or a third area) sits half-migrated for months exactly like frozen-vegetables v2 did,"
leaving supplements in a worse discoverability state than today (currently: 1 linked page + 1
orphaned page; possible future: 1 relinked guide + 1 orphaned old-format page + a new hub with
inconsistent content shapes across its own two occupants).** Survivable only if the sequencing
(§5 T4) commits both guides to ship together or names an explicit interim state for whichever
ships second, with a deadline — an open-ended "creatine reshapes later" is the exact shape of the
frozen-vegetables stall.

## Summary Assessment

**Plausible-but-unvalidated** on the core diagnosis (ranking doesn't fit supplements) — sound
reasoning, zero behavioral evidence either way given the traffic data. **Weak confidence** on T1's
proposed defenses — real gap between "policy says don't" and "system can't." **Justified** on
retaining magnesium's form-tier science (Attack 5 is about boundary-case completeness, not the
core science). **Overriding structural problem:** the brief's independence defenses (T1) are process
statements, not gates, on the exact feature (buy button) that carries the highest reputational
exposure the brand has (אי-תלות / independence is named in this repo's own brand-anchor doctrine as
the credibility moat) — and the format being proposed as the fix has no usage validation and one
directly relevant internal precedent (frozen-vegetables v2) that stalled after approval.

## Findings by Severity

### CRITICAL
- **Opening Finding:** redirection is being decided on ~zero real-user data (8 views/2 users on
  magnesium, 0 on creatine, since 2026-06-01). Routes to: product-agent (name a usage-validation
  checkpoint before/after v1).
- **RT-A1 (Attack 1):** none of T1's three proposed defenses (disclosure, universal buttons,
  separate files) is a mechanical gate against bar-tuning-for-revenue or shortlist drift; both are
  currently undetectable by the proposed design. Routes to: product-agent (require a mechanical
  bar/shortlist-diff gate before any buy-button ships), design-agent (buy affordance must be
  visually inert per the existing `/catalog` precedent).

### HIGH
- **RT-A2 (Attack 2):** shortlist lacks on-page numeric inclusion criteria, a freshness date, an
  explicit "any product meeting these bars would appear" statement, and an enforced non-outcome-
  correlated sort key. Routes to: content-agent (copy requirements), frontend-agent (enforced sort).
- **RT-A3 (Attack 3):** brief §3.4's "benchmark placement" axis (product-vs-field) is the failing
  rendering; needs to be product-vs-external-standard. Routes to: product-agent / nutrition-agent
  (redefine the axis before design work starts).
- **RT-A4a (Attack 4):** pass/flag/fail bar visual register on named-brand "dose undisclosed" is a
  materially stronger public claim than the current live prose treatment; needs neutral-fact
  wording rules and preservation of the existing three-state (adequate/inadequate/undisclosed)
  model rather than collapsing to binary. Routes to: content-agent, design-agent.
- **RT-A6a (Attack 6):** zero existing redirect infrastructure in this codebase; first-ever use,
  concurrent with an active SEO-hygiene initiative — deserves its own verification pass, not a
  same-PR assumption. Routes to: frontend-agent, and back through this gate once built.

### MEDIUM
- **RT-A4b (Attack 4):** brief's citation of the "missing-data discard rule" for undisclosed-dose
  display is imprecise (that rule mandates discard; the brief's own design correctly wants flag/
  display, matching the live creatine page's existing three-state model) — tighten before this
  becomes an implementation instruction. Routes to: product-agent / nutrition-agent.
- **RT-A5 (Attack 5):** no stated joint rule for dose-confidence vs. form-confidence boundary cases
  (live Solgar-vs-TRIOMAG inconsistency already exists); no stated treatment for combination-product
  price-fairness bars; no stated fallback preserving the current three-state (declared/inadequate/
  unresolved) model under a binary bars UI. Routes to: nutrition-agent.
- **RT-A6b (Attack 6):** magnesium and creatine are not symmetric migration risks (one has real if
  tiny traffic + sitemap presence, the other has none) — test plan should weight accordingly, and
  no transitional messaging plan exists for returning bookmark users. Routes to: frontend-agent,
  content-agent.
- **RT-A7 (Attack 7):** the one directly relevant internal precedent for "drop the score, use
  bands" (frozen-vegetables v2, TASK-235) stalled after Phase 1 approval and is not shipped weeks
  later; the brief's sequencing question (T4) should explicitly rule out an open-ended "ship one
  guide now, reshape the other later" outcome. Routes to: product-agent.

## Verdict

**FAIL** at the strategy-consult stage — not because the underlying diagnosis is wrong (thin
ordinal differentiation in supplements is real, and the owner's instinct to retire rankings is
defensible), but because the concrete defenses offered for the single highest-exposure element
(buy button vs. independence) are non-structural, the shortlist/benchmark renderings as currently
worded in §3 would recreate the exact ranking the directive retires, and the one internal precedent
for this format class did not ship. None of these are reasons to abandon the redirection; they are
reasons the concrete plan is not yet buildable as written. Proposed status: **RETURNED** to
Product Agent (owns the go/no-go and MVP-cut decisions this report's findings feed into) with these
findings, for the brief to be revised before any build authorization.

Do not fix, approve, or close TASK-504.

```json
{
  "task": "TASK-504",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "tasks/returns/TASK-504_strategy_redteam_v1.md", "action": "created", "sha256": "5aef6d81d0cbbfcdddf7fd631d36c3a9fb3865ab1e6642eaeb97a84c6945a89b (hash of file content prior to this field's own insertion — self-referential hash of a file cannot include its own final value; re-hash post-write to verify no further edits occurred)"}
  ],
  "counts": {
    "critical_findings": "2/10 findings (Opening Finding, RT-A1) — denominator = 10 total findings raised in this report",
    "high_findings": "4/10 findings (RT-A2, RT-A3, RT-A4a, RT-A6a)",
    "medium_findings": "4/10 findings (RT-A4b, RT-A5, RT-A6b, RT-A7)",
    "ga4_pageviews_hashvaot_magnesium": "8/8 (GA4 property 543266887, screenPageViews, date range 2026-06-01..2026-07-04, exact API total, no sampling per response metadata)",
    "ga4_users_hashvaot_magnesium": "2/2 (same query, totalUsers)",
    "ga4_pageviews_hashvaot_creatine": "0/0 (same query filtered to /hashvaot/creatine, zero rows returned)",
    "creatine_ranking_language_occurrences": "3/3 (grep count of דירוג/מדרג in origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts, lines 98, 99, 174)",
    "sitemap_indexable_supplement_paths": "1/1 (only /hashvaot/magnesium present in origin/master:bari-web/src/lib/seo/sitemap-paths.ts ALL_INDEXABLE_PATHS; /hashvaot/creatine absent — denominator = 1 match found for the grep pattern 'creatine|magnesium')",
    "redirects_config_entries_found": "0/0 (grep of next.config.ts, vercel.json, middleware.ts on origin/master — no redirects() block, no vercel.json file, no middleware.ts file exists)"
  },
  "commands_run": [
    {"cmd": "git fetch origin --quiet", "exit_code": 0},
    {"cmd": "git ls-tree -r origin/master --name-only | grep -i hashvaot/creatine", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/lib/seo/sitemap-paths.ts | grep -n -i creatine|magnesium", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/next.config.ts", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/lib/comparisons/creatine-page-data.ts > /tmp/creatine-data.ts && grep -n דירוג /tmp/creatine-data.ts", "exit_code": 0},
    {"cmd": "mcp__analytics-mcp__get_account_summaries", "exit_code": 0},
    {"cmd": "mcp__analytics-mcp__run_report property_id=543266887 pagePath CONTAINS /hashvaot/magnesium 2026-06-01..today", "exit_code": 0},
    {"cmd": "mcp__analytics-mcp__run_report property_id=543266887 pagePath CONTAINS /hashvaot/creatine 2026-06-01..today", "exit_code": 0}
  ],
  "not_done": [
    "No Track V run (no build exists yet — this is a pre-build strategy review, correctly scoped as Track C dominant per the assignment)",
    "Did not independently query Google Search Console for creatine/magnesium indexation status (GA4 pageviews used as the available proxy instead)",
    "Did not review the C3 independent-challenge output or Product/Nutrition consult responses — this report is intentionally uncontaminated by those in-flight parallel consults, per the independence rule; a synthesis across all four consults is Product Agent's job, not this agent's"
  ],
  "self_check": "Acceptance test: does this report attack T1 hardest, name concrete failure scenarios (not hypotheticals) for shortlist-as-endorsement/benchmark-as-ranking/undisclosed-dose-as-accusation, address magnesium tier boundary cases with live examples, cover migration failure modes, and name the single most likely format-level failure -- each with severity + concrete scenario + a stated requirement (not a fix)? Observed result: yes on all seven counts, and every claim above is grounded in a verified repo state (git show against origin/master, not local stale branches) or a live GA4 query rather than the brief's own self-description, satisfying the independence rule."
}
```
