# P500 / C3 independent challenge — supplement guides re-direction (route: C3)

## 1. Context
Repo: C:\Bari (read-only for you — you are a challenger, you build nothing, you close
nothing). Task: TASK-504. The owner has directed a strategic re-direction of Bari's
supplement product surface, and standing policy requires an independent C3 challenge
before a strategy fork of this size is executed.

Read FIRST: `C:\Bari\01_framework\product\supplement_guides_redirection_brief_v1.md`
(the full brief). Background if needed: `03_operations/reports/content/creatine_page_model_decision_v1.md`
(the no-grade ruling for creatine), `bari-web/src/lib/comparisons/magnesium-page-data.ts`
and `creatine-page-data.ts` (the two live supplement pages' data).

Summary of the fork: Bari currently ships supplement COMPARISON pages (magnesium =
scored + ranked; creatine = grade-free but comparison-framed). Owner verdict: ranking
supplements does not work, including doubts about magnesium's ranking. Direction:
retire supplement rankings, launch a new "מדריכים" (Guides) category — detailed
educational guide + attribute-level product assessment (dose adequacy, chemical
form/absorption, third-party verification, price-per-effective-unit), verdict-per-
attribute (pass/flag/fail), an UNORDERED shortlist of products clearing all bars,
worldwide-benchmark placement, pricing, and a plain buy button (no affiliate params in
v1).

## 2. Objective
Challenge the strategy INDEPENDENTLY. Specifically:
1. Is retiring supplement rankings the right call, or does it abdicate Bari's core job
   (clarity/verdict)? Steelman the case FOR keeping some ranking.
2. Is "guides" the right product form? Propose the strongest ALTERNATIVE shape you can
   construct (e.g., different IA, different verdict mechanism, different naming).
3. Attack the unordered-shortlist idea: does it secretly re-create a ranking (in-or-out
   is binary rank), and is that honest?
4. Attack the buy-button plan vs Bari's independence positioning: is the proposed
   mitigation (disclosure + buttons-for-all-passing + data separation) sufficient, or
   structurally naive?
5. The magnesium question: form-tier bands + UL flags retained as verdicts vs going
   fully flat — which is more defensible publicly, and why?
6. Name the single strongest argument AGAINST the whole re-direction, and the failure
   mode most likely to actually happen.

## 3. Boundaries
- Advice only. You never write files into the repo, never close tasks, never build.
- No new data collection; reason from the brief + named artifacts.
- OFF (Open Food Facts) is banned project-wide; if any suggestion of yours would rely
  on OFF data, drop it.

## 4. Return format
A structured challenge memo: numbered responses to the 6 objectives, each with a clear
position + reasoning; then "STRONGEST OBJECTION" and "MOST LIKELY FAILURE MODE"
sections; then a one-paragraph overall verdict (support / support-with-changes /
oppose) on the re-direction as specced.

## 5. Return contract
End with the machine-readable JSON block per
`C:\Bari\01_framework\operations\return_contract_v1.md`:
{"task": "TASK-504", "proposed_status": "RETURNED", "artifacts": [], "counts": {...},
"commands_run": [], "not_done": [...], "acceptance_test": "..."}
Do not close — propose RETURNED.
