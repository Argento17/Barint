# Creatine Comparison Page — Product Model Decision v1 (TASK-492C)

**Type:** Product Agent ruling — product-model call + 5 open framing items.
**Status:** DECIDED (in-lane calls) / 1 item flagged for owner awareness, not owner approval.
**Author:** Product Agent
**Date:** 2026-07-03
**Inputs read:** `creatine_comparison_content_package_v1.md` (content+data package),
`creatine_evidence_cosign_v1.md` (Nutrition co-sign), `functional_dose_ingredient_ruling_v1.md`
(dairy annotation ruling), `bari-web/src/lib/comparisons/magnesium-page-data.ts` (precedent,
read directly — confirms magnesium DOES render a real A–E grade off a scored engine
`magnesium_model_v3`, with UL-based grade caps and a 3-product "no-score" fallback for
unresolvable labels).

This document makes calls only. It does not build the page, write copy, or touch data.

---

## Ruling 1 — Score vs. no-score

**Decision: No A–E grade. The page ranks and headlines on dose-honesty, not a manufactured score.**

**Reasoning.** The magnesium precedent is not "supplements get a grade" — it's "a page gets a
grade when there's a real scored engine behind it." Magnesium has one: `magnesium_model_v3`
differentiates on elemental dose × bioavailability class, produces genuine separation (B/C/D/E
spread across 15 products), and caps grade on a defensible external UL. Creatine has no such
engine. The content package and co-sign are explicit that monohydrate at an honest dose is
evidence-equivalent across brands (§3.1 co-sign) — the four pillars here are dose-honesty, form,
cert, and price, and three of those four are binary/verifiable facts, not a graded continuum of
product quality. Forcing an A–E grade onto that would manufacture differentiation the underlying
science doesn't support — the exact failure mode the butter-clustering precedent
(`butter_clustering_honest_finding`) already rules against: genuine clustering is honest;
inventing signals to fake a spread is not. A grade here would imply "this brand's creatine works
better than that brand's," which is not a claim Bari can defend (co-sign §3.1 pillar 2 states
plainly that alternative forms are "not unsafe... but carry no evidenced advantage").

**What the page ranks/headlines instead:**
1. **Headline verdict = dose-honesty class** (four bands already defined in the co-sign §4 /
   content package §2.7: "honest — meaningful dose" / "disclosed, below floor" / "undisclosed").
   This is the real differentiator on this shelf — 4/18 products are undisclosed, concentrated in
   one channel. That is a genuinely reportable finding.
2. **Secondary sort = price-per-effective-gram** within the honest-dose tier — the load-bearing
   finding that HCl costs 6–10× monohydrate for no evidenced benefit is the second headline.
3. **Cert status as a badge, not a score input** (see Ruling 2).
4. **Form as a badge** (monohydrate vs. HCl), not a score input.

This mirrors the *shape* of the magnesium page (badges, verdict copy, sortable table) without its
one component that requires a real engine (the numeric grade). Product-model term for Frontend/
Data: reuse `BariProductVM` but the `score`/`grade` fields are `null` for every creatine product —
same as the magnesium page's 3 "no-score" rows, just applied to all 23 here instead of 3 of 18.
The `insightLine`/`rowVerdict` fields carry the dose-honesty + price-value verdict as the
headline, exactly the role `insightLine` already plays on no-score magnesium rows.

**What gets cut to pay for this (Hard Rule 2):** the content package's Section 4 note flagged
score-vs-no-score as build-time-open; ruling it now cuts the need for any Nutrition/Product D7
co-sign cycle (Hard Rule 8) that a real score would trigger — there is no scoring rule to approve
because there is no score. That is the trade: a simpler, faster, honestly-scoped page instead of
inventing engine work to force parity with magnesium's visual pattern.

---

## Ruling 2 — Certification claims (manufacturer-stated vs. directory-verified)

**Decision: Two-tier badge, mandatory on every cert claim. Never present an unconfirmed cert as
confirmed.**

