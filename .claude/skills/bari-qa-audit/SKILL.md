---
name: bari-qa-audit
description: Guide Claude through Bari QA validation — run the deterministic gate instruments (run_gates.py G1–G8, validate_comparison_page.py terminal battery, validate_return.py C0), check traceability, identify hard fails and warnings, freeze baselines, and invalidate bad runs.
---

# Bari QA Audit Skill

**Owner:** Adversarial QA Agent (`.claude/agents/adversarial-qa-agent.md`) — this skill is the
**data-side (Track V — Verification) instrument set** of that agent. Track C (adversarial Challenge)
is judgment work and lives in the agent file, not here. The agent's combined D10 go-live gate
requires Track V fully green AND zero open CRITICAL Track C findings.

## Use this skill when…

- You are running QA validation on a category corpus, generated page JSON, or enrichment output
- You are reviewing QA results and determining pass/fail
- You are validating an agent return contract (C0 gate)
- You are freezing a QA baseline after a successful run
- You are investigating a failed QA run or invalidating a contaminated one
- A user says "run QA", "run the gates", "validate this page", "check QA results", "freeze baseline",
  "investigate QA failure", or "invalidate this run"

---

## Instrument Map

| Instrument | What it proves | Command | Exit semantics |
|---|---|---|---|
| **G1–G8 gate suite**<br>`03_operations/page_generator/gates/run_gates.py` | Page JSON is schema-valid, coverage-complete, scope-explained, OFF-free, grade-honest vs traces, copy-safe, parity-diffed, data-sane | `python 03_operations/page_generator/gates/run_gates.py <frontend_json> --corpus <bsip1_dir> --run <bsip2_products_dir> [--baseline <live_json>] [--schema <schema.json>] [--config <gate_config.json>]` | `0` = all gates PASS (WARNs allowed) · `1` = any FAIL. Writes `<name>_gates_report.md` next to the input JSON |
| **Terminal pre-ship battery**<br>`03_operations/spine/validate_comparison_page.py` | The 7 run_005-class ship blockers: score==trace, OFF ban, PENDING render, count consistency, ingredient sanity, false superlatives (via rank_check.py), image presence | `python 03_operations/spine/validate_comparison_page.py --json <frontend_json> --traces <run_dir/products> [more dirs…] [--http]` | `0` = all hard gates pass · `1` = ≥1 hard gate failed |
| **Return-contract C0 gate**<br>`03_operations/validators/validate_return.py` | An agent return contract is schema-complete, artifact-shas match disk, counts carry denominators+sources, set-claims carry distributions, commands truthful, citations not fabricated | `python 03_operations/validators/validate_return.py --md <return.md>` (or `--json <contract.json>`, or stdin) `[--root C:\Bari] [--run-commands] [--emit-json]` | `0` = all HARD checks PASS (WARN allowed) · `1` = ≥1 HARD FAIL · `2` = usage/load error (bad JSON, no contract found) |
| **Fixture library (mutation-testing)**<br>`03_operations/page_generator/fixtures/` | Known-bad inputs keep FAILING, golden inputs keep PASSING after any gate/generator change | — | **Status: MISSING** — this directory does not exist in the repo (verified 2026-07-04). See "Fixture discipline" below |

**Memory law (hard, non-negotiable):**
1. **Go-live requires BOTH** `validate_comparison_page.py` (all hard gates) **AND** `run_gates.py`
   (G1–G8) exiting 0. One green instrument is never sufficient.
2. **Gates green ≠ done.** Done = the page **rendered in a real DOM** and **red-teamed**
   (Adversarial QA Track C challenge report with 0 open CRITICAL). These instruments prove data
   integrity; they do not prove the page displays or that claims survive an adversary.

---

## QA Validation Protocol

### 1. Run the G1–G8 gate suite

```
python C:\Bari\03_operations\page_generator\gates\run_gates.py <frontend_json> ^
    --corpus <bsip1_output_dir> ^
    --run    <bsip2_run_products_dir> ^
    [--baseline <current_live_json>] [--schema <schema.json>] [--config <gate_config.json>]
```

- **Always pass `--corpus` and `--run`.** Without `--corpus`, the G2 image-regression check is
  skipped (WARN); without `--run`, G5 cannot verify scores against traces (per-product WARNs) and
  G3 cannot detect unexplained missing barcodes. A run without them is a weaker, non-terminal run.
- Pass `--baseline` when a live version exists — G7 PARITY emits the side-by-side diff table
  (product count, image coverage, avg copy chars, per-barcode grade changes). G7 is informational
  and never auto-fails.
