# Return: P158

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P158_rescore_all_fix_shelfstats.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-16T08:46:10.224306+00:00 |
| Finished | 2026-06-16T08:51:07.843162+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P158 task prompt and execute it as specified.
Reading related task files and canonical scoring patterns.
Implementing per-shelf scoring config and rewriting `rescore_all.py` to apply shelf-relative stats from those configs.
Adding scoring blocks to configs, then rewriting `rescore_all.py`.
Rewriting `rescore_all.py` with the generic config-driven scoring loop.
Fixing the C10 milk baseline path (traces live in subdirs, not flat files) and re-running to verify.
C10 failures look like engine drift, not a shelf-stats bug. I'll make C10 report failures without aborting the shelf so we still get the full acceptance table.
## P158 / TASK-298 — RETURNED

### What changed

| File | Action | Verify at |
|------|--------|-----------|
| `03_operations/page_generator/rescore_all.py` | **rewritten** | Config-driven loop: `scoring.flags` → reload engine → `set_shelf_stats` / EV-056 sodium → `score_one()` → C10 → `clear_shelf_stats` → `generate_page` → acceptance vs `baseline_json` |
| `03_operations/page_generator/configs/brined_cheeses.json` | **modified** | `scoring` block: EV-056 sodium (`compute_from_corpus`), brined flags from `batch_run_brined_cheeses_005.py` |
| `03_operations/page_generator/configs/cereals.json` | **modified** | `scoring`: no shelf-rel; `BARI_SHELF_RELATIVE_V1=off`; source `batch_run_cereals_008.py` |
| `03_operations/page_generator/configs/hard_cheeses.json` | **modified** | `scoring`: `fat_saturated_g` median=18.0 scale=1.4; source golive + `constants.py` |
| `03_operations/page_generator/configs/juices.json` | **modified** | `scoring`: `sugars_g` median=9.5 scale=2.82; source golive + `constants.py` |
| `03_operations/page_generator/configs/cakes.json` | **modified** | `scoring`: `sugars_g` median=29.0 scale=9.044 + corpus_filter; source golive |
| `03_operations/page_generator/configs/cookies_coffee.json` | **modified** | `scoring`: all shelf-rel off; source `batch_run_cookies_005.py` + `batch_run_cakes_001.py` |
| `03_operations/page_generator/configs/hummus_shelfrel_002.json` | **modified** | `scoring`: `sodium_mg` median=390.0 scale=31.88; source `batch_run_hummus_shelfrel_002.py` |
| `03_operations/page_generator/configs/granola.json` | **modified** | `scoring`: no shelf-rel enrollment |
| `03_operations/page_generator/configs/snacks.json` | **modified** | `scoring`: no shelf-rel enrollment |

### ACCEPTANCE TABLE (actual run, wall-clock **10.3s**)

Command: `python 03_operations/page_generator/rescore_all.py` → exit **1**

| shelf | products | score-moves | grade-moves | reproduces-live? | C10 |
|-------|----------|-------------|-------------|------------------|-----|
| brined_cheeses | 36 | 14 | 3 | **NO** | FAIL (1 checked) |
| cakes | 65 | 19 | 3 | **NO** | PASS (20) |
| cereals | 20 | 0 | 0 | **YES** | FAIL (1) |
| cookies_coffee | 119 | 39 | 1 | **NO** | PASS (20) |
| granola | 25 | 15 | 8 | **NO** | FAIL (1) |
| hard_cheeses | 28 | 6 | 2 | **NO** | FAIL (1) |
| hummus_shelfrel_002 | 69 | 19 | 2 | **NO** | FAIL (1) |
| juices | 24 | 0 | 0 | **YES** | FAIL (1) |
| snacks | 53 | 16 | 10 | **NO** | PASS (20) |

**2/9 shelves reproduce live** (`cereals`, `juices`).

### Scoring blocks (nutrient / median / scale / key flags)

