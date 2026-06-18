# Return: P232

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P232_c1_spine_rt_pass2.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-18T12:45:38.210963+00:00 |
| Finished | 2026-06-18T12:49:07.806267+00:00 |
| Exit code | 0 |

---

## Output

```
## P232 — Spine red-team fixes PASS 2 (RETURNED)

Implemented all four C3-blessed fixes. Summary below with verification evidence.

---

### RT-5 — Pinned shelf stats in shadow diff

**Changes:** `lookup_shelf_rel()`, `_inject_shelf_stats()`, `score_corpus(..., shelf_rel=)` wired in `cmd_baseline` and `cmd_diff`.

**Verify — baseline runs (shelf-relative corpora):**
```
  cakes                  [published] n=167 errors=0
  brined_cheeses         [published] n= 48 errors=0
  cheese                 [published] n= 59 errors=0
```

**Score parity (cakes, shelf-relative vs live frontend — 10/10 sampled barcodes exact):**
```
7290119030095: shadow=50.5/C live=50.5/C
7296073346340: shadow=37.0/D live=37.0/D
5718021: shadow=32.2/E live=32.2/E
7290119045013: shadow=32.0/E live=32.0/E
7290016162264: shadow=32.0/E live=32.0/E
5431920: shadow=30.6/E live=30.6/E
7290006983787: shadow=30.4/E live=30.4/E
5431913: shadow=28.0/E live=28.0/E
4504670: shadow=26.4/E live=26.4/E
2472261: shadow=26.2/E live=26.2/E
```

---

### RT-6 — Registry source = live corpus (+ multi-source)

| Corpus | Registry `source` change | load_batch |
|---|---|---|
| **hard_cheeses** | `02_products/hard_cheeses/bsip1_outputs` | 66 products |
| **juices** | `02_products/juices/bsip1_outputs` | 33 products |
| **cookies_coffee** | `[run_cookies_001/output, run_cakes_001/output]` | 61 + 167 |
| **granola** | **DECLINED** — config `corpus_dirs` is already `run_cereals_005/output` (66 products); registry matched. `run_cereals_008` is the BSIP2 trace run, not the BSIP1 corpus source. |

**Verify — SOFT-9 on drifted categories:**
```
hard_cheeses: PASS soft SOFT-9-registry_source   all registry sources referenced by config corpus_dirs
juices:       PASS soft SOFT-9-registry_source   all registry sources referenced by config corpus_dirs
```

---

### RT-3 — Onboard reproduce-check

After conformance passes, `onboard_category.py` runs `shadow_backtest.py diff --corpus <name>` and hard-fails on moves > 0.

**Verify — `onboard_category.py --slug juices`:**
```
shadow reproduce-check: 0 score moves on corpus 'juices'

CONFORMS: this category will re-flow correctly on a score-flip.
```

---

### RT-7 — SOFT-12 calibration drift guardrail

Added `SOFT-12-calibration_drift` (warn if `|current - calibration_n|/calibration_n > 0.25`; skip when `calibration_n` absent). Created `03_operations/page_generator/configs/SHELF_REL_RECALIBRATION_POLICY.md`.

**Verify:** SOFT-12 fires nowhere (expected — no configs have `calibration_n` yet).

---

### Final verification

```
valid
```
```python
python -c "import ast;[ast.parse(open(f,encoding='utf-8').read()) for f in ['03_operations/bsip2/proto_v0/src/shadow_backtest.py','03_operations/page_generator/onboard_category.py','03_operations/page_generator/conformance.py']];print('valid')"
```

```
SUMMARY: 12 conform, 0 deferred (accepted), 0 non-conforming  (of 12).

