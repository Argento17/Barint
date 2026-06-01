#!/usr/bin/env node
// bari-qa-validate.js — Wave 1 automated QA checks
// Run: node .claude/bari-qa-validate.js

"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const src = (...parts) => path.join(ROOT, "src", ...parts);

let passed = 0;
let failed = 0;

function check(name, condition, detail) {
  if (condition) {
    console.log(`  ✓ ${name}`);
    passed++;
  } else {
    console.error(`  ✗ ${name}${detail ? ": " + detail : ""}`);
    failed++;
  }
}

function read(...parts) {
  return fs.readFileSync(src(...parts), "utf-8");
}

function routeExists(href) {
  const parts = href.replace(/^\//, "").split("/");
  return fs.existsSync(src("app", ...parts, "page.tsx"));
}

// ── 1. Grade palette consistency ─────────────────────────────────────────────
console.log("\n[1] Grade palette consistency");

const tokens = read("lib", "design", "bari-comparison-tokens.ts");

const expectedPalette = {
  A: "#176F53",
  B: "#176F53",
  C: "#8F6600",
  D: "#A63F2A",
  E: "#8B2E2E",
};

for (const [grade, textColor] of Object.entries(expectedPalette)) {
  check(
    `Grade ${grade} token text colour is ${textColor}`,
    tokens.includes(textColor)
  );
}

check(
  "All five grades (A–E) are defined in gradePalette",
  ["A", "B", "C", "D", "E"].every((g) =>
    new RegExp(`\\b${g}:\\s*\\{`).test(tokens)
  )
);

const gradeBadge = read("components", "comparisons", "bari-grade-badge.tsx");
check(
  "BariGradeBadge falls back to gradePalette.C",
  gradeBadge.includes("gradePalette.C")
);

// ── 2. Hero CTA scroll target ─────────────────────────────────────────────────
console.log("\n[2] Hero CTA scroll target");

const heroSrc = read("components", "home", "home-hero.tsx");
const engineSrc = read("components", "home", "home-analysis-engine.tsx");

check(
  "Hero primary CTA href is #analysis-engine",
  heroSrc.includes('href="#analysis-engine"')
);
check(
  'HomeAnalysisEngine section has id="analysis-engine"',
  engineSrc.includes('id="analysis-engine"')
);

// ── 3. Mobile above-fold CTA spacing ─────────────────────────────────────────
console.log("\n[3] Mobile above-fold CTA spacing");

check(
  "Hero CTA container uses responsive top margin (sm:mt-11)",
  heroSrc.includes("sm:mt-11")
);
check(
  "Hero trust row uses responsive top margin (sm:mt-16)",
  heroSrc.includes("sm:mt-16")
);
check(
  "Hero CTA container mobile margin is mt-7 (not mt-11)",
  heroSrc.includes("mt-7") && !heroSrc.match(/\bmt-11\b(?!.*sm:)/)
);

// ── 4. Blog-to-comparison cross-navigation ────────────────────────────────────
console.log("\n[4] Blog-to-comparison cross-navigation");

const breadContent = read("lib", "blog", "bread-analysis-content.ts");
const milkArticle = read("components", "blog", "milk-analysis-article.tsx");
const milkContent = read("lib", "blog", "milk-analysis-content.ts");
const blogIndex = read("lib", "blog", "blog-index-content.ts");

// Milk article -> /hashvaot/milk-comparison
check(
  "Milk article imports MILK_COMPARISON_HREF",
  milkArticle.includes("MILK_COMPARISON_HREF")
);
const milkHrefMatch = milkContent.match(/MILK_COMPARISON_HREF\s*=\s*"([^"]+)"/);
if (milkHrefMatch) {
  check(
    `MILK_COMPARISON_HREF route exists (${milkHrefMatch[1]})`,
    routeExists(milkHrefMatch[1])
  );
}

// Bread articles -> /hashvaot/bread (not the old broken /comparisons/bread)
check(
  "Bread articles ctaHref is not the broken /comparisons/bread",
  !breadContent.includes('ctaHref: "/comparisons/bread"')
);
const breadHrefMatch = breadContent.match(/BREAD_COMPARISON_HREF\s*=\s*"([^"]+)"/);
if (breadHrefMatch) {
  check(
    `BREAD_COMPARISON_HREF route exists (${breadHrefMatch[1]})`,
    routeExists(breadHrefMatch[1])
  );
} else {
  // ctaHref is a literal: confirm it resolves
  const literalMatch = breadContent.match(/ctaHref:\s*"([^"]+)"/);
  if (literalMatch) {
    check(
      `Bread ctaHref route exists (${literalMatch[1]})`,
      routeExists(literalMatch[1])
    );
  }
}

// Blog index comparisons link
const comparisonsHrefMatch = blogIndex.match(/comparisonsHref:\s*"([^"]+)"/);
if (comparisonsHrefMatch) {
  check(
    `Blog index comparisonsHref route exists (${comparisonsHrefMatch[1]})`,
    routeExists(comparisonsHrefMatch[1])
  );
}

// Blog footer back-to-comparisons link is present
check(
  "Blog index footer links to comparisons",
  blogIndex.includes("comparisonsHref")
);

// ── Summary ───────────────────────────────────────────────────────────────────
console.log("\n" + "─".repeat(50));
console.log(`Passed: ${passed}   Failed: ${failed}`);

if (failed > 0) {
  console.error("\nQA validation FAILED.\n");
  process.exit(1);
} else {
  console.log("\nAll checks passed.\n");
}
