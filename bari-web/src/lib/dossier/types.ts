/**
 * Product Dossier types (TASK-611 / PD-3, internal-only).
 *
 * Mirrors the ACTUAL JSON shape emitted by
 * `03_operations/product_dossier/build_dossiers.py` (PD-2/TASK-610) —
 * not the memo's idealized description. See lib/layer1_identity.py,
 * lib/layer2_evidence.py, lib/layer3_schema.py, lib/layer4_checks.py.
 *
 * This is a SEPARATE namespace from `@/lib/view-models` (BariProductVM).
 * It is never consumer-facing and must never be imported by any canonical
 * comparison component. Layer 3 keeps its three disjoint namespaces
 * (assessment / data_quality / publication_record) exactly as the compiler
 * emits them — this file must never introduce a blended/overall field.
 */

export type CheckStatus = "pass" | "warn" | "fail" | "unknown";

export type BarcodeStatus =
  | "verified"
  | "malformed"
  | "pending_manual_review"
  | "found_but_conflicting"
  | "not_found"
  | "unknown";

export interface IdentityFact<T = unknown> {
  value: T | null;
  source: string | null;
  derivation: string;
}

export interface BarcodeState {
  status: BarcodeStatus;
  reason: string | null;
  served_barcode_unadjudicated: string | null;
}

export interface Layer1Identity {
  pid: string | null;
  pid_status: "resolved" | "unresolved";
  provisional_key: string;
  aliases: string[];
  barcode_state: BarcodeState;
  recovered_gtin: string | null;
  identity_facts: {
    name: IdentityFact<string>;
    brand: IdentityFact<string>;
    package_size: IdentityFact<string>;
    manufacturer: IdentityFact<string>;
    retailer: IdentityFact<string>;
    source_urls: IdentityFact<string[]>;
    last_scrape: IdentityFact<string>;
  };
}

export interface Layer2Cell {
  value: number | string | null;
  raw_source_text: string | null;
  source: string;
  status: "retrieved" | "not_retrieved";
  flags: string[];
  captured_at: string | null;
  content_hash: string | null;
  extraction: { parser_version: string };
}

export type Layer2Evidence = Record<string, Layer2Cell>;

export type MetricAxis = "assessment" | "data_quality" | "publication_record";

export interface Metric<T = unknown> {
  key?: string;
  axis: MetricAxis;
  value: T | null;
  derivation: string;
  inputs?: string[];
  note: string | null;
}

export interface Layer3 {
  assessment: Record<string, Metric>;
  data_quality: Record<string, Metric>;
  publication_record: Record<string, Metric>;
}

export interface Layer4Check {
  name: string;
  status: CheckStatus;
  evidence: string[];
  reason: string | null;
}

export interface Layer4Checks {
  barcode: Layer4Check;
  source_traceability: Layer4Check;
  calculation: Layer4Check;
  publishability: Layer4Check;
}

export interface DossierGeneration {
  generated_at: string;
  compiler_version: string;
  parser_version: string;
  shelf_id: string;
  shelf_config_path: string;
  capture_match_note: string;
}

export interface ProductDossier {
  generation: DossierGeneration;
  layer_1: Layer1Identity;
  layer_2: Layer2Evidence;
  layer_3: Layer3;
  layer_4: Layer4Checks;
}

/** One row of the lightweight list-view index (src/data/dossiers_generated/index.json). */
export interface DossierIndexRow {
  key: string;
  shelfId: string;
  pid: string | null;
  pidStatus: "resolved" | "unresolved";
  name: string | null;
  brand: string | null;
  barcodeStatus: BarcodeStatus;
  barcodeReason: string | null;
  servedBarcode: string | null;
  checks: {
    barcode: CheckStatus;
    source_traceability: CheckStatus;
    calculation: CheckStatus;
    publishability: CheckStatus;
  };
  evidenceCompleteness: number | null;
  evidenceFlagRate: number | null;
  publishedScore: number | null;
  publishedGrade: string | null;
}

export interface DossierIndex {
  generatedAt: string;
  sourceDir: string;
  note: string;
  totalProducts: number;
  shelves: string[];
  products: DossierIndexRow[];
}
