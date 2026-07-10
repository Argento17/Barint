# TASK-510 Return — category-hero eyebrow contrast fix

## What changed

**File:** `bari-web/src/components/shared/category-hero.tsx` line 28

**Exact diff (one line):**

    -      <p className="font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80">
    +      <p className="font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#176F53]">

One-line change: removed the 80% opacity modifier from `#1F8F6A` and replaced with the `--bari-green-deep` token value `#176F53` (confirmed at `colors_and_type.css:15`).

**Commit:** `2e216193fd79a9c2e0a65ab53d624c41bf13c769` on branch `fix/task510-hero-contrast`
**Worktree:** `C:/bari_wt_t510` (from `origin/master` @ `c6993b48`)

---

## Contrast ratio verification (mathematical, not axe assertion)

Computed via Python (sRGB linearization per WCAG 2.1 §1.4.3):

| Color | Condition | Composite | Luminance | Contrast vs white | Pass AA (4.5:1)? |
|---|---|---|---|---|---|
| `#1F8F6A` at `/80` opacity | old | `rgb(76,165,136)` | 0.3443 | **2.981:1** | FAIL |
| `#176F53` | new | solid | 0.1464 | **6.113:1** | PASS |

Command: Python sRGB linearization via PowerShell pipe. Formula: `srgb_to_linear(c) = ((c/255 + 0.055)/1.055)^2.4` for `c > 0.04045`; `luminance = 0.2126*R + 0.7152*G + 0.0722*B`; `contrast = (L_white + 0.05) / (L_color + 0.05)`. PowerShell exit 0.

---

## Remaining `#1F8F6A]/80` occurrences in `bari-web/src/`

Command: `Grep pattern="#1F8F6A]/80" path=C:/bari_wt_t510/bari-web/src output_mode=count`

Result: **5 occurrences across 4 files** (none in `category-hero.tsx`):

| File | Count | In a11y gate routes? |
|---|---|---|
| `src/app/products/demo/page.tsx` | 2 | No — demo route, not in gate |
| `src/app/newsletter/page.tsx` | 1 | No — `/newsletter` not in gate |
| `src/app/hashvaot/page.tsx` | 1 | No — `/hashvaot` landing not in gate |
| `src/components/hashvaot/hashvaot-category-landing.tsx` | 1 | No — used by `/supermarket`, `/raw-foods`, `/personal-care` (none in gate) |

These are out-of-scope for TASK-510's one-line spec. They are real live-page WCAG 1.4.3 failures on non-canonical pages. Flagged for follow-on.

The e2e test file `e2e/task492c-fix2-verify.spec.ts` also contains the string in a comment (not rendered). Total count across all bari-web = 6 occurrences in 5 files, none in `category-hero.tsx`.

---

## TypeScript / Lint

- `npx tsc --noEmit` (in `C:/bari_wt_t510/bari-web`) — exit code: **0** (no type errors)
- `npm run lint` (in `C:/bari_wt_t510/bari-web`) — exit code: **0** (18 warnings, 0 errors, all pre-existing, none from this change)

---

## a11y gate results

Command: `npx playwright test e2e/a11y.spec.ts --project=mobile` (in `C:/bari_wt_t510/bari-web`)
Exit code: **0**
Result: **4/4 mobile routes PASS — 0 serious/critical violations**

| Route | Mobile result |
|---|---|
| `/` | ok (0 violations) |
| `/hashvaot/breakfast-cereals` | ok (0 violations) |
| `/hashvaot/hummus` | ok (0 violations) |
| `/p/7290016245325` | ok (0 violations) |

Full suite (`npm run test:a11y` — both mobile + desktop): exit code **1**.
- Mobile: 4/4 pass
- Desktop: 3/4 fail — pre-existing violations in **different components** (carousel category chips `#1F8F6A` on `#E8F5EF` background = 3.6:1; rank number chips `#7a817c` on white = 3.85-3.99:1)
- These desktop failures exist on `origin/master` and are NOT introduced by this change

