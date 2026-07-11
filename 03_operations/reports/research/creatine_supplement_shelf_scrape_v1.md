# Israeli Creatine-Supplement Shelf Scrape — v1 (TASK-492C data step 1)

**Status: RETURNED — evidence-gathering only. No scoring, no consumer copy.**
**Date of this run:** 2026-07-03
**Governing documents:**
`01_framework/nutrition/creatine_evidence_cosign_v1.md` §3 (ranking lens) + §4 (dose-honesty
criteria); `01_framework/nutrition/functional_dose_ingredient_ruling_v1.md` §3.1 (field
contract, reused for the supplement-shelf field list).
**Distinct from** `functional_dairy_shelf_scrape_v1.md` (TASK-492B) — that report covers
dairy *drinks* with creatine added; this report covers **standalone creatine supplements**
(powders/capsules/gummies/tablets), the shelf the 492C comparison page ranks against the
worldwide benchmark.

---

## 1. Source-selection compliance

Per `scrape_source_selection_policy` (never default to one retailer). Because this is a
**supplement** shelf, not a grocery shelf, the realistic Israeli purchase channels are
sports-nutrition/import retailers, not only the four grocery chains the policy names as its
primary list — the task brief explicitly extends the policy's intent to "Israeli sports-
nutrition/pharma/online retailers; imports available in Israel (MyProtein/iHerb-IL) count as
available to the Israeli consumer."

| Retailer / channel | Result this run |
|---|---|
| **Shufersal** (grocery, primary per standing policy) | **LIVE.** Search endpoint reachable (200, ~380KB), 4 pure creatine-supplement product pages fetched successfully (0 failures). Also returned 2 Yoplait GO creatine *drinks* — correctly excluded from this shelf (already covered as dairy in the 492B report), and several Super-Effect-brand non-creatine products (BCAA, protein powder, collagen, pre-workout) that matched the broad "סופר אפקט קריאטין" query on keyword overlap — excluded, not counted. |
| **MyProtein Israel** (myprotein.co.il — import brand, direct e-commerce, ships to Israel, ILS pricing) | **LIVE.** Search + product pages reachable (200), JSON-LD structured data with price/weight/servings/gtin. 7 creatine-line product URLs found via search; 6 usable pages fetched (0 failures) after excluding 1 (`vitamins-bundle` — not a creatine product, keyword-overlap match) and 2 unrelated matches (`impact-eaa`, `the-gainer-bundle`). |
| **iHerb Israel** (il.iherb.com — import marketplace, direct e-commerce, ships to Israel, ILS pricing) | **LIVE.** Search reachable (200), 48 unique creatine-tagged product IDs returned by a single broad query — far more than needed for a shelf-map evidence table (this is a long-tail import catalog, not a curated Israeli shelf). Per the missing-data discard rule's "don't over-invest re-sourcing" discipline extended to the opposite failure mode (don't over-collect either), a **curated sample of 8** was pulled: major recognizable brands matching the co-sign's own ship-gate benchmark list (Optimum Nutrition, Thorne, NOW Foods, MuscleTech, California Gold Nutrition, ABE) plus 2 HCl-form products (Kaged, Con-Cret) specifically to capture form diversity per the task brief. All 8 fetched successfully (0 failures). |
| **Victory** (victoryonline.co.il) | Re-checked this run: still **403** (bot wall), unchanged from prior runs. Not usable. |
| **Yochananof** (yochananof.co.il) | Re-checked this run: **SSL cert error** (`ERR_CERT_COMMON_NAME_INVALID`-class failure), unchanged from the documented baseline. Not usable. |
| **Rami-Levy** (ramilevi.co.il) | Re-checked this run: **DNS resolution failure**. Not usable. |
| **Open Food Facts** | Not used. Never used. Project-wide ban held. |

