# P554 / TASK-554 return — CI hardening

## Summary
Closed four audit gaps in CI wiring on branch `task554-ci-hardening`:

1. **shadow_gate.yml** — added `push: [master]` with the same path filter as PR (YAML anchor `&engine_paths` / `*engine_paths`).
2. **barint_ci.yml** — removed dead `argento_bari_ci.yml` path reference; added `e2e-smoke` job (build → Playwright chromium → `test:e2e` + `test:a11y`).
3. **playwright.config.ts** — CI uses `npm run start`; local dev unchanged.
4. **bari_page_gates.yml** — ported from untracked local copy (conformance sweep + OFF census).

## Verification
| Check | Result |
|-------|--------|
| YAML parse (3 workflows) | PASS |
| `npm run build` (bari-web) | exit 0 |
| `npm run test:e2e` CI=true mobile | 5/5 PASS |
| `npm run test:a11y` CI=true mobile | 2/4 PASS — **2 FAIL pre-existing** hero eyebrow `text-[#1F8F6A]/80` contrast on `/hashvaot/breakfast-cereals` + `/hashvaot/hummus` (TASK-510 fix on `fix/task510-hero-contrast`, not master). Out of TASK-554 DoD ("no other files touched"). **Expect e2e-smoke job red on a11y step until TASK-510 merges or owner accepts.** |
| argento reference in barint_ci | removed (0 matches) |

## not_done
- Branch protection / required checks on origin master (manual owner step per task).
- Drop argento from local `task506` before merge (follow-up on that branch).
- Middle gates in CI (explicit out-of-scope).

## Proposed status: RETURNED (CI wiring complete; a11y step surfaces pre-existing contrast debt)

```json
{
  "task": "TASK-554",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": ".github/workflows/shadow_gate.yml", "action": "modified", "sha256": "2dba51a429ea37cd0eec489f6368fd9471b362adcd435e37c8faee36c958e791"},
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "ebc4a5f4e1e8946243df15b48b9c7ec16c4a0057445fdef845d76fb30c8dae3f"},
    {"path": ".github/workflows/bari_page_gates.yml", "action": "created", "sha256": "15b8b4b20dd3862f1382bab04cf476aa40bdaa3f2406a9871fff2874242a381b"},
    {"path": "bari-web/playwright.config.ts", "action": "modified", "sha256": "eabc6e2b08c0473dde82a0c7cbee61eaca13f7d087b37a4ce4cc73a48af4f3a2"}
  ],
  "counts": {
    "workflow_files_touched": "4/4 (TASK-554 scope)",
    "yaml_parse_pass": "3/3 (barint_ci, shadow_gate, bari_page_gates)",
    "smoke_e2e_pass_mobile_ci": "5/5 (playwright smoke.spec.ts, CI=true)",
    "a11y_e2e_pass_mobile_ci": "2/4 (playwright a11y.spec.ts; 2 pre-existing contrast FAILs on category hero eyebrow)"
  },
  "commands_run": [
    {"cmd": "python -c import yaml; parse 3 workflows", "exit_code": 0},
    {"cmd": "npm run build (bari-web)", "exit_code": 0},
    {"cmd": "CI=true npm run test:e2e -- --project=mobile (bari-web)", "exit_code": 0},
    {"cmd": "CI=true npm run test:a11y -- --project=mobile (bari-web)", "exit_code": 1}
  ],
  "not_done": [
    "Branch protection + required checks on Argento17/Barint master (owner manual)",
    "Remove argento_bari_ci.yml reference from local task506 branch before that branch merges",
    "TASK-510 hero contrast fix needed for green a11y CI (pre-existing, out of scope)"
  ],
  "self_check": "Four workflow/config files changed only; shadow_gate has push:master with engine path filter; barint_ci has e2e-smoke job and no argento path; playwright uses start in CI — observed PASS on build + smoke; a11y fails on known pre-existing contrast (documented)."
}
```
