## 1. Recommendation

Build the PD first as a **versioned, deterministic materialized projection over the existing canonical artifacts**, not as a new transactional store that BSIP0/1/2 directly read from and write to. A big-bang unified writable record would create two authorities during migration, enlarge the blast radius, and violate tripwire-1 precisely when the evidence chain is incomplete. The PD’s single job is: **resolve every product’s identity, evidence, existing derived analysis, and validation state into one immutable, inspectable contract without changing the facts or scores that produced the published product.** This is still the canonical product spine—but initially a canonical **read model and contract**, with ownership migrated field-family by field-family only after parity gates prove it safe. The end state may consolidate storage behind that contract; the first release must not pretend that consolidation has already happened.

## 2. PD data model I would commit to

### Record envelope

Every dossier is generated through one shelf-independent pipeline and validated against one versioned schema:

```text
ProductDossier
  schema_version
  dossier_id
  product_id
  generation:
    generated_at
    generator_version
    input_artifact_ids
    input_hashes
    replay_run_id
  layer_1_identity
  layer_2_evidence
  layer_3_analysis
  layer_4_checks
```

Use the stable internal `product_id` as the dossier key. Barcode is an attribute and lookup alias, never the primary key. A PD exists even when the barcode is absent, malformed, or conflicting.

The generated artifact should be immutable and content-addressed or revisioned. Regeneration creates a new revision; it must not overwrite historical evidence silently. A small dossier index may map `product_id → current dossier revision` and valid verified barcode aliases. The projection should be rebuildable entirely from named inputs.

Ownership must be explicit in the schema:

- `source_owner`: artifact family authoritative for the value.
- `source_artifact_id` and `source_artifact_hash`.
- `source_path`: exact field or trace location.
- `derivation`: `copied`, `parsed`, `calculated`, `validated`, or `manual_decision`.
- `observed_at` and `generated_at`, kept distinct.
- `producer_version`.

The PD generator may resolve and present data, but it may not silently correct source artifacts.

### Layer 1 — Identity

**Initial sources of truth**

- `product_id` and canonical product membership: the existing served/corpus product registry or manifest mapping.
- Product name: the existing verbatim scraped/served string. No cleanup.
- Brand, category, package size, manufacturer, and source URLs: existing direct-scrape artifacts, with the currently served record retained as the publication reference where relevant.
- Capture references, last successful scrape, and scrape history: TASK-601 manifest and canonical captures.
- Barcode observations: direct captures plus future TASK-607 results.
- Barcode state and verified lookup aliases: a new, narrowly scoped **identity-resolution ledger**, because no existing artifact owns the five-state adjudication model.

The identity ledger is the one justified new authoritative store. It should contain decisions, not duplicate the underlying evidence:

```text
identity_resolution
  product_id
  barcode_state
  candidate_observations[]
  accepted_barcode: string|null
  decision_method
  decision_reason_code
  decided_at
  evidence_refs[]
  manual_decision_ref|null
```

Manual decisions are append-only, attributable, and reversible by supersession. They never rewrite the raw capture.

**Generation**

The PD generator joins product membership, served identity, manifest/capture metadata, and the identity-resolution ledger. It reports conflicts rather than choosing a convenient value unless an explicit resolution rule or manual decision exists.

### Layer 2 — Raw evidence and provenance

**Source of truth**

TASK-601’s canonical capture manifest and its referenced direct product captures are authoritative. The PD does not copy these into a second evidence database. It carries normalized evidence references and, where practical, the exact captured source text needed for inspection.

Each material field should expose an evidence cell:

```text
EvidenceField<T>
  value: T|null
  status: observed|not_found|parse_failed|conflicting|not_captured
  source_kind: direct_product_scrape
  source_url
  capture_id
  source_text
  extraction_method
  parser_version
  observed_at
  confidence
  manual_override|null
```

`confidence` describes evidential reliability; it must never substitute a value. If the one-shot scrape did not find the datum, `value` is `null`, with a reason such as `not_found` or `not_captured`.

OFF is not a valid enum member for `source_kind`. The schema validator must reject any nutrition or ingredient field whose lineage is not a direct product capture. This is stronger than a runtime convention.

Manual overrides belong in an append-only decision overlay referencing the original evidence. The resolved display value may show the override, but both original and override remain visible. An override cannot introduce an estimated nutrition or ingredient value; it may only adjudicate directly observed evidence or correct mapping under an authorized process.

### Layer 3 — Derived analysis

Layer 3 must contain two separate namespaces:

```text
analysis:
  product_quality:
    nutrition_dimensions
    ingredient_dimensions
    processing_indicators
    additive_signals
    category_relative_scores
    published_score_snapshot
  data_quality:
    evidence_strength
    data_completeness
    identity_confidence
    barcode_confidence
    image_confidence|null
```

**Sources of truth**

- Published scores and category-relative results: served comparison JSONs are authoritative for what is currently published.
- Calculation provenance and intermediate scoring inputs: BSIP2 traces are authoritative.
- Parsed and normalized nutrition/ingredient inputs: BSIP1 outputs/traces, linked back to Layer 2 evidence.
- Completeness and confidence metrics: newly derived by the PD generator from explicit, versioned rules. These are operational metadata, not product scores.

For the MVP, the PD must copy the published score snapshot exactly and link it to the corresponding BSIP2 trace. It must not recalculate and replace it. If replayed calculation differs, the dossier records a failed calculation check in Layer 4 while continuing to display the published value as published.

Longer term, stage-local derived artifacts may be migrated behind the PD contract. The migration unit is an entire field family, not an individual field. A family changes ownership only after:

