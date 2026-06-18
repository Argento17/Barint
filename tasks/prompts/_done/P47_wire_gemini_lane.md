# P47 / Wire the C1-GEMINI lane into the router (route: C1-CURSOR)

**➡️ Cursor task — extend `03_operations/router/dispatch.py` to add a Gemini CLI lane, mirroring the existing Cursor lane.**

---

TASK: Add a new execution lane **C1-GEMINI** (Google Gemini CLI) to
`03_operations/router/dispatch.py`, structurally mirroring the existing Cursor lane.
Do not change the Cursor, C2/opencode, or native-C1 behavior — additive only.

VERIFIED FACTS (use exactly):
- The Gemini CLI is installed. Subprocess entry point: `C:\Users\HP\AppData\Roaming\npm\gemini.cmd`
  (resolve it like the Cursor lane resolves its cmd: a module-level constant with a
  `shutil.which("gemini")` fallback; raise a clear error if not found).
- Working headless invocation (verified): `gemini.cmd --skip-trust -p "<message>"`.
  **Flag order matters: `--skip-trust` MUST precede `-p <message>`** (anything after `-p` is
  treated as the prompt). The CLI prints the answer to stdout; it also prints harmless
  warnings to stderr (256-color, ripgrep) — capture stdout as the result and append stderr
  for debugging, same as the Cursor lane.

WHAT TO ADD (mirror the Cursor lane's three pieces + route parsing):
1. `run_via_gemini_cli(message: str, timeout: int) -> tuple[int, str]` — mirror
   `run_via_cursor_cli`: build `[gemini_cmd, "--skip-trust", "-p", message]`, run via
   `subprocess.run` with `cwd=REPO_ROOT`, `capture_output=True`, `text=True`,
   `encoding="utf-8"`, `errors="replace"`, `timeout=timeout`, `shell=False`. Combine
   stdout + stderr like the Cursor lane. Reuse the same quota/limit detection pattern
   (`_looks_like_quota_exhaustion`) so an exhausted-quota return becomes exit 75 + the
   "LANE DOWN → reroute to native C1" banner (gemini quota strings to also match:
   "RESOURCE_EXHAUSTED", "quota", "429").
2. A resolver `find_gemini_cmd() -> Path` (or a module constant + which-fallback) for the
   `.cmd` path above.
3. Route parsing: extend `parse_route` to also accept `C1-GEMINI` (return it). Extend the
   main dispatch (`cmd_dispatch`) so `route == "C1-GEMINI"` calls a new `_dispatch_gemini(...)`
   that mirrors `_dispatch_cursor` (strip-owner-meta is already shared via the bootstrap;
   use the same prompt-bootstrap path the Cursor lane uses; write the same return file +
   board tick).
4. A `--selftest-gemini` CLI flag + `cmd_selftest_gemini(timeout)` mirroring
   `cmd_selftest_cursor`: send the PONG message through `run_via_gemini_cli`, PASS if
   "PONG" appears in the output.
5. Update the module docstring's lane list + usage examples to include C1-GEMINI and
   `--selftest-gemini`.

CONSTRAINTS:
- Additive only — Cursor / opencode / native-C1 paths byte-unchanged in behavior.
- stdlib only (subprocess, shutil, pathlib) — no new imports beyond what dispatch.py uses.
- No OFF (Open Food Facts) anything. Do not touch any file other than dispatch.py.

ACCEPTANCE: `python 03_operations/router/dispatch.py --selftest-gemini` runs and prints a
PASS with PONG received; `--selftest-cursor` and `--selftest` still work unchanged; a prompt
whose title carries `(route: C1-GEMINI)` would route to the gemini lane (you can show the
parse, no need to dispatch a real one).

RETURN: the diff summary (functions added, lines touched); the `--selftest-gemini` output;
confirmation `--selftest-cursor` still parses/runs; stdlib-only confirmation. End with the
machine-readable JSON return contract (`01_framework/operations/return_contract_v1.md`);
counts must include `lane_added: "C1-GEMINI"`, `files_touched: 1`, `selftest_gemini_pass`,
`cursor_lane_unchanged: true`, `new_deps: 0`. Propose RETURNED — do not write CLOSED; the
orchestrator verifies and closes.