| shelf | nutrient | median | scale | scale_type | key flags | canonical source |
|-------|----------|--------|-------|------------|-----------|------------------|
| brined_cheeses | sodium_mg | corpus-computed (1000.0) | corpus-computed (266.25) | stdev | `SODIUM_SHELF_RELATIVE_V1=on`, `GRAD_SODIUM_V1=on`, `DAIRY_PROTEIN_REWEIGHT_V1=on` | `batch_run_brined_cheeses_005.py` |
| cereals | — | — | — | — | `RECAL_P0=on`, `SHELF_RELATIVE_V1=off` | `batch_run_cereals_008.py` |
| hard_cheeses | fat_saturated_g | 18.0 | 1.4 | iqr | `SHELF_RELATIVE_V1=on`, `FAT_TECH_V1=on` | golive + `FATSAT_SHELF_REL_HARDCHEESE_*` |
| juices | sugars_g | 9.5 | 2.82 | iqr | `SHELF_RELATIVE_V1=on`, `FAT_TECH_V1=on`, `RECAL_P0=on` | golive + `SUGAR_SHELF_REL_JUICES_*` |
| cakes | sugars_g | 29.0 | 9.044 | iqr | `SHELF_RELATIVE_V1=on`, `RECAL_P0=off` | golive + `SUGAR_SHELF_REL_CAKES_*` |
| cookies_coffee | — | — | — | — | all shelf-rel off, `RECAL_P0=off` | `batch_run_cookies_005.py` + `batch_run_cakes_001.py` |
| hummus | sodium_mg | 390.0 | 31.88 | iqr | `SHELF_RELATIVE_V1=on`, `RECAL_P0=on` | `batch_run_hummus_shelfrel_002.py` |
| granola | — | — | — | — | `RECAL_P0=on`, `SHELF_RELATIVE_V1=off` | cereals runners (no enrollment) |
| snacks | — | — | — | — | `SHELF_RELATIVE_V1=off` | `batch_run_snack_bars_001.py` (no enrollment) |

### P157 defect fix — brined evidence

- **Before (P157):** 36 score-moves, 24 grade-moves (missing shelf-relative sodium).
- **After (P158):** 14 score-moves, 3 grade-moves with `median=1000.0mg` EV-056 stats applied.
- **Committed `run_brined_005` traces vs live:** **0/36** rounded score mismatches, **0/36** grade mismatches.
- **Staging traces vs committed:** **14/36** rounded score mismatches (~2.1pt systematic delta) — **engine drift since `run_brined_005`**, not a missing shelf-stats bug.

### Shelves not reproducing live — root causes

1. **brined_cheeses, cakes, hard_cheeses, cookies_coffee, granola** — committed run traces match live; fresh rescore diverges (~2pt) under today's engine with correct per-shelf flags/stats. **Finding (b): live pages were produced by committed runs; current engine no longer byte-reproduces those runs.**
2. **hummus_shelfrel_002** — live `hummus_frontend_v5.json` `_meta.source_run_id=run_hummus_003`; config targets `run_hummus_shelfrel_002`. **Finding (b): baseline mismatch, not trigger wiring.**
3. **snacks** — live displays 18 curated products; trigger scores full 53-product corpus. Common-barcode diff shows engine drift from `run_snack_bars_001` era.
4. **C10 milk** — 6/9 shelves fail: milk `bsip1_5411188112709` baseline=46.2 vs new=49.0 (Δ=2.8) under category flags. **Engine drift since golive 2026-06-15**; cakes/cookies/snacks pass C10 (20/20 milk products).

### Proposed status: RETURNED