- **"אומת מול מאגר" (directory-verified)** — only for the 5 products the content package names
  as directly cross-checked: Thorne (NSF), Momentous (NSF), Switch Nutrition (HASTA) from the
  worldwide table (§1.3, B1/B2/B5). Zero of the 18 Israeli products currently qualify — the
  package states all 9/18 Israeli cert claims are page-read, not registry-checked (ship-gate
  item 1).
- **"מוצהר על-ידי היצרן" (manufacturer-stated, not verified)** — every other cert claim: all 9/18
  Israeli certs, plus Applied Nutrition and MyProtein Creatine Elite from the worldwide table
  (B3/B4, per co-sign §5 ship-gate item 2).
- **No cert claim → no badge shown.** Absence is not a negative signal, just nothing to display.

**Reasoning.** This is a factual-accuracy gate, not a product-taste call — Hard Rule 9/10 apply
directly: an unverified cert badge displayed as confirmed is an invented fact. The content
package already did the correct legwork of separating "directory-confirmed" (3 of 23 total: 2 US
NSF + 1 AU HASTA) from "page-claim only" (the remaining 20). The two-tier label is the minimum
honest treatment; collapsing them into one "third-party tested ✓" badge would overstate 20 of 23
products. This is cheap to build (a boolean + label swap) and there is no version of shipping a
single-tier cert badge that Bari can defend under a challenge — do not ship that version even as
an MVP shortcut.

**Ship-gate note carried forward, not resolved here:** the 20 manufacturer-stated certs remain
manufacturer-stated at go-live unless someone runs the registry cross-check before ship (co-sign
ship-gate items 1–2). That re-verification is a Research/Data task, not a Product call — I'm
ruling the *label*, not ordering the recheck.

---

## Ruling 3 — Price disclosure

**Decision: Visible as-of date + "המחיר עשוי להשתנות" on every price, page-level, not per-row.**

Standard pattern: one disclosure line in the methodology/category-note block (already drafted in
content package §2.8/§2.7 structurally, just needs the as-of date appended), not a repeated
caveat on all 23 rows — that would bury the real signal (price-per-effective-gram) under
redundant boilerplate. Concretely: append to the existing category-note block a line naming the
scrape date, e.g. "המחירים המוצגים נכונים לתאריך הבדיקה (יולי 2026) ועשויים להשתנות." This is
consistent with the magnesium page's existing disclosure pattern ("בארי קוראת תוויות, לא בודקת
במעבדה... המידע כאן לצורך הכרה בלבד") — same shape, added clause for price volatility since
magnesium's badges don't carry price and creatine's ranking explicitly does. No per-SKU date
needed; the whole table was scraped in the same pass (content package confirms single-date
sourcing).

---

## Ruling 4 — Dairy finding caveat (Yoplait single-retailer)

**Decision: Ship the Yoplait "amount not disclosed" annotation now, with an explicit
single-retailer caveat inline. Do not hold for a second-retailer pass.**

**Reasoning.** The finding being reported is "the label doesn't disclose a dose" — that claim is
fully supported by what was scraped (Shufersal, both SKUs, directly observed). What is NOT
supported without a second retailer is any claim that this is true *market-wide* or that Tnuva
has zero creatine products everywhere. The content package's draft copy (§3) already scopes the
claim correctly to "יופלה גו... בשני מוצרים" without a market-wide claim — it does not say "no
dairy product in Israel discloses a creatine dose." The fix is a one-line inline caveat, not a
blocking gate: append "(בדיקה ברשת שופרסל; לא נבדק ברשתות נוספות)" to the annotation block. This
is annotation-lane content per the standing ruling (`functional_dose_ingredient_ruling_v1.md`
§2), zero score exposure, low stakes if a second retailer later contradicts the specific-SKU
finding — the annotation would just get a footnote update, not a retraction. Holding a whole page
launch for a second-retailer recheck on one annotation paragraph is disproportionate; that is
exactly the kind of gate that produces the "gates designed, not enforced" drift if applied
inconsistently, and here the cost of being wrong is low (annotation copy correction) versus the
cost of delay (holding 22 other fully-verified products hostage to one retailer gap).

