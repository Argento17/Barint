# TASK-549 — High-Protein-Dairy / GLP-1-Companion Shelf: Scoping Memo

**Product Agent, 2026-07-09.** Input: Project Comp daily scan 2026-07-09 (signal, not
evidence) — GLP-1 named 2026's #1 nutrition trend, protein+fiber reformulation wave, ZOE
protein guidance; IL milk shortage coinciding with recombinant/cow-free dairy landing on
shelves (Remilk×Gad, Strauss/Imagindairy).

**THE CALL: no new category, no new collection. MONITOR + route one question to Nutrition.**
The GLP-1-companion content play this signal describes is **already in flight, wider in
scope, and further along** than anything this memo could propose — TASK-535 (`/madrichim/glp1`
guide rebuild, IN_PROGRESS, Product-authored architecture at
`02_products/yogurt_system/guides/glp1_guide_v2_architecture.md`, dated 2026-07-08, one day
before this signal landed). Opening parallel work here would duplicate TASK-535 under a
different label — the exact overbuild pattern this mandate exists to catch.

---

## 1. What Bari already has vs. the gap

**Live corpus, verified by direct file read this session** (`Glob` on
`bari-web/src/data/comparisons/*.json`, 21 files / 18 distinct categories after excluding 2
red-team ledger files and one superseded `bread_frontend_v3.json` kept alongside `v4`):
yogurt-spoonable (78), yogurt-drinkable (20), cheese/cottage (47), hard-cheeses (31),
brined_cheeses (36), milk (18), plus 12 non-dairy categories. Grep of every comparison JSON
for `Remilk|רמילק|Imagindairy|אימג|cow-free|רקומביננטי|recombinant` — **0/18 files, 0 matches**:
no recombinant/cow-free dairy product exists in any live corpus today (source: this session's
grep, command in `commands_run`).

**Is "high-protein dairy" a new category, a lens, or redundant?** Redundant with work already
underway. TASK-535's Data Agent ran the exact per-100g protein-density check this memo would
otherwise have to commission, across all 5 dairy-adjacent + protein-adjacent shelves
(`02_products/yogurt_system/guides/glp1_bucketB_protein_check_v1.md`, orchestrator-verified).
Result, dairy subset only: **yogurt-spoonable** (23/78 clear ≥8g/100g, engineered tier),
**yogurt-drinkable** (secondary/on-the-go), **hard-cheeses** (31/31 clear ≥22g/100g, whole-shelf
"uniformly excellent" framing) are IN a cross-category high-protein guide; **cottage/cheese**
(47, mean 7.56g/100g) and **brined_cheeses** (36, mean 14.64g/100g) are OUT — checked and found
to be smooth gradients with no real tier, not assumed. Milk is OUT on a separately-tested,
structural basis (TASK-504A, referenced in the TASK-535 architecture doc: milk's ratio-based
bar was a low-calorie-filter artifact, never re-tested since).

A standalone "high-protein dairy" comparison page or hub collection would be a **re-slice of
data TASK-535 already curated**, filtered down to dairy-only — strictly narrower and strictly
later than what's already scoped. Building it would cost a new page/collection build to
deliver *less* than what TASK-535 ships as one section of a richer article. **Do not build it.**
If, after TASK-535 ships, hub-level browsability turns out to want a dairy-only filter chip on
top of the guide's existing per-category sections, that is a cheap downstream addition (reuse
the guide's already-computed qualifier lists) — not a reason to start now.

---

## 2. GLP-1-companion angle

Already answered, in more depth than this task's brief asks for. TASK-535's re-scoped guide
(owner-rejected 2026-07-08 for being yogurt-only, then re-architected same day) is precisely
"best high-protein picks for GLP-1 / eating-less," cross-category, with the protein target
(~1.2–1.6 g/kg, citing PMID:31794597 general + PMID:42303931 GLP-1-specific — already
Research-cosigned per `GLP1_GUIDE_SCIENCE_COSIGN_v1.md`) this signal's ZOE citation would have
supplied independently. It already resolves the fiber-adjacent framing this signal raises as a
*content*, not scoring, question, and it is explicitly a **guide** (`/madrichim/glp1`), not a
new comparison page — the exact "cheapest honest form" this mandate would have recommended.

**Nothing new opens here.** The one live gap TASK-535 itself flags (`not_done` in its v1.1
return) is a within-subtype narrowing of hummus's 34 qualifiers to a short list — that is
TASK-535's downstream step, already tracked there, not a new task.

---

## 3. Recombinant / cow-free dairy — routed to Nutrition, not decided here

Real signal, zero corpus exposure today (§1 grep, 0/18 files). This is a **watchlist
question**, not urgent BSIP0 work — there is no product to score yet from the approved
source-selection chain (Shufersal → Victory → Yochananof → Rami-Levy; OFF banned absolutely,
no exception). Framing the open question for Nutrition, to have an answer ready before, not
after, one of these products is scraped:

> **Watchlist question for Nutrition Agent:** if/when a recombinant-protein or cow-free dairy
> product (e.g., Remilk×Gad milk, Strauss/Imagindairy cheese) becomes available through Bari's
> approved retail-scrape chain, how should BSIP treat it — (a) on ingredient/nutrition basis:
> does precision-fermentation dairy protein score identically to conventional dairy protein of
> the same macro profile, or does the production method itself carry an evidence-backed scoring
> implication; (b) on additive/processing profile: what does the ingredient panel typically
> carry beyond the fermented protein (stabilizers, flavor systems) and how does that interact
> with existing additive-differentiation rules (e.g., the emulsifier CMC/P80 vs lecithin
> precedent); (c) on category placement: does it slot into the existing `milk` or yogurt
> corpus/shelf definition as-is, or does it need its own shelf identity? This is explicitly
> **not** a scoring change — Product is not asking Nutrition to score anything, only to have a
> documented position so that when/if BSIP0 corpus work is proposed later, D1/D4 gating isn't
> improvising the answer under launch pressure.

