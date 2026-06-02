#!/usr/bin/env node
// normalize-corpus-unknowns — applies the single §2.5 fix (derive-unknowns.mjs) to the
// live comparison datasets (TASK-130D). Idempotent. Scored-only. Never overwrites
// existing unknowns. No score or other-content changes.
//
//   node scripts/normalize-corpus-unknowns.mjs --check   # dry run, report only
//   node scripts/normalize-corpus-unknowns.mjs           # apply + write
//
// Diff-safety: each dataset is re-serialized with its own indent / EOL / trailing-newline
// so the ONLY changed lines are the inserted unknowns arrays. Before applying, a faithful-
// serialize guard asserts that re-serializing the UNCHANGED parse reproduces the file byte
// for byte; if it can't, the file is skipped (no risky reformat).

import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { missingNutritionFields, deriveUnknownsLine } from "./lib/derive-unknowns.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..");
const DATA_DIR = join(REPO, "src", "data", "comparisons");
const PAGE_DATA_DIR = join(REPO, "src", "lib", "comparisons");

// Live datasets = imported by a page-data module (skip deprecated orphans).
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

// Surgical text insertion. Inserts an "unknowns" array as the first child of each
// affected product's expansion object, touching nothing else — purely additive, so it
// preserves existing formatting (incl. value-identical trailing-zero floats e.g. 72.0)
// and produces a clean reviewable diff. Returns { text, changedIds }.
function surgicalInsert(raw, obj) {
  const inserts = []; // { at, text }
  const changedIds = [];
  const expandOpenRe = /"expansion"\s*:\s*\{[ \t]*\r?\n/g;

  for (const p of obj.products || []) {
    if (p.score === null || p.score === undefined) continue;
    const e = p.expansion;
    if (!e || typeof e !== "object") continue;
    if (Array.isArray(e.unknowns) && e.unknowns.length > 0) continue;
    const missing = missingNutritionFields(e.nutrition);
    if (missing.length === 0) continue;

    const idPos = raw.indexOf(`"${p.id}"`);
    if (idPos === -1) throw new Error(`surgical: id ${p.id} not found in raw`);
    expandOpenRe.lastIndex = idPos;
    const m = expandOpenRe.exec(raw);
    if (!m) throw new Error(`surgical: expansion open not found for ${p.id}`);
    const insertAt = m.index + m[0].length; // right after "expansion": {\r\n

    // child indent = whitespace at start of the next line (the first expansion child)
    const childIndentMatch = raw.slice(insertAt).match(/^([ \t]+)/);
    const childIndent = childIndentMatch ? childIndentMatch[1] : "        ";
    const unit = "  ";
    const eol = m[0].includes("\r\n") ? "\r\n" : "\n";
    const line = deriveUnknownsLine(missing);
    const text =
      `${childIndent}"unknowns": [${eol}` +
      `${childIndent}${unit}${JSON.stringify(line)}${eol}` +
      `${childIndent}],${eol}`;
    inserts.push({ at: insertAt, text });
    changedIds.push(p.id);
  }

  // apply from last to first so offsets stay valid
  inserts.sort((a, b) => b.at - a.at);
  let text = raw;
  for (const ins of inserts) text = text.slice(0, ins.at) + ins.text + text.slice(ins.at);
  return { text, changedIds };
}

// Verify a written file: parses, and stripping unknowns from the changed products
// reproduces the original object exactly (no score/other-field drift).
function verifyAgainstOriginal(originalObj, newText, changedIds) {
  const after = JSON.parse(newText);
  const changed = new Set(changedIds);
  const byId = Object.fromEntries((after.products || []).map((p) => [p.id, p]));
  for (const p of originalObj.products || []) {
    const a = byId[p.id];
    if (!a) throw new Error(`verify: product ${p.id} missing after write`);
    const aClone = JSON.parse(JSON.stringify(a));
    if (changed.has(p.id)) {
      // the only allowed delta is a newly-added unknowns array
      if (!Array.isArray(aClone.expansion.unknowns) || aClone.expansion.unknowns.length === 0)
        throw new Error(`verify: ${p.id} expected unknowns added`);
      delete aClone.expansion.unknowns;
      const orig = JSON.parse(JSON.stringify(p));
      delete orig.expansion.unknowns;
      if (JSON.stringify(aClone) !== JSON.stringify(orig))
        throw new Error(`verify: ${p.id} changed beyond unknowns`);
    } else {
      if (JSON.stringify(aClone) !== JSON.stringify(p))
        throw new Error(`verify: unaffected product ${p.id} changed`);
    }
  }
}

function main() {
  const apply = !process.argv.includes("--check");
  const live = liveDatasetFiles();
  const files = readdirSync(DATA_DIR).filter((f) => f.endsWith(".json") && live.has(f));

  console.log(`normalize-corpus-unknowns — ${apply ? "APPLY" : "CHECK (dry run)"}\n`);
  let totalChanged = 0;

  for (const fileName of files.sort()) {
    const path = join(DATA_DIR, fileName);
    const raw = readFileSync(path, "utf8");
    const obj = JSON.parse(raw);

    const originalObj = JSON.parse(raw); // pristine snapshot for verification
    // Single uniform write strategy: surgical text insertion. unknowns is inserted as the
    // first child of each affected product's expansion object — purely additive, never
    // reformats existing lines (preserves value-identical float formatting e.g. 72.0).
    const { text: outText, changedIds } = surgicalInsert(raw, obj);

    const changed = changedIds.length;
    totalChanged += changed;

    if (changed === 0) {
      console.log(`  OK    ${fileName} — 0 products needed unknowns (already compliant)`);
      continue;
    }

    // Always verify before writing: only added unknowns, nothing else moved.
    verifyAgainstOriginal(originalObj, outText, changedIds);

    console.log(`  ${apply ? "WRITE" : "WOULD"} ${fileName} — +unknowns on ${changed} product(s): ${changedIds.slice(0, 5).join(", ")}${changedIds.length > 5 ? ` … +${changedIds.length - 5}` : ""}`);
    if (apply) writeFileSync(path, outText);
  }

  console.log(`\nnormalize-corpus-unknowns: ${totalChanged} product(s) ${apply ? "updated" : "would be updated"} across ${files.length} live dataset(s)`);
}

main();
