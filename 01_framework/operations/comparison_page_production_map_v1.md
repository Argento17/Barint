# What Happens When You Ask for a Comparison Page on "X" — Full System Map v1

**Status:** reference document (2026-06-11)
**Audience:** owner
**Question answered:** "If I ask the system to produce a comparison page on product category X, what does the system actually do, and what does each agent do at every link in the chain?"
**Grounded in:** `bari-category-factory` skill, `orchestration_model_v1.md`, `.claude/scoring.md`, `bari-qa-audit` skill, the decision authority matrix, and the most recent real run (yogurts v4 / run_yogurt_006, TASK-249).

---

## 0. The 30-Second Version

```
You: "Build a comparison page for X"
        │
        ▼
ORCHESTRATOR (main chat) ── classifies the ask, opens TASK-NNN in C:\Bari\tasks\
        │
        ▼
[A] SCOPE        Product Agent + Nutrition Agent — is X one category? what's in/out? which lenses?
[B] ACQUIRE      Data Agent — BSIP0 scrape of real retailer pages (Shufersal et al). OFF is banned.
[C] ENRICH       Data Agent — BSIP1 semantic enrichment of Hebrew ingredient text
[D] SCORE        Data Agent (engine) + Nutrition Agent (methodology) — BSIP2 10-dimension scoring
[E] VERIFY       QA Agent — traceability, hard fails, baseline freeze
[F] ATTACK       Red-Team Agent — adversarial challenge report; CRITICALs block everything
[G] WRITE        Content Agent — Hebrew verdicts, insight lines, category caveat, methodology copy
[H] PACKAGE      Data Agent — frontend JSON + D4 additive wiring + invariant checks
[I] BUILD        Frontend Agent (+ Design Agent) — route, page-data, shelf filters, build/tsc
[J] GATE         QA Agent re-verify on the live tree + owner tripwire check + read-every-string gate
[K] CLOSE        Orchestrator/CC — verify every claim against artifacts, record CLOSED
        │
        ▼
Live page at bari-web /comparisons/x — consumer sees ranked shelf with scores, verdicts, glass box
```

Typical wall-clock for a new category end-to-end: multiple working sessions across several days. Most of the calendar time is B (scraping + parse quality) and the F→D loop (red-team findings forcing rebuilds — yogurts took 6 runs).

---

## 1. Phase 0 — The Ask Arrives (Orchestrator)

**Actor:** the main chat session (the Orchestrator). It is the only process that can spawn agents; subagents cannot spawn subagents.

What it does, in order:

