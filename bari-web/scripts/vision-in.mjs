#!/usr/bin/env node
/**
 * vision-in.mjs — the Design Agent's vision-in loop (TASK-505).
 *
 * Renders a route headlessly (project-installed Playwright), and for each requested
 * viewport emits:
 *   1. full-page PNG screenshot                       -> <out>/<slug>__<viewport>.png
 *   2. geometry.json (per matched element: rect + computed styles)
 *                                                     -> <out>/<slug>__<viewport>.geometry.json
 *   3. review.md — MEASURED summary (heights, margins, mechanical frozen-cap checks)
 *                                                     -> <out>/review.md
 *
 * The Design Agent feeds the PNG back as multimodal input and reads the numbers from
 * geometry.json — verdicts come from measurements, never guesses. Findings emitted here
 * are MEASURED facts, not design verdicts.
 *
 * Usage:
 *   npm run vision-in -- --route /hashvaot/brined-cheeses
 *   node scripts/vision-in.mjs --route /hashvaot/magnesium --viewport mobile
 *   node scripts/vision-in.mjs --route / --selectors "h1,.bari-cmp-row" --out .vision-in/run1
 *
 * Args:
 *   --route     path to render (required), e.g. /hashvaot/brined-cheeses
 *   --base      server origin              (default http://localhost:3000)
 *   --out       output directory           (default .vision-in/<timestamp>)
 *   --selectors comma-separated CSS list   (default: built-in comparison-page set below)
 *   --viewport  mobile | desktop | both    (default both; mobile = 375x812)
 *
 * Requires the app to already be running at --base (npm run dev / build+start).
 * Output is evidence for one review — do not commit it.
 */

import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

// ---------------------------------------------------------------- args
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (!args.route) {
  console.error("ERROR: --route is required, e.g. --route /hashvaot/brined-cheeses");
  process.exit(1);
}

const ROUTE = String(args.route);
const BASE = String(args.base ?? "http://localhost:3000");
const VIEWPORT_ARG = String(args.viewport ?? "both").toLowerCase();
if (!["mobile", "desktop", "both"].includes(VIEWPORT_ARG)) {
  console.error('ERROR: --viewport must be one of mobile | desktop | both');
  process.exit(1);
}

const STAMP = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
const OUT_DIR = path.resolve(String(args.out ?? path.join(".vision-in", STAMP)));

// Built-in selector set for Bari comparison pages. Labels are used in review.md.
// Sourced from the real DOM: CategoryHero renders <header><h1>, CategoryPrologue is the
// <section> right after it, rows/cells carry the bari-cmp-* classes (globals.css), the
// grade chip is the rounded-xl box inside the grade cell, and the methodology footer is
// the pb-6 <footer> (the site footer uses py-6, so it is excluded).
const DEFAULT_SELECTORS = [
  { label: "hero-header", selector: "header:has(h1)" },
  { label: "hero-title", selector: "h1" },
  { label: "prologue", selector: "header:has(h1) + section" },
  { label: "product-row", selector: ".bari-cmp-row" },
  { label: "row-head", selector: ".bari-cmp-rowhead" },
  { label: "product-name-cell", selector: ".bari-cmp-namecell" },
  { label: "score-chip", selector: ".bari-cmp-gradecell .rounded-xl" },
  { label: "thumbnail", selector: ".bari-cmp-thumbcell" },
  { label: "methodology-footer", selector: "footer.pb-6" },
];

const SELECTOR_SET = args.selectors
  ? String(args.selectors)
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => ({ label: s, selector: s }))
  : DEFAULT_SELECTORS;

const VIEWPORTS = [];
if (VIEWPORT_ARG === "mobile" || VIEWPORT_ARG === "both") {
  VIEWPORTS.push({ name: "mobile", width: 375, height: 812 });
}
if (VIEWPORT_ARG === "desktop" || VIEWPORT_ARG === "both") {
  VIEWPORTS.push({ name: "desktop", width: 1280, height: 720 });
}

