# STF VERDICT MEMO — Product Dossier ("PD") architecture

- **Date:** 2026-07-11
- **Task:** TASK-608 (owner-started major program)
- **Convened by:** owner ("Please review this, send to STF for review and debate, and come back with your resolution")
- **Seats:** Claude/Fable 5 (blind position + 2 rounds) · GPT-5.6 Sol (blind position + 2 rounds, read-only). Chair: Opus 4.8 (adjudicated; did not debate).
- **Disposition:** CONVERGED. Zero surviving cruxes. Debate produced net-new architecture beyond either blind position.
- **Appendix (provenance):** blind positions + rebuttals in `2026-07-11_product-dossier_appendix_{fable_r1,sol_r1,sol_r2}.md` (Fable R2 embedded §5 below).

---

## 1. Frame (as debated)

The owner has DECIDED to build a canonical **Product Dossier** — one per product (~710 served,
20 shelves) — with a 4-layer structure (Identity / Raw-evidence+provenance / Derived-analysis /
Checks), explicit barcode STATES (barcode not mandatory; broken = lower confidence, not a broken
pipeline), a 2D radar (not 3D) with user-selectable layers, and a two-page internal inspection
interface — **the foundation for Bari's future barcode scanner.** Trigger: 146/710 (21%) served
products carry a malformed/truncated barcode; 398/757 have no stored raw-capture; published pages
are not re-derivable from their named traces on 14/16 shelves.

**Owner amendment (the decisive reframe):** *"Essentially this encapsulates also BSIP1 and BSIP2
and BSIP0. All in one go. This is a huge structural shift."* The PD is the canonical product spine
unifying all three BSIP stages, not a UI feature. The debate's central crux therefore:
**build a new canonical store BSIP0/1/2 read-from and write-to (data-model re-architecture) vs a
unifying deterministic projection assembled over the existing stores (manifest + captures + traces
+ served JSON).**

Bounding constraints (non-negotiable): OFF-ban absolute; missing = NULL not invented (confidence
never a backdoor to synthesize data); product names verbatim; **tripwire-1** (PD never mutates a
published score); systematic-not-artisanal (one schema, one generation path); two-gate on anything
consumer-facing; reconcile-not-duplicate the TASK-601 manifest + replay + BSIP2 traces; owner-
explicit **do NOT combine product quality and data quality into one score.**

---

## 2. Converged recommendation (chair adopts)

**Build the PD as a deterministic compiled PROJECTION over the existing stores — NOT a new writable
store that BSIP0/1/2 read-from and write-to.** One shelf-agnostic compiler regenerates a per-product
dossier wholesale from named inputs; the dossier is hand-edited by no one; a committed baseline +
`--check` CI gate makes silent divergence a build break (the repo's existing Shadow1 / replay /
conformance pattern). Write-ownership of stage stores migrates INTO the PD contract later, **one
field-family at a time, behind parity gates — never a big-bang that creates two authorities during
migration** (the precise disease TASK-563 diagnosed).

**The owner's amendment is honored structurally, not dodged:** the PD *schema* unifies BSIP0/1/2
(Layer 2 = BSIP0 output; Layer 3 = BSIP1+BSIP2 output; Layer 4 = cross-stage reconciliation gate);
*storage* stays stage-local until migration is *earned*. The schema is the structural shift; the
storage consolidation is a later, evidence-gated decision that this architecture keeps open at zero
extra cost.

**Why derive, not build (both seats, independently):** a big-bang unified writable record would (a)
migrate three heterogeneous stores mid-flight of TASK-602; (b) launch with holes on the 8
non-recoverable-trace shelves it must either fake (banned) or admit (at which point it *is* a
projection); (c) reproduce the exact TASK-563 pathology — a second writable copy of every field
with bespoke write paths, claiming to be canonical. Derive-first satisfies every stated win
criterion: single source of truth per field, reduces the drift surface instead of adding one,
reuses the 601 manifest as the spine, is zero-throwaway (the schema + identity registry + verified-
alias index are the first modules of the eventual store *and* everything a scanner needs).

**The PD's single job:** *for every product, one deterministic, re-derivable record of everything
Bari knows about it and exactly how it knows it — written by one compiler, hand-edited by no one.*

---

## 3. The three refinements the debate produced (net-new, beyond both blind positions)

