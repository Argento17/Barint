const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const out = path.join(ROOT, "src/app/admin/page.tsx");
const page = fs.readFileSync(out, "utf8");
if (page.includes('type AdminTab = "products"')) {
  console.log("admin already patched");
  process.exit(0);
}
// Write full replacement - read from scripts/admin-page-template.txt if exists
const tpl = path.join(__dirname, "admin-page-template.txt");
if (!fs.existsSync(tpl)) {
  console.error("missing template");
  process.exit(1);
}
fs.writeFileSync(out, fs.readFileSync(tpl, "utf8"), "utf8");
console.log("wrote admin page");
