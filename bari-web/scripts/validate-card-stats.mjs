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

// Manifest — every /hashvaot featured card converted to deriveComparisonCardStats.
// TASK-568 pilot: cheese, protein_bars, granola. TASK-579 fan-out: the rest.
// Excluded (not in this manifest, by design — see derived_views_scoping_v1.md and the
// TASK-579 return for the per-card reasons):
//   - magnesium: no JSON `generated` source at all (hand-authored page-data, TASK-578)
//   - bread (featured-bread-intelligence-card-lite.tsx): bespoke BreadProduct shape +
//     scan-funnel stats (scanned/sufficient), not a { score, grade } corpus at all
const PILOT_CATEGORIES = [
  // TASK-579 fix: cheese-page-data.ts actually imports v5 (cheese de-anchor go-live,
  // commit e953c8d6) — v4 is an orphaned dataset version (confirmed via
  // `node scripts/validate-corpus.mjs --all` §4.3 "orphaned dataset versions"). The
  // TASK-568 pilot's manifest entry pointed at the wrong (orphaned) file; v4 and v5
  // happen to carry identical product/grade/count data as of this writing (verified),
  // so no reported number was actually wrong, but the file reference was.
  { id: "cheese", jsonFile: "cheese_frontend_v5.json" },
  { id: "protein_bars", jsonFile: "protein_combined_frontend_v2.json" },
  { id: "granola", jsonFile: "granola_frontend_v2.json" },
  { id: "breakfast_cereals", jsonFile: "cereals_frontend_v2.json" },
  { id: "brined_cheeses", jsonFile: "brined_cheeses_frontend_v2.json" },
  { id: "cakes_hard_cookies", jsonFile: "cakes_hard_cookies_frontend_v1.json" },
  { id: "chocolate_bars", jsonFile: "chocolate_bars_frontend_v1.json" },
  { id: "chocolate_tablets", jsonFile: "chocolate_tablets_frontend_v1.json" },
  { id: "cookies_coffee", jsonFile: "cookies_coffee_frontend_v2.json" },
  { id: "crackers", jsonFile: "crackers_frontend_v1.json" },
  { id: "hard_cheeses", jsonFile: "hard_cheeses_frontend_v4.json" },
  { id: "hummus", jsonFile: "hummus_frontend_v5.json" },
  { id: "juices", jsonFile: "juices_frontend_v3.json" },
  { id: "milk", jsonFile: "milk_frontend_v1.json" },
  { id: "snacks", jsonFile: "snacks_frontend_v5.json" },
  { id: "yogurt_spoonable", jsonFile: "yogurt_spoonable_frontend_v1.json" },
  { id: "yogurt_drinks", jsonFile: "yogurt_drinkable_frontend_v1.json" },
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