1. deterministic replay exists;
2. corpus-wide parity is proven against the prior artifact;
3. all consumers read the new contract;
4. the old writer becomes read-only;
5. the old representation is retired.

At no point should two stores both accept authoritative writes for the same field family.

### Layer 4 — Checks

Layer 4 is newly generated validation state, not another fact store:

```text
checks:
  identity
  barcode
  nutrition_table
  ingredients
  image
  source_traceability
  category_assignment
  calculation
  publishability
```

Each check has:

```text
status: pass|warn|fail|unknown|not_applicable
reason_codes[]
evidence_refs[]
checked_at
checker_version
blocking_scope: none|internal_generation|future_consumer_publish
```

Checks consume Layers 1–3 and never mutate them. The internal dossier should be generated even with failures; otherwise the products most in need of inspection disappear.

`publishability` in the MVP is **diagnostic shadow state only**. It cannot change current publication. Future scanner publication must use a separately versioned policy and the two-gate sign-off.

## 3. Barcode-state design

The five required states attach to the identity resolution for a stable `product_id`:

- `verified`: one syntactically valid, check-digit-valid barcode is supported by sufficient direct evidence or an authorized manual decision.
- `found-but-conflicting`: multiple plausible valid observations exist and no accepted resolution is established.
- `malformed`: barcode-like text was captured but fails structural validation, including truncation or check-digit failure.
- `not-found`: a qualifying capture was inspected and no barcode was present.
- `pending-manual-review`: evidence exists that automated rules deliberately cannot adjudicate.

I would also keep the evidence-availability distinction outside this state: a product lacking a usable raw capture is not falsely classified as `not-found`. Its barcode state should be `pending-manual-review` only if queued for review; otherwise the evidence cell records `not_captured` and the barcode check is `unknown`. If the five-state requirement is exhaustive, `pending-manual-review` must cover this unresolved condition with a reason code such as `NO_REPLAYABLE_CAPTURE`.

The model stores all observed candidates, preserving leading zeroes as strings. Validation includes symbology/length rules and check digits where applicable. No numeric coercion is allowed anywhere.

Pipeline enforcement:

- Product joins and PD generation use `product_id`, never barcode.
- Scanner lookup indexes only accepted barcodes from `verified` records.
- All other barcode states produce no scanner alias.
- A malformed/conflicting/missing barcode lowers `barcode_confidence` and causes a barcode `warn`, `fail`, or `unknown`; it does not suppress the dossier, null unrelated fields, alter quality scores, or break BSIP processing.
- TASK-607 writes new observations and resolution decisions, not edits to product names or scores.
- The present truncation failure is retired by forbidding inferred completion, preserving the captured text, validating as a string, and routing malformed values to state rather than using them as identifiers.

## 4. Quality vs data-quality mechanism

This separation must be enforced by type and policy, not labels alone.

- `product_quality` and `data_quality` are sibling schema objects with distinct types.
- Product-quality calculators may consume observed facts and BSIP inputs, but cannot read data-quality fields.
- Data-quality calculators may inspect provenance, presence, conflicts, and validation results, but cannot alter product-quality outputs.
- No top-level `overall_score` field is permitted.
- The schema rejects formulas whose input domains cross the boundary.
- The internal API returns separate radar series with explicit axis domains:
  - quality radar: nutrition, ingredient simplicity, processing, additive burden, category performance;
  - evidence radar: evidence strength, completeness, identity confidence, barcode confidence, eventually image confidence.
- The UI may overlay selectable series only when their meanings and scales are explicit. It must not draw a single polygon that visually implies one composite quality measure.
- Evidence weakness is displayed alongside a score, never multiplied into it, used to cap it, or treated as a penalty.
- Unknown inputs remain unknown; completeness is descriptive and cannot trigger estimation or rescoring.

Add a regression test that fails if any product-quality output changes when only provenance/completeness/barcode state changes. Add the inverse test that evidence metrics can change without changing the published score snapshot.

## 5. MVP boundary

The thinnest honest first cut is a schema, generator, validator, corpus index, and utilitarian internal inspection surface—not the full envisioned experience.

### Include now

- One versioned PD revision per served product, keyed by stable `product_id`.
- Input hashes and exact references to manifest entries, captures, BSIP1 artifacts, BSIP2 traces, and served JSON.
- Layer 1 identity with verbatim names and the five-state barcode model.
- Layer 2 evidence cells for barcode, nutrition, ingredients, and the other identity fields already recoverable from direct captures.
- Layer 3 snapshot of existing published scores plus linked BSIP2 calculation inputs; distinct basic completeness and evidence metrics.
- Layer 4 checks for identity, barcode, nutrition, ingredients, source traceability, category assignment, calculation parity, and shadow publishability.
- A corpus-wide list/filter page and a plain per-product inspection page sufficient to find:
  - malformed/conflicting/missing barcodes;
  - absent captures;
  - trace-to-served mismatches;
  - missing evidence;
  - calculation mismatches.
- A machine-readable barcode lookup index containing verified aliases only.
- Replay determinism, schema validation, OFF-lineage rejection, and exact served-score parity gates.
- Explicit coverage reporting: every served product must produce either a valid dossier or a visible generation failure. Silent omission is forbidden.

This is zero-throwaway scanner foundation because the schema, verified alias index, provenance contract, and validation states are the same backend primitives a scanner will need.

### Defer explicitly

