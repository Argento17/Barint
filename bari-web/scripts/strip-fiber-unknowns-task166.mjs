#!/usr/bin/env node
// TASK-166 — strip the fiber-only "data unavailable" disclosure from the three dairy
// datasets (yogurts / maadanim / cheese). Fiber is almost never printed on dairy labels,
// so the TASK-163 backfill produced ~110 fiber "unavailable" notes that are pure noise.
// Owner directive: fiber is dropped from these disclosures (explained once in the category
// intro by Content); sugar / energy / fat (and the other label-printed metrics) stay.
//
//   node scripts/strip-fiber-unknowns-task166.mjs --check   # dry run, report only
//   node scripts/strip-fiber-unknowns-task166.mjs           # apply + write
//
// Method: re-derives each product's unknowns line through the SAME shared §2.5 derivation
// (scripts/lib/derive-unknowns.mjs) but with `fiber` EXCLUDED from the field set, then
// surgically rewrites ONLY the existing unknowns array:
//   - fiber-only note  -> the whole "unknowns": [ ... ] block is removed.
//   - sugar+fiber etc. -> the line is rewritten to the fiber-dropped wording (singular).
// Wording stays byte-identical in style to hummus/snacks/bread (same template strings).
//
// Safety: every existing dairy unknowns array is verified to be a single element that
// reproduces deriveUnknownsLine(missing) exactly (checked at runtime). Surgical text edit
// preserves all other formatting / floats / EOL. A parse-and-diff guard asserts the ONLY
// per-product delta is the unknowns field; scores/grades/nutrition are byte-identical by id.

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

// Fields that may legitimately appear in a dairy disclosure. Fiber is intentionally
// excluded for these categories per TASK-166.
const EXCLUDE = new Set(["fiber"]);

function missingExcludingFiber(nutrition) {
  return missingNutritionFields(nutrition).filter((f) => !EXCLUDE.has(f));
}

// Locate a product's "id" inside the products[] array (skip any earlier metadata
// occurrence) by anchoring the search at the "products" key.
function findProductIdPos(raw, id) {
  const prodAnchor = raw.indexOf('"products"');
  const from = prodAnchor === -1 ? 0 : prodAnchor;
  const pos = raw.indexOf(`"${id}"`, from);
  if (pos === -1) throw new Error(`surgical: id ${id} not found in products[] region`);
  return pos;
}

// Match the existing single-element unknowns block belonging to one product. Anchored at
// the product id so we never cross into a neighbour. Captures leading indentation so we
// can remove the whole block (incl. its line) cleanly when the note is dropped.
function findUnknownsBlock(raw, id, expectedLine) {
  const idPos = findProductIdPos(raw, id);
  // "unknowns" : [ \n  <line> \n <indent> ] ,? \n
  const re = /([ \t]*)"unknowns"\s*:\s*\[\r?\n[ \t]*("(?:[^"\\]|\\.)*")\r?\n[ \t]*\](,?)(\r?\n)/g;
  re.lastIndex = idPos;
  const m = re.exec(raw);
  if (!m) throw new Error(`surgical: unknowns block not found for ${id}`);
  const got = JSON.parse(m[2]);
  if (got !== expectedLine)
    throw new Error(`surgical: ${id} unknowns line mismatch.\n  file: ${JSON.stringify(got)}\n  want: ${JSON.stringify(expectedLine)}`);
  return { start: m.index, end: m.index + m[0].length, indent: m[1], comma: m[3], eol: m[4], lineLiteral: m[2] };
}

function rewriteFile(raw, obj) {
  const edits = []; // { start, end, replacement }
  const removedIds = [];
  const rewrittenIds = [];

  for (const p of obj.products || []) {
    const e = p.expansion;
    if (!e || typeof e !== "object") continue;
    const u = e.unknowns;
    if (!Array.isArray(u) || u.length === 0) continue;

    // Validate the existing array is exactly the derivation (incl. fiber) — proves the
    // data is clean and the surgical anchor is safe.
    const fullMissing = missingNutritionFields(e.nutrition);
    const expectedExisting = deriveUnknownsLine(fullMissing);
    if (u.length !== 1 || u[0] !== expectedExisting)
      throw new Error(`precheck: ${p.id} existing unknowns not the canonical single derivation`);

    const newMissing = missingExcludingFiber(e.nutrition);
    const newLine = deriveUnknownsLine(newMissing); // null if nothing left

    if (newLine === u[0]) continue; // no fiber involved — leave untouched

    const block = findUnknownsBlock(raw, p.id, u[0]);

    if (newLine === null) {
      // Remove the whole unknowns block including its line + EOL.
      edits.push({ start: block.start, end: block.end, replacement: "" });
      removedIds.push(p.id);
    } else {
      // Replace only the line literal in place (keeps indentation / brackets / comma / EOL).
      const newLiteral = JSON.stringify(newLine);
      const litStart = raw.indexOf(block.lineLiteral, block.start);
      if (litStart === -1 || litStart >= block.end)
        throw new Error(`surgical: line literal not relocatable for ${p.id}`);
      edits.push({ start: litStart, end: litStart + block.lineLiteral.length, replacement: newLiteral });
      rewrittenIds.push(p.id);
    }
  }

  edits.sort((a, b) => b.start - a.start);
  let text = raw;
  for (const ed of edits) text = text.slice(0, ed.start) + ed.replacement + text.slice(ed.end);
  return { text, removedIds, rewrittenIds };
}

