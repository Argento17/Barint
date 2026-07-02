const fs = require("fs");
const path = require("path");
for (const f of ["scripts/mk-expand.js", "scripts/write-admin-expand.mjs"]) {
  let t = fs.readFileSync(f, "utf8");
  t = t.replace(/\nconst mkBody = fs[\s\S]*$/m, "\n");
  fs.writeFileSync(f, t, "utf8");
}
console.log("trimmed esm tail");
