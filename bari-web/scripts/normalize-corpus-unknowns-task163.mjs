#!/usr/bin/env node
// TASK-163 — scoped backfill of expansion.unknowns[] for yogurts / maadanim / cheese.
//
// Uses the SAME shared §2.5 derivation (scripts/lib/derive-unknowns.mjs) and the SAME
// surgical-text-insertion + verify-against-original strategy as
// scripts/normalize-corpus-unknowns.mjs — but scoped to exactly the three TASK-163
// datasets. The general normalizer currently aborts on a pre-existing bread metadata
// id-collision (an id that appears before the products[] array); that file is out of
// scope here and is deliberately NOT touched.
//
//   node scripts/normalize-corpus-unknowns-task163.mjs --check   # dry run
//   node scripts/normalize-corpus-unknowns-task163.mjs           # apply + write
//
// Additive only: inserts an "unknowns" array as the first child of each affected
// product's expansion object. Touches nothing else (scores, grades, floats, EOL).

import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { missingNutritionFields, deriveUnknownsLine } from "./lib/derive-unknowns.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..");
const DATA_DIR = join(REPO, "src", "data", "comparisons");

const TARGETS = [
  "yogurts_frontend_v2.json",
  "maadanim_frontend_v2.json",
  "cheese_frontend_v1.json",
];

// Locate a product's "id" inside the products[] array (skip any earlier metadata
// occurrence) by anchoring the search at the "products" key.
function findProductIdPos(raw, id) {
  const prodAnchor = raw.indexOf('"products"');
  const from = prodAnchor === -1 ? 0 : prodAnchor;
  const pos = raw.indexOf(`"${id}"`, from);
  if (pos === -1) throw new Error(`surgical: id ${id} not found in products[] region`);
  return pos;
}

function surgicalInsert(raw, obj) {
  const inserts = [];
  const changedIds = [];
  const expandOpenRe = /"expansion"\s*:\s*\{[ \t]*\r?\n/g;

  for (const p of obj.products || []) {
    if (p.score === null || p.score === undefined) continue;
    const e = p.expansion;
    if (!e || typeof e !== "object") continue;
    if (Array.isArray(e.unknowns) && e.unknowns.length > 0) continue;
    const missing = missingNutritionFields(e.nutrition);
    if (missing.length === 0) continue;

    const idPos = findProductIdPos(raw, p.id);
    expandOpenRe.lastIndex = idPos;
    const m = expandOpenRe.exec(raw);
    if (!m) throw new Error(`surgical: expansion open not found for ${p.id}`);
    const insertAt = m.index + m[0].length;

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

  inserts.sort((a, b) => b.at - a.at);
  let text = raw;
  for (const ins of inserts) text = text.slice(0, ins.at) + ins.text + text.slice(ins.at);
  return { text, changedIds };
}

function verifyAgainstOriginal(originalObj, newText, changedIds) {
  const after = JSON.parse(newText);
  const changed = new Set(changedIds);
  const byId = Object.fromEntries((after.products || []).map((p) => [p.id, p]));
  for (const p of originalObj.products || []) {
    const a = byId[p.id];
    if (!a) throw new Error(`verify: product ${p.id} missing after write`);
    const aClone = JSON.parse(JSON.stringify(a));
    if (changed.has(p.id)) {
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
  console.log(`normalize-corpus-unknowns-task163 — ${apply ? "APPLY" : "CHECK (dry run)"}\n`);
  let totalChanged = 0;

  for (const fileName of TARGETS) {
    const path = join(DATA_DIR, fileName);
    const raw = readFileSync(path, "utf8");
    const obj = JSON.parse(raw);
    const originalObj = JSON.parse(raw);

    const { text: outText, changedIds } = surgicalInsert(raw, obj);
    const changed = changedIds.length;
    totalChanged += changed;

    if (changed === 0) {
      console.log(`  OK    ${fileName} — 0 products needed unknowns`);
      continue;
    }
    verifyAgainstOriginal(originalObj, outText, changedIds);
    console.log(`  ${apply ? "WRITE" : "WOULD"} ${fileName} — +unknowns on ${changed} product(s)`);
    if (apply) writeFileSync(path, outText);
  }

  console.log(`\ntask163: ${totalChanged} product(s) ${apply ? "updated" : "would be updated"} across ${TARGETS.length} dataset(s)`);
}

main();
