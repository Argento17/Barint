# P71 — run_cookies_001: verify + routing/cap diagnostic (route: C2)

ROUTE: C2 (DeepSeek). MECHANICAL: parse 61 JSON traces, tally, no judgment, no edits. Read whole file.
End with the return-contract JSON exactly as specified at the bottom.

## TASK-275. Repo root: C:\Bari
Traces dir: `02_products/cookies_coffee/bsip2_outputs/run_cookies_001/products/` (61 subdirs, each has `bsip2_trace.json`).
Per trace, the fields you need: `grade_estimate`, `final_score_estimate`, `category` (the ROUTED category),
`context_flag`, and somewhere in the trace the binding cap + red-label info (search keys containing
`binding_cap`, `red_label`, `ISRAELI_RED_LABEL`, `caps`). Also check `off_used` / `off_source_used`.

## Produce these tallies (all from the 61 traces — paste real command output)
1. **Grade distribution**: count of A / B / C / D / E. (Expected from P68: A0 B0 C13 D15 E33 — confirm or correct.)
2. **Score stats**: min, max, median, mean, stdev, and the most-common score + its count.
3. **OFF**: count traces with `off_used`/`off_source_used` = true (expected 0).
4. **brined_food**: count traces with `context_flag == "brined_food"` (expected 0).
5. **ROUTING TALLY (key diagnostic)**: count of each distinct `category` value across the 61 traces
   (e.g. snack_bar_granola: N, cracker: N, bread: N, whole_food_fat: N, ...). This shows what lens each
   cookie was scored under.
6. **Binding-cap histogram**: for each trace, find the binding cap (the cap that set the final score, or the
   lowest cap applied) and tally how many traces are bound by each cap value/name. If the trace exposes a
   list of fired caps, report the most-common fired cap names + counts.
7. **2+ red labels**: count traces that fired 2 or more Israeli red labels (sugar + sat-fat etc.) — i.e. the
   `ISRAELI_RED_LABELS_2_PLUS` cap (45) or equivalent. Report how many of the 61.
8. **Cross-table**: grade distribution split BY routed category (e.g. of the 20 snack_bar_granola, how many
   E vs D vs C). This isolates whether one routed category is driving the E-cluster.

## Guards
- Read-only. Do not modify traces or any file. Do not infer — report only what the JSON contains.
- Use absolute paths under C:\Bari. Python `os.walk`/`glob` + `json.load`. Paste commands + real output.

## Return — end with EXACTLY this JSON
```json
{"task":"P71","proposed_status":"RETURNED","artifacts":[],
 "counts":{"grade_A":"N","grade_B":"N","grade_C":"N","grade_D":"N","grade_E":"N","score_min":"N","score_max":"N","score_median":"N","score_stdev":"N","most_common_score":"N(xK)","off_true":"N","brined_food":"N","two_plus_red_labels":"N"},
 "routing_tally":{"snack_bar_granola":"N","cracker":"N","bread":"N","whole_food_fat":"N","...":"N"},
 "binding_cap_histogram":{"<cap>":"N"},
 "grade_by_category":{"snack_bar_granola":{"E":"N","D":"N","C":"N"},"...":{}},
 "commands_run":[{"cmd":"...","exit_code":0}],
 "not_done":[],"self_check":"all tallies from 61 traces via real command output; P68 distribution confirmed/corrected"}
```
Do NOT close — propose RETURNED.
