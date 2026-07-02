const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
function w(rel, content) {
  const abs = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, content, "utf8");
  console.log("wrote", rel);
}

w("src/app/api/admin/categories/route.ts", fs.readFileSync(path.join(__dirname, "routes/categories.route.ts"), "utf8"));
w("src/app/api/admin/load/route.ts", fs.readFileSync(path.join(__dirname, "routes/load.route.ts"), "utf8"));
w("src/app/api/admin/save/route.ts", fs.readFileSync(path.join(__dirname, "routes/save.route.ts"), "utf8"));
