# GLP-1 Guide v2 — Rich Article Architecture (TASK-535, Product Agent ruling)

**Addendum (2026-07-08, same session, v1.1):** §2 below was revised after the Data Agent's
bucket-B protein-density check (`glp1_bucketB_protein_check_v1.md`, orchestrator-verified
against the shipped JSONs — numbers exact) surfaced a real conflict in the original "a shelf
that comes back flat gets cut" wording. The ruling and the reasoning behind it are in §2.1
below. Everything else in this document (§0, §1, §3-§6) is unchanged.

**Answers the owner rejection (2026-07-08, verbatim in TASK-535/TASK-504A):** "extremely bad
work... The theme of this article is a bit GLP-1. We need a rich background to explain the
issues + visuals + youtube links + rich context and then explain the protein thing and provide
recommendations. Why just Yogurts also? complete logic failure here."

**Status:** Product architecture + scope ruling. Not a build. Routes to Research → Content →
Frontend per the dependency order in §6. Page stays `noindex` throughout (standing rule,
TASK-504A).

---

## 0. What went wrong (diagnosis, not blame)

The shipped `/madrichim/yogurt-glp1` did the *last* step only (a filtered product shortlist)
and skipped everything that makes a medication-adjacent nutrition topic responsible to publish:
no explanation of what GLP-1 drugs are or why they change eating, no visual aids, no external
authority (video), and — because the underlying corpus check (TASK-504A) only ever tested
milk then yogurt — the recommendation surface was never widened to the other live categories
that could plausibly carry the same protein-density logic. Two separate failures, both fixed
below: (1) missing article body, (2) under-scoped category coverage.

---

## 1. Section architecture (ordered — owner's ordering stands)