```json
{
  "task": "TASK-298",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/rescore_all.py", "action": "modified", "sha256": "44DA81D8A03EFD5CAC1CFF40CBFE88F223E7842F7236CA7D876E3544078C7A14"},
    {"path": "03_operations/page_generator/configs/brined_cheeses.json", "action": "modified", "sha256": "9B7658C6A20C42BDCFBA99898698B7D24A52F8778BCAACC655A5968DB078CD45"},
    {"path": "03_operations/page_generator/configs/cereals.json", "action": "modified", "sha256": "1D6150A5731A808C0487EA7C08C447F87F96EFEFA4B144B44643615D8CAB2C26"},
    {"path": "03_operations/page_generator/configs/hard_cheeses.json", "action": "modified", "sha256": "F67E6AD2A40EFFA1DEFD73EFC7D4DEE0502F1E96445B0F05FFFFCE96927DF48C"},
    {"path": "03_operations/page_generator/configs/juices.json", "action": "modified", "sha256": "7F942EF410FE2B824CC482D1667D8696D40ED3B0D61FAF2A15C012005077A3F8"},
    {"path": "03_operations/page_generator/configs/cakes.json", "action": "modified", "sha256": "9740996BF67715DDFE291450A613BD91144FCBEFD6616D6E0021AD5DA26F80CA"},
    {"path": "03_operations/page_generator/configs/cookies_coffee.json", "action": "modified", "sha256": "966FDD3B4B98D09209B0F54B2C69460BA1A968E1B54678F9FBB732A78F86D8CA"},
    {"path": "03_operations/page_generator/configs/hummus_shelfrel_002.json", "action": "modified", "sha256": "6214E8DB17AAEB756B8F98E2CF15926FD3E486F82F2754DD068FD7CAB08AFCBF"},
    {"path": "03_operations/page_generator/configs/granola.json", "action": "modified", "sha256": "1049D1C7FE4CD920FF272764EDDE8DCDEBDB723E58950FCC3ECEF2AF8FAA4C06"},
    {"path": "03_operations/page_generator/configs/snacks.json", "action": "modified", "sha256": "5A5581E7FB01FCE6BA53024321C7DDCE5E076E605D4EE2CBE864F671D38F211E"},
    {"path": "_rescore_staging/run_summary.json", "action": "created", "sha256": "pending-orchestrator-verify"}
  ],
  "counts": {
    "reproduces_live_shelves": "2/9 (_rescore_staging/run_summary.json reproduces_live=true)",
    "shelves_c10_pass": "3/9 (_rescore_staging/run_summary.json c10_pass=true: cakes,cookies_coffee,snacks)",
    "shelves_off_zero": "9/9 (_rescore_staging/run_summary.json off_count=0)",
    "brined_committed_vs_live_score_moves": "0/36 (run_brined_005 traces vs brined_cheeses_frontend_v2.json)",
    "brined_staging_vs_live_score_moves": "14/36 (_rescore_staging/brined_cheeses vs live)",
    "wall_clock_sec": "10.28 (_rescore_staging/run_summary.json)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/rescore_all.py", "exit_code": 1},
    {"cmd": "python -c \"import json; from pathlib import Path; s=json.loads(Path('_rescore_staging/run_summary.json').read_text()); print(sum(1 for x in s['shelves'] if x['reproduces_live']), len(s['shelves']))\"", "exit_code": 0}
  ],
  "not_done": [
    "Target 9/9 shelves reproduce-live: 7/9 still NO (engine drift vs committed runs + hummus baseline mismatch)",
    "C10 milk invariant: 6/9 shelves fail under current engine (orchestrator triage needed)"
  ],
  "self_check": "Acceptance run: cereals 0/0 and juices 0/0 score+grade moves vs live (YES); brined shelf-relative fix reduced moves from 36/24 to 14/3; committed run_brined_005 still 0/36 vs live"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M .gitignore
 M tasks/DISPATCH_BOARD.md
?? 03_operations/page_generator/rescore_all.py
?? agent-tools/
?? tasks/TASK-298.md
?? tasks/prompts/P157_rescore_all_trigger.md
?? tasks/prompts/P158_rescore_all_fix_shelfstats.md
?? tasks/returns/P157_return.md
```

### After dispatch

```
M .gitignore
 M 03_operations/page_generator/configs/brined_cheeses.json
 M 03_operations/page_generator/configs/cakes.json
 M 03_operations/page_generator/configs/cereals.json
 M 03_operations/page_generator/configs/cookies_coffee.json
 M 03_operations/page_generator/configs/granola.json
 M 03_operations/page_generator/configs/hard_cheeses.json
 M 03_operations/page_generator/configs/hummus_shelfrel_002.json
 M 03_operations/page_generator/configs/juices.json
 M 03_operations/page_generator/configs/snacks.json
 M tasks/DISPATCH_BOARD.md
?? 03_operations/page_generator/rescore_all.py
?? tasks/TASK-298.md
?? tasks/prompts/P157_rescore_all_trigger.md
?? tasks/prompts/P158_rescore_all_fix_shelfstats.md
?? tasks/returns/P157_return.md
```

### Delta

### New / modified since dispatch
   M 03_operations/page_generator/configs/brined_cheeses.json
   M 03_operations/page_generator/configs/cakes.json
   M 03_operations/page_generator/configs/cereals.json
   M 03_operations/page_generator/configs/cookies_coffee.json
   M 03_operations/page_generator/configs/granola.json
   M 03_operations/page_generator/configs/hard_cheeses.json
   M 03_operations/page_generator/configs/hummus_shelfrel_002.json
   M 03_operations/page_generator/configs/juices.json
   M 03_operations/page_generator/configs/snacks.json
### Removed / cleaned since dispatch
  ?? agent-tools/
