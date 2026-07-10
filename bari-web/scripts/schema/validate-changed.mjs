#!/usr/bin/env node
// validate-changed — TASK-581
//
// CI entry point for the "changed comparison JSON" schema gate (page_schema_gate.yml).
// Takes explicit file paths as argv (produced by `git diff --name-only` in CI — i.e.
// exactly the comparison JSON files a PR touches, not the whole live set) and
// ajv-validates each against the canonical generated schema
// (schema/page-output-schema.generated.json, produced from
// src/lib/contracts/comparison-page-contract.ts). This is the enforcement backstop for
// "a new/edited shelf cannot ship non-conforming data without CI going red" — unlike
// run_gates.py's hand-rolled minimal validator (used interactively, historically blind
// to anyOf/oneOf unions — see TASK-581 return), ajv is a complete draft-07 validator.
//
//   node scripts/schema/validate-changed.mjs <file1.json> [file2.json ...]
//
// Paths may be relative to the current working directory or absolute. Exits 1 if any
// file fails to parse or fails schema validation; exits 0 (with a note) if given no args
// (mirrors the other changed-files-only CI gates' "nothing to gate" convention).

import Ajv from "ajv";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BARI_WEB = resolve(__dirname, "..", "..");
const GENERATED_SCHEMA_PATH = join(BARI_WEB, "schema", "page-output-schema.generated.json");

function main() {
  const files = process.argv.slice(2);
  if (files.length === 0) {
    console.log("validate-changed: no files given — nothing to gate.");
    process.exit(0);
  }

  if (!existsSync(GENERATED_SCHEMA_PATH)) {
    console.error(`validate-changed: generated schema not found at ${GENERATED_SCHEMA_PATH}. Run 'npm run generate-page-schema' first.`);
    process.exit(2);
  }
  const schema = JSON.parse(readFileSync(GENERATED_SCHEMA_PATH, "utf8"));
  const ajv = new Ajv({ allErrors: true, strict: false });
  const validate = ajv.compile(schema);

  let failCount = 0;
  for (const rawPath of files) {
    const path = resolve(process.cwd(), rawPath);
    let data;
    try {
      data = JSON.parse(readFileSync(path, "utf8"));
    } catch (e) {
      console.error(`FAIL  ${rawPath}  (unreadable/invalid JSON: ${e.message})`);
      failCount++;
      continue;
    }
    const valid = validate(data);
    if (valid) {
      const productCount = Array.isArray(data.products) ? data.products.length : "?";
      console.log(`PASS  ${rawPath}  (${productCount} products)`);
    } else {
      failCount++;
      console.error(`FAIL  ${rawPath}`);
      const grouped = new Map();
      for (const err of validate.errors) {
        const genericPath = err.instancePath.replace(/\/products\/\d+/, "/products/*");
        const key = `${genericPath} ${err.keyword} ${err.message}`;
        if (!grouped.has(key)) grouped.set(key, { ...err, instancePath: genericPath, count: 0 });
        grouped.get(key).count++;
      }
      for (const e of [...grouped.values()].slice(0, 20)) {
        const countNote = e.count > 1 ? `  (x${e.count})` : "";
        console.error(`    ${e.instancePath || "(root)"}: ${e.message}${countNote}`);
      }
      if (grouped.size > 20) console.error(`    … +${grouped.size - 20} more distinct error(s)`);
    }
  }

  console.log(`\n${files.length - failCount}/${files.length} file(s) PASS schema validation.`);
  process.exit(failCount > 0 ? 1 : 0);
}

main();