- Default schema (when `--schema` omitted): `03_operations/page_generator/contract/page_output_schema_v1.json`.
  If the schema file is missing, G1 is SKIP — do not treat a SKIP as a PASS on a terminal run.
- **Gates and their hard-fail conditions** (from the script itself):
  - **G1 SCHEMA** — JSON Schema violation (type/required/enum/additionalProperties)
  - **G2 COVERAGE** — imageUrl missing in frontend while BSIP1 has one; name with no Hebrew
    characters; `PENDING_COPY` in a served field after the copy stage ran; a row with NEITHER
    insightLine NOR rowVerdict authored; v3 pages: any PENDING consumerTakeaway /
    consumerExplanation.whyRated / bariInterpretation / bestUseCases
  - **G3 SCOPE** — a scored barcode (trace dir exists) not displayed and not explained in `_meta`
    exclusions; ghost products (displayed, no trace) are WARN
  - **G4 OFF** — any OFF marker in the products array or in a displayed product's BSIP1 corpus
    record (TASK-238 hard rule; `_meta` exclusion documentation naming OFF is WARN-only)
  - **G5 GRADE-INTEGRITY** — JSON grade ≠ grade derived from score (floor policy: an engine E must
    never display as D); JSON score ≠ trace score beyond 0.05 tolerance; displayed grade better
    than trace-derived grade (grade inflation); standalone Hebrew grade letter in prose ≠ badge grade
  - **G6 COPY-SAFETY** — sodium causally framed (כי/בגלל/בשל…נתרן); prior-run references;
    framework leakage (NOVA/BSIP/cap=/proxy/dimension); the 9 banned Hebrew phrases
  - **G7 PARITY** — never fails; read the diff table and judge movement yourself
  - **G8 DATA-SANITY** — physically impossible per-100g nutrition (sodium_mg>5000,
    energy_kcal>900, any macro gram>100); nutrition-panel text scraped into the ingredients field
- **Exit code 0 = pass (WARNs allowed); 1 = any FAIL.** Cite the written report
  (`<name>_gates_report.md`, next to the input) plus the exit code in your return. Never eyeball
  what the gate suite can check.

### 2. Run the terminal pre-ship battery

```
python C:\Bari\03_operations\spine\validate_comparison_page.py --json <frontend_json> --traces <run_dir/products> [--http]
```

- `--traces` accepts **one or more** `run_dir/products` directories containing `*/bsip2_trace.json`;
  first match wins on barcode collision (multi-run pages).
- `--http` additionally HEAD-checks every imageUrl (slow). A dead URL is a **hard fail**
  (`image-http`). Remember: image HTTP 200 ≠ image displays — render-verify separately.
- **Hard-fail checks** (each exits 1): `score==trace` (score AND grade must match the trace after
  1-decimal rounding; a null score is only legal when the trace agrees the product is unscoreable),
  `OFF ban` (off_used must be 0), `PENDING render` (no `PENDING_COPY` in any rendered field, page_copy
  included), `count consist` (`_meta.product_count` / hero counts / filters "all" / "מתוך N המוצרים"
  strings all agree), `ingredient` (truncation, trailing comma, <40 chars, marketing/nutrition bleed),
  `superlative` (rank_check.py re-derives every superlative claim against the FULL corpus — a false
  one is a hard fail; subpool/uniqueness claims are WARN), `image present` (every product has imageUrl).
- If `03_operations/validators/rank_check.py` is unavailable or errors, the superlative check
  degrades to a WARN phrase-scan — treat that as an incomplete run and run rank_check standalone
  (`python 03_operations/validators/rank_check.py --json <frontend_json> --emit-json`).
- **Exit 0 = all hard gates pass; exit 1 = ≥1 failed.** WARNs print in the RESULT line — they must
  be eyeballed and dispositioned (step 5), never silently accepted.

### 3. Check traceability

Before evaluating results, verify traceability (steps 1–2 automate most of this — confirm the
automated checks actually ran, i.e. corpus/traces were loaded, before trusting them):

- Every product in the page/QA sample must be traceable to its source corpus entry
  (G3 SCOPE + the `no trace` arm of `score==trace` enforce this — but only when `--run`/`--traces`
  point at the correct run directory; confirm the loader lines "Corpus loaded: N" / trace counts)
- Every label must be traceable to its enrichment step
- Every score must be traceable to its scoring rule via the product's `bsip2_trace.json`
- If any product, label, or score is untraced: **hard fail** — never substitute a summary for
  the trace file

