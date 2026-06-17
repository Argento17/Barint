# Return: P160

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P160_hummus_curation.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-17T10:52:30.354655+00:00 |
| Finished | 2026-06-17T10:53:52.056957+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P160 task prompt and the return contract so we can execute it exactly as specified.
I'll scan the hummus corpus for single-ingredient chickpea products and inspect how ingredients are stored in the canonical files.
Six raw-chickpea products are documented for exclusion; updating the config and re-running the shelf rescore.
## P160 / TASK-304 — Hummus curation return

### Excluded barcodes (6) — single-ingredient raw/dried/frozen chickpeas

| Barcode | Name | Ingredient evidence |
|---------|------|---------------------|
| `3643820` | חומוס ענק | `חומוס ענק עלול להכיל גלוטן חיטה` |
| `7296073005889` | חומוס לבן ענק שופרסל | `גרגרי חומוס` |
| `7296073006015` | חומוס גדול שופרסל | `גרגירי חומוס` |
| `7296073705505` | חומוס מוקפא | `חומוס` |
| `7296073733324` | חומוס | `100% חומוס עלול להכיל גלוטן חיטה` |
| `7296073733331` | חומוס ענק | `100% חומוס עלול להכיל גלוטן חיטה` |

All 6 added to `03_operations/page_generator/configs/hummus_shelfrel_002.json` `exclusions` with reason `out_of_scope: raw/dried chickpeas, not a prepared hummus spread`.

Corpus scan: 69 BSIP1 files → 6 matched single raw-chickpea ingredient pattern. No additional matches beyond these 6.

### Human review (kept, not excluded)

Three products have **empty** `ingredients_list` but nutrition profiles resembling raw chickpeas (`7296073733317`, `7296073733348`, `1990261`). Per conservative rule — no single-ingredient evidence → kept on shelf, flagged for review.

### Re-score results

- **New product count:** 63 (was 69; 6 excluded)
- **Scored corpus:** 69 traces unchanged
- **Grade A count:** 0 (was 5 at top — all raw chickpeas removed)

**New top-5:**

| Rank | Barcode | Grade | Score | Name | Notes |
|------|---------|-------|-------|------|-------|
| 1 | `208428` | B | 76.8 | חומוס שלם יכין | NOVA-3 canned whole chickpeas (retained per TASK-069) |
| 2 | `7290018359686` | B | 76.8 | הקיסר חומוס ענק | NOVA-3 canned whole chickpeas (retained per TASK-069) |
| 3 | `7296073733317` | B | 75.0 | חומוס | Empty ingredients — flagged |
| 4 | `7296073733348` | B | 75.0 | חומוס ענק | Empty ingredients — flagged |
| 5 | `1990261` | B | 73.3 | חומוס | Empty ingredients — flagged |

Raw chickpea bags (single-ingredient NOVA-1, grade A) are gone from the top. First prepared spread with tahini/מבושל is rank 7: `7296073725404` (חומוס מסעדות, B/70.6). Top-2 are canned whole chickpeas, not prepared dips — pre-existing TASK-069 boundary, out of P160 scope.

**Score distribution (63 products):** min=31.80, max=76.80, median=54.50, stdev=8.97, most_common=57 (×8). Grades: B=8, C=42, D=12, E=1.

### Gate results

| Gate | Result |
|------|--------|
| **G8 DATA-SANITY** | PASS |
| **C10 milk Δ** | PASS (20/20, delta=0.0) |
| **OFF** | 0 |
| **score==trace** | OK (0 mismatches) |
| **generate_page gate** | exit 0 PASS |

### Files changed

1. `03_operations/page_generator/configs/hummus_shelfrel_002.json` — added 6 exclusions
2. `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` — regenerated staging page
3. `_rescore_staging/hummus_shelfrel_002/verification_table.csv` — verification artifact

### Verify at

- `03_operations/page_generator/configs/hummus_shelfrel_002.json:37-44` — 6 exclusions
- `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` — 63 products, no excluded barcodes in `products[]`
- `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored_gates_report.md:17` — G8 PASS

**Proposed status: RETURNED** (orchestrator closes after verification)

```json
{
  "task": "TASK-304",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/configs/hummus_shelfrel_002.json", "action": "modified", "sha256": "ab08af7b657b08ee69a059779064fd2addfdb1830b05b193634004ae2d7990bb"},
    {"path": "_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json", "action": "created", "sha256": "8165ddacb9f7371c33206d258dc43ccc855f47c64cb65280c91bbf42165cea26"},
    {"path": "_rescore_staging/hummus_shelfrel_002/verification_table.csv", "action": "created", "sha256": "d842e1fda41b502d5d4a710cc436c261691d67a0668d4567d337f7f06ef50e1f"}
  ],
  "counts": {
    "excluded_raw_chickpeas": "6/69 (canonical_bsip1 corpus scan)",
    "displayed_products": "63/69 (hummus_shelfrel_002_rescored.json products[])",
    "grade_A_displayed": "0/63 (hummus_shelfrel_002_rescored.json)",
    "score_dist": "n=63 min=31.80 max=76.80 median=54.50 stdev=8.97 most_common=57(8) grade_dist={B:8,C:42,D:12,E:1} (_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/rescore_all.py --shelf hummus_shelfrel_002", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "G8 PASS + C10 milk Δ0 + OFF=0 + score==trace OK; top-5 no longer single-ingredient raw chickpea bags (previously 5× grade A); new max grade B/76.8"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M tasks/DISPATCH_BOARD.md
?? tasks/TASK-304.md
?? tasks/TASK-305.md
?? tasks/closed/TASK-303.md
?? tasks/prompts/P160_hummus_curation.md
```

### After dispatch

```
M 03_operations/page_generator/configs/hummus_shelfrel_002.json
 M tasks/DISPATCH_BOARD.md
?? tasks/TASK-304.md
?? tasks/TASK-305.md
?? tasks/closed/TASK-303.md
?? tasks/prompts/P160_hummus_curation.md
```

### Delta

### New / modified since dispatch
   M tasks/DISPATCH_BOARD.md
  M 03_operations/page_generator/configs/hummus_shelfrel_002.json
### Removed / cleaned since dispatch
  M tasks/DISPATCH_BOARD.md
