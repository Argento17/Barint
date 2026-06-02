#!/usr/bin/env node
// validate-corpus — MVP (TASK-130B, enforces category_module_contract_v1.md §2/§3)
//
// Single exit-coded gate over comparison datasets. Validates each dataset against the
// BariProductVM contract and the corpus-validity rules in the Category Module Contract.
//
//   node scripts/validate-corpus.mjs            # validate all datasets (default --all)
//   node scripts/validate-corpus.mjs <id>       # validate one category by id
//   node scripts/validate-corpus.mjs --all
//   node scripts/validate-corpus.mjs <id> --handoff   # handoff gate: failures are ERRORS
//
// Severity model (the MVP risk-R1 mitigation requested by the contract, §6.2 / R1):
//   - A category whose dataset is imported by a live page-data is LIVE. In default mode
//     its contract failures are reported as WARN (non-blocking, exit 0) so already-shipped
//     pages are not broken by a newly-introduced gate.
//   - A category that is NOT wired (orphan/new dataset) is a new handoff: failures are
//     ERRORS (blocking, exit 1).
//   - `--handoff` promotes every failure to ERROR regardless of LIVE status.
//   Structural failures that make a dataset unreadable (bad JSON, missing products[])
//   are always ERRORS.
//
// SHAPE SOURCE OF TRUTH: src/lib/view-models/index.ts (BariProductVM). This MVP encodes
// the runtime schema by hand because the contract is a compile-time TS interface with no
// runtime representation; a future hardening should generate the runtime schema from the
// type so the gate and the UI contract can never disagree (contract §6.5 — see GAPS).

import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..");
const DATA_DIR = join(REPO, "src", "data", "comparisons");
const PAGE_DATA_DIR = join(REPO, "src", "lib", "comparisons");

// ── Contract constants ────────────────────────────────────────────────────────
const GRADES = new Set(["A", "B", "C", "D", "E"]);
const CONFIDENCE = new Set(["verified", "partial", "insufficient"]);
const NUTRITION_FIELDS = ["energyKcal", "protein", "sugar", "fat", "fiber", "sodium"];
const RENDERED_STRING_FIELDS = [
  "insightLine",
  "positiveSignals",
  "limitingFactors",
  "unknowns",
  "caveats",
  "bottomLine",
  "comparisonContext",
];
// Rules that are advisory only — never block, even under --handoff. §2.4v2 (both
// pos+lim) is exemption-gated and the exemption registry is not yet machine-readable
// (contract R2), so it stays a warning until exemptions are declared.
const ALWAYS_WARN = new Set(["§2.4v2"]);
// §2.8 prohibited-vocabulary (heuristic backstop, not the authority — contract R4).
const PROHIBITED_VOCAB = [
  // framework / score-mechanics
  "NOVA", "BSIP", "cap", "floor", "dimension", "weight", "score",
  // health words (Hebrew)
  "בריא", "נקי", "מסוכן",
  // recommendations (Hebrew)
  "מומלץ", "כדאי", "עדיף",
];

// ── Discovery ─────────────────────────────────────────────────────────────────
function listDatasets() {
  return readdirSync(DATA_DIR)
    .filter((f) => f.endsWith(".json"))
    .map((f) => join(DATA_DIR, f));
}

// Scan page-data modules for `@/data/comparisons/<file>.json` imports → those datasets
// are LIVE (imported by a route). Returns Set of dataset filenames.
function liveDatasetFiles() {
  const live = new Set();
  const re = /@\/data\/comparisons\/([\w.-]+\.json)/g;
  for (const f of readdirSync(PAGE_DATA_DIR)) {
    if (!f.endsWith(".ts")) continue;
    const src = readFileSync(join(PAGE_DATA_DIR, f), "utf8");
    let m;
    while ((m = re.exec(src)) !== null) live.add(m[1]);
  }
  return live;
}

// ── Finding helpers ───────────────────────────────────────────────────────────
function makeReporter() {
  const findings = [];
  return {
    findings,
    add(rule, productId, message, value) {
      findings.push({ rule, productId, message, value });
    },
  };
}

