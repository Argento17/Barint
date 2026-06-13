# Golden Comparison Page — Production Playbook v1

**Status:** CANONICAL (owner-ratified 2026-06-13). The **brined-cheeses** page is the **golden
example** — every future shelf follows this playbook; back-corrections of older pages target this
standard. Reference route: `/hashvaot/brined-cheeses`.

This is the end-to-end, repeatable process that produced the golden page, plus the hard rules and
the specific failures we hit so the next shelf skips them. Read it before starting a shelf.

---

## 0. The golden example — concrete files to copy from
| Layer | File |
|---|---|
| Frontend data (authoritative) | `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` |
| Page data / copy install | `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts` |
| Page assembly (+ scoped polish) | `bari-web/src/components/comparisons/brined-cheeses-comparison-page.tsx` |
| Prologue charts | `bari-web/src/components/comparisons/brined-cheeses-prologue-visualizations.tsx` |
| Index card | `bari-web/src/components/hashvaot/featured-brined-cheeses-intelligence-card.tsx` |
| Copy source (verified) | `02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json` |
| Render spec (per-shelf) | `01_framework/operations/brined_golden_render_spec_v1.md` |
| Scoring methodology | `02_products/brined_cheeses/methodology/` |
| Screenshot harness | `bari-web/scripts/shot-brined-charts.mjs` |
| NotebookLM/chart handoff | `02_products/brined_cheeses/notebooklm_handoff/` |

---

## 1. Pipeline — stage by stage

### Stage 1 — Shelf scrape (BSIP0)
- Direct retailer scrape only (Shufersal primary). **OFF is BANNED, every field, forever**
  (`off_ban_hard_rule`). `off_source_used` must be 0. Capture name, brand, barcode, nutrition,
  `ingredients_raw`, image_urls.

### Stage 2 — Corpus filter (the discard rule)
- A product missing data (ingredients or nutrition) from the primary scrape: **one-shot recovery
  at most, else DISCARD** — never score-punish, never over-invest in re-sourcing
  (`missing_data_discard_rule`). Brined went 48→36 this way (12 with no ingredient list dropped).
- Result: every displayed product has a verifiable ingredient list + complete core nutrition.

### Stage 3 — Scoring (BSIP2)
- Engine: `03_operations/bsip2/proto_v0/src/score_engine.py`. Per-shelf run dir under
  `02_products/<shelf>/bsip2_outputs/run_<shelf>_NNN/` with a `verification_table.csv`.
- Sodium/sugar scored **shelf-relative** (distance from the shelf median), not absolute
  (`BARI_SODIUM_SHELF_RELATIVE_V1`). Protein reweighted as a positive for protein foods
  (`BARI_DAIRY_PROTEIN_REWEIGHT_V1`). Any scoring-rule change is D7: Nutrition ruling + Product
  co-sign + no-regression proof; **C3 consult is mandatory** on "is this collapse real" calls.
- **Frozen invariants are untouchable** (e.g. milk run_005_headpin). Don't move published scores.
- **Confidence archetype:** expected-null fields are NOT data gaps. For cheese, `fiber` and
  `sugar` are expected-null — they must NOT trigger a "missing nutrition" / partial-confidence
  label when the core (kcal, protein, fat, sodium) is complete. (This was a live bug — see §3.)

### Stage 4 — Copy (Content)
- Row = a 2-line interpretive **verdict** (standing → driver → catch → earned grade), differentiated
  per product. NOT a restatement of the columns (`comparison_row_verdict_model`).
- **Brand in every product title** (`… — מחלבות גד`). No internal tokens in consumer copy
  (`run_005`, `bc-019`, flag/EV ids — banned, gated). No grade/score inside description prose.
- Intro = a human story opening + an analytical view + a few **real run stats** + Nutrition's read,
  written readably (not a stat dump). One line of genuine expressive sentiment per page.
- **Ground EVERY claim against the AUTHORITATIVE frontend JSON (v2), not an older draft.** (The v1
  sourcing error shipped two wrong brand attributions — see §3.)