### 4. Identify hard fails

Hard fails block promotion. The taxonomy, mapped to the instrument that catches each:

| Hard fail | Caught by |
|---|---|
| Traceability gap (product/label/score untraced) | `score==trace` "no trace" · G3 · manual step 3 |
| Score/grade disagrees with trace; grade inflation | G5 · `score==trace` |
| OFF contamination anywhere in products or corpus records | G4 · `OFF ban` |
| Placeholder / unauthored copy in a served field | G2 · `PENDING render` |
| Label assigned to an out-of-scope product | G3 + manual scope review |
| Coverage below minimum threshold for a required label | G2 coverage lines + category config |
| Physically impossible nutrition; panel-as-ingredients | G8 · `ingredient` |
| False superlative claim vs full corpus | `superlative` (rank_check.py) |
| Duplicate product entries in the sample | G3 barcode sets + manual |
| Score produced by an unregistered/deprecated rule; runner/pipeline version mismatch | manual (no automated gate — check trace `engine_version` against the pipeline yourself) |

For each hard fail, record:
```json
{
  "fail_type": "<type>",
  "instrument": "<run_gates G# | validate_comparison_page <check> | manual>",
  "affected_product_ids": [],
  "affected_labels": [],
  "description": "<what went wrong — exact observed value, not a summary>",
  "resolution_required": "<what must be fixed before re-run>"
}
```

### 5. Identify warnings (acceptance discipline)

Warnings do not automatically block promotion but must be **explicitly accepted or resolved** —
a run with undispositioned WARNs is not a clean run:

- run_gates WARNs (e.g. corpus not provided, ghost products, OFF marker in `_meta`, no trace for
  a barcode) — a WARN caused by a missing input (`--corpus`/`--run` omitted) is resolved by
  re-running with the input, not by accepting it
- validate_comparison_page WARNs (`superlative-manual` review items, rank_check unavailable)
- Coverage between minimum and target threshold
- Label distribution significantly skewed vs baseline
- Enrichment confidence below target for a non-negligible portion of corpus
- New labels not present in the prior baseline (possible enrichment drift)

For each warning, record:
```json
{
  "warning_type": "<type>",
  "affected_scope": "<label, product set, or dimension>",
  "description": "<what was observed>",
  "owner_decision_required": "<accept | resolve>",
  "accepted_by": "<who, if accepted>"
}
```

### 6. Validate the return contract (C0 gate)

Every tracked deliverable's return block ends with the `return_contract_v1.md` JSON. Run the
deterministic gate on it — a model can be confident and wrong; a script can't be charmed:

```
python C:\Bari\03_operations\validators\validate_return.py --md <return_block.md> [--root C:\Bari] [--run-commands] [--emit-json]
```

