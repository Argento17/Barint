const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const src = fs.readFileSync(path.join(ROOT, "src/app/admin/page.tsx"), "utf8");
// If already has section tabs, skip
if (src.includes("AdminSectionTab")) {
  console.log("admin page already updated");
  process.exit(0);
}
