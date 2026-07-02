const fs = require("fs");
let t = fs.readFileSync("scripts/mk-expand.js", "utf8");
const cut = t.indexOf('write("src/app/api/admin/categories/route.ts"');
const tail = `

require("./write-api-routes-only.js");
require("./write-admin-page-only.js");

const mk = fs.readFileSync(__filename, "utf8");
const esm = mk
  .replace('const fs = require("fs");', 'import fs from "fs";')
  .replace('const path = require("path");', 'import path from "path";')
  .replace(
    'const ROOT = path.resolve(__dirname, "..");',
    'import { fileURLToPath } from "url";\\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\\nconst ROOT = path.resolve(__dirname, "..");',
  )
  .replace(/\\nrequire\\("\\.\\/write-api-routes-only\\.js\\");[\\s\\S]*$/, "\\n");
fs.writeFileSync(path.join(__dirname, "write-admin-expand.mjs"), esm);
console.log("wrote scripts/write-admin-expand.mjs");
`;
t = t.slice(0, cut) + tail;
fs.writeFileSync("scripts/mk-expand.js", t);
console.log("trimmed mk-expand.js");
