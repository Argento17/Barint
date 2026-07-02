const fs = require("fs");
let t = fs.readFileSync("scripts/mk-expand.js", "utf8");
// Escape template interpolations inside nested route writes (between write("src/app/api/admin/load and write("src/lib/hashvaot"))
const start = t.indexOf('write("src/app/api/admin/categories/route.ts"');
const end = t.indexOf('write("src/lib/hashvaot/hashvaot-categories.ts"');
let chunk = t.slice(start, end);
chunk = chunk.replace(/\$\{/g, "\\${");
t = t.slice(0, start) + chunk + t.slice(end);
fs.writeFileSync("scripts/mk-expand.js", t);
console.log("escaped");