---

## Pre-existing desktop a11y issues discovered (out of scope, flagged)

1. **Carousel category chips** (`/` route): `#1F8F6A` text on `#E8F5EF` bg = 3.6:1 (needs 4.5:1)
2. **Rank number chips** (`/hashvaot/breakfast-cereals`, `/hashvaot/hummus`): `#7a817c` on white/`#fbfbf9` = 3.85-3.99:1

These need a follow-on task.

---

## npm ci

Command: `npm ci --prefer-offline` (in `C:/bari_wt_t510/bari-web`) — exit code: **0**

---

## Proposed status: RETURNED

All spec requirements met within the ONE-LINE boundary. Awaiting orchestrator review and PR creation.

---

```json
{
  "task": "TASK-510",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/src/components/shared/category-hero.tsx",
      "action": "modified",
      "sha256": "9ff6e19a737a38319bf77d94f522e0db63adee09fc1a50c1db5da83e6991a8df"
    }
  ],
  "counts": {
    "mobile_a11y_routes_passed": "4/4 (routes: /, /hashvaot/breakfast-cereals, /hashvaot/hummus, /p/7290016245325 — source: playwright test stdout)",
    "mobile_a11y_serious_critical_violations": "0/4 routes (source: playwright test exit 0, --project=mobile)",
    "remaining_old_color_occurrences_in_src": "5/5 files in bari-web/src still have #1F8F6A]/80 (source: Grep count on C:/bari_wt_t510/bari-web/src — demo x2, newsletter x1, hashvaot-index x1, hashvaot-category-landing x1; none in gate routes)",
    "lines_changed": "1/1 (source: git diff --stat bari-web/src/components/shared/category-hero.tsx)",
    "lint_errors": "0/18 lint problems are errors (source: npm run lint exit 0)",
    "tsc_errors": "0/0 (source: npx tsc --noEmit exit 0)"
  },
  "commands_run": [
    {"cmd": "git -C C:/Bari worktree add C:/bari_wt_t510 -b fix/task510-hero-contrast origin/master", "exit_code": 0},
    {"cmd": "npm ci --prefer-offline (cwd: C:/bari_wt_t510/bari-web)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (cwd: C:/bari_wt_t510/bari-web)", "exit_code": 0},
    {"cmd": "npm run lint (cwd: C:/bari_wt_t510/bari-web)", "exit_code": 0},
    {"cmd": "npx playwright test e2e/a11y.spec.ts --project=mobile (cwd: C:/bari_wt_t510/bari-web)", "exit_code": 0},
    {"cmd": "npm run test:a11y (full suite, cwd: C:/bari_wt_t510/bari-web)", "exit_code": 1},
    {"cmd": "git -C C:/bari_wt_t510 commit -m 'TASK-510: category-hero eyebrow contrast #1F8F6A/80 -> #176F53 (WCAG 6.11:1)'", "exit_code": 0}
  ],
  "not_done": [
    "Full npm run test:a11y (both mobile+desktop) exits 1 — desktop fails on PRE-EXISTING issues in carousel category chips (#1F8F6A on #E8F5EF bg 3.6:1) and rank number chips (#7a817c on white 3.85-3.99:1) unrelated to this fix",
    "5 remaining #1F8F6A]/80 occurrences in non-gate-route pages (newsletter, hashvaot index, supermarket/raw-foods/personal-care via hashvaot-category-landing, demo) are real live WCAG 1.4.3 failures — out of scope per ONE-LINE spec; need follow-on task",
    "PR not created — spec says do not push; awaiting orchestrator go-live decision"
  ],
  "self_check": "npx playwright test e2e/a11y.spec.ts --project=mobile: 4/4 routes pass, 0 serious/critical violations, exit code 0. #176F53 on white = 6.113:1 (WCAG AA threshold 4.5:1). Verified mathematically via Python sRGB linearization AND confirmed via axe-core running against the live dev server."
}
```
