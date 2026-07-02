const fs = require("fs");
const p = "src/lib/seo/public-corpus-registry.ts";
let t = fs.readFileSync(p, "utf8");
t = t.replace('import type { ComparisonCorpusRaw } from "@/lib/comparisons/corpus";\n\n', "");
t = t.replace(/as ComparisonCorpusRaw/g, "as Record<string, unknown>");
t = t.replace(
  "const CORPUS_BY_SLUG: Record<string, ComparisonCorpusRaw>",
  "const CORPUS_BY_SLUG: Record<string, Record<string, unknown>>"
);
t = t.replace(
  "export function getCorpusBySlug(slug: string): ComparisonCorpusRaw | null",
  "export function getCorpusBySlug(slug: string): Record<string, unknown> | null"
);
t = t.replace(
  /const product = corpus\.products\.find\(\(p\) => p\.id === productId\);/,
  "const products = corpus.products as Array<{ id: string }>;\n  const product = products.find((p) => p.id === productId);"
);
fs.writeFileSync(p, t, "utf8");
console.log("fixed registry");