- Gate before ship: `integrations/clients/hebrew_readability.py` (leakage scan must be clean;
  ≤1 em-dash per sentence). HeBERT tone gate exists for wit/irony lines (it's a guard, not a writer).

### Stage 5 — Render trio (Frontend)
- Produce: `data/comparisons/<shelf>_frontend.json` + `lib/comparisons/<shelf>-page-data.ts` +
  `components/comparisons/<shelf>-comparison-page.tsx` + `app/hashvaot/<shelf>/page.tsx` + an
  **index card on `/hashvaot`** (a page isn't "rendered" until discoverable from the index).
- Wire `imageUrl` into the row VM (images must RENDER, not just resolve). Additives dropdown
  (`AdditivePanel`) populated per product. Category-caveat box present. Polish must be **scoped**
  (e.g. a `.bc-page` style block) so the shared components don't regress for other categories.

### Stage 6 — Prologue charts (data-journalism)
- 3 charts in the prologue, before the table (owner-sanctioned drift amendment). Golden set:
  **sodium×grade ("A הוא לא דל-נתרן", the signature/thesis chart)** + **protein×fat** + **calories×score**.
- Built in **recharts** (already in the app — do NOT hand-roll SVG, do NOT add CDN Chart.js).
  Hollow-point aesthetic (transparent fill + brand-teal ring).
- **HARD RULE: grade is NEVER color-encoded.** Uniform ink dots; grade shown only as a text lane
  label. Median reference line may use the brand accent (it's a reference, not a quality signal).
- **Data-driven** from the frontend JSON (charts recompute; captions' key numbers should derive,
  not hardcode, when generalized). Mobile-first (readable at 375px).

### Stage 7 — Data hygiene (two checks that bit us)
- **Sort the frontend JSON `products` array by score descending** (stable tiebreak). The page renders
  array order; an unsorted array puts an 80/A between 76/B rows.
- **Confidence labels correct** (see Stage 3 archetype): no "missing nutrition" when core nutrition
  is present.

### Stage 8 — Verification / red-team (do NOT skip; this is where we failed most)
- `npm run build` — **capture the REAL exit code**: `npm run build > log 2>&1; echo "EXIT:$?"`.
  A `… | tail` pipe reports tail's exit code (0) and **masks a failed build**. This fooled us twice.
- **SCREENSHOT the rendered page and LOOK at it.** Harness: a dev server on a port +
  `playwright` (installed) → `scripts/shot-brined-charts.mjs` writes PNGs you Read. "Data correct +
  builds" ≠ "looks good" — they are different jobs. The first chart round passed every data check and
  was still visually terrible; only looking caught it.
- Verify every chart number against the JSON; confirm no grade-color; images render; mobile+desktop
  coherent; shared components + legacy untouched (`git status` scope check).
- Owner-ready only at **zero CRITICAL**.

---

## 2. Hard rules (non-negotiable, every shelf)
1. **OFF banned**, every field, forever. Unknown is acceptable; OFF is not.
2. **No fabrication** — no invented products, names, brands, or numbers. Verify external tool output
   (NotebookLM etc.) against the authoritative JSON before using it.
3. **Grade is never color-encoded** anywhere (rows or charts).
4. **Verify, don't trust** — every return/claim is checked against the artifact (file:line / the real
   number / the real build), never the prose.
5. **Look at the pixels** for any visual deliverable.
6. **Authoritative data = the v2 frontend JSON**, not an older draft.
7. **Frozen invariants / published scores** need the owner.
8. **Local render only** — deploy is a separate, owner-gated step.

---

## 3. Failures we hit on brined (so the next shelf skips them)
- **Hand-rolled SVG charts** = ugly. The app already has **recharts** — use it.
- **Verified data but never looked at pixels** → shipped terrible charts that passed every numeric
  check. Fix: the screenshot loop (Stage 8).
- **Pipe masked a failed build** (`… | tail` → exit 0 over a real exit 1). Fix: capture `$?` directly.
- **Copy sourced from v1, not v2** → two wrong brand attributions + a "clean" claim on a
  preservative-containing cheese. Fix: ground in the authoritative v2.
- **External tool (NotebookLM) silently swapped the charts** for off-thesis ones and dropped the
  sodium story. Its DATA was faithful (verified), but always re-check the chart CHOICE serves the
  page thesis.
- **Unsorted products array** → out-of-order rows (80 between 76s). Fix: sort by score desc in JSON.
- **Expected-null fields flagged as "missing nutrition"** (sugar/fiber for cheese). Fix: the
  confidence archetype (expected-null ≠ gap).

---

## 4. Routing / cost (how to run the next shelf efficiently)
- Spec-complete code → **C1-CURSOR** (flat). Investigation → **C1-GEMINI** (flat). Bari-judgment
  (copy/scoring/governance) → **C1 native**. Mechanical → **C2**. Outside second opinion / fresh
  eyes → **C3** (programmatic, flat). Parallelize up to 3 C1-grade tasks, one per lane. Don't hoard
  on metered Claude. (`lane_routing_rules_v1.md`, `feedback_lane_routing_antilaziness`.)
- Render→red-team→consolidate→render as ONE macro; don't re-render per fix.

---

## 5. Open generalization work (TASK-268)
The brined page is the golden **instance**, built largely by hand. To make it a one-command spine
stage (`render_local_page`) for every shelf: parameterize the chart component (derive captions, make
clean-detection exclude stabilizers not just preservatives), templatize the render trio, and fold
Stages 7–8 into the build gate. Until then, this playbook is the manual procedure.
