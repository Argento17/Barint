(route: C2)

# P233 — Gold Set Phase 0: mechanical candidate extraction from the APPROVED Shadow baseline (TASK-349)

You are C2 (mechanical, ZERO-INFERENCE). Do exactly the steps below. Do not decide anything,
do not judge product quality, do not pick "best" anything by meaning — only sort by the numeric
`score` field and slice. If a step is ambiguous, STOP and say so rather than guessing.

## Repo / paths
- Repo root: `C:\Bari`
- INPUT (read-only, committed): `C:\Bari\03_operations\shadow\baselines\approved\baseline_20260616T052730Z.json`
  - Structure: top-level `corpora` is an object keyed by corpus name. Each corpus has a `products`
    object keyed by product id (pid). Each product snapshot has fields: `name`, `cat`, `subtype`,
    `nova`, `score` (number or null), `grade` (S/A/B/C/D/E or null), `ds`, and `dims` (object of 10
    dimension scores: processing_quality, nutrient_density, calorie_density, glycemic_quality,
    protein_quality, additive_quality, satiety_support, fat_quality, regulatory_quality,
    whole_food_integrity).

## Objective (read TASK-349 first)
Produce a compact, mechanical map of the scored corpus so a later step can hand-pick gold anchors.
For EACH corpus in the baseline:
1. **Grade distribution** — count of products at each grade S/A/B/C/D/E and `null`. Counts must sum
   to the corpus product total; report the total too.
2. **Top 5 by score** — the 5 products with the highest numeric `score` (descending). For each:
   pid, name, score, grade. Skip products whose `score` is null (note how many were skipped).
3. **Bottom 5 by score** — the 5 lowest numeric `score` (ascending). Same fields.
Then a final **corpus summary table**: corpus, n, min score, max score, and the most-common grade
with its count.

## Boundaries / guards
- READ-ONLY. Do not edit any repo file, do not run git, do not change scores.
- OFF ban: do not introduce or reference Open Food Facts data anywhere.
- Use only the numeric `score` field for ordering. Do NOT infer quality from names or dimensions.
- Output goes in your return text only (a markdown table). Do not write files in the repo.

## Return format
Markdown sections per corpus (grade dist + top5 + bottom5) + the final summary table, then the
machine-readable return contract JSON below. Counts must be derived from the file, and name the
denominator (e.g. `milk grade_dist sums to 18/18`).

## Do not close — propose RETURNED.

```json
{
  "task": "P233",
  "proposed_status": "RETURNED",
  "artifacts": [],
  "counts": {"<corpus>_total": "N/N (baseline products)"},
  "commands_run": [{"cmd": "<how you parsed the json>", "exit_code": 0}],
  "not_done": [],
  "self_check": "grade_dist per corpus sums to that corpus product total: <observed>"
}
```