- Polished two-page visual design.
- Radar rendering and interactive layer controls; retain radar-ready structured dimensions.
- Consumer scanner UI and scanner-result copy.
- Any scanner publication decision or consumer-facing publishability policy.
- Image-confidence calculation until there is a defensible image evidence model.
- Automated cross-source conflict resolution beyond deterministic high-confidence rules.
- Broad manual-review workflow tooling; initially support an append-only decisions file/ledger and filtered queues.
- Historical trend visualization.
- Consolidating or deleting BSIP0/1/2 stage-local stores.
- New scoring dimensions or scoring philosophy.
- Rescraping solely to make the dossier appear complete.
- Bespoke shelf adapters.

Page 2’s information must exist in the data model from the start, but its polished interface can wait. A simple structured evidence/checks panel is enough for the MVP.

## 6. Sequencing against TASK-602 / parser fix / 601 / 563 / 607

### 1. Freeze invariants and the contract

Before pipeline work, define the PD schema, source-ownership matrix, allowed lineage vocabulary, barcode state transitions, and corpus invariants:

- one dossier outcome per served product;
- published score and comparison fields byte- or value-equivalent;
- no OFF lineage;
- no invented values;
- missing remains null;
- names remain verbatim;
- no product-quality/data-quality cross-dependencies.

Capture the current 710-product served set and hashes as the publication parity baseline.

### 2. Land and verify TASK-601 first

The capture manifest, canonical keys, supersession/dedup behavior, replay harness, committed baseline, and `--check` gate are prerequisites for trustworthy Layer 2 generation. The PD should consume TASK-601, never reproduce its capture reconciliation logic.

The PD schema/generator skeleton and served/trace adapters can be developed in parallel, but no dossier evidence should be declared canonical before manifest identities are stable.

### 3. Land the shared parser fix before accepting new parsed outputs

Fix and regression-test the `bsip0_nutrition.py` classify/first-value bug. Pin parser versions in evidence lineage.

Do not block a first projection of the current published state on rewriting history. Generate a pre-fix audit projection if useful, but mark affected parsed evidence with its actual parser version. Only the fixed parser may produce the new baseline used for forward migration.

### 4. Run TASK-602 through the fixed, replayable path

TASK-602 should produce new direct captures into TASK-601’s manifest and replay framework. It must not write hand-shaped PD records. The PD projection is regenerated from the new manifest revision.

Diffs must be classified:

- expected new or changed raw observations;
- parser-output changes;
- identity/barcode-state changes;
- forbidden published-score changes.

Tripwire-1 means the rescrape cannot automatically move currently published scores through the PD project. Changed evidence can be inspected without changing the served snapshot.

### 5. Build the MVP projection and parity gates

Join the stabilized manifest/captures, BSIP1 outputs, BSIP2 traces, and served JSON. Generate all dossiers and checks. Require:

- complete corpus accounting;
- deterministic replay;
- published-value parity;
- explicit unresolved lineage;
- zero forbidden sources;
- no silent fallbacks.

This step should expose, rather than conceal, the current 14/16 non-re-derivability issue.

### 6. Address TASK-563 as trace-recovery work, not PD customization

For the eight non-recoverable-trace shelves, repair the shared artifact production/replay path. Do not add per-shelf dossier loaders. Until repaired, the dossier records `source_traceability = fail/unknown` with named missing artifacts and continues to exist.

If uniform recovery cannot be achieved immediately, retain the served JSON as the publication snapshot and truthfully mark calculation lineage incomplete. That is preferable to fabricated traceability.

### 7. Run TASK-607 barcode backfill through the identity-resolution path

Once stable `product_id`, captures, and barcode validation rules exist, TASK-607 can add direct observations and resolution decisions. It must update barcode state and the verified lookup index without altering scores or unrelated identity fields.

Prioritize the 146 malformed/truncated records and products with scanner-relevant uncertainty, but run one uniform mechanism across all products. Backfill completion is not required to ship the internal inspection MVP; the MVP is the tool that makes the backfill governable.

### 8. Only then consider write-side consolidation

After at least one full successful replay and a stable operating period, evaluate migrating stage outputs behind the PD contract. Proceed one field family at a time with dual-read comparison, never dual-authoritative writes. Consumer scanner work begins only after verified-barcode coverage, lookup behavior, and two-gate review are adequate.

## 7. Top 3 risks + kill-criteria

### Risk 1: The projection becomes a second, drifting copy

Materializing resolved fields could create another store whose values diverge from captures, traces, or served JSON.

**Controls:** immutable revisions, input hashes, exact source paths, deterministic generation, no free-form dossier edits, and regeneration-only updates.

**Kill-criterion:** If a dossier field cannot be reproduced from its declared artifact plus versioned rule, or operators begin editing generated dossier JSON directly, stop treating the materialized PD as canonical. Reduce it to an on-demand view until lineage and the decision ledger are fixed.

### Risk 2: “Confidence” quietly changes product quality or publication

Barcode/evidence weakness could become a penalty, cap, fallback trigger, or blended radar score, violating both tripwire-1 and the missing-data rule.

**Controls:** separate schema namespaces and calculator dependency graphs; no composite score; regression tests proving quality invariance under data-quality-only changes.

**Kill-criterion:** Any corpus diff shows a published/product-quality value changed solely because capture availability, barcode state, confidence, or completeness changed. Halt rollout and split the calculation paths before proceeding.

### Risk 3: The unified projection hides unresolved upstream non-replayability

A visually complete PD could falsely imply that served pages are re-derivable when traces are missing or inconsistent.

**Controls:** calculation and traceability checks distinguish `pass`, `fail`, and `unknown`; served JSON remains explicitly labeled as the publication snapshot; every derived value names its actual trace or admits that none exists.