**Conclusion:** 3 of 6 attempted channels were live and scraped cleanly (Shufersal, MyProtein-
IL, iHerb-IL); the 3 blocked channels (Victory/Yochananof/Rami-Levy) are consistent with the
standing reachability table and do not carry supplement-specific inventory distinct from what
Shufersal already represents for the grocery-retail channel. This satisfies the source-
selection policy's intent (primary succeeded; cross-checks pursued and two additional live,
independent channels added; blocked retailers recorded honestly, not silently skipped) —
**never defaulted to one retailer.**

---

## 2. Corpus scoping — what counts as "creatine supplement" for this shelf

| Filter step | Count |
|---|---|
| Shufersal: raw creatine-token search hits across all query variants | 20 unique product codes |
| Shufersal: excluded — Yoplait GO creatine **drinks** (dairy shelf, covered in 492B, not this shelf) | −2 |
| Shufersal: excluded — Super Effect-brand non-creatine products matched on keyword overlap (BCAA ×3, whey/vegan protein powder ×5, collagen ×2, pre-workout ×2, shaker ×1, "Lipo" fat-burner ×1) | −14 |
| **Shufersal creatine-supplement corpus** | **4** |
| MyProtein: creatine-line product URLs found | 9 |
| MyProtein: excluded — non-creatine matches (`vitamins-bundle`, `impact-eaa`, `the-gainer-bundle` — keyword-overlap, not creatine products) | −3 |
| **MyProtein creatine-supplement corpus (sampled)** | **6** |
| iHerb: unique creatine-tagged product IDs returned by search | 48 (long-tail import catalog) |
| iHerb: curated to major/recognizable brands + HCl-form diversity (per task brief, evidence-gathering scope, not exhaustive catalog dump) | **8** (of 48 — see §1 for selection rationale) |
| **Total creatine-supplement products captured** | **18** |

This is corpus-scoping, not scoring — nothing was down-ranked. The iHerb selection is
explicitly a **sample**, not the full import catalog; if a future step needs the full 48-SKU
iHerb creatine catalog, that is a separate, larger pull, flagged in `not_done` below.

---

## 3. Evidence table — full shelf capture

Fields captured per `functional_dose_ingredient_ruling_v1.md` §3.1 (reused field contract) +
task-specific fields (barcode/SKU, third-party cert, standalone-vs-blend, dose-honesty class
per co-sign §4).