### R-A — Identity key: mint an opaque immutable `bari_pid`; the registry is scope-disciplined.
Converged (Sol conceded, Fable defended, merged). Today's product ids are largely **barcode-derived**
(`bsip1_cereal_72968`) and 146/710 of those barcodes are truncated — so "the stable internal
product_id" inherits the very defect TASK-607 exposed. Reuse fails both ways: truncated barcodes that
collide → silent merge (captures cross-contaminate — the worst outcome); one product captured under
two truncations → split, orphaned evidence. **Decision: mint `bari_pid` (opaque, immutable, NEVER
barcode-derived) as the universal join key; barcode is an attribute/alias, never a key.** The one new
authoritative store = an **identity registry** holding ONLY what nothing else owns: the minted
`bari_pid`, the **alias table** (legacy bsip1 ids / served-JSON ids / (retailer,gtin) manifest keys →
pid), and the **barcode-state adjudication** (5 states + `recovered_gtin` candidates). Sol's "narrow
ledger" and Fable's "registry" are the SAME store — Fable's minted key at the center, Sol's
decisions-not-duplication discipline for its contents.

### R-B — Registry scope: identity-adjacent FACTS are projections, not registry copies. *(Sol's CRUX C — adopted.)*
name, brand, package size, manufacturer, source URLs, last-scrape timestamp are **provenance-pointed
projections** from the capture/served source they came from — exactly like nutrition — NOT stored
authoritatively in the registry. Otherwise "the one new identity store quietly becomes a second
product store" (drift surface added, not reduced — and it would trip Fable's own R1 kill-criterion).
The registry owns decisions and identifiers; it owns no product facts that a capture already sources.

### R-C — Publication is its own axis: THREE derived namespaces, not two. *(Fable's CRUX C — adopted.)*
Layer 3 splits into three disjoint namespaces, never blended, no cross-namespace composite number:
- **`assessment`** — what the *product* is: score, grade, nutrition/ingredient/processing/additive
  dims, category performance. Source: BSIP2 traces ONLY.
- **`data_quality`** (record_health) — how good the *record* is: completeness, evidence/identity/
  barcode confidence, image confidence. Source: PD compiler over Layers 1–2. Data-quality, not
  product-quality — so computing it creates zero scoring exposure.
- **`publication_record`** — what Bari *currently publishes, verbatim*: the served score/grade/copy,
  stamped with its `run_id` + trace hash, **pending a Layer-4 calculation check that may say FAIL.**
  This is neither assessment nor data-quality; on 8 shelves it is a number with no re-derivable
  trace, on 14/16 it disagrees with the trace its config names. Filing it under `product_quality`
  (as Sol's blind §2 did, and Fable's branch model latently did) would frame a possibly-unverifiable
  value as an assessment fact. Splitting it out is what keeps **tripwire-1** (never mutate published)
  and **traceability-honesty** (never imply re-derivability) from colliding: the calc check compares
  `publication_record.score` vs trace, and a FAIL is visible **without** demoting a value we can't
  stand behind out of "product quality."

**Quality vs data-quality is enforced by TYPE, not convention:** every metric declares
`axis: assessment | data_quality | publication_record`; a metric reading inputs across namespaces
fails the build; no `overall_score` field is permitted; the radar renders one namespace per
user-selectable layer with distinct visual treatment (the owner's "selectable layers" requirement is
exactly the affordance that keeps them from ever being averaged). Regression tests: product-quality
must not change when only provenance/completeness/barcode-state changes, and evidence metrics must be
able to change without moving the published snapshot.

### R-D — Parser-fix sequencing (CRUX B, converged rule).
*Only the fixed parser may produce a COMMITTED baseline; any pre-fix projection is uncommitted,
stamped with its actual `parser_version`, and never a comparison base.* Pre-fix audit projections are
allowed (they show current state); they are throwaway. One adjudication, not two.

---

## 4. Data model (committed shape)

```
03_operations/product_dossier/
  registry/product_registry.json     # NEW authoritative store — pid + alias table + barcode-state
                                      #   adjudication + recovered_gtin ONLY. Written by registry_ops.py.
  dossiers/{bari_pid}.json            # DERIVED, regenerated wholesale by ONE compiler. Never hand-edited.
  build_dossiers.py                   # the single generation path, all shelves, no per-shelf loaders
  dossier_baseline.jsonl + --check    # committed baseline, CI-gated next to replay_baseline
  manual_decisions/{bari_pid}.json    # 2nd & last writable surface: reviewed adjudications, merged as
                                      #   manual_override w/ author+date (never inline in the dossier)
```

