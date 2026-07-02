const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
function patch(rel, fn) {
  const abs = path.join(ROOT, rel);
  const t = fs.readFileSync(abs, "utf8");
  const n = fn(t);
  if (n !== t) fs.writeFileSync(abs, n, "utf8");
}
patch("src/lib/admin/github.ts", (t) => t.replace(
  "export interface FetchedFile {\n  data: Record<string, unknown>;\n  sha: string;\n}",
  `export interface FetchedFile {\n  data: {\n    _meta?: Record<string, unknown>;\n    products?: Record<string, unknown>[];\n    [key: string]: unknown;\n  };\n  sha: string;\n}`,
));
patch("src/app/api/admin/load/route.ts", (t) => t.replace(
  "const meta = data._meta ?? {};",
  "const meta = (data._meta ?? {}) as Record<string, unknown>;",
));
patch("src/app/api/admin/categories/route.ts", (t) => t.replace(
  "const meta = data._meta ?? {};",
  "const meta = (data._meta ?? {}) as Record<string, unknown>;",
));
console.log("patched types");
