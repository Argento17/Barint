#!/usr/bin/env node
// sync-ops-schema — TASK-581
//
// Adoption step: the TS contract (src/lib/contracts/comparison-page-contract.ts) is now
// the single source of truth for the page-output JSON Schema. This script takes the
// generated output (schema/page-output-schema.generated.json, produced by
// `npm run generate-page-schema` from that TS contract) and writes the SAME schema
// content to the ops-consumer path
// (03_operations/page_generator/contract/page_output_schema_v1.json), which
// 03_operations/page_generator/gates/run_gates.py (G1 SCHEMA gate) reads at runtime.
//
// This is a byte-for-byte content sync (title/$id/$comment adjusted to mark the file as
// generated) — there is exactly ONE schema from here on; the ops path is a synced copy,
// never hand-edited. CI's schema-lag-check job (page_schema_gate.yml) runs this same
// script and fails the build if the committed ops file drifts from what regeneration
// produces, which is what actually kills the schema-lag class permanently (TASK-581).
//
//   npm run sync-ops-schema      (assumes schema/page-output-schema.generated.json is fresh —
//                                  run `npm run generate-page-schema` first, or use
//                                  `npm run verify-schema-sync` which chains both)

import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BARI_WEB = resolve(__dirname, "..", "..");
const REPO_ROOT = resolve(BARI_WEB, "..");

const GENERATED_PATH = join(BARI_WEB, "schema", "page-output-schema.generated.json");
const OPS_PATH = join(REPO_ROOT, "03_operations", "page_generator", "contract", "page_output_schema_v1.json");

const GENERATED_NOTICE =
  "GENERATED FILE — DO NOT HAND-EDIT (TASK-581). Source of truth: " +
  "bari-web/src/lib/contracts/comparison-page-contract.ts. Regenerate + resync with " +
  "`npm run verify-schema-sync` from bari-web/ (chains generate-page-schema + sync-ops-schema). " +
  "CI's schema-lag-check job (.github/workflows/page_schema_gate.yml) fails the build if this " +
  "file drifts from what regeneration produces — hand edits will be reverted or will fail CI. " +
  "Consumed at runtime by 03_operations/page_generator/gates/run_gates.py (G1 SCHEMA gate).";

function main() {
  const generated = JSON.parse(readFileSync(GENERATED_PATH, "utf8"));

  // Same schema content (definitions/properties/required/etc. spread verbatim from the
  // generated output) with only the identity/meta keywords overridden so the file reads
  // as a deliberate, generated artifact rather than a stray copy.
  const synced = {
    ...generated,
    $id: "bari-page-output-v1",
    $comment: GENERATED_NOTICE,
    title: "Bari Category Page Output v1 (generated)",
    description:
      "JSON Schema for the RAW served comparison JSON under bari-web/src/data/comparisons/*_frontend_v*.json " +
      "(before the page-data.ts transform runs). Generated from comparison-page-contract.ts — see $comment.",
  };

  writeFileSync(OPS_PATH, JSON.stringify(synced, null, 2) + "\n");
  console.log(`sync-ops-schema: wrote ${OPS_PATH}`);
}

main();
