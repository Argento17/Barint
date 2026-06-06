import { test, expect } from "@playwright/test";

/**
 * Performance / Web-Vitals spec — key-free, no public URL, no external API.
 *
 * Why this exists: the project's metric is mobile comprehension, and load performance is
 * half of it. `pagespeed` (PageSpeed Insights API) needs a public URL + an API key the
 * agent's runtime doesn't inherit; Lighthouse CI runs but hits a Windows temp-cleanup race
 * on teardown. This spec sidesteps both — it drives the already-cached Chromium via
 * Playwright (the harness proven 5/5) and reads real Web Vitals from the page's own
 * Performance API: LCP, CLS, FCP, and navigation timing.
 *
 * MEASURE AGAINST PRODUCTION. Dev-server numbers are not representative (HMR + on-demand
 * compile). Run it against `npm run start`:
 *     npm run build && npm run start &      # production server on :3000
 *     PLAYWRIGHT_BASE_URL=http://localhost:3000 npx playwright test perf.spec.ts --project=mobile
 *
 * Gating: CLS is asserted hard (≤ 0.1 — layout stability is a real comprehension bug when
 * it breaks). LCP is reported and warned, not hard-failed, so the gate stays honest on a
 * cold server rather than flaky.
 */

const ROUTES = ["/", "/hashvaot/maadanim", "/hashvaot/hummus"];
const LCP_BUDGET_MS = 2500;
const CLS_BUDGET = 0.1;

type Vitals = { lcp: number; cls: number; fcp: number | null; load: number | null };

async function collectVitals(page: import("@playwright/test").Page): Promise<Vitals> {
  return page.evaluate(
    () =>
      new Promise<Vitals>((resolve) => {
        let lcp = 0;
        let cls = 0;
        new PerformanceObserver((l) => {
          for (const e of l.getEntries()) lcp = (e as PerformanceEntry).startTime;
        }).observe({ type: "largest-contentful-paint", buffered: true });
        new PerformanceObserver((l) => {
          for (const e of l.getEntries() as unknown as Array<{ value: number; hadRecentInput: boolean }>) {
            if (!e.hadRecentInput) cls += e.value;
          }
        }).observe({ type: "layout-shift", buffered: true });
        setTimeout(() => {
          const fcpEntry = performance.getEntriesByName("first-contentful-paint")[0];
          const nav = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming | undefined;
          resolve({
            lcp: Math.round(lcp),
            cls: Math.round(cls * 1000) / 1000,
            fcp: fcpEntry ? Math.round(fcpEntry.startTime) : null,
            load: nav ? Math.round(nav.loadEventEnd) : null,
          });
        }, 3000);
      })
  );
}

for (const route of ROUTES) {
  test(`web vitals: ${route}`, async ({ page }) => {
    await page.goto(route, { waitUntil: "networkidle" });
    const v = await collectVitals(page);
    const lcpFlag = v.lcp > LCP_BUDGET_MS ? `  ⚠ LCP over ${LCP_BUDGET_MS}ms budget` : "";
    console.log(
      `${route} — LCP=${v.lcp}ms CLS=${v.cls} FCP=${v.fcp}ms load=${v.load}ms${lcpFlag}`
    );
    // Hard gate: layout stability. Soft: LCP (reported above).
    expect(v.cls, `CLS budget on ${route}`).toBeLessThanOrEqual(CLS_BUDGET);
  });
}
