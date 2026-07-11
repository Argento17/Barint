/**
 * Product Dossier data access (TASK-611 / PD-3, internal-only).
 *
 * SERVER-ONLY: reads from disk via node:fs. Import this only from Server
 * Components (src/app/internal/dossier/**\/page.tsx) — never from a
 * "use client" component. There is no `server-only` package installed in
 * this project; the boundary is enforced by convention + code review, same
 * as the rest of this route tree's fs-reading page.tsx files.
 *
 * Reads ONLY from the gitignored, regenerable cache at
 * src/data/dossiers_generated/ (synced via `npm run sync:dossiers` from the
 * compiler's own gitignored, UNCOMMITTED output — see scripts/sync-dossiers.mjs
 * and 03_operations/product_dossier/build_dossiers.py). Never mutates,
 * never recomputes a score, never writes anything.
 */
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

import type { DossierIndex, DossierIndexRow, ProductDossier } from "./types";

const DATA_ROOT = join(process.cwd(), "src", "data", "dossiers_generated");
const INDEX_PATH = join(DATA_ROOT, "index.json");
const DOSSIERS_DIR = join(DATA_ROOT, "dossiers");

export class DossierDataUnavailableError extends Error {
  constructor() {
    super(
      "No dossier dev data found. Run `npm run sync:dossiers` (see scripts/sync-dossiers.mjs) " +
        "to copy the compiler's sample output into src/data/dossiers_generated/.",
    );
    this.name = "DossierDataUnavailableError";
  }
}

let cachedIndex: DossierIndex | null = null;

/** Loads and caches (per server process) the lightweight list-view index. */
export function loadDossierIndex(): DossierIndex {
  if (cachedIndex) return cachedIndex;
  if (!existsSync(INDEX_PATH)) throw new DossierDataUnavailableError();
  cachedIndex = JSON.parse(readFileSync(INDEX_PATH, "utf-8")) as DossierIndex;
  return cachedIndex;
}

export function dossierDataAvailable(): boolean {
  return existsSync(INDEX_PATH);
}

export function listDossierRows(): DossierIndexRow[] {
  return loadDossierIndex().products;
}

/** Finds the index row for a given key (pid when resolved, else provisional_key). */
export function findDossierRow(key: string): DossierIndexRow | undefined {
  return loadDossierIndex().products.find((row) => row.key === key);
}

/** Loads the full per-product dossier JSON by its index key. */
export function loadDossier(key: string): ProductDossier | null {
  const row = findDossierRow(key);
  if (!row) return null;
  const path = join(DOSSIERS_DIR, row.shelfId, `${key}.json`);
  if (!existsSync(path)) return null;
  return JSON.parse(readFileSync(path, "utf-8")) as ProductDossier;
}