// Frozen caps this script can check mechanically (Gen 1 constraints, design-agent.md).
// These produce MEASURED findings — facts, not verdicts.
const CAPS = [
  {
    appliesTo: (label) => /row-?head|rowhead/i.test(label),
    viewports: ["mobile", "desktop"],
    maxHeight: 80,
    rule: "collapsed row height must be <= 80px (frozen: 72px target, 80px max)",
  },
  {
    appliesTo: (label) => /hero-header|^header/i.test(label),
    viewports: ["mobile"],
    maxHeight: 280,
    rule: "hero max 280px on mobile (frozen)",
  },
];

function slugOf(route) {
  return route.replace(/^\//, "").replace(/\/+$/, "").replace(/\//g, "-") || "home";
}

const r2 = (n) => Math.round(n * 100) / 100;

// ---------------------------------------------------------------- capture
async function captureViewport(browser, viewport) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  const url = BASE.replace(/\/$/, "") + ROUTE;

  const resp = await page.goto(url, { waitUntil: "load", timeout: 60_000 });
  if (!resp || !resp.ok()) {
    throw new Error(`route ${url} returned ${resp ? resp.status() : "no response"}`);
  }

  // Freeze animations/transitions so geometry and pixels are stable.
  await page.addStyleTag({
    content:
      "*, *::before, *::after { animation: none !important; transition: none !important; caret-color: transparent !important; }",
  });
  await page.waitForLoadState("networkidle").catch(() => {});
  await page.waitForTimeout(500);

  const slug = slugOf(ROUTE);
  const pngPath = path.join(OUT_DIR, `${slug}__${viewport.name}.png`);
  await page.screenshot({ path: pngPath, fullPage: true });

  const elements = await page.evaluate((selectorSet) => {
    const out = [];
    for (const { label, selector } of selectorSet) {
      let nodes = [];
      try {
        nodes = Array.from(document.querySelectorAll(selector));
      } catch {
        out.push({ label, selector, error: "invalid selector", index: -1 });
        continue;
      }
      nodes.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        const cs = window.getComputedStyle(el);
        out.push({
          label,
          selector,
          index,
          rect: {
            x: rect.x + window.scrollX,
            y: rect.y + window.scrollY,
            width: rect.width,
            height: rect.height,
          },
          computed: {
            color: cs.color,
            backgroundColor: cs.backgroundColor,
            fontSize: cs.fontSize,
            lineHeight: cs.lineHeight,
            direction: cs.direction,
            marginTop: cs.marginTop,
            marginBottom: cs.marginBottom,
            paddingTop: cs.paddingTop,
            paddingBottom: cs.paddingBottom,
            borderRadius: cs.borderRadius,
          },
          text: (el.textContent || "").trim().slice(0, 80),
        });
      });
      if (nodes.length === 0) {
        out.push({ label, selector, index: -1, matches: 0 });
      }
    }
    return out;
  }, SELECTOR_SET);

  // Round rects for readability.
  for (const el of elements) {
    if (el.rect) {
      el.rect = {
        x: r2(el.rect.x),
        y: r2(el.rect.y),
        width: r2(el.rect.width),
        height: r2(el.rect.height),
      };
    }
  }

  const geometry = {
    route: ROUTE,
    url,
    viewport: { name: viewport.name, width: viewport.width, height: viewport.height },
    capturedAt: new Date().toISOString(),
    screenshot: path.basename(pngPath),
    selectors: SELECTOR_SET,
    elements,
  };

  const geoPath = path.join(OUT_DIR, `${slug}__${viewport.name}.geometry.json`);
  fs.writeFileSync(geoPath, JSON.stringify(geometry, null, 2), "utf8");

  await context.close();
  return { viewport, pngPath, geoPath, geometry };
}

