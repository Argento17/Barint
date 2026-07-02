const fs = require("fs");
const bak = fs.readFileSync("scripts/mk-expand.bak.js", "utf8");
function extract(startMarker, endMarker) {
  const i = bak.indexOf(startMarker);
  const j = bak.indexOf(endMarker, i);
  let chunk = bak.slice(i, j);
  const open = chunk.indexOf("`import");
  const close = chunk.lastIndexOf("`);");
  chunk = chunk.slice(open + 1, close);
  return chunk;
}
const load = extract('write("src/app/api/admin/load/route.ts"', 'write("src/app/api/admin/save/route.ts"');
let save = extract('write("src/app/api/admin/save/route.ts"', 'write("src/lib/hashvaot/hashvaot-categories.ts"');
// fix escaped interpolations in save
save = save.replace(/\\\$\{/g, "${");
fs.writeFileSync("scripts/load-route.txt", load, "utf8");
fs.writeFileSync("scripts/save-route.txt", save, "utf8");
console.log("extracted", load.length, save.length);