// ── Per-dataset validation ──────────────────────────────────────────────────────
function validateDataset(path, fileName) {
  const r = makeReporter();
  let data;
  try {
    data = JSON.parse(readFileSync(path, "utf8"));
  } catch (e) {
    return { fatal: true, findings: [{ rule: "JSON", productId: null, message: `unreadable dataset: ${e.message}` }], meta: {} };
  }

  const meta = data._meta || {};
  const products = Array.isArray(data.products) ? data.products : null;
  if (!products) {
    return { fatal: true, findings: [{ rule: "§2.1", productId: null, message: "missing or non-array products[]" }], meta };
  }

  // ── §2.2 count integrity + duplicate ids ────────────────────────────────────
  if (meta.product_count !== undefined && meta.product_count !== products.length) {
    r.add("§2.2", null, `_meta.product_count (${meta.product_count}) !== products.length (${products.length})`);
  }
  const scoredActual = products.filter((p) => p.score !== null && p.score !== undefined).length;
  if (meta.scored_count !== undefined && meta.scored_count !== scoredActual) {
    r.add("§2.2", null, `_meta.scored_count (${meta.scored_count}) !== count(score!==null) (${scoredActual})`);
  }
  const seen = new Set();
  for (const p of products) {
    if (seen.has(p.id)) r.add("§2.2", p.id, "duplicate id");
    seen.add(p.id);
  }

  // ── §1.3 _meta integrity (id consistency with category) ─────────────────────
  const idFromFile = fileName.replace(/_frontend_v.*\.json$/, "").replace(/\.json$/, "");
  if (meta.category !== undefined && meta.category !== idFromFile) {
    r.add("§1.3", null, `_meta.category (${meta.category}) !== dataset stem id (${idFromFile})`);
  }

  // ── Per-product checks ──────────────────────────────────────────────────────
  for (const p of products) {
    const id = p.id ?? "(no-id)";
    const e = p.expansion;

    // §2.1 schema conformance — required top-level keys + types
    for (const k of ["id", "name", "score", "grade", "insightLine", "confidence", "expansion"]) {
      if (!(k in p)) r.add("§2.1", id, `missing required key '${k}'`);
    }
    if ("imageUrl" in p && p.imageUrl !== null && typeof p.imageUrl !== "string")
      r.add("§2.1", id, "imageUrl must be string|null", p.imageUrl);
    if (p.score !== null && p.score !== undefined &&
        !(Number.isInteger(p.score) && p.score >= 0 && p.score <= 100))
      r.add("§2.1", id, "score must be integer 0-100 or null", p.score);
    if (p.grade !== null && p.grade !== undefined && !GRADES.has(p.grade))
      r.add("§2.1", id, "grade must be A-E or null", p.grade);
    if (!CONFIDENCE.has(p.confidence))
      r.add("§2.1", id, "confidence must be verified|partial|insufficient", p.confidence);
    if (typeof p.insightLine !== "string")
      r.add("§2.1", id, "insightLine must be a string", p.insightLine);
    if (!e || typeof e !== "object")
      r.add("§2.1", id, "expansion object missing");

    // §2.3 scored/grade coherence
    const scored = p.score !== null && p.score !== undefined;
    if (scored && (p.grade === null || p.grade === undefined))
      r.add("§2.3", id, "scored product has null grade (score⇔grade)", p.score);
    if (!scored && p.grade !== null && p.grade !== undefined)
      r.add("§2.3", id, "unscored product carries a grade (score⇔grade)", p.grade);
    if (p.confidence === "insufficient" && (scored || (p.grade !== null && p.grade !== undefined)))
      r.add("§2.3", id, "insufficient ⇒ score and grade must both be null", { score: p.score, grade: p.grade });

    if (!e || typeof e !== "object") continue;

    // §2.4 explanation completeness (the bread gap)
    if (scored) {
      const hasPos = Array.isArray(e.positiveSignals) && e.positiveSignals.length > 0;
      const hasLim = Array.isArray(e.limitingFactors) && e.limitingFactors.length > 0;
      if (p.insightLine === "")
        r.add("§2.4", id, "scored product has empty insightLine");
      if (!hasPos && !hasLim)
        r.add("§2.4", id, "scored product has no positiveSignals and no limitingFactors");
      // §2.4 v2 completeness (both required unless exempt). Reported separately; exemption
      // registry is not yet machine-readable (contract R2), so this is advisory in MVP.
      if (hasPos && !hasLim)
        r.add("§2.4v2", id, "limitingFactors empty (v2 wants both; exemption not verified)");
    }

    // §2.5 unknowns when nutrition data missing (scored products only)
    if (scored && e.nutrition && typeof e.nutrition === "object") {
      const anyNull = NUTRITION_FIELDS.some((f) => e.nutrition[f] === null);
      const hasUnknowns = Array.isArray(e.unknowns) && e.unknowns.length > 0;
      if (anyNull && !hasUnknowns) {
        const missing = NUTRITION_FIELDS.filter((f) => e.nutrition[f] === null);
        r.add("§2.5", id, "nutrition field(s) null but unknowns[] empty", missing.join(","));
      }
    }

    // §2.6 no-score products explicit (never blank/—/N/A)
    if (!scored) {
      const hasCaveat = Array.isArray(e.caveats) && e.caveats.some((s) => s && s.trim() && !["—", "N/A"].includes(s.trim()));
      const hasUnknown = Array.isArray(e.unknowns) && e.unknowns.some((s) => s && s.trim());
      if (!hasCaveat && !hasUnknown)
        r.add("§2.6", id, "no-score product has no caveats[]/unknowns[] explanation");
    }

    // §2.8 prohibited-vocabulary scan (heuristic)
    for (const field of RENDERED_STRING_FIELDS) {
      const v = field === "insightLine" ? p[field] : e[field];
      const strings = typeof v === "string" ? [v] : Array.isArray(v) ? v : [];
      for (const s of strings) {
        for (const term of PROHIBITED_VOCAB) {
          if (typeof s === "string" && s.toLowerCase().includes(term.toLowerCase()))
            r.add("§2.8", id, `prohibited token '${term}' in ${field}`, s);
        }
      }
    }
  }

  // ── §2.7 ordering: scored descending by score, insufficient appended last ────
  let sawNull = false;
  let lastScore = Infinity;
  for (const p of products) {
    const scored = p.score !== null && p.score !== undefined;
    if (!scored) { sawNull = true; continue; }
    if (sawNull) { r.add("§2.7", p.id, "scored product appears after an unscored one"); break; }
    if (p.score > lastScore) { r.add("§2.7", p.id, `out of order: ${p.score} > previous ${lastScore}`); }
    lastScore = p.score;
  }

  return { fatal: false, findings: r.findings, meta };
}