All non-deferred categories will re-flow correctly on a score-flip.
```

**Note:** `cakes` stem still shows a SOFT-9 warn for `cookies_coffee`'s `run_cookies_001` source because that corpus maps to the cakes shelf via shared `run_cakes_001`. The `cookies_coffee` stem itself passes SOFT-9. Task-required drifts (hard_cheeses, juices) are cleared.

---

### Files changed

| File | Action |
|---|---|
| `03_operations/bsip2/proto_v0/src/shadow_backtest.py` | modified |
| `03_operations/page_generator/affected_set.py` | modified |
| `03_operations/page_generator/conformance.py` | modified |
| `03_operations/page_generator/onboard_category.py` | modified |
| `03_operations/shadow/shadow_registry_v1.json` | modified |
| `03_operations/page_generator/configs/SHELF_REL_RECALIBRATION_POLICY.md` | created |

Unified diff is in `git diff` output above (6 files).

---

```json
{
  "task": "P232",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/shadow_backtest.py", "action": "modified", "sha256": "5e8304ec9d7acc0d6cd63a18b0393fc3a7fdf43957c1ddb96b5c21813ae38ba8"},
    {"path": "03_operations/page_generator/affected_set.py", "action": "modified", "sha256": "36294b062ac3f9cc924bf8afa620d6e21ba17f8c208bab6c22a4cee7a52cac62"},
    {"path": "03_operations/page_generator/conformance.py", "action": "modified", "sha256": "d2de9fed30f36a321f4cb29abf780d8e91dbb8df922b5f74619e20229bbc93ce"},
    {"path": "03_operations/page_generator/onboard_category.py", "action": "modified", "sha256": "18d4d46de3373c8917f68c68f49a219bf6719eb0631aedcc01724e68e216d8c8"},
    {"path": "03_operations/shadow/shadow_registry_v1.json", "action": "modified", "sha256": "13576fd3d2152cc64d78b71dd85a23ecfeeb95e7842305484fc428ed7fe0a5ef"},
    {"path": "03_operations/page_generator/configs/SHELF_REL_RECALIBRATION_POLICY.md", "action": "created", "sha256": "65ab05837bb437e712166edceea75d47c681b0ef40a79e2ccb9afa9dbdb4ec59"}
  ],
  "counts": {
    "conformance_summary": "12/12 conform, 0/12 non-conforming (conformance.py --all)",
    "soft9_hard_cheeses": "PASS (conformance.py --slug hard-cheeses)",
    "soft9_juices": "PASS (conformance.py --slug juices)",
    "soft12_fired": "0/12 categories (calibration_n absent everywhere)",
    "cakes_score_parity_sample": "10/10 exact score+grade match vs cakes_hard_cookies_frontend_v1.json",
    "registry_load_batch_hard_cheeses": "66/66 (load_batch on bsip1_outputs)",
    "registry_load_batch_juices": "33/33 (load_batch on bsip1_outputs)",
    "registry_load_batch_cookies_coffee": "228 raw across 2 dirs, deduped in score_corpus",
    "onboard_juices_reproduce_moves": "0/33 products moved (shadow diff --corpus juices)"
  },
  "commands_run": [
    {"cmd": "python -c \"import ast; ...\"; print('valid')", "exit_code": 0},
    {"cmd": "PYTHONIOENCODING=utf-8 python 03_operations/page_generator/conformance.py --all", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/shadow_backtest.py baseline --corpus cakes", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/shadow_backtest.py baseline --corpus brined_cheeses --corpus cheese", "exit_code": 0},
    {"cmd": "PYTHONIOENCODING=utf-8 python 03_operations/page_generator/onboard_category.py --slug juices", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "conformance.py --all must stay 12 conform / 0 non-conforming; observed SUMMARY: 12 conform, 0 deferred, 0 non-conforming (of 12)"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
?? tasks/prompts/P230_c1_spine_rt_fixes.md
?? tasks/prompts/P232_c1_spine_rt_pass2.md
?? tasks/returns/P230_return.md
```

### After dispatch

```
M 03_operations/bsip2/proto_v0/src/shadow_backtest.py
 M 03_operations/page_generator/affected_set.py
 M 03_operations/page_generator/conformance.py
 M 03_operations/page_generator/onboard_category.py
 M 03_operations/shadow/shadow_registry_v1.json
?? 03_operations/page_generator/configs/SHELF_REL_RECALIBRATION_POLICY.md
?? tasks/prompts/P230_c1_spine_rt_fixes.md
?? tasks/prompts/P232_c1_spine_rt_pass2.md
?? tasks/returns/P230_return.md
```

### Delta

### New / modified since dispatch
   M 03_operations/page_generator/affected_set.py
   M 03_operations/page_generator/conformance.py
   M 03_operations/page_generator/onboard_category.py
   M 03_operations/shadow/shadow_registry_v1.json
  ?? 03_operations/page_generator/configs/SHELF_REL_RECALIBRATION_POLICY.md
  M 03_operations/bsip2/proto_v0/src/shadow_backtest.py