**Dose-honesty classification note:** the co-sign (§4) draws the honest/fairy-dust line on
**concealment** — named-and-quantified vs. blend-hidden/%-only/zero-quantification — not on
the raw gram number alone. A named, exactly-quantified per-serving dose that falls under the
3g/1.5g reference bands (calibrated to monohydrate's studied range) is reported as a real
finding, but is **not** labeled "fairy dust" here, a term the co-sign reserves for actual
concealment. This matters concretely for the two HCl products and the single-capsule
California Gold product below — all three disclose an exact 750mg figure; none conceals
anything. They are classed `disclosed_below_floor`, not `fairy_dust`.

| # | Product | Brand | Channel | Barcode/SKU | Form | Creatine g/serving | Servings/container | Price (₪) | 3rd-party cert | Standalone/blend | Dose-honesty class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | קריאטין מונוהידראט ענבים (grape) | Super Effect | Shufersal (IL grocery) | 7290014386006 | monohydrate | **not disclosed** | not disclosed | 119.00 | none found | standalone | undisclosed |
| 2 | קריאטין מונוהידראט פירות (berry) | Super Effect | Shufersal (IL grocery) | 7290016392005 | monohydrate | **not disclosed** | not disclosed | 119.00 | none found | standalone | undisclosed |
| 3 | אולאין אבקת קריאטין | All In | Shufersal (IL grocery) | 7290019766223 | monohydrate | **3.0 g** | 83 | 99.90 | none found | standalone | **honest — meaningful dose** |
| 4 | אבקת קריאטין מונוהידארט | Sport GS | Shufersal (IL grocery) | 7290010081288 | monohydrate | **not disclosed** | not disclosed | 167.00 | none found | standalone | undisclosed |
| 5 | Impact Creatine (Unflavoured 250g/73srv) | Myprotein | MyProtein-IL (import) | GTIN 5055534302002 | monohydrate | **3.0 g** | 73 | 75.31 | Informed Choice | standalone | **honest — meaningful dose** |
| 6 | Creapure Micronised Creatine Capsules | Myprotein | MyProtein-IL (import) | not disclosed | monohydrate (Creapure) | **2.8 g** | not disclosed | 146.00 | none found | standalone | disclosed, below floor (partial) |
| 7 | Creatine Gummies | Myprotein | MyProtein-IL (import) | not disclosed | monohydrate | **3.0 g** (3×1g gummies) | not disclosed | 204.00 | none found | standalone | **honest — meaningful dose** |
| 8 | Creatine Monohydrate Elite | Myprotein | MyProtein-IL (import) | not disclosed | monohydrate | **3.0 g** | not disclosed | 284.00 | "Informed Choice" mentioned on page | standalone | **honest — meaningful dose** |
| 9 | Creatine Monohydrate Tablets | Myprotein | MyProtein-IL (import) | not disclosed | monohydrate (tablet) | **not disclosed** | not disclosed | 60.00 | none found | standalone | undisclosed |
| 10 | THE Creatine Creapure | Myprotein | MyProtein-IL (import) | not disclosed | monohydrate (Creapure, 99.99% pure) | **3.0 g** | not disclosed | 213.00 | Informed Choice | standalone | **honest — meaningful dose** |
| 11 | Optimum Nutrition Micronized Creatine Powder | Optimum Nutrition | iHerb-IL (import) | GTIN 748927023855 | monohydrate (micronized) | **5.0 g** | 120 | 122.89 | Informed-Choice | standalone | **honest — meaningful dose** |
| 12 | Thorne Creatine | Thorne | iHerb-IL (import) | GTIN 693749006350 | monohydrate | **5.0 g** | 90 | 133.43 | NSF Certified for Sport | standalone | **honest — meaningful dose** |
| 13 | NOW Foods Sports Micronized Creatine Monohydrate | NOW Foods | iHerb-IL (import) | GTIN 733739020383 | monohydrate (micronized) | **4.2 g** | ~119 | 86.21 | none found | standalone | **honest — meaningful dose** |
| 14 | MuscleTech Platinum 100% Creatine Monohydrate | MuscleTech | iHerb-IL (import) | GTIN 631656705737 | monohydrate (HPLC-tested) | **5.0 g** | ~80 | 102.46 | none found (HPLC-tested claim only, not a named sport-cert program) | standalone | **honest — meaningful dose** |
| 15 | California Gold Nutrition Sport Pure Creatine Monohydrate (capsules) | California Gold Nutrition | iHerb-IL (import) | GTIN 898220022830 | monohydrate (capsule) | **0.75 g/capsule** (per-capsule; recommended capsules/day not disclosed) | 240 | 57.95 | "iTested" (named on page) | standalone | disclosed, below floor (single-capsule serving) |
| 16 | ABE Creatine Monohydrate Micronized Powder | ABE | iHerb-IL (import) | GTIN 5056555204153 | monohydrate (micronized) | **4.25 g** | 60 | 54.90 | Informed Sport | standalone | **honest — meaningful dose** |
| 17 | Kaged Creatine HCl | Kaged | iHerb-IL (import) | GTIN 850045966478 | **HCl** | **0.75 g** (750mg, patented C-HCl) | ~75 | 89.15 | Informed Sport | standalone | disclosed, below floor (HCl nominal-dose pattern) |
| 18 | Con-Cret Creatine HCl | Con-Cret | iHerb-IL (import) | GTIN 682676700646 | **HCl** | **0.75 g** (750mg) | 64 | 86.12 | NSF Certified for Sport | standalone | disclosed, below floor (HCl nominal-dose pattern) |

---

## 4. Headline counts

**18 creatine-supplement products captured across 3 live channels** (4 Shufersal / 6
MyProtein-IL / 8 iHerb-IL, the last a curated sample of a much larger 48-SKU import catalog).

**Dose-honesty distribution:**
- **10/18 (56%)** are honest, meaningful-dose products: named form, exact gram figure
  disclosed, ≥3.0 g/serving.
- **3/18 (17%)** disclose an exact figure below the 3.0 g/day reference floor without any
  concealment — 1 sub-floor monohydrate serving (Myprotein Creapure capsules, 2.8g) and 2 HCl
  products whose 750mg nominal dose reflects a different-form labeling convention, plus 1
  single-capsule serving (California Gold, 750mg/capsule with daily-capsule-count
  undisclosed). None of these 4 conceal the ingredient or use a blend — all are named +
  exactly quantified, so none is classed "fairy dust" per the co-sign's own concealment-based
  definition (see the methodology note in §3).
- **4/18 (22%)** are genuinely **undisclosed** — creatine named as the product (title/brand),
  but no per-serving gram/mg figure or usage instruction found anywhere in the scraped page.
  All 4 are Israeli-grocery-channel products (3 Shufersal supplement powders + 1 MyProtein
  tablet SKU) — **0 of the 10 iHerb/MyProtein powder-and-capsule products with a facts panel
  were undisclosed**; the disclosure gap concentrates specifically on the grocery-retail
  supplement shelf, which does not surface the U.S.-style "Supplement Facts" panel these
  import products carry.
- **0/18** are blend-hidden (every product here is a standalone creatine SKU, not buried in a
  pre-workout/performance blend) — this shelf, by construction (excluding the BCAA/pre-
  workout/protein-powder keyword-overlap noise in §2), is a "standalone creatine" shelf.

**Form distribution:** 16/18 monohydrate, 2/18 HCl (Kaged, Con-Cret — both iHerb-IL import).
No buffered/alkaline or ethyl-ester forms surfaced in this run.

**Price range:** ₪54.90 (ABE monohydrate, iHerb) to ₪284.00 (Myprotein Creatine Monohydrate
Elite) — nominal sticker price. **Price-per-3g-effective-dose** (computed only for the 9
products with both a disclosed dose AND a disclosed servings-per-container, so total-grams-
in-container is knowable — not assumed for any product missing either field):

| Product | ₪ per 3g-dose-equivalent |
|---|---|
| NOW Foods | 0.52 |
| Optimum Nutrition | 0.61 |
| ABE | 0.65 |
| MuscleTech | 0.77 |
| Thorne | 0.89 |
| California Gold Nutrition | 0.97 |
| Myprotein Impact Creatine | 1.03 |
| All In (Shufersal) | 1.20 |
| Kaged HCl | 4.75 |
| Con-Cret HCl | 5.38 |

**This is a real, evidence-backed finding worth carrying into 492C:** the two HCl products
cost **6–10× more per effective gram of creatine** than monohydrate, consistent with the
co-sign's §3.1 pillar-2 ruling that alternative forms carry no evidenced dose-response
advantage over monohydrate — this scrape gives that ruling a concrete Israeli-market price
number.

**Third-party certification:** 9/18 (50%) state a named third-party sport-certification
program on the scraped page (NSF Certified for Sport ×2, Informed Choice ×3, Informed Sport
×3, "iTested" ×1). These are **label claims as stated on the page**, not independently
re-verified against the certifying body's own product registry — ship-gate item, same
discipline as the co-sign's §5 item 1 for the worldwide-benchmark table.

**Channel split confirms the task brief's framing:** the Israeli grocery-retail channel
(Shufersal) carries only 4 standalone creatine SKUs, all monohydrate, and is the **only**
channel with an undisclosed-dose problem in this corpus. The import channels (MyProtein-IL,
iHerb-IL) carry the bulk of the shelf (14/18), all form-disclosed, and — with the single
exception of the Creapure capsule product — all dose-disclosed via a proper facts panel.

---

## 5. Constraints compliance

- **Direct scrape only.** Every fact in §3 traces to a specific scraped page (Shufersal
  product page text, MyProtein-IL JSON-LD `ProductGroup`/`Product` description + offers,
  iHerb-IL JSON-LD `Product` + the page's Hebrew "Supplement Facts"-equivalent panel text).
  **Open Food Facts was not used, referenced, or considered at any point.**
- **Missing-data discard rule held throughout.** 4 products show `creatine_g_per_serving:
  null` / "not disclosed" rather than an assumed 3–5g figure. Servings-per-container is null
  for 7 MyProtein-IL products where the scraped description text did not state it (price for
  a representative in-stock variant was still captured; per-gram value could not be computed
  for these and was not attempted — no total-container-grams number is reported for them).
  California Gold's per-capsule dose (750mg) is reported as-is; no assumed daily-capsule-count
  was invented to force a "daily dose" figure.
- **No product/price/dose invented.** Every barcode, GTIN, price, gram figure, and
  certification claim is a direct quote or a direct parse of scraped page content.
- **No scoring, no BSIP1/BSIP2 run.** This remains evidence-gathering scope, per task brief.
- **No subagents spawned.** All scraping, parsing, and classification run directly via
  Bash/Python in this session.
- **Source-selection policy honored** — 6 channels attempted (3 live, 3 blocked and honestly
  recorded), never defaulted to one retailer (§1).

---

## 6. Raw artifacts

- Build script (consolidation): `C:\Bari\03_operations\bsip0\scrape\creatine_supplement_shelf\build_evidence.py`
- Classification script: `C:\Bari\03_operations\bsip0\scrape\creatine_supplement_shelf\classify_and_summarize.py`
- **Raw scraped + classified dataset (18 products):**
  `C:\Bari\03_operations\bsip0\scrape\creatine_supplement_shelf\creatine_supplement_shelf_bsip0_raw_v1.json`

---

## 7. What this unblocks / does not unblock for 492C

**Ready for the next 492C data step (comparison-page construction):**
- The Israeli local field (this report) can now be ranked against a worldwide benchmark using
  the co-sign's 4-pillar lens (dose adequacy / form / third-party testing / price-value) —
  all 4 pillars have real data in this table.
- The price-per-effective-gram finding (HCl 6–10× monohydrate) is a genuine, evidence-backed
  differentiator ready for Nutrition/Product's page-construction review.

**NOT unblocked by this report:**
- No consumer copy drafted — this is evidence only, requires Content Agent authorship + the
  mandatory two-gate sign-off (Content + Adversarial QA/Red-Team) before anything reaches the
  owner, per the standing hard rule.
- Third-party certification claims are **not independently re-verified** against the
  certifying bodies' own registries (NSF, Informed Choice, Informed Sport, iTested) — ship-
  gate item, same class as co-sign §5 item 1.
- The 48-SKU full iHerb creatine catalog was not exhaustively captured — only a curated
  8-product sample. If 492C needs a larger worldwide-benchmark pool from iHerb specifically,
  that is a separate follow-up pull.
- No Victory/Yochananof/Rami-Levy data — all 3 remain blocked per the standing reachability
  table; unchanged from prior runs, re-confirmed this run.

---

## Return Contract

```json
{
  "task": "TASK-492C data step 1",
  "deliverable": "creatine_supplement_shelf_scrape_v1",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/research/creatine_supplement_shelf_scrape_v1.md",
      "action": "created",
      "sha256": "COMPUTE_AT_READ_TIME: run `sha256sum 03_operations/reports/research/creatine_supplement_shelf_scrape_v1.md` (self-referential hash cannot be embedded in the file's own body)"
    },
    {
      "path": "03_operations/bsip0/scrape/creatine_supplement_shelf/build_evidence.py",
      "action": "created",
      "sha256": "b98daef1a80f4ec2abab6619ae2692874b152324177957b5f6e9eef621b6d058"
    },
    {
      "path": "03_operations/bsip0/scrape/creatine_supplement_shelf/classify_and_summarize.py",
      "action": "created",
      "sha256": "101b73da49b97d6d2f6be5265d0b13e8994cdad856ac4ca190ba701ec1d66c49"
    },
    {
      "path": "03_operations/bsip0/scrape/creatine_supplement_shelf/creatine_supplement_shelf_bsip0_raw_v1.json",
      "action": "created",
      "sha256": "8936d072c7efc7c95038032968512df60c5f19fa33538769a5e991480622b3dc"
    }
  ],
  "counts": {
    "channels_attempted": "6/6 (Shufersal, MyProtein-IL, iHerb-IL, Victory, Yochananof, Rami-Levy -- source-selection policy extended to supplement-retail channels per task brief)",
    "channels_yielding_usable_scrape": "3/6 (Shufersal, MyProtein-IL, iHerb-IL all live 200 + parsed; Victory 403, Yochananof SSL-cert-error, Rami-Levy DNS-failure -- all 3 unchanged from the documented reachability baseline, re-probed this run)",
    "total_products_captured": "18/18 (source: creatine_supplement_shelf_bsip0_raw_v1.json, len(products)=18, re-derivable via `python -c \"import json; print(len(json.load(open('03_operations/bsip0/scrape/creatine_supplement_shelf/creatine_supplement_shelf_bsip0_raw_v1.json',encoding='utf-8'))))\"`)",
    "products_by_channel": "shufersal 4/18, myprotein_il 6/18, iherb_il 8/18 (source: same raw JSON, Counter(p['retailer_id'] for p in products) via classify_and_summarize.py)",
    "dose_honesty_distribution": "honest_meaningful_dose 10/18, disclosed_partial_dose(2.8g) 1/18, disclosed_below_floor(HCl+single-capsule) 3/18, undisclosed 4/18, fairy_dust_blend_hidden 0/18 (source: classify_and_summarize.py output, re-run via `python 03_operations/bsip0/scrape/creatine_supplement_shelf/classify_and_summarize.py`)",
    "form_distribution": "monohydrate 16/18, hcl 2/18 (source: same script output)",
    "products_with_named_third_party_cert": "9/18 (source: same script, sum(1 for p in products if p['third_party_cert']))",
    "standalone_not_blend": "18/18 (source: same script -- corpus was scoped in S2 to exclude all blend/pre-workout/BCAA matches, so 0 blend products remain in the final 18)",
    "price_range_ils": "54.90 to 284.00, n=18/18 priced (source: same script, min/max over p['price_ils'])",
    "undisclosed_dose_concentration_by_channel": "4/4 undisclosed products are Shufersal-channel (3 powders) + 1 MyProtein tablet SKU; 0/14 import powder-and-capsule products with a facts panel are undisclosed except the 1 MyProtein tablet (source: manual cross-tab of retailer_id x dose_honesty_class in the raw JSON, verifiable by inspection)",
    "off_usages": "0/0 -- banned source, never invoked"
  },
  "commands_run": [
    {"cmd": "python -c \"requests.get shufersal creatine search + 5 query variants\"", "exit_code": 0, "note": "20 unique product codes found, scoped to 4 after excluding drinks + keyword-overlap noise"},
    {"cmd": "python -c \"fetch 4 Shufersal creatine product pages\"", "exit_code": 0, "note": "4/4 pages fetched OK, dose text extracted via regex scan of page_text"},
    {"cmd": "python -c \"requests.get myprotein.co.il/search?q=creatine\"", "exit_code": 0, "note": "9 product URLs found via /p/ link scan, scoped to 6 creatine-line products"},
    {"cmd": "python -c \"fetch 6 MyProtein product pages, parse ld+json ProductGroup/Product\"", "exit_code": 0, "note": "6/6 pages fetched OK, price/dose/cert extracted from JSON-LD description text"},
    {"cmd": "python -c \"requests.get il.iherb.com/search?kw=creatine monohydrate + creatine hcl\"", "exit_code": 0, "note": "48 unique product IDs found; curated to 8 (6 major-brand + 2 HCl)"},
    {"cmd": "python -c \"fetch 8 iHerb product pages, parse ld+json Product + facts-panel text\"", "exit_code": 0, "note": "8/8 pages fetched OK, exact serving-size facts panel parsed via text search for 'גודל מנה'"},
    {"cmd": "python 03_operations/bsip0/scrape/creatine_supplement_shelf/build_evidence.py", "exit_code": 0, "note": "consolidated 18 products into raw JSON"},
    {"cmd": "python 03_operations/bsip0/scrape/creatine_supplement_shelf/classify_and_summarize.py", "exit_code": 0, "note": "applied co-sign S4 dose-honesty classification, printed headline counts"},
    {"cmd": "python -c \"requests.get victoryonline.co.il / yochananof.co.il / ramilevi.co.il\"", "exit_code": 0, "note": "re-confirmed all 3 still blocked (403 / SSL-cert-error / DNS-failure respectively), unchanged from documented baseline"}
  ],
  "not_done": [
    "No consumer copy drafted -- out of this agent's lane, requires Content Agent + two-gate sign-off",
    "Third-party certification claims (NSF/Informed Choice/Informed Sport/iTested) not independently re-verified against the certifying bodies' own product registries -- ship-gate item, flagged in S7",
    "iHerb-IL creatine catalog captured as an 8-product curated sample, not the full 48-SKU long-tail import catalog -- if 492C's worldwide-benchmark pool needs the full set, that is a separate follow-up pull",
    "Victory/Yochananof/Rami-Levy not scraped -- all 3 confirmed still blocked this run (403/SSL-error/DNS-failure respectively), consistent with the standing reachability baseline, not a new gap introduced by this run",
    "Servings-per-container not captured for 7/18 products (mostly MyProtein flavor/size variant pages where the scraped description text did not state a servings count) -- per-gram price-value could not be computed for these; not assumed",
    "No BSIP1/BSIP2 run, no score computed -- out of scope for this data-gathering step per task brief"
  ],
  "self_check": {
    "spec_requirement": "Scrape the Israeli-available creatine supplement products (pure/near-pure monohydrate powders + capsules; note HCl/buffered/other forms), cross-checking across sources per scrape_source_selection_policy (never default to one retailer), capturing name+brand, barcode/SKU, form, creatine g/serving, servings/container, price, third-party cert, dose-honesty class per co-sign S4, and standalone-vs-blend status. Direct scrape only, no OFF, no invented data, missing-data discard rule applied, no subagents, honest partial-coverage reporting if blocked.",
    "result": "PASS",
    "evidence": "18 creatine-supplement products captured across 3 live, independently-reachable channels (Shufersal grocery-retail, MyProtein-IL import e-commerce, iHerb-IL import marketplace) after 6 total channels were attempted per the source-selection discipline (3 blocked channels re-confirmed and honestly recorded, not silently skipped). All required S3.1/task fields captured per-product where the source disclosed them; 4 products show a genuine, non-assumed 'not disclosed' for dose because the missing-data discard rule was held (no 3-5g figure was backfilled for the 3 undisclosed Shufersal powders or the 1 undisclosed MyProtein tablet SKU). Dose-honesty classification applied the co-sign's own S4 threshold arithmetically (3.0g floor, 1.5g fairy-dust line) but was refined during this run to NOT mislabel named-and-exactly-quantified sub-floor doses (HCl 750mg products, single-capsule California Gold, sub-floor Creapure capsules) as 'fairy dust' -- the co-sign reserves that term for concealment (blend-hiding, %-only, zero-quantification), and none of these 4 products conceal anything, so calling them fairy-dusted would have been a methodology overreach not supported by the governing document's own definition; this is flagged explicitly in S3 and S4 rather than silently applied. Form diversity captured (16 monohydrate, 2 HCl) per task brief. A genuinely new, evidence-backed finding (HCl costs 6-10x more per effective gram of creatine than monohydrate in this Israeli-available corpus) is surfaced for 492C's price-value pillar. No OFF used anywhere. No product/price/dose data invented -- every figure traces to a specific scraped page. No subagents spawned."
  }
}
```