**Kill-criterion:** If the generator must reverse-engineer calculation inputs from served outputs, use shelf-specific recovery logic, or fabricate provenance to achieve full coverage, reject the projection as dishonest. Ship incomplete dossiers with explicit failures and repair TASK-563/upstream replayability first.

The architecture is wrong only if the existing artifacts cannot supply stable product identity or deterministic lineage even after TASK-601 and trace repair. Short of that, a canonical, immutable projection is the lowest-risk route to the owner’s unified spine: one contract now, progressive ownership migration later, and no period in which PD construction can silently change what Bari publishes.


--- STDERR ---
OpenAI Codex v0.144.1
--------
workdir: C:\Users\HP\AppData\Local\Temp\tmpp5b5yc5o
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 019f5004-f42c-73b0-89ab-8ce011ecd96c
--------
user
# STF FRAME — Product Dossier ("PD") architecture

You are one of two independent SST-tier strategists in a Bari Strategy Task Force (STF).
You receive ONLY this frame — not the other seat's view, not the chair's. Write your full,
independent position to your assigned scratchpad file and return it. Do NOT implement anything;
this is strategy only.

## The question
The owner has DECIDED to build a canonical **Product Dossier (PD)** — one per product in the
current corpus (~710 served products across 20 shelves) — with a 4-layer structure, a 2D-radar
visual, a two-page internal inspection interface, positioned as the data-model foundation for
Bari's future **barcode scanner**. He triggered this after discovering 146/710 (21%) served
products carry a malformed/truncated barcode, plus a standing verifiability gap: 398/757 products
have NO stored raw-capture, and published pages are not re-derivable from their named traces on
14/16 shelves.

**This STF is NOT "should we build the PD" — the owner has decided.** Your job is to stress-test
and converge the **architecture, boundaries, and sequencing** so the build is right the first
time and honestly serves BOTH the internal-inspection need now AND the scanner later.

## OWNER AMENDMENT (load-bearing — the decisive reframe)
**"Essentially this encapsulates also BSIP1 and BSIP2 and BSIP0. All in one go. This is a huge
structural shift."** The PD is NOT an inspection page bolted on top of the pipeline — the owner
intends it as the **canonical product spine that unifies all three BSIP stages**:
- **BSIP0** (acquire/scrape → raw captures) feeds PD **Layer 2 (raw evidence + provenance)**.
- **BSIP1** (ingredient parse / enrichment / normalization) feeds PD **Layer 3 (derived) inputs**.
- **BSIP2** (scoring / traces) feeds PD **Layer 3 (category-relative scores)** and **Layer 4
  (calculation check)**.
- **Layer 1 (identity)** spans all three; **Layer 4 (checks)** is the cross-stage validation gate.
This makes the central crux SHARPER: does the PD become the **single canonical record BSIP0/1/2 all
read-from and write-to** (a genuine data-model re-architecture, migrating three stage-local stores
into one spine), or a **unifying VIEW/projection** that leaves BSIP0/1/2 stores in place and
assembles the dossier over them (manifest + captures + traces + served JSON)? Both are "one PD per
product"; they differ enormously in blast radius, migration cost, and drift risk. Take a firm
position on which, and stage the transition so nothing published moves (tripwire-1) and no stage
breaks mid-migration. Treat this as a spine-level structural decision, not a UI feature.

## The owner's specified structure (his intent, condensed — treat as requirements to satisfy, not to relitigate)
- **Layer 1 — Identity:** internal product ID, barcode OR barcode-status, brand, product name,
  category, package size, manufacturer, source URLs, last scrape date. **Barcode is NOT mandatory
  for the record to exist.** Explicit states: `verified` / `found-but-conflicting` / `malformed` /
  `not-found` / `pending-manual-review`. A broken barcode must **reduce confidence, not break the
  pipeline.**
- **Layer 2 — Raw evidence:** every important field carries provenance — value, source, extraction
  method, timestamp, confidence, original source text, manual override (if any).
  e.g. `protein_per_100g: {value 8.2, source manufacturer_page, source_text "חלבון 8.2 גרם",
  confidence high, verified_at 2026-07-11}`. Directly addresses the "not traceable" problem.
- **Layer 3 — Derived analysis:** SEPARATE raw facts from Bari calculations. Nutrition dims,
  ingredient dims, processing indicators, additive signals, category-relative scores, data
  completeness, evidence confidence, image confidence, barcode confidence. **Do not mix scraped
  values and calculated scores in the same layer.**
- **Layer 4 — Product checks:** machine-readable health state — identity / barcode / nutrition-
  table / ingredients / image / source-traceability / category-assignment / calculation /
  publishability checks.
- **Visual product view:** a clean **2D radar/polygon** (NOT 3D — 3D hides values & hurts
  comparison), with **user-selectable layers**. Candidate dims: nutritional quality, ingredient
  simplicity, processing level, additive burden, category performance, evidence strength, data
  completeness, identity confidence. **Owner explicit: do NOT combine product quality and data
  quality into one score — they mean different things.**
- **Interface (internal now, scanner-result foundation later):**
  Page 1 (overview): image, identity+barcode status, main radar, key strengths, key concerns,
  comparison vs category, overall evidence confidence, publishability status.
  Page 2 (evidence & checks): nutrition data+source, ingredient list+source, barcode validation,
  cross-source conflicts, missing fields, calculation inputs, failed validations, scrape history,
  manual decisions.
