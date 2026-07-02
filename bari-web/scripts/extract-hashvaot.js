const fs = require("fs");
const bak = fs.readFileSync("scripts/mk-expand.bak.js", "utf8");
function extract(startMarker, endMarker) {
  const i = bak.indexOf(startMarker);
  const j = bak.indexOf(endMarker, i);
  let chunk = bak.slice(i, j);
  const open = chunk.indexOf("`");
  const close = chunk.lastIndexOf("`);");
  chunk = chunk.slice(open + 1, close);
  return chunk;
}
const cat = extract('write("src/lib/hashvaot/hashvaot-categories.ts"', 'write("src/app/hashvaot/page.tsx"');
const page = extract('write("src/app/hashvaot/page.tsx"', 'const mk = fs.readFileSync');
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
function w(rel, c) {
  fs.mkdirSync(path.dirname(path.join(ROOT, rel)), { recursive: true });
  fs.writeFileSync(path.join(ROOT, rel), c, "utf8");
  console.log("wrote", rel);
}
w("src/lib/hashvaot/hashvaot-categories.ts", cat);
w("src/app/hashvaot/page.tsx", page);