// ---------------------------------------------------------------- review.md
function buildReview(captures) {
  const lines = [];
  lines.push(`# Vision-in capture - ${ROUTE}`);
  lines.push("");
  lines.push(`- Base: ${BASE}`);
  lines.push(`- Captured: ${new Date().toISOString()}`);
  lines.push(`- Output dir: ${OUT_DIR}`);
  lines.push("");
  lines.push(
    "All values below are MEASURED from the rendered DOM (getBoundingClientRect + " +
      "getComputedStyle). Findings are mechanical cap checks, NOT design verdicts; " +
      "the Design Agent reads the screenshot + geometry.json and issues the verdict."
  );
  lines.push("");

  const allFindings = [];

  for (const cap of captures) {
    const { viewport, pngPath, geometry } = cap;
    lines.push(`## Viewport: ${viewport.name} (${viewport.width}x${viewport.height})`);
    lines.push("");
    lines.push(`- Screenshot: \`${path.basename(pngPath)}\``);
    lines.push(`- Geometry: \`${path.basename(cap.geoPath)}\``);
    lines.push("");
    lines.push("| label | selector | matches | height min-max (px) | first rect (x,y,w,h) | margin t/b | font-size |");
    lines.push("|---|---|---|---|---|---|---|");

    for (const { label, selector } of SELECTOR_SET) {
      const matched = geometry.elements.filter((e) => e.label === label && e.rect);
      if (matched.length === 0) {
        lines.push(`| ${label} | \`${selector}\` | 0 | - | - | - | - |`);
        continue;
      }
      const heights = matched.map((e) => e.rect.height);
      const hMin = r2(Math.min(...heights));
      const hMax = r2(Math.max(...heights));
      const f = matched[0];
      lines.push(
        `| ${label} | \`${selector}\` | ${matched.length} | ${hMin}-${hMax} | ` +
          `${f.rect.x}, ${f.rect.y}, ${f.rect.width}, ${f.rect.height} | ` +
          `${f.computed.marginTop}/${f.computed.marginBottom} | ${f.computed.fontSize} |`
      );
    }
    lines.push("");

    // Mechanical frozen-cap checks.
    const findings = [];
    for (const capRule of CAPS) {
      if (!capRule.viewports.includes(viewport.name)) continue;
      for (const { label } of SELECTOR_SET) {
        if (!capRule.appliesTo(label)) continue;
        const matched = geometry.elements.filter((e) => e.label === label && e.rect);
        for (const el of matched) {
          if (el.rect.height > capRule.maxHeight) {
            findings.push(
              `MEASURED: [${viewport.name}] ${label}[${el.index}] height = ${el.rect.height}px ` +
                `exceeds cap ${capRule.maxHeight}px (${capRule.rule})`
            );
          }
        }
      }
    }
    if (findings.length) {
      lines.push("### MEASURED findings (mechanical cap checks)");
      lines.push("");
      for (const fdg of findings) lines.push(`- ${fdg}`);
      allFindings.push(...findings);
    } else {
      lines.push("### MEASURED findings: none (all mechanical caps within limits)");
    }
    lines.push("");
  }

  lines.push("---");
  lines.push(
    `Summary: ${captures.length} viewport(s), ${allFindings.length} measured cap ` +
      "exceedance(s). Contrast (4.5:1) is NOT computed here; feed color/backgroundColor " +
      "pairs from geometry.json into a contrast check, or run npm run test:a11y."
  );
  lines.push("");
  return { text: lines.join("\n"), findingsCount: allFindings.length };
}

// ---------------------------------------------------------------- main
(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  console.log(`vision-in: route=${ROUTE} base=${BASE} viewports=${VIEWPORTS.map((v) => v.name).join(",")}`);
  console.log(`vision-in: out=${OUT_DIR}`);

  const browser = await chromium.launch();
  const captures = [];
  try {
    for (const viewport of VIEWPORTS) {
      console.log(`vision-in: capturing ${viewport.name} (${viewport.width}x${viewport.height}) ...`);
      const cap = await captureViewport(browser, viewport);
      const matchedCount = cap.geometry.elements.filter((e) => e.rect).length;
      console.log(
        `vision-in:   ${path.basename(cap.pngPath)} + ${path.basename(cap.geoPath)} ` +
          `(${matchedCount} elements measured)`
      );
      captures.push(cap);
    }
  } finally {
    await browser.close();
  }

  const review = buildReview(captures);
  const reviewPath = path.join(OUT_DIR, "review.md");
  fs.writeFileSync(reviewPath, review.text, "utf8");
  console.log(`vision-in: review.md written (${review.findingsCount} measured cap exceedances)`);
  console.log(`vision-in: DONE -> ${OUT_DIR}`);
})().catch((err) => {
  console.error(`vision-in: FAILED - ${err.message}`);
  console.error(
    "vision-in: is the app running? Start it first: npm run dev (or npm run build && npm run start)"
  );
  process.exit(1);
});
