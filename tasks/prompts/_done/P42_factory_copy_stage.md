# P42 / TASK-260 — Factory: wire the copy stage into the DAG (route: C1, Data Agent)

CONTEXT: Repo C:\Bari. The factory chain (`03_operations/spine/pipeline_e2e.py`) now runs
raw HTML → extract → score → generate → gate, producing a STRUCTURALLY-gated page whose copy
fields are `PENDING_COPY`. Your job: add the **copy stage(s)** to the DAG so the throwaway
page comes out **copy-complete (0 PENDING_COPY)** and copy-gated — making it a *well-explained*
page, which is the factory's whole point.

## THE OWNER'S QUALITY BAR = THE MILK PAGE
Owner ruling 2026-06-12: the milk page is the best content version "in all content aspects."
**Read `bari-web/src/data/milk-comparison.json` first** and study its content depth — per
product it carries `consumerTakeaway` + `consumerExplanation` + `bariInterpretation` +
`bestUseCases`; page-level `story_headline` / `story_teaser` / `philosophy_note`. THIS is
what "well-explained" means here. Your copy stage must be *capable of carrying* that depth.
**If the canonical-v2 page schema (`03_operations/page_generator/contract/page_output_schema_v2.json`)
cannot represent milk-level content depth, FLAG it as a schema gap** — do not silently dumb
the content down to fit.

## USE THESE — extend, don't rebuild
- Pipeline: `03_operations/spine/pipeline_e2e.py` (keep its 5 stages green; add copy stages after generate_page, before/around gate).
- Copy engine (already exists, generic): `03_operations/page_generator/copy/build_copy_inputs.py` (deterministic fact-sheets) and `03_operations/page_generator/copy/merge_copy.py` (deterministic merge + readability + gates).
- Gates: `03_operations/page_generator/gates/run_gates.py` (G6 COPY-SAFETY must run on the merged copy).
- Runner + DB: `03_operations/spine/runner.py`, `spine_db.py` — import/reuse.

## THE AGENT-IN-LOOP SEAM (the key design)
Authoring milk-quality Hebrew copy is an LLM step, not a deterministic function. Design the
copy stage as THREE parts so the DAG owns the deterministic bookends and the authoring is a
clean, pluggable seam:
1. **build_copy_inputs** (DAG stage, deterministic) — fact-sheets from the generated page.
2. **author_copy** (the seam) — reads fact-sheets, writes authored-strings JSON. Define a
   precise **authoring contract**: exact input (fact-sheet fields) and output (the string
   fields the merge expects) as a documented JSON schema, so a real Content-Agent (LLM) pass
   plugs in unchanged. For THIS throwaway run, implement a clearly-labelled **baseline
   author** (deterministic, from fact-sheets) so the DAG runs end-to-end automatically — but
   mark it `author_engine: "baseline_placeholder"` and document that production swaps in the
   Content Agent with the milk page as the bar. Do NOT pretend the baseline is final quality.
3. **merge_copy + copy-gate** (DAG stage(s), deterministic) — merge authored strings into the
   page, run readability on every string, run the gate suite incl. G6.

## ACCEPTANCE
1. `pipeline_e2e.py --execute` runs the copy stages in order; the throwaway final page has
   **0 PENDING_COPY** and passes **G6 COPY-SAFETY + readability 100%**.
2. spine.db records the new copy stage_runs + lineage (page → fact_sheets → authored → final).
3. **Resume** + **incremental** still hold for the whole chain.
4. A written **authoring contract** (input fact-sheet schema → output string schema) so the
   real Content-Agent author swaps into the `author_copy` seam with no other change.
5. A **milk-depth schema assessment**: can canonical-v2 carry milk-level content depth? If
   not, list exactly which content dimensions (e.g. a per-product `bariInterpretation`-class
   field) are missing.

## GUARDS
- **THROWAWAY ONLY** — synthetic fixtures, scratch dirs (`spine/_e2e_out`), no live category, no consumer page, no yogurts/cereals. Do NOT touch `spine_yogurts.py`, live artifacts, published scores, the engine, or any consumer page.
- **OFF ban (TASK-238):** copy must never assert data the page doesn't have; null stays "data could not be retrieved"; no OFF anywhere.
- Import/reuse the runner + existing copy scripts; stdlib only for new code; no new deps.
- Baseline author must obey the standing editorial law (standalone lines; grade-in-prose = badge; sodium/fat never causal; no framework leakage) even as a placeholder — a placeholder that violates the law teaches the wrong contract.

## RETURN BLOCK
Updated pipeline path; the `--execute` stage dict (now ~7 stages); the final throwaway page
path + PENDING count (must be 0); G6 + readability result verbatim; spine.db copy stage_runs
+ lineage; resume + incremental proof; the **authoring contract** (paths/schema); the
**milk-depth schema assessment**. End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`pending_remaining: 0`, `copy_stages_added`, `author_engine: "baseline_placeholder"`,
`readability_clean`, `g6_pass`, `off_introduced: 0`, `schema_carries_milk_depth: true|false`.
**Propose RETURNED — do NOT write CLOSED; the orchestrator verifies and closes.**
