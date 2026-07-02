# P465 / TASK-462 CI green sweep, part 2: ESLint exit 0 in bari-web (route: C1-CURSOR)

## 1. Context / baseline
- You are ALREADY in isolated worktree `C:\bari_wt_t462b`, branch `ci/task462-green-eslint`, cut from origin/master `b632f9c6`. Repo root = this worktree. Never touch `C:\Bari`. Commit here; NO push/PR/deploy. Run `npm ci` in `bari-web\` first (no node_modules here yet).
- The `frontend` job of `.github/workflows/barint_ci.yml` fails on the ESLint step (`npm run lint` in `bari-web/`) on every PR and master push. Build and corpus validation PASS — lint is the only red step. Error classes seen in CI run 28601493400: `@typescript-eslint/no-explicit-any`, `@typescript-eslint/no-this-alias`, `react/no-unescaped-entities` (unescaped `'` / `"` in JSX), and React correctness errors ("Cannot access refs during render", "Calling setState synchronously within an effect can trigger cascading renders").

## 2. Objective — `npm run lint` exit 0, behavior-preserving
Run `npm run lint` in `bari-web\`, enumerate EVERY error (report the full count by rule), then fix minimally:
- `react/no-unescaped-entities`: escape the character with the HTML entity (`&apos;`, `&quot;`, etc.). The RENDERED text must be byte-identical — you are changing encoding, never wording.
- `@typescript-eslint/no-explicit-any`: give the correct concrete type where it is locally obvious from usage; otherwise `unknown` + narrowing. Zero runtime-behavior change.
- `@typescript-eslint/no-this-alias`: refactor to arrow function / direct `this` only if trivially safe; otherwise targeted disable (below).
- React correctness errors (refs-during-render, setState-in-effect): fix ONLY when the fix is small, local, and provably behavior-preserving (e.g. moving a ref read into an event handler/effect). If a real refactor would be needed, add a targeted `// eslint-disable-next-line <rule> -- TASK-462: pre-existing, needs dedicated fix` and LIST every such disable in the return — these become tracked debt, not silent suppressions.
- Do NOT edit `eslint.config.mjs` to turn rules off globally. Do NOT reformat unrelated code.

Gates (all in `bari-web\`, all must be in the return with exit codes):
1. `npm run lint` exit 0.
2. `npx tsc --noEmit` exit 0.
3. `npm run build` exit 0 (route list unchanged vs a pre-change build — capture both).
4. `git diff --stat` touches only files that had lint errors.

## 3. Boundaries
- **FREEZE (HARD):** an owner project is rewriting product descriptions. Do not change ANY consumer-visible wording — rowVerdict/insightLine/expansion strings, page prose, headings. Entity-escaping that renders identically is the ONLY permitted touch inside consumer strings. If a lint fix would force a wording change: targeted disable instead.
- OFF ban absolute — no data sourcing of any kind (this is a lint task; you should need no data).
- No dependency changes (package.json/lock untouched). No push/PR/deploy.
- You are the EXECUTOR of this task. Do NOT spawn any subagents; do every step yourself with your own tools.

## 4. Return
Write to `tasks\returns\P465_contract.md` (NOT P465_return.md — the router overwrites that path): error census by rule (before), fix census by strategy (typed / escaped / refactored / disabled-with-tag, counts + denominators), every eslint-disable added (file:line + rule), the 4 gate outputs with exit codes, real sha256 for every touched file. Full Return Contract v1 JSON. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P465_contract.md --root C:\bari_wt_t462b` exit 0 (PowerShell, not Git Bash). Commit code + contract. Leave tree clean. Propose RETURNED.
