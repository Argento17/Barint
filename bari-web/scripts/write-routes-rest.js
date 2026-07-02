const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
function w(rel, c) {
  const a = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(a), { recursive: true });
  fs.writeFileSync(a, c, "utf8");
  console.log("wrote", rel);
}

// LOAD ROUTE
w("src/app/api/admin/load/route.ts", fs.readFileSync(path.join(__dirname, "load-route.txt"), "utf8"));
w("src/app/api/admin/save/route.ts", fs.readFileSync(path.join(__dirname, "save-route.txt"), "utf8"));
