/**
 * Vision-in probe — the Design Agent's "eyes".
 *
 * Unlike visual.spec.ts (which pixel-diffs against committed baselines to catch
 * REGRESSIONS), this probe is a CAPTURE TOOL: it renders a route and emits, for the
 * mobile + desktop viewports, both
 *   1. a full-page screenshot            → e2e/vision-out/<slug>__<project>.png
 *   2. a machine-readable geometry report → e2e/vision-out/<slug>__<project>.geometry.json
 *
 * The Design Agent (v2) is fed BOTH so it reasons over exact pixels instead of guessing:
 *   - per-selector bounding boxes + computed margin/padding/font/color/bg/border  → alignment & spacing
 *   - a page-wide WCAG contrast scan of text-bearing nodes (ratio vs 4.5:1 / 3:1) → the invisible-glyph /
 *     low-contrast class that a text-only critic cannot see (the +/− glyph + box-outline bugs).
 *
 * Run (auto-starts the dev server, or reuses one already on :3000):
 *   npm run vision                                   # default route, both projects
 *   VISION_ROUTE=/hashvaot/snack-bars npm run vision # another route
 *   VISION_SELECTORS="[class*='chip'],h1,button" VISION_ROUTE=/ npm run vision
 *   npx playwright test e2e/vision-probe.spec.ts --project=mobile   # one viewport
 *
 * Env:
 *   VISION_ROUTE      route to probe              (default "/hashvaot/breakfast-cereals")
 *   VISION_SELECTORS  comma list of CSS selectors (default a generic component set)
 *   VISION_OUT        output dir                  (default "e2e/vision-out")
 *   VISION_MAX_NODES  contrast-scan node cap      (default 250)
 *
 * Output is gitignored — it is evidence for one review, not a committed baseline.
 */

import { test, expect } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

const ROUTE = process.env.VISION_ROUTE ?? "/hashvaot/breakfast-cereals";
const OUT = process.env.VISION_OUT ?? "e2e/vision-out";
const SELECTORS = (
  process.env.VISION_SELECTORS ??
  "h1,h2,h3,button,[class*='chip'],[class*='card'],[class*='row']"
)
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);
const MAX_NODES = Number(process.env.VISION_MAX_NODES ?? 250);