No corpus, no BSIP0, no scoring change proposed or implied by this memo.

---

## 4. Recommendation — single next step

**MONITOR, don't build.** Concretely:
1. **No new category, no new collection, no new corpus.** TASK-535 already is the cheapest
   honest form of the GLP-1-companion play; a dairy-only re-slice would be strictly worse value
   for strictly more build cost.
2. **Route the cow-free/recombinant dairy question to Nutrition Agent** as a watchlist item
   (§3 above) — answer it once, park it, do not act on it until a real product is scrapeable.
3. **No action on Google Trends demand data for this signal.** The skill's own fence applies:
   demand informs launch *order*, never a product's *quality*, and there is no candidate
   category here to sequence yet — nothing to order.
4. If a recombinant-dairy product later appears on Shufersal/Victory/Yochananof/Rami-Levy in
   meaningful volume, that is a fresh D1 category-sequencing decision at that time, informed by
   Nutrition's now-pre-answered §3 position — not a reason to act today.

**What's cut to pay for this:** nothing new was scoped, so nothing needs to be cut — that is
the point. The anti-overbuild call here is refusing a plausible-sounding build (a "high-protein
dairy" shelf) because the honest need is already served by cheaper, further-along work.

**Reversal condition:** revisit this call if (a) TASK-535 ships and hub telemetry
(Plausible `breakdown('event:page')`, once `PLAUSIBLE_API_KEY`/`PLAUSIBLE_SITE_ID` are live)
shows real demand for a dairy-only filter the guide doesn't serve, or (b) a cow-free dairy
product actually appears in the approved scrape chain, making §3 live rather than hypothetical.

---

## Return Contract

```json
{
  "task": "TASK-549",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "01_framework/operations/comp/signal_evaluations/task549_glp1_dairy_shelf_scope_v1.md", "action": "created", "sha256": "245215e2f7889401b34c68ef8f6d57c77be7b0b0c6730ed8616e524561c2ff90 (hash of the pre-this-edit version; writing this JSON block into the file changes its own hash again — self-hash paradox, same documented practice as TASK-535's return contracts; re-verify with `sha256sum` at read time)"}
  ],
  "counts": {
    "live_comparison_json_files": "21 files / 18 distinct categories (source: Glob bari-web/src/data/comparisons/*.json this session; 2 are _redteam_ledger.json, 1 is superseded bread_frontend_v3.json alongside v4)",
    "recombinant_cowfree_dairy_matches_in_corpus": "0/18 category files (source: this session's Grep for Remilk|רמילק|Imagindairy|אימג|cow-free|רקומבינטי|recombinant across bari-web/src/data/comparisons/*.json)",
    "dairy_shelves_already_in_glp1_guide_scope": "3/5 dairy-adjacent shelves IN (yogurt-spoonable 78, yogurt-drinkable 20, hard-cheeses 31/31≥22g/100g); 2/5 OUT checked (cheese/cottage 47 mean=7.56g/100g flat gradient, brined_cheeses 36 mean=14.64g/100g flat gradient) (source: 02_products/yogurt_system/guides/glp1_bucketB_protein_check_v1.md §2-6, orchestrator-verified per glp1_guide_v2_architecture.md §2.1)",
    "total_categories_recommending_products_in_glp1_guide": "5/18 (source: glp1_guide_v2_architecture.md §2.1 revised total)"
  },
  "commands_run": [
    {"cmd": "Read C:\\Bari\\tasks\\TASK-549.md", "exit_code": 0},
    {"cmd": "Glob 02_products/yogurt_system/*", "exit_code": 0},
    {"cmd": "Glob bari-web/src/data/comparisons/*.json", "exit_code": 0},
    {"cmd": "Grep 'Remilk|רמילק|Imagindairy|אימג|cow-free|רקומבינטי|recombinant' over bari-web/src/data/comparisons/*.json", "exit_code": 0},
    {"cmd": "Read 02_products/yogurt_system/guides/glp1_guide_v2_architecture.md", "exit_code": 0},
    {"cmd": "Read 02_products/yogurt_system/guides/glp1_bucketB_protein_check_v1.md", "exit_code": 0},
    {"cmd": "Read tasks/TASK-535.md, tasks/TASK-546.md", "exit_code": 0}
  ],
  "not_done": [
    "No BSIP0/corpus work opened for cow-free dairy — explicitly routed to Nutrition as a watchlist question, not answered or built here, per task brief",
    "No new collection/hub filter built for a dairy-only GLP-1 lens — recommended against, not deferred as a TODO; revisit only under the stated reversal condition",
    "Did not independently re-verify TASK-535's underlying distribution math (min/max/mean per category) beyond reading the already-orchestrator-verified artifact — relied on that prior verification per this memo's own citation, consistent with Hard Rule 9 (trace-derived, cited, not re-invented)"
  ],
  "self_check": "Acceptance test: does the memo answer whether a high-protein-dairy/GLP-1 shelf is a new category, a lens, or redundant, with the leanest form recommended and a stated anti-overbuild rationale; does it route (not answer) the cow-free dairy scoring question to Nutrition; and does it give one single best next step? Result: PASS on all three — called REDUNDANT with TASK-535 (cited, not assumed — read the actual architecture doc and bucket-B data), cow-free question framed as a precise watchlist item for Nutrition without touching scoring, and the single next step is MONITOR + route, with an explicit reversal condition and nothing new opened."
}
```