- **Layer 1 — Identity.** Truth = registry for {pid, aliases, barcode_status, recovered_gtin}; ALL
  other identity facts (name/brand/pkg/manufacturer/urls/last_scrape) = provenance-pointed projections
  (R-B). Tripwire-1 firewall: the registry never flows into published pages; served id/barcode stay
  untouched; any served-side backfill is a separate owner-gated write the registry merely informs.
- **Layer 2 — Raw evidence.** Truth = TASK-601 manifest + raw captures + replay baseline. No new store.
  Per-field cell `{value, raw_source_text, source, extraction(parser_version), captured_at,
  content_hash, flags}`, lifted from replay rows (already ~90% built; the PD pivots per-field-rows →
  per-product). OFF-never structurally: manifest membership admits only direct-scrape containers; a
  cell whose `source` is off-enum is a **build failure**. Missing = `{value:null, status:not_retrieved}`
  + Layer-4 fail; the compiler has NO imputation code path.
- **Layer 3 — Derived.** Three disjoint namespaces per R-C. PD never recomputes a score. The only
  PD-computed values are record-health metrics (data_quality axis).
- **Layer 4 — Checks.** Pure functions recomputed every compile; **imports** existing gate logic
  (run_gates G-checks, validate_comparison_page) — the per-product pivot of the gate suite, not a
  fork. calculation check = published (publication_record) vs trace (G5 per-product). `publishability`
  is diagnostic shadow state in the MVP — it CANNOT change current publication; the future scanner
  publish path uses a separately versioned policy + two-gate sign-off.

---

## 5. MVP boundary + sequencing (recommended build order)

**MVP (thinnest cut that unblocks the audit NOW and is zero-throwaway scanner foundation):**
1. **Identity registry + alias table + barcode-state backfill** — from served JSONs + 601 manifest +
   TASK-607 census. Turns "146 truncated / 398 uncaptured / 8 untraceable shelves" from task-file
   aggregates into per-product queryable state. Everything keys on `bari_pid`, so this is deliverable #1.
2. **Dossier compiler v1** — Layers 1+2 (provenance cells) + Layer 3 as read-only stamped copies with
   honest `derivation` labels (three namespaces) + Layer 4 with FOUR checks: barcode, source-
   traceability, calculation, publishability. That four-check set IS the requested internal audit.
3. **One internal Page-1 inspection view** — identity+status, check panel, evidence cells, score-as-
   copied; radar in simplest honest form (single 2D polygon, hard-toggled assessment/data_quality
   layers) or plain bars if the polygon costs >1 day. Internal-only route (no two-gate yet).
4. **CI:** `build_dossiers.py --check` vs committed baseline, next to the replay gate.

**Deferred (explicit):** Page 2 as designed UI (MVP shows raw evidence JSON inline); radar polish /
layer-blend UX; scanner UI + any consumer surface (two-gate applies then); image confidence;
cross-source conflict *resolution* UI (flag + route to pending_manual_review only); manual-override
forms (files, not forms); served-JSON barcode backfill (owner-gated, TASK-607); ANY BSIP0/1/2 store
migration (earned later per §7, not assumed now); new scoring dimensions/philosophy; rescraping solely
to make a dossier look complete.

**Sequencing (602 / parser-fix / 601 / 563 / 607 stream THROUGH the PD, they do not gate it):**
1. **Registry + alias backfill — start NOW.** Inputs all exist; blocks nothing; immediately gives the
   TASK-602 fan-out a dedup/targeting key better than barcodes.
2. **Parser fix lands before the committed Layer-2 baseline** (R-D). Build the compiler in parallel;
   freeze `dossier_baseline.jsonl` only after the parser fix + replay re-adjudication.
3. **TASK-602 — do NOT wait; the PD is the meter that measures it.** Missing capture = NULL cell +
   traceability FAIL = exactly the audit output wanted; each batch → manifest rebuild → recompile →
   coverage rises visibly per-product.
4. **TASK-607 — absorbed, not blocked-on.** Registry holds recovered_gtin + malformed state now; the
   served-side backfill stays a separate owner-gated write.
