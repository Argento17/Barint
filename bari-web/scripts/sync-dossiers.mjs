#!/usr/bin/env node
// sync-dossiers — TASK-611 (PD-3) dev-data step.
//
// The Product Dossier compiler (03_operations/product_dossier/build_dossiers.py,
// PD-2/TASK-610) lives in the Agent OS tree (C:\Bari), NOT under bari-web/src —
// per CLAUDE.md frontend work never edits pipeline assets under C:\Bari, and
// the reverse holds too: no Next.js source lives outside bari-web/. This script
// is the one-way READ bridge: it copies the compiler's already-generated,
// UNCOMMITTED sample dossiers (03_operations/product_dossier/dossiers_sample/,
// gitignored there too — R-D: never a comparison baseline) into a gitignored
// dir inside bari-web so the internal inspection routes can read them via
// normal Node fs from within the Next.js project boundary.
//
// It also builds a lightweight per-product INDEX (one row per dossier: pid,
// name, shelf, barcode status, layer-4 check statuses, evidence completeness)
// so the corpus list view (/internal/dossier) never has to parse all ~700 full
// dossier JSONs to render a table row.
//
// This script only READS from C:\Bari\03_operations\product_dossier and only
// WRITES under bari-web/src/data/dossiers_generated — it never touches a
// score, a served comparison JSON, or anything outside that boundary.
//
// Usage:
//   node scripts/sync-dossiers.mjs
//   node scripts/sync-dossiers.mjs --source <path-to-dossiers_sample-dir>

import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, ".."); // bari-web/
const AGENT_OS_ROOT = resolve(REPO, ".."); // C:\Bari (bari-web is a subtree of it)

const args = process.argv.slice(2);
const sourceFlagIdx = args.indexOf("--source");
const SOURCE_DIR =
  sourceFlagIdx !== -1 && args[sourceFlagIdx + 1]
    ? resolve(args[sourceFlagIdx + 1])
    : join(AGENT_OS_ROOT, "03_operations", "product_dossier", "dossiers_sample");

const OUT_DIR = join(REPO, "src", "data", "dossiers_generated");
const OUT_DOSSIERS_DIR = join(OUT_DIR, "dossiers");
const OUT_INDEX_PATH = join(OUT_DIR, "index.json");

function fail(msg) {
  console.error(`[sync-dossiers] ${msg}`);
  process.exit(1);
}

if (!existsSync(SOURCE_DIR)) {
  fail(
    `source dir not found: ${SOURCE_DIR}\n` +
      `Generate it first: python 03_operations/product_dossier/build_dossiers.py (run from C:\\Bari)`,
  );
}

// Fresh rebuild every run — this is a derived cache, never hand-edited.
if (existsSync(OUT_DIR)) rmSync(OUT_DIR, { recursive: true, force: true });
mkdirSync(OUT_DOSSIERS_DIR, { recursive: true });

const shelfDirs = readdirSync(SOURCE_DIR).filter((name) => statSync(join(SOURCE_DIR, name)).isDirectory());

const indexRows = [];
let copiedCount = 0;

for (const shelfId of shelfDirs) {
  const shelfPath = join(SOURCE_DIR, shelfId);
  const files = readdirSync(shelfPath).filter((f) => f.endsWith(".json"));

  for (const file of files) {
    const raw = readFileSync(join(shelfPath, file), "utf-8");
    let dossier;
    try {
      dossier = JSON.parse(raw);
    } catch {
      console.warn(`[sync-dossiers] skipping unparsable file: ${shelfId}/${file}`);
      continue;
    }

    const key = file.replace(/\.json$/, "");
    // Mirror the compiler's own on-disk layout (shelf/key.json) so a pid maps
    // 1:1 to a file path; the [pid] route just needs to find the shelf.
    const destShelfDir = join(OUT_DOSSIERS_DIR, shelfId);
    mkdirSync(destShelfDir, { recursive: true });
    writeFileSync(join(destShelfDir, `${key}.json`), JSON.stringify(dossier), "utf-8");
    copiedCount += 1;

    const layer1 = dossier.layer_1 ?? {};
    const layer3 = dossier.layer_3 ?? {};
    const layer4 = dossier.layer_4 ?? {};
    const dataQuality = layer3.data_quality ?? {};
    const publicationRecord = layer3.publication_record ?? {};

    indexRows.push({
      key,
      shelfId,
      pid: layer1.pid ?? null,
      pidStatus: layer1.pid_status ?? "unresolved",
      name: layer1.identity_facts?.name?.value ?? null,
      brand: layer1.identity_facts?.brand?.value ?? null,
      barcodeStatus: layer1.barcode_state?.status ?? "unknown",
      barcodeReason: layer1.barcode_state?.reason ?? null,
      servedBarcode: layer1.barcode_state?.served_barcode_unadjudicated ?? null,
      checks: {
        barcode: layer4.barcode?.status ?? "unknown",
        source_traceability: layer4.source_traceability?.status ?? "unknown",
        calculation: layer4.calculation?.status ?? "unknown",
        publishability: layer4.publishability?.status ?? "unknown",
      },
      evidenceCompleteness: dataQuality.evidence_completeness?.value ?? null,
      evidenceFlagRate: dataQuality.evidence_flag_rate?.value ?? null,
      publishedScore: publicationRecord.score?.value ?? null,
      publishedGrade: publicationRecord.grade?.value ?? null,
    });
  }
}

indexRows.sort((a, b) => (a.shelfId + a.key).localeCompare(b.shelfId + b.key));

writeFileSync(
  OUT_INDEX_PATH,
  JSON.stringify(
    {
      generatedAt: new Date().toISOString(),
      sourceDir: SOURCE_DIR,
      note: "DERIVED cache for /internal/dossier — regenerate via `npm run sync:dossiers`. Never hand-edited, never committed.",
      totalProducts: indexRows.length,
      shelves: shelfDirs.sort(),
      products: indexRows,
    },
    null,
    2,
  ),
  "utf-8",
);

console.log(`[sync-dossiers] copied ${copiedCount} dossiers across ${shelfDirs.length} shelves`);
console.log(`[sync-dossiers] wrote index: ${OUT_INDEX_PATH} (${indexRows.length} rows)`);