- Input: `--md` (last ```json fence extracted), `--json` (raw contract file), or stdin.
- Hard checks: **C1** schema (7 required keys, status ∈ RETURNED/BLOCKED, types) · **C2** artifacts
  (sha256 matches disk; deleted actually gone; created/modified exist) · **C3** counts form (every
  count carries a number AND a named source/denominator) · **C5** distribution (full-set "N/N"
  claims with N≥10, or score/grade-named counts, must carry stdev/median/most_common/min-max) ·
  **C4** commands (well-formed; with `--run-commands`, re-executed and exit codes must match) ·
  **C6** citations (PMID token format; handed to verify_citations.py when present — never trust
  agent identifiers).
- **Exit 0 = pass (WARN allowed) · 1 = HARD fail · 2 = load error.** Exit 2 (no parseable
  contract) is itself an automatic CHANGES_REQUESTED per the return contract rule.
- `--selftest` verifies the gate itself still distinguishes a good from a bad contract.

### 7. Fixture discipline (mutation-testing rule)

**Status: MISSING.** The fixture library the Adversarial QA Agent is chartered to own
(`03_operations/page_generator/fixtures/` — known-bad inputs that must keep failing, golden
inputs that must keep passing; founding known-bad = rejected yogurts v4) **does not exist at that
path** (verified 2026-07-04; the only `fixtures/` dir in the repo is
`03_operations/bsip0/scrape/_shared/fixtures/`, which holds scraper HTML samples — a different
instrument). Until it is built:

- The rule still binds as a **manual discipline**: after any gate/generator change, re-run the
  suites (steps 1–2) against at least one known-bad input and one known-good (golden) page JSON.
  A known-bad that passes = **the check is broken** = a FAIL of the change, not a pass of the input.
- Seeded-defect drills: plant a documented defect in a COPY of a corpus and confirm the suite
  catches it. Never seed defects in real corpora; always work on copies and say so.
- If you build the library, put it at the chartered path and update this section.

### 8. Freeze baselines

After a clean run (steps 1–2 exit 0, zero hard fails, all warnings accepted or resolved):

- Freeze the QA baseline by recording the run ID and date
- Update the baseline reference for the category (this becomes the `--baseline` input for the
  next run's G7 PARITY diff)
- Record which warnings were accepted and by whom
- **Forbidden:** freezing a baseline over a run with unresolved hard fails (Adversarial QA Agent
  hard rule 8; D9 is that agent's sole authority)

Baseline freeze record:
```json
{
  "category_slug": "<slug>",
  "baseline_run_id": "<run_id>",
  "freeze_date": "<ISO date>",
  "frozen_by": "<owner>",
  "gate_evidence": {
    "run_gates_exit": 0,
    "run_gates_report": "<path to *_gates_report.md>",
    "validate_comparison_page_exit": 0
  },
  "accepted_warnings": [],
  "prior_baseline_archived": true
}
```

### 9. Invalidate bad runs

A run must be invalidated if:

- Pipeline ran against wrong corpus version
- The gate suite or pipeline had a known bug during the run (mutation-testing failure class:
  a known-bad passed)
- Data contamination is detected post-run (e.g. OFF marker found later)
- Run was not initiated from a clean pipeline state

To invalidate:
- Mark the run ID as invalid in the QA run registry
- Record the invalidation reason
- Do not freeze or reference an invalidated run (including as a `--baseline`)
- Re-run from a clean state

Invalidation record:
```json
{
  "run_id": "<run_id>",
  "invalidated_date": "<ISO date>",
  "invalidated_by": "<owner>",
  "reason": "<description>",
  "replacement_run_id": "<new run id, if known>"
}
```

---

## Forbidden Actions

- Do not declare a page pass on one instrument alone — go-live evidence is BOTH
  `validate_comparison_page.py` AND `run_gates.py` at exit 0, cited with report paths
- Do not declare "done" on gate exit codes — done = rendered in a real DOM + red-teamed
  (Track C report, 0 open CRITICAL)
- Do not eyeball anything an instrument checks deterministically; do not paraphrase a gate
  report — cite the exact FAIL lines
- Do not freeze a baseline over a run with hard fails
- Do not accept warnings without recording who accepted them and why
- Do not run QA against a stale or previously invalidated baseline
- Do not promote a category with an unresolved hard fail
- Do not skip traceability checks even for small or low-stakes categories
- Do not invalidate a run without recording the reason and initiating a replacement run
- Do not fix what you find — this is the QA lane: identify, record, route to the owning agent
  (no self-healing)

---

## Expected Output Format

Final QA audit report:

```json
{
  "category_slug": "<slug>",
  "run_id": "<run_id>",
  "run_date": "<ISO date>",
  "auditor": "Claude (bari-qa-audit)",
  "instruments": {
    "run_gates": {"exit_code": 0, "report": "<path>", "gates_failed": []},
    "validate_comparison_page": {"exit_code": 0, "hard_fails": [], "warnings": []},
    "validate_return": {"exit_code": 0}
  },
  "traceability_check": "pass | fail",
  "hard_fails": [],
  "warnings": [],
  "verdict": "pass | fail | invalidated",
  "baseline_frozen": true,
  "baseline_run_id": "<run_id>",
  "promotion_blocked": false,
  "blocking_reason": "",
  "rendered_and_redteamed": false
}
```

(`rendered_and_redteamed` stays false until the DOM render check and Track C challenge report
exist — gates green alone never flips it.)

---

## Owner Mapping

| Responsibility | Owner |
|---|---|
| Gate instruments (run_gates.py, validate_comparison_page.py) | Adversarial QA Agent (runs), Data Architecture (maintains) |
| Return-contract C0 gate (validate_return.py) | Orchestrator (runs on every return) |
| Traceability Verification | Adversarial QA Agent — Track V |
| Hard Fail Review | Adversarial QA Agent |
| Warning Acceptance | Category Team + Adversarial QA Agent |
| Baseline Freeze Authorization (D9) | Adversarial QA Agent (sole authority) |
| Run Invalidation | Adversarial QA Agent + Engineering Lead |
| Fixture library (when built) | Adversarial QA Agent |
