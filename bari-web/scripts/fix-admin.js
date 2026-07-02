const fs = require("fs");
let t = fs.readFileSync("src/app/admin/page.tsx", "utf8");
const start = t.indexOf("\n          {loaded && (\n            <>");
const end = t.indexOf("{!loaded && !loaded &&");
if (start >= 0 && end > start) {
  t = t.slice(0, start) + "\n          {!loaded &&" + t.slice(end + "{!loaded && !loaded &&".length);
  fs.writeFileSync("src/app/admin/page.tsx", t, "utf8");
  console.log("removed duplicate block");
} else {
  console.log("markers not found", start, end);
}
