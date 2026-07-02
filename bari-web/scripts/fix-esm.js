const fs = require("fs");
const path = require("path");
const mk = fs.readFileSync(path.join(__dirname, "mk-expand.js"), "utf8");
const body = mk.replace(/^[\uFEFF]?const fs = require\("fs"\);\s*const path = require\("path"\);\s*const ROOT[\s\S]*?function hx\(hex\) \{ return Buffer\.from\(hex, "hex"\)\.toString\("utf8"\); \}\s*/m, "");
const esm = [
  'import fs from "fs";',
  'import path from "path";',
  'import { fileURLToPath } from "url";',
  'import { createRequire } from "module";',
  'const require = createRequire(import.meta.url);',
  'const __dirname = path.dirname(fileURLToPath(import.meta.url));',
  'const ROOT = path.resolve(__dirname, "..");',
  'function write(rel, content) {',
  '  const abs = path.join(ROOT, rel);',
  '  fs.mkdirSync(path.dirname(abs), { recursive: true });',
  '  fs.writeFileSync(abs, content, "utf8");',
  '  console.log("wrote", rel);',
  '}',
  'function patch(rel, fn) {',
  '  const abs = path.join(ROOT, rel);',
  '  const before = fs.readFileSync(abs, "utf8");',
  '  const after = fn(before);',
  '  if (after !== before) { fs.writeFileSync(abs, after, "utf8"); console.log("patched", rel); }',
  '}',
  'function hx(hex) { return Buffer.from(hex, "hex").toString("utf8"); }',
  '',
  body.replace(/require\("\.\/write-routes-files\.js"\);\s*require\("\.\/write-routes-rest\.js"\);\s*/g, ""),
  '',
].join("\n");
fs.writeFileSync(path.join(__dirname, "write-admin-expand.mjs"), esm, "utf8");
console.log("fixed write-admin-expand.mjs");