### 1.1 Opening frame
**Says:** Who this is for (anyone eating less — GLP-1 medication users named as the primary
audience per the owner's explicit ask — plus anyone else in a reduced-appetite state), and an
upfront non-medical-advice disclaimer. Sets expectation this is an educational + shopping guide,
not a medical protocol.
**Evidence needed:** none (framing only).
**Visual:** none required; optional hero image (reuse existing Bari illustration style, no new
character asset).

### 1.2 Background — what GLP-1 medications are and why eating changes
**Says:** Plain-language explanation of the drug class (semaglutide/tirzepatide/liraglutide —
generic and brand names may appear here, see §4 line), the mechanism (delayed gastric emptying,
central appetite suppression), and the resulting eating challenges: sharply reduced food
volume tolerance, early satiety, nausea in a subset of users, and the clinically documented risk
that a meaningful share of weight lost is lean muscle tissue, not fat.
**Evidence needed:** already sourced and cosigned — `GLP1_GUIDE_SCIENCE_COSIGN_v1.md` (Research
Agent, 2026-07-08) verified the two hero claims (lean-mass-share 25–39%, PMID:41877354, 20 RCTs/
15,782 participants; protein target ~1.2 g/kg, PMID:31794597 general + PMID:42303931 GLP-1-
specific). Reuse this document — do not re-derive. Research Agent adds any *new* background
claims this section needs (drug-class overview, prevalence, side-effect frequency) through the
same literature-client + CrossRef-integrity standard, not from training-data recall.
**Visual:** one explainer graphic — mechanism + eating-challenge list, icon-driven, Design/
Frontend to build using existing design tokens (no new component system).

### 1.3 Rich context — scale and why this matters now
**Says:** The real-world backdrop that makes this a live topic, not an abstract one: the
Israel 2026 basket funding Wegovy for ages 12–18, and the broader market signal (US CPG brands
launching "GLP-1 support" product lines, UK high-protein-dairy growth) that originally opened
this program (TASK-504A origin note, 2026-07-05).
**Evidence needed:** the TASK-504A origin note states these as background facts but was not
itself a cited research artifact — Research Agent must re-verify and freshen (basket policy
citation, market figures) before they appear as claims in shipped copy. Do not carry them
forward as "already proven" — they are candidate context pending the same verification bar as
§1.2.
**Visual:** none required; could carry a simple stat callout once Research supplies verified
figures.

### 1.4 Vetted video pack (2–4 embeds, placed after background/context, before the pivot)
**Says:** Nothing new — external authority reinforcing §1.2/§1.3 in the user's own words/voice.
**Evidence needed:** Research Agent sources candidates; vetting criteria in §3.
**Visual:** embedded YouTube players (Frontend — standard embed, not a new component).

### 1.5 Pivot — why protein specifically
**Says:** One bridge paragraph connecting §1.2's finding (lean mass loss, reduced food volume)
to the protein-density logic: if you can only eat a small amount, that small amount should be
protein-dense to protect muscle mass. This is the paragraph the owner said was missing context
for — it must land *after* the reader understands the problem, not before.
**Evidence needed:** none beyond §1.2's already-cosigned claims — this is a logical bridge, not
a new factual claim.
**Visual:** none.

### 1.6 The protein-density method (how Bari picked what's below)
**Says:** Plain explanation of the selection logic already built and QA-passed for yogurt
(absolute protein g/100g threshold, not a ratio-to-calories proxy — RT-1 from TASK-504A found
the ratio version was a low-calorie-filter artifact, not a real protein signal). State the
method once, generically, so it can apply to every category section in §1.7 without
re-explaining per shelf.
**Evidence needed:** none new — this is the already-built, already-QA'd yogurt methodology
(TASK-504A step 2, "Nutrition bar-finalization LOCKED").
**Visual:** none, or a simple "how we scored this" diagram reused from the comparison-page
methodology pattern already live elsewhere on the site.

### 1.7 Recommendations — by category (see §2/§2.1 for which categories qualify)
**Says:** One subsection per qualifying shelf (5, per §2.1's resolved ruling: yogurt-spoonable,
yogurt-drinkable, hummus, protein-bars, hard-cheeses), each reusing the frozen `ScoreChip` +
`CategoryNoteBox` components and pulling grades/copy live from the shipped comparison JSON —
no new scores, no new copy invented outside the existing two-gate process. Three distinct
recommendation framings apply, not one template: (a) yogurt-spoonable = engineered-formulation
shortlist (top scorers among the ≥8g tier); (b) protein-bars/hard-cheeses = whole-shelf
"everything here clears the bar, differentiate by score/additives" framing (§2.1); (c) hummus =
subtype framing, "choose chickpea/legume-based spreads for protein" (§2.1). Content must not
collapse these into one copy pattern.
**Evidence needed:** per-category protein-density check from Data Agent — done for all 5
qualifying shelves (`glp1_bucketB_protein_check_v1.md` + TASK-504A for yogurt). Still needed
before this section can ship: Content/Product's within-subtype narrowing of hummus's 34
qualifiers into a short concrete list (§2.1, not yet done).
**Visual:** existing ScoreChip cards per product, grouped by shelf.

### 1.8 Closing
**Says:** Restated disclaimer (not medical advice, talk to your care team), source list
(PMIDs + video credits), and the standing guardrails from §4 restated in plain language for the
reader (why you won't see a "GLP-1 friendly" badge on any product here).
**Evidence needed:** none — compiles what's already cited above.
**Visual:** none.

---

## 2. Category coverage ruling — "why just yogurt" fixed

**Evidence checked this session** (Product Agent, direct file inspection, not delegated):
`C:\Bari\bari-web\src\data\comparisons\*_frontend_v*.json` — 18 live scored/shipped categories,
`_meta.category` + `len(products)` read directly from each file (commands in the return
contract). Full inventory:

| Category (file) | `_meta.category` | Products |
|---|---|---|
| yogurt_spoonable_frontend_v1.json | yogurt-spoonable | 78 |
| yogurt_drinkable_frontend_v1.json | yogurt-drinkable | 20 |
| protein_combined_frontend_v2.json | protein-bars | 32 |
| cheese_frontend_v4.json | cheese (cottage/white cheese shelf — confirmed by product-name grep, see below) | 47 |
| hard_cheeses_frontend_v4.json | hard-cheeses | 31 |
| brined_cheeses_frontend_v2.json | brined_cheeses | 36 |
| hummus_frontend_v5.json | hummus | 57 |
| milk_frontend_v1.json | milk | 18 |
| juices_frontend_v3.json | juices | 17 |
| crackers_frontend_v1.json | crackers | 53 |
| bread_frontend_v4.json | bread | 23 |
| cakes_hard_cookies_frontend_v1.json | cakes-hard-cookies | 62 |
| cereals_frontend_v2.json | cereals | 20 |
| chocolate_bars_frontend_v1.json | chocolate-bars | 23 |
| chocolate_tablets_frontend_v1.json | chocolate-tablets | 35 |
| cookies_coffee_frontend_v2.json | cookies_coffee | 117 |
| granola_frontend_v2.json | granola | 22 |
| snacks_frontend_v5.json | snacks | 21 |

Cottage-cheese confirmation: `grep -c "קוטג" cheese_frontend_v4.json` → 47/47 products (every
product in that file's name field contains the cottage/white-cheese string, e.g. "קוטג 1%
שומן", "קוטג' 5%", "גבינה לבנה 5% שומן"). This is the "cottage was already in-corpus" category
TASK-504A referenced — it is the `cheese` file, not a separate cottage file.

### Ruling: three buckets (original, pre-Data-Agent-check pass)

**A — IN, already built and QA-passed (2/18):** `yogurt-spoonable` (78), `yogurt-drinkable`
(20, secondary/on-the-go callout). Reason: TASK-504A already ran the full protein-density check
against real per-100g data and found a genuine bimodal split (23/78 spoonable clear ≥8g
protein/100g in a real two-tier structure, not a smooth gradient) — this is the one shelf with
a verified, QA-passed recommendation basis. No further check needed; reuse as-is.

**B — CANDIDATE, needed a Data Agent protein-density check before inclusion (5/18):**
`protein-bars` (32), `cheese`/cottage (47), `hard-cheeses` (31), `brined_cheeses` (36),
`hummus` (57) — routed to Data Agent per §2's original wording, "a shelf that comes back flat
gets cut, not forced." **Results are in; see §2.1, which supersedes the literal application of
that sentence.**

**C — EXCLUDED, structural reason stated (11/18):** `milk` (18) — already tested and failed
(TASK-504A RT-1/RT-2: the ratio-based bar was a low-calorie-filter artifact and the real
high-protein dairy wasn't in this corpus; that gap is what produced the yogurt build, not a
milk fix — milk itself was never re-tested and stays out). `juices` (17), `cereals` (20),
`granola` (22) — carbohydrate/sugar-forward by category definition, the opposite nutrient
profile from what a reduced-appetite, muscle-preservation guide should recommend.
`crackers` (53), `bread` (23), `snacks` (21) — carb/fat-forward staples and salty snacks, not
protein-defining categories. `cakes-hard-cookies` (62), `chocolate-bars` (23),
`chocolate-tablets` (35), `cookies_coffee` (117) — dessert/treat categories; recommending a
treat shelf inside a medication-adjacent nutrition guide is a credibility risk independent of
any protein number. These 11 do not get a Data Agent check — the category definition itself is
the disqualifying reason, and that reasoning is available for challenge (Nutrition Agent can
overrule any one of these if a specific product genuinely breaks the category's profile, but
the *shelf* is not worth checking as a whole). **Unchanged by this addendum.**

---

## 2.1 Bucket-B disposition ruling (v1.1 addendum — answers the Data Agent's spec-conflict flag)

**Input:** `glp1_bucketB_protein_check_v1.md` (Data Agent, orchestrator-verified against the
shipped JSONs — numbers treated as exact per that verification, not re-derived here). Full
distributions for all 5 categories are in that document; this section states the disposition
only, citing the specific figures the ruling turns on.

### The conflict, named precisely

§2's original sentence — "a shelf that comes back flat... gets cut, not forced" — was written
to prevent one failure mode: **manufacturing a fake tier where no real one exists**, i.e.
picking an arbitrary cut point in a smooth gradient and dressing it up as a "shortlist." It was
**not** written with the case the Data Agent found in mind: a shelf that is flat because *every*
product on it already clears the bar by a wide margin. Read literally, the sentence cuts
protein-bars and hard-cheeses — the two shelves that are, by category definition, the most
protein-dense food in the entire 18-category inventory. That is a defect in how I wrote the
rule, not a correct application of it. Ruling it now, explicitly, so it is not ambiguous again.

### Ruling: "flat" is not one disposition — it is two, and they get different treatment

**Flat-and-cut (no honest signal to recommend on):** `cheese`/cottage (min=2.8g, max=17.0g,
mean=7.56g/100g — a continuous gradient across the whole range, no populated second cluster;
the one apparent outlier is a single product, n=1, not a tier) and `brined_cheeses` (min=7.0g,
max=24.0g, mean=14.64g/100g — three similarly-sized gaps scattered across the range, the
signature of a gradient, not a bimodal split; the largest gap isolates only 3 products as a
thin outlier tail). Both stay **CUT**. Cutting these is the correct reading of the original
rule: there is no defensible line to draw, and either recommending the whole 47/36 (diluting the
guide with plenty of low-protein products) or picking an arbitrary subset (an unearned "some of
these are better" claim with no real basis) would be dishonest. **Disposition unchanged from
what "flat = cut" was designed to do.**

**Flat-and-include (uniformly excellent — no filtering needed because the whole shelf already
clears):** `protein-bars` (min=25.0g/100g across all 32/32 products — 3× yogurt's 8g threshold;
Data Agent's own framing: "not flat in the sense of no signal — flat in the sense that protein
density does not discriminate within this category because the category definition already
guarantees it") and `hard-cheeses` (min=22.0g/100g across all 31/31 products — 2.75× the
threshold). **Ruling: INCLUDE both, with a threshold-anchored, defensible bar for why "flat"
does not mean "cut" here** — a shelf's floor at or above **2× yogurt's 8g threshold (16g/100g)**
clears categorically; no per-product filtering is applied because none is needed or honest to
imply. This is not the same recommendation format as yogurt's "here are the winners" shortlist —
it is a different, equally honest claim: **"every product on this shelf is protein-dense;
differentiate by Bari score, additives, or format, not by protein"** (this reuses each shelf's
existing grade/score, already shipped, already QA'd — no new differentiation invented). Content
must write this framing explicitly, not silently reuse the yogurt template's "top N" language,
or the copy would imply a false discrimination that doesn't exist on this shelf.

**Reversal condition:** this 16g/100g "uniformly excellent" line is anchored to these two
shelves' actual floors (25.0g, 22.0g — both comfortably clear it with margin). If a future
bucket-style check finds a shelf with a flat floor that only marginally clears 8g (e.g. a
9–11g/100g floor with no real tier), that is a different, weaker case and must come back to
Product for a fresh ruling — it does not auto-qualify under this addendum.

### Hummus — TIERED, but the tier is subtype, not formulation; frame it as such

Data Agent verdict: **TIERED**, ≥7g/100g clears **34/57 (60%)**, confirmed two ways (density: 19
products ≤2.5g vs 34 products ≥7.0g, only 4/57 (7%) in the middle; and product-type cross-tab:
`hummus_spread` 32/33 and `masabacha` 2/2 land in the ≥7g band, `matbucha` 10/10 and
`pepper_spread` 4/5 and `eggplant_spread` 5/7 land in the ≤3g band). **Ruling: INCLUDE**, but
the framing must match what the data actually shows. Yogurt's tier was *engineered* — some
products in one food type are formulated with more protein than others (Greek/skyr/fortified vs
standard), which supports "these specific products are the better pick." Hummus's tier is
*compositional by subtype* — chickpea/legume-based spreads (hummus, masabacha) are protein-dense
and vegetable-based spreads (matbucha, pepper, eggplant) are not, almost categorically. The
honest recommendation is **"choose chickpea/legume-based spreads for protein; the
vegetable-based spreads on this shelf (matbucha, pepper, eggplant) are not a protein source, and
that's fine if you're eating them as a flavor addition, not counted toward your protein"** — not
"some hummus products beat other hummus products." Content must not disguise a subtype fact as
a formulation finding. **A further within-subtype narrowing by score/grade (the 34 qualifiers
down to a short list, the same way yogurt's 23 became a 4-product shortlist) is still needed
before this ships as a concrete recommendation — that narrowing is Content/Product's downstream
step, not done in this ruling, and not yet delegated.**

### Revised total

**IN — recommending products (5/18):** `yogurt-spoonable` (78), `yogurt-drinkable` (20),
`hummus` (57, subtype-framed), `protein-bars` (32, whole-shelf/uniformly-excellent framing),
`hard-cheeses` (31, whole-shelf/uniformly-excellent framing).
**EXCLUDED (13/18):** the original 11 (unchanged) **plus** `cheese`/cottage (47) and
`brined_cheeses` (36), now excluded on a checked, not assumed, basis (flat gradient, no real
tier).

**Total: 5 (IN) + 13 (EXCLUDED) = 18/18.**

---

## 3. Visuals + video policy

**Visual types needed, by section:** §1.1 optional hero illustration; §1.2 one mechanism/
eating-challenge explainer graphic; §1.3 optional stat callout card; §1.6 optional "how we
scored this" methodology diagram (pattern already exists elsewhere on the site — reuse, don't
invent); §1.7 existing `ScoreChip` cards, one grid per qualifying shelf. Design/Frontend build
these — Product is scoping quantity and placement only, not designing them.

**YouTube vetting bar (Research Agent sources candidates; Product/QA apply this rubric before
any embed goes live):**
- **Accept:** credentialed source — a named MD/RD/PhD clinician, an accredited hospital or
  academic medical center channel, or a recognized professional society (e.g., an endocrine or
  obesity-medicine society) — explaining the drug class, mechanism, or nutrition considerations
  in general terms.
- **Reject:** any channel that sells or affiliate-links supplements, meal plans, or the
  medication itself; any content produced or sponsored by a drug manufacturer (pharma-brand
  promotional content); any influencer without a stated, checkable clinical credential; any
  video that names a specific product (food or drug brand) as "recommended" or "safe with."
- **Log requirement:** each accepted video gets one line — channel name, stated credential,
  one-sentence justification — in the same evidence-registry style as the PMID table in
  `GLP1_GUIDE_SCIENCE_COSIGN_v1.md`. No video ships without that line on file.
- **Volume:** 2–4 videos total for the whole article. This is not a curated video library.

---

## 4. Guardrails that survive the re-scope

- **No "GLP-1 friendly" badge on any product**, anywhere, ever.
- **No drug name as a product qualifier** — a product's `insightLine`/`rowVerdict`/expansion
  copy never says "Ozempic-friendly," "good with Wegovy," or equivalent.
- **No per-product medical claims** — a product can be described as protein-dense; it cannot be
  described as treating, mitigating, or being medically appropriate for medication use.
- **Page stays `noindex`** until the owner explicitly flips it (standing rule, unchanged).
- **The educational/claiming line, stated exactly:** §1.2/§1.3 (background and context) MAY
  name drug classes and brand names (semaglutide, tirzepatide, Ozempic, Wegovy, Mounjaro) — this
  is the owner's explicit ask for "rich context" and is genuine educational content about a
  medication class, not a product claim. §1.7 (recommendations) and every per-product string
  anywhere on the page MUST stay drug-name-free and badge-free — a recommendation can say "these
  are protein-dense options for anyone eating in smaller amounts," never "these work with
  [drug]." The line is: **drug names describe the medical background; they never touch a
  product.** This is the same distinction TASK-504A's Adversarial QA gate already enforced
  (0 drug names in visible product output, confirmed at terminal red-team) — this ruling just
  extends it explicitly to the new background/context sections where drug names now
  legitimately appear for the first time.

---

## 5. Anti-overbuild check

This is **one guide, one page** — not a program, not a hub, not a recurring series.

- **Reuse, don't rebuild:** `ScoreChip`, `CategoryNoteBox` (frozen components), the already-
  cosigned science evidence (`GLP1_GUIDE_SCIENCE_COSIGN_v1.md`), the already-built yogurt
  shortlist and its QA pass (TASK-504A). None of this gets re-derived.
- **What's genuinely new:** background/context copy + 2–4 vetted videos (Research + Content),
  the per-100g protein-density check on 5 candidate categories — **done** (Data Agent,
  `glp1_bucketB_protein_check_v1.md`, no new scrape/BSIP0/rescore), one rich-article layout
  extension to the existing page template (Frontend — a new section pattern, not a new page
  type), one elevated medication-adjacency red-team pass (Adversarial QA, same bar as before),
  and — newly scoped by §2.1 — three distinct recommendation-copy framings instead of one
  (engineered-tier / whole-shelf / subtype), plus a within-subtype narrowing pass for hummus.
- **What this must NOT become:** a multi-page "GLP-1 hub," a recurring content series, a new
  BSIP field, or a "GLP-1-friendliness score." No category gets rescored or rescraped to
  manufacture a protein signal that isn't already in the shipped data. §2.1 refined "flat = cut"
  into two dispositions (flat-and-cut vs. flat-and-uniformly-excellent) — that refinement is
  scoped and closed by this addendum; it is not an invitation to relitigate other categories'
  exclusions on the same "well actually it's flat for a good reason" logic without a real,
  checked distribution behind it, same evidentiary bar as this ruling used.
- **Scope cut that pays for the richness add:** the guide stays a single URL. Do not fork into
  per-category GLP-1 pages (e.g. no separate `/madrichim/glp1-hummus`) — one article, one set of
  category subsections inside it.
- **Routing call (Product scope decision, not implementation):** the current route
  `/madrichim/yogurt-glp1` is itself a symptom of the yogurt-only scoping error. Recommend
  Frontend rename the route to a category-neutral path (e.g. `/madrichim/glp1`) as part of the
  rebuild — cheap, and stops the URL from re-encoding the mistake being fixed. This is a Frontend
  implementation detail Product is flagging, not dictating.

---

## 6. Dependency order

1. **Research Agent** — background/mechanism claims (extend `GLP1_GUIDE_SCIENCE_COSIGN_v1.md`
   pattern for any new §1.2 claims), refresh §1.3's basket/market context claims, source 2–4
   videos against the §3 rubric. Runs in parallel with:
2. **Data Agent** — protein-density per-100g check on the 5 bucket-B categories (protein-bars,
   cheese, hard-cheeses, brined_cheeses, hummus), same method as the yogurt check (absolute
   grams, not ratio). Reports which shelves clear a real bimodal/tiered signal vs. a flat
   gradient.
3. **Content Agent** — authors all sections once Research + Data land; subject to the standing
   two-gate (Content + Adversarial QA) sign-off on every string, per the CLAUDE.md hard rule.
4. **Frontend Agent** — builds the rich-article layout, embeds videos, wires the per-category
   recommendation sections that Data Agent cleared, implements the route rename if accepted.
5. **Adversarial QA Agent** — elevated medication-adjacency red-team (same bar TASK-504A used:
   0 drug names in product-level output, 0 "friendly" badges, 0 per-product medical claims,
   citation-integrity check on every PMID/video credential).
6. **Orchestrator** — dispatches 1–2 in parallel, sequences 3→4→5, verifies claims, closes.

Product does not dispatch or sequence-execute this — the above is the *recommended* order for
the orchestrator to run, per the scope boundary in this agent's charter.

---

## Return Contract (v1.1 — addendum ruling on the Data Agent's bucket-B spec conflict)

```json
{
  "task": "TASK-535",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/yogurt_system/guides/glp1_guide_v2_architecture.md",
      "action": "modified",
      "sha256": "re-verify with `sha256sum 02_products/yogurt_system/guides/glp1_guide_v2_architecture.md` at read time (self-hash paradox — writing the hash into the file changes the file; documented in the v1.0 return, unchanged practice here)"
    }
  ],
  "counts": {
    "bucket_B_categories_checked_by_data_agent": "5/5 (protein-bars, cheese, hard-cheeses, brined_cheeses, hummus; source: 02_products/yogurt_system/guides/glp1_bucketB_protein_check_v1.md, orchestrator-verified against shipped JSONs per coordinator message this turn)",
    "bucket_B_disposition_flat_and_cut": "2/5 (cheese/cottage min=2.8g max=17.0g mean=7.56g/100g n=47; brined_cheeses min=7.0g max=24.0g mean=14.64g/100g n=36; both smooth gradients, no populated second cluster; source: glp1_bucketB_protein_check_v1.md §3, §5)",
    "bucket_B_disposition_flat_and_include_wholeshelf": "2/5 (protein-bars floor=25.0g/100g 32/32 products, 3x the 8g threshold; hard-cheeses floor=22.0g/100g 31/31 products, 2.75x the threshold; source: glp1_bucketB_protein_check_v1.md §2, §4)",
    "bucket_B_disposition_tiered_subtype": "1/5 (hummus, 34/57 clear >=7g/100g, 60%; subtype cross-tab hummus_spread 32/33 and masabacha 2/2 in >=7g band vs matbucha 10/10 and pepper_spread 4/5 and eggplant_spread 5/7 in <=3g band; source: glp1_bucketB_protein_check_v1.md §6)",
    "categories_now_recommending_products_in_guide": "5/18 (yogurt-spoonable 78, yogurt-drinkable 20, hummus 57, protein-bars 32, hard-cheeses 31; source: this addendum's §2.1 revised total, sums to 18 with the unchanged 13 excluded)",
    "categories_excluded_total_after_addendum": "13/18 (original 11 structural + cheese/cottage 47 + brined_cheeses 36, now excluded on a checked not assumed basis; source: §2.1 revised total)",
    "hummus_within_subtype_shortlist_narrowing": "0/34 done (explicitly not_done below — routed as Content/Product's next step, not completed in this ruling)"
  },
  "commands_run": [
    {"cmd": "Read C:\\Bari\\02_products\\yogurt_system\\guides\\glp1_bucketB_protein_check_v1.md in full, including §7 flag, before ruling", "exit_code": 0}
  ],
  "not_done": [
    "Hummus's 34/57 qualifiers are not yet narrowed to a concrete short recommendation list (by score/grade, same pattern as yogurt's 23->4) — Content/Product's next step, not this ruling's scope",
    "Content copy for the three distinct recommendation framings (engineered-tier, whole-shelf, subtype) not drafted — Content Agent's task, subject to two-gate sign-off",
    "No re-verification of the Data Agent's raw numbers performed independently by Product in this turn — relied on the coordinator's statement that the orchestrator already independently verified the distributions against the shipped JSONs; if that verification is later found incomplete, this ruling's category math must be re-checked"
  ],
  "self_check": "Acceptance test: does this addendum resolve the exact ambiguity the Data Agent flagged (does 'flat=cut' apply literally, or does a uniformly-high floor get a different disposition), rule it with a stated, defensible, numerically-anchored line (2x yogurt's 8g threshold) rather than a vague judgment call, and separately rule how hummus's subtype-driven tier should be framed so Content doesn't misrepresent it as a formulation finding? Result: PASS on both questions. Ruling: flat-and-cut stays cut (cheese/cottage, brined_cheeses — checked, no real signal); flat-and-uniformly-excellent gets included with whole-shelf framing, not a false shortlist (protein-bars, hard-cheeses); hummus is included but must be framed as a subtype choice (chickpea/legume vs vegetable spreads), not a per-product formulation win. Net effect: 5/18 categories now recommend products, up from 2/18, closing the 'why just yogurt' complaint with three honestly-differentiated recommendation patterns rather than one copy-pasted template."
}
```
