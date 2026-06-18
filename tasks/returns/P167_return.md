# Return: P167

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P167_affected_set.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-17T15:34:43.398562+00:00 |
| Finished | 2026-06-17T15:36:20.610170+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P167 task prompt and follow its instructions below the separator.
Reading sample shadow report, registry, configs, and shadow_backtest to implement the module.
Implementing `affected_set.py` and verifying it against the sample report.
## P167 / TASK-317 — RETURNED

Built `03_operations/page_generator/affected_set.py`: a read-only wrapper over shadow reports that resolves flag what-ifs into an affected-set manifest for the spine orchestrator.

### What was built

**`affected_set.py`** — CLI module that:
- Accepts `--report <shadow_report.json>` or invokes `shadow_backtest.py diff --set ...`
- Marks a corpus **affected** when `moved>0`, `grade_changes>0`, `added_pids`, `removed_pids`, or `invariant_violations`
- Maps corpora → `rescore_all` shelf keys via config stems, category match, source-path match, and aliases (`hummus→hummus_shelfrel_002`, `cakes_hard_cookies↔cakes`, `snack_bars→snacks`)
- Lists unmapped moved corpora under `affected_no_config` (cheese, maadanim, milk, yogurt in the sample)
- Emits `affected_set.json` and a human summary
- Exit codes: **2** frozen/invariant, **1** non-frozen movement, **0** none

### Verification

**Sample report** (`shadow_20260615T155350Z`):
- 9 affected corpora, 5 `affected_shelves`, 2 `frozen_breaches` (milk, snack_bars)
- `frozen_touched=true`, **exit 2** ✓ (milk moved → frozen breach)

**Exit-code matrix:**
| Report | Verdict | Exit |
|--------|---------|------|
| `shadow_20260615T155350Z` | FROZEN_TOUCHED | 2 |
| `shadow_20260611T165734Z` | MOVEMENT | 1 |
| `shadow_20260611T165604Z` | CLEAN | 0 |

**End-to-end `--set`** (`BARI_GLASSBOX_W4=on`, ~3.1s): resolved report `shadow_20260617T153603Z`, 2 affected corpora → shelves `cereals`, `hummus_shelfrel_002`, exit 1.

### Files changed

| Path | Action |
|------|--------|
| `03_operations/page_generator/affected_set.py` | created |
| `03_operations/page_generator/outputs/affected_set_sample.json` | created |

**Verify at:**
- `affected_set.py:1` — module + CLI
- `affected_set.py:build_affected_set` — manifest schema
- `affected_set.py:compute_exit_code` — exit 0/1/2 logic
- `outputs/affected_set_sample.json:96` — `frozen_breaches: ["milk","snack_bars"]`

```json
{
  "task": "TASK-317",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/affected_set.py", "action": "created", "sha256": "CD6374B31F74FC7FAEBF125802927687535BFB27089A9765AA318964070F637D"},
    {"path": "03_operations/page_generator/outputs/affected_set_sample.json", "action": "created", "sha256": "27EC8347269130B8CF516DD906B06D84C7AA69D2101F8DFEB497D5C8F7665C7D"}
  ],
  "counts": {
    "affected_corpora_sample: 9/12 (shadow_report.json corpora with movement)",
    "affected_shelves_sample: 5/9 (mapped shelves for affected corpora)",
    "frozen_breaches_sample: 2/2 (frozen corpora that moved: milk, snack_bars)",
    "affected_no_config_sample: 4/9 (moved corpora without page_generator config)",
    "exit_code_frozen_sample: 2/1 (FROZEN_TOUCHED report → exit 2)",
    "exit_code_movement: 1/1 (MOVEMENT-only report → exit 1)",
    "exit_code_clean: 0/1 (CLEAN report → exit 0)",
    "e2e_runtime_sec: 3.1/1 (--set BARI_GLASSBOX_W4=on full diff)"
  },
  "commands_run": [
    {"cmd": "python C:\\Bari\\03_operations\\page_generator\\affected_set.py --report C:\\Bari\\03_operations\\shadow\\runs\\shadow_20260615T155350Z\\shadow_report.json --out C:\\Bari\\03_operations\\page_generator\\outputs\\affected_set_sample.json", "exit_code": 2},
    {"cmd": "python C:\\Bari\\03_operations\\page_generator\\affected_set.py --report C:\\Bari\\03_operations\\shadow\\runs\\shadow_20260611T165734Z\\shadow_report.json --out NUL", "exit_code": 1},
    {"cmd": "python C:\\Bari\\03_operations\\page_generator\\affected_set.py --report C:\\Bari\\03_operations\\shadow\\runs\\shadow_20260611T165604Z\\shadow_report.json --out NUL", "exit_code": 0},
    {"cmd": "python C:\\Bari\\03_operations\\page_generator\\affected_set.py --set BARI_GLASSBOX_W4=on --out C:\\Bari\\03_operations\\page_generator\\outputs\\affected_set_e2e.json", "exit_code": 1}
  ],
  "not_done": [],
  "self_check": "Sample report shadow_20260615T155350Z: milk moved=4 → frozen_touched=true, frozen_breaches=['milk','snack_bars'], exit=2 — observed exit 2 and frozen_touched=true in affected_set_sample.json"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
?? 03_operations/page_generator/outputs/brined_cheeses_generated_v2.json
?? 03_operations/page_generator/outputs/brined_cheeses_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cakes_generated_v2.json
?? 03_operations/page_generator/outputs/cakes_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cereals_generated_v2.json
?? 03_operations/page_generator/outputs/cereals_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cookies_coffee_generated_v2.json
?? 03_operations/page_generator/outputs/cookies_coffee_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/granola_generated_v2.json
?? 03_operations/page_generator/outputs/granola_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/hummus_generated_v2.json
?? 03_operations/page_generator/outputs/hummus_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/juices_generated_v2.json
?? 03_operations/page_generator/outputs/juices_generated_v2_gates_report.md
?? tasks/TASK-317.md
?? tasks/TASK-318.md
?? tasks/prompts/P167_affected_set.md
?? tasks/prompts/P168_copy_stage.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
```

### After dispatch

```
?? 03_operations/page_generator/affected_set.py
?? 03_operations/page_generator/outputs/affected_set_sample.json
?? 03_operations/page_generator/outputs/brined_cheeses_generated_v2.json
?? 03_operations/page_generator/outputs/brined_cheeses_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cakes_generated_v2.json
?? 03_operations/page_generator/outputs/cakes_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cereals_generated_v2.json
?? 03_operations/page_generator/outputs/cereals_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/cookies_coffee_generated_v2.json
?? 03_operations/page_generator/outputs/cookies_coffee_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/granola_generated_v2.json
?? 03_operations/page_generator/outputs/granola_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/hummus_generated_v2.json
?? 03_operations/page_generator/outputs/hummus_generated_v2_gates_report.md
?? 03_operations/page_generator/outputs/juices_generated_v2.json
?? 03_operations/page_generator/outputs/juices_generated_v2_gates_report.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
```

### Delta

### New / modified since dispatch
  ?? 03_operations/page_generator/affected_set.py
  ?? 03_operations/page_generator/outputs/affected_set_sample.json
### Removed / cleaned since dispatch
  ?? tasks/TASK-317.md
  ?? tasks/TASK-318.md
  ?? tasks/prompts/P167_affected_set.md
  ?? tasks/prompts/P168_copy_stage.md