- Purpose: the internal product inspection page NOW; the foundation for the **barcode scanner
  result page** later.

## Bari hard constraints that BOUND any answer (non-negotiable)
- **OFF ban (absolute):** the ONLY nutrition/ingredient source is the direct product scrape;
  unknown is acceptable, OFF is not. PD provenance must NEVER admit an OFF-sourced field anywhere.
- **Missing-data-discard rule:** data not found one-shot → the field is NULL and the page says
  "data could not be retrieved"; never punish/cap/re-source/estimate. PD "confidence" must NOT
  become a backdoor to synthesize or infer missing values.
- **Do-not-invent-data; product names are verbatim strings** (tidying a truncated retail name = fabrication).
- **Tripwire-1:** PD must NEVER mutate a published score or scoring philosophy. It is a read-side
  record/inspection layer.
- **Systematic-not-artisanal + uniform-baseline:** PD is a pipeline output with ONE schema and ONE
  generation path — no bespoke per-shelf loaders.
- **Two-gate sign-off** governs anything consumer-facing. The internal inspection page is internal;
  the future scanner result page WILL be consumer (two-gate applies then).
- **Existing assets the PD must RECONCILE WITH, not duplicate:**
  - TASK-601 **capture provenance manifest** (canonical key + supersession + dedup; 807 canonical
    captures over the raw-source objects) + the **replay-everything harness** + committed baseline
    + `--check` regression gate (Shadow1 pattern).
  - **BSIP2 scoring traces** (per-product scoring provenance) and the **served comparison JSONs**
    (the current published record).
  - the shared **BSIP0 nutrition parser** (`bsip0_nutrition.py`) — currently has a live
    classify/first-value bug feeding a separate fix.

## The real decision space (take an explicit position on EACH)
1. **Build-vs-derive (the central crux):** Is the PD a NEW authoritative store, or a
   VIEW/projection assembled from existing stores (manifest + captures + traces + served JSON)?
   Where is the single source of truth for each layer? What, if anything, does the PD own that
   nothing else owns today?
2. **Layer boundaries:** Does the owner's 4-layer split map cleanly onto existing artifacts, or
   force duplication/drift? Where does each layer's data physically live and get written?
3. **Barcode-state model:** how the 5 states attach to identity, how "confidence reduces, pipeline
   never breaks" is enforced, and how this retires the current truncated-barcode failure mode.
4. **Quality vs data-quality separation:** how to STRUCTURALLY guarantee the two axes never merge
   (schema shape, radar layers, no blended score) per the owner's explicit rule.
5. **Anti-overbuild MVP boundary:** the thinnest PD that (a) unblocks the internal barcode/
   traceability audit NOW and (b) is the honest, no-throwaway foundation for the scanner — vs what
   is explicitly deferred (radar polish, page 2, scanner UI, image confidence).
6. **Sequencing & dependencies:** ordering vs the in-flight baseline re-scrape (TASK-602), the
   parser fix (other session), the TASK-601 manifest, the 8 non-recoverable-trace shelves
   (TASK-563), the barcode backfill (TASK-607). What must land first, what can parallelize.

## Decision criteria (what makes one architecture WIN)
- Single source of truth per field; REDUCES the current drift/duplication surface, never adds one.
- Reuses the TASK-601 manifest + replay + BSIP2 traces as the spine rather than a parallel store.
- STRUCTURALLY enforces: OFF-never, missing=NULL-not-invented, quality≠data-quality, tripwire-1 read-only.
- Thin MVP that ships internal-inspection value now AND is the honest scanner foundation (zero throwaway).
- Uniform: one schema, one generation path, all shelves.

## Required output — write your full position to your scratchpad file, then return it
1. **Recommendation** (1 paragraph): build-vs-derive verdict + the PD's single job in one sentence.
2. **PD data model you'd commit to** — per layer, WHERE each field's source of truth lives
   (new store vs existing artifact) and how it is generated.
3. **Barcode-state design** + how "confidence not a blocker" is enforced end-to-end.
4. **Quality vs data-quality** — the structural mechanism that keeps them separate.
5. **MVP boundary** — the thinnest first cut + an explicit deferral list.
6. **Sequencing** against TASK-602 / parser-fix / 601 / 563 / 607 — what lands first.
7. **Top 3 risks + kill-criteria** (what evidence would tell us this architecture is wrong).

Be decisive and specific. Reason from the constraints. This is a hard call — give your genuine
best architecture, not a survey of options.


---
## YOU ARE THE GPT / SOL 5.6 SEAT (read-only)
You cannot write files — output your FULL independent position as your response text, using the
required 7-part structure above (Recommendation / data model per layer / barcode-state / quality-
vs-data-quality mechanism / MVP boundary / sequencing / top-3 risks + kill-criteria). Be decisive
and specific; commit to ONE architecture. This is a blind position — you have not seen the other
seat's view. Reason from the Bari constraints.

codex
## 1. Recommendation

Build the PD first as a **versioned, deterministic materialized projection over the existing canonical artifacts**, not as a new transactional store that BSIP0/1/2 directly read from and write to. A big-bang unified writable record would create two authorities during migration, enlarge the blast radius, and violate tripwire-1 precisely when the evidence chain is incomplete. The PD’s single job is: **resolve every product’s identity, evidence, existing derived analysis, and validation state into one immutable, inspectable contract without changing the facts or scores that produced the published product.** This is still the canonical product spine—but initially a canonical **read model and contract**, with ownership migrated field-family by field-family only after parity gates prove it safe. The end state may consolidate storage behind that contract; the first release must not pretend that consolidation has already happened.

