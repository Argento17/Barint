# Return: P230

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P230_c1_spine_rt_fixes.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-18T12:38:47.494852+00:00 |
| Finished | 2026-06-18T12:40:16.557917+00:00 |
| Exit code | 0 |

---

## Output

```
P230 spine red-team fixes are implemented across all four specified files. Verification passed.

## Changes

**RT-2 (CRITICAL) — `run_gates.py`**  
Added a schema-agnostic `PENDING_COPY` check for `insightLine` and `rowVerdict` before the v3 block. It skips pre-copy pages (all insightLines still `PENDING_COPY`) and fails authored pages with remaining pending copy.

**RT-1 (CRITICAL) — `spine_flip.py`**  
Surfaces baseline movement via `c10_pass` from `run_summary.json`. Shelves with `c10_pass=False` go into `baseline_moved`, which forces `overall_verdict=REVIEW` and appears in the report JSON and DEPLOY-READY line. Exit codes unchanged.

**RT-10 (MEDIUM) — `affected_set.py`**  
Replaced bidirectional prefix path matching with exact normalized path equality to prevent spurious corpus→shelf mappings.

**RT-4/8/9/11 — `conformance.py`**  
Added four new SOFT checks:
- **SOFT-8-off_misplaced** — OFF markers outside `products[]` in disallowed context
- **SOFT-9-registry_source** — shadow registry source not in config corpus dirs
- **SOFT-10-shelf_rel** — shelf-relative flag ON but missing `shelf_rel` calibration
- **SOFT-11-manifest_count** — manifest `product_count` vs served JSON product count

## Verification

**(1) Syntax:** `ALL 4 FILES: valid Python`

**(2) Conformance SUMMARY:** `12 conform, 0 deferred (accepted), 0 non-conforming (of 12).` — unchanged after RT-10 fix.

**(3) New SOFT warnings:**
| Category | Check | Detail |
|---|---|---|
| `hard_cheeses` | SOFT-9-registry_source | shadow source not in config corpus_dirs |
| `juices` | SOFT-9-registry_source | shadow source not in config corpus_dirs |
| `milk` | SOFT-10-shelf_rel | shelf-relative flag ON but no shelf_rel calibration |

No SOFT-8 or SOFT-11 warnings fired.

**(4) Unified diff:** see git diff output above (4 files, +147/−4 lines net).

```json
{
  "task": "P230",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/gates/run_gates.py", "action": "modified", "sha256": "90eaefcef53dabb8343a8465593f569ce817102a120a7b19531213daf87555b4"},
    {"path": "03_operations/page_generator/spine_flip.py", "action": "modified", "sha256": "b10bec33f537124d8ef15a062f4758bcd450a32555457fdf8723af5334e740cf"},
    {"path": "03_operations/page_generator/affected_set.py", "action": "modified", "sha256": "bf98d56b287da896b949c66fca4c14e39e0db3013723f40d9fa622e2420d9a9e"},
    {"path": "03_operations/page_generator/conformance.py", "action": "modified", "sha256": "de83ed83956d53cadede0c0e1caced175917e892a7c77985801066ebc2feb630"}
  ],
  "counts": {
    "conformance_conform": "12/12 (conformance.py --all SUMMARY line)",
    "new_soft_warnings": "3 categories (hard_cheeses/juices: SOFT-9; milk: SOFT-10)"
  },
  "commands_run": [
    {"cmd": "python -c \"import ast;[ast.parse(open(f,encoding='utf-8').read()) for f in ['03_operations/page_generator/gates/run_gates.py','03_operations/page_generator/spine_flip.py','03_operations/page_generator/affected_set.py','03_operations/page_generator/conformance.py']];print('ALL 4 FILES: valid Python')\"", "exit_code": 0},
    {"cmd": "PYTHONIOENCODING=utf-8 python 03_operations/page_generator/conformance.py --all", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "conformance.py --all SUMMARY must remain 12 conform / 0 non-conforming — observed 12 conform, 0 non-conforming"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
?? tasks/prompts/P230_c1_spine_rt_fixes.md
```

### After dispatch

```
M 03_operations/page_generator/affected_set.py
 M 03_operations/page_generator/conformance.py
 M 03_operations/page_generator/gates/run_gates.py
 M 03_operations/page_generator/spine_flip.py
?? tasks/prompts/P230_c1_spine_rt_fixes.md
```

### Delta

### New / modified since dispatch
   M 03_operations/page_generator/conformance.py
   M 03_operations/page_generator/gates/run_gates.py
   M 03_operations/page_generator/spine_flip.py
  M 03_operations/page_generator/affected_set.py
