(route: C1-GROK)

# P237 — Gold Set Phase 1: encode the 30-product seed into `gold_set_seed_v0.json` (TASK-349)

Spec-complete data build. Read `tasks/TASK-349.md` and the Phase-0 source of truth
`03_operations/shadow/goldset/phase0_nutrition_grounding.md` first (it contains the 30 proposed seed
products with tiers, expected bands, dimension directions, and rationales).

## Repo / paths
- Repo root: `C:\Bari` (isolated checkout — work only in these paths).
- BUILD THIS FILE ONLY: `03_operations/shadow/goldset/gold_set_seed_v0.json`.
- Sources to read (read-only): the Phase-0 md (the 30 entries); per-corpus flag configs in
  `03_operations/shadow/shadow_registry_v1.json` (use each corpus's exact merged flag config so the
  harness scores apples-to-apples); BSIP1 product files under `03_operations/bsip1/...` and
  `02_products/...` (paths per the registry `source` per corpus) to CONFIRM nutrition values for the
  8 data-gap entries the Phase-0 note flagged (A02, A05, A06, A07, A08, A09, A10, P09).

## SHARED GOLD CONTRACT (identical across P236/P237/P238 — emit exactly this)
Top level: `{ "schema_version": "v0", "source_baseline": "baseline_20260616T052730Z", "note": "...", "entries": [ <entry>... ] }`
Entry:
```
{
  "id": "G-001", "pid": "bsip1_...", "corpus": "milk", "tier": "good|poor|ambiguous",
  "scoring_flags": { ... },                 // copy the corpus's exact merged flag config from the registry
  "expected": {
    "grade_band": ["B","C"],                // inclusive acceptable grades (S/A/B/C/D/E)
    "score_range": [50, 64],                // inclusive numeric range consistent with the grade band
    "dimensions": { "fat_quality": "low", "nutrient_density": "high" }   // 2-4 dims, labels: low|medium|high
  },
  "rubric": [ {"criterion":"...","rationale":"...","basis":"USDA FDC|BSIP0 panel|direct product scrape","citation":"..."} ],
  "provenance": { "authored_by":"nutrition-agent (P235)", "authored_blind": true,
                  "reviewed_by":"pending-red-team", "agreement":"pending" }
}
```

## Objective
1. Encode ALL 30 Phase-0 seed products into the entry format above. Carry over each product's tier,
   expected grade_band, score_range, dimension directions, and rubric rationale + basis from the md.
2. For each entry's `scoring_flags`, copy the EXACT merged flag config for that product's corpus from the
   registry (engine_default_flags + the corpus's flag overrides). Do not invent flags.
3. For the 8 data-gap entries, OPEN the BSIP1 product file and confirm the nutrition values the rationale
   relies on; if a value cannot be found in the scrape, leave it null and note it (missing-data rule —
   never fabricate, never substitute).
4. Grade-band ↔ score-range MUST be internally consistent with the cutoffs (S≥90, A 80-89, B 65-79,
   C 50-64, D 35-49, E 0-34). A band like ["B","C"] → range within [50,79].

## Boundaries / guards
- BUILD ONLY the one JSON file. Do NOT touch the engine, configs, page-JSON, or any other file. Never run git.
- **Independence firewall (C3 ruling): expected bands come from FIRST-PRINCIPLES nutrition + the physical
  label ONLY. Do NOT read or copy any Bari engine score/grade/dimension output into `expected`.** Keep
  `authored_blind: true` honest — the band must be defensible from the label alone.
- OFF ban (absolute): never source nutrition/ingredients/names from Open Food Facts. Direct scrape / USDA
  FDC / BSIP0 panel only. Any value that can't be sourced stays null.
- Valid JSON, UTF-8, Hebrew product names preserved.

## Return format
Path + sha, entry count by tier, the 8 data-gap entries' resolution (confirmed value or null + why), and
confirmation no engine score leaked into `expected`. End with the return contract. Do not close — propose RETURNED.

```json
{
  "task": "P237", "proposed_status": "RETURNED",
  "artifacts": [{"path": "03_operations/shadow/goldset/gold_set_seed_v0.json", "action": "created", "sha256": "<hash>"}],
  "counts": {"entries": "30/30 (good:10 poor:10 ambiguous:10)", "data_gap_resolved": "<k>/8 confirmed, <m>/8 null"},
  "commands_run": [{"cmd": "python -c 'import json;json.load(open(...))'  # validates", "exit_code": 0}],
  "not_done": [], "self_check": "no engine score/grade copied into any expected{}; band↔range internally consistent: <observed>"
}
```