## 2. PD data model I would commit to

### Record envelope

Every dossier is generated through one shelf-independent pipeline and validated against one versioned schema:

```text
ProductDossier
  schema_version
  dossier_id
  product_id
  generation:
    generated_at
    generator_version
    input_artifact_ids
    input_hashes
    replay_run_id
  layer_1_identity
  layer_2_evidence
  layer_3_analysis
  layer_4_checks
```

Use the stable internal `product_id` as the dossier key. Barcode is an attribute and lookup alias, never the primary key. A PD exists even when the barcode is absent, malformed, or conflicting.

The generated artifact should be immutable and content-addressed or revisioned. Regeneration creates a new revision; it must not overwrite historical evidence silently. A small dossier index may map `product_id → current dossier revision` and valid verified barcode aliases. The projection should be rebuildable entirely from named inputs.

Ownership must be explicit in the schema:

- `source_owner`: artifact family authoritative for the value.
- `source_artifact_id` and `source_artifact_hash`.
- `source_path`: exact field or trace location.
- `derivation`: `copied`, `parsed`, `calculated`, `validated`, or `manual_decision`.
- `observed_at` and `generated_at`, kept distinct.
- `producer_version`.

The PD generator may resolve and present data, but it may not silently correct source artifacts.

### Layer 1 — Identity

**Initial sources of truth**

- `product_id` and canonical product membership: the existing served/corpus product registry or manifest mapping.
- Product name: the existing verbatim scraped/served string. No cleanup.
- Brand, category, package size, manufacturer, and source URLs: existing direct-scrape artifacts, with the currently served record retained as the publication reference where relevant.
- Capture references, last successful scrape, and scrape history: TASK-601 manifest and canonical captures.
- Barcode observations: direct captures plus future TASK-607 results.
- Barcode state and verified lookup aliases: a new, narrowly scoped **identity-resolution ledger**, because no existing artifact owns the five-state adjudication model.

The identity ledger is the one justified new authoritative store. It should contain decisions, not duplicate the underlying evidence:

```text
identity_resolution
  product_id
  barcode_state
  candidate_observations[]
  accepted_barcode: string|null
  decision_method
  decision_reason_code
  decided_at
  evidence_refs[]
  manual_decision_ref|null
```

Manual decisions are append-only, attributable, and reversible by supersession. They never rewrite the raw capture.

**Generation**

The PD generator joins product membership, served identity, manifest/capture metadata, and the identity-resolution ledger. It reports conflicts rather than choosing a convenient value unless an explicit resolution rule or manual decision exists.

### Layer 2 — Raw evidence and provenance

**Source of truth**

TASK-601’s canonical capture manifest and its referenced direct product captures are authoritative. The PD does not copy these into a second evidence database. It carries normalized evidence references and, where practical, the exact captured source text needed for inspection.

Each material field should expose an evidence cell:

```text
EvidenceField<T>
  value: T|null
  status: observed|not_found|parse_failed|conflicting|not_captured
  source_kind: direct_product_scrape
  source_url
  capture_id
  source_text
  extraction_method
  parser_version
  observed_at
  confidence
  manual_override|null
```

`confidence` describes evidential reliability; it must never substitute a value. If the one-shot scrape did not find the datum, `value` is `null`, with a reason such as `not_found` or `not_captured`.

OFF is not a valid enum member for `source_kind`. The schema validator must reject any nutrition or ingredient field whose lineage is not a direct product capture. This is stronger than a runtime convention.

Manual overrides belong in an append-only decision overlay referencing the original evidence. The resolved display value may show the override, but both original and override remain visible. An override cannot introduce an estimated nutrition or ingredient value; it may only adjudicate directly observed evidence or correct mapping under an authorized process.

### Layer 3 — Derived analysis

Layer 3 must contain two separate namespaces:

```text
analysis:
  product_quality:
    nutrition_dimensions
    ingredient_dimensions
    processing_indicators
    additive_signals
    category_relative_scores
    published_score_snapshot
  data_quality:
    evidence_strength
    data_completeness
    identity_confidence
    barcode_confidence
    image_confidence|null
```

**Sources of truth**

- Published scores and category-relative results: served comparison JSONs are authoritative for what is currently published.
- Calculation provenance and intermediate scoring inputs: BSIP2 traces are authoritative.
- Parsed and normalized nutrition/ingredient inputs: BSIP1 outputs/traces, linked back to Layer 2 evidence.
- Completeness and confidence metrics: newly derived by the PD generator from explicit, versioned rules. These are operational metadata, not product scores.

For the MVP, the PD must copy the published score snapshot exactly and link it to the corresponding BSIP2 trace. It must not recalculate and replace it. If replayed calculation differs, the dossier records a failed calculation check in Layer 4 while continuing to display the published value as published.

Longer term, stage-local derived artifacts may be migrated behind the PD contract. The migration unit is an entire field family, not an individual field. A family changes ownership only after:

1. deterministic replay exists;
2. corpus-wide parity is proven against the prior artifact;
3. all consumers read the new contract;
4. the old writer becomes read-only;
5. the old representation is retired.

At no point should two stores both accept authoritative writes for the same field family.

### Layer 4 — Checks

Layer 4 is newly generated validation state, not another fact store:

```text
checks:
  identity
  barcode
  nutrition_table
  ingredients
  image
  source_traceability
  category_assignment
  calculation
  publishability
```

Each check has:

```text
status: pass|warn|fail|unknown|not_applicable
reason_codes[]
evidence_refs[]
checked_at
checker_version
blocking_scope: none|internal_generation|future_consumer_publish
```