function slugOf(route: string): string {
  return route.replace(/^\//, "").replace(/\/+$/, "").replace(/\//g, "-") || "home";
}

test(`vision-probe: ${ROUTE}`, async ({ page }, testInfo) => {
  test.setTimeout(90_000);

  const resp = await page.goto(ROUTE, { waitUntil: "load" });
  expect(resp?.ok(), `route ${ROUTE} should return 200`).toBeTruthy();

  // Settle JS-driven animations so geometry + screenshot are stable.
  await page.evaluate(() => {
    const s = document.createElement("style");
    s.textContent =
      "*, *::before, *::after { animation: none !important; transition: none !important; }";
    document.head.appendChild(s);
  });
  await page.waitForTimeout(800);

  const report = await page.evaluate(
    ({ selectors, maxNodes }) => {
      type RGB = { r: number; g: number; b: number; a: number };

      const parseColor = (c: string): RGB | null => {
        const m = c.match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        const p = m[1].split(",").map((x) => parseFloat(x.trim()));
        return { r: p[0], g: p[1], b: p[2], a: p[3] === undefined ? 1 : p[3] };
      };
      const relLum = ({ r, g, b }: RGB) => {
        const f = (v: number) => {
          v /= 255;
          return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        };
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
      };
      const contrast = (fg: RGB, bg: RGB) => {
        const L1 = relLum(fg);
        const L2 = relLum(bg);
        return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      };
      // Walk ancestors for the first opaque background; flatten alpha over white.
      const effectiveBg = (el: Element): RGB => {
        let node: Element | null = el;
        while (node) {
          const c = parseColor(getComputedStyle(node).backgroundColor);
          if (c && c.a > 0) {
            if (c.a >= 1) return c;
            return {
              r: Math.round(c.r * c.a + 255 * (1 - c.a)),
              g: Math.round(c.g * c.a + 255 * (1 - c.a)),
              b: Math.round(c.b * c.a + 255 * (1 - c.a)),
              a: 1,
            };
          }
          node = node.parentElement;
        }
        return { r: 255, g: 255, b: 255, a: 1 };
      };
      const box = (el: Element) => {
        const r = el.getBoundingClientRect();
        return {
          x: Math.round(r.x),
          y: Math.round(r.y),
          w: Math.round(r.width),
          h: Math.round(r.height),
        };
      };
      const styleOf = (el: Element) => {
        const s = getComputedStyle(el);
        return {
          margin: [s.marginTop, s.marginRight, s.marginBottom, s.marginLeft].join(" "),
          padding: [s.paddingTop, s.paddingRight, s.paddingBottom, s.paddingLeft].join(" "),
          fontSize: s.fontSize,
          fontWeight: s.fontWeight,
          lineHeight: s.lineHeight,
          color: s.color,
          background: s.backgroundColor,
          border: `${s.borderTopWidth} ${s.borderTopStyle} ${s.borderTopColor}`,
          gap: s.gap,
          display: s.display,
          flexDirection: s.flexDirection,
        };
      };

      const geometry: Record<string, unknown> = {};
      for (const sel of selectors) {
        let els: Element[];
        try {
          els = Array.from(document.querySelectorAll(sel));
        } catch (e) {
          geometry[sel] = { error: String(e) };
          continue;
        }
        const rows = els.slice(0, 40).map((el) => ({
          tag: el.tagName.toLowerCase(),
          text: (el.textContent || "").trim().slice(0, 40),
          box: box(el),
          style: styleOf(el),
        }));
        geometry[sel] = { count: els.length, items: rows };
      }

      // Page-wide WCAG contrast scan over elements with their own text.
      const findings: unknown[] = [];
      let scanned = 0;
      for (const el of Array.from(document.querySelectorAll("body *"))) {
        if (scanned >= maxNodes) break;
        const direct = Array.from(el.childNodes)
          .filter((n) => n.nodeType === 3)
          .map((n) => (n.textContent || "").trim())
          .join("")
          .trim();
        if (!direct) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === "hidden" || cs.display === "none" || parseFloat(cs.opacity) === 0)
          continue;
        const fg = parseColor(cs.color);
        if (!fg || fg.a === 0) continue;
        const bg = effectiveBg(el);
        const ratio = contrast(fg, bg);
        const sizePx = parseFloat(cs.fontSize);
        const bold = parseInt(cs.fontWeight) >= 700;
        const large = sizePx >= 24 || (sizePx >= 18.66 && bold);
        const required = large ? 3 : 4.5;
        scanned++;
        if (ratio < required) {
          findings.push({
            text: direct.slice(0, 40),
            color: cs.color,
            bg: `rgb(${bg.r},${bg.g},${bg.b})`,
            ratio: Math.round(ratio * 100) / 100,
            fontSizePx: sizePx,
            bold,
            required,
          });
        }
      }

      return {
        url: location.href,
        dir: document.documentElement.dir,
        geometry,
        contrastScanned: scanned,
        contrastFailCount: findings.length,
        contrastFindings: findings,
      };
    },
    { selectors: SELECTORS, maxNodes: MAX_NODES }
  );

  // Sanity: a blank page is a failed probe, not a clean one.
  type GeometryEntry = { count: number } | { error: string } | null;
  const anyGeometry = Object.values(
    report.geometry as Record<string, GeometryEntry>
  ).some(
    (g) =>
      g &&
      typeof g === "object" &&
      "count" in g &&
      typeof g.count === "number" &&
      g.count > 0
  );
  expect(
    anyGeometry || report.contrastScanned > 0,
    "probe captured no elements — page likely blank or route wrong"
  ).toBeTruthy();

  const dir = path.resolve(OUT);
  fs.mkdirSync(dir, { recursive: true });
  const base = `${slugOf(ROUTE)}__${testInfo.project.name}`;

  await page.screenshot({
    path: path.join(dir, `${base}.png`),
    fullPage: true,
    animations: "disabled",
    scale: "device",
  });
  fs.writeFileSync(
    path.join(dir, `${base}.geometry.json`),
    JSON.stringify(
      { route: ROUTE, project: testInfo.project.name, selectors: SELECTORS, ...report },
      null,
      2
    )
  );

  // Surface the headline in the runner log.
  console.log(
    `[vision-probe] ${base}: ${report.contrastFailCount} contrast fails / ${report.contrastScanned} text nodes → ${path.join(OUT, base)}.{png,geometry.json}`
  );
});
