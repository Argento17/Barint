# Bari frontend QA harness — E2E, accessibility, performance, bundle

Real instruments for the Frontend, QA, and Design agents. The project's one measurable
user metric is *"a first-time mobile user understands the shelf in 15-20 seconds"* — this
harness measures the parts of that which used to be vibes: does the page render, is it
accessible, is it fast, is the bundle bloated.

## Install (one-time)

```bash
npm install                     # installs @playwright/test, @axe-core/playwright, @lhci/cli
npx playwright install chromium # only if browsers aren't already cached
```

Everything is a **devDependency** — zero runtime/bundle impact on the shipped site.

## Commands

| Command | What it does |
|---|---|
| `npm run test:e2e`     | Smoke E2E — comparison routes render, RTL Hebrew, product rows paint |
| `npm run test:a11y`    | axe-core WCAG 2 A/AA scan; **fails on serious/critical** violations |
| `npm run test:perf`    | **Web-Vitals (LCP/CLS/FCP) via Playwright — key-free, primary perf gate.** Measure against production (see below) |
| `npm run test:visual` | Visual regression — full-page screenshots of 5 key routes on mobile (pixel-compare against baselines in `e2e/snapshots/`) |
| `npm run test:e2e:all` | Full suite, mobile + desktop projects |
| `npm run analyze`      | Next 16 built-in Turbopack bundle analyzer (`next experimental-analyze`) |
| `npm run lhci`         | Lighthouse CI — full perf/a11y/SEO scores (`lighthouserc.json`). Best on Linux/CI |

### Measuring performance (key-free, no public URL)

`test:perf` reads real Web Vitals from the page's own Performance API via the cached
Chromium — no PageSpeed key, no deployed URL. **Measure against the production build**, not
dev (dev numbers aren't representative):

```bash
npm run build
npm run start &   # production server on :3000
PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:perf
```

CLS is a hard gate (≤ 0.1); LCP is reported + warned (≤ 2500ms) so a cold server doesn't
flake the suite.

By default the Playwright config boots `npm run dev` itself (reused if already running).
Point at a deployed preview instead with `PLAYWRIGHT_BASE_URL=https://… npm run test:e2e`.

## Status (2026-06-04)

- **Smoke E2E — LIVE-VERIFIED.** 5/5 pass on mobile against the dev server.
- **a11y scan — LIVE-VERIFIED, and it already found a real bug.** axe reports a
  serious **WCAG 1.4.3 (color-contrast)** violation on the grade chips on
  `/hashvaot/maadanim`. That is a genuine finding for Design/Frontend, not a harness
  defect — the gate is doing its job. Fixing chip contrast is tracked separately; until
  then `test:a11y` will (correctly) fail on that route.
- **Web-Vitals perf (`test:perf`) — LIVE-VERIFIED 2026-06-04** against the production build:
  `/` LCP≈1.6s, `/hashvaot/maadanim` & `/hashvaot/hummus` LCP≈1.14s, **CLS=0 on all three**
  — comfortably inside budget. This is the primary, key-free perf instrument.
- **Lighthouse CI** config is wired (LCP/CLS/a11y/SEO budgets) and *runs* locally — it
  launches Chrome and completes the audit — but on Windows it currently aborts at teardown
  on a `chrome-launcher` temp-cleanup `EPERM` race. Treat it as the **CI/Linux** perf+SEO
  path; use `test:perf` for reliable local Web-Vitals. PageSpeed Insights (`pagespeed`
  client) is a third option but needs a *public* URL + a process-level `PAGESPEED_API_KEY`.

## Visual regression (`test:visual`)

**First-run setup** — create baseline screenshots:
```bash
npx playwright test e2e/visual.spec.ts --update-snapshots --project=mobile
npx playwright test e2e/visual.spec.ts --update-snapshots --project=desktop
```

Review and commit the generated PNGs in `e2e/snapshots/`. Subsequent runs compare:
```bash
npm run test:visual
```

On failure, actual/diff images are written to `test-results/` (gitignored).

Routes covered: `/`, `/hashvaot`, `/hashvaot/maadanim`, `/hashvaot/hard-cheeses`, `/hashvaot/snack-bars`, `/hashvaot/milk-comparison`.

Mobile full-page routes use JS freeze (`page.screenshot` + `toMatchSnapshot` with
3% tolerance) to work around unstoppable SVG radar chart / expandable card animations.
Desktop routes use standard `toHaveScreenshot` (2% threshold). See the spec file for
the exact branching logic.

Each route checks: 200 OK, RTL Hebrew, header visible, substantive text, no error overlay, grade chips present (comparison pages), filters not accidentally open, and a full-page pixel-compare screenshot. Mobile additionally checks for horizontal overflow.

## Bundle analyzer note

We use Next 16.1+'s **built-in Turbopack analyzer** (`next experimental-analyze`), not the
`@next/bundle-analyzer` plugin — that plugin is Webpack-only and would mean giving up
Turbopack. The built-in tool needs no extra dependency.