Checks consume Layers 1–3 and never mutate them. The internal dossier should be generated even with failures; otherwise the products most in need of inspection disappear.

`publishability` in the MVP is **diagnostic shadow state only**. It cannot change current publication. Future scanner publication must use a separately versioned policy and the two-gate sign-off.

## 3. Barcode-state design

The five required states attach to the identity resolution for a stable `product_id`:

- `verified`: one syntactically valid, check-digit-valid barcode is supported by sufficient direct evidence or an authorized manual decision.
- `found-but-conflicting`: multiple plausible valid observations exist and no accepted resolution is established.
- `malformed`: barcode-like text was captured but fails structural validation, including truncation or check-digit failure.
- `not-found`: a qualifying capture was inspected and no barcode was present.
- `pending-manual-review`: evidence exists that automated rules deliberately cannot adjudicate.

I would also keep the evidence-availability distinction outside this state: a product lacking a usable raw capture is not falsely classified as `not-found`. Its barcode state should be `pending-manual-review` only if queued for review; otherwise the evidence cell records `not_captured` and the barcode check is `unknown`. If the five-state requirement is exhaustive, `pending-manual-review` must cover this unresolved condition with a reason code such as `NO_REPLAYABLE_CAPTURE`.

The model stores all observed candidates, preserving leading zeroes as strings. Validation includes symbology/length rules and check digits where applicable. No numeric coercion is allowed anywhere.

Pipeline enforcement:

- Product joins and PD generation use `product_id`, never barcode.
- Scanner lookup indexes only accepted barcodes from `verified` records.
- All other barcode states produce no scanner alias.
- A malformed/conflicting/missing barcode lowers `barcode_confidence` and causes a barcode `warn`, `fail`, or `unknown`; it does not suppress the dossier, null unrelated fields, alter quality scores, or break BSIP processing.
- TASK-607 writes new observations and resolution decisions, not edits to product names or scores.
- The present truncation failure is retired by forbidding inferred completion, preserving the captured text, validating as a string, and routing malformed values to state rather than using them as identifiers.

## 4. Quality vs data-quality mechanism

This separation must be enforced by type and policy, not labels alone.

- `product_quality` and `data_quality` are sibling schema objects with distinct types.
- Product-quality calculators may consume observed facts and BSIP inputs, but cannot read data-quality fields.
- Data-quality calculators may inspect provenance, presence, conflicts, and validation results, but cannot alter product-quality outputs.
- No top-level `overall_score` field is permitted.
- The schema rejects formulas whose input domains cross the boundary.
- The internal API returns separate radar series with explicit axis domains:
  - quality radar: nutrition, ingredient simplicity, processing, additive burden, category performance;
  - evidence radar: evidence strength, completeness, identity confidence, barcode confidence, eventually image confidence.
- The UI may overlay selectable series only when their meanings and scales are explicit. It must not draw a single polygon that visually implies one composite quality measure.
- Evidence weakness is displayed alongside a score, never multiplied into it, used to cap it, or treated as a penalty.
- Unknown inputs remain unknown; completeness is descriptive and cannot trigger estimation or rescoring.

Add a regression test that fails if any product-quality output changes when only provenance/completeness/barcode state changes. Add the inverse test that evidence metrics can change without changing the published score snapshot.

## 5. MVP boundary

The thinnest honest first cut is a schema, generator, validator, corpus index, and utilitarian internal inspection surface—not the full envisioned experience.

### Include now

- One versioned PD revision per served product, keyed by stable `product_id`.
- Input hashes and exact references to manifest entries, captures, BSIP1 artifacts, BSIP2 traces, and served JSON.
- Layer 1 identity with verbatim names and the five-state barcode model.
- Layer 2 evidence cells for barcode, nutrition, ingredients, and the other identity fields already recoverable from direct captures.
- Layer 3 snapshot of existing published scores plus linked BSIP2 calculation inputs; distinct basic completeness and evidence metrics.
- Layer 4 checks for identity, barcode, nutrition, ingredients, source traceability, category assignment, calculation parity, and shadow publishability.
- A corpus-wide list/filter page and a plain per-product inspection page sufficient to find:
  - malformed/conflicting/missing barcodes;
  - absent captures;
  - trace-to-served mismatches;
  - missing evidence;
  - calculation mismatches.
- A machine-readable barcode lookup index containing verified aliases only.
- Replay determinism, schema validation, OFF-lineage rejection, and exact served-score parity gates.
- Explicit coverage reporting: every served product must produce either a valid dossier or a visible generation failure. Silent omission is forbidden.

This is zero-throwaway scanner foundation because the schema, verified alias index, provenance contract, and validation states are the same backend primitives a scanner will need.

### Defer explicitly

- Polished two-page visual design.
- Radar rendering and interactive layer controls; retain radar-ready structured dimensions.
- Consumer scanner UI and scanner-result copy.
- Any scanner publication decision or consumer-facing publishability policy.
- Image-confidence calculation until there is a defensible image evidence model.
- Automated cross-source conflict resolution beyond deterministic high-confidence rules.
- Broad manual-review workflow tooling; initially support an append-only decisions file/ledger and filtered queues.
- Historical trend visualization.
- Consolidating or deleting BSIP0/1/2 stage-local stores.
- New scoring dimensions or scoring philosophy.
- Rescraping solely to make the dossier appear complete.
- Bespoke shelf adapters.

Page 2’s information must exist in the data model from the start, but its polished interface can wait. A simple structured evidence/checks panel is enough for the MVP.

