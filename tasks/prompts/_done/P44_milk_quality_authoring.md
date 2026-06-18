# P44 / TASK-263 — Real Content-Agent milk-quality authoring through the contract (route: C1, Content Agent)

CONTEXT: Repo C:\Bari. The factory now emits milk-DEPTH v3 pages, but the copy is filled by a
**baseline placeholder author**. Your job: fill the `author_copy` seam with REAL milk-quality
Hebrew copy via the authoring contract, then merge+gate → a milk-quality throwaway page. This
proves the agent-in-loop authoring mechanism (the production design: the Content Agent IS the
author_copy stage). Your Pre-Return Self-Check in `.claude/agents/content-agent.md` is law.

## THE BAR = THE MILK PAGE
Read `bari-web/src/data/milk-comparison.json` and match its CONTENT quality — the depth and
tone of its `consumerExplanation`, `bariInterpretation`, `consumerTakeaway`, `bestUseCases`.
This is the owner's gold standard "in all content aspects."

## INPUTS (author from these ONLY — never invent)
- Authoring contract: `03_operations/page_generator/copy/authoring_contract.json` (v2 — input/output schema).
- Fact-sheets: `03_operations/spine/_e2e_out/copy/fact_sheets.json` (3 throwaway synthetic products; their real driver, dimension scores/strengths, null-safe nutrition, ingredients head, superlatives_allowed).
- The generated page (for the deterministic bariInterpretation key/label/score/strength you must write `interpretation` text against): `03_operations/spine/_e2e_out/page/e2e_page_throwaway.json`.
**These are SYNTHETIC fake products** (test cracker/cookie/oat-snack). Author real, honest copy
about the data each fact-sheet gives — this proves writing quality + mechanism, not real-world
product insight.

## AUTHOR (per product, all v3 fields, milk-depth)
`insightLine`, `rowVerdict`, `comparisonContext`, `expansion.positiveSignals[]`,
`expansion.limitingFactors[]`, `consumerTakeaway`, `expansion.consumerExplanation`
(`whyRated`, `good[]`, `watchOut[]`, `context`, `takeaway`), `bariInterpretation[].interpretation`
(one line per dimension, **grounded in that dimension's real score/strength — never contradict
the number**), `bestUseCases[]`. Page-level: `_page.{story_headline, story_teaser, philosophy_note}`.

## EDITORIAL LAW (each violation = revision)
Standalone lines (no cross-references); grade-in-prose = badge grade; **sodium & fat NEVER
causal**; named driver = the fact-sheet's real driver; `cap_misclaim_risk` products claim NO
cap; numbers only from the product's own fact-sheet; superlatives only if granted; no framework
leakage (NOVA/BSIP/cap/dimension/proxy); no banned phrases incl. "חלבון נמוך" as a bare
dismissal; bariInterpretation text must agree with the dimension score. Quality bar = the milk page.

## RUN THE TAIL
Write your authored output to the path the merge reads (the contract's output file, e.g.
`03_operations/spine/_e2e_out/copy/authored.json`, marking `_meta.author_engine: "content_agent_p44"`),
then run merge + gates directly (do NOT re-run the full pipeline — that would re-fire the
baseline author and overwrite you):
`python 03_operations/page_generator/copy/merge_copy.py --page .../e2e_page_throwaway.json --copy .../authored.json --out .../e2e_page_throwaway_final.json --config <copy_config> --schema 03_operations/page_generator/contract/page_output_schema_v3.json`
then `run_gates.py` on the final. Final must be **0 PENDING_COPY**, **G2/G6 PASS**, **readability 100%**.

## GUARDS
- **THROWAWAY ONLY** — scratch dirs, synthetic fixtures, no live category, no consumer page, no yogurts/cereals. Do NOT touch live page JSONs, the milk page (read-only), published scores, or the scoring engine.
- **OFF ban (TASK-238):** if a fact-sheet field is null, the copy says "data could not be retrieved" — never fill from OFF or invent. No OFF anywhere.

## RETURN BLOCK
The authored.json path; a 3-card sample (all v3 fields) for the orchestrator's editorial read
vs the milk bar; the merge + gate result verbatim (0 PENDING, G2/G6, readability N/N); which
superlatives you used; any bariInterpretation line where the score made the honest read
awkward. End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`products_authored: 3`, `v3_fields_per_product`, `pending_remaining: 0`, `readability_clean`,
`g2_g6_pass`, `off_introduced: 0`. **Propose RETURNED — do NOT write CLOSED; the orchestrator
verifies and does an editorial read before closing.**
