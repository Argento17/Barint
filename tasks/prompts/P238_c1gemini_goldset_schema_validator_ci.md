(route: C1-GEMINI)

# P238 — Gold Set Phase 1: formal schema + validator + CI wire (TASK-349)

Spec-complete build. Read `tasks/TASK-349.md` and `03_operations/shadow/goldset/phase0_nutrition_grounding.md`
first. You formalize the gold contract, build a linter, and wire the gate into CI alongside Shadow.

## Repo / paths
- Repo root: `C:\Bari` (isolated checkout — work only in these paths).
- BUILD THESE FILES ONLY:
  1. `03_operations/shadow/goldset/gold_set_schema.json` — a JSON-schema (draft 2020-12) of the gold contract below.
  2. `03_operations/shadow/goldset/validate_goldset.py` — stdlib-only linter that validates a seed file
     against the schema + the consistency rules; exit 0 ok / 1 invalid; CLI `python validate_goldset.py [--seed PATH]`.
  3. CI: ADD a `gold_check` step to the engine-touching workflow that already runs the Shadow diff. Find it
     under `.github/workflows/` (the one with `shadow` / `shadow_gate`). Add a job/step that runs
     `python 03_operations/shadow/goldset/validate_goldset.py` then `python 03_operations/shadow/goldset/gold_check.py`
     and treats **exit 2 as a reported FINDING (non-blocking: continue-on-error or a warning annotation), NOT a
     hard CI failure** — the accuracy gate surfaces disagreements for Nutrition review; it must never block a
     merge or be a lever to force engine changes (C3 backdoor ruling). exit 3 (harness error) MAY fail the job.

## SHARED GOLD CONTRACT (identical across P236/P237/P238 — your schema formalizes exactly this)
Top level: `{ "schema_version":"v0", "source_baseline":"...", "note":"...", "entries":[ <entry> ] }`
Entry fields: `id` (str), `pid` (str), `corpus` (str), `tier` (enum good|poor|ambiguous),
`scoring_flags` (object), `expected` { `grade_band` (array of S/A/B/C/D/E), `score_range` ([min,max] ints
0-100), `dimensions` (object of dim→ low|medium|high) }, `rubric` (array of {criterion, rationale,
basis ∈ {USDA FDC, BSIP0 panel, direct product scrape}, citation}), `provenance` { `authored_by`,
`authored_blind` (bool), `reviewed_by`, `agreement` (enum yes|no|pending) }.
Consistency rules the validator MUST enforce:
- grade_band non-empty, values from the 6 grades; score_range min≤max within [0,100] and consistent with
  the band per cutoffs (S≥90, A 80-89, B 65-79, C 50-64, D 35-49, E 0-34).
- dimension labels ∈ {low,medium,high}; dim keys ∈ the 10 engine dims (processing_quality,
  nutrient_density, calorie_density, glycemic_quality, protein_quality, additive_quality,
  satiety_support, fat_quality, regulatory_quality, whole_food_integrity).
- `basis` must NOT be "Open Food Facts" / "OFF" (OFF-ban check) and must be one of the allowed sources.
- **No engine-score field may exist in `expected`** (independence firewall): reject any key like
  `actual_score`, `bari_score`, `engine_grade` inside an entry.

## Boundaries / guards
- BUILD ONLY the 3 paths above. Do NOT touch the engine, configs, page-JSON, the seed file, or gold_check.py
  (other lanes own those). Never run git. The CI edit is additive — do not alter the existing shadow_gate logic.
- OFF ban (absolute): the validator actively rejects OFF as a basis; introduce no OFF anywhere.
- stdlib only (no jsonschema dep — implement the checks directly in validate_goldset.py).

## Return format
Paths + shas of the 3 files, the CI workflow filename + the added step, validator exit on a tiny valid and
a tiny invalid sample (paste both), and confirmation the CI step is non-blocking on exit 2. End with the
return contract. Do not close — propose RETURNED.

```json
{
  "task": "P238", "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/shadow/goldset/gold_set_schema.json", "action": "created", "sha256": "<hash>"},
    {"path": "03_operations/shadow/goldset/validate_goldset.py", "action": "created", "sha256": "<hash>"},
    {"path": ".github/workflows/<file>.yml", "action": "modified", "sha256": "<hash>"}
  ],
  "counts": {"consistency_rules": "<n> enforced", "ci_exit2_blocking": "false (finding-only)"},
  "commands_run": [{"cmd": "python validate_goldset.py --seed <valid-sample>", "exit_code": 0},
                   {"cmd": "python validate_goldset.py --seed <invalid-sample>", "exit_code": 1}],
  "not_done": [], "self_check": "OFF-as-basis rejected + no engine-score key allowed in expected: <observed>"
}
```
