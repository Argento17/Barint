---
id: TASK-321D
title: Milk baseline extraction — bespoke TS page-data → comparison JSON (conformance blocker #1)
owner: frontend-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  Parallel Claude chat: extract the live milk page's content (hero/prologue/methodology/caveat + per-product copy & render fields) from src/lib/comparisons/milk-comparison-page-data.ts into a new bari-web/src/data/comparisons/milk_frontend_v1.json mirroring the live page EXACTLY. New file only — do NOT alter the live milk route/component/data (no consumer-facing change). This becomes baseline_json for configs/milk.json. Isolated worktree, push branch, no merge/deploy.
---

# TASK-321D — Milk baseline extraction — bespoke TS page-data → comparison JSON (conformance blocker #1)

## Execution log (2026-06-17)

**Branch:** `sweep/milk-baseline-extract` (off `origin/master`, pushed to `Argento17/Barint`)
**Worktree:** `/c/bari-milk` — isolated, never touches main checkout or other parallel worktrees.
**Commit:** `cad0732c` — 1 file changed, 900 insertions(+)

---

## Deliverable

**New file:** `bari-web/src/data/comparisons/milk_frontend_v1.json`

| Field | Value |
|---|---|
| Path | `bari-web/src/data/comparisons/milk_frontend_v1.json` |
| SHA-256 | `AF00C425D41D19FBD8564DCAEC1D9C6D8E528A267268F9861171A57C04BE504F` |
| Product count | 18 |
| Grade distribution | A=3, B=2, C=8, D=4, E=1 |
| run_id | `run_005_headpin` (frozen 85/A ceiling) |
| off_used | false |
| Retailer | yochananof (direct scrape) |

---

## Sources read (no live file modified)

| Source file | What was extracted |
|---|---|
| `src/lib/comparisons/milk-comparison-page-data.ts` | hero, prologue, methodology, caveat notes, blog link, shelf lens options |
| `src/data/milk-comparison.json` | All 18 products — barcode, name, imageUrl, score, grade, nova_proxy, filterTags, energy_kcal, protein/sugar per 100ml, ingredients_display, consumerExplanation (→ rowVerdict + positiveSignals/limitingFactors/comparisonContext) |

**rowVerdict construction** (mirrors `buildMilkProductVM()` logic): `consumerExplanation.whyRated.trim() + " " + consumerExplanation.takeaway.trim()`

**Gap noted in _meta:** milk bespoke JSON does not carry full per-product fat/satFat/carbs/sodium panel. These gaps will be filled by the BSIP0 rescore in Wave 3.

---

## Zero-change verification

```
git diff --name-only       → (empty — no live file modified)
git status --short         → ?? bari-web/src/data/comparisons/milk_frontend_v1.json
```

Only the new additive JSON appears in git status. The live milk route (`/hashvaot/milk-comparison`), the bespoke TS module, and `milk-comparison.json` are all untouched.

---

## Build result

```
EXIT_CODE: 0
Next.js (Turbopack)
✓ Compiled successfully in 7.0s
✓ 43 pages generated (unchanged from master)
/hashvaot/milk-comparison → PRESENT (milk page still renders) ✓
```

---

## Return block

**Status:** RETURNED
**DoD claims verified:**
- [x] Branch `sweep/milk-baseline-extract` pushed to `origin` (Argento17/Barint)
- [x] `milk_frontend_v1.json` created at `bari-web/src/data/comparisons/` (shape: `_meta + page_copy + products[]`)
- [x] All 18 live milk products extracted verbatim (same scores, grades, copy)
- [x] `page_copy` captures hero, prologue (4 sentences), methodology (4 lines), two caveat notes, blog link, shelf lens options
- [x] `_meta`: source=milk-comparison-page-data.ts, run_id=run_005_headpin, off_used=false
- [x] Zero live files modified (`git diff --name-only` = empty)
- [x] `npm run build`: exit 0, 43 pages, 0 TypeScript errors
- [x] `/hashvaot/milk-comparison` still renders identically (no consumer-facing change)

**NOT done (out of scope):**
- Full nutrition panel (fat/satFat/carbs/sodium) — not in bespoke milk JSON; filled by Wave 3 BSIP0 rescore
- Structured d4_additives — same gap; Wave 3
- `configs/milk.json` wiring — next step after Wave 3 rescore, not part of this extraction task

```json
{
  "task_id": "TASK-321D",
  "status": "RETURNED",
  "agent": "frontend-agent",
  "branch": "sweep/milk-baseline-extract",
  "commit": "cad0732c",
  "build_exit_code": 0,
  "build_pages": 43,
  "typescript_errors": 0,
  "new_file": "bari-web/src/data/comparisons/milk_frontend_v1.json",
  "sha256": "AF00C425D41D19FBD8564DCAEC1D9C6D8E528A267268F9861171A57C04BE504F",
  "product_count": 18,
  "grade_distribution": { "A": 3, "B": 2, "C": 8, "D": 4, "E": 1 },
  "run_id": "run_005_headpin",
  "off_used": false,
  "live_files_modified": 0,
  "milk_route_present": true,
  "propose": "RETURNED"
}
```

## ORCHESTRATOR VERIFIED 2026-06-17
Branch sweep/milk-baseline-extract (cad0732ca) verified against origin: exactly ONE file ADDED
(bari-web/src/data/comparisons/milk_frontend_v1.json), zero live files modified. 18 products,
off_used=false, 0 OFF refs, run_id=run_005_headpin, grade dist A:3/B:2/C:8/D:4/E:1, page_copy present.
**Milk conformance blocker #1 RESOLVED** — configs/milk.json baseline_json now points at this file.
Remaining milk blockers: #2 retire the milk-canonical C10 gate in rescore_all (engine-path); #3 moot
(owner: scores don't matter). Branch unmerged (owner-gated); _meta.note flags fat/carbs/sodium absent
from the bespoke TS (generated page will pull full nutrition from BSIP at conform time).
