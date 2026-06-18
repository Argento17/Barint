# Return: P161

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P161_hummus_tighten_dips_only.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-17T11:20:51.945472+00:00 |
| Finished | 2026-06-17T11:22:08.828337+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P161 task prompt and the return contract so I can execute it exactly.
Next I'll pull the config, staging rescored data, and live hummus page for comparison.
I'll scan the hummus corpus for prepared-spread markers and empty ingredient data to decide what to exclude.
Scan found six new exclusions; I'll verify `3643714` and update the config.
Rescore passed; next I'll pull top-5, grade distribution, and live-page diffs.
## P161 / TASK-306 — Hummus tighten to prepared-dips-only return

### Excluded barcodes (6 new; 12 total with P160)

| Barcode | Name | Reason | Ingredient evidence |
|---------|------|--------|---------------------|
| `208428` | חומוס שלם יכין | `out_of_scope: whole chickpeas, not a prepared dip` | Marketing copy only — no tahini/oil/seasoning; `ingredients_list` = Shufersal nutrition blurb, not a spread formula |
| `7290018359686` | הקיסר חומוס ענק | `out_of_scope: whole chickpeas, not a prepared dip` | Same — marketing/recipe copy (`הוסיפו מלח ופלפל`), no actual spread ingredients |
| `7296073733317` | חומוס | `out_of_scope: no ingredient data, cannot confirm prepared dip` | `ingredients_list: []`, `ingredients_text_he: null` |
| `7296073733348` | חומוס ענק | `out_of_scope: no ingredient data, cannot confirm prepared dip` | `ingredients_list: []`, `ingredients_text_he: null` |
| `1990261` | חומוס | `out_of_scope: no ingredient data, cannot confirm prepared dip` | `ingredients_list: []`, `ingredients_text_he: null` |
| `3643714` | חומוס | `out_of_scope: no ingredient data, cannot confirm prepared dip` | `ingredients_list: []`, `ingredients_text_he: null` |

**KEPT: 57** (all show tahini and/or oil and/or seasoning in ingredient data).

**Borderline flagged for human review: 0** — no ambiguous cases; every non-excluded product has clear spread markers.

### Re-score results

- **New product count:** 57 (was 63 post-P160; 6 additional exclusions)
- **Scored corpus:** 69 traces unchanged

**Grade distribution (57 products):** `{B:2, C:42, D:12, E:1}` — min=31.80, max=70.60, median=54.00, stdev=6.41, most_common=57 (×8)

**New top-5 (prepared dips):**

| Rank | Barcode | Grade | Score | Short ingredients |
|------|---------|-------|-------|-------------------|
| 1 | `7296073725404` | B | 70.6 | חומוס מבושל + טחינה גולמית 31% |
| 2 | `6666307` | B | 67.7 | גרגירי חומוס, טחינה, שומשומין, תבלינים |
| 3 | `7296073725565` | C | 58.4 | חומוס מבושל + טחינה 15% + שמן סויה |
| 4 | `7296073725589` | C | 58.4 | חומוס מבושל + טחינה 15% + שמן סויה |
| 5 | `6666444` | C | 58.0 | ירקות, שמן, תבלינים |

Top is now `7296073725404` (חומוס מסעדות) — tahini-bearing spread. Canned/raw chickpeas and empty-ingredient products are gone from the top.

### Products needing fresh copy (grade change vs live)

| Barcode | Name | Live → Staging |
|---------|------|----------------|
| `7290106577572` | מטבוחה אמיתית | C → D |
| `7290106577480` | חציל על האש בטחינה | C → E |

No kept products are new vs live (all 57 were already on `hummus_frontend_v5.json`).

### Gate results

| Gate | Result |
|------|--------|
| **G8 DATA-SANITY** | PASS |
| **C10 milk Δ** | PASS (20/20, delta=0.0) |
| **OFF** | 0 |
| **score==trace** | OK (0 mismatches) |
| **Overall gate** | PASS (exit 0) |

### Files changed

1. `03_operations/page_generator/configs/hummus_shelfrel_002.json` — added 6 exclusions (lines 44–49)
2. `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` — regenerated staging page (57 products)
3. `_rescore_staging/hummus_shelfrel_002/verification_table.csv` — verification artifact (unchanged from P160 run)

### Verify at

- `03_operations/page_generator/configs/hummus_shelfrel_002.json:37-49` — 12 exclusions total
- `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` — 57 products; top barcode `7296073725404` grade B
- `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored_gates_report.md:17` — G8 PASS

**Proposed status: RETURNED** (orchestrator closes after verification)

```json
{
  "task": "TASK-306",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/configs/hummus_shelfrel_002.json", "action": "modified", "sha256": "8043d6b278d9bb07af6ebaef8a44ab72767f0f9b6fff27f0541b712993e12d93"},
    {"path": "_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json", "action": "modified", "sha256": "77a824c3afd40239005421a45d81bbb51b2e9129bffec2d11199ddc432cd688f"},
    {"path": "_rescore_staging/hummus_shelfrel_002/verification_table.csv", "action": "modified", "sha256": "d842e1fda41b502d5d4a710cc436c261691d67a0668d4567d337f7f06ef50e1f"}
  ],
  "counts": {
    "excluded_p161": "6/63 (canonical_bsip1 scan post-P160 exclusions)",
    "excluded_total": "12/69 (hummus_shelfrel_002.json exclusions[])",
    "kept_products": "57/69 (hummus_shelfrel_002_rescored.json products[])",
    "grade_dist": "n=57 min=31.80 max=70.60 median=54.00 stdev=6.41 most_common=57(8) grade_dist={B:2,C:42,D:12,E:1} (_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json)",
    "copy_needs_grade_change": "2/57 (7290106577480 C->E, 7290106577572 C->D vs hummus_frontend_v5.json)",
    "borderline_flagged": "0/63 (corpus scan)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/rescore_all.py --shelf hummus_shelfrel_002", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "G8 PASS + C10 milk Δ0 + OFF=0 + score==trace OK; top product 7296073725404 (B/70.6) has טחינה גולמית 31% — prepared dip, not whole chickpeas"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 03_operations/page_generator/configs/hummus_shelfrel_002.json
 M tasks/DISPATCH_BOARD.md
?? tasks/TASK-306.md
?? tasks/TASK-307.md
?? tasks/closed/TASK-303.md
?? tasks/closed/TASK-304.md
?? tasks/closed/TASK-305.md
?? tasks/prompts/P160_hummus_curation.md
?? tasks/prompts/P161_hummus_tighten_dips_only.md
?? tasks/returns/P160_return.md
```

### After dispatch

```
M 03_operations/page_generator/configs/hummus_shelfrel_002.json
 M tasks/DISPATCH_BOARD.md
?? tasks/TASK-306.md
?? tasks/TASK-307.md
?? tasks/closed/TASK-303.md
?? tasks/closed/TASK-304.md
?? tasks/closed/TASK-305.md
?? tasks/prompts/P160_hummus_curation.md
?? tasks/prompts/P161_hummus_tighten_dips_only.md
?? tasks/returns/P160_return.md
```

### Delta

*(no changes detected)*
