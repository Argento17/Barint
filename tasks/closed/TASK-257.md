---
id: TASK-257
title: "Page Generator — the machine that turns a scored shelf into a complete, gated category page"
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - generate_page.py exists (asserted) and is the production generator; TASK-321 conformance sweep complete 2026-06-18. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
owner: Orchestrator (program) · C1/C2 execution
created: 2026-06-12
returned: 2026-06-12
supersedes: TASK-256 relaunch chain (dead — goal drift; see owner_systematic_not_artisanal)
---

## Position in the architecture (NOT a new program)
TASK-257 = **Spine's missing QA + package stages**, built first because the last
failure (yogurt v4) happened exactly there. Mapping to the gap-analysis cards:
- **Card #7 (real DAG):** scrape=done (raw store) · extract=Phase 5 · score=BSIP2 ·
  **QA = Phase 0b gates (P26)** · **package = Phase 1 generator (P27)**. Stages are
  written as pure typed callables → Dagster/Prefect adoption later is wiring, not rework.
- **Card #8 (queryable datastore / generated view):** Phase 1 IS "frontend JSON
  becomes a generated view" — file-substrate first; **Phase 0a's contract is the
  future table schema**; datastore = substrate swap under a working generator.
- **Card #1 (dual-extractor):** Phase 5 — extends the machine backward into extract.
- **Card #2 (property-based engine tests):** NOT covered here — engine-side, belongs
  in **Shadow** as an independent parallel track (can be specced for C1 anytime).

## Owner intent (verbatim anchor)
"I want a process that takes a shelf and turns it into a well-explained, full of all
the products in the shelf, no errors, page. Like the Milk page, like the granola,
like the snacks. I wanted a machine that produces these pages quickly and efficiently."

## The machine (definition)
One command — `generate <category>` — consuming:
- **BSIP1 corpus** (nutrition, ingredients, images, Hebrew names)
- **BSIP2 run** (scores, grades, traces, explanation drivers)
- **category config** (dedup rules, exclusions-with-evidence, retailer scope)

Producing, mechanically and idempotently:
1. **frontend JSON** — ALL products, ALL fields carried (a generator never forgets
   images or drops 70 products; hand-built prompt chains do)
2. **copy layer** — per-product insight lines from trace drivers (standalone rule,
   no cross-references) + page strings (prologue, category caveat, methodology)
3. **gate report** — pass/fail, machine-run: coverage, scope, OFF, grade-integrity,
   copy-safety, claim gate, parity-vs-live
4. **preview build** — side-by-side with the current page → owner approves → swap.
   No swap without the Page Parity Gate. Ever.

## Phases
| Phase | Deliverable | Route | Prompt |
|---|---|---|---|
| 0a | Output contract reverse-engineered from the 3 working pages (milk/granola/snacks) → JSON schema + field inventory | C2 | P25 |
| 0b | Gate suite as code (7 gates, runnable on any frontend JSON) | C1 | P26 |
| 1 | `generate_page.py` — data → full frontend JSON (strings PENDING), validated by regenerating granola/snacks data and diffing ≈0 vs live (milk = shadow diff ONLY, frozen) | C1 (+C2 configs) | P27/P28 |
| 2 | Copy engine — insight lines from trace drivers + page strings + auto claim-gate run; confidence labels = mechanical mapping | C1 (+C2 mapping) | P29/P30 |
| 3 | Preview wiring + parity gate + owner side-by-side | C2 | P31 |
| 4 | Second category through the machine + "new category" runbook | C1/C2 | P32+ |
| 5 (backlog) | Extraction (raw store → BSIP1) + dual-extractor consensus — extends the machine back to fresh scrapes. Raw store already LIVE (Shufersal + Yohananof). | — | — |

## Pilot data
Yogurts — because every input already exists (87 scored & Nutrition-audited, 100%
images in BSIP1, run_yogurt_006_shipcfg2). **The deliverable is the machine.** The
yogurt page output swaps only after the parity gate and explicit owner approval;
until then the restored v3 page stays. Validation categories: granola + snacks
(regenerate their data from sources; diff vs live must be ≈0).

## Hard rules carried in
OFF ban (gate 4) · frozen invariants (milk shadow-diff only, no score moves) ·
honest grades (boundary rounding policy → Nutrition decision, gate-configurable) ·
no-erasure (exclusions always with evidence) · UI never interprets (VM contract).

## Definition of done
A new scored category goes from BSIP2 run to owner-approvable preview in ≤1 day of
C1/C2 prompt-rounds with zero orchestrator hand-assembly, and the gate report is
green without manual fixes.