// Verify: parse before/after; for every product, everything except expansion.unknowns is
// byte-identical, and unknowns changed exactly as intended (fiber removed).
function verify(originalObj, newText, removedIds, rewrittenIds) {
  const after = JSON.parse(newText);
  const removed = new Set(removedIds);
  const rewritten = new Set(rewrittenIds);
  const byId = Object.fromEntries((after.products || []).map((p) => [p.id, p]));

  for (const p of originalObj.products || []) {
    const a = byId[p.id];
    if (!a) throw new Error(`verify: product ${p.id} missing after write`);

    // Non-unknowns equality (scores, grades, nutrition, everything else).
    const aClone = JSON.parse(JSON.stringify(a));
    const orig = JSON.parse(JSON.stringify(p));
    if (aClone.expansion) delete aClone.expansion.unknowns;
    if (orig.expansion) delete orig.expansion.unknowns;
    if (JSON.stringify(aClone) !== JSON.stringify(orig))
      throw new Error(`verify: ${p.id} changed beyond unknowns`);

    // unknowns must be fiber-free now, and equal the no-fiber derivation.
    const newMissing = missingExcludingFiber(p.expansion ? p.expansion.nutrition : null);
    const expected = deriveUnknownsLine(newMissing);
    const actual = a.expansion && Array.isArray(a.expansion.unknowns) && a.expansion.unknowns.length
      ? a.expansion.unknowns[0]
      : null;

    if (expected === null) {
      if (actual !== null) throw new Error(`verify: ${p.id} expected unknowns removed, found ${JSON.stringify(actual)}`);
      if (!removed.has(p.id) && Array.isArray(p.expansion?.unknowns) && p.expansion.unknowns.length)
        throw new Error(`verify: ${p.id} should have been recorded as removed`);
    } else {
      if (actual !== expected) throw new Error(`verify: ${p.id} unknowns != no-fiber derivation`);
      if (/סיב/.test(actual)) throw new Error(`verify: ${p.id} still mentions fiber: ${actual}`);
    }
  }
}

function main() {
  const apply = !process.argv.includes("--check");
  console.log(`strip-fiber-unknowns-task166 — ${apply ? "APPLY" : "CHECK (dry run)"}\n`);

  let grandRemoved = 0, grandRewritten = 0, grandRemain = 0;

  for (const fileName of TARGETS) {
    const path = join(DATA_DIR, fileName);
    const raw = readFileSync(path, "utf8");
    const obj = JSON.parse(raw);
    const originalObj = JSON.parse(raw);

    const { text, removedIds, rewrittenIds } = rewriteFile(raw, obj);
    verify(originalObj, text, removedIds, rewrittenIds);

    // Count remaining (non-empty) unknowns after the edit.
    const after = JSON.parse(text);
    let remaining = 0;
    for (const p of after.products || []) {
      const u = p.expansion && p.expansion.unknowns;
      if (Array.isArray(u) && u.length) remaining++;
    }

    grandRemoved += removedIds.length;
    grandRewritten += rewrittenIds.length;
    grandRemain += remaining;

    console.log(
      `  ${apply ? "WRITE" : "WOULD"} ${fileName}\n` +
      `        fiber-only notes removed : ${removedIds.length}\n` +
      `        notes rewritten (fiber dropped, other metrics kept) : ${rewrittenIds.length}\n` +
      `        unknowns remaining (sugar/energy/fat/etc.) : ${remaining}`
    );
    if (apply) writeFileSync(path, text);
  }

  console.log(
    `\ntask166 totals — removed ${grandRemoved}, rewritten ${grandRewritten}, remaining ${grandRemain}` +
    ` across ${TARGETS.length} dataset(s).`
  );
}

main();
