# P48 / TASK-265 — Factory trust layer 4b: dual-extractor consensus (route: C1, Data Agent)

CONTEXT: Repo C:\Bari. The trust layer's second half: a **dual-extractor** so a single parser
bug can't silently corrupt data. Same raw HTML goes through TWO independent extractors — the
rule-based `replay_parse` (deterministic) and **Gemini** (independent LLM, different failure
mode) — and the consensus is compared field-by-field. Agreements → high confidence;
disagreements → flagged for review. Neither extractor silently wins.

## BUILD `03_operations/spine/dual_extract.py`
1. **Extractor A (rule-based):** the existing BSIP0 from `replay_parse` — either read the
   already-produced `03_operations/spine/_e2e_out/bsip0/bsip0_*.json`, or re-run replay_parse
   on the raw HTML. This is the deterministic baseline.
2. **Extractor B (Gemini, independent):** for each raw HTML fixture
   (`03_operations/spine/_fixtures_e2e/raw/raw_e2e_*.html`), call the Gemini CLI:
   `gemini --skip-trust -p "<extraction prompt with the HTML embedded>"` via subprocess
   (binary: `C:\Users\HP\AppData\Roaming\npm\gemini.cmd`; or `shutil.which("gemini")`).
   Parse Gemini's JSON reply (strip ``` fences if present; be robust to minor formatting).
3. **Consensus compare** per product, per field (energy_kcal, protein_g, fat_g,
   fat_saturated_g, carbohydrates_g, sugars_g, dietary_fiber_g, sodium_mg, + ingredients):
   - numeric: AGREE if within a small tolerance (e.g. ±0.1 or ±1%); else DISAGREE.
   - one side null/other present → FLAG (one-missing).
   - report both values on any disagreement.
4. **Emit** `03_operations/spine/_e2e_out/dual_extract_report.{json,md}`: per-product field
   table (A value · B value · verdict), plus an agreement-rate summary (confidence).

## GEMINI EXTRACTION PROMPT — fabrication is the risk; make these rules explicit
The prompt you send Gemini MUST instruct it to:
- Extract ONLY values **explicitly present in the provided HTML**. Return JSON.
- If a field is not in the HTML → **null**. Do NOT infer, estimate, round-from-memory, or
  use ANY outside/world knowledge.
- **Never use Open Food Facts or any external source** (TASK-238). The HTML is the only source.
- Return strict JSON with the exact field keys above; no prose.
The consensus check is itself the fabrication guard: if Gemini invents a value, it disagrees
with the rule-based parser → FLAGGED, never silently accepted.

## ACCEPTANCE
- `python 03_operations/spine/dual_extract.py` runs on all 3 fixtures, calls both extractors,
  writes the consensus report, exits 0.
- The report shows per-field A-vs-B verdicts + an agreement rate. On these clean synthetic
  fixtures, expect high agreement; report any disagreement with both values (don't hide it).
- If a Gemini call fails/times out, handle gracefully (mark that product's B-side "unavailable",
  don't crash).
- Zero OFF anywhere; the Gemini prompt enforces no-invention/no-external-source.
- Note how this wires into the factory: dual-extract runs at the extraction stage; fields that
  DISAGREE block auto-publish and route to review.

## GUARDS
- **THROWAWAY ONLY** — synthetic fixtures, scratch dirs. No live category, no consumer page,
  no yogurts/cereals. Do NOT modify replay_parse, the engine, live artifacts, or any score.
- stdlib + subprocess to the gemini CLI only; no new Python deps. Read-only over inputs.

## RETURN BLOCK
The `dual_extract.py` path; the run output; the consensus report (paste the per-field table +
agreement rate); any A-vs-B disagreement found (with both values + which you'd trust and why);
confirmation the Gemini prompt forbids invention/external sources; the factory-wiring note.
End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`products_cross_checked`, `fields_compared`, `fields_agree`, `fields_disagree`,
`gemini_calls_ok`, `off_introduced: 0`, `replay_parse_modified: false`. **Propose RETURNED —
do NOT write CLOSED; the orchestrator verifies and closes.**
