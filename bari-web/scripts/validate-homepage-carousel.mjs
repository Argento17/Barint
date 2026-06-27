/**
 * QA validation for homepage carousel data.
 * Checks: unique ids, hrefs, product constraints, alt text, spread/tokens presence.
 */

import { readFileSync } from "fs";
import { fileURLToPath, pathToFileURL } from "url";
import path from "path";
import { createRequire } from "module";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");

// ── Load data via dynamic import (TS compiled to .js via tsx if available) ──
// We read the raw .ts and parse the HOMEPAGE_CAROUSEL_CARDS array by importing
// the compiled JS from next build cache — or fall back to source parse.

let cards;
try {
  // Try to import via tsx (if available)
  const { HOMEPAGE_CAROUSEL_CARDS } = await import(
    pathToFileURL(
      path.resolve(projectRoot, "src/lib/home/homepage-carousel-data.ts")
    ).href
  );
  cards = HOMEPAGE_CAROUSEL_CARDS;
} catch {
  // Fallback: read and eval via node --input-type
  console.error("Could not import TS directly. Run with: node --loader tsx scripts/validate-homepage-carousel.mjs");
  process.exit(1);
}

// ── QA checks ────────────────────────────────────────────────────────────────

let pass = 0;
let fail = 0;

function check(label, ok, detail = "") {
  if (ok) {
    console.log(`  \u2713 ${label}`);
    pass++;
  } else {
    console.error(`  \u2717 ${label}${detail ? ": " + detail : ""}`);
    fail++;
  }
}

console.log("\n=== Bari Homepage Carousel QA ===\n");

// 1. Unique ids
const ids = cards.map((c) => c.id);
const uniqueIds = new Set(ids);
check("All card ids are unique", uniqueIds.size === ids.length,
  ids.length - uniqueIds.size + " duplicate(s)");

// 2. Unique hrefs (warn only — some cards share a page)
const hrefs = cards.map((c) => c.href);
const uniqueHrefs = new Set(hrefs);
console.log(`  i hrefs unique: ${uniqueHrefs.size}/${hrefs.length} (duplicates allowed for same-page cards)`);

// 3. comparison cards have exactly 2 products with productIds
const comparisons = cards.filter((c) => c.type === "comparison");
for (const c of comparisons) {
  check(
    `comparison "${c.id}" has leftProduct.productId`,
    Boolean(c.leftProduct?.productId)
  );
  check(
    `comparison "${c.id}" has rightProduct.productId`,
    Boolean(c.rightProduct?.productId)
  );
  check(
    `comparison "${c.id}" leftProduct != rightProduct id`,
    c.leftProduct?.productId !== c.rightProduct?.productId
  );
}

// 4. category_report cards have scoreSpread, NO product images
const catReports = cards.filter((c) => c.type === "category_report");
for (const c of catReports) {
  check(`category_report "${c.id}" has gradeDistribution`, Boolean(c.gradeDistribution));
  check(
    `category_report "${c.id}" has no leftProduct/rightProduct/spotlightProduct`,
    !c.leftProduct && !c.rightProduct && !c.spotlightProduct
  );
}

// 5. ingredient_investigation has tokens, NO photos
const ingredients = cards.filter((c) => c.type === "ingredient_investigation");
for (const c of ingredients) {
  check(
    `ingredient "${c.id}" has ingredientTokens`,
    Array.isArray(c.ingredientTokens) && c.ingredientTokens.length > 0
  );
  check(
    `ingredient "${c.id}" visualMode is ingredient_mask`,
    c.visualMode === "ingredient_mask"
  );
  check(
    `ingredient "${c.id}" has no product images`,
    !c.leftProduct && !c.rightProduct && !c.spotlightProduct
  );
}

// 6. supplement_report has supplement_molecule visualMode, no external URLs on products
const supplements = cards.filter((c) => c.type === "supplement_report");
for (const c of supplements) {
  check(`supplement "${c.id}" visualMode is supplement_molecule`, c.visualMode === "supplement_molecule");
  check(
    `supplement "${c.id}" has no product image URLs`,
    !c.spotlightProduct?.imageUrl && !c.leftProduct?.imageUrl
  );
}

// 7. product_spotlight has spotlightProduct with productId
const spotlights = cards.filter((c) => c.type === "product_spotlight");
for (const c of spotlights) {
  check(`spotlight "${c.id}" has spotlightProduct.productId`, Boolean(c.spotlightProduct?.productId));
}

// 8. All product imageAlts are non-empty (for verified images)
const allProducts = cards.flatMap((c) =>
  [c.leftProduct, c.rightProduct, c.spotlightProduct].filter(Boolean)
);
for (const p of allProducts) {
  if (p.imageStatus === "verified") {
    check(
      `product "${p.productId}" imageAlt non-empty`,
      Boolean(p.imageAlt && p.imageAlt.trim().length > 0)
    );
  }
}

// 9. No /hashvaot/themes/ photo URLs
for (const c of cards) {
  const raw = JSON.stringify(c);
  check(
    `card "${c.id}" has no /hashvaot/themes/ photo`,
    !raw.includes("/hashvaot/themes/")
  );
}

// 10. Total card count
check("Total cards === 9", cards.length === 9, `got ${cards.length}`);

// ── Summary ───────────────────────────────────────────────────────────────────
console.log(`\n=== Results: ${pass} passed, ${fail} failed ===\n`);
process.exit(fail > 0 ? 1 : 0);
