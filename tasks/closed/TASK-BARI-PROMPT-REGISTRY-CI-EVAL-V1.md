---
status: CLOSED
priority: high
owner: dev-agent
created: 2026-06-10
updated: 2026-06-10
closed: 2026-06-10
category: tooling
roadmap_impact: true
tags: [prompts, llm, ci, evals, regression, governance, reliability]
supersedes: []
superseded_by: []
deliverable_2_status: ACCEPTED
close_reason: >
  All 7 DoD items verified against artifacts and met. Delivered: prompt_registry_v1.yaml
  (30 surfaces + 5 excluded), prompt_eval_dataset_v1.yaml (50 examples), authored_vs_
  deterministic_copy_audit_v1.md (corrected v1.1), prompt_registry_versioning_protocol_v1.md
  (D4), and the evals/ harness (7 governance gates: copy golden-diff, schema validation,
  pairwise review ledger + unsafe-wording, CLS-06 false-close, LLM import tripwire, +
  existing router & scoring regression) — run_d3_ci.py ALL GREEN. Four fail thresholds
  enforced. No production prompt/copy/scoring/data changed. Owner accepted D4+D3b
  (go-ahead 2026-06-10). OPEN follow-ups (out of this task's scope, recommend a new task):
  (1) reword yogurt insightLines to remove the literal "NOVA 3/4" leak (tracked
  acknowledged_exception CMP-06:NOVA); (2) pure-function extraction to wire the 2 deferred
  golden_diff items (EXP-06 snacks limitingFactors, cereals multiretailer rowVerdict);
  (3) confirm GitHub Actions runs green on first PR.
---

## D2 corrections applied — 2026-06-10 (content-agent + qa-agent)

All 5 blocking edits from the QA review (below) are done. Re-submitted for
orchestrator acceptance; DoD item 6 stays unchecked; no v2 task opened; D3 not
implemented.

1. **Per-category provenance audit redone with file evidence** (no inference) —
   [`authored_vs_deterministic_copy_audit_v1.md`](../01_framework/operations/authored_vs_deterministic_copy_audit_v1.md)
   v1.1 now carries a per-category table with builder file + producing
   assignment/fn + classification + evidence line for all 12 categories.
2. **Headline corrected (retraction recorded):** *most* shipped insightLines are
   **authored / carried-verbatim**; deterministic builder scope is **narrow** —
   only salty_snacks + snacks (shared `build_insight_line`) and butter compute
   insightLine; snacks `limitingFactors` is computed; a separate multiretailer path
   computes rowVerdict for new-retailer products only.
3. **Routing corrected** in [`prompt_eval_dataset_v1.yaml`](../01_framework/operations/prompt_eval_dataset_v1.yaml)
   (validated). Examples changed (11): CMP-02 hummus, CMP-03 cheese, CMP-04 cereals,
   CMP-05 bread, CMP-06 yogurts, CMP-07 juices, CMP-08 hard_cheeses, CMP-09 maadanim,
   CMP-12 granola, CMP-17 cereals-rowVerdict → **golden_diff→pairwise_judge**;
   EXP-05 hummus arrays → **golden_diff→pairwise_judge**; EXP-07 bread arrays,
   EXP-08 yogurt arrays → **golden_diff→manual_review** (unverified provenance).
   Kept as golden_diff (verified computed): CMP-01, CMP-10, CMP-11, EXP-06 + CLS-01..06.
4. **cheese / hard_cheeses / maadanim individually verified** (all carried-verbatim
   or content-draft authored → pairwise). **hummus EXP-01/05 re-checked vs v5
   provenance** (carried-verbatim via build_glassbox_w4; v4 flagged STALE → pairwise).
5. **Completeness reframed:** dataset_meta.status = "v1 SEED — count-complete (50/50),
   field-complete (12/12), high-risk coverage PARTIAL (8/17)."

**Corrected method_distribution:** pairwise_judge 33 · golden_diff 10 ·
schema_validation 4 · manual_review 3 (verified against the YAML).

**rowVerdict finding:** splits *by producing run, not category* — cereals_008 =
authored (pairwise); multiretailer = computed (golden_diff). CMP-17 noted accordingly.

**Self-assessed recommendation: PASS WITH FIXES** — corrections complete and
file-evidenced; two surfaces (bread/yogurt expansion arrays) remain `manual_review`
until a builder is proven, and CLS-06 fixture + golden_diff snapshot capture are
hard D3 items. Awaiting orchestrator acceptance of D2.

# TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1: Prompt Versioning + CI Regression Evals for Production LLM Calls

## QA review — Deliverable 2 (2026-06-10, QA & Audit Lead) — CHANGES_REQUESTED

**Verdict: PASS WITH FIXES — DO NOT CLOSE. One CRITICAL correction is blocking.**

D2's structure is sound (50 examples, all 12 fields, correct bucket counts,
solid evidence/closure buckets) but its **central Step-0 classification is
inverted and not supported by per-category file evidence.**

