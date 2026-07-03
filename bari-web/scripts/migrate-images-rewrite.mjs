// TASK-478 Phase A — rewrite data files: retailer image URL → self-hosted /products/*.webp.
// Reads scripts/.image-migration-map.json (url → local path) produced by the fetch step,
// replaces every mapped URL verbatim across the frontend data files, and verifies that no
// migrated (optimizer-incompatible) host remains. Run from bari-web/: node scripts/migrate-images-rewrite.mjs

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const MAP = JSON.parse(fs.readFileSync(path.join(ROOT, "scripts", ".image-migration-map.json"), "utf8"));
const PHASE_A_HOST =
  /https?:\/\/(?:[\w.-]+\.)?(?:yochananof\.co\.il|vitamins4all\.co\.il|teva-call\.co\.il|solgar\.co\.il|biogaya\.co\.il|altman\.co\.il|tinc\.co\.il)/gi;

const DATA_DIRS = ["src/data", "src/data/comparisons", "src/lib/comparisons"];
const files = [];
for (const d of DATA_DIRS) {
  const abs = path.join(ROOT, d);
  if (!fs.existsSync(abs)) continue;
  for (const f of fs.readdirSync(abs)) if (/\.(json|ts)$/.test(f)) files.push(path.join(abs, f));
}

const mapped = Object.entries(MAP).filter(([, v]) => v); // skip discards (null)
let totalReplacements = 0;
const perFile = {};

for (const file of files) {
  let txt = fs.readFileSync(file, "utf8");
  const orig = txt;
  let n = 0;
  for (const [url, local] of mapped) {
    if (txt.includes(url)) {
      const parts = txt.split(url);
      n += parts.length - 1;
      txt = parts.join(local);
    }
  }
  // A source URL may have carried a trailing query (cache-buster or a third party's own
  // optimizer params like &w=256&q=75) that the map key did not include. A local /public
  // src must NOT have a query string (next/image rejects it → 500). Strip any residue.
  txt = txt.replace(/(\/products\/[A-Za-z0-9_.-]+\.webp)[?&][^"'\s\\)]*/g, "$1");
  if (txt !== orig) {
    fs.writeFileSync(file, txt);
    perFile[path.basename(file)] = n;
    totalReplacements += n;
  }
}

console.log("Rewrites per file:", perFile);
console.log("Total URL replacements:", totalReplacements);

// Verify: no optimizer-incompatible host should survive in the data files.
let remaining = 0;
for (const file of files) {
  const txt = fs.readFileSync(file, "utf8");
  const hits = txt.match(PHASE_A_HOST);
  if (hits) {
    remaining += hits.length;
    console.log(`  ⚠ ${path.basename(file)} still has ${hits.length} retailer-host ref(s): ${hits[0].slice(0, 70)}`);
  }
}
if (remaining === 0) console.log("✓ Verified: no optimizer-incompatible retailer image hosts remain.");
else {
  console.log(`✗ ${remaining} retailer-host reference(s) remain — investigate before shipping.`);
  process.exit(1);
}
