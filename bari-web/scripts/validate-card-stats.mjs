#!/usr/bin/env node
// validate-card-stats — TASK-568 parity fixture.
//
// For each pilot /hashvaot featured-card category, re-derives ComparisonCardStats
// straight from the raw frontend JSON (same file the actual comparison page reads) and
// prints the result. Any card that reads `deriveComparisonCardStats(xProducts, ...)` from
// the shared module (src/lib/derived/comparison-card-stats.ts) is, by construction, always
// in parity with this script's output — there is no second computation to drift.
//
// This is intentionally the same "read JSON, exit-coded" shape as validate-corpus.mjs
// (this repo's existing non-browser data gate) rather than a new test-runner dependency.
//
// Usage:
//   node scripts/validate-card-stats.mjs            # all pilot categories
//   node scripts/validate-card-stats.mjs cheese      # one category by id
//
// TODO (next hardening step, out of TASK-568 pilot scope): also statically grep each
// card's .tsx source for a literal number in a `stats={[...]}` block that disagrees with
// the value this script derives, so an un-converted card (one that still hand-types a
// stat instead of calling deriveComparisonCardStats) fails the gate instead of silently
// drifting. The manifest below is what that hardening would iterate over.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..");
const DATA_DIR = join(REPO, "src", "data", "comparisons");

// Import the actual shared derivation module — not a reimplementation. Explicit ".ts"
// extension because plain Node's ESM loader requires a full specifier (see the import
// note in comparison-card-stats.ts for why that file has no further relative imports).
const { deriveComparisonCardStats } = await import(
  "../src/lib/derived/comparison-card-stats.ts"
);

// Pilot manifest — the 3 cards converted in TASK-568 Phase 2. Extend as more cards
// convert to the shared module.
const PILOT_CATEGORIES = [
  { id: "cheese", jsonFile: "cheese_frontend_v4.json" },
  { id: "protein_bars", jsonFile: "protein_combined_frontend_v2.json" },
  { id: "granola", jsonFile: "granola_frontend_v2.json" },
];

function loadRawCorpus(jsonFile) {
  const raw = JSON.parse(readFileSync(join(DATA_DIR, jsonFile), "utf8"));
  if (!Array.isArray(raw.products)) {
    throw new Error(`${jsonFile}: missing products[] array`);
  }
  if (!raw._meta || typeof raw._meta.generated !== "string") {
    throw new Error(`${jsonFile}: missing _meta.generated`);
  }
  return raw;
}

function main() {
  const filterArg = process.argv[2];
  const categories = filterArg
    ? PILOT_CATEGORIES.filter((c) => c.id === filterArg)
    : PILOT_CATEGORIES;

  if (filterArg && categories.length === 0) {
    console.error(`Unknown category id "${filterArg}". Known: ${PILOT_CATEGORIES.map((c) => c.id).join(", ")}`);
    process.exit(1);
  }

  let hadError = false;

  for (const category of categories) {
    try {
      const raw = loadRawCorpus(category.jsonFile);
      const stats = deriveComparisonCardStats(raw.products, raw._meta.generated);
      console.log(`[${category.id}] ${category.jsonFile}`);
      console.log(`  productCount=${stats.productCount} scoredCount=${stats.scoredCount}`);
      console.log(
        `  gradeCounts=${JSON.stringify(stats.gradeCounts)} ceilingGrade=${stats.ceilingGrade}`
      );
      console.log(
        `  scoreLow=${stats.scoreLow} scoreHigh=${stats.scoreHigh} scoreSpread=${stats.scoreSpread}`
      );
      console.log(`  updatedLabel="${stats.updatedLabel}"`);
    } catch (err) {
      hadError = true;
      console.error(`[${category.id}] FAILED: ${err.message}`);
    }
  }

  process.exit(hadError ? 1 : 0);
}

main();