- **CRITICAL — classification inverted.** The audit claims "most insightLine /
  explanation arrays are deterministic builder output." File evidence shows the
  opposite: only **salty_snacks** and **butter** compute insightLine
  deterministically (real `build_insight_line()` functions). **hummus, cereals,
  bread, yogurts, juices, granola** carry **content-agent-authored** copy
  verbatim (e.g. juices `content_draft_v1.md`; yogurts "Content-authored
  insightLine … verbatim"; bread `INSIGHT_LINES` dict; cereals/granola "Content
  Agent authors"; hummus `carried_verbatim` + flagged "STALE — Content Agent must
  rewrite"). The audit generalized from ONE builder ("by strong inference").
- **GOVERNANCE VIOLATION (routing).** ≥5 examples route **authored** copy to
  `golden_diff` (CMP-02 hummus, CMP-04 cereals, CMP-05 bread, CMP-06 yogurts,
  CMP-07 juices) and CMP-17 routes the authored cereals `rowVerdict` to
  `golden_diff`. Authored copy must be `pairwise_judge` (+ manual). EXP-01/05
  (hummus arrays) must be re-verified — the v5 builder lineage carries authored,
  possibly-stale arrays, not the deterministic `build_hummus_explanation_v1.py`.
- **MINOR — overstated completeness.** "50-example set is complete" must be
  reframed as **"v1 seed; count-complete; coverage partial (8/17 high-risk)."**
- **ACCEPTABLE.** CLS-06 negative-control deferred to D3 — must be a HARD D3
  requirement. DoD item 6 correctly remains unchecked; the task is NOT closing.

**Blocking required edits (content-agent + qa-agent) before D2 acceptance:**
1. Redo Step-0 per-category with file evidence: identify the builder that produced
   each shipped `*_frontend_vN.json` and whether `insightLine`/arrays are computed
   vs carried-verbatim. Record evidence per category (no inference).
2. Re-route: hummus, cereals(008), bread, yogurts, juices insightLines →
   `pairwise_judge`. Keep salty_snacks, **snacks** (same builder), butter as
   `golden_diff` (verified deterministic). `rowVerdict` has a per-product
   built-vs-authored split (cereals-multiretailer COMPUTES it; cereals_008 +
   granola are AUTHORED) — split CMP-17/CMP-18 by provenance, do not route by
   category. Individually verify cheese, hard_cheeses, maadanim (still unverified).
3. Re-verify hummus explanation arrays (EXP-01/05): confirm v5 provenance; route
   authored/stale arrays to pairwise, deterministic ones to golden_diff.
4. Correct the audit headline + `method_distribution` to match reality.
5. Make CLS-06 fixture + builder golden_diff snapshot capture explicit hard D3 items.

**Follow-up task (separate from the D2 corrections):** open a task for v2 eval
coverage expansion — the 9 uncovered high-risk surfaces + Tier-2 instruction
prompts. The corrections above stay inside D2.



## Objective

Add prompt versioning and CI regression evaluation for **all Bari production LLM
calls**, so that any change to a production prompt is versioned, reviewed, and
gated by an automated eval before it can affect product or data quality.

**Hard constraint:** Do **not** change any production prompt in this task. This
task builds the registry, eval harness, CI gate, and rollback protocol — it does
not modify prompt behavior.

## Scope

Cover every prompt used for:

1. Ingredient parsing
2. Product categorization
3. Evidence extraction
4. Score explanation generation
5. Hebrew consumer-facing text
6. Comparison page generation
7. Agent routing or task closure **where LLM output affects product/data quality**

Out of scope: developer-only / non-product LLM usage that cannot reach product
or data quality (these may be cataloged but are not gated).

## Required prompt registry fields

Each registered prompt must carry:

- `prompt_id`
- `version`
- `status` — one of: `draft` / `candidate` / `production` / `rollback`
- `model`
- `temperature`
- `max_tokens`
- `retrieval_rules`
- `input_schema`
- `output_schema`
- `change_reason`
- `expected_effect`
- `risk_level`
- `owner`
- `reviewer`
- `linked_eval_set`
- `rollback_version`

## CI eval requirements

- Start with **50 golden examples**.
- Compare **candidate** prompt outputs against the **current production baseline**.
- Use **schema validation** wherever the output is structured.
- Use a **pairwise LLM judge only for semantic outputs** (e.g. Hebrew consumer
  text, explanations, comparison copy) — not for outputs that can be checked by schema.
- **Fail CI only when a regression crosses a defined threshold** (no flapping on
  noise).

### Required initial fail thresholds

| Check | Fail condition |
|-------|----------------|
| Schema validity | `< 98%` valid → fail |
| Score-affecting classification delta | `> 5%` of examples flip → fail |
| Unsafe / unapproved consumer wording | `> 0` occurrences → fail |
| Unexplained score delta | `>` approved tolerance → fail |

## Deliverables

1. **`prompt_registry_v1.yaml`** (or equivalent Git-tracked registry) holding all
   required fields per prompt.
   **→ DELIVERED 2026-06-10:**
   [`01_framework/operations/prompt_registry_v1.yaml`](../01_framework/operations/prompt_registry_v1.yaml)
   — 30 LLM surfaces registered (7 consumer / 10 copy-instruction / 13 operational),
   5 deterministic surface-classes registered as excluded, 17 high-risk. Adds an
   `llm-import-tripwire` CI rule (fail on any unregistered anthropic/openai/litellm
   import outside `.venv/`) and a deterministic-regression passthrough rule. Status
   = PASS WITH FIXES (4 open gaps logged in the registry `reconciliation` block).
2. **Eval dataset structure** with 50 initial golden examples, organized per
   prompt / eval set and linked from the registry via `linked_eval_set`.
   **→ DELIVERED 2026-06-10 (content-agent + qa-agent):**
   - Step 0 audit: [`01_framework/operations/authored_vs_deterministic_copy_audit_v1.md`](../01_framework/operations/authored_vs_deterministic_copy_audit_v1.md)
     — resolves gap #1. Key result: most `insightLine` + explanation arrays are
     **deterministic builder output** (→ golden_diff), not free-authored; the truly
     authored, pairwise-worthy copy is caveats, milk insights, homepage/methodology,
     glass-box, and patched verdicts.
   - Dataset: [`01_framework/operations/prompt_eval_dataset_v1.yaml`](../01_framework/operations/prompt_eval_dataset_v1.yaml)
     — exactly 50 examples (18/6/10/4/6/6), all 12 required fields present (validated).
     Methods: golden_diff 23 · pairwise_judge 22 · schema_validation 4 · manual_review 1.
   - New finding: deterministic **copy builders** are not covered by the existing
     router/score regression suites — golden_diff on builder copy is a new layer for
     Deliverable 3 (not a duplicate of excluded surfaces).
3. **CI check design** — how the gate runs (trigger, candidate vs. baseline diff,
   schema validators, pairwise judge invocation, threshold evaluation, pass/fail
   reporting).
   **→ DELIVERED 2026-06-10 (frontend-agent + qa-agent):** implemented under
   [`01_framework/operations/evals/`](../01_framework/operations/evals/):
   `run_copy_golden_diff.py` (golden_diff for VERIFIED-deterministic copy only:
   CMP-01 salty_snacks, CMP-10 snacks, CMP-11 butter — 3/3 pass),
   `run_cls06_check.py` + `fixtures/cls06_returned_fixture.md` (false-close negative
   control → RETURNED), `check_llm_import_tripwire.py` (0 unregistered LLM imports
   outside `.venv/`), consolidated `run_d3_ci.py`, and CI workflow
   `.github/workflows/prompt_governance_ci.yml`. **`run_d3_ci.py`: ALL GREEN** (5/5
   gates incl. existing router + scoring regression). snapshot_path wired in the
   dataset for the 3 verified examples; EXP-06 (snacks limitingFactors) DEFERRED —
   inline in main(), can't wire without a production change.
4. **Rollback protocol** — how a `production` prompt reverts to `rollback_version`
   when a regression ships or is detected post-merge.
   **→ DELIVERED 2026-06-10 (product-agent + qa-agent):**
   [`01_framework/operations/prompt_registry_versioning_protocol_v1.md`](../01_framework/operations/prompt_registry_versioning_protocol_v1.md)
   — version-bump triggers (7), lifecycle states (adds `deprecated` → 5 states),
   approvals by surface type (5 sign-off sets), rollback triggers (6) + process
   (revert to `rollback_version`, restore eval baseline, document, owner+reviewer
   sign-off), DoD-6 closure conditions, and the 2 deferred golden_diff items as
   governance notes. Registry YAML updated with `versioning_protocol`,
   `lifecycle_states`, `rollback_rule`, `deferred_golden_diff`.
5. **List of all existing Bari prompts that must be registered** — a discovery
   inventory across the 7 scope areas, mapping each prompt to file location, the
   model/params it currently uses, and its risk level.
   **→ DELIVERED 2026-06-10:**
   [`01_framework/operations/prompt_surface_inventory_v1.md`](../01_framework/operations/prompt_surface_inventory_v1.md)
   — 30 LLM surfaces (7 consumer-facing / 10 copy-instruction / 13 operational),
   17 high-risk, 5 deterministic surface-classes excluded. Key finding: Bari makes
   **no programmatic LLM calls** — LLM enters via Agent OS instructions (Channel A)
   and authored copy artifacts (Channel B); eval must run at artifact-generation
   level, not an API boundary. 4 gaps logged for the registry-build phase.

## Reconciliation decision note — Deliverable 1 (2026-06-10, product-agent)

In-lane governance call (no decision-authority tripwire fired). Recommendation:
**PASS WITH FIXES.** Registry is complete (30/30 surfaces + 5/5 excluded);
ownership and gaps #1/#2 now have decided resolution paths. DoD item 6 stays
**unchecked** because reconciliation sign-off requires the gap-#1 audit *output*,
which is produced inside Deliverable 2 (below).

**1. Ownership model for remaining deliverables — CONFIRMED as proposed:**

| Area | Owner(s) | Reviewer |
|------|----------|----------|
| Registry governance, version-bump protocol, reconciliation (D4) | product-agent | qa-agent |
| CI import tripwire + registry validation wiring (D3) | frontend-agent | qa-agent |
| Eval thresholds + CI pass/fail validation (D3) | qa-agent | product-agent |
| Evidence-extraction eval framing | research-agent + nutrition-agent | product-agent |
| Hebrew content eval scope/rubric (D2) | content-agent + qa-agent | nutrition-agent |

product-agent retains decision quality / scope-rationalization across all five.

**2. Gap #1 — per-category authored-vs-deterministic copy audit:**
- **Method (decided):** for each comparison category, classify every
  `insightLine` / `rowVerdict` / explanation-array string as **deterministic**
  (emitted by a `build_*_frontend*.py` / `build_*_explanation*.py` phrase-table —
  confirm by locating the builder and the field it writes) or **authored**
  (no builder writes it; originates from content-agent). Output = a per-category
  table: `category → field → {deterministic | authored} → eval_method`.
  Deterministic fields route to `golden_diff`/`schema_validation`; authored
  fields route to `pairwise_judge`.
- **Sequencing (decided):** **NOT a blocker before Deliverable 2.** The audit runs
  as **step 0 of Deliverable 2** (it sizes the pairwise vs. golden buckets within
  the 50). Owners: content-agent + qa-agent.

**3. Gap #2 — evidence-extraction modeling:**
- **CONFIRMED:** evidence extraction has **no code surface**; it is correctly
  modeled as `research-agent` **agent_generated_artifact**. Eval compares
  extracted claims to their cited sources (claim fidelity), not a code output.
- **Sign-off (decided):** **research-agent owns; nutrition-agent co-signs**
  (nutrition validates that extracted evidence is used correctly where it touches
  scoring philosophy). Matches the registry's existing owner/reviewer on
  `bari-agent-research`.

**4. Remaining gaps (deferred by design, not blockers):**
- Gap #3 (enforce `llm-import-tripwire`) → Deliverable 3, owner frontend-agent.
- Gap #4 (version-bump protocol for `.md` instruction files) → Deliverable 4,
  owner product-agent.
- v2 cleanup: split `bari-skills-bundle` (4) and `bari-agent-design-frontend` (2)
  into per-file entries — non-blocking.

**DoD item 6:** remains **unchecked** until the gap-#1 audit table exists (D2) and
inventory↔registry is signed off by product-agent. No eval examples built, no CI
enforced, no production prompts/scoring/copy changed by this note.

## D3b — threshold enforcement (2026-06-10, qa-agent + content-agent + frontend-agent)

Implements the two thresholds D3 left unenforced. **All 7 governance gates green**
via `run_d3_ci.py`.

- **schema_validation** — `evals/run_schema_validation_gate.py` (EXP-01..04;
  threshold ≥ 98%) → **100% on all 4** explanation-array surfaces.
- **pairwise_judge + unsafe wording** — `evals/run_pairwise_review_gate.py` (33
  examples): structured review packets (`evals/reviews/packets/`), verdict ledger
  (`evals/reviews/pairwise_verdicts_v1.yaml`, hash/TTL freshness → stale forces
  re-review), and a precise no-LLM lexical scan (`evals/wording_check.py` +
  `config/unsafe_wording_lexicon_v1.yaml`) → **ALL PASS**.
- Gates wired into `run_d3_ci.py` (now 7) + `.github/workflows/prompt_governance_ci.yml`.

**REAL FINDING surfaced (tracked, NOT fixed — this task must not change consumer
copy):** yogurt insightLines leak literal `NOVA 3` / `NOVA 4` into consumer copy
(framework-invisibility violation), 3 products. Recorded as an OPEN
`acknowledged_exception` (`CMP-06:NOVA`) with content-agent remediation under the D4
versioning protocol. **Recommend a follow-up task to reword the yogurt copy.**

Precision note: the 9 banned phrases were split into **absolute** (always fail) vs
**needs-reference** (fail only without a number) — shipped hummus/maadanim/granola
copy uses the compliant "low protein **(5.7 גרם)**" form, so a naive matcher
false-positived; the split removed those false positives while keeping the real
NOVA leak.

**DoD item 4 is now MET** — all four thresholds implemented and enforced:
schema validity (D3b), classification delta (existing regression), unsafe wording
(D3b), score delta (existing regression).

## Final assessment after D4 (2026-06-10, product-agent + qa-agent)

**Can DoD item 6 be checked? Not yet — one dependency outstanding.** Reconciliation
itself is complete (30/30 surfaces + 5/5 excluded registered; D2 audit accepted; D3
gates present & green), but DoD 6's closure condition (d) = "D4 protocol accepted",
and D4 is produced-but-not-yet-accepted. **DoD 6 becomes checkable the instant the
orchestrator accepts the D4 protocol.** Exact wording to use then:
`6. [x] … reconciled — 30/30 + 5/5; D2 audit + D3 gates + D4 protocol accepted.`

**[SUPERSEDED by D3b]** DoD item 4 is **now met** — see the D3b block above; all four
thresholds are implemented and enforced (7/7 gates green via `run_d3_ci.py`).

**Post-D3b closure status:** all DoD build-work is complete (1 registry · 2 dataset ·
3 CI design+runnable · 4 thresholds enforced · 5 rollback protocol · 7 no production
behavior changed). The task is **closable pending three non-build gates:**

1. **Orchestrator acceptance** of D4 (protocol) and D3b (enforcement) — staged
   pending, not self-accepted. On D4 acceptance, **DoD item 6 becomes checkable**.
2. **First-PR GitHub Actions** green confirmation (local 7-gate runner is green;
   runner unproven until a PR triggers it).
3. **Out-of-scope follow-ups (do NOT block this task):** (a) reword yogurt copy to
   remove the `NOVA 3/4` leak — CMP-06, tracked OPEN; (b) pure-function extraction to
   wire the 2 deferred golden_diff items (EXP-06, multiretailer rowVerdict). Both are
   explicitly excluded here (no consumer-copy change; no builder refactor).

**Recommendation: PASS.** No remaining in-scope build work. Recommend the orchestrator
accept D4+D3b, check DoD 6, run the first PR, and open one follow-up task for the
yogurt NOVA-leak reword + the deferred golden_diff extraction.

## Definition of Done

1. [x] Git-tracked prompt registry exists with all required fields, populated for
       every in-scope prompt — `prompt_registry_v1.yaml` (30 surfaces + 5 excluded).
2. [x] Eval dataset structure exists with 50 golden examples wired to their prompts —
       `prompt_eval_dataset_v1.yaml` (validated 50/50, 12/12 fields).
3. [x] CI check design documented and runnable — `evals/` + `run_d3_ci.py` (7 gates) +
       `.github/workflows/prompt_governance_ci.yml`; schema + pairwise-for-semantic-only.
4. [x] All four initial thresholds implemented and enforced as the fail gate —
       schema (D3b), classification delta + score delta (existing regression), unsafe
       wording (D3b). 7/7 gates green.
5. [x] Rollback protocol documented and references `rollback_version` / `status` —
       `prompt_registry_versioning_protocol_v1.md` (5 states incl. deprecated).
6. [x] Complete inventory produced and reconciled against the registry — 30/30 + 5/5;
       D2 audit + D3 gates + D4 protocol accepted (owner go-ahead 2026-06-10).
7. [x] **No production prompt behavior changed** — only eval/governance infra added;
       the one real finding (CMP-06 NOVA leak) was tracked, NOT edited.

## Notes / constraints

- Frozen invariants are not touched: this task adds governance tooling around
  prompts, it does not rescore anything or alter scoring philosophy.
- Discovery (deliverable 5) likely spans `03_operations/bsip2/`, the explanation
  engine, Hebrew copy generation, comparison page generation, and any agent
  router / task-closure LLM steps. Inventory before populating the registry.
- The four thresholds are **initial** values — tune after the first production
  baseline run, but changing a threshold is itself a registry/governance change.

## Ancestry

Created on owner request (2026-06-10) to add reliability/regression governance
over production LLM calls. Related governance: registry protocol v1, BSIP2
scoring governance, explanation engine v2.
