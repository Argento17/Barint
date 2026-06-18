# P70 — Cookies run #7: OFF-ban sweep + artifact inventory (route: C2)

ROUTE: C2 (DeepSeek). This is MECHANICAL grunt work: grep + count + list. No judgment, no scoring, no
copy, no file edits. Produce a report only. Read this whole file top-to-bottom; all instructions are here.
End with the return-contract JSON block exactly as specified at the bottom.

## TASK-275 (factory run #7, cookies-coffee). Repo root: C:\Bari

## What to do — two mechanical passes

### Pass 1 — OFF-ban sweep (hard launch-gate check; OFF must be 0 everywhere)
Search these paths for any Open Food Facts marker. Markers (case-insensitive):
`openfoodfacts`, `open_food_facts`, `off.net`, `world.openfoodfacts`, `off_source_used":true`, `"off_used":` (report its value).
Paths to sweep (recurse):
- `02_products/cookies_coffee/`  (all: bsip0_outputs, methodology, factory_run_001)
- `03_operations/bsip0/raw_store/shufersal/cookies_coffee/`
- `03_operations/bsip0/scrape/shufersal_cookies_coffee/`
- `03_operations/bsip1/run_cookies_001/`  (may not exist yet — if absent, say so, don't fail)
- `02_products/cookies_coffee/bsip2_outputs/run_cookies_001/`  (may not exist yet — if absent, say so)
Report: for EACH path, the file count scanned and the number of OFF-marker hits. For any hit: print
file:line + the matching text. The expected result is ZERO hits and every `off_source_used` / `off_used`
value = false/0. Use ripgrep if available, else python `os.walk` + substring scan.

### Pass 2 — Artifact inventory (count + list, no judgment)
- `cookies_coffee/bsip0_outputs/` : list files; report the raw JSON product count (len of the array in
  `cookies_coffee_bsip0_raw_20260613T163431.json`).
- `raw_store/shufersal/cookies_coffee/` : count banked HTML files (per-code subfolders) AND count lines in
  `manifest.jsonl`. Report both numbers and whether they match.
- `factory_run_001/corpus_filter.json` : report the 3 bucket counts (IN_SCORED / TRANSPARENCY_NULL /
  OUT_OF_SCOPE) and their sum.
- `cookies_coffee/methodology/` : list the .md files present.

## Guards
- Do NOT modify any file. Read/grep/count only.
- Do NOT invent or infer data. If a path is absent, report "absent" — never fabricate counts.
- Use absolute paths under C:\Bari. Run real commands; paste the command + its real output.

## Return — end with EXACTLY this JSON (machine-readable return contract)
```json
{"task":"P70","proposed_status":"RETURNED",
 "artifacts":[],
 "counts":{"off_hits_total":"N","off_source_used_true":"N","bsip0_products":"N","raw_html_files":"N","manifest_lines":"N","html_manifest_match":"yes/no","corpus_in_scored":"N","corpus_null":"N","corpus_out":"N","corpus_sum":"N"},
 "commands_run":[{"cmd":"...","exit_code":0}],
 "not_done":[],
 "self_check":"OFF sweep = N hits across M files scanned; inventory counts reported from real command output, not fabricated"}
```
Do NOT close — propose RETURNED. The orchestrator verifies.
