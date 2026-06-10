---
status: CLOSED
cc_reviewed: true
priority: medium
owner: dev-agent
created: 2026-06-09
updated: 2026-06-09
category: tooling
roadmap_impact: false
tags: [testing, visual-regression, playwright, e2e]
supersedes: []
superseded_by: []
---

# TASK-221: Screenshot Regression Checks for Bari Website

## Summary

Add Playwright-based screenshot regression testing for 6 key Bari website
routes, covering both mobile (Pixel 5) and desktop (1280×720) viewports
= 12 total tests.

## Routes covered

| Path                             | Name              | Mobile shot        | Desktop shot     |
|----------------------------------|-------------------|--------------------|------------------|
| `/`                              | homepage          | viewport (JS freeze) | full-page       |
| `/hashvaot`                      | hashvaot-index    | viewport (carousel masked) | viewport (carousel masked) |
| `/hashvaot/maadanim`             | hashvaot-maadanim | full-page (JS freeze) | full-page       |
| `/hashvaot/hard-cheeses`         | hashvaot-hard-cheeses | full-page (JS freeze) | full-page   |
| `/hashvaot/snack-bars`           | hashvaot-snack-bars | full-page (JS freeze) | full-page    |
| `/hashvaot/milk-comparison`      | hashvaot-milk     | full-page (JS freeze) | full-page       |

## What each test asserts

1. 200 OK response
2. RTL Hebrew document (`html[dir="rtl"]`)
3. Header / logo visible
4. Substantive Hebrew text (>100 chars, Hebrew Unicode range)
5. No Next.js error overlay
6. Grade chips (A–E) visible on comparison pages
7. Filters not accidentally open on comparison pages
8. No horizontal overflow on mobile viewport
9. Screenshot compared against baseline

## Implementation

- **`e2e/visual.spec.ts`** — test spec with 6 parameterized routes × 2 projects
- **`playwright.config.ts`** — added `snapshotDir: "./e2e/snapshots"`
- **`package.json`** — added `"test:visual"` script
- **`.gitignore`** — added `/test-results/`
- **`e2e/README.md`** — visual regression documentation + first-run setup

## Baseline screenshots (12 PNGs, 340KB – 3.9MB each)

Stored in `e2e/snapshots/visual.spec.ts-snapshots/`:
| File | Size |
|------|------|
| `homepage-mobile-win32.png` | 754 KB |
| `homepage-desktop-win32.png` | 405 KB |
| `hashvaot-index-mobile-win32.png` | 764 KB |
| `hashvaot-index-desktop-win32.png` | 341 KB |
| `hashvaot-maadanim-mobile-win32.png` | 3885 KB |
| `hashvaot-maadanim-desktop-win32.png` | 1263 KB |
| `hashvaot-hard-cheeses-mobile-win32.png` | 1543 KB |
| `hashvaot-hard-cheeses-desktop-win32.png` | 705 KB |
| `hashvaot-snack-bars-mobile-win32.png` | 1293 KB |
| `hashvaot-snack-bars-desktop-win32.png` | 520 KB |
| `hashvaot-milk-mobile-win32.png` | 1081 KB |
| `hashvaot-milk-desktop-win32.png` | 406 KB |

## Test commands

```bash
# First-run baseline creation
npx playwright test e2e/visual.spec.ts --update-snapshots --project=mobile --project=desktop

# Comparison (pixel-match against baselines)
npm run test:visual
```

## Return block

**Done and verified:**

- 12/12 tests pass in baseline creation mode
- 12/12 tests pass in comparison mode (final run: 53.1s)
- `.last-run.json` confirmed `status: "passed"` after isolated visual run
- `/hashvaot/milk-comparison` added (the actual route; `/hashvaot/milk` does not exist)

**Known limitations:**

1. **`.last-run.json` shows the LAST run irrespective of scope.** When `npx playwright test` is called without filters (e.g. `npx playwright test e2e/smoke.spec.ts e2e/a11y.spec.ts ...`), the combined result overwrites `.last-run.json`. A prior "failed" status was from the a11y run, not from visual regression. To check visual regression status, run `npm run test:visual` and inspect the exit code or `.last-run.json`.

2. **Mobile JS freeze workaround.** The homepage has an SVG radar chart animated via `requestAnimationFrame` (not CSS); Playwright's `animations: "disabled"` cannot freeze it. All mobile full-page comparison routes similarly have JS-driven content (expandable product cards, SVG charts). These routes use a JS freeze (`animation: none !important` injected via `<style>`) and `page.screenshot()` + `toMatchSnapshot()` instead of `toHaveScreenshot()`. Thresholds: homepage 0.01, mobile full-page 0.03 pixel ratio.

3. **Desktop routes use standard `toHaveScreenshot()`** with `animations: "disabled"` and `threshold: 0.02` — no freeze needed.

**To close:** Review the 12 baseline PNGs in `e2e/snapshots/` for correctness, then close this task.