1. **Classify the work** (per `work_classification_v1.md`). "Produce a comparison page for X" is always **Registry Work**: multi-step, reviewed deliverable, ships a governed artifact. So it gets a task — never handled inline.
2. **Registry First.** Checks `C:\Bari\tasks\` for an existing TASK covering X. If none, opens `TASK-NNN.md` with YAML frontmatter: `id, title, owner, status: IN_PROGRESS, priority, depends_on, blocks, summary`.
3. **Tripwire scan** (decision authority matrix). A *new* category page does not by itself trip a wire — but the orchestrator notes the two wires that will fire **later** in this chain: wire 2 (irreversible + consumer-facing = the actual go-live) and wire 1 (if anything touches frozen scores: milk run_005_headpin, bread real_bread_retail_003_v1, snack-bar ceiling 70/B).
4. **Dispatch plan.** Breaks the chain into delegation specs (objective / boundaries / inputs / deliverable + return format / guards) and dispatches the owning agents directly via the Agent tool — parallel where independent, background for long runs. The owner is never handed prompts to paste.
5. **Standing rule:** after *every* tracked deliverable returns, the orchestrator runs the CC close-readiness gate (Phase K) before moving to the next link. This is an instruction, not a hook — hooks can't fire agents on SubagentStop.

**Durable state created:** `tasks/TASK-NNN.md`, dashboard entry in `05_command_center/command_center.json` (auto-refreshes via PostToolUse hook).

---

## 2. Phase A — Scoping & Category Definition

**Actors:** Product Agent (decision quality, "should we / what's the MVP"), Nutrition Agent (category interpretation), Data Agent (shelf reality check). Research Agent optionally for market/evidence context.

This is Stage 1–2 of the category factory skill:

### A1. Shelf Mapping (Category Team = Product + Data)
- Identify the canonical retailer shelf slug(s) that constitute category X (e.g., yogurts = the Shufersal yogurt shelf; "category" means a real shelf a shopper stands in front of, not an abstract food group).
- Verify each shelf exists in the shelf registry; confirm no duplicate shelf→category assignment (a shelf cannot feed two categories — merging shelves across categories needs explicit owner approval).
- **Output:** `shelf_map.json` — `{shelf_slug, category_slug, mapping_rationale}` per shelf.

### A2. Corpus Filter (Data Architecture = Data Agent)
- Write the filter rules that cut the raw shelf down to in-scope products (e.g., yogurts excludes a granola that the retailer mis-shelved — run_006 excluded barcode 7290112346797 as `cereal_misroute_excluded`).
- Validate no overlap with other live categories; confirm minimum corpus size (too sparse → halt, do not build a 6-product "comparison").
- Boundary calls that look trivial but aren't get a **Nutrition Agent ruling** recorded in memory/registry — e.g., the prepared-spread vs raw-chickpea boundary is decided by tahini+sodium+energy, never protein or the word "סלט".
- **Output:** `corpus_filter.json` with product count estimate.

### A3. Lens & Presentation Decision (Product + Nutrition, owner only if a wire fires)
- Which of the 3 comparison lenses applies (Consumer Use-Case Guardrails v2), whether the category uses the standard A–E score model or a deviation. Deviations are *strategic*: frozen vegetables dropped grades entirely for 4 use-case segment bands — that was an owner-level call and is explicitly **not a precedent**.
- The Anti-Immunity Rule is a hard constraint: no category framing may make a product class immune to its real weaknesses.

### A4. BSIP0 Gate (Stage 3 of the skill)
- Entry check before any scraping money is spent: shelf map confirmed, corpus filter non-empty, no blocking category conflicts.
- **Fail → halt and report. Do not proceed to enrichment.**
- **Output:** `bsip0_gate_result.json` (pass/fail with evidence).

---

## 3. Phase B — BSIP0: Data Acquisition (Data Agent)

**Actor:** Data Agent. **Hard law of this phase: the only source for ingredients + nutrition is the direct product scrape. Open Food Facts is banned project-wide, for any field, forever.** Unknown is acceptable; OFF is not. Any OFF dependency = launch blocker.

What actually happens:

1. **Scrape.** Retailer product pages (Shufersal primary; Yohananof, Carrefour, Wolt also supported). The Yohananof scraper is 4-stage: discover → approve → scrape → audit. Each product yields raw HTML/JSON + images.
2. **OCR (when needed).** Physical label images go through the Azure-based OCR pipeline (`03_operations/bsip0/pipeline/`).
3. **Parse.** Nutrition panel + Hebrew ingredient text extracted. The parser persists the **raw nutrition source for replay** (post EV-029: a fat-overwrite parser bug taught us never to discard the raw).
4. **Field-level honesty.** If a field doesn't parse, it is **NULL** and the page will later say "data could not be retrieved" — no substitution from any other source, ever.
5. **Outputs land at** `02_products/{category}/observations_bsip0/{retailer}/` plus a raw JSON + log per run (e.g., `yogurt_bsip0_raw_20260611T072535.json`).

**Where this phase really bites (lesson from yogurts):** parse *quality*, not parse *coverage*. run_005 looked complete but the Shufersal parser was counting website disclaimer text as ingredients on 67/89 products — corrupting NOVA inference and all three 90/A grades. Nothing downstream can see this; only the red-team phase caught it. The fix (disclaimer-strip, `ingredient_text_quality` flags, `macros_plausible` gate) is now permanent BSIP1 infrastructure.

---

## 4. Phase C — BSIP1: Semantic Enrichment (Data Agent)

**Actor:** Data Agent, running `03_operations/bsip1/core/ingredient_enricher.py` (64-check pytest suite guards it).

Per product, the enricher derives from the raw Hebrew text:

- **Ingredient signals:** white flour vs whole grain, fermentation markers, sweeteners, protein source identification.
- **Additive classification:** E-number detection (incl. parenthesized forms — E414 was added this week), burden counting.
- **Matrix-integrity signals:** whole-grain ratio, fermentation presence.
- **Data-quality flags:** `ingredient_text_quality` (`disclaimer_stripped` / `marketing_bleed` / clean), `macros_plausible` (protein=190g/100g gets flagged, not scored), BSIP1 trust level (`high`/`medium`/`low`).
- **Category-specific corrections:** e.g., post-enrichment live-cultures correction for bio/probiotic yogurts.

**Output:** one canonical JSON per product at `03_operations/bsip1/run_{category}_NNN/output/`, with an inclusion/exclusion ledger (yogurt run_006: 88 included, 8 excluded with named reasons).

This is Stage 4 of the factory skill ("BSIP1 Enrichment"); its output report covers coverage stats, label distribution, flagged products.

---

## 5. Phase D — BSIP2: Scoring (Data Agent executes, Nutrition Agent owns the logic)

**Actors:** Data Agent runs the engine; **Nutrition Agent owns every methodological choice** and must sign any rule change; the `bari-bsip2-scoring-governance` skill binds both (evidence registry, label observability, activation scope, rollback plan — no rule ships without all four).

**Engine:** BSIP2 proto v0, algorithm 0.4.1, at `03_operations/bsip2/proto_v0/src/`. A category gets its own batch runner (`batch_run_{category}_NNN.py`).

Per product, six stages:

1. **Feature extraction** — 50+ features from nutrition panel, ingredients, category, regulatory labels. Missing fields are *recorded*, never imputed. Before this, `signal_extractor.py` produces layers L1–L6 (observed → ratios → ingredient flags → additives → NOVA proxy → matrix), and **Router v2** assigns the structural archetype in 3 stages (anchors → context-gated signals → resolution).
2. **Dimension scoring** — 10 dimensions, each 0–100, weighted: processing_quality 15%, nutrient_density 15%, calorie_density 15% (category-relative tables — yogurt's "normal" is 60–250 kcal, crackers 380–480), glycemic_quality 12%, protein_quality 10%, additive_quality 10%, fat_quality 8%, satiety_support 6%, regulatory_quality 5% (Israeli red labels: sugar 17.5g, satfat 5g, sodium 600mg per 100g), whole_food_integrity 4%.
3. **Guardrails** — trans-fat veto (floor 20), hard caps (NOVA 4, multiple red labels, high sugar/sodium, additive burden — most restrictive wins), soft penalties, and floors for honest whole foods (single-ingredient NOVA 1, whole-food fats).
4. **Hyper-palatability detection** — 4 combination patterns (fat-sugar, fat-sodium, refined-carb+fat, crunch-sweet) with amplifiers (chocolate coating, glucose syrup) and relief factors (whole nuts, dates), under a cumulative family budget.
5. **Concern coordination** — the same root concern can't be punished twice; per-family budgets (sugar, sodium, calorie, processing, fat-quality) keep the primary signal at full weight and demote echoes.
6. **Final resolution** — caps → penalties → floors → **confidence ceiling** (a low-confidence product cannot score high no matter what; per TASK-250 rulings, null sugar costs −10 confidence and null satfat −5) → clamp → grade. Grades: S 90–100, A 80–89, B 65–79, C 50–64, D 35–49, E 0–34. Grade is computed **before** rounding the display score (Ruling 3 — two yogurts changed grade because of this).

**Output:** one `bsip2_trace.json` per product (the full glass-box: every fired rule, every cap, every penalty) at `02_products/{category}/bsip2_outputs/run_{category}_NNN/`, plus a run summary.

**Standing engine guard:** any engine change must re-run `run_regression_check.py` (12-case golden corpus) and `run_router_regression.py` — frozen categories (milk, bread, snacks) must show **zero diff**, or the change is gated behind an env flag (the TASK-144 pattern: `BARI_TASK144_FIXES`, default OFF).

**Stage 6 of the factory skill — BSIP2 Readiness** — is the governance wrapper here: scoring logic registered and approved, label observability in place, rollback plan exists → `bsip2_readiness_checklist.json`.

---

## 6. Phase E — QA Gate (QA Agent)

**Actor:** QA Agent, per the `bari-qa-audit` skill. Stage 5 of the factory; **hard fails block promotion, no exceptions, even for small categories.**

1. **Run the QA runner** against the exact run ID — never a stale or invalidated baseline.
2. **Traceability check:** every product traces to its corpus entry, every label to its enrichment step, every score to a registered scoring rule. Any gap = hard fail.
3. **Hard fails** (block): coverage below minimum, out-of-scope label, unregistered scoring rule, traceability gap, duplicate products, runner/pipeline version mismatch.
4. **Warnings** (must be explicitly accepted with a named acceptor, or resolved): coverage between min and target, skewed label distribution, low enrichment confidence, new labels vs baseline (drift signal).
5. **Baseline freeze:** only over a clean run — run ID + date + acceptor recorded. Contaminated runs are **invalidated** with a recorded reason and a replacement run initiated; an invalidated run may never be referenced again.

**Output:** `qa_gate_result.json` + audit report with verdict pass/fail/invalidated.

---

## 7. Phase F — Red-Team Challenge (Red-Team Agent)

**Actor:** Red-Team Agent — adversarial and independent by design. It does not fix, approve, or close; it attacks. **Stage 5b — mandatory for every category, never skipped.**

- Input: the scored corpus JSON + the category methodology rationale.
- It hunts for: data corruption the pipeline self-certified (the disclaimer-text bug), implausible values no gate caught (protein=190), misrouted products, false sweetener/fermentation detections, copy that overstates, grade boundary artifacts, ceiling compression that hides real differences.
- **Output:** `02_products/{category}/reports/red_team_{corpus_version}.md`, every finding classified CRITICAL / HIGH / MEDIUM.
- **Gate:** open CRITICALs block advancement absolutely. HIGHs must be resolved or explicitly accepted in writing in the report.
- **The loop:** CRITICAL findings route back to Nutrition Agent (methodology) and Data Agent (pipeline) → fixes → **full regeneration as a new run number** → QA re-audit → red-team re-audit. Scores are expected to move; that's the point. Yogurts went run_005 → run_006 exactly this way: 12 RT findings produced 7 parser fixes + 5 methodology rulings (TASK-250), 14 products changed grade, and one false 90/S dropped to 89.9/A when the disclaimer strip removed fake fermentation keywords.

**Why both E and F exist:** QA verifies the pipeline did what it claims (propagation, traceability). Red-Team challenges whether what it claims is *true* (independent evidence). They catch disjoint failure classes.

---

## 8. Phase G — Consumer Copy (Content Agent)

**Actor:** Content Agent, writing **all** consumer-facing Hebrew. Bound by the editorial constitution stack: Editorial Intelligence v3 (insight-first, framework invisibility, consumer attention test), Assertive Writing v1 (finding-first, no-apology, 130+ phrase library), Insight Line Spec v1 (3 line types, grammar test, "restrained but fearless" — quiet lines on unremarkable products are *correct*), Score Presentation v1 (numeric/grade only — "72/B"; no strength labels; no color-encoding of judgment; 3 confidence states).

Deliverables per category:

1. **Hero/prologue** — what this shelf is and what Bari found, insight-first.
2. **Row verdicts** — each collapsed comparison row is a 2-line *human verdict* (standing → why → catch → grade), not terse tags. Verdicts must name calorie density + the *real fired driver* from the trace; **sodium appears as a displayed fact only, never as a driver the engine didn't fire** (standing rule, rollout pending across 8 legacy categories).
3. **Insight lines** — per-product, typed per the spec, derived from actual trace data. 9 phrases are banned outright (Explanation Engine v2). Internal jargon never leaks: "NOVA 4" became "עיבוד תעשייתי גבוה"; missing data reads "ערך הסוכר לא היה זמין במקור הנתונים", not "מדד זה לא נכלל בניתוח".
4. **Category caveat ("הערת קטגוריה")** — owner-mandated yellow box on EVERY comparison page, grounded in real engine behavior for this category (e.g., yogurts must disclose ceiling compression per Ruling 5).
5. **Methodology blurb** — how to read the scores, in consumer language.

**Hard gate attached to this phase (memory: read-copy-before-ship):** before any category push, a human-level read of **every** consumer-facing string. Generated copy has fabricated provenance before ("official food source" shipped live and was false). Deliberate deviations from editorial rules require an Exception Registry entry *first*.

---

## 9. Phase H — Frontend Packaging + D4 Wiring (Data Agent)

**Actor:** Data Agent. Stages 7 + 8 of the factory skill.

1. **Build the frontend JSON** via a category builder script (`build_{category}_frontend_vN.py`): per product — id, name, score, grade, insight line, confidence level, image URL, Hebrew ingredients, nutrition panel, limiting factors, glass-box payload, cluster/segment assignment. RTL-safe labels, Hebrew coverage validated.
2. **Apply data-honesty blocks:** products failing `macros_plausible` are blocked from the frontend entirely; `marketing_bleed` ingredient text is hidden (`ingr_text=None`) rather than displayed.
3. **D4 additive wiring (Stage 8, mandatory):** a `wire_d4_{category}.py` script runs `detect_additives_d4()` over every product's BSIP1 ingredient text and attaches each detected E-number with its Hebrew explanation from `w2_additive_copy_v1.md` (34 E-numbers, Content Agent owns the copy). Coverage gate: <15% ingredient-text coverage → halt and investigate. **Hard invariant: score, grade, and glassBox must be byte-identical before/after wiring** — D4 annotates, never moves a score.
4. **Builder assertions:** structural checks (e.g., every `_cluster` value ∈ valid cluster IDs), config hash recorded in the run record for reproducibility.

**Output:** `{category}_frontend_vN.json` in the data workspace, then copied to `bari-web/src/data/comparisons/` — the **only** thing the website ever consumes from the pipeline.

---

## 10. Phase I — Website Implementation (Frontend Agent + Design Agent)

**Actors:** Frontend Agent implements; Design Agent owns hierarchy/spacing/interaction and reviews against the canonical reference.

All work happens in `bari-web/` (Next.js) — never at the repo root. Governance stack: Frontend Integration v1 (10-section entry checklist, **7 canonical components only**), Canonical Reference Declaration (מעדנים is the reference implementation; 14 prohibited Gen-0 patterns), Legacy Isolation Policy (milk/bread/snack legacy tree never crosses into canonical builds), Design Token Governance (7 token categories, no improvising values), View Model v1 (**the UI never sorts, rounds, or interprets** — the JSON→`BariProductVM` transform in `src/lib/view-models/` and `src/lib/comparisons/` is the only interpretive layer).

Per category, the Frontend Agent creates/extends:

- `src/data/comparisons/{category}_frontend_vN.json` — the data drop.
- `src/lib/comparisons/{category}-comparison-page-data.ts` — page-data adapter (JSON → VM).
- `src/lib/comparisons/{category}-shelf-filters.ts` — typed shelf filter ids + Hebrew labels (yogurts gained a "bio" / "ביו/פרוביוטי" filter this way).
- The route + page composition from the 7 canonical components (comparison rows, glass-box preview, category caveat box, shelf filter bar, etc.).

**Exit criteria:** `tsc` passes, `next build` passes, RTL rendering verified, mobile hierarchy verified (current product phase metric: a mobile user understands the shelf in 15–20 seconds).

---

## 11. Phase J — Pre-Go-Live Gates (QA Agent + Orchestrator + Owner)

The page exists on a branch. Before it ships, four distinct gates, in order:

| # | Gate | Holder | What it checks |
|---|------|--------|----------------|
| 1 | **QA propagation re-verify** | QA Agent | The *live tree* matches the frozen run: scores in the built site == BSIP2 traces, no stale JSON, routes resolve, baseline frozen on the final artifacts |
| 2 | **Read-every-string** | Orchestrator + Content Agent | Every consumer-facing string read in full; no fabricated provenance/authority |
| 3 | **Owner tripwire** | **Owner** | Wire 2 always fires here: category go-live is irreversible + consumer-facing. Also wire 1 if any *published* grade changes (yogurts: two products changing published grade required explicit owner sign-off on Ruling 3 before launch) |
| 4 | **OFF-ban sweep** | QA Agent | No Open Food Facts dependency anywhere in the category's data, copy, images, or fallbacks — any hit is a launch blocker |

Only after all four: merge to master → deploy. The "frozen framing" rule applies at launch: freeze the *framing* ("best ≠ excellent"), version the *numbers* (every rescore re-verifies them).

---

## 12. Phase K — Verification & Close (Orchestrator / CC)

**Actor:** the Orchestrator wearing the CC hat. Domain agents only ever propose `RETURNED` or `BLOCKED` in a structured return block — **they never write CLOSED.**

For each returned task in the chain:

1. Read the return block's claims.
2. **Verify every claim against the artifact itself** — file:line, real numbers, not prose. ("88 products, 0 errors" → open the run summary and count.)
3. Hunt for unstated side-effects (did the engine change touch a frozen category? run the regression evidence).
4. Risk-classify; genuine judgment calls route per the authority matrix (owning agent → Product → owner only on a tripwire).
5. Record `status: CLOSED` with a `close_reason` citing evidence; open whatever the close unblocks (`blocks`/`depends_on` graph).
6. Report the decision map. Dashboard refreshes automatically.

Durable state at the end: closed TASKs in the registry, frozen QA baseline, red-team report at all-findings-closed, run records with config hashes, memory entries for any new ruling that future categories must respect.

---

## 13. Agent-by-Agent Responsibility Matrix

| Agent | Phases | Does | Never does |
|---|---|---|---|
| **Orchestrator (main chat)** | 0, J, K | Classifies, opens TASKs, dispatches 5-part delegation specs, runs the CC close gate after every return, closes with evidence | Executes pipeline work itself; hands the owner prompts to paste |
| **Product Agent** | A, J | Category go/no-go, scope rationalization, lens choice, kills overbuild, signs cross-category engine-rule adoption | Writes copy, touches the engine, gates pipeline stages it doesn't own |
| **Nutrition Agent** | A, D, F-loop | Category interpretation, boundary rulings, owns scoring methodology + every TASK-250-style ruling, resolves red-team methodology findings | Runs scrapers; closes its own tasks; manufactures differentiation where clustering is the honest finding |
| **Research Agent** | A (optional), F-loop | Evidence for rules (literature, USDA FDC; Tzameret directional-only), competitor/market context | Makes decisions — it produces evidence only |
| **Data Agent** | B, C, D, H | BSIP0 scrape + OCR, BSIP1 enrichment, BSIP2 batch runs, frontend JSON build, D4 wiring, regression runs | Uses OFF (banned); imputes missing fields; changes methodology without Nutrition sign-off |
| **QA Agent** | E, J | QA runner, traceability, hard-fail enforcement, warning adjudication, baseline freeze/invalidate, live-tree propagation re-verify, OFF sweep | Accepts a warning without a named acceptor; freezes over hard fails; skips traceability "because small category" |
| **Red-Team Agent** | F | Independent adversarial audit of scores, data, copy claims; CRITICAL/HIGH/MEDIUM report | Fixes, approves, closes — attack-only by design |
| **Content Agent** | G, (H copy source), J | All Hebrew consumer copy: verdicts, insight lines, caveat box, methodology, D4 additive explanations | Inventing data; leaking framework jargon; deviating from editorial law without an Exception Registry entry |
| **Frontend Agent** | I | Route, page-data adapter, shelf filters, canonical-component composition, tsc/build green | Sorting/rounding/interpreting in the UI; touching pipeline code; creating non-canonical components |
| **Design Agent** | I | Hierarchy, spacing, interaction review against the canonical reference; drift detection | Implementing data logic |
| **Marketing Agent** | post-launch | SEO/content/growth for the live page | Gating or initiating any pipeline stage |
| **Owner (you)** | A (only if strategic), J | Tripwire decisions only: go-live sign-off, published-grade changes, frozen invariants, new strategic framing | Everything else — autonomy-default means the system decides and logs |

---

## 14. The Artifact Trail (What Exists on Disk After a Full Run)

```
tasks/TASK-NNN.md                                        ← registry record, CLOSED w/ evidence
02_products/{cat}/shelf_map.json                          ← A1
02_products/{cat}/corpus_filter.json                      ← A2
02_products/{cat}/bsip0_gate_result.json                  ← A4
02_products/{cat}/observations_bsip0/{retailer}/...       ← B  raw scrape per product
03_operations/bsip1/run_{cat}_NNN/output/*.json           ← C  canonical enriched records
02_products/{cat}/bsip2_outputs/run_{cat}_NNN/*.json      ← D  per-product glass-box traces
02_products/{cat}/reports/run_{cat}_NNN_run_summary.json  ← D  run summary + config hash
qa_gate_result.json + baseline freeze record              ← E
02_products/{cat}/reports/red_team_{corpus}.md            ← F  all findings closed/accepted
01_framework/glass_box/w2_additive_copy_v1.md             ← G/H  (shared, 34 E-numbers)
02_products/{cat}/{cat}_frontend_vN.json                  ← H  packaged + D4-wired
bari-web/src/data/comparisons/{cat}_frontend_vN.json      ← H→I  the only pipeline→web handoff
bari-web/src/lib/comparisons/{cat}-comparison-page-data.ts← I
bari-web/src/lib/comparisons/{cat}-shelf-filters.ts       ← I
05_command_center/command_center.json                     ← K  dashboard state
```

---

## 15. Hard Laws That Bind the Entire Chain

1. **OFF ban (absolute):** no Open Food Facts data anywhere — nutrition, ingredients, names, images, fallback, validation, copy, confidence. NULL beats borrowed data. Any dependency = launch blocker.
2. **No invented data:** product/nutrition/ingredient facts come from the scrape or are absent.
3. **Frozen invariants:** milk = run_005_headpin (top 85/A), bread = real_bread_retail_003_v1, snack-bar ceiling = 70/B. Engine changes must prove zero diff on frozen categories or hide behind a default-OFF flag.
4. **Gates are sequential and non-skippable:** BSIP0 → enrichment → QA → red-team → readiness → packaging → D4. No frontend packaging before QA passes; no advancement past Stage 5 with open CRITICALs; no shipped JSON without D4 wiring.
5. **Honest findings stand:** if scores genuinely cluster, that's the finding — never add signals to manufacture differentiation (butter precedent).
6. **Separation of powers:** the engine scores, content explains, the UI displays. The UI never interprets; copy never claims what the trace didn't fire; D4 never moves a score.
7. **Closing authority is singular:** only the orchestrator/CC records CLOSED, only after artifact-level verification.
8. **Owner touches exactly two points** in a normal category run: the strategic scoping call *if* it's novel, and the go-live tripwire. Everything else is autonomous and logged.

---

## 16. Worked Example — Yogurts v4 (the most recent full traversal)

- **Phase B–D:** Shufersal yogurt shelf scraped; BSIP1 + BSIP2 produced run_yogurt_005; frontend v4 built. Looked clean.
- **Phase E+F:** QA FAIL + red-team FAIL. RT found the parser was counting website disclaimer text as ingredients on 67/89 products (corrupting NOVA + all three 90/A grades) and a protein=190 corruption no gate had blocked. 12 findings total.
- **The loop (Phase F→C/D):** TASK-249 (Data Agent) fixed 7 parser-level issues; TASK-250 (Nutrition Agent) issued 5 methodology rulings (null-sugar confidence −10, null-satfat −5, grade-before-round, sweetener detection, ceiling-compression disclosure). Full regeneration as **run_yogurt_006**: 88 products, 0 errors, A:14 B:30 C:20 D:23 E:1; one product blocked outright for implausible macros; the false 90/S fell to 89.9/A.
- **Phase G:** copy templates corrected in the same pass (NOVA jargon out, honest missing-data lines in); category caveat update routed to Content Agent (Ruling 5).
- **Phase J (current state, 2026-06-11):** three gates open before go-live — owner sign-off on the two published-grade changes (tripwire 2), Content Agent caveat copy, QA baseline freeze on run_006.
- **Phase K:** TASK-249 sits at RETURNED; CC will verify the return block's claims against the run artifacts before recording CLOSED.

This run is the system working as designed: the page was *buildable* after run_005, but four independent gates refused to let a corrupted corpus reach consumers, and the loop produced a measurably honest run_006.

---

*End of map. Known weak links and improvement candidates are deliberately out of scope here — that's the agreed next document.*