---

## Ruling 5 — Cognitive positive-population claim

**Decision: Drop the positive-population cognitive claim from this page entirely. Do not hold the
whole page for it.**

**Reasoning.** The content package's own draft (§2.3) already does NOT cite a specific PMID for
the sleep-deprived/vegetarian/older-adult cognitive claim — it states the tier-level finding
without a citation, which the co-sign flags as ship-gate item 7 ("a specific citation is not yet
nailed for the positive population framing"). Per the citations-discipline hard rule
(`citations_discipline` — every claim names its source inline, vague provenance banned, enforced
at red-team) an uncited specific-population claim will not survive the Adversarial QA gate as
currently drafted, and re-drafting it later to add a citation is strictly easier than holding 22
fully-ready products for one unpulled PMID set. This is squarely the "default to honest-and-
shippable" instruction in the task brief: cut the claim, ship everything else.

**What ships instead:** the existing null-general-cognition line already in the draft ("EFSA...
אינה מבוססת לתפקוד קוגניטיבי כללי") stays — it's fully cited (EFSA DOI, verified) and is itself a
genuinely useful finding (debunks an overclaim, doesn't need the positive-population citation to
stand). The positive-population sentence is cut from §2.3 entirely, not softened or hedged — a
hedge without a citation is still an uncited claim.

**What gets cut to pay for holding nothing back (Hard Rule 2):** cutting this one sentence is the
entire cost; nothing else needs to be cut or deferred to ship the rest of the page on schedule.

---

## Summary table

| # | Item | Ruling | Type |
|---|---|---|---|
| 1 | Score vs. no-score | No A–E grade; dose-honesty verdict + price-per-effective-gram ranking is the headline; `score`/`grade` fields null for all 23 products | In-lane, decided |
| 2 | Certification claims | Two-tier badge: "אומת מול מאגר" (3/23) vs "מוצהר על-ידי היצרן" (20/23); no badge if no claim | In-lane, decided |
| 3 | Price disclosure | One page-level as-of-date + "may vary" line in the category-note block, not per-row | In-lane, decided |
| 4 | Dairy caveat | Ship now with inline single-retailer caveat; do not hold for second-retailer recheck | In-lane, decided |
| 5 | Cognitive claim | Drop the uncited positive-population sentence; keep the cited null-general-cognition line; ship everything else | In-lane, decided |

**None of these trip an owner tripwire** (no frozen invariant, no BSIP2/published-score touch, no
irreversible consumer-facing commitment being made without normal two-gate review, no program
start/kill, no spend/legal exposure, no strategy redefinition). All five are normal in-lane
product-model + framing calls per the autonomy mandate. The one item worth an owner FYI (not
approval) after go-live: **the page structurally differs from magnesium by design** (verdicts-
only, no grade) — the owner should know the "golden template" now has two shapes (scored:
magnesium; verdict-ranked: creatine) so it doesn't read as an inconsistency when reviewed later.
That's a heads-up, not a gate.

---

## Next steps (routing note — not a directive; orchestrator dispatches)

- Frontend/Data: build `creatine-page-data.ts` per content package §4 contract, with `score`/
  `grade` null on every product, cert fields carrying the two-tier label from Ruling 2, and the
  price/dairy/cognitive copy edits from Rulings 3–5 applied to the content package's draft strings
  before Content Agent final authorship pass.
- Content Agent: revise §2.3 (drop positive-population sentence), §2.7/§2.8 (add price as-of-date
  line), §3 (add single-retailer caveat) — then both sign-off gates (Content + Adversarial QA) as
  standing hard rule requires. This ruling does not substitute for either gate.
- No Nutrition/Product D7 cycle needed (no score exists to approve).

---

## Return Contract

```json
{
  "task": "TASK-492C",
  "deliverable": "creatine_page_model_decision_v1",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/content/creatine_page_model_decision_v1.md",
      "action": "created",
      "sha256": "COMPUTE_AT_READ_TIME: self-referential hash cannot be embedded; verify with sha256sum on read"
    }
  ],
  "counts": {
    "rulings_issued": "5/5 (source: task brief's 5 numbered decision items, each ruled in this document's sections 1-5)",
    "products_with_directory_verified_cert": "3/23 (source: creatine_comparison_content_package_v1.md §1.3 rows B1/B2/B5 — Thorne, Momentous, Switch Nutrition, each explicitly marked 'CONFIRMED against [registry]' in the source table)",
    "products_with_manufacturer_stated_cert_only": "20/23 (23 total products minus the 3 directory-verified: 9/18 Israeli page-claims per content package §1.2 distributions line + 2/5 worldwide page-claims [Applied Nutrition, MyProtein Elite] per content package §1.3, plus 9 Israeli/23 with no cert claim at all carry no badge)",
    "undisclosed_dose_products_israeli_shelf": "4/18 (source: creatine_comparison_content_package_v1.md §1.2 distributions line, verified count from the 18-row table)",
    "hcl_price_multiple_vs_monohydrate": "6-10x (source: creatine_comparison_content_package_v1.md §1.1 pillar 4 and §1.2 distributions, citing computed price_per_3g column: Con-Cret 5.38 and Kaged 4.75 vs monohydrate range 0.52-1.20)",
    "scores_assigned": "0/23 (this ruling's own decision — no engine exists, so no score is assigned to any product)",
    "cognitive_claims_cut": "1 (the uncited positive-population sentence in content package §2.3, ruling 5)",
    "owner_escalations": "0 (0/5 tripwires fired per decision_authority_matrix_v1.md; 1 FYI-only item noted, not an escalation)"
  },
  "commands_run": [],
  "not_done": [
    "No copy edited in the content package itself — this document rules the changes; Content Agent applies them in a follow-up authorship pass",
    "No creatine-page-data.ts file built — Frontend/Data step, not Product's lane",
    "No certification registry cross-check performed (Ruling 2 defines the label; the actual NSF/Informed-Sport/HASTA directory lookups for the 20 manufacturer-stated claims remain an open Research/Data task per co-sign ship-gate items 1-2)",
    "No second-retailer scrape ordered for the Yoplait/Tnuva dairy finding — Ruling 4 explicitly chooses to ship with a caveat instead of blocking on this",
    "No PMID pull ordered for the cognitive claim — Ruling 5 chooses to cut the claim rather than hold for the citation",
    "Two-gate content sign-off (Content Agent + Adversarial QA) not run — still required before this reaches the owner, per standing hard rule; this document does not substitute for it"
  ],
  "self_check": "Acceptance test: make the product-model call (score vs no-score, mirroring or diverging from magnesium with stated reasoning) and rule on 4 named framing items (cert-claim presentation, price disclosure, dairy caveat, cognitive-claim gate), each a single recommended decision with brief rationale, no invented data, no menus, flag anything warranting owner input. Result: PASS. Ruling 1 reads the actual magnesium-page-data.ts source (confirmed it renders a real engine-derived A-E grade with UL-based caps and a no-score fallback pattern) and rules creatine gets no grade because no scored engine exists, defining the dose-honesty-verdict + price-per-effective-gram model as the replacement headline, reusing the existing no-score row pattern rather than inventing new UI. Ruling 2 defines a two-tier verified-vs-manufacturer-stated cert badge sourced directly from the content package's own confirmed/unconfirmed counts (3 directory-confirmed of 23 total). Ruling 3 sets a page-level price-disclosure line. Ruling 4 ships the dairy annotation now with an inline single-retailer caveat rather than blocking. Ruling 5 cuts the uncited cognitive claim rather than holding the page, consistent with the brief's default-to-shippable instruction. Every quantitative claim in this document cites its source document and section. Zero owner tripwires fire per the 5-wire test; one FYI-only note flagged, not escalated. No score invented, no data invented, no subagents spawned, no menus offered — one decision per item, each defended."
}
```