// ── CLI ─────────────────────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  const handoff = args.includes("--handoff");
  const positional = args.filter((a) => !a.startsWith("--"));
  const all = args.includes("--all") || positional.length === 0;
  const targetId = all ? null : positional[0];

  const live = liveDatasetFiles();
  let datasets = listDatasets();

  // Category stems that have a LIVE dataset → used to tell a DEPRECATED orphan (old
  // version of a live category) apart from a NEW un-wired category (handoff candidate).
  const stemOf = (f) => f.replace(/_frontend_v.*\.json$/, "").replace(/\.json$/, "");
  const liveStems = new Set([...live].map(stemOf));

  // Resolve which datasets to validate. For a single id, prefer the LIVE dataset for
  // that id; fall back to any dataset whose stem matches.
  if (targetId) {
    datasets = datasets.filter((p) => {
      const f = p.split(/[\\/]/).pop();
      const stem = f.replace(/_frontend_v.*\.json$/, "").replace(/\.json$/, "");
      return stem === targetId;
    });
    if (datasets.length === 0) {
      console.error(`validate-corpus: no dataset found for id '${targetId}'`);
      process.exit(2);
    }
    // If multiple versions match, validate only the LIVE one (the imported version).
    const liveMatch = datasets.filter((p) => live.has(p.split(/[\\/]/).pop()));
    if (liveMatch.length > 0) datasets = liveMatch;
  }

  let errorCount = 0;
  let warnCount = 0;
  const orphanWarnings = [];

  console.log(`validate-corpus — ${handoff ? "HANDOFF (errors block)" : "DEV (live=warn)"} mode\n`);

  for (const path of datasets) {
    const fileName = path.split(/[\\/]/).pop();
    const isLive = live.has(fileName);
    const isDeprecated = !isLive && liveStems.has(stemOf(fileName));

    // §4.3 orphaned dataset versions: present in data dir, imported by nothing.
    if (!isLive) orphanWarnings.push(fileName);

    // A DEPRECATED orphan (superseded version of a live category) is only a §4.3
    // warning — not a handoff candidate — so we skip deep content validation of it.
    if (isDeprecated) {
      console.log(`  SKIP  ${stemOf(fileName)}  (${fileName}) [deprecated orphan — §4.3 only]`);
      continue;
    }

    const { fatal, findings, meta } = validateDataset(path, fileName);
    const id = meta.category || fileName;

    // Severity: ALWAYS_WARN rules never block. Structural fatals always ERROR. Otherwise
    // ERROR if handoff mode OR the category is a new (un-wired) handoff candidate; a LIVE
    // category's failures are warnings in dev mode (contract R1 mitigation).
    const asError = (rule) => !ALWAYS_WARN.has(rule) && (fatal || handoff || !isLive);

    if (findings.length === 0) {
      console.log(`  PASS  ${id}  (${fileName})${isLive ? " [LIVE]" : " [orphan/new]"}`);
      continue;
    }

    const errs = findings.filter((f) => asError(f.rule));
    const warns = findings.filter((f) => !asError(f.rule));
    errorCount += errs.length;
    warnCount += warns.length;

    const status = errs.length ? "FAIL" : "WARN";
    console.log(`  ${status}  ${id}  (${fileName})${isLive ? " [LIVE]" : " [orphan/new]"}  — ${errs.length} error(s), ${warns.length} warning(s)`);
    // group by rule for readable per-product diagnostics
    const byRule = {};
    for (const f of findings) (byRule[f.rule] ||= []).push(f);
    for (const rule of Object.keys(byRule).sort()) {
      const items = byRule[rule];
      const sev = asError(rule) ? "ERROR" : "warn ";
      const sample = items.slice(0, 8);
      console.log(`      [${sev}] ${rule} — ${items.length} finding(s)`);
      for (const f of sample) {
        const val = f.value !== undefined ? `  (${typeof f.value === "object" ? JSON.stringify(f.value) : f.value})` : "";
        console.log(`         ${f.productId ?? "-"}: ${f.message}${val}`);
      }
      if (items.length > sample.length) console.log(`         … +${items.length - sample.length} more`);
    }
  }

  if (orphanWarnings.length) {
    warnCount += orphanWarnings.length;
    console.log(`\n  [warn ] §4.3 orphaned dataset versions (imported by no live page-data):`);
    for (const f of orphanWarnings) console.log(`         ${f}`);
  }

  console.log(`\nvalidate-corpus: ${errorCount} error(s), ${warnCount} warning(s)`);
  process.exit(errorCount > 0 ? 1 : 0);
}

main();
