#!/usr/bin/env node
// reorder-corpus — enforces contract §2.7 ordering on comparison datasets (TASK-130E):
// products ordered scored-descending by score, with insufficient (score === null)
// appended last. Re-sort ONLY — never changes a score, grade, or any product content.
//
//   node scripts/reorder-corpus.mjs <id> [<id> ...]   # e.g. bread snacks
//   node scripts/reorder-corpus.mjs <id> --check       # dry run, report violations only
//
// Stable sort: products with equal scores keep their existing relative order, and the
// insufficient tail keeps its existing order — so the diff is the minimal set of moves.
// Guard: a dataset is only rewritten if it re-serializes byte-faithfully (no formatting
// drift) AND a verification confirms the product multiset and every per-id score are
// unchanged — only sequence differs.

import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..");
const DATA_DIR = join(REPO, "src", "data", "comparisons");
const PAGE_DATA_DIR = join(REPO, "src", "lib", "comparisons");

function liveDatasetFor(id) {
  // find the dataset imported by the live page-data for this id (handles shared corpora)
  const re = /@\/data\/comparisons\/([\w.-]+\.json)/g;
  const stem = (f) => f.replace(/_frontend_v.*\.json$/, "").replace(/\.json$/, "");
  for (const f of readdirSync(PAGE_DATA_DIR)) {
    if (!f.endsWith(".ts")) continue;
    const src = readFileSync(join(PAGE_DATA_DIR, f), "utf8");
    let m;
    while ((m = re.exec(src)) !== null) {
      if (stem(m[1]) === id) return m[1];
    }
  }
  // fallback: any dataset file whose stem matches
  const match = readdirSync(DATA_DIR).find((f) => stem(f) === id);
  return match || null;
}

function serializeLike(obj, raw) {
  const indentMatch = raw.match(/\n(\s+)"/);
  const indent = indentMatch ? indentMatch[1].replace(/\r/g, "").length : 2;
  const eol = raw.includes("\r\n") ? "\r\n" : "\n";
  const trailing = /\n$/.test(raw) || /\r\n$/.test(raw);
  let out = JSON.stringify(obj, null, indent);
  if (eol === "\r\n") out = out.replace(/\n/g, "\r\n");
  if (trailing) out += eol;
  return out;
}

function orderViolations(products) {
  const v = [];
  let last = Infinity;
  let sawNull = false;
  for (const p of products) {
    if (p.score === null || p.score === undefined) { sawNull = true; continue; }
    if (sawNull) v.push(`${p.id}: scored after an insufficient product`);
    if (p.score > last) v.push(`${p.id}: ${p.score} > previous ${last}`);
    last = p.score;
  }
  return v;
}

function main() {
  const args = process.argv.slice(2);
  const check = args.includes("--check");
  const ids = args.filter((a) => !a.startsWith("--"));
  if (ids.length === 0) {
    console.error("usage: reorder-corpus <id> [<id> ...] [--check]");
    process.exit(2);
  }

  console.log(`reorder-corpus — ${check ? "CHECK (dry run)" : "APPLY"}\n`);

  for (const id of ids) {
    const fileName = liveDatasetFor(id);
    if (!fileName) { console.log(`  SKIP  ${id} — no dataset found`); continue; }
    const path = join(DATA_DIR, fileName);
    const raw = readFileSync(path, "utf8");
    const obj = JSON.parse(raw);
    const original = JSON.parse(raw);

    const before = orderViolations(obj.products);

    // stable sort: scored desc, insufficient last (relative order preserved within each)
    const scored = obj.products.filter((p) => p.score !== null && p.score !== undefined);
    const insufficient = obj.products.filter((p) => p.score === null || p.score === undefined);
    scored.sort((a, b) => b.score - a.score);
    obj.products = [...scored, ...insufficient];

    const after = orderViolations(obj.products);

    // ── verification: re-sort only, nothing else ──────────────────────────────
    const sameLen = obj.products.length === original.products.length;
    const idsBefore = original.products.map((p) => p.id).sort();
    const idsAfter = obj.products.map((p) => p.id).sort();
    const sameSet = JSON.stringify(idsBefore) === JSON.stringify(idsAfter);
    const scoreById = Object.fromEntries(original.products.map((p) => [p.id, p.score]));
    const scoresIntact = obj.products.every((p) => scoreById[p.id] === p.score);
    // every product object must be byte-identical to the original (only position changed)
    const origById = Object.fromEntries(original.products.map((p) => [p.id, JSON.stringify(p)]));
    const contentIntact = obj.products.every((p) => origById[p.id] === JSON.stringify(p));

    if (!(sameLen && sameSet && scoresIntact && contentIntact)) {
      console.log(`  ABORT ${id} (${fileName}) — verification failed (would change more than order)`);
      process.exit(1);
    }

    const faithful = serializeLike(original, raw) === raw;
    if (!faithful) {
      console.log(`  ABORT ${id} (${fileName}) — not byte-faithful; refusing to reformat`);
      process.exit(1);
    }

    const moved = obj.products.filter((p, i) => original.products[i].id !== p.id).length;
    console.log(`  ${check ? "WOULD" : "WRITE"} ${id} (${fileName}) — §2.7 violations ${before.length} → ${after.length}; ${moved} product(s) repositioned`);
    if (before.length) for (const b of before) console.log(`        - ${b}`);

    if (!check && before.length > 0) writeFileSync(path, serializeLike(obj, raw));
    else if (!check) console.log(`        (already ordered — no write)`);
  }
}

main();