5. **TASK-563 — orthogonal.** The 8 shelves compile honestly labeled (`published_json_as_record`) with
   a failing calculation check; a future owner-ordered re-derive re-stamps with zero schema change.

Critical path: **registry → compiler skeleton → (parser fix + replay re-baseline) → Layer-2 commit →
checks + view → CI gate.**

---

## 6. Risks, reversibility, owner decision points

**Reversibility class:** HIGH. The PD is derived and additive — it writes only to new paths under
`03_operations/product_dossier/`, never to served JSON, scores, or stage stores. Deleting the whole
directory restores the prior state exactly. The one new authoritative store (registry) is backfilled
deterministically and re-buildable. Nothing here is consumer-facing (the internal inspection page is
internal; the scanner is deferred behind two-gate).

**Top risks (merged from both seats):**
- **R1 — View rot into store.** Kill-criterion: a second pipeline stage needs dossier-reads to
  function, OR >5% of fields carry `manual_override` as their effective value → that is the *evidence*
  the store-migration is earned; promote field-family by family (BSIP1's records first), schema
  already proven. The view is the schema rehearsal — no throwaway.
- **R2 — Baseline-drift noise makes `--check` ignorable.** Kill-criterion: `--check` failing >2
  consecutive orchestrator cycles from out-of-band stage writes → fix upstream write-path discipline
  (uniform-baseline doctrine); the per-product calc check names each violation — escalate, never
  weaken the gate.
- **R3 — Identity resolution harder than assumed.** Kill-criterion: >3% of the 710 can't map
  deterministically to a unique pid after name+barcode+shelf resolution, OR any pid claims captures
  from two real products → retain retailer-native product ids at scrape time (a TASK-602 scope
  amendment, decided before fan-out completes).

**When the architecture is WRONG (both seats agree):** only if the existing artifacts cannot supply
stable product identity or deterministic lineage even after TASK-601 + trace repair. Short of that, a
canonical immutable projection is the lowest-risk route to the owner's unified spine.

**OWNER DECISION POINTS:**
1. **Accept the architecture (derive-first projection + minted `bari_pid` + 3 namespaces) → authorize
   the MVP build?** This is the program go/no-go (tripwire 3: starts a major program — already
   owner-initiated; this confirms the shape). On accept, the chair registers the build tasks.
2. **One latent strategic question, tagged for you (not blocking the MVP):** *Do you intend the PD to
   eventually REPLACE the served comparison JSONs as the publication source (pages render FROM
   dossiers)?* If YES within ~a quarter, build-as-store wins sooner and migration starts with the
   registry as its first module. If NO / not-now, derive-first is correct and keeps that door open at
   zero cost. Nothing in the frame says yes; tripwire-1 + in-flight 602/607 say not-now. **Recommended:
   derive-first now, revisit migration when R1's kill-criterion or your publication-source intent
   fires.** No action needed unless you want to steer it.

**Recommended follow-up tasks (register ONLY on owner accept, per STF protocol):**
- PD-1: identity registry + alias table + barcode-state backfill (BUILD-HEAVY).
- PD-2: `build_dossiers.py` compiler v1 (Layers 1+2 + 3-namespace L3 + 4 checks) + committed baseline
  + `--check` CI gate (BUILD-HEAVY).
- PD-3: internal Page-1 inspection view (Frontend, internal route).
- Dependency notes: PD-2 committed baseline waits on the parser fix (other session); PD-1 starts now.

---

## 7. Provenance
Blind R1 positions: `…_appendix_fable_r1.md`, `…_appendix_sol_r1.md`. Sol R2:
`…_appendix_sol_r2.md`. Fable R2 (verbatim): CRUX A DEFEND→merge (mint pid; ledger+alias = one store,
minted key at center); CRUX B CONCEDE→reconcile (fixed-parser-only committed baseline, pre-fix audit
allowed uncommitted); CRUX C: Sol's `published_score_snapshot` nested under `product_quality`
re-introduces the trap Sol's own §4 forbids → publication is its own axis (`publication_record`),
calc-check FAIL visible without demoting it out of product-quality. First live use of the STF pattern
on a program-scale architecture decision; the debate produced net-new structure (R-B, R-C) neither
blind position held alone — the anti-anchoring design working as intended.