## 6. Sequencing against TASK-602 / parser fix / 601 / 563 / 607

### 1. Freeze invariants and the contract

Before pipeline work, define the PD schema, source-ownership matrix, allowed lineage vocabulary, barcode state transitions, and corpus invariants:

- one dossier outcome per served product;
- published score and comparison fields byte- or value-equivalent;
- no OFF lineage;
- no invented values;
- missing remains null;
- names remain verbatim;
- no product-quality/data-quality cross-dependencies.

Capture the current 710-product served set and hashes as the publication parity baseline.

### 2. Land and verify TASK-601 first

The capture manifest, canonical keys, supersession/dedup behavior, replay harness, committed baseline, and `--check` gate are prerequisites for trustworthy Layer 2 generation. The PD should consume TASK-601, never reproduce its capture reconciliation logic.

The PD schema/generator skeleton and served/trace adapters can be developed in parallel, but no dossier evidence should be declared canonical before manifest identities are stable.

### 3. Land the shared parser fix before accepting new parsed outputs

Fix and regression-test the `bsip0_nutrition.py` classify/first-value bug. Pin parser versions in evidence lineage.

Do not block a first projection of the current published state on rewriting history. Generate a pre-fix audit projection if useful, but mark affected parsed evidence with its actual parser version. Only the fixed parser may produce the new baseline used for forward migration.

### 4. Run TASK-602 through the fixed, replayable path

TASK-602 should produce new direct captures into TASK-601’s manifest and replay framework. It must not write hand-shaped PD records. The PD projection is regenerated from the new manifest revision.

Diffs must be classified:

- expected new or changed raw observations;
- parser-output changes;
- identity/barcode-state changes;
- forbidden published-score changes.

Tripwire-1 means the rescrape cannot automatically move currently published scores through the PD project. Changed evidence can be inspected without changing the served snapshot.

### 5. Build the MVP projection and parity gates

Join the stabilized manifest/captures, BSIP1 outputs, BSIP2 traces, and served JSON. Generate all dossiers and checks. Require:

- complete corpus accounting;
- deterministic replay;
- published-value parity;
- explicit unresolved lineage;
- zero forbidden sources;
- no silent fallbacks.

This step should expose, rather than conceal, the current 14/16 non-re-derivability issue.

### 6. Address TASK-563 as trace-recovery work, not PD customization

For the eight non-recoverable-trace shelves, repair the shared artifact production/replay path. Do not add per-shelf dossier loaders. Until repaired, the dossier records `source_traceability = fail/unknown` with named missing artifacts and continues to exist.

If uniform recovery cannot be achieved immediately, retain the served JSON as the publication snapshot and truthfully mark calculation lineage incomplete. That is preferable to fabricated traceability.

### 7. Run TASK-607 barcode backfill through the identity-resolution path

Once stable `product_id`, captures, and barcode validation rules exist, TASK-607 can add direct observations and resolution decisions. It must update barcode state and the verified lookup index without altering scores or unrelated identity fields.

Prioritize the 146 malformed/truncated records and products with scanner-relevant uncertainty, but run one uniform mechanism across all products. Backfill completion is not required to ship the internal inspection MVP; the MVP is the tool that makes the backfill governable.

### 8. Only then consider write-side consolidation

After at least one full successful replay and a stable operating period, evaluate migrating stage outputs behind the PD contract. Proceed one field family at a time with dual-read comparison, never dual-authoritative writes. Consumer scanner work begins only after verified-barcode coverage, lookup behavior, and two-gate review are adequate.

## 7. Top 3 risks + kill-criteria

### Risk 1: The projection becomes a second, drifting copy

Materializing resolved fields could create another store whose values diverge from captures, traces, or served JSON.

**Controls:** immutable revisions, input hashes, exact source paths, deterministic generation, no free-form dossier edits, and regeneration-only updates.

**Kill-criterion:** If a dossier field cannot be reproduced from its declared artifact plus versioned rule, or operators begin editing generated dossier JSON directly, stop treating the materialized PD as canonical. Reduce it to an on-demand view until lineage and the decision ledger are fixed.

### Risk 2: “Confidence” quietly changes product quality or publication

Barcode/evidence weakness could become a penalty, cap, fallback trigger, or blended radar score, violating both tripwire-1 and the missing-data rule.

**Controls:** separate schema namespaces and calculator dependency graphs; no composite score; regression tests proving quality invariance under data-quality-only changes.

**Kill-criterion:** Any corpus diff shows a published/product-quality value changed solely because capture availability, barcode state, confidence, or completeness changed. Halt rollout and split the calculation paths before proceeding.

### Risk 3: The unified projection hides unresolved upstream non-replayability

A visually complete PD could falsely imply that served pages are re-derivable when traces are missing or inconsistent.

**Controls:** calculation and traceability checks distinguish `pass`, `fail`, and `unknown`; served JSON remains explicitly labeled as the publication snapshot; every derived value names its actual trace or admits that none exists.

**Kill-criterion:** If the generator must reverse-engineer calculation inputs from served outputs, use shelf-specific recovery logic, or fabricate provenance to achieve full coverage, reject the projection as dishonest. Ship incomplete dossiers with explicit failures and repair TASK-563/upstream replayability first.

The architecture is wrong only if the existing artifacts cannot supply stable product identity or deterministic lineage even after TASK-601 and trace repair. Short of that, a canonical, immutable projection is the lowest-risk route to the owner’s unified spine: one contract now, progressive ownership migration later, and no period in which PD construction can silently change what Bari publishes.
tokens used
9,582
