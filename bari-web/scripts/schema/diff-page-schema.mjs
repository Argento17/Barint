#!/usr/bin/env node
// diff-page-schema — TASK-569
//
// Compares the GENERATED schema (schema/page-output-schema.generated.json, produced
// from src/lib/contracts/comparison-page-contract.ts by generate-page-schema.mjs)
// against the hand-maintained schema
// (../03_operations/page_generator/contract/page_output_schema_v1.json) and prints a
// FULL categorized diff: missing property / extra property / type mismatch /
// required mismatch.
//
// READ-ONLY. Never writes to the hand-maintained schema. This is a diagnostic report
// for the adopting agent/orchestrator — adoption is a separate decision, not made here.
//
//   node scripts/schema/diff-page-schema.mjs

import { readFileSync, existsSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BARI_WEB = resolve(__dirname, "..", "..");
const REPO_ROOT = resolve(BARI_WEB, "..");

const GENERATED_PATH = join(BARI_WEB, "schema", "page-output-schema.generated.json");
const HAND_PATH = join(REPO_ROOT, "03_operations", "page_generator", "contract", "page_output_schema_v1.json");

function load(path, label) {
  if (!existsSync(path)) {
    console.error(`diff-page-schema: ${label} not found at ${path}`);
    process.exit(2);
  }
  return JSON.parse(readFileSync(path, "utf8"));
}

// Resolve a $ref against the schema's own `definitions` map (draft-07, local refs only —
// both schemas here only ever use "#/definitions/<Name>"). Also unwraps the common
// "nullable ref" pattern ts-json-schema-generator emits for `T | null`:
// { anyOf: [{ $ref: "#/definitions/T" }, { type: "null" }] } — without this, a nested
// structural diff into such a property would see no `properties`/`required` at all and
// wrongly report every child key as "extra_in_hand" (false positive, not a real gap).
function resolveRef(schema, node, seen = new Set()) {
  if (!node || typeof node !== "object") return node;
  if (node.$ref && typeof node.$ref === "string") {
    const m = node.$ref.match(/^#\/definitions\/(.+)$/);
    if (m && schema.definitions && schema.definitions[m[1]] && !seen.has(m[1])) {
      const next = new Set(seen);
      next.add(m[1]);
      return resolveRef(schema, schema.definitions[m[1]], next);
    }
  }
  const branches = node.anyOf || node.oneOf;
  if (Array.isArray(branches)) {
    const withShape = branches.find((b) => b && (b.$ref || b.properties));
    if (withShape) return resolveRef(schema, withShape, seen);
  }
  return node;
}

// Computes the resolved primitive-type set for a property, following $ref/anyOf/oneOf so
// e.g. a nullable-ref-to-enum (`grade: RawGrade | null`) compares as {string,null} against
// a hand-schema `["string","null"]` leaf instead of the meaningless {ref,null}.
function typeSetOf(schema, node) {
  if (!node) return new Set();
  if (node.$ref) return typeSetOf(schema, resolveRef(schema, node));
  if (Array.isArray(node.type)) return new Set(node.type);
  if (typeof node.type === "string") return new Set([node.type]);
  if (Array.isArray(node.anyOf) || Array.isArray(node.oneOf)) {
    const branches = node.anyOf || node.oneOf;
    const out = new Set();
    for (const b of branches) {
      for (const t of typeSetOf(schema, b)) out.add(t);
    }
    return out;
  }
  if (node.enum) return new Set(["string"]); // both schemas only ever enum over strings here
  if (node.properties || node.additionalProperties !== undefined) return new Set(["object"]);
  return new Set();
}

// Walk two "object" schema nodes (already $ref-resolved) and emit categorized findings.
function diffObjectNode(schema, path, genNode, handNode, findings) {
  const gen = resolveRef(schema.gen, genNode);
  const hand = resolveRef(schema.hand, handNode);

  const genProps = gen.properties || {};
  const handProps = hand.properties || {};
  const genRequired = new Set(gen.required || []);
  const handRequired = new Set(hand.required || []);

  const allKeys = new Set([...Object.keys(genProps), ...Object.keys(handProps)]);

  for (const key of [...allKeys].sort()) {
    const p = path ? `${path}.${key}` : key;
    const inGen = key in genProps;
    const inHand = key in handProps;

    if (inGen && !inHand) {
      findings.missing_in_hand.push({ path: p, note: "generated has it, hand-maintained schema does not" });
      continue;
    }
    if (!inGen && inHand) {
      findings.extra_in_hand.push({ path: p, note: "hand-maintained schema has it, generated (TS contract) does not" });
      continue;
    }

    // Both have it — compare required-ness and type.
    const genReq = genRequired.has(key);
    const handReq = handRequired.has(key);
    if (genReq !== handReq) {
      findings.required_mismatch.push({
        path: p,
        generated: genReq ? "required" : "optional",
        hand: handReq ? "required" : "optional",
      });
    }

    const genType = typeSetOf(schema.gen, genProps[key]);
    const handType = typeSetOf(schema.hand, handProps[key]);
    const genSorted = [...genType].sort().join("|");
    const handSorted = [...handType].sort().join("|");
    if (genSorted !== handSorted && genSorted !== "" && handSorted !== "") {
      findings.type_mismatch.push({ path: p, generated: genSorted || "(unresolved)", hand: handSorted || "(unresolved)" });
    }
  }
}

function main() {
  const generated = load(GENERATED_PATH, "generated schema");
  const hand = load(HAND_PATH, "hand-maintained schema");

  const findings = {
    missing_in_hand: [], // generated declares it; hand schema doesn't (hand is stale / lagging)
    extra_in_hand: [], // hand schema declares it; generated (TS contract) doesn't (hand has dead/unverified fields)
    type_mismatch: [],
    required_mismatch: [],
  };

  const schema = { gen: generated, hand };

  // Top level.
  diffObjectNode(schema, "", generated, hand, findings);

  // products[] (both schemas expose `products.items` as an object/$ref to the per-product def).
  const genProductsItems = generated.properties.products.items;
  const handProductsItems = hand.properties.products.items;
  diffObjectNode(schema, "products[]", genProductsItems, handProductsItems, findings);

  // expansion — resolve products[].properties.expansion in each.
  const genProduct = resolveRef(generated, genProductsItems);
  const handProduct = resolveRef(hand, handProductsItems);
  if (genProduct.properties.expansion && handProduct.properties.expansion) {
    diffObjectNode(schema, "products[].expansion", genProduct.properties.expansion, handProduct.properties.expansion, findings);
  }

  // d4_additives[] entries.
  if (genProduct.properties.d4_additives && handProduct.properties.d4_additives) {
    diffObjectNode(
      schema,
      "products[].d4_additives[]",
      genProduct.properties.d4_additives.items,
      handProduct.properties.d4_additives.items,
      findings
    );
  }

  // glassBox.
  if (genProduct.properties.glassBox && handProduct.properties.glassBox) {
    diffObjectNode(schema, "products[].glassBox", genProduct.properties.glassBox, handProduct.properties.glassBox, findings);
  }

  // metrics.
  if (genProduct.properties.metrics && handProduct.properties.metrics) {
    diffObjectNode(schema, "products[].metrics", genProduct.properties.metrics, handProduct.properties.metrics, findings);
  }

  // d3_processing_signal.
  if (genProduct.properties.d3_processing_signal && handProduct.properties.d3_processing_signal) {
    diffObjectNode(
      schema,
      "products[].d3_processing_signal",
      genProduct.properties.d3_processing_signal,
      handProduct.properties.d3_processing_signal,
      findings
    );
  }

  // nutrition.
  const genExpansion = resolveRef(generated, genProduct.properties.expansion);
  const handExpansion = resolveRef(hand, handProduct.properties.expansion);
  if (genExpansion.properties.nutrition && handExpansion.properties.nutrition) {
    diffObjectNode(schema, "products[].expansion.nutrition", genExpansion.properties.nutrition, handExpansion.properties.nutrition, findings);
  }

  // _meta.
  diffObjectNode(schema, "_meta", generated.properties._meta, hand.properties._meta, findings);

  // Report.
  const total =
    findings.missing_in_hand.length + findings.extra_in_hand.length + findings.type_mismatch.length + findings.required_mismatch.length;

  console.log("=".repeat(78));
  console.log("TASK-569 — Generated vs hand-maintained schema diff");
  console.log(`  generated: ${GENERATED_PATH}`);
  console.log(`  hand-maintained: ${HAND_PATH}`);
  console.log("=".repeat(78));

  for (const [cat, label] of [
    ["missing_in_hand", "MISSING PROPERTY (in generated, absent from hand-maintained schema — hand schema is lagging)"],
    ["extra_in_hand", "EXTRA PROPERTY (in hand-maintained schema, absent/dead in generated TS contract)"],
    ["type_mismatch", "TYPE MISMATCH"],
    ["required_mismatch", "REQUIRED/OPTIONAL MISMATCH"],
  ]) {
    console.log(`\n--- ${label}: ${findings[cat].length} ---`);
    for (const f of findings[cat]) {
      if (cat === "type_mismatch") {
        console.log(`  ${f.path}: generated=[${f.generated}] hand=[${f.hand}]`);
      } else if (cat === "required_mismatch") {
        console.log(`  ${f.path}: generated=${f.generated} hand=${f.hand}`);
      } else {
        console.log(`  ${f.path}  (${f.note})`);
      }
    }
  }

  console.log(`\nTOTAL DIFFERENCES: ${total}`);
  console.log(`  missing_in_hand=${findings.missing_in_hand.length} extra_in_hand=${findings.extra_in_hand.length} type_mismatch=${findings.type_mismatch.length} required_mismatch=${findings.required_mismatch.length}`);

  // Write machine-readable copy alongside for the return artifact.
  const outPath = join(BARI_WEB, "schema", "schema-diff-report.json");
  writeFileSync(outPath, JSON.stringify({ total, ...findings }, null, 2));
  console.log(`\nWrote machine-readable report: ${outPath}`);
}

main();
