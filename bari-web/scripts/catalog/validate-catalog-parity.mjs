#!/usr/bin/env node

import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, relative, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BARI_WEB = resolve(__dirname, "..", "..");
const COMPARISONS_DIR = join(BARI_WEB, "src", "lib", "comparisons");
const ROUTES_DIR = join(BARI_WEB, "src", "app", "hashvaot");
const REGISTRY_CATEGORIES_DIR = join(COMPARISONS_DIR, "registry", "categories");
const EXCLUDED_ROUTES = new Set([
  "magnesium",
  "supplements",
  "personal-care",
  "raw-foods",
  "supermarket",
]);

function importedFrontendDataset(loaderPath) {
  const source = readFileSync(loaderPath, "utf8");
  const match = source.match(
    /@\/data\/comparisons\/([\w.-]+_frontend_v\d+\.json)/
  );
  return match?.[1] ?? null;
}

function liveComparisonCategories() {
  const loadersByModule = new Map();
  for (const entry of readdirSync(COMPARISONS_DIR, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith(".ts")) continue;
    const dataset = importedFrontendDataset(join(COMPARISONS_DIR, entry.name));
    if (dataset) loadersByModule.set(entry.name.replace(/\.ts$/, ""), dataset);
  }

  const live = new Map();
  for (const entry of readdirSync(ROUTES_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory() || EXCLUDED_ROUTES.has(entry.name)) continue;
    const pagePath = join(ROUTES_DIR, entry.name, "page.tsx");
    let source;
    try {
      source = readFileSync(pagePath, "utf8");
    } catch {
      continue;
    }
    const importPattern = /@\/lib\/comparisons\/([\w.-]+)(?:\.ts)?["']/g;
    let match;
    while ((match = importPattern.exec(source)) !== null) {
      const dataset = loadersByModule.get(match[1]);
      if (dataset) live.set(entry.name, { dataset, loader: `${match[1]}.ts` });
    }
  }
  return live;
}

function registeredCategories() {
  const registered = new Map();
  for (const entry of readdirSync(REGISTRY_CATEGORIES_DIR, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith(".ts")) continue;
    const path = join(REGISTRY_CATEGORIES_DIR, entry.name);
    const source = readFileSync(path, "utf8");
    const match = source.match(/routePath:\s*["']\/hashvaot\/([^"']+)["']/);
    if (match) registered.set(match[1], relative(BARI_WEB, path).replaceAll("\\", "/"));
  }
  return registered;
}

function main() {
  const live = liveComparisonCategories();
  const registered = registeredCategories();
  const missingFromRegistry = [...live.keys()].filter((route) => !registered.has(route)).sort();
  const registeredButDead = [...registered.keys()].filter((route) => !live.has(route)).sort();

  console.log("Catalog/registry parity");
  console.log(`  live product-comparison routes: ${live.size}`);
  console.log(`  registered catalog routes: ${registered.size}`);
  for (const [route, { dataset, loader }] of [...live.entries()].sort()) {
    console.log(`  LIVE  ${route} <- ${loader} <- ${dataset}`);
  }

  if (missingFromRegistry.length > 0) {
    console.error(`MISSING_FROM_REGISTRY: ${missingFromRegistry.join(", ")}`);
  }
  if (registeredButDead.length > 0) {
    console.error(`REGISTERED_BUT_DEAD: ${registeredButDead.join(", ")}`);
  }
  if (missingFromRegistry.length > 0 || registeredButDead.length > 0) process.exit(1);

  console.log("PASS: catalog registry exactly matches the live product-comparison routes.");
}

main();
