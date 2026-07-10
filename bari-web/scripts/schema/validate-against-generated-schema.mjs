#!/usr/bin/env node
// validate-against-generated-schema — TASK-569
//
// Validates every LIVE comparison dataset (the highest-version *_frontend_v*.json per
// category, imported by a page-data.ts module — see liveDatasetFiles()) against the
// GENERATED schema (schema/page-output-schema.generated.json, produced from
// src/lib/contracts/comparison-page-contract.ts). Reports pass/fail per shelf.
//
// This is the sanity gate for step 4 of TASK-569: if the generated schema fails a shelf
// the CURRENT hand-maintained schema passes, the TS contract is wrong — fix the type,
// not the data (never touch src/data/comparisons/*.json from this script or task).
//
//   node scripts/schema/validate-against-generated-schema.mjs

import Ajv from "ajv";
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BARI_WEB = resolve(__dirname, "..", "..");
const DATA_DIR = join(BARI_WEB, "src", "data", "comparisons");
const PAGE_DATA_DIR = join(BARI_WEB, "src", "lib", "comparisons");
const GENERATED_SCHEMA_PATH = join(BARI_WEB, "schema", "page-output-schema.generated.json");

// Scan page-data modules + a couple of known direct importers for
// `@/data/comparisons/<file>.json` — those datasets are the LIVE, served ones.
function liveDatasetFiles() {
  const live = new Map(); // filename -> [importer, ...]
  const re = /@\/data\/comparisons\/([\w.-]+\.json)/g;
  const dirsToScan = [PAGE_DATA_DIR, join(BARI_WEB, "src", "lib", "seo"), join(BARI_WEB, "src", "lib", "home"), join(BARI_WEB, "src", "lib", "guides")];
  for (const dir of dirsToScan) {
    let files;
    try {
      files = readdirSync(dir);
    } catch {
      continue;
    }
    for (const f of files) {
      if (!f.endsWith(".ts")) continue;
      const src = readFileSync(join(dir, f), "utf8");
      let m;
      while ((m = re.exec(src)) !== null) {
        if (!live.has(m[1])) live.set(m[1], []);
        live.get(m[1]).push(f);
      }
    }
  }
  return live;
}

function main() {
  const schema = JSON.parse(readFileSync(GENERATED_SCHEMA_PATH, "utf8"));
  const ajv = new Ajv({ allErrors: true, strict: false });
  const validate = ajv.compile(schema);

  const live = liveDatasetFiles();
  // One entry per category stem — prefer the highest version among files actually
  // imported (page-data.ts modules import exactly one version per stem; take that one).
  const byStem = new Map();
  for (const [file, importers] of live) {
    const stem = file.replace(/_frontend_v\d+\.json$/, "");
    if (!byStem.has(stem)) byStem.set(stem, { file, importers });
  }

  console.log("=".repeat(78));
  console.log(`TASK-569 — validating ${byStem.size} live comparison datasets against generated schema`);
  console.log(`  schema: ${GENERATED_SCHEMA_PATH}`);
  console.log("=".repeat(78));

  const rows = [];
  let failCount = 0;

  for (const [stem, { file }] of [...byStem.entries()].sort()) {
    const path = join(DATA_DIR, file);
    let data;
    try {
      data = JSON.parse(readFileSync(path, "utf8"));
    } catch (e) {
      rows.push({ stem, file, status: "FAIL", errors: [`unreadable JSON: ${e.message}`] });
      failCount++;
      continue;
    }
    const valid = validate(data);
    const productCount = Array.isArray(data.products) ? data.products.length : 0;
    if (valid) {
      rows.push({ stem, file, status: "PASS", productCount, errors: [] });
    } else {
      failCount++;
      // De-duplicate by instancePath shape (drop the numeric product index) so 50
      // identical per-product errors collapse into one line with a count.
      const grouped = new Map();
      for (const err of validate.errors) {
        const genericPath = err.instancePath.replace(/\/products\/\d+/, "/products/*");
        const key = `${genericPath} ${err.keyword} ${err.message}`;
        if (!grouped.has(key)) grouped.set(key, { ...err, instancePath: genericPath, count: 0, sampleParams: err.params });
        grouped.get(key).count++;
      }
      rows.push({ stem, file, status: "FAIL", productCount, errors: [...grouped.values()] });
    }
  }

  for (const r of rows) {
    console.log(`\n  ${r.status}  ${r.stem}  (${r.file})  [${r.productCount ?? "?"} products, imported by ${importers_of(live, r.file)}]`);
    if (r.status === "FAIL") {
      for (const e of r.errors.slice(0, 15)) {
        const countNote = e.count > 1 ? `  (x${e.count})` : "";
        console.log(`      ${e.instancePath || "(root)"}: ${e.message}${countNote}`);
      }
      if (r.errors.length > 15) console.log(`      … +${r.errors.length - 15} more distinct error(s)`);
    }
  }

  function importers_of(liveMap, file) {
    return (liveMap.get(file) || []).join(", ");
  }

  console.log("\n" + "=".repeat(78));
  console.log(`SUMMARY: ${rows.length - failCount}/${rows.length} shelves PASS, ${failCount}/${rows.length} FAIL`);
  console.log("=".repeat(78));

  const outPath = join(BARI_WEB, "schema", "validation-report.json");
  writeFileSync(outPath, JSON.stringify({ total: rows.length, pass: rows.length - failCount, fail: failCount, rows }, null, 2));
  console.log(`Wrote machine-readable report: ${outPath}`);
  process.exit(failCount > 0 ? 1 : 0);
}

main();
