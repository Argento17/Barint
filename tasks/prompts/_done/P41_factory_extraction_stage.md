# P41 / TASK-259 — Factory: wire extraction Stage 0 (raw HTML → BSIP1) (route: C1, Data Agent)

CONTEXT: Repo C:\Bari. TASK-258 (P40) proved the Spine DAG executes a real chain
**BSIP1 → score → generate → gate** (`03_operations/spine/pipeline_e2e.py`), but it starts
from BSIP1-shaped fixtures — the extraction front is missing. Your job: add the real
**Stage 0** so the chain becomes a true **shelf → page** execution:

  raw HTML → **[extract: BSIP0]** → **[build: BSIP1]** → score → generate → gate

## USE THESE — inspect interfaces first, do not rebuild
- Existing pipeline (extend it, keep its 4 stages working): `03_operations/spine/pipeline_e2e.py`.
- Extraction: `03_operations/bsip0/raw_store/replay_parse.py` — the "offline BSIP0 replay
  parser." Key fns: `_parse_product_from_html(...)`, `run_replay_parse(...)`. Inspect its
  real input (raw HTML shape) and output (BSIP0 structured nutrition/ingredients).
- BSIP0 → BSIP1 builder: find the canonical transform that turns parsed BSIP0 into a BSIP1
  record (the shape pipeline_e2e's score stage already consumes — match it exactly). If no
  reusable builder exists, write a minimal one INSIDE the pipeline module (documented), but
  the BSIP1 output must match the schema the existing score stage reads.
- Runner + DB: `03_operations/spine/runner.py`, `spine_db.py` — import and reuse.

## THROWAWAY FIXTURE (no live category, no drift)
Prefer **synthetic raw HTML** fixtures (2–3 fake product pages whose HTML matches what
`replay_parse._parse_product_from_html` expects) under `03_operations/spine/_fixtures_e2e/raw/`.
If the parser genuinely needs real retailer HTML structure, you MAY copy a tiny throwaway
sample of banked raw pages (from `03_operations/bsip0/raw_store/shufersal/<cat>/`) as
**parser input only** — but the run output stays in the scratch dir `03_operations/spine/_e2e_out/`,
is a throwaway page, and is **never** a publishable/real category page. This is a pipeline
proof, not a category build.

## ACCEPTANCE
1. `pipeline_e2e.py --execute` now runs **Stage 0 (extract) + Stage 0.5 (build BSIP1)** plus
   the existing 4 stages, all **green**, producing the throwaway gated page from RAW input.
2. The BSIP0 → BSIP1 → score handoff is real: show a parsed value flowing from raw HTML
   through to a score (e.g. protein parsed from HTML → BSIP1 → influences the grade).
3. `spine.db` records the new stage_runs + lineage from raw → page.
4. **Resume** still holds (re-run with no change → all skipped) and **incremental** holds
   (edit a raw fixture → extraction + everything downstream re-runs; the BSIP1 fixtures that
   P40 used are removed/replaced so the chain now genuinely starts at raw).
5. Seam report: is the replay_parse BSIP0 output a clean match for the BSIP1 builder input,
   and the BSIP1 a clean match for the score stage? Document any mismatch.

## GUARDS
- **OFF ban (TASK-238) — extraction is the highest-risk point.** `replay_parse` / your build
  must NEVER fall back to Open Food Facts or any substitute. A field that doesn't parse from
  the raw HTML stays **null** — "data could not be retrieved." Any OFF path is a launch
  blocker: flag it, never introduce it. Grep the BSIP0/BSIP1 outputs for OFF markers and
  prove zero.
- **THROWAWAY ONLY.** No live category page, no yogurts/cereals, no consumer output, scratch
  dirs only. Do NOT touch `spine_yogurts.py`, live artifacts, published scores, the engine
  logic, or any consumer page.
- Import/reuse the runner + db; stdlib + existing scripts only; no new deps.

## RETURN BLOCK
The updated pipeline path + any new builder; the `--execute` stage dict (now 5–6 stages);
the raw→score trace evidence (one parsed value → grade); spine.db stage_runs + lineage
raw→page; resume + incremental proof; the seam report; grep proof of ZERO OFF in BSIP0/BSIP1
outputs. End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`stages_declared`, `stages_executed_real`, `chain_starts_at` ("raw_html"),
`off_introduced: 0`, `resume_all_skipped`, `seam_gaps_found`. **Propose RETURNED — do NOT
write CLOSED; the orchestrator verifies and closes.**
