const fs = require("fs");
const path = require("path");
let t = fs.readFileSync("scripts/mk-expand.js", "utf8");
const tail = `

require("./write-routes-files.js");
require("./write-routes-rest.js");

const mkBody = fs.readFileSync(__filename, "utf8");
const esm =
  'import fs from "fs";\\n' +
  'import path from "path";\\n' +
  'import { fileURLToPath } from "url";\\n' +
  'const __dirname = path.dirname(fileURLToPath(import.meta.url));\\n' +
  'const ROOT = path.resolve(__dirname, "..");\\n' +
  mkBody.replace(/^const fs[\\s\\S]*?function hx\\(hex\\)[\\s\\S]*?\\n\\n/, "");
fs.writeFileSync(path.join(__dirname, "write-admin-expand.mjs"), esm);
console.log("wrote scripts/write-admin-expand.mjs");
`;
const cut = t.indexOf("require(\"./write-api-routes-only.js\")");
if (cut >= 0) t = t.slice(0, cut);
t += tail;
fs.writeFileSync("scripts/mk-expand.js", t);
